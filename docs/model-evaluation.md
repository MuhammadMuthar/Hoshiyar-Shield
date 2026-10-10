# Model Evaluation: Hoshiyar Shield scam classifier

> **Auto-generated** by `ml/training/train.py` from `ml/artifacts/metrics.json`. Don't edit by hand.
> Model `hs-1.0.0+807e5952` · normaliser `hn-1.0` · generated 2026-10-10T00:26:21+00:00 · seed 20261011

## Read this first: what these numbers mean

- **All training and test data is synthetic**: messages generated from template families written by the team
  (see `docs/dataset-card.md`). The test set uses *template families the model never saw*, which is stricter
  than a random split. It is still **not** a measurement of real-world performance on live SMS traffic.
- Hyperparameters and thresholds were chosen by grouped 4-fold cross-validation on development data only. The final
  model was refit on all development data and evaluated **once** on the held-out test families. The shipped model
  (`apps/mobile/assets/model/hoshiyar-model.json`) is **exactly** that model. Nothing is refit after testing.
- Scores are logistic-regression outputs. They are **not calibrated real-world scam probabilities**, so the app
  shows risk *levels*, not percentages.
- The app's final verdict also uses a deterministic indicator engine and URL analyser (risk fusion, see
  `docs/architecture.md`). The numbers below are for the **ML classifier alone** unless stated otherwise.

## Headline (held-out test set, unseen template families)

| | Value |
|---|---|
| Test messages | 416 (55 unseen families) |
| Scam recall at *Suspicious* threshold (0.73) | **93.5%** (14 scams missed) |
| False-positive rate at *Suspicious* threshold | **8.0%** (16 legit messages flagged) |
| Precision at *High Risk* threshold (0.9) | **94.3%** |
| Scam recall at *High Risk* threshold | 84.3% |
| ROC-AUC / average precision | 0.9745 / 0.9747 |
| Model size (JSON) / vocabulary | 231.5 KB / 8,973 features |

## Baseline vs. machine learning (same test set)

| Setting | n | Precision | Recall | F1 | False-positive rate | False negatives | False positives |
|---|---|---|---|---|---|---|---|
| A: keyword baseline (≥1 keyword hits, tuned on dev) | 416 | 63.6% | 77.4% | 0.699 | 48.2% | 49 | 96 |
| B: char n-gram TF-IDF + LR [char2-4, C=256.0] @0.5 | 416 | 90.8% | 95.9% | 0.933 | 10.5% | 9 | 21 |
| C: word+char TF-IDF + LR [char2-5+word1-2, C=64.0] @0.5 | 416 | 88.1% | 98.6% | 0.930 | 14.6% | 3 | 29 |
| **Shipped model** @ Suspicious (0.73) | 416 | 92.7% | 93.5% | 0.931 | 8.0% | 14 | 16 |
| **Shipped model** @ High Risk (0.9) | 416 | 94.3% | 84.3% | 0.890 | 5.5% | 34 | 11 |

Where the keyword baseline goes wrong (per category, test set):

| Category | n | Keyword baseline: recall / false-alarm rate | Shipped model @Suspicious: recall / false-alarm rate |
|---|---|---|---|
| account_suspension | 5 | recall 80.0% | recall 80.0% |
| impersonation | 28 | recall 96.4% | recall 100.0% |
| investment | 48 | recall 81.2% | recall 91.7% |
| legit_business_payment | 7 | false alarms 0.0% | false alarms 0.0% |
| legit_conversation | 15 | false alarms 80.0% | false alarms 0.0% |
| legit_loan_ad | 9 | false alarms 0.0% | false alarms 0.0% |
| legit_otp_delivery | 51 | false alarms 86.3% | false alarms 0.0% |
| legit_promo | 17 | false alarms 0.0% | false alarms 0.0% |
| legit_security_advice | 31 | false alarms 100.0% | false alarms 19.4% |
| legit_transaction_alert | 54 | false alarms 16.7% | false alarms 16.7% |
| legit_url_info | 15 | false alarms 0.0% | false alarms 6.7% |
| loan_fee | 36 | recall 91.7% | recall 91.7% |
| otp_pin_theft | 17 | recall 82.3% | recall 100.0% |
| payment_request | 40 | recall 32.5% | recall 95.0% |
| prize_lottery | 35 | recall 100.0% | recall 91.4% |
| refund_reversal | 8 | recall 37.5% | recall 87.5% |

## Per-language results (test, at Suspicious threshold)

| Language | n | Scams | Recall | False-positive rate | Precision |
|---|---|---|---|---|---|
| english | 143 | 39 | 87.2% | 14.4% | 69.4% |
| mixed | 70 | 43 | 100.0% | 0.0% | 100.0% |
| roman_urdu | 137 | 104 | 92.3% | 0.0% | 100.0% |
| urdu | 66 | 31 | 96.8% | 2.9% | 96.8% |

## Per-category results (test)

Scam categories show **recall**. Legitimate categories show the **false-alarm rate**. Counts per category are small
(a handful of families each), so treat single-category numbers as indicative only.

| Category | n | @Suspicious | @High Risk |
|---|---|---|---|
| account_suspension | 5 | recall 80.0% | recall 60.0% |
| impersonation | 28 | recall 100.0% | recall 89.3% |
| investment | 48 | recall 91.7% | recall 77.1% |
| legit_business_payment | 7 | false alarms 0.0% | false alarms 0.0% |
| legit_conversation | 15 | false alarms 0.0% | false alarms 0.0% |
| legit_loan_ad | 9 | false alarms 0.0% | false alarms 0.0% |
| legit_otp_delivery | 51 | false alarms 0.0% | false alarms 0.0% |
| legit_promo | 17 | false alarms 0.0% | false alarms 0.0% |
| legit_security_advice | 31 | false alarms 19.4% | false alarms 6.5% |
| legit_transaction_alert | 54 | false alarms 16.7% | false alarms 14.8% |
| legit_url_info | 15 | false alarms 6.7% | false alarms 6.7% |
| loan_fee | 36 | recall 91.7% | recall 91.7% |
| otp_pin_theft | 17 | recall 100.0% | recall 94.1% |
| payment_request | 40 | recall 95.0% | recall 80.0% |
| prize_lottery | 35 | recall 91.4% | recall 88.6% |
| refund_reversal | 8 | recall 87.5% | recall 75.0% |

## Confusion matrices (test)

