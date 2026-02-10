@echo off
echo ========================================
echo GENERANDO APK DIRECTAMENTE
echo ========================================
echo.

cd mobile-app\android

echo Configurando variables...
set ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
set JAVA_HOME=C:\Program Files\Android\Android Studio\jbr

echo.
echo Generando APK de debug (mas rapido)...
echo.

call gradlew.bat assembleDebug

echo.
if exist "app\build\outputs\apk\debug\app-debug.apk" (
    echo ========================================
    echo APK GENERADO!
    echo ========================================
    echo.
    copy "app\build\outputs\apk\debug\app-debug.apk" "..\..\omni-inspector-debug.apk"
    echo.
    echo APK copiado a: omni-inspector-debug.apk
    echo.
    echo INSTALAR EN CELULAR:
    echo "%ANDROID_HOME%\platform-tools\adb.exe" install omni-inspector-debug.apk
    echo.
) else (
    echo ERROR: APK no se genero
)

pause
