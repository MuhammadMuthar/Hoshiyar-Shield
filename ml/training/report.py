"""Render docs/model-evaluation.md from metrics.json.

The evaluation document is generated, never hand-edited, so it can't drift
from what the pipeline actually measured.
"""

from __future__ import annotations


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def _m_row(name: str, m: dict) -> str:
    return (f"| {name} | {m['n']} | {_pct(m['precision'])} | {_pct(m['recall'])} | {m['f1']:.3f} | "
            f"{_pct(m['false_positive_rate'])} | {m['fn']} | {m['fp']} |")


M_HEAD = ("| Setting | n | Precision | Recall | F1 | False-positive rate | False negatives | False positives |\n"
          "|---|---|---|---|---|---|---|---|")


def render_report(m: dict) -> str:
    d, t, th, c = m["dataset"], m["test"], m["thresholds"], m["comparison"]
    lines: list[str] = []
    a = lines.append
    a("# Model Evaluation: Hoshiyar Shield scam classifier")
    a("")
    a("> **Auto-generated** by `ml/training/train.py` from `ml/artifacts/metrics.json`. Don't edit by hand.")
    a(f"> Model `{m['model_version']}` · normaliser `{m['normalizer_version']}` · generated {m['created_at']} · seed {m['seed']}")
    a("")
    a("## Read this first: what these numbers mean")
    a("")
    a("- **All training and test data is synthetic**: messages generated from template families written by the team")
    a("  (see `docs/dataset-card.md`). The test set uses *template families the model never saw*, which is stricter")
    a("  than a random split. It is still **not** a measurement of real-world performance on live SMS traffic.")
    a("- Hyperparameters and thresholds were chosen by grouped 4-fold cross-validation on development data only. The final")
    a("  model was refit on all development data and evaluated **once** on the held-out test families. The shipped model")
    a("  (`apps/mobile/assets/model/hoshiyar-model.json`) is **exactly** that model. Nothing is refit after testing.")
    a("- Scores are logistic-regression outputs. They are **not calibrated real-world scam probabilities**, so the app")
    a("  shows risk *levels*, not percentages.")
    a("- The app's final verdict also uses a deterministic indicator engine and URL analyser (risk fusion, see")
    a("  `docs/architecture.md`). The numbers below are for the **ML classifier alone** unless stated otherwise.")
    a("")
    a("## Headline (held-out test set, unseen template families)")
    a("")
    fs, fh = t["flagged_at_suspicious"], t["flagged_at_high"]
    a(f"| | Value |\n|---|---|")
    a(f"| Test messages | {fs['n']} ({d['split_families']['test']} unseen families) |")
    a(f"| Scam recall at *Suspicious* threshold ({th['suspicious']}) | **{_pct(fs['recall'])}** ({fs['fn']} scams missed) |")
    a(f"| False-positive rate at *Suspicious* threshold | **{_pct(fs['false_positive_rate'])}** ({fs['fp']} legit messages flagged) |")
    a(f"| Precision at *High Risk* threshold ({th['high']}) | **{_pct(fh['precision'])}** |")
    a(f"| Scam recall at *High Risk* threshold | {_pct(fh['recall'])} |")
    a(f"| ROC-AUC / average precision | {t['roc_auc']} / {t['average_precision']} |")
    a(f"| Model size (JSON) / vocabulary | {m['export']['model_json_kb']} KB / {m['export']['vocab_size']:,} features |")
    a("")
    a("## Baseline vs. machine learning (same test set)")
    a("")
    a(M_HEAD)
    b = c["A_keyword_baseline"]
    a(_m_row(f"A: keyword baseline (≥{b['min_keyword_hits']} keyword hits, tuned on dev)", b["test"]))
    a(_m_row(f"B: char n-gram TF-IDF + LR [{c['B_char_only']['config']}, C={c['B_char_only']['C']}] @0.5", c["B_char_only"]["test_at_0.5"]))
    a(_m_row(f"C: word+char TF-IDF + LR [{c['C_word_plus_char']['config']}, C={c['C_word_plus_char']['C']}] @0.5", c["C_word_plus_char"]["test_at_0.5"]))
    a(_m_row(f"**Shipped model** @ Suspicious ({th['suspicious']})", fs))
    a(_m_row(f"**Shipped model** @ High Risk ({th['high']})", fh))
    a("")
    a("Where the keyword baseline goes wrong (per category, test set):")
    a("")
    a("| Category | n | Keyword baseline: recall / false-alarm rate | Shipped model @Suspicious: recall / false-alarm rate |")
    a("|---|---|---|---|")
    pcs = t["per_category_at_suspicious"]
    for cat, bm in sorted(b["per_category"].items()):
        mm = pcs.get(cat)
        if cat.startswith("legit_"):
            a(f"| {cat} | {bm['n']} | false alarms {_pct(bm['false_positive_rate'])} | false alarms {_pct(mm['false_positive_rate'])} |")
        else:
            a(f"| {cat} | {bm['n']} | recall {_pct(bm['recall'])} | recall {_pct(mm['recall'])} |")
    a("")
    a("## Per-language results (test, at Suspicious threshold)")
    a("")
    a("| Language | n | Scams | Recall | False-positive rate | Precision |")
    a("|---|---|---|---|---|---|")
    for lang, r in sorted(t["per_language_at_suspicious"].items()):
        a(f"| {lang} | {r['n']} | {r['n_scam']} | {_pct(r['recall'])} | {_pct(r['false_positive_rate'])} | {_pct(r['precision'])} |")
    a("")
    a("## Per-category results (test)")
    a("")
    a("Scam categories show **recall**. Legitimate categories show the **false-alarm rate**. Counts per category are small")
    a("(a handful of families each), so treat single-category numbers as indicative only.")
    a("")
    a("| Category | n | @Suspicious | @High Risk |")
    a("|---|---|---|---|")
    pch = t["per_category_at_high"]
    for cat in sorted(pcs):
        s_, h_ = pcs[cat], pch[cat]
        if cat.startswith("legit_"):
            a(f"| {cat} | {s_['n']} | false alarms {_pct(s_['false_positive_rate'])} | false alarms {_pct(h_['false_positive_rate'])} |")
        else:
            a(f"| {cat} | {s_['n']} | recall {_pct(s_['recall'])} | recall {_pct(h_['recall'])} |")
    a("")
    a("## Confusion matrices (test)")
    a("")
    for name, mm in (("Suspicious threshold", fs), ("High Risk threshold", fh)):
        cm = mm["confusion_matrix"]["rows=actual[legit,scam]"]
        a(f"**{name}**\n")
        a("| | Predicted legit | Predicted scam |\n|---|---|---|")
        a(f"| **Actual legit** | {cm[0][0]} | {cm[0][1]} |")
        a(f"| **Actual scam** | {cm[1][0]} | {cm[1][1]} |")
        a("")
    a(f"Calibration on test: Brier score {t['calibration']['brier']}, expected calibration error (10 bins) "
      f"{t['calibration']['ece_10bin']}. Calibration on synthetic data says nothing about calibration on real messages.")
    a("")
    ch = m["challenge"]
    a("## Challenge set: unfamiliar patterns written separately (evaluation only)")
    a("")
    a(f"{ch['n']} hand-written messages ({ch['n_labelled']} labelled, {ch['n'] - ch['n_labelled']} deliberately ambiguous).")
    a("They use scam types that appear in **no** training template (job-visa fees, customs parcels, crypto")
    a("withdrawal tax, Hajj ballots, fake buyers, obfuscated text, …) and new legitimate hard negatives.")
    a("The same author (Claude) wrote the templates, so this isn't fully independent. See")
    a("`docs/COLLABORATION.md` §2.2-A for the independent ChatGPT-authored set.")
    a("")
    if "flagged_at_suspicious" in ch:
        a(M_HEAD)
        a(_m_row("Keyword baseline", ch["keyword_baseline"]))
        a(_m_row(f"ML @ Suspicious ({th['suspicious']})", ch["flagged_at_suspicious"]))
        a(_m_row(f"ML @ High Risk ({th['high']})", ch["flagged_at_high"]))
        a("")
    a("<details><summary>Every challenge message with its ML score (click to expand)</summary>\n")
    a("| id | label | language | pattern | ML score | ML-only verdict | text |")
    a("|---|---|---|---|---|---|---|")
    for it in ch["items"]:
        lab = {1: "scam", 0: "legit", None: "ambiguous"}[it["label"]]
        text = it["text"].replace("|", "/")
        text = text if len(text) <= 110 else text[:107] + "…"
        a(f"| {it['id']} | {lab} | {it['language']} | {it['pattern']} | {it['score']:.3f} | {it['ml_verdict']} | {text} |")
    a("\n</details>\n")
    for ce in m.get("contrib", []):
        a(f"### Independent set: `{ce['name']}`")
        a("")
        if "flagged_at_suspicious" in ce:
            a(M_HEAD)
            a(_m_row("Keyword baseline", ce["keyword_baseline"]))
            a(_m_row("ML @ Suspicious", ce["flagged_at_suspicious"]))
            a(_m_row("ML @ High Risk", ce["flagged_at_high"]))
            a("")
    a("## Demo library (ML-only scores; the app adds indicator fusion)")
    a("")
    a("| Sample | Example of | ML score | ML-only verdict |\n|---|---|---|---|")
    for s in m["demo_samples_ml_only"]:
        a(f"| {s['id']} | {s['example_of']} | {s['score']:.3f} | {s['ml_verdict']} |")
    a("")
    a(f"Demo samples found in training data: **{d['demo_samples_in_training']}**. "
      f"Challenge samples found in training data: **{d['challenge_samples_in_training']}**.")
    a("")
    a("## Thresholds (chosen on out-of-fold development scores only)")
    a("")
    a(f"- **Suspicious** ≥ {th['suspicious']}: {th['policy']['suspicious']}")
    a(f"- **High Risk** ≥ {th['high']}: {th['policy']['high']}")
    a("- The floors are a product decision. Synthetic data is easier than real SMS, so the thresholds aren't")
    a("  allowed to drop just because cross-validation scores were extreme.")
    a("")
    a("## Dataset & leakage controls")
    a("")
    a(f"- {d['rows_generated']} generated rows → {d['normalized_duplicates_dropped']} exact duplicates after normalisation removed → "
      f"**{d['rows_used']} rows** ({d['scam']} scam / {d['legit']} legit) from {d['families']} template families.")
    a(f"- Split by template family (StratifiedGroupKFold, 5 folds): 1 fold is the held-out **test** set "
      f"({d['split_sizes']['test']} rows, {d['split_families']['test']} families), and 4 folds are **development** data "
      f"({d['split_sizes']['dev_train_plus_val']} rows, {d['split_families']['dev_train_plus_val']} families) used for "
      f"grouped {d['cv_folds_in_dev']}-fold cross-validation and then for fitting the final model.")
    a("- Language mix (all rows): " + ", ".join(f"{k} {v}" for k, v in d["by_language"].items()) + ".")
    lk = m["leakage_checks"]
    a(f"- Shared families dev↔test: **{lk['shared_families_dev_test']}**; between any two folds: "
      f"{lk['shared_families_between_any_folds']}; identical normalised texts dev↔test: "
      f"**{lk['shared_normalized_texts_dev_test']}** (between any folds: {lk['shared_normalized_texts_between_any_folds']}).")
    nd = lk["near_duplicate_test_vs_dev"]
    a(f"- Near-duplicates (character TF-IDF cosine to the nearest development message): mean {nd['mean_cosine']}, max {nd['max_cosine']}, "
      f"{_pct(nd['share_test_above_0.9'])} of test messages above 0.9, {_pct(nd['share_test_above_0.8'])} above 0.8. "
      "Shared slot values (brand names, amounts) and common phrasing produce some similarity even across families.")
    a("- Vocabulary and IDF weights are fitted only on the training portion of each fit (never on test).")
    a("")
    a("## Model selection (grouped cross-validation on development data)")
    a("")
    sel = m["model_selection"]
    a(f"Criterion: {sel['criterion']}. Selected **{sel['selected']['config']}**, C={sel['selected']['C']}.")
    a("")
    a("| Config | C | Mean vocab | OOF log-loss | OOF AP | OOF ROC-AUC | OOF F1@0.5 |\n|---|---|---|---|---|---|---|")
    for r in sel["grid"]:
        a(f"| {r['config']} | {r['C']} | {r['vocab_size']:,} | {r['val_log_loss']} | {r['val_average_precision']} | {r['val_roc_auc']} | {r['val_f1_at_0.5']} |")
    a("")
    a("## What the model learned (largest weights)")
    a("")
    a("Character n-grams are shown with `·` for the word-boundary space. `zphonez` / `zurlz` / `zuanz` are placeholders")
    a("the normaliser substitutes for phone numbers, links and helpline (UAN) numbers.")
    a("")
    a("| Towards scam | weight | Towards legitimate | weight |\n|---|---|---|---|")
    for s, l_ in zip(m["top_features"]["towards_scam"][:20], m["top_features"]["towards_legit"][:20]):
        a(f"| `{s['feature'].replace(' ', '·')}` | {s['weight']} | `{l_['feature'].replace(' ', '·')}` | {l_['weight']} |")
    a("")
    a("## Export, parity and speed")
    a("")
    e, lat = m["export"], m["latency_ms_per_message_python"]
    a(f"- Exported JSON: {e['model_json_kb']} KB, {e['vocab_size']:,} features, weights rounded to 7 significant digits; "
      f"max |p_json − p_sklearn| on test = {e['json_vs_sklearn_max_abs_diff']:.2e}.")
    a("- TypeScript parity is checked by `apps/mobile/src/engine/__tests__/parity.test.ts` against "
      "`ml/artifacts/parity-fixtures.json` (normalised text must match exactly, and the score must match to within 1e-9).")
    a(f"- Python latency per message (dev container, not a phone): scikit-learn {lat['sklearn']} ms, "
      f"pure-Python JSON reference {lat['pure_python_json_reference']} ms. The app measures and shows real on-device latency.")
    a("")
    a("## Development history (honest record)")
    a("")
    a("The test fold was looked at after each of these runs, so the final numbers are not a perfectly \"blind\" estimate.")
    a("Changes between runs were driven by validation/cross-validation error analysis (more phrasings, more Urdu script,")
    a("more hard negatives, CV-based selection), not by editing templates to match specific test messages. The")
    a("hand-written challenge set and the independent ChatGPT set are the better guides to generalisation.")
    a("")
    a("| Run | Change | Test rows | ROC-AUC | Thresholds (susp/high) | Recall @Susp | FPR @Susp | Precision @High |")
    a("|---|---|---|---|---|---|---|---|")
    for h in m.get("history", []):
        a(f"| {h['run']} | {h['note']} | {h['test_rows']} | {h['roc_auc']} | {h['thresholds'][0]} / {h['thresholds'][1]} | "
          f"{_pct(h['recall_at_suspicious'])} | {_pct(h['fpr_at_suspicious'])} | {_pct(h['precision_at_high'])} |")
    fs_, fh_ = m["test"]["flagged_at_suspicious"], m["test"]["flagged_at_high"]
    a(f"| **v2 (shipped)** | grouped 4-fold CV for selection + thresholds; final fit on all dev data | {fs_['n']} | "
      f"{m['test']['roc_auc']} | {m['thresholds']['suspicious']} / {m['thresholds']['high']} | {_pct(fs_['recall'])} | "
      f"{_pct(fs_['false_positive_rate'])} | {_pct(fh_['precision'])} |")
    a("")
    a("## Known limitations")
    a("")
    a("- Synthetic data: real scams are more diverse, change over time, and include formats (voice calls, images) this model never sees.")
    a("- The model can be fooled by adversarial rewording. The indicator engine and the advice to always verify")
    a("  through official channels are the safety net.")
    a("- Small per-category test counts, so category-level numbers are indicative only.")
    a("- Next step: a consented pilot dataset of real, anonymised messages, labelled by fraud analysts.")
    a("")
    return "\n".join(lines) + "\n"
