# Omni Inspector - Mobile App

Aplicación móvil para inspección forense de contenedores, vehículos y carga usando IA.

## 🚀 Características

- **3 Módulos de Negocio:**
  - 🛡️ Alta de Riesgo (Underwriting)
  - 📋 Siniestros (Claims)
  - ⚖️ Recupero Legal (Legal Recovery)

- **Captura de Evidencia:**
  - Cámara de alta calidad
  - Múltiples fotos por inspección
  - Guardado automático en galería

- **Análisis con IA:**
  - Detección de daños
  - Clasificación de severidad
  - Detección de fraude
  - OCR de números de contenedor

## 📦 Instalación

```bash
cd mobile-app
npm install
```

## 🏃 Ejecutar

### iOS
```bash
npm run ios
```

### Android
```bash
npm run android
```

### Web (desarrollo)
```bash
npm run web
```

## 🛠️ Stack Tecnológico

- **Framework:** React Native + Expo
- **Navegación:** Expo Router
- **Cámara:** Expo Camera
- **Backend:** AWS (Amplify, S3, Bedrock, SageMaker)
- **Lenguaje:** TypeScript

## 📱 Estructura de Pantallas

```
/                    → Home (selección de módulo)
/inspection          → Formulario de inspección
/camera              → Captura de fotos
/results             → Resultados del análisis IA
```

## 🔐 Permisos Requeridos

- Cámara
- Galería de fotos
- Micrófono (para videos)
- Ubicación (opcional)

## 🌐 Integración AWS

La app se conectará a:
- **S3:** Almacenamiento de fotos
- **Bedrock:** Análisis multimodal con Nova Pro
- **SageMaker:** Detección de objetos con YOLOv11
- **Cognito:** Autenticación de usuarios

## 📝 Próximos Pasos

1. Configurar AWS Amplify
2. Integrar autenticación
3. Conectar con backend serverless
4. Implementar upload a S3
5. Integrar análisis IA en tiempo real
