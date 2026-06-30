import asyncio
from supabase import create_client
from google import genai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ==========================
# CONFIG
# ==========================

SUPABASE_URL = "https://ooaebqrtzlnuhhaqxilf.supabase.co"

SUPABASE_KEY = "sb_secret_cxcWocGujmZYrVievmy5aw_txA4GAcZ"

GEMINI_API_KEY = "AQ.Ab8RN6Jlq-HzesF-nSQHwXJINt09X70DwKKGCTuZrpqlCHrJlg"

RECIPIENT_EMAIL = "kirthikasri308@gmail.com"


# ==========================
# SUPABASE
# ==========================

def get_latest_investigation():

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    response = (
        supabase.table("llm_investigation_log")
        .select("*")
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    return response.data[0]


# ==========================
# GEMINI
# ==========================

def generate_email(record):

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    prompt = f"""
You are a Senior Data Quality Engineer.

Generate a professional email.

Transformation Name:
{record['transformation_name']}

Issue Type:
{record['issue_type']}

Severity:
{record['severity']}

Root Cause:
{record['root_cause']}

Business Impact:
{record['business_impact']}

Recommendation:
{record['recommendation']}

Action:
{record['action']}

Return EXACTLY in this format:

SUBJECT:
<subject>

BODY:
<body>
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    text = response.text

    subject = text.split("BODY:")[0] \
                  .replace("SUBJECT:", "") \
                  .strip()

    body = text.split("BODY:")[1].strip()

    return subject, body


# ==========================
# MCP EMAIL
# ==========================

async def send_email(subject, body):

    server_params = StdioServerParameters(
        command="uv",
        args=[
            "run",
            "src/gmail/server.py",
            "--creds-file-path",
            r"C:\Users\v-monishasub\.google\client_creds.json",
            "--token-path",
            r"C:\Users\v-monishasub\.google\app_tokens.json"
        ]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "send-email",
                {
                    "recipient_id": RECIPIENT_EMAIL,
                    "subject": subject,
                    "message": body
                }
            )

            print(result)


# ==========================
# MAIN
# ==========================

async def main():

    print("\nReading latest investigation...")

    record = get_latest_investigation()

    print(
        f"Investigation ID: {record['investigation_id']}"
    )

    print("\nGenerating email using Gemini...")

    subject, body = generate_email(record)

    print("\nSUBJECT:")
    print(subject)

    print("\nBODY:")
    print(body)

    print("\nSending email through Gmail MCP...")

    await send_email(subject, body)

    print("\nWorkflow completed successfully")


if __name__ == "__main__":
    asyncio.run(main())