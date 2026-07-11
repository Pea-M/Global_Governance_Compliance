import os
import json
import google.generativeai as genai
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
    treaties_violated: list[str] = Field(description="List of strings identifying specific laws violated, e.g., ['UN Article 19', 'UNDP SDG Target 16.10']")
    tactical_solution: str = Field(description="Clear, practical, highly actionable local workaround instructions for citizens or businesses to bypass this technical drop.")
    policy_reform: str = Field(description="Strategic, high-level governance structural recommendations auditing the implementation gap and actions needed.")

def generate_compliance_brief(anomaly: dict, headlines: list[dict]) -> dict:
    """
    Takes a normalized anomaly event and matching GDELT news context,
    cross-references them with international treaties, and returns a structured AI audit.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing GEMINI_API_KEY in environment variables.")
    
    genai.configure(api_key=api_key)
    
    # Format inputs for the prompt
    news_text = "\n".join([f"- Title: {h.get('headline')} (Source: {h.get('source_url')})" for h in headlines])
    treaties_text = json.dumps(TREATY_FRAMEWORKS, indent=2)
    
    prompt = f"""
    You are an expert Autonomous Geopolitical Risk & International Law Compliance AI.
    Your task is to analyze a technical digital network anomaly against ongoing regional context and international frameworks.

    === TECHNICAL ANOMALY DETECTED ===
    Target Application: {anomaly.get('target_app')}
    Failure Type Identified: {anomaly.get('failure_type')}
    Country Boundary: {anomaly.get('country_code')}
    Timestamp: {anomaly.get('timestamp')}

    === LIVE GEOPOLITICAL HEADLINES CONTEXTUALIZATION ===
    {news_text}

    === INTERNATIONAL TREATY REFERENCE MATRIX ===
    {treaties_text}

    === MANDATORY ANALYSIS INSTRUCTIONS ===
    1. Determine if the technical failure type combined with the local context constitutes a violation of the referenced international laws.
    2. Synthesize a practical, immediate 'tactical_solution' explaining how an enterprise or user on the ground can bypass or mitigate this block (e.g., specific routing, decentralized protocols, alternate tooling).
    3. Generate a macro-level governance and policy critique ('policy_reform') indicating what oversight rules have failed and what remediation is required.
    4. Guardrail: Rely strictly on the technical data and news context provided. Avoid generic conversational fluff.
    """

    # Using Gemini 1.5 Flash for fast, structured output
    model = genai.GenerativeModel("gemini-3.5-flash")
    
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": ComplianceAnalysis,
        }
    )
    
    # Return the clean, validated JSON dictionary
    return json.loads(response.text)

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