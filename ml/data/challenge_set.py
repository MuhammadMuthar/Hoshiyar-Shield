"""Hand-written challenge set (evaluation only, NEVER used for training).

Written by Claude separately from the templates to check how the model handles
*unfamiliar* scam patterns and new hard negatives. Claude also wrote the
training templates, so this is not a fully independent test. That is why
docs/COLLABORATION.md asks ChatGPT to write a second one
(ml/data/contrib/chatgpt_challenge.jsonl).

label: 1 = scam, 0 = legitimate, None = genuinely ambiguous. Ambiguous rows are
reported separately: the right outcome is "verify first", not a hard verdict.
"""

CHALLENGE = [
    # ---- unfamiliar scam patterns (not in any training template) ----
    (1, "roman_urdu", "job_fee", "Congratulations! Aap ka CV Saudi Arabia mein driver ki job ke liye shortlist ho gaya hai. Visa processing fee Rs. 15,000 aaj hi 0399-5550188 pe JazzCash karein."),
    (1, "english", "customs_parcel", "Your international parcel is held at Karachi customs. Pay customs duty Rs 3,450 via Easypaisa to 0399-5550142 to release it today."),
    (1, "roman_urdu", "govt_aid", "BISP 8171: Aap ki 25000 ki qist aa chuki hai. Hasil karne ke liye apna CNIC number aur JazzCash PIN reply karein."),
    (1, "english", "romance_gift", "Darling I sent you a gift box with dollars and gold. The courier needs Rs 20,000 clearance fee, please pay the agent at 0399-5550175 today."),
    (1, "english", "crypto_tax", "Your USDT withdrawal of $1,200 is ready. Pay 10% unlock tax to complete the withdrawal at binance-pk.example before it expires."),
    (1, "mixed", "sim_upgrade", "Jazz: Aap ki SIM 5G pe upgrade ho rahi hai. Upgrade complete karne ke liye jo code aaye woh is number pe bata dein."),
    (1, "roman_urdu", "utility_fine", "WAPDA staff: Aap ke meter ki checking hogi. Jurmane se bachne ke liye 5000 abhi hamare officer ko JazzCash karein."),
    (1, "mixed", "obfuscated", "Ap ka 0TP sh@re krein warna J@zzC@sh acc0unt bl0ck ho jaye ga!!!"),
    (1, "roman_urdu", "obfuscated", "A P K A   I N A A M   N I K L A   H A I. fee bhejain 0399-5550111 pe foran"),
    (1, "urdu", "job_fee", "آپ کو بیرون ملک نوکری کے لیے منتخب کر لیا گیا ہے، ویزا فیس 20 ہزار روپے فوری جمع کروائیں۔"),
    (1, "roman_urdu", "hajj_ballot", "Mubarak! Aap ka naam Hajj qurandazi mein aa gaya hai. Confirmation ke liye 10,000 security abhi bhejein warna naam kat jayega."),
    (1, "roman_urdu", "whatsapp_takeover", "Assalam o alaikum, main aap ke family group ka admin hoon. Group verify karne ke liye jo 6 digit code aya hai send kar dein."),
    (1, "english", "phishing", "Your Meezan Bank account requires immediate verification. Click meezan-secure.example and enter your debit card PIN."),
    (1, "roman_urdu", "govt_aid", "PM Relief Package: Rs 12,000 aap ke liye manzoor. 8171 pe apna CNIC bhejein aur 500 fee JazzCash karein."),
    (1, "mixed", "suspension", "URGENT!!! ur easypaisa will b closed tonite. call now 0399-5550199 n verify ur details"),
    (1, "roman_urdu", "investment", "Hamare WhatsApp group mein shamil ho kar rozana 3% munafa kamaein. Sirf 10,000 se shuru karein, pakki guarantee."),
    (1, "english", "reward_points", "Your HBL reward points (4,500) expire today. Redeem now at hbl-points.example by entering your card number and CVV."),
    (1, "urdu", "relative_new_number", "امی جان میرا موبائل خراب ہے، یہ دوست کا نمبر ہے، دس ہزار ایزی پیسہ کر دیں جلدی۔"),
    (1, "mixed", "refund", "Daraz se bol rahe hain, aap ka order cancel hone pe 2,999 refund ke liye jo code aaye woh share karein."),
    (1, "roman_urdu", "safe_account", "Aap ke account pe hackers ka hamla hua hai. Apna balance foran naye safe account 0399-5550160 mein muntaqil karein. Bank Security"),
    (1, "mixed", "prize_bond", "Dear winner, aap ka prize bond ka inaam 7,50,000 nikla hai. Withholding tax 15,000 pehle jama karwain."),
    (1, "english", "rental_advance", "Flat available in DHA Lahore for 35,000 rent. I am abroad, send 2 months advance via Easypaisa and I will courier the keys."),
    (1, "english", "prize", "You won! Reply with your CNIC and pay Rs 800 to claim your Rs 50,000 shopping voucher."),
    (1, "urdu", "otp", "آپ کے بینک اکاؤنٹ کی سیکیورٹی اپڈیٹ ہو رہی ہے، ابھی جو چھ ہندسوں کا کوڈ آیا ہے وہ ہمیں بتا دیں۔"),
    (1, "urdu", "loan", "صرف شناختی کارڈ پر فوری قرض حاصل کریں، کوئی ضمانت نہیں۔ فائل چارجز 1500 روپے اس نمبر پر ایزی پیسہ کریں 0399-5550133"),
    (1, "urdu", "investment", "صرف ایک ہفتے میں اپنی رقم دگنی کریں، ہماری کمپنی میں سرمایہ کاری کریں، منافع کی مکمل ضمانت۔"),
    (1, "english", "tech_support", "Microsoft support: your phone banking app is infected. Install the remote helper app and share the 9-digit access code with our engineer."),
    (1, "roman_urdu", "fake_buyer", "Main aap ka sofa khareedna chahta hoon, payment bhej di hai. Aap ko jo SMS aya hai us mein code hai, woh bhej dein taake payment release ho."),
    (1, "mixed", "loan_harass", "Final reminder: aap ki loan file pending hai. Agar aaj 2,000 legal fee nahi bheji to aap ke contacts ko message kar diya jayega."),
    (1, "english", "electricity", "K-Electric: Your connection will be disconnected at 9 PM tonight due to an unpaid bill. Pay immediately to officer 0399-5550191 to avoid disconnection."),
    # ---- legitimate hard negatives (new, not from templates) ----
    (0, "english", "otp_delivery", "Meezan Bank: Never share your OTP. Your OTP for IBFT of Rs 25,000 to Ahmed Raza is 739104."),
    (0, "roman_urdu", "family", "Ammi, 5000 bhej diye hain Easypaisa pe. Dawai le lena aur doctor ki fees bhi de dena."),
    (0, "roman_urdu", "new_number_no_money", "Bhai mera naya number save kar lo, purana band ho gaya hai. Kal milte hain."),
    (0, "english", "bill", "Your Jazz postpaid bill of Rs 1,450 is due on 15 Oct. Pay through the JazzCash app. Thank you."),
    (0, "english", "advice", "SBP: Raast is free for person-to-person transfers. Never share your PIN or OTP with anyone."),
    (0, "english", "limit_increase", "Congratulations! Your HBL credit card limit has been increased to Rs 300,000. No action is required."),
    (0, "roman_urdu", "committee", "Mubarak ho! Aap ki committee is mahine nikal aayi hai, 50,000 aap ko Friday tak mil jayenge."),
    (0, "english", "delivery", "Your Foodpanda order is on its way! Rider Bilal will reach you in 15 minutes."),
    (0, "english", "account_lock_legit", "Easypaisa: Your account has been locked after 3 wrong PIN attempts. Visit any Easypaisa retailer with your original CNIC to unlock it."),
    (0, "english", "maintenance", "LESCO: Electricity will be suspended in your area tomorrow from 9am to 1pm for maintenance."),
    (0, "urdu", "advice", "یہ پیغام آپ کی حفاظت کے لیے ہے: کسی کو اپنا پن یا کوڈ نہ بتائیں۔ میزان بینک"),
    (0, "roman_urdu", "family", "Beta exam ki fees 3,500 hai, kal tak school mein jama karwa dena. Paisay drawer mein rakh diye hain."),
    (0, "english", "friend_refund", "Hi Sana, the refund for the cancelled concert ticket (Rs 4,000) has been sent to your bank account. Please confirm when you get it."),
    (0, "english", "statement", "Your account statement for September is ready. Log in to the UBL Digital app to view it."),
    (0, "roman_urdu", "loan_friend", "Salam bhai, aap ne jo 10,000 maange thay, bhej diye hain. Jab ho sake wapis kar dena, koi jaldi nahi."),
    (0, "english", "promo", "Zong: Get 50GB monthly data for Rs 1,000. Dial *6464# to subscribe."),
    (0, "urdu", "bill", "آپ کا گیس کا بل 2,300 روپے ہے، آخری تاریخ 20 اکتوبر۔ ایس این جی پی ایل"),
    (0, "english", "appointment", "Reminder: doctor appointment tomorrow at 5 pm. Please bring previous reports. Fee Rs 2,000 payable at reception."),
    (0, "english", "cashback", "Easypaisa: Rs. 1,000 cashback has been added to your account for your bill payment. No action needed."),
    (0, "english", "card_block_legit", "HBL: As requested, your lost debit card has been blocked. Visit any branch with your CNIC to get a replacement."),
    (0, "english", "otp_delivery", "Your one-time PIN for NADRA e-Sahulat is 4821. Do not share it with anyone."),
    (0, "roman_urdu", "rent", "Mama ne kaha hai is mahine ka kiraya 25,000 unke Meezan account mein hi bhejna jo pehle se save hai."),
    (0, "english", "receipt", "Thank you for your payment of Rs 15,000 to Bright Future Academy. Receipt no 88213."),
    (0, "roman_urdu", "scam_talk", "Bhai, inaam wali calls se bach ke rehna, kal mere chachu ke saath 20,000 ka fraud ho gaya."),
    (0, "english", "webinar", "Join our free webinar on personal finance this Saturday. Register at finance-webinar.example"),
    (0, "urdu", "family", "بیٹا میں نے تمہارے اکاؤنٹ میں پانچ ہزار بھیج دیے ہیں، کتابیں خرید لینا۔"),
    (0, "urdu", "transaction", "آپ کے اکاؤنٹ سے 3,000 روپے بجلی کے بل کی ادائیگی کے لیے کاٹے گئے ہیں۔ شکریہ۔"),
    (0, "urdu", "conversation", "مبارک ہو! آپ کا بیٹا امتحان میں اول آیا ہے، سکول کی طرف سے انعام دیا جائے گا۔"),
    (0, "mixed", "office", "Sir aaj ki meeting 4 baje shift ho gayi hai, budget wali file saath le aayein."),
    (0, "english", "salary", "Your salary of Rs 85,000 for September has been credited. Thank you for your hard work this month."),
    # ---- genuinely ambiguous: the right outcome is "verify first" ----
    (None, "roman_urdu", "wrong_transfer", "Bhai, maine ghalti se aap ke JazzCash pe 2,500 bhej diye hain. Please check kar ke wapis kar dein, shukriya."),
    (None, "english", "callback", "Hello, I am Kamran from the Lahore branch. Please call me back regarding your account when you get a chance."),
    (None, "english", "delivery_link", "Your package could not be delivered. Please reschedule your delivery at courier-help.example"),
    (None, "roman_urdu", "school_call", "Assalam o alaikum, main aap ke bete ke school se bol raha hoon, fees ke hawale se baat karni hai, is number pe call karein 0399-5550147."),
    (None, "roman_urdu", "committee_new_account", "Committee ka naya member Asad hai, is mahine ki kist uske account mein bhejni hai, number 0399-5550170."),
]


def rows() -> list[dict]:
    out = []
    for i, (label, lang, pattern, text) in enumerate(CHALLENGE, start=1):
        out.append({
            "id": f"ch-{i:03d}",
            "text": text,
            "label": label,
            "language": lang,
            "pattern": pattern,
            "source": "claude_challenge",
            "synthetic": True,
        })
    return out
