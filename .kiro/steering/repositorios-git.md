---
inclusion: auto
---

# Registro de Repositorios Git del Proyecto

Este archivo mantiene un registro de todos los repositorios git asociados al proyecto, tanto el principal como los repos independientes.

## Repositorio Principal

### omni-inspector-ai
- **URL**: https://github.com/LuisRGomez/omni-inspector-ai.git
- **Descripción**: Proyecto principal OmniInspector - App móvil React Native para detección forense
- **Ubicación Local**: `C:\Users\TitoGomez\Desktop\talos forencing`
- **Contenido**:
  - App móvil React Native (OmniInspector/)
  - Backend AWS Lambda (forensic-detective/)
  - Scripts de automatización Jira
  - Configuraciones de infraestructura AWS
  - Documentación del proyecto

## Repositorios Independientes

### jira-mcp-extended
- **URL**: https://github.com/LuisRGomez/jira-mcp-extended
- **Descripción**: Extensiones para mcp-server-jira con 4 funciones adicionales (assign, comment, attachment, link)
- **Estado**: ✅ REPO INDEPENDIENTE CREADO Y PUSHEADO
- **Instalación**: 
  ```bash
  git clone https://github.com/LuisRGomez/jira-mcp-extended.git
  cd jira-mcp-extended
  python patch_v5_final.py
  ```
- **Razón de Separación**: 
  - Herramienta standalone reutilizable
  - No depende del proyecto OmniInspector
  - Fácil de compartir con otros usuarios de Kiro
  - Instalación independiente

## Reglas de Gestión

### ✅ HACER
- Mantener repos independientes para herramientas standalone
- Documentar cada repo en este archivo
- Usar submodules si necesitas incluir un repo en otro
- Versionar independientemente cada herramienta

### ❌ NO HACER
- Mezclar repos independientes con el proyecto principal
- Agregar subdirectorios con su propio .git al repo principal
- Perder track de qué repos existen

## Historial de Cambios

### 2026-02-11
- ✅ CORREGIDO: Revertido commit que mezclaba jira-mcp-fix con repo principal
- ✅ CREADO: Repo independiente jira-mcp-extended en GitHub
- ✅ PUSHEADO: Código limpio sin credenciales hardcodeadas
- ✅ LIMPIADO: Removidas carpetas jira-mcp-fix y jira-mcp-extended del repo principal
- 📝 Actualizado registro de repos con URL correcta

## Próximos Repos Potenciales

Herramientas que podrían convertirse en repos independientes:
- `ssh-mcp-tools` - Si creamos herramientas SSH reutilizables
- `aws-automation-scripts` - Scripts de automatización AWS genéricos
- `kiro-workflow-templates` - Templates de workflow para Kiro

---

**NOTA IMPORTANTE**: Antes de crear un nuevo repo git, verificar este archivo para evitar duplicados o mezclas accidentales.
