"""Export the trained model to portable JSON, and run inference from that JSON.

`predict_proba_json` is the reference implementation that the TypeScript
engine (`apps/mobile/src/engine/classifier.ts`) mirrors operation by
operation. The parity fixtures are produced with it.
"""

from __future__ import annotations

import hashlib
import json
import math

from .textnorm import NORMALIZER_VERSION, AnalyzerConfig, analyze, normalize

FORMAT = "hoshiyar-tfidf-logreg"
FORMAT_VERSION = 1


def _r(x: float) -> float:
    """Round to 7 significant digits: small JSON, error ~1e-7 relative."""
    return float(f"{x:.7g}")


def export_model(vectorizer, clf, cfg: AnalyzerConfig, thresholds: dict, metadata: dict) -> dict:
    vocab_items = sorted(vectorizer.vocabulary_.items(), key=lambda kv: kv[1])
    vocab = [term for term, _ in vocab_items]
    idf = [_r(v) for v in vectorizer.idf_]
    coef = [_r(v) for v in clf.coef_[0]]
    intercept = _r(float(clf.intercept_[0]))
    digest = hashlib.sha256(json.dumps([vocab, idf, coef, intercept], ensure_ascii=False).encode()).hexdigest()[:8]
    return {
        "format": FORMAT,
        "format_version": FORMAT_VERSION,
        "model_version": f"{metadata['version_prefix']}+{digest}",
        "normalizer_version": NORMALIZER_VERSION,
        "analyzer": cfg.to_dict(),
        "tfidf": {"sublinear_tf": True, "norm": "l2"},
        "thresholds": thresholds,
        "intercept": intercept,
        "vocab": vocab,
        "idf": idf,
        "coef": coef,
        "metadata": {k: v for k, v in metadata.items() if k != "version_prefix"},
    }


def sigmoid(z: float) -> float:
    """Numerically stable logistic function (mirrored in TypeScript)."""
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


class JsonModel:
    def __init__(self, model: dict):
        self.m = model
        self.cfg = AnalyzerConfig(**model["analyzer"])
        self.index = {t: i for i, t in enumerate(model["vocab"])}

    def score_details(self, text: str) -> dict:
        norm = normalize(text)
        counts: dict[int, int] = {}
        for f in analyze(norm, self.cfg):
            j = self.index.get(f)
            if j is not None:
                counts[j] = counts.get(j, 0) + 1
        idf, coef = self.m["idf"], self.m["coef"]
        vals = {j: (1.0 + math.log(c)) * idf[j] for j, c in counts.items()}
        norm2 = math.sqrt(sum(v * v for v in vals.values()))
        z = self.m["intercept"]
        if norm2 > 0:
            for j, v in vals.items():
                z += (v / norm2) * coef[j]
        p = sigmoid(z)
        return {"normalized": norm, "z": z, "p": p, "n_features": len(counts)}

    def predict_proba(self, text: str) -> float:
        return self.score_details(text)["p"]
