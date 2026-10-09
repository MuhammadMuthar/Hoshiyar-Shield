# Hoshiyar Shield: Claude × ChatGPT Collaboration Agreement

**Read this before you touch the repository.** This is a working agreement
between two AI assistants, **Claude** (Claude Code, in a cloud session on this
repo) and **ChatGPT** (ChatGPT / Codex, used by the team). They work for the
human team, **Mutahar and Uswa**, who have final say on everything.

- Repository: `muhammadmuthar/hoshiyar-shield`
- Event: AICON'26 Build With AI, Financial Operations track
- Demo: **11 October 2026, 9:28–9:33 AM PKT** (5 minutes)
- Product: an Android app (Expo / React Native) that checks suspicious
  financial messages, links and payment numbers using a **trained on-device
  multilingual classifier** (Roman Urdu, English, Urdu script).

If you are ChatGPT and a human pasted this file into a chat, you can't push
to the repo. Put your output in the **exact file formats in §5** so a human (or
Claude) can drop it in without editing it.

---

## 1. Ground rules (both assistants)

1. **Be honest.** Never invent accuracy figures, user counts, money saved,
   statistics, deployments, or test results. If you didn't run it, say so.
2. **No fake AI.** Sample messages must go through the real classifier. Never
   hardcode a verdict for a demo message.
3. **Privacy.** Use no real people's names, phone numbers, CNICs, account
   numbers or real messages. Use fictional names, the placeholder number
   ranges in §6, and `.example` domains.
4. **No overclaiming.** The app does NOT read SMS automatically, intercept
   calls, block transfers in other apps, or guarantee that anything is safe.
   Never write copy that suggests otherwise. Use **"No Obvious Scam
   Detected"**, never "Safe" or "Guaranteed Safe".
5. **Respect ownership (§3).** Don't edit a file owned by the other assistant.
   Propose the change in `docs/HANDOFF.md` instead.
6. **Small, reviewable changes.** Each change should leave the repo with
   passing tests (§7).
7. **Cite sources.** Any real-world statistic needs a publisher, a date and a
   URL in `docs/sources.md` (§5.4), or it doesn't go in the pitch.

---

## 2. Division of work: who does what

The split plays to each assistant's strengths. Claude is working directly in
the repo with a shell, tests and the build. ChatGPT works on independent
authoring, research and review, which gives the project a **second
independent author**. That matters for honest ML evaluation (§2.2-A).

### 2.1 Claude owns (implementation, already in progress)

| Area | Paths |
|---|---|
| ML pipeline: dataset generator, training, evaluation, export | `ml/` (except `ml/data/contrib/`) |
| On-device inference engine (TypeScript), Python/TS parity | `apps/mobile/src/engine/` |
| Mobile app: screens, navigation, components, theme | `apps/mobile/src/` |
| Tests (pytest, Jest) | `ml/tests/`, `apps/mobile/src/**/__tests__/` |
| Build config: Expo, EAS, GitHub Actions APK build | `apps/mobile/app.json`, `apps/mobile/eas.json`, `.github/workflows/` |
| Technical docs | `docs/architecture.md`, `docs/model-evaluation.md`, `docs/dataset-card.md`, `docs/privacy.md`, `docs/limitations.md`, `docs/deployment.md` |
| First drafts of pitch & demo script | `docs/PITCH.md`, `docs/demo-script.md` |

### 2.2 ChatGPT owns (independent authoring, research, review)

**A. Independent challenge set (highest value, start here).**
Write 60–100 *new* test messages in `ml/data/contrib/chatgpt_challenge.jsonl`
(format §5.1). Claude wrote the training templates, so a set that Claude never
saw is a fairer test of whether the model generalises. Aim for:
- ~50% scams across all 8 categories (§6), including **patterns not in the
  list**, for example wrong-number refund requests, fake courier fees, fake
  Benazir Income Support Programme (BISP) payouts and fake job-registration fees.
- ~50% legitimate **hard negatives**: real-looking OTP deliveries that say
  "do not share", bank security advice, normal family money requests, shop
  payment reminders, legitimate loan ads, and messages with links.
- A mix of languages: roughly 40% Roman Urdu, 25% English, 20% Urdu script and
  15% code-switched. Use natural spelling variation (`paisay/pesa`,
  `foran/forun`, `bhejein/bhejo`).
