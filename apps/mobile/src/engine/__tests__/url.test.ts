import { analyzeUrl, extractUrls, levenshtein, parseUrl } from '../url';

const level = (u: string) => {
  const r = analyzeUrl(u);
  if (!r.ok) throw new Error(r.message);
  return r;
};
const ids = (u: string) => level(u).cues.map((c) => c.id);

describe('parseUrl', () => {
  it('parses scheme, host, port, path and query', () => {
    const p = parseUrl('https://Secure.HBL-login.example:8443/verify?x=1#top')!;
    expect(p.scheme).toBe('https');
    expect(p.host).toBe('secure.hbl-login.example');
    expect(p.port).toBe('8443');
    expect(p.path).toBe('/verify');
    expect(p.query).toBe('x=1');
    expect(p.registrableDomain).toBe('hbl-login.example');
  });
  it('handles multi-part public suffixes like .com.pk', () => {
    expect(parseUrl('https://www.jazzcash.com.pk/app')!.registrableDomain).toBe('jazzcash.com.pk');
  });
  it('detects the @ userinfo trick', () => {
    const p = parseUrl('https://www.hbl.com@evil.example/login')!;
    expect(p.host).toBe('evil.example');
    expect(p.userinfo).toBe('www.hbl.com');
  });
  it('rejects garbage', () => {
    expect(parseUrl('')).toBeNull();
    expect(analyzeUrl('   ').ok).toBe(false);
  });
});

describe('analyzeUrl', () => {
  it('flags brand impersonation on an unofficial domain', () => {
    const r = level('http://jazzcash-verify.example/login');
    expect(r.level).toBe('HIGH');
    expect(ids('http://jazzcash-verify.example/login')).toEqual(expect.arrayContaining(['brand_impersonation', 'no_https', 'sensitive_path']));
  });
  it('flags look-alike spellings and digit substitution', () => {
    expect(ids('https://easypa1sa.com.pk')).toContain('brand_impersonation');
    expect(ids('https://meezanbnak.com')).toContain('brand_impersonation');
    expect(ids('https://easypaesa.com')).toContain('lookalike');
    expect(level('https://easypaesa.com').level).toBe('HIGH');
  });
  it('flags IP hosts, punycode, shorteners and the @ trick', () => {
    expect(level('http://192.0.2.15/kyc').level).toBe('HIGH');
    expect(ids('https://xn--hbl-xyz.example')).toContain('punycode');
    expect(ids('https://bit.ly/3xYz')).toContain('shortener');
    expect(level('https://www.hbl.com@evil.example/login').level).toBe('HIGH');
  });
  it('does not equate https with safety', () => {
    expect(level('https://hbl-secure-login.example/update').level).toBe('HIGH');
  });
  it('treats official domains as structurally clean but never "safe"', () => {
    const r = level('https://www.jazzcash.com.pk');
    expect(r.level).toBe('LOW');
    expect(r.matchesOfficialDomain).toBe(true);
    expect(r.recommendations.join(' ')).toMatch(/not a guarantee/);
  });
  it('flags very long and encoded links', () => {
    const long = 'https://pay.example/' + 'a%2F'.repeat(10) + 'b'.repeat(120);
    expect(ids(long)).toEqual(expect.arrayContaining(['very_long', 'encoded']));
  });
});

describe('extractUrls / levenshtein', () => {
  it('extracts links from free text without trailing punctuation', () => {
    expect(extractUrls('Verify now: http://x.example/a. Or www.y.example!')).toEqual(['http://x.example/a', 'www.y.example']);
  });
  it('computes edit distance', () => {
    expect(levenshtein('meezan', 'meezam')).toBe(1);
    expect(levenshtein('hbl', 'hbl')).toBe(0);
  });
});
