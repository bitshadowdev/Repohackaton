"""
Test de conexión con Cloudflare Workers AI usando API directa.

Ejecuta este script para verificar que tu configuración de Cloudflare esté correcta.
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 80)
print("TEST DE CONEXIÓN: CLOUDFLARE WORKERS AI (API Directa)")
print("=" * 80)
print()

# Verificar variables de entorno
print("🔍 Verificando configuración...")
print("-" * 80)

account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
model = os.getenv("CLOUDFLARE_MODEL", "@cf/openai/gpt-oss-120b")

if not account_id:
    print("❌ CLOUDFLARE_ACCOUNT_ID no configurado")
    sys.exit(1)
else:
    print(f"✅ CLOUDFLARE_ACCOUNT_ID: {account_id[:8]}...")

if not auth_token:
    print("❌ CLOUDFLARE_AUTH_TOKEN no configurado")
    sys.exit(1)
else:
    print(f"✅ CLOUDFLARE_AUTH_TOKEN: {auth_token[:8]}...")

print(f"✅ CLOUDFLARE_MODEL: {model}")

# Construir endpoint
api_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/responses"
print(f"\n📡 API Endpoint: {api_url}")
print("✅ Usando API directa de Workers AI (no requiere AI Gateway)")

# Test 1: Llamada simple
print("\n" + "=" * 80)
print("TEST 1: Llamada Simple")
print("=" * 80)
print("\n📝 Prompt: 'Di hola en una palabra'")

headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json"
}

payload = {
    "model": model,
    "input": "Di hola en una palabra"
}

try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(f"✅ Respuesta recibida: {result}")
except Exception as e:
    print(f"❌ Error en llamada: {e}")
    print(f"\nDetalles del error: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Pregunta más compleja
print("\n" + "=" * 80)
print("TEST 2: Pregunta Técnica")
print("=" * 80)
print("\n📝 Prompt: '¿Qué es Python en una oración?'")

payload = {
    "model": model,
    "input": "¿Qué es Python en una oración?"
}

try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    print(f"✅ Respuesta recibida: {result}")
except Exception as e:
    print(f"❌ Error en llamada: {e}")
    sys.exit(1)

# Resumen final
print("\n" + "=" * 80)
print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
print("=" * 80)
print()
print("🎉 Tu configuración de Cloudflare Workers AI está correcta.")
print("📌 Puedes usar el sistema con: python main.py")
print()
print("💡 Tips:")
print("  - El modelo actual es:", model)
print("  - Puedes cambiarlo en .env con CLOUDFLARE_MODEL")
print("  - Modelos disponibles: llama-2-7b, mistral-7b, codellama-7b, tinyllama")
print()
