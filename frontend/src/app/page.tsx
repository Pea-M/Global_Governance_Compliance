// Root page: two-panel layout — left AnomalyFeed, right PolicyOracle compliance report
// frontend/src/app/page.tsx
export default function HomePage() {
    return (
        <main className="max-w-4xl mx-auto p-6 mt-10 text-white">
            <h1 className="text-3xl font-bold">Governance & Disaster Case-Study Simulator</h1>
            <p className="text-slate-400 mt-2">
                Homepage tabloid coming in Phase 5. For now, visit a case study directly, e.g.:
            </p>

            <div className="flex flex-col gap-2 mt-4">
                <a
                    href="/case-studies/ed36fca2-8df2-482a-8756-ef2039ba39a1"
                    className="text-blue-400 underline inline-block"
                >
                    View the Noida Labor Protest case study
                </a>
                <a
                    href="/case-studies/f47ac10b-58cc-4372-a567-0e02b2c3d479"
                    className="text-blue-400 underline inline-block"
                >
                    View the Chernobyl case study
                </a>
            </div>

            <div className="mt-12 p-6 bg-slate-900 rounded-lg border border-slate-800">
                <h2 className="text-xl font-bold mb-2">My Profile & Drafts</h2>
                <p className="text-slate-400 text-sm mb-4">View your saved drafts and previous submissions.</p>
                <a
                    href="/profile"
                    className="inline-block bg-slate-800 hover:bg-slate-700 text-white font-semibold py-2 px-4 border border-slate-700 rounded transition-colors"
                >
                    Go to My Profile
                </a>
            </div>
        </main>
    );
}