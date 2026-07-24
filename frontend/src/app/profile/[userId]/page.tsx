// frontend/src/app/profile/[userId]/page.tsx
"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/AuthProvider";
import Link from "next/link";

interface Draft {
    id: string;
    case_study_id: string;
    form_data: Record<string, string>;
    updated_at: string;
}

export default function ProfilePage() {
    const { session, user } = useAuth();
    const [drafts, setDrafts] = useState<Draft[]>([]);
    const [submissions, setSubmissions] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!session?.access_token) return;
        fetch("http://127.0.0.1:8000/api/v1/drafts/", {
            headers: { Authorization: `Bearer ${session.access_token}` },
        })
            .then((res) => res.json())
            .then((data) => setDrafts(data.drafts || []))
            .catch(() => { });

        fetch("http://127.0.0.1:8000/api/v1/submissions/mine", {
            headers: { Authorization: `Bearer ${session.access_token}` },
        })
            .then((res) => res.json())
            .then((data) => setSubmissions(data.submissions || []))
            .catch(() => { })
            .finally(() => setLoading(false));
    }, [session]);

    return (
        <main className="max-w-3xl mx-auto p-6 mt-10 text-white">
            <h1 className="text-2xl font-bold mb-6">Your Drafts</h1>
            {loading ? (
                <p className="text-slate-400">Loading…</p>
            ) : drafts.length === 0 ? (
                <p className="text-slate-400">No saved drafts yet.</p>
            ) : (
                <ul className="space-y-3">
                    {drafts.map((d) => (
                        <li key={d.id} className="bg-slate-900 border border-slate-700 rounded p-4">
                            <p className="text-sm text-slate-400">
                                Last updated: {new Date(d.updated_at).toLocaleString()}
                            </p>
                            <p className="text-slate-200 mt-1 line-clamp-2">
                                {d.form_data?.own_analysis || "(empty analysis)"}
                            </p>
                            <Link
                                href={`/case-studies/${d.case_study_id}/submit`}
                                className="text-blue-400 underline text-sm mt-2 inline-block"
                            >
                                Resume this draft →
                            </Link>
                        </li>
                    ))}
                </ul>
            )}

            <h2 className="text-xl font-bold mt-10 mb-4">Your Submissions</h2>
            {submissions.length === 0 ? (
                <p className="text-slate-400">No submissions yet.</p>
            ) : (
                <ul className="space-y-3">
                    {submissions.map((s) => (
                        <li key={s.id} className="bg-slate-900 border border-slate-700 rounded p-4">
                            <p className="text-sm text-slate-400">{new Date(s.created_at).toLocaleString()}</p>
                            <p className="text-slate-200 mt-1 line-clamp-2">{s.own_analysis}</p>
                            <Link
                                href={`/case-studies/${s.case_study_id}/result/${s.id}`}
                                className="text-blue-400 underline text-sm mt-2 inline-block"
                            >
                                View critique →
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </main>
    );
}
