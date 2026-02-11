---
inclusion: auto
---

# Checklist de Verificación Jira - OBLIGATORIO

**Propósito:** Asegurar que TODAS las tareas cumplan con el workflow antes de marcar Done

---

## 🚨 CHECKLIST OBLIGATORIO - Antes de Marcar Done

### 1. Asignación ✅
```
[ ] Issue tiene assignee = "Luis Roberto Gomez"
[ ] Verificado con: mcp_jira_get_issue
[ ] Si falta: ejecutar assign_issues.py
```

### 2. Estado ✅
```
[ ] Issue movido a "In Progress" al empezar
[ ] Issue movido a "Done" solo después de testing
[ ] Transiciones documentadas en comentarios
```

### 3. Comentarios Técnicos ✅
```
[ ] Comentario de inicio con plan
[ ] Comentario técnico con arquitectura
[ ] Comentarios de progreso (si aplica)
[ ] Comentario final con evidencias
```

### 4. Testing Real ✅
```
Frontend:
[ ] npm install ejecutado
[ ] getDiagnostics ejecutado (0 errores)
[ ] Logs pegados en comentario de Jira

Backend:
[ ] Tests unitarios ejecutados
[ ] 100% tests passing
[ ] Output pegado en comentario de Jira

General:
[ ] Funcionalidad básica probada
[ ] Bugs encontrados documentados
```

### 5. Evidencias ✅
```
[ ] Logs de testing en comentario
[ ] Archivos creados/modificados listados
[ ] Líneas de código agregadas
[ ] Screenshots (si es UI)
[ ] Resultados de compilación
```

### 6. Worklog ✅
```
[ ] Worklog agregado con tiempo real
[ ] Tiempo estimado vs real documentado
```

---

## 🔍 Verificación Post-Completion

Después de marcar Done, VERIFICAR:

```bash
# 1. Verificar asignación
mcp_jira_get_issue(TALB-XX)
# Confirmar: assignee != null

# 2. Verificar comentarios
# Revisar que existan:
# - Comentario de inicio
# - Comentario técnico
# - Comentario final con logs

# 3. Verificar worklog
# Confirmar que hay tiempo registrado
```

---

## ❌ Errores Comunes a Evitar

### Error 1: Marcar Done sin asignar
```
❌ MAL:
- Completar tarea
- Mover a Done
- assignee = null

✅ BIEN:
- Asignar a Luis Roberto Gomez
- Completar tarea
- Verificar asignación
- Mover a Done
```

### Error 2: Testing simulado
```
❌ MAL:
"Testing completado" (sin logs)

✅ BIEN:
**Testing Ejecutado:**
```
$ npm install
✓ Dependencies installed

$ getDiagnostics
✓ 0 errors
```
```

### Error 3: Comentarios genéricos
```
❌ MAL:
"Tarea completada"

✅ BIEN:
✅ Tarea completada

**Testing:**
[logs reales]

**Entregables:**
- AnalysisScreen.tsx (+250 líneas)
- MetricCard.tsx (+80 líneas)

**Tiempo:** 2h 30m
```

---

## 🎯 Estándar de Calidad

Toda tarea Done debe tener:

1. ✅ Assignee correcto
2. ✅ Comentarios completos (inicio, técnico, final)
3. ✅ Logs reales de testing
4. ✅ Evidencias concretas
5. ✅ Worklog con tiempo real
6. ✅ Archivos listados con líneas de código

**Si falta CUALQUIERA de estos elementos:**
- ❌ La tarea NO está completa
- 🔄 Volver a "In Progress"
- ✅ Completar elementos faltantes
- ✅ Re-verificar checklist

---

## 📊 Métricas de Calidad

### Por Tarea
- Comentarios: mínimo 3 (inicio, técnico, final)
- Evidencias: logs reales obligatorios
- Worklog: tiempo real registrado
- Asignación: 100% de tareas asignadas

### Por Sprint/Semana
- % tareas con testing real: 100%
- % tareas con evidencias: 100%
- % tareas asignadas: 100%
- Bugs encontrados y resueltos: documentados

---

## 🚀 Proceso de Mejora Continua

### Después de cada grupo de tareas:
1. Revisar checklist de todas las tareas Done
2. Identificar tareas que no cumplen estándar
3. Corregir deficiencias
4. Actualizar workflow si es necesario

### Auditoría semanal:
```bash
# Verificar todas las tareas Done de la semana
mcp_jira_search_issues("status = Done AND updated >= -7d")

# Para cada tarea:
# - Verificar assignee
# - Verificar comentarios
# - Verificar evidencias
```

---

**Última actualización:** 11 de febrero de 2026  
**Estado:** Activo  
**Modo:** Obligatorio para TODAS las tareas

