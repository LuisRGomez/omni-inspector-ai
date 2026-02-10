@echo off
echo ========================================
echo BUILD APK - Omni Inspector
echo ========================================
echo.

echo Verificando Android Studio...
if not exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo ERROR: Android Studio no esta instalado o ANDROID_HOME no configurado
    echo.
    echo Descarga Android Studio de: https://developer.android.com/studio
    echo Luego configura ANDROID_HOME en variables de entorno
    echo.
    pause
    exit /b 1
)

echo Android Studio encontrado!
echo.

echo Instalando dependencias...
call npm install

echo.
echo Generando APK...
echo Esto puede tomar 5-10 minutos...
echo.

call npx expo run:android --variant release

echo.
echo ========================================
echo APK GENERADO!
echo ========================================
echo.
echo Ubicacion: android\app\build\outputs\apk\release\app-release.apk
echo.
pause
