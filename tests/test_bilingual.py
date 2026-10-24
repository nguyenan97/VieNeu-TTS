"""Bilingual voices (vieneu.bilingual) — torch-free, no model download."""
import numpy as np
import pytest

from apps import user_voices
from vieneu import bilingual
from vieneu.bilingual import (EN_VOICE_KEY, blend_en_voice, bilingual_voice_of, infer_bilingual,
                              is_english_sentence, language_runs)

SR = 48_000
TEXT = (
    "Sáng nay mình check email. Hôm nay team có meeting.\n"
    "Good morning everyone. How are you today?\n"
    "Buổi trưa đi ăn cơm. Can you help me? Thank you so much, have a nice day nhé!"
)
VI_VOICE = {"speaker_emb": np.ones(4, np.float32), "codes": np.array([[1, 2]]), "description": "vi"}
EN_VOICE = {"speaker_emb": np.zeros(4, np.float32), "codes": np.array([[7, 8]])}
VOICE = {**VI_VOICE, EN_VOICE_KEY: EN_VOICE}


@pytest.mark.parametrize("sentence, expected", [
    ("Good morning everyone.", True),
    ("Sure, no problem.", True),
    ("Hôm nay team có meeting.", False),          # Vietnamese sentence with English words
    ("have a nice day nhé!", False),
    ("OK.", False),                               # one word is not a sentence
])
def test_is_english_sentence(sentence, expected):
    assert is_english_sentence(sentence) is expected


def test_language_runs_merge_and_gaps():
    runs = language_runs(TEXT)
    assert [(lang, gap) for lang, _, gap in runs] == [
        ("vi", "sentence"), ("en", "para"), ("vi", "para"), ("en", "sentence"), ("vi", "sentence"),
    ]
    assert runs[0][1] == "Sáng nay mình check email. Hôm nay team có meeting."
    assert runs[1][1] == "Good morning everyone. How are you today?"


def test_blend_en_voice():
    en = blend_en_voice(VI_VOICE, np.zeros(4), np.array([[7, 8]]), weight=0.8)
    np.testing.assert_allclose(en["speaker_emb"], np.full(4, 0.8, np.float32))
    assert en["codes"].tolist() == [[7, 8]]


class _FakeTTS:
    sample_rate = SR

    def __init__(self, quiet_first_en=False):
        self.calls = []
        self.quiet_first_en = quiet_first_en
        self._preset_voices = {"Custom": VOICE, "Plain": VI_VOICE}

    def resolve_voice_name(self, name):
        return name if name in self._preset_voices else None

    def infer(self, text, voice=None, **kw):
        is_en = voice["speaker_emb"][0] == 0
        self.calls.append(("en" if is_en else "vi", text))
        n = int(SR * len(text) / 15)                       # ~15 chars/s
        amp = 0.3 if is_en else 0.1                        # different loudness per voice
        if is_en and self.quiet_first_en and sum(c[0] == "en" for c in self.calls) == 1:
            amp = 0.005                                    # a near-silent take
        return (amp * np.sin(np.arange(n) / 10)).astype(np.float32)


def test_infer_bilingual_routes_runs_and_levels():
    tts = _FakeTTS()
    wav = infer_bilingual(tts, TEXT, VOICE, temperature=0.7)
    assert [lang for lang, _ in tts.calls] == ["vi", "en", "vi", "en", "vi"]
    assert wav.dtype == np.float32 and wav.size > 0
    # every run is brought to the same loudness, so the louder English voice no longer stands out
    vi_rms = np.sqrt((wav[: SR // 2] ** 2).mean())
    assert 0.05 < vi_rms < 0.15


def test_infer_bilingual_retries_bad_take():
    tts = _FakeTTS(quiet_first_en=True)
    infer_bilingual(tts, TEXT, VOICE)
    assert [lang for lang, _ in tts.calls] == ["vi", "en", "en", "vi", "en", "vi"]


def test_bilingual_voice_of():
    tts = _FakeTTS()
    assert bilingual_voice_of(tts, "Custom") is VOICE
    assert bilingual_voice_of(tts, "Plain") is None
    assert bilingual_voice_of(tts, VOICE) is VOICE
    assert bilingual_voice_of(tts, None) is None


def test_user_voice_json_roundtrip():
    tts = _FakeTTS()
    data = user_voices._entry_to_json(VOICE)
    assert data[EN_VOICE_KEY]["codes"] == [[7, 8]]
    entry = user_voices._entry_from_json(tts, data)
    np.testing.assert_allclose(entry[EN_VOICE_KEY]["speaker_emb"], EN_VOICE["speaker_emb"])
    assert entry[EN_VOICE_KEY]["codes"].tolist() == [[7, 8]]


def test_plain_voice_json_has_no_en_voice():
    assert EN_VOICE_KEY not in user_voices._entry_to_json(VI_VOICE)
    assert bilingual.has_english("Chỉ có tiếng Việt thôi.") is False
