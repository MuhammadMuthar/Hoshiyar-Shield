"""Edge-case inputs shared by the Python tests and the Python/TS parity fixtures."""

EDGE_CASES = [
    "",
    " ",
    "\t\n  \r\n",
    "🎉🎉🎉",
    "OTP",
    "ok",
    "ＪａｚｚＣａｓｈ ＯＴＰ ｓｈａｒｅ ｋａｒｅｉｎ",          # full-width obfuscation
    "O​T​P share karein foran",                    # zero-width characters
    "۰۳۹۹۵۵۵۰۱۲۳ پر رابطہ کریں",                             # Urdu digits phone number
    "كيا يه انعام ہے",                                       # Arabic kaf / yeh / heh variants
    "انعـــام نکلا ہے",                                      # tatweel
    "مُبارَک ہو آپ کا اِنعام",                               # diacritics
    "acc0unt bl0ck ho jayega, 0TP bhejein",                  # leetspeak
    "j4zzc4sh p@ss $end karo",
    "Call 111-555-123 or 0800-55123 for help",               # UAN / toll free
    "+92 399 5550123 / 0092-399-5550123 / 03995550123 / 0399 5550123",
    "Visit https://example.com/a?b=c and www.test.example and bit-ly.example/x now",
    "email me at ahmed.raza@mail.example please",
    "Rs.5,000/- only!!! PKR 25,000.00",
    "MUBARAK HO APKA INAAM NIKLA HAI FEE BHEJEIN",
    "mubarak ho apka inaam nikla hai fee bhejein",
    "Mubarak   ho!!!   apka    inaam",
    "Tabs\tand\nnewlines and em-spaces",
    "Apka JazzCash account block hone wala hai 😱🔥 apna OTP foran share karein 👉",
    "Assalam o alaikum! آپ کا account block ho jayega, OTP bhejein",  # script mixing
    "inaam " * 400,                                           # long repetitive text
    "Bank ne kaha hai kabhi bhi apna OTP kisi ko na batayein. " * 30,
]
