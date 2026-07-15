import { useEffect, useMemo, useState } from 'react';
import { BackendClient } from './api/backendClient';
import { ChatInput } from './components/ChatInput';
import { ChatWindow } from './components/ChatWindow';
import { ErrorState } from './components/ErrorState';
import { Header } from './components/Header';
import { Action, QuickActions } from './components/QuickActions';
import { VideoCard } from './components/VideoCard';
import { useChromeStorage } from './hooks/useChromeStorage';
import { useCurrentTab } from './hooks/useCurrentTab';
import { useYoutubeVideo } from './hooks/useYoutubeVideo';
import { FlashcardsPage } from './pages/FlashcardsPage';
import { NotesEmpty, NotesPage } from './pages/NotesPage';
import { QuizEmpty, QuizPage } from './pages/QuizPage';
import { SettingsPage } from './pages/SettingsPage';
import { ChatMessage, Flashcard, Page, QuizQuestion, Settings, VideoStatus } from './types';
import { friendlyError, uid } from './utils/format';

const defaultSettings: Settings = { backendUrl: 'http://localhost:8000', apiKey: '' };

export default function App() {
  const { tab, loading: tabLoading } = useCurrentTab();
  const video = useYoutubeVideo(tab);
  const storedSettings = useChromeStorage<Settings>('settings', defaultSettings);
  const [page, setPage] = useState<Page>('chat');
  const [status, setStatus] = useState<VideoStatus>('not_processed');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatSessionId, setChatSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadingLabel, setLoadingLabel] = useState('Finding relevant parts...');
  const [activeAction, setActiveAction] = useState<Action | null>(null);
  const [error, setError] = useState('');
  const [notes, setNotes] = useState({ title: '', content: '' });
  const [quiz, setQuiz] = useState<QuizQuestion[]>([]);
  const [cards, setCards] = useState<Flashcard[]>([]);
  const client = useMemo(() => new BackendClient(storedSettings.value), [storedSettings.value]);

  useEffect(() => {
    if (!video) return;
    const key = `chat:${video.youtubeVideoId}`;
    chrome.storage.local.get(key).then(result => {
      const state = result[key] as { messages?: ChatMessage[]; chatSessionId?: string } | undefined;
      setMessages(state?.messages ?? []); setChatSessionId(state?.chatSessionId ?? null);
    });
  }, [video?.youtubeVideoId]);

  useEffect(() => {
    if (!video || !storedSettings.ready) return;
    let cancelled = false;
    setStatus('processing'); setError('');
    client.processVideo(video).then(result => { if (!cancelled) setStatus(result.indexedStatus === 'completed' ? 'ready' : result.indexedStatus === 'failed' ? 'failed' : 'processing'); }).catch(err => { if (!cancelled) { setStatus('failed'); setError(friendlyError(err)); } });
    return () => { cancelled = true; };
  }, [video?.youtubeVideoId, storedSettings.ready, client]);

  const persistChat = (next: ChatMessage[], session = chatSessionId) => {
    setMessages(next);
    if (video) void chrome.storage.local.set({ [`chat:${video.youtubeVideoId}`]: { messages: next, chatSessionId: session } });
  };
  const assistantMessage = (content: string): ChatMessage => ({ id: uid(), role: 'assistant', content, createdAt: new Date().toISOString() });

  const send = async (question: string) => {
    if (!video || loading) return;
    const next = [...messages, { id: uid(), role: 'user' as const, content: question, createdAt: new Date().toISOString() }];
    persistChat(next); setLoading(true); setLoadingLabel('Finding relevant parts...'); setError('');
    try { const response = await client.chat(video, question, chatSessionId); setChatSessionId(response.chatSessionId); persistChat([...next, { ...assistantMessage(response.answer), sources: response.sources }], response.chatSessionId); setStatus('ready'); }
    catch (err) { setError(friendlyError(err)); }
    finally { setLoading(false); }
  };

  const runAction = async (action: Action) => {
    if (!video || loading) return;
    setLoading(true); setActiveAction(action); setError('');
    const labels: Record<Action, string> = { summary: 'Creating a clear summary...', notes: 'Creating study notes...', quiz: 'Building your quiz...', flashcards: 'Making flashcards...' };
    setLoadingLabel(labels[action]);
    try {
      if (action === 'summary') { const result = await client.summary(video.youtubeVideoId, 'short'); const next = [...messages, assistantMessage(`## Video summary\n\n${result.summary}`)]; persistChat(next); }
      if (action === 'notes') { const result = await client.notes(video.youtubeVideoId); setNotes(result); setPage('notes'); }
      if (action === 'quiz') { const result = await client.quiz(video.youtubeVideoId); setQuiz(result.questions); setPage('quiz'); }
      if (action === 'flashcards') { const result = await client.flashcards(video.youtubeVideoId); setCards(result.flashcards); setPage('flashcards'); }
    } catch (err) { setError(friendlyError(err)); }
    finally { setLoading(false); setActiveAction(null); }
  };

  let content;
  if (page === 'settings') content = <SettingsPage settings={storedSettings.value} onSave={storedSettings.save}/>;
  else if (page === 'notes') content = notes.content ? <NotesPage {...notes}/> : <NotesEmpty/>;
  else if (page === 'quiz') content = quiz.length ? <QuizPage questions={quiz}/> : <QuizEmpty/>;
  else if (page === 'flashcards') content = <FlashcardsPage cards={cards}/>;
  else if (tabLoading) content = <div className="flex flex-1 items-center justify-center text-xs text-slate-500">Detecting current video…</div>;
  else if (!video) content = <div className="flex flex-1 flex-col items-center justify-center px-10 text-center"><span className="text-4xl">▶️</span><h1 className="mt-4 text-base font-bold text-slate-900">Open a YouTube video</h1><p className="mt-2 text-xs leading-5 text-slate-500">Navigate to a YouTube watch page, then reopen TubeMind AI to start chatting.</p></div>;
  else content = <><VideoCard video={video} status={status}/><QuickActions onAction={runAction} disabled={loading || status !== 'ready'} active={activeAction}/>{error && <ErrorState message={error}/>}<ChatWindow messages={messages} loading={loading} loadingLabel={loadingLabel}/><ChatInput onSend={send} disabled={loading || status !== 'ready'}/></>;

  return <div className="flex h-[620px] w-[420px] flex-col overflow-hidden bg-slate-50"><Header page={page} onPage={setPage}/>{content}</div>;
}
