# Architecture

## One-line summary
A message is analysed entirely on the phone: **normalise → ML score → deterministic warning cues
→ structural URL analysis → explicit fusion → explanation and safe actions.** The ML model is trained in
Python and shipped as JSON. TypeScript reimplements the inference exactly.

```
                ┌────────────────────────── PHONE (no network needed) ──────────────────────────┐
 user pastes →  │ normalize.ts ─┬─▶ classifier.ts (TF-IDF + LR, 8,973 features) ─▶ score + top words │
 / types /      │  (spec shared │                                                                   │
 demo sample    │   with Python)└─▶ indicators.ts (negation-aware cues) ──┐                         │
                │                   url.ts (structure only, never opens) ─┼─▶ analyze.ts fusion F1–F4│
                │                   phone.ts (PK number normalisation) ───┘        │                 │
                │                                                                  ▼                 │
                │                                         Result screen: level, reasons, actions    │
                │   reputation.ts (demo + local reports) ◀── Number screen     reports.ts ◀── Report │
                └───────────────────────────────────────────────────────────────────────────────────┘
 OFFLINE, IN THE REPO:  ml/data (templates → dataset) → ml/training/train.py (grouped CV, test, export)
                        → hoshiyar-model.json + parity fixtures + metrics → copied into apps/mobile/assets
```

## Components

| Layer | Path | Responsibility |
|---|---|---|
| Normaliser (spec) | `ml/training/textnorm.py` ↔ `apps/mobile/src/engine/normalize.ts` | Whitespace/zero-width cleanup, full-width → ASCII, Urdu digits → ASCII, ASCII lower-case, e-mail/URL/UAN/phone → placeholder tokens, de-leet (`0TP`, `j4zzc4sh`, `p@ss`), Urdu letter canonicalisation, digit → `0`, everything else → space. Written to be **exactly portable**: no `\s \d \w \b`, no look-behind, per-code-point processing. |
| Features | same files, `analyze()` | Word-bounded character n-grams (2–4 for the shipped model) on the normalised text. |
| Classifier | `ml/training/train.py` → `src/engine/classifier.ts` | TF-IDF (sublinear tf, smooth idf, L2) + logistic regression. TS mirrors the Python reference (`jsonmodel.py`) operation by operation. It also returns per-word contributions, which decompose a linear model's score exactly. |
| Indicator engine | `src/engine/indicators.ts` | Deterministic, sentence-level, **negation-aware** cue extraction (credential requests vs protective advice, advance fees, safe accounts, remote access, guaranteed returns, wrong-transfer tricks, new-number relatives, urgency, threats, institution mentions, links). These are concrete facts about the text. They are **not** presented as an explanation of the ML model. |
| URL analyser | `src/engine/url.ts` | Own parser (React Native's `URL` polyfill is incomplete). Checks scheme, IP hosts, `@` userinfo trick, punycode/non-ASCII, shorteners, risky TLDs, sub-domain depth, ports, encodings, brand keywords on unofficial domains, look-alikes (edit distance ≤ 2, digit substitution) against a small official-domain reference list. Never fetches. |
| Fusion | `src/engine/analyze.ts` | Rules below. Every result carries a `fusion` audit trail shown under "Technical details". |
| Phone & reputation | `src/engine/phone.ts`, `reputation.ts` | `+92 3XX XXXXXXX` normalisation; report lookup over labelled synthetic demo records + the user's local reports; wording never accuses. |
| Reports | `src/engine/reports.ts`, `src/features/reports.ts` | Validation (target, category, consent, no CNIC/card numbers in text), local rate limiting (5/hour, 10 s apart), AsyncStorage persistence. |
| Clustering | `ml/scripts/cluster_campaigns.py` | Char n-gram TF-IDF + agglomerative clustering (cosine, average linkage, threshold 0.75) over 157 **simulated** reports → `campaigns.json`. |
| UI | `src/app/*` (Expo Router) | Onboarding, tabs (Home, Scan, Link, Number, Intel), Result, Report, About/Settings. |

## Risk fusion rules (explicit and tested)

Thresholds come from the model artifact (`suspicious ≥ 0.73`, `high ≥ 0.90`, chosen on
out-of-fold development scores; see `model-evaluation.md`).

| Rule | Condition | Effect |
|---|---|---|
| **F1** | ML score vs thresholds | Base level LOW / SUSPICIOUS / HIGH |
| **F2** | ≥ 2 high-severity cues | → HIGH |
|  | exactly 1 high-severity cue | → at least SUSPICIOUS; HIGH if F1 was already SUSPICIOUS+ |
| **F3** | a medium-severity **action** cue (asks you to pay, call, return money, …) **and** (another medium/high cue **or** ML score ≥ 0.20) | → at least SUSPICIOUS |
| **F4** | level is HIGH **and** the message contains protective security advice **and** nothing asks you to act | capped at SUSPICIOUS |

Design constraints: fusion **never lowers a result to LOW** and never hides the ML score. Rules were
checked only against the development split (see `system-evaluation.md` for the disclosure about
what was seen when). Tests: `src/engine/__tests__/analyze.test.ts`.

High-severity cues: `credential_request`, `credential_on_link`, `upfront_fee_for_benefit`,
`safe_account`, `remote_access`, `guaranteed_returns`, `suspicious_link`.
Medium action cues: `payment_demand`, `transfer_to_number`, `contact_request`, `personal_data`,
`new_number_money`, `wrong_transfer_return`, `risky_link`, `link_action`.

## Why this model (and not a transformer)?

- Roman Urdu spelling varies a lot. Overlapping character n-grams share most features across variants,
  without a hand-built dictionary.
- It runs in about 1–4 ms on-device in pure TypeScript, needs no native ML runtime (it works in Expo
  Go), and fits in a 232 KB JSON file.
- It is linear, so the per-word explanation is faithful to the model.
- We compared it against a keyword baseline and a word+char variant (results in `model-evaluation.md`).
  A multilingual transformer would need a GPU for training, much larger on-device files and a native
  runtime. It is a sensible next step once real, consented data exists.

## Data flow & storage

| Data | Where | When |
|---|---|---|
| Message text | memory only (`features/session.ts`) | while viewing a result |
| Recent checks | AsyncStorage `hs.history.v1` | **only** if the user enables it; 48-char preview |
| Reports | AsyncStorage `hs.reports.v1` | when the user saves one; message text only if opted in |
| Preferences | AsyncStorage `hs.prefs.v1` | onboarding flag, toggles |

No backend is required. An optional reporting backend is described in `deployment.md` as future work.

## Testing map

| Area | Tests |
|---|---|
| Normalisation, analyzer, dataset provenance, leakage, artifact behaviour | `ml/tests/*.py` (pytest, 30) |
| Python ⇄ TS parity (252 fixtures) | `src/engine/__tests__/parity.test.ts` |
| URL, phone, reports, reputation, indicators, fusion, edge cases, offline | `src/engine/__tests__/*.test.ts` |
| System-level evaluation | `src/engine/__tests__/system-eval.test.ts` |
| UI flows on real routes (onboarding, scan → result, paste, samples, link, number, report, intel, about) | `__tests__/app-flows.test.tsx` |