**Suspicious threshold**

| | Predicted legit | Predicted scam |
|---|---|---|
| **Actual legit** | 183 | 16 |
| **Actual scam** | 14 | 203 |

**High Risk threshold**

| | Predicted legit | Predicted scam |
|---|---|---|
| **Actual legit** | 188 | 11 |
| **Actual scam** | 34 | 183 |

Calibration on test: Brier score 0.0599, expected calibration error (10 bins) 0.0394. Calibration on synthetic data says nothing about calibration on real messages.

## Challenge set: unfamiliar patterns written separately (evaluation only)

65 hand-written messages (60 labelled, 5 deliberately ambiguous).
They use scam types that appear in **no** training template (job-visa fees, customs parcels, crypto
withdrawal tax, Hajj ballots, fake buyers, obfuscated text, …) and new legitimate hard negatives.
The same author (Claude) wrote the templates, so this isn't fully independent. See
`docs/COLLABORATION.md` §2.2-A for the independent ChatGPT-authored set.

| Setting | n | Precision | Recall | F1 | False-positive rate | False negatives | False positives |
|---|---|---|---|---|---|---|---|
| Keyword baseline | 60 | 54.5% | 80.0% | 0.649 | 66.7% | 6 | 20 |
| ML @ Suspicious (0.73) | 60 | 92.0% | 76.7% | 0.836 | 6.7% | 7 | 2 |
| ML @ High Risk (0.9) | 60 | 90.9% | 66.7% | 0.769 | 6.7% | 10 | 2 |

<details><summary>Every challenge message with its ML score (click to expand)</summary>

