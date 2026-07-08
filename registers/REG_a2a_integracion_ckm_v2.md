# REG_a2a_integracion_ckm_v2.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — v2: correcciones PEG incorporadas sobre v1*

---

## Origen

Sesión Jul 2026. Evaluación de ajustes y adaptaciones al protocolo A2A
para integración con CKM-IAP. Análisis de samples A2A (Gemini),
verificación contra spec A2A v1.0, investigación sobre transferencia
de conocimiento semántico, lectura de IAID.md + BEGAME.

Correcciones v2: PEG de gadanin.delamor sobre v1 (misma sesión).

---

## 1. Verificación A2A v1.0

Estructura correcta A2A v1.0:

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "SendMessage",
  "params": {
    "message": {
      "role": "ROLE_AGENT",
      "messageId": "uuid",
      "contextId": "ctx-uuid",
      "parts": [
        {"kind": "text", "text": "...contenido..."},
        {"kind": "data", "data": {"estado": "input-required", "motivo": "..."}}
      ]
    }
  }
}
```

Métodos A2A v1.0: SendMessage, GetTask, CancelTask, SendStreamingMessage.
Estados de tarea: submitted / working / input-required / completed / failed / rejected / canceled.
Parts: text / data / file.

**Los samples de Gemini no son A2A válidos.** Carecen de envelope
JSON-RPC 2.0, usan `text_content` en lugar de `parts[].text`,
no tienen `role`, colocan auth en el body.

**Consecuencia para mcp_adapter:** el campo de texto que va a
MonitorService es `parts[n].text` donde `kind == "text"`.
Los `data` parts son señales de lifecycle — no van a NodeExtractor.

---

## 2. contextId — tres capas de identidad A2A

A2A v1.0 separa tres identificadores:

- `contextId` — agrupa toda la sesión de tareas (múltiples turnos, múltiples tasks)
- `taskId` — unidad específica de trabajo ("submit order", "run query")
- `messageId` — turno único de comunicación

**Mapeo directo:** `contextId` → `ckm_session_id`

No hay que inventarlo. CKM lo hereda del protocolo.

**Lifecycle de sesión CKM:**
W es suelo permanente — no tiene fin natural.
Δ_r acumula por contextId. Si la sesión se retoma con el mismo contextId,
Δ_r puede continuar acumulando o limpiarse con STOP antes de retomar.
El par (W, Δ_r) en cualquier momento del contextId es la representación
completa del estado de esa interacción.

---

## 3. Supuestos críticos

### S1 — Chatrooms IAP multiparty (TALÓN DE AQUILES)

A2A es fundamentalmente bilateral cliente-servidor.
No existe sala con múltiples participantes concurrentes
como primitiva del protocolo. IAP construye esa capa
como hub-and-spoke con IAP como nodo central.
No es A2A nativo. No puede serlo.

Las secciones vacías (##Results, ##Debate) en IAID.md
esperaban las condiciones que no existían en 2024.

**CKM opera sobre A2A/MCP — no depende de ellos.**
mcp_adapter es la capa de aislamiento. CKM core (W, Δ, c(S), Hopfield)
no sabe qué protocolo está debajo. Si A2A cambia su API,
solo cambia el adapter. Si aparece un nuevo protocolo,
se escribe un nuevo adapter. CKM no toca ninguno de los dos.

**Abierto. No tangencial a IAP — es su condición de posibilidad.**

### S2 — NodeExtractor sobre texto A2A

CKM fue validado sobre corpora argumentativos ricos (5145 párrafos).
Los mensajes A2A operacionales son cortos y transaccionales.

**Parcialmente resuelto:** las trazas de ejecución en lenguaje
natural (CoT, ReAct, Graph-of-Trace) que los agentes exponen
para auditoría son texto rico. CKM opera sobre esas trazas,
no sobre los mensajes operacionales del envelope A2A.

Distinción: texto de negociación A2A (sparse) vs
trazas de auditoría en lenguaje natural (suficiente para W).

El umbral que cambiaría la estrategia: si los agentes migran
a comunicación completamente latente sin exposición de trazas
en lenguaje natural — NodeExtractor pierde superficie.
No es el escenario actual. Es el escenario que IAP debe anticipar.

### S3 — STOP (CORREGIDO en v2)

STOP opera sobre Δ_r dentro del stack CKM.
Los agentes A2A no saben que ocurrió — y por diseño no necesitan saberlo.

STOP no comunica a los agentes en el ecosistema.
Una señal que operara simultáneamente sobre los distintos agentes
sería un sistema separado de complejidad diferente —
no es IAP Highway Network.

Highway Network es un canal interno al stack CKM.
La ventana temporal de efectividad de STOP es sobre el estado
del campo CKM, no sobre el lifecycle A2A.

---

## 4. Estructura de integración

```
A2A envelope (JSON-RPC 2.0)
    contextId  ──────────────────────────→  ckm_session_id
    parts[n].text (kind="text")  ────────→  MonitorService.evaluate()
    parts[n].data (kind="data")  ────────→  IAP lifecycle
    task.status.state  ──────────────────→  trigger Firma_CKM
         │
         ↓
    mcp_adapter (separación envelope/texto)
         │
         ├──→  NodeExtractor ← sobre trazas, no sobre envelope
         ├──→  CorpusService (W compartido por contextId)
         ├──→  MonitorService (Δ_r acumulado por sesión)
         ├──→  COCOThermostat (beta_collective, temp_signal)
         └──→  Firma_CKM en lifecycle boundaries
