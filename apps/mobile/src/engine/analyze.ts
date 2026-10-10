/**
 * analyzeMessage(): the single entry point every message goes through,
 * whether typed, pasted, shared or picked from the demo library.
 *
 * Pipeline (all on-device, no network):
 *   1. ML classifier (char n-gram TF-IDF + logistic regression) → score.
 *   2. Deterministic indicator engine → concrete warning cues.
 *   3. Structural URL analysis for any links (never opened).
 *   4. Explicit risk fusion (rules F1–F4 below) → HIGH / SUSPICIOUS / LOW.
 *
 * Fusion rules (documented in docs/architecture.md, tested in __tests__):
 *   F1  ML level from the model's validated thresholds.
 *   F2  Escalate: two or more high-severity cues → HIGH. One high-severity cue
 *       → at least SUSPICIOUS, or HIGH if the ML level is already SUSPICIOUS+.
 *   F3  Escalate: a medium-severity *action* cue (asks you to pay, call, return
 *       money, …) together with either another medium/high cue or an ML score
 *       ≥ 0.20 → at least SUSPICIOUS.
 *   F4  Cap: if the message contains security advice ("never share your
 *       OTP") and nothing in it asks you to act (no pay / share / click /
 *       call / install request), a HIGH result is capped at SUSPICIOUS.
 *       Awareness messages share vocabulary with scams; a message that only
 *       advises and asks nothing can't take your money by itself.
 * Fusion never lowers a result to LOW and never hides the ML score.
 */
import { ScamClassifier, displayToken, type ModelArtifact, type TokenContribution } from './classifier';
import { extractIndicators, type Indicator } from './indicators';
import { extractPkMobiles } from './phone';
import type { UrlAnalysis } from './url';

export type RiskLevel = 'HIGH' | 'SUSPICIOUS' | 'LOW';

export const RISK_LABEL: Record<RiskLevel, string> = {
  HIGH: 'High Risk',
  SUSPICIOUS: 'Suspicious',
  LOW: 'No Obvious Scam Detected',
};

export interface AnalysisResult {
  level: RiskLevel;
  title: string;
  headline: string;
  ml: {
    score: number;
    level: RiskLevel;
    thresholds: { suspicious: number; high: number };
    modelVersion: string;
    nFeatures: number;
    topRaising: TokenContribution[];
    topLowering: TokenContribution[];
  };
  indicators: Indicator[];
  urls: UrlAnalysis[];
  phoneNumbers: string[];
  recommendations: string[];
  fusion: string[];
  lowInformation: boolean;
  truncated: boolean;
  charCount: number;
  latencyMs: number;
}

export class AnalysisInputError extends Error {
  constructor(public readonly code: 'empty') {
    super('Paste or type a message to analyse.');
  }
}

export const MAX_CHARS = 10000;
const ORDER: Record<RiskLevel, number> = { LOW: 0, SUSPICIOUS: 1, HIGH: 2 };
const atLeast = (a: RiskLevel, b: RiskLevel): RiskLevel => (ORDER[a] >= ORDER[b] ? a : b);

const ACTION_ADVICE: Record<string, string> = {
  credential_request: 'Do not share any OTP, PIN, CVV or password. No bank or wallet will ever ask for them.',
  credential_on_link: 'Never type your PIN, OTP or card details into a website opened from a message.',
  upfront_fee_for_benefit: "Do not pay any 'verification', 'processing' or 'tax' fee. Genuine prizes and loans never require one.",
  payment_demand: 'Do not send any fee until you have verified the request through an official channel.',
  transfer_to_number: 'Do not send money to this number. Verify the request first using contact details you already trust.',
  contact_request: "Don't call the number in the message. Use the helpline on the back of your card or in the official app.",
  suspicious_link: 'Do not open the link. Open the official app or type the official website yourself.',
  risky_link: 'Avoid the link. Open the official app or type the official website yourself.',
  link_action: 'Do not log in or verify anything through a link in a message.',
  safe_account: 'Banks never ask you to move money to a "safe account". Hang up and call your bank.',
  remote_access: 'Never install AnyDesk or other screen-sharing apps because someone asked you to.',
  guaranteed_returns: 'Guaranteed profit is a red flag. Check that the company is registered with SECP before investing anything.',
  new_number_money: 'Call the person on their old, known number before sending anything.',
  wrong_transfer_return: "Check your balance in the official app. If money really arrived, ask your bank to reverse it. Don't send it to a new number.",
  personal_data: 'Do not share your CNIC or account details with unverified callers or messages.',
};

let defaultClassifier: ScamClassifier | null = null;

