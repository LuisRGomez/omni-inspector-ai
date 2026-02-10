@echo off
echo ========================================
echo Build APK Limpio - Omni Inspector
echo ========================================
echo.
echo Configuracion simplificada:
echo - Solo dependencias esenciales
echo - Sin dataset (360 MB menos)
echo - node_modules excluido automaticamente
echo.
echo Iniciando build...
echo.
call eas build --platform android --profile preview --clear-cache
echo.
pause
