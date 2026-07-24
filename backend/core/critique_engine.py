# core/critique_engine.py
# Shared AI critique logic called by all category modules.
# Reuses the oracle.py pattern from v1 (constrained prompt + enforced schema).
# Implementation begins in Phase 1.
import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class ProsConsAnalysis(BaseModel):
    pros: list[str] = Field(description="Genuine strengths of the user's proposed response")
    cons: list[str] = Field(description="Genuine weaknesses, risks, or gaps in the user's proposed response")
    additions: list[str] = Field(description="Specific things missing from the plan that should be added")
    deletions: list[str] = Field(description="Specific things in the plan that should be cut or reconsidered")


class CritiqueAnalysis(BaseModel):
    summary_of_user_idea: str = Field(description="A brief, neutral restatement of what the user proposed")
    future_prediction: str = Field(
        description="A grounded narrative forecast of likely consequences if this plan were enacted. "
                    "Never a numeric score or single-word label."
    )
    pros_cons_additions_deletions: ProsConsAnalysis
    reality_comparison: str | None = Field(
        default=None,
        description="Only populate if a documented historical outcome was provided. A narrative "
                    "comparison of the user's plan against what actually happened — where it aligns, "
                    "where it diverges. Leave null if the case is still ongoing."
    )


def _format_legal_references(legal_refs: list[dict]) -> str:
    if not legal_refs:
        return "No specific legal references were recorded for this case study."
    return "\n".join(
        f"- [{r.get('ref_type', 'reference')}] {r.get('title')}: {r.get('description', '')}"
        for r in legal_refs
    )


def _format_historical_outcome(outcome: dict | None) -> str:
    if not outcome:
        return "NONE — this case is still ongoing. No real-world outcome exists yet."
    parts = []
    if outcome.get("immediate_actions"):
        parts.append("Immediate actions actually taken: " + "; ".join(outcome["immediate_actions"]))
    if outcome.get("committees_formed"):
        parts.append("Bodies actually formed: " + "; ".join(outcome["committees_formed"]))
    if outcome.get("final_reforms"):
        parts.append("Reforms actually enacted: " + "; ".join(outcome["final_reforms"]))
    if outcome.get("after_effects"):
        parts.append("Documented after-effects: " + "; ".join(outcome["after_effects"]))
    return "\n".join(parts) if parts else "Outcome record exists but is empty."


def generate_critique(
    submission: dict,
    case_study: dict,
    legal_references: list[dict],
    historical_outcome: dict | None,
    max_retries: int = 3,
) -> dict:
    """
    Guardrails (PLANNING.md Section 2.9):
    - Grounded strictly in the submission + legal references + historical outcome given.
    - Never a bare numeric score — always narrative + structured pros/cons/additions/deletions.
    - reality_comparison stays null unless the case is genuinely resolved with real outcome data.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")

    client = genai.Client(api_key=api_key)
    is_resolved = case_study.get("status") == "resolved" and historical_outcome is not None

    prompt = f"""
You are a senior policy analyst and historian reviewing a proposed governance
response to a real crisis. Write with genuine analytical judgment — do not
sound like a checklist or a scoring system. Never invent facts beyond what
is given below.

=== THE CASE ===
Title: {case_study.get('title')}
Category: {case_study.get('category')}
Status: {case_study.get('status')}
Cause: {case_study.get('cause')}
Location: {case_study.get('location')}
People Affected: {case_study.get('affected')}

=== LEGAL / JURISDICTIONAL FRAMEWORK IN FORCE AT THE TIME ===
{_format_legal_references(legal_references)}

=== THE USER'S PROPOSED RESPONSE ===
Own analysis: {submission.get('own_analysis')}
Immediate action: {"; ".join(submission.get('immediate_action', []))}
Problem highlights: {"; ".join(submission.get('problem_highlights', []))}
Constitutional/legal references the user cited: {"; ".join(submission.get('constitutional_refs', []))}
Policy reforms proposed: {"; ".join(submission.get('policy_reforms', []))}

=== DOCUMENTED REAL-WORLD OUTCOME ===
{_format_historical_outcome(historical_outcome)}

=== YOUR TASK ===
1. summary_of_user_idea — neutrally restate what the user proposed.
2. future_prediction — a grounded narrative forecast of what would likely
   follow from this plan, given the case's actual context. Prose, not a label.
3. pros_cons_additions_deletions — specific, genuine pros, cons, additions
   (what's missing), and deletions (what should be cut/reconsidered).
4. reality_comparison — {"compare the user's plan against the documented real outcome above: where it aligns, where it diverges, what that suggests." if is_resolved else "leave this null. This case is still ongoing — there is no real outcome to compare against. Do not invent one."}

Guardrail: only cite legal references and outcome facts actually given above.
If unsure of a specific detail, speak to the general pattern rather than
fabricating a specific.
"""

    last_error = None
    import time
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=CritiqueAnalysis,
                ),
            )
            result = json.loads(response.text)
            if not is_resolved:
                result["reality_comparison"] = None
            return result
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"⚠️ Gemini call failed (attempt {attempt+1}/{max_retries}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
    raise last_error or RuntimeError("Generative call failed mysteriously with no exception caught.")