// frontend/src/app/case-studies/[id]/result/[submissionId]/page.tsx
// AI Critique & Outcome Comparison page — Your Ideas vs. What Actually Happened.
// Implementation begins in Phase 1.
import CritiqueResult from '@/components/CritiqueResult';
import { CritiqueResponse } from '@/types/case_study';

async function getCritiqueData(submissionId: string): Promise<CritiqueResponse | null> {
  try {
    // Assumes you have a GET endpoint in backend/routers/critiques.py
    const res = await fetch(`http://127.0.0.1:8000/api/v1/critiques/${submissionId}`, {
      cache: 'no-store'
    });
    if (!res.ok) return null;
    return res.json();
  } catch (error) {
    console.error("Failed to fetch critique:", error);
    return null;
  }
}

export default async function ResultPage({ params }: { params: Promise<{ id: string, submissionId: string }> }) {
  const resolvedParams = await params;
  const critique = await getCritiqueData(resolvedParams.submissionId);

  if (!critique) {
    return (
      <div className="flex h-screen items-center justify-center">
        <h1 className="text-2xl text-red-500">Critique still generating or not found.</h1>
      </div>
    );
  }

  return (
    <main className="max-w-4xl mx-auto p-6 mt-10">
      <h1 className="text-3xl font-extrabold text-white mb-8">AI Policy Critique</h1>
      <CritiqueResult critique={critique} />
    </main>
  );
}