"""
Ejemplo de uso del Sistema de Permisos.

Este archivo muestra cómo el sistema de permisos puede ser utilizado para
restringir o permitir acciones específicas de los agentes.
"""

import os
from dotenv import load_dotenv

# Los siguientes imports funcionan gracias a `uv pip install -e .`
from autopoietic_orchestrator import create_orchestrator
from permissions.permissions_manager import Action, PermissionRequest, InteractivePermissionsManager


load_dotenv()


def ejemplo_permiso_interactivo():
    """
    Ejemplo 1: Una tarea que requiere un permiso que será decidido por el usuario.
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Permiso Interactivo")
    print("="*80)

    # 1. Crear una instancia del gestor de permisos INTERACTIVO
    permissions = InteractivePermissionsManager()

    # 2. Inyectar el gestor en el orquestador
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
        permissions_manager=permissions
    )

    print("\nAhora se simularán dos solicitudes de permiso que requerirán tu aprobación.")

    # --- Solicitud 1: Escribir un archivo (acción importante) ---
    request_write = PermissionRequest(
        agent_id="file_writer_agent",
        action=Action.WRITE_FILE,
        resource="/tmp/report.txt",
        context={"data_size": "1024 bytes"}
    )

    print("\n--- Solicitud 1: Escritura de archivo ---")
    if orchestrator.permissions_manager.request_permission(request_write):
        print("\n✅ El usuario CONCEDIÓ el permiso para escribir el archivo.")
    else:
        print("\n❌ El usuario DENEGÓ el permiso para escribir el archivo.")

    # --- Solicitud 2: Eliminar un archivo (acción importante) ---
    request_delete = PermissionRequest(
        agent_id="cleanup_agent",
        action=Action.DELETE_FILE,
        resource="/tmp/old_data.csv",
        context={"reason": "Deleting obsolete data"}
    )

    print("\n--- Solicitud 2: Eliminación de archivo ---")
    if orchestrator.permissions_manager.request_permission(request_delete):
        print("\n✅ El usuario CONCEDIÓ el permiso para eliminar el archivo.")
    else:
        print("\n❌ El usuario DENEGÓ el permiso para eliminar el archivo.")


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
    print("EJEMPLOS DE USO - SISTEMA DE PERMISOS INTERACTIVO")
    print("🛡️ "*40)

    ejemplo_permiso_interactivo()
    ejemplo_listado_de_acciones()

    print("\n" + "✅"*40)
    print("FIN DE EJEMPLOS")
    print("✅"*40 + "\n")
