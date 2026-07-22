import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# Load .env variables (SUPABASE_URL, SUPABASE_SERVICE_KEY)
load_dotenv()

app = FastAPI(
    title="Global Governance & Compliance Engine API",
    description="Surfaces network anomaly incidents and AI-generated compliance reports.",
    version="0.1.0",
)

# -----------------------------------------------------------------
# CORS — allow local Next.js dev server
# -----------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------
# Supabase client (service key — read + write)
# -----------------------------------------------------------------
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment.")
    return create_client(url, key)


# -----------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------

@app.get("/api/v1/incidents", summary="List recent anomaly events")
def list_incidents():
    """
    Returns the 10 most recent rows from **anomaly_events**,
    ordered by timestamp descending.
    """
    supabase = get_supabase()
    response = (
        supabase
        .table("anomaly_events")
        .select("*")
        .order("timestamp", desc=True)
        .limit(10)
        .execute()
    )
    return {"incidents": response.data}


@app.get(
    "/api/v1/incidents/{incident_id}/report",
    summary="Get news context + compliance report for one incident",
)
def get_incident_report(incident_id: str):
    """
    Returns all **news_contexts** rows and the single **compliance_reports**
    row that belong to the given anomaly_id (UUID).
    Raises 404 if the anomaly does not exist.
    """
    supabase = get_supabase()

    # Verify the incident exists
    incident_resp = (
        supabase
        .table("anomaly_events")
        .select("id")
        .eq("id", incident_id)
        .execute()
    )
    if not incident_resp.data:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

    # Fetch related news context rows
    news_resp = (
        supabase
        .table("news_contexts")
        .select("*")
        .eq("anomaly_id", incident_id)
        .execute()
    )

    # Fetch the compliance report (one per anomaly)
    report_resp = (
        supabase
        .table("compliance_reports")
        .select("*")
        .eq("anomaly_id", incident_id)
        .execute()
    )
    compliance_report = report_resp.data[0] if report_resp.data else None

    return {
        "anomaly_id": incident_id,
        "news_contexts": news_resp.data,
        "compliance_report": compliance_report,
    }

from fastapi import Header

@app.post("/api/v1/engine/trigger")
def trigger_engine(x_trigger_key: str = Header(None)):
    if x_trigger_key != os.getenv("TRIGGER_SECRET"):
        raise HTTPException(status_code=403, detail="Forbidden")
    """
    Synchronously calls **run_orchestrator()** from run_engine.py.
    Returns success/failure with any error message.
    """
    try:
        from run_engine import run_orchestrator
        run_orchestrator()
        return {"status": "success", "message": "Pipeline completed successfully."}
    except SystemExit as exc:
        # run_orchestrator() calls sys.exit(1) on fatal errors
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline exited with code {exc.code}.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# FastAPI app: entry point that wires together routers, middleware, and startup events
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from routers import case_studies, submissions, critiques
# Load .env variables (SUPABASE_URL, SUPABASE_SERVICE_KEY)
load_dotenv()

app = FastAPI(
    title="Global Governance & Compliance Engine API",
    description="Surfaces network anomaly incidents and AI-generated compliance reports.",
    version="0.1.0",
)

# -----------------------------------------------------------------
# Routers
# -----------------------------------------------------------------
app.include_router(case_studies.router)
app.include_router(submissions.router)
app.include_router(critiques.router)

# -----------------------------------------------------------------
# CORS — allow local Next.js dev server
# -----------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------
# Supabase client (service key — read + write)
# -----------------------------------------------------------------
def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in environment.")
    return create_client(url, key)


# -----------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------

@app.get("/api/v1/incidents", summary="List recent anomaly events")
def list_incidents():
    """
    Returns the 10 most recent rows from **anomaly_events**,
    ordered by timestamp descending.
    """
    supabase = get_supabase()
    response = (
        supabase
        .table("anomaly_events")
        .select("*")
        .order("timestamp", desc=True)
        .limit(10)
        .execute()
    )
    return {"incidents": response.data}


@app.get(
    "/api/v1/incidents/{incident_id}/report",
    summary="Get news context + compliance report for one incident",
)
def get_incident_report(incident_id: str):
    """
    Returns all **news_contexts** rows and the single **compliance_reports**
    row that belong to the given anomaly_id (UUID).
    Raises 404 if the anomaly does not exist.
    """
    supabase = get_supabase()

    # Verify the incident exists
    incident_resp = (
        supabase
        .table("anomaly_events")
        .select("id")
        .eq("id", incident_id)
        .execute()
    )
    if not incident_resp.data:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")

    # Fetch related news context rows
    news_resp = (
        supabase
        .table("news_contexts")
        .select("*")
        .eq("anomaly_id", incident_id)
        .execute()
    )

    # Fetch the compliance report (one per anomaly)
    report_resp = (
        supabase
        .table("compliance_reports")
        .select("*")
        .eq("anomaly_id", incident_id)
        .execute()
    )
    compliance_report = report_resp.data[0] if report_resp.data else None

    return {
        "anomaly_id": incident_id,
        "news_contexts": news_resp.data,
        "compliance_report": compliance_report,
    }


from fastapi import Header

@app.post("/api/v1/engine/trigger")
def trigger_engine(x_trigger_key: str = Header(None)):
    if x_trigger_key != os.getenv("TRIGGER_SECRET"):
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        from run_engine import run_orchestrator
        run_orchestrator()
        return {"status": "success", "message": "Pipeline completed successfully."}
    except SystemExit as exc:
        # run_orchestrator() calls sys.exit(1) on fatal errors
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline exited with code {exc.code}.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))