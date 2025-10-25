# 🔄 DIAGRAMA DE FLUJO DEL SISTEMA AUTOPOIÉTICO

## Flujo Completo de Procesamiento de Tareas

---

## 📊 VISIÓN GENERAL

```
┌────────────────────────────────────────────────────────────────────┐
│                         USUARIO                                     │
│                    "Organizar viaje windsurf"                       │
└─────────────────────────┬──────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ENTRADA AL SISTEMA                                │
│  OrchestratorState = {                                               │
│    messages: [HumanMessage("Organizar viaje windsurf")],            │
│    route: None,                                                      │
│    task_complexity: None,                                            │
│    agent_catalog: None                                               │
│  }                                                                   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│              🤖 META-AGENTE ROUTER (Nodo 1)                          │
│                                                                      │
│  1️⃣  Obtiene catálogo de agentes disponibles                        │
│  2️⃣  Analiza la tarea del usuario                                   │
│  3️⃣  Evalúa complejidad (0.0 - 1.0)                                 │
│  4️⃣  Compara con capacidades del catálogo                           │
│  5️⃣  Genera RouterDecision estructurada                             │
│                                                                      │
│  Output: {                                                           │
│    route: "EJECUCION_DIRECTA" o "DIAGNOSTICO_ESTRUCTURAL",         │
│    reasoning: "...",                                                 │
│    task_complexity: 0.5,                                             │
│    requires_new_agent: False                                         │
│  }                                                                   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   DECISIÓN CONDICIONAL                               │
│                   ¿Qué ruta tomar?                                   │
└──────────┬────────────────────────────────────────┬─────────────────┘
           │                                        │
           │ route == "EJECUCION_DIRECTA"          │ route == "DIAGNOSTICO_ESTRUCTURAL"
           │                                        │
           ▼                                        ▼
┌──────────────────────────┐            ┌──────────────────────────────┐
│   📦 EJECUCION_DIRECTA   │            │  🔬 DIAGNOSTICO_ESTRUCTURAL  │
│      (Nodo 2a)           │            │        (Nodo 2b)             │
│                          │            │                              │
│ 1️⃣  Selecciona agente    │            │ 1️⃣  Analiza brecha           │
│    apropiado del        │            │    de capacidades            │
│    catálogo              │            │                              │
│                          │            │ 2️⃣  Genera propuesta de      │
│ 2️⃣  Usa system_prompt    │            │    nuevo agente              │
│    del agente            │            │    (Metaproducción)          │
│                          │            │                              │
│ 3️⃣  Ejecuta con LLM      │            │ 3️⃣  Proporciona respuesta    │
│                          │            │    provisional con           │
│ 4️⃣  Retorna respuesta    │            │    agente general            │
│                          │            │                              │
│ Agente usado:            │            │ Propuesta:                   │
│ - windsurf_planner       │            │ - Nuevo AgentSpec            │
│ - code_analyst           │            │ - Capacidades requeridas     │
│ - general_assistant      │            │ - Herramientas necesarias    │
└──────────┬───────────────┘            └──────────┬───────────────────┘
           │                                        │
           │                                        │
           └────────────────┬───────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    SALIDA DEL SISTEMA                                │
│  OrchestratorState actualizado = {                                   │
│    messages: [                                                       │
│      HumanMessage("Organizar viaje windsurf"),                      │
│      AIMessage("[Agente: windsurf_planner]\n\nPara tu viaje...")    │
│    ],                                                                │
│    route: "END",                                                     │
│    task_complexity: 0.5                                              │
│  }                                                                   │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         USUARIO                                      │
│                  Recibe respuesta final                              │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 EJEMPLO 1: Tarea Simple

### Input
```
"¿Cuál es la capital de Francia?"
```

### Flujo

```
Usuario
  ↓
Router evalúa:
  - Complejidad: 0.1 (muy simple)
  - Agente disponible: general_assistant ✅
  - Decisión: EJECUCION_DIRECTA
  ↓
DirectExecutionNode:
  - Selecciona: general_assistant
  - Ejecuta con prompt general
  ↓
Respuesta: "La capital de Francia es París."
```

**Duración**: ~2-3 segundos  
**Agente**: general_assistant  
**Ruta**: EJECUCION_DIRECTA

---

## 🏄 EJEMPLO 2: Tarea Especializada (Windsurf)

### Input
```
"Quiero hacer windsurf este fin de semana. 
¿Qué condiciones necesito?"
```

### Flujo

```
Usuario
  ↓
