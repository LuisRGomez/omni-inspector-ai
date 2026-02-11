---
inclusion: auto
---

# Jira Workflow Automation - Proyecto TALB

## Configuración del Proyecto

**Proyecto:** TALB (Omni-Inspector AI)  
**Board:** https://hdisegurossa.atlassian.net/jira/software/projects/TALB/boards/3784  
**Responsable:** Kiro AI Agent

---

## Reglas de Trabajo

### 1. Al Empezar una Tarea, Bug o Epic

**🚨 CRÍTICO - WORKFLOW OBLIGATORIO:**

Cuando empieces a trabajar en CUALQUIER issue (Task, Bug, Epic):

```
1. ✅ Buscar el issue en Jira (mcp_jira_get_issue)
2. ✅ MOVER A "IN PROGRESS" (mcp_jira_transition_issue)
   - Obligatorio para que el PM vea progreso en tiempo real
   - NUNCA trabajar en issues que están en "To Do"
3. ✅ ASIGNAR a "Luis Roberto Gomez" (usar script assign_issues.py)
   - CRÍTICO: TODAS las tareas deben tener assignee
   - Verificar que la asignación fue exitosa
4. ✅ AGREGAR COMENTARIO DE INICIO (mcp_jira_add_comment):
   🚀 Iniciando trabajo en este issue
   
   **Plan:**
   - [ ] Paso 1
   - [ ] Paso 2
   - [ ] Paso 3
   
   **Tiempo estimado:** Xh
   
5. ✅ AGREGAR COMENTARIO TÉCNICO (mcp_jira_add_comment):
   🏗️ Análisis Técnico
   
   **Arquitectura:**
   - Módulo/componente a implementar
   - Dependencias necesarias
   - Patrones de diseño
   
   **Decisiones:**
   - Por qué esta tecnología/approach
   - Alternativas consideradas
   - Trade-offs
   
   **Impacto:**
   - Qué otros módulos afecta
   - Breaking changes (si hay)
   
6. ✅ AGREGAR WORKLOG (mcp_jira_add_worklog)
   - Tiempo estimado inicial
```

**🚨 REGLAS CRÍTICAS:**
- ❌ PROHIBIDO marcar Done sin asignar primero
- ❌ PROHIBIDO trabajar sin mover a "In Progress"
- ❌ PROHIBIDO omitir comentarios técnicos
- ✅ VERIFICAR que cada paso se completó exitosamente

**Script para asignar (OBLIGATORIO):**
```bash
# Ejecutar SIEMPRE antes de empezar
python assign_issues.py TALB-XX
```

### 2. Durante el Desarrollo

Mientras trabajas:

```
1. Agregar comentarios con progreso cada hora o hito importante
2. Si encuentras un problema:
   - Crear un Bug en Jira
   - Linkear al issue original
   - Documentar: síntomas, causa raíz, solución
3. Si necesitas investigación:
   - Agregar comentario con hallazgos
   - Actualizar descripción si es necesario
```

### 3. Al Completar una Tarea

**🚨 TESTING OBLIGATORIO - NO NEGOCIABLE:**

Antes de marcar como Done, EJECUTAR Y DOCUMENTAR:

```
1. ✅ TESTING REAL (OBLIGATORIO):
   
   Frontend (React Native):
   - [ ] Ejecutar: npm install
   - [ ] Ejecutar: getDiagnostics en archivos modificados
   - [ ] Verificar: 0 errores de TypeScript
   - [ ] Verificar: Código compila sin errores
   - [ ] Copiar logs de testing en comentario de Jira
   
   Backend (Python):
   - [ ] Ejecutar: python test_*.py
   - [ ] Verificar: 100% tests passing
   - [ ] Copiar output de tests en comentario de Jira
   - [ ] Verificar: No errores de sintaxis
   
   ❌ Si falla CUALQUIER test:
   - Crear bug en Jira
   - Linkear a la tarea
   - Arreglar el problema
   - Re-ejecutar tests
   - Documentar solución

2. ✅ VERIFICAR ASIGNACIÓN:
   - Confirmar que assignee = "Luis Roberto Gomez"
   - Si no está asignado: ejecutar assign_issues.py

3. ✅ AGREGAR COMENTARIO CON EVIDENCIAS (mcp_jira_add_comment):
   ✅ Tarea completada
   
   **Testing Ejecutado:**
   ```
   [PEGAR LOGS REALES AQUÍ]
   
   Ejemplo Frontend:
   $ npm install
   ✓ Dependencies installed successfully
   
   $ getDiagnostics
   ✓ 0 errors, 0 warnings
   
   Ejemplo Backend:
   $ python test_lambda_corrections.py
   Ran 12 tests in 0.234s
   OK - 100% pass rate
   ```
   
   **Entregables:**
   - Archivo X creado (líneas de código)
   - Funcionalidad Y implementada
   - Tests: X/X passing
   
   **Archivos modificados:**
   - path/to/file1.ts (+50 líneas)
   - path/to/file2.py (+120 líneas)
   
   **Tiempo real:** Xh Ym

4. ✅ AGREGAR WORKLOG FINAL (mcp_jira_add_worklog)
   - Tiempo real invertido

5. ✅ MOVER A "DONE" (mcp_jira_transition_issue)
   - Solo después de completar pasos 1-4
```

