import { useEffect, useState } from 'react';

export function useCurrentTab() {
  const [tab, setTab] = useState<chrome.tabs.Tab | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => { chrome.tabs.query({ active: true, currentWindow: true }).then(([active]) => setTab(active ?? null)).finally(() => setLoading(false)); }, []);
  return { tab, loading };
}
