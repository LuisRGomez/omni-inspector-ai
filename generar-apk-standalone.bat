@echo off
echo ========================================
echo GENERANDO APK STANDALONE
echo ========================================
echo.
echo Este APK NO necesita Metro ni servidor
echo Funcionara completamente independiente
echo.

cd mobile-app

echo Paso 1: Exportando bundle de produccion...
call npx expo export --platform android

echo.
echo Paso 2: Compilando APK con el bundle...
cd android

set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr

call gradlew.bat assembleRelease

echo.
if exist "app\build\outputs\apk\release\app-release.apk" (
    echo ========================================
    echo APK STANDALONE GENERADO!
    echo ========================================
    echo.
    copy "app\build\outputs\apk\release\app-release.apk" "..\..\omni-inspector-standalone.apk"
    echo.
    echo APK: omni-inspector-standalone.apk
    echo.
    echo Este APK funciona SIN servidor Metro
    echo Instalalo con:
    echo "%ANDROID_HOME%\platform-tools\adb.exe" install -r omni-inspector-standalone.apk
    echo.
) else (
    echo ERROR: APK no se genero
)

cd ..\..
pause
