// frontend/src/app/case-studies/[id]/page.tsx
import CaseStudyHeader from '@/components/CaseStudyHeader';
import Timeline from '@/components/Timeline';
import LegalReferencePanel from '@/components/LegalReferencePanel';
import { CaseStudyResponse } from '@/types/case_study';
import Link from 'next/link';

async function getCaseStudy(id: string): Promise<CaseStudyResponse | null> {
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/case-studies/${id}`, {
            cache: 'no-store',
        });
        if (!res.ok) return null;
        return res.json();
    } catch (error) {
        console.error("Failed to fetch case study:", error);
        return null;
    }
}

export default async function CaseStudyPage({ params }: { params: Promise<{ id: string }> }) {
    const resolvedParams = await params;
    const data = await getCaseStudy(resolvedParams.id);

    if (!data) {
        return (
            <div className="flex h-screen items-center justify-center">
                <h1 className="text-2xl text-red-500">Case study not found.</h1>
            </div>
        );
    }

    return (
        <main className="max-w-4xl mx-auto p-6 mt-10 space-y-6">
            <CaseStudyHeader caseStudy={data.case_study} outcome={data.historical_outcome} />
            <Timeline events={data.timeline_events} />
            <LegalReferencePanel legalReferences={data.legal_references} />
            <Link
                href={`/case-studies/${resolvedParams.id}/submit`}
                className="block text-center bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded transition-colors"
            >
                Propose Your Solution
            </Link>
        </main>
    );
}