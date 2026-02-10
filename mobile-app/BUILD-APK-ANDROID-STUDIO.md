# 📦 Generar APK con Android Studio

## 🎯 Ventajas de Android Studio

- ✅ Build local (no depende de servidores)
- ✅ Más rápido una vez configurado
- ✅ Control total del proceso
- ✅ No hay límites de tamaño

## 📥 Paso 1: Instalar Android Studio

1. **Descargar:**
   - Ve a: https://developer.android.com/studio
   - Descarga Android Studio (1 GB aprox)

2. **Instalar:**
   - Ejecuta el instalador
   - Selecciona "Standard" installation
   - Acepta las licencias
   - Espera a que descargue componentes (~10 GB)

3. **Configurar:**
   - Abre Android Studio
   - Ve a: Tools > SDK Manager
   - Asegúrate de tener instalado:
     - Android SDK Platform 33 o superior
     - Android SDK Build-Tools
     - Android Emulator (opcional)

## 🔧 Paso 2: Configurar Variables de Entorno

### Windows:

1. Busca "Variables de entorno" en el menú inicio
2. Agrega estas variables:

```
ANDROID_HOME = C:\Users\TU_USUARIO\AppData\Local\Android\Sdk
```

3. Agrega a PATH:
```
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\tools\bin
```

4. Reinicia la terminal

## 🚀 Paso 3: Generar APK

### Opción A: Con Expo (Recomendado)

```bash
cd mobile-app

# Generar APK de desarrollo
npx expo run:android

# O generar APK de producción
eas build --platform android --profile production --local
```

### Opción B: Build Nativo

```bash
cd mobile-app

# Pre-build (genera carpetas android/)
npx expo prebuild

# Build con Gradle
cd android
./gradlew assembleRelease

# El APK estará en:
# android/app/build/outputs/apk/release/app-release.apk
```

## 📱 Paso 4: Instalar APK en tu Celular

### Método 1: USB

1. Conecta tu celular por USB
2. Habilita "Depuración USB" en opciones de desarrollador
3. Ejecuta:
```bash
adb install android/app/build/outputs/apk/release/app-release.apk
```

### Método 2: Compartir Archivo

1. Copia el APK a tu celular
2. Abre el archivo APK
3. Habilita "Instalar apps desconocidas"
4. Instala

## 🐛 Troubleshooting

### Error: "ANDROID_HOME not set"
```bash
# Windows
setx ANDROID_HOME "C:\Users\TU_USUARIO\AppData\Local\Android\Sdk"

# Reinicia la terminal
```

### Error: "SDK location not found"
Crea el archivo `android/local.properties`:
```
sdk.dir=C:\\Users\\TU_USUARIO\\AppData\\Local\\Android\\Sdk
```

### Error: "Gradle build failed"
```bash
cd android
./gradlew clean
./gradlew assembleRelease
```

### Error: "No connected devices"
```bash
# Ver dispositivos conectados
adb devices

# Si no aparece, verifica:
# 1. Depuración USB habilitada
# 2. Cable USB funcional
# 3. Drivers instalados
```

## ⚡ Build Rápido (Una vez configurado)

```bash
cd mobile-app
npx expo run:android --variant release
```

Esto:
1. Compila la app
2. Genera el APK
3. Lo instala en tu celular (si está conectado)

## 📊 Tamaños Esperados

- **APK Debug:** ~50-80 MB
- **APK Release:** ~30-50 MB
- **AAB (Play Store):** ~20-30 MB

## 🎯 Siguiente Paso

Una vez que tengas Android Studio instalado:

```bash
cd mobile-app
npx expo run:android
```

Esto generará el APK automáticamente.
