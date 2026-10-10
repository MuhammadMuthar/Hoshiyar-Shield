/**
 * System-level evaluation: the full app pipeline (ML + indicators + fusion)
 * on the same data as the ML-only report.
 *
 * Always runs as a sanity test. With HS_WRITE_SYSTEM_EVAL=1 it also writes
 * ml/artifacts/system-metrics.json and docs/system-evaluation.md:
 *   HS_WRITE_SYSTEM_EVAL=1 npx jest system-eval
 *
 * Fusion rules may only be tuned against the DEV split. Test, challenge and
 * independent (ChatGPT) results are reported, not optimised.
 */
import * as fs from 'fs';
import * as path from 'path';

import { analyzeMessage, type RiskLevel } from '../analyze';

const ROOT = path.resolve(__dirname, '../../../../..');
const ML = path.join(ROOT, 'ml');

interface Row {
  text: string;
  label: 0 | 1;
  language: string;
  group: string;
}

function loadSplit(which: 'dev' | 'test'): Row[] {
  const splits = new Map<string, string>();
  const csv = fs.readFileSync(path.join(ML, 'data/generated/splits.csv'), 'utf-8').trim().split('\n').slice(1);
  for (const line of csv) {
    const [id, , split] = line.split(',');
    splits.set(id, split);
  }
  const rows: Row[] = [];
  const seen = new Set<string>();
  for (const line of fs.readFileSync(path.join(ML, 'data/generated/dataset.jsonl'), 'utf-8').split('\n')) {
    if (!line.trim()) continue;
    const r = JSON.parse(line);
    if (splits.get(r.id) !== which || seen.has(r.id)) continue;
    seen.add(r.id);
    rows.push({ text: r.text, label: r.label, language: r.language, group: r.category });
  }
  return rows;
}

function loadItems(kind: 'challenge' | 'contrib'): { name: string; rows: Row[]; ambiguous: string[] }[] {
  const m = JSON.parse(fs.readFileSync(path.join(ML, 'artifacts/metrics.json'), 'utf-8'));
  const sets = kind === 'challenge' ? [m.challenge] : m.contrib;
  return sets.map((s: { name: string; items: { text: string; label: 0 | 1 | null; language: string; pattern: string }[] }) => ({
    name: s.name,
    rows: s.items.filter((i) => i.label !== null).map((i) => ({ text: i.text, label: i.label as 0 | 1, language: i.language, group: i.pattern })),
    ambiguous: s.items.filter((i) => i.label === null).map((i) => i.text),
  }));
}

function metrics(rows: Row[], flagged: boolean[]) {
  let tp = 0, fp = 0, tn = 0, fn = 0;
  rows.forEach((r, i) => {
    if (r.label === 1 && flagged[i]) tp++;
    else if (r.label === 1) fn++;
    else if (flagged[i]) fp++;
    else tn++;
  });
  const precision = tp + fp ? tp / (tp + fp) : 0;
  const recall = tp + fn ? tp / (tp + fn) : 0;
  return {
    n: rows.length, tp, fp, tn, fn,
    precision: +precision.toFixed(4), recall: +recall.toFixed(4),
    f1: precision + recall ? +((2 * precision * recall) / (precision + recall)).toFixed(4) : 0,
    false_positive_rate: fp + tn ? +(fp / (fp + tn)).toFixed(4) : 0,
  };
}

function evaluate(rows: Row[]) {
  const results = rows.map((r) => analyzeMessage(r.text));
  const sys = (lv: RiskLevel[]) => results.map((x) => lv.includes(x.level));
  const ml = (lv: RiskLevel[]) => results.map((x) => lv.includes(x.ml.level));
  const latencies = results.map((r) => r.latencyMs).sort((a, b) => a - b);
  const byLang: Record<string, unknown> = {};
  for (const lang of [...new Set(rows.map((r) => r.language))].sort()) {
    const idx = rows.map((r, i) => (r.language === lang ? i : -1)).filter((i) => i >= 0);
    const sub = idx.map((i) => rows[i]);
    byLang[lang] = metrics(sub, idx.map((i) => results[i].level !== 'LOW'));
  }
  return {
    ml_only: { at_suspicious: metrics(rows, ml(['SUSPICIOUS', 'HIGH'])), at_high: metrics(rows, ml(['HIGH'])) },
    system: { at_suspicious: metrics(rows, sys(['SUSPICIOUS', 'HIGH'])), at_high: metrics(rows, sys(['HIGH'])) },
    system_by_language_at_suspicious: byLang,
    median_latency_ms_node: +latencies[Math.floor(latencies.length / 2)].toFixed(2),
    errors: {
      missed_scams: rows.filter((r, i) => r.label === 1 && results[i].level === 'LOW').map((r) => r.text).slice(0, 15),
      false_alarms: rows
        .map((r, i) => ({ r, res: results[i] }))
        .filter(({ r, res }) => r.label === 0 && res.level !== 'LOW')
        .map(({ r, res }) => `[${res.level}] ${r.text}`)
        .slice(0, 15),
    },
  };
}

const pct = (x: number) => `${(x * 100).toFixed(1)}%`;

