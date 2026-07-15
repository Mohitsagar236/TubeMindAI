import ReactMarkdown from 'react-markdown';
import { Bot } from 'lucide-react';
import { ChatMessage } from '../types';
import { SourceTimestamp } from './SourceTimestamp';
export function MessageBubble({ message }: { message: ChatMessage }) {
  const user = message.role === 'user';
  return <div className={`flex gap-2 ${user ? 'justify-end' : 'justify-start'}`}>{!user && <span className="grid h-7 w-7 shrink-0 place-items-center rounded-lg bg-slate-900 text-white"><Bot size={14}/></span>}<div className={`max-w-[84%] ${user ? 'rounded-2xl rounded-br-md bg-gradient-to-br from-indigo-600 to-blue-600 px-3.5 py-2.5 text-white shadow-md shadow-indigo-100' : 'rounded-2xl rounded-bl-md border border-slate-200 bg-white px-3.5 py-3 text-slate-700 shadow-sm'}`}><div className={`markdown text-[12px] leading-[19px] ${user ? 'text-white' : ''}`}><ReactMarkdown>{message.content}</ReactMarkdown></div>{!user && !!message.sources?.length && <div className="mt-2.5 border-t border-slate-100 pt-2"><p className="mb-1.5 text-[9px] font-bold uppercase tracking-wider text-slate-400">Sources</p><div className="flex flex-wrap gap-1">{message.sources.map((s, i) => <SourceTimestamp key={`${s.startTimeSeconds}-${i}`} source={s}/>)}</div></div>}</div></div>;
}
