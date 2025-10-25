"""Es la clase base del agente"""
from abc import ABC, abstractmethod
from event import Event

class AbstractAgent(ABC):
    """Es es un contrato general que tienen que 
    seguir todos los agentes"""
    @abstractmethod
    def update_system_promt(self):
        pass

    # Get response 
    @abstractmethod
    def get_response(self) -> Event:
        pass

    

class BaseAgent(AbstractAgent):
    def __init__(self):
        self.nombre = "Default Agent"
        