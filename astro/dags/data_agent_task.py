import json
from llm_utils import llm_call


def data_agent_task(
        rules,
        silver_summary,
        silver_sample,
        raw_summary,
        raw_sample):

    prompt = f"""
You are a Data Investigation Agent.

Business Rules:
{rules}

Silver Summary:
{silver_summary}

Silver Sample:
{silver_sample}

Raw Summary:
{raw_summary}

Raw Sample:
{raw_sample}

Tasks:

1. Detect DATA_ERROR.

2. Find root cause.

3. Recommend corrective action.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add explanation.

{{
"issue_type":"DATA_ERROR",
"root_cause":"",
"recommendation":"",
"confidence":0.95
}}
"""

    response_text = llm_call(prompt)

    print("========== DATA AGENT RESPONSE ==========")
    print(response_text)
    print("=========================================")

    response_text = response_text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "")
        response_text = response_text.replace("```", "")
        response_text = response_text.strip()

    result = json.loads(response_text)

    return result