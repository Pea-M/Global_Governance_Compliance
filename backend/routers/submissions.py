# routers/submissions.py
# FastAPI router for user submission endpoints.
# Implementation begins in Phase 1.
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from core.supabase_client import supabase

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])

# 1. Define the Expected Frontend Payload
class SubmissionCreate(BaseModel):
    case_study_id: str = Field(..., description="UUID of the parent case study")
    user_id: str = Field(..., description="UUID of the user submitting the analysis")
    own_analysis: str
    immediate_action: List[str]
    problem_highlights: List[str]
    constitutional_refs: List[str]
    policy_reforms: List[str]

# 2. Define the POST Route
@router.post("/")
def create_submission(payload: SubmissionCreate):
    try:
        # payload.model_dump() converts the Pydantic object into a native Python dictionary.
        # FastAPI handles the conversion of Python Lists to JSONB automatically for Supabase.
        insert_data = payload.model_dump()
        
        # Execute the insert
        resp = supabase.table("submissions").insert(insert_data).execute()
        
        if not resp.data:
            raise HTTPException(status_code=400, detail="Failed to save submission to the database.")
            
        created_submission = resp.data[0]
        
        return {
            "status": "success",
            "message": "Submission recorded successfully.",
            "submission_id": created_submission["id"],
            "data": created_submission
        }
        
    except Exception as e:
        # This will catch Foreign Key constraint errors 
        # (e.g., if the frontend sends a fake case_study_id or user_id)
        error_msg = str(e)
        if "foreign key constraint" in error_msg.lower():
            raise HTTPException(status_code=400, detail="Invalid Case Study ID or User ID.")
        
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {error_msg}")


# 3. (Optional) Define a GET Route to fetch a specific submission
@router.get("/{submission_id}")
def get_submission(submission_id: str):
    try:
        resp = supabase.table("submissions").select("*").eq("id", submission_id).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request format.")
        
    if not resp.data:
        raise HTTPException(status_code=404, detail=f"Submission '{submission_id}' not found.")
        
    return resp.data[0]
# add to routers/submissions.py
@router.get("/case-study/{case_study_id}")
def list_submissions_for_case(case_study_id: str):
    resp = (
        supabase.table("submissions")
        .select("id, own_analysis, created_at")
        .eq("case_study_id", case_study_id)
        .order("created_at", desc=True)
        .execute()
    )
    return {"submissions": resp.data}