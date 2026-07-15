import { useMemo } from 'react';
import { CurrentVideo } from '../types';
import { extractYoutubeVideoId } from '../utils/youtube';

export function useYoutubeVideo(tab: chrome.tabs.Tab | null): CurrentVideo | null {
  return useMemo(() => {
    const url = tab?.url ?? '';
    const youtubeVideoId = extractYoutubeVideoId(url);
    if (!youtubeVideoId) return null;
    return { youtubeVideoId, youtubeUrl: url, title: tab?.title?.replace(/\s*-\s*YouTube$/, '') || 'YouTube video', thumbnailUrl: `https://img.youtube.com/vi/${youtubeVideoId}/hqdefault.jpg` };
  }, [tab]);
}
