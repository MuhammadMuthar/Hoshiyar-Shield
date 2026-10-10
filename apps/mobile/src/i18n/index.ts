import { en, type Strings } from './en';
import { ur } from './ur';

export type Lang = 'en' | 'ur';

/** Returns UI strings; untranslated Urdu keys fall back to English. */
export function strings(lang: Lang = 'en'): Strings {
  return lang === 'ur' ? { ...en, ...ur } : en;
}

/** Share of keys translated (the language switch is only offered when complete). */
export function urduCoverage(): number {
  const keys = Object.keys(en);
  return keys.filter((k) => (ur as Record<string, string | undefined>)[k]).length / keys.length;
}
