/**
 * Text normalisation + feature analyzer: TypeScript port of
 * `ml/training/textnorm.py`. Both implement the SAME specification.
 *
 * Any change here must also be made in Python, followed by retraining
 * (`ml/training/train.py`). The parity test (`__tests__/parity.test.ts`)
 * fails if the two drift apart.
 *
 * Parity rules: no `\s`, `\d`, `\w`, `\b` and no look-behind in regexes;
 * ASCII-only lower-casing; per-code-point processing (`Array.from`).
 */

export const NORMALIZER_VERSION = 'hn-1.0';

const WHITESPACE = new Set<number>([
  0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x1c, 0x1d, 0x1e, 0x1f, 0x85, 0xa0, 0x1680, 0x2028, 0x2029, 0x202f,
  0x205f, 0x3000, 0x2000, 0x2001, 0x2002, 0x2003, 0x2004, 0x2005, 0x2006, 0x2007, 0x2008, 0x2009,
  0x200a,
]);
const INVISIBLE = new Set<number>([0x200b, 0x200c, 0x200d, 0x200e, 0x200f, 0x2060, 0xfeff, 0x00ad]);

export const TOKEN_URL = ' zurlz ';
export const TOKEN_EMAIL = ' zemailz ';
export const TOKEN_PHONE = ' zphonez ';
export const TOKEN_UAN = ' zuanz ';

const TLDS =
  'com|pk|net|org|info|biz|xyz|top|online|site|club|live|link|click|example|' +
  'co|io|me|ly|gl|cc|tk|ml|ga|cf|gq|app|shop|store|vip|icu|win|loan|today|support';

const EMAIL_RE = /[a-z0-9._%+-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z][a-z]+/g;
const URL_RE = new RegExp(
  '(?:https?://|www\\.)[^ ]+' +
    '|[a-z0-9-]+(?:\\.[a-z0-9-]+)*\\.(?:' + TLDS + ')(?![a-z0-9-])(?:/[^ ]*)?',
  'g',
);
const UAN_RE = /111[ -]?[0-9]{3}[ -]?[0-9]{3}(?![0-9])|0800[ -]?[0-9]{5}(?![0-9])/g;
const PHONE_RE =
  /(?:\+|00)?92[ -]?3[0-9]{2}[ -]?[0-9]{7}(?![0-9])|03[0-9]{2}[ -]?[0-9]{7}(?![0-9])/g;

const LEET: Record<string, string> = {
  '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a', $: 's',
};

const URDU_MAP: Record<number, string> = {
  0x064a: 'ی', // Arabic yeh -> Urdu yeh
  0x0649: 'ی', // alef maksura -> Urdu yeh
  0x0643: 'ک', // Arabic kaf -> keheh
  0x0647: 'ہ', // Arabic heh -> heh goal
  0x0623: 'ا', // alef hamza above -> alef
  0x0625: 'ا', // alef hamza below -> alef
  0x0629: 'ۃ', // teh marbuta -> teh marbuta goal
};

const isAz = (ch: string) => ch >= 'a' && ch <= 'z';
const isAlnum = (ch: string) => (ch >= 'a' && ch <= 'z') || (ch >= '0' && ch <= '9');

function stepPrepare(text: string): string {
  let out = '';
  for (const raw of Array.from(text)) {
    let cp = raw.codePointAt(0) as number;
    if (INVISIBLE.has(cp)) continue;
    if (WHITESPACE.has(cp)) {
      out += ' ';
      continue;
    }
    if (cp >= 0xff01 && cp <= 0xff5e) cp -= 0xfee0; // full-width ASCII
    if (cp >= 0x06f0 && cp <= 0x06f9) cp = cp - 0x06f0 + 48; // Urdu digits
    else if (cp >= 0x0660 && cp <= 0x0669) cp = cp - 0x0660 + 48; // Arabic-Indic digits
    if (cp >= 65 && cp <= 90) cp += 32; // ASCII lower-case only
    out += String.fromCodePoint(cp);
  }
  return out;
}

function stepDeleet(s: string): string {
  const chars = Array.from(s);
  const n = chars.length;
  let out = '';
  for (let i = 0; i < n; i++) {
    const ch = chars[i];
    const sub = LEET[ch];
    if (sub !== undefined) {
      const prev = i > 0 ? chars[i - 1] : ' ';
      const next = i + 1 < n ? chars[i + 1] : ' ';
      if (isAz(prev) && isAz(next)) {
        out += sub;
        continue;
      }
      if (ch === '0' && !isAlnum(prev) && isAz(next)) {
        out += 'o';
        continue;
      }
    }
    out += ch;
  }
  return out;
}

function mapChar(ch: string): string {
  const cp = ch.codePointAt(0) as number;
  if (cp >= 97 && cp <= 122) return ch;
  if (cp >= 48 && cp <= 57) return '0';
  const mapped = URDU_MAP[cp];
  if (mapped !== undefined) return mapped;
  if ((cp >= 0x064b && cp <= 0x065f) || cp === 0x0670 || cp === 0x0640 || (cp >= 0x06d6 && cp <= 0x06ed)) {
    return '';
  }
  if ((cp >= 0x0621 && cp <= 0x063a) || (cp >= 0x0641 && cp <= 0x064a) || (cp >= 0x0671 && cp <= 0x06d3)) {
    return ch;
  }
  return ' ';
}

/** Normalise a raw message into the canonical form used for features. */
export function normalize(text: string): string {
  if (!text) return '';
  let s = stepPrepare(text);
  s = s.replace(EMAIL_RE, TOKEN_EMAIL);
  s = s.replace(URL_RE, TOKEN_URL);
  s = s.replace(UAN_RE, TOKEN_UAN);
  s = s.replace(PHONE_RE, TOKEN_PHONE);
  s = stepDeleet(s);
  let mapped = '';
  for (const ch of Array.from(s)) mapped += mapChar(ch);
  return mapped
    .split(' ')
    .filter((t) => t.length > 0)
    .join(' ');
}

export interface AnalyzerConfig {
  char_min: number;
  char_max: number;
  word_max: number;
}

/**
 * Feature strings for a *normalised* text: word-bounded character n-grams
 * (each token padded with one space), plus optional `w:` word n-grams.
 * After normalisation every character is in the BMP, so string indices
 * equal code points here.
 */
export function analyze(normalized: string, cfg: AnalyzerConfig): string[] {
  const feats: string[] = [];
  const tokens = normalized ? normalized.split(' ').filter((t) => t.length > 0) : [];
  for (const tok of tokens) {
    const w = ' ' + tok + ' ';
    const len = w.length;
    for (let n = cfg.char_min; n <= cfg.char_max; n++) {
      if (n > len) break;
      for (let i = 0; i <= len - n; i++) feats.push(w.slice(i, i + n));
    }
  }
  if (cfg.word_max >= 1) for (const t of tokens) feats.push('w:' + t);
  if (cfg.word_max >= 2) {
    for (let i = 0; i + 1 < tokens.length; i++) feats.push('w:' + tokens[i] + ' ' + tokens[i + 1]);
  }
  return feats;
}
