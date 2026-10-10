/** Pakistani mobile number normalisation (+92 3XX XXXXXXX). */

export interface PhoneParseOk {
  ok: true;
  /** E.164, e.g. +923995550142 */
  e164: string;
  /** Local display, e.g. 0399-5550142 */
  display: string;
  /** Original network prefix. Numbers can be ported, so this is only a hint. */
  prefixNetwork: string;
}

export interface PhoneParseError {
  ok: false;
  error: 'empty' | 'invalid_chars' | 'not_mobile' | 'wrong_length';
  message: string;
}

function prefixNetwork(code: number): string {
  if (code >= 300 && code <= 309) return 'Jazz prefix';
  if (code >= 320 && code <= 329) return 'Jazz (ex-Warid) prefix';
  if (code >= 310 && code <= 319) return 'Zong prefix';
  if (code >= 330 && code <= 339) return 'Ufone/Onic prefix';
  if (code >= 340 && code <= 349) return 'Telenor prefix';
  if (code === 355) return 'SCOM prefix';
  return 'Unrecognised prefix';
}

export function normalizePkMobile(input: string): PhoneParseOk | PhoneParseError {
  const raw = (input ?? '').trim();
  if (!raw) return { ok: false, error: 'empty', message: 'Enter a mobile number, e.g. 0399-5550142.' };
  if (/[^0-9+\-\s().]/.test(raw)) {
    return { ok: false, error: 'invalid_chars', message: 'Use digits only, e.g. 0399-5550142 or +92 399 5550142.' };
  }
  if (raw.indexOf('+') > 0 || (raw.match(/\+/g) ?? []).length > 1) {
    return { ok: false, error: 'invalid_chars', message: '"+" can only appear at the start (+92…).' };
  }
  let digits = raw.replace(/[^0-9]/g, '');
  if (raw.startsWith('+')) {
    if (!digits.startsWith('92')) {
      return { ok: false, error: 'not_mobile', message: 'Only Pakistani (+92) mobile numbers are supported.' };
    }
    digits = digits.slice(2);
  } else if (digits.startsWith('0092')) digits = digits.slice(4);
  else if (digits.startsWith('92') && digits.length === 12) digits = digits.slice(2);
  else if (digits.startsWith('0')) digits = digits.slice(1);

  if (!digits.startsWith('3')) {
    return { ok: false, error: 'not_mobile', message: 'Pakistani mobile numbers start with 03 (e.g. 0300…). Landlines are not supported.' };
  }
  if (digits.length !== 10) {
    return { ok: false, error: 'wrong_length', message: 'A Pakistani mobile number has 11 digits, e.g. 0399-5550142.' };
  }
  const code = Number(digits.slice(0, 3));
  return {
    ok: true,
    e164: `+92${digits}`,
    display: `0${digits.slice(0, 3)}-${digits.slice(3)}`,
    prefixNetwork: prefixNetwork(code),
  };
}

/** Find Pakistani mobile numbers inside free text (normalised to E.164). */
export function extractPkMobiles(text: string): string[] {
  const re = /(?:\+|00)?92[ -]?3[0-9]{2}[ -]?[0-9]{7}(?![0-9])|0?3[0-9]{2}[ -]?[0-9]{7}(?![0-9])/g;
  const out = new Set<string>();
  for (const m of text.match(re) ?? []) {
    const r = normalizePkMobile(m.replace(/^00/, '+'));
    if (r.ok) out.add(r.e164);
  }
  return [...out];
}

/** Mask a number for display in aggregate/public views: 0399-55•••42 */
export function maskNumber(e164: string): string {
  const local = '0' + e164.replace(/^\+92/, '');
  return `${local.slice(0, 4)}-${local.slice(4, 6)}•••${local.slice(-2)}`;
}