Router evalúa:
  - Complejidad: 0.5 (media)
  - Keywords detectadas: "windsurf"
  - Agente disponible: windsurf_planner ✅
  - Decisión: EJECUCION_DIRECTA
  ↓
DirectExecutionNode:
  - Selecciona: windsurf_planner
  - System prompt especializado en windsurf
  - Acceso a herramientas: weather_api, location_db
  ↓
Respuesta:
  "[Agente: windsurf_planner]
  
  Para windsurf este fin de semana necesitas:
  
  **Condiciones Meteorológicas:**
  - Viento: 15-25 nudos (ideal)
  - Dirección: Cross-shore preferible
  - Temperatura: 18-25°C
  
  **Equipo:**
  - Tabla: 120-140L según tu peso
  - Vela: 5.0-6.5m² según viento
  - Arnés y traje de neopreno
  
  ..."
```

**Duración**: ~3-5 segundos  
**Agente**: windsurf_planner  
**Ruta**: EJECUCION_DIRECTA

---

## 🔬 EJEMPLO 3: Tarea Compleja (Metaproducción)

### Input
```
"Necesito un sistema que analice sensores IoT 
en tiempo real y prediga fallos en maquinaria"
```

### Flujo

```
Usuario
  ↓
Router evalúa:
  - Complejidad: 0.85 (muy compleja)
  - Capacidades requeridas: IoT, ML, tiempo real
  - Catálogo actual: general, code, windsurf
  - NO hay agente con capacidades IoT ❌
  - Decisión: DIAGNOSTICO_ESTRUCTURAL
  ↓
StructuralDiagnosisNode:
  │
  ├─ 1. Analiza brecha de capacidades
  │    ▼
  │    "Se requiere: análisis IoT, ML predictivo,
  │     detección de anomalías en tiempo real.
  │     Disponible: Ninguna capacidad de IoT."
  │
  ├─ 2. Genera propuesta de nuevo agente
  │    ▼
  │    AgentSpec {
  │      agent_id: "iot_predictive_analyst",
  │      role: "Analista predictivo de IoT",
  │      capabilities: [
  │        "real_time_sensor_analysis",
  │        "anomaly_detection",
  │        "predictive_maintenance",
  │        "ml_pipeline_integration"
  │      ],
  │      tools: [
  │        "sensor_db",
  │        "ml_model_api",
  │        "alert_system"
  │      ],
  │      system_prompt: "Eres un especialista..."
  │    }
  │
  └─ 3. Proporciona respuesta provisional
       ▼
       Usa general_assistant mientras se diseña
       el agente especializado
  ↓
Respuesta:
  "## Diagnóstico Estructural
  
  **Brecha de Capacidades Identificada:**
  El catálogo actual no tiene agentes con capacidades
  de análisis de sensores IoT, ML en tiempo real, ni
  mantenimiento predictivo.
  
  **Propuesta de Nuevo Agente:**
  - ID: iot_predictive_analyst
  - Rol: Analista predictivo de IoT
  - Capacidades: real_time_analysis, ML, anomaly_detection
  
  **Siguiente Paso:**
  Este agente requiere:
  1. Ensayo en sandbox con datos de sensores
  2. Evaluación de precisión y latencia
  3. Aprobación por MA-Asimilador
  4. Integración al catálogo
  
  ---
  
  **Respuesta Provisional:**
  [Usando general_assistant]
  
  Para analizar sensores IoT en tiempo real necesitarías:
  - Sistema de ingesta de datos (MQTT/Kafka)
  - Pipeline de ML (TensorFlow/PyTorch)
  - Base de datos temporal (InfluxDB)
  ..."
```

**Duración**: ~5-8 segundos  
**Agente**: N/A (propone nuevo agente)  
**Ruta**: DIAGNOSTICO_ESTRUCTURAL

---

## 🔄 CIRCULARIDAD PRODUCTIVA

```
┌────────────────────────────────────────────────────────────┐
│                    CICLO AUTOPOIÉTICO                       │
└────────────────────────────────────────────────────────────┘

    1. PRODUCCIÓN                2. MANTENIMIENTO
    ↓                            ↓
 Ejecutar tareas         →    Monitorear KPIs
 con agentes                  (latencia, accuracy,
 existentes                   costo, errores)
    ↓                            ↓
    │                            │
    │                         ¿KPIs ok?
    │                            │
    │                         No ↓
    │                            
    └──────────────┐         3. REPARACIÓN
                   │         ↓
                   │    Ajustar prompts,
                   │    re-entrenar,
                   │    optimizar
                   │         ↓
                   │         │
                   │      ¿Reparable?
                   │         │
                   │      No ↓
                   │         
                   └──→  4. REPRODUCCIÓN
                         (METAPRODUCCIÓN)
                         ↓
                      Diseñar nuevo
                      agente → Ensayar
                      → Evaluar → Asimilar
                         ↓
                      Catálogo
                      actualizado
                         ↓
                    ← ─ ─ ┘
                    Volver a 1
