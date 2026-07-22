# Governance & Disaster Case-Study Simulator

An interactive platform where users analyze real historical and unfolding crises — disasters, governance failures, geopolitical events — and propose structured, multi-tier solutions across immediate action and policy reform. Every submission is critiqued by an AI engine benchmarked against the legal framework that actually applied at the time, and — for resolved cases — against the real, documented outcome.

This is not a live news dashboard or a policy-recommendation engine. It's a decision-practice tool: read a real bounded scenario, commit to a structured answer *before* seeing what happened, then compare your reasoning against history.

---

## 1. Why This Project Exists

### 1.1 The Problem
Existing crisis and governance information — news coverage, NGO trackers, government portals — is almost entirely descriptive. It tells you *what happened*, but rarely asks you to *commit to a decision* the way real administrators, ministers, or policymakers had to, under the same time pressure and the same incomplete information.

Meanwhile, tools that do ask you to practice this kind of judgment (Model UN, UPSC-style mock interviews, civics classrooms) are high quality but access-gated, slow, and disconnected from a fast, checkable feedback loop grounded in real history.

### 1.2 The Bet
Pairing a structured decision exercise with an AI critique that's graded against **documented reality** — not against the AI's own opinion — is a genuinely underserved combination. The value isn't in aggregating live data (several well-funded organizations already do that better). The value is the loop itself:

> Read a real scenario → commit to a structured answer → get critiqued against the legal framework that actually applied → see what real decision-makers did and how it played out.

### 1.3 Who It's For
- **Primary:** competitive-exam aspirants (UPSC-style), public-policy and poli-sci students, and anyone who enjoys games like *Democracy 4* or *Frostpunk* but wants real history and real legal frameworks underneath, not a fictional ruleset.
- **Secondary:** educators who want a structured "what would you do" classroom exercise with a genuine reveal-and-compare mechanic.

---

## 2. What Carries Over From v1

This project began as a **Global Governance & Compliance Engine** monitoring internet censorship via OONI and GDELT. That work was not discarded — it evolved:

| v1 Component | New Role |
|---|---|
| OONI + GDELT ingestion pipeline | Live-data module for the **Digital Censorship & Internet Freedom** case-study category |
| Gemini + Pydantic structured-output pattern | The exact mechanism reused for the AI Critique Engine |
| `anomaly_events` / `news_contexts` / `compliance_reports` tables | Feed source for censorship-category case studies |
| Supabase RLS/GRANT setup, FastAPI app, GitHub Actions cron, git workflow | Reused as-is across the full project |

---

## 3. Core Features

### 3.1 The Core Loop
1. Browse case studies across categories.
2. Read a full case-study page — header facts, timeline of unfolding, applicable legal/jurisdiction framework, media/reports.
3. Submit a structured, multi-layer proposed response.
4. Receive an AI critique: summary, likely consequences, pros/cons/additions/deletions — and, for resolved cases, a narrative comparison against what actually happened.
5. Browse other users' submissions and critiques (planned — see Roadmap).

### 3.2 Content Categories
Fires · Terrorist Attacks · International Relations · Economic Policy · Cyclones/Natural Disasters · Civil Unrest · Digital Censorship & Internet Freedom.

Each category is its own ingestion module. Some are live-API-fed (fires, cyclones, censorship); others are necessarily hand-curated/editorial (international relations, economic policy) since no clean global API exists for events like a bilateral pact or a central bank rate decision.

### 3.3 Case-Study Page
- Header: event name, date, location, deaths, people affected, cause, region.
- Photos / articles / artifacts / reports panel.
- Chronological timeline-of-unfolding, with responsible actor per event.
- **Legal & Jurisdiction Reference panel** — every law, constitutional article, treaty, and policy actually in force at the time. This is the ceiling the AI critique checks a submission against.
- Context-scoped chatbot (planned) — grounded strictly to that case study's own data, never open-domain.

### 3.4 Structured Solution Input
Four panels:
- **Own Analysis** — free-form reasoning.
- **Immediate Action** — on-ground response.
- **Problem Highlights** — short-form problem framing.
- **Refer to Constitution** — explicit citation of the laws/articles the plan relies on.

Plus policy-reform sub-actions (propose a body/department, draft rules/acts).

### 3.5 AI Critique Engine
Every critique includes:
- **Summary of the user's idea** — neutral restatement.
- **Likely consequences** — a grounded narrative forecast, never a numeric score.
- **Pros / Cons / Additions / Deletions** — structured, specific critique.
- **Against what actually happened** — populated only for resolved case studies; explicitly shows "still developing" for ongoing cases rather than fabricating a comparison.

