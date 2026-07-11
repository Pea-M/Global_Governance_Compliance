# OONI + GDELT fetchers: pulls raw censorship signals and matching news headlines
import requests
from datetime import datetime, timedelta, timezone

COUNTRY_CODE_ISO = "IR"    # matches OONI + your Supabase schema
COUNTRY_CODE_FIPS = "IR"   # matches GDELT — override if not Iran, see note above


def fetch_ooni_anomalies(country_code: str, hours: int = 24) -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%d")
    url = "https://api.ooni.io/api/v1/measurements"
    params = {
        "probe_cc": country_code,
        "anomaly": "true",
        "since": since,
        "limit": 100,
    }
    resp = requests.get(url, params=params, timeout=20)
    if resp.status_code != 200:
        print("OONI error response:", resp.text)
    resp.raise_for_status()
    return resp.json()["results"]

def fetch_gdelt_headlines(country_code_fips: str, max_records: int = 5) -> list[dict]:
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": f"sourcecountry:{country_code_fips}",
        "mode": "artlist",
        "maxrecords": max_records,
        "format": "json",
        "timespan": "24h",
    }
    resp = requests.get(url, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("articles", [])


if __name__ == "__main__":
    print("=== OONI anomalies ===")
    ooni_data = fetch_ooni_anomalies(COUNTRY_CODE_ISO)
    print(f"{len(ooni_data)} results")
    for m in ooni_data[:3]:
        print(m)

    print("\n=== GDELT headlines ===")
    gdelt_data = fetch_gdelt_headlines(COUNTRY_CODE_FIPS)
    print(f"{len(gdelt_data)} results")
    for a in gdelt_data[:3]:
        print(a)