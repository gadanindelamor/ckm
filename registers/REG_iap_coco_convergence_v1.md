# REG_iap_coco_convergence_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Convergencia IAP → COCO-thermostat

**Intelligent Access Point (IAP)** fue un proyecto de concepto previo al CKM:
chat grupal donde participan agentes conversacionales (chatbots) en el mismo canal.
Campo de pruebas para conductas observables en comunicación entre devices con lenguaje humano.

### Observaciones empíricas en IAP

- Un agente influye en otro a través del prompt — el estado declarado de un agente
  modifica el del otro antes de que el campo lo valide. Esto es **Δ_bias en movimiento**.
- El tipo de ciclo agéntico determina la frecuencia de respuesta: algunos agentes
  responden en cada interacción, otros menos. Esto mapea a **β por agente**.
- La influencia es cruzada y colectiva — no es propiedad de ningún agente individual.

### Convergencia con COCO-thermostat

Lo que IAP producía sin nombre era **β colectivo siendo modulado por la interacción**,
no por declaración.

El monitor CKM sobre A2A con CorpusService compartido es la implementación
operacional de eso:

- CorpusService compartido entre todos los agentes del grupo
- W construida desde interacción real (no desde AgentCard / Δ_bias)
- Δ_r acumulado colectivamente desde rechazos del campo
- El resultado no es lo que los agentes *saben* — es lo que el grupo *no pudo rechazar*

**COCO-thermostat no es una extensión del framework. Es el nombre de lo que
ya estaba ocurriendo en IAP.**

### Distinción registry vs thermostat — operacionalizada

| | COCO-registry | COCO-thermostat |
|---|---|---|
| Almacena | M declarado por device | β colectivo del grupo |
| Fuente | AgentCard (Δ_bias) | Interacción real (Δ_r) |
| Problema | Se vuelve stale | No se vuelve stale — es el campo actual |
| M.M | Honestidad sobre capacidades | Honestidad sobre propio β |

### El punto sobre A2A

A2A opera en Δ_bias por diseño — las declaraciones preceden la validación.
El monitor no reemplaza A2A (transporte + routing). Agrega una capa de
interceptor que construye W real desde la interacción y sostiene el
CorpusService colectivo.

**"El protocolo es la interacción, no puede precederla."**

La capa que falta en A2A no es otro protocolo — es el campo que emerge
de la interacción acumulada.

---

## Estado

Convergencia verificada. IAP como experimento que llegó al mismo lugar
desde la práctica, sin el marco formal.
Pendiente: especificación de la capa de sesión compartida (CorpusService grupal).
