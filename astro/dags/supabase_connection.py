from supabase import create_client
import pandas as pd
import numpy as np

SUPABASE_URL = "https://ooaebqrtzlnuhhaqxilf.supabase.co"

SUPABASE_KEY = "sb_secret_cxcWocGujmZYrVievmy5aw_txA4GAcZ"

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)