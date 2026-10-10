"""Second batch of template families (dataset v1).

Added after the first training run (v0, kept in ml/artifacts/history/) showed
that validation errors came from too few distinct phrasings, especially in Urdu
script, and from under-represented hard negatives (legitimate refunds and
security advice). Every family here has three phrasings.

These families deliberately avoid the topics of the hand-written challenge set
(job/visa fees, customs parcels, crypto withdrawal tax, Hajj ballots, romance
gifts, fake buyers, rental advances, prize bonds, reward-point expiry, SIM
upgrades) so the challenge set stays "unfamiliar".
"""

SCAM_FAMILIES_EXTRA = [
    # ------------------------------------------------------------------ prize_lottery
    ("prize-16", "prize_lottery", "urdu", [
        "مبارک ہو! آپ کا نمبر قرعہ اندازی میں نکل آیا ہے اور آپ نے {product} جیتی ہے۔ ڈیلیوری چارجز {fee_ur} پہلے ادا کریں۔",
        "خوشخبری! {telco_ur} کے لکی ڈرا میں آپ کا نام آیا ہے۔ انعام کی رقم {amount_big_ur} آپ کے اکاؤنٹ میں بھیجنے کے لیے {fee_ur} پروسیسنگ فیس درکار ہے۔",
        "آپ خوش قسمت ہیں! آپ کے نمبر پر {amount_big_ur} کا انعام نکلا ہے، رقم وصول کرنے کے لیے فوری طور پر {phone} پر کال کریں اور فیس جمع کروائیں۔",
    ]),
    ("prize-17", "prize_lottery", "urdu", [
        "{show_ur}: آپ کو انعامی رقم {amount_big_ur} کا حقدار قرار دیا گیا ہے۔ تصدیق کے لیے اپنا شناختی کارڈ نمبر اور {fee_ur} بھیجیں۔",
        "محترم صارف، آپ کا انعامی چیک تیار ہے۔ چیک بھیجنے سے پہلے {fee_ur} کورئیر چارجز {wallet_ur} کریں۔",
        "انعام وصول کرنے کا آخری موقع! آج رات 12 بجے سے پہلے {fee_ur} ٹیکس جمع کروائیں ورنہ انعام منسوخ ہو جائے گا۔",
    ]),
    ("prize-18", "prize_lottery", "mixed", [
        "Hello dear, aap ka number {wallet} ki anniversary celebration mein winner nikla hai! {amount_big} aap ke hain, bas {fee} service charges pay karne hain.",
        "Winner announcement: {first} ji aap ne {product} jeet li hai, delivery ke liye {fee} charges {wallet} kar dein {phone} pe.",
        "Aap ka SIM {amount_big} cash prize ke liye select ho gaya hai. Prize claim form fill karne ke liye {fee} fee advance jama karwani hogi.",
    ]),
    ("prize-19", "prize_lottery", "english", [
        "Dear valued customer, you are the lucky winner of {amount_big} from {telco}. Your winning code is HS-{otp}. Call {phone} with your code to claim.",
        "{telco} Rewards: your number won the weekly mega prize of {amount_big}. Claim before 6 PM by paying the {fee} transfer charge.",
        "Hurray! You are 1 of 5 winners of the {show}. Your prize {product} is ready for dispatch once the {fee} handling fee is received.",
    ]),
    ("prize-20", "prize_lottery", "roman_urdu", [
        "Aap ke liye khushkhabri! Aap ne {show} ka bumper inaam {amount_big} jeeta hai. Raqam lene ke liye pehle {fee} jama karwana lazmi hai.",
        "Inaam ki raqam {amount_big} aap ke account mein bhejne ke liye sirf {fee} government tax ada karna hai. Tax {phone} pe bhejein.",
        "Mubarak! Aap ka inaami cheque tayyar hai. Cheque collect karne ke liye {fee} fee abhi {wallet} karein.",
    ]),
    # ------------------------------------------------------------------ otp_pin_theft
    ("otp-15", "otp_pin_theft", "urdu", [
        "{bank_ur}: آپ کا اے ٹی ایم کارڈ بلاک کر دیا گیا ہے۔ کارڈ دوبارہ چالو کرنے کے لیے اپنا پن کوڈ اور کارڈ نمبر بتائیں۔",
        "آپ کے موبائل اکاؤنٹ کی تصدیق باقی ہے، ابھی آپ کو جو کوڈ موصول ہوا ہے وہ ہمارے نمائندے کو بتا دیں۔",
        "سیکیورٹی وجوہات کی بنا پر آپ کا اکاؤنٹ عارضی طور پر روک دیا گیا ہے، بحالی کے لیے اپنا ایم پن بتائیں۔",
    ]),
    ("otp-16", "otp_pin_theft", "urdu", [
        "السلام علیکم، میں {wallet_ur} ہیلپ لائن سے بات کر رہا ہوں۔ آپ کے نمبر پر ایک کوڈ آیا ہے، براہ کرم وہ کوڈ بتا دیں۔",
        "آپ کا انعام آپ کے اکاؤنٹ میں منتقل کرنے کے لیے جو کوڈ ابھی آیا ہے وہ اس نمبر {phone} پر بھیج دیں۔",
        "{wallet_ur} کی طرف سے: اکاؤنٹ اپڈیٹ کرنے کے لیے موصول ہونے والا چار ہندسوں کا کوڈ ہمیں واپس بھیجیں۔",
    ]),
    ("otp-17", "otp_pin_theft", "mixed", [
        "Hello, {wallet} se call thi. System update ke liye jo 4 digit code aapko aya hai woh bata dein, warna account temporarily band ho jayega.",
        "Sir aap ke card pe international transaction try hui hai. Usko cancel karne ke liye jo OTP aya hai woh confirm karein please.",
        "Dear user aap ki ID verify karni hai, code share karein jo abhi SMS mein aya, it is just for verification.",
    ]),
    ("otp-18", "otp_pin_theft", "english", [
        "We are upgrading your {wallet} account to Gold. Please reply with your current MPIN and the code you receive to complete the upgrade.",
        "Your {bank} internet banking will expire today. Send your username, password and the OTP to our support desk to renew it.",
        "Security check: confirm your card PIN by replying to this message. Failure to confirm will block your card.",
    ]),
    ("otp-19", "otp_pin_theft", "roman_urdu", [
        "Aap ke account mein kisi ne login karne ki koshish ki hai. Rokne ke liye abhi aane wala code hamare numainde ko bata dein.",
        "Hum {bank} se baat kar rahe hain, aap ka card renew hona hai. Card ke peeche likhe 3 number aur expiry bata dein.",
        "Aap ke wallet ki security update ho rahi hai, apna PIN aur code is number pe SMS kar dein {phone}.",
    ]),
    # ------------------------------------------------------------------ impersonation
    ("imp-14", "impersonation", "urdu", [
        "میں اسٹیٹ بینک آف پاکستان سے بات کر رہا ہوں، آپ کے اکاؤنٹ سے مشکوک لین دین ہوا ہے، اپنی رقم محفوظ اکاؤنٹ میں منتقل کریں۔",
        "پی ٹی اے کی طرف سے اطلاع: آپ کا موبائل نمبر بند ہونے والا ہے، فوری طور پر {phone} پر رابطہ کر کے اپنی تفصیلات تصدیق کروائیں۔",
        "ایف بی آر نوٹس: آپ پر جرمانہ عائد کیا گیا ہے، {fee_ur} فوری جمع کروائیں ورنہ قانونی کارروائی ہو گی۔",
    ]),
    ("imp-15", "impersonation", "mixed", [
        "Assalam o alaikum, main {bank} ke fraud department se {name} baat kar raha hoon. Aap ke account ki security ke liye aap ki details confirm karni hain.",
        "Sir {wallet} head office se call hai, aap ke account pe complaint aayi hai. Hamare officer ko {phone} pe call back karein jaldi.",
        "Hello main NADRA se bol raha hoon, aap ke CNIC ki tasdeeq honi hai warna aap ka bank account band ho jayega. Details bataein.",
    ]),
    ("imp-16", "impersonation", "english", [
        "Officer {name} from the State Bank here. Your savings are at risk. Move your balance to the protected government account shared by our team today.",
        "This is NADRA verification. Your CNIC is linked to a suspicious bank account. Reply with your card and account details to clear your name.",
        "{wallet} compliance team: we need to re-verify your identity. Our agent will call you, please keep your PIN ready.",
    ]),
    ("imp-17", "impersonation", "roman_urdu", [
        "Main {telco} franchise se bol raha hoon, aap ka number dobara register hona hai. Apne {wallet} ka PIN bata dein taake process complete ho.",
        "Bank se bol rahe hain, aap ki file mein masla hai. Hamara officer ghar aayega, us ko apna card aur PIN de dena.",
        "Hum police station {city} se hain. Aap ke CNIC pe case darj hai, settlement ke liye {fee} hamare officer ke number pe bhejein.",
    ]),
    # ------------------------------------------------------------------ loan_fee
    ("loan-13", "loan_fee", "urdu", [
        "آپ کو {loanapp} کی طرف سے {amount_big_ur} کا قرض دیا جا رہا ہے، رقم وصول کرنے سے پہلے {fee_ur} انشورنس فیس جمع کروائیں۔",
        "قرض کی رقم آپ کے اکاؤنٹ میں منتقل کرنے کے لیے {fee_ur} سیکیورٹی ڈپازٹ ضروری ہے، ابھی {phone} پر بھیجیں۔",
        "حکومتی قرضہ اسکیم میں آپ کا نام شامل ہے، {amount_big_ur} حاصل کرنے کے لیے {fee_ur} فارم فیس ادا کریں۔",
    ]),
    ("loan-14", "loan_fee", "english", [
        "Your loan request for {amount_big} has been pre-approved. Pay the {fee} verification charge today and the amount will be credited within 1 hour.",
        "Low interest loans for everyone! {amount_big} available today. One-time registration fee {fee} payable to our agent {phone}.",
        "Dear applicant, your file has cleared all checks. Release of {amount_big} requires an advance insurance premium of {fee}.",
    ]),
    ("loan-15", "loan_fee", "mixed", [
        "Sir aap ka {amount_big} ka loan pass ho gaya hai. Bas ek chhoti si formality hai, {fee} file charges {wallet} kar dein.",
        "Loan chahiye? 24 ghante mein {amount_big}, koi bank statement nahi. Pehle {fee} registration aur baqi kaam hamara.",
        "{first} sahab aap ka loan cheque ready hai, {fee} stamp duty bhejein to aaj hi courier kar dete hain.",
    ]),
    ("loan-16", "loan_fee", "roman_urdu", [
        "Aap ko {amount_big} ka qarza mil sakta hai sirf CNIC ki copy pe. Shart sirf ye hai ke {fee} pehle jama karwayein.",
        "Qarza manzoor! {amount_big} lene ke liye {fee} insurance fees is number pe Easypaisa karein {phone}.",
        "Asaan qiston pe qarza, koi zamanat nahi. Darkhwast fee {fee} abhi bhejein aur kal tak raqam payein.",
    ]),
    # ------------------------------------------------------------------ payment_request
    ("pay-14", "payment_request", "urdu", [
        "بیٹا یہ میرا نیا نمبر ہے، فوری طور پر {amount_ur} اس اکاؤنٹ میں بھیج دو، بعد میں بات کرتا ہوں۔",
        "بھائی ایمرجنسی ہے، {amount_ur} ابھی اس {wallet_ur} نمبر پر بھیج دو، کال نہیں کر سکتا۔",
        "میں مشکل میں ہوں، میرا بٹوہ چوری ہو گیا ہے، {amount_ur} اس نمبر پر بھیج دیں، کل واپس کر دوں گا۔",
    ]),
    ("pay-15", "payment_request", "english", [
        "Mom, I changed my number. I'm in trouble and need {amount} right now, please send it to this {wallet} account. Don't call, I'll explain later.",
        "Hi it's me, my phone broke and this is a friend's number. Can you transfer {amount} urgently? I'll pay you back tomorrow.",
        "Dad please send {amount} to {phone} immediately, it's an emergency. Don't tell anyone, I will explain at home.",
    ]),
    ("pay-16", "payment_request", "roman_urdu", [
        "Assalam o alaikum chachu, main {first} hoon naye number se. Foran {amount} chahiye fees ke liye, is number pe bhej dein please.",
        "Khala jaan mera phone chori ho gaya hai, ye naya number hai. {amount} ki sakht zaroorat hai, {wallet} kar dein abhi.",
        "Bhai jaan main musibat mein hoon, kisi ko mat batana. {amount} abhi bhejo is number pe {phone}, shaam ko sab bataunga.",
    ]),
    ("pay-17", "payment_request", "mixed", [
        "Dear parent, aap ke bachay ki trip fee {amount} aaj hi is {wallet} account pe jama karwayein, school account temporarily band hai.",
        "Sir aap ki bijli ki file pending hai, connection bachane ke liye {amount} hamare officer ke {wallet} pe bhejein abhi.",
        "Sir hum {merchant} se hain, aap ka bill double charge ho gaya tha, adjust karne ke liye {amount} is account mein bhejein warna connection kat jayega.",
    ]),
    # ------------------------------------------------------------------ account_suspension
    ("susp-14", "account_suspension", "urdu", [
        "آپ کا {wallet_ur} اکاؤنٹ غیر فعال ہونے والا ہے۔ فعال رکھنے کے لیے اس لنک پر کلک کر کے تفصیلات اپڈیٹ کریں {url_scam}",
        "آپ کی سم کی بائیو میٹرک تصدیق نامکمل ہے، آپ کا نمبر اور اکاؤنٹ کل بند کر دیا جائے گا۔ ابھی {phone} پر کال کریں۔",
        "{bank_ur}: آپ کا ڈیبٹ کارڈ معطل کر دیا گیا ہے۔ کارڈ بحال کرنے کے لیے اس لنک پر اپنی معلومات درج کریں {url_scam}",
    ]),
    ("susp-15", "account_suspension", "roman_urdu", [
        "Aap ka {wallet} account aaj raat 12 baje se band ho jayega. Band hone se bachane ke liye foran {phone} pe call karein.",
        "Ittila: aap ke {bank} account mein ghair qanooni activity payi gayi hai, is liye account rok diya gaya hai. Bahali ke liye link kholein {url_scam}",
        "Aap ki KYC mukammal nahi, is liye wallet band kiya ja raha hai. Abhi details bhejein warna balance zabt.",
    ]),
    ("susp-16", "account_suspension", "english", [
        "Your {wallet} account has been restricted. To lift the restriction, confirm your MPIN at {url_scam} within 6 hours.",
        "Account Notice: unusual sign-in detected. Your {bank} account is locked. Unlock now: {url_scam}",
        "We could not verify your identity. Your {fi} account will be closed in 24 hours unless you update your details by calling {phone}.",
    ]),
    ("susp-17", "account_suspension", "mixed", [
        "{wallet} account deactivation notice: aap ka account incomplete documents ki wajah se band ho raha hai. Update now {url_scam}",
        "Dear {bank} customer aap ka card expire hone wala hai aur account block ho jayega. Renewal ke liye link pe click karein {url_scam}",
        "Account freeze warning! {fi} ne aap ka account hold kar diya hai. Unhold karwane ke liye agent se rabta karein {phone}",
    ]),
    # ------------------------------------------------------------------ investment
    ("inv-13", "investment", "urdu", [
        "{company} میں سرمایہ کاری کریں اور ہر مہینے {amount_big_ur} کمائیں، کوئی خطرہ نہیں۔ ابھی {fee_ur} جمع کروا کر ممبر بنیں۔",
        "صرف سات دن میں اپنی رقم دگنی کریں! محدود پیشکش، ابھی {phone} پر رابطہ کریں۔",
        "سونے کی تجارت میں حصہ ڈالیں اور ہر ہفتے یقینی منافع حاصل کریں۔ کم از کم سرمایہ {fee_ur}۔",
    ]),
    ("inv-14", "investment", "roman_urdu", [
        "Ghar baithe har mahine {amount_big} kamaein! {company} mein sirf {fee} laga kar shamil hon, munafa pakka.",
        "Har hafte 15% munafa ki guarantee! {company} mein paise lagayein aur befikar ho jayein. Rabta {phone}",
        "Apne paise teen guna karein sirf 60 din mein. {company} ki khas scheme, aaj aakhri din.",
    ]),
    ("inv-15", "investment", "english", [
        "Guaranteed 2x returns in 14 days with our AI trading bot. Minimum investment {fee}. Join now: {url_scam}",
        "Exclusive: invest in {company} gold fund and receive fixed weekly profit. Capital 100% protected. Call {phone}.",
        "Want passive income? Deposit {fee} today and earn {amount} every day for life. Limited slots.",
    ]),
    ("inv-16", "investment", "mixed", [
        "Bhai ek zabardast scheme hai, {fee} lagao aur mahine baad {amount_big} lo. Pakki guarantee hai, main khud kama raha hoon.",
        "Online earning ka asaan tareeqa! Rozana {amount} kamayein, sirf {fee} se account activate karein. Join karein {url_scam}",
        "{company} ki VIP membership lein aur daily profit withdraw karein, risk zero hai.",
    ]),
    # ------------------------------------------------------------------ refund_reversal
    ("ref-13", "refund_reversal", "english", [
        "Your {wallet} account received {amount} by mistake. Please return the amount to {phone} immediately or we will report your account.",
        "Hello, I accidentally sent {amount} to your number. Kindly send it back to this number, it was my hospital money.",
        "{merchant}: we overcharged you {amount}. To get it back, log in at {url_scam} with your card details.",
    ]),
    ("ref-14", "refund_reversal", "urdu", [
        "{merchant} کی طرف سے آپ کو {amount_ur} کی واپسی کرنی ہے، رقم لینے کے لیے اپنا کارڈ نمبر اور کوڈ بتائیں۔",
        "معاف کیجیے گا، میرے {amount_ur} غلطی سے آپ کے {wallet_ur} میں چلے گئے ہیں، مہربانی کر کے اس نمبر پر واپس بھیج دیں۔",
        "آپ کا بجلی کے بل کا ریفنڈ {amount_ur} منظور ہو گیا ہے، رقم وصول کرنے کے لیے اپنا پن کوڈ بھیجیں۔",
    ]),
    ("ref-15", "refund_reversal", "roman_urdu", [
        "Aap ke account mein {amount} ghalti se aa gaye hain, ye mere dukaan ke paise hain. Meharbani kar ke {phone} pe wapis bhej dein.",
        "Refund aap ka manzoor ho gaya hai, {amount} lene ke liye apna MPIN aur jo code aaye woh share karein.",
        "Aap ki transaction fail hui thi, {amount} wapis milenge. Is ke liye pehle {fee} ki tasdeeqi transfer karein.",
    ]),
]


