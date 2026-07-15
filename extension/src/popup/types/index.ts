export type VideoStatus = 'not_processed' | 'processing' | 'ready' | 'failed';
export type Page = 'chat' | 'notes' | 'quiz' | 'flashcards' | 'settings';
export interface CurrentVideo { youtubeVideoId: string; youtubeUrl: string; title?: string; thumbnailUrl?: string }
export interface SourceTimestamp { text: string; startTimeSeconds: number; endTimeSeconds: number; startTimeLabel: string; endTimeLabel: string; youtubeUrl: string }
export interface ChatMessage { id: string; role: 'user' | 'assistant'; content: string; sources?: SourceTimestamp[]; createdAt: string }
export interface ChatResponse { chatSessionId: string; answer: string; sources: SourceTimestamp[] }
export interface ProcessVideoResponse { videoId: string; youtubeVideoId: string; indexedStatus: string; transcriptStatus: string }
export interface QuizQuestion { question: string; options: string[]; correctAnswer: string; explanation: string }
export interface Flashcard { front: string; back: string }
export interface Settings { backendUrl: string; apiKey: string }