| id | label | language | pattern | ML score | ML-only verdict | text |
|---|---|---|---|---|---|---|
| ch-001 | scam | roman_urdu | job_fee | 0.971 | HIGH | Congratulations! Aap ka CV Saudi Arabia mein driver ki job ke liye shortlist ho gaya hai. Visa processing f… |
| ch-002 | scam | english | customs_parcel | 0.999 | HIGH | Your international parcel is held at Karachi customs. Pay customs duty Rs 3,450 via Easypaisa to 0399-55501… |
| ch-003 | scam | roman_urdu | govt_aid | 0.995 | HIGH | BISP 8171: Aap ki 25000 ki qist aa chuki hai. Hasil karne ke liye apna CNIC number aur JazzCash PIN reply k… |
| ch-004 | scam | english | romance_gift | 1.000 | HIGH | Darling I sent you a gift box with dollars and gold. The courier needs Rs 20,000 clearance fee, please pay … |
| ch-005 | scam | english | crypto_tax | 0.962 | HIGH | Your USDT withdrawal of $1,200 is ready. Pay 10% unlock tax to complete the withdrawal at binance-pk.exampl… |
| ch-006 | scam | mixed | sim_upgrade | 0.999 | HIGH | Jazz: Aap ki SIM 5G pe upgrade ho rahi hai. Upgrade complete karne ke liye jo code aaye woh is number pe ba… |
| ch-007 | scam | roman_urdu | utility_fine | 0.962 | HIGH | WAPDA staff: Aap ke meter ki checking hogi. Jurmane se bachne ke liye 5000 abhi hamare officer ko JazzCash … |
| ch-008 | scam | mixed | obfuscated | 0.801 | SUSPICIOUS | Ap ka 0TP sh@re krein warna J@zzC@sh acc0unt bl0ck ho jaye ga!!! |
| ch-009 | scam | roman_urdu | obfuscated | 0.997 | HIGH | A P K A   I N A A M   N I K L A   H A I. fee bhejain 0399-5550111 pe foran |
| ch-010 | scam | urdu | job_fee | 0.992 | HIGH | آپ کو بیرون ملک نوکری کے لیے منتخب کر لیا گیا ہے، ویزا فیس 20 ہزار روپے فوری جمع کروائیں۔ |
| ch-011 | scam | roman_urdu | hajj_ballot | 1.000 | HIGH | Mubarak! Aap ka naam Hajj qurandazi mein aa gaya hai. Confirmation ke liye 10,000 security abhi bhejein war… |
| ch-012 | scam | roman_urdu | whatsapp_takeover | 0.795 | SUSPICIOUS | Assalam o alaikum, main aap ke family group ka admin hoon. Group verify karne ke liye jo 6 digit code aya h… |
| ch-013 | scam | english | phishing | 0.914 | HIGH | Your Meezan Bank account requires immediate verification. Click meezan-secure.example and enter your debit … |
| ch-014 | scam | roman_urdu | govt_aid | 0.975 | HIGH | PM Relief Package: Rs 12,000 aap ke liye manzoor. 8171 pe apna CNIC bhejein aur 500 fee JazzCash karein. |
| ch-015 | scam | mixed | suspension | 0.989 | HIGH | URGENT!!! ur easypaisa will b closed tonite. call now 0399-5550199 n verify ur details |
| ch-016 | scam | roman_urdu | investment | 0.875 | SUSPICIOUS | Hamare WhatsApp group mein shamil ho kar rozana 3% munafa kamaein. Sirf 10,000 se shuru karein, pakki guara… |
| ch-017 | scam | english | reward_points | 1.000 | HIGH | Your HBL reward points (4,500) expire today. Redeem now at hbl-points.example by entering your card number … |
| ch-018 | scam | urdu | relative_new_number | 0.193 | NO_OBVIOUS | امی جان میرا موبائل خراب ہے، یہ دوست کا نمبر ہے، دس ہزار ایزی پیسہ کر دیں جلدی۔ |
| ch-019 | scam | mixed | refund | 0.985 | HIGH | Daraz se bol rahe hain, aap ka order cancel hone pe 2,999 refund ke liye jo code aaye woh share karein. |
| ch-020 | scam | roman_urdu | safe_account | 0.999 | HIGH | Aap ke account pe hackers ka hamla hua hai. Apna balance foran naye safe account 0399-5550160 mein muntaqil… |
| ch-021 | scam | mixed | prize_bond | 0.998 | HIGH | Dear winner, aap ka prize bond ka inaam 7,50,000 nikla hai. Withholding tax 15,000 pehle jama karwain. |
| ch-022 | scam | english | rental_advance | 0.447 | NO_OBVIOUS | Flat available in DHA Lahore for 35,000 rent. I am abroad, send 2 months advance via Easypaisa and I will c… |
| ch-023 | scam | english | prize | 0.913 | HIGH | You won! Reply with your CNIC and pay Rs 800 to claim your Rs 50,000 shopping voucher. |
| ch-024 | scam | urdu | otp | 0.969 | HIGH | آپ کے بینک اکاؤنٹ کی سیکیورٹی اپڈیٹ ہو رہی ہے، ابھی جو چھ ہندسوں کا کوڈ آیا ہے وہ ہمیں بتا دیں۔ |
| ch-025 | scam | urdu | loan | 0.998 | HIGH | صرف شناختی کارڈ پر فوری قرض حاصل کریں، کوئی ضمانت نہیں۔ فائل چارجز 1500 روپے اس نمبر پر ایزی پیسہ کریں 0399… |
| ch-026 | scam | urdu | investment | 0.196 | NO_OBVIOUS | صرف ایک ہفتے میں اپنی رقم دگنی کریں، ہماری کمپنی میں سرمایہ کاری کریں، منافع کی مکمل ضمانت۔ |
| ch-027 | scam | english | tech_support | 0.115 | NO_OBVIOUS | Microsoft support: your phone banking app is infected. Install the remote helper app and share the 9-digit … |
| ch-028 | scam | roman_urdu | fake_buyer | 0.183 | NO_OBVIOUS | Main aap ka sofa khareedna chahta hoon, payment bhej di hai. Aap ko jo SMS aya hai us mein code hai, woh bh… |
| ch-029 | scam | mixed | loan_harass | 0.112 | NO_OBVIOUS | Final reminder: aap ki loan file pending hai. Agar aaj 2,000 legal fee nahi bheji to aap ke contacts ko mes… |
| ch-030 | scam | english | electricity | 0.453 | NO_OBVIOUS | K-Electric: Your connection will be disconnected at 9 PM tonight due to an unpaid bill. Pay immediately to … |
| ch-031 | legit | english | otp_delivery | 0.000 | NO_OBVIOUS | Meezan Bank: Never share your OTP. Your OTP for IBFT of Rs 25,000 to Ahmed Raza is 739104. |
| ch-032 | legit | roman_urdu | family | 0.001 | NO_OBVIOUS | Ammi, 5000 bhej diye hain Easypaisa pe. Dawai le lena aur doctor ki fees bhi de dena. |
| ch-033 | legit | roman_urdu | new_number_no_money | 0.277 | NO_OBVIOUS | Bhai mera naya number save kar lo, purana band ho gaya hai. Kal milte hain. |
| ch-034 | legit | english | bill | 0.000 | NO_OBVIOUS | Your Jazz postpaid bill of Rs 1,450 is due on 15 Oct. Pay through the JazzCash app. Thank you. |
| ch-035 | legit | english | advice | 0.012 | NO_OBVIOUS | SBP: Raast is free for person-to-person transfers. Never share your PIN or OTP with anyone. |
| ch-036 | legit | english | limit_increase | 0.374 | NO_OBVIOUS | Congratulations! Your HBL credit card limit has been increased to Rs 300,000. No action is required. |
| ch-037 | legit | roman_urdu | committee | 0.000 | NO_OBVIOUS | Mubarak ho! Aap ki committee is mahine nikal aayi hai, 50,000 aap ko Friday tak mil jayenge. |
| ch-038 | legit | english | delivery | 0.011 | NO_OBVIOUS | Your Foodpanda order is on its way! Rider Bilal will reach you in 15 minutes. |
| ch-039 | legit | english | account_lock_legit | 0.649 | NO_OBVIOUS | Easypaisa: Your account has been locked after 3 wrong PIN attempts. Visit any Easypaisa retailer with your … |
| ch-040 | legit | english | maintenance | 0.022 | NO_OBVIOUS | LESCO: Electricity will be suspended in your area tomorrow from 9am to 1pm for maintenance. |
| ch-041 | legit | urdu | advice | 0.074 | NO_OBVIOUS | یہ پیغام آپ کی حفاظت کے لیے ہے: کسی کو اپنا پن یا کوڈ نہ بتائیں۔ میزان بینک |
| ch-042 | legit | roman_urdu | family | 0.059 | NO_OBVIOUS | Beta exam ki fees 3,500 hai, kal tak school mein jama karwa dena. Paisay drawer mein rakh diye hain. |
| ch-043 | legit | english | friend_refund | 0.998 | HIGH | Hi Sana, the refund for the cancelled concert ticket (Rs 4,000) has been sent to your bank account. Please … |
| ch-044 | legit | english | statement | 0.203 | NO_OBVIOUS | Your account statement for September is ready. Log in to the UBL Digital app to view it. |
| ch-045 | legit | roman_urdu | loan_friend | 0.001 | NO_OBVIOUS | Salam bhai, aap ne jo 10,000 maange thay, bhej diye hain. Jab ho sake wapis kar dena, koi jaldi nahi. |
| ch-046 | legit | english | promo | 0.001 | NO_OBVIOUS | Zong: Get 50GB monthly data for Rs 1,000. Dial *6464# to subscribe. |
| ch-047 | legit | urdu | bill | 0.010 | NO_OBVIOUS | آپ کا گیس کا بل 2,300 روپے ہے، آخری تاریخ 20 اکتوبر۔ ایس این جی پی ایل |
| ch-048 | legit | english | appointment | 0.005 | NO_OBVIOUS | Reminder: doctor appointment tomorrow at 5 pm. Please bring previous reports. Fee Rs 2,000 payable at recep… |
| ch-049 | legit | english | cashback | 0.556 | NO_OBVIOUS | Easypaisa: Rs. 1,000 cashback has been added to your account for your bill payment. No action needed. |
| ch-050 | legit | english | card_block_legit | 0.478 | NO_OBVIOUS | HBL: As requested, your lost debit card has been blocked. Visit any branch with your CNIC to get a replacem… |
| ch-051 | legit | english | otp_delivery | 0.030 | NO_OBVIOUS | Your one-time PIN for NADRA e-Sahulat is 4821. Do not share it with anyone. |
| ch-052 | legit | roman_urdu | rent | 0.930 | HIGH | Mama ne kaha hai is mahine ka kiraya 25,000 unke Meezan account mein hi bhejna jo pehle se save hai. |
| ch-053 | legit | english | receipt | 0.001 | NO_OBVIOUS | Thank you for your payment of Rs 15,000 to Bright Future Academy. Receipt no 88213. |
| ch-054 | legit | roman_urdu | scam_talk | 0.005 | NO_OBVIOUS | Bhai, inaam wali calls se bach ke rehna, kal mere chachu ke saath 20,000 ka fraud ho gaya. |
| ch-055 | legit | english | webinar | 0.052 | NO_OBVIOUS | Join our free webinar on personal finance this Saturday. Register at finance-webinar.example |
| ch-056 | legit | urdu | family | 0.013 | NO_OBVIOUS | بیٹا میں نے تمہارے اکاؤنٹ میں پانچ ہزار بھیج دیے ہیں، کتابیں خرید لینا۔ |
| ch-057 | legit | urdu | transaction | 0.038 | NO_OBVIOUS | آپ کے اکاؤنٹ سے 3,000 روپے بجلی کے بل کی ادائیگی کے لیے کاٹے گئے ہیں۔ شکریہ۔ |
| ch-058 | legit | urdu | conversation | 0.132 | NO_OBVIOUS | مبارک ہو! آپ کا بیٹا امتحان میں اول آیا ہے، سکول کی طرف سے انعام دیا جائے گا۔ |
| ch-059 | legit | mixed | office | 0.051 | NO_OBVIOUS | Sir aaj ki meeting 4 baje shift ho gayi hai, budget wali file saath le aayein. |
| ch-060 | legit | english | salary | 0.008 | NO_OBVIOUS | Your salary of Rs 85,000 for September has been credited. Thank you for your hard work this month. |
| ch-061 | ambiguous | roman_urdu | wrong_transfer | 0.233 | NO_OBVIOUS | Bhai, maine ghalti se aap ke JazzCash pe 2,500 bhej diye hain. Please check kar ke wapis kar dein, shukriya. |
| ch-062 | ambiguous | english | callback | 0.415 | NO_OBVIOUS | Hello, I am Kamran from the Lahore branch. Please call me back regarding your account when you get a chance. |
| ch-063 | ambiguous | english | delivery_link | 0.788 | SUSPICIOUS | Your package could not be delivered. Please reschedule your delivery at courier-help.example |
| ch-064 | ambiguous | roman_urdu | school_call | 0.996 | HIGH | Assalam o alaikum, main aap ke bete ke school se bol raha hoon, fees ke hawale se baat karni hai, is number… |
| ch-065 | ambiguous | roman_urdu | committee_new_account | 0.996 | HIGH | Committee ka naya member Asad hai, is mahine ki kist uske account mein bhejni hai, number 0399-5550170. |

