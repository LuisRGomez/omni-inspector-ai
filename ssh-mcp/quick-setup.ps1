# Script de configuracion rapida SSH MCP
# Este script te ayuda a configurar tu servidor SSH de forma interactiva

Write-Host "=== Configuracion Rapida SSH MCP ===" -ForegroundColor Cyan
Write-Host ""

# Solicitar datos al usuario
Write-Host "Ingresa los datos de tu servidor SSH:" -ForegroundColor Yellow
Write-Host ""

$host_input = Read-Host "Host (IP o dominio, ej: 192.168.1.100)"
$port_input = Read-Host "Puerto (presiona Enter para usar 22)"
$user_input = Read-Host "Usuario (ej: root, admin, ubuntu)"

Write-Host ""
Write-Host "Metodo de autenticacion:" -ForegroundColor Yellow
Write-Host "1. Contraseña"
Write-Host "2. Clave SSH"
$auth_method = Read-Host "Selecciona (1 o 2)"

if ($auth_method -eq "2") {
    $key_path = Read-Host "Ruta completa a tu clave privada SSH"
    # Convertir barras a formato Windows
    $key_path = $key_path -replace '/', '\\'
    $key_path = $key_path -replace '\\', '\\\\'
} else {
    $password_input = Read-Host "Contraseña SSH" -AsSecureString
    $password_plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($password_input)
    )
}

$sudo_support = Read-Host "Necesitas soporte para sudo? (s/n)"

if ($sudo_support -eq "s") {
    $sudo_password = Read-Host "Contraseña sudo" -AsSecureString
    $sudo_plain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sudo_password)
    )
}

# Usar puerto por defecto si no se especifico
if ([string]::IsNullOrWhiteSpace($port_input)) {
    $port_input = "22"
}

# Construir la configuracion
$config = @{
    mcpServers = @{
        ssh = @{
            command = "npx.cmd"
            args = @(
                "ssh-mcp",
                "-y",
                "--",
                "--host=$host_input",
                "--port=$port_input",
                "--user=$user_input"
            )
            disabled = $false
            autoApprove = @()
        }
    }
}

# Agregar autenticacion
if ($auth_method -eq "2") {
    $config.mcpServers.ssh.args += "--key=$key_path"
} else {
    $config.mcpServers.ssh.args += "--password=$password_plain"
}

# Agregar sudo si se solicito
if ($sudo_support -eq "s") {
    $config.mcpServers.ssh.args += "--sudoPassword=$sudo_plain"
}

# Crear directorio si no existe
$configDir = "..\\.kiro\\settings"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Guardar configuracion
$configPath = "$configDir\mcp.json"
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8

Write-Host ""
Write-Host "=== Configuracion Completada ===" -ForegroundColor Green
Write-Host ""
Write-Host "Archivo guardado en: $configPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos pasos:" -ForegroundColor Yellow
Write-Host "1. Reinicia Kiro o reconecta el servidor MCP desde el panel"
Write-Host "2. Prueba con comandos como: 'Lista los archivos en /home'"
Write-Host ""
Write-Host "Configuracion aplicada:" -ForegroundColor Cyan
Write-Host "  Host: $host_input"
Write-Host "  Puerto: $port_input"
Write-Host "  Usuario: $user_input"
if ($auth_method -eq "2") {
    Write-Host "  Autenticacion: Clave SSH"
} else {
    Write-Host "  Autenticacion: Contraseña"
}
if ($sudo_support -eq "s") {
    Write-Host "  Sudo: Habilitado"
}
Write-Host ""
