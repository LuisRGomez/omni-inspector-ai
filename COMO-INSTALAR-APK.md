# 📱 Cómo Instalar el APK - Omni Inspector

## 🎯 CUANDO EL APK ESTÉ LISTO

El APK se está generando ahora. Cuando termine, estará en:
```
omni-inspector.apk (en la raíz del proyecto)
```

## 📥 MÉTODOS DE INSTALACIÓN

### Método 1: USB (MÁS RÁPIDO)

1. **Conecta tu celular por USB**
2. **Habilita Depuración USB:**
   - Ve a Ajustes > Acerca del teléfono
   - Toca 7 veces en "Número de compilación"
   - Vuelve a Ajustes > Opciones de desarrollador
   - Activa "Depuración USB"
3. **Instala:**
```bash
adb install omni-inspector.apk
```

### Método 2: Compartir Archivo (MÁS FÁCIL)

1. **Envía el APK por WhatsApp/Email/Drive**
2. **Abre el archivo en tu celular**
3. **Habilita "Instalar apps desconocidas"** (si te lo pide)
4. **Presiona "Instalar"**
5. **¡Listo!**

### Método 3: Servidor Local

1. **Copia el APK a una carpeta accesible**
2. **Comparte por red local**
3. **Descarga desde el celular**
4. **Instala**

## 🧪 PROBAR LA APP

### Primera Vez:

1. **Abre "Omni Inspector"**
2. **Selecciona un módulo:**
   - Underwriting (Suscripción)
   - Claims (Reclamos)
   - Legal Recovery (Recupero Legal)

3. **Completa el formulario:**
   - Contenedor: ABCD1234567
   - Precinto: SEAL123456
   - Ubicación: Puerto Buenos Aires

4. **Toma fotos:**
   - Mínimo 1, máximo 10
   - Toma fotos del contenedor desde diferentes ángulos

5. **Presiona "Analizar"**
   - La app enviará las fotos a AWS
   - Bedrock Nova Pro las analizará
   - Verás los resultados en 10-30 segundos

### Resultados Esperados:

```
✅ Daños detectados (tipo, severidad, ubicación)
✅ Score de fraude (0-1)
✅ Estado del precinto (intacto/manipulado)
✅ Número de contenedor (OCR)
✅ Recomendaciones
```

## 📊 FUNCIONALIDADES

### Offline:
- ✅ Captura de fotos
- ✅ Formulario de inspección
- ✅ Navegación entre pantallas

### Online (requiere internet):
- ✅ Upload de fotos a S3
- ✅ Análisis con Bedrock Nova Pro
- ✅ Detección de fraude
- ✅ OCR de contenedor

## 🔧 TROUBLESHOOTING

### "No se puede instalar"
- Habilita "Instalar apps desconocidas" en Ajustes
- Verifica que tengas espacio suficiente (~50 MB)

### "La app se cierra"
- Verifica que tengas Android 5.0 o superior
- Reinicia el celular
- Reinstala la app

### "No analiza las fotos"
- Verifica que tengas internet
- Verifica que las fotos se hayan tomado correctamente
- Intenta con menos fotos (3-5)

### "Error de conexión"
- Verifica tu conexión a internet
- El backend AWS debe estar activo
- Intenta de nuevo en unos segundos

## 📱 REQUISITOS

- **Android:** 5.0 o superior
- **Espacio:** ~50 MB
- **Internet:** Solo para análisis (opcional para captura)
- **Cámara:** Requerida
- **Permisos:** Cámara, Almacenamiento

## 🎯 DATOS DE PRUEBA

### Inspección de Prueba:
```
Módulo: Underwriting
Contenedor: TEST1234567
Precinto: SEAL001
Ubicación: Puerto Buenos Aires
Fotos: 3-5 fotos del contenedor
```

### Resultado Esperado:
```
Análisis completo en 10-30 segundos
Daños: Lista de daños detectados
Fraude: Score entre 0-1
Precinto: Estado verificado
Contenedor: Número extraído por OCR
```

## 🚀 DESPUÉS DE INSTALAR

1. **Prueba con inspección real**
2. **Verifica que el análisis funcione**
3. **Revisa los resultados**
4. **Ajusta según necesites**

## 📞 SOPORTE

### Backend AWS:
- Lambda: omni-inspector-bedrock-analyzer
- API: https://efjyl1of9i.execute-api.us-east-1.amazonaws.com/prod/analyze
- S3: omni-inspector-photos-prod

### Logs:
```bash
aws logs tail /aws/lambda/omni-inspector-bedrock-analyzer --follow
```

## ✅ CHECKLIST

- [ ] APK generado
- [ ] APK copiado a celular
- [ ] App instalada
- [ ] Permisos otorgados
- [ ] Inspección de prueba realizada
- [ ] Análisis funcionando
- [ ] Resultados verificados

## 🎉 ¡LISTO!

Una vez instalado, tendrás una app profesional de inspección con IA que:
- Captura fotos
- Analiza con Bedrock Nova Pro
- Detecta fraude
- Verifica precintos
- Extrae números de contenedor

**¡Todo funcionando en tu celular! 🚀**
