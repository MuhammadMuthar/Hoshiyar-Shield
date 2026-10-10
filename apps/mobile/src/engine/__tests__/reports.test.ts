import { buildReport, checkRateLimit, classifyTarget, validateReport, type ReportDraft } from '../reports';
import { DEMO_RECORDS, lookupNumber } from '../reputation';

const draft = (o: Partial<ReportDraft> = {}): ReportDraft => ({
  target: '0399-5550199', category: 'prize_lottery', description: '', includeMessage: false, consent: true, ...o,
});

describe('report validation', () => {
  it('accepts a valid phone or URL report', () => {
    expect(validateReport(draft())).toEqual({});
    expect(validateReport(draft({ target: 'http://jazzcash-verify.example/x' }))).toEqual({});
    expect(classifyTarget('http://jazzcash-verify.example/x')).toEqual({ type: 'url', value: 'jazzcash-verify.example' });
  });
  it('requires target, category and consent', () => {
    const e = validateReport(draft({ target: '', category: null, consent: false }));
    expect(Object.keys(e).sort()).toEqual(['category', 'consent', 'target']);
  });
  it('rejects invalid targets and CNIC/card numbers in descriptions', () => {
    expect(validateReport(draft({ target: 'hello' })).target).toBeTruthy();
    expect(validateReport(draft({ description: 'my cnic 35202 1234567 1 abc' })).description).toBeTruthy();
    expect(validateReport(draft({ description: 'x'.repeat(501) })).description).toBeTruthy();
  });
  it('never stores message text unless the user opted in', () => {
    expect(buildReport(draft({ messageText: 'secret' })).messageText).toBeUndefined();
    expect(buildReport(draft({ messageText: 'secret', includeMessage: true })).messageText).toBe('secret');
  });
});

describe('rate limiting', () => {
  const now = new Date('2026-10-10T10:00:00Z');
  it('blocks rapid repeats and more than 5 per hour', () => {
    expect(checkRateLimit([], now)).toBeNull();
    expect(checkRateLimit([{ createdAt: '2026-10-10T09:59:55Z' }], now)).toMatch(/wait/);
    const five = Array.from({ length: 5 }, (_, i) => ({ createdAt: new Date(now.getTime() - (i + 1) * 60_000).toISOString() }));
    expect(checkRateLimit(five, now)).toMatch(/per hour/);
    expect(checkRateLimit([{ createdAt: '2026-10-10T08:00:00Z' }], now)).toBeNull();
  });
});

describe('reputation lookup', () => {
  it('summarises demo reports without accusing anyone', () => {
    const r = lookupNumber('+923995550142');
    expect(r.total).toBe(3);
    expect(r.headline).toBe('3 reports describe suspicious prize-fee requests associated with this number.');
    expect(r.caveats.join(' ')).toMatch(/synthetic DEMO/);
    expect(r.headline + r.caveats.join(' ')).not.toMatch(/fraudster|scammer/i);
    expect(r.lastReported).toBe('2026-10-06');
  });
  it('says an unreported number is not verified safe', () => {
    const r = lookupNumber('+923995550999');
    expect(r.level).toBe('none');
    expect(r.caveats[0]).toMatch(/not a verified safe number/);
  });
  it('merges local reports and labels them', () => {
    const r = lookupNumber('+923995550999', [{ number: '+923995550999', category: 'loan_fee', date: '2026-10-09', source: 'local' }]);
    expect(r.localCount).toBe(1);
    expect(r.caveats.join(' ')).toMatch(/saved on this phone/);
  });
  it('demo data only uses the placeholder number range', () => {
    for (const rec of DEMO_RECORDS) expect(rec.number).toMatch(/^\+92399555\d{4}$/);
  });
});
