/**
 * English UI strings for the core flows. ChatGPT provides the Urdu
 * translation in ./ur.ts (docs/COLLABORATION.md §2.2-C), same keys.
 * Safety meaning must stay exact: "No obvious scam detected" ≠ "safe".
 */
export const en = {
  tagline: 'Scams se hoshiyar. Paisa mehfooz.',
  welcomeTitle: 'Hoshiyar raho. Apna paisa bachao.',
  welcomeBody: 'AI-powered protection against suspicious financial messages and payment scams.',
  getProtected: 'Get Protected',
  scanMessage: 'Scan a Message',
  checkLink: 'Check a Link',
  checkNumber: 'Check a Number',
  reportScam: 'Report a Scam',
  analyze: 'Analyse message',
  paste: 'Paste',
  clear: 'Clear',
  scanAnother: 'Scan another',
  riskHigh: 'High Risk',
  riskSuspicious: 'Suspicious',
  riskLow: 'No Obvious Scam Detected',
  privacyOnDevice: 'Analysed on this phone. Your message is not uploaded.',
  aiCanBeWrong: 'AI can make mistakes. Always verify through official channels.',
};

export type Strings = typeof en;
