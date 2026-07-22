import os
import json
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# 1. Hardcoded Treaty Framework (Static Context)
TREATY_FRAMEWORKS = [
    {
        "id": "UN_ART_19",
        "name": "UN Universal Declaration of Human Rights",
        "article": "Article 19",
        "description": "Everyone has the right to freedom of opinion and expression; this right includes freedom to hold opinions without interference and to seek, receive and impart information and ideas through any media and regardless of frontiers."
    },
    {
        "id": "UNDP_SDG_16_10",
        "name": "UNDP Sustainable Development Goals",
        "article": "Target 16.10",
        "description": "Ensure public access to information and protect fundamental freedoms, in accordance with national legislation and international agreements."
    }
]

# 2. Enforce Strict Output Format for Supabase
class ComplianceAnalysis(BaseModel):
    treaties_violated: list[str] = Field(
        description="Each entry cites a specific treaty/article and frames it with historical precedent and real-world impact — written as an expert analyst would, not a bare legal label."
    )
    tactical_solution: str = Field(
        description="Grounded, specific, actionable real-world guidance, written in expert analytical prose, not a generic checklist."
    )
    policy_reform: str = Field(
        description="A closing analytical narrative connecting historical pattern, the current incident, and a forward-looking policy recommendation — read like the final section of an intelligence briefing memo."
    )

from google import genai
from google.genai import types

import time

def generate_compliance_brief(anomaly: dict, headlines: list[dict], max_retries: int = 3) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")

    client = genai.Client(api_key=api_key)

    news_text = "\n".join([f"- Title: {h.get('headline')} (Source: {h.get('source_url')})" for h in headlines])
    treaties_text = json.dumps(TREATY_FRAMEWORKS, indent=2)

    prompt = f"""
You are a senior international correspondent and digital-rights analyst —
the kind who has spent years covering internet governance and censorship
for an outlet like Reuters or The Economist. You are writing a briefing
for policy makers and risk analysts. Write with real analytical voice and
judgment. Do not sound like a compliance checklist or an automated system.

=== INCIDENT SNAPSHOT ===
Target Application: {anomaly.get('target_app')}
Failure Type: {anomaly.get('failure_type')}
Country: {anomaly.get('country_code')}
Detected: {anomaly.get('timestamp')}

=== TODAY'S ON-THE-GROUND HEADLINES ===
{news_text}

=== TREATY FRAMEWORK REFERENCE ===
{treaties_text}

=== YOUR BRIEFING TASK ===
Connect today's technical signal to the larger story — this is a briefing,
not a snapshot.

1. treaties_violated: For each law or article implicated, frame it with
   precedent, not just a citation. Note the broader pattern this fits
   (e.g. how this kind of app-specific throttling has historically been used
   around moments of unrest or political sensitivity in this country), and
   briefly note the real-world harm this kind of blocking tends to cause —
   cut-off communication during protests, disrupted independent reporting,
   families unable to reach each other.

2. tactical_solution: Practical, specific, ground-level guidance — actual
   tools or protocols a person or business could use right now, not a
   generic "use a VPN."

3. policy_reform: Write this like the closing section of a real briefing
   memo — the arc from historical pattern, to today's incident, to what's
   likely next, and what concrete oversight change would actually alter
   that trajectory.

Guardrails:
- Ground every specific, checkable claim in what's provided above (this
  incident's data, today's headlines).
- You may draw on broadly known historical patterns to give this real
  analytical depth, but never invent specific dates, statistics, or direct
  quotes you are not confident are accurate. If you're not certain of a
  specific detail, speak to the general pattern rather than a fabricated
  instance.
- Write in flowing, analytical prose. No bullet-point robotic language,
  no "in conclusion," no generic filler.
"""
    last_error = None
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ComplianceAnalysis,
                ),
            )
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                wait = 5 * (attempt + 1)
                print(f"⚠️ Gemini call failed (attempt {attempt+1}/{max_retries}): {e}. Retrying in {wait}s...")
                time.sleep(wait)
    assert last_error is not None
    raise last_error


# =====================================================================
# TESTING BLOCK: Runs only if you execute `python oracle.py` directly
# =====================================================================
if __name__ == "__main__":
    print("🚀 Booting Oracle Offline Test...")
    
    try:
        with open("mock_data.json", "r") as f:
            mock_data = json.load(f)
            
        print("✅ Loaded mock_data.json successfully. Pinging Gemini API...")
        
        # Pass the mock data into your function
        ai_brief = generate_compliance_brief(
            anomaly=mock_data["anomaly"], 
            headlines=mock_data["headlines"]
        )
        
        print("\n🧠 === AI COMPLIANCE REPORT GENERATED ===")
        print(json.dumps(ai_brief, indent=2))
        print("========================================")
        
    except FileNotFoundError:
        print("❌ Could not find mock_data.json. Make sure it is in the same folder.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")