@echo off
echo ========================================
echo Omni Inspector - Build APK
echo ========================================
echo.
echo Este proceso creara un APK instalable en tu celular.
echo.
echo PASOS:
echo 1. Login en Expo (si es primera vez)
echo 2. Configurar proyecto
echo 3. Iniciar build (toma 10-15 min)
echo.
echo ========================================
echo.

echo Paso 1: Login en Expo...
echo.
call eas login

echo.
echo ========================================
echo Paso 2: Configurando proyecto...
echo ========================================
echo.
call eas build:configure

echo.
echo ========================================
echo Paso 3: Iniciando build APK...
echo ========================================
echo.
echo Esto tomara 10-15 minutos.
echo El build se hace en los servidores de Expo.
echo Puedes cerrar esta ventana y ver el progreso en expo.dev
echo.

call eas build --platform android --profile preview

echo.
echo ========================================
echo Build completado!
echo ========================================
echo.
echo Descarga el APK del link que aparecio arriba
echo o ve a: https://expo.dev
echo.
pause
