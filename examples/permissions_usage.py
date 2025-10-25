"""
Ejemplo de uso del Sistema de Permisos.

Este archivo muestra cómo el sistema de permisos puede ser utilizado para
restringir o permitir acciones específicas de los agentes.
"""

import os
from dotenv import load_dotenv

# Los siguientes imports funcionan gracias a `uv pip install -e .`
import os
from dotenv import load_dotenv
import time

# Los siguientes imports funcionan gracias a `uv pip install -e .`
from autopoietic_orchestrator import create_orchestrator
from permissions.permissions_manager import Action, InteractivePermissionsManager
from commands import WriteFileCommand, ShellCommand


load_dotenv()


def ejemplo_patron_comando_interactivo():
    """
    Ejemplo que demuestra el patrón Command con aprobación interactiva del usuario.
    """
    print("\n" + "="*80)
    print("EJEMPLO: Patrón Command con Permiso Interactivo")
    print("="*80)

    # 1. Crear una instancia del gestor de permisos INTERACTIVO
    permissions = InteractivePermissionsManager()

    # 2. Inyectar el gestor en el orquestador
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
        permissions_manager=permissions
    )

    print("\nSe simularán solicitudes de ejecución de comandos que requerirán tu aprobación.")

    # --- Comando 1: Escribir un archivo (acción real) ---
    file_path = os.path.join(os.getcwd(), "test_file.txt")
    write_command = WriteFileCommand(
        agent_id="file_writer_agent",
        file_path=file_path,
        content=f"Este archivo fue escrito por un agente a las {time.ctime()}\n"
    )

    print("\n--- Solicitud 1: Comando de Escritura de Archivo ---")
    result = orchestrator.permissions_manager.request_permission_and_execute(write_command)

    if result.success:
        print(f"\n✅ {result.message}")
        # Verificar que el archivo existe
        if os.path.exists(file_path):
            print(f"   VERIFICACIÓN: El archivo '{file_path}' ha sido creado exitosamente.")
            # Limpieza
            #os.remove(file_path)
            #print(f"   LIMPIEZA: El archivo de prueba ha sido eliminado.")
        else:
            print(f"   VERIFICACIÓN FALLIDA: El archivo no fue encontrado.")
    else:
        print(f"\n❌ {result.message}")

    # --- Comando 2: Ejecutar un comando de shell ---
    shell_command = ShellCommand(
        agent_id="system_info_agent",
        command="echo 'Hola desde un comando de shell'"
    )

    print("\n--- Solicitud 2: Comando de Ejecución de Shell ---")
    result = orchestrator.permissions_manager.request_permission_and_execute(shell_command)

    if result.success:
        print(f"\n✅ {result.message}")
        print(f"   SALIDA DEL COMANDO:\n---\n{result.output.strip()}\n---")
    else:
        print(f"\n❌ {result.message}")


def ejemplo_listado_de_acciones():
    """
    Muestra todas las acciones que pueden ser permisionadas.
    """
    print("\n" + "="*80)
    print("EJEMPLO: Acciones Disponibles para Permisos")
    print("="*80)

    print("\n📋 Acciones que el sistema de permisos puede gestionar:")
    print("-" * 80)
    for action in Action:
        print(f"  • {action.name:20} → {action.value}")


if __name__ == "__main__":
    print("\n" + "🛡️ "*40)
    print("EJEMPLO - PATRÓN COMMAND CON PERMISOS INTERACTIVOS")
    print("🛡️ "*40)

    ejemplo_patron_comando_interactivo()
    ejemplo_listado_de_acciones()

    print("\n" + "✅"*40)
    print("FIN DE EJEMPLOS")
    print("✅"*40 + "\n")
