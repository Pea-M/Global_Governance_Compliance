# import os
# from dotenv import load_dotenv
# from supabase import create_client

# load_dotenv()

# url = os.environ["SUPABASE_URL"]
# key = os.environ["SUPABASE_SERVICE_KEY"]

# supabase = create_client(url, key)

# # Insert one dummy row
# insert_result = supabase.table("anomaly_events").insert({
#     "country_code": "IR",
#     "failure_type": "dns_tampering",
#     "target_app": "WhatsApp",
# }).execute()

# print("Inserted:", insert_result.data)

# # Read it back
# read_result = supabase.table("anomaly_events").select("*").execute()
# print("Current rows:", read_result.data)