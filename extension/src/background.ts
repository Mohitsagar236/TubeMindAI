chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get(['backendUrl']).then((stored) => {
    if (!stored.backendUrl) void chrome.storage.local.set({ backendUrl: 'http://localhost:8000' });
  });
});

chrome.runtime.onMessage.addListener((message: { type?: string; url?: string }, _sender, sendResponse) => {
  if (message.type === 'OPEN_TIMESTAMP' && message.url) {
    chrome.tabs.query({ active: true, currentWindow: true }).then(([tab]) => {
      if (tab?.id) void chrome.tabs.update(tab.id, { url: message.url });
      sendResponse({ ok: true });
    });
    return true;
  }
  return false;
});
