/**
 * On-device TF-IDF + logistic-regression inference.
 *
 * Mirrors `ml/training/jsonmodel.py` (JsonModel.score_details) operation by
 * operation, including summation order, so scores match the Python reference
 * to ~1e-12. No network access: the model is a bundled JSON asset.
 */
import { analyze, normalize, type AnalyzerConfig, NORMALIZER_VERSION } from './normalize';

export interface ModelArtifact {
  format: string;
  format_version: number;
  model_version: string;
  normalizer_version: string;
  analyzer: AnalyzerConfig;
  tfidf: { sublinear_tf: boolean; norm: string };
  thresholds: { suspicious: number; high: number };
  intercept: number;
  vocab: string[];
  idf: number[];
  coef: number[];
  metadata: Record<string, unknown>;
}

/** A word whose character n-grams pushed the score up (or down). */
export interface TokenContribution {
  token: string;
  /** Sum of (feature value × weight) for the token's n-grams; >0 = towards "scam". */
  weight: number;
}

export interface ClassifierOutput {
  normalized: string;
  /** Logit (intercept + Σ feature × weight). */
  z: number;
  /** Logistic-regression output in [0,1]. NOT a calibrated real-world probability. */
  score: number;
  /** Number of distinct model features present in the message. */
  nFeatures: number;
  /** Words that raised the score most (model-derived explanation). */
  topRaising: TokenContribution[];
  /** Words that lowered the score most. */
  topLowering: TokenContribution[];
}

/** Numerically stable logistic function (same as Python `sigmoid`). */
export function sigmoid(z: number): number {
  if (z >= 0) return 1 / (1 + Math.exp(-z));
  const e = Math.exp(z);
  return e / (1 + e);
}

export class ScamClassifier {
  readonly model: ModelArtifact;
  private readonly index: Map<string, number>;

  constructor(model: ModelArtifact) {
    if (model.format !== 'hoshiyar-tfidf-logreg') throw new Error(`Unsupported model format: ${model.format}`);
    if (model.normalizer_version !== NORMALIZER_VERSION) {
      throw new Error(
        `Model was trained with normaliser ${model.normalizer_version} but the app has ${NORMALIZER_VERSION}`,
      );
    }
    if (model.vocab.length !== model.idf.length || model.vocab.length !== model.coef.length) {
      throw new Error('Corrupt model: vocab/idf/coef length mismatch');
    }
    this.model = model;
    this.index = new Map(model.vocab.map((term, i) => [term, i]));
  }

  get version(): string {
    return this.model.model_version;
  }

  get thresholds(): { suspicious: number; high: number } {
    return this.model.thresholds;
  }

  score(text: string, explain = true): ClassifierOutput {
    const normalized = normalize(text);
    const tokens = normalized ? normalized.split(' ') : [];
    const cfg = this.model.analyzer;

    // Term counts in first-occurrence order (Map preserves insertion order, like a Python dict).
    const counts = new Map<number, number>();
    for (const f of analyze(normalized, cfg)) {
      const j = this.index.get(f);
      if (j !== undefined) counts.set(j, (counts.get(j) ?? 0) + 1);
    }

    const { idf, coef } = this.model;
    const values = new Map<number, number>();
    for (const [j, c] of counts) values.set(j, (1 + Math.log(c)) * idf[j]);
    let sumSq = 0;
    for (const v of values.values()) sumSq += v * v;
    const norm2 = Math.sqrt(sumSq);

    let z = this.model.intercept;
    const featureContribution = new Map<number, number>();
    if (norm2 > 0) {
      for (const [j, v] of values) {
        const contrib = (v / norm2) * coef[j];
        z += contrib;
        featureContribution.set(j, contrib);
      }
    }
    const score = sigmoid(z);

    let topRaising: TokenContribution[] = [];
    let topLowering: TokenContribution[] = [];
    if (explain && featureContribution.size > 0) {
      // Spread each n-gram's contribution evenly over its occurrences, then add
      // it up per token. Because the model is linear, these per-word sums
      // decompose the score exactly: a faithful, model-derived explanation.
      const perToken = new Map<string, number>();
      const charOnly: AnalyzerConfig = { ...cfg, word_max: 0 };
      for (const tok of tokens) {
        let sum = 0;
        const feats = analyze(tok, charOnly);
        if (cfg.word_max >= 1) feats.push('w:' + tok);
        for (const f of feats) {
          const j = this.index.get(f);
          if (j === undefined) continue;
          const contrib = featureContribution.get(j);
          if (contrib !== undefined) sum += contrib / (counts.get(j) ?? 1);
        }
        perToken.set(tok, (perToken.get(tok) ?? 0) + sum);
      }
      const ranked = [...perToken.entries()]
        .filter(([tok]) => tok.length > 1)
        .map(([token, weight]) => ({ token, weight }));
      topRaising = ranked.filter((t) => t.weight > 0).sort((a, b) => b.weight - a.weight).slice(0, 6);
      topLowering = ranked.filter((t) => t.weight < 0).sort((a, b) => a.weight - b.weight).slice(0, 4);
    }

    return { normalized, z, score, nFeatures: counts.size, topRaising, topLowering };
  }
}

/** Human-friendly label for placeholder tokens produced by the normaliser. */
export function displayToken(token: string): string {
  switch (token) {
    case 'zphonez':
      return 'a mobile number';
    case 'zurlz':
      return 'a link';
    case 'zuanz':
      return 'a helpline number';
    case 'zemailz':
      return 'an email address';
    default:
      return token.replace(/0+/g, '#');
  }
}