**🚨 REGLAS CRÍTICAS:**
- ❌ PROHIBIDO marcar Done sin ejecutar tests reales
- ❌ PROHIBIDO marcar Done sin pegar logs en Jira
- ❌ PROHIBIDO marcar Done sin verificar asignación
- ❌ PROHIBIDO omitir evidencias de testing
- ✅ Los logs deben ser REALES, no simulados
- ✅ Si no hay tests, crear tests básicos primero

### 4. Creación de Bugs

Cuando encuentres un bug:

```json
{
  "summary": "[BUG] Descripción corta del problema",
  "description": "
    ## Síntomas
    - Qué está fallando
    - Cómo se reproduce
    
    ## Causa Raíz
    - Por qué está pasando
    - Análisis técnico
    
    ## Solución Implementada
    - Qué se hizo para arreglarlo
    - Código relevante
    
    ## Testing
    - Cómo se verificó la solución
    
    ## Próximos Pasos
    - Acciones pendientes
    
    Archivo de análisis: [nombre-archivo].md
  ",
  "priority": "High/Medium/Low",
  "linked_to": "TALB-XX"
}
```

**IMPORTANTE:** 
1. ✅ Escribir análisis completo DENTRO de Jira (no solo en archivo)
2. ✅ Linkear el bug a la tarea relacionada usando API
3. ✅ Crear archivo .md adicional para referencia

---

## Formato de Comentarios

### Comentario de Inicio
```
🚀 Iniciando trabajo en esta tarea

**Plan:**
- [ ] Paso 1
- [ ] Paso 2
- [ ] Paso 3

**Tiempo estimado:** 2h
```

### Comentario de Progreso
```
📝 Progreso: 50%

**Completado:**
- ✅ Paso 1
- ✅ Paso 2

**En proceso:**
- 🔄 Paso 3

**Próximo:**
- Paso 4
```

### Comentario de Bug Encontrado
```
🐛 Bug encontrado: [descripción]

**Impacto:** Alto/Medio/Bajo
**Creado:** TALB-XX
**Estado:** Investigando/Solucionado

**Detalles:** [link al bug]
```

### Comentario Final
```
✅ Tarea completada

**Entregables:**
- Archivo X creado
- Funcionalidad Y implementada
- Tests pasando

**Evidencias:**
- 📸 Screenshot: [descripción]
- 🎥 Video: [link o descripción]
- 📊 Logs: [resultados]

**Tiempo real:** 2.5h

**Notas:**
- Consideración importante 1
- Consideración importante 2
```

---

## Workflow Automático

### Estados del Kanban
1. **To Do** - Tareas pendientes
2. **In Progress** - En desarrollo
3. **Code Review** - Esperando revisión (opcional)
4. **Testing** - En pruebas (opcional)
5. **Done** - Completado

### Transiciones Automáticas

```python
# Al empezar
transition_to_in_progress(issue_key)
assign_to_me(issue_key)
add_comment(issue_key, inicio_template)

# Durante desarrollo
add_comment(issue_key, progreso_template)
add_worklog(issue_key, "1h", "Desarrollo de funcionalidad X")

# Si hay bug
bug_key = create_bug(bug_data)
link_issues(issue_key, bug_key, "is blocked by")

# Al terminar
transition_to_done(issue_key)
add_comment(issue_key, final_template)
add_worklog(issue_key, "30m", "Testing y documentación")
```

---

## Prioridades

### Highest (Crítico)
- Bloquea otras tareas
- Funcionalidad core
- Bugs en producción

### High (Alto)
- Importante para el sprint
- Funcionalidad principal
- Bugs que afectan UX

### Medium (Medio)
- Mejoras
- Refactoring
- Bugs menores

### Low (Bajo)
- Nice to have
- Optimizaciones
- Documentación adicional

---

## Ejemplo de Flujo Completo

### Tarea: TALB-13 - Setup proyecto React Native + Expo

**1. Inicio (12:00 PM)**
```
🚀 Iniciando trabajo en esta tarea

**Plan:**
- [ ] Instalar Expo CLI
- [ ] Crear proyecto con TypeScript
- [ ] Configurar estructura de carpetas
- [ ] Instalar dependencias base
- [ ] Probar en simulador

**Tiempo estimado:** 1h
```

**2. Progreso (12:30 PM)**
```
📝 Progreso: 60%

**Completado:**
- ✅ Expo CLI instalado
- ✅ Proyecto creado
- ✅ Estructura de carpetas configurada

**En proceso:**
- 🔄 Instalando dependencias

**Próximo:**
- Probar en simulador
```

**3. Bug Encontrado (12:45 PM)**
```
🐛 Bug encontrado: Error al instalar react-native-svg

**Impacto:** Medio
**Creado:** TALB-38
**Estado:** Solucionado

**Solución:** Actualizar a versión compatible con Expo 50
```

