#!/usr/bin/env python3
"""
Test directo del servidor MCP de Jira (sin pasar por Kiro)
"""

import asyncio
from mcp_server_jira.server import JiraServer

async def test_assign():
    # Crear servidor con token por defecto
    # IMPORTANT: Replace with your actual Jira token
    import os
    jira_token = os.getenv("JIRA_TOKEN", "YOUR_JIRA_TOKEN_HERE")
    
    server = JiraServer(
        base_url="https://your-domain.atlassian.net",
        default_token=jira_token,
        email="your-email@example.com"
    )
    
    print("🧪 Test 1: Assign issue")
    try:
        result = await server.assign_issue(
            issue_key="YOUR-ISSUE-KEY",  # Replace with your issue key
            account_id="YOUR-ACCOUNT-ID",  # Replace with your account ID
            token=None  # Usa el default_token
        )
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
    
    print("\n🧪 Test 2: Add comment")
    try:
        result = await server.add_comment(
            issue_key="YOUR-ISSUE-KEY",  # Replace with your issue key
            comment_text="Test comment from Python - verifying MCP server works correctly",
            token=None
        )
        print(f"✅ Resultado: {result}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_assign())
