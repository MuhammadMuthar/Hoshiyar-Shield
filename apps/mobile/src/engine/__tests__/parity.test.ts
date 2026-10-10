/**
 * Python ⇄ TypeScript parity. Fixtures come from `ml/training/train.py`, which
 * runs the pure-Python reference (`jsonmodel.py`) on the exported model.
 */
import fixtures from '../__fixtures__/parity-fixtures.json';
import modelJson from '../../../assets/model/hoshiyar-model.json';
import { ScamClassifier, type ModelArtifact } from '../classifier';
import { NORMALIZER_VERSION, normalize } from '../normalize';

const clf = new ScamClassifier(modelJson as ModelArtifact);

describe('Python/TypeScript parity', () => {
  it('fixtures were generated for the bundled model and normaliser', () => {
    expect(fixtures.model_version).toBe(clf.version);
    expect(fixtures.normalizer_version).toBe(NORMALIZER_VERSION);
    expect(fixtures.fixtures.length).toBeGreaterThan(200);
  });

  it.each(fixtures.fixtures.map((f, i) => [i, f] as const))('fixture %i normalises identically', (_i, f) => {
    expect(normalize(f.text)).toBe(f.normalized);
  });

  it('every fixture scores identically (|Δ| < 1e-9)', () => {
    let worst = 0;
    for (const f of fixtures.fixtures) {
      const out = clf.score(f.text, false);
      expect(out.nFeatures).toBe(f.n_features);
      worst = Math.max(worst, Math.abs(out.score - f.p), Math.abs(out.z - f.z));
    }
    expect(worst).toBeLessThan(1e-9);
  });
});
