import { BookOpen, Brain, Layers3, Sparkles } from 'lucide-react';
export type Action = 'summary' | 'notes' | 'quiz' | 'flashcards';
const actions = [{ id: 'summary', label: 'Summary', Icon: Sparkles }, { id: 'notes', label: 'Notes', Icon: BookOpen }, { id: 'quiz', label: 'Quiz', Icon: Brain }, { id: 'flashcards', label: 'Cards', Icon: Layers3 }] as const;
export function QuickActions({ onAction, disabled, active }: { onAction: (action: Action) => void; disabled: boolean; active?: Action | null }) {
  return <div className="grid grid-cols-4 gap-2 px-4 py-3">{actions.map(({ id, label, Icon }) => <button key={id} disabled={disabled} onClick={() => onAction(id)} className="group flex flex-col items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-1 py-2 text-[10px] font-medium text-slate-600 transition hover:-translate-y-0.5 hover:border-indigo-200 hover:text-indigo-700 disabled:opacity-50"><Icon size={16} className={active === id ? 'animate-pulse text-indigo-600' : 'text-slate-400 group-hover:text-indigo-600'}/>{label}</button>)}</div>;
}
