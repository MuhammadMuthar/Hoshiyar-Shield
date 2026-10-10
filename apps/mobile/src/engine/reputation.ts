/**
 * Payment-recipient reputation lookup.
 *
 * Data sources, always labelled in the UI:
 *  - DEMO records: synthetic, fictional placeholder numbers (0399-555xxxx)
 *    for the hackathon demo. They do not describe real people.
 *  - LOCAL records: reports the user saved on THIS phone. Not verified and
 *    not sent anywhere.
 *
 * The wording never calls anyone a fraudster: reports are unverified claims.
 * An unreported number is NOT a verified safe number.
 */
import { maskNumber } from './phone';

export type ScamCategory =
  | 'prize_lottery' | 'otp_pin_theft' | 'impersonation' | 'loan_fee' | 'payment_request'
  | 'account_suspension' | 'investment' | 'refund_reversal' | 'other';

export const CATEGORY_LABEL: Record<ScamCategory, string> = {
  prize_lottery: 'Prize / lottery fee',
  otp_pin_theft: 'OTP / PIN theft',
  impersonation: 'Bank or official impersonation',
  loan_fee: 'Loan processing fee',
  payment_request: 'Urgent payment request',
  account_suspension: 'Fake account suspension',
  investment: 'Investment / double money',
  refund_reversal: 'Refund / wrong-transfer trick',
  other: 'Other',
};

/** Short phrase used inside sentences ("N reports describe …"). */
const CATEGORY_PHRASE: Record<ScamCategory, string> = {
  prize_lottery: 'prize-fee requests',
  otp_pin_theft: 'requests for OTPs or PINs',
  impersonation: 'callers claiming to be a bank or official body',
  loan_fee: 'loan processing-fee requests',
  payment_request: 'urgent money requests',
  account_suspension: 'fake account-blocking warnings',
  investment: 'guaranteed-profit investment offers',
  refund_reversal: 'wrong-transfer or refund tricks',
  other: 'other suspicious activity',
};

export interface ReputationRecord {
  /** E.164 */
  number: string;
  category: ScamCategory;
  /** ISO date */
  date: string;
  source: 'demo' | 'local';
  note?: string;
}

/** Synthetic demo records (fictional numbers). */
export const DEMO_RECORDS: ReputationRecord[] = [
  { number: '+923995550142', category: 'prize_lottery', date: '2026-09-21', source: 'demo', note: 'Asked for a "verification fee" to release a prize' },
  { number: '+923995550142', category: 'prize_lottery', date: '2026-09-30', source: 'demo', note: 'Prize message claiming a TV show lucky draw' },
  { number: '+923995550142', category: 'prize_lottery', date: '2026-10-06', source: 'demo', note: 'Requested JazzCash transfer for "tax"' },
  { number: '+923995550193', category: 'loan_fee', date: '2026-09-18', source: 'demo', note: 'Loan "approved", processing fee requested' },
  { number: '+923995550193', category: 'loan_fee', date: '2026-10-03', source: 'demo' },
  { number: '+923995550178', category: 'otp_pin_theft', date: '2026-10-01', source: 'demo', note: 'Asked for the code just received' },
  { number: '+923995550160', category: 'impersonation', date: '2026-09-27', source: 'demo', note: 'Claimed to be bank security, asked to move money to a "safe account"' },
  { number: '+923995550160', category: 'impersonation', date: '2026-10-04', source: 'demo' },
  { number: '+923995550160', category: 'otp_pin_theft', date: '2026-10-07', source: 'demo' },
  { number: '+923995550111', category: 'payment_request', date: '2026-10-05', source: 'demo', note: '"New number" relative asking for urgent money' },
];

export interface ReputationSummary {
  number: string;
  masked: string;
  total: number;
  demoCount: number;
  localCount: number;
  categories: { category: ScamCategory; label: string; count: number }[];
  lastReported: string | null;
  firstReported: string | null;
  level: 'reported' | 'none';
  headline: string;
  caveats: string[];
  records: ReputationRecord[];
}

export function lookupNumber(e164: string, localRecords: ReputationRecord[] = [], includeDemo = true): ReputationSummary {
  const records = [
    ...(includeDemo ? DEMO_RECORDS : []),
    ...localRecords,
  ].filter((r) => r.number === e164);
  const counts = new Map<ScamCategory, number>();
  for (const r of records) counts.set(r.category, (counts.get(r.category) ?? 0) + 1);
  const categories = [...counts.entries()]
    .map(([category, count]) => ({ category, label: CATEGORY_LABEL[category], count }))
    .sort((a, b) => b.count - a.count);
  const dates = records.map((r) => r.date).sort();
  const demoCount = records.filter((r) => r.source === 'demo').length;
  const localCount = records.length - demoCount;

  const caveats: string[] = [];
  let headline: string;
  if (records.length === 0) {
    headline = 'No reports found for this number.';
    caveats.push('An unreported number is not a verified safe number. New scam numbers appear every day.');
    caveats.push('Before paying, confirm who owns the account through a channel you already trust.');
  } else {
    const top = categories[0];
    const n = records.length;
    headline = `${n} ${n === 1 ? 'report describes' : 'reports describe'} suspicious ${CATEGORY_PHRASE[top.category]} associated with this number.`;
    caveats.push('Reports are unverified claims. They do not prove who owns this number or that the owner committed fraud.');
    if (demoCount) caveats.push(`${demoCount} of these ${demoCount === 1 ? 'is' : 'are'} synthetic DEMO records (fictional data for the hackathon demo).`);
    if (localCount) caveats.push(`${localCount} ${localCount === 1 ? 'was' : 'were'} saved on this phone by you. They have not been submitted to any national service.`);
  }
  return {
    number: e164,
    masked: maskNumber(e164),
    total: records.length,
    demoCount,
    localCount,
    categories,
    lastReported: dates.length ? dates[dates.length - 1] : null,
    firstReported: dates.length ? dates[0] : null,
    level: records.length ? 'reported' : 'none',
    headline,
    caveats,
    records,
  };
}
