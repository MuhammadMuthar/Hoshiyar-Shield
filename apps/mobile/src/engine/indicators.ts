/**
 * Deterministic warning-cue extraction (no ML).
 *
 * These cues are concrete, checkable facts about a message ("asks you to
 * share an OTP", "asks for a fee to release a prize"). They are NOT an
 * explanation of the ML model. The model's own explanation comes from its
 * feature weights (see classifier.ts). Matching runs on the same normalised
 * text as the model, sentence by sentence, with negation handling so that
 * security advice ("never share your OTP") is recognised as protective.
 */
import { normalize } from './normalize';
import { analyzeUrl, extractUrls, type UrlAnalysis } from './url';

export type Severity = 'high' | 'medium' | 'low';
/** `action`: the message asks you to DO something risky. `context`: framing only. `protective`: safety advice. */
export type CueKind = 'action' | 'context' | 'protective';

export interface Indicator {
  id: string;
  severity: Severity;
  kind: CueKind;
  label: string;
  explanation: string;
  /** Normalised words/phrases that triggered the cue (for transparency). */
  evidence: string[];
}

export interface IndicatorResult {
  indicators: Indicator[];
  urls: UrlAnalysis[];
}

// ---------------------------------------------------------------------------- lexicons
// Written in natural spelling and passed through normalize(), so they use the
// same canonical form (Urdu letters, de-leeted, digits as 0) as the message.
const L = (words: string[]) => words.map((w) => normalize(w)).filter(Boolean);

const CREDENTIAL = L([
  'otp', 'one time password', 'one time pin', 'pin', 'pin code', 'mpin', 'm pin', 'cvv', 'cvc', 'password',
  'passcode', 'verification code', 'security code', 'code', 'card number', 'card details', 'card ki details',
  'card ke peeche', 'expiry', 'username', 'login details',
  'او ٹی پی', 'پن', 'پن کوڈ', 'ایم پن', 'کوڈ', 'پاس ورڈ', 'کارڈ نمبر', 'کارڈ کی تفصیلات', 'تصدیقی کوڈ', 'ون ٹائم',
]);
/** Verbs that hand something to another person. */
const DISCLOSE = L([
  'share', 'send', 'reply', 'tell', 'provide', 'give', 'forward', 'read', 'sms', 'bata', 'batain', 'batayein',
  'bataein', 'batayen', 'btao', 'bata dein', 'bata do', 'bhej', 'bhejein', 'bhejain', 'bhejen', 'bhejo',
  'likh', 'de dein', 'de do', 'de dena', 'screenshot',
  'بتائیں', 'بتا', 'بھیجیں', 'بھیج', 'شیئر', 'دیں', 'ہمیں',
]);
/** Verbs used on a web form ("enter your PIN at …"): risky only with a link. */
const ENTER = L(['enter', 'confirm', 'verify', 'type', 'update', 'login', 'log in', 'sign in', 'darj', 'درج']);
const NEGATION = L(['never', 'not', 'dont', 'don', 'na', 'nah', 'mat', 'nahi', 'nahin', 'nai', 'nhi', 'kabhi', 'kbhi', 'avoid', 'نہ', 'مت', 'نہیں', 'کبھی']);
const STRONG_NEGATION = L(['never', 'kabhi', 'kbhi', 'کبھی']);
/** Conditional / "this is fraud" framing used by awareness messages. */
const AWARENESS = L([
  'agar koi', 'if someone', 'if anyone', 'اگر کوئی', 'fraud hai', 'fraud he', 'is a scam', 'is fraud', 'scam hai',
  'dhoka hai', 'samajh lein', 'یہ فراڈ ہے', 'فراڈ ہے', 'دھوکہ ہے',
]);
const PROTECTIVE_PHRASES = L([
  'never ask', 'will never', 'never share', 'do not share', 'don t share', 'kabhi nahi mangta', 'nahi mangta',
  'nahi mangte', 'nahi mangti', 'share na karein', 'na batayein', 'kisi ko na batayein', 'kisi ko mat batayein',
  'kisi ke sath share na', 'نہیں مانگتا', 'نہ بتائیں', 'مت بتائیں', 'شیئر نہ کریں',
]);