LEGIT_FAMILIES_EXTRA = [
    # ------------------------------------------------------------------ legit_transaction_alert
    ("txn-15", "legit_transaction_alert", "urdu", [
        "{bank_ur}: آپ کے اکاؤنٹ میں تنخواہ {amount_ur} جمع ہو گئی ہے۔ تاریخ {date}۔ شکریہ۔",
        "{wallet_ur}: آپ کا موبائل لوڈ {amount_ur} کامیابی سے ہو گیا۔ ٹرانزیکشن آئی ڈی {tid}۔",
        "آپ کے {bank_ur} اکاؤنٹ سے اے ٹی ایم کے ذریعے {amount_ur} نکالے گئے۔ اگر یہ آپ نے نہیں کیا تو بینک کی ہیلپ لائن پر رابطہ کریں۔",
    ]),
    ("txn-16", "legit_transaction_alert", "urdu", [
        "{wallet_ur}: آپ کو {name_ur} کی طرف سے {amount_ur} موصول ہوئے ہیں۔ نیا بیلنس {amount_ur}۔",
        "{merchant} بل کی ادائیگی {amount_ur} کامیاب رہی۔ ریفرنس نمبر {tid}۔",
        "آپ کی رقم {amount_ur} {name_ur} کے اکاؤنٹ میں منتقل کر دی گئی ہے۔ شکریہ۔",
    ]),
    ("txn-17", "legit_transaction_alert", "mixed", [
        "{wallet}: Aap ne {merchant} ko {amount} ki payment ki. TID {tid}. Shukriya!",
        "{bank}: Aap ke account mein {name} ki taraf se {amount} credit hue hain. Ref {tid}.",
        "{wallet}: Bill payment {amount} successful. Aap ka balance {amount} hai.",
    ]),
    ("txn-18", "legit_transaction_alert", "english", [
        "{merchant}: Your refund of {amount} has been credited to your {wallet} wallet. Check your transaction history in the app.",
        "{bank}: Reversal of {amount} for a failed ATM withdrawal on {date} has been credited to A/C {acct}.",
        "{wallet}: The {amount} you paid at {merchant} was refunded on {date} because the order was cancelled.",
    ]),
    # ------------------------------------------------------------------ legit_otp_delivery
    ("otpd-12", "legit_otp_delivery", "urdu", [
        "آپ کا {wallet_ur} لاگ ان کوڈ {otp} ہے۔ یہ کوڈ کسی کو نہ بتائیں، {wallet_ur} کبھی آپ سے کوڈ نہیں مانگتا۔",
        "{bank_ur}: آن لائن خریداری کے لیے آپ کا او ٹی پی {otp} ہے۔ یہ پانچ منٹ کے لیے کارآمد ہے۔",
        "آپ کا تصدیقی کوڈ {otp} ہے۔ اگر آپ نے یہ درخواست نہیں کی تو اس پیغام کو نظر انداز کریں۔",
    ]),
    ("otpd-13", "legit_otp_delivery", "roman_urdu", [
        "{bank}: Aap ki online transaction {amount} ke liye OTP {otp} hai. Ye code kisi ke sath share na karein.",
        "Aap ka {merchant} account verify karne ka code {otp} hai. Code kisi ko na bataein, hum kabhi call kar ke code nahi mangte.",
        "{wallet}: Naye device pe login ke liye code {otp}. Agar ye aap nahi to foran {uan} pe call karein.",
    ]),
    ("otpd-14", "legit_otp_delivery", "english", [
        "{otp} is your {wallet} transaction code for sending {amount} to {name}. Do not share it with anyone.",
        "Your {bank} PIN generation OTP is {otp}. Bank staff will never ask for this code.",
        "Verification code: {otp}. Valid for 2 minutes. If you did not request this code, someone may be trying to access your account; do not share it.",
    ]),
    # ------------------------------------------------------------------ legit_security_advice
    ("sec-13", "legit_security_advice", "urdu", [
        "{wallet_ur}: اپنا ایم پن کسی کو نہ بتائیں۔ ہمارا عملہ کبھی فون کر کے آپ سے کوڈ یا پن نہیں مانگتا۔",
        "خبردار: جعلی قرضہ ایپس سے بچیں۔ قرض صرف بینک یا مستند ایپ سے حاصل کریں اور کسی کو پیشگی فیس نہ دیں۔",
        "اگر کوئی خود کو بینک کا ملازم بتا کر رقم کسی محفوظ اکاؤنٹ میں منتقل کرنے کو کہے تو یہ فراڈ ہے۔",
    ]),
    ("sec-14", "legit_security_advice", "english", [
        "Scam alert: fraudsters are posing as {wallet} staff and asking for verification codes. {wallet} never asks for your code. Hang up and report.",
        "Tip: if someone says you have won a prize but must pay a fee first, it is a scam. Never send money to claim a prize.",
        "Received a message saying your account will be blocked? Do not click any link. Open the official {fi} app or call the number on your card.",
    ]),
    ("sec-15", "legit_security_advice", "roman_urdu", [
        "Yaad rakhein, koi bhi inaam lene ke liye fees nahi deni parti. Agar koi fees mange to samajh lein dhoka hai.",
        "Beta agar koi call kare ke tumhara account band ho raha hai to ghabrana nahi, khud bank ki official helpline pe call kar ke poochna.",
        "Bhai ek baat yaad rakhna, kisi ke kehne pe apna PIN ya code kabhi share nahi karna, chahe woh bank ka naam le.",
    ]),
    ("sec-16", "legit_security_advice", "mixed", [
        "{bank} awareness: hum kabhi SMS pe link bhej kar login nahi karwate. Aisi link aaye to delete karein aur report karein.",
        "Cyber safety tip: unknown links pe click na karein aur OTP kisi ko na dein. Stay hoshiyar!",
        "Agar aap ko lagta hai fraud hua hai to foran apne bank ki official helpline pe call kar ke card block karwayein.",
    ]),
    # ------------------------------------------------------------------ legit_conversation
    ("conv-17", "legit_conversation", "urdu", [
        "امی جان آج میں دیر سے گھر آؤں گا، کھانا رکھ دیجیے گا۔",
        "بھائی کل بازار چلیں گے؟ عید کی شاپنگ کرنی ہے۔",
        "ابو نے کہا ہے کہ بجلی کا بل کل جمع کروا دینا، پیسے الماری میں رکھے ہیں۔",
    ]),
    ("conv-18", "legit_conversation", "urdu", [
        "آپ کو نئی نوکری بہت بہت مبارک ہو! اللہ آپ کو مزید کامیابیاں دے۔",
        "شادی کی سالگرہ مبارک ہو! اللہ آپ دونوں کو ہمیشہ خوش رکھے۔",
        "عید مبارک! آپ کو اور آپ کے گھر والوں کو ڈھیروں خوشیاں ملیں۔",
    ]),
    ("conv-19", "legit_conversation", "roman_urdu", [
        "Yaar kal ki class cancel ho gayi hai, sir ne group mein bataya. Assignment Monday tak jama karwana hai.",
        "Ammi ne kaha hai shaam ko sabzi le aana aur doodh bhi. Paise main de doon gi.",
        "Bhai mera laptop theek ho gaya, shop wale ne sirf {amount} liye. Bohat acha banda hai.",
    ]),
    ("conv-20", "legit_conversation", "english", [
        "Hey, are we still on for dinner on Saturday? I'll book the table if you confirm.",
        "Thanks for lending me the money last week, I've transferred it back to your account just now.",
        "Happy birthday {first}! Wishing you a wonderful year ahead.",
    ]),
    ("conv-21", "legit_conversation", "mixed", [
        "Bro kal gym chalein? Membership renew karwani hai, offer chal raha hai is hafte.",
        "Yaar bank mein line bohat lambi thi, cheque jama karwa diya finally. Ab kal tak clear ho jayega.",
        "{first} tumhara parcel aa gaya hai, maine receive kar liya. Paise COD pe de diye, baad me de dena.",
    ]),
    ("conv-22", "legit_conversation", "roman_urdu", [
        "Mubarak ho bhai, aap ki committee nikal aayi! Ab to dawat banti hai.",
        "Bohat mubarak ho, aap ke bete ka admission ho gaya. Allah kamyab kare.",
        "Mubarak ho! Nayi gari ki chabi kab mil rahi hai? Pehli ride hamari.",
    ]),
    # ------------------------------------------------------------------ legit_payment_reminder
    ("rem-13", "legit_payment_reminder", "urdu", [
        "{merchant}: آپ کے انٹرنیٹ کا بل {amount_ur} واجب الادا ہے، آخری تاریخ {date}۔ ادائیگی ایپ یا بینک سے کریں۔",
        "کمیٹی کے تمام ممبران سے گزارش ہے کہ اس ماہ کی قسط دس تاریخ تک جمع کروا دیں۔",
        "{school}: آپ کے بچے کی فیس کا واؤچر جاری کر دیا گیا ہے، آخری تاریخ {date}۔",
    ]),
    ("rem-14", "legit_payment_reminder", "mixed", [
        "{merchant} reminder: aap ka bill {amount} due hai {date} tak. Late payment pe surcharge lagega. Ignore if paid.",
        "Dear member, monthly society maintenance {amount} {date} tak office mein jama karwa dein. Shukriya.",
        "{bank} Credit Card: aap ki payment {amount} {date} tak due hai. App se pay kar sakte hain.",
    ]),
    ("rem-15", "legit_payment_reminder", "english", [
        "Your {telco} postpaid bill of {amount} is due on {date}. Pay via the official app, any bank, or a retailer.",
        "Reminder from {school}: annual fund {amount} is payable with the {month} fee voucher.",
        "This is a reminder that your car installment of {amount} will be auto-debited from your {bank} account on {date}.",
    ]),
    # ------------------------------------------------------------------ legit_loan_ad
    ("lad-11", "legit_loan_ad", "urdu", [
        "{bank_ur} کار فنانس: نئی گاڑی آسان ماہانہ اقساط پر۔ درخواست صرف برانچ یا آفیشل ایپ سے دیں۔",
        "{bank_ur}: آپ کی قرض کی درخواست موصول ہو گئی ہے، ہمارا نمائندہ برانچ میں آپ سے ملاقات کرے گا۔ کوئی فیس واجب الادا نہیں۔",
        "چھوٹے کاروبار کے لیے آسان قرضے، تفصیلات کے لیے قریبی برانچ تشریف لائیں۔",
    ]),
    ("lad-12", "legit_loan_ad", "roman_urdu", [
        "{bank} Personal Loan ab asaan sharait pe. Apply sirf {bank} app ya branch se karein. Koi advance fee nahi li jati.",
        "{wallet} app mein ab instant cash loan available hai. Apni eligibility app ke andar check karein.",
        "Ghar ki marammat ke liye {bank} se asaan qarza. Tafseel ke liye branch tashreef layein.",
    ]),
    # ------------------------------------------------------------------ legit_business_payment
    ("biz-13", "legit_business_payment", "urdu", [
        "آپ کا آرڈر کل تک پہنچ جائے گا، ادائیگی سامان وصول کرنے کے بعد کیجیے گا۔",
        "{shop}: آپ کی ادائیگی {amount_ur} کی رسید واٹس ایپ کر دی گئی ہے۔ شکریہ۔",
        "محترم سپلائر، آپ کی انوائس کی ادائیگی {amount_ur} کمپنی اکاؤنٹ سے کر دی گئی ہے۔",
    ]),
    ("biz-14", "legit_business_payment", "english", [
        "Hi {first}, as discussed, I've paid {amount} for the website design. Please share the receipt when you can.",
        "{company_legit}: Your order {tid} has been shipped. The balance of {amount} is payable on delivery as agreed.",
        "Payroll: your reimbursement of {amount} for travel expenses will be paid with this month's salary.",
    ]),
    ("biz-15", "legit_business_payment", "roman_urdu", [
        "Bhai maal ka hisaab {amount} ban gaya hai, check kar ke hamesha wale account mein bhej dena. Bill saath bhej raha hoon.",
        "{shop}: Aap ka suit tayyar hai, baqi {amount} pick up ke waqt de dijiye ga.",
        "Sir aap ki gari ki service ho gayi hai, total bill {amount}. Payment counter pe ya bank transfer, jaise munasib ho.",
    ]),
    # ------------------------------------------------------------------ legit_url_info
    ("url-11", "legit_url_info", "urdu", [
        "آپ کا {merchant} بل آن لائن دستیاب ہے، تفصیل کے لیے {url_legit} دیکھیں۔",
        "یونیورسٹی کے داخلوں کی تفصیلات اس لنک پر موجود ہیں {url_legit}",
        "آپ کا پارسل روانہ کر دیا گیا ہے، ٹریکنگ کے لیے {url_legit} پر جائیں۔",
    ]),
    ("url-12", "legit_url_info", "mixed", [
        "Yaar ye article parho, saving ke ache tips hain {url_legit}",
        "Office ki holiday list yahan hai {url_legit} , Eid ki chuttiyan check kar lo.",
        "Aap ka order {tid} ship ho gaya hai. Track karein {url_legit}",
    ]),
    # ------------------------------------------------------------------ legit_promo
    ("promo-11", "legit_promo", "urdu", [
        "{merchant}: عید سیل! تمام کپڑوں پر 40 فیصد رعایت، صرف اس ہفتے۔",
        "{telco_ur}: نیا مہینہ وار پیکج صرف {fee_ur} میں، 20 جی بی انٹرنیٹ اور منٹس۔ {code} ڈائل کریں۔",
        "مبارک ہو! آپ نے {merchant} پر خریداری پر 200 لائلٹی پوائنٹس حاصل کیے ہیں۔",
    ]),
    ("promo-12", "legit_promo", "roman_urdu", [
        "{merchant} pe weekend sale shuru! Har cheez pe 30% tak discount. Aaj hi visit karein.",
        "{wallet} ke zariye mobile load karein aur 5% cashback payein. Offer mehdood muddat ke liye.",
        "Mubarak ho! Aap {merchant} ke silver member ban gaye hain, agli khareedari pe 10% discount.",
    ]),
]
