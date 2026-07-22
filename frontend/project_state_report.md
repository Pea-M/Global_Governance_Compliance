# Project State Report

### 1. File Tree of frontend/src
```text
c:\DACSS\frontend\src\app\ (DIR)
c:\DACSS\frontend\src\app\case-studies\ (DIR)
c:\DACSS\frontend\src\app\case-studies\[id]\ (DIR)
c:\DACSS\frontend\src\app\case-studies\[id]\page.tsx (1968 bytes)
c:\DACSS\frontend\src\app\case-studies\[id]\result\ (DIR)
c:\DACSS\frontend\src\app\case-studies\[id]\result\[submissionId]\ (DIR)
c:\DACSS\frontend\src\app\case-studies\[id]\result\[submissionId]\page.tsx (1375 bytes)
c:\DACSS\frontend\src\app\case-studies\[id]\submit\ (DIR)
c:\DACSS\frontend\src\app\case-studies\[id]\submit\page.tsx (549 bytes)
c:\DACSS\frontend\src\app\globals.css (60 bytes)
c:\DACSS\frontend\src\app\layout.tsx (544 bytes)
c:\DACSS\frontend\src\app\page.tsx (780 bytes)
c:\DACSS\frontend\src\app\profile\ (DIR)
c:\DACSS\frontend\src\app\profile\[userId]\ (DIR)
c:\DACSS\frontend\src\app\profile\[userId]\page.tsx (159 bytes)
c:\DACSS\frontend\src\components\ (DIR)
c:\DACSS\frontend\src\components\AnomalyFeed.tsx (94 bytes)
c:\DACSS\frontend\src\components\CaseStudyHeader.tsx (1869 bytes)
c:\DACSS\frontend\src\components\Chatbot.tsx (144 bytes)
c:\DACSS\frontend\src\components\CritiqueResult.tsx (2794 bytes)
c:\DACSS\frontend\src\components\HomepageCustomizer.tsx (155 bytes)
c:\DACSS\frontend\src\components\LegalReferencePanel.tsx (1555 bytes)
c:\DACSS\frontend\src\components\PolicyOracle.tsx (107 bytes)
c:\DACSS\frontend\src\components\SolutionForm.tsx (4216 bytes)
c:\DACSS\frontend\src\components\Timeline.tsx (1254 bytes)
c:\DACSS\frontend\src\components\TriviaWidget.tsx (123 bytes)
c:\DACSS\frontend\src\lib\ (DIR)
c:\DACSS\frontend\src\lib\supabase.ts (267 bytes)
c:\DACSS\frontend\src\types\ (DIR)
c:\DACSS\frontend\src\types\case_study.ts (1669 bytes)
```

### 2. File Contents

#### FILE: c:\DACSS\frontend\src\app\layout.tsx
```tsx
// frontend/src/app/layout.tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Governance & Disaster Case-Study Simulator",
    description: "Analyze real crises, propose your response, get critiqued against reality.",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className="bg-slate-950 text-white min-h-screen">{children}</body>
        </html>
    );
}
```

#### FILE: c:\DACSS\frontend\src\app\page.tsx
```tsx
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
```

#### FILE: c:\DACSS\frontend\src\app\globals.css
```tsx
@tailwind base;
@tailwind components;
@tailwind utilities;
```

#### FILE: c:\DACSS\frontend\tailwind.config.js
```tsx
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: { extend: {} },
  plugins: [],
};
```

#### FILE: c:\DACSS\frontend\tsconfig.json
```tsx
{
  "compilerOptions": {
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": false,
    "noEmit": true,
    "incremental": true,
    "module": "esnext",
    "esModuleInterop": true,
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": [
        "./src/*"
      ]
    }
  },
  "include": [
    "next-env.d.ts",
    ".next/types/**/*.ts",
    "**/*.ts",
    "**/*.tsx"
  ],
  "exclude": [
    "node_modules"
  ]
}
```

