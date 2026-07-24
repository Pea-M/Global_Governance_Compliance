# routers/drafts.py
# Phase 4 — Authenticated draft autosave endpoints.
# Allows a signed-in user to save/restore their in-progress form before submitting.

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, Any, Dict
from core.supabase_client import supabase
from core.auth import get_user_id_from_token as _get_user_id_from_token

router = APIRouter(prefix="/api/v1/drafts", tags=["drafts"])


# ------------------------------------------------------------------
# Pydantic schemas
# ------------------------------------------------------------------
class DraftUpsert(BaseModel):
    case_study_id: str
    form_data: Dict[str, Any]  # The raw JSON of the form fields


# ------------------------------------------------------------------
# GET /api/v1/drafts/
# List all active drafts for the authenticated user (used by profile page)
# ------------------------------------------------------------------
@router.get("/")
def list_drafts(authorization: Optional[str] = Header(None)):
    user_id = _get_user_id_from_token(authorization)

    resp = (
        supabase.table("drafts")
        .select("*")
        .eq("user_id", user_id)
        .order("updated_at", desc=True)
        .execute()
    )
    return {"drafts": resp.data}


# ------------------------------------------------------------------
# GET /api/v1/drafts/{case_study_id}
# Fetch the user's current draft for a given case study
# ------------------------------------------------------------------
@router.get("/{case_study_id}")
def get_draft(case_study_id: str, authorization: Optional[str] = Header(None)):
    user_id = _get_user_id_from_token(authorization)

    resp = (
        supabase.table("drafts")
        .select("*")
        .eq("user_id", user_id)
        .eq("case_study_id", case_study_id)
        .order("updated_at", desc=True)
        .limit(1)
        .execute()
    )

    if not resp.data:
        return {"draft": None}

    return {"draft": resp.data[0]}


# ------------------------------------------------------------------
# POST /api/v1/drafts/
# Upsert (create or update) the user's draft for a given case study
# ------------------------------------------------------------------
@router.post("/")
def upsert_draft(payload: DraftUpsert, authorization: Optional[str] = Header(None)):
    user_id = _get_user_id_from_token(authorization)

    # Check if a draft already exists for this user + case study
    existing = (
        supabase.table("drafts")
        .select("id")
        .eq("user_id", user_id)
        .eq("case_study_id", payload.case_study_id)
        .limit(1)
        .execute()
    )

    if existing.data:
        # Update the existing draft
        draft_id = existing.data[0]["id"]
        resp = (
            supabase.table("drafts")
            .update({"form_data": payload.form_data})
            .eq("id", draft_id)
            .execute()
        )
    else:
        # Create a new draft
        resp = (
            supabase.table("drafts")
            .insert({
                "user_id": user_id,
                "case_study_id": payload.case_study_id,
                "form_data": payload.form_data,
            })
            .execute()
        )

    if not resp.data:
        raise HTTPException(status_code=500, detail="Failed to save draft.")

    return {"status": "saved", "draft": resp.data[0]}


# ------------------------------------------------------------------
# DELETE /api/v1/drafts/{case_study_id}
# Clear draft after a successful submission
# ------------------------------------------------------------------
@router.delete("/{case_study_id}")
def delete_draft(case_study_id: str, authorization: Optional[str] = Header(None)):
    user_id = _get_user_id_from_token(authorization)

    supabase.table("drafts").delete().eq("user_id", user_id).eq("case_study_id", case_study_id).execute()
    return {"status": "deleted"}
