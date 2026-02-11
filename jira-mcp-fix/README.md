# Bug Fixes for mcp-server-jira

This directory contains critical bug fixes for the `mcp-server-jira` package (v0.1.1).

## Issues Fixed

### 1. Missing `requests` Import
**Severity:** Critical  
**Affected Functions:** `assign_issue()`, `add_comment()`

**Problem:**
The functions `assign_issue` and `add_comment` use the `requests` library but it was not imported, causing `NameError: name 'requests' is not defined`.

**Solution:**
Added `import requests` to the imports section in `server.py`.

### 2. Incorrect Error Handling
**Severity:** High  
**Affected Functions:** `assign_issue()`, `add_comment()`

**Problem:**
When `response.raise_for_status()` throws an exception, it was not properly caught, leading to cryptic error messages like `'str' object has no attribute 'message'`.

**Solution:**
Wrapped HTTP calls in try/except blocks to catch `requests.exceptions.HTTPError` and `requests.exceptions.RequestException`, then raise descriptive `JiraError` exceptions.

## Files

- `patch_jira_mcp_imports.py` - Adds missing `requests` import
- `patch_jira_mcp_errors.py` - Fixes error handling in assign_issue and add_comment
- `test_jira_mcp_direct.py` - Direct test to verify fixes work
- `JIRA-MCP-FIXED.md` - Detailed documentation of the fix

## Installation & Usage

### Apply Patches

```bash
# Install mcp-server-jira first
pip install mcp-server-jira

# Apply patches
python patch_jira_mcp_imports.py
python patch_jira_mcp_errors.py
```

### Verify Fixes

```bash
python test_jira_mcp_direct.py
```

Expected output:
```
✅ Test 1: Assign issue - SUCCESS
✅ Test 2: Add comment - SUCCESS
```

### Restart MCP Server

After applying patches, restart your MCP server to load the fixed code:
- In Kiro: Go to MCP Servers panel → Reconnect "jira" server
- Or restart your IDE/application

## Technical Details

### Before (Broken)

```python
async def assign_issue(self, issue_key: str, account_id: str, token: str | None = None) -> dict:
    url = f"{self.base_url}/rest/api/3/issue/{issue_key}/assignee"
    response = requests.put(url, headers=self._get_headers(token), json={"accountId": account_id})
    if response.status_code == 204:
        return {"success": True, "message": f"Issue {issue_key} assigned successfully"}
    response.raise_for_status()  # ❌ Unhandled exception
    result = response.json() if response.text else {"success": True}
    return result
```

### After (Fixed)

```python
async def assign_issue(self, issue_key: str, account_id: str, token: str | None = None) -> dict:
    url = f"{self.base_url}/rest/api/3/issue/{issue_key}/assignee"
    try:
        response = requests.put(url, headers=self._get_headers(token), json={"accountId": account_id})
        if response.status_code == 204:
            return {"success": True, "message": f"Issue {issue_key} assigned successfully"}
        response.raise_for_status()
        result = response.json() if response.text else {"success": True}
        return result
    except requests.exceptions.HTTPError as e:
        raise JiraError(f"Failed to assign issue {issue_key}: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        raise JiraError(f"Network error assigning issue: {str(e)}")
```

## Backup

The patch scripts automatically create a backup of the original file:
- Location: `{site-packages}/mcp_server_jira/server.py.backup`

To restore original:
```bash
cp server.py.backup server.py
```

## Tested With

- Python: 3.11
- mcp-server-jira: 0.1.1
- OS: Windows 11
- Jira Cloud API: v3

## Contributing

These fixes should be submitted as a PR to the upstream repository:
https://github.com/QuantGeekDev/mcp-server-jira

## License

Same as mcp-server-jira (MIT)

## Author

Luis Roberto Gomez (luis.gomez@hdi.com.ar)  
Date: February 11, 2026

## Related Issues

- Missing import causes NameError in assign_issue and add_comment
- Unhandled HTTPError exceptions cause cryptic error messages
- MCP framework receives malformed error responses
