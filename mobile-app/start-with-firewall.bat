@echo off
echo ========================================
echo Configurando Firewall para Expo...
echo ========================================
echo.

REM Agregar regla de firewall para Metro Bundler
netsh advfirewall firewall add rule name="Expo Metro Bundler" dir=in action=allow protocol=TCP localport=8081
netsh advfirewall firewall add rule name="Expo Metro Bundler 8082" dir=in action=allow protocol=TCP localport=8082
netsh advfirewall firewall add rule name="Expo Dev Server" dir=in action=allow protocol=TCP localport=19000-19006

echo.
echo Firewall configurado!
echo.
echo ========================================
echo Iniciando Expo en modo LAN...
echo ========================================
echo.

call npm start -- --lan

pause
