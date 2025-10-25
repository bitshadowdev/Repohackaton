"""
Ejemplos básicos de uso del Sistema Autopoiético de Agentes.

Este archivo muestra cómo usar el orquestador en diferentes escenarios.
"""

import sys
from pathlib import Path

# Añadir src al path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from autopoietic_orchestrator import create_orchestrator
from orchestrator_state import AgentSpec
import os
from dotenv import load_dotenv

load_dotenv()


def ejemplo_1_tarea_simple():
    """
    Ejemplo 1: Tarea simple que usa ejecución directa.
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Tarea Simple (Ejecución Directa)")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    tarea = "¿Cuál es la capital de Francia?"
    print(f"\n📝 Tarea: {tarea}")
    
    result = orchestrator.invoke(tarea, thread_id="ejemplo_1")
    
    print(f"\n📊 Ruta: {result['route']}")
    print(f"📈 Complejidad: {result.get('task_complexity', 0):.2f}")
    print(f"\n💬 Respuesta:")
    print("-" * 80)
    print(result['messages'][-1]['content'])


def ejemplo_2_agente_especializado():
    """
    Ejemplo 2: Tarea que requiere agente especializado (windsurf).
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Agente Especializado (Windsurf)")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    tarea = "Quiero hacer windsurf este fin de semana. ¿Qué condiciones de viento necesito y qué equipo debo llevar?"
    print(f"\n📝 Tarea: {tarea}")
    
    result = orchestrator.invoke(tarea, thread_id="ejemplo_2")
    
    print(f"\n📊 Ruta: {result['route']}")
    print(f"📈 Complejidad: {result.get('task_complexity', 0):.2f}")
    print(f"\n💬 Respuesta:")
    print("-" * 80)
    print(result['messages'][-1]['content'])


def ejemplo_3_metaproduccion():
    """
    Ejemplo 3: Tarea compleja que requiere metaproducción.
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Metaproducción (Diagnóstico Estructural)")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    tarea = """Necesito un sistema que analice en tiempo real datos de sensores IoT 
    de maquinaria industrial, detecte patrones anómalos usando machine learning, 
    y prediga fallos antes de que ocurran."""
    
    print(f"\n📝 Tarea: {tarea}")
    
    result = orchestrator.invoke(tarea, thread_id="ejemplo_3")
    
    print(f"\n📊 Ruta: {result['route']}")
    print(f"📈 Complejidad: {result.get('task_complexity', 0):.2f}")
    print(f"\n💬 Respuesta:")
    print("-" * 80)
    print(result['messages'][-1]['content'][:1000] + "...")  # Truncar para brevedad


def ejemplo_4_agregar_agente():
    """
    Ejemplo 4: Añadir un nuevo agente al catálogo.
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Añadir Nuevo Agente al Catálogo")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    print("\n📋 Catálogo ANTES de añadir agente:")
    print("-" * 80)
    catalog = orchestrator.get_agent_catalog()
    for agent in catalog:
        print(f"  - {agent['agent_id']}: {agent['role']}")
    
    # Crear nuevo agente
    nuevo_agente = AgentSpec(
        agent_id="financial_analyst",
        role="Analista financiero",
        capabilities=["market_analysis", "portfolio_optimization", "risk_assessment"],
        tools=["stock_api", "financial_calculator", "news_aggregator"],
        system_prompt="""Eres un analista financiero experto.
Analizas mercados, optimizas portafolios y evalúas riesgos.
Usa datos actualizados y proporciona análisis fundamentados.""",
        version="1.0.0",
        active=True
    )
    
    # Añadir al catálogo
    success = orchestrator.add_agent_to_catalog(nuevo_agente.dict())
    
    if success:
        print(f"\n✅ Agente '{nuevo_agente.agent_id}' añadido exitosamente")
    
    print("\n📋 Catálogo DESPUÉS de añadir agente:")
    print("-" * 80)
    catalog = orchestrator.get_agent_catalog()
    for agent in catalog:
        print(f"  - {agent['agent_id']}: {agent['role']}")


def ejemplo_5_conversacion_multiturno():
    """
    Ejemplo 5: Conversación multi-turno con persistencia.
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: Conversación Multi-turno (Persistencia)")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    thread_id = "conversation_1"
    
    # Turno 1
    print("\n🔵 Turno 1:")
    tarea1 = "Revisa este código: def suma(a, b): return a + b + 1"
    print(f"👤 Usuario: {tarea1}")
    
    result1 = orchestrator.invoke(tarea1, thread_id=thread_id)
    print(f"🤖 Asistente: {result1['messages'][-1]['content'][:200]}...")
    
    # Turno 2 (el sistema debe recordar el contexto)
    print("\n🔵 Turno 2:")
    tarea2 = "¿Cuál es el error que encontraste?"
    print(f"👤 Usuario: {tarea2}")
    
    result2 = orchestrator.invoke(tarea2, thread_id=thread_id)
    print(f"🤖 Asistente: {result2['messages'][-1]['content'][:200]}...")


def ejemplo_6_streaming():
    """
    Ejemplo 6: Uso de streaming para respuestas incrementales.
    """
    print("\n" + "="*80)
    print("EJEMPLO 6: Streaming de Respuestas")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    tarea = "Explica los principios de autopoiesis en sistemas de IA"
    print(f"\n📝 Tarea: {tarea}")
    print("\n💬 Streaming de eventos:")
    print("-" * 80)
    
    for event in orchestrator.stream(tarea, thread_id="streaming_1"):
        print(f"📡 Evento: {list(event.keys())}")


def ejemplo_7_catalogo_completo():
    """
    Ejemplo 7: Explorar el catálogo de agentes completo.
    """
    print("\n" + "="*80)
    print("EJEMPLO 7: Catálogo Completo de Agentes")
    print("="*80)
    
    orchestrator = create_orchestrator(
        model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    catalog = orchestrator.get_agent_catalog()
    
    print(f"\n📊 Total de agentes: {len(catalog)}")
    print("-" * 80)
    
    for agent in catalog:
        status = "✅ ACTIVO" if agent["active"] else "❌ INACTIVO"
        print(f"\n{status}")
        print(f"  ID: {agent['agent_id']}")
        print(f"  Rol: {agent['role']}")
        print(f"  Capacidades: {', '.join(agent['capabilities'])}")


if __name__ == "__main__":
    print("\n" + "🎯" * 40)
    print("EJEMPLOS DE USO - SISTEMA AUTOPOIÉTICO DE AGENTES")
    print("🎯" * 40)
    
    # Ejecutar ejemplos
    # Descomenta los que quieras probar:
    
    # ejemplo_1_tarea_simple()
    # ejemplo_2_agente_especializado()
    # ejemplo_3_metaproduccion()
    # ejemplo_4_agregar_agente()
    # ejemplo_5_conversacion_multiturno()
    # ejemplo_6_streaming()
    ejemplo_7_catalogo_completo()
    
    print("\n" + "✅" * 40)
    print("FIN DE EJEMPLOS")
    print("✅" * 40 + "\n")
