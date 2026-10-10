/**
 * In-memory hand-off of the current analysis between screens. Message text
 * is never put in the URL and is never persisted here.
 */
import { useSyncExternalStore } from 'react';

import type { AnalysisResult } from '../engine/analyze';

export interface CurrentAnalysis {
  text: string;
  result: AnalysisResult;
  source: 'typed' | 'pasted' | 'sample' | 'link';
  sampleId?: string;
}

let current: CurrentAnalysis | null = null;
const listeners = new Set<() => void>();

export function setCurrentAnalysis(a: CurrentAnalysis | null) {
  current = a;
  listeners.forEach((l) => l());
}

export function getCurrentAnalysis() {
  return current;
}

export function useCurrentAnalysis(): CurrentAnalysis | null {
  return useSyncExternalStore(
    (cb) => {
      listeners.add(cb);
      return () => listeners.delete(cb);
    },
    () => current,
    () => current,
  );
}
