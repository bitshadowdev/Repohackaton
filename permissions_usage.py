"""
Ejemplo de uso del Sistema de Permisos.

Este archivo muestra cómo el sistema de permisos puede ser utilizado para
restringir o permitir acciones específicas de los agentes.
"""

import sys
from pathlib import Path
import os

# Añadir src al path

from src.autopoietic_orchestrator import create_orchestrator
from src.permissions.permissions_manager import Action, PermissionRequest
from dotenv import load_dotenv

load_dotenv()


def ejemplo_permiso_concedido():
    """
    Ejemplo 1: Una tarea que requiere un permiso que es concedido.
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Permiso Concedido")
    print("="*80)

    # Crear orquestador con un manejador de permisos simple
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    tarea = "Escribe un archivo de prueba en /tmp/test.txt"
    print(f"\n📝 Tarea: {tarea}")

    # Simular una solicitud de permiso
    request = PermissionRequest(
        agent_id="test_agent",
        action=Action.WRITE_FILE,
        resource="/tmp/test.txt",
        context={"data": "Hello, world!"}
    )

    # El manejador de permisos por defecto concede esta acción
    if orchestrator.permissions_manager.request_permission(request):
        print(f"\n✅ Permiso CONCEDIDO para {request.action.value} en {request.resource}")
        # Aquí iría la lógica para ejecutar la acción
    else:
        print(f"\n❌ Permiso DENEGADO para {request.action.value} en {request.resource}")


def ejemplo_permiso_denegado():
    """
    Ejemplo 2: Una tarea que requiere un permiso que es denegado.
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Permiso Denegado")
    print("="*80)

    # Crear orquestador
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    tarea = "Eliminar un archivo importante del sistema"
    print(f"\n📝 Tarea: {tarea}")

    # Simular una solicitud de permiso para una acción peligrosa
    request = PermissionRequest(
        agent_id="rogue_agent",
        action=Action.DELETE_FILE,
        resource="/etc/important_config",
        context={"reason": "Accidental request"}
    )

    # El manejador de permisos por defecto deniega esta acción
    if orchestrator.permissions_manager.request_permission(request):
        print(f"\n✅ Permiso CONCEDIDO para {request.action.value} en {request.resource}")
    else:
        print(f"\n❌ Permiso DENEGADO para {request.action.value} en {request.resource}")
        print("   Razón: La política de seguridad prohíbe la eliminación de archivos críticos.")


def ejemplo_listado_de_acciones():
    """
    Muestra todas las acciones que pueden ser permisionadas.
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Acciones Disponibles para Permisos")
    print("="*80)

    print("\n📋 Acciones que el sistema de permisos puede gestionar:")
    print("-" * 80)
    for action in Action:
        print(f"  • {action.name:20} → {action.value}")


if __name__ == "__main__":
    print("\n" + "🛡️ "*40)
    print("EJEMPLOS DE USO - SISTEMA DE PERMISOS")
    print("🛡️ "*40)

    ejemplo_permiso_concedido()
    ejemplo_permiso_denegado()
    ejemplo_listado_de_acciones()

    print("\n" + "✅"*40)
    print("FIN DE EJEMPLOS")
    print("✅"*40 + "\n")
