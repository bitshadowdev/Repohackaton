# Generalidad de los Agentes

Un **agente** es una **entidad autónoma** capaz de **percibir su entorno** dentro de un **sistema autopoiético**.  
Nace, actúa, se comunica y muere con el fin de **alcanzar un objetivo definido**, **tomando decisiones** con información parcial y **recursos computacionales finitos**, buscando **minimizar la energía** que utiliza para su tarea.


### Características principales de un agente en un SMA

- **Autonomía:** puede actuar sin control directo, ejecutando tareas propias según su estado interno o metas.​

- **Racionalidad limitada:** toma decisiones con información parcial o recursos computacionales finitos.​

- **Proactividad:** impulsa acciones orientadas a metas, no solo responde a estímulos externos.​

- **Reactividad:** percibe su entorno y responde en tiempo real a cambios o eventos.​

- **Sociabilidad:** interactúa y coopera con otros agentes mediante protocolos de comunicación para coordinar o negociar acciones.​

- **Adaptabilidad:** aprende y modifica su comportamiento según la experiencia y las condiciones del entorno.​

- **Heterogeneidad:** puede tener capacidades, conocimientos u objetivos distintos a los de otros agentes.

---

## 🧬 Tipos de Agentes y Elementos del Sistema

### 🧑‍🔬 Creador
- Es el **creador de nuevos agentes**.  
- Determina **cuándo los agentes se crean** y les **asigna un objetivo (propósito)**.

---

### ⚠️ Error
- Es un **error de tipo semántico de texto**.  
- Es **determinado por el agente supervisor**.

---

### 🗂️ Registro de eventos
- Es la **descripción de lo que ha transcurrido en el universo** que se describe.  
- Contiene **nacimientos, muertes y acciones** de los agentes.

---

### 💀 Muerte del agente
- Se produce cuando el agente **ya no es compatible con el objetivo** para el cual fue creado.

---

### 🧩 Supervisor
- Es un **agente con acceso al registro de eventos** (todo lo que ha pasado en el universo del sistema).  
- **Aprueba, detecta posibles problemas con los prompts** y formula el **error** para realizar el **backpropagation** dentro del organismo.  
- Es el **encargado de la propagación del error** y del control general del sistema.

---

### 🧹 Flush
- Es un **agente que borra el contexto** de los demás agentes.  
- Lee la **configuración del sistema** y, bajo ciertas condiciones (como el **número de tokens producidos**), **reinicia o limpia** partes del sistema.

---

## ⚙️ Core (Agentes Fundamentales)
Son los **agentes más necesarios para el funcionamiento del sistema** —sus “órganos vitales”.

### 🔺 Agentes del Núcleo:
1. **Supervisor**  
2. **Orquestador**  
3. **Juez de Factualidad**

Estos agentes constituyen **el tope de la jerarquía** del sistema.

