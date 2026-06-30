from supabase_connection import supabase


def store_result_task(
        transformation_name,
        issue_type,
        root_cause,
        recommendation,
        confidence,
        severity,
        business_impact,
        action):

    row = {

        "transformation_name": transformation_name,

        "issue_type": issue_type,

        "root_cause": root_cause,

        "recommendation": recommendation,

        "confidence": confidence,

        "severity": severity,

        "business_impact": business_impact,

        "action": action

    }

    response = (
        supabase
        .table("llm_investigation_log")
        .insert(row)
        .execute()
    )

    print(response)