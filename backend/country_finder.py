# import requests
# from datetime import datetime, timedelta, timezone

# CANDIDATES = ["IR", "RU", "MM", "CU", "BY", "PK", "SD", "ET", "VE", "EG", "TR", "IN"]

# def count_ooni_anomalies(cc: str, days: int = 5) -> int:
#     since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
#     url = "https://api.ooni.io/api/v1/measurements"
#     params = {"probe_cc": cc, "anomaly": "true", "since": since, "limit": 1000}
#     resp = requests.get(url, params=params, timeout=20)
#     if resp.status_code != 200:
#         return -2  # API error, distinct from a real zero
#     meta = resp.json().get("metadata", {})
#     count = meta.get("count", -1)
#     if count == -1:
#         return 1000  # still overflowing even at this window -> very high volume, cap for display
#     return count

# if __name__ == "__main__":
#     results = [(cc, count_ooni_anomalies(cc)) for cc in CANDIDATES]
#     results.sort(key=lambda x: x[1], reverse=True)

#     print(f"{'Country':<10}{'Anomalies (5d)'}")
#     for cc, n in results:
#         flag = "  <- API ERROR" if n == -2 else ("  <- 1000+" if n == 1000 else "")
#         print(f"{cc:<10}{n}{flag}")