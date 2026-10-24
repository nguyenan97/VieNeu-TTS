"""Bilingual (Vietnamese + English) voices for v3 Turbo.

The preset voices are Vietnamese speakers, and the model copies their accent
into English too. A bilingual voice keeps a Vietnamese preset for Vietnamese
sentences and adds an ``en_voice`` used for sentences written fully in English:

    {"speaker_emb": ..., "codes": ...,                 # Vietnamese voice (e.g. Hải Đăng)
     "en_voice": {"speaker_emb": ..., "codes": ...}}    # English voice

The English voice takes its reference codes (which carry the accent and prosody)
from a native-English clip, and its speaker embedding is blended toward the
Vietnamese voice so the two sound like one person. Measured with the model's own
speaker encoder, a 0.8 blend lifted similarity to Hải Đăng from 0.49 to 0.76
(Hải Đăng reading English himself: 0.78), while Whisper still transcribed the
English sentences word for word.

English words inside a Vietnamese sentence ("check email nhé") stay with the
Vietnamese voice; only whole English sentences switch. Each sentence run is
loudness-matched and re-generated when a take comes out abnormally quiet or slow.
"""
import re
from typing import Any, List, Optional, Tuple, Union

import numpy as np

from vieneu_utils.codeswitch import RE_VI_DIACRITIC
from vieneu_utils.core_utils import V3_GAP_SILENCE, pause_pad_samples, split_into_sentences

EN_VOICE_KEY = "en_voice"
DEFAULT_EN_WEIGHT = 0.8          # share of the Vietnamese voice in the English speaker embedding
TARGET_DB = -21.0                # RMS of the voiced part of every run, so the two voices match
MAX_TRIES = 3

_RE_WORD = re.compile(r"[^\W\d_]+")
_RE_PARAGRAPH = re.compile(r"[\r\n]+")


def is_english_sentence(sentence: str) -> bool:
    """A sentence of 2+ words with no Vietnamese diacritics."""
    return len(_RE_WORD.findall(sentence)) >= 2 and not RE_VI_DIACRITIC.search(sentence)


def language_runs(text: str) -> List[Tuple[str, str, str]]:
    """Split ``text`` into ``(lang, run_text, gap_before)``: consecutive sentences of the
    same language inside a paragraph are merged; ``gap_before`` is "para" or "sentence"."""
    runs: List[Tuple[str, str, str]] = []
    for pi, para in enumerate(p for p in _RE_PARAGRAPH.split(text) if p.strip()):
        para_runs: List[Tuple[str, List[str]]] = []
        for s in split_into_sentences(para):
            lang = "en" if is_english_sentence(s) else "vi"
            if para_runs and para_runs[-1][0] == lang:
                para_runs[-1][1].append(s)
            else:
                para_runs.append((lang, [s]))
        for ri, (lang, sents) in enumerate(para_runs):
            runs.append((lang, " ".join(sents), "para" if ri == 0 and pi > 0 else "sentence"))
    return runs


def has_english(text: str) -> bool:
    return any(lang == "en" for lang, _, _ in language_runs(text))


def blend_en_voice(vi_voice: dict, en_emb: np.ndarray, en_codes: Optional[np.ndarray],
                   weight: float = DEFAULT_EN_WEIGHT) -> dict:
    """English voice: ``en_codes`` + speaker embedding moved ``weight`` toward ``vi_voice``."""
    emb = (1.0 - weight) * np.asarray(en_emb, np.float32) + weight * np.asarray(vi_voice["speaker_emb"], np.float32)
    return {"speaker_emb": emb.astype(np.float32),
            "codes": None if en_codes is None else np.asarray(en_codes, dtype=np.int64)}


def make_bilingual_voice(tts, vi_voice: str, en_ref_audio: str, weight: float = DEFAULT_EN_WEIGHT,
                         description: str = "") -> dict:
    """Build a bilingual voice entry from a preset Vietnamese voice and an English reference clip."""
    vi = tts.get_preset_voice(vi_voice)
    en_emb, en_codes = tts.encode_reference(en_ref_audio)
    entry = {k: v for k, v in vi.items() if k not in ("featured", EN_VOICE_KEY)}
    entry["description"] = description or f"Song ngữ · {vi_voice} + giọng Anh"
    entry[EN_VOICE_KEY] = blend_en_voice(vi, en_emb, en_codes, weight)
    return entry


def _level(wav: np.ndarray) -> np.ndarray:
    voiced = wav[np.abs(wav) > 0.01]
    if not voiced.size:
        return wav
    gain = 10 ** (TARGET_DB / 20) / float(np.sqrt((voiced ** 2).mean()))
    return np.clip(wav * gain, -1.0, 1.0).astype(np.float32)


def _take_ok(text: str, wav: np.ndarray, sr: int) -> bool:
    """Reject a take that is near-silent or far slower/faster than normal speech."""
    if wav.size == 0:
        return False
    voiced = wav[np.abs(wav) > 0.01]
    if not voiced.size or 20 * np.log10(float(np.sqrt((voiced ** 2).mean()))) < -30:
        return False
    chars_per_s = len(text) / (wav.size / sr)
    return 6.0 < chars_per_s < 30.0


def infer_bilingual(tts, text: str, voice: dict, **kwargs: Any) -> np.ndarray:
    """Synthesize ``text`` with the Vietnamese part of ``voice`` and its ``en_voice``
    for whole English sentences. ``kwargs`` go to ``tts.infer`` for every run."""
    vi_voice = {k: v for k, v in voice.items() if k != EN_VOICE_KEY}
    en_voice = voice[EN_VOICE_KEY]
    kwargs.pop("voice", None)
    kwargs.pop("ref_audio", None)
    sr = tts.sample_rate

    out: List[np.ndarray] = []
    prev: Optional[np.ndarray] = None
    for lang, run, gap in language_runs(text):
        wav = None
        for _ in range(MAX_TRIES):
            take = tts.infer(run, voice=en_voice if lang == "en" else vi_voice, **kwargs)
            ok = _take_ok(run, take, sr)
            if wav is None or ok:
                wav = take
            if ok:
                break
        if wav is None or wav.size == 0:
            continue
        wav = _level(wav)
        if prev is not None:
            out.append(np.zeros(pause_pad_samples(prev, wav, sr, V3_GAP_SILENCE[gap]), dtype=np.float32))
        out.append(wav)
        prev = wav
    return np.concatenate(out) if out else np.array([], dtype=np.float32)


def bilingual_voice_of(tts, voice: Union[str, dict, None]) -> Optional[dict]:
    """The bilingual entry ``voice`` refers to, or ``None`` for an ordinary voice."""
    if isinstance(voice, dict):
        return voice if EN_VOICE_KEY in voice else None
    if isinstance(voice, str):
        name = tts.resolve_voice_name(voice)
        entry = tts._preset_voices.get(name) if name else None
        return entry if isinstance(entry, dict) and EN_VOICE_KEY in entry else None
    return None
