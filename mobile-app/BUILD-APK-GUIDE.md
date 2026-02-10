# 📦 Guía para Crear APK de Omni Inspector

## 🚀 Pasos para Generar el APK

### 1. Login en Expo (Primera vez)

```bash
cd mobile-app
eas login
```

Si no tienes cuenta:
- Ve a https://expo.dev
- Crea una cuenta gratis
- Usa esas credenciales para login

### 2. Configurar el Proyecto

```bash
eas build:configure
```

Esto creará el archivo `eas.json` (ya está creado).

### 3. Crear el Build APK

```bash
eas build --platform android --profile preview
```

**Opciones:**
- `preview`: APK para instalar directamente (recomendado)
- `production`: AAB para Google Play Store

### 4. Esperar el Build

El build se hace en los servidores de Expo (no en tu PC).
- Tiempo estimado: 10-15 minutos
- Puedes ver el progreso en: https://expo.dev/accounts/[tu-usuario]/projects/omni-inspector/builds

### 5. Descargar e Instalar

Una vez completado:
1. Recibirás un link de descarga
2. Descarga el APK en tu celular
3. Instala el APK (necesitas habilitar "Instalar apps desconocidas")

## 📱 Instalación en Android

1. Descarga el APK en tu celular
2. Ve a Configuración > Seguridad
3. Habilita "Instalar apps desconocidas" para tu navegador
4. Abre el APK descargado
5. Presiona "Instalar"

## 🆓 Límites del Plan Gratuito

Expo ofrece:
- ✅ Builds ilimitados para desarrollo
- ✅ 30 builds/mes en el plan gratuito
- ✅ Almacenamiento de builds por 30 días

## 🔄 Actualizar la App

Para crear una nueva versión:

1. Actualiza el código
2. Incrementa la versión en `app.json`:
```json
"version": "1.0.1"
```
3. Ejecuta nuevamente:
```bash
eas build --platform android --profile preview
```

## 🌐 Alternativa: Build Local

Si prefieres hacer el build en tu PC (requiere Android Studio):

```bash
eas build --platform android --profile preview --local
```

Esto toma más tiempo pero no usa los servidores de Expo.

## 📝 Notas Importantes

- El APK generado es una app completa, NO necesita Expo Go
- Funciona offline (excepto las llamadas a AWS)
- Puedes compartir el APK con otros usuarios
- Para iOS necesitas una cuenta de Apple Developer ($99/año)

## 🐛 Troubleshooting

### Error: "Not logged in"
```bash
eas login
```

### Error: "Project not configured"
```bash
eas build:configure
```

### Error: "Build failed"
- Revisa los logs en expo.dev
- Verifica que `app.json` esté correcto
- Asegúrate de que todas las dependencias estén instaladas

## 🎯 Siguiente Paso

Una vez que tengas el APK instalado, podrás:
1. Probar la app sin problemas de red
2. Capturar fotos reales
3. Integrar con el backend AWS
4. Hacer demos profesionales