**4. Completado (1:00 PM)**
```
✅ Tarea completada

**Entregables:**
- Proyecto mobile-app/ creado
- Estructura de carpetas configurada
- Dependencias instaladas
- App corriendo en simulador iOS

**Archivos creados:**
- mobile-app/package.json
- mobile-app/tsconfig.json
- mobile-app/App.tsx
- mobile-app/src/screens/HomeScreen.tsx

**Tiempo real:** 1h

**Notas:**
- Usar Expo SDK 50
- TypeScript configurado con strict mode
- Listo para empezar desarrollo
```

---

## Integración con Kiro

Cuando trabajes en una tarea, automáticamente:

1. Buscarás la tarea en Jira
2. Actualizarás el estado
3. Agregarás comentarios de progreso
4. Crearás bugs si es necesario
5. Documentarás todo el proceso
6. Marcarás como completado

Todo esto usando las herramientas de Jira MCP que ya están configuradas.

---

**Última actualización:** 11 de febrero de 2026  
**Estado:** Activo  
**Modo:** Automático


---

## Estrategia de Testing

### Tareas de Evidencia (Testing E2E)

Después de cada semana de desarrollo, crear tarea de testing:

**Estructura:**
```
Semana 1: TALB-13 a TALB-17 (desarrollo)
→ TALB-39: Testing E2E - Semana 1 (evidencias)

Semana 2: TALB-18 a TALB-22 (desarrollo)  
→ TALB-40: Testing E2E - Semana 2 (evidencias)
```

**En la tarea de testing:**
1. ✅ Compilar proyecto completo
2. ✅ Probar en emulador
3. ✅ Probar en dispositivo real (si es posible)
4. ✅ Tomar screenshots de cada funcionalidad
5. ✅ Grabar videos cortos
6. ✅ Si hay bugs:
   - Crear bug en Jira
   - Linkear a la tarea de testing
   - Arreglar el bug
   - Documentar solución
   - Volver a probar
7. ✅ Subir evidencias a Jira
8. ✅ Crear checklist en subtareas

**Checklist de Testing (Subtareas):**
- [ ] Compilación exitosa
- [ ] Prueba en emulador Android
- [ ] Prueba en dispositivo real
- [ ] Screenshots tomados
- [ ] Videos grabados
- [ ] Bugs encontrados y arreglados
- [ ] Evidencias subidas a Jira

**Formato de Evidencias:**
```
evidencias/
├── semana1/
│   ├── TALB-13-setup.png
│   ├── TALB-14-camera.png
│   ├── TALB-15-detection.mp4
│   └── TALB-16-boxes.mp4
└── semana2/
    └── ...
```


---

## Comentarios Técnicos y Arquitectura

### Al Empezar una Tarea

Agregar comentario técnico con:

```
🏗️ Análisis Técnico

**Arquitectura:**
- Módulo/componente a implementar
- Dependencias necesarias
- Patrones de diseño a usar

**Decisiones:**
- Por qué esta tecnología/approach
- Alternativas consideradas
- Trade-offs

**Impacto:**
- Qué otros módulos afecta
- Breaking changes (si hay)
- Performance considerations
```

### Durante el Desarrollo

Agregar comentarios sobre:
- Decisiones arquitectónicas importantes
- Problemas encontrados y cómo se resolvieron
- Refactorings necesarios
- Deuda técnica identificada

### Ejemplo Real (TALB-14)

```
🏗️ Análisis Técnico - Cámara

**Arquitectura:**
- Componente: CameraScreen.tsx
- Librería: react-native-vision-camera (mejor que Expo Camera)
- Patrón: Hooks (useCameraDevice, useCameraPermission)

**Decisiones:**
- Vision Camera vs Expo Camera
  ✅ Vision Camera: Mejor performance, más features
  ❌ Expo Camera: Requiere Expo (no usamos)
  
- Permisos: Solicitud automática en useEffect
- Overlay: Absolute positioning para controles

**Impacto:**
- Dependencias: +5 paquetes (navigation, vision-camera)
- AndroidManifest.xml: Permisos agregados
- App.tsx: Navegación refactorizada
- Performance: Excelente (60fps en preview)

**Próximo:**
- TALB-15: Integrar con YOLO (backend o local)
- Considerar: TensorFlow Lite para detección on-device
```

---

## Testing Obligatorio

### CRÍTICO: Toda tarea debe compilar y ejecutar

Antes de marcar como Done:

1. ✅ `npm install` sin errores
2. ✅ Compilación exitosa
3. ✅ App se abre sin crashear
4. ✅ Funcionalidad básica probada

**Si no compila o crashea:**
- ❌ NO marcar como Done
- 🐛 Crear bug
- 🔧 Arreglar
- ✅ Re-probar

### Mínimo Testing por Tarea

```
**Testing Básico:**
- [x] Compila sin errores
- [x] No crashea al abrir
- [x] Funcionalidad principal funciona
- [ ] Testing completo en tarea E2E
```