const FEE = L([
  'fee', 'fees', 'charges', 'charge', 'tax', 'processing', 'registration', 'advance', 'deposit', 'stamp',
  'duty', 'activation', 'clearance', 'token money', 'jurmana', 'fine', 'penalty', 'file charges', 'insurance',
  'فیس', 'چارجز', 'ٹیکس', 'جرمانہ', 'ڈپازٹ', 'پیشگی',
]);
const PAY_IMPERATIVE = L([
  'send', 'pay', 'transfer', 'deposit', 'jama', 'bhejein', 'bhejain', 'bhejen', 'bhejo', 'bhej dein',
  'bhej do', 'karwayein', 'karwaen', 'karwain', 'karwa dein', 'ada karein', 'ada', 'jazzcash karein',
  'easypaisa karein', 'jazzcash kar dein', 'easypaisa kar dein', 'jazzcash karo', 'easypaisa karo',
  'nayapay karein', 'sadapay karein', 'upaisa karein', 'jazzcash karen', 'easypaisa karen', 'jazzcash kr dein',
  'ادا', 'جمع', 'بھیجیں', 'بھیج دیں', 'بھیج دو', 'کروائیں', 'ایزی پیسہ کریں', 'جاز کیش کریں',
]);
const BENEFIT = L([
  'inaam', 'inam', 'enaam', 'prize', 'winner', 'won', 'win', 'jeet', 'jeeta', 'jeeti', 'jeete', 'lucky draw',
  'qurandazi', 'reward', 'bonus', 'cashback', 'gift', 'giveaway', 'cheque', 'muntakhib', 'selected',
  'loan approved', 'approved', 'manzoor', 'sanctioned', 'pass ho gaya', 'qarza', 'loan', 'refund',
  'wapis milenge',
  'انعام', 'انعامی', 'جیت', 'جیتی', 'لکی ڈرا', 'قرعہ', 'بونس', 'منظور', 'قرض', 'قرضہ', 'ریفنڈ', 'واپسی',
]);
const CONTACT = L(['call', 'contact', 'rabta', 'whatsapp', 'call back', 'call karein', 'phone karein', 'رابطہ', 'کال']);
const URGENCY = L([
  'urgent', 'urgently', 'immediately', 'foran', 'fauran', 'fori', 'forun', 'foren', 'abhi', 'jaldi', 'jldi',
  'right now', 'aaj raat', 'aaj hi', 'tonight', 'within', 'expires', 'expire', 'last chance', 'final',
  'aakhri', 'sirf aaj', 'warna', 'wrna', 'otherwise', '00 ghante', '0 ghante', 'deadline',
  'فوری', 'فوراً', 'ابھی', 'جلدی', 'ورنہ', 'آخری',
]);
const THREAT = L([
  'block', 'blocked', 'band', 'bandh', 'suspend', 'suspended', 'closed', 'deactivate', 'deactivated',
  'freeze', 'frozen', 'terminate', 'terminated', 'legal action', 'fir', 'arrest', 'case', 'zabt', 'cancel',
  'cancelled', 'disconnected', 'kaat',
  'بند', 'بلاک', 'معطل', 'منسوخ', 'گرفتار', 'مقدمہ', 'قانونی',
]);
const INSTITUTION = L([
  'jazzcash', 'easypaisa', 'nayapay', 'sadapay', 'upaisa', 'hbl', 'ubl', 'mcb', 'meezan', 'alfalah',
  'allied bank', 'faysal', 'askari', 'bankislami', 'js bank', 'standard chartered', 'bank al habib',
  'state bank', 'sbp', 'fia', 'pta', 'nadra', 'fbr', 'bisp', 'ehsaas', 'police', 'head office',
  'customer care', 'helpline', 'fraud department', 'security department', 'bank',
  'بینک', 'اسٹیٹ بینک', 'ایف آئی اے', 'پی ٹی اے', 'نادرا', 'ایف بی آر', 'جاز کیش', 'ایزی پیسہ',
]);
const SECRECY = L([
  'kisi ko na batana', 'kisi ko mat batana', 'kisi ko mat batayein', 'kisi ko na bataein', 'don t tell anyone',
  'do not tell anyone', 'keep this confidential', 'confidential', 'keep it secret', 'کسی کو نہ بتائیں', 'کسی کو مت بتانا',
]);
const SAFE_ACCOUNT = L(['safe account', 'mehfooz account', 'protected account', 'secure account', 'محفوظ اکاؤنٹ']);
const REMOTE = L(['anydesk', 'teamviewer', 'screen sharing', 'screen share', 'remote helper', 'remote access', 'quick support', 'rustdesk']);
const GUARANTEE = L([
  'guaranteed', 'guarantee', 'double', 'do guna', 'teen guna', 'three times', '2x', '3x', 'munafa pakka',
  'pakka munafa', 'pakki guarantee', 'risk free', 'no risk', 'zero risk', 'sure profit', 'fixed weekly profit',
  'دگنا', 'دگنی', 'یقینی منافع', 'ضمانت', 'گارنٹی',
]);
const INVEST = L([
  'invest', 'investment', 'profit', 'munafa', 'returns', 'earn', 'kamao', 'kamaein', 'kamayein', 'scheme',
  'trading', 'crypto', 'forex', 'bitcoin', 'deposit', 'plot', 'سرمایہ', 'منافع', 'کمائیں',
]);
const NEW_NUMBER = L([
  'naya number', 'naye number', 'new number', 'changed my number', 'phone kharab', 'phone gum', 'phone chori',
  'mobile kharab', 'phone broke', 'dost ka number', 'friend s number', 'نیا نمبر', 'موبائل خراب', 'فون گم', 'دوست کا نمبر',
]);
const MONEY_ASK = L([
  'bhej', 'bhejein', 'bhejo', 'bhej dein', 'bhej do', 'send', 'transfer', 'chahiye', 'paise', 'paisay', 'jazzcash',
  'easypaisa', 'kar dein', 'karo', 'بھیج', 'بھیجیں', 'پیسے', 'ایزی پیسہ', 'جاز کیش', 'کر دیں',
]);
const MONEY = L([
  'rs', 'rupay', 'rupees', 'rupee', 'pkr', 'paise', 'paisay', 'pese', 'raqam', 'amount', 'money', 'payment',
  'balance', 'fee', 'fees', 'charges', 'kiraya', 'rent', 'lakh', 'hazar', 'jazzcash', 'easypaisa', 'nayapay',
  'sadapay', 'upaisa', 'روپے', 'رقم', 'پیسے', 'ہزار', 'لاکھ', 'فیس', 'جاز کیش', 'ایزی پیسہ',
]);
const MISTAKE = L(['ghalti se', 'galti se', 'ghalti', 'by mistake', 'accidentally', 'wrong number', 'غلطی سے']);
const RETURN = L(['wapis', 'wapas', 'return', 'send back', 'send it back', 'back', 'lauta', 'واپس']);
const LINK_ACTION = L(['verify', 'update', 'login', 'log in', 'unblock', 'claim', 'click', 'darj', 'register', 'download', 'install', 'link kholein', 'لنک']);
const PERSONAL = L(['cnic', 'shanakhti card', 'شناختی کارڈ', 'cnic number', 'bank details', 'account details']);
const PERSONAL_VERB = L(['share', 'send', 'bata', 'batayein', 'bataein', 'bhejein', 'provide', 'confirm', 'details', 'reply', 'بتائیں', 'بھیجیں']);