> **Hard design constraint:** no bare numeric leaderboard score, ever. Single-number LLM-as-judge scoring rewards confident, verbose writing over substance — this was a deliberate lesson learned and corrected during development. Critique output is always narrative + structured pros/cons, never a percentage badge.

### 3.6 Live vs. Resolved Cases
A case study's `status` field distinguishes:
- **`resolved`** — has a documented `historical_outcome`; critiques include a real comparison.
- **`ongoing`** — no outcome yet; critiques show only summary, forecast, and pros/cons, with an explicit "resolution pending" message. Once real-world resolution is documented, the case flips to `resolved` and every existing submission can retroactively show its comparison.

---

## 4. Data Model

**Core content:** Case Study → Timeline Events, Legal References, Media Items, and (once resolved) one Historical Outcome.

**User interaction:** User → Submissions → one AI Critique per submission → Comments (planned).

```
Case Study 1 ──< Timeline Event
Case Study 1 ──< Legal Reference
Case Study 1 ──< Media Item
Case Study 1 ── 1 Historical Outcome     (nullable until resolved)
Case Study 1 ──< Submission
Submission  1 ── 1 AI Critique
```

---

## 5. Architecture & Tech Stack

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router) + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | Supabase (Postgres), RLS-secured |
| LLM | Gemini API via `google-genai`, Pydantic-enforced structured output |
| Automation | GitHub Actions cron, one workflow per live-data category |
| Live data sources | OONI + GDELT (censorship, built), NASA FIRMS (fires, planned), GDACS (cyclones, planned) |

### 5.1 Guardrails (non-negotiable design constraints)
- AI critiques are grounded only in the submission, the case study's legal references, and its documented outcome — never free-associated.
- No bare numeric score, anywhere.
- Chatbot (when built) is context-scoped to one case study, never open-domain.
- Terrorist Attacks category is built last, curated only from established datasets, never live-scraped — accuracy and reputational risk here is higher than for any other category.
- Any admin/trigger endpoint requires auth before public deployment.
- Ongoing-case forecasts are visually and textually distinct from resolved-case comparisons — a user should never mistake a prediction for a verified fact.

---

## 6. Project Structure

```
project-root/
├── .github/workflows/          # one cron per live-data category
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── routers/                # case_studies, submissions, critiques, auth (Phase 4), chatbot (Phase 6)
│   ├── modules/                # one folder per live-data category (censorship, fires, cyclones)
│   ├── core/                   # supabase_client, critique_engine
│   ├── scripts/                # db seed script + fixtures
├── frontend/
│   ├── src/app/                # homepage, case-studies/[id], submit, result/[submissionId]
│   ├── src/components/         # CaseStudyHeader, Timeline, LegalReferencePanel, SolutionForm, CritiqueResult
│   ├── src/lib/                # supabase client
│   ├── src/types/               # shared TypeScript contracts
├── PLANNING.md                  # full project vision, phased build sequence
├── README.md
```

---

## 7. Current Status

**Phase 1 — Core Loop: complete and verified end to end**, tagged `v1.0-phase1-core-loop`.
- Case-study page renders real data (header, timeline, legal references) from a live FastAPI backend backed by Supabase.
- Structured submission form posts to the backend, triggers AI critique generation, and redirects to a result page.
- Critique engine produces grounded, specific, narrative critiques — verified against both `resolved` and `ongoing` case-study branches.
- Draft autosave (browser-local) protects in-progress submissions from being lost on a crash or reload.

**Not yet built** (see `PLANNING.md` for the full phased roadmap):
- Additional live-data category modules (fires, cyclones)
- Editorial content-entry flow for international relations / economic policy
- Auth, user profiles, saved drafts/submissions history
- Comment system with moderation
- Context-scoped chatbot, trivia widget, homepage personalization
- Terrorist Attacks category (deliberately last)

---

## 8. Getting Started (local development)

### 8.1 Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# populate .env from .env.example with your Supabase + Gemini keys
uvicorn main:app --reload
```
API docs available at `http://127.0.0.1:8000/docs`.

### 8.2 Frontend
```bash
cd frontend
npm install
# populate .env.local from .env.example with your Supabase URL + anon key
npm run dev
```
Runs at `http://localhost:3000`.

### 8.3 Seeding sample data
```bash
cd backend
python scripts/seed.py
```
Loads fixture case studies, submissions, and critiques from `db/fixtures/core_fixtures.json` into Supabase.

---

## 9. Roadmap

See `PLANNING.md` for the complete, detailed phase-by-phase build sequence (Phases 0–7), including the open decisions still pending: backend hosting choice, Power BI's role in a future cross-user analytics dashboard, and auth provider confirmation.

This is a long-term build — no artificial timeline, no feature permanently cut. Sequencing exists so each phase ships something genuinely usable before the next begins.