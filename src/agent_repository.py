"""
Repositorio Organizacional de Agentes.

Gestiona el catálogo de AgentSpecs, proporcionando acceso a las
especificaciones de agentes disponibles y permitiendo la metaproducción
(creación y modificación de agentes).
"""

from typing import Optional
from orchestrator_state import AgentSpec


class AgentRepository:
    """
    Repositorio que mantiene el catálogo de agentes del sistema.
    
    Este es el componente que almacena la 'estructura' (agentes concretos)
    mientras se mantiene la 'organización' (invariantes y roles).
    """
    
    def __init__(self):
        self._catalog: dict[str, AgentSpec] = {}
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """
        Inicializa el catálogo con agentes predeterminados.
        """
        # Agente general de propósito
        self.add_agent(AgentSpec(
            agent_id="general_assistant",
            role="Asistente general",
            capabilities=["conversation", "information_retrieval", "task_planning"],
            tools=["web_search", "calculator"],
            system_prompt="""Eres un asistente general integrado en un sistema autopoiético.
Tu función es manejar tareas rutinarias de conversación e información.
Usa herramientas cuando sea necesario y mantén respuestas concisas.""",
            version="1.0.0",
            active=True
        ))
        
        # Agente especializado en análisis de código
        self.add_agent(AgentSpec(
            agent_id="code_analyst",
            role="Analista de código",
            capabilities=["code_review", "bug_detection", "optimization_suggestions"],
            tools=["code_search", "syntax_checker", "complexity_analyzer"],
            system_prompt="""Eres un especialista en análisis de código.
Revisa código, detecta bugs, y sugiere optimizaciones.
Cita líneas específicas y proporciona ejemplos concretos.""",
            version="1.0.0",
            active=True
        ))
        
        # Agente especializado en windsurf (ejemplo del caso de uso)
        self.add_agent(AgentSpec(
            agent_id="windsurf_planner",
            role="Planificador de windsurf",
            capabilities=["weather_analysis", "location_recommendation", "equipment_advice"],
            tools=["weather_api", "location_db", "equipment_catalog"],
            system_prompt="""Eres un especialista en planificación de viajes de windsurf.
Analizas condiciones meteorológicas, recomiendas locaciones y asesoras sobre equipo.
Proporciona información basada en datos meteorológicos actuales.""",
            version="1.0.0",
            active=True
        ))
    
    def add_agent(self, spec: AgentSpec) -> None:
        """
        Añade una especificación de agente al catálogo.
        """
        self._catalog[spec.agent_id] = spec
    
    def get_agent(self, agent_id: str) -> Optional[AgentSpec]:
        """
        Obtiene la especificación de un agente por ID.
        """
        return self._catalog.get(agent_id)
    
    def get_all_agents(self) -> list[AgentSpec]:
        """
        Obtiene todas las especificaciones de agentes activos.
        """
        return [spec for spec in self._catalog.values() if spec.active]
    
    def find_agent_by_capability(self, capability: str) -> list[AgentSpec]:
        """
        Busca agentes que tengan una capacidad específica.
        """
        return [
            spec for spec in self._catalog.values()
            if capability in spec.capabilities and spec.active
        ]
    
    def update_agent(self, agent_id: str, updates: dict) -> bool:
        """
        Actualiza una especificación de agente existente.
        
        Esto forma parte del proceso de metaproducción: modificar
        la estructura mientras se conserva la organización.
        """
        if agent_id not in self._catalog:
            return False
        
        spec = self._catalog[agent_id]
        for key, value in updates.items():
            if hasattr(spec, key):
                setattr(spec, key, value)
        
        return True
    
    def deactivate_agent(self, agent_id: str) -> bool:
        """
        Desactiva un agente (sin eliminarlo del catálogo).
        """
        if agent_id in self._catalog:
            self._catalog[agent_id].active = False
            return True
        return False
    
    def get_catalog_summary(self) -> list[dict]:
        """
        Obtiene un resumen del catálogo para el estado del grafo.
        """
        return [
            {
                "agent_id": spec.agent_id,
                "role": spec.role,
                "capabilities": spec.capabilities,
                "active": spec.active,
            }
            for spec in self._catalog.values()
        ]
