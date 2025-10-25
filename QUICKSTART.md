# 🚀 Guía de Inicio Rápido

## Sistema Autopoiético de Agentes - Meta-Agente Orquestador

Esta guía te ayudará a poner en marcha el sistema en **5 minutos**.

---

## ⚡ Instalación Rápida

```bash
# 1. Navegar al directorio
cd Repohackaton

# 2. Crear entorno virtual (Windows)
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -e .

# 4. Configurar API Key
copy .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

---

## 🎯 Primer Uso

### Opción 1: Modo Interactivo

```bash
python main.py
```

Verás algo como:

```
================================================================================
SISTEMA AUTOPOIÉTICO DE AGENTES DE IA
Meta-Agente Orquestador con LangGraph
================================================================================

📋 CATÁLOGO DE AGENTES DISPONIBLES:
--------------------------------------------------------------------------------
✅ general_assistant
   Rol: Asistente general
   Capacidades: conversation, information_retrieval, task_planning

✅ code_analyst
   Rol: Analista de código
   Capacidades: code_review, bug_detection, optimization_suggestions

✅ windsurf_planner
   Rol: Planificador de windsurf
   Capacidades: weather_analysis, location_recommendation, equipment_advice

💬 MODO INTERACTIVO
Escribe tu tarea o pregunta (o 'salir' para terminar)
--------------------------------------------------------------------------------

👤 Usuario: _
```

### Opción 2: Uso Programático

```python
import sys
sys.path.insert(0, "src")

from autopoietic_orchestrator import create_orchestrator
import os

# Crear orquestador
orchestrator = create_orchestrator(
    model_name="gpt-4",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Ejecutar tarea
result = orchestrator.invoke("¿Qué es la autopoiesis?")

# Ver respuesta
print(result["messages"][-1]["content"])
```

---

## 📝 Ejemplos de Tareas

### 1. Tarea Simple (Ejecución Directa)

```
👤 Usuario: ¿Cuál es la capital de España?

📊 Ruta elegida: EJECUCION_DIRECTA
📈 Complejidad de tarea: 0.10
```

### 2. Tarea con Agente Especializado

```
👤 Usuario: Quiero hacer windsurf este fin de semana. ¿Qué condiciones necesito?

📊 Ruta elegida: EJECUCION_DIRECTA
📈 Complejidad de tarea: 0.50

[Agente: windsurf_planner]
Para windsurf necesitas...
```

### 3. Tarea que Requiere Metaproducción

```
👤 Usuario: Necesito analizar datos de sensores IoT en tiempo real

📊 Ruta elegida: DIAGNOSTICO_ESTRUCTURAL
📈 Complejidad de tarea: 0.85

## Diagnóstico Estructural

**Brecha de Capacidades Identificada:**
...

**Propuesta de Nuevo Agente:**
- ID: iot_analyst
- Rol: Analista de sensores IoT
...
```

---

## 🔧 Configuración Alternativa (LM Studio Local)

Si prefieres usar un modelo local sin API key:

1. **Instala LM Studio**: https://lmstudio.ai/

2. **Carga un modelo** (ej: `qwen2.5-coder-14b-instruct`)

3. **Inicia el servidor local** en puerto 1234

4. **Modifica `main.py`** (líneas 37-40):

```python
# Comentar la configuración de OpenAI
# orchestrator = create_orchestrator(
#     model_name=os.getenv("OPENAI_MODEL", "gpt-4"),
#     api_key=os.getenv("OPENAI_API_KEY"),
# )

# Descomentar la configuración de LM Studio
orchestrator = create_orchestrator(
    model_name="qwen2.5-coder-14b-instruct",
    base_url="http://localhost:1234/v1",
    api_key="sk-no-key"
)
```

5. **Ejecuta**: `python main.py`

---

## 📊 Entender el Flujo

```
Usuario → Meta-Agente Router → Evaluación
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
         EJECUCION_DIRECTA              DIAGNOSTICO_ESTRUCTURAL
         (Agente existente)             (Propone nuevo agente)
                    ↓                               ↓
                    └───────────────┬───────────────┘
                                    ↓
                                Respuesta
```

**El router decide:**
- **EJECUCION_DIRECTA**: Si hay un agente adecuado en el catálogo
- **DIAGNOSTICO_ESTRUCTURAL**: Si se necesita crear un nuevo agente

---

## 🎓 Conceptos Clave

### Organización vs. Estructura

- **Organización** = Reglas invariantes (seguridad, calidad)
- **Estructura** = Agentes concretos (pueden cambiar)

### Metaproducción

El sistema puede **crear sus propios agentes** cuando detecta brechas de capacidades.

### Circularidad Productiva

El sistema se **auto-mantiene** mediante ciclos de:
1. Producción (ejecutar tareas)
2. Mantenimiento (monitorear KPIs)
3. Reparación (ajustar agentes)
4. Reproducción (crear nuevos agentes)

---

## 🆘 Solución de Problemas

### Error: "No API Key"

```bash
# Asegúrate de tener .env configurado:
echo OPENAI_API_KEY=sk-... > .env
```

### Error: ImportError

```bash
# Reinstala dependencias:
pip install -e .
```

### El sistema no responde

- Verifica tu conexión a internet (si usas OpenAI)
- Verifica que LM Studio esté corriendo (si usas local)
- Revisa los logs en la consola

---

## 📚 Siguiente Paso

Explora los **ejemplos avanzados**:

```bash
python examples/basic_usage.py
```

Lee la **documentación completa**: `README.md`

---

## 💡 Tips

1. **Comienza con tareas simples** para familiarizarte con el sistema
2. **Observa las métricas de complejidad** para entender el routing
3. **Prueba diferentes tipos de tareas** para ver cómo el sistema se adapta
4. **Añade tus propios agentes** cuando encuentres brechas específicas

---

**¿Listo para comenzar?** 🚀

```bash
python main.py
```
