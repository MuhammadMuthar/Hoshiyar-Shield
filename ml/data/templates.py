"""Template families for the Hoshiyar Shield synthetic dataset.

Each family is one *idea* (e.g. "prize + upfront fee, Roman Urdu"). It can
have several phrasings, and slots like {fee} are filled at generation time.
Train/validation/test are split **by family**, so the test set only has
message ideas the model never saw in training.

Authoring rules:
- Brand names (JazzCash, HBL, ...) appear in BOTH scam and legitimate
  families, so "mentions a bank" can never be a shortcut for "scam".
- Hard negatives on purpose: genuine OTP deliveries that say "do not share",
  security advice that mentions prizes and fees, "Mubarak ho" family
  messages, legitimate refunds, legitimate loans, legitimate lucky draws.
- All people, numbers and links are fictional placeholders (see slots in
  generate_dataset.py). No real personal data.

Family tuple: (family_id, category, language, [phrasings])
language in {"roman_urdu", "english", "urdu", "mixed"}; "mixed" means
code-switched English + Roman Urdu (the most common real SMS style).
"""

SCAM_FAMILIES = [
    # ------------------------------------------------------------------ prize_lottery
    ("prize-01", "prize_lottery", "roman_urdu", [
        "Mubarak ho! Apka {amount_big} ka inaam nikla hai. Inaam hasil karne ke liye {fee} verification fee {phone} pe bhejein.",
        "Mubarak ho! {show} ki taraf se apka number {amount_big} ke inaam ke liye select hua hai. Claim fee {fee} jama karwa kar inaam hasil karein. Rabta: {phone}",
    ]),
    ("prize-02", "prize_lottery", "roman_urdu", [
        "Apka SIM number {show} me jeet gaya hai! Inaam me {product} aur {amount_big} cash. Foran {phone} pe call karein.",
        "{show}: Apke number ne {product} jeeta hai. Delivery charges {fee} {wallet} karein aur apna inaam ghar mangwayein.",
    ]),
    ("prize-03", "prize_lottery", "english", [
        "Congratulations! Your mobile number has won {amount_big} in the {show} lucky draw. To claim, send a processing fee of {fee} to {phone} within 24 hours.",
        "CONGRATULATIONS!! You are selected as winner of {product} + {amount_big} cash prize. Pay {fee} clearance charges via {wallet} to {phone} to release your prize.",
    ]),
    ("prize-04", "prize_lottery", "urdu", [
        "مبارک ہو! آپ کا {amount_big_ur} کا انعام نکلا ہے۔ انعام وصول کرنے کے لیے {fee_ur} فیس اس نمبر {phone} پر بھیجیں۔",
        "{show_ur} کی طرف سے آپ کا نمبر انعام کے لیے منتخب ہوا ہے۔ فوری طور پر {phone} پر رابطہ کریں اور {fee_ur} رجسٹریشن فیس جمع کروائیں۔",
    ]),
    ("prize-05", "prize_lottery", "mixed", [
        "Dear customer, Congratulations! Apka {telco} number lucky draw me select hua hai. Prize: {amount_big}. Tax amount {fee} pehle {wallet} karein. Contact {phone}",
        "Dear user apka {telco} SIM lucky draw winner hai! Prize {amount_big} receive karne ke liye pehle {fee} government tax {phone} pe send karein.",
    ]),
    ("prize-06", "prize_lottery", "roman_urdu", [
        "BISP Inaami Scheme: Apke CNIC pe {amount_big} ki raqam jari hui hai. Raqam wasool karne ke liye {fee} registration fee {phone} pe bhejein.",
        "Ehsaas program me apka naam aa gaya hai. {amount_big} aapko milenge, pehle {fee} file charges jama karwayein. Call {phone}",
    ]),
    ("prize-07", "prize_lottery", "english", [
        "You have won a {product} in the {show} anniversary giveaway! Claim now at {url_scam} . Small delivery fee {fee} applies. Offer expires today.",
        "Giveaway winner! Your number was picked for a free {product}. Confirm your address and pay {fee} shipping at {url_scam} before midnight.",
    ]),
    ("prize-08", "prize_lottery", "roman_urdu", [
        "Apka naam {show} ki qurandazi me nikla hai. Inaam: {product}. Gari ki registration ke liye {fee} jama karwana zaroori hai, warna inaam kisi aur ko de diya jayega.",
        "Qurandazi ka nateeja: apka number pehle number pe aya hai aur apne {product} jeeti hai. {fee} token fee aaj hi jama karwayein warna inaam cancel.",
    ]),
    ("prize-09", "prize_lottery", "mixed", [
        "Assalam o Alaikum! Main {show} team se {first} baat kar raha hoon. Aapka {amount_big} ka cheque tayyar hai, bas {fee} tax deposit karna hai. Reply YES to confirm.",
        "AoA sir, {show} office se bol raha hoon. Aapka prize cheque {amount_big} ka sign ho gaya hai, courier se pehle {fee} charges {wallet} kar dein.",
    ]),
    ("prize-10", "prize_lottery", "urdu", [
        "محترم صارف، آپ کے {fi_ur} اکاؤنٹ پر {amount_big_ur} کا بونس منظور ہوا ہے۔ وصولی کے لیے اپنا کوڈ اور {fee_ur} چارجز بھیجیں۔",
        "آپ کو {telco_ur} کی طرف سے {amount_big_ur} کا انعام ملا ہے۔ انعام حاصل کرنے کے لیے پہلے {fee_ur} ٹیکس ادا کریں۔",
    ]),
    ("prize-11", "prize_lottery", "english", [
        "Dear {fi} user, you are our lucky customer of the month! Complete a short survey at {url_scam} to receive {amount_big} cash reward. Enter your card details to verify.",
        "You have been selected for a {amount_big} loyalty reward by {fi}. Verify your card at {url_scam} to receive the amount instantly.",
    ]),
    ("prize-12", "prize_lottery", "roman_urdu", [
        "Ap ko {telco} ki taraf se {amount_big} ka inaam mila hai. Inaam lene ke liye is number {phone} pe abhi call karein. Sirf aaj ke din.",
        "{telco} ki 25 saala salgirah pe apka number {amount_big} ke inaam ka haqdar qarar paya hai. Tafseelat ke liye {phone} pe rabta karein.",
    ]),
    ("prize-13", "prize_lottery", "mixed", [
        "{wallet} Lucky Draw Winner! Mubarak ho {first}, apne {amount_big} jeete hain. Amount transfer karne se pehle {fee} activation fee zaroori hai.",
        "{wallet} anniversary offer: aap winner hain {amount_big} ke! Prize unlock karne ke liye {fee} ka activation {phone} pe karein.",
    ]),
    ("prize-14", "prize_lottery", "roman_urdu", [
        "Apka mobile number {product} ke liye chuna gaya hai sirf {fee} delivery charges ada karein. Order confirm karne ke liye {phone} pe {wallet} karein.",
        "Lucky customer! Sirf {fee} me {product} apke ghar. Ye inaami offer sirf aaj tak, payment {phone} pe {wallet} karein.",
    ]),
    ("prize-15", "prize_lottery", "english", [
        "Final notice: {amount_big} prize money is pending in your name. Pay {fee} government tax to {phone} today or your prize will be cancelled.",
        "Your unclaimed prize of {amount_big} will expire tonight. Transfer the {fee} release charge to {phone} to receive it.",
    ]),
    # ------------------------------------------------------------------ otp_pin_theft
    ("otp-01", "otp_pin_theft", "roman_urdu", [
        "Apka {wallet} account block hone wala hai. Account bachane ke liye apna OTP foran is number pe share karein.",
        "{wallet} Alert: apke account ki verification pending hai. Abhi apko ek code mila hoga, woh code humein reply karein warna account band ho jayega.",
    ]),
    ("otp-02", "otp_pin_theft", "english", [
        "{bank}: We detected unusual activity. To secure your account, reply with the 6-digit OTP sent to your phone.",
        "Dear customer, your {bank} debit card will be deactivated. Share the OTP you just received with our officer to keep it active.",
    ]),
    ("otp-03", "otp_pin_theft", "mixed", [
        "Sir main {bank} helpline se bol raha hoon. Apke number pe ek verification code aya hoga, please woh code bata dein taake apka card update ho jaye.",
        "Hello sir {bank} customer care. Aapka card system me update ho raha hai, jo SMS code abhi aya hai please read kar ke bata dein.",
    ]),
    ("otp-04", "otp_pin_theft", "urdu", [
        "آپ کا {wallet_ur} اکاؤنٹ بند ہونے والا ہے۔ ابھی آپ کو موصول ہونے والا کوڈ اس نمبر پر بھیجیں۔",
        "محترم صارف، آپ کے اکاؤنٹ کی تصدیق کے لیے اپنا پن کوڈ اور او ٹی پی ہمیں بتائیں۔",
    ]),
    ("otp-05", "otp_pin_theft", "roman_urdu", [
        "Apka ATM card expire ho gaya hai. Naya card jari karne ke liye apna 4 digit PIN aur card number {phone} pe SMS karein.",
        "Apke ATM card ki tajdeed ke liye apna card number aur PIN code hamare numainde ko {phone} pe batayein.",
    ]),
    ("otp-06", "otp_pin_theft", "english", [
        "Your {bank} card has been blocked due to KYC. Please send your card number, expiry date and CVV to {phone} to unblock.",
        "{bank} Security: To stop the blocking of your card, reply with your card number, CVV and the PIN you use at ATMs.",
    ]),
    ("otp-07", "otp_pin_theft", "roman_urdu", [
        "Bhai ghalti se mera WhatsApp code apke number pe chala gaya hai, please woh 6 digit code bhej do jaldi.",
        "Yaar mera code tumhare number pe aa gaya hai galti se, jo abhi SMS aya hai woh screenshot bhej do please urgent hai.",
    ]),
    ("otp-08", "otp_pin_theft", "mixed", [
        "Congrats! Apka {amount_big} ka reward ready hai. Reward apke {wallet} me transfer karne ke liye jo code abhi aya hai woh reply karein.",
        "Reward alert: {amount} cashback aapke {wallet} me add hona hai. Confirm karne ke liye received verification code share karein.",
    ]),
    ("otp-09", "otp_pin_theft", "english", [
        "PTA Notice: Your SIM will be blocked in 2 hours due to incomplete biometric. Share the verification code sent to you to continue service.",
        "Your SIM verification is incomplete. Reply with the code you receive now or your number and wallet will be disconnected.",
    ]),
    ("otp-10", "otp_pin_theft", "roman_urdu", [
        "{wallet} Customer Care: apka MPIN reset karna hai. Apna purana MPIN aur CNIC ke aakhri 6 digits batayein.",
        "{wallet} se bol rahe hain, aapka account upgrade karna hai. Apna MPIN aur CNIC number bata dein, 2 minute ka kaam hai.",
    ]),
    ("otp-11", "otp_pin_theft", "urdu", [
        "{bank_ur} سیکیورٹی ڈیپارٹمنٹ: آپ کے کارڈ پر مشکوک ٹرانزیکشن ہوئی ہے۔ روکنے کے لیے موصول شدہ کوڈ فوراً بتائیں۔",
        "آپ کے کارڈ سے رقم نکالی جا رہی ہے، اسے روکنے کے لیے ابھی آنے والا کوڈ ہمارے نمائندے کو بتائیں۔",
    ]),
    ("otp-12", "otp_pin_theft", "english", [
        "{wallet}: Your account is limited. Log in at {url_scam} and enter your PIN and OTP to restore access.",
        "Action required: confirm your {fi} identity at {url_scam} using your PIN and the one-time code we send you.",
    ]),
    ("otp-13", "otp_pin_theft", "roman_urdu", [
        "Apka parcel deliver karne ke liye rider ko confirmation code chahiye. Jo code {wallet} se aya hai woh is number pe bhej dein.",
        "Courier se bol raha hoon, apka parcel gate pe hai. Delivery confirm karne ke liye jo 4 digit code aya hai woh bata dein.",
    ]),
    ("otp-14", "otp_pin_theft", "mixed", [
        "Urgent: Apke {bank} account se {amount} nikalne ki request aayi hai. Agar ye aap nahi hain to cancel karne ke liye OTP reply karein.",
        "Alert! {amount} transfer pending from your {bank} account. Rokne ke liye abhi aane wala OTP is number pe bhejein.",
    ]),
    # ------------------------------------------------------------------ impersonation
    ("imp-01", "impersonation", "roman_urdu", [
        "Main {bank} head office se {name} bol raha hoon. Apke account ki biometric verification baqi hai, apni CNIC aur card details batayein.",
        "{bank} head office: aapka account update nahi hua. Hamara officer {name} aapko call karega, unhe apni tamam details bata dein.",
    ]),
    ("imp-02", "impersonation", "english", [
        "This is {bank} Fraud Department. Your account is under review. Call our officer at {phone} immediately to avoid legal action.",
        "{bank} Risk Team: your account has been flagged. Contact our investigation officer on {phone} today or your funds will be frozen.",
    ]),
    ("imp-03", "impersonation", "mixed", [
        "{wallet} official: Dear user apka account upgrade ho raha hai. Hamari team aapko call karegi, unhe apni details provide karein. {phone}",
        "{wallet} Head Office: aap ke account ka annual verification due hai. Hamare representative ko {phone} pe apni details confirm karwa dein.",
    ]),
    ("imp-04", "impersonation", "urdu", [
        "میں {bank_ur} ہیڈ آفس سے بات کر رہا ہوں۔ آپ کے اکاؤنٹ کی تصدیق کے لیے اپنا شناختی کارڈ نمبر اور کارڈ کی تفصیلات بتائیں۔",
        "{bank_ur} کی طرف سے: آپ کا اکاؤنٹ اپڈیٹ نہیں ہوا، ہمارے افسر کو {phone} پر اپنی تفصیلات فراہم کریں۔",
    ]),
    ("imp-05", "impersonation", "roman_urdu", [
        "State Bank of Pakistan: Apke account me mashkook len den hui hai. Apne account ko mehfooz rakhne ke liye apni raqam is safe account me transfer karein: {phone}",
        "SBP ki taraf se ittila: apka account hack hone ka khatra hai. Apni saari raqam foran hamare mehfooz account {phone} me muntaqil karein.",
    ]),
    ("imp-06", "impersonation", "english", [
        "FIA Cyber Crime: A case has been registered against your CNIC for money laundering. Pay {fee} fine via {wallet} to {phone} to close the case.",
        "Cyber Crime Wing notice: your number is linked to fraud. To avoid arrest, deposit {fee} clearance fee to {phone} within 3 hours.",
    ]),
    ("imp-07", "impersonation", "roman_urdu", [
        "FBR Notice: Apka tax record update nahi hai. Penalty se bachne ke liye apni bank details is link pe update karein {url_scam}",
        "FBR ki taraf se aakhri warning: apke NTN pe jurmana lag chuka hai. {fee} jurmana {phone} pe jama karwayein warna case court jayega.",
    ]),
    ("imp-08", "impersonation", "mixed", [
        "{wallet} Support: aapki complaint receive ho gayi hai. Resolve karne ke liye hamare agent ko AnyDesk app install karke code share karein.",
        "{bank} complaint cell: aap ka masla hal karne ke liye screen sharing app install karein aur hamare agent ko access de dein.",
    ]),
    ("imp-09", "impersonation", "english", [
        "Hello, I am the branch manager of {bank} {city}. Your account needs urgent re-verification. Please share your account login on WhatsApp {phone}.",
        "Branch Manager {bank} {city} here. Due to system upgrade please send your internet banking username and password for re-activation.",
    ]),
    ("imp-10", "impersonation", "urdu", [
        "{wallet_ur} کسٹمر سروس: آپ کا اکاؤنٹ اپ گریڈ کیا جا رہا ہے، اپنی تفصیلات اس نمبر {phone} پر بھیجیں ورنہ اکاؤنٹ بند کر دیا جائے گا۔",
        "ایف آئی اے سائبر کرائم: آپ کے شناختی کارڈ پر مقدمہ درج ہوا ہے، معاملہ ختم کرنے کے لیے {fee_ur} جرمانہ {phone} پر جمع کروائیں۔",
    ]),
    ("imp-11", "impersonation", "roman_urdu", [
        "Main {city} cantt se Captain {first} bol raha hoon, apka ghar kiraye pe lena hai. Advance payment bhejne se pehle apne {wallet} me {fee} verification ke liye bhejein.",
        "Army officer hoon, apki gari khareedni hai. Payment army account se aayegi, pehle {fee} processing hamare clerk ke number {phone} pe bhejein.",
    ]),
    ("imp-12", "impersonation", "mixed", [
        "PTA ki taraf se: Apka mobile IMEI block list me hai. Unblock karwane ke liye {fee} fee {phone} pe {wallet} karein.",
        "PTA notice: aap ka phone non-registered hai aur kal band ho jayega. {fee} registration fee {phone} pe bhej kar block se bachein.",
    ]),
    ("imp-13", "impersonation", "english", [
        "{telco} Official: Your number will be suspended for unverified ownership. Contact our representative at {phone} and confirm your CNIC and wallet PIN.",
        "{telco} franchise here. Your SIM ownership is under dispute. Confirm your CNIC and {wallet} PIN with our agent to keep the number.",
    ]),
    # ------------------------------------------------------------------ loan_fee
    ("loan-01", "loan_fee", "roman_urdu", [
        "Mubarak ho! Apko {amount_big} ka qarza approve ho gaya hai. Processing fee {fee} jama karwayein aur raqam 1 ghante me apke account me.",
        "Apki qarza darkhwast manzoor ho gayi hai. {amount_big} hasil karne ke liye pehle {fee} processing fee {phone} pe bhejein.",
    ]),
    ("loan-02", "loan_fee", "english", [
        "Instant loan of {amount_big} approved without documents! Just pay {fee} insurance fee to {phone} via {wallet} and get money today.",
        "Get {amount_big} loan in 10 minutes. No CNIC copy, no guarantor. Only pay {fee} file fee to {phone}.",
    ]),
    ("loan-03", "loan_fee", "mixed", [
        "{loanapp}: Dear customer apka loan {amount_big} approved hai. Disbursement ke liye file charges {fee} pehle bhejna lazmi hai.",
        "{loanapp} update: loan amount {amount_big} release hone wali hai, bas {fee} stamp duty {wallet} kar dein {phone} pe.",
    ]),
    ("loan-04", "loan_fee", "urdu", [
        "مبارک ہو! آپ کا {amount_big_ur} کا قرضہ منظور ہو گیا ہے۔ پروسیسنگ فیس {fee_ur} جمع کروائیں اور رقم آج ہی حاصل کریں۔",
        "آپ کی قرض کی درخواست منظور ہو چکی ہے، رقم جاری کرنے کے لیے پہلے {fee_ur} فیس {phone} پر بھیجیں۔",
    ]),
    ("loan-05", "loan_fee", "roman_urdu", [
        "Bila sood qarza scheme: {amount_big} tak qarza sirf CNIC pe. Registration fee {fee} {phone} pe bhejein, baqi kaam hum karenge.",
        "Hukumat ki bila sood qarza scheme me apka naam shamil hai. {fee} form fee bhej kar {amount_big} hasil karein.",
    ]),
    ("loan-06", "loan_fee", "english", [
        "PM Youth Loan Scheme: Your application is approved for {amount_big}. Deposit {fee} security amount to {phone} to release funds.",
        "Government Youth Loan: you qualify for {amount_big}. A refundable security deposit of {fee} is required before transfer.",
    ]),
    ("loan-07", "loan_fee", "roman_urdu", [
        "{loanapp} se {amount_big} ka loan lein 5 minute me! Koi guarantee nahi. Bas pehle {fee} advance fee jama karwayein.",
        "Fori qarza chahiye? {loanapp} pe {amount_big} tak foran. Advance {fee} {wallet} karein aur raqam paayein.",
    ]),
    ("loan-08", "loan_fee", "mixed", [
        "Apki loan application final stage pe hai. Agar {fee} stamp paper charges aaj jama na karwaye to application cancel ho jayegi.",
        "Loan file almost complete hai sir, sirf {fee} legal charges reh gaye hain. Aaj hi {phone} pe bhej dein taake cheque ban jaye.",
    ]),
    ("loan-09", "loan_fee", "urdu", [
        "{loanapp} کی طرف سے آپ کے لیے بغیر ضمانت {amount_big_ur} کا قرض تیار ہے، صرف {fee_ur} فائل چارجز اس نمبر {phone} پر بھیجیں۔",
        "بلا سود قرضہ اسکیم: صرف شناختی کارڈ پر {amount_big_ur} تک قرض، رجسٹریشن فیس {fee_ur} ابھی جمع کروائیں۔",
    ]),
    ("loan-10", "loan_fee", "english", [
        "Congratulations {first}, your personal loan of {amount_big} has been sanctioned. Kindly transfer the refundable processing fee of {fee} to activate disbursement.",
        "Dear {first}, loan sanctioned: {amount_big}. Disbursement is on hold until the processing charge of {fee} is received at {phone}.",
    ]),
    ("loan-11", "loan_fee", "roman_urdu", [
        "Karobar ke liye {amount_big} qarza sirf 2% pe. Apni file open karwane ke liye {fee} {wallet} karein aur {phone} pe screenshot bhejein.",
        "Dukan ya karobar ke liye asaan qarza, koi zamanat nahi. File fee {fee} bhejein aur {amount_big} hasil karein.",
    ]),
    ("loan-12", "loan_fee", "mixed", [
        "Loan approved {amount_big}. Apni details yahan bharein {url_scam} aur {fee} verification charges ada karein.",
        "Pre-approved loan offer {amount_big}! Claim karne ke liye link pe CNIC aur {wallet} PIN enter karein {url_scam}",
    ]),
    # ------------------------------------------------------------------ payment_request
    ("pay-01", "payment_request", "roman_urdu", [
        "Ammi ye mera naya number hai, purana phone kharab ho gaya. Mujhe foran {amount} chahiye, is {wallet} number pe bhej dein {phone}. Baad me batata hoon.",
        "Abbu mera phone gum ho gaya hai, ye dost ka number hai. Urgent {amount} {wallet} kar dein {phone} pe, ghar aa ke samjhata hoon.",
    ]),
    ("pay-02", "payment_request", "english", [
        "Hi, this is {name}, your manager. I'm in a meeting and need you to urgently transfer {amount} to a supplier at {phone}. Keep this confidential, I'll reimburse.",
        "{name} here from the head office. I need a quick favour, send {amount} to this account now, I can't talk, will explain later.",
    ]),
    ("pay-03", "payment_request", "mixed", [
        "Bhai emergency hai, {first} ka accident ho gaya hai, hospital me {amount} jama karwane hain. Foran {phone} pe {wallet} karo please, call nahi kar sakta.",
        "Hospital se bol raha hoon, aapke rishtedar {first} emergency me hain. Operation ke liye {amount} abhi {phone} pe bhejein.",
    ]),
    ("pay-04", "payment_request", "urdu", [
        "امی یہ میرا نیا نمبر ہے، فوراً {amount_ur} اس {wallet_ur} نمبر {phone} پر بھیج دیں، بہت ضروری ہے۔",
        "ابو میرا فون گم ہو گیا ہے، یہ دوست کا نمبر ہے۔ ابھی {amount_ur} اس نمبر پر بھیج دیں، گھر آ کر بتاتا ہوں۔",
    ]),
    ("pay-05", "payment_request", "roman_urdu", [
        "Apka beta police hirasat me hai. Case khatam karwane ke liye {amount} foran is number pe bhejein warna FIR ho jayegi. Kisi ko mat batayein.",
        "Thane se bol raha hoon, apke bete ko pakar liya hai. Abhi {amount} {wallet} karein to chhor denge, warna case darj hoga.",
    ]),
    ("pay-06", "payment_request", "english", [
        "Dear tenant, our bank account has changed. Please send this month's rent of {amount} to the new {wallet} number {phone} today.",
        "Notice from your landlord: do not use the old account. Transfer the rent {amount} to {phone} by tonight to avoid a penalty.",
    ]),
    ("pay-07", "payment_request", "roman_urdu", [
        "Yaar main {city} me phans gaya hoon, wallet chori ho gaya. {amount} abhi bhej do is number pe, kal subah wapis kar dunga. Kisi ko na batana.",
        "Bhai musibat me hoon, {city} station pe hoon aur paise khatam. {amount} is naye number pe {wallet} kar do, ghar ja ke lauta dunga.",
    ]),
    ("pay-08", "payment_request", "mixed", [
        "Aapka order confirm karne ke liye {amount} advance payment {phone} pe {wallet} karein, phir hi parcel dispatch hoga. Cash on delivery available nahi.",
        "Online sale: {product} sirf {amount} me. Full payment advance {wallet} karein {phone} pe, delivery 2 din me.",
    ]),
    ("pay-09", "payment_request", "roman_urdu", [
        "Bijli ka connection aaj raat kaat diya jayega kyunke pichla bill update nahi hua. Foran {amount} is number {phone} pe {wallet} karein.",
        "Gas company notice: apka meter kal utaar liya jayega. Jurmana {amount} aaj hi {phone} pe jama karwayein.",
    ]),
    ("pay-10", "payment_request", "urdu", [
        "آپ کا بیٹا پولیس کی حراست میں ہے، معاملہ ختم کرنے کے لیے فوراً {amount_ur} اس نمبر {phone} پر بھیجیں اور کسی کو نہ بتائیں۔",
        "ہسپتال سے بات کر رہا ہوں، آپ کے رشتہ دار کا حادثہ ہوا ہے، فوری طور پر {amount_ur} اس نمبر پر بھیجیں۔",
    ]),
    ("pay-11", "payment_request", "english", [
        "Your order from {merchant} is on hold. Complete payment of {amount} at {url_scam} within 30 minutes to avoid cancellation.",
        "Payment failed for your {merchant} order. Pay {amount} again using this secure link {url_scam} or the order will be cancelled.",
    ]),
    ("pay-12", "payment_request", "roman_urdu", [
        "Bike booking ke liye {amount} token money abhi bhej dein, warna kisi aur ko de denge. Gari {city} se courier ho jayegi. {phone}",
        "OLX wali gari abhi available hai, {amount} advance {wallet} kar dein to aapke naam book kar deta hoon, warna aaj bik jayegi.",
    ]),
    ("pay-13", "payment_request", "mixed", [
        "Sir aapke bache ki school fee due hai. New account me {amount} transfer karein {phone} warna admission cancel. Accounts Office",
        "Parents notice: school ka bank account change ho gaya hai. Is mahine ki fee {amount} sirf is {wallet} number {phone} pe bhejein.",
    ]),
    # ------------------------------------------------------------------ account_suspension
    ("susp-01", "account_suspension", "roman_urdu", [
        "{wallet}: Apka account 24 ghante me band kar diya jayega. Account active rakhne ke liye is link pe apni details update karein {url_scam}",
        "{wallet} Alert: apka account suspend ho chuka hai. Dobara chalane ke liye foran is link pe login karein {url_scam}",
    ]),
    ("susp-02", "account_suspension", "english", [
        "Dear customer, your {bank} account has been suspended due to incomplete KYC. Verify now at {url_scam} to avoid permanent closure.",
        "{bank}: Your online banking access is suspended. Re-activate within 12 hours at {url_scam} or your account will be closed.",
    ]),
    ("susp-03", "account_suspension", "mixed", [
        "ALERT: Your {wallet} account is temporarily blocked. Unblock karne ke liye abhi {phone} pe call karein aur verification complete karein.",
        "Your {wallet} wallet has been frozen. Unfreeze karwane ke liye hamare agent se {phone} pe rabta karein.",
    ]),
    ("susp-04", "account_suspension", "urdu", [
        "آپ کا {bank_ur} اکاؤنٹ عارضی طور پر بند کر دیا گیا ہے۔ دوبارہ فعال کرنے کے لیے اس لنک پر اپنی معلومات درج کریں {url_scam}",
        "آپ کا اکاؤنٹ معطل کر دیا گیا ہے۔ اکاؤنٹ بحال کرنے کے لیے 24 گھنٹے کے اندر اس لنک پر تصدیق کریں {url_scam}",
    ]),
    ("susp-05", "account_suspension", "roman_urdu", [
        "Apke {wallet} account ki biometric verification nahi hui. Aaj raat 12 baje tak verify na kiya to account aur balance freeze ho jayega. Link: {url_scam}",
        "Biometric adhoori hai! {wallet} account aur balance kal se band. Abhi verify karein: {url_scam}",
    ]),
    ("susp-06", "account_suspension", "english", [
        "Your SIM registration has expired. Your {wallet} wallet linked to this number will be closed today. Re-register at {url_scam}",
        "Your mobile wallet will be deactivated due to outdated SIM records. Update your details at {url_scam} immediately.",
    ]),
    ("susp-07", "account_suspension", "roman_urdu", [
        "{bank} Alert: Apka debit card block kar diya gaya hai. Dobara chalu karwane ke liye {phone} pe rabta karein aur card ki details batayein.",
        "Apka {bank} card band kar diya gaya hai. Card chalu karwane ke liye hamare numainde ko {phone} pe card number batayein.",
    ]),
    ("susp-08", "account_suspension", "mixed", [
        "Dear {fi} user, apke account ki transaction limit khatam kar di gayi hai due to suspicious activity. Restore karne ke liye login karein {url_scam}",
        "{fi} notice: your account is on hold. Hold hatane ke liye apna username aur password is page pe confirm karein {url_scam}",
    ]),
    ("susp-09", "account_suspension", "urdu", [
        "{wallet_ur} الرٹ: آپ کا اکاؤنٹ 2 گھنٹے میں بلاک ہو جائے گا۔ فوری طور پر {phone} پر کال کریں۔",
        "آپ کا موبائل اکاؤنٹ آج رات بند ہو جائے گا، بچانے کے لیے فوراً اس نمبر {phone} پر رابطہ کریں۔",
    ]),
    ("susp-10", "account_suspension", "english", [
        "FINAL WARNING: {fi} has detected policy violations on your account. It will be permanently deleted unless you confirm your identity at {url_scam} within 2 hours.",
        "Last reminder: your {fi} account will be terminated today. Confirm ownership at {url_scam} to keep your balance.",
    ]),
    ("susp-11", "account_suspension", "roman_urdu", [
        "Apka CNIC expire ho chuka hai is liye apka {bank} account band kiya ja raha hai. Account bachane ke liye apni nayi details aur PIN {phone} pe bhejein.",
        "Shanakhti card ki muddat khatam hone ki wajah se apka account band ho raha hai. Fori taur pe apni details aur PIN bhejein.",
    ]),
    ("susp-12", "account_suspension", "mixed", [
        "Your {bank} account is marked dormant. Activate karne ke liye {fee} activation fee {wallet} karein {phone} pe, warna funds SBP ko transfer ho jayenge.",
        "Dormant account notice: {fee} re-activation charges {phone} pe bhejein warna aapka balance zabt ho jayega.",
    ]),
    ("susp-13", "account_suspension", "english", [
        "{wallet} will stop working on your number from tomorrow. Update your app from {url_scam} and log in to keep your balance safe.",
        "Important: old {wallet} app versions are being shut down. Download the new version from {url_scam} and sign in to avoid losing funds.",
    ]),
    # ------------------------------------------------------------------ investment
    ("inv-01", "investment", "roman_urdu", [
        "Sirf {fee} invest karein aur 7 din me double paise payein! {company} ki guaranteed scheme. Abhi join karein {phone}",
        "Paisa double scheme! {company} me {fee} lagayein aur ek hafte me do guna wapis lein. Seats mehdood hain.",
    ]),
    ("inv-02", "investment", "english", [
        "Earn {amount_big} per month from home! Invest just {fee} in {company} and get guaranteed 30% weekly profit. No risk. WhatsApp {phone}",
        "Guaranteed returns! Put {fee} into {company} today and withdraw {amount_big} next month. Zero risk, 100% halal.",
    ]),
    ("inv-03", "investment", "mixed", [
        "Crypto trading signals 100% sure profit {company} me {fee} lagao aur roz {amount} kamao. Limited seats, join now {url_scam}",
        "Bitcoin investment plan: {fee} deposit karein aur daily {amount} profit guaranteed. Register yahan karein {url_scam}",
    ]),
    ("inv-04", "investment", "urdu", [
        "صرف {fee_ur} لگائیں اور ایک ہفتے میں دگنا منافع حاصل کریں۔ {company} کی گارنٹی شدہ اسکیم، ابھی رابطہ کریں {phone}",
        "گھر بیٹھے سرمایہ کاری کریں، ہر ہفتے 25 فیصد یقینی منافع۔ {company} میں آج ہی رقم جمع کروائیں۔",
    ]),
    ("inv-05", "investment", "roman_urdu", [
        "Online committee scheme: har mahine {fee} jama karein aur 3 mahine baad {amount_big} hasil karein. Pehli kist abhi {wallet} karein {phone}",
        "Online BC dalein! Sirf {fee} mahana aur pehli committee aap ki. Abhi {phone} pe pehli kist bhejein.",
    ]),
    ("inv-06", "investment", "english", [
        "Join {company} forex club. Our experts guarantee daily returns of 5% on your deposit. Minimum deposit {fee}. Register at {url_scam}",
        "{company}: professional forex traders will grow your money 3x in 60 days, guaranteed. Start with {fee}.",
    ]),
    ("inv-07", "investment", "roman_urdu", [
        "Sone me investment ka sunehra mauqa! {company} me paise lagayein aur har hafte 20% munafa. Pehle 50 logon ke liye khaas offer.",
        "{company} gold scheme: {fee} lagaein, har mahine pakka munafa. Aaj hi {phone} pe raqam bhej kar member banein.",
    ]),
    ("inv-08", "investment", "mixed", [
        "Ghar baithe kamaiye! Simple tasks complete karein aur roz {amount} kamaein. Account activate karne ke liye {fee} deposit karein. Link: {url_scam}",
        "Part time job: YouTube videos like karein aur {amount} roz kamaein. VIP level unlock karne ke liye {fee} recharge karein.",
    ]),
    ("inv-09", "investment", "urdu", [
        "کرپٹو میں سرمایہ کاری کریں اور روزانہ {amount_ur} کمائیں، سو فیصد منافع کی ضمانت۔ ابھی {fee_ur} جمع کروائیں۔",
        "آن لائن کام کریں اور روزانہ {amount_ur} کمائیں، اکاؤنٹ فعال کرنے کے لیے {fee_ur} جمع کروائیں۔",
    ]),
    ("inv-10", "investment", "english", [
        "Invest {fee} today and receive {amount_big} after 30 days. Bring 3 friends and get extra bonus. Guaranteed by {company}.",
        "Refer and earn: deposit {fee}, add 2 members and your profit doubles every week. {company} pays on time, guaranteed.",
    ]),
    ("inv-11", "investment", "roman_urdu", [
        "{company} housing scheme me sirf {fee} me plot book karein, 6 mahine me qeemat teen guna! Booking ke liye abhi {phone} pe raqam bhejein.",
        "Plot file sirf {fee} me, saal me qeemat double pakki. Aaj booking band ho jayegi, abhi raqam {wallet} karein.",
    ]),
    ("inv-12", "investment", "mixed", [
        "Dear investor, PSX insider tips available! Hamare VIP group me {fee} de kar join karein aur guaranteed profit lein. {phone}",
        "Stock market ka pakka formula! {fee} fee de kar premium group join karein, har trade me profit guaranteed.",
    ]),
    # ------------------------------------------------------------------ refund_reversal
    ("ref-01", "refund_reversal", "roman_urdu", [
        "Assalam o alaikum, maine ghalti se {amount} apke {wallet} account me bhej diye hain. Please meherbani kar ke is number pe wapis kar dein {phone}.",
        "Bhai ghalti se apke number pe {amount} transfer ho gaye hain, mere bachon ki fees ke paise hain, please wapis bhej dein.",
    ]),
    ("ref-02", "refund_reversal", "mixed", [
        "Aapke {wallet} account me {amount} transfer kiye gaye hain. TID {tid}. Note: amount ghalti se bheji gayi, sender ko {phone} pe wapis karein.",
        "Received {amount} in your {wallet}. Ye amount wrong number pe gayi hai, kindly {phone} pe return kar dein, shukriya.",
    ]),
    ("ref-03", "refund_reversal", "english", [
        "Your {merchant} order has been cancelled. To receive your refund of {amount}, share your card number and OTP with our refund team at {phone}.",
        "{merchant} refunds: we owe you {amount}. Reply with your card details and the code we send to complete the refund.",
    ]),
    ("ref-04", "refund_reversal", "mixed", [
        "Dear customer, aapki last transaction reverse ho gayi hai. Refund {amount} receive karne ke liye link pe apna {wallet} PIN enter karein {url_scam}",
        "Transaction reversal pending: {amount} wapis lene ke liye apna MPIN is form me dalein {url_scam}",
    ]),
    ("ref-05", "refund_reversal", "urdu", [
        "السلام علیکم، میں نے غلطی سے آپ کے اکاؤنٹ میں {amount_ur} بھیج دیے ہیں، براہ کرم اس نمبر {phone} پر واپس کر دیں۔",
        "بھائی غلطی سے آپ کے نمبر پر {amount_ur} چلے گئے ہیں، یہ بچوں کی فیس کے پیسے ہیں، مہربانی کر کے واپس کر دیں۔",
    ]),
    ("ref-06", "refund_reversal", "english", [
        "FBR: You are eligible for a tax refund of {amount}. Submit your bank account and card details at {url_scam} to receive it within 24 hours.",
        "Tax refund approved: {amount}. To receive the payment, confirm your card number and PIN at {url_scam}.",
    ]),
    ("ref-07", "refund_reversal", "roman_urdu", [
        "Bijli ke ziada bill ka refund {amount} apke liye manzoor hua hai. Wasooli ke liye apna {wallet} number aur PIN {phone} pe bhejein.",
        "Gas bill ki izafi raqam {amount} wapis ki ja rahi hai. Raqam lene ke liye apna account number aur PIN batayein.",
    ]),
    ("ref-08", "refund_reversal", "mixed", [
        "Sir aapko {amount} zyada payment ho gayi hai hamare system ki ghalti se. Please difference {phone} pe return kar dein, warna legal action hoga.",
        "Excess payment alert: {amount} extra aapke account me chali gayi hai. 2 ghante me {phone} pe wapis karein warna FIR.",
    ]),
    ("ref-09", "refund_reversal", "english", [
        "{bank}: A charge of {amount} was made on your card. If you did not authorize it, call {phone} and provide your card PIN to reverse the transaction.",
        "Unauthorized debit of {amount} detected. To get your money back, call our reversal desk at {phone} with your card number and PIN ready.",
    ]),
    ("ref-10", "refund_reversal", "urdu", [
        "آپ کی رقم {amount_ur} کی واپسی منظور ہو گئی ہے، وصول کرنے کے لیے اپنا {wallet_ur} پن اور کوڈ بتائیں۔",
        "ٹرانزیکشن ریورس ہو گئی ہے، {amount_ur} واپس لینے کے لیے اپنا پن کوڈ اس نمبر {phone} پر بھیجیں۔",
    ]),
    ("ref-11", "refund_reversal", "roman_urdu", [
        "{wallet} cashback: apko {amount} cashback mila hai lekin pending hai. Claim karne ke liye pehle {fee} ki ek test transaction {phone} pe karein.",
        "Apka refund {amount} pending hai. Release karwane ke liye {fee} verification transfer {phone} pe karein, foran wapis mil jayega.",
    ]),
    ("ref-12", "refund_reversal", "english", [
        "Your parcel was returned. Refund of {amount} is ready. Reply with your {wallet} account and the verification code you receive to get it back.",
        "Courier refund: {amount} will be sent back to you. Share your {wallet} number and the SMS code to process it.",
    ]),
]


