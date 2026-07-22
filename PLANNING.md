# Governance & Disaster Case-Study Simulator — Full Project Vision

> v2 of this project's planning doc. Supersedes the old MVP-speedrun PLANNING.md.
> Nothing from the original build is discarded — see "What Carries Over" below.
> This document reflects the COMPLETE vision across all 4 hand-drawn wireframes.
> No feature here is "cut" — the roadmap sequences everything, it doesn't delete anything.
> Reference this file at the start of every AI coding session.

---

## 0. What Carries Over From v1 (nothing is lost)

| v1 component | New role |
|---|---|
| `scraper.py` (OONI + GDELT) | Becomes the live-data ingestion module for the **Digital Censorship & Internet Freedom** category — one of several category modules, not the whole product |
| `oracle.py` (Gemini + Pydantic structured output) | The exact pattern reused for the new **AI Critique Engine** — same technique (constrained prompt + enforced schema), new prompt content |
| `anomaly_events` / `news_contexts` / `compliance_reports` | Repurposed as the auto-generation source for `case_studies` where `category = digital_censorship` — mapped in the data model below, not deleted |
| `run_engine.py` | Becomes the orchestrator pattern for *every* category's ingestion module, not just censorship |
| Supabase project, RLS/GRANT setup, FastAPI app, GitHub Actions cron, git workflow | All directly reused as-is |
| Every debugging lesson (venv activation, `.gitignore` discipline, secrets handling, dev/main sync habits) | Encoded into Section 9 below so they don't get relearned the hard way twice |

---

## 1. Goal

### Why
Two real problems, not one. First: existing crisis/governance information (news coverage, NGO trackers, government portals) is descriptive — it tells you *what happened*, rarely asks you to *commit to a decision* the way real decision-makers had to. Second: existing "propose a policy" venues (Model UN, UPSC mock interviews, civics classrooms) are high-quality but access-gated, slow, and don't connect a person's reasoning to real, checkable historical outcomes in a fast feedback loop. This project's actual bet: pairing a structured decision exercise with an AI critique that's graded against **documented reality**, not against the AI's own opinion, is a genuinely underserved combination.

### Who
- Primary: people who want to *practice thinking like a policymaker/administrator* — competitive-exam aspirants (UPSC-style), poli-sci/public-policy students, and the more broadly curious who enjoy games like Democracy 4 or Frostpunk but want real history and real legal frameworks underneath, not a fictional ruleset.
- Secondary: educators who want a structured way to run a "what would you do" classroom exercise with an actual reveal-and-compare mechanic at the end.

### What makes it valuable
Not the live data feeds (six different orgs already do that better, with more resources — this was the honest conclusion from evaluating v1). The value is the **loop**: read a real bounded scenario → commit to a structured, multi-layer answer *before* seeing the outcome → get critiqued against the legal framework that actually applied at the time → see what real decision-makers actually did and how it played out. That loop doesn't require winning a data-freshness arms race against NetBlocks or Access Now. It requires good case-study content and a disciplined AI-critique design — both fully in this project's control.

---

## 2. Features & Guardrails (complete inventory, nothing deferred out of the plan)

### 2.1 Core Loop
- Browse case studies across categories (see 2.2)
- Read a full case-study page: header facts, photo/article/report panel, chronological unfolding timeline, applicable legal/jurisdiction framework
- Submit a structured, multi-layer proposed response (see 2.4)
- Receive an AI critique benchmarked against real documented outcome (resolved cases) or a forecast-only critique (ongoing cases — see 2.6)
- View other users' submitted solutions and their critiques; comment on them

