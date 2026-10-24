"""Vietnamese/English code-switching pre-pass (vieneu_utils.codeswitch)."""
import json

import pytest

from vieneu_utils import codeswitch
from vieneu_utils.codeswitch import tag_english
from vieneu_utils.phonemize_text import normalize_to_chunks_v3, phonemize_text_with_emotions


@pytest.fixture(autouse=True)
def _enabled(monkeypatch):
    monkeypatch.delenv("VIENEU_LEXICON", raising=False)
    codeswitch.set_enabled(True)
    yield
    codeswitch.set_enabled(True)


def _phones(text, enabled=True):
    codeswitch.set_enabled(enabled)
    return " | ".join(phonemize_text_with_emotions(c) for c in normalize_to_chunks_v3(text))


@pytest.mark.parametrize("sentence, expected", [
    # unaccented stop-final syllables cannot be Vietnamese
    ("Bạn cứ do it đi.", "Bạn cứ do <en>it</en> đi."),
    ("Sếp nói but mình không nghe.", "Sếp nói <en>but</en> mình không nghe."),
    # adjacent tags merge into one phrase
    ("Thôi, let it go đi em.", "Thôi, <en>let it</en> go đi em."),
    # long ALL-CAPS dictionary words are read as words, not spelled
    ("Dùng sản phẩm của MICROSOFT.", "Dùng sản phẩm của <en>microsoft</en>."),
    ("Gửi POST request lên server.", "Gửi <en>post request</en> lên <en>server</en>."),
])
def test_tags_english(sentence, expected):
    assert tag_english(sentence) == expected


@pytest.mark.parametrize("sentence", [
    "Hôm nay trời đẹp, chúng tôi đi dạo quanh hồ.",
    "Thế kỷ XX và Chiến tranh thế giới thứ II.",           # Roman numerals
    "UBND TP.HCM và trường THPT tổ chức khai giảng.",      # Vietnamese acronyms
    "Anh ấy làm ở phòng HR.",                              # short acronym: normalizer decides
    "Hôm qua anh ấy [cười] kể chuyện [sigh] mệt quá.",     # emotion cues
    "khong co gi dau ban oi, it thoi ma.",                 # typed without diacritics
    "TIN NÓNG: BÃO SỐ BA ĐỔ BỘ VÀO MIỀN BẮC.",             # all-caps headline
])
def test_leaves_vietnamese_alone(sentence):
    assert tag_english(sentence) == sentence


@pytest.mark.parametrize("span", ["support@example.com", "https://vieneu.io/docs", "config.yaml", "C:\\data\\test.txt"])
def test_protected_spans_untouched(span):
    assert span in tag_english(f"Bạn mở {span} giúp tôi.")


def test_fixes_pipeline_readings():
    assert _phones("Bạn cứ do it đi.") != _phones("Bạn cứ do it đi.", enabled=False)
    assert "mˈaɪkɹəsˌɑːft" in _phones("Dùng sản phẩm của MICROSOFT.")
    assert "mˈaɪkɹəsˌɑːft" not in _phones("Dùng sản phẩm của MICROSOFT.", enabled=False)


def test_pure_vietnamese_unchanged_in_pipeline():
    text = "Thế kỷ XX, UBND TP.HCM gửi email đến support@example.com. Hôm qua [cười] vui quá."
    assert _phones(text) == _phones(text, enabled=False)


def test_disabled_is_identity():
    codeswitch.set_enabled(False)
    assert tag_english("Bạn cứ do it đi.") == "Bạn cứ do it đi."


def test_lexicon(tmp_path, monkeypatch):
    lex = tmp_path / "lexicon.json"
    lex.write_text(json.dumps({"ESP32": "<en>E S P</en> ba hai", "HR": "<en>H R</en>"}), encoding="utf-8")
    monkeypatch.setenv("VIENEU_LEXICON", str(lex))
    assert tag_english("Mạch ESP32 của phòng HR.") == "Mạch <en>E S P</en> ba hai của phòng <en>H R</en>."
