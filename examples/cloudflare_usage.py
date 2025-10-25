"""
Ejemplo de uso del Sistema Autopoiético con Cloudflare Workers AI.

Este ejemplo muestra cómo usar Cloudflare Workers AI como backend LLM
en lugar de OpenAI, lo cual es más económico.
"""

import sys
from pathlib import Path
import os

# Añadir src al path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root / "src"))

from query_llm import create_cloudflare_llm, CLOUDFLARE_MODELS
from dotenv import load_dotenv

load_dotenv()


def ejemplo_basico_cloudflare():
    """
    Ejemplo básico de uso directo del LLM de Cloudflare.
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: Uso Básico de Cloudflare Workers AI")
    print("="*80)
    
    # Crear LLM de Cloudflare
    llm = create_cloudflare_llm(
        model="llama-2-7b",  # Modelo económico y rápido
        temperature=0.7
    )
    
    # Test simple
    print("\n📝 Pregunta: ¿Qué es Python?")
    respuesta = llm.invoke("Explica qué es Python en una oración.")
    print(f"\n🤖 Respuesta: {respuesta}")


def ejemplo_modelos_disponibles():
    """
    Muestra los modelos disponibles en Cloudflare Workers AI.
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: Modelos Disponibles en Cloudflare")
    print("="*80)
    
    print("\n📋 Modelos de chat disponibles:")
    print("-" * 80)
    
    for nombre, modelo_id in CLOUDFLARE_MODELS.items():
        tipo = "Chat/Texto" if "chat" in modelo_id or "instruct" in modelo_id else "Embeddings"
        print(f"  • {nombre:15} → {modelo_id:50} [{tipo}]")
    
    print("\n💡 Tip: Los modelos más pequeños (tinyllama) son más rápidos")
    print("        Los modelos más grandes (llama-2-13b) son más precisos")


def ejemplo_comparacion_modelos():
    """
    Compara respuestas de diferentes modelos de Cloudflare.
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: Comparación de Modelos")
    print("="*80)
    
    pregunta = "¿Qué son los principios SOLID en programación?"
    
    modelos_a_probar = ["tinyllama", "llama-2-7b", "mistral-7b"]
    
    for modelo in modelos_a_probar:
        if modelo not in CLOUDFLARE_MODELS:
            continue
        
        print(f"\n🔹 Modelo: {modelo}")
        print("-" * 80)
        
        try:
            llm = create_cloudflare_llm(model=modelo, temperature=0.3)
            respuesta = llm.invoke(pregunta)
            print(f"Respuesta: {respuesta[:300]}...")
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def ejemplo_con_orquestador():
    """
    Integra Cloudflare Workers AI con el sistema autopoiético.
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: Cloudflare con Sistema Autopoiético")
    print("="*80)
    
    # NOTA: Para usar Cloudflare con el orquestador, necesitamos
    # modificar la implementación para aceptar LLMs personalizados
    
    print("\n📝 Para integrar Cloudflare con el orquestador:")
    print("""
    1. El orquestador actual usa ChatOpenAI de LangChain
    2. Para usar Cloudflare, necesitamos pasar CloudflareLLM personalizado
    3. Esto requiere modificar AutopoieticOrchestrator para aceptar llm_instance
    
    Ejemplo futuro:
    
        from src.query_llm import create_cloudflare_llm
        from src.autopoietic_orchestrator import AutopoieticOrchestrator
        
        # Crear LLM de Cloudflare
        llm = create_cloudflare_llm(model="llama-2-7b")
        
        # Crear orquestador con LLM personalizado
        orchestrator = AutopoieticOrchestrator(llm_instance=llm)
        
        # Usar normalmente
        result = orchestrator.invoke("Organizar viaje de windsurf")
    """)


