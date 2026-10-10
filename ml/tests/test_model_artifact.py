"""Tests against the exported, shipped model (run train.py first)."""
import csv
import json
from pathlib import Path

import pytest

from training.jsonmodel import JsonModel, sigmoid
from training.textnorm import NORMALIZER_VERSION, normalize

ML = Path(__file__).resolve().parents[1]
ROOT = ML.parent
MODEL = ML / "artifacts" / "hoshiyar-model.json"
APP_MODEL = ROOT / "apps" / "mobile" / "assets" / "model" / "hoshiyar-model.json"
FIXTURES = ML / "artifacts" / "parity-fixtures.json"


@pytest.fixture(scope="module")
def model():
    return JsonModel(json.loads(MODEL.read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def raw():
    return json.loads(MODEL.read_text(encoding="utf-8"))


def test_artifact_structure(raw):
    assert raw["format"] == "hoshiyar-tfidf-logreg"
    assert raw["normalizer_version"] == NORMALIZER_VERSION
    assert len(raw["vocab"]) == len(raw["idf"]) == len(raw["coef"]) > 1000
    assert len(set(raw["vocab"])) == len(raw["vocab"])
    t = raw["thresholds"]
    assert 0 < t["suspicious"] <= t["high"] < 1
    assert "synthetic" in raw["metadata"]["disclaimer"]


def test_app_copy_is_identical():
    assert APP_MODEL.read_bytes() == MODEL.read_bytes()


def test_sigmoid_is_stable():
    assert sigmoid(-1000) == 0.0
    assert sigmoid(1000) == 1.0
    assert abs(sigmoid(0) - 0.5) < 1e-12


def test_empty_input_does_not_crash(model):
    d = model.score_details("")
    assert d["n_features"] == 0 and 0 <= d["p"] <= 1


def test_urdu_text_produces_features(model):
    d = model.score_details("آپ کا اکاؤنٹ بند ہونے والا ہے، کوڈ بھیجیں")
    assert d["n_features"] > 10


def test_roman_urdu_spelling_variants_score_consistently(model):
    # The ML score must be high and stable across spelling variants.
    # Finding (kept on purpose): the most heavily respelled variant scores ~0.73,
    # right at the ML "Suspicious" threshold. The app's verdict for it comes from
    # risk fusion (prize claim + upfront fee are high-severity cues); that is
    # tested in apps/mobile/src/engine/__tests__/analyze.test.ts.
    variants = [
        "Mubarak ho! Apka 5 lakh ka inaam nikla hai. Verification fee foran bhejein.",
        "mubarik ho apka 5 lac ka inam nikla he verification fee foren bhejain",
        "Mubaarak ho aapka 5 lakh ka inaam nikla hy. Verification fee fori bhejo",
    ]
    scores = [model.predict_proba(v) for v in variants]
    assert min(scores) > 0.6, scores
    assert max(scores) - min(scores) < 0.3, scores


def test_legitimate_messages_with_scam_words_are_not_flagged(model, raw):
    t = raw["thresholds"]["suspicious"]
    legit = [
        "Your Meezan Bank OTP for an online purchase of Rs 2,999 is 581204. Do not share this code with anyone. Meezan Bank will never ask for your OTP.",
        "Ammi, aap ke Easypaisa pe 5,000 bhej diye hain. Dawai le lijiye ga, shaam ko call karta hoon.",
        "HBL: Your A/C ****4821 has been debited by Rs. 3,450 on 09-Oct-2026 for a purchase at Imtiaz Store.",
    ]
    for text in legit:
        assert model.predict_proba(text) < t, text


def test_changing_the_message_changes_the_score(model):
    a = model.predict_proba("Apka JazzCash account block hone wala hai. Apna OTP foran share karein.")
    b = model.predict_proba("Apka JazzCash bill payment kamyab raha. Shukriya.")
    assert a - b > 0.5


def test_parity_fixtures_are_current(model, raw):
    fx = json.loads(FIXTURES.read_text(encoding="utf-8"))
    assert fx["model_version"] == raw["model_version"]
    for f in fx["fixtures"][:80]:
        d = model.score_details(f["text"])
        assert d["normalized"] == f["normalized"]
        assert abs(d["p"] - f["p"]) < 1e-12


def test_no_family_leakage_in_saved_split():
    rows = list(csv.DictReader((ML / "data" / "generated" / "splits.csv").open(encoding="utf-8")))
    test_fams = {r["template_family"] for r in rows if r["split"] == "test"}
    dev_fams = {r["template_family"] for r in rows if r["split"] == "dev"}
    assert test_fams and dev_fams and not (test_fams & dev_fams)


def test_metrics_are_test_set_not_training(raw):
    m = json.loads((ML / "artifacts" / "metrics.json").read_text(encoding="utf-8"))
    assert m["model_version"] == raw["model_version"]
    assert m["dataset"]["split_sizes"]["test"] > 300
    assert m["leakage_checks"]["shared_families_dev_test"] == 0
