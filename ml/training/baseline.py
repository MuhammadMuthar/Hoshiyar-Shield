"""Baseline A: deterministic keyword-count classifier (the "if text.includes('OTP')" approach).

It exists only as a comparison. It shows why a keyword list isn't enough:
genuine OTP deliveries and bank security advice contain the same words.
"""

from __future__ import annotations

from .textnorm import normalize

KEYWORDS = [
    # English
    "otp", "pin", "code", "cvv", "password", "prize", "winner", "won", "lottery", "lucky draw",
    "congratulations", "fee", "charges", "processing", "blocked", "suspend", "verify",
    "verification", "urgent", "claim", "refund", "loan", "invest", "profit", "guaranteed",
    "cnic", "account", "link", "deposit",
    # Roman Urdu
    "inaam", "inam", "mubarak", "foran", "jaldi", "band", "block", "wapis", "qarza", "munafa",
    "bhejein", "jama", "raqam",
    # Urdu script
    "انعام", "فیس", "کوڈ", "پن", "بلاک", "بند", "فوری", "قرض", "منافع", "واپس", "تصدیق", "مبارک",
]
_KW = [normalize(k) for k in KEYWORDS]


def keyword_score(text: str) -> int:
    norm = " " + normalize(text) + " "
    return sum(1 for k in _KW if k and k in norm)


def predict(texts: list[str], min_hits: int) -> list[int]:
    return [1 if keyword_score(t) >= min_hits else 0 for t in texts]
