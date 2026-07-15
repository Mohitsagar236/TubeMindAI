import { useEffect, useRef } from 'react';
import { ChatMessage } from '../types';
import { EmptyState } from './EmptyState';
import { LoadingState } from './LoadingState';
import { MessageBubble } from './MessageBubble';
export function ChatWindow({ messages, loading, loadingLabel }: { messages: ChatMessage[]; loading: boolean; loadingLabel?: string }) { const end = useRef<HTMLDivElement>(null); useEffect(() => end.current?.scrollIntoView({ behavior: 'smooth' }), [messages, loading]); return <div className="min-h-0 flex-1 overflow-y-auto px-4 py-2">{messages.length === 0 && !loading ? <EmptyState/> : <div className="space-y-3">{messages.map(m => <MessageBubble key={m.id} message={m}/>)}{loading && <LoadingState label={loadingLabel}/>}<div ref={end}/></div>}</div>; }
