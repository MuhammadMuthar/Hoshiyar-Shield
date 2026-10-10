# Model Evaluation: Hoshiyar Shield scam classifier

> **Auto-generated** by `ml/training/train.py` from `ml/artifacts/metrics.json`. Don't edit by hand.
> Model `hs-1.0.0+807e5952` · normaliser `hn-1.0` · generated 2026-10-10T00:24:34+00:00 · seed 20261011

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
- Python latency per message (dev container, not a phone): scikit-learn 0.793 ms, pure-Python JSON reference 0.214 ms. The app measures and shows real on-device latency.

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

