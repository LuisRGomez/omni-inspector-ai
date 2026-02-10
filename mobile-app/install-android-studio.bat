@echo off
echo ========================================
echo Instalacion Android Studio
echo ========================================
echo.
echo PASOS MANUALES:
echo.
echo 1. Descarga Android Studio desde:
echo    https://developer.android.com/studio
echo.
echo 2. Ejecuta el instalador
echo.
echo 3. Durante la instalacion, asegurate de seleccionar:
echo    - Android SDK
echo    - Android SDK Platform
echo    - Android Virtual Device
echo.
echo 4. Una vez instalado, abre Android Studio y:
echo    - Acepta las licencias
echo    - Descarga los componentes necesarios
echo.
echo 5. Luego ejecuta en mobile-app:
echo    npx expo run:android
echo.
echo ========================================
echo.
echo Abriendo pagina de descarga...
start https://developer.android.com/studio
echo.
pause
