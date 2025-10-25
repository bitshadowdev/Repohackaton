# 🌩️ Cloudflare Workers AI con Endpoint OpenAI-Compatible

## Cambio de Arquitectura

**Antes**: Cliente personalizado `CloudflareLLM` con API propietaria de Cloudflare
**Ahora**: Uso directo de `ChatOpenAI` de LangChain con endpoint OpenAI-compatible de Cloudflare

## ✅ Ventajas del Nuevo Approach

1. **Simplicidad**: No necesitas cliente personalizado
2. **Compatibilidad**: 100% compatible con LangChain (invoke, with_structured_output, etc.)
3. **Mantenibilidad**: Menos código custom, menos bugs
4. **Flexibilidad**: Funciona como cualquier otro endpoint OpenAI

---

## 📋 Configuración

### 1. Variables de Entorno (.env)

```bash
# Cloudflare Workers AI
CLOUDFLARE_ACCOUNT_ID=tu-account-id
CLOUDFLARE_AUTH_TOKEN=tu-token
CLOUDFLARE_GATEWAY_ID=openai-compat
CLOUDFLARE_MODEL=@cf/meta/llama-2-7b-chat-int8

# Selector de provider
LLM_PROVIDER=cloudflare
```

### 2. Endpoint OpenAI-Compatible

Cloudflare expone un gateway OpenAI-compatible en:

```
https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openai
```

Donde:
- `{account_id}`: Tu Account ID de Cloudflare
- `{gateway_id}`: ID del gateway (por defecto: `openai-compat`)

---

## 🔧 Cómo Funciona

### Internamente en el Código

```python
# src/autopoietic_orchestrator.py

if provider == "cloudflare":
    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    auth_token = os.getenv("CLOUDFLARE_AUTH_TOKEN")
    gateway_id = os.getenv("CLOUDFLARE_GATEWAY_ID", "openai-compat")
    
    llm_kwargs = {
        "base_url": f"https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openai",
        "api_key": auth_token,
        "model": os.getenv("CLOUDFLARE_MODEL", "@cf/meta/llama-2-7b-chat-int8"),
        "temperature": 0.2,
    }
    
    llm = ChatOpenAI(**llm_kwargs)
```

### Uso Normal

Una vez configurado, el sistema usa Cloudflare **exactamente igual** que OpenAI:

```python
from src.autopoietic_orchestrator import create_orchestrator

# Crear orquestador (detecta provider automáticamente)
orchestrator = create_orchestrator(llm_provider="cloudflare")

# Usar normalmente
result = orchestrator.invoke("Hola, ¿qué es Python?")
```

---

## 🎯 Modelos Disponibles en Cloudflare

| Modelo | ID | Uso |
|--------|-----|-----|
| **Llama 2 7B** | `@cf/meta/llama-2-7b-chat-int8` | Chat general (económico) |
| **Llama 2 13B** | `@cf/meta/llama-2-13b-chat-int8` | Chat avanzado |
| **Mistral 7B** | `@cf/mistral/mistral-7b-instruct-v0.1` | Instruct (preciso) |
| **CodeLlama 7B** | `@cf/meta/codellama-7b-instruct` | Código |
| **TinyLlama** | `@cf/tinyllama/tinyllama-1.1b-chat-v1.0` | Ultra rápido |

Actualiza `CLOUDFLARE_MODEL` en `.env` para cambiar de modelo.

---

## 🔍 Troubleshooting

### Error: "404 Not Found"

**Causa**: El gateway_id no existe o no está configurado correctamente.

**Solución**:
1. Ve a Cloudflare Dashboard → AI Gateway
2. Crea un nuevo gateway con nombre "openai-compat"
3. O usa el ID del gateway que ya tienes

### Error: "401 Unauthorized"

**Causa**: Token incorrecto o sin permisos.

**Solución**:
1. Ve a: https://dash.cloudflare.com/profile/api-tokens
2. Crea token con permisos: `AI Gateway: Edit`
3. Actualiza `CLOUDFLARE_AUTH_TOKEN` en `.env`

### Error: "Model not found"

**Causa**: El modelo especificado no existe en Cloudflare.

**Solución**:
- Usa formato completo: `@cf/meta/llama-2-7b-chat-int8`
- Verifica modelos disponibles en: https://developers.cloudflare.com/workers-ai/models/

### El sistema es lento o timeouts

**Causa**: Cold starts de Cloudflare Workers.

**Solución**:
- Primera llamada puede tardar ~5-10s (cold start)
- Llamadas subsecuentes son rápidas (<1s)
- Usa modelos más pequeños (tinyllama) para desarrollo

---

## 💰 Costos

Cloudflare Workers AI tiene pricing extremadamente económico:

- **Free Tier**: 10,000 requests/día
- **Paid**: ~$0.00001 por 1K tokens (500x más barato que GPT-4)

Comparación:
- OpenAI GPT-4: ~$0.05/request
- Cloudflare Llama-2: ~$0.0001/request
- **Ahorro**: ~500x

---

## 🚀 Próximos Pasos

1. **Prueba el sistema**:
   ```bash
   python main.py
   ```

2. **Experimenta con modelos**:
   - Cambia `CLOUDFLARE_MODEL` en `.env`
   - Reinicia `main.py`

3. **Monitorea uso**:
   - Dashboard de Cloudflare muestra requests y latencia
   - https://dash.cloudflare.com/ai-gateway

---

## 📚 Referencias

- **Cloudflare AI Gateway**: https://developers.cloudflare.com/ai-gateway/
- **Workers AI Models**: https://developers.cloudflare.com/workers-ai/models/
- **OpenAI Compatibility**: https://developers.cloudflare.com/ai-gateway/providers/openai/

---

**Resumen**: Ahora usamos el endpoint OpenAI-compatible de Cloudflare, que es más simple, más robusto y 100% compatible con LangChain. No más clientes personalizados. 🎉
