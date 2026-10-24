"""
Vietnamese/English code-switching pre-pass for VieNeu-TTS.

sea-g2p picks a language per word from two dictionaries; a word found in both
("do", "it", "can", "not") follows its nearest unambiguous neighbour. That
reads short English phrases inside a Vietnamese sentence as Vietnamese
("cứ do it đi" -> "dò ít"), and the normalizer spells long ALL-CAPS words with
Vietnamese letter names ("MICROSOFT" -> "mờ i xê rờ..."). This pass runs on a
raw sentence BEFORE the normalizer and wraps the words that cannot be
Vietnamese in ``<en>...</en>``, which sea-g2p already routes to its English
engine — the phoneme inventory the model was trained on does not change.

Rules (each one only fires when the evidence is unambiguous):

* Vietnamese phonotactics: a syllable ending in p/t/c/ch must carry a sắc or
  nặng tone, and no Vietnamese syllable contains f/j/w/z or ends in s, l, r,
  d, k... So an unaccented "it", "not", "bus", "file" is English. Applied only
  to sentences that contain Vietnamese diacritics, so text typed without
  accents ("khong co gi dau") is left alone.
* ALL-CAPS words of 4+ letters that sea-g2p knows as a single English word
  (MICROSOFT, NVIDIA, POST) are lowercased inside ``<en>``. Shorter acronyms
  (HR, UBND, THPT) stay with the normalizer, which has its own reading table;
  Roman numerals and all-caps headlines are skipped.
* Adjacent tagged words are merged into one span so an English phrase keeps
  its phrase-level stress ("<en>let it go</en>").

Disable with ``VIENEU_CODESWITCH=0`` or :func:`set_enabled`. Optional user
lexicon: ``VIENEU_LEXICON=path/to/lexicon.json`` mapping whole words to the
text that should be read instead, e.g. ``{"ESP32": "<en>E S P</en> ba hai"}``.
"""

import json
import logging
import os
import re
from functools import lru_cache
from typing import Optional

logger = logging.getLogger("Vieneu.CodeSwitch")

_VI_LETTERS = "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
RE_VI_DIACRITIC = re.compile(f"[{_VI_LETTERS}]", re.IGNORECASE)

# Spans the pass must not touch: existing <en> tags, emotion cues, and
# whitespace-delimited chunks that look like URLs, emails, paths or file names.
_PROTECTED = (
    r"<en>.*?</en>"
    r"|\[[^\]]*\]"
    r"|<\|[^|]*\|>"
    r"|\S*(?:://|@|www\.|[\\/])\S*"
    r"|\S*[A-Za-z0-9]\.[A-Za-z]\S*"
)
RE_TOKEN = re.compile(rf"({_PROTECTED})|([A-Za-z{_VI_LETTERS}]+(?:['’][A-Za-z]+)*)", re.IGNORECASE | re.DOTALL)

RE_NON_VI_LETTER = re.compile(r"[fjwz]", re.IGNORECASE)
# Every Vietnamese syllable ends in a vowel or one of these codas.
RE_VI_CODA = re.compile(r"(?:[aeiouy]|p|t|c|ch|m|n|ng|nh)$", re.IGNORECASE)
RE_STOP_CODA = re.compile(r"(?:p|t|c|ch)$", re.IGNORECASE)
RE_ROMAN = re.compile(r"^[IVXLCDM]+$")
RE_ADJACENT_EN = re.compile(r"</en>(\s+)<en>")

_enabled: Optional[bool] = None


def is_enabled() -> bool:
    global _enabled
    if _enabled is None:
        _enabled = os.getenv("VIENEU_CODESWITCH", "1").strip().lower() not in ("0", "false", "no", "off")
    return _enabled


def set_enabled(enabled: bool) -> None:
    """Turn the pre-pass on or off for this process (overrides VIENEU_CODESWITCH)."""
    global _enabled
    _enabled = bool(enabled)


@lru_cache(maxsize=1)
def _g2p():
    from sea_g2p import G2P
    return G2P(lang="vi")


@lru_cache(maxsize=8192)
def _is_english_word(word: str) -> bool:
    """sea-g2p reads ``word`` as one English word rather than spelling it out."""
    phones = _g2p().convert(f"<en>{word}</en>").strip(" .")
    return bool(phones) and " " not in phones


def _impossible_vietnamese(word: str) -> bool:
    """An unaccented word that cannot be a Vietnamese syllable."""
    if RE_VI_DIACRITIC.search(word) or not word.isascii():
        return False
    if RE_NON_VI_LETTER.search(word) or not RE_VI_CODA.search(word):
        return True
    return bool(RE_STOP_CODA.search(word))


@lru_cache(maxsize=4)
def _load_lexicon(path: str) -> tuple:
    try:
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
    except (OSError, ValueError) as e:
        logger.warning(f"Không đọc được lexicon {path}: {e}")
        return ()
    # Longest key first so "ESP32 S3" wins over "ESP32".
    items = sorted(((str(k), str(v)) for k, v in entries.items() if str(k).strip()), key=lambda kv: -len(kv[0]))
    return tuple((re.compile(rf"(?<!\w){re.escape(k)}(?!\w)"), v) for k, v in items)


def apply_lexicon(text: str) -> str:
    path = os.getenv("VIENEU_LEXICON")
    if not path:
        return text
    for pattern, replacement in _load_lexicon(path):
        text = pattern.sub(lambda _m, r=replacement: r, text)
    return text


def tag_english(sentence: str) -> str:
    """Wrap the words of ``sentence`` that can only be English in ``<en>...</en>``."""
    if not sentence or not is_enabled():
        return sentence
    sentence = apply_lexicon(sentence)

    words = [m.group(2) for m in RE_TOKEN.finditer(sentence) if m.group(2)]
    if not words:
        return sentence
    has_diacritics = bool(RE_VI_DIACRITIC.search(sentence))
    long_words = [w for w in words if len(w) >= 2]
    headline = len(long_words) >= 3 and sum(w.isupper() for w in long_words) / len(long_words) >= 0.6

    def repl(m: re.Match) -> str:
        word = m.group(2)
        if not word:
            return m.group(0)                       # protected span
        if word.isupper() and len(word) >= 2:
            if (not headline and len(word) >= 4 and word.isascii()
                    and not RE_ROMAN.match(word) and _is_english_word(word.lower())):
                return f"<en>{word.lower()}</en>"
            return word                             # short acronym: normalizer's call
        if has_diacritics and _impossible_vietnamese(word):
            return f"<en>{word}</en>"
        return word

    tagged = RE_TOKEN.sub(repl, sentence)
    return RE_ADJACENT_EN.sub(r"\1", tagged)
