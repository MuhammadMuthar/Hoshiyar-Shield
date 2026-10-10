import AsyncStorage from '@react-native-async-storage/async-storage';

/** AsyncStorage wrapper that never throws (storage failures must not break analysis). */
export async function readJson<T>(key: string, fallback: T): Promise<T> {
  try {
    const raw = await AsyncStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

export async function writeJson(key: string, value: unknown): Promise<boolean> {
  try {
    await AsyncStorage.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

export async function removeKey(key: string): Promise<void> {
  try {
    await AsyncStorage.removeItem(key);
  } catch {
    // ignore
  }
}

export const KEYS = {
  prefs: 'hs.prefs.v1',
  history: 'hs.history.v1',
  reports: 'hs.reports.v1',
} as const;
