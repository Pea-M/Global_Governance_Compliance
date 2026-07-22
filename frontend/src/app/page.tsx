// Root page: two-panel layout — left AnomalyFeed, right PolicyOracle compliance report
// frontend/src/app/page.tsx
export default function HomePage() {
    return (
        <main className="max-w-4xl mx-auto p-6 mt-10 text-white">
            <h1 className="text-3xl font-bold">Governance & Disaster Case-Study Simulator</h1>
            <p className="text-slate-400 mt-2">
                Homepage tabloid coming in Phase 5. For now, visit a case study directly, e.g.:
            </p>

            <a
                href="/case-studies/ed36fca2-8df2-482a-8756-ef2039ba39a1"
                className="text-blue-400 underline mt-4 inline-block"
            >
                View the Noida Labor Protest case study
            </a>
        </main>
    );
}