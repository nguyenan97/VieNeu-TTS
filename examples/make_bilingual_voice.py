"""Create a bilingual voice: a Vietnamese preset for Vietnamese sentences plus an
English voice for sentences written fully in English (see vieneu/bilingual.py).

    uv run python examples/make_bilingual_voice.py
    uv run python examples/make_bilingual_voice.py --name "Custom Song Ngữ" --vi-voice "Hải Đăng" --weight 0.8

The voice is saved to ~/.vieneu/user_voices_v3_turbo.json, so it appears in the
web UI voice list and works with examples/long_form.py --voice "<name>".

The default English reference, examples/audio_ref/en_kokoro_am_michael.wav, was
generated with Kokoro-82M (hexgrad/Kokoro-82M, Apache-2.0), voice "am_michael".
Any clean 5-15 s clip of a native English speaker works as --en-ref.
"""
import argparse
from pathlib import Path

from apps.user_voices import load_user_voices, save_bilingual_voice, user_voices_path
from vieneu import Vieneu

DEFAULT_EN_REF = Path(__file__).parent / "audio_ref" / "en_kokoro_am_michael.wav"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", default="Custom Song Ngữ", help="name of the new voice")
    ap.add_argument("--vi-voice", default="Hải Đăng", help="preset voice for Vietnamese sentences")
    ap.add_argument("--en-ref", type=Path, default=DEFAULT_EN_REF, help="native English reference clip")
    ap.add_argument("--weight", type=float, default=0.8,
                    help="0-1: how far the English voice moves toward --vi-voice "
                         "(higher = sounds more like the same person, lower = more native accent)")
    ap.add_argument("--device", default="auto", help="auto | cpu | cuda")
    args = ap.parse_args()

    tts = Vieneu(device=args.device)
    load_user_voices(tts)
    name = save_bilingual_voice(tts, args.name, args.vi_voice, str(args.en_ref), weight=args.weight,
                                description=f"Song ngữ · {args.vi_voice} + giọng Anh ({args.weight:.0%})")
    print(f"Saved bilingual voice '{name}' -> {user_voices_path(tts)}")


if __name__ == "__main__":
    main()