```

---

## 🧬 ORGANIZACIÓN vs ESTRUCTURA

```
┌─────────────────────────────────────────────────────────────┐
│                  ORGANIZACIÓN (Invariante)                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • Seguridad: No ejecución fuera de sandbox          │   │
│  │  • Calidad: Accuracy ≥ 85%                           │   │
│  │  • Presupuestos: Latencia ≤ 5s, Costo ≤ $0.10       │   │
│  │  • Trazabilidad: Log de todas las decisiones         │   │
│  └──────────────────────────────────────────────────────┘   │
│                           ↑                                  │
│                           │                                  │
│                      PRESERVA                                │
│                           │                                  │
│                           ↓                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           ESTRUCTURA (Mutable)                        │   │
│  │                                                       │   │
│  │  Catálogo de Agentes:                                │   │
│  │  ├─ general_assistant                                │   │
│  │  ├─ code_analyst                                     │   │
│  │  ├─ windsurf_planner                                 │   │
│  │  └─ [nuevos agentes pueden añadirse]                 │   │
│  │                                                       │   │
│  │  Prompts: [pueden modificarse]                       │   │
│  │  Herramientas: [pueden añadirse/quitarse]            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

La ORGANIZACIÓN se mantiene constante mientras
la ESTRUCTURA se adapta a las perturbaciones externas
```

---

## 🎛️ CONTROL DE VIABILIDAD

```
┌──────────────────────────────────────────────────────────┐
│              NÚCLEO DE VIABILIDAD (K)                     │
│                                                           │
│  ┌────────────────────────────────────────────────┐      │
│  │  Accuracy      ████████████████░░  85%  ✅     │      │
│  │  Latency       ██████████████░░░░  3.2s ✅     │      │
│  │  Cost          ████████████░░░░░░  $0.07 ✅    │      │
│  │  Error Rate    ████░░░░░░░░░░░░░░  4%   ✅     │      │
│  └────────────────────────────────────────────────┘      │
│                                                           │
│  Estado: 🟢 VIABLE                                        │
│                                                           │
│  Si alguna métrica sale del núcleo K:                    │
│  → Activar homeostasis (ajuste automático)               │
│  → O iniciar metaproducción (nuevo agente)               │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 PERSISTENCIA Y CHECKPOINTING

```
Usuario → Tarea 1 → Router → Ejecución → Respuesta 1
                                              ↓
                                         CHECKPOINT
                                    (guarda estado en disco)
                                              ↓
Usuario → Tarea 2 → [recupera estado] → Router → ...
          (mismo thread_id)

Esto permite:
✅ Conversaciones multi-turno
✅ Recuperación después de errores
✅ Historial persistente
✅ Context awareness
```

---

## 🎯 RESUMEN VISUAL

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT                                 │
│              "Organizar windsurf"                        │
└────────────────────┬────────────────────────────────────┘
                     ↓
              ┌──────────────┐
              │   🤖 ROUTER  │  ← Cerebro del sistema
              │   (Meta-Ag)  │
              └──────┬───────┘
                     │
        ┌────────────┴────────────┐
        ↓                         ↓
    ┌────────┐              ┌──────────┐
    │ SIMPLE │              │ COMPLEJA │
    │ (0.5)  │              │  (0.85)  │
    └───┬────┘              └────┬─────┘
        ↓                        ↓
    ┌──────────┐          ┌──────────────┐
    │ Agente   │          │ Propone      │
    │ Existente│          │ Nuevo Agente │
    └────┬─────┘          └──────┬───────┘
         ↓                       ↓
    ┌─────────────────────────────────┐
    │         RESPUESTA                │
    └─────────────────────────────────┘
```

---

**Este diagrama representa el flujo completo del sistema autopoiético** 🔄

Para ejecutar el sistema y ver estos flujos en acción:
```bash
python main.py
```
