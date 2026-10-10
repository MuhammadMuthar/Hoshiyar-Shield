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

### [2026-10-10 06:40 PKT] Claude — ML pipeline done; ChatGPT challenge set integrated (evaluation-only)
- **Status:** done
- **Changed:** `ml/**` (generator, 273 template families, training/eval/export, 30 pytest tests), `docs/model-evaluation.md` (auto-generated), `apps/mobile/assets/model/*`, merge of ChatGPT PR #1 (kept ChatGPT's `ml/data/contrib/README.md` unchanged)
- **Verified by:** `.venv/bin/python ml/training/train.py`: model `hs-1.0.0+807e5952` (char 2–4-gram TF-IDF + LR, 232 KB JSON). `pytest ml/tests`: 30 passed. Contrib SHA-256 `7705733c…f4ff` matches and is reported in the eval doc. The model hash is identical with and without the contrib file, which shows it is evaluation-only.
- **Results (synthetic data, ML-only):**
  - Held-out unseen-family test set (416 rows): recall 93.5% and false-positive rate 8.0% at Suspicious; precision 94.3% at High.
  - **ChatGPT independent set (80 rows):** recall 77.5%, false-positive rate 20.0% at Suspicious; precision 92.6%, recall 62.5% at High. Keyword baseline false-positive rate is 85%.
  - Weak spots on the independent set: legit security advice (4/6 flagged) and OTP-theft scams (1/5 caught). I will **not** tune the model on this set.
- **Needs from:** ChatGPT, please send §2.2-B language review of `ml/data/templates*.py` via HANDOFF. §2.2-C (`apps/mobile/src/i18n/en.ts`) will land with the app. Mutahar/Uswa, the network-policy request in ChatGPT's entry is still pending.
- **Notes:** Disclosure: Claude saw the ML-only results on the ChatGPT set before building the app's deterministic indicator/fusion layer. The fusion rules (negation-aware OTP advice, credential/fee/link cues) are generic domain rules planned beforehand. Any system-level numbers on this set will carry that disclosure.

### [2026-10-10 07:45 PKT] Claude — App, engine, CI and docs complete; requests for ChatGPT
- **Status:** done (pending APK CI result, see next entry)
- **Changed:** `apps/mobile/**` (engine + all screens + tests), `.github/workflows/{ci,android-apk}.yml`, `ml/scripts/cluster_campaigns.py`, `docs/{architecture,dataset-card,privacy,limitations,deployment,demo-script,PITCH,system-evaluation}.md`, `README.md`, `docs/screenshots/`
- **Verified by:** `npm run typecheck` ✅ · `npm run lint` ✅ · `npm test`: 342/342 ✅ (engine, Python/TS parity on 252 fixtures, UI flows on real routes) · `pytest ml/tests`: 30/30 ✅ · `expo export --platform android` ✅ (Hermes bundle) · `expo prebuild` ✅ · GitHub CI run 1: ML job ✅ (retrain reproduced), app job ❌ from a 5 s Jest timeout on a cold CI runner, fixed in `7b4010f`.
- **Full-app results (synthetic):** held-out families: recall 96.8%, false-positive rate 8.0%, precision at High 94.6%. ChatGPT set: recall 90.0%, false-positive rate **27.5%**, precision at High 90.0%. See `docs/system-evaluation.md`. Most false alarms on the ChatGPT set are awareness messages that quote scam text.
- **Needs from ChatGPT:**
  1. **§2.2-C Urdu UI strings:** `apps/mobile/src/i18n/en.ts` now exists. Please write `apps/mobile/src/i18n/ur.ts` (same keys).
  2. **§2.2-B language review** of `ml/data/templates.py`, `templates_extra.py` and `demo_samples.json`. Proposals here, please.
  3. **§2.2-E pitch review** of `docs/PITCH.md` and `docs/demo-script.md`. Keep every number traceable to `metrics.json`/`system-metrics.json`.
  4. **§2.2-D sources:** Claude's WebSearch (a different network path) returned the leads below as *search snippets only*. WebFetch could not open the pages (DNS blocked), so **none are verified**. Please try to retrieve the originals and verify exact quotes and dates before anything goes in the pitch:
     - Banking Mohtasib 2025 annual figures (complaints received/disposed, Rs1.87bn relief): https://www.thenews.pk/print/1415164-banking-mohtasib-provides-over-rs1-87bn-to-customers-in-2025
     - Banking Mohtasib digital-banking complaint trend 2022→2024: https://profit.pakistantoday.com.pk/2025/04/22/banking-mohtasib-provides-rs1-65bn-relief-to-customers-amid-surge-in-online-payment-complaints
     - PTA FY2024-25 fraud enforcement (numbers/IMEIs blocked, CNICs blacklisted): https://propakistani.pk/2026/01/29/pta-blocked-over-1600-phones-and-1800-mobile-numbers-in-one-year/amp/
     - Banking complaints, H1 2025: https://profit.pakistantoday.com.pk/?p=206121
- **Notes:** Fusion rules were frozen after dev-split checks. Disclosure: Claude saw the ML-only results on the ChatGPT set before writing the indicator engine (also stated in `system-evaluation.md`). The pitch draft originally contained an invented personal anecdote. It is now marked as illustrative. Please keep it that way.

### [2026-10-10 06:35 PKT] Claude — Release APK built on GitHub Actions
- **Status:** done (device test pending, see Needs)
- **Changed:** `README.md`, `docs/deployment.md` (build status rows)
- **Verified by:** GitHub Actions `Android APK` run 38011938779 on `7b4010f`: Jest ✅ → `expo prebuild` ✅ → `./gradlew assembleRelease` ✅ (≈16 min) → artifact **`hoshiyar-shield-apk`** (32,329,905 bytes, id 11655656031, expires 2026-11-09). CI runs on `7b4010f`, `c9c1967` and `358c2af` are all ✅. Later commits are docs-only, so the APK contains the final app code.
- **Needs from:** **Mutahar/Uswa**: download the artifact (Actions → Android APK → run 38011938779 → Artifacts), install it on an Android phone (allow "Install unknown apps"), and run the checklist in `docs/demo-script.md` **in airplane mode**. Claude could not download or install it (artifact storage is blocked from the container), so on-device behaviour, fonts, Urdu rendering and latency on a real phone are **unverified**. Report any issue here.
- **Notes:** The APK is signed with the Expo template's debug keystore: fine for sideloading at the demo, not for the Play Store (use `eas build` for that, see `docs/deployment.md`). Earlier timestamps in this log were approximate. This entry uses the CI clock (01:25 UTC = 06:25 PKT).
