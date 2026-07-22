import json
import os
import sys

# Append parent directories to path so Python can find core modules easily
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.supabase_client import supabase

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "../db/fixtures/core_fixtures.json")

def run_seeder():
    print("🚀 Connecting to Supabase API to seed fixtures...")
    
    if not os.path.exists(FIXTURE_PATH):
        print(f"❌ Error: Cannot find fixture template at: {FIXTURE_PATH}")
        sys.exit(1)
        
    with open(FIXTURE_PATH, "r") as f:
        fixtures = json.load(f)

    try:
        
                
        # --- LEVEL 1: Independent Roots ---
        if "anomaly_events" in fixtures and fixtures["anomaly_events"]:
            print("📦 Upserting technical anomaly footprints...")
            supabase.table("anomaly_events").upsert(fixtures["anomaly_events"]).execute()
    
        if "case_studies" in fixtures and fixtures["case_studies"]:
            print("📦 Upserting baseline case studies...")
            supabase.table("case_studies").upsert(fixtures["case_studies"]).execute()

# --- LEVEL 2: Dependents ---
        level_2_tables = [
        "news_contexts", 
        "compliance_reports", 
        "timeline_events", 
        "legal_references", 
        "media_items", 
        "historical_outcomes", 
        "submissions"
    ]
        for table in level_2_tables:
            if table in fixtures and fixtures[table]:
                print(f"📦 Upserting relational dependents into [{table}]...")
                supabase.table(table).upsert(fixtures[table]).execute()

    # --- LEVEL 3: Grandchildren ---
    
        if "ai_critiques" in fixtures and fixtures["ai_critiques"]:
            print("📦 Upserting engine evaluations into [ai_critiques]...")
            supabase.table("ai_critiques").upsert(fixtures["ai_critiques"]).execute()

        print("🎉 Successfully pushed all local fixtures to Supabase Cloud!")

    except Exception as e:
        print(f"❌ Database Transaction Refused: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_seeder()