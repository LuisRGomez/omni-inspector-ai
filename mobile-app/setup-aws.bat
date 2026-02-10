@echo off
echo ========================================
echo Configuracion AWS Amplify
echo ========================================
echo.
echo Este script configurara AWS Amplify para Omni Inspector
echo.
echo REQUISITOS:
echo - Tener AWS CLI instalado y configurado
echo - Tener credenciales AWS con permisos necesarios
echo.
pause
echo.

echo Paso 1: Instalando AWS Amplify...
call npm install aws-amplify @aws-amplify/react-native amazon-cognito-identity-js @react-native-community/netinfo @react-native-async-storage/async-storage

echo.
echo Paso 2: Instalando Amplify CLI...
call npm install -g @aws-amplify/cli

echo.
echo Paso 3: Configurando Amplify...
echo Ejecuta manualmente:
echo   amplify init
echo   amplify add auth
echo   amplify add storage
echo   amplify add api
echo   amplify push
echo.
echo ========================================
echo Configuracion completada!
echo ========================================
pause
