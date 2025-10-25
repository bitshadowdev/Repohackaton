"""
Orquestador Autopoiético basado en LangGraph.

Implementa el grafo completo que conecta:
1. Meta-Agente Router (evaluación y enrutamiento)
2. Nodos de ejecución (directa o diagnóstico estructural)
3. Sistema de persistencia y checkpointing

Este es el núcleo del sistema autopoiético que mantiene la circularidad
productiva y permite la metaproducción.
"""

from typing import Optional, Any
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from orchestrator_state import OrchestratorState, RouteLabel
from agent_repository import AgentRepository
from meta_agent_router import MetaAgentRouter
from execution_nodes import DirectExecutionNode, StructuralDiagnosisNode
from langchain_openai import ChatOpenAI
import os
import requests
from typing import List, Any, Dict
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import Generation, LLMResult
from abc import ABC, abstractmethod


class CloudflareResponseParser(ABC):
    """Clase base abstracta para analizar las respuestas de la IA de Cloudflare."""
    @abstractmethod
    def parse(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Analiza los datos de respuesta y devuelve el contenido del mensaje si se encuentra.
        """
        pass

class OutputFormatParser(CloudflareResponseParser):
    """Analiza el formato 'output' de Cloudflare."""
    def parse(self, data: Dict[str, Any]) -> Optional[str]:
        if "output" not in data:
            return None
        
        output_list = data["output"]
        if not isinstance(output_list, list):
            return None

        for item in output_list:
            if isinstance(item, dict) and item.get("type") == "message":
                if item.get("role") == "assistant" and "content" in item:
                    content_list = item["content"]
                    if isinstance(content_list, list):
                        for content_item in content_list:
                            if isinstance(content_item, dict):
                                if content_item.get("type") == "output_text" and "text" in content_item:
                                    return content_item["text"]
        return None

class ResultFormatParser(CloudflareResponseParser):
    """Analiza el formato 'result' de Cloudflare."""
    def parse(self, data: Dict[str, Any]) -> Optional[str]:
        if "result" not in data:
            return None
            
        result_data = data["result"]
        
        if isinstance(result_data, list) and len(result_data) > 0:
            for item in result_data:
                if isinstance(item, dict):
                    if item.get("role") == "assistant" and "content" in item:
                        content_list = item["content"]
                        if isinstance(content_list, list):
                            for content_item in content_list:
                                if isinstance(content_item, dict):
                                    # Priorizar output_text
                                    if content_item.get("type") == "output_text" and "text" in content_item:
                                        return content_item["text"]
                                    # Fallback a cualquier texto
                                    elif "text" in content_item:
                                        return content_item["text"]
        
        if isinstance(result_data, str):
            return result_data
            
        return None


class CloudflareWorkersAI(BaseLLM):
    """
    Cliente LangChain para Cloudflare Workers AI (API directa).
    Más simple que usar AI Gateway - no requiere configuración adicional.
    """
    
    account_id: str
    auth_token: str
    model: str = "@cf/meta/llama-2-7b-chat-int8"
    
    def __init__(self, account_id: str, auth_token: str, model: str = "@cf/meta/llama-2-7b-chat-int8", **kwargs):
        super().__init__(account_id=account_id, auth_token=auth_token, model=model, **kwargs)
        self.response_parsers: List[CloudflareResponseParser] = [
            OutputFormatParser(),
            ResultFormatParser(),
        ]

    @property
    def _llm_type(self) -> str:
        return "cloudflare_workers_ai"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Llamada directa a Cloudflare Workers AI."""
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/v1/responses"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "input": prompt
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, dict):
                for parser in self.response_parsers:
                    parsed_text = parser.parse(result)
                    if parsed_text is not None:
                        return parsed_text
            
            # Fallback: devolver todo como string
            return str(result)
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error conectando con Cloudflare: {str(e)}")
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """Genera respuestas para múltiples prompts."""
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([Generation(text=text)])
        
        return LLMResult(generations=generations)
    
    def _format_messages_to_prompt(self, messages: List[BaseMessage]) -> str:
        """Convierte mensajes de LangChain a prompt de texto."""
        parts = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                parts.append(f"User: {msg.content}")
            elif isinstance(msg, AIMessage):
                parts.append(f"Assistant: {msg.content}")
            elif isinstance(msg, SystemMessage):
                parts.append(f"System: {msg.content}")
        return "\n\n".join(parts) + "\n\nAssistant:"
    
    def invoke(self, input: Any, config: Optional[Dict] = None, **kwargs) -> AIMessage:
        """Invoke compatible con LangChain (acepta string o mensajes)."""
        if isinstance(input, str):
            prompt = input
        elif isinstance(input, list):
            prompt = self._format_messages_to_prompt(input)
        else:
            prompt = str(input)
        
        content = self._call(prompt, **kwargs)
        return AIMessage(content=content)


