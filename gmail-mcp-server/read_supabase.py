from supabase import create_client


SUPABASE_URL = "https://ooaebqrtzlnuhhaqxilf.supabase.co"

SUPABASE_KEY = "sb_secret_cxcWocGujmZYrVievmy5aw_txA4GAcZ"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

response = (
    supabase.table("llm_investigation_log")
    .select("*")
    .order("created_at", desc=True)
    .limit(1)
    .execute()
)

print(response.data)