import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';

import { KEYS, readJson, removeKey, writeJson } from './storage';

/** Non-sensitive local preferences only. */
export interface Preferences {
  onboarded: boolean;
  /** Opt-in: keep a short list of recent checks on this phone (off by default). */
  saveHistory: boolean;
  /** Hackathon demo mode: show the sample library and demo reputation data. */
  demoMode: boolean;
}

const DEFAULTS: Preferences = { onboarded: false, saveHistory: false, demoMode: true };

interface Ctx extends Preferences {
  loaded: boolean;
  update: (patch: Partial<Preferences>) => void;
  resetAll: () => Promise<void>;
}

const PrefsContext = createContext<Ctx | null>(null);

export function PreferencesProvider({ children }: { children: ReactNode }) {
  const [prefs, setPrefs] = useState<Preferences>(DEFAULTS);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    readJson<Partial<Preferences>>(KEYS.prefs, {}).then((p) => {
      setPrefs({ ...DEFAULTS, ...p });
      setLoaded(true);
    });
  }, []);

  const update = useCallback((patch: Partial<Preferences>) => {
    setPrefs((prev) => {
      const next = { ...prev, ...patch };
      void writeJson(KEYS.prefs, next);
      return next;
    });
  }, []);

  const resetAll = useCallback(async () => {
    await Promise.all([removeKey(KEYS.prefs), removeKey(KEYS.history), removeKey(KEYS.reports)]);
    setPrefs({ ...DEFAULTS, onboarded: true });
    void writeJson(KEYS.prefs, { ...DEFAULTS, onboarded: true });
  }, []);

  const value = useMemo(() => ({ ...prefs, loaded, update, resetAll }), [prefs, loaded, update, resetAll]);
  return <PrefsContext.Provider value={value}>{children}</PrefsContext.Provider>;
}

export function usePreferences(): Ctx {
  const ctx = useContext(PrefsContext);
  if (!ctx) throw new Error('usePreferences must be used inside PreferencesProvider');
  return ctx;
}
