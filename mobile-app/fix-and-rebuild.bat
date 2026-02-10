@echo off
echo ========================================
echo Solucionando problemas del build...
echo ========================================
echo.

echo Paso 1: Actualizando dependencias...
call npm install expo@latest
call npm install react-native@0.74.5
call npm install react-native-safe-area-context@4.10.5
call npm install expo-image-picker@~15.1.0
call npm install typescript@~5.3.3

echo.
echo Paso 2: Limpiando cache...
call npx expo install --fix

echo.
echo Paso 3: Iniciando build con cache limpio...
call eas build --platform android --profile preview --clear-cache

echo.
echo ========================================
echo Proceso completado!
echo ========================================
pause