// ---------------------------------------------------------------------------- helpers
interface Sentence {
  tokens: string[];
  padded: string;
}

function toSentence(norm: string): Sentence {
  return { tokens: norm ? norm.split(' ') : [], padded: ' ' + norm + ' ' };
}

/** Indices (token positions) where a phrase starts. */
function findAll(s: Sentence, phrases: string[]): { phrase: string; at: number }[] {
  const out: { phrase: string; at: number }[] = [];
  for (const p of phrases) {
    const pt = p.split(' ');
    for (let i = 0; i + pt.length <= s.tokens.length; i++) {
      let ok = true;
      for (let k = 0; k < pt.length; k++) if (s.tokens[i + k] !== pt[k]) { ok = false; break; }
      if (ok) out.push({ phrase: p, at: i });
    }
  }
  return out;
}

const has = (s: Sentence, phrases: string[]) => phrases.some((p) => s.padded.includes(' ' + p + ' '));
const hits = (s: Sentence, phrases: string[]) => [...new Set(phrases.filter((p) => s.padded.includes(' ' + p + ' ')))];

function isNegated(s: Sentence, verbAt: number): boolean {
  if (has(s, STRONG_NEGATION) || has(s, AWARENESS)) return true;
  for (let i = Math.max(0, verbAt - 5); i <= Math.min(s.tokens.length - 1, verbAt + 2); i++) {
    if (NEGATION.includes(s.tokens[i])) return true;
  }
  return false;
}

/** Split raw text into sentences before normalising (punctuation is removed by normalize). */
export function splitSentences(raw: string): string[] {
  return raw
    .split(/[.!?؟۔\n\r]+|\s[-–—|]\s/)
    .map((x) => normalize(x))
    .filter((x) => x.length > 0);
}

