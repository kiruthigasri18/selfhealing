from metadata_task import metadata_task
from pinecone_task import pinecone_task
from code_reader_task import code_reader_task
from silver_summary_task import silver_summary_task
from code_agent_task import code_agent_task
from raw_summary_task import raw_summary_task
from data_agent_task import data_agent_task
from rca_task import rca_task
from store_result_task import store_result_task


def investigate():

    # =====================================================
    # Metadata
    # =====================================================

    metadata = metadata_task()

    print(metadata)

    # =====================================================
    # Retrieve Rules
    # =====================================================

    rules = pinecone_task(
        metadata["rule_description"]
    )

    # =====================================================
    # Read Transformation Code
    # =====================================================

    code = code_reader_task(
        metadata["code_file_path"]
    )

    # =====================================================
    # Silver Layer Summary
    # =====================================================

    silver = silver_summary_task(
        metadata["table_name"]
    )

    # =====================================================
    # Code Agent
    # =====================================================

    code_agent_result = code_agent_task(

        metadata["transformation_name"],

        rules,

        code,

        silver["summary"],

        silver["sample"]

    )

    print("CODE AGENT RESULT")
    print(code_agent_result)

    # =====================================================
    # CODE ERROR PATH
    # =====================================================

    if code_agent_result["code_issue"]:

        data_agent_result = {

            "issue_type": "CODE_ERROR",

            "root_cause": code_agent_result["reason"],

            "recommendation": "Fix transformation logic identified by Code Agent.",

            "confidence": 0.95

        }

    # =====================================================
    # DATA ERROR PATH
    # =====================================================

    else:

        raw = raw_summary_task(
            metadata["raw_table_name"]
        )

        data_agent_result = data_agent_task(

            rules,

            silver["summary"],

            silver["sample"],

            raw["summary"],

            raw["sample"]

        )

    print("INVESTIGATION RESULT")
    print(data_agent_result)

    # =====================================================
    # RCA Agent
    # =====================================================

    rca = rca_task(

        code_agent_result,

        data_agent_result

    )

    print("RCA RESULT")
    print(rca)

    # =====================================================
    # Store Result
    # =====================================================

    store_result_task(

        metadata["transformation_name"],

        data_agent_result["issue_type"],

        data_agent_result["root_cause"],

        data_agent_result["recommendation"],

        data_agent_result["confidence"],

        rca["severity"],

        rca["business_impact"],

        rca["action"]

    )

    print("Investigation Completed")