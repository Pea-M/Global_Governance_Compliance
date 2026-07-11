Global Governance & Compliance Engine
An automated data and intelligence pipeline that converts raw, chaotic internet-censorship signals into structured, predictive risk analysis. By cross-referencing live network anomalies with regional news events, the engine autonomously tracks digital sovereignty blockages and maps them to international legal frameworks. The platform transforms descriptive infrastructure data into prescriptive policy adjustments and tactical workarounds in seconds instead of days.

🎯 Project Overview
This engine serves two primary user archetypes who depend on rapid, high-fidelity digital intelligence:

Corporate & Supply-Chain Risk Managers: Professionals who require early-warning infrastructure alerts before critical communication drops impact localized manufacturing hubs or logistics routes.

Policy Makers, NGOs, & Human-Rights Auditors: Organizations seeking real-time, technically-backed, and immutable digital proof of structural treaty violations on the ground.

🏗️ Technical Architecture & Data Models
The core application follows a decoupled structural footprint. The processing loop runs on a cloud schedule to ingest data and update records, keeping the frontend entirely read-only and lightning-fast.

Data relationships follow a one-to-many cascading model inside our relational Postgres database cluster:

anomaly_events (The Technical Footprint): Captures localized target application failures, technical drops, timestamp metrics, and country codes.

news_contexts (The Geopolitical Catalyst): Maps multiple concurrent media headlines and url tracking sources to the exact timing window of the network failure.

compliance_reports (The Prescriptive Intelligence): Stores the singular, highly structured legal audit showing violated clauses, technical workarounds, and macro reform advice.

  [ OONI API ]    ──>  [ anomaly_events ]  ──────┐
                                                 │
  [ GDELT API ]   ──>  [ news_contexts ]   ──( FK )──> [ Gemini 3.5 Flash Oracle ] ──> [ compliance_reports ]
                                                 │
  [ TREATIES ]    ──>  ( Static Matrix )   ──────┘
⚡ Current Progress (Achieved & Pushed to GitHub)
Phase 1 of the core automation engine is complete, tested, and fully committed to the repository:

Live Data Ingestion Pipeline (scraper.py): Fully integrated with the Open Observatory of Network Interference (OONI) API and the Global Database of Events, Language, and Tone (GDELT) API. Includes customized user-agent formatting and dynamic rate-limiting cooling parameters to manage API connection stability.

Autonomous Legal Treaty Audit (oracle.py): Configured with static legal matrices including the UN Universal Declaration of Human Rights (Article 19) and the UNDP Sustainable Development Goals (Target 16.10). Leverages the active production Gemini 3.5 Flash model with strict Pydantic parsing guidelines to output immutable, structured JSON data arrays.

Relational Cloud Integration (run_engine.py): A unified orchestrator that executes the end-to-end data pipeline. It extracts live telemetry from target volatile environments (hardcoded to IR for the MVP scope), generates the compliance summary, maintains absolute transactional database relationships, and writes securely to cloud-hosted Supabase PostgreSQL tables.

Isolated Environment Foundations: Standardized via dedicated local virtual environments (venv/) and structured modular schemas, ensuring full security decoupling via locally managed .env keys.

📂 Repository Directory Tree
Plaintext
global-governance-engine/
├── .github/
│   └── workflows/
│       └── cron_ingestion.yml    # Future serverless automation cron worker
├── backend/
│   ├── mock_data.json            # Offline payload validation payload
│   ├── oracle.py                 # Structured compliance synthesis module
│   ├── requirements.txt          # Active backend dependency lockfile
│   ├── run_engine.py             # Definitive transactional execution orchestrator
│   ├── sanity_check.py           # Local environment initialization tester
│   └── scraper.py                # Normalized OONI & GDELT client modules
├── PLANNING.md                   # Definitive strategic project roadmap
└── README.md                     # Technical implementation documentation
🚀 Getting Started
1. Environment Setup
Clone the repository and initialize your local virtual environment within the backend/ path:

Bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
2. Configuration Secrets
Duplicate the .env.example file and rename it to .env. Populate the target properties with your production infrastructure tokens:

Plaintext
SUPABASE_URL=your_supabase_project_endpoint
SUPABASE_SERVICE_KEY=your_private_write_access_token
GEMINI_API_KEY=your_google_ai_studio_token
3. Execution
To run the automated collection loop and push a fresh live entry block straight to the Supabase cloud cluster, execute the top-level orchestrator:

Bash
python run_engine.py
⏳ Coming Soon Features
The project is moving steadily through its evolutionary prototyping lifecycle. The following milestones are actively under development:

🔹 FastAPI Application Layer (backend/main.py)
Constructing standardized REST endpoints (GET /api/v1/incidents and GET /api/v1/incidents/{id}/report) to expose normalized database structures securely over HTTP.

Implementing Swagger documentation configurations (/docs) for simplified frontend testing contracts.

🔹 Next.js Interactive Workspace (frontend/)
Building a responsive, high-contrast dark-mode workspace dashboard using Next.js (App Router) and Tailwind CSS.

Implementing an explicit two-panel UX flow: a left-side chronological event feed displaying target blocked platforms and live GDELT catalyst headlines, coupled with a right-side panel that maps out the compliance report instantaneously on page load.

Integrating Recharts graphic matrices to visualize regional volatility trends natively without introducing heavy iframe integration bottlenecks.

🔹 Phase 2: Early Warning Alerts (Next 3–4 Weeks)
Designing an automated asynchronous notification worker within run_engine.py.

Integrating webhook alert handlers to dispatch compiled AI policy briefings straight to corporate Slack lines or secure human-rights monitoring emails via Twilio SendGrid the moment an infrastructure anomaly trips the system baseline.

🔹 Phase 3: Macro Scope Scaling (Months 2–6)
Scaling the single-country scope out to a dynamic multi-country radar matrix backed by parameter-driven Supabase query filters.

Broadening the engine's data tracking parameters to introduce dedicated tabs for alternative governance vectors, specifically mapping Supply-Chain interruptions and Environmental/Climate hazards.

Strict Core Guardrail: The platform will remain an open-source, read-only intelligence resource; public user authentication systems or billing layers are explicitly out of scope to preserve rapid, barrier-free access to data.
