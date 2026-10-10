# PITCH: Hoshiyar Shield (5 minutes)

**AICON'26 Build With AI · Financial Operations · 11 Oct 2026, 9:28–9:33 PKT · Mutahar & Uswa**

> Rule for this pitch: every number on a slide must come from `ml/artifacts/metrics.json`,
> `ml/artifacts/system-metrics.json` or a **VERIFIED** row in `docs/sources.md`. As of this draft,
> **no external statistic is verified**, so the problem section uses a story, not numbers.

## Outline (slides)
| # | Time | Slide | Visual |
|---|---|---|---|
| 1 | 0:00–0:35 | **"Imagine Ammi gets this"**: the problem | A Roman Urdu prize-fee SMS on a phone screen |
| 2 | 0:35–1:00 | **Hoshiyar Shield**: the pipeline | Paste → on-device AI → warning cues → verdict + safe action |
| 3 | 1:00–2:30 | **Live demo** | Phone mirrored (airplane mode visible) |
| 4 | 2:30–3:20 | **Financial intelligence** | Number check (DEMO data) + campaign clusters (SIMULATED) |
| 5 | 3:20–4:15 | **The AI, honestly** | Baseline vs ML vs full app table; Python ⇄ TS parity; limitations |
| 6 | 4:15–5:00 | **Impact & ask** | Banks/wallets pilot; SDG 16.4 & 8.10; one-line vision |

---

## Full speaking script

### 0:00–0:35 · Problem *(Mutahar)*
> "Imagine your mother gets this message: *'Mubarak ho! Apka 5 lakh ka inaam nikla hai. Verification fee
> bhejein.'* It uses a TV show she watches, a number that looks normal, and the language she actually
> texts in: Roman Urdu. *(This example is illustrative, not a real case.)*
> Scammers in Pakistan don't hack systems. They hack trust: fake JazzCash 'account blocked' alerts, a 'bank
> officer' asking for the code you just received, a relative 'on a new number' who needs money now.
> Spam filters are built for English keywords. But *paisay, pesay, paise* and *bhejein, bhejain, bhejo* are all
> the same word, and a real bank OTP message contains the same words as a scam."

*(Optional, only if a row in `docs/sources.md` is VERIFIED: one sentence with the figure, publisher and date.)*

### 0:35–1:00 · Solution *(Uswa)*
> "Hoshiyar Shield is an Android app that tells you, **before you pay**, whether a financial message, link or
> payment number looks like a scam, in Roman Urdu, Urdu and English. You paste the message. A trained AI model
> **on your phone** scores it, a rule engine finds concrete warning signs, and you get a clear verdict, the
> reason, and what to do. Nothing is uploaded, and it works in airplane mode, which is how this phone is set
> right now."

### 1:00–2:30 · Live demo *(Uswa drives, Mutahar narrates; see `demo-script.md`)*
1. Paste a **new** Roman Urdu prize-fee scam (not from the sample list) → **High Risk**. Read the reason: *"It promises money but asks you to pay first: the classic advance-fee scam."*
2. Scroll: warning signs, then **"What the AI model saw"**: the words that pushed *the model's* score up. *"These come from the model's own weights, not from a keyword list."*
3. Point at *"Analysed on this phone in 3 ms · no internet used."*
4. **Real bank OTP message** → **No Obvious Scam Detected**. *"It contains OTP, share and a bank name. A keyword filter flags it. Ours sees that it says 'never share'. And we never say 'safe', only 'no obvious scam detected'."*
5. **Urdu-script** sample → High Risk, rendered right-to-left.
6. **Wrong transfer?** → **Suspicious**. *"When it's genuinely unclear, we say: check your balance in the official app first."*

### 2:30–3:20 · Financial intelligence *(Mutahar)*
> "Before sending money, you can check the number. *(Number tab → 0399-5550142)* 'Three reports describe
> suspicious prize-fee requests associated with this number.' It never says 'fraudster', and an unreported
> number is **not** called safe. These three records are clearly labelled demo data.
> Now imagine thousands of consented reports. *(Intel tab)* Our clustering groups differently worded messages
> into campaigns, for example 18 reports of one OTP-theft script. Fraud teams could review **one campaign
> instead of hundreds of complaints**. This screen uses **simulated** data, and it says so on screen."

