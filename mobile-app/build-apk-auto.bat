@echo off
echo ========================================
echo GENERANDO APK - OMNI INSPECTOR
echo ========================================
echo.

REM Configurar ANDROID_HOME
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools

echo Configuracion:
echo ANDROID_HOME: %ANDROID_HOME%
echo.

echo Verificando Android SDK...
if not exist "%ANDROID_HOME%\platform-tools\adb.exe" (
    echo ERROR: Android SDK no encontrado
    pause
    exit /b 1
)
echo Android SDK encontrado!
echo.

echo Generando carpetas nativas...
echo Y | call npx expo prebuild --clean --platform android

if errorlevel 1 (
    echo.
    echo ERROR en prebuild, intentando sin --clean...
    echo Y | call npx expo prebuild --platform android
)

echo.
echo Compilando APK...
echo Esto puede tomar 5-10 minutos...
echo.

cd android
call gradlew.bat assembleRelease

echo.
echo ========================================
echo APK GENERADO!
echo ========================================
echo.

cd ..
if exist "android\app\build\outputs\apk\release\app-release.apk" (
    echo Copiando APK...
    copy "android\app\build\outputs\apk\release\app-release.apk" "omni-inspector.apk"
    echo.
    echo ========================================
    echo LISTO! APK en: omni-inspector.apk
    echo ========================================
) else (
    echo ERROR: APK no se genero
)

echo.
pause