#### FILE: c:\DACSS\frontend\next.config.js
(File does not exist)

#### FILE: c:\DACSS\frontend\next.config.mjs
(File does not exist)

#### FILE: c:\DACSS\frontend\next.config.ts
(File does not exist)

#### FILE: c:\DACSS\frontend\src\app\case-studies\[id]\page.tsx
```tsx
// frontend/src/app/case-studies/[id]/page.tsx
// HMR trigger
// import CaseStudyHeader from '@/components/CaseStudyHeader';
// import Timeline from '@/components/Timeline';
// import LegalReferencePanel from '@/components/LegalReferencePanel';
// import { CaseStudyResponse } from '@/types/case_study';
// import Link from 'next/link';

// async function getCaseStudy(id: string): Promise<CaseStudyResponse | null> {
//     try {
//         const res = await fetch(`http://127.0.0.1:8000/api/v1/case-studies/${id}`, {
//             cache: 'no-store',
//         });
//         if (!res.ok) return null;
//         return res.json();
//     } catch (error) {
//         console.error("Failed to fetch case study:", error);
//         return null;
//     }
// }

// export default async function CaseStudyPage({ params }: { params: { id: string } }) {
//     const data = await getCaseStudy(params.id);

//     if (!data) {
//         return (
//             <div className="flex h-screen items-center justify-center">
//                 <h1 className="text-2xl text-red-500">Case study not found.</h1>
//             </div>
//         );
//     }

//     return (
//         <main className="max-w-4xl mx-auto p-6 mt-10 space-y-6">
//             <CaseStudyHeader caseStudy={data.case_study} outcome={data.historical_outcome} />
//             <Timeline events={data.timeline_events} />
//             <LegalReferencePanel legalReferences={data.legal_references} />
//             <Link
//                 href={`/case-studies/${params.id}/submit`}
//                 className="block text-center bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-4 rounded transition-colors"
//             >
//                 Propose Your Solution
//             </Link>
//         </main>
//     );
// }
// frontend/src/app/case-studies/[id]/page.tsx
export default function CaseStudyPage() {
    return <div>Test</div>;
}
```

#### FILE: c:\DACSS\frontend\src\app\case-studies\[id]\submit\page.tsx
```tsx
import SolutionForm from '@/components/SolutionForm';

export default function SubmitPage({ params }: { params: { id: string } }) {
    return (
        <main className="max-w-3xl mx-auto p-6 mt-10 space-y-6">
            <h1 className="text-3xl font-extrabold text-white">Submit Policy Analysis</h1>
            <p className="text-slate-400">
                Draft your immediate actions and long-term policy reforms for this case study.
            </p>

            <SolutionForm caseStudyId={params.id} />
        </main>
    );
}

```

#### FILE: c:\DACSS\frontend\src\app\case-studies\[id]\result\[submissionId]\page.tsx
```tsx
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

