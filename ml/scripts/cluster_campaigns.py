"""Scam-campaign clustering over SYNTHETIC demo reports.

    .venv/bin/python ml/scripts/cluster_campaigns.py

What it shows: differently worded scam reports that share a pattern (e.g.
several prize-fee messages) can be grouped into one "campaign" with character
n-gram TF-IDF + cosine similarity + agglomerative clustering. Analysts could
then review groups instead of individual reports.

What it does NOT show: real reports, live national data, or common ownership.
Similar wording does not prove the same people are behind messages.

Input: 160 synthetic reports generated from the scam template families
(seeded, separate from the classifier dataset), with synthetic report dates
and masked placeholder numbers. Output: ml/artifacts/campaigns.json (schema
in docs/COLLABORATION.md §5.5), also copied into the app.
"""

from __future__ import annotations

import datetime as dt
import json
import random
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "ml"))

from data.generate_dataset import ALL_SCAM, add_noise, fill, vary_roman  # noqa: E402
from training.textnorm import AnalyzerConfig, make_analyzer, normalize  # noqa: E402

SEED = 77
N_ACTIVE_CAMPAIGNS = 9           # families that behave like active campaigns
REPORTS_PER_CAMPAIGN = (9, 22)
N_BACKGROUND = 30                # one-off reports from other families
DISTANCE_THRESHOLD = 0.75        # cosine distance cut for average linkage
MIN_CAMPAIGN_SIZE = 4
START = dt.date(2026, 9, 1)
END = dt.date(2026, 10, 9)
OUT = ROOT / "ml" / "artifacts" / "campaigns.json"
APP_COPY = ROOT / "apps" / "mobile" / "assets" / "model" / "campaigns.json"

CATEGORY_LABEL = {
    "prize_lottery": "Prize / lottery fee", "otp_pin_theft": "OTP / PIN theft",
    "impersonation": "Bank or official impersonation", "loan_fee": "Loan processing fee",
    "payment_request": "Urgent payment request", "account_suspension": "Fake account suspension",
    "investment": "Investment / double money", "refund_reversal": "Refund / wrong-transfer trick",
}


