import { extractPkMobiles, maskNumber, normalizePkMobile } from '../phone';

describe('normalizePkMobile', () => {
  it.each([
    '0399-5550142', '03995550142', '+92 399 5550142', '+923995550142', '0092 399 5550142', '923995550142', '3995550142', '(0399) 555-0142',
  ])('normalises %s', (input) => {
    const r = normalizePkMobile(input);
    expect(r).toEqual(expect.objectContaining({ ok: true, e164: '+923995550142', display: '0399-5550142' }));
  });
  it.each([
    ['', 'empty'], ['abc', 'invalid_chars'], ['042-35761234', 'not_mobile'], ['0300-12345', 'wrong_length'],
    ['+1 555 0100', 'not_mobile'], ['03001234567890', 'wrong_length'], ['03+001234567', 'invalid_chars'],
  ])('rejects %s (%s)', (input, error) => {
    const r = normalizePkMobile(input);
    expect(r.ok).toBe(false);
    if (!r.ok) expect(r.error).toBe(error);
  });
  it('gives a network prefix hint', () => {
    const r = normalizePkMobile('0345-5550142');
    expect(r.ok && r.prefixNetwork).toBe('Telenor prefix');
  });
});

describe('extractPkMobiles / maskNumber', () => {
  it('finds numbers in text', () => {
    expect(extractPkMobiles('call 0399-5550142 or +92 399 5550111')).toEqual(['+923995550142', '+923995550111']);
  });
  it('masks numbers for aggregate views', () => {
    expect(maskNumber('+923995550142')).toBe('0399-55•••42');
  });
});
