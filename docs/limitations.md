# Limitations (read before presenting or deploying)

## Evidence
1. **All training and test data is synthetic.** Results show how the model generalises to *unseen synthetic
   message families* and to messages from a different author (ChatGPT). They do **not** measure real-world
   accuracy, and we have no field data.
2. **Independent-author results are noticeably worse:** at the Suspicious level, ML-only gets 77.5% recall with
   20% false positives, and the full app gets 90% recall with 27.5% false positives (80 messages). Most false
   alarms are security-awareness messages that quote scam phrases.
3. **English legitimate messages** cause most false alarms on the held-out test set (14% false-positive rate
   for English, versus 0–3% for the other languages).
4. Scores are **not calibrated real-world probabilities**, so the app shows risk levels and never says "97% scam".
5. The test fold was viewed after each development run (v0 → v2; see the history in `model-evaluation.md`), so the
   test numbers are not perfectly "blind".

## Product scope
6. Hoshiyar does **not** read SMS automatically, intercept calls, block payments in other apps, verify who
   sent a message, or verify who owns a number.
7. Reputation data is **synthetic demo data** plus the user's own local reports. No national database is connected.
8. The official-domain list for look-alike detection is a **small starter list** that must be verified and
   maintained. URL analysis is structural, not a malicious-URL database.
9. Campaign clustering runs on **simulated** reports. Similar wording does not prove common ownership.
10. The Urdu UI translation is pending (`src/i18n/ur.ts`, owned by ChatGPT). Analysis already supports Urdu script.
11. Sharing directly from the SMS app into Hoshiyar (Android share-intent) is not implemented. It needs a native
    module and a development build. The `hoshiyar://scan?text=…` deep link pre-fills the scanner.

## Engineering
12. The release APK from GitHub Actions is signed with a debug keystore: fine for a demo, not for distribution.
13. Language quality of the synthetic Roman Urdu and Urdu has not been reviewed by native speakers.
14. Adversaries can reword messages to evade any text classifier. That's why every result tells people to verify through official channels.

## What would change our minds / next steps
A consented pilot with a bank or wallet: real, anonymised, analyst-labelled messages; measure recall,
false-positive rate, time-to-review, and whether users correctly identify suspicious payment requests;
recalibrate thresholds; then consider a small multilingual transformer.
