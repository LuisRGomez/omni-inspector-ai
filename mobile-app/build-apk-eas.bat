@echo off
echo ========================================
echo GENERANDO APK CON EAS BUILD
echo ========================================
echo.

echo Este metodo es MAS SIMPLE y RAPIDO
echo El build se hace en la nube de Expo
echo.

echo Iniciando build...
echo.

call eas build --platform android --profile preview --non-interactive

echo.
echo ========================================
echo BUILD INICIADO!
echo ========================================
echo.
echo El APK se esta generando en la nube
echo Tiempo estimado: 10-15 minutos
echo.
echo Puedes ver el progreso en:
echo https://expo.dev/accounts/titog/projects/omni-inspector/builds
echo.
echo Cuando termine, recibiras un link de descarga
echo.
pause
