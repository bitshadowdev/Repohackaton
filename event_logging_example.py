import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from event import Event
from registro_de_eventos import EventRegister

def run_event_example():
    """
    Ejecuta un ejemplo de registro y visualización de eventos.
    """
    print("Creando eventos...")
    
    # Crear algunos eventos
    Event(
        event_type="Creación de Agente",
        event_name="Agente de Viajes",
        event_description="Se ha creado un nuevo agente para planificar viajes."
    )
    
    Event(
        event_type="Ejecución de Tarea",
        event_name="Búsqueda de Vuelos",
        event_description="El agente de viajes está buscando vuelos a París."
    )
    
    Event(
        event_type="Creación de Herramienta",
        event_name="API de Clima",
        event_description="Se ha añadido una nueva herramienta para consultar el clima."
    )
    
    print("Eventos creados.")
    print()
    
    # Crear un registro de eventos y mostrar los eventos
    event_register = EventRegister()
    event_register.display_events()

if __name__ == "__main__":
    run_event_example()
