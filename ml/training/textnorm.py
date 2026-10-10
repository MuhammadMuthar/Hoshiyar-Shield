"""Text normalisation and feature extraction for Hoshiyar Shield.

THIS FILE IS A SPECIFICATION SHARED WITH TYPESCRIPT.
`apps/mobile/src/engine/normalize.ts` implements exactly the same steps. If you
change anything here, change it there too, retrain, and keep the parity test
(`apps/mobile/src/engine/__tests__/parity.test.ts`) passing.

Parity rules we follow on purpose:
- No `\\s`, `\\d`, `\\w` or `\\b` in regexes. Python and JavaScript disagree on
  their Unicode behaviour. Only explicit ASCII classes are used.
- No look-behind (keeps the JS port simple). Only `(?![...])` look-ahead.
- Lower-casing is ASCII-only, done by hand.
- Characters are processed by Unicode code point. Everything outside a small
  allow-list (a-z, digits, Urdu/Arabic letters) becomes a space, so emoji and
  astral characters can never cause UTF-16 vs code-point mismatches.

Why character n-grams: Roman Urdu has no standard spelling ("paisay / pesay /
paise", "foran / forun", "bhejein / bhejain / bhejo"). Overlapping character
n-grams share most of their features across these variants, so the model
generalises across spellings without a hand-built dictionary.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

NORMALIZER_VERSION = "hn-1.0"

# --- Step 0: whitespace & invisible characters ------------------------------
_WHITESPACE = set(
    "\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f\x85\xa0     　"
    + "".join(chr(c) for c in range(0x2000, 0x200B))
)
# Zero-width & formatting characters are deleted (not replaced by a space):
# they are a common trick to break keyword filters ("O​T​P").
_INVISIBLE = set("​‌‍‎‏⁠﻿­")

# --- Step 3: placeholder tokens --------------------------------------------
# The classifier never sees the actual URL, e-mail or phone number. It only
# sees that one was present. Link structure is judged by the separate URL
# analyser, so the text model can't memorise particular domains or numbers.
TOKEN_URL = " zurlz "
TOKEN_EMAIL = " zemailz "
TOKEN_PHONE = " zphonez "
TOKEN_UAN = " zuanz "  # UAN / toll-free numbers (111-xxx-xxx, 0800-xxxxx)

_TLDS = (
    "com|pk|net|org|info|biz|xyz|top|online|site|club|live|link|click|example|"
    "co|io|me|ly|gl|cc|tk|ml|ga|cf|gq|app|shop|store|vip|icu|win|loan|today|support"
)
EMAIL_RE = re.compile(r"[a-z0-9._%+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z][a-z]+")
URL_RE = re.compile(
    r"(?:https?://|www\.)[^ ]+"
    r"|[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:" + _TLDS + r")(?![a-z0-9-])(?:/[^ ]*)?"
)
UAN_RE = re.compile(r"111[ -]?[0-9]{3}[ -]?[0-9]{3}(?![0-9])|0800[ -]?[0-9]{5}(?![0-9])")
PHONE_RE = re.compile(
    r"(?:\+|00)?92[ -]?3[0-9]{2}[ -]?[0-9]{7}(?![0-9])|03[0-9]{2}[ -]?[0-9]{7}(?![0-9])"
)

# --- Step 4: de-obfuscation ("acc0unt", "j4zzc4sh", "p@ss", "0TP") ----------
LEET = {"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"}

# --- Step 5: Urdu / Arabic script canonicalisation --------------------------
URDU_MAP = {
    0x064A: "ی",  # Arabic yeh        -> Farsi/Urdu yeh
    0x0649: "ی",  # alef maksura      -> Urdu yeh
    0x0643: "ک",  # Arabic kaf        -> keheh
    0x0647: "ہ",  # Arabic heh        -> heh goal
    0x0623: "ا",  # alef with hamza above -> alef
    0x0625: "ا",  # alef with hamza below -> alef
    0x0629: "ۃ",  # teh marbuta       -> teh marbuta goal
}


def _is_az(ch: str) -> bool:
    return "a" <= ch <= "z"


def _is_alnum(ch: str) -> bool:
    return ("a" <= ch <= "z") or ("0" <= ch <= "9")


def _step_prepare(text: str) -> str:
    """Whitespace, invisibles, full-width ASCII, Urdu digits, ASCII lowercase."""
    out = []
    for ch in text:
        cp = ord(ch)
        if ch in _INVISIBLE:
            continue
        if ch in _WHITESPACE:
            out.append(" ")
            continue
        if 0xFF01 <= cp <= 0xFF5E:  # full-width ASCII -> ASCII
            cp -= 0xFEE0
            ch = chr(cp)
        if 0x06F0 <= cp <= 0x06F9:  # Extended Arabic-Indic (Urdu) digits
            ch = chr(cp - 0x06F0 + 48)
        elif 0x0660 <= cp <= 0x0669:  # Arabic-Indic digits
            ch = chr(cp - 0x0660 + 48)
        if "A" <= ch <= "Z":
            ch = chr(ord(ch) + 32)
        out.append(ch)
    return "".join(out)


def _step_deleet(s: str) -> str:
    out = []
    n = len(s)
    for i, ch in enumerate(s):
        if ch in LEET:
            prev = s[i - 1] if i > 0 else " "
            nxt = s[i + 1] if i + 1 < n else " "
            if _is_az(prev) and _is_az(nxt):
                out.append(LEET[ch])
                continue
            if ch == "0" and not _is_alnum(prev) and _is_az(nxt):
                out.append("o")
                continue
        out.append(ch)
    return "".join(out)


def _map_char(ch: str) -> str:
    cp = ord(ch)
    if 97 <= cp <= 122:
        return ch
    if 48 <= cp <= 57:
        return "0"  # keep "a number was here" + its length, not its value
    if cp in URDU_MAP:
        return URDU_MAP[cp]
    if 0x064B <= cp <= 0x065F or cp == 0x0670 or cp == 0x0640 or 0x06D6 <= cp <= 0x06ED:
        return ""  # harakat / diacritics / tatweel
    if 0x0621 <= cp <= 0x063A or 0x0641 <= cp <= 0x064A or 0x0671 <= cp <= 0x06D3:
        return ch
    return " "


def normalize(text: str) -> str:
    """Normalise a raw message into the canonical form used for features."""
    if not text:
        return ""
    s = _step_prepare(text)
    s = EMAIL_RE.sub(TOKEN_EMAIL, s)
    s = URL_RE.sub(TOKEN_URL, s)
    s = UAN_RE.sub(TOKEN_UAN, s)
    s = PHONE_RE.sub(TOKEN_PHONE, s)
    s = _step_deleet(s)
    s = "".join(_map_char(ch) for ch in s)
    return " ".join(t for t in s.split(" ") if t)


@dataclass(frozen=True)
class AnalyzerConfig:
    char_min: int = 2
    char_max: int = 5
    word_max: int = 0  # 0 = no word features, 1 = unigrams, 2 = + bigrams

    def to_dict(self) -> dict:
        return {"char_min": self.char_min, "char_max": self.char_max, "word_max": self.word_max}


def analyze(normalized: str, cfg: AnalyzerConfig) -> list[str]:
    """Turn a *normalised* string into a list of feature strings.

    Character n-grams are taken inside each token padded with one space on
    each side (like scikit-learn's `char_wb`). Word features get a `w:`
    prefix so they can never collide with character n-grams.
    """
    feats: list[str] = []
    tokens = [t for t in normalized.split(" ") if t] if normalized else []
    for tok in tokens:
        w = " " + tok + " "
        length = len(w)
        for n in range(cfg.char_min, cfg.char_max + 1):
            if n > length:
                break
            for i in range(length - n + 1):
                feats.append(w[i : i + n])
    if cfg.word_max >= 1:
        feats.extend("w:" + t for t in tokens)
    if cfg.word_max >= 2:
        feats.extend("w:" + a + " " + b for a, b in zip(tokens, tokens[1:]))
    return feats


def make_analyzer(cfg: AnalyzerConfig):
    """scikit-learn compatible callable analyzer (raw text in, features out)."""

    def _analyzer(raw: str) -> list[str]:
        return analyze(normalize(raw), cfg)

    return _analyzer
