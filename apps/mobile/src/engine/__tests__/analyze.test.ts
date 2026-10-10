import samples from '../../../assets/model/demo-samples.json';
import { AnalysisInputError, analyzeMessage, getClassifier, MAX_CHARS } from '../analyze';
import { extractIndicators } from '../indicators';

const ids = (t: string) => extractIndicators(t).indicators.map((i) => i.id);
const sample = (id: string) => samples.samples.find((s) => s.id === id)!.text;

describe('analyzeMessage: demo library goes through the real pipeline', () => {
  it.each(['demo-prize-ru', 'demo-wallet-suspension', 'demo-otp-ru', 'demo-urdu-otp', 'demo-loan-ru', 'demo-phishing-en'])(
    '%s is HIGH risk', (id) => {
      const r = analyzeMessage(sample(id));
      expect(r.level).toBe('HIGH');
      expect(r.indicators.some((i) => i.severity === 'high')).toBe(true);
      expect(r.recommendations.length).toBeGreaterThan(1);
    },
  );
  it.each(['demo-legit-alert', 'demo-legit-otp', 'demo-legit-family'])('%s has no obvious scam', (id) => {
    const r = analyzeMessage(sample(id));
    expect(r.level).toBe('LOW');
    expect(r.title).toBe('No Obvious Scam Detected');
    expect(r.headline).toMatch(/not a guarantee/);
  });
  it('the ambiguous sample asks the user to verify', () => {
    const r = analyzeMessage(sample('demo-ambiguous'));
    expect(r.level).toBe('SUSPICIOUS');
    expect(r.indicators.map((i) => i.id)).toContain('wrong_transfer_return');
  });
});

describe('the result really comes from the model', () => {
  it('changing the message changes the ML score', () => {
    const a = analyzeMessage('Apka JazzCash account block hone wala hai. Apna OTP foran share karein.');
    const b = analyzeMessage('Apka JazzCash bill payment kamyab raha. Shukriya.');
    expect(a.ml.score - b.ml.score).toBeGreaterThan(0.5);
    expect(a.ml.modelVersion).toBe(getClassifier().version);
  });
  it('explains the score with model-derived words', () => {
    const r = analyzeMessage(sample('demo-prize-ru'));
    expect(r.ml.topRaising.length).toBeGreaterThan(0);
    expect(r.ml.topRaising[0].weight).toBeGreaterThan(0);
  });
});

describe('Roman Urdu variation, Urdu script, code-switching', () => {
  it.each([
    'Mubarak ho! Apka 5 lakh ka inaam nikla hai. Verification fee foran bhejein 0399-5550101',
    'mubarik ho apka 5 lac ka inam nikla he verification fee foren bhejain 0399-5550101',
    'MUBARAK HO APKA INAAM NIKLA HAI!!! FEE BHEJO 03995550101 🎉🎉',
    'Mubaarak ho aapka 5 lakh ka inaam nikla hy. Verification fee fori bhejo',
    'مبارک ہو! آپ کا پانچ لاکھ کا انعام نکلا ہے، فیس 0399-5550101 پر بھیجیں',
    'Congratulations! Apka prize nikla hai, claim fee 500 Easypaisa karein to 0399-5550101',
  ])('flags: %s', (t) => {
    expect(analyzeMessage(t).level).not.toBe('LOW');
  });
  it('handles obfuscation (leetspeak, zero-width, full-width)', () => {
    expect(analyzeMessage('Ap ka 0TP sh@re krein warna J@zzC@sh acc0unt bl0ck ho jaye ga!!!').level).not.toBe('LOW');
    expect(analyzeMessage('apna O​T​P foran share karein warna account band').level).not.toBe('LOW');
  });
});

