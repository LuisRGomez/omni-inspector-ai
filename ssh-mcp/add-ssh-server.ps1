# Script para agregar un servidor SSH adicional a la configuración MCP
# Uso: .\add-ssh-server.ps1

Write-Host "➕ Agregar Servidor SSH MCP" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

$configPath = ".kiro\settings\mcp.json"

# Verificar si existe el archivo de configuración
if (!(Test-Path $configPath)) {
    Write-Host "❌ No se encontró el archivo de configuración en $configPath" -ForegroundColor Red
    Write-Host "Ejecuta primero .\configure-ssh.ps1 para crear la configuración inicial" -ForegroundColor Yellow
    exit 1
}

# Leer configuración actual
$config = Get-Content $configPath -Raw | ConvertFrom-Json

# Solicitar información del nuevo servidor
$serverName = Read-Host "Ingresa un nombre para este servidor (ej: produccion, desarrollo, backup)"
$host = Read-Host "Ingresa el host o IP del servidor SSH"
$user = Read-Host "Ingresa el usuario SSH"
$port = Read-Host "Ingresa el puerto SSH (presiona Enter para usar 22)"
if ([string]::IsNullOrWhiteSpace($port)) { $port = "22" }

Write-Host ""
Write-Host "Selecciona el método de autenticación:" -ForegroundColor Yellow
Write-Host "1. Contraseña"
Write-Host "2. Clave SSH"
$authMethod = Read-Host "Opción (1 o 2)"

$args = @(
    "ssh-mcp",
    "-y",
    "--",
    "--host=$host",
    "--port=$port",
    "--user=$user"
)

if ($authMethod -eq "1") {
    $password = Read-Host "Ingresa la contraseña SSH" -AsSecureString
    $passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
    )
    $args += "--password=$passwordPlain"
} elseif ($authMethod -eq "2") {
    $keyPath = Read-Host "Ingresa la ruta completa a tu clave privada SSH"
    $args += "--key=$keyPath"
} else {
    Write-Host "❌ Opción inválida" -ForegroundColor Red
    exit 1
}

# Preguntar por sudo
Write-Host ""
$addSudo = Read-Host "¿Necesitas ejecutar comandos con sudo? (s/n)"
if ($addSudo -eq "s") {
    $sudoPassword = Read-Host "Ingresa la contraseña de sudo" -AsSecureString
    $sudoPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sudoPassword)
    )
    $args += "--sudoPassword=$sudoPasswordPlain"
}

# Agregar el nuevo servidor a la configuración
$newServer = @{
    command = "npx.cmd"
    args = $args
    disabled = $false
    autoApprove = @()
}

$config.mcpServers | Add-Member -MemberType NoteProperty -Name "ssh-$serverName" -Value $newServer -Force

# Guardar configuración actualizada
$configJson = $config | ConvertTo-Json -Depth 10

Write-Host ""
Write-Host "💾 Guardando configuración actualizada..." -ForegroundColor Cyan
$configJson | Out-File -FilePath $configPath -Encoding UTF8

Write-Host "✅ Servidor '$serverName' agregado exitosamente!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Servidores configurados:" -ForegroundColor Yellow
$config.mcpServers.PSObject.Properties | ForEach-Object {
    Write-Host "  - $($_.Name)" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "🔄 Recuerda reconectar el servidor MCP en Kiro para aplicar los cambios" -ForegroundColor Yellow
Write-Host ""