/** Lazily load the bundled model (≈230 KB JSON) once. */
export function getClassifier(): ScamClassifier {
  if (!defaultClassifier) {
    const model = require('../../assets/model/hoshiyar-model.json') as ModelArtifact;
    defaultClassifier = new ScamClassifier(model);
  }
  return defaultClassifier;
}

const now = () =>
  typeof globalThis.performance?.now === 'function' ? globalThis.performance.now() : Date.now();

export function analyzeMessage(text: string, classifier: ScamClassifier = getClassifier()): AnalysisResult {
  const start = now();
  if (typeof text !== 'string' || text.trim().length === 0) throw new AnalysisInputError('empty');
  const truncated = text.length > MAX_CHARS;
  const input = truncated ? text.slice(0, MAX_CHARS) : text;

  // 1. ML
  const out = classifier.score(input);
  const t = classifier.thresholds;
  const mlLevel: RiskLevel = out.score >= t.high ? 'HIGH' : out.score >= t.suspicious ? 'SUSPICIOUS' : 'LOW';

  // 2-3. deterministic cues + URL structure
  const { indicators, urls } = extractIndicators(input);
  const high = indicators.filter((i) => i.severity === 'high');
  const medium = indicators.filter((i) => i.severity === 'medium');
  const mediumAction = medium.filter((i) => i.kind === 'action');
  const actions = indicators.filter((i) => i.kind === 'action');

  // 4. fusion
  const fusion: string[] = [`F1 ML score ${out.score.toFixed(3)} → ${mlLevel}`];
  let level: RiskLevel = mlLevel;
  if (high.length >= 2) {
    level = 'HIGH';
    fusion.push(`F2 ${high.length} high-severity cues → HIGH`);
  } else if (high.length === 1) {
    const target: RiskLevel = ORDER[mlLevel] >= ORDER.SUSPICIOUS ? 'HIGH' : 'SUSPICIOUS';
    if (ORDER[target] > ORDER[level]) fusion.push(`F2 high-severity cue "${high[0].id}" → ${target}`);
    level = atLeast(level, target);
  }
  if (mediumAction.length >= 1 && (medium.length + high.length >= 2 || out.score >= 0.2)) {
    if (ORDER[level] < ORDER.SUSPICIOUS) fusion.push(`F3 action cue "${mediumAction[0].id}" with supporting evidence → SUSPICIOUS`);
    level = atLeast(level, 'SUSPICIOUS');
  }
  const protective = indicators.some((i) => i.kind === 'protective');
  if (level === 'HIGH' && actions.length === 0 && protective) {
    level = 'SUSPICIOUS';
    fusion.push('F4 security advice and no request to pay/share/click/call/install → capped at SUSPICIOUS');
  }

  // Explanation & advice
  const lead = actions[0] ?? high[0] ?? medium[0];
  let headline: string;
  if (level === 'HIGH') {
    headline = lead
      ? `${lead.explanation} Do not act on this message without verifying through an official channel.`
      : 'The AI model found strong similarities to known financial scam messages. Verify before acting.';
  } else if (level === 'SUSPICIOUS') {
    headline = lead
      ? `${lead.explanation} It may be genuine, so verify it independently before you do anything.`
      : 'Some wording resembles scam messages. It may be genuine, so verify it independently before acting.';
  } else {
    headline =
      'No strong scam indicators were found. This is not a guarantee. Stay careful with links, codes and payment requests.';
  }

  const recs: string[] = [];
  for (const ind of indicators) {
    const a = ACTION_ADVICE[ind.id];
    if (a && !recs.includes(a)) recs.push(a);
  }
  if (level !== 'LOW') {
    recs.push("Verify through your bank or wallet's official app, or the helpline printed on your card.");
    recs.push('If you already shared a code or sent money, call your bank immediately to block your account.');
  } else {
    recs.push('Never share OTPs, PINs or passwords, even if a message looks official.');
    recs.push('When in doubt, check directly in the official app instead of replying.');
  }

  const latencyMs = now() - start;
  return {
    level,
    title: level === 'HIGH' ? 'High Risk: possible financial scam' : RISK_LABEL[level],
    headline,
    ml: {
      score: out.score,
      level: mlLevel,
      thresholds: t,
      modelVersion: classifier.version,
      nFeatures: out.nFeatures,
      topRaising: out.topRaising.map((x) => ({ ...x, token: displayToken(x.token) })),
      topLowering: out.topLowering.map((x) => ({ ...x, token: displayToken(x.token) })),
    },
    indicators,
    urls,
    phoneNumbers: extractPkMobiles(input),
    recommendations: recs.slice(0, 6),
    fusion,
    lowInformation: out.nFeatures < 25 || out.normalized.length < 15,
    truncated,
    charCount: text.length,
    latencyMs,
  };
}
