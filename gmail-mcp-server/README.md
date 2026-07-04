# Gmail MCP Server

Model Context Protocol server for Gmail, used by the selfhealing project to send
investigation/notification emails via the Gmail API.

## Setup

```bash
pip install -e .
```

Run the server (requires Google OAuth credentials):

```bash
python src/gmail/server.py --creds-file-path <path-to-client_creds.json> --token-path <path-to-app_tokens.json>
```