// ---------------------------------------------------------------------------- main
export function extractIndicators(raw: string): IndicatorResult {
  const full = toSentence(normalize(raw));
  const sentences = splitSentences(raw).map(toSentence);
  const found = new Map<string, Indicator>();
  const add = (id: string, severity: Severity, kind: CueKind, label: string, explanation: string, evidence: string[]) => {
    const prev = found.get(id);
    if (prev) prev.evidence = [...new Set([...prev.evidence, ...evidence])];
    else found.set(id, { id, severity, kind, label, explanation, evidence: [...new Set(evidence)] });
  };
  const hasPhone = has(full, ['zphonez']);
  const hasLink = has(full, ['zurlz']);

  let paymentDemand = false;
  for (const s of sentences) {
    // Credential requests vs. protective advice ---------------------------------
    const creds = findAll(s, CREDENTIAL);
    if (creds.length) {
      const verbs = findAll(s, DISCLOSE);
      const live = verbs.filter((v) => !isNegated(s, v.at));
      if (live.length) {
        add('credential_request', 'high', 'action', 'Asks for a code, PIN or card details',
          'It asks you to share an OTP, PIN, password or card details. Banks and wallets never ask for these.',
          [...creds.map((c) => c.phrase), ...live.map((v) => v.phrase)]);
      } else if (verbs.length) {
        add('protective_advice', 'low', 'protective', 'Contains security advice',
          'It tells you NOT to share codes, which genuine bank messages usually say.', creds.map((c) => c.phrase));
      }
      const enter = findAll(s, ENTER).filter((v) => !isNegated(s, v.at));
      if (enter.length && hasLink) {
        add('credential_on_link', 'high', 'action', 'Asks you to enter secrets on a link',
          'It asks you to enter your PIN, OTP or card details on a website link.',
          [...creds.map((c) => c.phrase), ...enter.map((v) => v.phrase)]);
      }
    }
    if (has(s, PROTECTIVE_PHRASES)) {
      add('protective_advice', 'low', 'protective', 'Contains security advice',
        'It tells you NOT to share codes, which genuine bank messages usually say.', hits(s, PROTECTIVE_PHRASES));
    }

    // Money demands -------------------------------------------------------------
    const livePay = findAll(s, PAY_IMPERATIVE).filter((v) => !isNegated(s, v.at));
    if (has(s, FEE) && livePay.length) {
      paymentDemand = true;
      add('payment_demand', 'medium', 'action', 'Asks you to pay a fee or charge',
        'It asks you to pay a fee, tax or charge.', [...hits(s, FEE), ...livePay.map((v) => v.phrase)].slice(0, 6));
    }
    const moneyContext = has(s, MONEY) || s.tokens.some((t) => /^0+$/.test(t) && t.length >= 3);
    if (has(s, ['zphonez']) && moneyContext && livePay.length) {
      add('transfer_to_number', 'medium', 'action', 'Asks you to send money to a mobile number',
        'It asks you to send money to a personal mobile/wallet number you cannot verify.', hits(s, PAY_IMPERATIVE).slice(0, 4));
    }
    if (has(s, ['zphonez']) && findAll(s, CONTACT).some((v) => !isNegated(s, v.at))) {
      add('contact_request', 'medium', 'action', 'Asks you to call or message a number',
        "It asks you to contact a number given in the message instead of your bank's official helpline.", hits(s, CONTACT));
    }
    if (has(s, PERSONAL) && findAll(s, PERSONAL_VERB).some((v) => !isNegated(s, v.at))) {
      add('personal_data', 'medium', 'action', 'Asks for personal or account details',
        'It asks for your CNIC or account details.', hits(s, PERSONAL));
    }
    // Specific fraud mechanisms -------------------------------------------------
    const safe = findAll(s, SAFE_ACCOUNT);
    if (safe.length) {
      if (safe.some((x) => !isNegated(s, x.at))) {
        add('safe_account', 'high', 'action', 'Asks you to move money to a "safe account"',
          'Banks and the State Bank never ask you to move money to a "safe" account.', hits(s, SAFE_ACCOUNT));
      } else {
        add('protective_advice', 'low', 'protective', 'Contains security advice',
          'It warns about a common scam, as awareness messages do.', hits(s, SAFE_ACCOUNT));
      }
    }
    const remote = findAll(s, REMOTE);
    if (remote.length && remote.some((x) => !isNegated(s, x.at))) {
      add('remote_access', 'high', 'action', 'Asks you to install a screen-sharing app',
        'Screen-sharing apps let a caller see your codes and control your phone.', hits(s, REMOTE));
    }
    if (has(s, SECRECY) && !findAll(s, CREDENTIAL).length) {
      add('secrecy', 'medium', 'context', 'Asks you to keep it secret',
        'Scammers ask for secrecy so that you do not check with family or the bank.', hits(s, SECRECY));
    }
  }

  // Message-level combinations ------------------------------------------------------
  if (has(full, BENEFIT) && paymentDemand) {
    add('upfront_fee_for_benefit', 'high', 'action', 'Fee demanded before a prize, loan or refund',
      'It promises money (a prize, loan, refund or reward) but asks you to pay first. That is the classic advance-fee scam.',
      hits(full, BENEFIT).slice(0, 4));
  } else if (has(full, BENEFIT)) {
    add('benefit_claim', 'low', 'context', 'Mentions a prize, loan, reward or refund',
      'Unexpected prizes, approvals or refunds are common bait.', hits(full, BENEFIT).slice(0, 4));
  }
  if (has(full, GUARANTEE) && has(full, INVEST)) {
    add('guaranteed_returns', 'high', 'action', 'Promises guaranteed or unrealistic profit',
      'Guaranteed or "double your money" returns are a hallmark of investment fraud.', hits(full, GUARANTEE).slice(0, 4));
  }
  if (has(full, NEW_NUMBER) && has(full, MONEY_ASK)) {
    add('new_number_money', 'medium', 'action', 'Claims a new number and asks for money',
      'Scammers pose as relatives on a "new number". Call the person on their old number first.', hits(full, NEW_NUMBER));
  }
  if (has(full, MISTAKE) && has(full, RETURN)) {
    add('wrong_transfer_return', 'medium', 'action', 'Asks you to return money "sent by mistake"',
      'Check your real balance in the official app first. These "received" messages are often fake.', hits(full, MISTAKE));
  }
  const urgency = hits(full, URGENCY);
  if (urgency.length) {
    add('urgency', urgency.length >= 2 ? 'medium' : 'low', 'context', 'Creates urgency',
      'It pressures you to act fast. Pressure is used to stop you from verifying.', urgency.slice(0, 4));
  }
  const threat = hits(full, THREAT);
  if (threat.length) {
    add('threat', 'medium', 'context', 'Threatens blocking, closure or penalties',
      'It threatens to block your account or take action against you.', threat.slice(0, 4));
  }
  const inst = hits(full, INSTITUTION);
  if (inst.length) {
    add('institution_mention', 'low', 'context', 'Mentions a bank, wallet or authority',
      'Scammers often impersonate banks, wallets and government bodies. A mention alone proves nothing.', inst.slice(0, 3));
  }

  // Links (structural analysis, never opened) -----------------------------------------
  const urls: UrlAnalysis[] = [];
  for (const u of extractUrls(raw).slice(0, 5)) {
    const r = analyzeUrl(u);
    if (r.ok) urls.push(r);
  }
  const worst = urls.find((u) => u.level === 'HIGH') ?? urls.find((u) => u.level === 'SUSPICIOUS') ?? urls[0];
  if (worst) {
    const host = worst.parsed.host;
    if (worst.level === 'HIGH') {
      add('suspicious_link', 'high', 'action', 'Contains a suspicious link',
        `The link (${host}) has strong warning signs: ${worst.cues.filter((c) => c.severity === 'high').map((c) => c.label.toLowerCase()).join(', ')}.`, [host]);
    } else if (worst.level === 'SUSPICIOUS') {
      add('risky_link', 'medium', 'action', 'Contains a link with warning signs',
        `The link (${host}) has warning signs: ${worst.cues.filter((c) => c.severity === 'medium').map((c) => c.label.toLowerCase()).join(', ')}.`, [host]);
    } else {
      add('contains_link', 'low', 'context', 'Contains a link',
        `Open links only if you trust the sender. Prefer the official app.`, [host]);
    }
    if (has(full, LINK_ACTION) && worst.level !== 'LOW' && !worst.matchesOfficialDomain) {
      add('link_action', 'medium', 'action', 'Asks you to act through a link',
        'It asks you to verify, log in or claim something through a link.', hits(full, LINK_ACTION).slice(0, 3));
    }
  } else if (hasLink) {
    add('contains_link', 'low', 'context', 'Contains a link', 'Open links only if you trust the sender.', []);
  }
  if (hasPhone && !found.has('contact_request') && !found.has('transfer_to_number')) {
    add('mobile_number', 'low', 'context', 'Contains a mobile number',
      'Official institutions use helplines or short codes, not personal mobile numbers.', ['zphonez']);
  }

  const order: Record<Severity, number> = { high: 0, medium: 1, low: 2 };
  const kindOrder: Record<CueKind, number> = { action: 0, context: 1, protective: 2 };
  const indicators = [...found.values()].sort(
    (a, b) => order[a.severity] - order[b.severity] || kindOrder[a.kind] - kindOrder[b.kind],
  );
  return { indicators, urls };
}
