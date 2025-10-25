"""
Nodos de ejecución para el sistema autopoiético.

Implementa los nodos que ejecutan las tareas después del enrutamiento:
- EJECUCION_DIRECTA: Usa agentes existentes
- DIAGNOSTICO_ESTRUCTURAL: Inicia metaproducción (diseño de nuevos agentes)
"""

from typing import Optional, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

from orchestrator_state import OrchestratorState, AgentSpec
from agent_repository import AgentRepository


class DirectExecutionNode:
    """
    Nodo que ejecuta tareas usando agentes existentes del catálogo.
    
    Este nodo representa la operación normal del sistema cuando la tarea
    encaja con las capacidades actuales (sin necesidad de metaproducción).
    """
    
    def __init__(
        self,
        agent_repository: AgentRepository,
        model_name: str = "gpt-4",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        llm: Optional[Any] = None,
    ):
        self.agent_repository = agent_repository
        
        # Configurar LLM (inyectable)
        if llm is not None:
            self.llm = llm
        else:
            llm_kwargs = {
                "model": model_name,
                "temperature": 0.7,
            }
            if base_url:
                llm_kwargs["base_url"] = base_url
            if api_key:
                llm_kwargs["api_key"] = api_key
            self.llm = ChatOpenAI(**llm_kwargs)
    
    def execute(self, state: OrchestratorState) -> OrchestratorState:
        """
        Ejecuta la tarea usando un agente apropiado del catálogo.
        """
        # Obtener el último mensaje del usuario
        if not state.get("messages"):
            return state
        
        last_message = state["messages"][-1]
        user_task = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Seleccionar el agente más apropiado
        selected_agent = self._select_agent(user_task, state)
        
        if not selected_agent:
            # Si no hay agente apropiado, usar el general
            selected_agent = self.agent_repository.get_agent("general_assistant")
        
        # Ejecutar la tarea con el agente seleccionado
        response = self._execute_with_agent(user_task, selected_agent, state)
        
        # Actualizar el estado
        return {
            **state,
            "route": "END",
            "messages": state["messages"] + [
                {
                    "role": "assistant",
                    "content": f"[Agente: {selected_agent.agent_id}]\n\n{response}"
                }
            ]
        }
    
    def _select_agent(
        self, 
        task: str, 
        state: OrchestratorState
    ) -> Optional[AgentSpec]:
        """
        Selecciona el agente más apropiado para la tarea.
        
        En una implementación más sofisticada, esto podría usar
        embeddings o clasificación para matching semántico.
        """
        # Por ahora, usar lógica simple basada en keywords
        task_lower = task.lower()
        
        # Mapeo de keywords a agentes
        keyword_map = {
            "windsurf": "windsurf_planner",
            "weather": "windsurf_planner",
            "surf": "windsurf_planner",
            "code": "code_analyst",
            "bug": "code_analyst",
            "review": "code_analyst",
            "analyze": "code_analyst",
        }
        
        for keyword, agent_id in keyword_map.items():
            if keyword in task_lower:
                agent = self.agent_repository.get_agent(agent_id)
                if agent:
                    return agent
        
        # Default al asistente general
        return self.agent_repository.get_agent("general_assistant")
    
    def _execute_with_agent(
        self, 
        task: str, 
        agent: AgentSpec,
        state: OrchestratorState
    ) -> str:
        """
        Ejecuta la tarea usando el prompt de sistema del agente.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", agent.system_prompt),
            ("human", "{task}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"task": task})
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error al ejecutar tarea: {str(e)}"


class StructuralDiagnosisNode:
    """
    Nodo que inicia el proceso de metaproducción.
    
    Cuando una tarea requiere capacidades no disponibles, este nodo
    genera propuestas para crear o modificar agentes (metaproducción).
    """
    
    def __init__(
        self,
        agent_repository: AgentRepository,
        model_name: str = "gpt-4",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        llm: Optional[Any] = None,
    ):
        self.agent_repository = agent_repository
        
        # Configurar LLM (inyectable)
        if llm is not None:
            self.llm = llm
        else:
            llm_kwargs = {
                "model": model_name,
                "temperature": 0.3,  # Más bajo para diseño de agentes
            }
            if base_url:
                llm_kwargs["base_url"] = base_url
            if api_key:
                llm_kwargs["api_key"] = api_key
            self.llm = ChatOpenAI(**llm_kwargs)
        
        # LLM con salida estructurada para diseño de agentes (opcional)
        self.structured_llm = None
        if hasattr(self.llm, "with_structured_output"):
            try:
                self.structured_llm = self.llm.with_structured_output(AgentSpec)
            except Exception:
                self.structured_llm = None
    
    def diagnose(self, state: OrchestratorState) -> OrchestratorState:
        """
        Diagnostica la necesidad estructural y propone un nuevo agente.
        
        Este es el inicio del ciclo de metaproducción:
        1. Analizar la brecha de capacidades
        2. Diseñar una especificación de agente
        3. (En implementación completa: evaluar, ensayar, asimilar)
        """
        # Obtener la tarea del usuario
        if not state.get("messages"):
            return state
        
        last_message = state["messages"][-1]
        user_task = last_message.content if hasattr(last_message, 'content') else str(last_message)
        
        # Analizar brecha de capacidades
        gap_analysis = self._analyze_capability_gap(user_task, state)
        
        # Generar propuesta de nuevo agente
        agent_proposal = self._design_new_agent(user_task, gap_analysis)
        
        # En una implementación completa, aquí iríamos a:
        # - Ensayo en sandbox
        # - Evaluación A/B
        # - Asimilación al catálogo
        # Por ahora, solo reportamos la propuesta
        
        proposal_text = f"""## Diagnóstico Estructural

