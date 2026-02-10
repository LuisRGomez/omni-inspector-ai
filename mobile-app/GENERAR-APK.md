# 📦 Generar APK - Guía Rápida

## 🎯 Opción 1: Android Studio (RECOMENDADO)

### Paso 1: Instalar Android Studio
1. Descarga: https://developer.android.com/studio
2. Ejecuta el instalador
3. Selecciona "Standard" installation
4. Espera que descargue todo (~10 GB, 30-60 min)

### Paso 2: Configurar Variables de Entorno
1. Busca "Variables de entorno" en Windows
2. Agrega nueva variable de sistema:
   - Nombre: `ANDROID_HOME`
   - Valor: `C:\Users\TU_USUARIO\AppData\Local\Android\Sdk`
3. Edita PATH y agrega:
   - `%ANDROID_HOME%\platform-tools`
   - `%ANDROID_HOME%\tools`
4. Reinicia la terminal

### Paso 3: Generar APK
```bash
cd mobile-app
build-apk-simple.bat
```

Espera 5-10 minutos y listo!

**APK estará en:**
```
android\app\build\outputs\apk\release\app-release.apk
```

## 🎯 Opción 2: EAS Build (Cloud)

### Ventajas:
- No necesita Android Studio
- Build en la nube
- Más rápido si ya tenés cuenta

### Pasos:
```bash
cd mobile-app

# Login (si no lo hiciste)
eas login

# Build
eas build --platform android --profile preview
```

Espera 15-20 minutos y descarga el APK del link que te da.

## 🎯 Opción 3: Expo Build (Deprecated pero funciona)

```bash
cd mobile-app
expo build:android -t apk
```

## 📱 Instalar APK en tu Celular

### Método 1: USB
1. Conecta celular por USB
2. Habilita "Depuración USB" en opciones de desarrollador
3. Ejecuta:
```bash
adb install android\app\build\outputs\apk\release\app-release.apk
```

### Método 2: Compartir Archivo
1. Copia el APK a tu celular (WhatsApp, Drive, etc.)
2. Abre el archivo APK en tu celular
3. Habilita "Instalar apps desconocidas" si te lo pide
4. Instala

### Método 3: QR Code
1. Sube el APK a Google Drive o Dropbox
2. Genera link de descarga
3. Crea QR code del link
4. Escanea con tu celular

## 🐛 Problemas Comunes

### "ANDROID_HOME not set"
```bash
setx ANDROID_HOME "C:\Users\TU_USUARIO\AppData\Local\Android\Sdk"
# Reinicia la terminal
```

### "SDK location not found"
Crea `android/local.properties`:
```
sdk.dir=C:\\Users\\TU_USUARIO\\AppData\\Local\\Android\\Sdk
```

### "Gradle build failed"
```bash
cd android
./gradlew clean
./gradlew assembleRelease
```

### "No connected devices"
```bash
adb devices
# Si no aparece, verifica USB debugging
```

## ⚡ Build Rápido (Una vez configurado)

```bash
cd mobile-app
npx expo run:android --variant release
```

Esto compila, genera APK y lo instala automáticamente si tenés el celular conectado.

## 📊 Tamaños Esperados

- **APK Debug:** ~50-80 MB
- **APK Release:** ~30-50 MB
- **AAB (Play Store):** ~20-30 MB

## 🚀 Después de Instalar

1. Abre la app
2. Selecciona módulo
3. Completa formulario
4. Toma fotos
5. Analiza con Bedrock
6. Ve resultados

## 💡 Tips

- El APK funciona offline (excepto análisis AWS)
- Puedes compartir el APK con otros
- No necesita Expo Go
- Es una app nativa completa

## 📝 Notas

- Primera build tarda más (descarga dependencias)
- Builds siguientes son más rápidas
- El APK es para testing, no para Play Store
- Para Play Store necesitas AAB y firma

## ✅ Checklist

- [ ] Android Studio instalado
- [ ] ANDROID_HOME configurado
- [ ] Terminal reiniciada
- [ ] `build-apk-simple.bat` ejecutado
- [ ] APK generado
- [ ] APK instalado en celular
- [ ] App funcionando

## 🆘 Ayuda

Si algo falla:
1. Lee el error completo
2. Busca en Google el error específico
3. Verifica que Android Studio esté bien instalado
4. Verifica variables de entorno
5. Reinicia la terminal

## 🎯 Alternativa: Probar sin APK

Si no querés instalar Android Studio ahora:

1. Usa Expo Go (escanea QR)
2. Prueba en web (http://localhost:8081)
3. Genera APK después cuando tengas tiempo

**La app funciona igual en todas las plataformas!**
