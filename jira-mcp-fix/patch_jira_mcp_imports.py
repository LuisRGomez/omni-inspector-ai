#!/usr/bin/env python3
"""
Patch para agregar import de requests en mcp-server-jira
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

# Verificar si requests ya está importado
if 'import requests' in content:
    print("✅ requests ya está importado")
    sys.exit(0)

# Agregar import de requests después de httpx
old_imports = '''import httpx
from mcp.server import Server'''

new_imports = '''import httpx
import requests
from mcp.server import Server'''

if old_imports in content:
    content = content.replace(old_imports, new_imports)
    
    # Guardar cambios
    with open(server_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Import de requests agregado exitosamente")
    print("\n🔄 IMPORTANTE: Reinicia el servidor MCP de Jira para aplicar los cambios")
else:
    print("⚠️  No se encontró el patrón de imports esperado")
    print("Agregando import manualmente...")
    
    # Buscar la primera línea con "from mcp" y agregar antes
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('from mcp.server'):
            lines.insert(i, 'import requests')
            break
    
    content = '\n'.join(lines)
    with open(server_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Import de requests agregado")
