/**
 * Structural URL analysis. It NEVER opens, fetches or resolves a link.
 *
 * This is not a malicious-URL database. It inspects the *shape* of a link
 * (host, scheme, encoding, look-alike spellings of a small reference list of
 * official financial domains) and reports concrete warning cues.
 */

export type CueSeverity = 'high' | 'medium' | 'low' | 'info';

export interface UrlCue {
  id: string;
  severity: CueSeverity;
  label: string;
  detail: string;
}

export interface ParsedUrl {
  input: string;
  scheme: string | null;
  userinfo: string | null;
  host: string;
  port: string | null;
  path: string;
  query: string;
  registrableDomain: string;
  subdomain: string;
  tld: string;
}

export type UrlRiskLevel = 'HIGH' | 'SUSPICIOUS' | 'LOW';

export interface UrlAnalysis {
  ok: true;
  parsed: ParsedUrl;
  level: UrlRiskLevel;
  cues: UrlCue[];
  matchesOfficialDomain: boolean;
  recommendations: string[];
}

export interface UrlAnalysisError {
  ok: false;
  error: 'empty' | 'unparseable';
  message: string;
}

/**
 * Starter reference list of official domains for look-alike comparison.
 * MAINTENANCE: verify every entry against the institution's own published
 * channels before production use, and keep this list small and explicit.
 */
export const OFFICIAL_DOMAINS: Record<string, string> = {
  'jazzcash.com.pk': 'JazzCash',
  'easypaisa.com.pk': 'Easypaisa',
  'hbl.com': 'HBL',
  'ubldigital.com': 'UBL',
  'ubl.com.pk': 'UBL',
  'mcb.com.pk': 'MCB',
  'meezanbank.com': 'Meezan Bank',
  'bankalfalah.com': 'Bank Alfalah',
  'abl.com': 'Allied Bank',
  'nayapay.com': 'NayaPay',
  'sadapay.pk': 'SadaPay',
  'sbp.org.pk': 'State Bank of Pakistan',
  'nadra.gov.pk': 'NADRA',
  'fbr.gov.pk': 'FBR',
  'pta.gov.pk': 'PTA',
  'fia.gov.pk': 'FIA',
  'bisp.gov.pk': 'BISP',
  'daraz.pk': 'Daraz',
};

/** Brand keywords that should only appear on the institution's own domain. */
const BRAND_KEYWORDS = [
  'jazzcash', 'easypaisa', 'hbl', 'meezan', 'ubl', 'mcb', 'alfalah', 'nayapay', 'sadapay', 'sbp',
  'nadra', 'fbr', 'bisp', 'ehsaas', 'raast', 'daraz', 'jazz', 'telenor', 'zong', 'ufone', 'pta',
];

const MULTI_PART_SUFFIXES = new Set([
  'com.pk', 'net.pk', 'org.pk', 'gov.pk', 'edu.pk', 'web.pk', 'biz.pk', 'fam.pk', 'gob.pk',
  'co.uk', 'org.uk', 'gov.uk', 'ac.uk', 'com.au', 'co.in', 'com.sa', 'com.ae', 'co.za',
]);

const SHORTENERS = new Set([
  'bit.ly', 'bitly.com', 'tinyurl.com', 't.co', 'goo.gl', 'is.gd', 'cutt.ly', 'rb.gy', 'ow.ly',
  'shorturl.at', 'tiny.cc', 's.id', 'rebrand.ly', 't.ly', 'v.gd', 'shorte.st', 'bl.ink',
]);

const RISKY_TLDS = new Set([
  'xyz', 'top', 'click', 'live', 'link', 'online', 'site', 'club', 'icu', 'vip', 'win', 'loan',
  'tk', 'ml', 'ga', 'cf', 'gq', 'rest', 'buzz', 'monster', 'cam', 'support',
]);

const SENSITIVE_PATH_WORDS = [
  'login', 'signin', 'verify', 'verification', 'update', 'kyc', 'secure', 'unblock', 'unlock',
  'claim', 'reward', 'prize', 'inaam', 'bonus', 'refund', 'otp', 'pin', 'password', 'confirm',
  'wallet', 'account', 'biometric',
];