describe('system-level evaluation (ML + indicators + fusion)', () => {
  const dev = evaluate(loadSplit('dev'));
  const test = evaluate(loadSplit('test'));

  it('fusion improves scam recall over ML alone on held-out test families', () => {
    expect(test.system.at_suspicious.recall).toBeGreaterThanOrEqual(test.ml_only.at_suspicious.recall);
  });

  it('keeps the false-positive rate bounded on held-out test families', () => {
    expect(test.system.at_suspicious.false_positive_rate).toBeLessThan(0.2);
  });

  it('writes the system evaluation report when requested', () => {
    if (process.env.HS_WRITE_SYSTEM_EVAL !== '1') return;
    const challenge = loadItems('challenge').map((s) => ({ name: s.name, ...evaluate(s.rows),
      ambiguous: s.ambiguous.map((t) => ({ text: t, level: analyzeMessage(t).level })) }));
    const contrib = loadItems('contrib').map((s) => ({ name: s.name, ...evaluate(s.rows) }));
    const model = JSON.parse(fs.readFileSync(path.join(ML, 'artifacts/hoshiyar-model.json'), 'utf-8'));
    const out = { model_version: model.model_version, generated_by: 'apps/mobile/src/engine/__tests__/system-eval.test.ts', dev, test, challenge, contrib };
    fs.writeFileSync(path.join(ML, 'artifacts/system-metrics.json'), JSON.stringify(out, null, 2));

    const L: string[] = [];
    const row = (name: string, m: ReturnType<typeof metrics>) =>
      `| ${name} | ${m.n} | ${pct(m.precision)} | ${pct(m.recall)} | ${m.f1.toFixed(3)} | ${pct(m.false_positive_rate)} | ${m.fn} | ${m.fp} |`;
    const head = '| Pipeline | n | Precision | Recall | F1 | False-positive rate | Missed scams | False alarms |\n|---|---|---|---|---|---|---|---|';
    const block = (title: string, e: ReturnType<typeof evaluate>, note: string) => {
      L.push(`## ${title}`, '', note, '', head);
      L.push(row('ML only, flagged at Suspicious+', e.ml_only.at_suspicious));
      L.push(row('**Full app (ML + cues + fusion), Suspicious+**', e.system.at_suspicious));
      L.push(row('ML only, High', e.ml_only.at_high));
      L.push(row('**Full app, High**', e.system.at_high));
      L.push('', `Median analysis time (Node.js on the build container, not a phone): ${e.median_latency_ms_node} ms.`, '');
    };
    L.push('# System Evaluation: full on-device pipeline', '',
      '> **Auto-generated** by `HS_WRITE_SYSTEM_EVAL=1 npx jest system-eval` (in `apps/mobile`). Don\'t edit by hand.',
      `> Model \`${model.model_version}\`. All data is synthetic; see \`docs/model-evaluation.md\` for the ML-only report and caveats.`, '',
      'The app\'s verdict combines the ML score with deterministic warning cues (fusion rules F1–F4 in',
      '`apps/mobile/src/engine/analyze.ts`). "Flagged" means the app shows **Suspicious** or **High Risk**.', '',
      '**Tuning discipline:** the fusion rules and cue lexicons were checked only against the *development* split.',
      '**Disclosure:** Claude had seen the ML-only results on the challenge and ChatGPT sets before writing the',
      'indicator engine. The rules are generic (negation-aware credential requests, advance fees, links, safe-account',
      'and remote-access requests) and were not edited to fit individual messages from those sets.', '');
    block('Development split (used for fusion sanity checks)', dev, 'The same families the model was trained on. Optimistic by construction.');
    block('Held-out test families', test, 'Template families never seen in training.');
    for (const c of challenge) {
      block(`Challenge set: ${c.name}`, c as unknown as ReturnType<typeof evaluate>, 'Hand-written unfamiliar patterns (Claude). Evaluation only.');
      L.push('Deliberately ambiguous messages (the right outcome is "verify first"):', '');
      for (const a of c.ambiguous) L.push(`- **${a.level}**: ${a.text}`);
      L.push('');
    }
    for (const c of contrib) {
      block(`Independent set: ${c.name}`, c as unknown as ReturnType<typeof evaluate>, 'Written by ChatGPT without seeing templates or model outputs. Evaluation only.');
      L.push('| Language | n | Recall | False-positive rate |', '|---|---|---|---|');
      for (const [lang, m] of Object.entries(c.system_by_language_at_suspicious) as [string, ReturnType<typeof metrics>][]) {
        L.push(`| ${lang} | ${m.n} | ${pct(m.recall)} | ${pct(m.false_positive_rate)} |`);
      }
      L.push('', '<details><summary>Remaining errors (full app)</summary>', '', '**Missed scams**', '');
      for (const t of c.errors.missed_scams) L.push(`- ${t.replace(/\|/g, '/')}`);
      L.push('', '**False alarms**', '');
      for (const t of c.errors.false_alarms) L.push(`- ${t.replace(/\|/g, '/')}`);
      L.push('', '</details>', '');
    }
    fs.writeFileSync(path.join(ROOT, 'docs/system-evaluation.md'), L.join('\n') + '\n');
  });
});
