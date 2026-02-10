# 🔧 Solución: Error "Failed to download remote update"

Este error ocurre cuando Expo Go no puede descargar la app desde tu PC.

## ✅ Solución Rápida (Recomendada)

### Opción 1: Conectar Manualmente por IP

1. **En tu celular, abre Expo Go**

2. **NO escanees el QR**, en su lugar:
   - Toca en "Enter URL manually" (abajo)
   - Ingresa: `exp://10.2.20.151:8081`
   - Presiona "Connect"

3. **Si no funciona, prueba con localhost:**
   - Ingresa: `exp://localhost:8081`

### Opción 2: Usar Túnel (Más Lento pero Más Confiable)

1. **Detén el servidor** (Ctrl+C en la terminal)

2. **Inicia con túnel:**
```bash
npx expo start --tunnel
```

3. **Espera 30-60 segundos** a que se establezca el túnel

4. **Escanea el nuevo QR** que aparece

## 🔥 Solución de Firewall (Windows)

El firewall de Windows puede estar bloqueando la conexión.

### Ejecuta como Administrador:

```cmd
netsh advfirewall firewall add rule name="Expo Metro" dir=in action=allow protocol=TCP localport=8081
netsh advfirewall firewall add rule name="Expo Dev" dir=in action=allow protocol=TCP localport=19000-19006
```

O simplemente ejecuta el archivo: `start-with-firewall.bat` (como administrador)

## 📱 Verificar Conexión

### 1. Verifica que estés en la misma WiFi
- PC: Abre CMD y ejecuta `ipconfig`
- Busca tu IP (ej: 10.2.20.151)
- Celular: Ve a Configuración > WiFi > Detalles de red
- Verifica que ambos tengan IPs en el mismo rango (ej: 10.2.20.x)

### 2. Prueba la conexión
En tu celular, abre el navegador y ve a:
```
http://10.2.20.151:8081
```

Si ves una página de Expo, la conexión funciona.

## 🌐 Alternativa: Expo Go Development Build

Si nada funciona, puedes crear un build de desarrollo:

```bash
npx expo install expo-dev-client
npx expo run:android
```

Esto instalará la app directamente en tu celular sin necesidad de Expo Go.

## 🆘 Última Opción: Emulador Android

Si tienes Android Studio instalado:

```bash
# Inicia el emulador
# Luego en la terminal de Expo presiona:
a
```

Esto abrirá la app en el emulador de Android.

## 📞 Estado Actual

Tu servidor está corriendo en:
- **IP:** 10.2.20.151
- **Puerto:** 8081
- **URL:** exp://10.2.20.151:8081

Intenta conectarte manualmente con esa URL en Expo Go.
