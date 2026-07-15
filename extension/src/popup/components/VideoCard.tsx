import { CheckCircle2, Circle, LoaderCircle, Youtube } from 'lucide-react';
import { CurrentVideo, VideoStatus } from '../types';

const statusView = { not_processed: ['Not processed', 'bg-slate-100 text-slate-600', Circle], processing: ['Processing', 'bg-amber-50 text-amber-700', LoaderCircle], ready: ['Ready', 'bg-emerald-50 text-emerald-700', CheckCircle2], failed: ['Failed', 'bg-red-50 text-red-700', Circle] } as const;
export function VideoCard({ video, status }: { video: CurrentVideo; status: VideoStatus }) {
  const [label, classes, Icon] = statusView[status];
  return <section className="mx-4 mt-4 flex gap-3 rounded-2xl border border-slate-200 bg-white p-3 shadow-soft">
    <div className="relative h-[66px] w-[108px] shrink-0 overflow-hidden rounded-xl bg-slate-100"><img src={video.thumbnailUrl} alt="Video thumbnail" className="h-full w-full object-cover"/><Youtube className="absolute bottom-1 right-1 rounded bg-red-600 p-0.5 text-white" size={18}/></div>
    <div className="min-w-0 flex-1"><p className="line-clamp-2 text-[13px] font-semibold leading-[18px] text-slate-900">{video.title}</p><p className="mt-1 truncate font-mono text-[9px] text-slate-400">{video.youtubeVideoId}</p><span className={`mt-1 inline-flex items-center gap-1 rounded-full px-2 py-1 text-[10px] font-semibold ${classes}`}><Icon size={11} className={status === 'processing' ? 'animate-spin' : ''}/>{label}</span></div>
  </section>;
}
