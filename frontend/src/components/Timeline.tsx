// components/Timeline.tsx
// Chronological timeline-of-unfolding widget with actor labels and parallel data track.
// Implementation begins in Phase 1.
import { TimelineEvent } from '@/types/case_study';

interface Props {
  events: TimelineEvent[];
}

export default function Timeline({ events }: Props) {
  if (!events || events.length === 0) return null;

  return (
    <section className="bg-slate-900 border border-slate-700 rounded-lg p-8 shadow-lg mt-8">
      <h2 className="text-2xl font-bold text-white mb-6">Event Timeline</h2>
      <div className="border-l-2 border-slate-600 pl-6 space-y-8">
        {events.map((event) => (
          <div key={event.id} className="relative">
            <div className="absolute w-3 h-3 bg-blue-500 rounded-full -left-[1.65rem] top-1.5"></div>
            
            <span className="text-sm text-blue-400 font-mono">
              {new Date(event.event_timestamp).toLocaleString()}
            </span>
            <h3 className="text-lg font-bold text-slate-200 mt-1">
              Actor: {event.responsible_actor}
            </h3>
            <p className="text-slate-400 mt-2">{event.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}