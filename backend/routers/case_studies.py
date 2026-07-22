from fastapi import APIRouter, HTTPException
from core.supabase_client import supabase

router = APIRouter(prefix="/api/v1/case-studies", tags=["case-studies"])

@router.get("/{case_study_id}")
def get_case_study(case_study_id: str):
    try:
        # Pull everything at once using PostgREST relation embedding
        resp = supabase.table("case_studies").select(
            "*, "
            "timeline_events(*), "
            "legal_references(*), "
            "media_items(*), "
            "historical_outcomes(*)"
        ).eq("id", case_study_id).execute()
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid query or UUID format: {str(e)}")

    if not resp.data:
        raise HTTPException(status_code=404, detail=f"Case study '{case_study_id}' not found.")

    # Extract the main case study row
    data = resp.data[0]

    # Pull children lists out of the payload object
    timeline = data.pop("timeline_events", [])
    # PostgREST embedding order can vary; sort in memory by timestamp
    timeline.sort(key=lambda x: x.get("event_timestamp", ""))

    legal_refs = data.pop("legal_references", [])
    media = data.pop("media_items", [])
    
    # Safely pop out the 1:1 historical outcome record
    outcomes = data.pop("historical_outcomes", [])
    if isinstance(outcomes, list):
        historical_outcome = outcomes[0] if outcomes else None
    else:
        # If Supabase infers a 1:1 relation, it returns a dict directly instead of a list
        historical_outcome = outcomes or None

    return {
        "case_study": data,
        "timeline_events": timeline,
        "legal_references": legal_refs,
        "media_items": media,
        "historical_outcome": historical_outcome,
    }