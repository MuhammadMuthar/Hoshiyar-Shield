/**
 * Scam-report validation and local abuse controls (pure logic; storage lives
 * in src/features/reports). Reports stay on the phone in this MVP.
 */
import { normalizePkMobile } from './phone';
import type { ScamCategory } from './reputation';
import { parseUrl } from './url';

export interface ReportDraft {
  target: string;
  category: ScamCategory | null;
  description: string;
  /** Optional, off by default: the user must actively choose to attach message text. */
  messageText?: string;
  includeMessage: boolean;
  consent: boolean;
}

export interface StoredReport {
  id: string;
  createdAt: string;
  targetType: 'phone' | 'url';
  /** E.164 number or URL host */
  target: string;
  category: ScamCategory;
  description: string;
  messageText?: string;
}

export type ReportErrors = Partial<Record<'target' | 'category' | 'description' | 'consent' | 'rate', string>>;

export const MAX_DESCRIPTION = 500;
export const RATE_LIMIT = { perHour: 5, minSecondsBetween: 10 };

export function classifyTarget(target: string): { type: 'phone'; value: string } | { type: 'url'; value: string } | null {
  const t = target.trim();
  if (!t) return null;
  const phone = normalizePkMobile(t);
  if (phone.ok) return { type: 'phone', value: phone.e164 };
  if (/[a-z]/i.test(t) && t.includes('.')) {
    const u = parseUrl(t);
    if (u && u.host.includes('.')) return { type: 'url', value: u.host };
  }
  return null;
}

export function validateReport(d: ReportDraft): ReportErrors {
  const e: ReportErrors = {};
  if (!d.target.trim()) e.target = 'Enter the phone number or link you want to report.';
  else if (!classifyTarget(d.target)) e.target = 'Enter a Pakistani mobile number (03xx…) or a web link.';
  if (!d.category) e.category = 'Choose what kind of scam this was.';
  if (d.description.length > MAX_DESCRIPTION) e.description = `Keep the description under ${MAX_DESCRIPTION} characters.`;
  if (/\b(\d[ -]?){13}\b/.test(d.description)) {
    e.description = "Please don't include CNIC or card numbers in the description.";
  }
  if (!d.consent) e.consent = 'Please confirm the statement above to save the report.';
  return e;
}

/** Returns an error message if the user is reporting too fast, else null. */
export function checkRateLimit(previous: { createdAt: string }[], now: Date = new Date()): string | null {
  const t = now.getTime();
  const times = previous.map((p) => new Date(p.createdAt).getTime()).filter((x) => !Number.isNaN(x));
  const lastHour = times.filter((x) => t - x < 3600_000);
  if (lastHour.length >= RATE_LIMIT.perHour) {
    return `You can save up to ${RATE_LIMIT.perHour} reports per hour. Please try again later.`;
  }
  const latest = Math.max(0, ...times);
  if (latest && t - latest < RATE_LIMIT.minSecondsBetween * 1000) {
    return 'Please wait a few seconds before saving another report.';
  }
  return null;
}

export function buildReport(d: ReportDraft, now: Date = new Date()): StoredReport {
  const target = classifyTarget(d.target);
  if (!target || !d.category) throw new Error('Invalid report: validate first');
  return {
    id: `r-${now.getTime().toString(36)}-${Math.floor(Math.random() * 1e6).toString(36)}`,
    createdAt: now.toISOString(),
    targetType: target.type,
    target: target.value,
    category: d.category,
    description: d.description.trim().slice(0, MAX_DESCRIPTION),
    messageText: d.includeMessage && d.messageText ? d.messageText.slice(0, 2000) : undefined,
  };
}
