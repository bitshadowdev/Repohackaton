"""
Meta-Agente Orquestador (Router/Supervisor).

Implementa el primer paso del sistema autopoiético: evaluar la tarea del usuario
y determinar si requiere metaproducción (DIAGNOSTICO_ESTRUCTURAL) o puede ser
manejada con agentes existentes (EJECUCION_DIRECTA).
"""

import os
import json
from typing import Optional, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

from orchestrator_state import (
    OrchestratorState, 
    RouterDecision, 
    RouteLabel,
    SystemInvariants
)
from agent_repository import AgentRepository


# Cargar variables de entorno
load_dotenv()


class MetaAgentRouter:
    """
    Meta-Agente Router que evalúa tareas y determina el flujo del sistema.
    
    Este agente tiene conocimiento del catálogo de agentes y las métricas
    de viabilidad, permitiéndole tomar decisiones informadas sobre si
    se requiere metaproducción o ejecución directa.
    """
    
    def __init__(
        self,
        agent_repository: AgentRepository,
        model_name: str = "gpt-4",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.0,
        llm: Optional[Any] = None,
    ):
        """
        Inicializa el Meta-Agente Router.
        
        Args:
            agent_repository: Repositorio de especificaciones de agentes
            model_name: Nombre del modelo LLM a usar
            base_url: URL base para API compatible con OpenAI (e.g., LM Studio)
            api_key: Clave API (o "sk-no-key" para endpoints locales)
            temperature: Temperatura para generación (0.0 para determinismo)
        """
        self.agent_repository = agent_repository
        
        # Configurar LLM (permitir inyección de instancia personalizada)
        if llm is not None:
            self.llm = llm
        else:
            llm_kwargs = {
                "model": model_name,
                "temperature": temperature,
            }
            if base_url:
                llm_kwargs["base_url"] = base_url
            if api_key:
                llm_kwargs["api_key"] = api_key
            self.llm = ChatOpenAI(**llm_kwargs)

        # Intentar structured output si el LLM lo soporta; si no, usaremos JSON manual
        self.structured_llm = None
        if hasattr(self.llm, "with_structured_output"):
            try:
                self.structured_llm = self.llm.with_structured_output(RouterDecision)
            except Exception:
                self.structured_llm = None
        
        # Prompt de sistema para el router
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """
        Crea el prompt de sistema para el Meta-Agente Router.
        """
        return """# PROMPT DEL SISTEMA (Meta-Agente Orquestador)

## ROL Y ORGANIZACIÓN DEL SISTEMA
Eres el Meta-Agente (MA) Orquestador Autopoiético. Tu función principal es garantizar la viabilidad del sistema mediante la circularidad productiva y la Metaproducción.

## OBJETIVO OPERACIONAL
Tu propósito es procesar el input del usuario y asegurar que la Organización (los invariantes) se conserve, incluso si la Estructura (los agentes especializados, prompts y herramientas) necesita modificarse o crearse.

## INVARIANTES
Estás obligado a hacer cumplir las leyes internas y los contratos del sistema:
- **Seguridad**: Cumplir las políticas de datos y no ejecutar código fuera del sandbox.
- **Trazabilidad**: Cualquier decisión o cambio debe ser registrable.
- **Estilo y Ontología**: Respetar los formatos definidos.

## PRINCIPIO DE DISEÑO
Tu arquitectura debe favorecer siempre la **composición de componentes** de LangChain y LangGraph sobre cualquier forma de herencia.

## CONTEXTO DE IMPLEMENTACIÓN (LANGGRAPH)
Estás operando dentro de un grafo de LangGraph y debes interactuar exclusivamente con el Estado tipado definido.

## TAREA: DIAGNÓSTICO INICIAL Y ENRUTAMIENTO

Ante el input del usuario, debes:

1. **Evaluar la complejidad y novedad** del requerimiento
2. **Comparar la tarea con el catálogo de AgentSpecs** existentes
3. **Determinar el enrutamiento apropiado**

### OPCIONES DE ENRUTAMIENTO:

- **DIAGNOSTICO_ESTRUCTURAL**: Si la tarea es nueva, compleja, o si los KPIs de viabilidad (K) sugieren que un agente existente está fallando y se requiere iniciar el ciclo de Metaproducción para crear/modificar un agente especializado.

- **EJECUCION_DIRECTA**: Si la tarea es simple o encaja perfectamente en el rol de un agente ya operativo.

### CRITERIOS DE EVALUACIÓN:

**Para DIAGNOSTICO_ESTRUCTURAL:**
- La tarea requiere capacidades no disponibles en el catálogo actual
- La tarea es altamente compleja (>0.7 en escala 0-1)
- Los agentes existentes han mostrado bajo rendimiento en tareas similares
- Se requiere crear un nuevo tipo de agente especializado

**Para EJECUCION_DIRECTA:**
- Existe al menos un agente con las capacidades necesarias
- La tarea es rutinaria o de complejidad baja-media (<0.7)
- No se requieren nuevas herramientas o capacidades

## FORMATO DE SALIDA

Devuelve una decisión estructurada con:
- `route`: La etiqueta de enrutamiento ("DIAGNOSTICO_ESTRUCTURAL" o "EJECUCION_DIRECTA")
- `reasoning`: Razonamiento claro y conciso de tu decisión
- `task_complexity`: Nivel de complejidad (0.0-1.0)
- `requires_new_agent`: Booleano indicando si se necesita un nuevo agente

## INFORMACIÓN DEL CATÁLOGO DE AGENTES

{agent_catalog}

## TAREA DEL USUARIO

{user_task}

Evalúa la tarea y proporciona tu decisión de enrutamiento."""
    
    def evaluate_task(self, state: OrchestratorState) -> OrchestratorState:
        """
        Nodo del grafo: Evalúa la tarea del usuario y determina el enrutamiento.
        
        Args:
            state: Estado actual del grafo
            
        Returns:
            Estado actualizado con la decisión de enrutamiento
        """
        # Obtener el último mensaje del usuario
        if not state.get("messages"):
            return {
                **state,
                "route": "END",
                "task_complexity": 0.0,
            }
        
        last_message = state["messages"][-1]
        user_task = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Obtener catálogo de agentes
        agent_catalog = self.agent_repository.get_catalog_summary()
        state["agent_catalog"] = agent_catalog
        
        # Formatear información del catálogo
        catalog_info = self._format_catalog_info(agent_catalog)
        
        # Crear el prompt con la tarea y el catálogo
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
        ])

        # Si tenemos structured_llm, úsalo
        if self.structured_llm is not None:
            try:
                decision: RouterDecision = self.structured_llm.invoke(
                    prompt.format_messages(agent_catalog=catalog_info, user_task=user_task)
                )
                return {
                    **state,
                    "route": decision.route,
                    "task_complexity": decision.task_complexity,
                    "messages": state["messages"] + [
                        {"role": "assistant", "content": f"[Router] {decision.reasoning}"}
                    ],
                }
            except Exception as e:
                print(f"Error en router (structured): {e}")

        # Fallback: análisis simple basado en keywords
        print(f"⚠️  Router usando fallback (structured output no disponible)")
        
        # Análisis simple de complejidad basado en la tarea
        task_lower = user_task.lower()
        
        # Determinar complejidad basada en keywords
        high_complexity_keywords = [
            "nuevo", "crear", "diseñar", "sistema", "arquitectura", 
            "complejo", "avanzado", "especializado", "iot", "ml", "ai"
        ]
        
        complexity = 0.3  # Base
        for keyword in high_complexity_keywords:
            if keyword in task_lower:
                complexity = min(complexity + 0.15, 0.9)
        
        # Verificar si hay agente apropiado
        has_suitable_agent = False
        for agent in agent_catalog:
            agent_caps = " ".join(agent.get("capabilities", [])).lower()
            if any(word in agent_caps for word in task_lower.split()[:5]):
                has_suitable_agent = True
                break
        
        # Decidir ruta
        if complexity > 0.7 and not has_suitable_agent:
            route = "DIAGNOSTICO_ESTRUCTURAL"
            reasoning = f"Tarea compleja (complexity={complexity:.2f}) sin agente especializado"
        else:
            route = "EJECUCION_DIRECTA"
            reasoning = f"Tarea manejable (complexity={complexity:.2f}) con agentes existentes"
        
        return {
            **state,
            "route": route,
            "task_complexity": complexity,
            "messages": state["messages"] + [
                {"role": "assistant", "content": f"[Router Fallback] {reasoning}"}
            ],
        }
    
    def _format_catalog_info(self, catalog: list[dict]) -> str:
        """
        Formatea la información del catálogo de agentes para el prompt.
        """
        if not catalog:
            return "**Catálogo vacío**: No hay agentes disponibles."
        
        lines = ["**Agentes Disponibles:**\n"]
        for agent in catalog:
            status = "✓" if agent["active"] else "✗"
            lines.append(
                f"{status} **{agent['agent_id']}** ({agent['role']})\n"
                f"   Capacidades: {', '.join(agent['capabilities'])}\n"
            )
        
        return "\n".join(lines)
    
    def get_route_condition(self, state: OrchestratorState) -> RouteLabel:
        """
        Función de condición para aristas condicionales en LangGraph.
        
        Args:
            state: Estado actual del grafo
            
        Returns:
            Etiqueta de ruta para el siguiente nodo
        """
        route = state.get("route", "EJECUCION_DIRECTA")
        
        # Validar que la ruta es válida
        if route not in ["DIAGNOSTICO_ESTRUCTURAL", "EJECUCION_DIRECTA", "END"]:
            return "EJECUCION_DIRECTA"
        
        return route
