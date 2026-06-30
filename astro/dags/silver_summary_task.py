import pandas as pd
from supabase_connection import supabase


def silver_summary_task(table_name):

    response = (
        supabase
        .table(table_name)
        .select("*")
        .limit(100)
        .execute()
    )

    df = pd.DataFrame(response.data)

    summary = df.describe(
        include="all"
    ).fillna("").to_string()

    sample = df.head(
        10
    ).fillna("").to_dict("records")

    return {
        "summary": summary,
        "sample": sample
    }