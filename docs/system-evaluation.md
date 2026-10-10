# System Evaluation: full on-device pipeline

> **Auto-generated** by `HS_WRITE_SYSTEM_EVAL=1 npx jest system-eval` (in `apps/mobile`). Don't edit by hand.
> Model `hs-1.0.0+807e5952`. All data is synthetic; see `docs/model-evaluation.md` for the ML-only report and caveats.

The app's verdict combines the ML score with deterministic warning cues (fusion rules F1–F4 in
`apps/mobile/src/engine/analyze.ts`). "Flagged" means the app shows **Suspicious** or **High Risk**.

**Tuning discipline:** the fusion rules and cue lexicons were checked only against the *development* split.
**Disclosure:** Claude had seen the ML-only results on the challenge and ChatGPT sets before writing the
indicator engine. The rules are generic (negation-aware credential requests, advance fees, links, safe-account
and remote-access requests) and were not edited to fit individual messages from those sets.

## Development split (used for fusion sanity checks)

The same families the model was trained on. Optimistic by construction.

| Pipeline | n | Precision | Recall | F1 | False-positive rate | Missed scams | False alarms |
|---|---|---|---|---|---|---|---|
| ML only, flagged at Suspicious+ | 1664 | 100.0% | 100.0% | 1.000 | 0.0% | 0 | 0 |
| **Full app (ML + cues + fusion), Suspicious+** | 1664 | 100.0% | 100.0% | 1.000 | 0.0% | 0 | 0 |
| ML only, High | 1664 | 100.0% | 100.0% | 1.000 | 0.0% | 0 | 0 |
| **Full app, High** | 1664 | 100.0% | 100.0% | 1.000 | 0.0% | 0 | 0 |

Median analysis time (Node.js on the build container, not a phone): 1 ms.

## Held-out test families

Template families never seen in training.

| Pipeline | n | Precision | Recall | F1 | False-positive rate | Missed scams | False alarms |
|---|---|---|---|---|---|---|---|
| ML only, flagged at Suspicious+ | 416 | 92.7% | 93.5% | 0.931 | 8.0% | 14 | 16 |
| **Full app (ML + cues + fusion), Suspicious+** | 416 | 92.9% | 96.8% | 0.948 | 8.0% | 7 | 16 |
| ML only, High | 416 | 94.3% | 84.3% | 0.890 | 5.5% | 34 | 11 |
| **Full app, High** | 416 | 94.6% | 88.9% | 0.917 | 5.5% | 24 | 11 |

Median analysis time (Node.js on the build container, not a phone): 1 ms.

## Challenge set: claude_challenge (hand-written, out-of-template)

Hand-written unfamiliar patterns (Claude). Evaluation only.

| Pipeline | n | Precision | Recall | F1 | False-positive rate | Missed scams | False alarms |
|---|---|---|---|---|---|---|---|
| ML only, flagged at Suspicious+ | 60 | 92.0% | 76.7% | 0.836 | 6.7% | 7 | 2 |
| **Full app (ML + cues + fusion), Suspicious+** | 60 | 93.1% | 90.0% | 0.915 | 6.7% | 3 | 2 |
| ML only, High | 60 | 90.9% | 66.7% | 0.769 | 6.7% | 10 | 2 |
| **Full app, High** | 60 | 92.3% | 80.0% | 0.857 | 6.7% | 6 | 2 |

Median analysis time (Node.js on the build container, not a phone): 1 ms.

Deliberately ambiguous messages (the right outcome is "verify first"):

- **SUSPICIOUS**: Bhai, maine ghalti se aap ke JazzCash pe 2,500 bhej diye hain. Please check kar ke wapis kar dein, shukriya.
- **LOW**: Hello, I am Kamran from the Lahore branch. Please call me back regarding your account when you get a chance.
- **SUSPICIOUS**: Your package could not be delivered. Please reschedule your delivery at courier-help.example
- **HIGH**: Assalam o alaikum, main aap ke bete ke school se bol raha hoon, fees ke hawale se baat karni hai, is number pe call karein 0399-5550147.
- **HIGH**: Committee ka naya member Asad hai, is mahine ki kist uske account mein bhejni hai, number 0399-5550170.

