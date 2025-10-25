"""
Implementación del patrón de diseño Command.

Este módulo define una estructura para encapsular todas las solicitudes de acción
como objetos de comando desacoplados. Cada comando contiene la lógica para su
propia ejecución y la información necesaria para una solicitud de permiso.
"""

from abc import ABC, abstractmethod
import os
import subprocess
from dataclasses import dataclass
from permissions.permissions_manager import Action, PermissionRequest


@dataclass
class CommandResult:
    """Representa el resultado de la ejecución de un comando."""
    success: bool
    message: str
    output: str = ""


class Command(ABC):
    """Clase base abstracta para todos los objetos de comando."""
    
    @property
    @abstractmethod
    def permission_request(self) -> PermissionRequest:
        """Devuelve la solicitud de permiso asociada con este comando."""
        pass

    @abstractmethod
    def execute(self) -> CommandResult:
        """Ejecuta la lógica del comando."""
        pass


class WriteFileCommand(Command):
    """
    Comando para escribir contenido en un archivo.
    La ejecución de este comando escribe un archivo real en el sistema.
    """
    def __init__(self, agent_id: str, file_path: str, content: str):
        self.agent_id = agent_id
        self.file_path = file_path
        self.content = content
        self._permission_request = PermissionRequest(
            agent_id=self.agent_id,
            action=Action.WRITE_FILE,
            resource=self.file_path,
            context={"content_length": len(self.content)}
        )

    @property
    def permission_request(self) -> PermissionRequest:
        return self._permission_request

    def execute(self) -> CommandResult:
        try:
            # Crear directorios si no existen
            dir_name = os.path.dirname(self.file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(self.content)
            
            message = f"Archivo escrito exitosamente en {self.file_path}"
            print(f"-> {message}")
            return CommandResult(success=True, message=message)
        except IOError as e:
            message = f"Error de E/S al escribir el archivo: {e}"
            print(f"-> {message}")
            return CommandResult(success=False, message=message)
        except Exception as e:
            message = f"Un error inesperado ocurrió: {e}"
            print(f"-> {message}")
            return CommandResult(success=False, message=message)


class ShellCommand(Command):
    """
    Comando para ejecutar un proceso de shell.
    
    ADVERTENCIA: La ejecución de comandos de shell es inherentemente peligrosa.
    Este es un ejemplo y debería ser usado con extrema precaución.
    """
    def __init__(self, agent_id: str, command: str):
        self.agent_id = agent_id
        self.command = command
        self._permission_request = PermissionRequest(
            agent_id=self.agent_id,
            action=Action.EXECUTE_COMMAND,
            resource=self.command
        )

    @property
    def permission_request(self) -> PermissionRequest:
        return self._permission_request

    def execute(self) -> CommandResult:
        try:
            print(f"-> Ejecutando comando de shell: {self.command}")
            # Usar shell=False y pasar argumentos como lista es más seguro
            # pero para un ejemplo simple, shell=True es más directo.
            # En un sistema real, esto necesitaría un sandboxing robusto.
            result = subprocess.run(
                self.command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=True, 
                timeout=30
            )
            message = "Comando ejecutado exitosamente."
            print(f"-> Salida: {result.stdout}")
            return CommandResult(success=True, message=message, output=result.stdout)
        except subprocess.CalledProcessError as e:
            message = f"Error al ejecutar el comando: {e.stderr}"
            print(f"-> {message}")
            return CommandResult(success=False, message=message, output=e.stderr)
        except subprocess.TimeoutExpired:
            message = "El comando excedió el tiempo límite de ejecución."
            print(f"-> {message}")
            return CommandResult(success=False, message=message)
        except Exception as e:
            message = f"Un error inesperado ocurrió: {e}"
            print(f"-> {message}")
            return CommandResult(success=False, message=message)