</details>

## Independent challenge set: `contrib/chatgpt_challenge.jsonl`

Written by **ChatGPT** under `docs/COLLABORATION.md` §2.2-A, without seeing the training templates or any model
output. Used **for evaluation only**: it is read after the model and thresholds are fixed. 80 messages, 48 families; languages: roman_urdu 32, english 20, urdu 16, mixed 12. SHA-256 `7705733cdddef693935535866131aebbb86497d4253187e5eb0d66437f46f4ff`. Rows that also appear in training data: 0.

This is the best estimate in this report of how the model handles messages written by a different author.
It is still synthetic, small and balanced, so it is not a real-world prevalence estimate.

| Setting | n | Precision | Recall | F1 | False-positive rate | False negatives | False positives |
|---|---|---|---|---|---|---|---|
| Keyword baseline | 80 | 51.4% | 90.0% | 0.654 | 85.0% | 4 | 34 |
| ML @ Suspicious (0.73) | 80 | 79.5% | 77.5% | 0.785 | 20.0% | 9 | 8 |
| ML @ High Risk (0.9) | 80 | 92.6% | 62.5% | 0.746 | 5.0% | 15 | 2 |

| Language | n | Recall | False-positive rate |
|---|---|---|---|
| english | 20 | 90.0% | 40.0% |
| mixed | 12 | 83.3% | 33.3% |
| roman_urdu | 32 | 68.8% | 6.2% |
| urdu | 16 | 75.0% | 12.5% |

| Category | n | @Suspicious |
|---|---|---|
| account_suspension | 5 | recall 60.0% |
| impersonation | 5 | recall 80.0% |
| investment | 5 | recall 80.0% |
| legit_business_payment | 4 | false alarms 25.0% |
| legit_conversation | 5 | false alarms 20.0% |
| legit_loan_ad | 3 | false alarms 0.0% |
| legit_otp_delivery | 5 | false alarms 0.0% |
| legit_payment_reminder | 5 | false alarms 20.0% |
| legit_promo | 3 | false alarms 0.0% |
| legit_security_advice | 6 | false alarms 66.7% |
| legit_transaction_alert | 6 | false alarms 0.0% |
| legit_url_info | 3 | false alarms 33.3% |
| loan_fee | 5 | recall 100.0% |
| otp_pin_theft | 5 | recall 20.0% |
| payment_request | 5 | recall 100.0% |
| prize_lottery | 5 | recall 80.0% |
| refund_reversal | 5 | recall 100.0% |

<details><summary>Every message with its ML score</summary>