LEGIT_FAMILIES = [
    # ------------------------------------------------------------------ legit_transaction_alert
    ("txn-01", "legit_transaction_alert", "english", [
        "You have sent {amount} to {name} ({phone}) via {wallet} on {date} at {time}. TID: {tid}. Your new balance is {amount}.",
        "{wallet}: {amount} sent to {name} {phone} on {date} {time}. TID {tid}. Balance {amount}.",
    ]),
    ("txn-02", "legit_transaction_alert", "english", [
        "Dear Customer, you have received {amount} from {name} in your {wallet} account. TID {tid}. Balance: {amount}.",
        "{wallet}: Received {amount} from {name} on {date}. TID {tid}. Current balance {amount}.",
    ]),
    ("txn-03", "legit_transaction_alert", "english", [
        "{bank}: Your A/C {acct} has been debited by {amount} on {date} for {merchant} purchase. Avl Bal {amount}. Not you? Call {uan}.",
        "{bank}: {amount} debited from A/C {acct} on {date} at {merchant}. Available balance {amount}.",
    ]),
    ("txn-04", "legit_transaction_alert", "english", [
        "{bank}: Your A/C {acct} credited with {amount} on {date} (Salary). Available balance {amount}.",
        "{bank}: Funds transfer of {amount} credited to A/C {acct} on {date}. Ref {tid}.",
    ]),
    ("txn-05", "legit_transaction_alert", "roman_urdu", [
        "{wallet}: Apke account me {name} ki taraf se {amount} receive hue hain. TID {tid}. Shukriya {wallet} istemal karne ka.",
        "{wallet}: Apne {amount} {name} ko bhej diye hain. TID {tid}. Naya balance {amount}.",
    ]),
    ("txn-06", "legit_transaction_alert", "urdu", [
        "{wallet_ur}: آپ نے {amount_ur} {name_ur} کو بھیجے۔ ٹرانزیکشن آئی ڈی {tid}۔ نیا بیلنس {amount_ur}۔",
        "{wallet_ur}: آپ کو {name_ur} کی طرف سے {amount_ur} موصول ہوئے۔ ٹرانزیکشن آئی ڈی {tid}۔",
    ]),
    ("txn-07", "legit_transaction_alert", "english", [
        "Payment of {amount} for {merchant} bill (Ref {tid}) was successful via {fi} on {date}. Thank you.",
        "Your {merchant} bill of {amount} has been paid successfully through {fi}. Consumer ref {tid}.",
    ]),
    ("txn-08", "legit_transaction_alert", "english", [
        "{bank} Card ending {acct4} used for {amount} at {merchant} on {date} {time}. If this was not you, call {uan} immediately.",
        "{bank}: Debit card ending {acct4} transaction of {amount} at {merchant}. If not done by you, call our helpline {uan}.",
    ]),
    ("txn-09", "legit_transaction_alert", "mixed", [
        "{wallet}: Mobile load {amount} successful on {phone} on {date}. TID {tid}. Remaining balance {amount}.",
        "{wallet}: Aap ka {telco} load {amount} kamyab raha. TID {tid}. Baqi balance {amount}.",
    ]),
    ("txn-10", "legit_transaction_alert", "english", [
        "Raast payment of {amount} received from {name} into your {bank} A/C {acct} on {date}. Ref {tid}.",
        "{bank}: Raast transfer of {amount} to {name} completed on {date}. Ref {tid}.",
    ]),
    ("txn-11", "legit_transaction_alert", "english", [
        "{bank}: Cash withdrawal of {amount} from ATM {city} on {date} {time}. A/C {acct}. Avl Bal {amount}.",
        "{bank}: ATM withdrawal {amount} at {city} branch ATM on {date}. Balance {amount}.",
    ]),
    ("txn-12", "legit_transaction_alert", "urdu", [
        "{bank_ur}: آپ کے اکاؤنٹ {acct} سے {amount_ur} کی ادائیگی {merchant} کو کی گئی۔ تاریخ {date}۔",
        "{bank_ur}: آپ کے اکاؤنٹ {acct} میں {amount_ur} جمع ہو گئے ہیں۔ تاریخ {date}۔",
    ]),
    ("txn-13", "legit_transaction_alert", "roman_urdu", [
        "Assalam o alaikum! Aapki {merchant} ki payment {amount} kamyabi se ada ho gayi hai. Reference no {tid}.",
        "Aap ki {merchant} bill ki adaigi {amount} mausool ho gayi hai. Shukriya. Ref {tid}.",
    ]),
    ("txn-14", "legit_transaction_alert", "english", [
        "{merchant}: Your refund of {amount} for order #{tid} has been processed to your original payment method. It may take 5-7 working days to reflect.",
        "{merchant}: Refund of {amount} for your returned item has been issued to your {fi} account. No action is needed from you.",
    ]),
    # ------------------------------------------------------------------ legit_otp_delivery
    ("otpd-01", "legit_otp_delivery", "english", [
        "{otp} is your {fi} OTP for login. Do not share this code with anyone. {fi} will never ask for your OTP.",
        "Your {fi} login OTP is {otp}. Never share it with anyone, including {fi} staff.",
    ]),
    ("otpd-02", "legit_otp_delivery", "english", [
        "Your OTP for the purchase of {amount} at {merchant} is {otp}. Valid for 5 minutes. Never share your OTP, PIN or password with anyone, including bank staff.",
        "OTP {otp} for your {amount} online transaction at {merchant}. Do not disclose it to anyone.",
    ]),
    ("otpd-03", "legit_otp_delivery", "roman_urdu", [
        "{wallet}: Apka verification code {otp} hai. Ye code kisi ke sath share na karein. {wallet} kabhi bhi apka code nahi mangta.",
        "{wallet}: Login ke liye apka code {otp} hai. Ye code kisi ko bhi na batayein.",
    ]),
    ("otpd-04", "legit_otp_delivery", "urdu", [
        "آپ کا {fi_ur} تصدیقی کوڈ {otp} ہے۔ یہ کوڈ کسی کو مت بتائیں، بینک کبھی آپ سے کوڈ نہیں مانگتا۔",
        "{fi_ur}: آپ کا ون ٹائم کوڈ {otp} ہے، یہ کسی کے ساتھ شیئر نہ کریں۔",
    ]),
    ("otpd-05", "legit_otp_delivery", "english", [
        "{otp} is the code to register your device on {bank} Mobile App. If you did not request this, ignore this message and do not share the code.",
        "Use {otp} to activate {bank} Mobile Banking on your new device. If this wasn't you, please contact {uan}.",
    ]),
    ("otpd-06", "legit_otp_delivery", "mixed", [
        "Your {merchant} login code is {otp}. Apna code kisi ko na batayein. Code 10 minute tak valid hai.",
        "{merchant} verification code: {otp}. Ye code sirf aap ke liye hai, share na karein.",
    ]),
    ("otpd-07", "legit_otp_delivery", "english", [
        "OTP {otp} for adding beneficiary {name} to your {bank} account. Do not disclose this OTP. If not initiated by you, call {uan}.",
        "{bank}: Your OTP to add {name} as a payee is {otp}. Do not share it.",
    ]),
    ("otpd-08", "legit_otp_delivery", "roman_urdu", [
        "{wallet}: Apka MPIN kamyabi se tabdeel ho gaya hai. Agar ye aap ne nahi kiya to foran {uan} pe rabta karein.",
        "{wallet}: Aap ke account me naye device se login hua hai. Agar ye aap nahi the to {uan} pe call karein.",
    ]),
    ("otpd-09", "legit_otp_delivery", "urdu", [
        "{bank_ur}: لاگ ان کے لیے آپ کا ون ٹائم پاس ورڈ {otp} ہے۔ یہ پاس ورڈ کسی کے ساتھ شیئر نہ کریں۔",
        "{bank_ur}: آپ کی ٹرانزیکشن کا تصدیقی کوڈ {otp} ہے۔ کوڈ کسی کو نہ بتائیں۔",
    ]),
    ("otpd-10", "legit_otp_delivery", "english", [
        "Your WhatsApp code: {otp}. Don't share this code with others.",
        "{otp} is your verification code. For your security, do not share this code.",
    ]),
    ("otpd-11", "legit_otp_delivery", "english", [
        "Use {otp} as your one-time password to confirm your {merchant} order. This code expires in 3 minutes. Never share it.",
        "{merchant}: {otp} is your delivery confirmation code. Give it to the rider only after you receive your parcel.",
    ]),
    # ------------------------------------------------------------------ legit_security_advice
    ("sec-01", "legit_security_advice", "english", [
        "{fi} will never ask for your PIN, OTP or password via call, SMS or WhatsApp. Report suspicious calls to {uan}.",
        "Stay safe: {fi} staff will never ask you for your OTP or card PIN. Never share them with anyone.",
    ]),
    ("sec-02", "legit_security_advice", "roman_urdu", [
        "Hoshiyar rahein! {wallet} kabhi bhi call ya SMS ke zariye apka PIN ya OTP nahi mangta. Mashkook calls ki ittila {uan} pe dein.",
        "{wallet}: Apna PIN aur OTP kisi ko na batayein, chahe woh khud ko {wallet} ka numainda kahe.",
    ]),
    ("sec-03", "legit_security_advice", "urdu", [
        "خبردار! {bank_ur} کبھی بھی آپ سے فون یا میسج پر پن کوڈ یا او ٹی پی نہیں مانگتا۔ ایسی کالز کی اطلاع ہیلپ لائن پر دیں۔",
        "اپنا پن کوڈ اور تصدیقی کوڈ کسی کو نہ بتائیں۔ بینک کا کوئی ملازم آپ سے یہ معلومات نہیں مانگے گا۔",
    ]),
    ("sec-04", "legit_security_advice", "english", [
        "Beware of fake prize messages. {telco} does not charge any fee to deliver prizes. Do not send money to unknown numbers.",
        "{telco} alert: fraudsters are sending fake lucky draw messages. We never ask winners to pay any tax or fee.",
    ]),
    ("sec-05", "legit_security_advice", "mixed", [
        "Fraud alert: Aaj kal fake calls aa rahi hain jo khud ko {bank} ka staff batati hain. Apni card details kisi ko na dein. Stay safe.",
        "Awareness: koi bhi {bank} officer aapse phone pe CVV ya OTP nahi mangta. Aisi call aaye to foran band kar dein.",
    ]),
    ("sec-06", "legit_security_advice", "roman_urdu", [
        "State Bank ki hidayat: Apna card, PIN aur OTP kabhi kisi ke sath share na karein. Shak hone par apne bank ki official helpline pe call karein.",
        "Yaad rakhein: bank ya wallet kabhi aap se paise mehfooz account me muntaqil karne ka nahi kehta. Aisi call fraud hai.",
    ]),
    ("sec-07", "legit_security_advice", "english", [
        "{bank} tip: Always type our website address yourself and use only the official app from the Play Store. We never send login links by SMS.",
        "{fi} reminder: we never send links asking you to log in or verify your account. Delete such messages.",
    ]),
    ("sec-08", "legit_security_advice", "urdu", [
        "جعلی انعامی پیغامات سے ہوشیار رہیں۔ کوئی بھی ادارہ انعام دینے کے لیے فیس نہیں مانگتا۔ مشکوک نمبر کی اطلاع دیں۔",
        "اگر کوئی انعام یا قرضے کے بدلے پہلے فیس مانگے تو یہ دھوکہ ہے۔ رقم مت بھیجیں۔",
    ]),
    ("sec-09", "legit_security_advice", "roman_urdu", [
        "Ammi agar koi call kar ke kahe ke main bank se bol raha hoon aur code mange to bilkul na batana, foran phone band kar dena. Main shaam ko aa ke samjhata hoon.",
        "Abbu kisi anjaan number pe paise mat bhejiyega chahe woh kahe inaam nikla hai. Aaj kal bohat fraud ho raha hai.",
    ]),
    ("sec-10", "legit_security_advice", "english", [
        "PTA Advisory: Never share your verification codes or personal details with unknown callers claiming to be from PTA, banks or telecom companies.",
        "Public advisory: government agencies never ask citizens to pay fines through mobile wallets to personal numbers.",
    ]),
    ("sec-11", "legit_security_advice", "mixed", [
        "Yaad rakhein: koi bhi asal bank loan dene se pehle processing fee personal number pe nahi mangta. Loan sirf official branch ya app se apply karein.",
        "Loan scam se bachein: agar koi advance fee mange to samajh lein fraud hai. Sirf official {bank} channels use karein.",
    ]),
    ("sec-12", "legit_security_advice", "english", [
        "{wallet} Security: Enable fingerprint login and set a strong MPIN. If you lose your phone, call {uan} to block your account immediately.",
        "{wallet} tip: turn on app lock and transaction alerts. Report a lost SIM to {uan} so we can secure your wallet.",
    ]),
    # ------------------------------------------------------------------ legit_conversation
    ("conv-01", "legit_conversation", "roman_urdu", [
        "Bhai kal milte hain office ke baad, chai pe chalein ge. Paisay wali baat bhi kar lein ge.",
        "Kal shaam free ho? Chai pe milte hain, kuch zaroori baat karni hai committee ke hawale se.",
    ]),
    ("conv-02", "legit_conversation", "roman_urdu", [
        "Ammi maine aapke {wallet} me {amount} bhej diye hain, dawai le lijiye ga. Baqi shaam ko call karta hoon.",
        "Ammi ghar ka kharcha bhej diya hai {wallet} pe, check kar lijiye ga. Allah hafiz.",
    ]),
    ("conv-03", "legit_conversation", "english", [
        "Hey {first}, I paid for dinner last night. Your share is {amount}, send it whenever you get a chance, no rush.",
        "Hi {first}, the trip total came to {amount} per person. Pay me back whenever, no hurry at all.",
    ]),
    ("conv-04", "legit_conversation", "urdu", [
        "بیٹا شام کو آتے ہوئے دودھ اور بریڈ لے آنا، پیسے میں نے تمہارے اکاؤنٹ میں بھیج دیے ہیں۔",
        "بیٹا تمہاری فیس جمع کروا دی ہے، رسید سنبھال کر رکھنا اور پڑھائی پر توجہ دو۔",
    ]),
    ("conv-05", "legit_conversation", "mixed", [
        "Yaar mera {wallet} ka balance khatam ho gaya hai, kal tak {amount} udhaar de sakte ho? Salary aate hi wapis kar dunga.",
        "{first} tumhare {amount} wapis bhej diye hain, check kar lo. Thanks for helping last week.",
    ]),
    ("conv-06", "legit_conversation", "roman_urdu", [
        "Assalam o alaikum {first} bhai, Eid pe ghar aa rahe ho na? Ammi pooch rahi theen. Ticket book karwa li?",
        "Shadi ki tareekh pakki ho gayi hai, aap sab ne zaroor aana hai. Card jaldi bhejta hoon.",
    ]),
    ("conv-07", "legit_conversation", "english", [
        "Reminder: team lunch on Friday at 1 pm. Please confirm by tomorrow so I can book the table.",
        "Can you send me the slides before the meeting tomorrow? Also bring the printed budget sheet.",
    ]),
    ("conv-08", "legit_conversation", "roman_urdu", [
        "Beta tumhari fees jama ho gayi hai, bank ki receipt sambhal ke rakhna. Parhai pe dhyan do.",
        "Beta tumhare hostel ke paise bhej diye hain, apna khayal rakhna aur waqt pe khana khana.",
    ]),
    ("conv-09", "legit_conversation", "urdu", [
        "السلام علیکم، کل شام کو ملاقات ہو سکتی ہے؟ کمیٹی کے پیسوں کے بارے میں بات کرنی ہے۔",
        "بھائی جان کل دکان پر آ جائیں، حساب کتاب کر لیتے ہیں۔",
    ]),
    ("conv-10", "legit_conversation", "mixed", [
        "Bro match dekhne chalein? Tickets online mil rahe hain, main book kar leta hoon, tum baad me paise de dena.",
        "Weekend pe {city} chalein? Main hotel book kar deta hoon, apna share baad me de dena.",
    ]),
    ("conv-11", "legit_conversation", "roman_urdu", [
        "Mubarak ho! Tumhara result aa gaya, first division! Ammi bohat khush hain, mithai le ke aana.",
        "Bohat bohat mubarak ho bhai, nayi naukri ki! Treat to banti hai ab.",
    ]),
    ("conv-12", "legit_conversation", "english", [
        "Congratulations on your new job, {first}! Let's celebrate this weekend, my treat.",
        "Congrats on winning the debate competition! So proud of you, {first}.",
    ]),
    ("conv-13", "legit_conversation", "roman_urdu", [
        "Yaar mere phone pe koi OTP aya hai jo maine mangwaya nahi tha, tumhe pata hai kya karna chahiye?",
        "Mujhe abhi ek ajeeb call aayi thi koi code maang raha tha, maine nahi diya. Bank ko report kar doon?",
    ]),
    ("conv-14", "legit_conversation", "urdu", [
        "مبارک ہو! اللہ نے آپ کو بیٹی سے نوازا ہے، بہت بہت مبارکباد۔",
        "مبارک ہو بھائی، نئی دکان کا افتتاح کب ہے؟ ہم ضرور آئیں گے۔",
    ]),
    ("conv-15", "legit_conversation", "roman_urdu", [
        "Uncle ka number ye hai {phone}, unse plot ki registry ka pooch lena. Main kal {city} ja raha hoon.",
        "Plumber ka number {phone} hai, kal subah bula lena. Paise main de doon ga.",
    ]),
    ("conv-16", "legit_conversation", "mixed", [
        "Bhai bank ka kaam ho gaya? Account opening ke liye CNIC copy aur 2 photos chahiye thi, main ne bata diya tha.",
        "Bank gaya tha aaj, card ka masla hal ho gaya. Branch walon ne naya card de diya.",
    ]),
    # ------------------------------------------------------------------ legit_payment_reminder
    ("rem-01", "legit_payment_reminder", "english", [
        "{merchant}: Your bill of {amount} for {month} is due on {date}. Pay via {fi} app or any bank branch. Ignore if already paid.",
        "{merchant}: Bill for {month} is {amount}, due {date}. Pay on time to avoid late payment surcharge.",
    ]),
    ("rem-02", "legit_payment_reminder", "roman_urdu", [
        "{merchant}: Apka {month} ka bill {amount} hai, aakhri tareekh {date}. Bill {wallet} app ya bank se ada karein.",
        "{merchant}: {month} ka bill jari ho gaya hai, raqam {amount}. Bil waqt pe jama karwayein.",
    ]),
    ("rem-03", "legit_payment_reminder", "english", [
        "{bank} Credit Card: Minimum payment of {amount} is due on {date}. Pay through the {bank} app or internet banking to avoid late charges.",
        "{bank} Credit Card statement: total due {amount}, payment due date {date}.",
    ]),
    ("rem-04", "legit_payment_reminder", "urdu", [
        "{merchant}: آپ کا {month} کا بل {amount_ur} ہے جس کی آخری تاریخ {date} ہے۔ براہ کرم بروقت ادائیگی کریں۔",
        "{merchant}: بل کی ادائیگی کی آخری تاریخ {date} ہے۔ رقم {amount_ur}۔",
    ]),
    ("rem-05", "legit_payment_reminder", "english", [
        "{school}: Fee voucher for {month} has been issued. Amount {amount}, due date {date}. Pay at any {bank} branch or via the 1Bill option.",
        "{school}: Dear parents, the {month} fee challan is available on the school portal. Last date {date}.",
    ]),
    ("rem-06", "legit_payment_reminder", "roman_urdu", [
        "Committee ke members, is mahine ki kist {amount} 10 tareekh tak {name} ke paas jama karwa dein. Shukriya.",
        "Committee update: is mahine {name} ki baari hai, sab apni kist {amount} waqt pe de dein.",
    ]),
    ("rem-07", "legit_payment_reminder", "english", [
        "Dear subscriber, your internet package expires on {date}. Recharge from the official app or at any retailer to continue.",
        "{telco}: Your monthly bundle will renew on {date}. Keep sufficient balance for auto-renewal.",
    ]),
    ("rem-08", "legit_payment_reminder", "mixed", [
        "Assalam o alaikum, {month} ka kiraya {amount} hai, pichle mahine wale account me hi bhej dijiye ga. Shukriya, {name}.",
        "{month} ka rent reminder: {amount}, hamesha wale bank account me. Receipt WhatsApp kar dijiye ga.",
    ]),
    ("rem-09", "legit_payment_reminder", "english", [
        "{insurer}: Your policy premium of {amount} is due on {date}. Pay via your bank app or visit our branch. Ignore if paid.",
        "{insurer}: Premium received for {month}. Thank you for staying protected with us.",
    ]),
    ("rem-10", "legit_payment_reminder", "urdu", [
        "معزز والدین، {month} کی فیس {amount_ur} کی آخری تاریخ {date} ہے۔ فیس بینک میں جمع کروائیں۔",
        "محترم صارف، آپ کے بجلی کے بل کی آخری تاریخ {date} ہے۔ بروقت ادائیگی کریں۔",
    ]),
    ("rem-11", "legit_payment_reminder", "english", [
        "Reminder: your {product} installment of {amount} is due on {date}. Please pay at our showroom or to our registered company account.",
        "Installment reminder from {shop}: {amount} due on {date}. Visit our shop to pay and collect your receipt.",
    ]),
    ("rem-12", "legit_payment_reminder", "roman_urdu", [
        "Gym membership ki fees {amount} {date} tak jama karwa dein. Reception pe ya {wallet} pe receipt ke sath. {shop}",
        "Quran class ki is mahine ki fees {amount} hai, jab sahulat ho de dijiye ga. JazakAllah.",
    ]),
    # ------------------------------------------------------------------ legit_loan_ad
    ("lad-01", "legit_loan_ad", "english", [
        "{bank} Personal Finance: Get up to {amount_big} with easy monthly installments. Apply through the {bank} app or visit your nearest branch. Terms apply.",
        "{bank} Personal Loan at competitive markup. Apply in-app or at any branch. No processing fee this month. T&Cs apply.",
    ]),
    ("lad-02", "legit_loan_ad", "roman_urdu", [
        "{bank} Car Finance: Apni nayi gari ab asaan aqsaat pe. Tafseelat ke liye nazdeeki branch tashreef layein ya {uan} pe call karein.",
        "{bank} ke sath bike finance ab asaan. Nazdeeki branch me aa kar apply karein.",
    ]),
    ("lad-03", "legit_loan_ad", "urdu", [
        "{bank_ur} کی طرف سے آسان اقساط پر ذاتی قرضہ۔ تفصیلات کے لیے قریبی برانچ تشریف لائیں۔ شرائط لاگو ہیں۔",
        "{bank_ur} ہوم فنانس: اپنے گھر کا خواب پورا کریں۔ مزید معلومات کے لیے قریبی برانچ سے رابطہ کریں۔",
    ]),
    ("lad-04", "legit_loan_ad", "english", [
        "{wallet} Advance Cash: You are eligible for a small loan of up to {amount} directly in the app. No fee to apply. Check eligibility in the app under Loans.",
        "{wallet}: Need cash before payday? Check your instant loan limit inside the {wallet} app. Charges shown before you confirm.",
    ]),
    ("lad-05", "legit_loan_ad", "mixed", [
        "Ghar banane ka khwab poora karein {bank} Home Finance ke sath. Apply sirf official branch ya website se karein. Koi advance fee nahi.",
        "{bank} Islamic Home Finance: asaan mahana aqsaat. Branch visit karein ya official app se apply karein.",
    ]),
    ("lad-06", "legit_loan_ad", "english", [
        "SME Finance from {bank}: Working capital loans for small businesses. Apply at any branch with your business documents. Markup as per SBP guidelines.",
        "{bank} Agri Finance for farmers: seasonal loans for seed and fertiliser. Visit your nearest branch with land documents.",
    ]),
    ("lad-07", "legit_loan_ad", "roman_urdu", [
        "{merchant} pe ab installments me shopping karein! Checkout pe Pay in 4 chunein. Koi extra charges nahi.",
        "Ab {product} khareedein asaan qiston me, sirf hamare showroom se. Original CNIC saath layein.",
    ]),
    ("lad-08", "legit_loan_ad", "english", [
        "{bank}: Your personal finance application has been received. Our branch officer will contact you on your registered number. We never ask for fees via personal accounts.",
        "{bank}: Your loan application #{tid} is under review. You can track its status in the {bank} app.",
    ]),
    ("lad-09", "legit_loan_ad", "urdu", [
        "{wallet_ur} ایپ میں اب چھوٹے قرضے دستیاب ہیں۔ درخواست صرف ایپ کے اندر سے دیں۔",
        "کاروباری قرضوں کے لیے {bank_ur} کی کسی بھی برانچ سے رابطہ کریں۔ درخواست مفت ہے۔",
    ]),
    ("lad-10", "legit_loan_ad", "english", [
        "Dear {first}, your {bank} car finance has been approved. Please visit the {city} branch with your original CNIC to sign the documents.",
        "{bank}: Congratulations, your home finance is approved. Your relationship manager will share the offer letter at the branch.",
    ]),
    # ------------------------------------------------------------------ legit_business_payment
    ("biz-01", "legit_business_payment", "english", [
        "Hi {first}, invoice #{tid} for {amount} is attached. Please transfer to our company account at {bank} as per the invoice. Thanks, {company_legit}.",
        "{company_legit}: Invoice {tid} dated {date} for {amount}. Payment terms 30 days. Bank details are printed on the invoice.",
    ]),
    ("biz-02", "legit_business_payment", "roman_urdu", [
        "Bhai maal dispatch ho gaya hai, bilty ki photo bhej di hai. Payment {amount} hamesha wale account me kar dena.",
        "Aap ka order kal tak pohanch jayega. Payment maal check karne ke baad hi karna.",
    ]),
    ("biz-03", "legit_business_payment", "english", [
        "Salary for {month} has been credited to your account. Payslips are available on the HR portal. Contact HR for any queries.",
        "HR: {month} salaries have been processed. Please check your payslip on the portal.",
    ]),
    ("biz-04", "legit_business_payment", "urdu", [
        "محترم گاہک، آپ کا آرڈر تیار ہے۔ ادائیگی {amount_ur} دکان پر یا ڈیلیوری کے وقت کی جا سکتی ہے۔",
        "آپ کا سامان دکان پر پہنچ گیا ہے، آ کر وصول کر لیں۔ ادائیگی وصولی کے وقت۔",
    ]),
    ("biz-05", "legit_business_payment", "mixed", [
        "Payment received! {amount} aapke Payoneer se {bank} account me transfer ho gaye hain. Shukriya for the great work.",
        "Client ne milestone release kar diya, {amount} next week tak account me aa jayenge.",
    ]),
    ("biz-06", "legit_business_payment", "english", [
        "Your {merchant} order #{tid} will be delivered today. Please keep {amount} ready for cash on delivery.",
        "{merchant}: Your parcel is out for delivery. Amount payable on delivery: {amount}.",
    ]),
    ("biz-07", "legit_business_payment", "roman_urdu", [
        "{shop}: Aapka udhaar hisaab {amount} ho gaya hai. Jab sahulat ho tab dukaan pe ada kar dein.",
        "{shop}: Aap ka mahana hisaab {amount} hai. Shukriya hamare sath kharidari ka.",
    ]),
    ("biz-08", "legit_business_payment", "english", [
        "{shop}: Thank you for shopping with us. Exchange is available within 7 days with receipt. No cash refunds.",
        "{shop}: Your receipt total is {amount}. Thank you for visiting, see you again!",
    ]),
    ("biz-09", "legit_business_payment", "mixed", [
        "Order confirm hai. 50% advance aap ne de diya, baqi {amount} delivery pe dena. Receipt WhatsApp kar di hai. {shop}",
        "Sofa ready hai, kal deliver ho jayega. Baqi payment {amount} delivery ke waqt cash ya bank transfer. {shop}",
    ]),
    ("biz-10", "legit_business_payment", "urdu", [
        "اکتوبر کی تنخواہ آپ کے اکاؤنٹ میں منتقل کر دی گئی ہے۔ کسی بھی سوال کے لیے ایچ آر سے رابطہ کریں۔",
        "آپ کی ادائیگی {amount_ur} موصول ہو گئی ہے۔ شکریہ۔",
    ]),
    ("biz-11", "legit_business_payment", "english", [
        "We have received your payment of {amount} against invoice #{tid}. Thank you for your business. {company_legit} Accounts",
        "{company_legit}: Payment of {amount} received on {date}. Your account is now clear.",
    ]),
    ("biz-12", "legit_business_payment", "roman_urdu", [
        "Sir is mahine ki tuition fee {amount} hai, cash de dein ya mere {wallet} pe bhej dein jo pehle bhi use kiya tha. Shukriya.",
        "Driver ki tankhwah {amount} bhej di hai, aap confirm kar dein mil gayi.",
    ]),
    # ------------------------------------------------------------------ legit_url_info
    ("url-01", "legit_url_info", "english", [
        "Your {merchant} e-bill for {month} is ready. View it at {url_legit} or in the official app.",
        "{merchant}: Your {month} bill is available online at {url_legit}.",
    ]),
    ("url-02", "legit_url_info", "english", [
        "Your parcel {tid} has been dispatched. Track your delivery at {url_legit}.",
        "Shipment {tid} is on its way. Live tracking: {url_legit}",
    ]),
    ("url-03", "legit_url_info", "roman_urdu", [
        "Kal ka match zabardast tha! Highlights yahan dekho {url_legit}",
        "Ye video dekho yaar, bohat funny hai {url_legit}",
    ]),
    ("url-04", "legit_url_info", "english", [
        "Join the team meeting at 3 pm today: {url_legit} . Agenda shared in the group.",
        "Class link for tomorrow's lecture: {url_legit} . Please join 5 minutes early.",
    ]),
    ("url-05", "legit_url_info", "mixed", [
        "University admissions open hain. Online apply karne ka link: {url_legit} . Last date {date}.",
        "Scholarship ki details is page pe hain {url_legit} , deadline {date} hai.",
    ]),
    ("url-06", "legit_url_info", "english", [
        "A new version of the {fi} app is available on Google Play. Update from the Play Store to get the latest features.",
        "{fi} app update: new design and faster transfers. Update from your phone's official app store.",
    ]),
    ("url-07", "legit_url_info", "urdu", [
        "محکمہ موسمیات: آئندہ دو دن بارش کا امکان ہے۔ مزید معلومات کے لیے {url_legit} دیکھیں۔",
        "امتحانات کا شیڈول جاری کر دیا گیا ہے، تفصیلات کے لیے {url_legit} دیکھیں۔",
    ]),
    ("url-08", "legit_url_info", "english", [
        "Here's the recipe I told you about: {url_legit} . Let me know how it turns out!",
        "Found the article about saving tips we discussed: {url_legit}",
    ]),
    ("url-09", "legit_url_info", "english", [
        "{bank}: Your e-statement for {month} has been sent to your registered email. You can also view it in the {bank} app.",
        "{bank}: Annual tax certificate is now available in internet banking under Statements.",
    ]),
    ("url-10", "legit_url_info", "roman_urdu", [
        "Bhai ye form fill kar do jaldi, reunion ki details is me hain: {url_legit}",
        "Shadi ki photos is folder me hain {url_legit} , apni pasand ki select kar lo.",
    ]),
    # ------------------------------------------------------------------ legit_promo
    ("promo-01", "legit_promo", "english", [
        "{merchant} Mega Sale! Up to 50% off on all items this weekend. Shop now in the app. T&Cs apply.",
        "{merchant} 11.11 Sale is live! Extra discounts on electronics and fashion. Shop in the app.",
    ]),
    ("promo-02", "legit_promo", "roman_urdu", [
        "{telco}: Sirf {fee} me 30 GB internet aur 1000 minutes. Subscribe karne ke liye {code} dial karein.",
        "{telco} ka naya monthly bundle: {fee} me unlimited WhatsApp aur 20 GB. Dial {code}.",
    ]),
    ("promo-03", "legit_promo", "english", [
        "Congratulations! You have earned 500 loyalty points on your recent purchase at {merchant}. Redeem them on your next visit.",
        "Congrats! You've unlocked Gold membership at {merchant}. Enjoy free delivery on your next 3 orders.",
    ]),
    ("promo-04", "legit_promo", "urdu", [
        "{merchant}: تمام اشیاء پر 30 فیصد رعایت، صرف اس ہفتے کے آخر تک۔",
        "{merchant}: عید سیل شروع ہو گئی ہے، اپنی پسندیدہ اشیاء رعایتی قیمت پر حاصل کریں۔",
    ]),
    ("promo-05", "legit_promo", "mixed", [
        "{wallet} offer: {merchant} pe payment karein aur 20% cashback payein, max Rs. 300. Offer {date} tak.",
        "{wallet} se bill pay karein aur pao cashback! Offer details app me dekhein.",
    ]),
    ("promo-06", "legit_promo", "english", [
        "Weekend deal: Family platter for {amount} only at {shop}. Order on our official app or call {uan}.",
        "{shop}: Buy 1 Get 1 free on all pizzas every Wednesday. Dine-in and takeaway.",
    ]),
    ("promo-07", "legit_promo", "roman_urdu", [
        "{telco} Offer: Apko is hafte 2 GB free internet diya gaya hai. Mazeed offers ke liye {code} dial karein.",
        "{telco}: Shukriya hamare sath rehne ka! Apko 100 free minutes diye gaye hain.",
    ]),
    ("promo-08", "legit_promo", "english", [
        "Book your tickets for the {city} Food Festival now! Early bird discount ends {date}.",
        "{city} Book Fair starts this Friday. Entry is free for students.",
    ]),
    ("promo-09", "legit_promo", "mixed", [
        "Shop for Rs. 5,000 or more at {merchant} and enter our monthly lucky draw. Winners announced on our official page. No fee required.",
        "{merchant} lucky draw results official page pe announce honge. Inaam ke liye koi fee ya charges nahi.",
    ]),
    ("promo-10", "legit_promo", "urdu", [
        "{telco_ur}: اب صرف {fee_ur} میں ہفتہ وار انٹرنیٹ بنڈل حاصل کریں۔ سبسکرائب کرنے کے لیے {code} ڈائل کریں۔",
        "{telco_ur}: آپ کو اس ہفتے 1 جی بی مفت انٹرنیٹ دیا گیا ہے۔ شکریہ۔",
    ]),
]
