import SolutionForm from '@/components/SolutionForm';

export default async function SubmitPage({ params }: { params: Promise<{ id: string }> }) {
    const resolvedParams = await params;

    return (
        <main className="max-w-3xl mx-auto p-6 mt-10 space-y-6">
            <h1 className="text-3xl font-extrabold text-white">Submit Policy Analysis</h1>
            <p className="text-slate-400">
                Draft your immediate actions and long-term policy reforms for this case study.
            </p>

            <SolutionForm caseStudyId={resolvedParams.id} />
        </main>
    );
}
