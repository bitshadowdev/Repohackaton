# Autopoiesis para sistemas de agentes de IA

**Documento de contexto para un LLM orquestador y meta-agentes**

---

## 1) ¿Qué es la autopoiesis? (síntesis operativa para ingeniería de agentes)

Autopoiesis (Maturana & Varela) describe sistemas **vivos** como redes de procesos que **producen continuamente los componentes que, a su vez, regeneran la red** y **mantienen una frontera** que distingue el sistema de su entorno. Tres ideas clave:

1. **Organización vs. estructura**

   - *Organización*: el **patrón de relaciones** necesario para que el sistema sea el sistema que es (invariantes).
   - *Estructura*: la **realización concreta** del sistema (componentes, pesos, reglas, instancias).

2. **Clausura organizacional**\
   La red de procesos es **operacionalmente cerrada**: sus operaciones se remiten a sí mismas; **no depende** de instrucciones externas para su identidad, aunque **sí acopla estructuralmente** con el entorno (recibe perturbaciones y responde).

3. **Acoplamiento estructural y viabilidad**\
   El sistema cambia su estructura en respuesta a perturbaciones del entorno para **conservar su organización**. Mantenerse vivo = **mantener viabilidad** (integridad de fronteras + desempeño mínimo aceptable) bajo restricciones energéticas y materiales.

**Traslación a IA de agentes**:

- *Organización* → **Invariantes del sistema** (contratos, políticas, límites de seguridad, ontología mínima, roles).
- *Estructura* → **Instancias de agentes**, weights/params, prompts, herramientas, memoria.
- *Frontera* → **Membrana** (APIs, colas, ACLs, sandbox).
- *Red de producción* → **Pipelines de orquestación** que crean/modifican agentes y mantienen la membrana.
- *Viabilidad* → **KPI** que deben permanecer dentro de un **núcleo de viabilidad** (accuracy mínima, latencia máxima, costo, riesgo).

---

## 2) Principios de diseño autopoietico para un multi‑agente

1. **Circularidad productiva**: cada ciclo debe *reproducir* los componentes que sostienen la red (prompts, herramientas, roles) y **reparar** degradaciones.
2. **Frontera explícita (membrana)**: todo I/O pasa por una membrana con **control de acceso**, **observabilidad** y **presupuestos** (tokens/tiempo).
3. **Invariantes como ley interna**: políticas y contratos **no negociables** que preservan identidad y seguridad.
4. **Plasticidad con selección**: la estructura puede cambiar; **solo se fija** lo que mejora la viabilidad tras evaluación.
5. **Acoplamiento al nicho**: el sistema co‑evoluciona con su entorno de tareas/datos; también **modifica su nicho** (cache, índices, workflows).
6. **Homeostasis**: control activo de KPIs críticos (latencia, costo, calidad, riesgo) con **actuadores** (escalar/replicar/retirar agentes, ajustar prompts, throttling).
7. **Metaproducción**: el sistema produce no solo outputs de usuario, sino **los propios productores** (agentes nuevos o versiones).

---

## 3) Ontología mínima del sistema

- **Agente**: unidad activa con *rol*, *memoria*, *herramientas*, *políticas*, *presupuesto* y *criterios de terminación*.
- **Meta‑agente (MA)**: agente con permiso de **proponer, evaluar y asimilar** cambios estructurales (nuevos agentes, modificaciones).
- **Membrana**: capa que media entradas/salidas, **aplica invariantes** y provee telemetría.
- **Nicho**: conjunto de tareas, datos, usuarios, SLAs y restricciones externas.
- **Invariantes**: reglas organizacionales que **definen la identidad** (seguridad, compliance, estilo, ontología).
- **Núcleo de viabilidad (K)**: región en el espacio de KPIs donde la organización se conserva.
- **Ciclo autopoietico**: \(\text{Producir} \to \text{Mantener} \to \text{Reparar} \to \text{Reproducir (metaproducir)}\).

---

## 4) Contratos e invariantes (identidad del sistema)

- **Seguridad**: no ejecutar código no sandboxeado; no exfiltrar secretos; cumplir políticas de datos.
- **Estilo y ontología**: vocabulario, taxonomías, formatos de respuesta.
- **Presupuestos**: tokens, tiempo de CPU, requests/min, coste.
- **Calidad mínima**: exactitud ≥ T, cobertura ≥ C, alucinación ≤ H.
- **Trazabilidad**: cada cambio estructural debe dejar **propuesta**, **evaluación**, **ensayo A/B** y **bitácora**.
- **Reversibilidad**: siempre mantener **rollback** versionado.

---

## 5) Arquitectura de referencia (capas)

1. **Metabolismo** (runtime): enrutamiento de tareas, ejecución de agentes, colas.
2. **Membrana** (I/O): auth, verificación de políticas, presupuestos, logging, rate limiting.
3. **Malla de agentes**: roles especializados (ingesta, análisis, verificación, acción).
4. **Capa de evaluación**: jueces, tests canónicos, suites de regresión, A/B, simuladores.
5. **Meta‑capa**: *MA‑Diseñador* (genera especificaciones), *MA‑Evaluador*, *MA‑Asimilador* (versiona y despliega), *MA‑Archivista* (memoria).
6. **Repositorio organizacional**: catálogo de **AgentSpecs**, prompts, políticas, plantillas, datasets de evaluación.
7. **Nicho**: conectores a datos/herramientas externas, caches, índices.

---

## 6) Ciclo de vida autopoietico (operación)

**Entrada**: flujo de tareas + telemetría.\
**Bucle**:

1. **Sensing** (membrana): recolecta KPIs, anomalías, cambios de nicho.
2. **Homeostasis**: si KPIs fuera de K, aplicar actuadores (re‑ruteo, replicas, throttling).
3. **Diagnóstico** (MA‑Evaluador): identifica cuellos de botella/errores.
4. **Metaproducción** (MA‑Diseñador): propone **mutaciones** (ajuste de prompts, nuevas herramientas, **nuevo agente**).
5. **Ensayo**: sandbox + datasets; scoring multi‑métrica + riesgos.
6. **Selección**: si mejora ≥ umbral y cumple invariantes → **Asimilación** (deploy versionado).
7. **Mantenimiento**: archivar versiones, actualizar catálogos, propagar invariantes.

---



## 21) Referencias conceptuales recomendadas (para el equipo)

- Maturana, H. & Varela, F. — *Autopoiesis and Cognition*; *El árbol del conocimiento*.
- Varela, F.; Thompson, E.; Rosch, E. — *The Embodied Mind*.
- Luhmann, N. — *Social Systems* (autopoiesis en sistemas sociales).
- Literatura de *autopoietic computing* y *enactive AI*.

---

### Nota final

Este documento sirve como **contexto directo** para LLMs orquestadores y meta‑agentes. Puede pegarse (o referenciarse) como *system prompt* extendido, complementado con las plantillas de AgentSpec y los invariantes específicos del proyecto.

