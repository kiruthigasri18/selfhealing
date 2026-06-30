import json
from llm_utils import llm_call


def rca_task(
        code_result,
        data_result):

    prompt = f"""
Code Agent Output:

{code_result}

Data Agent Output:

{data_result}

Determine:

1. Severity
2. Business Impact
3. Recommended Action

Return JSON only.

{{
"severity":"HIGH",
"business_impact":"",
"action":""
}}
"""

    response_text = llm_call(
        prompt
    )

    result = json.loads(
        response_text
    )

    return result