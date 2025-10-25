# Sistema Autopoiético de Agentes de IA

Sistema de orquestación de agentes basado en principios autopoiéticos (Maturana & Varela), implementado con **LangChain** y **LangGraph**.

## 🎯 Características Principales

- **Meta-Agente Orquestador**: Router inteligente que evalúa tareas y determina el flujo de ejecución
- **Metaproducción**: Capacidad del sistema para proponer y crear nuevos agentes especializados
- **Circularidad Productiva**: Mantiene la viabilidad del sistema mediante ciclos de producción-mantenimiento-reparación
- **Invariantes del Sistema**: Políticas de seguridad, calidad y trazabilidad que preservan la identidad organizacional
- **LangGraph**: Orquestación con grafo de estados, flujo condicional y persistencia

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO                              │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              META-AGENTE ROUTER                         │
│  (Evalúa complejidad y enruta tareas)                   │
└─────────┬───────────────────────┬───────────────────────┘
          │                       │
          ▼                       ▼
┌──────────────────┐    ┌──────────────────────────────┐
│ EJECUCION_DIRECTA│    │ DIAGNOSTICO_ESTRUCTURAL      │
│                  │    │                              │
│ Usa agentes      │    │ Propone nuevos agentes       │
│ existentes del   │    │ (Metaproducción)             │
│ catálogo         │    │                              │
└──────────────────┘    └──────────────────────────────┘
          │                       │
          └───────────┬───────────┘
                      ▼
              ┌───────────────┐
              │   RESPUESTA   │
              └───────────────┘
```

### Componentes Clave

1. **`orchestrator_state.py`**: Define el estado tipado del grafo y los invariantes del sistema
2. **`agent_repository.py`**: Repositorio organizacional de especificaciones de agentes
3. **`meta_agent_router.py`**: Meta-agente que evalúa y enruta tareas
4. **`execution_nodes.py`**: Nodos de ejecución (directa y diagnóstico estructural)
5. **`autopoietic_orchestrator.py`**: Orquestador principal con grafo de LangGraph

## 📋 Requisitos

- Python 3.13+
- LangChain 0.1.0+
- LangGraph 0.0.20+
- OpenAI API Key (o LM Studio local)

## 🚀 Instalación

1. **Clonar el repositorio**:
```bash
cd Repohackaton
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -e .
```

4. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env con tu API key
```

## 💻 Uso

### Modo Interactivo

```bash
python main.py
```

El sistema mostrará el catálogo de agentes disponibles y entrará en modo interactivo donde puedes escribir tus tareas.

### Ejemplos de Tareas

**Tarea Simple (Ejecución Directa)**:
```
👤 Usuario: ¿Cuál es la capital de Francia?
```

**Tarea con Agente Especializado**:
```
👤 Usuario: Quiero organizar un viaje de windsurf. ¿Qué condiciones meteorológicas necesito?
```

**Tarea Compleja (Requiere Metaproducción)**:
```
👤 Usuario: Necesito analizar datos de sensores IoT en tiempo real y predecir fallos en maquinaria industrial
```

### Uso Programático

```python
from src.autopoietic_orchestrator import create_orchestrator

# Crear orquestador
orchestrator = create_orchestrator(
    model_name="gpt-4",
    api_key="your-api-key"
)

# Procesar tarea
result = orchestrator.invoke("Tu tarea aquí")

# Ver resultado
print(result["messages"][-1]["content"])
```

## 🔧 Configuración con LM Studio (Local)

Si prefieres usar un modelo local con LM Studio:

1. Inicia LM Studio y carga un modelo (ej: `qwen2.5-coder-14b-instruct`)
2. Activa el servidor local en el puerto 1234
3. En `main.py`, usa:

```python
orchestrator = create_orchestrator(
    model_name="qwen2.5-coder-14b-instruct",
    base_url="http://localhost:1234/v1",
    api_key="sk-no-key"
)
```

## 📚 Conceptos de Autopoiesis

### Organización vs. Estructura

- **Organización**: Patrones de relaciones invariantes (políticas, seguridad, calidad)
- **Estructura**: Componentes concretos que pueden cambiar (agentes, prompts, herramientas)

### Ciclo Autopoiético

1. **Sensing**: Recolecta KPIs y detecta anomalías
2. **Homeostasis**: Ajusta estructura para mantener viabilidad
3. **Diagnóstico**: Identifica brechas de capacidades
4. **Metaproducción**: Propone y crea nuevos agentes
5. **Ensayo**: Valida en sandbox
6. **Asimilación**: Integra al catálogo

### Invariantes del Sistema

El sistema mantiene estos contratos no negociables:

- **Seguridad**: No ejecutar código fuera del sandbox
- **Trazabilidad**: Registrar todas las decisiones
- **Calidad Mínima**: Accuracy ≥ 85%, hallucination ≤ 5%
- **Presupuestos**: Latencia ≤ 5s, costo ≤ $0.10/request

## 🧪 Catálogo de Agentes Predeterminado

- **`general_assistant`**: Asistente general para tareas rutinarias
- **`code_analyst`**: Especialista en análisis de código
- **`windsurf_planner`**: Planificador de viajes de windsurf

## 🛠️ Desarrollo

### Añadir un Nuevo Agente

```python
from src.orchestrator_state import AgentSpec

nuevo_agente = AgentSpec(
    agent_id="mi_agente",
    role="Descripción del rol",
    capabilities=["cap1", "cap2"],
    tools=["tool1", "tool2"],
    system_prompt="Prompt de sistema detallado...",
    version="1.0.0",
    active=True
)

orchestrator.add_agent_to_catalog(nuevo_agente.dict())
```

### Estructura del Proyecto

```
Repohackaton/
├── src/
│   ├── orchestrator_state.py      # Estado y tipos
│   ├── agent_repository.py        # Repositorio de agentes
│   ├── meta_agent_router.py       # Meta-agente router
│   ├── execution_nodes.py         # Nodos de ejecución
│   └── autopoietic_orchestrator.py # Orquestador principal
├── main.py                        # Aplicación principal
├── pyproject.toml                 # Dependencias
├── .env.example                   # Variables de entorno
└── README.md                      # Esta documentación
```

## 📖 Referencias Conceptuales

- Maturana, H. & Varela, F. — *Autopoiesis and Cognition*
- LangChain Documentation: https://python.langchain.com/
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/

## 📄 Licencia

Este proyecto es parte de un hackathon educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:

1. Respetar los invariantes del sistema
2. Documentar nuevos agentes y capacidades
3. Mantener la composición sobre herencia
4. Añadir tests para nuevas funcionalidades

---

**Desarrollado con principios autopoiéticos** 🔄
