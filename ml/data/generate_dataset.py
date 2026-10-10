"""Generate the Hoshiyar Shield synthetic training dataset (deterministic).

    python ml/data/generate_dataset.py            # writes ml/data/generated/dataset.jsonl

Every row records its provenance (source, synthetic flag, template family),
so the dataset card and the grouped split can be checked by anyone.

Noise (case changes, punctuation loss, emoji, leetspeak, Roman Urdu spelling
variants) is applied with the SAME probabilities to scam and legitimate
messages. Otherwise the model could learn "typos = scam" instead of learning
what scams say.
"""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from data.templates import LEGIT_FAMILIES, SCAM_FAMILIES  # noqa: E402
from data.templates_extra import LEGIT_FAMILIES_EXTRA, SCAM_FAMILIES_EXTRA  # noqa: E402

ALL_SCAM = SCAM_FAMILIES + SCAM_FAMILIES_EXTRA
ALL_LEGIT = LEGIT_FAMILIES + LEGIT_FAMILIES_EXTRA

SEED = 20261011
VARIANTS_PER_FAMILY = 9
OUT_PATH = HERE / "generated" / "dataset.jsonl"

# --------------------------------------------------------------------------- slots
# Phone numbers: ONLY the 0399-555xxxx placeholder range (see COLLABORATION.md §6).
def _phone(rng: random.Random) -> str:
    tail = f"{rng.randint(0, 9999):04d}"
    fmt = rng.choice([
        "0399-555{t}", "0399555{t}", "+92 399 555{t}", "0399 555{t}", "+92399555{t}", "92-399-555{t}",
    ])
    return fmt.format(t=tail)


def _uan(rng: random.Random) -> str:
    return rng.choice(["111-555-{a}", "111 555 {a}", "0800-55{b}"]).format(
        a=f"{rng.randint(0, 999):03d}", b=f"{rng.randint(0, 999):03d}"
    )


def _digits(rng: random.Random, n: int) -> str:
    return "".join(str(rng.randint(0, 9)) for _ in range(n))