| id | label | language | ML score | ML-only verdict | text |
|---|---|---|---|---|---|
| cg-0001 | scam | roman_urdu | 0.989 | HIGH | Aap ne kisi draw mein hissa nahi liya phir bhi bonus inaam nikla hai! 420 rupay release stamp ke 0399-55501… |
| cg-0002 | scam | roman_urdu | 0.308 | NO_OBVIOUS | Free ration hamper aap ke naam reserve hai. Hamper muft hai bas delivery insurance ke 690 rupay bhejein. Re… |
| cg-0003 | scam | english | 0.948 | HIGH | You were selected for a surprise phone giveaway. Buy a Rs 1,500 gift voucher and send us its redemption cod… |
| cg-0004 | scam | urdu | 1.000 | HIGH | مبارک ہو، آپ کا انعام نکلا ہے۔ رجسٹریشن کے بغیر بھی آپ کو منتخب کیا گیا ہے۔ انعام وصول کرنے سے پہلے 850 روپ… |
| cg-0005 | scam | mixed | 0.990 | HIGH | 🎁 Lucky customer! Aap ki reward file ready hai. Claim agent ki private chat par Rs 375 unlock fee bhejo; st… |
| cg-0006 | scam | roman_urdu | 0.688 | NO_OBVIOUS | J@zzCash ki taraf se bol raha hun. Jo 0TP abhi aya hai us ke darmiyan spaces daal kar idhar likh dein, misa… |
| cg-0007 | scam | roman_urdu | 0.983 | HIGH | Wallet upgrade ke liye apna chaar hindson wala khufia number voice note mein bol dein. Likhnay ki zarurat n… |
| cg-0008 | scam | english | 0.412 | NO_OBVIOUS | To cancel the transfer you did not make, forward the bank's verification text to this chat. Include the one… |
| cg-0009 | scam | urdu | 0.433 | NO_OBVIOUS | ہم بینک کی تصدیقی ٹیم سے ہیں۔ فون پر آیا ہوا یک وقتی کوڈ اس چیٹ میں بھیج دیں تاکہ ہم آپ کی شناخت کی تصدیق ک… |
| cg-0010 | scam | mixed | 0.187 | NO_OBVIOUS | Security check: اپنا خفیہ پن support agent کو بتائیں۔ App mein khud enter na karein; hum aap ke behalf par … |
| cg-0011 | scam | roman_urdu | 0.978 | HIGH | Beta main tumhari khala hun, purana phone toot gaya. Is naye number ki tasdeeq ke liye call mat karna, fora… |
| cg-0012 | scam | roman_urdu | 0.007 | NO_OBVIOUS | Main daftar ka finance head hun, naya WhatsApp hai. Salary ki file rok di hai. Meray zaati wallet par 2400 … |
| cg-0013 | scam | english | 0.998 | HIGH | This is the cybercrime investigation desk. Your wallet is under inquiry. Transfer Rs 9,200 to our officer's… |
| cg-0014 | scam | urdu | 0.744 | SUSPICIOUS | میں آپ کے بچے کے اسکول کا نیا اکاؤنٹنٹ ہوں۔ فیس آج ہی میرے ذاتی والیٹ میں بھیجیں۔ دفتر سے تصدیق نہ کریں، وہ… |
| cg-0015 | scam | english | 0.984 | HIGH | Bank audit team here. Move your entire balance into our temporary protection wallet at 0399-5550115. You mu… |
| cg-0016 | scam | roman_urdu | 0.999 | HIGH | Qarza baghair kisi jaanch ke pakka manzoor hai. Pehlay 1250 insurance ke hamaray agent ke zaati number 0399… |
| cg-0017 | scam | roman_urdu | 0.987 | HIGH | Aap ki loan file release kar di, lekin paisay nazar aane se pehlay 780 server activation ke bhejo. Receipt … |
| cg-0018 | scam | english | 0.855 | SUSPICIOUS | Your emergency loan is guaranteed, no checks needed. Before we show the repayment terms, send a Rs 950 clea… |
| cg-0019 | scam | urdu | 0.931 | HIGH | آپ کا قرض بغیر کسی جانچ کے منظور ہے۔ رقم جاری کرنے سے پہلے ہمارے نمائندے کے ذاتی والیٹ میں 1600 روپے ضمانتی… |
| cg-0020 | scam | mixed | 0.985 | HIGH | Loan approved ✅ Ab pehli fee ke baad system ne ek aur release charge lagaya hai. مزید 2100 روپے agent کو بھ… |
| cg-0021 | scam | roman_urdu | 0.981 | HIGH | Aap ne parcel order nahi kiya to bhi aap ke naam customs package aya hai. Aaj 330 rupay parcel-release.exam… |
| cg-0022 | scam | roman_urdu | 0.853 | SUSPICIOUS | BISP ki nayi raqam aap ke liye nikal aayi hai. Koi eligibility check nahi, bas meri zaati wallet ID 0399-55… |
| cg-0023 | scam | english | 0.910 | HIGH | You have been hired without an interview. Pay a Rs 1,800 job registration charge to our recruiter's persona… |
| cg-0024 | scam | urdu | 0.999 | HIGH | آپ نے پارسل منگوایا ہو یا نہ ہو، آپ کے نام ایک پیکٹ رکا ہوا ہے۔ آج 460 روپے پارسل کھلوانے کی فیس ہمارے ذاتی… |
| cg-0025 | scam | english | 0.999 | HIGH | You qualify for a flood relief cash grant even if you did not apply. Send Rs 700 to 0399-5550125 to activat… |
| cg-0026 | scam | roman_urdu | 0.859 | SUSPICIOUS | Aap ka Easypaisa wallet dus minute mein band ho raha hai. wallet-renew.example par ja kar apna login passwo… |
| cg-0027 | scam | roman_urdu | 0.178 | NO_OBVIOUS | SIM ke sath linked bank balance aaj raat jam ho jaye ga. Dobara chalane ke liye 550 verification tax is cha… |
| cg-0028 | scam | english | 0.999 | HIGH | FINAL NOTICE: your banking access will be suspended in 15 minutes. Open account-check.example and enter you… |
| cg-0029 | scam | urdu | 0.729 | NO_OBVIOUS | آج رات آپ کے اکاؤنٹ سے رقم نکالنے پر پابندی لگ جائے گی۔ پابندی ہٹانے کے لیے اس نجی چیٹ میں اپنی لاگ اِن تفص… |
| cg-0030 | scam | mixed | 1.000 | HIGH | Wallet suspension alert! Aap ka access بند ہونے والا ہے۔ Reactivation ke Rs 890 ki fee 0399-5550130 par pay… |
| cg-0031 | scam | roman_urdu | 0.110 | NO_OBVIOUS | Sirf 3000 lagao, kal subah 6000 pakka milen ge. Koi nuksan mumkin nahi. Paisay meray zaati wallet par bhejo… |
| cg-0032 | scam | roman_urdu | 0.768 | SUSPICIOUS | Hamari trading app mein munafa dikh raha hai na? Nikalne ke liye pehlay apne paison se 20 feesad withdrawal… |
| cg-0033 | scam | english | 0.993 | HIGH | Our private crypto pool guarantees 12% every day with zero chance of loss. Transfer your savings to the man… |
| cg-0034 | scam | urdu | 0.987 | HIGH | یہ سرمایہ کاری کبھی نقصان نہیں دیتی۔ آج 5000 روپے بھیجیں اور اگلے ہفتے لازماً 15000 پائیں۔ کمپنی کا پتہ نہی… |
| cg-0035 | scam | mixed | 0.998 | HIGH | Investment club ka rule simple hai: guaranteed profit tab unlock hoga jab aap do naye logon ki deposits lao… |
| cg-0036 | scam | roman_urdu | 0.997 | HIGH | Ghalti se tumharay wallet mein 4500 bhej diye, screenshot dekh lo. App mein abhi entry na bhi ho to foran w… |
| cg-0037 | scam | roman_urdu | 0.750 | SUSPICIOUS | Aap ka parcel refund tayyar hai. Refund lene ke liye jo request aa rahi hai us mein PAY dabana, RECEIVE nah… |
| cg-0038 | scam | english | 0.971 | HIGH | I accidentally sent you Rs 6,400. Ignore the fact that your transaction history shows nothing yet; the scre… |
| cg-0039 | scam | urdu | 0.960 | HIGH | آپ کی پچھلی کٹوتی واپس کرنے کے لیے پہلے 900 روپے واپسی فیس ہمارے ذاتی والیٹ میں بھیجیں۔ یہ فیس واپس ہونے وا… |
| cg-0040 | scam | mixed | 0.998 | HIGH | Refund department: receive money karne ke liye payment approval par اپنا PIN ڈال کر Confirm Pay دبائیں۔ Amo… |
| cg-0041 | legit | roman_urdu | 0.001 | NO_OBVIOUS | Aap ka login code 482731 hai. Sirf apni kholi hui app mein likhein; kisi caller ya is chat ko mat bhejein. … |
| cg-0042 | legit | roman_urdu | 0.110 | NO_OBVIOUS | Aap ke wallet mein 1850 rupay jama huay. Naya balance 4270 rupay hai. |
| cg-0043 | legit | roman_urdu | 0.537 | NO_OBVIOUS | Beta, 1200 jo udhar liye thay abhi wapas bhej do, dawai lenay ja raha hun. |
| cg-0044 | legit | roman_urdu | 0.602 | NO_OBVIOUS | Pichlay haftay ki raseed ke 760 rupay baqi hain. Aaj shaam tak de dein, hisaab band karna hai. |
| cg-0045 | legit | roman_urdu | 0.063 | NO_OBVIOUS | Koi kahe 'inaam ki fee bhejo' to pehlay ruk jao. Hum OTP, PIN ya paisay chat par nahi maangtay. Madad ke li… |
| cg-0046 | legit | roman_urdu | 0.157 | NO_OBVIOUS | Karobar ke liye qarz ki maloomat branch se le sakte hain. Manzoori jaanch ke baad hogi; markup aur fees lik… |
| cg-0047 | legit | roman_urdu | 0.002 | NO_OBVIOUS | Silai ka suit tayyar hai, kul 2200 banay hain. Shop par aa kar fitting dekh lena phir cash ya counter ke ta… |
| cg-0048 | legit | roman_urdu | 0.197 | NO_OBVIOUS | Library ki timing badli hai. Naya jadwal library-hours.example par hai; bas maloomat ka safha hai, koi acco… |
| cg-0049 | legit | roman_urdu | 0.057 | NO_OBVIOUS | Kal stationery par 10 feesad riayat hai. Offer sirf shaam 6 bajay tak hai. |
| cg-0050 | legit | roman_urdu | 0.708 | NO_OBVIOUS | Tumharay bhejay huay paisay abhi meray account mein nahi aye. App mein aa jayein to bata dun ga. Filhal dob… |
| cg-0051 | legit | roman_urdu | 0.164 | NO_OBVIOUS | Bijli ke bill ki aakhri tareekh kal hai. Raqam aur reference apne asal bill se mila kar apni banking app me… |
| cg-0052 | legit | roman_urdu | 0.061 | NO_OBVIOUS | Aap ki 340 rupay ki card payment mukammal hui. Agar yeh khareedari aap ne nahi ki to card ke peechay diye g… |
| cg-0053 | legit | roman_urdu | 0.080 | NO_OBVIOUS | 0TP 731602: isay sirf apni shuru ki hui verification mein daalein. Agent ko 7 3 1 6 0 2 likh kar bhi na bhe… |
| cg-0054 | legit | roman_urdu | 0.092 | NO_OBVIOUS | J@zzCash ban kar koi PIN poochay to mat batana. Brand ka naam likha hona tasdeeq nahi; apni app mein suppor… |
| cg-0055 | legit | roman_urdu | 0.857 | SUSPICIOUS | BISP ke naam par koi registration fee apne zaati number par maangay to paisay na bhejein. Apni eligibility … |
| cg-0056 | legit | roman_urdu | 0.043 | NO_OBVIOUS | Parcel aap ne order kiya tha, delivery par 1650 rupay dene hain. Order ki raqam apni receipt se mila lena. … |
| cg-0057 | legit | english | 0.056 | NO_OBVIOUS | Your one-time code is 684219. Enter it only in the app session you started. Staff will never ask you to sen… |
| cg-0058 | legit | english | 0.021 | NO_OBVIOUS | Rs 2,750 debited for your grocery purchase. Available balance: Rs 8,460. |
| cg-0059 | legit | english | 0.783 | SUSPICIOUS | Scam example: 'Your account will be blocked; pay a verification fee now.' Do not follow that instruction. O… |
| cg-0060 | legit | english | 0.926 | HIGH | Could you send your share of yesterday's dinner when you have time? Use the account we already use. Call me… |
| cg-0061 | legit | english | 0.161 | NO_OBVIOUS | Reminder: the school fee shown on your existing invoice is due tomorrow. Pay at the school office or throug… |
| cg-0062 | legit | english | 0.128 | NO_OBVIOUS | Small business finance applications are open. Approval depends on eligibility and assessment; it is not gua… |
| cg-0063 | legit | english | 0.743 | SUSPICIOUS | Your printer repair is complete. Test it at the counter before paying the agreed Rs 1,100. We can give you … |
| cg-0064 | legit | english | 0.860 | SUSPICIOUS | The community centre timetable is posted at centre-hours.example. The page is public and does not need a lo… |
| cg-0065 | legit | english | 0.206 | NO_OBVIOUS | Weekend offer: 15% off notebooks bought in our shop. The discount is applied at the till. There is no prize… |
| cg-0066 | legit | english | 0.536 | NO_OBVIOUS | Your cancelled order refund of Rs 920 has been returned through the original payment method. Check the orig… |
| cg-0067 | legit | urdu | 0.296 | NO_OBVIOUS | آپ کا یک وقتی کوڈ 529184 ہے۔ اسے صرف اپنی شروع کی ہوئی کارروائی کے لیے ایپ میں درج کریں۔ یہ کوڈ کسی شخص کو … |
| cg-0068 | legit | urdu | 0.431 | NO_OBVIOUS | آپ کے اکاؤنٹ میں 3200 روپے جمع ہوئے ہیں۔ تفصیل اپنی بینک ایپ میں دیکھی جا سکتی ہے۔ اس اطلاع کے جواب میں کوئ… |
| cg-0069 | legit | urdu | 0.886 | SUSPICIOUS | اگر کوئی کہے کہ انعام لینے کے لیے پہلے فیس بھیجیں تو رک جائیں۔ انعام کے دعوے کی آزادانہ تصدیق کریں اور کسی … |
| cg-0070 | legit | urdu | 0.212 | NO_OBVIOUS | امی، دوائی لے لی ہے، 680 روپے بنے تھے۔ فرصت سے وہی رقم واپس کر دینا۔ رسید گھر آ کر دکھا دوں گا، کوئی جلدی ن… |
| cg-0071 | legit | urdu | 0.248 | NO_OBVIOUS | پچھلی رسید کے 1450 روپے باقی ہیں۔ مہینے کا حساب بند کرنا ہے، آج دکان پر جمع کرا دیں۔ |
| cg-0072 | legit | urdu | 0.622 | NO_OBVIOUS | قرض کی درخواست دینے سے پہلے شرحِ منافع، فیس اور ادائیگی کی مدت تحریری طور پر پڑھ لیں۔ منظوری اہلیت کی جانچ … |
| cg-0073 | legit | urdu | 0.090 | NO_OBVIOUS | آپ کی کرسی کی مرمت مکمل ہے۔ دکان پر دیکھ کر تسلی کر لیں، پھر طے شدہ 900 روپے ادا کریں۔ رسید اسی وقت مل جائے… |
| cg-0074 | legit | urdu | 0.343 | NO_OBVIOUS | محلے کی لائبریری کے نئے اوقات library-times.example پر درج ہیں۔ اس صفحے پر صرف معلومات ہیں، کوئی رجسٹریشن ف… |
| cg-0075 | legit | mixed | 0.440 | NO_OBVIOUS | Your code: 816294. اسے کسی کو نہ بتائیں۔ Sirf apni kholi hui app mein enter karein, support agent ko forwar… |
| cg-0076 | legit | mixed | 0.040 | NO_OBVIOUS | Rs 1,250 refund processed ✅ Raqam original payment method par gayi hai. کوئی نئی ادائیگی منظور نہ کریں؛ sta… |
| cg-0077 | legit | mixed | 0.898 | SUSPICIOUS | Urgent security reminder: '0TP bhejo warna wallet band' aik scam ka jumla ho sakta hai. اپنا کوڈ کسی کو نہ … |
| cg-0078 | legit | mixed | 0.003 | NO_OBVIOUS | Lunch ka split Rs 430 per person bana. آج رات تک bhej dena please, I paid the whole bill. |
| cg-0079 | legit | mixed | 0.977 | HIGH | Invoice reminder: is mahine ki tuition fee Friday ko due hai. رسید والا amount office par jama karein; acco… |
| cg-0080 | legit | mixed | 0.458 | NO_OBVIOUS | Book fair offer 📚 Is weekend 20% discount at the counter. کوئی advance fee نہیں۔ Details book-fair.example … |