### 3:20–4:15 · The AI, honestly *(Uswa)*
> "We trained a character n-gram TF-IDF and logistic-regression model on 2,080 messages from 273 template
> families: scams, plus the hard part, legitimate OTPs, security advice and 'Mubarak ho' family messages.
> Character n-grams handle Roman Urdu spelling. We test only on **message families the model never saw**.
>
> On those held-out families, a keyword baseline raised false alarms on **48%** of legitimate messages. Our full
> app caught **96.8%** of scams at **8%** false alarms, with **94.6%** precision at High Risk.
> Our teammate ChatGPT wrote 80 messages **without seeing our data**. There we catch 90% of scams, but false
> alarms rise to 27.5%, mostly awareness messages that quote scams. All of this is synthetic. Real-world
> accuracy is **not measured yet**, and that's our next step.
> One more thing: the same model runs in Python and on the phone, and we verified both give identical results
> on 252 test messages."

### 4:15–5:00 · Impact & close *(Mutahar)*
> "Who adopts this? Banks and wallets, as a 'check before you pay' feature in their apps and as a feed of
> consented scam reports for their fraud teams. Telecoms, to spot campaigns early. It costs almost nothing to
> run: no servers, no GPU, and private by design.
> It supports **SDG 16.4**, fighting organised crime and illicit financial flows, and **SDG 8.10**, financial
> inclusion, because people only adopt digital payments they trust.
> Our ask: a pilot with one bank or wallet, using consented real messages, to measure recall, false alarms
> and whether users stop before paying.
> **Financial fraud protection should be understandable, accessible, and available in the languages
> Pakistanis actually use.** Hoshiyar raho. Paisa mehfooz."

---

## Slide content (copy-ready)
**Slide 5 table**

| On held-out synthetic message families (416) | Scams caught | False alarms |
|---|---|---|
| Keyword filter | 77.4% | 48.2% |
| Hoshiyar AI model alone | 93.5% | 8.0% |
| **Hoshiyar full app (AI + warning cues)** | **96.8%** | **8.0%** |
| Independent author set (80 msgs), full app | 90.0% | 27.5% |

Footnote: *Synthetic data. Real-world performance not yet measured. Details: docs/model-evaluation.md.*

## Pilot metrics we would measure (proposed, not achieved)
Scam recall on analyst-labelled real messages · legitimate-message false-positive rate · median on-device
analysis time · time for an analyst to review a campaign vs individual complaints · % of users who correctly
stop before a suspicious payment (A/B in a wallet app).

## SDG mapping (precise)
- **SDG 16.4** (reduce illicit financial flows, combat organised crime): earlier warnings and campaign-level
  intelligence on scam operations.
- **SDG 8.10** (expand access to banking and financial services): trust is a precondition for digital-finance adoption.
- We do **not** claim measured impact on either. These are the targets the product is designed to serve.

## Likely judge questions & evidence-based answers
| Question | Answer |
|---|---|
| Is this real AI or keyword matching? | A trained logistic-regression model on character n-grams, compared against a keyword baseline. On held-out families the keyword baseline had 48% false alarms vs 8% for ours (`model-evaluation.md`). The on-screen word explanation comes from the model's weights. |
| Why not an LLM/transformer? | It has to run offline on mid-range phones, in milliseconds, privately, and on Roman Urdu with no standard spelling. Character n-grams do that in a 232 KB file. A transformer is the next step once real consented data exists. |
| How do you know it works on real scams? | We don't yet, and we say so. Everything is synthetic. Our most honest estimate is the independent ChatGPT-written set: 90% recall, 27.5% false alarms. The next step is a consented bank/wallet pilot. |
| Did you test on training data? | No. The test set is 55 template families excluded from training, with leakage checks (0 shared families, 0 duplicate texts). We also publish our development history, including that we looked at test results between runs. |
| Is "on-device" really true? | Yes. The model ships as JSON inside the APK. TypeScript inference matches Python on 252 fixtures to within 1e-9, a test asserts no network call during analysis, and the demo runs in airplane mode. |
| What about privacy? | No SMS, contacts or call-log permissions (explicitly blocked). Nothing uploaded. Reports stay on the phone; message text is attached only if the user opts in. |
| Can it read my SMS automatically / block payments? | No, by design. Automatic SMS reading needs default-SMS-app permissions that conflict with privacy and Play policy. Blocking payments needs bank integration, which is exactly what a pilot would explore. |
| What if a reported number belongs to an innocent person? | Reports are worded as unverified claims ("N reports describe…"), never accusations. Numbers are masked in aggregates, and demo data uses a fictional range. A real deployment needs verification and appeal workflows. |
| False positives annoy users. | That's why we have three levels. "Suspicious" means verify first, not panic. Most of our independent-set false alarms are awareness messages that quote scams, and that's the top item to fix. |
| Business model? | B2B2C: banks and wallets embed "check before you pay" and receive anonymised campaign intelligence. Running cost is close to zero because inference runs on the device. |
| How did a two-person team build this in 24 hours? | With two AI collaborators under a written agreement (`docs/COLLABORATION.md`). One built the system; the other independently wrote the evaluation set and researched sources, so we couldn't grade our own homework. |
