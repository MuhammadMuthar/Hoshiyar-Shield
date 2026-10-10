# Dataset Card: Hoshiyar Shield financial-scam SMS dataset (v1)

## Summary
| | |
|---|---|
| Purpose | Train and evaluate a binary classifier: **financial scam (1)** vs **legitimate / not a scam (0)** |
| Size | 2,457 generated rows → **2,080** after removing exact duplicates *after normalisation* |
| Balance | 1,084 scam · 996 legitimate |
| Families | **273** template families (each family = one message idea with 2–3 phrasings) |
| Languages | English 684 · Roman Urdu 650 · code-switched (`mixed`) 425 · Urdu script 321 |
| Provenance | 100% **synthetic**, written by the team's AI collaborator (Claude) from domain knowledge. No real messages, people or numbers. |
| Generator | `ml/data/generate_dataset.py` (seed 20261011), templates in `ml/data/templates.py` and `templates_extra.py` |
| Files | `ml/data/generated/dataset.jsonl` (rows), `ml/data/generated/splits.csv` (fold assignment) |

## Schema (one JSON object per line)
`id`, `text`, `label` (0/1), `label_name`, `language` (`roman_urdu`/`english`/`urdu`/`mixed`),
`category`, `source` (`synthetic_template`), `synthetic` (true), `template_family`, `author`.

## Categories
**Scam (label 1):** `prize_lottery`, `otp_pin_theft`, `impersonation`, `loan_fee`, `payment_request`,
`account_suspension`, `investment`, `refund_reversal`.

**Legitimate (label 0):** `legit_transaction_alert`, `legit_otp_delivery`, `legit_security_advice`,
`legit_conversation`, `legit_payment_reminder`, `legit_loan_ad`, `legit_business_payment`,
`legit_url_info`, `legit_promo`.

Ordinary advertising (`legit_promo`) is **not** treated as fraud. The label means *financial scam*, not spam.

## Deliberate hard negatives
Genuine-looking OTP deliveries ("…is your OTP. Do not share it"), bank and telecom security advice
(which mentions prizes, fees, OTPs and "safe accounts"), "Mubarak ho" family messages, legitimate loan
approvals and refund notices, legitimate lucky draws "with no fee", known-shop advance payments, and
family money transfers. Brand names (JazzCash, HBL, …) appear in both classes, so a brand mention can't
act as a shortcut.

## Variation and noise
- Slots: amounts in several formats (`Rs. 5,000`, `5 lakh`, `PKR`), wallets/banks, fictional names,
  placeholder phones, `.example` links, OTPs, dates.
- Roman Urdu spelling variants (`hai/he/hy`, `apka/aapka/ap ka`, `bhejein/bhejain/bhejo`, …), 40% per word.
- Noise applied **with the same probabilities to both labels**: case changes, missing punctuation, extra
  spaces, emoji, leetspeak. This stops the model from learning "typos = scam".

## Splits and leakage controls
- 5 folds by **template family** (StratifiedGroupKFold). Fold 0 = **test** (416 rows, 55 families); folds 1–4 =
  development data (1,664 rows, 218 families) for grouped 4-fold CV and the final fit.
- Verified: 0 shared families and 0 identical normalised texts between any folds. Test-to-dev nearest-neighbour
  cosine (char TF-IDF): mean 0.40, max 0.80, 0% above 0.8.

## Separate evaluation-only sets
| Set | Author | Size | Use |
|---|---|---|---|
| `ml/data/challenge_set.py` | Claude, separately from the templates | 65 (60 labelled + 5 ambiguous) | unfamiliar patterns (job/visa fees, customs parcels, crypto tax, Hajj ballots, fake buyers, obfuscation) |
| `ml/data/contrib/chatgpt_challenge.jsonl` | ChatGPT, **without seeing templates or model outputs** | 80 (40/40), SHA-256 `7705733c…f4ff` | independent-author estimate |
| `ml/data/demo_samples.json` | team | 10 | presentation library (verified not in training) |

## Known limitations of this dataset
- Synthetic: real scam traffic is more varied, evolves weekly, and includes images and voice.
- A single author wrote all the templates, so stylistic bias is likely. The independent ChatGPT set exists to expose that.
- Urdu-script and Roman Urdu text were written by an AI and have not been reviewed by native speakers
  (ChatGPT's language review is requested in `COLLABORATION.md` §2.2-B).
- Placeholder phone range `0399-555xxxx` is believed to be unallocated but not formally verified.
- No real-world prevalence: the 52/48 class balance is a design choice.

## Licence & ethics
Created for this project; no third-party data. Public datasets such as the UCI SMS Spam Collection were
considered but not used: they are mostly English *advertising* spam rather than financial fraud, and the
build environment couldn't download them.