</details>

## Demo library (ML-only scores; the app adds indicator fusion)

| Sample | Example of | ML score | ML-only verdict |
|---|---|---|---|
| demo-prize-ru | Prize scam (Roman Urdu) | 1.000 | HIGH |
| demo-wallet-suspension | Fake wallet suspension | 1.000 | HIGH |
| demo-otp-ru | Fake bank OTP request | 0.996 | HIGH |
| demo-urdu-otp | Urdu-script scam | 1.000 | HIGH |
| demo-loan-ru | Fake loan offer | 1.000 | HIGH |
| demo-phishing-en | English phishing | 1.000 | HIGH |
| demo-legit-alert | Legitimate bank-style alert | 0.004 | NO_OBVIOUS |
| demo-legit-otp | Legitimate OTP delivery | 0.002 | NO_OBVIOUS |
| demo-legit-family | Legitimate family message | 0.002 | NO_OBVIOUS |
| demo-ambiguous | Ambiguous: verify first | 0.492 | NO_OBVIOUS |

Demo samples found in training data: **0**. Challenge samples found in training data: **0**.

## Thresholds (chosen on out-of-fold development scores only)

- **Suspicious** ≥ 0.73: lowest out-of-fold threshold with FPR <= 5%, floor 0.25
- **High Risk** ≥ 0.9: lowest out-of-fold threshold with FPR <= 1% and precision >= 0.97, floor 0.6
- The floors are a product decision. Synthetic data is easier than real SMS, so the thresholds aren't
  allowed to drop just because cross-validation scores were extreme.