### 2.2 Content Categories
Fires · Terrorist Attacks · International Relations · Economic Policy · Cyclones/Natural Disasters · Civil Unrest · Digital Censorship & Internet Freedom (v1's existing module). Each category is its own ingestion module (see Section 8) — some are live-API-fed, some are necessarily hand-curated/editorial (see honest breakdown in Section 8).

### 2.3 Case-Study Page
- Header block: event name, date, location, deaths, people affected, cause, region affected
- Photos / Articles / Artifacts / Reports panel
- Timeline-of-unfolding widget: chronological markers, each with the responsible actor (CM/president/agency), and a parallel "endures / stats / data / news" track
- Legal & Jurisdiction Reference panel: every law, constitutional article, treaty, and policy that was **actually in force and applicable at the time** — this is the ceiling the AI critique checks a user's answer against, not a generic legal library
- Context-scoped chatbot: "ask for details regarding this event" — grounded strictly to this case study's own data (events/history/timeline/laws), never open-domain
- Actions: Create Report / Run Simulation / Propose Solution, and View Other's Solutions & Reports

### 2.4 Structured Solution Input
Four panels, exactly as designed:
- **Own Analysis** — free-form but length-guided ("type/note down as possible")
- **Immediate Action** — on-ground response, with adjustable severity/scope sliders ("adjustable riders")
- **Problem Highlights** — short-form problem framing, with hints/citations pulling from a framework + AI-suggested prompts, plus a supply-chain/resources sub-section (water/irrigation, map view, satellite view where relevant)
- **Refer to Constitution** — explicit citation of the laws/articles/jurisdiction the user's plan relies on (e.g. "Article 19 — Right to..."), plus consideration of bilateral relations, economy, trade deficit, info-tech availability, and stakeholders at that time
- Policy Reform sub-actions: propose creating a body/department, draft rules/acts
- Input mode: v1 ships as structured form controls (dropdowns, tag pickers, sliders); true drag-and-drop composition is a v2 polish pass once the structured version is proven (see Section 4)
- Submit / Run / Check actions

### 2.5 AI Critique & Outcome Comparison ("AI Result — Final Output")
- **Your Ideas** panel: summarizes the user's policy, body formed, agenda back to them
- **What Actually Happened** panel *(resolved case studies only)*: real evacuation timeline, committee formed, final act/reform, policy signed
- **Future Prediction** panel: collapse of related industries, second-order impacts, possibilities — framed explicitly as the AI's projection, not fact
- **After Effects** panel: people affected, spread/region, progress, further developments
- Pros / Cons / Additions / Deletions — a structured critique, not a bare numeric score (see guardrail below)
- Comments section on the result
- Download Detailed Summary (PDF export)

### 2.6 Live / Ongoing Events — a genuinely different mechanic, not the same one reused
This was a real design gap in the wireframes, resolved here explicitly: a case study with `status = ongoing` has **no real outcome yet**, so it cannot honestly show a "what actually happened" comparison. Instead:
- The AI critique for an ongoing case shows only **Your Ideas + Future Prediction + Pros/Cons** — the "What Actually Happened" panel is replaced with "Resolution pending — this story is still developing."
- A background/admin process periodically reviews ongoing cases and, once real-world resolution is documented, flips `status` to `resolved` and back-fills the `historical_outcome` record — at which point every existing submission against that case study can retroactively show its comparison.
- This is closer to a forecasting mechanic (à la Metaculus) than a history-quiz mechanic for the ongoing-case subset, and the UI should say so plainly so users aren't misled about what's verified vs. predicted.

### 2.7 Homepage — Fully Customizable Tabloid
- Category tabs across the top (Fires / Terrorist Attacks / Intl Relations / Economic Policies / Cyclones / Civil Unrest)
- Numbered current-affairs feed, each item linking to view / case-study / news-articles / actions
- Location filter chips (country-based)
- Popular Case Studies / Events section
- Current Affairs section (distinct from resolved case studies — see 2.6)
- Historical Parity / Photo Museum / Culture section
- Today's Trivia widget
- Random Historical Fact ("what happened 50/100 years ago on this day")
- General chatbot entry point (ask for details on events/history/timeline/laws)
- Per-section customization sliders so a user's homepage reflects their own interests, not a fixed layout

### 2.8 Social Layer
- User profiles: display name, bio, their submitted case studies/solutions, their notes
- View other users' submissions and AI critiques
- Comment on submissions
- Per-user storage of their own case-study notes/history

### 2.9 Cross-cutting Guardrails
- **AI critiques are grounded, never free-associated.** The critique prompt is always constrained to (a) the user's actual submitted text, (b) the case study's stored `legal_references`, and (c) the stored `historical_outcome` when it exists. Same anti-hallucination discipline as v1's `oracle.py` — this project's core lesson from v1 was exactly about not letting an LLM assert unverified claims with false confidence.
- **No bare numeric leaderboard score.** Per the v1 postmortem: LLM-as-judge single-number scoring rewards confident, verbose writing over substance. Critique output is structured (pros/cons/additions/deletions) — a rubric, not a score — full stop, this is a hard constraint on the design, not a style preference.
- **Chatbot is context-scoped, never open-domain.** It only ever answers from the specific case study's own stored data. It does not become a general geopolitics chatbot.
- **Terrorist Attacks category needs a deliberately more careful sourcing process than any other category** — misattributed or poorly-sourced content here is a real accuracy and reputational risk, more so than disaster data. This category is built last (Section 4), curated only from established datasets, never live-scraped from arbitrary news sources.
- **Comments require moderation from day one of the social layer shipping** — no public text box goes live without at minimum a report/hide mechanism.
- **`POST` trigger/admin endpoints require auth**, same lesson as v1's open `/engine/trigger` gap.
- **Ongoing-case forecasts are visually and textually distinct from resolved-case comparisons** — a user should never mistake an AI prediction for a verified historical fact.

---

## 3. Data Models

Not database tables yet — just the real entities and how they relate.

**Core content:**
- **Case Study** — the central unit. Has a category, a status (`ongoing` / `pending_resolution` / `resolved`), and all header facts (date, location, cause, deaths, affected, region).
- **Timeline Event** — many per Case Study. A dated marker with a responsible actor and description.
- **Legal Reference** — many per Case Study. The specific laws/articles/treaties/policies in force *at that time*, typed (constitution article / national law / international treaty / policy).
- **Media Item** — many per Case Study. Photos, articles, reports, artifacts, with source attribution.
- **Historical Outcome** — one per Case Study, but only populated once `status = resolved`. What actually happened: immediate actions taken, committees formed, final reforms enacted, after-effects, pros/cons of the real response.

**User interaction:**
- **User** — profile, auth identity, bio.
- **Submission** — one user's structured answer to one Case Study (own analysis, immediate action, problem highlights, constitution references, proposed bodies/departments, draft rules/acts).
- **AI Critique** — one per Submission. Summary of the user's idea, future prediction, pros/cons/additions/deletions, and — only if the linked Case Study is resolved — the comparison against Historical Outcome.
- **Comment** — many per Submission, authored by a User.
- **User Preferences** — one per User. Homepage widget configuration, location filters, category weighting.

**Engagement / discovery:**
- **Trivia Item** — question, options, correct answer, category, active date.
- **Historical Parity Fact** — recurring "on this day" content, independent of the case-study system.
- **Chatbot Message** — belongs to a User (nullable if anonymous) and optionally scoped to a Case Study; role (user/assistant), content, timestamp.

**Relationships, drawn out:**
```
Case Study 1 ──< Timeline Event
Case Study 1 ──< Legal Reference
Case Study 1 ──< Media Item
Case Study 1 ── 1 Historical Outcome        (nullable until resolved)
Case Study 1 ──< Submission
Submission  1 ── 1 AI Critique
Submission  1 ──< Comment
User        1 ──< Submission
User        1 ──< Comment
User        1 ── 1 User Preferences
Case Study  1 ──< Chatbot Message           (context-scoped)

[existing v1 pipeline] Anomaly Event ──feeds──> Case Study (category = digital_censorship)
```

---

## 4. Build Sequence — phased, not stripped

Per your instruction: nothing below is cut from the plan. This is a sequencing decision (what gets built and proven first), not a scope decision (everything is committed across the year).

- **Phase 0 (done):** v1 infrastructure — repo, Supabase, FastAPI skeleton, GitHub Actions, one working live-data module (censorship).
- **Phase 1 — Core loop, single category:** Case Study, Timeline Event, Legal Reference, Media Item, Historical Outcome, Submission, AI Critique for **Historical Disasters only** (Chernobyl as the first hand-written case study). Structured (non-drag-drop) submission form. No auth yet — anonymous submissions are fine for proving the loop. This is the smallest slice that makes the *actual* value proposition (the critique-against-reality loop) testable end to end.
- **Phase 1.5 — Data Seeding & Fixtures:** Establish relational integrity via JSON fixtures and automated seeding scripts to allow for reproducible development environments. `backend/db/fixtures/core_fixtures.json` holds structured seed records (case studies, timeline events, legal references) that mirror the target Supabase schema. `backend/scripts/seed.py` reads these fixtures and performs idempotent upserts — new developers (or a fresh CI environment) can restore a known-good data state with a single command, without relying on hand-crafted SQL or manual Table Editor inserts.
- **Phase 2 — More categories, and an honest split between live and editorial content:** Fires (NASA FIRMS live feed), Cyclones (GDACS/NOAA live feed), Digital Censorship (existing OONI/GDELT pipeline, now mapped into the shared `case_studies` schema), International Relations and Economic Policy (these are **necessarily hand-curated/editorial** — there is no clean global live API for something like a central bank rate decision or a bilateral pact; build an admin content-entry flow instead of pretending this can be fully automated).
- **Phase 3 — Ongoing/live-event mechanic:** implement the `status` state machine (Section 2.6) and the admin resolution-review flow. Drag-and-drop polish on the submission form.
- **Phase 4 — Social layer:** auth (Supabase Auth), profiles, comments with moderation, viewing others' submissions.
- **Phase 5 — Homepage personalization + analytics:** customizable widget sliders, location filters, popular/trending tracking. This is also where a **Power BI cross-user analytics dashboard** earns a real, non-redundant purpose it didn't have in v1 — aggregate patterns across all submissions (most-cited legal articles, category popularity, submission trends over time) rather than re-visualizing the same single feed the main site already shows. *(Flagged as open decision — see Section 11.)*
- **Phase 6 — Engagement features:** context-scoped chatbot, trivia, historical-parity/culture section.
- **Phase 7 — Terrorist Attacks category:** deliberately last, once the editorial curation workflow from Phase 2 is mature and trustworthy, given the accuracy/reputational stakes flagged in Section 2.9.

---

## 5. Wireframes

Four hand-drawn pages, finalized:
1. **Case Study Page** — header facts, photos/articles panel, timeline-of-unfolding, legal/jurisdiction reference column, chatbot entry, Create Report/Run Simulation/Propose Solution + View Others' actions.
2. **Homepage Tabloid** — category tabs, numbered current-affairs feed, location filters, popular case studies, current affairs, historical-parity/culture section, trivia, chatbot, full customization.
3. **AI Result Page** — Your Ideas vs. What Actually Happened, Future Prediction, After Effects, Pros/Cons/Additions/Deletions, comments, download summary.
4. **Solution/Simulation Proposal Page** — Own Analysis + Policy Reforms (left/solution pane) and Problem Highlights + Refer to Constitution (right/problem pane, layout-only split per your note) with Submit/Run/Check.

UX-first per your own rule — these stay paper/Figma until Phase 1's core loop is validated with real content, then get built once, properly, rather than iterated in code.

---

## 6. Future & Timeline
Committed to building this out over roughly a year, iterating continuously — no artificial speedrun constraint, no permanent scope cuts. The discipline instead comes from **sequencing** (Section 4) so that each phase ships something genuinely usable and testable before the next one starts, rather than a year of unshippable partial work across every feature simultaneously.

---

## 7. Presentation
A website (Next.js + Tailwind frontend, FastAPI backend), responsive for both desktop reading (case-study deep-dives) and mobile (quick homepage browsing, trivia). No native mobile app planned — a website covers the actual usage pattern.

---

## 8. Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js (App Router) + Tailwind + shadcn/ui | Reused from v1; shadcn's form primitives cover sliders/dropdowns for the structured submission UI |
| Drag-and-drop (Phase 3) | dnd-kit | Add only once the structured-form version is proven — don't front-load this |
| Backend | FastAPI (Python) | Reused from v1 |
| Database | Supabase Postgres | Reused; schema extended per Section 3 |
| Auth (Phase 4) | Supabase Auth | Same project, no new vendor |
| File/media storage (Phase 1+) | Supabase Storage | For case-study photos/articles/reports |
| LLM | Gemini API via `google-genai` | Reused pattern from `oracle.py` |
| Automation | GitHub Actions | Reused; one workflow per live-data category module |
| Fires (Phase 2) | NASA FIRMS API | Real-time satellite fire data, free, well-documented |
| Cyclones/disasters (Phase 2) | GDACS API | Global disaster alerting, free |
| Digital censorship (Phase 2) | OONI + GDELT | Already built in v1 |
| Intl relations / economic policy | Manual/editorial entry via an admin flow | Honest limitation — no clean live API exists for this; don't pretend otherwise |
| Terrorist attacks (Phase 7) | Curated from an established academic dataset (e.g. GTD), never live-scraped | Accuracy/reputational caution per Section 2.9 |
| Analytics dashboard (Phase 5) | Power BI — *pending your confirmation, see Section 11* | Cross-user submission-pattern analytics, not a redundant re-visualization of the main feed |
| Backend hosting | *Undecided — see Section 11* | Vercel doesn't run a persistent FastAPI server well; needs a real decision before any Phase 1 deploy |
| Frontend hosting | Vercel | Already the plan from v1, still correct |

---

## 9. Development Process

### 9.1 Folder structure (grows with each phase, doesn't need to be rebuilt)
```
project-root/
├── .github/workflows/
│   ├── cron_censorship.yml
│   ├── cron_fires.yml            (Phase 2)
│   ├── cron_cyclones.yml         (Phase 2)
├── backend/
│   ├── main.py                   # FastAPI app, includes routers below
│   ├── routers/
│   │   ├── case_studies.py
│   │   ├── submissions.py
│   │   ├── critiques.py
│   │   ├── chatbot.py            (Phase 6)
│   │   ├── auth.py               (Phase 4)
│   ├── modules/                  # one folder per live-data category
│   │   ├── censorship/
│   │   │   ├── scraper.py        # existing, unchanged
│   │   │   ├── oracle.py         # existing, unchanged
│   │   ├── fires/                (Phase 2)
│   │   ├── cyclones/             (Phase 2)
│   ├── db/                    
│   │   └── fixtures/          
│   │       └── core_fixtures.json
│   ├── scripts/               
│   │   └── seed.py
│   ├── core/
│   │   ├── supabase_client.py
│   │   ├── critique_engine.py    # shared AI-critique logic, all categories call this
│   ├── run_engine.py             # orchestrator, loops all active modules
│   ├── requirements.txt
│   ├── .env.example
├── frontend/
│   ├── src/app/
│   │   ├── page.tsx                                  # homepage tabloid
│   │   ├── case-studies/[id]/page.tsx
│   │   ├── case-studies/[id]/submit/page.tsx
│   │   ├── case-studies/[id]/result/[submissionId]/page.tsx
│   │   ├── profile/[userId]/page.tsx                 (Phase 4)
│   ├── src/components/
│   │   ├── CaseStudyHeader.tsx
│   │   ├── Timeline.tsx
│   │   ├── LegalReferencePanel.tsx
│   │   ├── SolutionForm.tsx
│   │   ├── CritiqueResult.tsx
│   │   ├── Chatbot.tsx            (Phase 6)
│   │   ├── TriviaWidget.tsx       (Phase 6)
│   │   ├── HomepageCustomizer.tsx (Phase 5)
│   ├── src/lib/supabase.ts
├── PLANNING.md
├── README.md
```

### 9.2 Naming conventions
Unchanged from v1: Python = snake_case, React/TS components = PascalCase files, DB columns = snake_case.

### 9.3 Dev environment
Unchanged: Python venv per-session activation, `.env`/`.env.local` split between backend/frontend, `NEXT_PUBLIC_` prefix rule for browser-exposed vars. Set the workspace default interpreter once (Section from v1 debugging) so new terminals don't silently fall back to a global Python.

### 9.4 Version control — lessons encoded, not relearned
- Work on `dev`, sync to `main` as one uninterrupted block: `git checkout main && git merge dev && git push origin main` — don't split pull/merge/push across separate sessions, that's exactly what caused repeated conflicts in v1.
- **Edit a given file (especially README) in exactly one place per day** — local editor *or* GitHub web UI, never both without pulling in between first.
- Confirm `git status` is clean and `.env`/`.env.local` are absent before every push — non-negotiable habit, not a one-time check.
- Every new table added to Supabase needs its RLS policy *and* its GRANT statements — the auto-expose toggle is off project-wide, this will keep coming up as new tables are added through the phases above.

### 9.5 Database & data models
Build per-phase, matching Section 4 — don't create Phase 5's tables while still building Phase 1. Each new table: create in Table Editor → add RLS policy → add GRANT statements → sanity-check with a throwaway insert/read script before wiring real code against it, same discipline as v1.

### 9.6 Backend routes
Each phase adds its own router file under `routers/`, tested via `/docs` before any frontend code touches it — same discipline as v1's `main.py` verification step.

### 9.7 Frontend
Build against real seeded data (not mock fixtures) once Phase 1's backend is confirmed working — v1 found this faster than maintaining parallel mock data.

### 9.8 Integration & versioning
Tag a release at the end of each completed phase (`v1.0-phase1-core-loop`, `v1.0-phase2-categories`, etc.) — gives you real checkpoints across a year-long build instead of one undifferentiated `main` branch.

### 9.9 CI/CD
One GitHub Actions workflow per live-data category module, each with its own secrets and its own `workflow_dispatch` for manual testing before trusting its schedule — proven pattern from v1's censorship cron.

### 9.10 Testing protocol (every phase, not just Phase 1)
1. Ingestion (for live-data categories): print raw API JSON, confirm schema hasn't drifted.
2. Database: check Table Editor after every insert-type change — actually look, don't just trust a print statement.
3. API: exercise every new endpoint via `/docs` before frontend work starts.
4. UI: load the deployed URL in a private window, confirm real data renders.
5. **New for this phase of the project:** AI critique output — read it critically for anything suspiciously specific (invented dates/statistics/quotes) before trusting it, every time the critique prompt changes.

---

## 10. SDLC Model
**Incremental development**, not the pure evolutionary-prototyping model v1 used. The distinction matters: prototyping assumes you're building throwaway/refined versions toward an unclear target. This project's target is now fully specified (Sections 2–5) — what's unknown is only *sequencing*, not *scope*. Incremental development fits that: each phase in Section 4 is a complete, permanent, production-quality slice that's fully built, tested, and shipped before the next phase starts — nothing gets thrown away and rebuilt, each phase's code is additive infrastructure for the next one.

---

## 11. Open Decisions — need your input before the relevant phase starts

1. **Power BI's role** — Section 8/4 proposes repurposing it as a Phase 5 cross-user analytics dashboard rather than dropping it. Confirm or reject.
2. **Backend hosting** — FastAPI needs a real persistent host before any public deploy (Vercel alone doesn't cleanly cover this). Recommend evaluating Render or Fly.io free tiers when Phase 1 nears deploy — not urgent yet, but don't let it become a Day-4-style surprise late in Phase 1.
3. **Auth provider** — defaulting to Supabase Auth (same project, no new vendor) for Phase 4. Confirm.
4. **Terrorist Attacks sourcing** — confirmed direction is curated-only from an established dataset, built last (Phase 7). Confirm this is acceptable rather than any live-scraping approach.
5. **Handwriting items still unconfirmed** from the wireframe review: the cut-off word top-right of Image 1 ("into resp... & ___"), the intended header text above the Laws/Constitution/Articles/Policies list in Image 1's right column, and the "concerns raised also for be[tter]" note near Image 4's Submit/Run/Check buttons.
