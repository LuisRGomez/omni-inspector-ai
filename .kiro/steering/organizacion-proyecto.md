---
inclusion: auto
---

# Reglas de Organizacion del Proyecto

## Estructura de Carpetas

Este proyecto sigue una estructura organizada por temas. Cada funcionalidad o modulo debe tener su propia carpeta.

### Reglas Principales

1. **Cada tema en su carpeta**
   - Todos los archivos relacionados con un tema especifico deben ir en una carpeta dedicada
   - Ejemplos: `ssh-mcp/`, `database-tools/`, `api-clients/`, etc.

2. **Documentos generales en raiz**
   - Solo documentos que aplican a todo el proyecto van en la raiz
   - Ejemplo: `README.md` (indice general del proyecto)

3. **Configuraciones en .kiro/**
   - Archivos de configuracion de Kiro van en `.kiro/settings/`
   - Steering files van en `.kiro/steering/`
   - Hooks van en `.kiro/hooks/`

4. **Scripts ejecutables en su carpeta tematica**
   - Los scripts deben estar en la carpeta del tema al que pertenecen
   - Ejemplo: `ssh-mcp/quick-setup.ps1`

5. **TODO EL CODIGO FUENTE EN INGLES - REGLA CRITICA**
   - Variables, funciones, clases, metodos: SIEMPRE en ingles
   - Comentarios en codigo: en ingles
   - Nombres de archivos de codigo: en ingles
   - Mensajes de commit: en ingles
   - Documentacion tecnica: puede ser en español para el usuario final
   - Esta regla NO aplica a: documentacion de usuario, README en español, mensajes UI
   - Ejemplos:
     - ✅ CORRECTO: `function getUserData()`, `class DatabaseConnection`, `const apiEndpoint`
     - ❌ INCORRECTO: `function obtenerDatosUsuario()`, `class ConexionBaseDatos`

6. **Autonomia Total - Full Self-Sustainable**
   - El agente debe poder configurar y gestionar todo de forma autonoma
   - Acceso completo a AWS, GitHub, servidores, bases de datos, etc.
   - Credenciales y accesos deben estar disponibles para configuracion automatica
   - El agente debe poder: crear recursos, configurar servicios, hacer deploys, gestionar infraestructura
   - Objetivo: cero intervencion manual, todo automatizable

### Estructura Actual

```
talos-forencing/
├── ssh-mcp/                    # Modulo SSH MCP
│   ├── README-SSH-MCP.md       # Documentacion principal del modulo
│   ├── SSH-MCP-SETUP.md        # Guia de configuracion
│   ├── COMANDOS-UTILES.md      # Ejemplos de uso
│   ├── quick-setup.ps1         # Script de configuracion
│   ├── test-ssh-connection.ps1 # Script de verificacion
│   └── ...                     # Otros archivos del modulo
├── .kiro/
│   ├── settings/
│   │   └── mcp.json            # Configuracion MCP
│   └── steering/
│       └── organizacion-proyecto.md  # Este archivo
└── README.md                   # Indice general del proyecto
```

## Cuando Crear una Nueva Carpeta

Crea una nueva carpeta cuando:
- Estas agregando una nueva funcionalidad o herramienta
- Tienes multiples archivos relacionados con un tema especifico
- Quieres mantener el proyecto organizado y facil de navegar

### Ejemplos de Carpetas Tematicas

- `ssh-mcp/` - Herramientas SSH y MCP
- `database-tools/` - Scripts y herramientas de base de datos
- `api-clients/` - Clientes para APIs externas
- `monitoring/` - Herramientas de monitoreo
- `backup-scripts/` - Scripts de respaldo
- `deployment/` - Scripts de despliegue

## Nomenclatura de Archivos

### Documentacion
- `README-[TEMA].md` - Documentacion principal de un modulo
- `[TEMA]-SETUP.md` - Guia de configuracion
- `[TEMA]-GUIDE.md` - Guia de uso

### Scripts
- `[accion]-[tema].ps1` - Scripts PowerShell
- `[accion]-[tema].sh` - Scripts Bash
- Ejemplos: `quick-setup.ps1`, `test-connection.ps1`

### Configuracion
- `[tema]-config.json` - Archivos de configuracion
- `[tema]-examples.json` - Ejemplos de configuracion

## Actualizacion de Rutas

Cuando muevas archivos a carpetas tematicas:
1. Actualiza todas las referencias de rutas en scripts
2. Actualiza la documentacion con las nuevas ubicaciones
3. Actualiza el README.md principal con la nueva estructura

## Beneficios de Esta Organizacion

- ✅ Facil de navegar y encontrar archivos
- ✅ Escalable para proyectos grandes
- ✅ Modulos independientes y reutilizables
- ✅ Documentacion clara y accesible
- ✅ Mantenimiento simplificado
