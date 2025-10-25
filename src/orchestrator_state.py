"""
Estado tipado para el Meta-Agente Orquestador Autopoiético.

Define el esquema de estado que fluye a través del grafo de LangGraph,
respetando los principios de organización vs. estructura y los invariantes
del sistema autopoiético.
"""

from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field


# ============================================================================
# TIPOS DE ENRUTAMIENTO
# ============================================================================

RouteLabel = Literal[
    "DIAGNOSTICO_ESTRUCTURAL",  # Requiere metaproducción (crear/modificar agentes)
    "EJECUCION_DIRECTA",        # Tarea rutinaria con agentes existentes
    "END"                       # Finalizar
]


# ============================================================================
# ESQUEMA DE ESTADO DEL GRAFO
# ============================================================================

class OrchestratorState(TypedDict):
    """
    Estado principal del grafo de orquestación.
    
    Claves del estado:
    - messages: Historial de mensajes (acumulador con add_messages)
    - route: Etiqueta de enrutamiento para flujo condicional
    - task_complexity: Nivel de complejidad evaluado (0.0-1.0)
    - viability_kpis: Métricas de viabilidad del sistema
    - context: Contexto adicional (RAG, catálogo de agentes, etc.)
    - agent_catalog: Catálogo de especificaciones de agentes disponibles
    """
    messages: Annotated[list[AnyMessage], add_messages]
    route: Optional[RouteLabel]
    task_complexity: Optional[float]
    viability_kpis: Optional[dict]
    context: Optional[str]
    agent_catalog: Optional[list[dict]]


# ============================================================================
# MODELOS PYDANTIC PARA SALIDAS ESTRUCTURADAS
# ============================================================================

class RouterDecision(BaseModel):
    """
    Decisión estructurada del router.
    """
    route: RouteLabel = Field(
        description="Etiqueta de enrutamiento basada en la evaluación de la tarea"
    )
    reasoning: str = Field(
        description="Razonamiento breve de la decisión de enrutamiento"
    )
    task_complexity: float = Field(
        ge=0.0, 
        le=1.0,
        description="Nivel de complejidad de la tarea (0=simple, 1=compleja)"
    )
    requires_new_agent: bool = Field(
        description="Si la tarea requiere crear un nuevo agente especializado"
    )


class AgentSpec(BaseModel):
    """
    Especificación de un agente del sistema.
    
    Representa la 'estructura' que puede cambiar mientras se
    mantiene la 'organización' (invariantes).
    """
    agent_id: str = Field(description="Identificador único del agente")
    role: str = Field(description="Rol o especialización del agente")
    capabilities: list[str] = Field(description="Capacidades del agente")
    tools: list[str] = Field(description="Herramientas disponibles")
    system_prompt: str = Field(description="Prompt de sistema del agente")
    version: str = Field(default="1.0.0", description="Versión del agente")
    active: bool = Field(default=True, description="Si el agente está activo")


class ViabilityMetrics(BaseModel):
    """
    Métricas de viabilidad del sistema (núcleo K).
    
    Define el espacio de KPIs donde la organización se conserva.
    """
    accuracy: float = Field(ge=0.0, le=1.0, description="Precisión del sistema")
    latency_ms: float = Field(ge=0.0, description="Latencia en milisegundos")
    cost_per_request: float = Field(ge=0.0, description="Costo por petición")
    error_rate: float = Field(ge=0.0, le=1.0, description="Tasa de error")
    within_viability: bool = Field(
        description="Si las métricas están dentro del núcleo de viabilidad"
    )


# ============================================================================
# INVARIANTES DEL SISTEMA
# ============================================================================

class SystemInvariants:
    """
    Invariantes organizacionales del sistema autopoiético.
    
    Estas reglas NO DEBEN ser violadas; definen la identidad del sistema.
    """
    
    # Seguridad
    SECURITY_POLICIES = {
        "no_code_execution_outside_sandbox": True,
        "no_secret_exfiltration": True,
        "data_privacy_compliance": True,
    }
    
    # Presupuestos
    BUDGETS = {
        "max_tokens_per_request": 8000,
        "max_latency_ms": 5000,
        "max_cost_per_request": 0.10,
    }
    
    # Calidad mínima
    QUALITY_THRESHOLDS = {
        "min_accuracy": 0.85,
        "max_hallucination_rate": 0.05,
        "min_coverage": 0.90,
    }
    
    # Trazabilidad
    TRACEABILITY = {
        "log_all_decisions": True,
        "version_control_changes": True,
        "enable_rollback": True,
    }
    
    @classmethod
    def validate_invariants(cls, metrics: ViabilityMetrics) -> bool:
        """
        Valida que las métricas cumplan con los invariantes.
        """
        checks = [
            metrics.accuracy >= cls.QUALITY_THRESHOLDS["min_accuracy"],
            metrics.latency_ms <= cls.BUDGETS["max_latency_ms"],
            metrics.cost_per_request <= cls.BUDGETS["max_cost_per_request"],
            metrics.error_rate <= cls.QUALITY_THRESHOLDS["max_hallucination_rate"],
        ]
        return all(checks)