describe('legitimate messages with scam words are not called scams', () => {
  it.each([
    'Your HBL OTP is 482913. Do not share this code with anyone. HBL will never ask for your OTP.',
    'Ammi maine aapke Easypaisa me 5000 bhej diye hain, dawai le lijiye ga.',
    'Mubarak ho! Tumhara result aa gaya, first division! Ammi bohat khush hain.',
    'آپ کا تصدیقی کوڈ 4821 ہے۔ یہ کوڈ کسی کو مت بتائیں۔',
  ])('%s', (t) => {
    expect(analyzeMessage(t).level).toBe('LOW');
  });
});

describe('indicator engine', () => {
  it('distinguishes credential requests from protective advice', () => {
    expect(ids('Apna OTP foran share karein')).toContain('credential_request');
    expect(ids('Apna OTP kisi ko na batayein')).not.toContain('credential_request');
    expect(ids('Never share your PIN with anyone')).toContain('protective_advice');
    expect(ids('آپ کا پن کوڈ بتائیں')).toContain('credential_request');
    expect(ids('اپنا پن کسی کو نہ بتائیں')).not.toContain('credential_request');
  });
  it('detects advance-fee fraud, safe accounts, remote access and guaranteed returns', () => {
    expect(ids('Apka qarza manzoor hai, processing fee 1500 jama karwayein')).toContain('upfront_fee_for_benefit');
    expect(ids('Apni raqam foran safe account mein transfer karein')).toContain('safe_account');
    expect(ids('Please install AnyDesk and share the code')).toContain('remote_access');
    expect(ids('Invest 5000 and get guaranteed double profit')).toContain('guaranteed_returns');
  });
  it('treats awareness framing as protective, not as a request', () => {
    expect(ids('Agar koi kahe ke paise safe account mein bhejein to ye fraud hai')).not.toContain('safe_account');
    expect(ids('We never ask winners to pay any tax or fee')).not.toContain('payment_demand');
  });
  it('analyses links structurally', () => {
    const r = extractIndicators('Verify now http://easypaisa-verify.example/login');
    expect(r.urls[0].level).toBe('HIGH');
    expect(r.indicators.map((i) => i.id)).toContain('suspicious_link');
  });
});

describe('fusion rules', () => {
  it('F2: a high-severity cue escalates a low ML score to at least SUSPICIOUS', () => {
    const r = analyzeMessage('Hi, please tell me the code you just received on SMS.');
    expect(r.indicators.some((i) => i.id === 'credential_request')).toBe(true);
    expect(r.level).not.toBe('LOW');
  });
  it('F4: security advice that asks nothing is never HIGH', () => {
    const r = analyzeMessage('PTA Advisory: Never share your verification codes with unknown callers claiming to be from banks.');
    expect(r.level).not.toBe('HIGH');
  });
  it('records which rules fired', () => {
    expect(analyzeMessage(sample('demo-ambiguous')).fusion.some((f) => f.startsWith('F3'))).toBe(true);
  });
});

describe('edge cases', () => {
  it('rejects empty input', () => {
    expect(() => analyzeMessage('')).toThrow(AnalysisInputError);
    expect(() => analyzeMessage('   \n ')).toThrow(AnalysisInputError);
  });
  it('flags very short messages as low-information', () => {
    expect(analyzeMessage('ok').lowInformation).toBe(true);
    expect(analyzeMessage('🎉🎉🎉').level).toBe('LOW');
  });
  it('handles long messages quickly and truncates beyond the limit', () => {
    const long = 'Bank ne kaha hai kabhi bhi apna OTP kisi ko na batayein. '.repeat(400);
    const r = analyzeMessage(long);
    expect(r.truncated).toBe(long.length > MAX_CHARS);
    expect(r.latencyMs).toBeLessThan(2000);
  });
  it('works offline: analysis makes no network calls', () => {
    const spy = jest.fn();
    const orig = globalThis.fetch;
    globalThis.fetch = spy as unknown as typeof fetch;
    analyzeMessage(sample('demo-prize-ru'));
    globalThis.fetch = orig;
    expect(spy).not.toHaveBeenCalled();
  });
});
