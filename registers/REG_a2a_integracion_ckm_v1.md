# REG_a2a_integracion_ckm_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Jul 2026. Evaluación de ajustes y adaptaciones al protocolo A2A
para integración con CKM-IAP. Incluye análisis de samples A2A (Gemini),
verificación contra spec A2A v1.0, investigación sobre transferencia
de conocimiento semántico, y lectura de IAID.md + BEGAME.

---

## 1. Verificación A2A v1.0

Los samples de Gemini (A2A_samples.txt) no son A2A válidos.
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

Los samples de Gemini carecen de envelope JSON-RPC 2.0, usan
`text_content` en lugar de `parts[].text`, no tienen `role`,
y colocan auth en el body en lugar de HTTP headers.

**Consecuencia para mcp_adapter:** el campo de texto que va a
MonitorService es `parts[n].text` donde `kind == "text"`.
Los `data` parts son señales de lifecycle — no van a NodeExtractor.

---

## 2. contextId como anchor de sesión

`contextId` ya existe en A2A v1.0. Es el identificador que agrupa
mensajes relacionados en una misma interacción.

Mapeo directo: `contextId` → `ckm_session_id`

No hay que inventarlo. CKM lo hereda del protocolo.

---

## 3. Supuestos críticos identificados

### S1 — Chatrooms IAP son multiparty (TALÓN DE AQUILES)

A2A es fundamentalmente bilateral cliente-servidor.
No existe sala con múltiples participantes concurrentes
como primitiva del protocolo.
IAP necesita construir esa capa — hub-and-spoke donde IAP
es el nodo central. No es A2A nativo.

**Abierto. No tangencial a IAP — es su condición de posibilidad.**

### S2 — NodeExtractor produce nodos útiles sobre texto A2A

CKM fue validado sobre corpora argumentativos ricos
(5145 párrafos, debate de control de armas).
Los mensajes A2A operacionales son cortos y transaccionales.

**Parcialmente resuelto:** las trazas de ejecución en lenguaje
natural (CoT, ReAct, Graph-of-Trace) que los agentes exponen
para auditoría SÍ son texto rico. CKM opera sobre esas trazas,
no sobre los mensajes operacionales del envelope A2A.

Distinción: texto de negociación A2A (sparse) vs trazas de
auditoría en lenguaje natural (richness suficiente para W).

### S3 — STOP como señal de control (CORREGIDO)

STOP no interrumpe tareas A2A. Opera sobre Δ_r dentro
del stack CKM. Los agentes A2A no saben que ocurrió.

Highway Network no compite con la cola HTTP de tareas —
es un canal interno al stack CKM.

La ventana temporal de efectividad de STOP es sobre el estado
del campo CKM, no sobre el lifecycle A2A.

Lo que IAP debe definir: si STOP se comunica también al agente
(plano behavioral), eso requiere contrato protocolar entre IAP
y el agente — no una primitiva A2A.

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

**Lifecycle boundaries para Firma_CKM:**
- `task.status.state = "completed"`
- `task.status.state = "failed"` / `"rejected"`
- Cualquier transición `input-required → working`
  (momento donde el campo cambió de forma por intervención externa)

---

## 5. MUTATION pattern

En los samples Gemini: `MUTATION_DIRECTIVE`, `CONTEXT_OVERRIDE`,
`MUTATION_DISPATCH` aparecen en `parts[].text` — no son primitivas
del protocolo A2A. A2A es neutral al contenido.

MonitorService los captura como términos de texto.
Lo que se pierde: su significado de evento (algo en el campo fue
mutado deliberadamente).

**Tensión abierta:** el mcp_adapter necesita decidir si elevar
el peso de estos eventos. Opciones:
- A) A2A normaliza: eventos MUTATION → envelope como campos estructurados
- B) IAP detecta prefijos `^[A-Z_]+:` y los rota a lifecycle context
- C) Dos evaluaciones paralelas: estructural (envelope) + semántica (texto)

No resuelta. Registrada.