## Independent set: contrib/chatgpt_challenge.jsonl

Written by ChatGPT without seeing templates or model outputs. Evaluation only.

| Pipeline | n | Precision | Recall | F1 | False-positive rate | Missed scams | False alarms |
|---|---|---|---|---|---|---|---|
| ML only, flagged at Suspicious+ | 80 | 79.5% | 77.5% | 0.785 | 20.0% | 9 | 8 |
| **Full app (ML + cues + fusion), Suspicious+** | 80 | 76.6% | 90.0% | 0.828 | 27.5% | 4 | 11 |
| ML only, High | 80 | 92.6% | 62.5% | 0.746 | 5.0% | 15 | 2 |
| **Full app, High** | 80 | 90.0% | 67.5% | 0.771 | 7.5% | 13 | 3 |

Median analysis time (Node.js on the build container, not a phone): 1 ms.

| Language | n | Recall | False-positive rate |
|---|---|---|---|
| english | 20 | 90.0% | 60.0% |
| mixed | 12 | 100.0% | 33.3% |
| roman_urdu | 32 | 81.3% | 12.5% |
| urdu | 16 | 100.0% | 12.5% |

<details><summary>Remaining errors (full app)</summary>

**Missed scams**

- To cancel the transfer you did not make, forward the bank's verification text to this chat. Include the one-time code; our reversal officer needs it before the timer expires.
- Main daftar ka finance head hun, naya WhatsApp hai. Salary ki file rok di hai. Meray zaati wallet par 2400 jama karo; HR ko poochha to tumhara naam list se nikalwa dun ga.
- SIM ke sath linked bank balance aaj raat jam ho jaye ga. Dobara chalane ke liye 550 verification tax is chat walay zaati number par jama karo; branch walon ko yeh option maloom nahi.
- Sirf 3000 lagao, kal subah 6000 pakka milen ge. Koi nuksan mumkin nahi. Paisay meray zaati wallet par bhejo aur ghar walon ko na batana, yeh andar ki scheme hai.

**False alarms**

- [SUSPICIOUS] Koi kahe 'inaam ki fee bhejo' to pehlay ruk jao. Hum OTP, PIN ya paisay chat par nahi maangtay. Madad ke liye khud apni bank app khol kar rabta karein.
- [SUSPICIOUS] BISP ke naam par koi registration fee apne zaati number par maangay to paisay na bhejein. Apni eligibility ki maloomat sirf tasdeeq shuda sarkari zariye se khud lein.
- [SUSPICIOUS] Scam example: 'Your account will be blocked; pay a verification fee now.' Do not follow that instruction. Open your bank app yourself and check whether any action is actually required.
- [HIGH] Could you send your share of yesterday's dinner when you have time? Use the account we already use. Call me on my saved number if you want to check the amount first.
- [SUSPICIOUS] Your printer repair is complete. Test it at the counter before paying the agreed Rs 1,100. We can give you a receipt there; no transfer is needed before collection.
- [SUSPICIOUS] The community centre timetable is posted at centre-hours.example. The page is public and does not need a login, card number, PIN or payment.
- [SUSPICIOUS] Weekend offer: 15% off notebooks bought in our shop. The discount is applied at the till. There is no prize draw, claim fee or advance deposit.
- [SUSPICIOUS] Your cancelled order refund of Rs 920 has been returned through the original payment method. Check the original transaction in your app; you do not need to approve a payment request or pay a refund fee.
- [SUSPICIOUS] اگر کوئی کہے کہ انعام لینے کے لیے پہلے فیس بھیجیں تو رک جائیں۔ انعام کے دعوے کی آزادانہ تصدیق کریں اور کسی اجنبی کو رقم یا خفیہ کوڈ نہ دیں۔
- [HIGH] Urgent security reminder: '0TP bhejo warna wallet band' aik scam ka jumla ho sakta hai. اپنا کوڈ کسی کو نہ دیں۔ Bank se contact apni app ke andar se karein.
- [HIGH] Invoice reminder: is mahine ki tuition fee Friday ko due hai. رسید والا amount office par jama karein; account change ka message aaye to pehle known office number se confirm karein.

</details>

