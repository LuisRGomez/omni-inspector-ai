@echo off
echo ========================================
echo VERIFICANDO ESTADO DEL APK
echo ========================================
echo.

echo Buscando APK...
if exist "mobile-app\android\app\build\outputs\apk\release\app-release.apk" (
    echo.
    echo ========================================
    echo APK ENCONTRADO!
    echo ========================================
    echo.
    echo Ubicacion: mobile-app\android\app\build\outputs\apk\release\app-release.apk
    echo.
    dir "mobile-app\android\app\build\outputs\apk\release\app-release.apk"
    echo.
    echo Copiando a la raiz...
    copy "mobile-app\android\app\build\outputs\apk\release\app-release.apk" "omni-inspector.apk"
    echo.
    echo APK copiado a: omni-inspector.apk
    echo.
    echo LISTO PARA INSTALAR!
) else (
    echo APK aun no generado...
    echo.
    echo Verificando procesos Java/Gradle...
    tasklist | findstr /i "java.exe"
    echo.
    echo El build sigue en progreso. Espera unos minutos mas...
)

echo.
pause
