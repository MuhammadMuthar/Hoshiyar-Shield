# Demo Script: Hoshiyar Shield (AICON'26, 11 Oct 2026, 9:28–9:33 PKT)

Everything below runs **offline**. Turn on **airplane mode** before you start: it *proves* the
on-device claim, and Wi-Fi at venues fails.

## Pre-flight checklist (do this 30 minutes before)
- [ ] APK installed from GitHub Actions (artifact `hoshiyar-shield-apk`), **or** Expo Go + dev server as a fallback.
- [ ] Open the app once. Finish onboarding ("Get Protected") on the demo phone, then **re-install or "Delete all
      data"** if you want to show onboarding live.
- [ ] About → Settings: **Hackathon demo mode ON**, "Save recent checks" ON (so Home shows recent checks).
- [ ] Airplane mode ON. Brightness at max. Do-not-disturb ON. Battery > 50%.
- [ ] Screen mirroring/projector tested. Font size normal.
- [ ] Copy the "live" scam text (below) into the phone's clipboard, or have it in a notes app ready to copy.
- [ ] Backup: a screen recording of the full flow on a laptop, plus `docs/screenshots/` open in a tab.
- [ ] One person speaks while the other drives the phone. Rehearse the hand-offs.

## Messages to use
**Live scam (Roman Urdu), not in the sample library, so you can show it's not canned:**
```
Mubarak ho! Apka number Jeeto Inaam Scheme mein 2 lakh ke inaam ke liye select hua hai. Inaam lene ke liye 1,500 verification fee abhi JazzCash karein 0399-5550142 pe. Sirf aaj!
```
Library samples (Scan → "Demo library"): *Prize + fee*, *Wallet blocked*, *Bank OTP call*, *اکاؤنٹ بند* (Urdu),
*Loan fee*, *Card phishing*, *Bank debit alert*, *Real OTP message*, *Ammi ko paise*, *Wrong transfer?*

Expected results (produced by the shipped model `hs-1.0.0+807e5952`; rerun if the model changes):

| Message | Verdict | Key cue shown |
|---|---|---|
| Live scam above | **High Risk** | Fee demanded before a prize, loan or refund |
| *Wallet blocked* | **High Risk** | Contains a suspicious link (jazzcash-verify.example) |
| *اکاؤنٹ بند* (Urdu) | **High Risk** | Asks for a code, PIN or card details |
| *Real OTP message* | **No Obvious Scam Detected** | "Contains security advice" (reassuring sign) |
| *Wrong transfer?* | **Suspicious** | Asks you to return money "sent by mistake" |
| Link `http://jazzcash-verify.example/login` | **High Risk** | Uses the name "jazzcash" on an unofficial domain |
| Number `0399-5550142` | 3 reports (DEMO) | "3 reports describe suspicious prize-fee requests…" |

## Full demo (≈ 2.5 minutes inside the 5-minute pitch)
1. **Home** (5 s): "Shield ready on this phone · On-device AI · Works offline." Point at airplane mode.
2. **Scan a Message → Paste** the live scam → **Analyse message**.
3. **Result** (40 s): the shield turns red. Read the title "*High Risk: possible financial scam*" and the
   one-line reason. Scroll to:
   - **Warning signs found**: fee before prize, pay a fee, send money to a number, urgency.
   - **What the AI model saw**: score 100/100 with the thresholds, and the words that pushed it up.
     Say: "These are the model's own weights, not a keyword list."
   - **What you should do**: don't pay, verify via the official app.
   - Point at "*Analysed on this phone in N ms · no internet used*".
4. **Scan another → Demo library → Real OTP message → Analyse** (25 s): **No Obvious Scam Detected**, even
   though it contains "OTP", "share" and a bank name. "A keyword filter would flag this. Ours doesn't, and it
   still never says *safe*."
5. **Urdu sample (اکاؤنٹ بند)** (15 s): High Risk; the message renders right-to-left.
6. **Wrong transfer?** (15 s): **Suspicious**. "When it's genuinely ambiguous, we tell people to verify,
   not panic."
7. **Number tab → 0399-5550142** (20 s): "*3 reports describe suspicious prize-fee requests associated with
   this number*". Point at "synthetic DEMO records" and "an unreported number is not a verified safe number".
8. **Intel tab** (20 s): simulated reports grouped into campaigns. "This is what a bank's fraud team could see
   from consented reports." Point at the **SIMULATED DATA** banner.

## 90-second emergency demo (if time is short or something breaks)
1. Paste the live scam → Analyse → High Risk + reasons (30 s).
2. Demo library → *Real OTP message* → No Obvious Scam Detected (20 s).
3. Link tab → tap the first demo chip → High Risk look-alike (15 s).
4. About → model version + "Held-out test" line (15 s). Close with the one-line vision.

## If something goes wrong
| Problem | Do this |
|---|---|
| APK won't install / crashes | Switch to Expo Go (`npx expo start` on the laptop + phone on the same hotspot), or play the screen recording |
| Clipboard paste blocked | Long-press the text box → Paste, or use the *Prize + fee* sample |
| Projector issue | Show `docs/screenshots/` from the laptop while narrating |
| Judge asks to try their own text | Let them, and say up front: "Synthetic training, so it can be wrong. That's why it always says verify." |

## What not to say
- ❌ "It blocks scams automatically" / "reads your SMS" / "guarantees safety" / "98% accurate in the real world"
- ✅ "On synthetic, held-out message families, the full app caught 96.8% of scams with an 8% false-alarm rate. On messages written by an independent author, recall was 90% with 27.5% false alarms, and we're working on that."
