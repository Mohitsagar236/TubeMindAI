import { ChatResponse, CurrentVideo, Flashcard, ProcessVideoResponse, QuizQuestion, Settings } from '../types';

type RequestOptions = { method?: string; body?: unknown };
export class BackendClient {
  constructor(private settings: Settings) {}
  private async request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (this.settings.apiKey.trim()) headers['X-OpenAI-API-Key'] = this.settings.apiKey.trim();
    let response: Response;
    try { response = await fetch(`${this.settings.backendUrl.replace(/\/$/, '')}${path}`, { method: options.method ?? 'GET', headers, body: options.body === undefined ? undefined : JSON.stringify(options.body) }); }
    catch { throw new Error('Unable to connect to TubeMind backend. Please make sure the backend server is running.'); }
    if (!response.ok) {
      const data = await response.json().catch(() => ({})) as { detail?: string; message?: string };
      throw new Error(data.detail || data.message || `Request failed (${response.status}).`);
    }
    return response.json() as Promise<T>;
  }
  processVideo(video: CurrentVideo) { return this.request<ProcessVideoResponse>('/api/videos/process', { method: 'POST', body: video }); }
  chat(video: CurrentVideo, question: string, chatSessionId: string | null) { return this.request<ChatResponse>('/api/chat', { method: 'POST', body: { youtubeUrl: video.youtubeUrl, youtubeVideoId: video.youtubeVideoId, question, chatSessionId } }); }
  summary(youtubeVideoId: string, summaryType: 'short' | 'detailed' | 'key_points' | 'chapter_wise') { return this.request<{ summary: string }>('/api/videos/summary', { method: 'POST', body: { youtubeVideoId, summaryType } }); }
  notes(youtubeVideoId: string) { return this.request<{ title: string; content: string }>('/api/notes/generate', { method: 'POST', body: { youtubeVideoId, format: 'study_notes' } }); }
  quiz(youtubeVideoId: string, numberOfQuestions = 10, difficulty = 'medium') { return this.request<{ questions: QuizQuestion[] }>('/api/quiz/generate', { method: 'POST', body: { youtubeVideoId, numberOfQuestions, difficulty } }); }
  flashcards(youtubeVideoId: string, numberOfCards = 10) { return this.request<{ flashcards: Flashcard[] }>('/api/flashcards/generate', { method: 'POST', body: { youtubeVideoId, numberOfCards } }); }
}
