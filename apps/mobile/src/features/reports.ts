/** Local-only scam reports (this MVP does not upload anything). */
import { useCallback, useEffect, useState } from 'react';

import type { StoredReport } from '../engine/reports';
import type { ReputationRecord } from '../engine/reputation';
import { KEYS, readJson, writeJson } from './storage';

export async function loadReports(): Promise<StoredReport[]> {
  return readJson<StoredReport[]>(KEYS.reports, []);
}

export async function saveReport(r: StoredReport): Promise<boolean> {
  const list = await loadReports();
  return writeJson(KEYS.reports, [r, ...list].slice(0, 200));
}

export function toReputationRecords(reports: StoredReport[]): ReputationRecord[] {
  return reports
    .filter((r) => r.targetType === 'phone')
    .map((r) => ({ number: r.target, category: r.category, date: r.createdAt.slice(0, 10), source: 'local' as const, note: r.description || undefined }));
}

export function useReports() {
  const [reports, setReports] = useState<StoredReport[]>([]);
  const refresh = useCallback(() => {
    loadReports().then(setReports);
  }, []);
  useEffect(refresh, [refresh]);
  return { reports, refresh };
}