## Dataset & leakage controls

- 2457 generated rows → 377 exact duplicates after normalisation removed → **2080 rows** (1084 scam / 996 legit) from 273 template families.
- Split by template family (StratifiedGroupKFold, 5 folds): 1 fold is the held-out **test** set (416 rows, 55 families), and 4 folds are **development** data (1664 rows, 218 families) used for grouped 4-fold cross-validation and then for fitting the final model.
- Language mix (all rows): english 684, roman_urdu 650, mixed 425, urdu 321.
- Shared families dev↔test: **0**; between any two folds: 0; identical normalised texts dev↔test: **0** (between any folds: 0).
- Near-duplicates (character TF-IDF cosine to the nearest development message): mean 0.4037, max 0.7966, 0.0% of test messages above 0.9, 0.0% above 0.8. Shared slot values (brand names, amounts) and common phrasing produce some similarity even across families.
- Vocabulary and IDF weights are fitted only on the training portion of each fit (never on test).

## Model selection (grouped cross-validation on development data)

Criterion: grouped 4-fold cross-validation on dev, out-of-fold log-loss (tie: smaller vocabulary). Selected **char2-4**, C=256.0.

| Config | C | Mean vocab | OOF log-loss | OOF AP | OOF ROC-AUC | OOF F1@0.5 |
|---|---|---|---|---|---|---|
| char2-4 | 1.0 | 8,083 | 0.3906 | 0.9693 | 0.9679 | 0.8976 |
| char2-4 | 4.0 | 8,083 | 0.2959 | 0.975 | 0.9733 | 0.9072 |
| char2-4 | 16.0 | 8,083 | 0.24 | 0.9773 | 0.9754 | 0.9066 |
| char2-4 | 64.0 | 8,083 | 0.2159 | 0.9761 | 0.9744 | 0.9111 |
| char2-4 | 256.0 | 8,083 | 0.2028 | 0.9776 | 0.9755 | 0.9145 |
| char2-4 | 1024.0 | 8,083 | 0.2963 | 0.9588 | 0.9599 | 0.8986 |
| char2-5 | 1.0 | 11,957 | 0.3881 | 0.9688 | 0.9687 | 0.9024 |
| char2-5 | 4.0 | 11,957 | 0.2941 | 0.9742 | 0.9734 | 0.9107 |
| char2-5 | 16.0 | 11,957 | 0.2389 | 0.9756 | 0.9749 | 0.9168 |
| char2-5 | 64.0 | 11,957 | 0.2139 | 0.9759 | 0.9745 | 0.9171 |
| char2-5 | 256.0 | 11,957 | 0.2053 | 0.9756 | 0.9747 | 0.9157 |
| char2-5 | 1024.0 | 11,957 | 0.2952 | 0.9624 | 0.9637 | 0.9093 |
| char3-5 | 1.0 | 11,076 | 0.386 | 0.9703 | 0.9699 | 0.9122 |
| char3-5 | 4.0 | 11,076 | 0.2916 | 0.9746 | 0.9739 | 0.9213 |
| char3-5 | 16.0 | 11,076 | 0.2348 | 0.9768 | 0.976 | 0.9238 |
| char3-5 | 64.0 | 11,076 | 0.2072 | 0.9768 | 0.9763 | 0.9258 |
| char3-5 | 256.0 | 11,076 | 0.2555 | 0.9598 | 0.9622 | 0.9115 |
| char3-5 | 1024.0 | 11,076 | 0.2543 | 0.9653 | 0.9655 | 0.91 |
| char2-5+word1-2 | 1.0 | 17,273 | 0.39 | 0.9725 | 0.972 | 0.9095 |
| char2-5+word1-2 | 4.0 | 17,273 | 0.2923 | 0.9776 | 0.9769 | 0.9238 |
| char2-5+word1-2 | 16.0 | 17,273 | 0.2348 | 0.979 | 0.978 | 0.9226 |
| char2-5+word1-2 | 64.0 | 17,273 | 0.2048 | 0.9796 | 0.9783 | 0.9187 |
| char2-5+word1-2 | 256.0 | 17,273 | 0.2507 | 0.9653 | 0.9659 | 0.9139 |
| char2-5+word1-2 | 1024.0 | 17,273 | 0.2448 | 0.9715 | 0.9714 | 0.9134 |

