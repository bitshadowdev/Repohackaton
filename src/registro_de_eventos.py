class EventRegister:
    """Es el registro de eventos 
    aqui el event manager va a almacenar los eventos"""
    def __init__(self):
        self.events = []
        # Resumen de los eventos que han trans currido en el sistema desde 
        # el nacimiento del primer agente. 
        self.summary = ""