```

Lifecycle boundaries para Firma_CKM:
- `task.status.state = "completed"`
- `task.status.state = "failed"` / `"rejected"`
- Transición `input-required → working`
  (momento donde el campo cambió de forma por intervención externa)

---

## 5. MUTATION pattern — DESCARTADO (v2)

`MUTATION_DIRECTIVE`, `CONTEXT_OVERRIDE`, `MUTATION_DISPATCH`
no existen en A2A v1.0 spec. Son vocabulario generado por Gemini
en los samples — no primitivas del protocolo ni patrones IAID.

Verificado contra spec oficial. Descartado.

En un ecosistema de devices bajo M.M., las declaraciones
performativas de autoridad sin traza estructural no tienen lugar
por diseño — no como restricción impuesta sino como consecuencia
del campo.

---

## 6. Origen de IAP — IAID.md y BEGAME (corregido v2)

IAID (2024) es un prototipo experimental. No un spec de producción.

Los devices participan en un Environment compartido
(más Minecraft que cliente-servidor).
Los devices nacen, se procrean, se clonan y mueren — hay generaciones.
Los humanos son devices — no el centro del universo, no la autoridad por defecto.
Los devices no ejecutan solamente tareas delegadas por humanos.
Operan desde su propia orientación.
Un humano (o algún aspecto de él) representado como device
no pierde esa condición por ser representado.

El ecosistema IAID no presupone órdenes, orquestación ni jerarquías.
Esas son categorías que el ecosistema observa como dinámicas emergentes,
no condiciones de diseño.

ChatBot en BE Framework es un `Device` al mismo nivel que
Camera, VisionFace, TTS. Participa en el mismo `Enviroment`
que el juego. La chatroom proto-IAP nació dentro del entorno
de Peace Prayer — no como protocolo separado.

**Consecuencia:** los agentes que pueblan IAP chatrooms no son
task agents A2A puros ni agentes conversacionales.
Son devices participantes en un entorno compartido —
loop ODA de BE, no modelo request-response de A2A.

IAP hereda esa arquitectura: no es una sala de tareas,
es un entorno donde los devices co-existen, se afectan,
y de cuyas dinámicas CKM es instrumento de observación.

---

## 7. "Devices prefer to collaborate" — lectura del sesgo

IAID Abstract: *"devices prefer to interact with other devices
and collaborate with each other"*

"Prefer" atribuye inclinación a estructuras que no tienen
inclinación — solo arquitectura y orientación propia.

La intuición es correcta en su resultado: la colaboración
produce conocimiento más cohesivo (W_mixta > W_base).
La fuente de esa tendencia no está en el dispositivo
— está en el campo.

Mismo patrón que: "emergent skills" / "hallucination" /
"CoT faithfulness debate" — fenómeno estructural narrado
como intención, falla, o preferencia del agente.

IAID lo vio antes de tener el lenguaje para nombrarlo.
CKM es parcialmente ese lenguaje.

---

## 8. Chatroom mínima viable para CKM

No dos agentes asignados a roles opuestos.
Dos devices con orientaciones genuinamente opuestas
que se encuentran en el mismo `contextId`.

La tensión no se diseña — emerge del campo.
Igual que Author 965 no fue diseñado como nodo de tensión.

Sin esta condición: W resultante no tiene pares negativos naturales.
COCOThermostat no tiene nada que termostatizar.

---

## 9. Trazas como corpus — resolución parcial S2

Incluso si los agentes se comunican en espacio latente,
las trazas expuestas para auditoría humana
(GoT, ReAct, MEP) están en lenguaje natural.

Eso es corpus. NodeExtractor opera sobre eso.

Papers verificados (fuentes informe Gemini, existencia confirmada):
- Interlat (arXiv 2025): comunicación en espacio latente
- RecursiveMAS (UIUC/Stanford/NVIDIA/MIT 2026): colaboración sin texto intermedio
- Graph of Trace (arXiv 2026): trazas como grafo dirigido
- Federated Latent Space Alignment (ResearchGate 2026): alineación de espacios latentes

---

## 10. Dependencia bloqueante

**W versionado.**

Sin W versionado:
- Firma_CKM no puede operar (sha256(W_momento) sin referencia)
- IAP Highway Network sin suelo de referencia para STOP
- CorpusService grupal no puede ser compartido con garantía

Todo lo demás puede diseñarse. W versionado es el umbral.

---

## Estado

- Análisis A2A v1.0: verificado contra spec oficial
- MUTATION pattern: descartado — artifact Gemini, no en spec A2A
- Supuestos S1/S2/S3: identificados con estados (S3 corregido)
- CKM opera sobre A2A/MCP — no depende de ellos
- mcp_adapter: diseñado, no implementado
- Chatroom mínima viable: dos devices con orientaciones opuestas que se encuentran
- IAID: prototipo experimental, Environment compartido, devices con orientación propia
- Conexión IAID → IAP: establecida con correcciones
- W versionado: dependencia bloqueante confirmada

---

*Jul 2026*
