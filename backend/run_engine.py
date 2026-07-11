import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Import functions from your existing modules
from scraper import fetch_ooni_anomalies, normalize_ooni_result, fetch_gdelt_headlines
from oracle import generate_compliance_brief

# Load database keys and API secrets from .env
load_dotenv()

def run_orchestrator():
    print("🚀 Initializing Global Governance & Compliance Pipeline...")
    
    # 1. Initialize Supabase Admin Connection Session
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Missing Supabase database credentials in environment configuration.")
        sys.exit(1)
        
    supabase = create_client(supabase_url, supabase_key)

    # Hardcoded target country for locked MVP scope (Iran)
    target_country = "IR"

    # 2. Ingest & Normalize Technical Network Anomaly Footprints
    print(f"📡 Fetching raw network telemetry from OONI for country: {target_country}...")
    try:
        raw_anomalies = fetch_ooni_anomalies(target_country, hours=24)
        if not raw_anomalies:
            print("🛑 No network anomalies detected in the last 24 hours. Pipeline idling safely.")
            return
            
        # Target the most recent anomaly signature
        normalized_anomaly = normalize_ooni_result(raw_anomalies[0])
        print(f"✅ Target Anomaly Isolated: {normalized_anomaly['target_app']} via {normalized_anomaly['failure_type']}")
    except Exception as e:
        print(f"❌ Failed to fetch telemetry from OONI API: {e}")
        sys.exit(1)

    # 3. Ingest Contextual Real-World News Media Channels
    print(f"📰 Querying GDELT context matching country timeline: {target_country}...")
    try:
        raw_articles = fetch_gdelt_headlines(target_country, max_records=3)
        normalized_news = [
            {"headline": a["title"], "source_url": a["url"]} 
            for a in raw_articles
        ]
        print(f"✅ Context Synced: Gathered {len(normalized_news)} live validation headlines.")
    except Exception as e:
        print(f"⚠️ Warning: GDELT tracking rate limited or offline ({e}). Proceeding with empty context context.")
        normalized_news = []

    # 4. Generate AI Prescriptive Policy Brief & Legal Treaty Audit
    print("🧠 Dispatching aggregated timeline variables to Compliance Oracle...")
    try:
        ai_brief = generate_compliance_brief(normalized_anomaly, normalized_news)
        print("✅ Analysis Complete: Autonomous treaty compliance brief successfully generated.")
    except Exception as e:
        print(f"❌ Oracle Generation Failure: {e}")
        sys.exit(1)

    # 5. Execute Sequence Database Insertions (Relational Mapping)
    print("\n💾 Committing pipeline output rows to Supabase Cloud Cluster...")
    
    try:
        # Step A: Insert the core Technical Anomaly Event record
        anomaly_insert = supabase.table("anomaly_events").insert(normalized_anomaly).execute()
        anomaly_id = anomaly_insert.data[0]["id"]
        print(f"   -> [anomaly_events]: Row created successfully. Assigned ID: {anomaly_id}")

        # Step B: Insert matching News Context entries bound to the Anomaly via Foreign Key
        if normalized_news:
            news_rows = [
                {
                    "anomaly_id": anomaly_id,
                    "headline": item["headline"],
                    "source_url": item["source_url"]
                }
                for item in normalized_news
            ]
            supabase.table("news_contexts").insert(news_rows).execute()
            print(f"   -> [news_contexts]: Committed {len(news_rows)} rows tied to Anomaly ID.")
        else:
            print("   -> [news_contexts]: Skipped insertion (no context articles fetched).")

        # Step C: Insert the AI synthesized Compliance Report bound to the Anomaly
        report_row = {
            "anomaly_id": anomaly_id,
            "treaties_violated": ai_brief["treaties_violated"],
            "tactical_solution": ai_brief["tactical_solution"],
            "policy_reform": ai_brief["policy_reform"]
        }
        supabase.table("compliance_reports").insert(report_row).execute()
        print("   -> [compliance_reports]: Committed analytical summary row successfully.")
        
        print("\n🎉 End-to-End Pipeline Execution Finished Successfully.")
        
    except Exception as e:
        print(f"❌ Database Transaction Refusal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_orchestrator()