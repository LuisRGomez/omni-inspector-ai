---
inclusion: auto
---

# Reglas de Trabajo con Jira - Proyecto Omni Inspector

**Proyecto**: Omni Inspector - TFLite Real-Time Detection  
**Metodología**: Kanban con tracking completo en Jira  
**Rol**: Desarrollador simulado con documentación profesional

---

## 🎯 Objetivo

Trabajar como un desarrollador profesional usando Jira para:
- Trackear progreso de tareas
- Documentar decisiones técnicas
- Reportar bugs encontrados
- Identificar deuda técnica
- Mantener historial completo del desarrollo

---

## 📋 Estructura del Proyecto Jira

### Proyecto
```
Nombre: Omni Inspector - TFLite Detection
Tipo: Kanban
Key: OMNI
```

### Épicas (12 total)
```
OMNI-EPIC-1: Phase 1 - Setup TFLite Model
OMNI-EPIC-2: Phase 2 - Install Dependencies
OMNI-EPIC-3: Phase 3 - Create TFLiteDetectionService
OMNI-EPIC-4: Phase 4 - Modify CameraScreen
OMNI-EPIC-5: Phase 5 - Enhance UI with POC Look & Feel
OMNI-EPIC-6: Phase 6 - Create Backend API
OMNI-EPIC-7: Phase 7 - Create AnalysisService
OMNI-EPIC-8: Phase 8 - Integrate Analysis in CameraScreen
OMNI-EPIC-9: Phase 9 - Testing
OMNI-EPIC-10: Phase 10 - Optimization
OMNI-EPIC-11: Phase 11 - Build and Deploy
OMNI-EPIC-12: Phase 12 - Documentation
```

### Columnas del Board
```
1. Backlog       - Tareas pendientes
2. To Do         - Listas para empezar
3. In Progress   - Trabajando actualmente
4. Review        - Esperando validación
5. Done          - Completadas
```

---

## 🔄 Workflow de Tareas

### Al Empezar una Tarea

1. **Mover card a "In Progress"**
2. **Agregar comentario inicial**:
   ```
   🚀 Empezando implementación
   📅 Inicio: [timestamp]
   ```

### Durante la Implementación

**Agregar comentarios según lo que pase**:

#### ✅ Progreso Normal
```
✅ [Descripción del avance]
📝 Detalles técnicos relevantes
⏱️ Tiempo estimado restante: X min
```

#### ⚠️ Deuda Técnica Identificada
```
⚠️ DEUDA TÉCNICA DETECTADA

Descripción: [Qué se hizo de forma subóptima]
Razón: [Por qué se hizo así]
Impacto: [Bajo/Medio/Alto]
Solución futura: [Cómo mejorarlo]
Estimación: [Tiempo para arreglarlo]

Ejemplo:
⚠️ DEUDA TÉCNICA DETECTADA

Descripción: Throttling implementado con setTimeout en lugar de requestAnimationFrame
Razón: Más simple para MVP, funciona bien en pruebas
Impacto: Bajo - puede causar micro-stutters en dispositivos lentos
Solución futura: Migrar a requestAnimationFrame con frame skipping inteligente
Estimación: 30 minutos
```

#### 🐛 Bug Encontrado
```
🐛 BUG ENCONTRADO

Título: [Descripción corta del bug]
Severidad: [Critical/High/Medium/Low]
Descripción: [Qué está pasando]
Pasos para reproducir:
1. [Paso 1]
2. [Paso 2]
3. [Resultado esperado vs actual]

Workaround temporal: [Si existe]
Solución propuesta: [Cómo arreglarlo]

Crear issue separado: [Sí/No]
```

**Si el bug es crítico, crear issue de tipo "Bug" en Jira**

#### 📝 Nota Técnica
```
📝 NOTA TÉCNICA

[Información relevante para el futuro]
[Decisiones de diseño]
[Alternativas consideradas]
```

#### 🔍 Investigación Necesaria
```
🔍 INVESTIGACIÓN REQUERIDA

Tema: [Qué necesita investigarse]
Razón: [Por qué es necesario]
Bloqueante: [Sí/No]
Tiempo estimado: [X horas]
```

#### ⏸️ Bloqueado
```
⏸️ BLOQUEADO

Razón: [Por qué está bloqueado]
Dependencia: [De qué depende]
Acción requerida: [Qué se necesita para desbloquearlo]
```