class AutopoieticOrchestrator:
    """
    Orquestador principal del sistema autopoiético de agentes.
    
    Implementa un grafo de LangGraph con:
    - Nodo de routing (Meta-Agente)
    - Nodos de ejecución (directa y diagnóstico)
    - Flujo condicional basado en evaluación de tareas
    - Persistencia para continuidad entre sesiones
    """
    
    def __init__(
        self,
        model_name: str = "gpt-4",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        enable_checkpointing: bool = True,
        llm: Optional[Any] = None,
    ):
        """
        Inicializa el orquestador autopoiético.
        
        Args:
            model_name: Nombre del modelo LLM
            base_url: URL base para API compatible con OpenAI
            api_key: Clave API
            enable_checkpointing: Si se habilita persistencia
        """
        # Inicializar repositorio de agentes
        self.agent_repository = AgentRepository()
        
        # Preparar instancia LLM común para todos los nodos (inyectable)
        self.llm = llm or self._build_default_llm(model_name=model_name, base_url=base_url, api_key=api_key)

        # Inicializar componentes
        self.router = MetaAgentRouter(
            agent_repository=self.agent_repository,
            model_name=model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=0.0,  # Determinístico para routing
            llm=self.llm,
        )
        
        self.direct_executor = DirectExecutionNode(
            agent_repository=self.agent_repository,
            model_name=model_name,
            base_url=base_url,
            api_key=api_key,
            llm=self.llm,
        )
        
        self.structural_diagnosis = StructuralDiagnosisNode(
            agent_repository=self.agent_repository,
            model_name=model_name,
            base_url=base_url,
            api_key=api_key,
            llm=self.llm,
        )
        
        # Construir grafo
        self.graph = self._build_graph()
        
        # Compilar con checkpointer si está habilitado
        checkpointer = MemorySaver() if enable_checkpointing else None
        self.app = self.graph.compile(checkpointer=checkpointer)
    
    def _build_graph(self) -> StateGraph:
        """
        Construye el grafo de estados de LangGraph.
        
        Estructura del grafo:
        START → router → {DIAGNOSTICO_ESTRUCTURAL, EJECUCION_DIRECTA} → END
        """
        # Crear grafo con el estado tipado
        graph = StateGraph(OrchestratorState)
        
        # Añadir nodos
        graph.add_node("router", self.router.evaluate_task)
        graph.add_node("direct_execution", self.direct_executor.execute)
        graph.add_node("structural_diagnosis", self.structural_diagnosis.diagnose)
        
        # Arista inicial: START → router
        graph.add_edge(START, "router")
        
        # Aristas condicionales desde el router
        graph.add_conditional_edges(
            "router",
            self.router.get_route_condition,
            {
                "DIAGNOSTICO_ESTRUCTURAL": "structural_diagnosis",
                "EJECUCION_DIRECTA": "direct_execution",
                "END": END,
            }
        )
        
        # Aristas finales: ambos nodos de ejecución terminan
        graph.add_edge("direct_execution", END)
        graph.add_edge("structural_diagnosis", END)
        
        return graph

    def _build_default_llm(self, model_name: str, base_url: Optional[str], api_key: Optional[str]):
        """
        Construye un LLM por defecto basado en variables de entorno/proveedor.
        Soporta: openai, cloudflare, lmstudio.
        
        Cloudflare usa API directa: /ai/v1/responses
        """
        provider = (os.getenv("LLM_PROVIDER", "openai") or "openai").lower()

        if provider == "cloudflare":
            # Cloudflare Workers AI - API directa
            account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
            auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
            model = os.getenv("CLOUDFLARE_MODEL", "@cf/openai/gpt-oss-120b")
            
            if not account_id or not auth_token:
                raise ValueError(
                    "Para usar Cloudflare, configura CLOUDFLARE_ACCOUNT_ID y "
                    "CLOUDFLARE_AUTH_TOKEN en .env"
                )
            
            return CloudflareWorkersAI(
                account_id=account_id,
                auth_token=auth_token,
                model=model
            )
            
        # OpenAI o LM Studio (endpoint OpenAI-compatible)
        llm_kwargs = {
            "model": model_name,
            "temperature": 0.2,
        }
        
        if provider == "lmstudio":
            # LM Studio
            base = base_url or os.getenv("LM_STUDIO_BASE_URL")
            if base:
                llm_kwargs["base_url"] = base
                llm_kwargs["api_key"] = api_key or "sk-no-key"
        else:
            # OpenAI por defecto
            if api_key or os.getenv("OPENAI_API_KEY"):
                llm_kwargs["api_key"] = api_key or os.getenv("OPENAI_API_KEY")
            if base_url:
                llm_kwargs["base_url"] = base_url

        return ChatOpenAI(**llm_kwargs)
    
    def invoke(
        self, 
        user_input: str, 
        thread_id: Optional[str] = None
    ) -> dict:
        """
        Invoca el orquestador con una entrada del usuario.
        
        Args:
            user_input: Tarea o consulta del usuario
            thread_id: ID de hilo para persistencia (opcional)
            
        Returns:
            Estado final del grafo después de la ejecución
        """
        # Preparar estado inicial
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "route": None,
            "task_complexity": None,
            "viability_kpis": None,
            "context": None,
            "agent_catalog": None,
        }
        
        # Configuración para checkpointing
        config = {}
        if thread_id:
            config["configurable"] = {"thread_id": thread_id}
        
        # Ejecutar el grafo
        result = self.app.invoke(initial_state, config=config)
        
        return result
    
    async def ainvoke(
        self, 
        user_input: str, 
        thread_id: Optional[str] = None
    ) -> dict:
        """
        Versión asíncrona de invoke.
        """
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "route": None,
            "task_complexity": None,
            "viability_kpis": None,
            "context": None,
            "agent_catalog": None,
        }
        
        config = {}
        if thread_id:
            config["configurable"] = {"thread_id": thread_id}
        
        result = await self.app.ainvoke(initial_state, config=config)
        
        return result
    
    def stream(self, user_input: str, thread_id: Optional[str] = None):
        """
        Ejecuta el grafo con streaming de eventos.
        
        Útil para UIs reactivas que necesitan updates incrementales.
        """
        initial_state = {
            "messages": [{"role": "user", "content": user_input}],
            "route": None,
            "task_complexity": None,
            "viability_kpis": None,
            "context": None,
            "agent_catalog": None,
        }
        
        config = {}
        if thread_id:
            config["configurable"] = {"thread_id": thread_id}
        
        for event in self.app.stream(initial_state, config=config):
            yield event
    
    def get_graph_visualization(self) -> str:
        """
        Retorna una representación visual del grafo (si está disponible).
        
        Útil para debugging y documentación.
        """
        try:
            # LangGraph puede tener métodos para visualización
            # Esto es un placeholder para futuras implementaciones
            return "Graph visualization not implemented yet"
        except Exception as e:
            return f"Error generating visualization: {str(e)}"
    
    def get_agent_catalog(self) -> list[dict]:
        """
        Obtiene el catálogo actual de agentes.
        """
        return self.agent_repository.get_catalog_summary()
    
    def add_agent_to_catalog(self, agent_spec: dict) -> bool:
        """
        Añade un nuevo agente al catálogo (metaproducción).
        
        Args:
            agent_spec: Diccionario con la especificación del agente
            
        Returns:
            True si se añadió exitosamente
        """
        from orchestrator_state import AgentSpec
        
        try:
            spec = AgentSpec(**agent_spec)
            self.agent_repository.add_agent(spec)
            return True
        except Exception as e:
            print(f"Error añadiendo agente: {e}")
            return False


