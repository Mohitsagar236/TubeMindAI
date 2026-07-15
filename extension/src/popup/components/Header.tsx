import { ArrowLeft, BrainCircuit, Settings } from 'lucide-react';
import { Page } from '../types';

export function Header({ page, onPage }: { page: Page; onPage: (page: Page) => void }) {
  return <header className="flex h-[72px] shrink-0 items-center justify-between bg-slate-950 px-5 text-white">
    <button className="flex items-center gap-3 text-left" onClick={() => onPage('chat')} aria-label="Go to chat">
      {page !== 'chat' ? <ArrowLeft size={20}/> : <span className="grid h-10 w-10 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-lg shadow-indigo-950"><BrainCircuit size={22}/></span>}
      <span><strong className="block text-[15px] tracking-tight">TubeMind AI</strong><span className="text-[11px] text-slate-400">Chat with this video</span></span>
    </button>
    <button onClick={() => onPage('settings')} className={`rounded-xl p-2.5 transition hover:bg-white/10 ${page === 'settings' ? 'bg-white/10 text-cyan-300' : 'text-slate-300'}`} aria-label="Settings"><Settings size={19}/></button>
  </header>;
}
