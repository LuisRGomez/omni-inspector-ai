# 📱 INSTRUCCIONES SIMPLES - Omni Inspector

## 🎯 LO MÁS FÁCIL: USAR ANDROID STUDIO

### Opción 1: Script Automático
```
Doble click en: abrir-android-studio.bat
```

### Opción 2: Manual
1. Abre Android Studio
2. Click "Open"
3. Selecciona: `mobile-app\android`
4. Espera sync (2-3 min)
5. Click botón verde ▶️ "Run"
6. ¡Listo!

## 📱 CONECTAR CELULAR

1. Conecta por USB
2. En el celular:
   - Ajustes > Acerca del teléfono
   - Toca 7 veces "Número de compilación"
   - Vuelve > Opciones de desarrollador
   - Activa "Depuración USB"
3. Acepta el permiso en el celular
4. Verás tu celular en Android Studio

## 🚀 EJECUTAR LA APP

### Desde Android Studio:
1. Selecciona tu celular en el dropdown
2. Click ▶️ "Run"
3. Espera 2-5 minutos
4. ¡La app se abre en tu celular!

### Generar APK:
1. Menu: Build > Build APK(s)
2. Espera 2-3 minutos
3. Click "locate"
4. ¡APK listo para compartir!

## ✅ VENTAJAS

- **Más fácil** - Todo visual, sin comandos
- **Más rápido** - Android Studio optimiza todo
- **Debugging** - Ves logs en tiempo real
- **Hot reload** - Cambios instantáneos

## 🎮 PROBAR LA APP

1. Abre "Omni Inspector"
2. Selecciona módulo (Underwriting/Claims/Legal)
3. Completa formulario:
   - Contenedor: ABCD1234567
   - Precinto: SEAL123456
   - Ubicación: Puerto Buenos Aires
4. Toma 3-5 fotos
5. Presiona "Analizar"
6. ¡Ve los resultados de Bedrock!

## 📊 LO QUE ESTÁ FUNCIONANDO

✅ **Backend AWS:**
- Lambda: omni-inspector-bedrock-analyzer
- API Gateway: https://efjyl1of9i.execute-api.us-east-1.amazonaws.com/prod/analyze
- S3: omni-inspector-photos-prod
- Bedrock Nova Pro: Análisis con IA

✅ **Mobile App:**
- 4 pantallas completas
- Captura de fotos
- Análisis con IA
- Detección de fraude
- OCR de contenedor
- Verificación de precinto

## 🔧 SI ALGO FALLA

### Android Studio no abre:
```
Ejecuta: abrir-android-studio.bat
```

### Celular no aparece:
- Desconecta y reconecta USB
- Revoca permisos USB en el celular
- Acepta de nuevo

### Gradle sync failed:
- File > Invalidate Caches > Restart

### Build failed:
- Build > Clean Project
- Build > Rebuild Project

## 📞 ARCHIVOS IMPORTANTES

- `abrir-android-studio.bat` - Abre Android Studio
- `ABRIR-EN-ANDROID-STUDIO.md` - Guía detallada
- `RESUMEN-FINAL-COMPLETO.md` - Todo el proyecto
- `DEPLOYMENT-COMPLETE.md` - Backend AWS

## 🎉 RESUMEN

**TODO ESTÁ LISTO:**
- ✅ Backend AWS desplegado
- ✅ Mobile app completa
- ✅ Android Studio configurado
- ✅ Solo falta ejecutar!

**PRÓXIMO PASO:**
```
Doble click en: abrir-android-studio.bat
```

**¡En 5 minutos tendrás la app corriendo en tu celular! 🚀**
