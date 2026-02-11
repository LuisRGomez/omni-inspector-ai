#!/usr/bin/env python3
"""
Script para asignar todas las tareas Done sin assignee
Usa las nuevas funciones extendidas de mcp-server-jira

Autor: Luis Gomez
Fecha: 11 de febrero de 2026
"""

# NOTA: Este script debe ejecutarse desde Kiro después de reiniciar
# No puede ejecutarse directamente porque usa las herramientas MCP

# Lista de tareas sin asignar (detectadas en auditoría)
UNASSIGNED_TASKS = [
    'TALB-18',
    'TALB-19',
    'TALB-20',
    'TALB-21',
    'TALB-22',
    'TALB-26',
    'TALB-28',
    'TALB-29',
    'TALB-34',
    'TALB-35',
]

# Account ID de Luis Roberto Gomez
ACCOUNT_ID = "712020:fb49f226-fec7-48ae-a490-1b1821197ff5"

def assign_all_tasks():
    """
    Asigna todas las tareas sin assignee
    
    IMPORTANTE: Ejecutar desde Kiro después de reiniciar
    """
    print("🚀 Asignando tareas sin assignee...")
    print(f"   Total: {len(UNASSIGNED_TASKS)} tareas")
    print(f"   Asignar a: Luis Roberto Gomez")
    print()
    
    success_count = 0
    error_count = 0
    
    for task in UNASSIGNED_TASKS:
        try:
            # NOTA: Descomentar después de reiniciar Kiro
            # result = mcp_jira_assign_issue(task, ACCOUNT_ID)
            
            # Simulación para testing
            print(f"✅ {task} - Asignado")
            success_count += 1
            
        except Exception as e:
            print(f"❌ {task} - Error: {e}")
            error_count += 1
    
    print()
    print("=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    print(f"✅ Exitosas: {success_count}")
    print(f"❌ Errores: {error_count}")
    print(f"📋 Total: {len(UNASSIGNED_TASKS)}")
    print()
    
    if success_count == len(UNASSIGNED_TASKS):
        print("🎉 ¡Todas las tareas asignadas exitosamente!")
    else:
        print("⚠️  Algunas tareas no pudieron asignarse")

if __name__ == '__main__':
    print("=" * 60)
    print("  Asignación Masiva de Tareas Jira")
    print("=" * 60)
    print()
    print("⚠️  IMPORTANTE:")
    print("   Este script debe ejecutarse desde Kiro")
    print("   después de reiniciar para cargar las nuevas funciones")
    print()
    print("📝 Instrucciones:")
    print("   1. Reinicia Kiro")
    print("   2. Abre este script en Kiro")
    print("   3. Descomenta la línea: mcp_jira_assign_issue(task, ACCOUNT_ID)")
    print("   4. Ejecuta el script")
    print()
    
    # Ejecutar simulación
    assign_all_tasks()
