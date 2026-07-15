export function extractYoutubeVideoId(url: string): string | null {
  try {
    const parsed = new URL(url);
    if (parsed.hostname.includes('youtube.com')) return parsed.searchParams.get('v');
    if (parsed.hostname.includes('youtu.be')) return parsed.pathname.replace(/^\//, '').split('/')[0] || null;
    return null;
  } catch { return null; }
}

export function timestampUrl(videoId: string, seconds: number): string {
  return `https://www.youtube.com/watch?v=${encodeURIComponent(videoId)}&t=${Math.floor(seconds)}s`;
}