def ejemplo_costo_comparativo():
    """
    Muestra la comparación de costos entre proveedores.
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: Comparación de Costos")
    print("="*80)
    
    print("""
    💰 COMPARACIÓN DE COSTOS (aproximados):
    
    OpenAI GPT-4:
      - Input: $0.03 / 1K tokens
      - Output: $0.06 / 1K tokens
      - Promedio: ~$0.05 / request
    
    Cloudflare Workers AI:
      - Modelo Llama 2: $0.00001 / 1K tokens
      - Modelo Mistral: $0.00001 / 1K tokens
      - Promedio: ~$0.0001 / request
      
    LM Studio (Local):
      - Costo: $0 (gratis)
      - Requisito: GPU/CPU local
    
    📊 Cloudflare es ~500x más barato que OpenAI
    📊 LM Studio es gratis pero requiere hardware local
    """)


def test_conexion_cloudflare():
    """
    Verifica que las credenciales de Cloudflare estén configuradas.
    """
    print("\n" + "="*80)
    print("TEST: Verificación de Credenciales Cloudflare")
    print("="*80)
    
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
    
    print("\n🔍 Verificando configuración...")
    
    if not account_id:
        print("❌ CLOUDFLARE_ACCOUNT_ID no configurado en .env")
        print("   Obtén tu Account ID en: https://dash.cloudflare.com")
    else:
        print(f"✅ CLOUDFLARE_ACCOUNT_ID: {account_id[:8]}...")
    
    if not auth_token:
        print("❌ CLOUDFLARE_AUTH_TOKEN no configurado en .env")
        print("   Crea un token en: https://dash.cloudflare.com/profile/api-tokens")
    else:
        print(f"✅ CLOUDFLARE_AUTH_TOKEN: {auth_token[:8]}...")
    
    if account_id and auth_token:
        print("\n✅ Credenciales configuradas correctamente")
        print("\n🧪 Probando conexión...")
        
        try:
            llm = create_cloudflare_llm(model="tinyllama", temperature=0.5)
            respuesta = llm.invoke("Di 'Hola'")
            print(f"\n🎉 ¡Conexión exitosa!")
            print(f"📝 Respuesta de prueba: {respuesta}")
        except Exception as e:
            print(f"\n❌ Error al conectar: {str(e)}")
            print("\nVerifica que:")
            print("  1. Las credenciales sean correctas")
            print("  2. Tengas acceso a Workers AI en tu cuenta")
            print("  3. Tu conexión a internet esté activa")
    else:
        print("\n⚠️  Configura tus credenciales en .env para continuar")


def guia_configuracion():
    """
    Guía paso a paso para configurar Cloudflare Workers AI.
    """
    print("\n" + "="*80)
    print("GUÍA: Cómo Configurar Cloudflare Workers AI")
    print("="*80)
    
    print("""
    📚 PASOS PARA CONFIGURAR CLOUDFLARE WORKERS AI:
    
    1️⃣  CREAR CUENTA EN CLOUDFLARE:
       - Ve a: https://dash.cloudflare.com
       - Regístrate o inicia sesión
       - Es gratis para empezar
    
    2️⃣  OBTENER ACCOUNT ID:
       - En el dashboard, ve a cualquier sección
       - El Account ID aparece en la barra lateral
       - Cópialo y guárdalo
    
    3️⃣  CREAR API TOKEN:
       - Ve a: https://dash.cloudflare.com/profile/api-tokens
       - Click en "Create Token"
       - Selecciona "Edit Cloudflare Workers" template
       - O crea un Custom Token con permisos de Workers AI
       - Copia el token (solo se muestra una vez)
    
    4️⃣  CONFIGURAR .ENV:
       - Abre el archivo .env en tu proyecto
       - Añade:
         CLOUDFLARE_ACCOUNT_ID=tu-account-id-aqui
         CLOUDFLARE_AUTH_TOKEN=tu-token-aqui
    
    5️⃣  PROBAR CONEXIÓN:
       - Ejecuta: python examples/cloudflare_usage.py
       - El test verificará tu configuración
    
    💡 TIPS:
       - Workers AI tiene un free tier generoso
       - Los modelos pequeños (tinyllama) son ideales para desarrollo
       - Usa modelos grandes (llama-2-13b) solo para producción
       - Cloudflare tiene latencia baja (edge computing)
    
    📖 Documentación oficial:
       https://developers.cloudflare.com/workers-ai/
    """)


if __name__ == "__main__":
    print("\n" + "🌩️ "*40)
    print("EJEMPLOS DE USO: CLOUDFLARE WORKERS AI")
    print("🌩️ "*40)
    
    # Ejecutar todos los ejemplos
    # Comenta/descomenta según lo que quieras probar
    
    # test_conexion_cloudflare()  # Empieza por aquí
    # guia_configuracion()
    # ejemplo_modelos_disponibles()
    # ejemplo_basico_cloudflare()
    # ejemplo_comparacion_modelos()
    # ejemplo_costo_comparativo()
    
    # Por defecto, mostrar la guía
    print("\n📋 Ejecutando: Verificación + Guía de Configuración\n")
    test_conexion_cloudflare()
    guia_configuracion()
    
    print("\n" + "✅"*40)
    print("FIN DE EJEMPLOS")
    print("✅"*40 + "\n")
