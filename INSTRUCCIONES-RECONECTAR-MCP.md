# 🚀 RECONECTAR MCP JIRA - INSTRUCCIONES

## ✅ ESTADO ACTUAL

El servidor MCP Jira ha sido **extendido exitosamente** con 4 nuevas funciones:
- ✅ `assign_issue` - Asignar issues a usuarios
- ✅ `add_comment` - Agregar comentarios
- ✅ `add_attachment` - Subir archivos
- ✅ `link_issues` - Vincular issues

**Sintaxis**: ✅ CORRECTA  
**Verificación**: ✅ COMPLETA  
**Archivo**: 728 líneas (original: 556)

---

## 🔄 PASO 1: RECONECTAR MCP

### Opción A: Reconectar desde Kiro (RECOMENDADO)
1. Abrir panel lateral "MCP Servers"
2. Buscar servidor "jira"
3. Click en botón "Reconnect" o ícono de reconexión
4. Esperar mensaje de éxito

### Opción B: Reiniciar Kiro
- Cerrar y abrir Kiro completamente
- Más lento pero garantiza carga limpia

---

## 🧪 PASO 2: PROBAR FUNCIONES

Después de reconectar, ejecutar este test:

```python
# Test 1: Asignar issue
kiroPowers(
    action="use",
    powerName="jira",
    serverName="jira",
    toolName="assign_issue",
    arguments={
        "issue_key": "TALB-18",
        "account_id": "712020:fb49f226-fec7-48ae-a490-1b1821197ff5"
    }
)
```

Si funciona, verás:
```json
{
  "success": true,
  "message": "Issue TALB-18 assigned"
}
```

---

## 📋 PASO 3: ASIGNAR TAREAS PENDIENTES

Ejecutar script para asignar 10 tareas Done sin assignee:

```bash
python assign_all_unassigned.py
```

**Tareas**: TALB-18, 19, 20, 21, 22, 26, 28, 29, 34, 35  
**Assignee**: Luis Roberto Gomez

---

## ⚠️ SI HAY PROBLEMAS

### Error: "Tool not found"
- MCP no reconectó correctamente
- Solución: Reiniciar Kiro completo

### Error: "Connection failed"
- Verificar credenciales en `.kiro/settings/mcp.json`
- Verificar que el servidor esté habilitado

### Error de sintaxis al reconectar
- Restaurar backup: `python jira-mcp-fix/force_restore.py`
- Re-aplicar parche: `python jira-mcp-fix/patch_v5_final.py`

---

## 📝 RESUMEN

1. ✅ Parche aplicado correctamente
2. 🔄 Reconectar MCP Jira
3. 🧪 Probar assign_issue
4. 📋 Ejecutar assign_all_unassigned.py

**Tiempo estimado**: 2-3 minutos

---

**¿Listo para reconectar?** → Abre el panel MCP Servers en Kiro