### Al Completar una Tarea

1. **Agregar comentario final**:
   ```
   ✅ COMPLETADO
   
   Resumen:
   - [Qué se implementó]
   - [Archivos modificados/creados]
   - [Tests agregados]
   
   Tiempo real: [X horas/minutos]
   Tiempo estimado: [Y horas/minutos]
   
   Deuda técnica: [Ninguna / Ver comentario anterior]
   Bugs encontrados: [Ninguno / Ver issues creados]
   
   Siguiente paso: [Qué tarea sigue]
   ```

2. **Mover card a "Done"**
3. **Actualizar tiempo real vs estimado**

---

## 🐛 Gestión de Bugs

### Cuándo Crear un Bug Issue

Crear issue separado de tipo "Bug" cuando:
- Severidad es High o Critical
- Afecta funcionalidad existente
- Requiere investigación profunda
- No se puede arreglar en la tarea actual

### Template de Bug Issue

```
Título: [BUG] [Descripción corta]

Tipo: Bug
Prioridad: [Highest/High/Medium/Low]
Severidad: [Critical/High/Medium/Low]
Epic: [Epic relacionado]
Labels: bug, [componente afectado]

Descripción:
[Descripción detallada del problema]

Pasos para Reproducir:
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

Resultado Esperado:
[Qué debería pasar]

Resultado Actual:
[Qué está pasando]

Entorno:
- OS: [Android/iOS/Ambos]
- Versión: [X.X.X]
- Dispositivo: [Modelo]

Logs/Screenshots:
[Si aplica]

Workaround:
[Si existe una solución temporal]

Impacto:
[Cómo afecta a los usuarios]

Solución Propuesta:
[Cómo arreglarlo]
```

---

## 📊 Labels a Usar

### Por Tipo
- `setup` - Configuración inicial
- `model` - Relacionado con modelo ML
- `tflite` - TensorFlow Lite específico
- `ui` - Interfaz de usuario
- `backend` - API/servidor
- `testing` - Tests
- `documentation` - Docs
- `optimization` - Mejoras de performance
- `bug` - Bugs
- `technical-debt` - Deuda técnica

### Por Componente
- `camera` - CameraScreen
- `detection-service` - TFLiteDetectionService
- `analysis-service` - AnalysisService
- `forensic` - forensic_analyzer.py
- `bedrock` - AWS Bedrock
- `gradle` - Configuración Android

### Por Prioridad
- `critical` - Bloqueante, debe arreglarse YA
- `high-priority` - Importante, próxima tarea
- `low-priority` - Puede esperar

---

## 🎯 Story Points

Usar escala Fibonacci para estimar:

```
1 punto  = 15-30 min   (Tarea trivial)
2 puntos = 30-60 min   (Tarea simple)
3 puntos = 1-2 horas   (Tarea normal)
5 puntos = 2-4 horas   (Tarea compleja)
8 puntos = 4-8 horas   (Tarea muy compleja)
13 puntos = > 8 horas  (Épica, dividir en subtasks)
```

---

## 📝 Comentarios Automáticos

### Al Empezar el Día
```
📅 DÍA [N] - [Fecha]

Plan del día:
- [ ] [Tarea 1]
- [ ] [Tarea 2]
- [ ] [Tarea 3]

Objetivo: [Qué se quiere lograr hoy]
```

### Al Terminar el Día
```
📊 RESUMEN DEL DÍA [N]

Completado:
✅ [Tarea 1] - [Tiempo real]
✅ [Tarea 2] - [Tiempo real]

En progreso:
🔄 [Tarea 3] - [% completado]

Bloqueadores:
⏸️ [Si hay alguno]

Deuda técnica identificada:
⚠️ [Resumen]

Bugs encontrados:
🐛 [Resumen]

Plan para mañana:
- [ ] [Tarea siguiente]
```

---

## 🔗 Links entre Issues

### Tipos de Relaciones
- **Blocks** - Esta tarea bloquea otra
- **Is blocked by** - Esta tarea está bloqueada por otra
- **Relates to** - Relacionada con otra tarea
- **Duplicates** - Duplicado de otra issue
- **Causes** - Esta tarea causa un bug
- **Is caused by** - Este bug es causado por una tarea

### Ejemplo
```
OMNI-15 (Implementar frame processor)
  → Blocks → OMNI-20 (Renderizar bounding boxes)
  → Relates to → OMNI-10 (Instalar react-native-fast-tflite)
```