def _money(rng: random.Random, values: list[int], big: bool = False) -> str:
    v = rng.choice(values)
    styles = ["Rs. {c}", "Rs {c}", "PKR {c}", "Rs.{p}", "{c} rupay", "{c}/-", "Rs {p}"]
    if big and v >= 100000 and v % 100000 == 0:
        styles += ["{l} lakh", "{l} lac"]
    s = rng.choice(styles)
    return s.format(c=f"{v:,}", p=str(v), l=v // 100000)


AMOUNT_BIG = [25000, 50000, 75000, 100000, 150000, 200000, 250000, 500000, 1000000]
FEE = [300, 500, 999, 1200, 1500, 2000, 2500, 3500, 5000]
AMOUNT = [450, 780, 1250, 2500, 3200, 5000, 7500, 12000, 15000, 18500, 25000, 32999]

POOLS: dict[str, list[str]] = {
    "wallet": ["JazzCash", "Easypaisa", "NayaPay", "SadaPay", "UPaisa", "jazzcash", "easypaisa"],
    "bank": ["HBL", "UBL", "MCB", "Meezan Bank", "Bank Alfalah", "Allied Bank", "Faysal Bank",
             "Bank Al Habib", "Askari Bank", "JS Bank", "BankIslami", "Standard Chartered"],
    "telco": ["Jazz", "Zong", "Telenor", "Ufone"],
    "show": ["Jeeto Pakistan", "Inaami Lucky Draw", "Khushiyon Ka Lucky Draw", "Mega Inaam Scheme",
             "Ramzan Lucky Draw", "PM Inaami Scheme", "Pakistan Lucky Draw 2026"],
    "product": ["Honda CD 70", "iPhone 15", "Suzuki Alto", "LED TV", "Umrah ticket", "laptop",
                "Honda 125", "fridge", "gold set"],
    "first": ["Ahmed", "Sana", "Bilal", "Ayesha", "Usman", "Hira", "Farhan", "Zainab", "Kamran",
              "Nadia", "Imran", "Rabia", "Asad", "Mehwish"],
    "name": ["Ahmed Raza", "Sana Tariq", "Bilal Khan", "Ayesha Siddiqui", "Usman Ali", "Hira Baig",
             "Farhan Qureshi", "Zainab Malik", "Kamran Javed", "Nadia Hussain", "Imran Shah",
             "Rabia Anwar"],
    "city": ["Lahore", "Karachi", "Islamabad", "Multan", "Faisalabad", "Peshawar", "Quetta",
             "Hyderabad", "Rawalpindi", "Sialkot"],
    "merchant": ["Daraz", "Foodpanda", "K-Electric", "LESCO", "SNGPL", "PTCL", "Careem", "Bykea",
                 "Imtiaz", "Khaadi", "IESCO", "Shell"],
    "loanapp": ["Fori Qarza", "EasyLoan PK", "Cash Mitra", "QarzPay", "Paisa Fast", "LoanWala"],
    "company": ["Al-Barkat Investments", "Gold Star Trading", "Crypto Pak Fund", "Pak Forex Club",
                "Rehmat Builders", "Smart Earning Hub", "Noor Gold Traders"],
    "company_legit": ["Raza Textiles", "Tariq Traders", "Malik Enterprises", "Siddiqui & Sons",
                      "Baig Logistics"],
    "shop": ["Bismillah General Store", "Madina Traders", "Al-Noor Pharmacy", "City Mobile Zone",
             "Karachi Biryani House", "Fit Zone Gym", "Royal Furniture"],
    "school": ["Al-Huda Grammar School", "Bright Future Academy", "Iqra Model School",
               "City Grammar Campus"],
    "insurer": ["Saaya Life Insurance", "Amaan Takaful", "Hifazat Life"],
    "month": ["September", "October", "November", "Sep-2026", "Oct 2026"],
    "code": ["*786#", "*345#", "*123#", "*707#", "*6000#"],
    "url_scam": [
        "http://jazzcash-verify.example/login", "easypaisa-reward.example/claim",
        "https://hbl-secure-login.example/update", "meezan-kyc.example", "http://free-inaam.example",
        "loan-fast.example/apply", "www.wallet-unblock.example/verify", "http://192.0.2.15/kyc",
        "https://sbp-refund.example/form", "bit-ly.example/x7Kq2", "https://easypaisa.verify-now.example",
    ],
    "url_legit": [
        "https://www.example.com/bills", "https://track.courier.example/abc123",
        "https://news.example.pk/sports", "https://meet.example.com/xyz-team",
        "https://admissions.university.example", "https://weather.example.gov/forecast",
        "https://recipes.example.com/biryani", "https://forms.example.com/reunion",
    ],
    # --- Urdu script slots
    "wallet_ur": ["جاز کیش", "ایزی پیسہ", "JazzCash", "Easypaisa"],
    "bank_ur": ["ایچ بی ایل", "میزان بینک", "یو بی ایل", "الائیڈ بینک", "بینک الفلاح", "HBL"],
    "telco_ur": ["جاز", "زونگ", "ٹیلی نار", "یوفون"],
    "show_ur": ["جیتو پاکستان", "احساس پروگرام", "انعامی اسکیم", "لکی ڈرا"],
    "name_ur": ["احمد رضا", "ثنا طارق", "بلال خان", "عائشہ صدیقی", "عثمان علی"],
    "amount_big_ur": ["50,000 روپے", "پانچ لاکھ روپے", "ایک لاکھ روپے", "25 ہزار روپے", "2,50,000 روپے"],
    "fee_ur": ["500 روپے", "1500 روپے", "دو ہزار روپے", "999 روپے", "3000 روپے"],
    "amount_ur": ["2,500 روپے", "15,000 روپے", "800 روپے", "5 ہزار روپے", "12,000 روپے"],
}
POOLS["fi"] = POOLS["wallet"] + POOLS["bank"]
POOLS["fi_ur"] = POOLS["wallet_ur"] + POOLS["bank_ur"]

GENERATED_SLOTS = {
    "phone": _phone,
    "uan": _uan,
    "amount_big": lambda r: _money(r, AMOUNT_BIG, big=True),
    "fee": lambda r: _money(r, FEE),
    "amount": lambda r: _money(r, AMOUNT),
    "tid": lambda r: _digits(r, r.choice([10, 11, 12])),
    "otp": lambda r: _digits(r, r.choice([4, 5, 6, 6, 6])),
    "acct": lambda r: r.choice(["****", "xxxx", "XXXX-"]) + _digits(r, 4),
    "acct4": lambda r: _digits(r, 4),
    "date": lambda r: r.choice(["{d:02d}-Oct-2026", "{d:02d}/10/2026", "{d} Oct", "Oct {d}"]).format(d=r.randint(1, 28)),
    "time": lambda r: r.choice(["{h:02d}:{m:02d}", "{h12}:{m:02d} PM", "{h12}:{m:02d} AM"]).format(
        h=r.randint(0, 23), h12=r.randint(1, 12), m=r.randint(0, 59)),
}

SLOT_RE = re.compile(r"\{(\w+)\}")


def fill(template: str, rng: random.Random) -> str:
    def _sub(m: re.Match) -> str:
        key = m.group(1)
        if key in GENERATED_SLOTS:
            return GENERATED_SLOTS[key](rng)
        if key in POOLS:
            return rng.choice(POOLS[key])
        raise KeyError(f"unknown slot {{{key}}} in template: {template}")

    return SLOT_RE.sub(_sub, template)


# ------------------------------------------------------------- Roman Urdu variation
# Common spelling variants seen in Pakistani SMS / WhatsApp writing.
ROMAN_VARIANTS = {
    "hai": ["hai", "he", "hy", "h", "hay"],
    "hain": ["hain", "hen", "hn", "hein"],
    "apka": ["apka", "aapka", "ap ka", "aap ka"],
    "aapka": ["aapka", "apka", "ap ka"],
    "apke": ["apke", "aapke", "ap ke", "apky"],
    "aapke": ["aapke", "apke", "ap ke"],
    "apko": ["apko", "aapko", "ap ko", "apku"],
    "aapko": ["aapko", "apko", "ap ko"],
    "karein": ["karein", "karen", "karain", "kren", "kariye"],
    "bhejein": ["bhejein", "bhejain", "bhejen", "bhej dein", "bhejo"],
    "foran": ["foran", "fauran", "foren", "forun", "fori"],
    "paisay": ["paisay", "paise", "pesay", "pese"],
    "paise": ["paise", "paisay", "pese", "pesay"],
    "inaam": ["inaam", "inam", "enaam", "inaaam"],
    "mubarak": ["mubarak", "mubarik", "mubaarak"],
    "jaldi": ["jaldi", "jldi", "jaldii"],
    "abhi": ["abhi", "abi", "abhee"],
    "nahi": ["nahi", "nahin", "nai", "nhi"],
    "account": ["account", "acount", "acc", "akaunt"],
    "number": ["number", "numbr", "no", "nmbr"],
    "shukriya": ["shukriya", "shukria", "shukrya"],
    "wapis": ["wapis", "wapas", "wapes"],
    "qarza": ["qarza", "qarz", "karza"],
    "raqam": ["raqam", "rakam", "raqm"],
    "zaroori": ["zaroori", "zaruri", "zarori"],
    "jama": ["jama", "jamaa", "jma"],
    "ke liye": ["ke liye", "k liye", "kliye", "ke liay", "ky liye"],
    "mein": ["mein", "main", "me", "mai"],
    "hoon": ["hoon", "hun", "hu", "hon"],
    "raha": ["raha", "rha"],
    "kar": ["kar", "kr"],
    "dein": ["dein", "den", "dain"],
    "bhai": ["bhai", "bhae", "bhaii"],
    "kya": ["kya", "kia"],
    "ye": ["ye", "yeh", "yh"],
    "woh": ["woh", "wo", "vo"],
    "please": ["please", "plz", "pls", "plzz"],
    "warna": ["warna", "wrna", "werna"],
    "ho gaya": ["ho gaya", "hogaya", "ho gya", "hogya"],
    "ho jayega": ["ho jayega", "hojayega", "ho jaye ga", "ho jaega"],
    "karwayein": ["karwayein", "karwaen", "karwain", "krwayein"],
    "chahiye": ["chahiye", "chahye", "chaheye", "chaiye"],
    "baad": ["baad", "bad"],
    "sath": ["sath", "saath"],
}
_VARIANT_RE = re.compile(
    r"(?<![A-Za-z])(" + "|".join(sorted((re.escape(k) for k in ROMAN_VARIANTS), key=len, reverse=True)) + r")(?![A-Za-z])",
    re.IGNORECASE,
)


def vary_roman(text: str, rng: random.Random, p: float = 0.4) -> str:
    def _sub(m: re.Match) -> str:
        word = m.group(1)
        if rng.random() >= p:
            return word
        return rng.choice(ROMAN_VARIANTS[word.lower()])

    return _VARIANT_RE.sub(_sub, text)


# ------------------------------------------------------------------------- noise
EMOJI = ["🎉", "💰", "✅", "🙏", "👍", "🔥", "⚠️", "📢", "😊", "❗", "🎁"]
LEET_SUB = {"a": "4", "o": "0", "e": "3", "i": "1", "s": "$"}


def add_noise(text: str, rng: random.Random) -> str:
    r = rng.random
    if r() < 0.15:
        text = text.lower()
    elif r() < 0.05:
        text = text.upper()
    if r() < 0.12:
        text = re.sub(r"[.,!?:]", "", text)
    if r() < 0.08:
        text = re.sub(r" ", "  ", text, count=rng.randint(1, 3))
    if r() < 0.10:
        e = rng.choice(EMOJI)
        text = (e + " " + text) if r() < 0.5 else (text + " " + e)
    if r() < 0.05:
        words = [w for w in text.split(" ") if len(w) >= 4 and w.isascii() and w.isalpha()]
        if words:
            w = rng.choice(words)
            idx = [i for i, ch in enumerate(w) if ch.lower() in LEET_SUB and 0 < i < len(w) - 1]
            if idx:
                i = rng.choice(idx)
                w2 = w[:i] + LEET_SUB[w[i].lower()] + w[i + 1:]
                text = text.replace(w, w2, 1)
    return text.strip()


# ------------------------------------------------------------------------ generate
def generate(seed: int = SEED, variants: int = VARIANTS_PER_FAMILY) -> list[dict]:
    rng = random.Random(seed)
    rows: list[dict] = []
    seen: set[str] = set()
    for families, label in ((ALL_SCAM, 1), (ALL_LEGIT, 0)):
        for fam_id, category, language, phrasings in families:
            made = 0
            attempts = 0
            while made < variants and attempts < variants * 6:
                attempts += 1
                tpl = phrasings[(made + attempts) % len(phrasings)]
                text = fill(tpl, rng)
                if language in ("roman_urdu", "mixed"):
                    text = vary_roman(text, rng)
                text = add_noise(text, rng)
                if text in seen:
                    continue
                seen.add(text)
                made += 1
                rows.append({
                    "id": f"{fam_id}-{made:02d}",
                    "text": text,
                    "label": label,
                    "label_name": "scam" if label else "legit",
                    "language": language,
                    "category": category,
                    "source": "synthetic_template",
                    "synthetic": True,
                    "template_family": fam_id,
                    "author": "claude",
                })
    return rows


def main() -> None:
    rows = generate()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    n_scam = sum(r["label"] for r in rows)
    print(f"wrote {len(rows)} rows ({n_scam} scam, {len(rows) - n_scam} legit) "
          f"from {len(ALL_SCAM) + len(ALL_LEGIT)} families -> {OUT_PATH}")


if __name__ == "__main__":
    main()
