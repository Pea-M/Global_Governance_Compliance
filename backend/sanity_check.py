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
# import os
# from dotenv import load_dotenv

# # This loads your .env file
# load_dotenv()

# # This checks if the keys are actually being seen by the python interpreter
# supabase_url = os.getenv("SUPABASE_URL")
# gemini_key = os.getenv("GEMINI_API_KEY")

# if supabase_url and gemini_key:
#     print("✅ Environment is READY. All keys detected.")
# else:
#     print("❌ Environment is NOT DONE. Check your .env file.")