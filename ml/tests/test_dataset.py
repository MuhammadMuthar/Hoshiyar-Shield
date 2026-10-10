import json
import re
from pathlib import Path

from data.challenge_set import rows as challenge_rows
from data.generate_dataset import generate
from training.textnorm import normalize

ML = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "text", "label", "language", "category", "source", "synthetic", "template_family"}


def test_generation_is_deterministic():
    assert generate()[:50] == generate()[:50]


def test_rows_have_provenance_fields_and_consistent_labels():
    rows = generate()
    assert len(rows) > 1500
    for r in rows:
        assert REQUIRED <= r.keys()
        assert r["synthetic"] is True
        assert r["label"] == (0 if r["category"].startswith("legit_") else 1)
        assert r["language"] in {"roman_urdu", "english", "urdu", "mixed"}
    langs = {r["language"] for r in rows}
    assert langs == {"roman_urdu", "english", "urdu", "mixed"}


def test_balanced_enough():
    rows = generate()
    share = sum(r["label"] for r in rows) / len(rows)
    assert 0.4 < share < 0.6


def test_only_placeholder_phone_numbers():
    pk_mobile = re.compile(r"(?:\+92|0092|92|0)[ -]?3\d{2}[ -]?\d{7}")
    for r in generate():
        for m in pk_mobile.findall(r["text"]):
            digits = re.sub(r"\D", "", m)
            assert digits.endswith(digits[-7:]) and "399555" in digits, m


def test_hard_negatives_exist():
    rows = generate()
    legit_otp = [r for r in rows if r["category"] == "legit_otp_delivery"]
    assert any("otp" in r["text"].lower() for r in legit_otp)
    legit_mubarak = [r for r in rows if r["label"] == 0 and "mubarak" in r["text"].lower()]
    assert legit_mubarak


def test_demo_and_challenge_messages_are_not_in_training_data():
    train_norms = {normalize(r["text"]) for r in generate()}
    demo = json.loads((ML / "data" / "demo_samples.json").read_text(encoding="utf-8"))["samples"]
    assert not {normalize(s["text"]) for s in demo} & train_norms
    assert not {normalize(r["text"]) for r in challenge_rows()} & train_norms
