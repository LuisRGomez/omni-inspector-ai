# Script para configurar el servidor SSH MCP
# Uso: .\configure-ssh.ps1

Write-Host "🔧 Configurador de SSH MCP Server" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar información al usuario
$host = Read-Host "Ingresa el host o IP del servidor SSH"
$user = Read-Host "Ingresa el usuario SSH"
$port = Read-Host "Ingresa el puerto SSH (presiona Enter para usar 22)"
if ([string]::IsNullOrWhiteSpace($port)) { $port = "22" }

Write-Host ""
Write-Host "Selecciona el método de autenticación:" -ForegroundColor Yellow
Write-Host "1. Contraseña"
Write-Host "2. Clave SSH"
$authMethod = Read-Host "Opción (1 o 2)"

$config = @{
    mcpServers = @{
        ssh = @{
            command = "npx.cmd"
            args = @(
                "ssh-mcp",
                "-y",
                "--",
                "--host=$host",
                "--port=$port",
                "--user=$user"
            )
            disabled = $false
            autoApprove = @()
        }
    }
}

if ($authMethod -eq "1") {
    $password = Read-Host "Ingresa la contraseña SSH" -AsSecureString
    $passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
    )
    $config.mcpServers.ssh.args += "--password=$passwordPlain"
} elseif ($authMethod -eq "2") {
    $keyPath = Read-Host "Ingresa la ruta completa a tu clave privada SSH"
    $config.mcpServers.ssh.args += "--key=$keyPath"
} else {
    Write-Host "❌ Opción inválida" -ForegroundColor Red
    exit 1
}

# Preguntar por opciones adicionales
Write-Host ""
$addSudo = Read-Host "¿Necesitas ejecutar comandos con sudo? (s/n)"
if ($addSudo -eq "s") {
    $sudoPassword = Read-Host "Ingresa la contraseña de sudo" -AsSecureString
    $sudoPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sudoPassword)
    )
    $config.mcpServers.ssh.args += "--sudoPassword=$sudoPasswordPlain"
}

# Guardar configuración
$configPath = ".kiro\settings\mcp.json"
$configJson = $config | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "💾 Guardando configuración en $configPath..." -ForegroundColor Cyan

# Crear directorio si no existe
$configDir = Split-Path -Parent $configPath
if (!(Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

# Guardar archivo
$configJson | Out-File -FilePath $configPath -Encoding UTF8

Write-Host "✅ Configuración guardada exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Configuración:" -ForegroundColor Yellow
Write-Host $configJson
Write-Host ""
Write-Host "🔄 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Ve a la vista 'MCP Server' en el panel de Kiro"
Write-Host "2. Haz clic en 'Reconectar' o reinicia Kiro"
Write-Host "3. ¡Listo! Ahora puedes ejecutar comandos SSH remotos"
Write-Host ""
