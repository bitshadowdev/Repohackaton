from event_manager import EventManager
import datetime 

class Event:
    def __init__(self, event_type, event_name, event_description, requires_confirmation=False):
        self.event_time = datetime.datetime.now()
        # Registro de eventos
        self.event_manager_ref = EventManager()
        
        # tipo de evento, crear herramienta, crear agente, refinar prompt etc.
        self.event_type = event_type
        self.event_name = event_name 
        # Esta descripcion proviene de la IA
        self.event_description = event_description
        # Confirmación del usuario
        self.requires_confirmation = requires_confirmation
        self.event_manager_ref.register_event(self)
 