import { Clock3 } from 'lucide-react';
import { SourceTimestamp as Source } from '../types';
export function SourceTimestamp({ source }: { source: Source }) { return <button title={source.text} onClick={() => void chrome.runtime.sendMessage({ type: 'OPEN_TIMESTAMP', url: source.youtubeUrl })} className="inline-flex items-center gap-1 rounded-full border border-indigo-100 bg-indigo-50 px-2 py-1 text-[10px] font-semibold text-indigo-700 hover:bg-indigo-100"><Clock3 size={10}/>{source.startTimeLabel}{source.endTimeLabel ? `–${source.endTimeLabel}` : ''}</button>; }