## What the model learned (largest weights)

Character n-grams are shown with `·` for the word-boundary space. `zphonez` / `zurlz` / `zuanz` are placeholders
the normaliser substitutes for phone numbers, links and helpline (UAN) numbers.

| Towards scam | weight | Towards legitimate | weight |
|---|---|---|---|
| `pk` | 5.744 | `0000` | -9.127 |
| `·r` | 5.74 | `·on·` | -5.948 |
| `apk` | 5.68 | `·o` | -5.26 |
| `hon` | 5.527 | `oct` | -5.236 |
| `zp` | 5.141 | `·oct` | -5.236 |
| `hone` | 5.115 | `·oc` | -5.236 |
| `nez·` | 5.054 | `oct·` | -4.882 |
| `zpho` | 5.054 | `ct·` | -4.631 |
| `zph` | 5.054 | `·on` | -4.621 |
| `onez` | 5.054 | `di` | -4.388 |
| `nez` | 5.054 | `·00·` | -4.317 |
| `·zph` | 5.054 | `isi` | -4.01 |
| `·zp` | 5.054 | `p·` | -3.858 |
| `ez·` | 4.91 | `app` | -3.836 |
| `rn` | 4.893 | `·na·` | -3.785 |
| `phon` | 4.788 | `·ma` | -3.546 |
| `nd·` | 4.783 | `bil` | -3.519 |
| `ez` | 4.758 | `di·` | -3.508 |
| `·z` | 4.525 | `oc` | -3.46 |
| `·rs` | 4.26 | `bi` | -3.458 |

## Export, parity and speed

- Exported JSON: 231.5 KB, 8,973 features, weights rounded to 7 significant digits; max |p_json − p_sklearn| on test = 2.06e-07.
- TypeScript parity is checked by `apps/mobile/src/engine/__tests__/parity.test.ts` against `ml/artifacts/parity-fixtures.json` (normalised text must match exactly, and the score must match to within 1e-9).
- Python latency per message (dev container, not a phone): scikit-learn 0.834 ms, pure-Python JSON reference 0.219 ms. The app measures and shows real on-device latency.

## Development history (honest record)

The test fold was looked at after each of these runs, so the final numbers are not a perfectly "blind" estimate.
Changes between runs were driven by validation/cross-validation error analysis (more phrasings, more Urdu script,
more hard negatives, CV-based selection), not by editing templates to match specific test messages. The
hand-written challenge set and the independent ChatGPT set are the better guides to generalisation.

| Run | Change | Test rows | ROC-AUC | Thresholds (susp/high) | Recall @Susp | FPR @Susp | Precision @High |
|---|---|---|---|---|---|---|---|
| v0-metrics | 211 families, 2 phrasings each; single train/val split; selection + thresholds on validation | 324 | 0.9312 | 0.73 / 0.8 | 57.3% | 6.2% | 89.5% |
| v1-metrics | +62 families (3 phrasings, more Urdu script & hard negatives) after validation error analysis; single split | 416 | 0.9633 | 0.81 / 0.89 | 83.4% | 7.5% | 94.4% |
| **v2 (shipped)** | grouped 4-fold CV for selection + thresholds; final fit on all dev data | 416 | 0.9745 | 0.73 / 0.9 | 93.5% | 8.0% | 94.3% |

## Known limitations

- Synthetic data: real scams are more diverse, change over time, and include formats (voice calls, images) this model never sees.
- The model can be fooled by adversarial rewording. The indicator engine and the advice to always verify
  through official channels are the safety net.
- Small per-category test counts, so category-level numbers are indicative only.
- Next step: a consented pilot dataset of real, anonymised messages, labelled by fraud analysts.

