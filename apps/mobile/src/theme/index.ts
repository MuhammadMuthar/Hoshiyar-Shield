/** Hoshiyar Shield design tokens. Dark-first, high contrast for outdoor use. */
import type { RiskLevel } from '../engine/analyze';

export const colors = {
  bg: '#0B1220',
  bgDeep: '#070C17',
  surface: '#111B30',
  surfaceAlt: '#17233D',
  surfaceHigh: '#1E2B49',
  border: '#23314F',
  borderStrong: '#33446A',
  text: '#F8FAFC',
  textMuted: '#AEBBD0',
  textDim: '#7C8CA8',
  emerald: '#10B981',
  emeraldBright: '#34D399',
  emeraldSoft: 'rgba(16,185,129,0.14)',
  teal: '#14B8A6',
  tealSoft: 'rgba(20,184,166,0.14)',
  amber: '#F59E0B',
  amberBright: '#FBBF24',
  amberSoft: 'rgba(245,158,11,0.15)',
  red: '#EF4444',
  redBright: '#F87171',
  redSoft: 'rgba(239,68,68,0.15)',
  sky: '#38BDF8',
  skySoft: 'rgba(56,189,248,0.14)',
  white: '#FFFFFF',
  overlay: 'rgba(7,12,23,0.72)',
} as const;

export const font = {
  regular: 'Inter_400Regular',
  medium: 'Inter_500Medium',
  semibold: 'Inter_600SemiBold',
  bold: 'Inter_700Bold',
  extrabold: 'Inter_800ExtraBold',
} as const;

export const radius = { sm: 10, md: 14, lg: 20, xl: 28, pill: 999 } as const;
export const space = (n: number) => n * 4;

export interface RiskStyle {
  color: string;
  bright: string;
  soft: string;
  label: string;
  short: string;
}

export const riskStyle: Record<RiskLevel, RiskStyle> = {
  HIGH: { color: colors.red, bright: colors.redBright, soft: colors.redSoft, label: 'High Risk', short: 'HIGH RISK' },
  SUSPICIOUS: { color: colors.amber, bright: colors.amberBright, soft: colors.amberSoft, label: 'Suspicious', short: 'SUSPICIOUS' },
  LOW: { color: colors.emerald, bright: colors.emeraldBright, soft: colors.emeraldSoft, label: 'No Obvious Scam Detected', short: 'NO OBVIOUS SCAM' },
};

export const severityColor = { high: colors.red, medium: colors.amber, low: colors.sky } as const;

/** True if the text is mostly Arabic-script (Urdu) characters → render right-to-left. */
export function isRtl(text: string): boolean {
  let rtl = 0;
  let ltr = 0;
  for (const ch of text) {
    const cp = ch.codePointAt(0) ?? 0;
    if (cp >= 0x0600 && cp <= 0x06ff) rtl++;
    else if ((cp >= 65 && cp <= 90) || (cp >= 97 && cp <= 122)) ltr++;
  }
  return rtl > ltr;
}
