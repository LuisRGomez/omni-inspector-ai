# Configuración del Servidor SSH MCP

## ✅ Instalación Completada

Todo está instalado y listo para usar:
- ✅ Node.js v24.13.0
- ✅ npm/npx 11.6.2
- ✅ uv/uvx 0.10.0
- ✅ ssh-mcp server descargado

## 📝 Configuración

El archivo de configuración está en: `.kiro/settings/mcp.json`

### Opción 1: Configuración Automática (Recomendado)

Ejecuta el script interactivo:

```powershell
.\configure-ssh.ps1
```

Este script te guiará paso a paso para configurar tu conexión SSH.

### Opción 2: Configuración Manual

Pasos para configurar tu servidor SSH:

1. Abre el archivo `.kiro/settings/mcp.json`
2. Reemplaza los siguientes valores:
   - `YOUR_HOST`: La IP o hostname de tu servidor (ej: `192.168.1.100` o `example.com`)
   - `YOUR_USER`: Tu usuario SSH (ej: `root`, `admin`, `ubuntu`)
   - `YOUR_PASSWORD`: Tu contraseña SSH

### Ejemplo de configuración:

```json
{
  "mcpServers": {
    "ssh": {
      "command": "npx.cmd",
      "args": [
        "ssh-mcp",
        "-y",
        "--",
        "--host=192.168.1.100",
        "--port=22",
        "--user=admin",
        "--password=mipassword123"
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Opciones adicionales disponibles:

- `--key=/ruta/a/clave/privada`: Usar autenticación por clave SSH en lugar de contraseña
- `--sudoPassword=password`: Contraseña para ejecutar comandos con sudo
- `--timeout=60000`: Timeout en milisegundos (default: 60000)
- `--maxChars=none`: Sin límite de caracteres en comandos
- `--disableSudo`: Deshabilitar comandos sudo

## 🚀 Uso

Una vez configurado, podrás pedirme que:
- Ejecute comandos en tu servidor remoto
- Liste archivos y directorios
- Gestione procesos
- Instale paquetes
- Y mucho más!

Ejemplos:
- "Lista los archivos en /var/www"
- "Verifica el espacio en disco del servidor"
- "Reinicia el servicio nginx"
- "Muestra los procesos en ejecución"

## 🧪 Probar la Conexión

Puedes probar tu conexión SSH antes de configurar Kiro:

```powershell
.\test-ssh-connection.ps1 -host "192.168.1.100" -user "admin" -password "tupassword"
```

## 🔄 Reconectar el servidor

Después de editar la configuración:
1. Ve a la vista "MCP Server" en el panel de Kiro
2. Haz clic en reconectar
3. O simplemente reinicia Kiro

## 🔒 Seguridad

⚠️ **Importante**: Tu contraseña estará en texto plano en el archivo de configuración. 
Considera usar autenticación por clave SSH para mayor seguridad:

```json
"args": [
  "ssh-mcp",
  "-y",
  "--",
  "--host=192.168.1.100",
  "--user=admin",
  "--key=C:\\Users\\TuUsuario\\.ssh\\id_rsa"
]
```