def sanitize(text: str) -> str:
    """Representative pattern: replace numbers, links and amounts with placeholders."""
    t = re.sub(r"(https?://|www\.)\S+|\b[\w-]+(\.[\w-]+)*\.(example|com|pk)(/\S*)?", "<LINK>", text)
    t = re.sub(r"(\+92|0092|92)?[ -]?0?3\d{2}[ -]?\d{7}", "<PHONE>", t)
    t = re.sub(r"(?i)(Rs\.?\s?|PKR\s?)?\d[\d,]*(\.\d+)?(/-)?(\s?(rupay|lakh|lac))?", " <AMOUNT> ", t)
    t = "".join(ch for ch in t if ord(ch) <= 0xFFFF and ch not in "\ufe0f\u200d")
    t = re.sub(r"\s+([.,!?:;،۔])", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def link_kind(text: str) -> str:
    if re.search(r"(https?://|www\.)|\.example", text):
        return "link"
    if re.search(r"0?3\d{2}[ -]?\d{7}", text):
        return "phone_number"
    return "none"


def main() -> None:
    rng = random.Random(SEED)
    span = (END - START).days
    families = ALL_SCAM[:]
    rng.shuffle(families)
    active, background = families[:N_ACTIVE_CAMPAIGNS], families[N_ACTIVE_CAMPAIGNS:]

    reports = []
    for fam_id, category, language, phrasings in active:
        n = rng.randint(*REPORTS_PER_CAMPAIGN)
        start = rng.randint(0, span - 12)
        length = rng.randint(7, span - start)
        for i in range(n):
            text = fill(rng.choice(phrasings), rng)
            if language in ("roman_urdu", "mixed"):
                text = vary_roman(text, rng)
            reports.append({"text": add_noise(text, rng), "category": category, "source_family": fam_id,
                            "date": (START + dt.timedelta(days=start + rng.randint(0, length))).isoformat(),
                            "channel": rng.choice(["SMS", "SMS", "WhatsApp", "Call follow-up SMS"])})
    for _ in range(N_BACKGROUND):
        fam_id, category, language, phrasings = rng.choice(background)
        reports.append({"text": add_noise(fill(rng.choice(phrasings), rng), rng), "category": category,
                        "source_family": fam_id, "date": (START + dt.timedelta(days=rng.randint(0, span))).isoformat(),
                        "channel": "SMS"})
    rng.shuffle(reports)

    texts = [r["text"] for r in reports]
    vec = TfidfVectorizer(analyzer=make_analyzer(AnalyzerConfig(2, 4, 0)), sublinear_tf=True, min_df=1)
    X = vec.fit_transform(texts).toarray()
    labels = AgglomerativeClustering(
        n_clusters=None, metric="cosine", linkage="average", distance_threshold=DISTANCE_THRESHOLD
    ).fit_predict(X)

    vocab = np.array(vec.get_feature_names_out())
    campaigns = []
    for lab, count in Counter(labels).most_common():
        if count < MIN_CAMPAIGN_SIZE:
            continue
        idx = [i for i, l in enumerate(labels) if l == lab]
        members = [reports[i] for i in idx]
        centroid = X[idx].mean(axis=0)
        rep_i = idx[int(np.argmax(X[idx] @ centroid))]
        cats = Counter(m["category"] for m in members)
        dom, dom_n = cats.most_common(1)[0]
        dates = sorted(m["date"] for m in members)
        words = [w.strip() for w in vocab[np.argsort(centroid)[::-1]] if len(w.strip()) >= 4 and " " not in w.strip()]
        top_terms = []
        for w in words:
            if w not in ("zphonez", "zurlz", "zuanz") and not any(w in t or t in w for t in top_terms):
                top_terms.append(w)
            if len(top_terms) == 5:
                break
        weekly = Counter((dt.date.fromisoformat(d) - START).days // 7 for d in dates)
        purity = dom_n / count
        fam_purity = Counter(m["source_family"] for m in members).most_common(1)[0][1] / count
        campaigns.append({
            "campaign_id": "",
            "report_count": count,
            "dominant_category": dom,
            "dominant_category_label": CATEGORY_LABEL[dom],
            "category_share": round(purity, 2),
            "representative_pattern": sanitize(reports[rep_i]["text"]),
            "first_seen": dates[0],
            "last_seen": dates[-1],
            "top_terms": top_terms,
            "weekly_reports": [weekly.get(w, 0) for w in range((END - START).days // 7 + 1)],
            "contact_methods": dict(Counter(link_kind(m["text"]) for m in members)),
            "channels": dict(Counter(m["channel"] for m in members)),
            "_source_family_purity": round(fam_purity, 2),
        })
    campaigns.sort(key=lambda c: (-c["report_count"], c["last_seen"]))
    for i, c in enumerate(campaigns, start=1):
        c["campaign_id"] = f"C-{i:02d}"

    clustered = sum(c["report_count"] for c in campaigns)
    by_cat = Counter(r["category"] for r in reports)
    weekly_all = Counter((dt.date.fromisoformat(r["date"]) - START).days // 7 for r in reports)
    phrases = Counter()
    for r in reports:
        toks = normalize(r["text"]).split()
        for a, b in zip(toks, toks[1:]):
            if all(len(x) > 2 and x not in ("zphonez", "zurlz", "000") for x in (a, b)):
                phrases[f"{a} {b}"] += 1
    doc = {
        "generated_from": "synthetic demo reports",
        "is_synthetic": True,
        "disclaimer": "SIMULATED DATA for the hackathon demo. These are not real reports, not live national data, "
                      "and similar wording does not prove that the same people are behind different messages.",
        "method": f"char 2-4-gram TF-IDF (Hoshiyar normaliser) + agglomerative clustering (cosine, average linkage, "
                  f"distance threshold {DISTANCE_THRESHOLD}); groups with >= {MIN_CAMPAIGN_SIZE} reports shown",
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "window": {"start": START.isoformat(), "end": END.isoformat()},
        "total_reports": len(reports),
        "clustered_reports": clustered,
        "unclustered_reports": len(reports) - clustered,
        "reports_by_category": {k: {"label": CATEGORY_LABEL[k], "count": v} for k, v in by_cat.most_common()},
        "weekly_reports": [weekly_all.get(w, 0) for w in range((END - START).days // 7 + 1)],
        "contact_methods": dict(Counter(link_kind(r["text"]) for r in reports)),
        "top_phrases": [{"phrase": p, "count": n} for p, n in phrases.most_common(8)],
        "evaluation": {
            "note": "Because the data is synthetic we know which template family produced each report. "
                    "Mean family purity of shown clusters measures how well clustering recovers them.",
            "mean_family_purity": round(float(np.mean([c["_source_family_purity"] for c in campaigns])), 3) if campaigns else None,
            "mean_category_purity": round(float(np.mean([c["category_share"] for c in campaigns])), 3) if campaigns else None,
            "active_campaign_families": N_ACTIVE_CAMPAIGNS,
            "clusters_found": len(campaigns),
        },
        "campaigns": campaigns,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copy(OUT, APP_COPY)
    print(f"{len(reports)} synthetic reports -> {len(campaigns)} campaigns ({clustered} clustered); "
          f"family purity {doc['evaluation']['mean_family_purity']}, category purity {doc['evaluation']['mean_category_purity']}")
    for c in campaigns:
        print(f"  {c['campaign_id']} n={c['report_count']:2d} {c['dominant_category']:<18} {c['first_seen']}..{c['last_seen']} "
              f"fam={c['_source_family_purity']} | {c['representative_pattern'][:80]}")


if __name__ == "__main__":
    main()
