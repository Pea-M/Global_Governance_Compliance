// components/CritiqueResult.tsx
import { CritiqueResponse } from "@/types/case_study";

interface Props {
  critique: CritiqueResponse;
}

export default function CritiqueResult({ critique }: Props) {
  const { pros, cons, additions, deletions } = critique.pros_cons_additions_deletions;

  return (
    <div className="space-y-6">
      <div className="bg-slate-900 border border-slate-700 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-3">Your Proposal, Summarized</h3>
        <p className="text-slate-300">{critique.summary_of_user_idea}</p>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-3">Likely Consequences</h3>
        <p className="text-slate-300">{critique.future_prediction}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-green-900/20 border border-green-800 rounded-lg p-6">
          <h4 className="font-bold text-green-400 mb-4">Pros</h4>
          <ul className="list-disc list-inside text-slate-300 space-y-2">
            {pros.map((p, i) => <li key={i}>{p}</li>)}
          </ul>
        </div>
        <div className="bg-red-900/20 border border-red-800 rounded-lg p-6">
          <h4 className="font-bold text-red-400 mb-4">Cons</h4>
          <ul className="list-disc list-inside text-slate-300 space-y-2">
            {cons.map((c, i) => <li key={i}>{c}</li>)}
          </ul>
        </div>
        <div className="bg-blue-900/20 border border-blue-800 rounded-lg p-6">
          <h4 className="font-bold text-blue-400 mb-4">Suggested Additions</h4>
          <ul className="list-disc list-inside text-slate-300 space-y-2">
            {additions.map((a, i) => <li key={i}>{a}</li>)}
          </ul>
        </div>
        <div className="bg-yellow-900/20 border border-yellow-800 rounded-lg p-6">
          <h4 className="font-bold text-yellow-400 mb-4">Reconsider / Cut</h4>
          <ul className="list-disc list-inside text-slate-300 space-y-2">
            {deletions.map((d, i) => <li key={i}>{d}</li>)}
          </ul>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-700 rounded-lg p-6">
        <h3 className="text-xl font-bold text-white mb-3">Against What Actually Happened</h3>
        {critique.reality_comparison ? (
          <p className="text-slate-300">{critique.reality_comparison}</p>
        ) : (
          <p className="text-slate-500 italic">
            This case is still developing — there's no documented real-world outcome yet to
            compare your plan against. Check back once it's resolved.
          </p>
        )}
      </div>
    </div>
  );
}