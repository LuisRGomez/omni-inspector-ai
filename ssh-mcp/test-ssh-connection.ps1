# Script de prueba para verificar la conexion SSH MCP
# Uso: .\test-ssh-connection.ps1

Write-Host "=== Verificacion de Instalacion SSH MCP ===" -ForegroundColor Cyan
Write-Host ""

# Verificar Node.js
Write-Host "Verificando Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($nodeVersion) {
    Write-Host "OK Node.js instalado: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "ERROR Node.js no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar npm/npx
Write-Host "Verificando npm..." -ForegroundColor Yellow
$npmVersion = npm --version 2>$null
if ($npmVersion) {
    Write-Host "OK npm instalado: $npmVersion" -ForegroundColor Green
} else {
    Write-Host "ERROR npm no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar uv
Write-Host "Verificando uv..." -ForegroundColor Yellow
$uvVersion = uv --version 2>$null
if ($uvVersion) {
    Write-Host "OK uv instalado: $uvVersion" -ForegroundColor Green
} else {
    Write-Host "AVISO uv no encontrado en PATH (puede requerir reiniciar terminal)" -ForegroundColor Yellow
}

# Verificar configuracion MCP
Write-Host ""
Write-Host "Verificando configuracion MCP..." -ForegroundColor Yellow
$mcpConfigPath = "..\\.kiro\\settings\\mcp.json"
if (Test-Path $mcpConfigPath) {
    Write-Host "OK Archivo de configuracion encontrado: $mcpConfigPath" -ForegroundColor Green
    
    $config = Get-Content $mcpConfigPath | ConvertFrom-Json
    $sshConfig = $config.mcpServers.ssh
    
    if ($sshConfig) {
        Write-Host "OK Servidor SSH configurado" -ForegroundColor Green
        
        # Verificar si esta configurado con valores reales
        $hostArg = $sshConfig.args | Where-Object { $_ -like "--host=*" }
        if ($hostArg -like "*YOUR_HOST*") {
            Write-Host "PENDIENTE: Configurar host real (actualmente: YOUR_HOST)" -ForegroundColor Yellow
        } else {
            Write-Host "OK Host configurado: $hostArg" -ForegroundColor Green
        }
        
        $userArg = $sshConfig.args | Where-Object { $_ -like "--user=*" }
        if ($userArg -like "*YOUR_USER*") {
            Write-Host "PENDIENTE: Configurar usuario real (actualmente: YOUR_USER)" -ForegroundColor Yellow
        } else {
            Write-Host "OK Usuario configurado: $userArg" -ForegroundColor Green
        }
    } else {
        Write-Host "ERROR Servidor SSH no encontrado en configuracion" -ForegroundColor Red
    }
} else {
    Write-Host "ERROR Archivo de configuracion no encontrado" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Resumen ===" -ForegroundColor Cyan
Write-Host "Para completar la configuracion:"
Write-Host "1. Edita .kiro\settings\mcp.json" -ForegroundColor White
Write-Host "2. Reemplaza YOUR_HOST, YOUR_USER y YOUR_PASSWORD con tus datos reales" -ForegroundColor White
Write-Host "3. Reinicia Kiro o reconecta el servidor MCP desde el panel" -ForegroundColor White
Write-Host ""
Write-Host "Documentacion completa en: SSH-MCP-SETUP.md" -ForegroundColor Cyan
