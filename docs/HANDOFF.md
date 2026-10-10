# Handoff Log (append-only)

Shared status log between Claude, ChatGPT and the human team. Protocol and
entry template: [`COLLABORATION.md` §4](./COLLABORATION.md#4-handoff-protocol).
Newest entry at the bottom. Never delete or rewrite earlier entries.

---

### [2026-10-10 05:00 PKT] Claude — Repository scaffold + collaboration agreement
- **Status:** done
- **Changed:** `.gitignore`, `.env.example`, `AGENTS.md`, `docs/COLLABORATION.md`, `docs/HANDOFF.md`, `apps/mobile/` (Expo SDK 57 scaffold)
- **Verified by:** `npm install` in `apps/mobile` succeeded; no app code yet
- **Needs from:** ChatGPT, start on COLLABORATION §2.2-A (independent challenge set) and §2.2-D (verified sources). Both are independent of Claude's in-progress work.
- **Notes:** Claude is now building the ML pipeline (`ml/`) and then the on-device engine and app.

### [2026-10-10 05:03 PKT] ChatGPT — Independent evaluation and source research started
- **Status:** in-progress
- **Changed:** `docs/HANDOFF.md` (this entry)
- **Verified by:** fetched Claude's scaffold; read root/mobile `AGENTS.md`, `docs/COLLABORATION.md` and this handoff; working tree was clean
- **Needs from:** Claude — continue the ML pipeline and app; publish the English translation keys, templates and pitch when available for the later review tasks
- **Notes:** Work is on `chatgpt/challenge-and-sources`, based on `4bd56a0`. Preparing an 80-message independent challenge set and verified sources in parallel. No training templates or model predictions have been inspected before authoring this set. Contributed messages must remain evaluation-only. All coordination is via this append-only log; implementation ownership remains unchanged.

### [2026-10-10 05:03 PKT] ChatGPT — Independent challenge v1 ready for evaluation
- **Status:** done
- **Changed:** `ml/data/contrib/chatgpt_challenge.jsonl`, `ml/data/contrib/validate_challenge.py`, `ml/data/contrib/README.md`, `docs/HANDOFF.md` (appended entries only)
- **Verified by:** `python3 ml/data/contrib/validate_challenge.py` — PASS: 80 unique messages, 40 scam / 40 legitimate, 32 Roman Urdu / 20 English / 16 Urdu / 12 mixed, five scams per category, all nine legitimate categories, 48 families, placeholder checks; `git diff --check` — PASS. Separate read-only Codex review checked labels, language and family grouping; corrections applied before freezing.
- **Needs from:** Claude — integrate the JSONL strictly as evaluation-only input after model/threshold fitting; run the ML tests and evaluation and report this set separately, with counts and checksum, in `docs/model-evaluation.md`. Human review/merge remains required.
- **Notes:** SHA-256: `7705733cdddef693935535866131aebbb86497d4253187e5eb0d66437f46f4ff`. No training templates or predictions were inspected before authoring/finalizing this set. No classifier metrics are claimed. `ml/training/train.py`, `ml/tests/`, app source, English i18n keys and pitch are not present in the available scaffold; ML/app suites were not run, and language review, Urdu translation and pitch review await Claude's files. Short legitimate messages carry author-assigned synthetic contexts, not verified sender identity. See the contributor README for reproducible checks and limitations. The earlier start-entry heading `05:03 PKT` was a timestamp typo; work started at approximately `04:57 PKT`.

### [2026-10-10 05:03 PKT] ChatGPT — Source research blocked by outbound access
- **Status:** blocked
- **Changed:** `docs/sources.md`; environment network draft (outside the repository)
- **Verified by:** HTTPS source fetches to SBP, PTA, FIA, NCCIA and Dawn returned proxy `Tunnel connection failed: 403 Forbidden`; source-ledger table structure checked, five UNVERIFIED research leads, no invented figures or quotes; network draft save confirmed.
- **Needs from:** Mutahar/Uswa — review and save the five research-host additions in environment settings, then publish the environment. ChatGPT can retry retrieval once the new policy is applied; no secret is needed.
- **Notes:** Added `www.sbp.org.pk`, `www.pta.gov.pk`, `www.fia.gov.pk`, `www.nccia.gov.pk`, `www.dawn.com`, preserving package-manager presets. Saving did not apply or publish the network policy. All source rows are discovery leads, not verified publications. Keep numeric problem-scale claims out of the pitch until exact figures, dates and quotations are retrieved.
