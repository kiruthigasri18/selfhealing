import json
from llm_utils import llm_call


def code_agent_task(
        transformation_name,
        rules,
        code,
        silver_summary,
        sample_data):

    prompt = f"""
You are a Code Investigation Agent.

Transformation:
{transformation_name}

Business Rules:
{rules}

Transformation Code:
{code}

Silver Summary:
{silver_summary}

Sample Data:
{sample_data}

Tasks:

1. Verify code implements the rule correctly.

2. Detect CODE_ERROR.

3. Decide whether raw data investigation is required.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanation.
Do not add text before or after JSON.

Expected format:

{{
"code_issue": false,
"need_raw_data": true,
"reason":"No code issue found"
}}
"""

    response_text = llm_call(prompt)

    print("========== CODE AGENT RESPONSE ==========")
    print(response_text)
    print("=========================================")

    response_text = response_text.strip()

    # Remove markdown wrappers if Gemini adds them
    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    try:
        result = json.loads(response_text)

    except Exception as e:
        print("JSON PARSE ERROR")
        print(response_text)
        raise e

    return result
