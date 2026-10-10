"""Train, evaluate and export the Hoshiyar Shield financial-scam classifier.

    .venv/bin/python ml/training/train.py

Pipeline (all deterministic, seed below):
 1. Generate the synthetic dataset from template families.
 2. Normalise, drop exact duplicates (after normalisation).
 3. Split into 5 folds BY TEMPLATE FAMILY (StratifiedGroupKFold): fold 0 is
    the held-out TEST set; folds 1-4 are development data. Test messages come
    from message ideas never seen in development.
 4. Leakage checks: no shared families, no shared normalised texts, and a
    near-duplicate similarity report.
 5. Model selection by grouped 4-fold CROSS-VALIDATION on development data
    (out-of-fold log-loss): char n-gram configs (+ one word+char config) x
    regularisation strengths.
 6. Risk thresholds chosen on OUT-OF-FOLD development scores (policy below).
 7. Final model refit on all development data, then a single evaluation on
    TEST + keyword baseline + challenge sets.
 8. Export the exact evaluated model to JSON for on-device TypeScript
    inference, plus parity fixtures, metrics.json and model-evaluation.md.

The shipped model is exactly the one evaluated on the test set. Nothing is
refit after testing, so the reported numbers describe the artifact in the app.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, log_loss, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parents[2]
ML = ROOT / "ml"
sys.path.insert(0, str(ML))

from data.challenge_set import rows as challenge_rows  # noqa: E402
from data.generate_dataset import OUT_PATH as DATASET_PATH  # noqa: E402
from data.generate_dataset import generate  # noqa: E402
from training import baseline  # noqa: E402
from training.edge_cases import EDGE_CASES  # noqa: E402
from training.jsonmodel import JsonModel, export_model  # noqa: E402
from training.textnorm import NORMALIZER_VERSION, AnalyzerConfig, make_analyzer, normalize  # noqa: E402

SEED = 20261011
VERSION_PREFIX = "hs-1.0.0"

ARTIFACTS = ML / "artifacts"
APP_MODEL_DIR = ROOT / "apps" / "mobile" / "assets" / "model"
APP_FIXTURE_DIR = ROOT / "apps" / "mobile" / "src" / "engine" / "__fixtures__"
DEMO_SAMPLES = ML / "data" / "demo_samples.json"
CONTRIB_DIR = ML / "data" / "contrib"
EVAL_DOC = ROOT / "docs" / "model-evaluation.md"

CONFIGS = {
    "char2-4": AnalyzerConfig(2, 4, 0),
    "char2-5": AnalyzerConfig(2, 5, 0),
    "char3-5": AnalyzerConfig(3, 5, 0),
    "char2-5+word1-2": AnalyzerConfig(2, 5, 2),
}
C_GRID = [1.0, 4.0, 16.0, 64.0, 256.0, 1024.0]

# Threshold policy (product decision, documented in docs/model-evaluation.md),
# applied to out-of-fold cross-validation scores on development data:
# - SUSPICIOUS starts at the lowest score whose out-of-fold false-positive rate
#   is <= 5% (catch as many scams as possible within an alarm budget), but never
#   below 0.25.
# - HIGH RISK starts at the lowest score whose out-of-fold FPR is <= 1% and
#   precision >= 0.97, but never below 0.60.
# The floors exist because synthetic data is easier than real SMS. Scores on
# real messages will be less extreme, so we don't let thresholds collapse
# towards 0 just because cross-validation was easy.
SUSPICIOUS_FPR_BUDGET, SUSPICIOUS_FLOOR = 0.05, 0.25
HIGH_FPR_BUDGET, HIGH_MIN_PRECISION, HIGH_FLOOR = 0.01, 0.97, 0.60


# ----------------------------------------------------------------------------- helpers
def binary_metrics(y_true, y_pred) -> dict:
    y_true = np.asarray(y_true).astype(int)
    y_pred = np.asarray(y_pred).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    fpr = fp / (fp + tn) if fp + tn else 0.0
    return {
        "n": int(len(y_true)), "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "precision": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4),
        "false_positive_rate": round(fpr, 4), "false_negatives": fn,
        "confusion_matrix": {"rows=actual[legit,scam]": [[tn, fp], [fn, tp]]},
    }


def calibration(y_true, p, bins: int = 10) -> dict:
    y_true = np.asarray(y_true, dtype=float)
    p = np.asarray(p, dtype=float)
    brier = float(np.mean((p - y_true) ** 2))
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (p >= lo) & (p < hi) if hi < 1 else (p >= lo) & (p <= hi)
        if mask.any():
            ece += mask.mean() * abs(p[mask].mean() - y_true[mask].mean())
    return {"brier": round(brier, 4), "ece_10bin": round(float(ece), 4)}


def fit(cfg: AnalyzerConfig, texts, y, C: float, vec: TfidfVectorizer | None = None):
    if vec is None:
        vec = TfidfVectorizer(
            analyzer=make_analyzer(cfg), sublinear_tf=True, min_df=2, norm="l2",
            smooth_idf=True, dtype=np.float64,
        )
        X = vec.fit_transform(texts)
    else:
        X = vec.transform(texts)
    clf = LogisticRegression(C=C, class_weight="balanced", max_iter=5000, solver="lbfgs")
    clf.fit(X, y)
    return vec, clf


def choose_thresholds(y_val, p_val) -> dict:
    y_val = np.asarray(y_val)
    p_val = np.asarray(p_val)
    neg = p_val[y_val == 0]
    grid = np.round(np.arange(0.05, 0.991, 0.01), 2)

    def fpr_at(t):
        return float((neg >= t).mean()) if len(neg) else 0.0

    def prec_at(t):
        flagged = p_val >= t
        return float(y_val[flagged].mean()) if flagged.any() else 1.0

    t_susp = next((float(t) for t in grid if fpr_at(t) <= SUSPICIOUS_FPR_BUDGET), 0.5)
    t_high = next((float(t) for t in grid if fpr_at(t) <= HIGH_FPR_BUDGET and prec_at(t) >= HIGH_MIN_PRECISION), 0.9)
    t_susp = max(t_susp, SUSPICIOUS_FLOOR)
    t_high = max(t_high, HIGH_FLOOR, t_susp)
    return {
        "suspicious": round(t_susp, 2),
        "high": round(t_high, 2),
        "policy": {
            "suspicious": f"lowest out-of-fold threshold with FPR <= {SUSPICIOUS_FPR_BUDGET:.0%}, floor {SUSPICIOUS_FLOOR}",
            "high": f"lowest out-of-fold threshold with FPR <= {HIGH_FPR_BUDGET:.0%} and precision >= {HIGH_MIN_PRECISION}, floor {HIGH_FLOOR}",
        },
    }


def grouped_metrics(df: pd.DataFrame, score_col: str, t: float, by: str) -> dict:
    out = {}
    for key, g in df.groupby(by):
        m = binary_metrics(g["label"], (g[score_col] >= t).astype(int))
        out[str(key)] = {"n": m["n"], "n_scam": int(g["label"].sum()), "recall": m["recall"],
                         "false_positive_rate": m["false_positive_rate"], "precision": m["precision"],
                         "fn": m["fn"], "fp": m["fp"]}
    return out


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


HISTORY_NOTES = {
    "v0-metrics.json": "211 families, 2 phrasings each; single train/val split; selection + thresholds on validation",
    "v1-metrics.json": "+62 families (3 phrasings, more Urdu script & hard negatives) after validation error analysis; single split",
}


def _history() -> list[dict]:
    """Earlier development runs, kept so the evaluation history is transparent."""
    out = []
    for path in sorted((ARTIFACTS / "history").glob("*.json")):
        h = json.loads(path.read_text(encoding="utf-8"))
        t = h["test"]
        out.append({
            "run": path.stem, "note": HISTORY_NOTES.get(path.name, ""),
            "test_rows": t["flagged_at_suspicious"]["n"], "roc_auc": t["roc_auc"],
            "thresholds": [h["thresholds"]["suspicious"], h["thresholds"]["high"]],
            "recall_at_suspicious": t["flagged_at_suspicious"]["recall"],
            "fpr_at_suspicious": t["flagged_at_suspicious"]["false_positive_rate"],
            "precision_at_high": t["flagged_at_high"]["precision"],
        })
    return out


# ---------------------------------------------------------------------------- pipeline
def main() -> dict:
    t_start = time.time()
    rng = np.random.default_rng(SEED)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    # 1. dataset ---------------------------------------------------------------
    rows = generate()
    DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DATASET_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    df = pd.DataFrame(rows)
    df["norm"] = df["text"].map(normalize)
    n_before = len(df)
    df = df.drop_duplicates(subset="norm", keep="first").reset_index(drop=True)
    n_dupes = n_before - len(df)
    print(f"[data] {len(df)} rows after dropping {n_dupes} normalised duplicates")

    # 2. grouped split -----------------------------------------------------------
    # 5 family-grouped folds: fold 0 = held-out TEST; folds 1-4 = development
    # data used for 4-fold cross-validation (model selection + thresholds).
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    folds = list(sgkf.split(df["text"], df["label"], groups=df["template_family"]))
    df["cv_fold"] = -1
    for k, (_, idx) in enumerate(folds):
        df.loc[idx, "cv_fold"] = k
    df["split"] = np.where(df.cv_fold == 0, "test", "dev")
    dev = df[df.split == "dev"].reset_index(drop=True)
    te = df[df.split == "test"].reset_index(drop=True)
    print(f"[split] dev={len(dev)} (4 CV folds) test={len(te)} "
          f"(families {dev.template_family.nunique()}/{te.template_family.nunique()})")
    df[["id", "template_family", "split", "cv_fold"]].to_csv(ML / "data" / "generated" / "splits.csv", index=False)

    # 3. leakage checks ----------------------------------------------------------
    fold_fams = [set(df[df.cv_fold == k].template_family) for k in range(5)]
    fold_norms = [set(df[df.cv_fold == k].norm) for k in range(5)]
    leak = {
        "shared_families_between_any_folds": sum(len(fold_fams[i] & fold_fams[j]) for i in range(5) for j in range(i + 1, 5)),
        "shared_families_dev_test": len(set(dev.template_family) & set(te.template_family)),
        "shared_normalized_texts_dev_test": len(set(dev.norm) & set(te.norm)),
        "shared_normalized_texts_between_any_folds": sum(len(fold_norms[i] & fold_norms[j]) for i in range(5) for j in range(i + 1, 5)),
    }
    assert all(v == 0 for v in leak.values()), f"leakage detected: {leak}"
    nd_vec = TfidfVectorizer(analyzer=make_analyzer(AnalyzerConfig(2, 5, 0)), sublinear_tf=True, min_df=1)
    Xdev_nd = nd_vec.fit_transform(dev.text)
    Xte_nd = nd_vec.transform(te.text)
    nearest = (Xte_nd @ Xdev_nd.T).max(axis=1).toarray().ravel()
    leak["near_duplicate_test_vs_dev"] = {
        "max_cosine": round(float(nearest.max()), 4),
        "mean_cosine": round(float(nearest.mean()), 4),
        "share_test_above_0.9": round(float((nearest > 0.9).mean()), 4),
        "share_test_above_0.8": round(float((nearest > 0.8).mean()), 4),
    }
    print(f"[leakage] {leak}")

    # 4. model selection by grouped 4-fold CV on dev (out-of-fold predictions) -----
    cv_folds = sorted(dev.cv_fold.unique())
    selection = []
    oof: dict[tuple[str, float], np.ndarray] = {}
    for name, cfg in CONFIGS.items():
        per_c = {C: np.zeros(len(dev)) for C in C_GRID}
        vocab_sizes = []
        for k in cv_folds:
            trn, hold = dev.cv_fold != k, dev.cv_fold == k
            vec_k = None
            for C in C_GRID:
                vec_k, clf_k = fit(cfg, dev.text[trn], dev.label[trn], C, vec=vec_k)
                per_c[C][hold.values] = clf_k.predict_proba(vec_k.transform(dev.text[hold]))[:, 1]
            vocab_sizes.append(len(vec_k.vocabulary_))
        for C in C_GRID:
            p = per_c[C]
            oof[(name, C)] = p
            selection.append({
                "config": name, "C": C, "vocab_size": int(np.mean(vocab_sizes)),
                "val_log_loss": round(float(log_loss(dev.label, p, labels=[0, 1])), 4),
                "val_average_precision": round(float(average_precision_score(dev.label, p)), 4),
                "val_roc_auc": round(float(roc_auc_score(dev.label, p)), 4),
                "val_f1_at_0.5": binary_metrics(dev.label, (p >= 0.5).astype(int))["f1"],
            })
    best_row = min(selection, key=lambda r: (r["val_log_loss"], r["vocab_size"]))
    best_name, best_C = best_row["config"], best_row["C"]
    best_cfg = CONFIGS[best_name]
    print(f"[select] best by CV out-of-fold log-loss: {best_name} C={best_C}")

    thresholds = choose_thresholds(dev.label, oof[(best_name, best_C)])
    print(f"[thresholds] {thresholds['suspicious']} / {thresholds['high']}")

    # Final model: refit on ALL development data. This exact model is tested and shipped.
    vec, clf = fit(best_cfg, dev.text, dev.label, best_C)
    tr = dev  # the final model's training data (used in metadata below)

    # Best model of each feature family (selected by CV), for an honest B-vs-C comparison.
    def best_of(pred):
        cands = [r for r in selection if pred(r["config"])]
        return min(cands, key=lambda r: (r["val_log_loss"], r["vocab_size"]))
    alt_rows = {
        "B_char_only": best_of(lambda c: "+word" not in c),
        "C_word_plus_char": best_of(lambda c: "+word" in c),
    }

    # 5. test evaluation (one shot) -----------------------------------------------
    te["p"] = clf.predict_proba(vec.transform(te.text))[:, 1]
    ts, th = thresholds["suspicious"], thresholds["high"]
    test_eval = {
        "flagged_at_suspicious": binary_metrics(te.label, (te.p >= ts).astype(int)),
        "flagged_at_high": binary_metrics(te.label, (te.p >= th).astype(int)),
        "at_0.5": binary_metrics(te.label, (te.p >= 0.5).astype(int)),
        "roc_auc": round(float(roc_auc_score(te.label, te.p)), 4),
        "average_precision": round(float(average_precision_score(te.label, te.p)), 4),
        "calibration": calibration(te.label, te.p),
        "per_language_at_suspicious": grouped_metrics(te, "p", ts, "language"),
        "per_category_at_suspicious": grouped_metrics(te, "p", ts, "category"),
        "per_category_at_high": grouped_metrics(te, "p", th, "category"),
    }
    comparison = {}
    for label_, r in alt_rows.items():
        v2, c2 = fit(CONFIGS[r["config"]], dev.text, dev.label, r["C"])
        p2 = c2.predict_proba(v2.transform(te.text))[:, 1]
        comparison[label_] = {
            "config": r["config"], "C": r["C"], "vocab_size": r["vocab_size"],
            "val_log_loss": r["val_log_loss"],
            "test_at_0.5": binary_metrics(te.label, (p2 >= 0.5).astype(int)),
            "test_roc_auc": round(float(roc_auc_score(te.label, p2)), 4),
        }

    # Baseline A: keyword counts, threshold (min hits) tuned on validation F1.
    base_val = {k: binary_metrics(dev.label, baseline.predict(list(dev.text), k)) for k in (1, 2, 3, 4)}
    base_k = max(base_val, key=lambda k: (base_val[k]["f1"], -k))
    base_test = binary_metrics(te.label, baseline.predict(list(te.text), base_k))
    te["baseline_pred"] = baseline.predict(list(te.text), base_k)
    baseline_by_cat = {}
    for cat, g in te.groupby("category"):
        m = binary_metrics(g.label, g.baseline_pred)
        baseline_by_cat[cat] = {"recall": m["recall"], "false_positive_rate": m["false_positive_rate"], "n": m["n"]}
    comparison["A_keyword_baseline"] = {"min_keyword_hits": base_k, "test": base_test,
                                        "per_category": baseline_by_cat}

    # 6. challenge sets ------------------------------------------------------------------
    def eval_set(rows_: list[dict], name: str) -> dict:
        cdf = pd.DataFrame(rows_)
        cdf["p"] = clf.predict_proba(vec.transform(cdf.text))[:, 1]
        labelled = cdf[cdf.label.notna()].copy()
        labelled["label"] = labelled.label.astype(int)
        res = {"name": name, "n": int(len(cdf)), "n_labelled": int(len(labelled))}
        if len(labelled) and labelled.label.nunique() == 2:
            res["flagged_at_suspicious"] = binary_metrics(labelled.label, (labelled.p >= ts).astype(int))
            res["flagged_at_high"] = binary_metrics(labelled.label, (labelled.p >= th).astype(int))
            res["keyword_baseline"] = binary_metrics(labelled.label, baseline.predict(list(labelled.text), base_k))
            if "language" in labelled:
                res["per_language_at_suspicious"] = grouped_metrics(labelled, "p", ts, "language")

        def verdict(p):
            return "HIGH" if p >= th else ("SUSPICIOUS" if p >= ts else "NO_OBVIOUS")

        res["items"] = [
            {"id": r.id, "label": None if pd.isna(r.label) else int(r.label), "language": r.language,
             "pattern": getattr(r, "pattern", None) or getattr(r, "category", None),
             "score": round(float(r.p), 4), "ml_verdict": verdict(r.p), "text": r.text}
            for r in cdf.itertuples()
        ]
        return res

    challenge_eval = eval_set(challenge_rows(), "claude_challenge (hand-written, out-of-template)")
    contrib_evals = []
    for path in sorted(CONTRIB_DIR.glob("*.jsonl")):
        crow = load_jsonl(path)
        res = eval_set(crow, f"contrib/{path.name}")
        res["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        res["families"] = len({r.get("template_family") for r in crow})
        res["by_language"] = pd.Series([r["language"] for r in crow]).value_counts().to_dict()
        res["in_training_data"] = len({normalize(r["text"]) for r in crow} & set(df.norm))
        if "flagged_at_suspicious" in res:
            cdf_ = pd.DataFrame(res["items"])
            cdf_["category"] = [r.get("category") for r in crow]
            cdf_ = cdf_[cdf_.label.notna()]
            res["per_category_at_suspicious"] = grouped_metrics(
                cdf_.assign(label=cdf_.label.astype(int)), "score", ts, "category")
        contrib_evals.append(res)
        print(f"[contrib] evaluated {path.name}")

    # 7. export ---------------------------------------------------------------------------
    created = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    model_json = export_model(vec, clf, best_cfg, {"suspicious": ts, "high": th}, {
        "version_prefix": VERSION_PREFIX,
        "created_at": created,
        "trained_on": f"{len(tr)} synthetic messages ({int(tr.label.sum())} scam / {int((tr.label == 0).sum())} legit), "
                      f"{tr.template_family.nunique()} template families",
        "languages": sorted(df.language.unique().tolist()),
        "config": best_name, "C": best_C, "seed": SEED, "sklearn_version": sklearn.__version__,
        "test_summary": {
            "recall_at_suspicious": test_eval["flagged_at_suspicious"]["recall"],
            "fpr_at_suspicious": test_eval["flagged_at_suspicious"]["false_positive_rate"],
            "precision_at_high": test_eval["flagged_at_high"]["precision"],
        },
        "disclaimer": "Trained and evaluated on synthetic data; real-world performance is not yet measured. "
                      "Scores are model outputs, not calibrated real-world scam probabilities.",
    })
    model_path = ARTIFACTS / "hoshiyar-model.json"
    model_text = json.dumps(model_json, ensure_ascii=False, separators=(",", ":"))
    model_path.write_text(model_text, encoding="utf-8")
    APP_MODEL_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(model_path, APP_MODEL_DIR / "hoshiyar-model.json")
    shutil.copy(DEMO_SAMPLES, APP_MODEL_DIR / "demo-samples.json")
    size_kb = round(model_path.stat().st_size / 1024, 1)

    # JSON-model parity with scikit-learn (rounding to 7 significant digits).
    jm = JsonModel(model_json)
    sk_p = clf.predict_proba(vec.transform(te.text))[:, 1]
    json_p = np.array([jm.predict_proba(t) for t in te.text])
    max_diff = float(np.abs(sk_p - json_p).max())
    assert max_diff < 1e-4, f"JSON export diverges from sklearn by {max_diff}"

    # Parity fixtures for the TypeScript engine.
    demo = json.loads(DEMO_SAMPLES.read_text(encoding="utf-8"))["samples"]
    fixture_texts = [s["text"] for s in demo] + [r["text"] for r in challenge_rows()] + EDGE_CASES
    sample_idx = rng.choice(len(te), size=min(150, len(te)), replace=False)
    fixture_texts += [te.text[i] for i in sorted(sample_idx)]
    fixtures = []
    for t in fixture_texts:
        d = jm.score_details(t)
        fixtures.append({"text": t, "normalized": d["normalized"], "n_features": d["n_features"],
                         "z": d["z"], "p": d["p"]})
    fixture_doc = {"model_version": model_json["model_version"], "normalizer_version": NORMALIZER_VERSION,
                   "count": len(fixtures), "fixtures": fixtures}
    (ARTIFACTS / "parity-fixtures.json").write_text(json.dumps(fixture_doc, ensure_ascii=False, indent=1), encoding="utf-8")
    APP_FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(ARTIFACTS / "parity-fixtures.json", APP_FIXTURE_DIR / "parity-fixtures.json")

    # Latency (Python reference; on-device latency is measured live in the app).
    sample = list(te.text[:200])
    t0 = time.perf_counter()
    for t in sample:
        clf.predict_proba(vec.transform([t]))
    sk_ms = (time.perf_counter() - t0) / len(sample) * 1000
    t0 = time.perf_counter()
    for t in sample:
        jm.predict_proba(t)
    json_ms = (time.perf_counter() - t0) / len(sample) * 1000

    # Most influential n-grams (global, from the linear weights).
    vocab = model_json["vocab"]
    coef = np.array(model_json["coef"])
    order = np.argsort(coef)
    top_scam = [{"feature": vocab[i], "weight": round(float(coef[i]), 3)} for i in order[::-1][:30]]
    top_legit = [{"feature": vocab[i], "weight": round(float(coef[i]), 3)} for i in order[:30]]

    demo_scores = []
    for s in demo:
        p = jm.predict_proba(s["text"])
        demo_scores.append({"id": s["id"], "example_of": s["example_of"], "score": round(p, 4),
                            "ml_verdict": "HIGH" if p >= th else ("SUSPICIOUS" if p >= ts else "NO_OBVIOUS")})

    demo_norms = {normalize(s["text"]) for s in demo}
    challenge_norms = {normalize(r["text"]) for r in challenge_rows()}

    metrics = {
        "model_version": model_json["model_version"],
        "created_at": created,
        "normalizer_version": NORMALIZER_VERSION,
        "seed": SEED,
        "dataset": {
            "rows_generated": n_before, "normalized_duplicates_dropped": n_dupes, "rows_used": len(df),
            "families": int(df.template_family.nunique()),
            "scam": int(df.label.sum()), "legit": int((df.label == 0).sum()),
            "by_language": df.language.value_counts().to_dict(),
            "by_category": df.category.value_counts().to_dict(),
            "split_sizes": {"dev_train_plus_val": len(dev), "test": len(te)},
            "split_families": {"dev_train_plus_val": int(dev.template_family.nunique()),
                               "test": int(te.template_family.nunique())},
            "cv_folds_in_dev": len(cv_folds),
            "test_by_language": te.language.value_counts().to_dict(),
            "demo_samples_in_training": len(demo_norms & set(df.norm)),
            "challenge_samples_in_training": len(challenge_norms & set(df.norm)),
        },
        "leakage_checks": leak,
        "model_selection": {"criterion": "grouped 4-fold cross-validation on dev, out-of-fold log-loss (tie: smaller vocabulary)",
                            "selected": {"config": best_name, "C": best_C, "analyzer": best_cfg.to_dict()},
                            "grid": selection},
        "thresholds": thresholds,
        "test": test_eval,
        "comparison": comparison,
        "challenge": challenge_eval,
        "contrib": contrib_evals,
        "demo_samples_ml_only": demo_scores,
        "export": {"model_json_kb": size_kb, "vocab_size": len(vocab),
                   "json_vs_sklearn_max_abs_diff": max_diff},
        "latency_ms_per_message_python": {"sklearn": round(sk_ms, 3), "pure_python_json_reference": round(json_ms, 3),
                                          "note": "Measured on the CI/dev container, not a phone. The app shows live on-device latency."},
        "top_features": {"towards_scam": top_scam, "towards_legit": top_legit},
        "runtime_seconds": round(time.time() - t_start, 1),
        "history": _history(),
    }
    (ARTIFACTS / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    from training.report import render_report  # local import keeps the pipeline readable
    EVAL_DOC.write_text(render_report(metrics), encoding="utf-8")
    print(f"[done] model {model_json['model_version']} ({size_kb} KB, vocab {len(vocab)}) "
          f"test recall@susp={test_eval['flagged_at_suspicious']['recall']} "
          f"fpr@susp={test_eval['flagged_at_suspicious']['false_positive_rate']} "
          f"precision@high={test_eval['flagged_at_high']['precision']} in {metrics['runtime_seconds']}s")
    return metrics


if __name__ == "__main__":
    main()
