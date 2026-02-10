@echo off
echo ========================================
echo ABRIENDO ANDROID STUDIO
echo ========================================
echo.

echo Abriendo proyecto en Android Studio...
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" "%~dp0mobile-app\android"

echo.
echo Android Studio se esta abriendo...
echo.
echo PASOS A SEGUIR:
echo.
echo 1. Espera que sincronice (2-3 minutos)
echo 2. Conecta tu celular por USB
echo 3. Habilita "Depuracion USB" en el celular
echo 4. Click en el boton verde "Run" (play)
echo 5. Espera 2-5 minutos
echo 6. La app se instalara automaticamente!
echo.
echo O para generar APK:
echo Menu: Build ^> Build Bundle(s) / APK(s) ^> Build APK(s)
echo.
pause
