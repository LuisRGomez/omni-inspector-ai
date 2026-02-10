@echo off
echo ========================================
echo INSTALAR APP EN TU CELULAR - SIMPLE
echo ========================================
echo.

echo Conecta tu celular por USB
echo.
pause

echo.
echo Instalando app en tu celular...
echo.

"C:\Users\%USERNAME%\AppData\Local\Android\Sdk\platform-tools\adb.exe" install -r "mobile-app\android\app\build\outputs\apk\debug\app-debug.apk"

echo.
echo Iniciando servidor Metro...
echo.

cd mobile-app
start cmd /k "npx expo start"

echo.
echo ========================================
echo LISTO!
echo ========================================
echo.
echo 1. Espera 30 segundos a que cargue Metro
echo 2. Abre "Omni Inspector" en tu celular
echo 3. Deberia funcionar!
echo.
echo Si sale error rojo, presiona R dos veces
echo.
pause
