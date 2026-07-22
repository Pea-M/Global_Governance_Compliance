// components/SolutionForm.tsx
// Structured four-panel submission form: Own Analysis, Immediate Action, Problem Highlights, Constitution.
// Implementation begins in Phase 1.
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { SubmissionPayload } from "@/types/case_study";

export default function SolutionForm({ caseStudyId }: { caseStudyId: string }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Using simple strings for textareas, which we will split into arrays on submit
  const [formData, setFormData] = useState({
    own_analysis: "",
    immediate_action: "",
    problem_highlights: "",
    constitutional_refs: "",
    policy_reforms: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const toArray = (text: string) => text.split('\n').filter(line => line.trim() !== '');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload: SubmissionPayload = {
      case_study_id: caseStudyId,
      user_id: "c56a4180-65aa-42ec-a945-5fd21dec0538", // Hardcoded fixture user UUID
      own_analysis: formData.own_analysis,
      immediate_action: toArray(formData.immediate_action),
      problem_highlights: toArray(formData.problem_highlights),
      constitutional_refs: toArray(formData.constitutional_refs),
      policy_reforms: toArray(formData.policy_reforms),
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/submissions/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to save submission.");

      const data = await res.json();

      // Trigger critique generation before navigating to the result page
      await fetch(`http://127.0.0.1:8000/api/v1/critiques/generate/${data.submission_id}`, {
        method: "POST",
      });

      router.push(`/case-studies/${caseStudyId}/result/${data.submission_id}`);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const inputClass = "w-full bg-slate-800 border border-slate-600 rounded p-3 text-slate-200 focus:outline-none focus:border-blue-500 mb-4";

  return (
    <form onSubmit={handleSubmit} className="bg-slate-900 p-6 rounded-lg shadow-lg border border-slate-700">
      {error && <div className="bg-red-900/50 text-red-300 p-3 rounded mb-4">{error}</div>}

      <label className="block text-sm font-bold text-slate-300 mb-2">Your Analysis</label>
      <textarea name="own_analysis" rows={4} className={inputClass} onChange={handleChange} required placeholder="What is the root cause?" />

      <label className="block text-sm font-bold text-slate-300 mb-2">Immediate Actions (One per line)</label>
      <textarea name="immediate_action" rows={3} className={inputClass} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Problem Highlights (One per line)</label>
      <textarea name="problem_highlights" rows={3} className={inputClass} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Constitutional/Legal Refs (One per line)</label>
      <textarea name="constitutional_refs" rows={2} className={inputClass} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Policy Reforms (One per line)</label>
      <textarea name="policy_reforms" rows={3} className={inputClass} onChange={handleChange} required />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded transition-colors disabled:opacity-50"
      >
        {loading ? "Analyzing..." : "Submit to Critique Engine"}
      </button>
    </form>
  );
}