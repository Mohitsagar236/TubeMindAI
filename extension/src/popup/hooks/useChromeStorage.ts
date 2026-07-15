import { useCallback, useEffect, useState } from 'react';

export function useChromeStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(initialValue);
  const [ready, setReady] = useState(false);
  useEffect(() => { chrome.storage.local.get(key).then((result) => { if (result[key] !== undefined) setValue(result[key] as T); setReady(true); }); }, [key]);
  const save = useCallback(async (next: T) => { setValue(next); await chrome.storage.local.set({ [key]: next }); }, [key]);
  return { value, save, ready };
}
