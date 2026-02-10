# Setup script para Omni Inspector Mobile App

Write-Host "🚀 Configurando Omni Inspector Mobile App..." -ForegroundColor Cyan

# Verificar Node.js
Write-Host "`n📦 Verificando Node.js..." -ForegroundColor Yellow
node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Node.js no está instalado. Instálalo desde https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Instalar dependencias
Write-Host "`n📥 Instalando dependencias..." -ForegroundColor Yellow
npm install

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

# Crear carpeta de assets
Write-Host "`n📁 Creando carpeta de assets..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "assets" | Out-Null

Write-Host "`n✅ Setup completado!" -ForegroundColor Green
Write-Host "`n📱 Para ejecutar la app:" -ForegroundColor Cyan
Write-Host "   npm start          → Iniciar Expo" -ForegroundColor White
Write-Host "   npm run android    → Ejecutar en Android" -ForegroundColor White
Write-Host "   npm run ios        → Ejecutar en iOS" -ForegroundColor White
Write-Host "   npm run web        → Ejecutar en navegador" -ForegroundColor White
