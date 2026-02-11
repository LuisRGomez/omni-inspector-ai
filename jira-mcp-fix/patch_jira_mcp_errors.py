#!/usr/bin/env python3
"""
Patch para arreglar el manejo de errores en mcp-server-jira
El problema: cuando response.raise_for_status() falla, no maneja correctamente la excepción
"""

import os
import sys

# Encontrar el archivo del servidor
try:
    import mcp_server_jira
    server_file = os.path.join(os.path.dirname(mcp_server_jira.__file__), 'server.py')
    print(f"📍 Archivo del servidor: {server_file}")
except ImportError:
    print("❌ mcp-server-jira no está instalado")
    sys.exit(1)

# Leer el contenido actual
with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Backup
backup_file = server_file + '.backup'
if not os.path.exists(backup_file):
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup creado: {backup_file}")

# Patch 1: Arreglar assign_issue para manejar errores correctamente
old_assign = '''    async def assign_issue(self, issue_key: str, account_id: str, token: str | None = None) -> dict:
        """Assign issue to user"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/assignee"
        response = requests.put(url, headers=self._get_headers(token), json={"accountId": account_id})
        if response.status_code == 204:
            return {"success": True, "message": f"Issue {issue_key} assigned successfully"}
        response.raise_for_status()
        result = response.json() if response.text else {"success": True}
        return result'''

new_assign = '''    async def assign_issue(self, issue_key: str, account_id: str, token: str | None = None) -> dict:
        """Assign issue to user"""
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
            raise JiraError(f"Network error assigning issue: {str(e)}")'''

# Patch 2: Arreglar add_comment para manejar errores correctamente
old_comment = '''    async def add_comment(self, issue_key: str, comment_text: str, token: str | None = None) -> dict:
        """Add comment to issue"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment_text}]}]}}
        response = requests.post(url, headers=self._get_headers(token), json=payload)
        response.raise_for_status()
        return response.json()'''

new_comment = '''    async def add_comment(self, issue_key: str, comment_text: str, token: str | None = None) -> dict:
        """Add comment to issue"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        payload = {"body": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment_text}]}]}}
        try:
            response = requests.post(url, headers=self._get_headers(token), json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise JiraError(f"Failed to add comment to {issue_key}: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise JiraError(f"Network error adding comment: {str(e)}")'''

# Aplicar patches
modified = False

if old_assign in content:
    content = content.replace(old_assign, new_assign)
    print("✅ Patch 1 aplicado: assign_issue con manejo de errores")
    modified = True
else:
    print("⚠️  Patch 1 ya aplicado o código cambió")

if old_comment in content:
    content = content.replace(old_comment, new_comment)
    print("✅ Patch 2 aplicado: add_comment con manejo de errores")
    modified = True
else:
    print("⚠️  Patch 2 ya aplicado o código cambió")

# Guardar cambios
if modified:
    with open(server_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✅ Servidor parcheado exitosamente: {server_file}")
    print("\n🔄 IMPORTANTE: Reinicia el servidor MCP de Jira para aplicar los cambios")
    print("   En Kiro: Ve a la vista 'MCP Servers' y reconecta el servidor 'jira'")
else:
    print("\n⚠️  No se aplicaron cambios")
