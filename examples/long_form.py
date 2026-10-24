"""Render a long text file (article, book chapter, podcast script) to one audio file.

    uv run python examples/long_form.py input.txt -o output.wav --voice "Hải Đăng"
    uv run python examples/long_form.py input.txt --ref-audio my_voice.wav --temperature 0.7
    uv run python examples/long_form.py input.txt --voice "Custom Song Ngữ"   # bilingual voice

Paragraphs are synthesized a group at a time and appended to the output file, so
memory stays flat however long the text is, and progress / ETA are printed as it
goes. On CUDA every chunk of a group is batched into the same forward pass.
"""
import argparse
import sys
import time
from pathlib import Path

import numpy as np
import soundfile as sf

from apps.user_voices import load_user_voices
from vieneu import Vieneu
from vieneu_utils.core_utils import V3_GAP_SILENCE, pause_pad_samples


def paragraph_groups(text: str, group_chars: int) -> list[str]:
    """Pack whole paragraphs into groups of about ``group_chars`` characters."""
    groups, current, size = [], [], 0
    for para in (p.strip() for p in text.splitlines()):
        if not para:
            continue
        if current and size + len(para) > group_chars:
            groups.append("\n".join(current))
            current, size = [], 0
        current.append(para)
        size += len(para)
    if current:
        groups.append("\n".join(current))
    return groups


def _fmt(seconds: float) -> str:
    m, s = divmod(int(round(seconds)), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="UTF-8 text file; blank lines / newlines separate paragraphs")
    ap.add_argument("-o", "--output", type=Path, help="output .wav/.flac (default: input name + .wav)")
    ap.add_argument("--voice", help='preset voice name, e.g. "Hải Đăng" (default: the model default)')
    ap.add_argument("--ref-audio", type=Path, help="clone this 3-15 s clip instead of a preset voice")
    ap.add_argument("--temperature", type=float, default=0.7,
                    help="lower = steadier pronunciation, higher = livelier (default 0.7, UI default 0.8)")
    ap.add_argument("--device", default="auto", help="auto | cpu | cuda")
    ap.add_argument("--threads", type=int, default=0, help="CPU/ONNX threads (0 = engine default)")
    ap.add_argument("--max-chars", type=int, default=256, help="max characters per model chunk")
    ap.add_argument("--group-chars", type=int, default=1500, help="characters synthesized per step")
    ap.add_argument("--batch-size", type=int, default=None, help="GPU: chunks per forward pass")
    args = ap.parse_args()

    text = args.input.read_text(encoding="utf-8")
    groups = paragraph_groups(text, args.group_chars)
    if not groups:
        sys.exit("Input file has no text.")
    out = args.output or args.input.with_suffix(".wav")

    t_load = time.time()
    tts = Vieneu(device=args.device, threads=args.threads)
    load_user_voices(tts)                             # voices saved from the web UI / make_bilingual_voice.py
    voice = args.voice
    if args.ref_audio:
        voice = "_long_form_ref"
        tts.add_voice(voice, args.ref_audio)          # encode the clip once, not per group
    print(f"Model ready in {time.time() - t_load:.1f}s (backend: {getattr(tts, 'backend', '?')}). "
          f"{len(text):,} chars in {len(groups)} groups -> {out}")

    sr = tts.sample_rate
    total_chars = sum(len(g) for g in groups)
    done_chars, audio_s, prev = 0, 0.0, None
    t0 = time.time()
    with sf.SoundFile(str(out), "w", samplerate=sr, channels=1, subtype="PCM_16") as f:
        for i, group in enumerate(groups, 1):
            wav = tts.infer(group, voice=voice, temperature=args.temperature,
                            max_chars=args.max_chars, batch_size=args.batch_size)
            if wav.size == 0:
                continue
            if prev is not None:
                pad = pause_pad_samples(prev, wav, sr, V3_GAP_SILENCE["para"])
                if pad > 0:
                    f.write(np.zeros(pad, dtype=np.float32))
                    audio_s += pad / sr
            f.write(np.clip(wav, -1.0, 1.0))
            prev = wav
            audio_s += wav.size / sr
            done_chars += len(group)
            elapsed = time.time() - t0
            eta = elapsed / done_chars * (total_chars - done_chars)
            print(f"[{i}/{len(groups)}] audio {_fmt(audio_s)} | elapsed {_fmt(elapsed)} | "
                  f"RTF {elapsed / audio_s:.2f} | ETA {_fmt(eta)}", flush=True)

    print(f"Done: {out} ({_fmt(audio_s)} of audio in {_fmt(time.time() - t0)})")


if __name__ == "__main__":
    main()
