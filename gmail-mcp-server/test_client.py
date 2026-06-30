import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
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

            tools = await session.list_tools()
            print("\nAVAILABLE TOOLS:")
            for tool in tools.tools:
                print("-", tool.name)

            result = await session.call_tool(
                "send-email",
                {
                    "recipient_id": "kirthikasri308@gmail.com",
                    "subject": "MCP Test",
                    "message": "Hello from MCP Client"
                }
            )

            print("\nRESULT:")
            print(result)


if __name__ == "__main__":
    asyncio.run(main())