# 🚀 OMNI INSPECTOR

App móvil de inspección con IA usando AWS Bedrock Nova Pro.

## ⚡ INICIO RÁPIDO

```bash
# Compilar APK Debug (más rápido, para pruebas)
scripts\compilar-debug-wsl.bat

# Compilar APK Release (optimizado, para producción)
scripts\compilar-react-native-wsl.bat
```

---

## 📊 ESTADO DEL PROYECTO

| Componente | Estado |
|------------|--------|
| Backend AWS | ✅ 100% Funcional |
| React Native App | ✅ Configurado |
| Integración | ✅ Lista |
| APK | 🔄 Listo para compilar |

---

## 📁 ESTRUCTURA

```
omni-inspector/
├── OmniInspector/           # App React Native (ACTUAL)
│   ├── src/
│   │   ├── screens/         # 4 pantallas
│   │   ├── navigation/      # React Navigation
│   │   ├── services/        # AWS Bedrock
│   │   └── config/          # Configuración
│   └── android/             # Código nativo
├── mobile-app/              # App Expo (OBSOLETA)
├── lambda-bedrock-analyzer.py  # Lambda AWS
├── scripts/                 # Scripts de compilación
│   ├── compilar-debug-wsl.bat
│   ├── compilar-react-native-wsl.bat
│   └── ...
├── docs/                    # Documentación
└── README.md               # Este archivo
```

---

## 🎯 SCRIPTS PRINCIPALES

### Compilación React Native
- `scripts/compilar-debug-wsl.bat` - APK Debug (rápido) ⭐
- `scripts/compilar-react-native-wsl.bat` - APK Release (optimizado) ⭐

### Scripts Expo (OBSOLETOS)
- `scripts/COMPILAR-WSL-COMPLETO.bat` - Ya no funciona (Expo abandonado)
- `scripts/GENERAR-APK-EAS.bat` - Ya no funciona (Expo abandonado)

---

## 📖 DOCUMENTACIÓN

### Principal
- `OmniInspector/README.md` - Documentación de la app React Native
- `START.md` - Guía de inicio rápido

### Carpeta docs/
- `RESUMEN-COMPLETO.md` - Resumen ejecutivo
- `DEPLOYMENT-COMPLETE.md` - Deploy AWS
- `ESTADO-FINAL.md` - Estado del proyecto

### Carpeta apk/
- `LEER-PRIMERO.md` - Información sobre APK
- `COMO-INSTALAR-APK.md` - Guía de instalación
- `EJECUTAR-AHORA.md` - Pasos para compilar
- `README-APK.md` - Documentación APK

---

## 🌐 BACKEND AWS

- **API**: https://efjyl1of9i.execute-api.us-east-1.amazonaws.com/prod/analyze
- **Lambda**: omni-inspector-bedrock-analyzer
- **S3**: omni-inspector-photos-prod
- **Bedrock**: Nova Pro (us.amazon.nova-pro-v1:0)
- **Región**: us-east-1

---

## 🔧 REQUISITOS

- Windows 10/11 con WSL (Ubuntu)
- Node.js 18+ (en WSL)
- Java 17+ (en WSL) ✅ Ya instalado
- Celular Android 5.0+

---

## 🔗 PROYECTOS RELACIONADOS

### Jira MCP Extended
MCP Server para gestión completa de proyectos Jira (45 tools).

**Repositorio independiente:** https://github.com/LuisRGomez/jira-mcp-extended

Funcionalidades:
- ✅ Gestión de Issues (Epics, Stories, Tasks, Bugs, Sub-tasks)
- ✅ Administración de Proyectos
- ✅ Sprints y Boards Agile
- ✅ Workflows y permisos
- ✅ Integración con Kiro AI

---

## 📱 USO

1. **Compilar APK Debug**: `scripts\compilar-debug-wsl.bat`
2. **Instalar**: Copiar APK al celular vía USB
3. **Usar**: Abrir "Omni Inspector" en el celular

---

## 🎉 FUNCIONALIDADES

### Backend
- ✅ Análisis con Bedrock Nova Pro
- ✅ Detección de fraude
- ✅ Verificación de precintos
- ✅ OCR de contenedores

### Mobile App (React Native)
- ✅ 4 pantallas (Home, Inspección, Cámara, Resultados)
- ✅ React Navigation
- ✅ React Native Vision Camera
- ✅ Integración AWS Bedrock
- ✅ UI profesional

---

## 🔄 MIGRACIÓN EXPO → REACT NATIVE

**Por qué migramos:**
- Expo tenía conflictos de Gradle insolubles
- React Native puro es más estable
- Mejor control sobre dependencias nativas
- Compilación más confiable

**Estado:**
- ✅ Todas las pantallas migradas
- ✅ Navegación configurada
- ✅ Permisos Android configurados
- ✅ Camera configurada
- 🔄 Listo para compilar APK

---

## 📞 INFORMACIÓN

- **GitHub**: https://github.com/LuisRGomez/omni-inspector-ai
- **AWS Account**: 472661249377
- **Proyecto**: React Native 0.83 + AWS Bedrock

---

**Desarrollado con ❤️ usando React Native + AWS Bedrock Nova Pro**
