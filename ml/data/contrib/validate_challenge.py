"""Validate the frozen v1 independent challenge set with the standard library.

Run from the repository root: python3 ml/data/contrib/validate_challenge.py
This checks the dataset contract, not classifier accuracy or real-world truth.
"""

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata


SCAM_CATEGORIES = {
    "prize_lottery", "otp_pin_theft", "impersonation", "loan_fee",
    "payment_request", "account_suspension", "investment", "refund_reversal",
}
LEGIT_CATEGORIES = {
    "legit_transaction_alert", "legit_otp_delivery", "legit_security_advice",
    "legit_conversation", "legit_payment_reminder", "legit_loan_ad",
    "legit_business_payment", "legit_url_info", "legit_promo",
}
LANGUAGES = {"roman_urdu": 32, "english": 20, "urdu": 16, "mixed": 12}
REQUIRED = {
    "id", "text", "label", "language", "category", "source", "synthetic",
    "template_family",
}
DOMAIN = re.compile(r"(?<![\w@])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}(?![\w.])", re.I)
PHONE_LIKE = re.compile(r"(?<!\w)\+?\d[\d ()-]{5,}\d(?!\w)")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def validate(path):
    raw = path.read_bytes()
    if not raw.endswith(b"\n"):
        raise ValueError("JSONL must end with a newline")
    rows = []
    seen_texts = set()
    family_labels = defaultdict(set)
    for number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip():
            raise ValueError(f"line {number}: blank row")
        row = json.loads(line, object_pairs_hook=unique_object)
        if not isinstance(row, dict) or not REQUIRED <= row.keys() or row.keys() - REQUIRED - {"notes"}:
            raise ValueError(f"line {number}: invalid fields")
        if row["id"] != f"cg-{number:04d}":
            raise ValueError(f"line {number}: expected ordered, unique cg- ID")
        for key in REQUIRED - {"label", "synthetic"}:
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"{row['id']}: {key} must be a nonempty string")
        if "notes" in row and not isinstance(row["notes"], str):
            raise ValueError(f"{row['id']}: notes must be a string")
        if type(row["label"]) is not int or row["label"] not in (0, 1):
            raise ValueError(f"{row['id']}: label must be integer 0 or 1")
        if row["synthetic"] is not True or row["source"] != "chatgpt_authored":
            raise ValueError(f"{row['id']}: incorrect provenance")
        categories = SCAM_CATEGORIES if row["label"] else LEGIT_CATEGORIES
        if row["category"] not in categories or row["language"] not in LANGUAGES:
            raise ValueError(f"{row['id']}: invalid category/label or language")
        if not re.fullmatch(r"cg-[a-z0-9]+(?:-[a-z0-9]+)*", row["template_family"]):
            raise ValueError(f"{row['id']}: invalid family identifier")
        if row["text"] != row["text"].strip() or any(c in row["text"] for c in "\r\n\t"):
            raise ValueError(f"{row['id']}: text must be a single, trimmed message")
        normalized = " ".join(unicodedata.normalize("NFKC", row["text"]).casefold().split())
        if normalized in seen_texts:
            raise ValueError(f"{row['id']}: duplicate message")
        seen_texts.add(normalized)
        for domain in DOMAIN.findall(row["text"]):
            if not domain.lower().endswith(".example"):
                raise ValueError(f"{row['id']}: domain must end in .example")
        for match in PHONE_LIKE.finditer(row["text"]):
            candidate = match.group()
            if len(re.sub(r"\D", "", candidate)) >= 7 and not re.fullmatch(r"0399-555[0-9]{4}", candidate):
                raise ValueError(f"{row['id']}: non-placeholder long number")
        family_labels[row["template_family"]].add(row["label"])
        rows.append(row)
    if len(rows) != 80 or Counter(row["label"] for row in rows) != {0: 40, 1: 40}:
        raise ValueError("v1 requires 80 messages, 40 per label")
    if Counter(row["language"] for row in rows) != LANGUAGES:
        raise ValueError("v1 language counts changed")
    for label in (0, 1):
        if Counter(row["language"] for row in rows if row["label"] == label) != {k: v // 2 for k, v in LANGUAGES.items()}:
            raise ValueError(f"label {label}: language counts changed")
    if Counter(row["category"] for row in rows if row["label"] == 1) != {k: 5 for k in SCAM_CATEGORIES}:
        raise ValueError("v1 requires five scams per category")
    if {row["category"] for row in rows if row["label"] == 0} != LEGIT_CATEGORIES:
        raise ValueError("missing legitimate category")
    if any(len(labels) != 1 for labels in family_labels.values()):
        raise ValueError("one family has conflicting labels; review it")
    return {
        "rows": len(rows),
        "labels": dict(sorted(Counter(row["label"] for row in rows).items())),
        "languages": LANGUAGES,
        "categories": dict(sorted(Counter(row["category"] for row in rows).items())),
        "families": len(family_labels),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


if __name__ == "__main__":
    target = Path(__file__).with_name("chatgpt_challenge.jsonl")
    try:
        result = validate(target)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
    print("PASS: independent challenge v1 structure and placeholder checks")
    print(json.dumps(result, ensure_ascii=False, indent=2))
