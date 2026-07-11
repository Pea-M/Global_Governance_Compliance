import requests
from datetime import datetime, timedelta, timezone
# temporary, don't leave this in scraper.py permanently
from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
COUNTRY_CODE_ISO = "IR"
COUNTRY_CODE_FIPS = "IR"

APP_NAMES = {
    "signal": "Signal",
    "telegram": "Telegram",
    "facebook_messenger": "Facebook Messenger",
    "whatsapp": "WhatsApp",
    "web_connectivity": "Website",
}


def fetch_ooni_anomalies(country_code: str, hours: int = 24) -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%d")
    url = "https://api.ooni.io/api/v1/measurements"
    params = {"probe_cc": country_code, "anomaly": "true", "since": since, "limit": 100}
    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code != 200:
        print("OONI error response:", resp.text)
    resp.raise_for_status()
    return resp.json()["results"]


def normalize_ooni_result(m: dict) -> dict:
    test_name = m.get("test_name", "unknown")
    target_app = APP_NAMES.get(test_name, test_name)

    scores = m.get("scores", {})
    failure_type = "unknown"
    for key, val in scores.items():
        if key.endswith("_failure") and val:
            failure_type = val
            break
        if key.endswith("_dns_blocking") and val is True:
            failure_type = "dns_blocking"
            break

    return {
        "timestamp": m.get("measurement_start_time"),
        "country_code": m.get("probe_cc"),
        "failure_type": failure_type,
        "target_app": target_app,
    }


import time # <--- ADD THIS

def fetch_gdelt_headlines(country_code_fips: str, max_records: int = 5) -> list[dict]:
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    # Adding a header to identify as a browser, which reduces block probability
    headers = {'User-Agent': 'Mozilla/5.0'} 
    params = {
        "query": f"sourcecountry:{country_code_fips}",
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "timespan": "24h",
    }
    # Pass the headers here
    resp = requests.get(url, params=params, headers=headers, timeout=20)
    
    if resp.status_code == 429:
        print("⚠️ GDELT Rate limited! Sleeping for 10 seconds...")
        time.sleep(10) # Wait 10 seconds and retry
        resp = requests.get(url, params=params, headers=headers, timeout=20)
        
    resp.raise_for_status()
    return resp.json().get("articles", [])


if __name__ == "__main__":
    print("=== OONI anomalies (normalized validation) ===")
    ooni_data = fetch_ooni_anomalies(COUNTRY_CODE_ISO)
    print(f"{len(ooni_data)} raw results fetched.")
    normalized = [normalize_ooni_result(m) for m in ooni_data]
    if normalized:
        print("Sample normalized output:", normalized[0])

    print("\n=== GDELT headlines (validation) ===")
    gdelt_data = fetch_gdelt_headlines(COUNTRY_CODE_FIPS)
    print(f"{len(gdelt_data)} live results fetched.")