---

## 📈 Métricas a Trackear

### Por Sprint/Semana
- Velocity (story points completados)
- Tiempo real vs estimado
- Bugs encontrados vs resueltos
- Deuda técnica acumulada

### Por Tarea
- Tiempo de ciclo (To Do → Done)
- Número de comentarios
- Número de subtasks
- Complejidad real vs estimada

---

## 🎨 Formato de Commits (si aplica)

Cuando haga commits, usar formato convencional:

```
[OMNI-XX] tipo: descripción corta

Descripción detallada si es necesario

Closes OMNI-XX
```

Tipos:
- `feat`: Nueva funcionalidad
- `fix`: Bug fix
- `refactor`: Refactorización
- `test`: Tests
- `docs`: Documentación
- `chore`: Tareas de mantenimiento

---

## 🚨 Reglas Críticas

### SIEMPRE
1. ✅ Mover card antes de empezar a trabajar
2. ✅ Agregar comentario al empezar
3. ✅ Documentar deuda técnica cuando la identifiques
4. ✅ Crear bug issue si es High/Critical
5. ✅ Agregar comentario final al completar
6. ✅ Actualizar tiempo real vs estimado

### NUNCA
1. ❌ Dejar card en "In Progress" sin comentarios
2. ❌ Marcar como Done sin comentario final
3. ❌ Ignorar bugs encontrados
4. ❌ Ocultar deuda técnica
5. ❌ Saltarse documentación de decisiones

---

## 📚 Ejemplos Reales

### Ejemplo 1: Tarea Normal
```
Card: OMNI-13 - Implementar método detectObjects()

Comentario 1 (10:30):
🚀 Empezando implementación
📅 Inicio: 11/02/2026 10:30

Comentario 2 (10:45):
✅ Método básico implementado
📝 Usando modelo.detect() de react-native-fast-tflite
⏱️ Tiempo estimado restante: 15 min

Comentario 3 (11:00):
⚠️ DEUDA TÉCNICA DETECTADA

Descripción: No hay manejo de errores si el modelo falla
Razón: Enfocado en happy path para MVP
Impacto: Medio - app puede crashear si modelo no carga
Solución futura: Agregar try-catch y fallback a detección mock
Estimación: 20 minutos

Comentario 4 (11:05):
✅ COMPLETADO

Resumen:
- Implementado detectObjects() con throttling
- Agregado filtrado de clases relevantes
- Archivos: TFLiteDetectionService.ts

Tiempo real: 35 minutos
Tiempo estimado: 30 minutos

Deuda técnica: Ver comentario anterior (manejo de errores)
Bugs encontrados: Ninguno

Siguiente paso: OMNI-14 - Agregar manejo de errores
```

### Ejemplo 2: Bug Crítico Encontrado
```
Card: OMNI-25 - Integrar frame processor en CameraScreen

Comentario 1 (14:00):
🚀 Empezando integración

Comentario 2 (14:30):
🐛 BUG ENCONTRADO

Título: Frame processor causa crash en Android 11
Severidad: Critical
Descripción: Al activar detección, app crashea inmediatamente en Android 11

Pasos para reproducir:
1. Abrir app en Android 11
2. Ir a CameraScreen
3. Toggle detección ON
4. App crashea

Workaround temporal: Deshabilitar frame processor en Android < 12
Solución propuesta: Investigar compatibilidad de Worklets

Crear issue separado: Sí

Comentario 3 (14:35):
⏸️ BLOQUEADO

Razón: Bug crítico debe resolverse primero
Dependencia: OMNI-BUG-1
Acción requerida: Investigar y arreglar compatibilidad Android 11

---

Issue Creado: OMNI-BUG-1
Título: [BUG] Frame processor crashea en Android 11
Prioridad: Highest
Severidad: Critical
```

---

## 🎯 Objetivo Final

Mantener un **historial completo y profesional** del desarrollo que permita:
- Ver exactamente qué se hizo y cuándo
- Entender decisiones técnicas tomadas
- Identificar patrones de problemas
- Estimar mejor futuros proyectos
- Onboarding rápido de nuevos desarrolladores
- Auditoría de calidad del código

---

**Estas reglas se aplican automáticamente a todo el trabajo en el proyecto Omni Inspector - TFLite Detection**
