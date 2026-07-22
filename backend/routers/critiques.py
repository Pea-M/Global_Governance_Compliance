# routers/critiques.py
# FastAPI router for AI critique retrieval endpoints.
# Implementation begins in Phase 1.
from fastapi import APIRouter, HTTPException
from core.supabase_client import supabase
from core.critique_engine import generate_critique

router = APIRouter(prefix="/api/v1/critiques", tags=["critiques"])


def _fetch_case_bundle(case_study_id: str):
    case_resp = supabase.table("case_studies").select("*").eq("id", case_study_id).execute()
    if not case_resp.data:
        raise HTTPException(status_code=404, detail=f"Case study '{case_study_id}' not found.")
    legal_resp = supabase.table("legal_references").select("*").eq("case_study_id", case_study_id).execute()
    outcome_resp = supabase.table("historical_outcomes").select("*").eq("case_study_id", case_study_id).execute()
    historical_outcome = outcome_resp.data[0] if outcome_resp.data else None
    return case_resp.data[0], legal_resp.data, historical_outcome


@router.post("/generate/{submission_id}")
def generate_and_store_critique(submission_id: str):
    sub_resp = supabase.table("submissions").select("*").eq("id", submission_id).execute()
    if not sub_resp.data:
        raise HTTPException(status_code=404, detail=f"Submission '{submission_id}' not found.")
    submission = sub_resp.data[0]

    case_study, legal_references, historical_outcome = _fetch_case_bundle(submission["case_study_id"])

    try:
        critique = generate_critique(submission, case_study, legal_references, historical_outcome)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Critique generation failed: {e}")

    row = {
        "submission_id": submission_id,
        "summary_of_user_idea": critique["summary_of_user_idea"],
        "future_prediction": critique["future_prediction"],
        "pros_cons_additions_deletions": critique["pros_cons_additions_deletions"],
        "comparison_to_reality": critique.get("reality_comparison"),
    }
    insert_resp = supabase.table("ai_critiques").upsert(row, on_conflict="submission_id").execute()
    return {"status": "success", "critique": insert_resp.data[0]}


@router.get("/{submission_id}")
def get_critique(submission_id: str):
    resp = supabase.table("ai_critiques").select("*").eq("submission_id", submission_id).execute()
    if not resp.data:
        raise HTTPException(status_code=404, detail="No critique found for this submission.")
    return resp.data[0]