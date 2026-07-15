chrome.runtime.onMessage.addListener((message: { type?: string }, _sender, sendResponse) => {
  if (message.type === 'GET_YOUTUBE_VIDEO') {
    const title = document.querySelector<HTMLHeadingElement>('h1.ytd-watch-metadata yt-formatted-string')?.textContent?.trim() || document.title.replace(/\s*-\s*YouTube$/, '');
    sendResponse({ url: location.href, title });
  }
  return false;
});
