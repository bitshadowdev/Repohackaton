"""
Sistema Autopoiético de Agentes de IA

Paquete principal que implementa un sistema de orquestación de agentes
basado en principios autopoiéticos usando LangChain y LangGraph.
"""

__version__ = "1.0.0"
__author__ = "Hackathon Team"

from .autopoietic_orchestrator import AutopoieticOrchestrator, create_orchestrator
from .orchestrator_state import (
    OrchestratorState,
    AgentSpec,
    RouterDecision,
    ViabilityMetrics,
    SystemInvariants,
)
from .agent_repository import AgentRepository
from .meta_agent_router import MetaAgentRouter

__all__ = [
    "AutopoieticOrchestrator",
    "create_orchestrator",
    "OrchestratorState",
    "AgentSpec",
    "RouterDecision",
    "ViabilityMetrics",
    "SystemInvariants",
    "AgentRepository",
    "MetaAgentRouter",
]