def create_orchestrator(
    model_name: str = "gpt-4",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    llm_provider: str = "openai",
) -> AutopoieticOrchestrator:
    """
    Factory function para crear un orquestador autopoiético.
    
    Args:
        model_name: Nombre del modelo LLM
        base_url: URL base para API compatible con OpenAI (e.g., LM Studio)
        api_key: Clave API
        llm_provider: Proveedor de LLM ("openai", "cloudflare", "lmstudio")
        
    Returns:
        Instancia del orquestador
        
    Ejemplos de uso:
    
        # Con OpenAI:
        >>> orchestrator = create_orchestrator(
        ...     model_name="gpt-4",
        ...     api_key="sk-...",
        ...     llm_provider="openai"
        ... )
        
        # Con Cloudflare Workers AI:
        >>> orchestrator = create_orchestrator(
        ...     model_name="llama-2-7b",
        ...     llm_provider="cloudflare"
        ... )
        
        # Con LM Studio:
        >>> orchestrator = create_orchestrator(
        ...     model_name="qwen2.5-coder-14b-instruct",
        ...     base_url="http://localhost:1234/v1",
        ...     api_key="sk-no-key",
        ...     llm_provider="lmstudio"
        ... )
    """
    # Construir LLM según provider
    provider = (llm_provider or os.getenv("LLM_PROVIDER", "openai")).lower()

    if provider == "cloudflare":
        # Cloudflare Workers AI - API directa
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
        model = os.getenv("CLOUDFLARE_MODEL", "@cf/openai/gpt-oss-120b")
        
        if not account_id or not auth_token:
            raise ValueError(
                "Para usar Cloudflare, configura CLOUDFLARE_ACCOUNT_ID y "
                "CLOUDFLARE_AUTH_TOKEN en .env"
            )
        
        llm = CloudflareWorkersAI(
            account_id=account_id,
            auth_token=auth_token,
            model=model
        )
    else:
        # OpenAI o LM Studio (endpoint OpenAI-compatible)
        llm_kwargs = {
            "model": model_name,
            "temperature": 0.2,
        }
        
        if provider == "lmstudio":
            # LM Studio
            base = base_url or os.getenv("LM_STUDIO_BASE_URL")
            if base:
                llm_kwargs["base_url"] = base
                llm_kwargs["api_key"] = api_key or "sk-no-key"
        else:
            # OpenAI por defecto
            if api_key or os.getenv("OPENAI_API_KEY"):
                llm_kwargs["api_key"] = api_key or os.getenv("OPENAI_API_KEY")
            if base_url:
                llm_kwargs["base_url"] = base_url
        
        llm = ChatOpenAI(**llm_kwargs)

    return AutopoieticOrchestrator(
        model_name=model_name,
        base_url=base_url,
        api_key=api_key,
        llm=llm,
    )
