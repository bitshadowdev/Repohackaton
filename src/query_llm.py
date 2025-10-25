"""
Cliente LLM para Cloudflare Workers AI.

Proporciona una interfaz compatible con LangChain para usar
modelos de Cloudflare Workers AI en el sistema autopoiético.
"""

import os
import requests
from typing import Any, List, Optional, Dict
from dotenv import load_dotenv
from langchain_core.language_models.llms import BaseLLM
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_core.outputs import Generation, LLMResult
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

load_dotenv()


class CloudflareLLM(BaseLLM):
    """
    LLM compatible con LangChain que usa Cloudflare Workers AI.
    
    Permite usar modelos de Cloudflare como alternativa a OpenAI
    en el sistema autopoiético.
    
    Ejemplo de uso:
        >>> llm = CloudflareLLM(
        ...     account_id="tu-account-id",
        ...     auth_token="tu-token",
        ...     model="@cf/meta/llama-2-7b-chat-int8"
        ... )
        >>> response = llm.invoke("¿Qué es Python?")
    """
    
    account_id: str
    auth_token: str
    model: str = "@cf/meta/llama-2-7b-chat-int8"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    def __init__(
        self,
        account_id: Optional[str] = None,
        auth_token: Optional[str] = None,
        model: str = "@cf/meta/llama-2-7b-chat-int8",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ):
        """
        Inicializa el cliente de Cloudflare LLM.
        
        Args:
            account_id: ID de cuenta de Cloudflare (o usa env var CLOUDFLARE_ACCOUNT_ID)
            auth_token: Token de autenticación (o usa env var CLOUDFLARE_AUTH_TOKEN)
            model: Modelo a usar (por defecto: llama-2-7b-chat)
            temperature: Temperatura para generación (0.0-1.0)
            max_tokens: Máximo de tokens a generar
        """
        account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        auth_token = auth_token or os.getenv("CLOUDFLARE_AUTH_TOKEN")
        
        if not account_id or not auth_token:
            raise ValueError(
                "Se requiere CLOUDFLARE_ACCOUNT_ID y CLOUDFLARE_AUTH_TOKEN. "
                "Configúralos en .env o pásalos como argumentos."
            )
        
        super().__init__(
            account_id=account_id,
            auth_token=auth_token,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    @property
    def _llm_type(self) -> str:
        """Retorna el tipo de LLM."""
        return "cloudflare"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Llamada principal al LLM de Cloudflare.
        
        Args:
            prompt: Texto de entrada
            stop: Secuencias de parada (opcional)
            run_manager: Manager de callbacks
            
        Returns:
            Respuesta del modelo
        """
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
        }
        
        # Algunos modelos de Cloudflare soportan estos parámetros
        if self.temperature is not None:
            payload["temperature"] = self.temperature
        
        if stop:
            payload["stop"] = stop
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Cloudflare Workers AI puede retornar diferentes formatos
            # Intentamos extraer la respuesta del formato más común
            if result.get("success") and result.get("result"):
                response_text = result["result"].get("response", "")
                if not response_text:
                    # Algunos modelos retornan en 'text'
                    response_text = result["result"].get("text", "")
                if not response_text:
                    # O en 'generated_text'
                    response_text = result["result"].get("generated_text", "")
                return response_text
            else:
                error_msg = result.get("errors", ["Error desconocido"])
                raise ValueError(f"Error en Cloudflare API: {error_msg}")
                
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error al conectar con Cloudflare: {str(e)}")
    
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """
        Genera respuestas para múltiples prompts.
        """
        generations = []
        for prompt in prompts:
            text = self._call(prompt, stop=stop, run_manager=run_manager, **kwargs)
            generations.append([Generation(text=text)])
        
        return LLMResult(generations=generations)


class CloudflareChatLLM(CloudflareLLM):
    """
    Versión del LLM de Cloudflare compatible con mensajes de chat.
    
    Formatea mensajes en el estilo esperado por modelos de chat.
    """
    
    def _format_messages(self, messages: List[BaseMessage]) -> str:
        """
        Formatea una lista de mensajes en un prompt para el modelo.
        
        Args:
            messages: Lista de mensajes (HumanMessage, AIMessage, etc.)
            
        Returns:
            Prompt formateado como string
        """
        formatted_parts = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_parts.append(f"User: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_parts.append(f"Assistant: {message.content}")
            else:
                # Otros tipos de mensajes (SystemMessage, etc.)
                role = getattr(message, "role", "User")
                formatted_parts.append(f"{role}: {message.content}")
        
        # Añadir prompt final para la respuesta
        formatted_parts.append("Assistant:")
        
        return "\n\n".join(formatted_parts)
    
    def invoke(self, input: Any, **kwargs) -> str:
        """
        Invoca el modelo con mensajes o texto.
        
        Args:
            input: Puede ser string o lista de mensajes
            
        Returns:
            Respuesta del modelo
        """
        if isinstance(input, list) and all(isinstance(m, BaseMessage) for m in input):
            prompt = self._format_messages(input)
        else:
            prompt = str(input)
        
        return self._call(prompt, **kwargs)


# ============================================================================
# MODELOS DISPONIBLES EN CLOUDFLARE WORKERS AI
# ============================================================================

CLOUDFLARE_MODELS = {
    # Modelos de chat/texto
    "llama-2-7b": "@cf/meta/llama-2-7b-chat-int8",
    "llama-2-13b": "@cf/meta/llama-2-13b-chat-int8",
    "mistral-7b": "@cf/mistral/mistral-7b-instruct-v0.1",
    "codellama-7b": "@cf/meta/codellama-7b-instruct",
    
    # Modelos más pequeños
    "tinyllama": "@cf/tinyllama/tinyllama-1.1b-chat-v1.0",
    
    # Embeddings (para RAG)
    "bge-base": "@cf/baai/bge-base-en-v1.5",
    "bge-small": "@cf/baai/bge-small-en-v1.5",
}


def create_cloudflare_llm(
    model: str = "llama-2-7b",
    temperature: float = 0.7,
    **kwargs
) -> CloudflareChatLLM:
    """
    Factory function para crear un LLM de Cloudflare.
    
    Args:
        model: Nombre corto del modelo (ver CLOUDFLARE_MODELS)
        temperature: Temperatura para generación
        **kwargs: Argumentos adicionales
        
    Returns:
        Instancia de CloudflareChatLLM
        
    Ejemplo:
        >>> llm = create_cloudflare_llm(model="llama-2-7b")
        >>> response = llm.invoke("¿Qué es Python?")
    """
    model_id = CLOUDFLARE_MODELS.get(model, model)
    
    return CloudflareChatLLM(
        model=model_id,
        temperature=temperature,
        **kwargs
    )


# ============================================================================
# EJEMPLO DE USO
# ============================================================================

def test_cloudflare_llm():
    """
    Función de prueba para el LLM de Cloudflare.
    """
    print("=" * 80)
    print("TEST: Cloudflare Workers AI")
    print("=" * 80)
    
    try:
        # Crear LLM
        llm = create_cloudflare_llm(model="llama-2-7b", temperature=0.7)
        
        # Test simple
        print("\n📝 Test 1: Pregunta simple")
        response = llm.invoke("¿Qué es Python en una oración?")
        print(f"Respuesta: {response}")
        
        # Test con mensajes
        print("\n📝 Test 2: Conversación con mensajes")
        messages = [
            HumanMessage(content="Hola, soy un desarrollador Python"),
            AIMessage(content="¡Hola! Encantado de ayudarte con Python."),
            HumanMessage(content="¿Cuál es la diferencia entre lista y tupla?")
        ]
        response = llm.invoke(messages)
        print(f"Respuesta: {response}")
        
        print("\n✅ Tests completados exitosamente")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de configurar en .env:")
        print("  CLOUDFLARE_ACCOUNT_ID=tu-account-id")
        print("  CLOUDFLARE_AUTH_TOKEN=tu-token")


if __name__ == "__main__":
    test_cloudflare_llm()