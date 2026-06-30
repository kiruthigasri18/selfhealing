import pandas as pd
from supabase_connection import supabase


def raw_summary_task(raw_table_name):

    response = (
        supabase
        .table(raw_table_name)
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