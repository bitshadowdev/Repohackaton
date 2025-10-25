from event_manager import EventManager

class EventRegister:
    """Es el registro de eventos 
    aqui el event manager va a almacenar los eventos"""
    def __init__(self):
        self.event_manager = EventManager()
        self.events = self.event_manager.events
        
    def display_events(self):
        print("--- REGISTRO DE EVENTOS ---")
        if not self.events:
            print("No hay eventos registrados.")
            return
        
        for event_time, event in sorted(self.events.items()):
            print(f"[{event_time}] - {event.event_type}: {event.event_name}")
            print(f"  Descripción: {event.event_description}")
            print("-" * 30)