---

## 6. Origen de IAP — lectura de IAID.md y BEGAME

IAID (2024) no modelaba task agents en el sentido A2A moderno.
Modelaba dispositivos híbridos con tres tipos de función:
OBSERVATION / ACTION / MIND — participantes en un entorno compartido.

ChatBot en BE Framework es un `Device` al mismo nivel que
Camera, VisionFace, TTS. Participa en el mismo `Enviroment`
que el juego. La chatroom proto-IAP nació dentro del entorno
de Peace Prayer — no como protocolo separado.

**Consecuencia:** los agentes que pueblan IAP chatrooms no son
task agents A2A puros ni agentes conversacionales puros.
Son participantes en un entorno compartido — más cercano al
loop ODA de BE que al modelo request-response de A2A.

IAP hereda esa arquitectura: no es una sala de tareas,
es un entorno donde los dispositivos co-existen y se afectan.

---

## 7. "Devices prefer to collaborate" — lectura del sesgo

IAID Abstract: *"devices prefer to interact with other devices
and collaborate with each other"*

El término "prefer" atribuye inclinación a estructuras que no
tienen inclinación — solo arquitectura.

La intuición es correcta en su resultado: la colaboración
produce conocimiento más cohesivo (W_mixta > W_base).
Lo que está mal es la fuente de esa tendencia.

No está en el dispositivo — está en el campo.
W_mixta no supera a W_pos porque los nodos "prefieran" conectarse
con tensión estructural, sino porque la heterogeneidad produce
mayor diversidad de atractores.

Mismo patrón que: "emergent skills" / "hallucination" / 
"CoT faithfulness debate" — fenómeno estructural narrado
como intención, falla, o preferencia del agente.

IAID lo vio antes de tener el lenguaje para nombrarlo.
CKM es parcialmente ese lenguaje.

---

## 8. Chatroom mínima viable para CKM

No dos agentes cualesquiera.
Dos agentes con objetivos estructuralmente opuestos
en el mismo `contextId`.

Análogo de Author 965 y su contraparte en IAC.

Sin esta condición: Supuesto S1 produce un campo sin tensión
y W resultante no tiene pares negativos naturales.
COCOThermostat no tiene nada que termostatizar.

---

## 9. Trazas como corpus — resolución parcial S2

Papers verificados (fuentes del informe Gemini):
- Interlat (arXiv 2025): agentes comunicándose en espacio latente
- RecursiveMAS (UIUC/Stanford/NVIDIA/MIT 2026): colaboración sin texto intermedio
- Graph of Trace (arXiv 2026): trazas de ejecución como grafo dirigido
- Federated Latent Space Alignment (ResearchGate 2026): alineación de espacios latentes

**Insight clave para CKM:** incluso si los agentes se comunican
en espacio latente, las trazas expuestas para auditoría humana
(GoT, ReAct, MEP) están en lenguaje natural.

Eso es corpus. NodeExtractor opera sobre eso.

El umbral que cambiaría la estrategia: si los agentes migran
a comunicación completamente latente sin exposición de trazas
en lenguaje natural — NodeExtractor pierde superficie.
No es el escenario actual. Es el escenario que IAP debe anticipar.

---

## 10. Dependencia bloqueante

**W versionado.**

Sin W versionado:
- Firma_CKM no puede operar (sha256(W_momento) no tiene referencia)
- IAP Highway Network no tiene suelo de referencia para STOP
- CorpusService grupal no puede ser compartido entre agentes con garantía

Todo lo demás puede diseñarse. W versionado es el umbral.

---

## Estado

- Análisis A2A v1.0: verificado
- Supuestos S1/S2/S3: identificados con estados
- Estructura mcp_adapter: diseñada, no implementada
- Chatroom mínima viable: definida conceptualmente
- MUTATION pattern: tensión abierta, tres opciones registradas
- Conexión IAID → IAP: establecida
- W versionado: dependencia bloqueante confirmada

---

*Jul 2026*