**Brecha de Capacidades Identificada:**
{gap_analysis}

**Propuesta de Nuevo Agente:**
- **ID**: {agent_proposal.get('agent_id', 'N/A')}
- **Rol**: {agent_proposal.get('role', 'N/A')}
- **Capacidades**: {', '.join(agent_proposal.get('capabilities', []))}
- **Herramientas**: {', '.join(agent_proposal.get('tools', []))}

**Siguiente Paso:**
Para implementar este agente, se requiere:
1. Ensayo en sandbox con dataset de prueba
2. Evaluación de métricas de viabilidad
3. Aprobación de MA-Asimilador
4. Despliegue versionado al catálogo

Por ahora, proporciono una respuesta provisional con el asistente general."""
        
        # Respuesta provisional usando agente general
        general_agent = self.agent_repository.get_agent("general_assistant")
        provisional_response = self._execute_provisional(user_task, general_agent)
        
        # Actualizar estado
        return {
            **state,
            "route": "END",
            "messages": state["messages"] + [
                {
                    "role": "assistant",
                    "content": f"{proposal_text}\n\n---\n\n**Respuesta Provisional:**\n{provisional_response}"
                }
            ]
        }
    
    def _analyze_capability_gap(
        self, 
        task: str, 
        state: OrchestratorState
    ) -> str:
        """
        Analiza la brecha entre capacidades requeridas y disponibles.
        """
        catalog = state.get("agent_catalog", [])
        
        prompt = f"""Analiza la siguiente tarea e identifica las capacidades requeridas que NO están disponibles en el catálogo actual.

**Tarea del Usuario:**
{task}

**Catálogo Actual:**
{self._format_catalog(catalog)}

Identifica:
1. Capacidades requeridas por la tarea
2. Capacidades faltantes en el catálogo
3. Justificación de por qué se necesita un nuevo agente"""
        
        try:
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"No se pudo analizar brecha de capacidades: {str(e)}"
    
    def _design_new_agent(self, task: str, gap_analysis: str) -> dict:
        """
        Diseña la especificación de un nuevo agente basado en la brecha identificada.
        """
        prompt = f"""Diseña un nuevo agente especializado basado en el análisis de brecha.

**Análisis de Brecha:**
{gap_analysis}

**Tarea Original:**
{task}

Proporciona una especificación de agente con:
- agent_id: Un ID único descriptivo (snake_case)
- role: Descripción del rol (2-5 palabras)
- capabilities: Lista de capacidades específicas
- tools: Lista de herramientas necesarias
- system_prompt: Prompt de sistema detallado para el agente"""
        
        try:
            # Intentar obtener salida estructurada
            # Nota: Dependiendo del modelo, esto puede requerir ajustes
            response = self.llm.invoke([{"role": "user", "content": prompt}])
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Parseo básico (en producción, usar structured output)
            return {
                "agent_id": "specialized_agent_" + str(hash(task))[:8],
                "role": "Agente especializado",
                "capabilities": ["capability_1", "capability_2"],
                "tools": ["tool_1", "tool_2"],
                "system_prompt": content[:500]  # Truncar para ejemplo
            }
        except Exception as e:
            return {
                "agent_id": "error_agent",
                "role": "Error en diseño",
                "capabilities": [],
                "tools": [],
                "system_prompt": f"Error: {str(e)}"
            }
    
    def _format_catalog(self, catalog: list[dict]) -> str:
        """Formatea el catálogo para el prompt."""
        if not catalog:
            return "Catálogo vacío"
        
        lines = []
        for agent in catalog:
            lines.append(
                f"- {agent['agent_id']}: {', '.join(agent['capabilities'])}"
            )
        return "\n".join(lines)
    
    def _execute_provisional(self, task: str, agent: Optional[AgentSpec]) -> str:
        """
        Ejecuta una respuesta provisional mientras se diseña el agente especializado.
        """
        if not agent:
            return "No hay agente disponible para respuesta provisional."
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", agent.system_prompt + "\n\nNOTA: Esta es una respuesta provisional mientras se diseña un agente especializado."),
            ("human", "{task}")
        ])
        
        try:
            response = (prompt | self.llm).invoke({"task": task})
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error en respuesta provisional: {str(e)}"
