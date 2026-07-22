# core/supabase_client.py
# Shared Supabase client instance used across all modules.
# Implementation begins in Phase 1.
import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Load database keys from your backend environment variables
load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

if not supabase_url or not supabase_key:
    print("❌ Error: Missing Supabase database credentials in environment configuration.")
    sys.exit(1)

# Export this instance globally
supabase = create_client(supabase_url, supabase_key)