# Independent ChatGPT challenge set, v1

`chatgpt_challenge.jsonl` contains **80 synthetic, independently authored
evaluation messages**. It follows `docs/COLLABORATION.md` §5.1 and is for
evaluation only. Do not include these rows in training, feature fitting,
vocabulary/IDF fitting, calibration, threshold selection or template generation.

## Composition

| Language | Scam | Legitimate scenario | Total |
|---|---:|---:|---:|
| Roman Urdu | 16 | 16 | 32 |
| English | 10 | 10 | 20 |
| Urdu script | 8 | 8 | 16 |
| Code-switched (`mixed`) | 6 | 6 | 12 |
| Total | 40 | 40 | 80 |

Each of the eight scam categories has five messages. All nine agreed
`legit_*` categories are represented. The set includes wrong-number refunds,
unsolicited courier fees, fake BISP/relief payouts, job-registration fees,
credential requests through voice notes, payment approvals disguised as
refunds, and investment withdrawals conditioned on further payments or
recruitment. Obfuscated spelling, spaces, emojis, links and routine urgency
also appear in legitimate scenarios, so those features alone do not determine
the label.

There are **48 `template_family` groups**. Close translations or variations of
the same idea share a family; 80 rows must not be treated as 80 independent
fraud mechanisms. Preserve both `id` and `template_family` when reporting
errors or sampling results.

## Provenance and limitations

- Authored on 10 October 2026 (PKT), from the collaboration contract at
  scaffold commit `4bd56a02cbe878958b53715aa7d70bf1823f88ea`. The author and
  reviewing Codex agent did not inspect training templates or model
  predictions before finalizing this version. They knew the project brief,
  category vocabulary and contract example. This is a separate authoring
  pass, not an external human annotation study or a claim of statistical
  independence.
- All messages, amounts, codes and scenarios are fictional. Phone numbers
  use only `0399-555xxxx`; domains use only `.example`. Brand names in
  impersonation examples do not imply endorsement.
- Labels describe author-assigned scenarios, not authenticated senders or
  verified transactions. A short family request or transaction alert cannot
  be proved legitimate from its text. In particular, the ordinary urgent
  requests in `cg-0043`, `cg-0044`, `cg-0071` and `cg-0078` are negative
  scenarios by construction; the app must still avoid claiming they are safe.
- This is a small, curated, balanced challenge set, not a representative
  sample of Pakistani messages or real-world scam prevalence. Many scams
  deliberately contain several explicit cues. Many negatives contain
  protective advice, although several ordinary alerts, reminders and
  requests omit such disclaimers. The set is not a full robustness audit.
- Roman Urdu and Urdu received a second model-based language review, not
  an independent native-speaker sign-off. Human review remains valuable.
- No classifier has been run on these rows in this contribution. Schema
  validation, language review and label review are **not accuracy results**.

## Reproduce the data checks

From the repository root, with Python 3.11 or newer and no third-party
dependencies:

```bash
python3 ml/data/contrib/validate_challenge.py
```

The validator checks JSONL shape, unique ordered IDs and texts, exact v1
class/language counts, category coverage, provenance flags, family identifiers,
domain suffixes and long-number placeholders. It cannot establish real-world
truth, native fluency, all forms of personal data, or classifier quality.

Frozen v1 SHA-256 of `chatgpt_challenge.jsonl`:

```text
7705733cdddef693935535866131aebbb86497d4253187e5eb0d66437f46f4ff
```

## Integration handoff to Claude

1. Keep this file outside every training/fitting path. Read it only after
   fitting the existing model and freezing preprocessing and thresholds.
2. Pass only each row's `text` to inference. Labels, notes, language,
   category, IDs and family names are evaluation metadata, never features.
3. Report it separately as the **synthetic independent-author challenge
   set**, with this checksum, model revision, total evaluated row count,
   confusion matrix, scam precision/recall and macro F1. Include counts by
   language and scam category; five cases per scam category are too few for
   strong subgroup conclusions. If any cases fail to run, report them rather
   than silently dropping them.
4. Do not select thresholds, rewrite failed messages or add copies to
   training to improve this score. If findings inform model changes, state
   that the set has become a development set and obtain new unseen examples
   for a fresh holdout evaluation.
5. Run the repository ML tests and training/evaluation command when the
   pipeline lands. At this scaffold revision, `ml/training/train.py` and
   `ml/tests/` are absent, so end-to-end ingestion and model behavior remain
   untested. Do not substitute the data validator for those checks.

If a label or spelling needs correction, document it as a new version before
evaluation, preserve old results with their original checksum, and keep
model-driven edits separate from independent authoring.
