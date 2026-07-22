// components/LegalReferencePanel.tsx
// Displays the applicable laws, constitutional articles, treaties, and policies for a case study.
// Implementation begins in Phase 1.
// components/LegalReferencePanel.tsx
import { LegalReference } from "@/types/case_study";

interface Props {
  legalReferences: LegalReference[];
}

export default function LegalReferencePanel({ legalReferences }: Props) {
  if (!legalReferences || legalReferences.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 text-slate-400 text-sm">
        No legal or jurisdictional references recorded for this case study.
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-6">
      <h3 className="text-lg font-bold text-white mb-4">Legal & Jurisdictional Framework</h3>
      <p className="text-slate-400 text-xs mb-4">
        The laws, articles, and treaties actually in force at the time — this is the ceiling
        any proposed response was bound by.
      </p>
      <ul className="space-y-3">
        {legalReferences.map((ref) => (
          <li key={ref.id} className="border-l-2 border-blue-700 pl-3">
            <span className="text-xs uppercase tracking-wide text-blue-400">{ref.ref_type}</span>
            <p className="font-semibold text-slate-200">{ref.title}</p>
            {ref.description && <p className="text-sm text-slate-400 mt-1">{ref.description}</p>}
          </li>
        ))}
      </ul>
    </div>
  );
}