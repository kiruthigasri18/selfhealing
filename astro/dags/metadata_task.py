from supabase_connection import supabase


def metadata_task():

    response = (
        supabase
        .table("transformation_metadata")
        .select("*")
        .eq("active", True)
        .execute()
    )

    
    metadata = response.data[0]

    print(metadata)

    return {
        "transformation_name": metadata["transformation_name"],
        "table_name": metadata["table_name"],
        "raw_table_name": metadata["raw_table_name"],
        "code_file_path": metadata["code_file_path"],
        "rule_description": metadata["rule_description"]
    }