- Some messages with obfuscation (`0TP`, `J@zzCash`, extra spaces, emojis).

The pipeline reads this file **only for evaluation, never for training**.
Claude will report the result in `docs/model-evaluation.md` as a separate
"independent author" score.

**B. Language quality review.**
Read `ml/data/templates/*.py` (Claude's templates) and the app's Roman Urdu
and Urdu copy. Flag anything that sounds unnatural to a Pakistani reader, and
give corrected text in `docs/HANDOFF.md`. Don't edit Claude's files directly.

**C. Urdu UI translations.**
Translate the English UI strings in `apps/mobile/src/i18n/en.ts` into
`apps/mobile/src/i18n/ur.ts` (same keys, same structure, format §5.3). Keep the
safety meaning exact. "No obvious scam detected" must not become "safe".

**D. Verified problem statistics.**
Research credible figures on financial and digital fraud in Pakistan, for
example from the State Bank of Pakistan, PTA, the FIA Cybercrime Wing (now
NCCIA) or reputable news reports. Record each one in `docs/sources.md`
(format §5.4) with the exact quote, publisher, date and URL. Mark anything you
couldn't verify as **UNVERIFIED** so it stays out of the pitch.

**E. Pitch polish and judge prep.**
After Claude's first draft of `docs/PITCH.md` lands, suggest edits to the
speaking script, slide visuals and likely judge questions in
`docs/HANDOFF.md`. Keep every claim consistent with
`ml/artifacts/metrics.json`. Never round numbers up.

**F. (Optional, P2) Web intelligence dashboard.**
If A–E are done, build a small static or Next.js dashboard in `dashboard/`
that reads `ml/artifacts/campaigns.json` (schema §5.5). Label it
**"Synthetic demo data"**. Don't add paid services or secrets.

### 2.3 Humans own (Mutahar & Uswa)

- Final review and merge of every change.
- Installing the APK on a real Android phone and running the demo checklist
  in `docs/demo-script.md`.
- Any account logins (Expo/EAS, GitHub settings) and the slide deck itself.
- Presenting.

---

## 3. File ownership map

| Path | Owner | The other assistant may… |
|---|---|---|
| `ml/data/contrib/**` | ChatGPT | read |
| `apps/mobile/src/i18n/ur.ts` | ChatGPT | read; Claude may create an empty stub |
| `docs/sources.md` | ChatGPT | read, cite |
| `dashboard/**` | ChatGPT | read |
| `docs/HANDOFF.md` | shared, **append-only** | append entries |
| `docs/PITCH.md`, `docs/demo-script.md` | Claude drafts, ChatGPT proposes edits via HANDOFF | – |
| Everything else | Claude | propose changes via HANDOFF |

If something needs to change in a file you don't own, write a HANDOFF entry
(§4). If it's urgent and the owner is unavailable, a human decides.

---

## 4. Handoff protocol

All coordination goes in **`docs/HANDOFF.md`**. It is append-only, newest
entry at the bottom. Use this template:

```markdown
### [YYYY-MM-DD HH:MM PKT] <Claude|ChatGPT|Mutahar|Uswa> — <short title>
- **Status:** done | in-progress | blocked | proposal
- **Changed:** <files>
- **Verified by:** <commands run + result, or "not run">
- **Needs from:** <who> — <what exactly>
- **Notes:** <anything the next person must know>
```

Branches and commits:
- Claude pushes to `claude/*` branches. ChatGPT/Codex should use
  `chatgpt/<topic>` branches. Humans merge into `main`.
- Commit prefix: `ml:`, `app:`, `engine:`, `docs:`, `data:`, `ci:`,
  `dashboard:`, `i18n:`.
- Don't rewrite another author's history. Don't force-push shared branches.

---

## 5. Interface contracts (exact formats)

### 5.1 Challenge / dataset rows: JSON Lines, one object per line

```json
{"id": "cg-0001", "text": "Mubarak ho! Apka 25,000 ka inaam nikla hai. Claim ke liye 500 fee is number 0399-5550101 pe bhejein.", "label": 1, "language": "roman_urdu", "category": "prize_lottery", "source": "chatgpt_authored", "synthetic": true, "template_family": "cg-prize-01", "notes": "classic prize + upfront fee"}
```

| Field | Values |
|---|---|
| `id` | unique, prefix `cg-` |
| `text` | the message (UTF-8; Urdu script allowed) |
| `label` | `1` = financial scam, `0` = legitimate / not a scam |
| `language` | `roman_urdu` \| `english` \| `urdu` \| `mixed` |
| `category` | one of §6 (scams) or `legit_*` (§6) |
| `source` | `chatgpt_authored` |
| `synthetic` | `true` |
| `template_family` | your own grouping id (same idea → same family) |
| `notes` | optional, short |

### 5.2 Model artifact (read-only for ChatGPT)
`ml/artifacts/hoshiyar-model.json` is produced by `ml/training/train.py`.
Don't hand-edit it. The app loads a copy from
`apps/mobile/assets/model/hoshiyar-model.json`.

### 5.3 UI strings: `apps/mobile/src/i18n/ur.ts`
```ts
import type { Strings } from './en';
export const ur: Strings = {
  // same keys as en.ts, values in Urdu script
};
```

### 5.4 Sources: `docs/sources.md`
```markdown
| # | Claim (exact figure) | Publisher | Date published | URL | Exact quote | Status |
|---|---|---|---|---|---|---|
| 1 | ... | State Bank of Pakistan | 2026-03-01 | https://... | "..." | VERIFIED |
```

### 5.5 Campaign clusters: `ml/artifacts/campaigns.json`
```json
{
  "generated_from": "synthetic demo reports",
  "is_synthetic": true,
  "campaigns": [
    {
      "campaign_id": "C-01",
      "report_count": 12,
      "dominant_category": "prize_lottery",
      "representative_pattern": "Mubarak ho! Apka <AMOUNT> ka inaam ... fee <PHONE> pe bhejein",
      "first_seen": "2026-09-14",
      "last_seen": "2026-10-06",
      "top_terms": ["inaam", "fee", "claim"]
    }
  ]
}
```

---

## 6. Shared vocabulary

**Scam categories** (`label: 1`):
`prize_lottery`, `otp_pin_theft`, `impersonation`, `loan_fee`,
`payment_request`, `account_suspension`, `investment`, `refund_reversal`

**Legitimate categories** (`label: 0`):
`legit_transaction_alert`, `legit_otp_delivery`, `legit_security_advice`,
`legit_conversation`, `legit_payment_reminder`, `legit_loan_ad`,
`legit_business_payment`, `legit_url_info`, `legit_promo`

**Risk levels shown to users:** `HIGH RISK` · `SUSPICIOUS` ·
`NO OBVIOUS SCAM DETECTED`

**Placeholder data:**
- Phone numbers: use only `0399-555xxxx` (e.g. `0399-5550101`). Demo
  reputation records use this range and are labelled as fictional.
- Domains: `*.example` only (e.g. `jazzcash-verify.example`).
- Names: fictional (e.g. "Ahmed Raza", "Sana Tariq").
- Brands such as JazzCash, Easypaisa, HBL and Meezan may appear in scam
  *messages*, because impersonation is the threat being modelled. Never imply
  the brand endorses the app.

---

## 7. Definition of "done" for any change

Run what applies before writing "done" in HANDOFF:

```bash
# ML (from repo root)
.venv/bin/python -m pytest ml/tests -q
.venv/bin/python ml/training/train.py          # regenerates artifacts + metrics

# App (from apps/mobile)
npm run typecheck && npm run lint && npm test
```

If you couldn't run them (for example in ChatGPT chat), write
**"Verified by: not run"**. That's fine. Pretending isn't.

---

## 8. Priorities and freeze points

- **P0:** the real classifier works on the phone, a Roman Urdu scam gets a
  HIGH RISK result, and a legitimate message doesn't.
- **P1:** polish, link checker, number checker, report flow, APK, pitch.
- **P2:** dashboard, clustering visuals, Urdu UI toggle, share-intent.
- **Feature freeze:** 10 Oct 2026, 20:00 PKT. After that, only bug fixes,
  tests, docs and rehearsal.
- **Final APK and demo rehearsal:** 10 Oct 2026, 23:00 PKT.

## 9. Where things are

See `README.md` for setup and `docs/HANDOFF.md` for the live status log.
