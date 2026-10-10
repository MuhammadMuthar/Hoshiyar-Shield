from training.edge_cases import EDGE_CASES
from training.textnorm import AnalyzerConfig, analyze, normalize


def test_empty_and_whitespace():
    assert normalize("") == ""
    assert normalize("   \t\n") == ""
    assert analyze("", AnalyzerConfig()) == []


def test_ascii_lowercase_and_punctuation_removed():
    assert normalize("MUBARAK HO!!! Apka INAAM") == "mubarak ho apka inaam"


def test_digits_collapse_to_zero_keeping_length():
    assert normalize("Rs. 5,000 only") == "rs 0 000 only"


def test_urls_emails_phones_become_placeholders():
    n = normalize("Visit https://x.example/a?b=1 or www.y.example, mail a.b@c.example, call 0399-5550123")
    assert "zurlz" in n and "zemailz" in n and "zphonez" in n
    assert "example" not in n
    assert normalize("+92 399 5550123") == "zphonez"
    assert normalize("923995550123") == "zphonez"
    assert normalize("bit-ly.example/x7Kq2") == "zurlz"


def test_uan_is_distinguished_from_mobile_numbers():
    assert normalize("call 111-555-123") == "call zuanz"
    assert normalize("call 0800-55123") == "call zuanz"


def test_leetspeak_is_undone():
    assert normalize("acc0unt bl0ck") == "account block"
    assert normalize("0TP bhejein") == "otp bhejein"
    assert normalize("j4zzc4sh p@ss") == "jazzcash pass"


def test_invisible_and_fullwidth_obfuscation():
    assert normalize("O​T​P") == "otp"
    assert normalize("ＯＴＰ") == "otp"


def test_urdu_script_is_kept_and_canonicalised():
    # Arabic kaf/yeh/heh -> Urdu forms; diacritics & tatweel dropped; Urdu digits mapped
    assert normalize("كيا") == normalize("کیا")
    assert normalize("انعـــام") == "انعام"
    assert normalize("مُبارَک") == "مبارک"
    assert normalize("۰۳۹۹۵۵۵۰۱۲۳") == "zphonez"
    assert normalize("آپ کا انعام۔") == "آپ کا انعام"


def test_emoji_removed():
    assert normalize("inaam 🎉🎉 nikla") == "inaam nikla"


def test_idempotent_on_edge_cases():
    for text in EDGE_CASES:
        once = normalize(text)
        assert normalize(once) == once, text


def test_char_ngrams_are_word_bounded():
    feats = analyze("ab cd", AnalyzerConfig(2, 3, 0))
    assert " a" in feats and "ab " in feats and "b c" not in feats
    # ' ab ' -> 3 bigrams + 2 trigrams, twice
    assert len(feats) == 10


def test_word_features_are_prefixed():
    feats = analyze("otp share", AnalyzerConfig(2, 2, 2))
    assert "w:otp" in feats and "w:otp share" in feats


def test_roman_urdu_spelling_variants_share_features():
    cfg = AnalyzerConfig(2, 4, 0)
    a = set(analyze(normalize("bhejein"), cfg))
    b = set(analyze(normalize("bhejain"), cfg))
    assert len(a & b) / len(a | b) > 0.3
