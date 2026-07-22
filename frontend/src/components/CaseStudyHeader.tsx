// components/CaseStudyHeader.tsx
// Renders the case study header block: event name, date, location, deaths, affected, cause, region.
// Implementation begins in Phase 1.
// frontend/src/components/CaseStudyHeader.tsx
import { CaseStudy, HistoricalOutcome } from '@/types/case_study';

interface Props {
  caseStudy: CaseStudy;
  outcome: HistoricalOutcome | null;
}

export default function CaseStudyHeader({ caseStudy, outcome }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-8 shadow-lg">
      <div className="flex justify-between items-start mb-4">
        <h1 className="text-4xl font-extrabold text-white">{caseStudy.title}</h1>
        <span className="px-3 py-1 text-sm font-semibold rounded-full bg-blue-900 text-blue-200 uppercase tracking-wide">
          {caseStudy.category}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-slate-300 mb-6">
        <p><strong>Date:</strong> {new Date(caseStudy.event_date).toLocaleDateString()}</p>
        <p><strong>Location:</strong> {caseStudy.location}</p>
        <p><strong>Status:</strong> {caseStudy.status}</p>
        <p><strong>Affected:</strong> {caseStudy.affected} individuals</p>
      </div>
      
      <div className="bg-slate-800 p-4 rounded text-slate-200">
        <h3 className="font-bold text-lg mb-2">Root Cause</h3>
        <p>{caseStudy.cause}</p>
      </div>

      {outcome && (
        <div className="mt-6 border-t border-slate-700 pt-6">
          <h3 className="font-bold text-green-400 mb-2">Final Reforms Achieved:</h3>
          <ul className="list-disc list-inside text-slate-300">
            {outcome.final_reforms.map((reform, idx) => (
              <li key={idx}>{reform}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}