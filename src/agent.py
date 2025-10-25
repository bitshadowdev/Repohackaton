"""Es la clase base del agente"""
from abc import ABC, abstractmethod

class Agent(ABC):
    """Es es un contrato general que tienen que 
    seguir todos los agentes"""
    @abstractmethod
    def update_system_promt(self):
        pass



class Agent:
    def __init__(self):
        pass