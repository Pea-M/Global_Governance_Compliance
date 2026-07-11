# Global Governance & Compliance Engine — Project Context

> Reference this file at the start of every AI coding session ("see PLANNING.md, now build X").
> Do not re-explain the vision each time — scope every prompt to one file/module below.

## What this is
An engine that turns raw internet-censorship signals into actionable intelligence:
detect a network anomaly (OONI) → explain it with real-world news (GDELT) → audit it
against international law (UN Art 19, UNDP SDG 16) via LLM → surface a tactical + policy
brief. Goes from "descriptive" (what happened) to "prescriptive" (what to do about it),
in seconds instead of days.

## Users
- **Primary:** corporate/supply-chain risk managers who need early warning before an
  outage hits the news.
- **Secondary:** policy makers, NGOs, human-rights auditors who need real-time,
  technically-backed proof of treaty violations.

## MVP scope — LOCKED
- **One country only** (pick one volatile region, e.g. Iran/Russia/Myanmar). No global map,
  no country selector. Hardcode the `country_code`.
- **One page, two panels.** Left = facts (blocked apps + top 3 headlines, today).
  Right = AI compliance report (treaty violated + tactical workaround). No "Generate"
  button — report is already on screen when the page loads.
- **Manual trigger first.** `run_engine.py` run by hand on your laptop, verified end to
  end, *before* wiring GitHub Actions automation.
- **Non-goals for MVP:** no auth, no payments, no multi-country dropdown, no chat
  interface, no editing/deleting data (read-only for users).

## Features & guardrails
- Global Radar (hotspot view) → Incident Drill-Down (click → matching news) → AI Policy
  Brief (tactical solution + treaty audit) → Compliance panel (which article was violated).
- **Anti-hallucination:** LLM prompt must be constrained to *only* the incident/news/treaty
  text passed in — never a general chatbot.
- **Provenance is always visible:** "Anomaly data: OONI. News: GDELT. Policy: AI-generated."
- **Read-only for the public site.** Frontend uses an anon read-only Supabase key; only the
  backend automation writes.

## Data models
| Entity | Key fields | Relationship |
|---|---|---|
| `anomaly_events` | id (UUID), timestamp, country_code, failure_type, target_app | 1 |
| `news_contexts` | id, anomaly_id (FK), headline, source_url | many per anomaly |
| `compliance_reports` | id, anomaly_id (FK), treaties_violated (text[]), tactical_solution, policy_reform | 1 per anomaly |
| `treaty_frameworks` (static, hardcoded, no API) | treaty_id, law_name, article_number, description | referenced by LLM prompt, not FK'd |

One `AnomalyEvent` + many `NewsContext` + treaty list → LLM → one `ComplianceReport`.

## Tech stack (decided, don't relitigate)
- Backend: Python 3.10+, FastAPI, `requirements.txt`, local venv.
- AI: Gemini API (or OpenAI) — structured JSON output only, no freeform chat.
- DB: Supabase (Postgres). Service key = write (backend only). Anon key = read (frontend only).
- Automation: GitHub Actions cron, `.yml` in `.github/workflows/`.
- Frontend: Next.js (App Router) + Tailwind. Charts: Recharts (Power BI optional/secondary, skip for MVP — adds deploy friction, revisit in Phase 3 if desired).
- Hosting: Vercel (frontend, auto-deploy on push to `main`). Supabase and GitHub Actions are already hosted.

## Folder structure
```
global-governance-engine/
├── .github/workflows/cron_ingestion.yml
├── backend/
│   ├── main.py            # FastAPI app
│   ├── scraper.py         # OONI + GDELT fetchers
│   ├── oracle.py          # LLM prompt + synthesis
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/app/page.tsx, layout.tsx
│   ├── src/components/AnomalyFeed.tsx, PolicyOracle.tsx
│   ├── src/lib/supabase.ts
│   └── tailwind.config.js
└── README.md
```
Naming: Python = snake_case. React/TS components = PascalCase files, camelCase internals.
DB columns = snake_case (matches backend, zero translation friction).

## API endpoints (backend contract)
- `GET /api/v1/incidents` — recent anomalies + country codes
- `GET /api/v1/incidents/{id}/report` — news + compliance report for one incident
- `POST /api/v1/engine/trigger` — manually re-run the pipeline (debugging only, secured)

## Git workflow
- `main` = always deployable, tied to Vercel prod. `dev` = working branch, merge only
  after the relevant step in the testing protocol below passes.
- Tag `v0.1.0-mvp` once the MVP is live end-to-end.

## Testing protocol (run at every step, not just at the end)
1. Ingestion: print raw OONI/GDELT JSON to terminal — confirm schema hasn't drifted.
2. Database: open Supabase table browser — confirm rows match fields, no truncation.
3. API: hit endpoints via `/docs` (Swagger) or `curl` — confirm 200/404 as expected.
4. UI: load the deployed URL in a private window — confirm layout renders, data is live.

## Roadmap (so "Ongoing" on the resume has a real answer)
- **Phase 1 (now, Days 1–4):** single-country MVP above, manual → then automated pipeline.
- **Phase 2 (next 3–4 weeks):** webhook/Slack/email alerting when a new report is generated —
  turns this from a dashboard into an early-warning system.
- **Phase 3 (months 2–6):** multi-sector tabs (supply chain, climate) + multi-country
  dropdown backed by a dynamic Supabase query. Still no auth, no payments — stays an
  open intelligence platform, not a SaaS product.

## SDLC
Prototyping (evolutionary) + iterative enhancement. Ship a thin vertical slice end-to-end
first, then widen. Don't build ahead of the current phase.
