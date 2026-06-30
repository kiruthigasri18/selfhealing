from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"
)

investigation = {
    "transformation_name": "delivery_delay_days",
    "issue_type": "DATA_ERROR",
    "severity": "HIGH",
    "root_cause": "The 'delivery_status' classification logic incorrectly labels orders with missing or null delivery dates as DELAYED.",
    "recommendation": "Implement a PENDING status for orders with null delivery dates.",
    "business_impact": "False reporting of delivery delays.",
    "action": "Patch transformation logic and audit historical records."
}

prompt = f"""
You are a Data Quality Engineer.

Generate a professional email.

Transformation Name:
{investigation['transformation_name']}

Issue Type:
{investigation['issue_type']}

Severity:
{investigation['severity']}

Root Cause:
{investigation['root_cause']}

Business Impact:
{investigation['business_impact']}

Recommendation:
{investigation['recommendation']}

Action:
{investigation['action']}

Return in this format:

SUBJECT:
<subject>

BODY:
<body>
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt
)

print(response.text)