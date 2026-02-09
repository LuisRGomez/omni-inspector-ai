# SSH MCP - Instalacion Completa

## Estado de la Instalacion

✅ **TODO INSTALADO Y LISTO PARA USAR**

### Componentes Instalados:

- ✅ **Node.js v24.13.0** - Runtime JavaScript
- ✅ **npm 11.6.2 / npx** - Gestor de paquetes Node
- ✅ **uv 0.10.0** - Gestor de paquetes Python ultrarapido
- ✅ **ssh-mcp** - Servidor MCP para conexiones SSH
- ✅ **Configuracion MCP** - Archivo base creado en `.kiro/settings/mcp.json`

---

## Que Puedes Hacer Ahora

Con esta extension SSH MCP podras:

- 🖥️ Ejecutar comandos en servidores remotos via SSH
- 📁 Listar y gestionar archivos remotos
- 🔧 Instalar paquetes y configurar servicios
- 📊 Monitorear procesos y recursos del sistema
- 🔄 Reiniciar servicios y aplicaciones
- 🔐 Ejecutar comandos con sudo (si lo configuras)

Todo esto usando lenguaje natural, sin necesidad de abrir una terminal SSH manualmente.

---

## Configuracion Rapida (3 pasos)

### Paso 1: Edita el archivo de configuracion

Abre: `.kiro/settings/mcp.json`

### Paso 2: Reemplaza los valores de ejemplo

```json
{
  "mcpServers": {
    "ssh": {
      "command": "npx.cmd",
      "args": [
        "ssh-mcp",
        "-y",
        "--",
        "--host=TU_IP_O_HOSTNAME",      // ej: 192.168.1.100 o example.com
        "--port=22",                     // cambiar si usas otro puerto
        "--user=TU_USUARIO",             // ej: root, admin, ubuntu
        "--password=TU_CONTRASEÑA"       // tu contraseña SSH
      ],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Paso 3: Reconecta el servidor

- Opcion A: Reinicia Kiro
- Opcion B: Ve al panel "MCP Server" y haz clic en reconectar

---

## Ejemplos de Uso

Una vez configurado, puedes pedirme cosas como:

```
"Lista los archivos en /var/www"
"Muestra el uso de disco del servidor"
"Verifica si nginx esta corriendo"
"Reinicia el servicio apache2"
"Instala python3-pip en el servidor"
"Muestra los ultimos 20 logs del sistema"
"Crea un directorio llamado backups en /home"
```

---

## Archivos de Ayuda Incluidos

- 📄 **SSH-MCP-SETUP.md** - Guia detallada de configuracion
- 📄 **ssh-config-examples.json** - 6 ejemplos de configuracion diferentes
- 📄 **test-ssh-connection.ps1** - Script para verificar la instalacion

### Ejecutar el script de prueba:

```powershell
powershell -ExecutionPolicy Bypass -File test-ssh-connection.ps1
```

---

## Configuraciones Avanzadas

### Usar clave SSH (mas seguro que contraseña):

```json
"args": [
  "ssh-mcp",
  "-y",
  "--",
  "--host=example.com",
  "--user=admin",
  "--key=C:\\Users\\TitoGomez\\.ssh\\id_rsa"
]
```

### Habilitar comandos sudo:

```json
"args": [
  "ssh-mcp",
  "-y",
  "--",
  "--host=192.168.1.100",
  "--user=ubuntu",
  "--password=userpass",
  "--sudoPassword=sudopass"
]
```

### Multiples servidores:

Puedes configurar varios servidores SSH simultaneamente. Ver ejemplos en `ssh-config-examples.json`.

---

## Seguridad

⚠️ **IMPORTANTE:**

1. Tu contraseña estara en texto plano en el archivo de configuracion
2. Considera usar autenticacion por clave SSH para mayor seguridad
3. Asegurate de que el archivo `.kiro/settings/mcp.json` tenga permisos restrictivos
4. No compartas este archivo en repositorios publicos

---

## Solucion de Problemas

### El servidor no se conecta:

1. Verifica que el host, usuario y contraseña sean correctos
2. Asegurate de que el servidor SSH este accesible desde tu red
3. Revisa el puerto (por defecto 22)
4. Verifica que el firewall permita conexiones SSH

### Error "command not found":

- Reinicia tu terminal o Kiro para que el PATH se actualice
- Verifica que Node.js este instalado: `node --version`

### Comandos muy lentos:

- Aumenta el timeout: `--timeout=120000` (2 minutos)
- Verifica la latencia de red al servidor

---

## Recursos Adicionales

- Repositorio oficial: https://github.com/tufantunc/ssh-mcp
- Documentacion MCP: https://modelcontextprotocol.io
- Lista de servidores MCP: https://mcpservers.org

---

## Proximos Pasos

1. ✏️ Edita `.kiro/settings/mcp.json` con tus credenciales
2. 🔄 Reconecta el servidor MCP
3. 🚀 Empieza a usar comandos SSH con lenguaje natural

**¡Ya estas listo para gestionar tus servidores remotos desde Kiro!**
