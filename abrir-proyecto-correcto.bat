@echo off
echo ========================================
echo ABRIENDO PROYECTO EN ANDROID STUDIO
echo ========================================
echo.

echo IMPORTANTE: Si Android Studio ya esta abierto, cierralo primero!
echo.
pause

echo.
echo Abriendo Android Studio...
echo.

cd "%~dp0mobile-app\android"
start "" "C:\Program Files\Android\Android Studio\bin\studio64.exe" .

echo.
echo ========================================
echo PASOS EN ANDROID STUDIO:
echo ========================================
echo.
echo 1. Cuando se abra, ve a: File ^> Open
echo 2. Navega a: C:\Users\TitoGomez\Desktop\talos forencing\mobile-app\android
echo 3. Click "OK"
echo 4. Espera que sincronice (veras "Gradle sync" abajo)
echo 5. Cuando termine, conecta tu celular
echo 6. Click en el boton verde "Run" (play)
echo.
echo O MAS FACIL:
echo.
echo 1. File ^> Open
echo 2. Selecciona la carpeta "android"
echo 3. Espera sync
echo 4. Run!
echo.
pause