export default async function ResultPage({ params }: { params: { id: string, submissionId: string } }) {
  const critique = await getCritiqueData(params.submissionId);

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
```

#### FILE: c:\DACSS\frontend\src\app\profile\[userId]\layout.tsx
(File does not exist)

#### FILE: c:\DACSS\frontend\src\app\profile\[userId]\page.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// frontend/src/app/profile/[userId]/page.tsx
// Phase 4 — User profile page: display name, bio, submissions, notes.
// Implementation begins in Phase 4.

```

#### FILE: c:\DACSS\frontend\src\components\AnomalyFeed.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// AnomalyFeed: displays blocked apps and top 3 news headlines for the current anomaly event

```

#### FILE: c:\DACSS\frontend\src\components\CaseStudyHeader.tsx
```tsx
// components/CaseStudyHeader.tsx
// Renders the case study header block: event name, date, location, deaths, affected, cause, region.
// Implementation begins in Phase 1.
// frontend/src/components/CaseStudyHeader.tsx
import { CaseStudy, HistoricalOutcome } from '@/types/case_study';

interface Props {
  caseStudy: CaseStudy;
  outcome: HistoricalOutcome | null;
}

export default function CaseStudyHeader({ caseStudy, outcome }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg p-8 shadow-lg">
      <div className="flex justify-between items-start mb-4">
        <h1 className="text-4xl font-extrabold text-white">{caseStudy.title}</h1>
        <span className="px-3 py-1 text-sm font-semibold rounded-full bg-blue-900 text-blue-200 uppercase tracking-wide">
          {caseStudy.category}
        </span>
      </div>
      
      <div className="grid grid-cols-2 gap-4 text-slate-300 mb-6">
        <p><strong>Date:</strong> {new Date(caseStudy.event_date).toLocaleDateString()}</p>
        <p><strong>Location:</strong> {caseStudy.location}</p>
        <p><strong>Status:</strong> {caseStudy.status}</p>
        <p><strong>Affected:</strong> {caseStudy.affected} individuals</p>
      </div>
      
      <div className="bg-slate-800 p-4 rounded text-slate-200">
        <h3 className="font-bold text-lg mb-2">Root Cause</h3>
        <p>{caseStudy.cause}</p>
      </div>

      {outcome && (
        <div className="mt-6 border-t border-slate-700 pt-6">
          <h3 className="font-bold text-green-400 mb-2">Final Reforms Achieved:</h3>
          <ul className="list-disc list-inside text-slate-300">
            {outcome.final_reforms.map((reform, idx) => (
              <li key={idx}>{reform}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
```

#### FILE: c:\DACSS\frontend\src\components\Chatbot.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// components/Chatbot.tsx
// Phase 6 — Context-scoped chatbot grounded to a single case study's data.
// Implementation begins in Phase 6.

```

#### FILE: c:\DACSS\frontend\src\components\CritiqueResult.tsx
```tsx
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
```

#### FILE: c:\DACSS\frontend\src\components\HomepageCustomizer.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// components/HomepageCustomizer.tsx
// Phase 5 — Per-section slider controls for user homepage personalization.
// Implementation begins in Phase 5.

```

#### FILE: c:\DACSS\frontend\src\components\LegalReferencePanel.tsx
```tsx
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
```

#### FILE: c:\DACSS\frontend\src\components\PolicyOracle.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// PolicyOracle: renders the AI-generated compliance report — treaties violated and tactical workaround

```

#### FILE: c:\DACSS\frontend\src\components\SolutionForm.tsx
```tsx
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
```

#### FILE: c:\DACSS\frontend\src\components\Timeline.tsx
```tsx
// components/Timeline.tsx
// Chronological timeline-of-unfolding widget with actor labels and parallel data track.
// Implementation begins in Phase 1.
import { TimelineEvent } from '@/types/case_study';

interface Props {
  events: TimelineEvent[];
}

export default function Timeline({ events }: Props) {
  if (!events || events.length === 0) return null;

  return (
    <section className="bg-slate-900 border border-slate-700 rounded-lg p-8 shadow-lg mt-8">
      <h2 className="text-2xl font-bold text-white mb-6">Event Timeline</h2>
      <div className="border-l-2 border-slate-600 pl-6 space-y-8">
        {events.map((event) => (
          <div key={event.id} className="relative">
            <div className="absolute w-3 h-3 bg-blue-500 rounded-full -left-[1.65rem] top-1.5"></div>
            
            <span className="text-sm text-blue-400 font-mono">
              {new Date(event.event_timestamp).toLocaleString()}
            </span>
            <h3 className="text-lg font-bold text-slate-200 mt-1">
              Actor: {event.responsible_actor}
            </h3>
            <p className="text-slate-400 mt-2">{event.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
```

#### FILE: c:\DACSS\frontend\src\components\TriviaWidget.tsx
**EMPTY FILE** (Only comments/whitespace found)
```tsx
// components/TriviaWidget.tsx
// Phase 6 — Daily trivia widget on the homepage.
// Implementation begins in Phase 6.

```
