# 🔧 Troubleshooting - Omni Inspector App

## Error: "Algo salió mal" en Expo Go

### Solución 1: Verificar que estés en la misma red WiFi
- Tu celular y tu PC deben estar en la misma red WiFi
- Desactiva VPN si tienes una activa
- Verifica que tu firewall no esté bloqueando el puerto 8081

### Solución 2: Limpiar caché y reiniciar
```bash
# En la terminal donde corre Expo, presiona:
Shift + R  # Para limpiar caché y recargar
```

O reinicia el servidor:
```bash
cd mobile-app
npx expo start --clear
```

### Solución 3: Usar túnel de Expo
Si tu red tiene problemas, usa el túnel:
```bash
npx expo start --tunnel
```
Esto es más lento pero funciona en cualquier red.

### Solución 4: Probar en el navegador primero
```bash
# En la terminal donde corre Expo, presiona:
w  # Para abrir en navegador web
```

### Solución 5: Verificar versiones
El error puede ser por versiones incompatibles. Actualiza:
```bash
npm install expo@latest expo-camera@latest expo-router@latest
```

## Error: "Network response timed out"
- Verifica tu conexión WiFi
- Reinicia el router
- Usa `npx expo start --tunnel`

## Error: Permisos de cámara
- Ve a Configuración > Apps > Expo Go > Permisos
- Activa Cámara y Almacenamiento

## Error: "Unable to resolve module"
```bash
# Limpia node_modules y reinstala
rm -rf node_modules
npm install
npx expo start --clear
```

## Logs en Tiempo Real
Para ver errores detallados, mira la terminal donde corre `npm start`.
Los errores aparecerán ahí cuando intentes abrir la app.

## Contacto
Si el error persiste, comparte:
1. El mensaje de error exacto de Expo Go
2. Los logs de la terminal
3. Tu versión de Expo Go (en la app)
