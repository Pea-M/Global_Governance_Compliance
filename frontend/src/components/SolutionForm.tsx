"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { SubmissionPayload } from "@/types/case_study";
import { supabase } from "@/lib/supabase";
import { useAuth } from "@/components/AuthProvider";

const API = "http://127.0.0.1:8000";

export default function SolutionForm({ caseStudyId }: { caseStudyId: string }) {
  const router = useRouter();
  const { session } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [draftSaving, setDraftSaving] = useState(false);
  const [draftStatus, setDraftStatus] = useState<"idle" | "saving" | "saved">("idle");
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const [formData, setFormData] = useState({
    own_analysis: "",
    immediate_action: "",
    problem_highlights: "",
    constitutional_refs: "",
    policy_reforms: "",
  });

  // ------------------------------------------------------------------
  // Helper: get the current user's JWT for authenticated API calls
  // ------------------------------------------------------------------
  const getAuthHeader = async (): Promise<HeadersInit> => {
    const { data } = await supabase.auth.getSession();
    const token = data.session?.access_token;
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  // ------------------------------------------------------------------
  // Restore draft from local storage & backend on mount
  // ------------------------------------------------------------------
  useEffect(() => {
    const loadDraft = async () => {
      // 1. Instantly load from localStorage (bulletproof against unmount drops)
      const local = localStorage.getItem(`draft_${caseStudyId}`);
      if (local) {
        try {
          const parsed = JSON.parse(local);
          if (parsed && typeof parsed === "object") {
            setFormData(parsed);
          }
        } catch (e) { }
      }

      try {
        const { data: sessionData } = await supabase.auth.getSession();
        const token = sessionData.session?.access_token;
        const headers = token ? { Authorization: `Bearer ${token}` } : {};
        const res = await fetch(`${API}/api/v1/drafts/${caseStudyId}`, { headers });
        if (!res.ok) return;
        const { draft } = await res.json();

        // Only override if we don't have local data, or if the user wants to resume other device's draft
        if (draft?.form_data && !local) {
          setFormData(draft.form_data);
          localStorage.setItem(`draft_${caseStudyId}`, JSON.stringify(draft.form_data));
        }
      } catch {
        // Can't load backend draft — not a critical failure
      }
    };
    loadDraft();
  }, [caseStudyId]);

  const latestFormData = useRef(formData);
  const latestToken = useRef(session?.access_token);
  const latestDraftStatus = useRef(draftStatus);

  useEffect(() => {
    latestFormData.current = formData;
    // Keep localStorage perfectly synced on every single change
    localStorage.setItem(`draft_${caseStudyId}`, JSON.stringify(formData));
  }, [formData, caseStudyId]);

  useEffect(() => {
    latestToken.current = session?.access_token;
  }, [session?.access_token]);

  useEffect(() => {
    latestDraftStatus.current = draftStatus;
  }, [draftStatus]);

  // Handle immediate save on unmount if it was in the middle of typing
  useEffect(() => {
    return () => {
      if (latestDraftStatus.current === "idle" && !Object.values(latestFormData.current).every((v) => v.trim() === "")) {
        // Fire and forget a fetch keepalive
        const token = latestToken.current;
        if (token) {
          const dataStr = JSON.stringify({ case_study_id: caseStudyId, form_data: latestFormData.current });
          fetch(`${API}/api/v1/drafts/`, {
            method: "POST",
            headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
            body: dataStr,
            keepalive: true
          }).catch(() => { });
        }
      }
    };
  }, [caseStudyId]);

  // ------------------------------------------------------------------
  // Autosave draft on every form change (debounced 2s)
  // ------------------------------------------------------------------
  const saveDraft = useCallback(
    async (data: typeof formData) => {
      if (Object.values(data).every((v) => v.trim() === "")) return;
      setDraftSaving(true);
      setDraftStatus("saving");
      try {
        const headers = await getAuthHeader();
        const res = await fetch(`${API}/api/v1/drafts/`, {
          method: "POST",
          headers: { "Content-Type": "application/json", ...headers },
          body: JSON.stringify({ case_study_id: caseStudyId, form_data: data }),
        });
        if (!res.ok) {
          const errBody = await res.text();
          console.error("Draft save failed:", res.status, errBody);
          throw new Error("Draft save failed");
        }
        setDraftStatus("saved");
      } catch {
        setDraftStatus("idle");
      } finally {
        setDraftSaving(false);
      }
    },
    [caseStudyId]
  );

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      if (draftStatus === "idle") saveDraft(formData);
    }, 2000);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [formData, saveDraft, draftStatus]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDraftStatus("idle");
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const toArray = (text: string) => text.split("\n").filter((line) => line.trim() !== "");

  // ------------------------------------------------------------------
  // Submit
  // ------------------------------------------------------------------
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const { data: sessionData } = await supabase.auth.getSession();
      const token = sessionData.session?.access_token;
      const userId = sessionData.session?.user?.id;

      if (!token || !userId) {
        throw new Error("You must be signed in to submit.");
      }

      const authHeader = { Authorization: `Bearer ${token}` };

      const payload: SubmissionPayload = {
        case_study_id: caseStudyId,
        user_id: userId,
        own_analysis: formData.own_analysis,
        immediate_action: toArray(formData.immediate_action),
        problem_highlights: toArray(formData.problem_highlights),
        constitutional_refs: toArray(formData.constitutional_refs),
        policy_reforms: toArray(formData.policy_reforms),
      };

      const res = await fetch(`${API}/api/v1/submissions/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeader },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Failed to save submission.");
      const data = await res.json();

      const critiqueRes = await fetch(
        `${API}/api/v1/critiques/generate/${data.submission_id}`,
        { method: "POST", headers: authHeader }
      );

      if (!critiqueRes.ok)
        throw new Error("Critique generation failed. The server might be experiencing issues.");

      // Clear draft on full success
      await fetch(`${API}/api/v1/drafts/${caseStudyId}`, {
        method: "DELETE",
        headers: authHeader,
      });
      localStorage.removeItem(`draft_${caseStudyId}`);

      router.push(`/case-studies/${caseStudyId}/result/${data.submission_id}`);
    } catch (err: any) {
      setError(err.message);
      // Draft is still saved on backend — safe to retry
    } finally {
      setLoading(false);
    }
  };

  const manuallySave = () => {
    saveDraft(formData);
  };

  const inputClass =
    "w-full bg-slate-800 border border-slate-600 rounded p-3 text-slate-200 focus:outline-none focus:border-blue-500 mb-4";

  return (
    <form onSubmit={handleSubmit} className="bg-slate-900 p-6 rounded-lg shadow-lg border border-slate-700">
      {/* Draft status indicator */}
      <div className="flex items-center justify-between mb-4 h-8">
        <h3 className="text-lg font-bold text-white">Solution Form</h3>
        <div className="flex items-center gap-3">
          {draftStatus === "saving" && (
            <span className="text-xs text-slate-500 animate-pulse">Saving draft…</span>
          )}
          {draftStatus === "saved" && (
            <span className="text-xs text-green-500">✓ Draft saved</span>
          )}
          <button
            type="button"
            onClick={manuallySave}
            disabled={draftSaving}
            className="text-xs bg-slate-800 border border-slate-600 hover:bg-slate-700 text-slate-300 py-1 px-3 rounded transition-colors disabled:opacity-50"
          >
            Save Draft
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-900/50 text-red-300 p-3 rounded mb-4">
          {error} — your draft is safe, you can retry.
        </div>
      )}

      <label className="block text-sm font-bold text-slate-300 mb-2">Your Analysis</label>
      <textarea name="own_analysis" rows={4} className={inputClass} value={formData.own_analysis} onChange={handleChange} required placeholder="What is the root cause?" />

      <label className="block text-sm font-bold text-slate-300 mb-2">Immediate Actions (One per line)</label>
      <textarea name="immediate_action" rows={3} className={inputClass} value={formData.immediate_action} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Problem Highlights (One per line)</label>
      <textarea name="problem_highlights" rows={3} className={inputClass} value={formData.problem_highlights} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Constitutional/Legal Refs (One per line)</label>
      <textarea name="constitutional_refs" rows={2} className={inputClass} value={formData.constitutional_refs} onChange={handleChange} required />

      <label className="block text-sm font-bold text-slate-300 mb-2">Policy Reforms (One per line)</label>
      <textarea name="policy_reforms" rows={3} className={inputClass} value={formData.policy_reforms} onChange={handleChange} required />

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded transition-colors disabled:opacity-50"
      >
        {loading ? "Analyzing…" : "Submit to Critique Engine"}
      </button>
    </form>
  );
}