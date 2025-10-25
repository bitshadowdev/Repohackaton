"""
Aplicación principal del Sistema Autopoiético de Agentes.

Punto de entrada para ejecutar el orquestador y procesar tareas.
"""

import os
import sys
from pathlib import Path

# Añadir src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from autopoietic_orchestrator import create_orchestrator
from dotenv import load_dotenv


def main():
    """
    Función principal que ejecuta el orquestador autopoiético.
    """
    # Cargar variables de entorno
    load_dotenv()
    
    print("=" * 80)
    print("SISTEMA AUTOPOIÉTICO DE AGENTES DE IA")
    print("Meta-Agente Orquestador con LangGraph")
    print("=" * 80)
    print()
    
    # Configuración del LLM
    # Opción 1: Usar OpenAI (requiere OPENAI_API_KEY en .env)
    # Opción 2: Usar LM Studio local (descomenta las líneas siguientes)
    
    provider = (os.getenv("LLM_PROVIDER", "openai") or "openai").lower()
    print(f"Proveedor LLM configurado: {provider}")

    # Construir orquestador según provider
    if provider == "cloudflare":
        # Cloudflare no requiere base_url; credenciales van en .env
        orchestrator = create_orchestrator(
            model_name=os.getenv("CLOUDFLARE_MODEL", "llama-2-7b"),
            llm_provider="cloudflare",
        )
    elif provider == "lmstudio":
        orchestrator = create_orchestrator(
            model_name=os.getenv("LM_STUDIO_MODEL", "qwen2.5-coder-14b-instruct"),
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key="sk-no-key",
            llm_provider="lmstudio",
        )
    else:
        # OpenAI por defecto
        orchestrator = create_orchestrator(
            model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
            api_key=os.getenv("OPENAI_API_KEY"),
            llm_provider="openai",
        )
    
    # Para LM Studio (local):
    # orchestrator = create_orchestrator(
    #     model_name="qwen2.5-coder-14b-instruct",
    #     base_url="http://localhost:1234/v1",
    #     api_key="sk-no-key"
    # )
    
    # Mostrar catálogo de agentes disponibles
    print("\n📋 CATÁLOGO DE AGENTES DISPONIBLES:")
    print("-" * 80)
    catalog = orchestrator.get_agent_catalog()
    for agent in catalog:
        status = "✅" if agent["active"] else "❌"
        print(f"{status} {agent['agent_id']}")
        print(f"   Rol: {agent['role']}")
        print(f"   Capacidades: {', '.join(agent['capabilities'])}")
        print()
    
    # Modo interactivo
    print("\n💬 MODO INTERACTIVO")
    print("Escribe tu tarea o pregunta (o 'salir' para terminar)")
    print("-" * 80)
    
    session_id = "session_001"
    
    while True:
        try:
            user_input = input("\n👤 Usuario: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["salir", "exit", "quit", "q"]:
                print("\n👋 ¡Hasta luego!")
                break
            
            # Procesar la tarea
            print("\n🤖 Procesando...\n")
            
            result = orchestrator.invoke(user_input, thread_id=session_id)
            
            # Mostrar resultado
            print("\n" + "=" * 80)
            print("RESULTADO:")
            print("=" * 80)
            
            # Mostrar métricas de routing
            if result.get("route"):
                print(f"\n📊 Ruta elegida: {result['route']}")
            if result.get("task_complexity") is not None:
                print(f"📈 Complejidad de tarea: {result['task_complexity']:.2f}")
            
            # Mostrar mensajes
            print("\n💬 Respuesta:")
            print("-" * 80)
            messages = result.get("messages", [])
            if messages:
                # Mostrar el último mensaje (la respuesta del asistente)
                last_msg = messages[-1]
                if isinstance(last_msg, dict):
                    print(last_msg.get("content", str(last_msg)))
                else:
                    content = getattr(last_msg, "content", str(last_msg))
                    print(content)
            
            print("\n" + "=" * 80)
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


def demo_examples():
    """
    Ejecuta ejemplos de demostración del sistema.
    """
    print("=" * 80)
    print("EJEMPLOS DE DEMOSTRACIÓN")
    print("=" * 80)
    
    # Crear orquestador
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    # Ejemplos de tareas
    examples = [
        # Tarea simple (EJECUCION_DIRECTA)
        "¿Cuál es la capital de Francia?",
        
        # Tarea de windsurf (debería usar agente especializado)
        "Quiero organizar un viaje de windsurf a la costa. ¿Qué condiciones meteorológicas necesito?",
        
        # Tarea compleja que podría requerir nuevo agente (DIAGNOSTICO_ESTRUCTURAL)
        "Necesito analizar datos de sensores IoT en tiempo real y predecir fallos en maquinaria industrial",
        
        # Tarea de código (debería usar code_analyst)
        "Revisa este código Python y encuentra posibles bugs: def suma(a,b): return a+b+1",
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n\n{'='*80}")
        print(f"EJEMPLO {i}")
        print(f"{'='*80}")
        print(f"\n👤 Tarea: {example}")
        
        result = orchestrator.invoke(example, thread_id=f"demo_{i}")
        
        print(f"\n📊 Ruta: {result.get('route')}")
        print(f"📈 Complejidad: {result.get('task_complexity', 0):.2f}")
        
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            content = last_msg.get("content") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
            print(f"\n🤖 Respuesta:\n{content[:500]}...")  # Truncar para demo


if __name__ == "__main__":
    # Usar modo interactivo por defecto
    # Para ejecutar ejemplos, descomenta la siguiente línea:
    # demo_examples()
    
    main()
