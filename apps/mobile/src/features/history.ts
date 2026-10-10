/**
 * Recent checks: ONLY stored when the user opts in (Settings → Save recent
 * checks). We keep a short preview, not the full message.
 */
import { useCallback, useEffect, useState } from 'react';

import type { RiskLevel } from '../engine/analyze';
import { KEYS, readJson, writeJson } from './storage';

export interface HistoryItem {
  id: string;
  at: string;
  kind: 'message' | 'link' | 'number';
  level: RiskLevel | 'REPORTED' | 'NONE';
  preview: string;
}

const MAX_ITEMS = 12;

export async function addHistory(item: Omit<HistoryItem, 'id' | 'at'>, enabled: boolean) {
  if (!enabled) return;
  const list = await readJson<HistoryItem[]>(KEYS.history, []);
  const preview = item.preview.length > 48 ? item.preview.slice(0, 48) + '…' : item.preview;
  const next = [{ ...item, preview, id: `${Date.now()}`, at: new Date().toISOString() }, ...list].slice(0, MAX_ITEMS);
  await writeJson(KEYS.history, next);
}

export function useHistory(enabled: boolean) {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const refresh = useCallback(() => {
    const load = enabled ? readJson<HistoryItem[]>(KEYS.history, []) : Promise.resolve<HistoryItem[]>([]);
    void load.then(setItems);
  }, [enabled]);
  useEffect(refresh, [refresh]);
  const clear = useCallback(async () => {
    await writeJson(KEYS.history, []);
    setItems([]);
  }, []);
  return { items, refresh, clear };
}