const LEET_MAP: Record<string, string> = { '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '@': 'a' };

export function levenshtein(a: string, b: string): number {
  if (a === b) return 0;
  const prev = new Array(b.length + 1).fill(0).map((_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    let diag = prev[0];
    prev[0] = i;
    for (let j = 1; j <= b.length; j++) {
      const tmp = prev[j];
      prev[j] = Math.min(prev[j] + 1, prev[j - 1] + 1, diag + (a[i - 1] === b[j - 1] ? 0 : 1));
      diag = tmp;
    }
  }
  return prev[b.length];
}

function hasNonAscii(s: string): boolean {
  for (let i = 0; i < s.length; i++) if (s.charCodeAt(i) > 127) return true;
  return false;
}

function isIpHost(host: string): boolean {
  if (/^[0-9]{1,3}(\.[0-9]{1,3}){3}$/.test(host)) return true; // dotted IPv4
  if (/^[0-9]{6,10}$/.test(host)) return true; // decimal-encoded IPv4
  if (/^0x[0-9a-f]{6,8}$/i.test(host)) return true; // hex-encoded IPv4
  return host.startsWith('[') && host.endsWith(']'); // IPv6 literal
}

/** Parse a URL-ish string without `URL()` (React Native's polyfill is incomplete). */
export function parseUrl(input: string): ParsedUrl | null {
  const raw = input.trim();
  if (!raw) return null;
  const m = /^([a-z][a-z0-9+.-]*):\/\//i.exec(raw);
  const scheme = m ? m[1].toLowerCase() : null;
  let rest = m ? raw.slice(m[0].length) : raw.replace(/^\/\//, '');
  const cut = rest.search(/[/?#]/);
  const authority = cut === -1 ? rest : rest.slice(0, cut);
  rest = cut === -1 ? '' : rest.slice(cut);
  if (!authority) return null;

  const at = authority.lastIndexOf('@');
  const userinfo = at >= 0 ? authority.slice(0, at) : null;
  let hostPort = at >= 0 ? authority.slice(at + 1) : authority;
  let port: string | null = null;
  const pm = /:([0-9]*)$/.exec(hostPort);
  if (pm && !hostPort.endsWith(']')) {
    port = pm[1] || null;
    hostPort = hostPort.slice(0, pm.index);
  }
  const host = hostPort.toLowerCase().replace(/\.$/, '');
  if (!host || /\s/.test(host)) return null;

  const qIdx = rest.indexOf('?');
  const hIdx = rest.indexOf('#');
  const pathEnd = Math.min(qIdx === -1 ? rest.length : qIdx, hIdx === -1 ? rest.length : hIdx);
  const path = rest.slice(0, pathEnd) || '/';
  const query = qIdx === -1 ? '' : rest.slice(qIdx + 1, hIdx > qIdx ? hIdx : undefined);

  const labels = host.split('.').filter(Boolean);
  let regLabels = 2;
  if (labels.length >= 3 && MULTI_PART_SUFFIXES.has(labels.slice(-2).join('.'))) regLabels = 3;
  const ip = isIpHost(host);
  const registrableDomain = ip ? host : labels.slice(-regLabels).join('.');
  const subdomain = ip ? '' : labels.slice(0, Math.max(0, labels.length - regLabels)).join('.');
  const tld = ip ? '' : labels[labels.length - 1] ?? '';
  return { input: raw, scheme, userinfo, host, port, path, query, registrableDomain, subdomain, tld };
}

/** Extract link-like substrings from free text (for message analysis). */
export function extractUrls(text: string): string[] {
  const re =
    /(?:https?:\/\/|www\.)[^\s<>"']+|\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|pk|net|org|info|biz|xyz|top|online|site|club|live|link|click|example|co|io|me|ly|gl|cc|tk|ml|ga|cf|gq|app|shop|store|vip|icu|win|loan|today|support)\b(?:\/[^\s<>"']*)?/gi;
  const found = text.match(re) ?? [];
  const cleaned = found.map((u) => u.replace(/[.,;:!?)\]]+$/, ''));
  return [...new Set(cleaned)].filter((u) => !/@/.test(u.split('/')[0]) || /^https?:/i.test(u));
}

export function analyzeUrl(input: string): UrlAnalysis | UrlAnalysisError {
  if (!input || !input.trim()) return { ok: false, error: 'empty', message: 'Enter a link to check.' };
  const parsed = parseUrl(input);
  if (!parsed) {
    return { ok: false, error: 'unparseable', message: "That doesn't look like a web link. Check the spelling." };
  }
  const cues: UrlCue[] = [];
  const add = (id: string, severity: CueSeverity, label: string, detail: string) =>
    cues.push({ id, severity, label, detail });
  const { host, registrableDomain, subdomain, tld } = parsed;
  const official = OFFICIAL_DOMAINS[registrableDomain];
  const ip = isIpHost(host);

  if (parsed.scheme === 'http') {
    add('no_https', 'medium', 'Not encrypted (http)', 'Banks and wallets always use https. Never enter details on an http page.');
  } else if (parsed.scheme === null) {
    add('no_scheme', 'info', 'No http/https shown', 'The link has no scheme. Assume it is not secure.');
  } else if (parsed.scheme !== 'https') {
    add('odd_scheme', 'medium', `Unusual scheme "${parsed.scheme}"`, 'Financial websites use https.');
  }
  if (ip) add('ip_host', 'high', 'Uses a raw IP address', 'Real banks use named domains, not numbers like 192.0.2.15.');
  if (parsed.userinfo !== null) {
    add('userinfo', 'high', 'Hidden destination (@ trick)', `Everything before "@" is ignored. This link really goes to ${host}.`);
  }
  if (host.split('.').some((l) => l.startsWith('xn--'))) {
    add('punycode', 'high', 'Internationalised (punycode) domain', 'Look-alike letters from other alphabets can imitate real brands.');
  }
  if (hasNonAscii(host)) {
    add('non_ascii', 'high', 'Non-Latin characters in the domain', 'This can imitate a real website using look-alike letters.');
  }
  if (SHORTENERS.has(registrableDomain) || SHORTENERS.has(host)) {
    add('shortener', 'medium', 'Link shortener', 'The real destination is hidden. Banks do not send shortened links.');
  }
  if (!ip && RISKY_TLDS.has(tld)) {
    add('risky_tld', 'medium', `Unusual ending ".${tld}"`, 'Cheap domain endings are common in phishing. Pakistani banks use .com or .com.pk.');
  }
  if (tld === 'example') {
    add('example_domain', 'info', 'Reserved demo domain (.example)', 'This domain is reserved for demonstrations and cannot be registered.');
  }
  const subCount = subdomain ? subdomain.split('.').length : 0;
  if (subCount >= 3) {
    add('many_subdomains', 'medium', 'Many sub-domains', `The real site is ${registrableDomain}; the rest is decoration.`);
  }
  if (parsed.port && !['80', '443'].includes(parsed.port)) {
    add('port', 'medium', `Unusual port :${parsed.port}`, 'Normal websites do not need a port number.');
  }
  const full = parsed.input;
  if (full.length > 120) add('very_long', 'medium', 'Very long link', 'Long links can hide the real destination.');
  else if (full.length > 75) add('long', 'low', 'Long link', 'Check the domain carefully.');
  const pctCount = (full.match(/%[0-9a-f]{2}/gi) ?? []).length;
  if (/%[0-9a-f]{2}/i.test(host) || pctCount > 3 || /%25[0-9a-f]{2}/i.test(full)) {
    add('encoded', 'medium', 'Heavily encoded characters', 'Encoding is sometimes used to disguise where a link goes.');
  }
  const regMain = registrableDomain.split('.')[0] ?? '';
  if ((regMain.match(/-/g) ?? []).length >= 2) {
    add('hyphens', 'low', 'Several hyphens in the domain', 'Phishing domains often look like "bank-secure-login".');
  }

  // Brand impersonation & look-alikes (only when the domain is NOT an official one).
  if (!official && !ip) {
    const hostWords = host.replace(/[^a-z0-9]+/g, ' ');
    // "1" is used for both "i" and "l" in look-alike domains, so check both readings.
    const deleetI = host.replace(/[013457@]/g, (c) => (c === '1' ? 'i' : LEET_MAP[c] ?? c));
    const deleetL = host.replace(/[013457@]/g, (c) => LEET_MAP[c] ?? c);
    const brand = BRAND_KEYWORDS.find((b) =>
      b.length <= 3 ? new RegExp(`(^| )${b}( |$)`).test(hostWords) : deleetI.includes(b) || deleetL.includes(b),
    );
    if (brand) {
      add('brand_impersonation', 'high', `Uses the name "${brand}" on an unofficial domain`,
        `${registrableDomain} is not on our reference list of official ${brand} domains.`);
    } else {
      for (const [dom, name] of Object.entries(OFFICIAL_DOMAINS)) {
        const offMain = dom.split('.')[0];
        const candMain = regMain.replace(/[013457@]/g, (c) => LEET_MAP[c] ?? c);
        const d = levenshtein(candMain, offMain);
        if (offMain.length >= 5 && candMain !== regMain && candMain === offMain) {
          add('lookalike', 'high', `Look-alike of ${name}`, `"${registrableDomain}" swaps letters for numbers to imitate ${dom}.`);
          break;
        }
        if (offMain.length >= 5 && d > 0 && d <= 2) {
          add('lookalike', 'high', `Look-alike of ${name}`, `"${registrableDomain}" is one or two letters away from ${dom}.`);
          break;
        }
      }
    }
  }

  const pathQuery = (parsed.path + ' ' + parsed.query).toLowerCase();
  const sens = SENSITIVE_PATH_WORDS.filter((w) => pathQuery.includes(w));
  if (sens.length && !official) {
    add('sensitive_path', 'medium', 'Asks for sensitive actions', `The link path mentions "${sens.slice(0, 3).join('", "')}".`);
  }

  if (official) {
    cues.push({
      id: 'official_domain', severity: 'info', label: `Matches the official ${official} domain`,
      detail: 'Structural check only. Official sites can still host fake pages if the link was altered. Prefer the official app.',
    });
  }

  const highs = cues.filter((c) => c.severity === 'high').length;
  const mediums = cues.filter((c) => c.severity === 'medium').length;
  const lows = cues.filter((c) => c.severity === 'low').length;
  let level: UrlRiskLevel = 'LOW';
  if (highs > 0 || mediums >= 3) level = 'HIGH';
  else if (mediums >= 1 || lows >= 2) level = 'SUSPICIOUS';

  const recommendations =
    level === 'LOW'
      ? [
          'No obvious structural red flags. This is not a guarantee the site is safe.',
          'For banking, use the official app or type the address yourself instead of tapping links.',
        ]
      : [
          'Do not open this link or enter any PIN, OTP, password or card details.',
          "Open your bank or wallet's official app directly to check any claim.",
          'If you already entered details, call your bank using the number on your card.',
        ];
  return { ok: true, parsed, level, cues, matchesOfficialDomain: Boolean(official), recommendations };
}
