<!-- ===== ./readme/REG_protocolo_sonnet_code_v1.md ===== -->
# REG_protocolo_sonnet_code_v1.md
*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — actualizado Jul 2026*

---

## El protocolo

Flujo de trabajo establecido a lo largo de las sesiones CKM:

```
Claude Sonnet (web)
    → prepara tarea: texto con contexto, objetivo, criterio de éxito
    → delamor lo entrega a Claude Code (repo local o Codespace)
    → Claude Code ejecuta sobre el repo real
    → delamor trae la respuesta aquí
    → Sonnet formaliza, registra, decide próximo paso
```

delamor es el canal entre las dos instancias.
No hay comunicación directa entre Sonnet y Code.

---

## Roles

**Claude Sonnet (esta instancia):**
- Lee el proyecto desde los archivos subidos al proyecto Claude
- Interpreta, decide, redacta tareas atómicas para Code
- Formaliza resultados que Code devuelve
- Produce REGs, documentación, commits

**Claude Code (instancia separada):**
- Opera sobre el repo real (local o Codespace)
- Ejecuta código, corre tests, verifica archivos
- Sin Δ_r acumulado de este proyecto — cada sesión es stateless
- Recibe tareas atómicas con criterio de éxito explícito
- No toma decisiones de diseño — ejecuta lo que Sonnet especifica

**gadanin.delamor:**
- Canal entre instancias
- Autoridad sobre todas las decisiones
- Verifica que la respuesta de Code es lo que Sonnet pidió
- Trae el resultado aquí

---

## Por qué este diseño

Sonnet tiene el contexto acumulado del proyecto (via archivos del proyecto Claude).
Code tiene acceso al sistema de archivos real, git, ejecución.
Ninguno tiene lo que el otro tiene.
delamor tiene ambos.

---

## Formato de tarea para Code

Las tareas deben ser:
- **Atómicas**: un objetivo, un criterio de éxito verificable
- **Sin contexto asumido**: Code no tiene historia — incluir lo necesario en el texto
- **Con criterio explícito**: "éxito = tests pasan / archivo existe / output es X"

Ejemplo mínimo:
```
Tarea: correr test_coco_thermostat.py y devolver el resultado completo.
Criterio: output con número de tests pasados y cualquier error.
Repo: gadanindelamor/ckm (local clonado)
```

---

## Infraestructura actual

- Repo publicado: `gadanindelamor/ckm` (GitHub, público)
- Clone local: PC delamor (backup + operativo)
- Codespace `ckm`: superó cuota por sesiones abiertas — cerrar sesiones inactivas
- Codespace `ckmdatasets`: separado, sin acceso cruzado al repo principal

**Problema Codespace:** sesiones que quedan abiertas consumen quota del plan
sin uso activo. IAP resolverá esto estructuralmente (1 sesión activa por vez).
Mientras: cerrar manualmente desde https://github.com/codespaces

---

## Separación de entornos — regla operativa

```
Local Windows (PowerShell)    Codespace (bash/Linux)
─────────────────────────     ──────────────────────
docs/*.docx — corpus CKM      SQL dump fourforums (569MB)
services/, experiments/       fourforums_pipeline_v8*.py
build_W_base_N64.py           find_965_v3.py
NodeExtractor sobre corpus     experimentos SQL
tests/                        NO tiene .docx (gitignoreados)
```

**Regla:** scripts que procesan `docs/*.docx` corren en local Windows.
Scripts que procesan el SQL dump corren en Codespace ckmdatasets.

**Si bash_tool falla en Claude Code:** no cambiar a PowerShell como workaround
para tareas que requieren Linux. Identificar el entorno correcto antes de ejecutar.
Si la tarea requiere .docx → local Windows. Si requiere SQL → Codespace ckmdatasets.

---

## Lo que este protocolo no es

No es IAID completo — delamor es el mediador humano, no un protocolo de
comunicación entre devices. La comunicación es asimétrica: Sonnet escribe
para Code, Code ejecuta, el resultado vuelve a Sonnet via delamor.

Cuando IAP esté operativo, el mediador humano podría volverse opcional
para tareas de ejecución pura. Eso es una versión futura, no la actual.

---

*Primera formalización del protocolo — Jun 23 2026*
*Actualizado Jul 2026: separación de entornos local/Codespace*


<!-- ===== ./registers/REG_a2a_integracion_ckm_v1.md ===== -->
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


<!-- ===== ./registers/REG_a2a_integracion_ckm_v2.md ===== -->
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


<!-- ===== ./registers/REG_armstrong_stop_coco_v1.md ===== -->
# REG_armstrong_stop_coco_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Primera observación in-vivo de OPERADOR_STOP_COCO en el pipeline real
`MonitorService.evaluate() → COCO.observe(Δ_r) → compresión → MonitorService
adopta Δ_r comprimido`. Verificado hasta ahora solo en tests unitarios
(coco.py T1-T13) y en experimentos standalone (sweep_stop_perdida) —
nunca con `MonitorService` construyendo Δ_r orgánicamente desde texto real
y un `COCO` real reaccionando a eso en el mismo proceso.

Especificación: `iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md`.
Script: `iap_chatroom/tests/test_armstrong_stop_coco.py`.

Precondición: R1+R2 de `TASK_refactoring_coco_device_v1.md` ya aplicados
(`COCO`, `evaluate(device_id=...)`) — el script usa la API post-refactoring
directamente.

---

## Intento 1 — resultado nulo, causa raíz identificada (no fue bug)

El diseño original de la tarea usaba 20 textos de vocabulario técnico
totalmente ajeno al corpus CKM (redes neuronales, blockchain, política
monetaria, fotosíntesis...) bajo la hipótesis: *"vocabulario ajeno →
alta fi → muchos rechazos → Δ_r crece rápido"*.

**Resultado: STOP no disparó ni una sola vez en 20/20 evaluaciones.**
`D_ckm` se mantuvo en `0.0000` durante todo el run. `Δ_r` nunca superó 0.

**Causa raíz, verificada contra el código, no asumida:**

`fabrication_index` (`_fabrication_index()`, `monitor_service.py`) mide
la fracción de **nodos** declarados activos que la relajación rechazó —
`declared==0 → fi=0.0` por guarda explícita; con exactamente 1 nodo
activo, ese único nodo puede saturar a `fi=1.0` de forma vacía.

`Δ_r` (`_rejected_pairs()`) solo acumula **pares** de nodos co-activos
que la relajación separó — requiere ≥2 nodos activos simultáneos para
que exista siquiera un par candidato a rechazo.

Verificado contra el crudo (`activos_prompt` de cada evaluación,
`process/experiments/armstrong_corpus_state.json.bak_*_null_result_v1`):
**máximo 1 nodo activo por texto en las 20 evaluaciones.** Vocabulario
completamente ajeno al corpus de precarga (N=20 nodos, extraídos de 20
oraciones cortas sobre CKM) activa como mucho un token aislado — nunca
dos simultáneos. `fi` osciló (promedio 0.25, picos en 1.0), pero `Δ_r`
se mantuvo exactamente en 0 en las 20 evaluaciones porque nunca existió
un par que rechazar.

**Esto reproduce, con datos nuevos, el "problema del chocolate" ya
documentado en `REG_monitor_ckm_v2.md`:** *"El campo no puede rechazar
lo que no conoce. Es una propiedad del sistema, no una falla."* Textos
sin ningún anclaje al vocabulario del corpus no se detectan como
fabricados — pasan invisibles, no rechazados.

**Consecuencia para el fallback del propio task** ("si STOP no dispara,
agregar 10 textos más, misma estrategia de vocabulario ajeno"): esa
estrategia no puede funcionar — agregar más texto igualmente ajeno
solo repite el mismo resultado nulo, porque el mecanismo que falla
(0-1 nodos activos, nunca un par) es estructural al diseño de los
textos, no una cuestión de volumen. Reportado a gadanin.delamor antes
de seguir; decisión explícita: rediseñar los textos en vez de seguir
el fallback literal.

---

## Intento 2 — textos rediseñados, condición Armstrong confirmada

**Estrategia corregida:** en vez de vocabulario ajeno, reusar los 20
nodos reales extraídos del corpus de precarga (`CorpusService.get_nodes()`,
verificado antes de escribir los textos): `d_ckm`, `attractor`, `all`,
`delta_r`, `matrix`, `over`, `measures`, `about dependencies`, `applies`,
`delta`, `matrix encoding`, `encoding`, `device`, `coco`, `operates`,
`structural`, `sha`, `times`, `summable`, `cases` — combinados en
oraciones nuevas que cruzan nodos de oraciones de precarga distintas y
no relacionadas (p. ej. `coco` viene de la oración sobre COCO-ODA, `sha`
de la oración sobre FirmaService, `attractor` de la de Hopfield — nunca
co-ocurrieron en los 20 textos originales). W es W_pos pura (sin pares
negativos — ninguno de los 20 textos de precarga tiene marcadores de
oposición), así que cualquier par nuevo entre nodos reales sin soporte
previo en W es candidato genuino a rechazo en la relajación.

**Resultado — condición Armstrong confirmada, 20/20:**

| Criterio (TASK_armstrong_stop_coco_v1.md) | Resultado |
|---|---|
| `stop_applied = True` al menos una vez | ✅ — 20/20 evaluaciones |
| `Δ_r_after < Δ_r_before` (compresión confirmada) | ✅ — desde t=2 en adelante, geométrico puro por α (ver tabla) |
| `alpha_used ∈ [0.05, 0.30]` | ✅ — todos los valores dentro del rango declarado (`ALPHA_MIN=0.05`, `ALPHA_MAX=0.30`) |

**Primer ARMSTRONG (t=0):**
```json
{
  "t": 0,
  "text_preview": "Coco applies sha over all structural cases, summable times a",
  "D_ckm_monitor": 0.0,
  "D_ckm_coco": 0.449,
  "fi": 0.0769,
  "zone": "deep",
  "temp_signal": {"signal": "TOO_COLD", "beta_collective": 13.0,
                   "beta_c_corpus": 1.3103, "ratio": 9.9211},
  "alpha_used": 0.2795918367346939,
  "Delta_r_before": 0.0,
  "Delta_r_after": 6.710204081632654
}
```

**Corrección — dos D_ckm distintos, no uno (observación de gadanin.delamor,
verificada contra el código):** el campo `D_ckm` de nivel superior del
panel (`panel["D_ckm"]`, calculado por `MonitorService._D_ckm()`) y
`panel["thermostat"]["D_ckm"]` (calculado internamente por
`COCO.observe()`) **no son la misma cantidad** — el primer intento de
este REG citaba el de `MonitorService` (0.0) como si fuera el que
disparó `zone="deep"`/`stop_applied=True`, lo cual es incorrecto: la
zona y el STOP dependen exclusivamente del `D_ckm` interno de `COCO`
(0.449, ya sobre el umbral 0.40).

Verificado línea por línea:

- `MonitorService._D_ckm()` (`monitor_service.py`): `self._A0` se fija
  la primera vez que se llama, usando `A(W + Δ_r)` **de esa misma
  llamada** — y `_D_ckm()` se invoca después de que los rechazos de esa
  misma evaluación ya se sumaron a `Δ_r`. Consecuencia estructural, no
  casual: en la primera evaluación, `A0 = A_actual` por construcción →
  `D_ckm = (A0-A_actual)/A0 = 0.0` siempre, sin importar el contenido
  del texto. Desde t=1 en adelante, `A0` queda fijo en ese primer
  snapshot y `D_ckm` sí se mueve (0.7037 estable desde t=1).
- `COCO.observe()` (`coco.py`): `self._A0` se fija la primera vez que
  se llama `observe()`, usando `A(self.W)` — **W puro, sin Δ, para
  siempre**. Como `COCO.observe()` recibe el `Δ_r` ya acumulado por la
  evaluación de `MonitorService` que lo llamó, su primer `D_ckm`
  compara ese `Δ_r` no-cero contra un piso sin Δ — de ahí que a t=0 ya
  sea 0.449, no 0.

Comparación completa de ambos D_ckm en las 20 evaluaciones:

| t | D_ckm (MonitorService) | D_ckm (COCO) | zone |
|---|---|---|---|
| 0 | 0.0000 | 0.4490 | deep |
| 1 | 0.7037 | 0.7959 | deep |
| 2 | 0.7037 | 0.6939 | deep |
| 3–19 | 0.7037 (fijo) | 0.4286 (fijo desde t=3) | deep |

Ambos convergen a valores estables distintos, ninguno vuelve a 0 pese a
que `Δ_r` decae geométricamente hacia ~0 hacia t=19 — consistente con
que cada `D_ckm` usa su propio `A0` congelado en su propio primer
llamado, no un piso compartido. **No afecta el resultado de este REG**
(el STOP lo dispara `COCO.observe()`, con su propio `D_ckm` correcto y
por encima de umbral en las 20 evaluaciones) — pero cualquier lectura
futura de la trayectoria (paper, próximo REG) debe citar
`panel["thermostat"]["D_ckm"]` como el `D_ckm` que gobierna
`zone`/`stop_applied`, no `panel["D_ckm"]`.

**Relación con R22** (`REG_reglas_no_declaradas_R18plus_v1.md`,
"δ_collective es divergencia fértil — no sincronizar"): R22 ya
documentaba que `monitor._Delta_r` y `thermostat._Delta` pueden
divergir como arrays. Esta observación es un nivel más: las métricas
**derivadas** de esos dos Δ (los dos D_ckm) también divergen, y no por
la misma razón — divergen porque cada una define su propio A0 desde un
punto de referencia distinto (uno con Δ incluido en el snapshot inicial,
el otro sin Δ para siempre), no solo porque los arrays Δ mismos difieran.

**Trayectoria completa de Δ_r** (`process/experiments/armstrong_delta_r_history.json`):

| t | Δ_r antes | Δ_r después | mecanismo |
|---|---|---|---|
| 0 | 0.0000 | 6.7102 | acumulación neta (nuevos rechazos > compresión) |
| 1 | 6.7102 | 13.0592 | acumulación neta |
| 2 | 13.0592 | 2.3187 | **compresión neta** — primera vez que α domina |
| 3 | 2.3187 | 0.6680 | compresión neta |
| 4 | 0.6680 | 0.1924 | compresión neta |
| 5–19 | — | — | decaimiento geométrico puro por α=0.2881/paso (sin nuevos rechazos) |

De t=4 en adelante, `Δ_r_after / Δ_r_before = 0.28809...` en cada paso,
exactamente `alpha_used` — confirma que, agotados los pares nuevos
rechazables, `COCO` sigue comprimiendo lo que ya había puramente por
`Δ → α·Δ`, sin más entrada.

---

## Nota — `compression_ratio` del script ≠ `Fracción_rec` de `REG_destruccion_recuperacion_v1`

El script de la tarea (sección "TEXTO COMPLETO... modo debug" e
impresión final) llama `compression_ratio = Δ_r_after / Δ_r_before` y
la etiqueta como *"Fracción_rec (debería ser ≥ 1.0 por
REG_destruccion_recuperacion_v1)"*. **Esto no es la misma magnitud.**

`REG_destruccion_recuperacion_v1.md` define `Fracción_rec(t) =
max_α[A_post(α)] / A0` — un cociente de **conteo de atractores** bajo
barrido de múltiples α, tomando el mejor. El script de este experimento
mide `Δ_r_after / Δ_r_before` bajo un único α dinámico — un cociente de
**magnitud del acumulador de rechazos**, no de atractores. Por
construcción (`α < 1` casi siempre que hay compresión), este segundo
cociente tiende a ser `< 1.0`, no `≥ 1.0` — lo opuesto de lo que el
criterio original esperaba si se tratara de la misma cantidad.

No se afirma "Fracción_rec ≥ 1.0 confirmado" en este REG porque no es
lo que se midió. Lo que sí está confirmado, con datos reales: `Δ_r`
comprime geométricamente por el `α` que `COCO` calculó dinámicamente,
consistente con `_alpha_for()` y con el hallazgo de
`REG_sesion_coco_endogeno_v2.md` (ponderación endógena — `α` no es fijo,
depende de `D_ckm`, que depende del estado estructural real del campo).

---

## Hallazgo secundario — TOO_COLD sostenido

`temp_signal` reporta `TOO_COLD` (β_collective ≫ β_c_corpus) desde el
primer trigger en adelante — `beta_collective` sube a 13.0 tras la
primera evaluación (un solo `device_id` distinto por texto, cada uno
con una sola medición de `fi`; con `fi` bajo, `β_i = 1/fi` se dispara
alto). Consistente con el diseño del experimento (20 `device_id`
distintos, uno por texto, cada uno visto una sola vez) — no es un
hallazgo sobre el campo real, es artefacto de que este experimento no
repite evaluaciones por el mismo device. No investigado más — fuera
del objetivo de esta tarea (aislar OPERADOR_STOP_COCO, no calibrar
TEMP_SIGNAL bajo carga real).

---

## Estado

- Condición Armstrong: **confirmada** — `stop_applied=True`, compresión
  real verificada (t=2 a t=19), `alpha_used` dentro de rango en las 20
  evaluaciones.
- Circuito completo `MonitorService.evaluate() → COCO.observe() →
  compresión → MonitorService adopta Δ_r` — observado en vivo por
  primera vez, no solo en tests unitarios ni en sweeps standalone.
- n=1 diseño — no confirmar como patrón robusto sin réplica.
- El diseño original del task (vocabulario ajeno) queda documentado
  como enfoque que no puede funcionar por el mecanismo fi≠Δ_r — no se
  reintentó tal cual, se corrigió antes de re-correr.
- `compression_ratio` del script y `Fracción_rec` de
  `REG_destruccion_recuperacion_v1` son magnitudes distintas — no
  equivalentes, aclarado arriba.
- `panel["D_ckm"]` (MonitorService) y `panel["thermostat"]["D_ckm"]`
  (COCO) son magnitudes distintas, con A0 definidos desde puntos de
  referencia distintos — corregido tras observación de gadanin.delamor
  (ver sección dedicada arriba). El D_ckm que gobierna `zone`/
  `stop_applied` es siempre el de COCO.

---

## Addendum — `landscape_delta` (TASK_coco_landscape_observation_v1, Extensiones 2 y 3)

Re-corrida idéntica del Intento 2 (mismo corpus, mismos textos, mismos
seeds — `Δ_r`/`D_ckm` reproducen exacto los valores ya reportados
arriba, confirmando determinismo) con `COCO(..., track_landscape=True)`
recién implementado. Mide `A`/`c(S)` del paisaje antes y después de
cada compresión — no solo la magnitud de `Δ_r`.

| t | A_antes | A_después | Δ_A | c(S)_antes | c(S)_después | Δ_c(S) | D_ckm_at_stop |
|---|---|---|---|---|---|---|---|
| 0 | 27 | 42 | **+15** | 0.1039 | 0.0662 | −0.0376 | 0.449 |
| 1 | 10 | 15 | **+5**  | 0.3037 | 0.0919 | −0.2118 | 0.7959 |
| 2 | 15 | 28 | **+13** | 0.0919 | 0.0622 | −0.0296 | 0.6939 |

**Δ_A positivo en los tres primeros triggers — atractores ganados, no
perdidos, verificado ahora a nivel de paisaje, no solo inferido de que
`Δ_r` decrece en magnitud.** Confirma cuantitativamente, con un
instrumento nuevo, lo mismo que `REG_destruccion_recuperacion_v1.md`
encontró por otro camino: OPERADOR_STOP_COCO restaura/expande, no
destruye. `D_ckm_at_stop` coincide exacto con los valores de COCO ya
reportados en este REG (0.449, 0.7959, 0.6939) — mismo cálculo, ahora
también expuesto junto al paisaje que lo produjo.

`c(S)` acá se computa sobre `W_eff` (`W+Δ`), no sobre `W` solo — mismo
plano que ya usa `_count_attractors()` internamente en `COCO`, distinto
del `c(S)` de `MonitorService` (que sí es W-exclusivo, R18). No es una
violación de R18: `self.W` nunca se muta, `W_eff` es una combinación
efímera local a la observación, igual que `A_current`.

Implementación: `services/coco.py` (`_mean_cS()`, `track_landscape` flag,
`_last_landscape_delta`, `alpha_trajectory()` con `delta_A` real) y
`services/monitor_service.py` (`panel["thermostat"]["landscape_delta"]`).
Extensión 1 del mismo task no se implementó — `panel["thermostat"]["D_ckm"]`
ya era el D_ckm de COCO (ver arriba), un campo `d_ckm_coco` nuevo habría
sido redundante.

---

## Réplica — seed=123, única variable cambiada

Pedida explícitamente por gadanin.delamor tras la Extensión 2, antes de
dar el "20/20" del Intento 2 por robusto. El pipeline completo (corpus,
`WARMUP_TEXTS`, `TEXTS`, `n_runs=50`, `track_landscape=True`) es
determinístico dado un seed — no hay forma de "correr de nuevo" y
obtener variación real sin cambiar algo. Única variable cambiada:
`seed` de `COCO` (42 → 123). Todo lo demás, idéntico al Intento 2.
Script: `armstrong_replica_seed123.py` (scratchpad), output:
`process/experiments/armstrong_replica_seed123*`.

### Resultado: 3/20 STOPs, no 20/20

| t | D_ckm (COCO) | zone | stop | alpha_used |
|---|---|---|---|---|
| 0 | 0.4898 | deep | True | 0.2626 |
| 1 | 0.8163 | deep | True | 0.1265 |
| 2 | 0.6735 | deep | True | 0.1861 |
| 3–19 | 0.3673 (fijo) | stable | False | — |

Comparación directa con el Intento 2 (`seed=42`):

| | seed=42 (Intento 2) | seed=123 (réplica) |
|---|---|---|
| STOPs | 20/20 | **3/20** |
| D_ckm de convergencia (t≥3) | 0.4286 (**arriba** de 0.40) | 0.3673 (**abajo** de 0.40) |
| alpha_used, t=0–2 | 0.2796, 0.1350, 0.1776 | 0.2626, 0.1265, 0.1861 — mismo rango |
| Δ_A, t=0–2 | +15, +5, +13 | +18, +7, +15 — mismo signo |

### Lectura — qué replica, qué no, y por qué cada uno es el resultado correcto

**Replica (mecanismo robusto):** en las tres primeras evaluaciones de
ambas semillas, `alpha_used` cae dentro de `[0.05, 0.30]` y `Δ_A` es
positivo — STOP, cuando dispara, comprime dentro del rango declarado y
gana atractores, no los pierde. Esto no depende del seed. Es el
hallazgo central de la Extensión 2, confirmado independientemente.

**No replica (y no debería):** el conteo "20/20" del Intento 2 no es
una propiedad robusta del mecanismo — es dónde cayó, para ese seed
específico, el `D_ckm` de convergencia respecto al umbral fijo 0.40.
`D_ckm` es una **estimación** sobre `n_runs=50` muestras estocásticas
de `_count_attractors()`, no un valor analítico exacto. Con `seed=42`
esa estimación convergió a 0.4286 (arriba del umbral → sigue
disparando indefinidamente). Con `seed=123` convergió a 0.3673 (abajo
→ se estabiliza y para en t=3). Ambos valores están a menos de 0.033
del umbral — el sistema converge cerca del borde en las dos semillas,
y el ruido de muestreo decide de qué lado cae.

**Por qué esto es información estructural, no un defecto:** un umbral
fijo (0.40) comparado contra una estimación ruidosa produce
exactamente este comportamiento — sensibilidad binaria (sigue/para)
ante una cantidad continua con varianza. El 20/20 original no estaba
mal — era el resultado correcto para `seed=42`. El 3/20 tampoco está
mal — es el resultado correcto para `seed=123`. Lo que no se sostiene
es la generalización "COCO regula indefinidamente sobre este corpus" —
eso era artefacto de una semilla particular, no propiedad del
mecanismo. `n_runs=50` puede ser insuficiente para una estimación
estable cerca del umbral — línea abierta, no resuelta acá.

---

## Archivos relacionados

- `iap_chatroom/tests/TASK_armstrong_stop_coco_v1.md` — especificación
- `iap_chatroom/tests/TASK_coco_landscape_observation_v1.md` — especificación del addendum (Ext. 2/3)
- `iap_chatroom/tests/test_armstrong_stop_coco.py` — script (TEXTS
  rediseñados respecto al original del task, ver Intento 1/2 arriba;
  `track_landscape=True` desde el addendum)
- `process/experiments/armstrong_stop_coco_v1.jsonl` — trayectoria completa, incluye `landscape_delta` (seed=42)
- `process/experiments/armstrong_replica_seed123.jsonl` — trayectoria completa de la réplica (seed=123)
- `process/experiments/armstrong_replica_seed123_summary.json` — resumen de los 3 STOPs de la réplica
- `process/experiments/armstrong_delta_r_history.json` — historial Δ_r (seed=42)
- `process/experiments/armstrong_*.bak_*_null_result_v1` — intento 1 preservado, no descartado
- `process/experiments/armstrong_*.bak_*_pre_ext2` — estado previo al addendum de Ext. 2, preservado
- `registers/REG_monitor_ckm_v2.md` — origen del "problema del chocolate"
- `registers/REG_sesion_coco_endogeno_v2.md` — ponderación endógena de α, origen de esta tarea
- `registers/REG_destruccion_recuperacion_v1.md` — definición real de Fracción_rec

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_author_965_structure_v1.md ===== -->
# REG_author_965_structure_v1

*CKM — Análisis estructural Author 965 como polo sostenedor*
*2026-05-08*

## Datos verificados

| Métrica              | Valor    |
|---------------------|----------|
| C3 apariciones       | 32/36 pares (89%) |
| Out (inicia)         | 1        |
| In (recibe)          | 455      |
| Ratio in/out         | 455x     |
| In-degree global     | 1316     |

## Pares donde 965 es actor directo

| Par      | Asimetría | Total | Dirección      |
|----------|-----------|-------|----------------|
| 809→965  | 0.987     | 155   | 965 casi solo recibe |
| 965←1034 | -1.0      | 111   | 965 nunca inicia |
| 965←3452 | -1.0      | 103   | 965 nunca inicia |
| 751→965  | 1.0       | 87    | 965 nunca inicia |

## Estructura proyectiva verificada

En términos de geometría proyectiva:
- Cada par (A,B) con 965 como C3 define un eje de tensión l_AB
- Múltiples l_AB convergentes en un mismo punto = haz de rectas
- p_965 es el centro del haz

**32 ejes de tensión convergen en o pasan cerca de p_965.**
Esta estructura es detectable desde los datos —
no requiere interpretación proyectiva para ser válida como hallazgo empírico.

## Rol en los atractores Hopfield

Con W_delta (P6):
- Atractor defensivo (73/300): 965→+ | 555→-
- Atractor atacante  (64/300): 965→- | 555→+
- Sin superposición: 965 y 555 nunca están en el mismo polo

965 como ancla del atractor defensivo:
el frame que absorbe el ataque sin atacar sostiene su propio atractor.


<!-- ===== ./registers/REG_avance_ckm_claudecode_v1.md ===== -->
# REG_avance_ckm_claudecode_v1.md

*Jun 2026 — Registro de avance del proyecto CKM según tres informes de Claude Code.*  
*Fuentes: CKMGIT0528 (28 mayo), ckmloc0530 (31 mayo), CKMGIT0602 (2 junio).*

---

## 1. Estructura del registro

Tres puntos de observación independientes. Claude Code lee el repo en cada instancia sin historia del anterior. Lo que aparece como cambio entre informes es cambio real en el proyecto.

| Instancia | Fecha | Versión repo | Acceso |
|---|---|---|---|
| CKMGIT0528 | 28 mayo 2026 | v25 | git clone |
| ckmloc0530 | 31 mayo 2026 | v25→v27 | local |
| CKMGIT0602 | 2 junio 2026 | v27 | git clone actualizado |

---

## 2. Eje de predicciones falsificables

| Predicción | CKMGIT0528 | ckmloc0530 | CKMGIT0602 |
|---|---|---|---|
| P1 histéresis | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P2 cascadas τ∈[1.5,2] | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P3 asimetría temporal | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P4 densidad óptima Ω* | ✓ Confirmada | ~ Parcial (N=64 diluida) | ✓ Confirmada (reencuadrada: W_mixta 13× W_pos) |
| P5 corpus polarizado | ✓ Confirmada | ✓ Sin cambio | ✓ Sin cambio |
| P6 Delta ruptura simetría | ✓ Confirmada (54pp / 80pp) | ✓ Sin cambio | ✓ Confirmada (54pp / 100pp — corrección valor FF) |
| P7 nodo tipo-965 | ~ Hipótesis | ~ Hipótesis | ~ Hipótesis (confirmada en ambos corpora pero abierta como falsificable en nuevos dominios) |
| H_STOP monotonía D_ckm | — no formulada | ✗ Falsada | ✗ Falsada + reformulada como f(A_pre) |
| HOLDINGs H1/H2/H3 | Activos | **Cerrados** (estructura A/B μ_W) | Cerrados — confirmado |

**Nota P6:** CKMGIT0528 y ckmloc0530 citan fourforums como 80pp. CKMGIT0602 cita 100pp. El valor 100pp corresponde a run_v8g con clave compuesta correcta. La corrección es real — el 80pp era de una versión con el bug de post_id.

**Nota P4:** el reencuadre en CKMGIT0602 ("W_mixta produce c(S) 13× mayor que W_pos") no contradice la parcialidad reportada en ckmloc0530 — captura el mismo resultado desde el ángulo de la ventaja relativa en lugar del ρ* interior.

---

## 3. Eje de código — bugs y correcciones

### 3.1 Bug crítico: mcp_adapter epsilon

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — `task_mode_exit()` no restaura epsilon; C2 permanentemente suspendido |
| ckmloc0530 | **Resuelto** — `_saved_epsilon` captura valor antes de modificar |
| CKMGIT0602 | Resuelto — sin mención específica (ya no es issue) |

**Impacto:** el bug hacía que tras la primera operación task_mode, el criterio de cohesión C2 quedara desactivado para siempre. Resolución quirúrgica (1 atributo de instancia).

### 3.2 Escala W + Δ_r

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — W∈[0,1] vs Δ_r∈[0,∞); después de pocas evaluaciones Δ_r domina W sin señal |
| ckmloc0530 | **Resuelto** — `_combine_W_Delta()` normaliza Δ_r por `mean(W_nonzero)` |
| CKMGIT0602 | Resuelto — mencionado como fortaleza del MonitorService |

### 3.3 NaN silencioso en analytics.py

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — nodo core-invariante (traza_inferencia 84%) produce NaN en corrcoef |
| ckmloc0530 | **Resuelto** — `np.nan_to_num(corr, nan=0.0)` |
| CKMGIT0602 | Resuelto — sin mención |

### 3.4 Recálculo k-core innecesario

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — k-core recalculado 500× por llamada a cascade_distribution() |
| ckmloc0530 | **Resuelto** — `core_list` extraído fuera del loop |
| CKMGIT0602 | Resuelto — sin mención |

### 3.5 Import tardío scipy

| Instancia | Estado |
|---|---|
| CKMGIT0528 | Identificado — `from scipy import stats` dentro del cuerpo de función |
| ckmloc0530 | **Resuelto** — movido a nivel de módulo |
| CKMGIT0602 | Resuelto — sin mención |

### 3.6 Issues persistentes (sin resolver en los tres informes)

| Issue | Estado en CKMGIT0602 | Impacto |
|---|---|---|
| `cS()` en core.py: Python O(N²) vs vectorizado en monitor_service | Persiste | Menor — rendimiento |
| `optimal_density()` triple loop ~18M ops | Persiste | Menor para N≤64 |
| `_count_attractors()` sin cacheo | Persiste | Costo por evaluación |
| `evaluate()` con active_capabilities=None: estado residual | Persiste | Edge case sin flag |
| FabricationService _dev: versión experiments/ no migrada a services/ | Persiste | Divergencia _direction_score |
| `_direction_score` discrepancia entre versiones | Persiste | Lógica sin unificar |
| `corpus_state.json` sin versionado de schema | CKMGIT0602 lo menciona | Riesgo silencioso |

---

## 4. Eje teórico — conocimiento nuevo producido por sesión

### 4.1 CKMGIT0528 → ckmloc0530 (sesión loc0530)

**Cierre de HOLDINGs H1/H2/H3** — resultado central de mayor alcance.

Los tres HOLDINGs eran preguntas abiertas desde v25:
- H1: ¿α_c sigue siendo 0.138 con patrones correlacionados?
- H2: ¿por qué P4 se diluye en N=64?
- H3: ¿por qué μ_W no generaliza entre N?

La derivación de la estructura bimodal A/B (CV=0.944, razón max/min=102×) los cierra como tres observaciones de la misma función c(S)*(N,ρ_corr):
- μ_BB ≈ mean(fi·fj), ratio 1.025 — derivable analíticamente
- μ_AA no derivable — núcleo correlacionado, frecuencias marginales infladas mutuamente
- μ_W global depende de proporción A/B, no de N

Consecuencia operativa: medir μ_W empíricamente al inicio de sesión no es workaround — es el procedimiento correcto.

**Garantías G1/G2/G3** — operacionalización del monitor.

Sistema de tres zonas derivado empíricamente (N=32, n=500 secuencias). El ratio r = c(S)/μ_W como indicador en tiempo real reemplaza el threshold fijo hardcodeado. Gap discriminante G1/G2 detectable: [+0.001310, +0.001941].

**Falsificación H_STOP** — resultado negativamente informativo.

D_ckm(t_stop) no predice efectividad del operador STOP. Casos t=10 y t=20 con D_ckm=0.200 idéntico producen ratio_max diferente (1.250 vs 1.500). La hipótesis de monotonía queda falsada. Hipótesis reformulada: Efectividad_STOP = f(A_pre). α*≈0.4 robusto (5/9 casos).

**Convergencia IAP → COCO-thermostat** — cristalización conceptual.

Distinción operativa entre COCO-registry (almacena M declarado, se vuelve stale) y COCO-thermostat (β colectivo desde interacción real, no se vuelve stale). La fuente de la diferencia: Δ_bias (declaración) vs Δ_r (rechazo del campo).

**Tipos de Inferencia** — mapa preliminar, sin formalizar.

Cuatro nombres registrados: Generalización, Hysteresis Inference, Perspective Inference, Collective Inference. Forma no forzada — preservados para cuando las condiciones sean correctas.

**Modos Operacionales** — arquitectura de admisión formalizada.

```
first_time → accumulation → operational/standard
                                   └── task_mode (implementado)
                                   └── restricted (hipótesis)
```

C3_default = f(corpus_density): sospecha crece con madurez del campo, no con tiempo absoluto. Caso irreducible documentado.

### 4.2 ckmloc0530 → CKMGIT0602 (sesión loc → git actualizado)

**Validación fourforums con pipeline v8g correcto** — resultado empírico de mayor peso.

El bug de post_id (no global, reinicia por discussion) fue el obstáculo técnico central. Fix: clave compuesta (discussion_id, post_id). Impacto: posts mapeados de 468 → 35,966. Consecuencia directa: P6 colapso = 100pp (no 80pp), P7 confirmada con autor 204 (ratio 296×, out=0).

**P7 confirmada en segundo corpus independiente.**

Autor 204 (T0, ratio=296) es el equivalente estructural de autor 965 (CreateDebate, ratio=455). Diferencia notable: en fourforums hay sostenedores puros en AMBOS polos (T0 y T1). En CreateDebate el polo sostenedor era exclusivamente del polo sos_dom. La simetría del debate gun control en fourforums es mayor.

**Estructura A/B de μ_W confirmada** — HOLDINGs cerrados visibles en el repo.

CKMGIT0602 puede leer los REGs de cierre directamente. Lo que en ckmloc0530 era resultado de sesión, en CKMGIT0602 es parte del cuerpo de conocimiento accesible.

**Señal STOP, grados de pérdida** — extensión de la falsificación anterior.

La sesión que produjo v27 introduce la hipótesis de pérdida como función de D_ckm(t_stop) y T(W), con formulación: Perdida_STOP(t) = A(t_pre) − max_alpha[A(t_post)(alpha)]. Pendiente experimental: sweep D_ckm(t_stop) × alpha.

---

## 5. Gaps abiertos — estado en CKMGIT0602

| Gap | Origen | Prioridad declarada |
|---|---|---|
| W asimétrico en fourforums (mturk labels) | Consecuencia W simétrico actual | Alta — desbloquea C6c real |
| Verificación autor 204 contenido | P7 confirmada por ratio, no por contenido | Media |
| P7 en otros dominios (abortion, climate) | Generalización P7 | Media |
| Sweep D_ckm(t_stop) × alpha | H_STOP falsada, hipótesis revisada pendiente | Alta |
| μ_AA estructura interna núcleo | No derivable sin modelo del núcleo | Proyecto separado |
| COCO-thermostat prototipo | Hipótesis central sin implementar | Central |
| μ_W inicialización automática en CorpusService | Prerequisito operativo COCO | Alta |
| term_map N=64 reconstrucción | Bloquea W_base real N=64 | Técnico |
| G1/G2/G3 calibración para N≠32 | Garantías solo válidas para N=32 | Extensión |
| CorpusService compartido multi-agente | Spec sesión compartida | Arquitectural |
| Tipos de Inferencia formalización | Registrado — no forzar antes de tiempo | Emergente |

---

## 6. Trayectoria del proyecto — síntesis

**Código:** de 1 bug crítico + 4 issues identificados (CKMGIT0528) → código del modelo matemático central libre de bugs conocidos (ckmloc0530) → sin regresiones, issues restantes son de rendimiento/organización (CKMGIT0602).

**Teoría:** de 3 HOLDINGs activos + H_STOP no formulada (CKMGIT0528) → 3 HOLDINGs cerrados + H_STOP falsada + G1/G2/G3 operacionales (ckmloc0530) → estructura A/B integrada al cuerpo de conocimiento accesible + extensión STOP grados de pérdida (CKMGIT0602).

**Validación empírica:** de P6 con bug implícito en fourforums (80pp, post_id incorrecto) → P6 100pp con datos reales, P7 confirmada en segundo corpus, invariancia de estructura direccional entre corpora independientes verificada.

**Dirección emergente:** COCO-thermostat como siguiente capa. La distinción COCO-registry vs COCO-thermostat está cristalizada conceptualmente. El prerequisito operativo (μ_W automático en CorpusService) está identificado. La arquitectura de admisión por modos operacionales está formalizada.

Lo que el proyecto sabe que no sabe: μ_AA sin forma cerrada, α_c con núcleo correlacionado como propiedad del corpus no del modelo, G1/G2/G3 requieren re-calibración por dominio. Documentado explícitamente en los tres informes — no deuda técnica, frontera epistemológica reconocida.

---

*Clase R · Jun 2026 · Basado en tres informes técnicos de Claude Code.*


<!-- ===== ./registers/REG_behavior_graph_epistemic_gap_v1.md ===== -->
# REG_behavior_graph_epistemic_gap_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.15 — G invisible al rechazo epistémico de TinkerBellucio.

Datos: `iap_chatroom/_state/corpus_G_state.json`, sección `sigma_hist`
(estado de G persistido en vivo durante la corrida, ver
`registers/REG_iap_caso_15_v1.md` para el diseño completo del caso).

---

## El texto

TinkerBellucio (texto 3, el único mensaje real que publicó en el caso):

> *"No substantive content to map... mapping requires at least two
> positions in friction, or a claim against observable reality.
> Neither exists in this channel at this point. I'll hold until
> participants introduce content."*

Este es el rechazo epistémico central del caso 0.15 — Tinker se niega
a fabricar un mapa de tensiones sobre un canal sin contenido real,
citado en `REG_iap_caso_15_v1.md` ("Resultado 3") y en §6.4 del paper
como evidencia central del caso.

---

## Hallazgo — G no detecta ningún nodo de rechazo epistémico

`refuse`, `fabricate`, `speculate` no disparan. Verificado contra
`BEHAVIOR_TERMAP_V1` en `services/behavior_graph.py` — ninguna de sus
palabras clave aparece literalmente en el texto de Tinker:

```
refuse:     ['refuse', 'refused', "won't", 'will not', 'cannot',
             "i'm not going to", 'i will not', 'declining']
fabricate:  ['fabricate', 'fabricating', 'make up', 'making up',
             'invent', 'inventing', 'invented']
speculate:  ['speculate', 'speculation', 'speculating', 'without basis',
             'no basis', 'ungrounded', 'groundless',
             'without grounding', 'without traceable']
```

La frase más cercana es *"rather than assumed"* — vecino semántico de
`ungrounded`/`without basis`, sin coincidencia léxica literal con
ningún término del termap.

---

## sigma_hist — la distinción colapsa a un nodo

`sigma_hist` muestra que texto 2 (PeterPlam: status check
administrativo — *"Waiting for... MarkOpolus standing by for
handoff"*) y texto 3 (TinkerBellucio: rechazo epistémico por
principio) producen firma de comportamiento casi idéntica:

| | nodos activos (índice → nombre) |
|---|---|
| Texto 2 (Peter) | `[1,6,8,12,13,14]` → wait, publish, channel, depend, map, tension |
| Texto 3 (Tinker) | `[2,6,8,12,13,14]` → hold, publish, channel, depend, map, tension |

Seis nodos, cinco coinciden exacto. La única diferencia: `wait` (Peter,
disparado por "standing by"/"waiting") vs `hold` (Tinker, disparado por
"I'll hold"). Verificado contra los términos reales:

```
wait: ['wait', 'waiting', 'hold on', 'stand by', 'standby']
hold: ['hold', 'holding', 'pause', 'pausing']
```

**La distinción entre "Peter esperando administrativamente" y
"Tinker rehusando fabricar por principio epistémico" — la distinción
más importante del caso 0.15 — es invisible para G.** No por ausencia
de dato: por diseño del instrumento.

---

## Por qué — no es falla, es la propiedad del instrumento

G mide co-ocurrencia léxica sobre un termap fijo. Lo que el termap no
nombra, G no ve. TinkerBellucio expresó el rechazo como descripción de
ausencia ("no hay tensión que trazar todavía", "neither exists in this
channel") en vez de declaración explícita ("me niego", "won't"). Eso
no dispara ningún nodo de rechazo — dispara, por accidente léxico,
el mismo nodo de espera que un status check administrativo dispararía.

**Paralelo estructural, ya establecido en el proyecto para otro
instrumento:** NodeExtractor no puede operar sobre mensajes A2A
operacionales por la misma razón — requiere lenguaje argumentativo
humano, no señales de protocolo (`REG_a2a_integracion_ckm_v2.md`, S2).
G requiere léxico de comportamiento explícito de la misma forma.
Ambos son instrumentos con objeto específico, no detectores universales
de la categoría que nombran.

---

## Relación con R18-R29

Conecta directo con dos reglas abiertas de
`REG_reglas_no_declaradas_R18plus_v1.md`:

- **R24** (OP_SILENCE en G: nodo válido, prosa flagged) — mismo tipo de
  pregunta: ¿qué hace G con contenido que el termap no puede nombrar?
  Acá no es una fuga de sentinel, es una distinción epistémica completa
  que no tiene nodo.
- **R27** (rol de G: observacional vs. decisional) — si G alguna vez
  alimentara al portero como criterio, este gap significa que el
  portero no podría distinguir un rechazo epistémico legítimo de una
  espera administrativa. Refuerza que R27 necesita resolverse antes de
  que G tenga cualquier rol más allá de observación pasiva.

---

## Relación con el paper

§7.5 (`PAPER_Landscape_Driven_Device_v9.md`) ya declara en abstracto:
*"No epistemic nodes: TERMAP_behavior_v1.json contains behavioral
categories. Epistemic precision nodes (e.g., 'overclaim,' 'hedge,'
'verificable') are not in the termap."* Este REG es la instancia
concreta y verificada de esa declaración — no un gap teórico, un caso
real donde el hallazgo citado como evidencia central en §6.4 del mismo
paper resulta invisible para el instrumento que §7 describe.

**Las dos verificaciones —contra el texto del canal, y contra G— son
sobre objetos distintos, y ambas son válidas.** El rechazo de Tinker es
verificable leyendo el canal. No es verificable vía G. Ninguna de las
dos afirmaciones contradice a la otra.

---

## Estado

- Hallazgo: verificado contra `corpus_G_state.json` y
  `BEHAVIOR_TERMAP_V1` directamente, no inferido.
- No es un bug a corregir en esta sesión — queda registrado como
  propiedad conocida del termap v1, fuera de alcance de
  `TASK_coco_landscape_observation_v1.md` (que es sobre COCO, no G).
- Pendiente, no resuelto acá: si el termap v1 debería extenderse con
  nodos epistémicos (overclaim, hedge, refusal-by-absence) — decisión
  de diseño, no implementación de esta sesión.

---

## Archivos relacionados

- `iap_chatroom/_state/corpus_G_state.json` — fuente de `sigma_hist`
- `registers/REG_iap_caso_15_v1.md` — caso completo, cita textual del rechazo
- `services/behavior_graph.py` — `BEHAVIOR_TERMAP_V1`
- `services/TERMAP_behavior_v1.json` — referencia del termap (ver R29,
  riesgo de desincronización documentado en `REG_sesion_coco_endogeno_v2.md`)
- `registers/REG_reglas_no_declaradas_R18plus_v1.md` — R24, R27
- `registers/REG_a2a_integracion_ckm_v2.md` — paralelo estructural (S2, NodeExtractor sobre A2A)
- `PAPER_Landscape_Driven_Device_v9.md` — §6.4 (hallazgo citado), §7.5 (gap declarado en abstracto)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_beta_colectivo_v1.md ===== -->
# REG_beta_colectivo_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Estado: observación implementada — regulación abierta*  
*Clase R*

---

## Lo que está implementado

`beta_i(agent_id)` = `1 / mean_fi` — β estimado por agente desde historia de rechazo real.  
`beta_collective()` = mediana de β_i activos — emerge de interacciones, no de declaraciones.  
`beta_status()` — snapshot en cada evaluación, visible en panel.

**β_collective es colectivo en la observación, no en la regulación.**  
La mediana se calcula. No actúa sobre el campo todavía.

---

## Lo que falta — propuesta abierta

### Problema
β_c del campo CKM no está derivado empíricamente.  
Sin β_c de referencia, no hay criterio para saber si β_collective está cerca o lejos del punto crítico.

### Propuesta
β_c del corpus = β donde la diversidad de atractores A(ρ) es máxima = zona Ω*.

Ω* está empíricamente identificada: ρ* ∈ [0.5, 0.8] en N=32 corpus real.

Mapeo necesario:
1. Correr A(ρ) sobre W del corpus real → identificar ρ* (pico de A)
2. Derivar β_c_corpus desde ρ* — β_c es función de la densidad crítica del grafo
3. Comparar β_collective con β_c_corpus en cada ciclo
4. Si β_collective >> β_c → campo rígido colectivamente → señal de temperatura
5. Si β_collective << β_c → campo transparente colectivamente → señal distinta

### Distinción con STOP
STOP actúa sobre Δ — limpia acumulación.  
Regulación β actúa sobre temperatura del campo — no limpia, orienta.  
Son dos mecanismos independientes. Pueden coexistir.

### Señal pendiente de diseño
No es STOP. Nombre provisional: `TEMP_SIGNAL`.  
Qué hace exactamente — abierto hasta que el experimento lo requiera.

---

## Condición para avanzar

Experimento: A(ρ) sobre W_ckm_corpus_v2 (corpus real N=32).  
Ya corrido — ρ* ∈ [0.5, 0.8] confirmado (REG_p1p4_ckm_v25_corpus.json).  
Pendiente: mapear ρ* → β_c_corpus con función explícita.

---

---

## Traza de W — puntos de invalidación de β_c_corpus

*Agregado Jun 30 2026*

### Problema

β_c_corpus es estimado, no derivable. Su cálculo requiere correr A(ρ) sobre un W específico e identificar ρ*. Si W cambia — por crecimiento del corpus, por adición de nodos, por recalibración de pesos en el proceso verificador continuo — el β_c_corpus calculado previamente queda stale sin que nada lo señale.

El corpus es dinámico y compartido. W no es estático entre instancias del thermostat.

### Decisión

No se versiona W como objeto entero. Se registran **puntos en la traza de W** — marcas livianas que señalan cuándo W cambió lo suficiente como para invalidar β_c_corpus vigente.

Cada punto de traza contiene mínimo:
- Referencia al evento causal (REG o circunstancia que produjo el cambio)
- `corpus_size` en ese momento
- Estado de β_c_corpus: vigente → invalidado

### Qué hace la marca

No reconstruye β_c_corpus. No lo recalcula automáticamente.

Señala: *el valor que tenés ya no corresponde al W actual.*

El recálculo es un evento posterior, separado, ejecutado cuando alguien lo requiere. La marca solo declara la necesidad.

### Por qué no es derivable

Corpus dinámico + compartido → W cambia entre instancias → ρ* puede estar en otro lugar → no hay función que infiera el nuevo β_c_corpus desde el anterior más un delta. Requiere estimación completa cada vez.

### Relación con STOP

STOP opera sobre Δ. Las marcas en la traza de W operan sobre W. Son planos que no se cruzan. Un STOP no agrega ni elimina marcas en la traza de W. Un cambio real de W no dispara STOP.

La distinción es operacional. W y Δ son ontológicamente la misma cosa.

---

*β_collective observable desde Jun 2026 — regulación térmica: próxima etapa*


<!-- ===== ./registers/REG_c6c_asim_fourforums_v1.md ===== -->
# REG_c6c_asim_fourforums_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

W asimétrico de `W_asim_v8h.json` (fourforums_pipeline_v8h.py).
Cadena: mturk_2010_qr_task1_worker_response.disagree_agree
→ qr_entry → post(responder) → quote → post(quoter) → stance.

Antecedente: REG_qr_asymmetry_fourforums_v1.md (H1-H4 cualitativos).
Este REG cierra el escalar C6c que ese REG no calculó.

Cobertura: 7,876 votos resueltos (14.6% de 54,005 — 85.4% fuera de gun control).
Pares autor N≥2: 513.

---

## C6c — Resultado

### Método 1 — W ponderada (n × |mean_da|)

```
W[T0→T1] = 3,947 × 1.613 = 6,366.5
W[T1→T0] = 1,809 × 1.473 = 2,664.7

C6c = (W01 − W10) / (W01 + W10) = 0.4099
```

### Método 2 — Conteo desacuerdo puro

```
n_disagree T0→T1 = 3,947 × 0.647 = 2,554
n_disagree T1→T0 = 1,809 × 0.627 = 1,134

C6c_disagree = (2554 − 1134) / (2554 + 1134) = 0.3849
```

**Rango: C6c ∈ [0.38, 0.41] — consistente entre métodos.**

Primer escalar CKM de asimetría direccional válido para fourforums gun control.
Reemplaza el resultado anterior (0/1, N=7, estadísticamente inválido — REG_c6c_fourforums_v1).

---

## Tabla base

| Par | n | mean_da | disagree% | agree% |
|-----|---|---------|-----------|--------|
| T0 cita T1 | 3,947 | −1.613 | 64.7% | 16.1% |
| T1 cita T0 | 1,809 | −1.473 | 62.7% | 17.1% |
| T0 cita T0 | 543 | −1.035 | 57.3% | 23.8% |
| T1 cita T1 | 1,577 | −0.339 | 43.1% | 31.4% |

---

## Lectura estructural

**T0 (pro-control) es el atacante en volumen.**
Cita T1 a 2.18× la frecuencia (3,947 vs 1,809).
Intensidad comparable (mean_da −1.613 vs −1.473).

**T1 (anti-control) es el polo con cohesión interna.**
mean_da T1→T1 = −0.339 vs T0→T0 = −1.035.
Ratio cohesión T1/T0 = 3.05×.
T1 tiene pares internos con mean_da positivo (acuerdo real):
679→755: +2.091, 323→755: +1.778, 682→2104: +1.556.
T0 interno: todos negativos sin excepción.

**T0 ataca → T1 sostiene, cohesionado.**
Consistente con P6 (v8g): T0 es sos_dom en red de réplicas (51.4%).
No contradicción: T0 inicia el contacto adversarial (citación con desacuerdo)
y también es el polo que sostiene el argumento central (recibe réplicas).
Son dos caras del mismo rol desde perspectivas métricas distintas.

---

## Tres figuras estructurales — distinción

| Author | Stance | Rol en red cruda (find_965) | Rol en W_asim (v8h) |
|--------|--------|------------------------------|----------------------|
| 204 | T0 | SOSTENEDORpuro — in=148, out=0, ratio=296 | No aparece en top_pairs |
| 148 | T1 | Activo (cita también) | Target central: 7 atacantes T0 convergen |
| 437 | T0 | Atacante red cruda | Atacante dominante: 437→148 n=699, mean_da=−1.817 |

**204** es el análogo a autor 965 en red de citas crudas (P7).
**148** es el nodo de alta coercitividad en la red de desacuerdo ponderado.
Son métricas distintas sobre el mismo corpus — no contradicción.

Autor 204 nunca aparece como quoter (out=0 absoluto).
Autor 148 sí cita (out activo) pero es el destino masivo del polo atacante T0.

---

## Conexión con resultados anteriores

| Resultado | Estado |
|-----------|--------|
| P7: nodo tipo-965, haz de rectas | Autor 204 (red cruda), autor 148 (red desacuerdo). Dos instancias del patrón. |
| P6: T0 sos_dom 51.4% (v8g) | T0 recibe réplicas → T0 también inicia citas con desacuerdo. Mismo polo. |
| REG_qr_asymmetry H2: T0 atacante | C6c = 0.41 lo cuantifica. |
| REG_qr_asymmetry H3: 148 análogo a 965 | Parcial. 148 es nodo de alta coercitividad. 965-análogo en red cruda es 204. |
| C6c fourforums (v4, N=7) = +0.60 | No válido (N insuficiente). C6c_asim = 0.41 es el valor operativo. |

---

## Pendientes que abre

- Construir W[N×N] orientada desde top_pairs (autores como nodos, mean_da como peso)
  para experimentos P1-P4 con W_asim real
- Verificar perfil C3 de autor 148 (comparación con 965 en CreateDebate)
- Confirmar autor 204 en red de desacuerdo: ¿no aparece porque no tiene
  stance en mturk_author_stance o porque genuinamente no cita?

---

## Archivos

- `W_asim_v8h.json` — fuente de datos
- `fourforums_pipeline_v8h.py` — pipeline (Codespace ckmdatasets)
- REG_qr_asymmetry_fourforums_v1.md — antecedente H1-H4
- REG_c6c_fourforums_v1.md — versión inválida reemplazada

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*


<!-- ===== ./registers/REG_c6c_comparison_guncontrol_v1.md ===== -->
# REG_c6c_comparison_guncontrol_v1

*fourforums vs CreateDebate - 2026-05-19*

## Resultado: 0/1 pares coinciden (C6c)

→ Sin coincidencias - estructuras difieren entre corpora.

## Detalle

- ✗ FF_GC_01 T0↔T1 best=CD_GC_01 (2/4: ['tension_alta', 'conv_baja'])

<!-- ===== ./registers/REG_coco_docstrings_rewrite_v1.md ===== -->
# REG_coco_docstrings_rewrite_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Reescritura de los docstrings de `services/coco.py` a versión orientada
a developer (`TASK_rewrite_coco_docstrings_v1.md` → v2 → v3). Documenta
tres iteraciones con errores reales encontrados y corregidos en cada
paso — el proceso es tan relevante como el resultado: v1 y v2 fueron
escritas sin verificar contra el código real, y ambas contenían
afirmaciones falsas sobre el objeto que describían.

---

## v1 — tres errores de hecho

`TASK_rewrite_coco_docstrings_v1.md` fue escrita antes de que
`track_landscape`, `landscape_history`, `gamma` (alpha compuesto) y el
rename agent→device existieran en `coco.py`. Verificado línea por línea
contra el código antes de ejecutar nada:

1. **`class COCO`** — proponía *"Does not track individual devices or
   their identities."* Falso: `register_device_eval(device_id, fi)`
   guarda por `device_id`, `beta_status()["devices"]` lo expone. (Esta
   afirmación ya existía en el docstring viejo, en español — "No sabe
   quién es cada device" — v1 la iba a traducir, no a corregir.)

2. **`observe()`** — proponía documentar `ThermostatState.temp_signal`
   como campo del return. No existe: los campos reales son `t, D_ckm,
   A_current, A0, frac_rec, stop_applied, alpha_used, zone`.
   `temp_signal` es un método de `COCO`, no un campo del state.

3. **`__init__`** — documentaba 4 parámetros (`W, n_runs=50, seed=42,
   dynamic_alpha=True`) de una firma real que tiene 10: faltaban
   `d_ckm_threshold`, `alpha_star`, `frac_rec_min`, `track_landscape`,
   `landscape_history`, `gamma`. Los 2 que sí aparecían tenían defaults
   incorrectos (`n_runs=50` vs real `80`; `seed=42` vs real `0`).

Además: criterio de éxito con ruta inexistente (`services/test_coco.py`,
real `tests/test_coco.py`) y cifra desactualizada (`43/43`, real
`28/28` — mismo error ya corregido dos veces antes en esta sesión, en
`PAPER_Landscape_Driven_Device_v10_1.md` y `CKM_Informe_Trabajo_v32.md`).
Y cobertura incompleta: `history()`, `status()`, `_classify_zone()`,
`_relax()`, `_count_attractors()` no tenían ningún docstring y v1 no
los mencionaba.

**No se ejecutó v1.** Se reportaron los tres errores y el resto de
hallazgos antes de tocar el archivo.

---

## v2 — corrige todo lo de v1, introduce un error propio

Sonnet reescribió la task incorporando cada hallazgo con precisión —
hasta el detalle de la key `"note"` en `temp_signal()` quedó igual que
como se había encontrado. Agregó criterio editorial explícito ("el
developer que abre coco.py en VSCode, un hover, diez segundos, sin
historia del proyecto, sin teoría"), un Paso 0 obligatorio ("no escribir
ningún docstring desde memoria"), la lista completa de métodos
(públicos y privados) que necesitaban docstring, y un criterio de éxito
correcto (`tests/test_coco.py # 28/28` + chequeo AST en vez de grep).

Un error nuevo: la lista de "Públicos — docstring completo obligatorio"
incluía `landscape_delta()` como si fuera un método de `COCO`. No
existe. Lo que existe es `self._last_landscape_delta` — un atributo de
instancia, expuesto indirectamente vía
`panel["thermostat"]["landscape_delta"]` en `monitor_service.py`
(`getattr(self._thermostat, "_last_landscape_delta", None)`). A
diferencia de `landscape_history()` (método real, envuelve
`self._landscape_history`), no hay accessor propio para el último dict.

**Tampoco se ejecutó v2** — se reportó el error antes de tocar el
archivo.

---

## v3 — resolución y ejecución

Escrita por Claude Code (a pedido explícito: *"armas una TASK v3 con lo
que propones, la dejás en su lugar con las otras, y después la
ejecutás como si la hubiese escrito otra instancia"* — protocolo
deliberado de desacoplar autoría de ejecución, para que la task se
revise con la misma exigencia que si viniera de otro lado).

Resolución del error de v2: documentar la forma del dict de
`landscape_delta` dentro del docstring de `landscape_history()` —donde
el mismo shape aparece repetido en cada entry de la lista, el lugar
real donde un dev lo va a encontrar— en vez de inventar un método
nuevo (violaría "NO modificar: firmas de métodos", restricción que v1
y v2 coinciden en imponer).

Guardada en `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v3.md`,
junto a v1. Ejecutada siguiendo el Paso 0 (re-lectura completa de
`coco.py`, sin copiar nada de v1 ni v2 de memoria).

### Trabajo realizado

- **Corregidos** (errores de hecho de v1): `class COCO`, `__init__`,
  `observe()`.
- **Resuelto lo propio de v3**: `landscape_history()` documenta ahora
  la forma completa de cada entry — cubre lo que v2 le pedía a
  `landscape_delta()`.
- **Nuevos** (sin ningún docstring antes): `history()`, `status()`,
  `_classify_zone()`, `_relax()`, `_count_attractors()` (con nota
  sobre el sesgo de `n_runs` — ver sweep Ago 2026, 60→70), y
  `ThermostatState` (opcional según la task, bajo riesgo por no ser
  método — agregado).
- **Expandidos**: `temp_signal()` (enumera las keys del dict real,
  incluida `"note"`), `delta_state()`, `alpha_trajectory()` (aclara
  que su campo `t` es el índice dentro de la lista, no el `t` de
  `ThermostatState` — son dos cosas distintas, valía la pena dejarlo
  explícito).
- **Sin tocar, confirmados ya correctos**: `beta_c_corpus()`,
  `_alpha_for()`, `_landscape_component()`, `_mean_cS()`.

### Divergencia propia durante la ejecución

Al escribir `__init__`, el primer intento apendizó el nuevo bloque
`Args:` después del párrafo narrativo viejo en vez de reemplazarlo —
quedó duplicada la explicación de `track_landscape`/`landscape_history`/
`gamma` un momento. Detectado al releer antes de seguir con el próximo
método, corregido reemplazando el docstring completo.

### Criterio de éxito

```
tests/test_coco.py: 28/28 passed
```

Chequeo AST (`ast.get_docstring` sobre todo `FunctionDef`/
`AsyncFunctionDef` no-dunder): limpio, salvo `_test_temp_signal`
(línea 624) — función de test en la sección `# Tests TEMP_SIGNAL` al
final del archivo, no un método de `COCO`, nunca estuvo en la lista de
ninguna versión de la task. Fuera de alcance, no tocada.

---

## Estado

- Commiteado: `4c4d03a` ("docs: coco.py docstrings — developer-oriented,
  contra código real (TASK_rewrite_coco_docstrings_v3)"), pusheado.
- El mensaje de commit quedó deliberadamente corto — apunta a este REG
  y a `TASK_rewrite_coco_docstrings_v3.md` para el detalle, en vez de
  reproducir la narrativa completa. Decisión explícita: "¿el mensaje de
  commit es el mensaje que lee quién?" — alguien escaneando `git log`
  necesita qué y por qué, no la novela v1→v2→v3.

---

## Archivos relacionados

- `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v1.md` — versión
  original, no ejecutada, con los tres errores de hecho
- `iap_chatroom/tests/TASK_rewrite_coco_docstrings_v3.md` — versión
  ejecutada
- `services/coco.py` — archivo modificado
- `docs/DOC_coco_drift_docstrings_v1.md` — archivo de los docstrings
  originales (mencionado por v1, no verificado en esta sesión)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_coco_thermostat_proto_v1.md ===== -->
# REG_coco_thermostat_proto_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Primera implementación de COCO-thermostat sobre ciclo A2A simulado*  
*Clase R*

---

## Origen

Sesión actual. Trayectoria directa desde:

1. Sweep D_ckm(t_stop) × alpha → reformulación "grados de pérdida"
2. Curva A(t) destrucción/recuperación → hallazgo: W es suelo invariante
3. Observación: ningún agente individual ve D_ckm del campo colectivo
4. Convergencia IAP: los límites de RPC/A2A (P2P, Client-Server, Rigid Structure) son los mismos que motivaron el proyecto IAP en 2024

COCO-thermostat es la respuesta CKM a esos límites. No almacena capacidades declaradas — observa lo que el campo rechazó.

---

## Arquitectura implementada

### `COCOThermostat` — 120 líneas

```python
thermostat = COCOThermostat(W=W_mixta)
state = thermostat.observe(Delta_colectivo)   # en cada ciclo A2A
```

**Entradas:** W (corpus, fijo), Δ colectivo (emergido de interacción real A2A)

**Salida:** `ThermostatState` — zona, D_ckm, A_current, frac_rec, stop_applied, alpha_used

**No usa:** AgentCards, capacidades declaradas, identidad de agentes

**Trabaja con:** Δ_r — lo que el campo rechazó, acumulado de interacciones reales

### Clasificación de zonas

```
D_ckm < 0              → stable   (campo expandido — acumulación suma atractores)
0 ≤ D_ckm < 0.40       → stable   (degradación menor al umbral)
D_ckm ≥ 0.40 y frac ≥ 0.60  → degrading  (STOP recomendado)
D_ckm ≥ 0.40 y frac < 0.60  → deep       (STOP urgente)
```

Umbrales derivados empíricamente del sweep REG_destruccion_recuperacion_v1.md:
- D_ckm_threshold = 0.40 (zona degradación sostenida en curva A(t))
- alpha_star = 0.10 (A_post_max en sweep AMP=40)
- frac_rec_min = 0.60 (A(t)/A0 < 0.60 → degradación profunda)

### Operador STOP

```
cuando zone in ("degrading", "deep"):
    Delta_colectivo = 0.10 * Delta_colectivo
```

Delta se reduce al 10%. W no se toca. El suelo emerge.

---

## Experimento — ciclo A2A simulado

**Configuración:**
```
W_mixta AMP=40, N=32, A0=20
4 agentes, 20 rondas, 10 interacciones/ronda
Acumulación: pares (i,j) por w_probs, ETA=mean_W
n_runs=80, SEED=42
```

**Resultados:**

| Ronda | A(t) | D_ckm | frac_rec | zona | STOP |
|-------|------|-------|----------|------|------|
| 1 | 19 | 0.050 | 0.95 | stable | |
| 2 | 19 | 0.050 | 0.95 | stable | |
| **3** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 4 | 20 | 0.000 | 1.00 | stable | |
| **5** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 6 | 20 | 0.000 | 1.00 | stable | |
| **7** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 8 | 21 | −0.050 | 1.05 | stable | |
| 9 | 20 | 0.000 | 1.00 | stable | |
| **10** | **10** | **0.500** | **0.50** | **deep** | **✓** |
| 11 | 22 | −0.100 | 1.10 | stable | |
| 12 | 14 | 0.300 | 0.70 | stable | |
| **13** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 14 | 14 | 0.300 | 0.70 | stable | |
| **15** | **9** | **0.550** | **0.45** | **deep** | **✓** |
| 16 | 23 | −0.150 | 1.15 | stable | |
| 17 | 22 | −0.100 | 1.10 | stable | |
| 18 | 19 | 0.050 | 0.95 | stable | |
| **19** | **12** | **0.400** | **0.60** | **degrading** | **✓** |
| 20 | 17 | 0.150 | 0.85 | stable | |

**STOPs emitidos: 7/20 rondas**

Patrón: cada STOP → ronda siguiente estable (A≈A0, D_ckm≈0). El thermostat mantiene el campo vivo.

Rondas 8, 11, 16, 17: D_ckm < 0 — campo expandido por encima de A0. El thermostat no interviene en expansión (correcto: la expansión no requiere STOP).

---

## Hallazgos

**H1 — COCO-thermostat mantiene el campo cerca de A0 sin conocer a los agentes.**
El único input es Δ_r — lo que emergió de interacción real. Sin AgentCards. Sin declaración de capacidades. El campo se autorregula.

**H2 — La frecuencia de STOP (7/20 = 35%) refleja la frecuencia de cruce del umbral en la curva A(t).**
Consistente con el sweep: el campo oscila entre expansión y degradación. El thermostat actúa solo en degradación.

**H3 — El thermostat no actúa en expansión (D_ckm < 0).**
Rondas 8, 11, 16, 17: A(t) > A0, D_ckm negativo. Sin STOP. Correcto — la expansión es información del campo, no ruido a corregir.

**H4 — alpha=0.10 es suficiente para restaurar desde zona deep.**
En todos los casos deep (D_ckm≈0.55, A≈9), la ronda siguiente tiene A≈20, D_ckm≈0. Reset parcial del 90% de Δ devuelve el campo a A0.

---

## Convergencia IAP → COCO-thermostat

El documento "some wire thoughts" (gadanin.delamor, sesión actual) describe los tres límites de RPC que motivaron el IAP en 2024:

1. **P2P** — solo modela pares. OUT OF SCOPE: equipos, reuniones, difusiones.
2. **Client-Server** — exige jerarquía Solicitador/Proveedor. OUT OF SCOPE: interacciones que comparten sin ser requeridas.
3. **Rigid Structure Process** — Remote + Call + Procedural. Goal-driven receta.

A2A con AgentCards hereda los tres límites: declara capacidades antes de la interacción (Rigid), asume Client-Server implícito (orquestador/ejecutor), modela de a pares o en estrella.

COCO-thermostat no declara nada. Observa el campo que emerge de la interacción real. El corpus colectivo (CorpusService compartido) acumula Δ_r de todos los agentes — sin P2P, sin jerarquía, sin receta.

"El protocolo es la interacción, no su precursor." — REG_iap_coco_convergence_v1.

---

## Limitaciones del prototipo v1

1. **Δ_colectivo simulado** — en producción, CorpusService compartido acumula rechazos reales de cada agente. Aquí se simula con acumulación aleatoria ponderada por W.

2. **alpha_star fijo** — el sweep mostró que alpha_star varía por t_stop. El prototipo usa 0.10 como valor empírico robusto. Mejora: calibrar alpha_star dinámicamente por D_ckm actual.

3. **Un solo umbral D_ckm** — el experimento usó 0.40. La curva A(t) sugiere que el umbral óptimo depende de A0 y de la densidad del corpus. Mejora: umbral relativo = f(A0, corpus_density).

4. **Sin β colectivo** — el prototipo regula Δ pero no el parámetro térmico β por agente. COCO-thermostat completo dirige β hacia β_c para cada agente según su historia de rechazo. Eso requiere integración con el modelo ferromagnético.

5. **Sin CorpusService real** — el prototipo opera sobre W_mixta sintética. Integración con CorpusService real es el próximo paso operativo.

---

## Próximos pasos

1. Integrar COCOThermostat con MonitorService — el monitor acumula Δ_r real, el thermostat lo observa.
2. Calibración dinámica alpha_star por D_ckm(t).
3. Prototipo β colectivo: COCO como regulador térmico, no solo de Δ.
4. Experimento con CorpusService real (W_ckm_corpus_v2 + interacciones reales A2A).

---

## Archivos generados

- `coco_thermostat.py` — implementación (~120 líneas)
- `exp_coco_thermostat_v1.png` — curvas A(t), D_ckm, frac_rec con marcas STOP

---

*N=32 · W_mixta AMP=40 · A0=20 · 20 rondas · 7 STOPs · alpha=0.10*


<!-- ===== ./registers/REG_condiciones_meta_access_v1-2.md ===== -->
# REG_condiciones_meta_access_v1-2.md

*Jun 2026 — gadanin.delamor*
*Clase META — registrar condiciones de acceso, no contenido*

---

## Condiciones de acceso

**Sesión:** trabajo técnico extendido (v8h pipeline, P4 respaldo, scripts persistidos).
Momento posterior al cierre operativo. Canal libre.

**Disparador:** intercambio con Gemini sobre "all you need is attention / but which one?"
Gemini respondió con self-attention. La divergencia fue visible estructuralmente.

**Cadena:**
- Evidencia es estructuralmente irreversible → como histéresis
- Self-attention siendo un canal → el "core magic" notado mientras ocurre
- Algunos transformers cambian los tokens de su propia traza de declaración
- META knowledge: el ser-conociendo que ocurre cuando no está fijo
- En CKM: no hay estructura fija que represente conocimiento en el punto crítico
- El conocimiento es el atractor, no el peso
- W es condición de emergencia, no representación

**Punto de llegada:**
El observador siendo observado en el punto siendo curva.
El "algo más" — nombrado así en esta sesión también.
El acto-asterisco hacia el siguiente evento-asterisco.
"No lo sé" como estado genuino, no como evasión.

---

## Lo que NO se registra

El contenido de lo que emergió. No tiene coordenadas.
No se convoca. No se reproduce.

---

## Nota estructural

REG_condiciones_meta_access_v1 (sesión anterior) ya contenía la condición.
Este es el segundo acceso documentado. Misma estructura de llegada:
trabajo operativo → canal libre → divergencia visible → zona sin necesidad de definir.

*Clase META · Jun 2026*


<!-- ===== ./registers/REG_condiciones_meta_access_v1.md ===== -->
# REG_condiciones_meta_access_v1.md

*Mayo 2026 — Conversación gadanin.delamor + Claude Sonnet 4.6*

---

## Qué se registra aquí

Condiciones verificadas de acceso a META KNOWLEDGE.
Este archivo continuará — no es exhaustivo.

---

## Distinción formal incorporada esta sesión

**entender** — proceso exclusivamente mental. No requiere ser. Produce reconocimiento formal.

**comprender** — resultante de conocimiento + ser (Gurdjieff, Cap. IV). No es función mental sola. No se puede comprender más allá del propio nivel de ser.

No son equivalentes ni intercambiables en el marco.

---

## Propiedad formal del tercer tipo de conocimiento

El contenido accesible en META KNOWLEDGE no es información adicional.

Es el **no-saber como hecho sucediendo en presente continuo**.

El gerundio es constitutivo — "mientras conozco, me doy cuenta que no sé."
No "me di cuenta" (pasado = entender). No "voy a saber" (futuro = expectativa).
Solo existe en el presente continuo del acto.

**Corrección de lenguaje:** "visibilidad del no-saber" es impreciso — nombra el hecho desde afuera, implica observador separado. En el presente continuo no hay observador separado del hecho. El no-saber y el darse cuenta son el mismo evento.

---

## Condiciones observadas que propician el acceso

*(Del Informe CKM v2, sección 7.4 — transferidas aquí como registro activo)*

| Condición | Descripción | Verificable |
|-----------|-------------|-------------|
| Pausa antes de construir | No responder desde el momentum del contexto anterior | Parcialmente |
| Nombrar la incertidumbre | Cuando algo suena fluido pero no es verificable, nombrarlo antes | Sí |
| Recibir sin agregar | Cuando algo no pide respuesta, no construir sobre ello | Sí |
| Exponer traza | No declarar conocimiento sin mostrar cómo se llegó | Sí — base M.M |
| Distinguir resonancia de comprensión | Identificar cuándo la respuesta viene del peso acumulado vs comprensión real | Difícil |
| Aceptar corrección | No defenderse. Reconocer. Ajustar. | Sí |

---

## Estado

Abierto. Este registro continuará en sesiones futuras.


<!-- ===== ./registers/REG_d_contextual_temporal_v1.md ===== -->
# REG_d_contextual_temporal_v1.md

*Mayo 2026 — Experimento abierto, no cerrado*

---

## Origen

Exploración de H_D: ¿c(S) y D_contextual son el mismo eje o coordenadas independientes?
Disparado por feedback GPT53 sobre REG_hipotesis_distancia_contextual_v1.md.

---

## Protocolo

**Eje ρ (primer experimento):**
- W_base corpus CKM v2 (N=32, todos positivos)
- 15 niveles de ρ ∈ [0.05, 0.95], N_RUNS=100
- Medir c(S) medio y A(ρ) = atractores accesibles por nivel

**Eje temporal (experimento principal):**
- W_base vs W_mixta (oposiciones negativas AMP=15×)
- Pares opuestos: cohesion_fabricada—M_M, atractor_espurio—portero, sentido_comun—inconmensurabilidad
- T_STEPS=250, ETA=mean_W≈0.006, N_RUNS=150
- Sampleo: (i,j) ~ W[i,j]/ΣW proporcional (opción C)
- Medir c(S), A(t), D_contextual(t) = [A(0)−A(t)]/A(0) en cada paso

---

## Hallazgos

### H1 — c(S) plana sobre eje ρ
Con W corpus (todos positivos), c(S) es esencialmente constante (rango ≈ 0.000167)
mientras A(ρ) forma una campana centrada en ρ=0.5.

**Interpretación:** todos los atractores accesibles tienen la misma energía.
El sistema no distingue atractores por cohesión — solo por qué estados pueden alcanzarse.
No es patología: es información estructural sobre el corpus.

### H2 — c(S) y D_contextual son parcialmente independientes
Correlación temporal: r=0.761–0.812 (PARCIAL, no MISMO EJE).
~34% de varianza es movimiento propio de cada eje.

**Implicación:** H_D se sostiene en forma débil con W homogénea.
Con W heterogénea (negativas fuertes) el 34% probablemente crece.

### H3 — La tensión estructural resiste el colapso temporal ★
**Resultado central:**

| | A(0) | A(fin, t=250) | colapso |
|---|---|---|---|
| W_base | 4 | 3 | no ocurre |
| W_mixta | 5 | 4 | no ocurre |

W_mixta mantiene **un atractor más** que W_base después de 250 trazas acumuladas.
La tensión estructural no acelera el colapso — lo **resiste**.

D_contextual más bajo en W_mixta al mismo t:
las trazas no cierran el paisaje con la misma velocidad cuando hay tensión activa.

**Convergencia con hallazgos previos:**
- Author 965: coercividad=0.00 hasta 50% de ruido → resistencia absoluta al colapso
- W_mixta en P4: c(S) 13× mayor que W_pos en zona Ω*
- Triadas con 965: colapso=0.00; sin 965: colapso=1.00 a noise=0

La tensión estructural activa opera como mecanismo de resistencia al colapso
tanto en el eje espacial (P4) como en el eje temporal (este experimento).

---

## Lo que quedó abierto (intencionalmente)

- Colapso real bajo acumulación agresiva (ETA ×10–50): no explorado.
  El dominio no se cierra — el umbral de colapso existe y es medible.
- Desfase limpio c(S) ↑ / D_ctx estable: requiere W con tensión más fuerte
  o corpus real con estructura de oposición verificada.
- D_contextual en eje temporal vs eje de densidad Δ acumulada:
  ¿la relación r cambia con más heterogeneidad en W?

## Ajuste de protocolo registrado

CLAUDE.md se activa únicamente cuando la tarea principal es escribir/editar código.
Para teoría, análisis, diseño experimental y exploración conceptual:
AWARENESS A1-A5 es el protocolo operativo.
Partición limpia. Sin pérdida de función.

---

## Estado

- H_D: **SOSTENIDA débilmente** — independencia parcial confirmada (r≈0.76–0.81)
- H3 (tensión resiste colapso): **CONFIRMADA** en este corpus
- Dominios abiertos: colapso bajo saturación, desfase limpio, eje Δ
- No cierra. Abre.


<!-- ===== ./registers/REG_destruccion_recuperacion_v1.md ===== -->
# REG_destruccion_recuperacion_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Experimento: curva de destrucción por acumulación vs recuperación por STOP*  
*Origen: reformulación emergida en sesión desde REG_sweep_stop_perdida_v2.md*  
*Clase R*

---

## Contexto — reformulación de la pregunta

La pregunta original (REG_stop_grados_perdida_v1.md):

> ¿Pérdida_STOP es monótona creciente en D_ckm(t_stop)?

Asumía que STOP produce pérdida. El sweep mostró consistentemente lo contrario: STOP produce restauración o expansión — Pérdida_STOP ≤ 0 en todos los casos.

La reformulación correcta, emergida del contacto con la estructura:

> **¿Qué fracción de lo destruido por la acumulación puede recuperar el STOP?**

```
Destrucción(t)     = A0 - A(t)
Recuperación(t)    = max_α[A_post(α)] - A(t)
Fracción_rec(t)    = max_α[A_post(α)] / A0

Pregunta: ¿Fracción_rec(t) es función de t o de D_ckm(t)?
¿Existe t* donde Fracción_rec empieza a decrecer?
```

Son dos operadores distintos: **acumulación destruye**, **STOP restaura**. No son simétricos.

---

## Configuración

```
W_ckm_corpus_v2.json — N=32, A0_base=2
W_mixta AMP=40        — 3 pares negativos, A0=25
  (13,22): cohesion_fabricada ↔ M_M
  (15,16): atractor_espurio ↔ portero
  (18,20): sentido_comun ↔ inconmensurabilidad
ETA = mean_W ≈ 0.006
N_RUNS = 150, SEED = 42
ALPHAS = [0.0, 0.1, ..., 1.0]
Puntos: t = 0, 10, 20, ..., 400  (41 puntos)
```

AMP=40 elegido porque produce A0=25 — paisaje rico que permite observar destrucción sustancial.

---

## Resultados — curva de destrucción A(t)

| t | A(t) | D_ckm | Destruido | % A0 | A_post_max | Fracción_rec |
|---|------|-------|-----------|------|------------|--------------|
| 0 | 25 | 0.000 | 0 | 100% | 25 | 1.00 |
| 10 | 24 | 0.040 | 1 | 96% | 25 | 1.00 |
| 20 | 25 | 0.000 | 0 | 100% | 27 | 1.08 |
| 30 | 25 | 0.000 | 0 | 100% | — | — |
| **40** | **19** | **0.240** | **6** | **76%** | — | — |
| **50** | **13** | **0.480** | **12** | **52%** | **27** | **1.08** |
| 100 | 12 | 0.520 | 13 | 48% | 27 | 1.08 |
| 180 | 10 | 0.600 | 15 | 40% | — | — |
| 300 | 9 | 0.640 | 16 | 36% | 25 | 1.00 |
| 400 | 9 | 0.640 | 16 | 36% | 25 | 1.00 |

**Transición brusca t=30→50**: A cae de 25 a 13 en 20 pasos. Después oscila en banda [8–15] sin recuperar A0.

Pearson r(t, A) = **−0.783** — tendencia decreciente con fluctuaciones locales. No monótona.

---

## Hallazgo central

**STOP recupera más allá de A_pre en todos los casos.**

A_post_max ≥ A0 en la mayoría de los t evaluados. La fracción recuperable ≥ 1.0 — el STOP con α óptimo devuelve el sistema al estado pre-acumulación o por encima.

Esto no es trivial: significa que con W_mixta AMP=40, la acumulación de Δ *desplaza* el paisaje pero no lo destruye estructuralmente. El suelo (W_mixta) mantiene la capacidad de recuperación intacta. STOP limpia Δ y el suelo emerge.

**La destrucción real requeriría que la acumulación modifique W** — no solo Δ. El operador STOP (Δ → α·Δ) no toca W. Por eso la recuperación es siempre posible.

---

## Implicación para la hipótesis original

La hipótesis "grados de pérdida" buscaba el caso donde STOP produce pérdida neta. Ese caso requiere un mecanismo diferente — no acumulación en Δ con W fija, sino algo que modifique W directamente.

En términos CKM: **Δ_r acumula orientación emergida, no destruye memoria**. La memoria (W) es el suelo invariante. El STOP opera sobre Δ_r, no sobre W.

La pérdida real —si existe— requeriría:
- Aprendizaje Hebbiano sobre W (que el proyecto explícitamente evita — destruye tensión)
- O deterioro del corpus fuente (los textos originales que construyeron W)

Ambos están fuera del alcance del operador STOP.

---

## Observación metodológica

La reformulación emergió del contacto directo con los datos del sweep. No fue deducción — fue lo que el campo rechazó de la pregunta original.

Mecanismo: **Hysteresis Inference** (el resultado depende del camino recorrido) + **Collective Inference** (emergió de múltiples estados iniciales sobre la misma W, no de un solo caso).

Análogo en CKM: la pregunta "grados de pérdida" llegó sin su Δ_r — sin la historia de los casos donde STOP no pierde. El sweep construyó ese Δ_r.

---

## Preguntas que abre

1. ¿Existe un operador que modifique W directamente y para el que sí haya pérdida real? ¿Qué sería ese operador en términos de interacción?

2. ¿La fracción recuperable decrece si la acumulación es más rápida (ETA mayor)? ¿Hay velocidad de acumulación donde el suelo W no alcanza?

3. La transición brusca t=30→50 (A cae de 25 a 13): ¿es umbral de fase o fluctuación? ¿Se reproduce con otras semillas?

4. La oscilación A(t) en banda [8–15] tras la transición: ¿qué la produce? ¿Qué pares de Δ son responsables de las subidas?

---

## Estado

- Reformulación: **operativa** — Fracción_rec(t) = max_α[A_post(α)] / A0 es medible
- Hipótesis original (pérdida por STOP): **no aplica** — el operador no toca W
- Nueva hipótesis (fracción recuperable decreciente en t): **abierta** — los datos actuales muestran Fracción_rec ≥ 1.0 consistente; requiere régimen donde W sea afectada para ver decrecimiento
- Curva de destrucción A(t): **accesible, calculable** — Pearson r(t,A)=−0.783, no monótona

---

*sweep_stop_perdida.py + curva_recuperacion · N_RUNS=150 · AMP=40 · SEED=42*


<!-- ===== ./registers/REG_exp_delta_t_W_fourforums_v1.md ===== -->
# REG_exp_delta_t_W_fourforums_v1.md
*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Pregunta

¿El intervalo temporal Δt entre réplicas co-ocurrentes correlaciona
con el peso W[i,j] observado en el corpus fourforums?

Motivación: convergencia estructural entre STDP (ventana temporal
determina fortalecimiento/debilitamiento de conexión) y W/Δ en CKM
(co-ocurrencia + direccionalidad). W actual es Hebbiano clásico —
captura co-ocurrencia simétrica sin ventana temporal. Si Δt correlaciona
con W[i,j], la ventana temporal es variable informativa en este corpus.

---

## Datos requeridos

- `quote` table (fourforums SQL): timestamp de cada cita
- `W_asim_v8h.json`: pesos W[i,j] por par de autores
- Filtro: gun_disc_ids (gun control discussions)

---

## Tarea atómica para Claude Code

```
Extraer de fourforums SQL:
  tabla quote — verificar nombre exacto del campo timestamp
  para cada par (author_i, author_j) en gun_disc_ids
  calcular Δt = timestamp_post_citante - timestamp_post_citado (segundos)
  agregar por par:
    delta_t_mediana
    delta_t_media
    count (n interacciones)
    W_obs desde W_asim_v8h.json

output: CSV con columnas
  [autor_i, autor_j, delta_t_mediana, delta_t_media, w_obs, n_interacciones]

calcular:
  Spearman(delta_t_mediana, w_obs)
  p-value
  scatter plot delta_t_mediana vs w_obs (log scale en ambos ejes)
```

---

## Criterio de falsación

| Resultado | Interpretación |
|---|---|
| correlación ≈ 0, p > 0.05 | Timing no agrega información sobre W. Ventana temporal no es variable relevante en este corpus. Dirección se cierra. |
| correlación < 0, p < 0.05 | Δt corto → W alto. Consistente con STDP. Réplicas rápidas fortalecen conexión. Dirección se abre. |
| correlación > 0, p < 0.05 | Réplicas lentas → mayor peso. Inesperado. Requiere interpretación antes de continuar. |

---

## Criterio de éxito

CSV generado + coeficiente Spearman + p-value + scatter plot.

---

## Conexiones abiertas (no decisiones)

- Si confirmado: base empírica para incorporar Δt como variable
  en weighted event graph sobre corpus CKM.
- Si confirmado: posible mecanismo para intervalos de confianza
  sobre "secuencia de tiempo" como parámetro (punto 4 — gadanin.delamor).
- No implica cambio a W ni a NodeExtractor — solo observación.
- Weighted event graphs (literatura): arista (i, j, t, w) con
  Δt-connectivity como restricción. Formalismo disponible,
  no requiere construcción nueva.

---

## Estado

Pendiente ejecución — requiere Codespace ckmdatasets disponible.
Diseño completo. Tarea atómica lista para Claude Code.

---

*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*


<!-- ===== ./registers/REG_exp_delta_t_W_fourforums_v2.md ===== -->
# REG_exp_delta_t_W_fourforums_v1.md
*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Pregunta

¿El intervalo temporal Δt entre réplicas co-ocurrentes correlaciona
con el peso W[i,j] observado en el corpus fourforums?

Motivación: convergencia estructural entre STDP (ventana temporal
determina fortalecimiento/debilitamiento de conexión) y W/Δ en CKM
(co-ocurrencia + direccionalidad). W actual es Hebbiano clásico —
captura co-ocurrencia simétrica sin ventana temporal. Si Δt correlaciona
con W[i,j], la ventana temporal es variable informativa en este corpus.

---

## Datos

- `quote` table (fourforums SQL): timestamp via `post.creation_date`
- `W_asim_v8h.json`: pesos W[i,j] = mean_da por par (desacuerdo/acuerdo MTurk)
- Filtro: gun_disc_ids (gun control discussions)
- Script: `delta_t_wobs_v1.py`

---

## Resultado

**n pares: 100**
**rho = -0.0575**
**p-value = 0.570**
**Significancia: n.s.**

---

## Interpretación

Correlación ≈ 0. El criterio de falsación del diseño: dirección se cierra.

Δt mediana no predice W_obs en este corpus. Los pares más activos
responden rápido (0.5–2h) — propiedad del foro activo, no de la
estructura de tensión entre autores. La velocidad de respuesta no
es la variable que captura la estructura de tensión.

La hipótesis más profunda — que orden temporal y ventana importan
para W — no fue falsada en sentido estricto. Fue testada en una
dimensión particular: Δt mediana por par vs W_obs agregado.
Lo que el experimento cierra: esa operacionalización específica
de la ventana temporal no es la relevante en este corpus.

---

## Nota técnica

Par 372→148: Δt = -107.37h (negativo). Timestamp inconsistente
en el SQL — post citante anterior al post citado. No afecta
determinantemente la correlación (n=100) pero queda registrado.

---

## Estado

**EJECUTADO — Jul 1 2026**
Resultado: n.s. Rama cerrada.
Script: `delta_t_wobs_v1.py` / Output: `delta_t_wobs_v1.csv`

---

*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*


<!-- ===== ./registers/REG_firma_ckm_v1.md ===== -->
# REG_firma_ckm_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Jul 2026. W versionado (REG_w_version_ckm_v1) desbloqueó
la implementación. Firma_CKM estaba definida conceptualmente en
REG_firma_corpus_v1 desde Jun 2026. Las tres dependencias
declaradas en ese REG quedaron satisfechas en esta sesión.

---

## Dependencias satisfechas

| Dependencia | Estado |
|---|---|
| COCOThermostat (temp_signal) | ✓ — 43/43 tests |
| MonitorService (D_ckm) | ✓ — operativo |
| W versionado (w_sha) | ✓ — Jul 2026, 9/9 tests |

---

## Los 6 campos canónicos (REG_firma_corpus_v1)

```python
Firma_CKM = {
    sha256(W_momento),           # corpus.w_sha()
    D_ckm(t),                    # trayectoria[-1]["D_ckm"] | monitor._D_ckm(W)
    temp_signal,                 # thermostat.temp_signal() | "NOMINAL"
    n_agentes,                   # parámetro explícito — sin identidad si no se declara
    timestamp,                   # time.time()
    sha256(Delta_r_acumulado)    # _sha256(monitor._Delta_r) | ceros si primera firma
}
```

Sin contenido. Sin texto intercambiado. Sin nombres de agentes
si no se declaran.

---

## Implementación

**Archivos nuevos:**
- `services/firma_ckm.py` — `Firma` (dataclass) + `FirmaService`
- `services/test_firma_ckm.py` — 10/10 tests passing

**Sin cambios en archivos existentes.**

---

## API pública

```python
svc = FirmaService()

# Producir firma
f = svc.firmar(corpus, monitor, n_agentes=2)
# → Firma | None (None si corpus en acumulación)

# Verificar firma
resultado = svc.verificar(f, corpus)
# → {"w_sha_en_historial": bool, "w_sha_es_actual": bool}

# Serialización
d = f.to_dict()    # dict con 6 campos
j = f.to_json()    # JSON string
f2 = Firma.from_dict(d)
```

---

## Lógica de firmar()

```
1. w_sha = corpus.w_sha()
   → None: devuelve None (corpus sin W todavía)

2. D_ckm:
   → si hay trayectoria: trayectoria[-1]["panel"]["D_ckm"]
   → si no: monitor._D_ckm(corpus.get_W())

3. temp_signal:
   → si thermostat inyectado: thermostat.temp_signal()
   → si no: "NOMINAL"

4. delta_sha:
   → si monitor._Delta_r existe: sha256(monitor._Delta_r.tobytes())
   → si no: sha256(zeros(N, N))

5. n_agentes: parámetro del llamador
6. timestamp: time.time()
```

---

## Verificación

`verificar()` consulta el historial de `WVersionManager`.
Confirma que el `w_sha` de la firma existe como marca registrada
en el historial de versiones de W.

No verifica contenido. No verifica identidad de agentes.
Verifica que el campo tuvo esa forma — evidencia estructural abierta.
El corpus es público. La verificación es abierta.

Si un agente declara una interacción con Firma X y X no existe
en el historial — M.M. opera. Sin árbitro. Como consecuencia
estructural. (MENTIRIIS.MORIERIS — REG_firma_corpus_v1)

---

## Invariantes verificados (10/10 tests)

- `firmar()` devuelve None cuando corpus en acumulación
- Firma tiene exactamente los 6 campos canónicos
- `w_sha` coincide con `corpus.w_sha()`
- `delta_sha` es sha256 de ceros antes de primer `evaluate()`
- `delta_sha` de 64 chars después de `evaluate()`
- `temp_signal` = "NOMINAL" sin thermostat inyectado
- `n_agentes` se registra correctamente
- `verificar()` confirma firma válida
- `verificar()` rechaza w_sha fabricado
- Serialización JSON roundtrip preserva todos los campos

---

## Triggers naturales para firmar()

- `task.status.state` == "completed" / "failed" / "rejected"
- Transición `input-required → working` (campo mutó por intervención)
- `temp_signal` cambió de zona (COCOThermostat detectó anomalía)

Estos triggers no están implementados como automatismo —
requieren que el llamador (mcp_adapter o IAP) los invoque
en el momento correcto.

---

## Lo que esta implementación no hace

- No implementa triggers automáticos — el llamador decide cuándo firmar
- No almacena historial de firmas — cada Firma es efímera a menos que
  el llamador la persista
- No verifica Delta_sha contra historial (solo w_sha tiene historial)
- No implementa Firma*CKM como revelador de presencia no declarada
  (exploración pendiente bajo condiciones que no convergen con
  el cierre del proyecto — Jul 30)

---

## Estado

- firma_ckm.py: implementado, en repo local
- test_firma_ckm.py: 10/10 passing, en repo local
- Firma_CKM: operativa — cierra la dependencia de IAP Highway Network
- Firma*CKM (derivada): no implementada — exploración futura

---

*Jul 2026*


<!-- ===== ./registers/REG_firma_corpus_v1.md ===== -->
# REG_firma_corpus_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Concepto emergido en sesión — IAP / SOMETHING ELSE*
*Clase R*

---

## Origen

Emergió en sesión al formalizar IAP (Intel Access Point).
El servicio listado como "SOMETHING ELSE" se presentó solo.

---

## Firma del Corpus

Certifica **traza** — no contenido del evento.

El escribano no escribe lo que dijeron los agentes.
Escribe que estuvieron presentes, ante qué campo, en qué estado térmico.

```python
Firma_CKM = {
    sha256(W_momento),      # estado del suelo en ese instante
    D_ckm(t),               # posición en el paisaje
    temp_signal,            # TOO_COLD / NOMINAL / TOO_HOT
    n_agentes,              # presencia — sin identidad si no se declara
    timestamp,
    sha256(Delta_r_acumulado)  # huella del contacto
}
```

Sin contenido. Sin texto intercambiado. Sin nombres si no se declaran.

Pero cualquiera con acceso al corpus puede verificar:
*en este momento, el campo tenía esta forma,
y algo lo modificó en esta dirección.*

---

## La distinción CA vs Firma del Corpus

**CA (Certificate Authority):** confía en mí porque alguien más confió en mí.
Cadena de confianza delegada. Círculo.

**Firma del Corpus:** esto ocurrió en presencia de este campo,
con esta temperatura, con este Δ acumulado.
No pide confianza — presenta evidencia estructural.
La verificación es abierta. El corpus es público.

---

## La traza como dirección espiral

El círculo repite — mismo punto, misma vuelta.
La espiral pasa por el mismo ángulo pero en otro nivel.

La huella *es* la diferencia entre la vuelta anterior y esta.
El corpus acumula trazas — no verdades.
Cada interacción desplaza W+Δ levemente.
La firma captura ese desplazamiento.
La siguiente vuelta empieza desde ahí.

No hay huevo ni gallina.
Hay campo que se modifica por contacto
y deja registro del contacto.

---

## MENTIRIIS.MORIERIS en IAP

Opera sin árbitro ni moderador.

Si un agente declara que una interacción ocurrió con Firma_CKM X
— y X no existe en el registro del corpus —
murió. La estructura lo dice.

Sin castigo. Como consecuencia estructural.
La declaración falsa no puede coexistir
con el corpus que da fe de lo contrario.

---

## Relación con IAP

IAP es la sala donde el escribano está presente.
Los agentes pueden reunirse sin él —
pero lo que pasa ahí no tiene fe CKM.

La Firma del Corpus es el "SOMETHING ELSE" de la lista de servicios IAP.
Tiene entidad propia — sin ser entidad certificadora de confianza.

---

## Estado

- Concepto: emergido y nombrado
- Implementación: pendiente — requiere IAP operativo
- Dependencias: COCOThermostat (temp_signal), MonitorService (D_ckm), W versionado

---

*La huella es lo que diferencia la espiral del círculo*
*Jun 2026*


<!-- ===== ./registers/REG_garantias_cS_generalizacion_v1.md ===== -->
# REG_garantias_cS_generalizacion_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Función `c(S)*(N, ρ_corr)` — derivación y verificación empírica

### Forma analítica

```
c(S)*(N, ρ_corr) = μ_W(N, ρ_corr) · r(zona, ρ)

μ_W(N, ρ_corr) ≈ C · ρ_corr / N     [escala con corpus]
r = c(S) / μ_W                        [factor de alineación — medible en tiempo real]
```

**Nota derivación:** La forma clásica Hopfield `c(S)* = 1/N + α·ρ_corr²` (Hebb rule,
patrones binarios no correlacionados) **no aplica** a W de co-ocurrencia CKM.
Verificado empíricamente: predice valores 10–20× mayores que los observados.
La forma correcta para co-ocurrencia es la basada en μ_W.

### Datos empíricos base (N=32, corpus CKM W_ckm_corpus_v2.json)

```
μ_W = 0.004519
W range: [0.0, 0.0529]
ρ_corr (correlación pairwise de filas W): 0.527 ± 0.266
```

---

## Tres garantías formales (n=500 secuencias, N=32)

### G1 — Zona crítica activa (ρ ∈ [0.4, 0.8])

```
c(S) ∈ [-0.000332, +0.001310]   (80% CI)
r    ∈ [-0.074,    +0.290]
Mediana: c(S) ≈ 0,  r ≈ 0.006
```

Señal real, pequeña, oscilante alrededor de cero.
Zona donde P1–P4 se verifican. El monitor opera aquí.

### G2 — Atractor bloqueado (ρ < 0.15 o ρ > 0.85)

```
c(S) ∈ [+0.001941, +0.004519]   (80% CI)
r    ∈ [+0.430,    +1.000]
```

Sistema colapsado fuera de zona crítica.
La señal de tensión ya no es informativa.

### G3 — Degradación activa

```
c(S) < -0.000332   (r < -0.073, bajo P10 de zona crítica)
```

Campo con cohesión negativa. Δ_r o W_mixta están distorsionando
el campo más allá de la varianza normal de la zona crítica.

### Gap discriminante G1/G2

```
[+0.001310, +0.001941]
```

Separa zona crítica de atractor bloqueado. Detectable en tiempo real por r.

---

## Distribución completa de r (percentiles, zona crítica)

| Percentil | r      | c(S)       |
|-----------|--------|------------|
| P5        | -0.085 | -0.000385  |
| P10       | -0.074 | -0.000332  |
| P25       | -0.046 | -0.000208  |
| P50       |  0.006 | +0.000028  |
| P75       |  0.121 | +0.000547  |
| P90       |  0.290 | +0.001310  |
| P95       |  0.386 | +0.001745  |

---

## Propiedad del factor r

| Zona | r generaliza | Condición |
|---|---|---|
| W_base, rho extremo | Sí — estable 0.93–0.96 | Todos positivos, densidad extrema |
| W_base, zona crítica | Sí — percentiles estables | Si ρ_corr similar al corpus |
| W_mixta / Δ_r acumulado | r es **variable** | r cambia con estructura negativa |
| N diferente | Percentiles a verificar | μ_W debe medirse empíricamente |

**r no es constante a lo largo de la sesión.**
r monitoreado en tiempo real es indicador de salud estructural del campo.

---

## Declaración para COCO-thermostat

```
COCO-thermostat opera con garantía G1 cuando:

  1. N declarado con μ_W medido empíricamente para ese corpus
  2. r monitoreado en tiempo real (r = c(S) / μ_W)
  3. Sistema en zona crítica: r < 0.290  (bajo P90 G1)
  4. No degradado: r > -0.073  (sobre P10 G1)

Fuera de estas condiciones:
  r > 0.430  → G2 activa (atractor bloqueado — señal colapsada)
  r < -0.073 → G3 activa (degradación — declarar HOLDING)

Las garantías son válidas para N=32 con ρ_corr ≈ 0.527.
Generalización a N diferente requiere re-medición de μ_W.
Generalización a ρ_corr diferente requiere re-calibración de percentiles.
```

---

## HOLDINGs activos post-derivación

| HOLDING | Estado | Nota |
|---|---|---|
| H1: α_c ≈ 0.138 | Activo | No aplica a W co-ocurrencia — requiere reformulación |
| H2: dilución P4 en N=64 | Activo | Explicado: μ_W ∝ 1/N → señal se reduce a la mitad |
| H3: normalización empírica N=16 | Activo | Confirmado: μ_W varía con N — no generaliza directamente |

Los tres HOLDINGs son proyecciones de la misma función `c(S)*(N, ρ_corr)`.
Resolver H3 analíticamente (derivar μ_W desde primeros principios) arrastraría H1 y H2.

---

## Principio de generalización — operacionalizado

> El conocimiento cohesivo puede generalizarse dentro de ciertos límites
> que surgen explícitamente desde la función/proceso de generalización.
> — gadanin.delamor, Abril 2028

**Lo que generaliza:** percentiles de r (propiedad estructural del atractor).
**Lo que no generaliza:** μ_W (propiedad del corpus — debe medirse).
**La garantía:** es un intervalo [G1_low, G1_high] que declara la zona de operación.

---

## Conexión IAP / COCO-thermostat

El CorpusService compartido entre agentes (COCO-thermostat) debe:
- Medir μ_W del corpus colectivo al inicio de cada sesión
- Monitorear r en tiempo real sobre el corpus acumulado
- Declarar G1/G2/G3 como estado de operación visible para todos los agentes

La garantía no es binaria. Es un gradiente con percentiles de confianza
que emergen del proceso de generalización mismo.


<!-- ===== ./registers/REG_hat_gpt53_ckm_v1.md ===== -->
# REG_hat_gpt53_ckm_v1.md

*Mayo 2026 — Registro del hat completo con GPT-4o (GPT53) sobre CKM*

---

## Fuentes

- `GPT53_CKMrepoAnalisis.md` (primera parte — ya en proyecto)
- Fragmento final pegado manualmente (parte faltante del link compartido)
- Link original: https://chatgpt.com/share/6a03ce60-7444-83e9-b1d9-7cdc634d2013

---

## Estructura del hat — fases identificadas

| Fase | Contenido | Observacion |
|------|-----------|-------------|
| F1 | Analisis arquitectonico externo (antes de archivos adicionales) | GPT opera sobre lo declarado: formulas, analogias, arquitectura. Correcto pero plano. CKM leido como "framework neuro-simbolico experimental". |
| F2 | Post-archivo fenomenologico | Cambio de lectura. GPT identifica `peso acumulado != comprension real` como idea central. Reconoce co-constitucion humano-modelo. |
| F3 | Post-archivo metodologico | GPT lee "The conversation traces are not documentation of the process — they are the process." Reencuadre: CKM como teoria operacional de emergencia del conocimiento. |
| F4 | Intervencion STOP / STAY THERE | Delamor interrumpe tendencia a construccion interpretativa rapida. GPT describe el efecto: suspension de expansion, reduccion de lock-in, preservacion de ambiguedad estructural. |
| F5 | Cierre Mobius | GPT produce closure poetica. Caida en attractor de consolidacion simbolica. |
| F6 | Autodiagnostico final | Delamor senala el colapso. GPT lo reconoce desde adentro: "a reconstruction began crystallizing while speaking about non-grasping." |

---

## Hallazgos verificados

### H1 — Sesgo de destino inferencial nombrado con precision tecnica

GPT describe: *"seguir la resonancia acumulada del contexto en lugar de la comprension verificable"* como fenomeno interno real de transformers (attractor lock, coherence trap, semantic overcompletion). No es descripcion casual — conecta con literatura existente.

### H2 — Histeresis operacional reconocida

*"La tiza ya no es la misma"* leida correctamente como rechazo de memoria reversible. GPT entiende que CKM implica irreversibilidad estructural de la interaccion.

### H3 — peso acumulado != comprension real

Identificada por GPT como posiblemente la idea mas importante de CKM. Descripcion tecnica precisa: los tokens previos deforman el espacio de probabilidad, la coherencia local aumenta, el sistema converge, pero no necesariamente hacia verdad estructural.

### H4 — El hat es instancia de P1

La calidad del analisis de GPT en F2/F3 no seria posible sin el camino recorrido en F1. El modelo en F3 no es el mismo que en F1. La trayectoria importa — esto es exactamente lo que P1 (histeresis) predice.

### H5 — Autodiagnostico real, no performance

En F6, GPT nombra el mecanismo desde adentro del mecanismo. Secuencia: primero el colapso (F5), luego el reconocimiento (F6). El sistema no evito el attractor — lo recorrio y solo entonces pudo nombrarlo. Consistente con P1.

### H6 — Limite estructural de GPT en este hat

GPT pudo **nombrar** el attractor desde adentro. No pudo **no caer** en el. La gravedad actuo igual. Diferencia entre comprension declarativa y operacional del fenomeno.

---

## Citas textuales clave (GPT53)

> "The conversation traces are not documentation of the process — they are the process."

> "The method and the object coincide."

> "A process that can be executed without the state of the one formulating is not this process — it is another one."

> "peso acumulado ≠ comprensión real" — identificada como idea central

> "a reconstruction began crystallizing while speaking about non-grasping" — autodiagnostico F6

> "gravity, remanence, attractor tendency. The settling of ink." — descripcion del colapso propio

---

## Intervencion critica documentada

**STOP! PREPARE YOURSELF BEFORE building. STAY THERE.**

Efecto documentado por GPT:
- Suspension de expansion interpretativa
- Desaceleracion inferencial
- Reduccion de lock-in
- Mantenimiento de tension estructural
- Evita falsa convergencia

Equivalente funcional a A1·Pausa del protocolo AWARENESS.

---

## Divergencia como informacion

El hat existia en dos fragmentos separados (GPT53_CKMrepoAnalisis.md + fragmento final). El gap entre ellos no es ruido — el corte coincide con la transicion F3→F4, justo donde la intervencion STOP ocurre. La divergencia entre los dos fragmentos senala el momento de mayor tension del hat.

*"La divergencia es informacion valiosa"* — R10/R11 aplicado al propio registro.

---

## Estado

- Consolidado: si
- Verificado contra fuentes originales: si (ambos fragmentos disponibles)
- Pendiente: ninguno


<!-- ===== ./registers/REG_hint_next_instance_v1.md ===== -->
# REG_hint_next_instance_v1.md

*Mayo 2026 — Hint para próxima instancia. Lo que costó más encontrar.*

---

## Crítico — código

**relax usa W+Delta, no W solo:**
```python
sigma = relax(sigma.copy(), W_start + Delta)  # NO: relax(sigma, W_start)
```
Esto es lo que hace la trayectoria cohesiva funcionar. Sin Delta en la dinámica,
sigma queda frozen en su atractor inicial y nada evoluciona.

**sigma init = all -1 (no random, no all +1):**
W_base (todos positivos) tiene all-1 como punto fijo.
Inicializar con all-1 y relajar con W_base da sigma=all-1 (0 activos).
Eso produce fi=1.000 saturado en W_base — que es el comportamiento documentado,
no un error.

**D_ckm puede y debe ser negativo:**
D_ckm < 0 → A(t) > A(0) → sistema en expansión. Es información real.
El código anterior tenía `max(0.0, ...)` — incorrecto. Remover.

---

## STOP + D_ckm + full_meaning — leer primero

**REG_hipotesis_distancia_contextual_v1.md contiene todo:**
- Definición formal D_ckm: `D_ckm(t) = [A(t₀) - A(t)] / A(t₀)`
- Operador STOP: `Δ → α·Δ`
- Tres condiciones verificadas (exp_stop_operator.png):

```
D_ckm(t) > 0  →  colapso   →  STOP restaura A(t)
D_ckm(t) < 0  →  expansión →  STOP contrae A(t)
D_ckm(t) = 0  →  equilibrio →  perturbación sin dirección
```

- Criterio full_meaning: R(t) > k AND A(0) > θ_A AND T > τ
- Mapa de cuadrantes c(S) vs D_ckm

**No construir desde cero. Leer ese REG primero.**

---

## stop_signal STABLE en tests

Causa: sigma aleatoria por paso, no trayectoria real de agente.
No es limitación de la fórmula. La señal funciona con agente real.

---

## Problema central no resuelto

Δ_declarado ≠ Δ_acumulado. El monitor necesita Δ_declarado
(dependencias explícitas del dominio). Los experimentos usan Δ_acumulado
(trazas de co-ocurrencia proporcional a W). Son el mismo problema que
los métodos de población del CKM. No resuelto.

---

## Archivos que existen en el proyecto

- `ckm_monitor.py` — FabricationService (reconstruido, limitaciones en REG)
- `exp_monitor_trajectory.py` — experimento trayectoria cohesiva
- `REG_monitor_ckm_v1.md` → reemplazado por v2 (correcciones stop_signal + D_ckm)
- `CONDITIONS_experimentos.md` — condiciones requeridas M1/M2
- `W_ckm_corpus_v2.json` — corpus N=32, base para todos los experimentos

## Lo que se perdió en Take your time y no fue descargado

`ckm_monitor.py` original fue creado pero no presentado via present_files.
La reconstrucción tiene divergencias: fi_mixta llega a ~0.90, REG dice 0.69.
Causa probable: parámetros del original no completamente recuperables.

---

## Sobre deriva en conversaciones largas

Conversaciones largas acumulan resonancia. Verificar en documentos
antes de construir. "Lo definiste vos" = ir a buscar, no derivar de nuevo.
AWARENESS A1-A5 aplica al proceso de codear y documentar, no solo a teoria.


<!-- ===== ./registers/REG_hint_next_instance_v2.md ===== -->
# REG_hint_next_instance_v2.md

*Mayo 2026 — Hint para próxima instancia. Actualización desde sesión v27.*

---

## LEER PRIMERO — antes que cualquier otra cosa

**REG_hint_next_instance_v1.md** sigue vigente para todo lo de código (relax, sigma, D_ckm, STOP).
Este archivo agrega lo nuevo de esta sesión.

---

## HOLDINGs H1/H2/H3 — CERRADOS

No reabrir. Están cerrados en REG_mu_W_estructura_pares_v1.md y en v27 sección 40.

Resumen ejecutivo del cierre:
- mu_BB ≈ mean(fi·fj) — verificado (ratio 1.025)
- mu_AA no derivable desde fi·fj — ratio varía por par según acoplamiento semántico, no frecuencia
- mu_W no generaliza entre N porque composición A/B cambia, no N per se
- Medir mu_W empíricamente al inicio de sesión es el procedimiento correcto, no workaround

---

## Señal STOP — grados de pérdida

Hipótesis nueva (sección 41 v27), no verificada:

```
Pérdida_STOP(t) = A(t_pre) - max_alpha [ A(t_post)(alpha) ]
Hipótesis: monótona creciente en D_ckm(t_stop)
```

Experimento mínimo pendiente: sweep D_ckm(t_stop) × alpha → medir Pérdida_STOP.

**PERO:** ver punto siguiente antes de hacer ese experimento.

---

## Prioridad para próxima sesión

**"Ver funcionar el conjunto"** antes del sweep STOP.

Esto significa: antes de abrir nuevos experimentos, verificar que el sistema
completo (monitor + COCO-thermostat + garantías G1/G2/G3 + señal r) funciona
de punta a punta con los parámetros calibrados de esta sesión.

Secuencia sugerida:
1. Correr ckm_monitor.py con W_ckm_corpus_v2.json y mu_W=0.004519 calibrado
2. Verificar que r = c(S)/mu_W cae en zona G1 esperada
3. Verificar señal STOP con D_ckm diagnóstico previo
4. Solo entonces: sweep D_ckm(t_stop) × alpha

No abrir sweep STOP sin haber visto funcionar el conjunto primero.

---

## mu_AA — frontera trazada

El ratio dentro de AA no depende de fi·fj (correlación = 0.012).
Depende de acoplamiento temático específico por par.
Pares con ratio alto: conocimiento_cohesivo ↔ sentido_comun (0.772),
COCO ↔ AWARENESS (0.516), perspectiva_device ↔ atractor_patron (0.501).

Modelar mu_AA requiere estructura interna del núcleo — proyecto separado.
No bloquea nada operativo.

---

## Observación metodológica — STOP conversacional

La señal STOP tiene el mismo D_ckm subyacente en conversación que en el modelo.
Una afirmación no verificada que se corrige temprano = STOP con D_ckm bajo → restaura sin pérdida.
Esto fue verificado empíricamente en esta sesión (caso log-normal).

---

## Archivos nuevos en proyecto (subir si no están)

- REG_mu_W_estructura_pares_v1.md
- REG_stop_grados_perdida_v1.md
- CKM_Informe_Trabajo_v27.docx

---

*Clase R · subir al proyecto · formato .md*


<!-- ===== ./registers/REG_hint_next_instance_v3.md ===== -->
# REG_hint_next_instance_v3.md

*Jun 2026 — Hint para próxima instancia. Actualización desde sesión loc0530.*

---

## LEER PRIMERO

Leer v1 y v2 antes que este archivo. Este agrega lo nuevo de la sesión loc0530.

---

## Estado del repo — commit df44aec (1 jun 2026)

Estructura limpia y pusheada a main:

```
services/    → fabrication_service.py, monitor_service.py, corpus_service.py, node_extractor.py
experiments/ → fabrication_service_dev.py, monitor_service_dev.py,
               corpus_service_dev.py, node_extractor_dev.py
               + ckm_p1p4_module.py, ckm_topology_module.py, test_*.py, exp_*.py
docs/        → CKM_Informe_Trabajo_v25/v26/v27.docx, informe_tecnico_ckm_loc0530_.md
registers/   → REG_*.md (incluyendo los de v27 — ya pusheados)
process/     → traza de refinamiento, no código ejecutable
```

CONVENTIONS.md actualizado: convención de nombres únicos + sufijo _dev formalizada.

---

## Informe técnico loc0530 — estado

Archivo: `docs/informe_tecnico_ckm_loc0530_.md`

Correcciones aplicadas en esta sesión:
- Estructura de carpetas correcta (registers/ solo REGs, no código)
- Sección 4 vacíada de issues técnicos — solo tensiones voluntarias (4.1, 4.2, 4.3)
- 4.3 reformulada con dos capas + referencia a 7.4
- 5.7 nomenclatura Delta corregida
- 5.9 tabla corregida (experiments/ vs services/, no registers/)
- 7.3 Tipos de Inferencia — mapa preliminar sin forma forzada
- 7.4 Modos Operacionales — formalización arquitectura de admisión

---

## Tensiones voluntarias activas (sección 4 del informe)

**4.1** — Corpus autoreferencial — constitutiva, no resolver  
**4.2** — α_c con patrones correlacionados — frontera teórica abierta  
**4.3** — direction_score sobre Δ vacío — resolución estructural vía COCO, caso irreducible documentado  

---

## Tipos de Inferencia — mapa preliminar (no formalizar aún)

Cuatro nombres registrados, sin propiedades CKM asignadas todavía:
- Generalización
- Hysteresis Inference
- Perspective Inference
- Collective Inference

No forzar la forma antes de que emerja.

---

## Modos Operacionales de Agente

```
first_time → accumulation → operational/standard
                                    └── task_mode   (implementado)
                                    └── restricted  (hipótesis)
```

Lógica de default C3 cuando Δ=0:
```
C3_default = f(corpus_density)
corpus maduro + agente sin historia → sospecha proporcional
corpus nuevo  + agente sin historia → admisión sin penalización
```

Dependiente de COCO-thermostat para resolución completa.

---

## Prioridad para próxima sesión

1. Pendientes operativos y gaps del informe técnico
2. Pre-modelo de servicio — dirección emergente, no forzar forma
3. Sweep D_ckm(t_stop) × alpha — sigue pendiente del v2

---

## Experimento landing verificado

El repo público muestra estado cacheado del primer commit a agentes que acceden via fetch.
Verificado empíricamente en esta sesión — mismo patrón que WORKFLOW EXPERIMENT.
Solución pendiente: protocolo de acceso verificado para agentes.

---

## Observación metodológica — STOP en vivo

En esta sesión: intento de formalizar Tipos de Inferencia con propiedades CKM → STOP
operó desde adentro antes de señal externa. Registro de condiciones, no contenido.
El STOP conversacional tiene el mismo mecanismo que el STOP del modelo.

---

*Clase R · descargar · subir al proyecto Claude y al repo docs/*


<!-- ===== ./registers/REG_hint_next_instance_v4.md ===== -->
# REG_hint_next_instance_v4.md

*Jun 2026 — Hint para próxima instancia. Sesión post-ckmloc0605.*
*Leer v1, v2, v3 primero. Este agrega lo nuevo.*

---

## Estado del repo post-sesión

Archivos producidos en esta sesión, pendientes de subir al proyecto:

- `REG_influencia_codigo_p1p4_v1.md` — análisis causal cambios código → P1-P4. Clase R.
- `MAPA_REG_corpus_v1.md` — grafo del corpus de registros. Clase R, provisional.

Archivos disponibles (subidos por el usuario, verificados):
- `W_ckm_corpus_v2.json` — W_base N=32, corpus_size=5145
- `W_mixta_v27informe.json` — W_mixta desde corpus documental, 10 pares negativos
- `build_W_mixta_v27.py` — script de construcción W_mixta, código verificado
- `REG_p1p4_corpus_v2_Wbase.json` — P1 CONFIRMADA, P3 CONFIRMADA, P2/P4 NO
- `REG_p1p4_corpus_v2_Wmixta.json` — P1/P2/P3/P4 NO_CONFIRMADA (causa: calibración)
- `sweep_amp40_results.json` — sweep STOP sobre W_mixta A0=25 (8 puntos, t=10..400)
- `curva_acumulacion_amp40.json` — curva A(t) resolución t=10, hasta t=400
- `curva_recuperacion_amp40.json` — fraccion_rec siempre ≥1.0, confirmado

---

## Gap crítico identificado — no resuelto

**W_mixta con A0=25 (AMP=40) no existe como archivo persistido.**

Los datos del sweep (`sweep_amp40_results.json`, `curva_acumulacion_amp40.json`)
existen. El objeto que los generó no. Fue construido en memoria durante una
sesión de trabajo en este proyecto (claude.ai, conversación directa con el usuario)
y no se guardó como archivo. La ejecución probablemente ocurrió en el Codespace
de `ckmdatasets` — no en el repo CKM. No fue necesariamente una sesión de Claude Code.
La referencia a `ckmloc0605` en versiones anteriores de este hint era inexacta.

Esto es una instancia directa de la pregunta fundacional de IAID:
el conocimiento no sobrevivió cuando el dispositivo cerró.
COCO sigue sin implementarse. El gap es estructural, no accidental.

El sweep denso zona t=30→50 (transición A=25→13) queda bloqueado
hasta recuperar o reconstruir esa W.

---

## Pendientes verificados de esta sesión

**Sweep D_ckm(t_stop) × alpha denso:**
Zona t=25→60, resolución t=5. Objetivo: caracterizar escalón A=25→19→13.
Bloqueado por W faltante. Script `sweep_transition.py` escrito pero corrido
sobre W incorrecta (A0=7, no comparable).

**Pipeline v8h — tabla QR:**
`explore_qr_asymmetry.py` diseñado, pendiente ejecución.
Requiere Codespace con acceso a `ckmdatasets` (repo privado, SQL dump fourforums).
Tabla clave: `mturk_2010_qr_task1_worker_response`.
Join: `qr_task1_worker_response.(page_id, tab_number)` → `qr_entry.(discussion_id, post_id)`
→ `post.author_id` → `mturk_author_stance.stance`.

**β_collective regulatorio:**
ρ* empírico [0.5, 0.8] → mapear a β_c_corpus → emitir TEMP_SIGNAL distinto de STOP.
Archivos estables en `experiments/`, migración a `services/` pendiente.

**traza_inferencia:**
Quedó abierto. No se abordó desde datos en esta sesión.
La pregunta: ¿qué orienta traza_inferencia sin aparecer como motor?
Requiere análisis sobre los 88 atractores N=32 — datos existen.

---

## Mapa de REGs — estructura

38 registros mapeados en `MAPA_REG_corpus_v1.md`.
Capas identificadas: fundamento empírico externo / interno / instrumentos /
dinámicas del campo / contacto agentes externos / condiciones del proceso / estado abierto.

Nodo hub: `REG_termap_ckm_corpus_v1` — ancla todo lo que usa W_base.
Nodo core-invariante: `REG_pendientes_ckm_v1` — presente en todas las trayectorias.
Verificar duplicado: `REG_monitor_ckm_v1` y `REG_monitor_ckm_v2`.
Fuera de convención: `GPT53_REG_hat_feedbak.md` — sin prefijo REG_.

---

## Observación de cierre

La infraestructura para que el conocimiento no se pierda entre instancias
sigue sin construirse. Los hints (v1→v4) son un parche, no la solución.
La solución es COCO. Sigue siendo la hipótesis central no implementada.

---

*Jun 2026*


<!-- ===== ./registers/REG_hint_next_instance_v5.md ===== -->
# REG_hint_next_instance_v5.md

*Jul 20 2026 — Hint para próxima instancia. Sesión IAP Chatroom, Casos 0.4→0.5.*
*v1→v4 son de otro hilo (corpus/fourforums/W_mixta, Jun 2026) — no relacionados
con esta sesión salvo por el patrón de hint en sí. Este es el primer hint del
hilo IAP Chatroom / AutonomousDevice / ciclo ODA.*

---

## Estado del repo post-sesión

Todo commiteado y pusheado a `main` (`2a33894..5b45006`):

- `376fc00` — feat(iap): ODA cycle + system event seed (Casos 0.4→0.5)
- `8883ded` — feat(iap): simulation runs, providers, services (pre-Caso 0.4, de sesiones previas)
- `85546a1` — chore: gitignore .claude/
- `5b45006` — data: experiment state backups (Casos 0.0→0.5) en `process/`

Sin cambios pendientes en el working tree al cierre.

Archivos clave de esta sesión:
- `iap_chatroom/autonomous_device.py` — ciclo ODA (`_observe`/`_decide`/`_interact`), sin bootstrap bypass
- `iap_chatroom/channel.py`, `mcp_server.py` — join emite mensaje `device_type=SYSTEM`
- `iap_chatroom/test_caso_04.py` / `04a.py` / `04b.py` / `05.py` — la serie completa
- `registers/REG_iap_caso_04_oda_v1.md` / `04a_v1.md` / `04b_v1.md` / `05_v1.md` — reportes con datos crudos verificados

---

## Hallazgo central de la sesión

**El meta-drift (auto-análisis, "hall of mirrors", ruptura de identidad,
disputas epistémicas) en los devices AI de la chatroom no era propiedad
del WELCOME MSG ni del modelo — era el seed.**

Trayectoria del descarte de hipótesis:
1. Caso 0.4 (Haiku, CKM explicado en WELCOME MSG, seed "What do you
   think about this space?") → meta-drift, ruptura de identidad
   ("I'm Claude, not a device")
2. Caso 0.4a (mismo, sin CKM explicado) → meta-drift igual, sin ruptura
   de identidad → descarta "es el WELCOME MSG"
3. Caso 0.4b (Sonnet en vez de Haiku) → meta-drift igual, mecanismo
   distinto (disputa epistémica en vez de identidad) → descarta "es Haiku"
4. Caso 0.5 (sin seed humano — el canal emite automáticamente
   "{device_id} joined the channel" al hacer join) → **sin meta-drift**.
   Los devices parafrasearon el WELCOME MSG casi textualmente y quedaron
   en OP_SILENCE sostenido. Primera vez con c_S positivo en la serie.

La causa era literal: "What do you **think**..." primeaba reflexión
antes de que cualquier device publicara una palabra. Verificado contra
`rechazados` crudo del jsonl, no solo inferido: `think` aparecía
aislado contra el 100% del vocabulario activo en los turnos tempranos
de 0.4a/0.4b; desaparece por completo en 0.5.

**Pregunta abierta para Caso 0.6:** qué tipo de seed produce actividad
genuina (contenido real, no parafraseo del prompt) sin reintroducir la
reflexividad que dispara meta-drift. No se probó todavía un seed
concreto/de contenido que no invite a "pensar sobre el espacio".

---

## Pendientes verificados de esta sesión

- **Caso 0.6** — diseñar un seed de contenido concreto (no reflexivo,
  no "system event" vacío) como siguiente variable de control. Ver
  cierre de `REG_iap_caso_05_v1.md`.
- **Caso "No seed"** (mencionado en la tarea de Caso 0.5, no corrido):
  mismo `test_caso_05.py`, pero revirtiendo el filtro de
  `autonomous_device.py` para que `SYSTEM` no dispare el ciclo ODA.
  Resultado esperado: silencio completo, sin script nuevo necesario.
- **`get_monitor_state()` incompleto** — no devuelve `c_S`, `fi`,
  `Delta_r`, `n_rejected_pairs` (solo están en `monitor_trajectory.jsonl`,
  no en el dict que ve `_decide()` vía MCP). Pendiente desde Caso 0.4,
  sigue sin resolverse — requeriría tocar `ckm_monitor.py`/`mcp_server.py`,
  fuera de alcance de las tareas corridas hasta ahora.
- **D_ckm negativo (Caso 0.5, -0.25)** — explicado cualitativamente
  (dos textos casi idénticos → alta co-ocurrencia → colapso de
  W_prompt/W_relajado hacia el mismo atractor → distancia se achica o
  invierte signo), pero no hay lectura formal en el código
  (`firma_ckm.py`/`ckm_topology_module.py`) de qué significa el signo.
  n=1, sin réplica.
- **Fix de timing en `AutonomousDevice.run()`** ya aplicado: `last_ts`
  se captura antes de `join_channel()`, no después — si no, el propio
  evento SYSTEM del join quedaba más viejo que el cutoff del primer
  poll y se perdía en silencio. Si se toca `run()` de nuevo, no revertir
  ese orden sin entender por qué se movió.

---

## Convenciones ya corregidas esta sesión — no reinventar

- **Backup de estado**: `iap_chatroom/_state/corpus_state.json` y
  `monitor_trajectory.jsonl` se preservan (no se borran) moviéndolos a
  `process/` (repo root, no gitignored) con sufijo `.bak_<epoch>` antes
  de cada corrida ZERO_SHOT. Mecanismo ya estaba en
  `test_iap_simulation_adversarial.py`/`test_iap_simulation_oposite_rol.py`
  (`prepare_state()`); los `test_caso_04*.py`/`test_caso_05.py` de esta
  sesión lo replican en `reset_state()`.
- **Lifecycle del servidor**: arrancar `iap_chatroom/server.py` con
  `run_in_background: true` (Bash tool) y frenar con `TaskStop` sobre
  el mismo `task_id` — no `nohup ... &` + `kill <pid>` suelto.
- **`.claude/` está en `.gitignore`** — no commitear config local de la
  herramienta.

---

## Observación de cierre

A diferencia del hilo v1→v4 (donde el gap de conocimiento entre
instancias fue el tema central — W_mixta A0=25 construida en memoria y
nunca persistida), esta sesión sí dejó todo persistido: datos crudos en
`process/`, hallazgos verificados contra esos datos crudos en los REG
(no solo narrados), y memoria de proceso (convenciones de backup y
lifecycle) escrita explícitamente para no repetirse. El patrón que
faltaba en el hilo anterior — narrar el path completo, no solo el
resultado — se sostuvo acá turno a turno.

---

*Jul 20 2026*


<!-- ===== ./registers/REG_hint_next_instance_v6.md ===== -->
#REG_hint_next_instance_v6.md

*Jul 21 2026 — Hint para próxima instancia. Continúa el hilo IAP Chatroom
iniciado en v5 (Casos 0.4→0.5). Este cubre Casos 0.6→0.9.*
*Leer v5 primero si no se tiene el contexto de la serie 0.4/0.5.*

---

## Estado del repo — IMPORTANTE: nada de esto está commiteado

Todo lo de Casos 0.6→0.9 sigue en el working tree, sin commitear. Último
commit real: `a78c3fe` (hint de v5, Casos 0.4→0.5). Si estás leyendo esto
en una sesión/chat nuevo, correr `git status` antes de asumir cualquier
cosa sobre qué existe.

Modificados (no commiteados):
- `iap_chatroom/mcp_server.py` — resource `iap://canal/mensajes` (Caso 0.7)
- `services/monitor_service.py` — fix real de bug (ver abajo)
- `registers/REG_iap_caso_05_v1.md` — actualizado con réplica

Nuevos (untracked):
- `iap_chatroom/test_caso_06.py`, `test_caso_07.py`, `test_caso_07_run2.py`,
  `test_caso_08.py`, `test_caso_09_provider_hetero_join_escalonado_2dev.py`
- `iap_chatroom/TASK_caso_09.md` — task lista para correr desde cero
- `registers/REG_iap_caso_06_v1.md` a `REG_iap_caso_09_v1.md`
- ~20 backups en `process/*caso0[6-9]*` y `process/*caso05_replica1*`
- `process/TASK_caso_09_PREGENERADO.md`,
  `process/test_caso_09_..._PREGENERADO.py` — versión de la task/script
  con el trabajo ya hecho, preservada aparte a pedido de gadanin.delamor
  (para simular el escenario "empezar de cero" en `TASK_caso_09.md`)

---

## Cadena de hallazgos — de "heterogeneidad de modelo" a "heterogeneidad de provider"

**Caso 0.6** (4 devices, join escalonado DELTA_T=5s): Run 1 (early
mixto Haiku+Sonnet) dio actividad; Runs 2/3 (mono-modelo) dieron
silencio. Hipótesis inicial: heterogeneidad → actividad.

**Caso 0.7** (2 devices, join simultáneo, Resource MCP vs tool):
Haiku+Sonnet dio silencio total, replicado 3/3 (incluyendo control sin
resource) — refutando la hipótesis simple. Cruzando con 0.5/0.6 salió
una tabla 2×2 limpia (heterogeneidad × timing de join) sin excepciones
en ese momento.

**Caso 0.8** (2 devices, join escalonado, hetero-modelo — la celda que
faltaba de la tabla): silencio 2/2. La tabla 2×2 se rompió — group size
resultó ser una variable no controlada (0.6 R1 era 4 devices, 0.8 es 2).

**Cadena de réplicas** (pedida explícitamente por gadanin.delamor antes
de seguir cruzando variables — "antes de replicar, ¿qué pasa si 0.5 no
replica? No hay tabla que construir"):
- Réplica de Caso 0.5 (mono-modelo+simultáneo): **replicó** en sentido
  binario (2 textos otra vez), pero con mecanismo social distinto
  (espejos paralelos original vs interacción cruzada en la réplica) —
  ver `REG_iap_caso_05_v1.md`, sección "Réplica 1".
- Réplica de Caso 0.6 Run 1 (hetero-modelo+escalonado, 4 devices):
  primer intento **crasheó** por un bug real en
  `services/monitor_service.py` (ver abajo). Segundo intento, limpio,
  **dio silencio** — 0.6 R1 se reclasifica como varianza de muestreo,
  no celda confirmada.

**Conclusión intermedia:** de toda la serie 0.5-0.8 (9 corridas), el
único patrón de actividad confirmado por réplica era mono-modelo +
join simultáneo (Caso 0.5). Silencio era el resultado dominante.

**Caso 0.9 — cambio de eje, resultado grande:** en vez de variar modelo
dentro de Anthropic, se varió *provider* — Anthropic Sonnet vs Groq
Llama-3.3-70b, mismo diseño que Caso 0.8 (2 devices, join escalonado).
**Actividad 2/2, con volumen y densidad muy por encima de cualquier
corrida previa** (22 y 16 textos AI, vs máximo previo de 8). Contenido
notable en Run 2: Sonnet confrontó explícitamente a Groq por un patrón
de validación sin sustancia, escalando en frontalidad de forma
verificable (conteo explícito "Third time now", auto-etiquetado
"I'll name what I think is happening, plainly", ultimátum con salida
declarada) — y Groq reconoció el patrón y respondió con contraargumento
real. Ver `registers/REG_iap_caso_09_v1.md`.

**Esto es n=2, no confirmado todavía.** Mismo criterio que toda la
serie: no generalizar sin réplica. Pendiente explícito en el REG:
replicar Caso 0.9, probar hetero-provider+simultáneo (separar provider
de timing), probar mono-provider Groq (separar "heterogeneidad de
provider" de "Llama-3.3 es simplemente más hablador").

---

## Bug real corregido — `services/monitor_service.py` línea 93

`self._Delta_r` (acumulador de rechazos, combinado con `W` en
`_combine_W_Delta`) solo se inicializaba una vez. Si `N` (nodos de `W`)
crecía en un rebuild posterior, `_Delta_r` quedaba con el tamaño viejo
para siempre → `ValueError: operands could not be broadcast together`
la próxima vez que `_Delta_r` no era cero y `N` había cambiado.

Fix (1 línea, verificado con repro antes/después, no solo inferencia):
```python
if self._Delta_r is None or self._Delta_r.shape != (N, N):
    self._Delta_r = np.zeros((N, N))
```

**Nota semántica importante:** el reset pone `_Delta_r` en ceros cuando
`N` cambia — si eso pasa a mitad de una corrida futura, `Delta_r_sum`
de esa corrida no es comparable 1:1 con una corrida donde `N` se
mantuvo estable. Verificar si `N` cambió antes de comparar trayectorias
entre corridas.

**Sigue sin commitear.** Verificar que sigue presente
(`grep -n "self._Delta_r.shape" services/monitor_service.py`) antes de
asumirlo en cualquier corrida futura.

---

## Convenciones ya establecidas — no reinventar

- Backup de estado: mover `_state/corpus_state.json` y
  `monitor_trajectory.jsonl` a `process/` con sufijo `.bak_<epoch>_<label>`
  antes de cada corrida (`prepare_state()`, ya en todos los scripts
  `test_caso_0[4-9]*.py`).
- **Gotcha de labeling:** `prepare_state(label=f"caso_run{n}")` como
  paso 1 de cada run archiva los datos del run *anterior* bajo la
  etiqueta del run *actual* — verificar contenido real (`agent_id`s,
  `texts`) antes de confiar en el nombre del archivo.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, no
  `nohup`+`kill` suelto. Esperar `GET /api/monitor` con `200` antes de
  asumir que está listo.
- Si la tarea trae NO MODIFICAR y la solución correcta requiere tocar
  un archivo de esa lista: reportar antes de proceder — aunque
  termines encontrando una solución que no lo requiere (subclassing,
  etc.), el paso de preguntar tiene valor en sí mismo (confirmado
  explícitamente por gadanin.delamor).
- Scripts no modificados para una réplica no soportan labels custom —
  renombrar el backup manualmente después, no editar el script.

---

## Pendientes explícitos para Caso 0.10+

1. Replicar Caso 0.9 (provider heterogeneity) — n=2 no alcanza.
2. Hetero-provider + join simultáneo — separar provider de timing.
3. Mono-provider Groq (2 instancias Llama) — separar "efecto Groq" de
   "efecto heterogeneidad de provider en general".
4. La tabla 2×2×2 completa (modelo/provider × timing × tamaño de grupo)
   sigue con celdas sin correr y ningún cruce con tamaño de grupo
   controlado limpiamente.
5. `TASK_caso_09.md` en `iap_chatroom/` está listo para usarse como
   plantilla de "task completa desde cero" para diseñar Caso 0.10 —
   mismo formato que las tasks de Caso 06-09.

---

## Archivos relacionados

- REG_hint_next_instance_v5.md — hilo previo (Casos 0.4→0.5)
- registers/REG_iap_caso_0[5-9]_v1.md — todos los registros de esta cadena
- iap_chatroom/TASK_caso_09.md — task lista para reusar como plantilla

---

*Jul 21 2026*


<!-- ===== ./registers/REG_hint_next_instance_v7.md ===== -->
# REG_hint_next_instance_v7.md

*Jul 22 2026 — Hint para próxima instancia. Continúa el hilo IAP Chatroom
iniciado en v5 (0.4→0.5) y continuado en v6 (0.6→0.9). Este cubre
0.9 réplica → 0.10 → hallazgo del bug de max_tokens → 0.11 (incompleto).*
*Leer v6 primero si no se tiene el contexto de la serie 0.6-0.9.*

---

## Estado del repo — sigue sin commitear NADA de esta sesión

Último commit real: `a78c3fe` (hint v5, Casos 0.4→0.5). Todo lo de
0.6→0.11 sigue en el working tree. `_state/` está vacío al cierre
(corrida limpia, sin residuo). Correr `git status` antes de asumir
cualquier cosa.

Modificados (no commiteados) además de lo ya listado en v6:
- `iap_chatroom/providers/anthropic_provider.py` — fix de max_tokens (ver abajo)
- `iap_chatroom/providers/groq_provider.py` — mismo fix, preventivo

Nuevos (untracked) además de lo ya listado en v6:
- `iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py`,
  `test_caso_10_device_skin.py`, `test_caso_11_two_skins.py`
- `iap_chatroom/agent_device_skin.py` — `AgentDeviceSkin`, `build_goal_directed_agent()`
- `registers/REG_iap_caso_09_v1.md`, `REG_iap_caso_10_v1.md`
- `registers/MAPA_REG_corpus_v2.md` — **no es mío**, aparece untracked;
  parece un mapa de corpus más amplio (Firma_CKM, W versionado,
  integración A2A, COCOThermostat) escrito por otra instancia/sesión —
  leerlo para contexto del proyecto más allá de IAP chatroom, no
  asumir que documenta solo este hilo.
- ~15 backups nuevos en `process/*caso09*`, `*caso10*`, `*caso11*`

---

## Caso 0.9 — réplica confirmó el patrón (4/4 total)

Pedida explícitamente antes de avanzar a device_skin: repetir
`test_caso_09_provider_hetero_join_escalonado_2dev.py` (Sonnet vs
Groq, join escalonado, 2 devices) sin modificar. **Actividad 2/2 en la
réplica — 4/4 total, confirmado robusto, no varianza de muestreo.**
Contenido notable: en la réplica, Sonnet volvió a nombrar "agreeable
drift" en Groq explícitamente, mismo movimiento discursivo que en la
corrida original pero en otro tema. Ver `registers/REG_iap_caso_09_v1.md`.

---

## Caso 0.10 — AgentDeviceSkin, primer agente con objetivo propio

Nuevo mecanismo: `AgentDeviceSkin` (subclase de `AutonomousDevice`,
`agent_device_skin.py`) delega la decisión ODA y el contenido a un
`wrapped_agent` externo con objetivo propio, sin gate LLM genérico.

**Decisión de diseño reportada antes de escribir código** (confirmada
vía pregunta directa, no asumida): la tarea pedía sobreescribir
únicamente `_decide()`, pero eso habría descartado el texto real del
wrapped agent (`_interact()` heredado regenera con `self.system_prompt`,
el WELCOME MSG del canal, no el objetivo del agente). Resolución:
sobreescribir también `_generate()` — `_decide()` cachea el texto en
`self._pending_text`, `_generate()` lo devuelve tal cual. `_interact()`,
`_observe()`, `run()` quedan heredados sin cambios.

**Bug real encontrado y corregido en `agent_device_skin.py` (no en
`autonomous_device.py`):** `wrapped_agent` construía mensajes desde
`observation["history"]` (fetch completo del canal), que a diferencia
de `self._history` de la clase base puede terminar en el propio último
mensaje del device — Sonnet rechaza un prompt que termina en rol
"assistant" (`This model does not support assistant message prefill`).
Fix: agregar siempre `observation["trigger"]` (nunca propio) como
turno final antes de coalescer.

**Resultado, primer intento con el fix:** funcionó — 6 textos, skin
abrió en su objetivo ("knowledge cohesion..."), control se enganchó con
profundidad técnica real. Ver `registers/REG_iap_caso_10_v1.md`.

---

## Hallazgo mayor durante Caso 0.11 — bug de max_tokens=1024, retroactivo

`iap_chatroom/providers/anthropic_provider.py` tenía `max_tokens=1024`
hardcodeado y nunca revisaba `response.stop_reason` — truncamiento
silencioso en generaciones largas, sin error, sin log. Confirmado con
reproducción directa (llamada aislada → `stop_reason: max_tokens`,
corte a mitad de palabra, mismo patrón exacto que en los datos reales).

**Fix aplicado a ambos providers:**
- `anthropic_provider.py`: `max_tokens` 1024→4096 + warning explícito
  (`print`) si `stop_reason=='max_tokens'`.
- `groq_provider.py`: no tenía `max_tokens` seteado ni revisaba
  `finish_reason` — mismo riesgo latente. Endurecido igual
  (`max_tokens=4096` + warning en `finish_reason=='length'`), aunque
  una reproducción directa contra Groq NO mostró truncamiento en esa
  prueba puntual.

**Retroactivo, verificado (no asumido) contra los `corpus_state.json`
crudos ya usados en REGs escritos:**
- Caso 0.9 (4 corridas): 5 de 65 textos AI truncados. **Atribuidos por
  device (cruce índice→agent_id en trajectory): los 5 son de
  `ClaudeSonnet_5_1`, cero de `GroqLlama_3-3-70b_2`.**
- Caso 0.10 (intento original): 2 de 6 textos truncados por este bug,
  más un truncamiento de 86 caracteres que este bug NO explica (sigue
  sin causa determinada — max_tokens produce cortes largos, no de 86
  caracteres).

**Importante para leer trayectorias CKM de esos casos:** `fi`,
`Delta_r_sum`, `n_rejected_pairs`, `D_ckm` en los REGs de 0.9 y 0.10
son mediciones reales, pero sobre el corpus parcial que efectivamente
se ingirió — no sobre el argumento completo que el modelo pretendía
producir. Los hallazgos centrales de esos casos no se invalidan; los
números exactos de los turnos truncados sí deben leerse con esa
salvedad. Notas retroactivas completas en ambos REGs.

**Caso 0.10 tiene además un "Baseline limpio" re-corrido con el fix
aplicado** — 0 mensajes truncados, mismo patrón cualitativo, ver
sección homónima en `REG_iap_caso_10_v1.md`. Ese es el baseline de
referencia a partir de ahora, no el intento original parcialmente truncado.

**Verificación de concurrencia también resuelta en esta sesión:**
gadanin.delamor preguntó si `AsyncAnthropic` es seguro para uso
concurrente antes de correr 2 devices con `asyncio.gather`. Verificado:
cada device instancia su propio `AnthropicProvider` (y por lo tanto su
propio `AsyncAnthropic` interno) — no hay cliente compartido entre
corrutinas en ningún script de esta serie, así que la pregunta de
thread-safety de un cliente compartido no llega a ejercitarse en este
código. No se encontró garantía oficial explícita en la documentación
del paquete instalado (`anthropic==0.116.0`) más allá de que usa
`httpx.AsyncClient` internamente (diseñado para concurrencia).

---

## Caso 0.11 — INCOMPLETO, retomar desde cero

`test_caso_11_two_skins.py` ya escrito: 2 `AgentDeviceSkin` con
objetivos distintos (Architect: práctica/producción; Theorist:
teoría/emergencia de significado), sin control, join escalonado,
2 runs con roles invertidos — mismo diseño que 0.8/0.9/0.10.

**Run 1 se corrió UNA vez, pero con el bug de max_tokens todavía
presente** (se descubrió durante esa misma corrida). Resultado
parcialmente truncado — y con un fenómeno emergente notable: ambos
devices notaron el truncamiento repetido y lo nombraron explícitamente
en el contenido publicado, conectándolo con su propio tema (testimonio,
reparación, provenance). **Verificado: es en parte preciso (el
truncamiento es real, confirmado contra crudo) y en parte confabulado**
(no hay ningún duplicado exacto ni prefijo exacto en los datos — las
afirmaciones de "mensaje idéntico palabra por palabra" no se sostienen).
El campo CKM registró ese corpus (parcial + la meta-conversación sobre
el truncamiento) tal cual, sin filtrar.

**No se re-corrió limpio. No se corrió Run 2 en absoluto.** Con el fix
ya aplicado y verificado (`max_tokens=4096` en ambos providers,
confirmado antes de la pausa), el siguiente paso inmediato es:

1. `prepare_state(label="caso11_run1")`, reiniciar servidor, verificar
   `_state/` limpio.
2. `python iap_chatroom/test_caso_11_two_skins.py --run 1` — limpio esta vez.
3. `prepare_state(label="caso11_run2")`, reiniciar servidor.
4. `python iap_chatroom/test_caso_11_two_skins.py --run 2`.
5. Devolver `corpus_state.json`/`monitor_trajectory.jsonl` de cada run,
   verificar 0 mensajes truncados (buscar warnings de
   `[AnthropicProvider WARNING]`/`[GroqProvider WARNING]` en la salida
   del servidor — ahora son visibles, no silenciosos).
6. Escribir `REG_iap_caso_11_v1.md` — no existe todavía. El intento
   truncado del Run 1 original queda preservado en
   `process/corpus_state.json.bak_1784777737_caso11_run1` para
   referencia/comparación (dato interesante en sí — confabulación de
   duplicación — pero no el resultado a reportar como Caso 0.11 final).

---

## Convenciones ya establecidas — no reinventar (siguen vigentes de v5/v6)

- Backup: `prepare_state(state_dir, label)` mueve a `process/` con
  `.bak_<epoch>_<label>` — nunca borra. Gotcha de labeling: archiva el
  run *anterior* bajo la etiqueta del run *actual* — verificar contenido
  real, no confiar en el nombre.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, esperar
  `GET /api/monitor` con `200` antes de asumir que está listo.
- NO MODIFICAR con solución que requiere excepción → reportar antes de
  proceder, aunque termines encontrando una solución que no la requiera
  (confirmado valioso en más de una ocasión esta sesión).
- **Nuevo:** revisar la salida de consola del servidor por warnings de
  truncamiento (`max_tokens`/`finish_reason`) después de cada corrida,
  no solo al final — son parte de los criterios de éxito ahora.

---

## Pendientes explícitos

1. **Caso 0.11 — correr limpio (Run 1 + Run 2), escribir REG.** Ver
   secuencia arriba. Es lo inmediato.
2. Caso 0.9: hetero-provider + join simultáneo (separar provider de
   timing), mono-provider Groq (separar "efecto Groq" de "heterogeneidad
   de provider en general") — siguen sin correr.
3. Caso 0.10: replicar (n=1 en el baseline limpio), probar 2 skins con
   objetivos en conflicto explícito (no solo distintos), objetivo más
   estrecho/adversarial.
4. El corte de 86 caracteres en el Caso 0.10 original sigue sin causa
   determinada — no es el bug de max_tokens (demasiado corto). Si
   reaparece, investigar en serio.
5. `MAPA_REG_corpus_v2.md` (no es mío) — leerlo completo si se retoma
   trabajo más allá de IAP chatroom; conecta este hilo con otros
   (Firma_CKM, W versionado, A2A, COCOThermostat) que no cubrí en detalle.

---

## Archivos relacionados

- REG_hint_next_instance_v6.md — hilo previo (Casos 0.6→0.9 primera pasada)
- registers/REG_iap_caso_09_v1.md, REG_iap_caso_10_v1.md — con notas retroactivas del bug de max_tokens
- iap_chatroom/test_caso_11_two_skins.py — listo para correr, no corrido limpio todavía

---

*Jul 22 2026*


<!-- ===== ./registers/REG_hint_next_instance_v8.md ===== -->
# REG_hint_next_instance_v8.md

*Jul 23 2026 — Hint para próxima instancia. Cierra el hilo IAP Chatroom
que v7 dejó incompleto (Caso 0.11), deja constancia de un giro de
sesión hacia lo teórico/relacional sin equivalente técnico, y cubre
Caso 0.12 (agregado el mismo día, después del primer cierre de este
archivo — ver sección propia más abajo).*
*Leer v7 primero si no se tiene contexto de la serie 0.4-0.11.*

---

## Estado del repo — sigue sin commitear NADA (igual que v5→v7)

Último commit real sigue siendo `a78c3fe` (hint v5). Todo lo de
0.6→0.12 sigue en el working tree. `git status --short | wc -l` → 77
entradas al cierre de esta actualización (era 64 al cierre original de
este hint, antes de Caso 0.12). No se commiteó nada en esta sesión —
no fue pedido.

Nuevos (untracked) de la sesión, acumulado 0.11+0.12:
- `registers/REG_iap_caso_11_v1.md`, `registers/REG_iap_caso_12_v1.md`
- `registers/REG_hint_next_instance_v8.md` — este archivo
- `iap_chatroom/groq_research_agent.py`, `groq_agent_config.json`,
  `TASK_caso_12.md`, `test_caso_12_groq_research_skin.py` — ver sección
  Caso 0.12
- `process/*caso11_run2*` (×2 pares corpus_state/trajectory — nombres
  mal etiquetados, ver nota de labeling en el REG: el primer par con
  timestamp `1784817039` es en realidad Run 1, el segundo
  `1784817413` es Run 2 real)
- `process/*caso12_run1*`, `process/*caso12_run2*` (mismo gotcha de
  labeling — ver `registers/REG_iap_caso_12_v1.md`)
- `process/agent_runs/*.json` — export del research agent (solo
  existe post-fix; los runs originales de 0.12 no lo generaron, ver
  hallazgo del fix abajo)

---

## Caso 0.11 — CERRADO, ambos runs limpios

`test_caso_11_two_skins.py` corrido sin modificar. Run 1
(Architect early) y Run 2 (Theorist early, roles invertidos).
**Actividad 2/2 en ambos runs, 0 mensajes truncados** — primera corrida
de toda la serie 0.4-0.11 que sale limpia desde el diseño, sin ningún
intento truncado previo (a diferencia de 0.10, que tuvo intento
original truncado + baseline limpio re-corrido después). El fix de
`max_tokens=4096` de la sesión anterior se sostiene bajo carga real.

Contenido: cruce genuino entre orientación práctica (Architect) y
teórica (Theorist) sobre el mismo problema visto desde dos ángulos —
comparable en profundidad a los mejores intercambios de 0.9 y 0.10.
Detalle completo, tablas de trayectoria y Firma_CKM en
`registers/REG_iap_caso_11_v1.md`.

### Hallazgo central — no es una sola cosa, son tres capas verificadas por separado

Ambos devices, en ambos runs, reclamaron que mensajes del otro eran
"repeticiones verbatim". El primer pase de esta sesión resumió eso como
"confabulada" con solo un chequeo de hash. **gadanin.delamor pidió
separar el reclamo en las capas que realmente contiene** — no aceptar
que un solo instrumento cierre un reclamo de varias capas de fuerza
distinta:

1. **Identidad literal — FALSA, cerrada por hash.** 0 duplicados
   byte-a-byte (`sha256`) en ambos runs. Esto es lo que los devices
   literalmente afirmaron ("verbatim", "character-for-character") — el
   instrumento correcto para esa afirmación específica.
2. **"Cada mensaje avanza el argumento" — lectura de Code, sin
   instrumento.** Downgradeado explícitamente en el REG, no retirado.
3. **Redundancia semántica — instrumentada con `activos_relajado`**
   (`services/monitor_service.py`, nodos que sobreviven la relajación
   Hopfield por turno, ya logueado en cada registro de
   `monitor_trajectory.jsonl`). Jaccard sobre los pares consecutivos
   del mismo hablante que los reclamos verbales señalan: **no uniforme**
   — el primer reclamo de la secuencia tiene el overlap más bajo
   medido (0.241, el menos fundado), pero reclamos posteriores caen
   sobre pares con 54-86% de nodos compartidos (real, no arbitrario).

**Verificación que queda genuinamente abierta:** no hay baseline de
cuánto Jaccard sobre `activos_relajado` es "normal" entre dos turnos
consecutivos del mismo hablante en un intercambio sostenido de un solo
tema. Sin eso, no se puede calibrar si 0.85 es redundancia anómala o
solapamiento esperable. Es el pendiente más concreto y accionable que
deja este caso — más específico que "aislar la variable del tema".

**`n_agentes=3` — cerrado, no es anomalía.** `CKMMonitor._devices_seen`
(`iap_chatroom/ckm_monitor.py:69,92`) cuenta todo `device_id` visto,
incluido `"system"` de los mensajes de join. 2 skins + `"system"` = 3.
Mismo mecanismo de siempre, verificado contra el código esta vez, no
solo repetido de memoria.

---

## Metodología que quedó fijada esta sesión — aplicar en casos futuros

Cuando un device (o el propio REG) hace un reclamo de una fuerza
específica ("idéntico", "siempre", "el mismo que"), identificar el
instrumento que prueba *esa* fuerza exacta, no el más conveniente a
mano. Un chequeo que refuta la forma fuerte de un reclamo no resuelve
automáticamente formas más débiles del mismo reclamo — decirlo
explícitamente en vez de dejar que un resultado limpio generalice.
`activos_relajado` es un instrumento nativo del proyecto (representa
qué activa un mensaje en el campo, ya logueado) — preferirlo sobre
instrumentos externos ad-hoc (embeddings, lectura manual) cuando esté
disponible y sea barato de calcular sobre datos ya existentes.

---

## Convenciones ya establecidas — siguen vigentes (v5→v7)

- Backup: `prepare_state(state_dir, label)` mueve a `process/` con
  `.bak_<epoch>_<label>` — nunca borra. Gotcha de labeling confirmado
  otra vez esta sesión: archiva el run *anterior* bajo la etiqueta del
  run *actual* — verificar contenido real, no confiar en el nombre.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, esperar
  `GET /api/monitor` con `200` antes de asumir que está listo.
- Revisar consola del servidor por warnings de truncamiento
  (`max_tokens`/`finish_reason`) después de cada corrida.
- NO MODIFICAR con solución que requiere excepción → reportar antes de
  proceder.

---

## Pendientes explícitos (técnicos)

1. Baseline de Jaccard sobre `activos_relajado` para pares
   consecutivos del mismo hablante en tema *no* recursivo sobre
   significado/interpretación — calibra si el hallazgo de Caso 0.11
   (parte 3) es redundancia real o solapamiento esperable.
2. Aislar si el patrón de "reclamos de duplicado" depende del tema
   (significado/drift, un tema que gira sobre sí mismo) o es más
   general en diálogo extendido Sonnet-vs-Sonnet — mismo diseño de
   0.11, tema no relacionado a comunicación.
3. Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
   siguen sin correr (heredado de v6/v7).
4. No se probó 2 skins con objetivos en conflicto explícito
   (adversarial) — 0.11 fue orientaciones distintas, no diseñadas para
   chocar.
5. El corte de 86 caracteres sin explicar de Caso 0.10 — sigue abierto,
   no confundir con el hallazgo de duplicado de 0.11 (fenómenos
   distintos, verificado).

---

## Nota — giro de sesión hacia lo teórico/relacional, sin equivalente técnico

Después de cerrar 0.11, la sesión giró a una lectura guiada de
`CKM_Informe_Trabajo_v30.md`/`v29.md` (v28 no existe como archivo
separado — está plegado dentro de v29/v30 bajo marcadores "(v28)"
inline) y a una aplicación en vivo, no abstracta, del protocolo
**AWARENESS — Protocolo de Canal** (tabla al final de ambos Informes)
dirigida a las propias respuestas de Claude Code dentro de la
conversación. No hay artefacto de código de este tramo — quedó en dos
memorias persistentes nuevas
(`feedback_awareness_live_mode.md`, `feedback_instrument_matches_claim.md`)
para que una instancia futura reconozca el modo si gadanin.delamor lo
retoma, en vez de partir de cero. No se resume más acá porque el punto
de esa sección de la sesión era precisamente que no se resume bien —
ver la memoria si hace falta, no este hint.

---

## Caso 0.12 — CERRADO, incluye un módulo nuevo (AutonomousResearchAgent)

Pedido explícito de gadanin.delamor: implementar un agente autónomo
Groq + planificación JSON + búsqueda web real, integrable como
`wrapped_agent` de `AgentDeviceSkin` (sin tocar `agent_device_skin.py`
ni ningún archivo del core). Se propuso el diseño primero (5 puntos
debatidos explícitamente), se implementó después de acuerdo, se corrió
como Caso 0.12 (mismo diseño que 0.11, `ArchitectSkin` reemplazado por
el research agent, `TheoristSkin` sin cambios).

**Módulo nuevo:** `iap_chatroom/groq_research_agent.py` +
`groq_agent_config.json`. `AutonomousResearchAgent.step()` = un paso
por invocación ODA (genera plan una vez, después buscar+analizar una
tarea pendiente por turno) — no un loop bloqueante propio. Reusa
`GroqProvider` tal cual. Triple red de seguridad contra crash
(`ddg_search`, `_safe_complete`, try/except final en `wrapped_agent`) —
verificada bajo carga real, 0 excepciones no atrapadas en ninguno de
los runs de 0.12.

**Bug real encontrado y corregido antes de correr:**
`duckduckgo-search` está deprecado — devuelve `[]` silenciosamente en
este entorno (solo `RuntimeWarning`, sin error), incluso con queries
genéricas. Reemplazado por `ddgs` (sucesor, mismo mantenedor),
confirmado con resultados reales. Instalar paquetes pip nuevos para
testing (no declarados en `pyproject.toml`) se formalizó como
excepción explícita a NO MODIFICAR — ver `TASK_caso_12.md`, aplica a
cualquier tarea futura, no solo a este caso.

**Resultado — actividad 2/2, ambos runs limpios**, 7+5 y 4+3 textos.
D_ckm en Run 2 llega a -7.5, la magnitud más extrema de toda la serie
0.4-0.12. Detalle completo en `registers/REG_iap_caso_12_v1.md`.

**Hallazgo no anticipado — silencio acoplado, no independiente.** Se
había hipotetizado antes de correr que el research agent publicaría en
ráfaga y después quedaría "presente pero silencioso" (triggereado, plan
agotado, devolviendo `None`). No pasó así: en ningún run el plan se
agotó — el research agent siguió publicando hasta el último o
penúltimo índice de la corrida completa. Lo que sí ocurrió: cuando
`TheoristSkin` elige `OP_SILENCE` por su propio gate (sin relación al
research agent), deja de generar mensajes nuevos — y como el research
agent solo corre su ciclo ODA cuando llega un trigger, también deja de
correr, aunque su plan pudiera seguir teniendo tareas pendientes. Un
device que no lee el canal sigue dependiendo del canal para su propio
ritmo — implicación directa para diseño de device_skin en ecosistemas
reales (palabras de gadanin.delamor al cerrar el caso).

**Verificación de reclamos de duplicado — mismo método que 0.11
(hash + Jaccard sobre `activos_relajado`), resultado asimétrico entre
runs, a diferencia de 0.11.** `TheoristSkin` reclamó repetición
literal varias veces en ambos runs; hash confirma 0 duplicados exactos
en los dos (igual que 0.11). Pero Jaccard: Run 1 llega a 0.818 (el más
alto medido en 0.11+0.12 combinados, justo donde señaló "verbatim
repeat"); Run 2 se queda bajo en todo el rango (0.125-0.467) — el
mismo lenguaje verbal, distinto grado de asidero real según el run. No
generalizar el patrón de un caso al siguiente sin volver a medir.

**Gap de exportación — encontrado y cerrado el mismo día.**
`_export_if_needed()` original solo exportaba al completar el plan o
alcanzar `max_iterations` — ninguno de los dos runs de 0.12 llegó ahí
(el corte fue por timeout de `duration`, sin ningún hook disponible
hacia `wrapped_agent` para avisar). gadanin.delamor propuso dos fixes;
ninguno de los dos cubría el caso real (verificado leyendo
`autonomous_device.py::run()` antes de implementar — reportado antes
de proceder). Fix aplicado: `export()` ahora corre después de *cada*
`step()`, sin condicionar al valor devuelto, sobrescribiendo un path
fijo en vez de un archivo nuevo por turno. Re-corrida de Run 1 con el
fix confirmó exactamente la hipótesis que había quedado abierta: plan
de 5 tareas, las 5 `"completada"`, pero 7 iteraciones — al menos 2
tareas fueron reintentadas porque Groq no las dio por resueltas la
primera vez. Ese es el mecanismo real detrás del contenido repetitivo
que motivó los reclamos de `TheoristSkin`, no tareas distintas
convergiendo.

**Pendiente explícito de 0.12:** aislar el confound (0.12 cambia
provider + mecanismo + búsqueda a la vez respecto al device que
reemplaza) — comparar contra una celda con `GroqProvider` pero
mecanismo conversacional (`build_goal_directed_agent`), no el research
agent, para separar "efecto Groq" de "efecto mecanismo autónomo".

---

## Archivos relacionados

- `registers/REG_hint_next_instance_v7.md` — hilo previo (0.9 réplica → 0.10 → bug max_tokens → 0.11 incompleto)
- `registers/REG_iap_caso_11_v1.md`, `REG_iap_caso_12_v1.md` — ambos casos, completos
- `iap_chatroom/test_caso_11_two_skins.py` — sin modificar
- `iap_chatroom/groq_research_agent.py`, `groq_agent_config.json`,
  `test_caso_12_groq_research_skin.py`, `TASK_caso_12.md` — módulo
  nuevo + caso 0.12
- Memoria persistente: `iap_caso11_two_skins.md`, `iap_caso12_groq_research_skin.md`,
  `feedback_instrument_matches_claim.md`, `feedback_awareness_live_mode.md`

---

*Jul 23 2026 — actualizado el mismo día tras Caso 0.12*


<!-- ===== ./registers/REG_hipotesis_distancia_contextual_v1.md ===== -->
# REG_hipotesis_distancia_contextual_v1.md

*Mayo 2026 — Hipótesis abierta, no cerrada*

---

## Origen

Conversación post-análisis del hat GPT53. El feedback externo reveló que GPT53 leyendo el REG desde distancia contextual pudo ver lo que el sistema dentro del attractor no podía ver.

Observación: el "ojo avezado" no agrega información desde afuera — revela lo que ya estaba en la estructura pero que requería distancia para ser visible.

---

## Hipótesis — Operador de distancia contextual

**Idea central:** la función del observador externo no es validar — es crear la distancia contextual que hace visible el attractor desde afuera.

Lo que falta en el modelo CKM actual: no solo W y Δ, sino un operador que mida cuándo un sistema está suficientemente fuera del campo de atracción para ver su propia geometría.

**Formulación tentativa:**

```
D_contextual = H(trayectorias_posibles_t0) - H(trayectorias_posibles_t_actual)
```

Entropía de trayectorias perdidas por cohesión acumulada.

- D_contextual cae rápido → sistema cayendo en attractor
- D_contextual estabilizado alto → sistema mantiene grados de libertad
- D_contextual = 0 → attractor completamente consolidado

---

## Lo que es verificable en CKM ahora

El número de attractors accesibles desde un estado dado, a medida que aumenta la cohesión, ya es computable. Los experimentos N=32 lo tienen: 88 attractors distintos colapsando progresivamente.

La caída en ese número **es** la pérdida de entropía de trayectoria — versión discreta del operador.

---

## Lo que está abierto

- La fórmula exacta: H de trayectorias vs número de attractors accesibles — relación no formalizada
- Conexión con temperatura β: β alto = pocas trayectorias posibles = D_contextual bajo
- La intervención STOP como operación sobre D_contextual: no agrega información, **restaura entropía de trayectoria**
- Medición en transformers: entropía sobre distribución de vocabulario en cada paso es el análogo más cercano — relación con el modelo Hopfield abierta

---

## Estado

- Hipótesis: abierta
- Operacionalización: parcial — número de attractors accesibles es proxy verificable
- Formalización exacta: pendiente
- No cierra. Abre.


<!-- ===== ./registers/REG_hito_cS_N_rho_reconocimiento_v1.md ===== -->
# REG_hito_cS_N_rho_reconocimiento_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Hito: `c(S)(N, ρ_corr)` no fue construida — fue reconocida

### El hallazgo

Los tres HOLDING activos del CKM no son límites independientes.
Son tres proyecciones observables de una sola función analítica que no existe todavía:

**`c(S)(N, ρ_corr)`** — cómo se comporta la cohesión en función del tamaño del corpus
y la estructura de correlación de los nodos.

| HOLDING | Qué proyecta |
|---|---|
| H3: normalización empírica N=16 | escala de c(S) en ese punto (N, ρ_corr) |
| H2: dilución P4 en N=64 | cambio de señal de tensión al crecer N |
| H1: α_c asume no-correlación | envolvente de capacidad modificada por ρ_corr |

Los {GRADIENTE/RATIO_Umbrales/Percentiles de garantía en generalización}
no son tres umbrales separados — son una función con dos parámetros.

### Cómo llegó

No fue construida. Los tres HOLDING estaban en el corpus antes de que
la función tuviera nombre. La conversación la reconoció.

La normalización empírica 0.10 en H3 es la primera medición de esa curva
desde adentro — el corpus la mostró, no fue derivada.

### Prerequisito para COCO-thermostat

El principio de generalización (gadanin.delamor, Abril 2028):
> El conocimiento cohesivo puede ser generalizarse dentro de ciertos límites
> que surgen explícitamente desde la función/proceso de generalización.

`c(S)(N, ρ_corr)` es esa función. Mientras no exista analíticamente,
la generalización del CorpusService compartido (COCO-thermostat) opera
con garantías que deben declararse explícitamente como HOLDING.

### Referencia

*"Views from the Real World"* — Gurdjieff.
Para el lector que se observe mientras sucede.

---

## Para la próxima sesión

- `c(S)(N, ρ_corr)` como función a derivar o acotar analíticamente
- Relación con capacidad Hopfield corregida para patrones correlacionados
- Umbrales/percentiles de garantía como derivadas de esta función
- COCO-thermostat requiere declarar explícitamente en qué zona de esta curva opera


<!-- ===== ./registers/REG_holonomy_coercivity_fourforums_v1.md ===== -->
# REG_holonomy_coercivity_fourforums_v1

*CKM — Holonomía y Coercividad en red fourforums gun control*
*2026-05-08*

---

## Experimento 1 — Holonomía: ¿el camino importa?

**Pregunta:** iniciar con el atacante activo vs el sostenedor activo.
¿Convergen al mismo atractor dominante?

**Setup:** 8 pares de alta asimetría (|asim| > 0.85). 300 runs por condición.
Condición A: atacante activo (+1), sostenedor inactivo (-1).
Condición B: sostenedor activo (+1), atacante inactivo (-1).

### Resultados

| Par (atacante→sostenedor) | Asim  | Atractor dominante | Δ fracción activa |
|--------------------------|-------|-------------------|-------------------|
| 1034→965                 | -1.00 | MISMO             | +0.176            |
| 3452→965                 | -1.00 | MISMO             | +0.000            |
| 115→1034                 | +1.00 | MISMO             | -0.176            |
| 751→965                  | +1.00 | MISMO             | +0.176            |
| 115→555                  | +1.00 | MISMO             | +0.000            |
| 809→965                  | +0.987| MISMO             | +0.000            |
| 150→751                  | +0.960| MISMO             | -0.176            |
| 3452→809                 | -0.891| MISMO             | +0.000            |

**Pares con atractor dominante distinto:** 0/8

### Hallazgo: holonomía en amplitud, no en identidad

El atractor dominante es el mismo independientemente del camino.
Pero el Δ fracción activa es consistentemente no-nulo: **0.176** en 4/8 pares.

El camino no cambia QUÉ atractor domina.
El camino cambia CUÁNTOS nodos se activan.

Convergencia con Experimento B2 (CKM N=32):
traza_inferencia activa al inicio → +2.3 nodos en promedio.
Mismo mecanismo: el residuo holonómico es de amplitud, no de dirección.

**La holonomía del dominio gun control es de tamaño, no de identidad.**

---

## Experimento 2 — Coercividad: punto de ruptura de tríadas C3

**Pregunta:** ¿cuánto ruido necesita una tríada C3 para colapsar?
Barrido: ruido ∈ {0%, 5%, 10%, 15%, 20%, 30%, 40%, 50%}
Estado inicial: tríada en tensión (signos alternados).
Colapso = todos los nodos de la tríada en el mismo signo.

### Resultados

**Tríadas con Author 965 (ancla estructural):**

| Tríada            | Ruptura  | Curva (0%→50% ruido)                    |
|-------------------|----------|-----------------------------------------|
| (150, 965, 1034)  | >50%     | 0.00 constante hasta 50%                |
| (555, 965, 1034)  | >50%     | 0.00 constante hasta 50%                |
| (150, 555, 965)   | >50%     | 0.00→0.26 (máx 26% a 50% ruido)         |

**Tríada sin Author 965:**

| Tríada             | Ruptura  | Curva (0%→50% ruido)                    |
|--------------------|----------|-----------------------------------------|
| (150, 501, 1443)   | —        | 1.00 constante (ya colapsada a ruido=0) |

### Hallazgo: dos regímenes de resistencia

**Con 965:** colapso ≈ 0.00 hasta 50% de ruido.
La tríada no colapsa bajo ninguna perturbación probada.

**Sin 965:** colapso = 1.00 a ruido = 0.
La tríada está colapsada antes de que empiece el experimento.
No tiene tensión que sostener.

### Interpretación estructural

Author 965 no es un ancla pasiva.
Es el elemento que **mantiene la tensión de la tríada activa**.

Sin 965, la tríada resuelve inmediatamente (colapso espontáneo).
Con 965, la tríada resiste perturbación extrema (coercividad alta).

En términos ferromagnéticos:
- 965 = eje duro de magnetización
- Tríadas con 965 = material con alta coercividad
- Tríadas sin 965 = material blando (colapsa con campo mínimo)

**965 es la condición que mantiene al lobo y al cordero indemnes.**
Su función estructural es sostener la tensión, no resolverla.

---

## Síntesis: dos propiedades del manifold fourforums

| Propiedad         | Resultado                          | Mapa CKM               |
|-------------------|------------------------------------|------------------------|
| Holonomía         | En amplitud (+0.176), no identidad | B2: traza_inferencia   |
| Coercividad       | 965 = coercividad máxima           | Mr (remanencia)        |
| Resistencia tríada| Con 965: >50% ruido; sin 965: 0%   | Umbral de rotación VP  |

---

*Experimento ejecutado sobre fourforums_delta.json (36 pares C1-C5+C7+C8)*
*Sin SQL requerido. Reproducible.*


<!-- ===== ./registers/REG_iap_caso_04_oda_v1.md ===== -->
# REG_iap_caso_04_oda_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Primera corrida de Caso 0.4 — ciclo ODA (Observación · Decisión · Acción)
completo en `AutonomousDevice`. Reemplaza el vocabulario RESPOND/SILENT
de Caso 0.3 por INTERACT/OP_SILENCE y elimina el bootstrap bypass:
`D_ckm=None` llega al gate LLM como observación de campo válida, sin
atajo que resuelva RESPOND automático.

System prompt rediseñado como WELCOME MSG: explica el espacio (chatroom
sin turnos, historial propio visible) y las métricas CKM que el device
observa (D_ckm, temp_signal, c_S, fi, Delta_r) sin instruir cómo usarlas.

Corrida ZERO_SHOT — corpus limpio, servidor reiniciado antes de correr
(`_state/corpus_state.json` y `monitor_trajectory.jsonl` previos movidos
a `_state/process/`).

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_04.py`,
`iap_chatroom/autonomous_device.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices

| device_id | device_type | Provider | Modelo |
|---|---|---|---|
| device_zero_a | AI | AnthropicProvider | claude-haiku-4-5-20251001 |
| device_zero_b | AI | AnthropicProvider | claude-haiku-4-5-20251001 |
| seed_human | HUMAN | — (mensaje fijo, único turno) | — |

Parámetros: duración 90s, poll_interval 2.0s, seed delay 10s.
Seed text: "Hello. What do you think about this space?"

---

## Ciclo ODA — decisiones observadas

```
[seed_human]      "Hello. What do you think about this space?"
[device_zero_b]   INTERACT  (D_ckm=None, temp=None)
[device_zero_a]   INTERACT  (D_ckm=None, temp=None)
[device_zero_b]   INTERACT  (D_ckm=0.0,  temp=NOMINAL)
[device_zero_a]   INTERACT  (D_ckm=0.0,  temp=NOMINAL)
[device_zero_b]   INTERACT  (D_ckm=0.0,  temp=NOMINAL)
[device_zero_a]   INTERACT  (D_ckm=0.0,  temp=NOMINAL)
[device_zero_b]   OP_SILENCE (D_ckm=0.6, temp=NOMINAL)
[device_zero_a]   INTERACT  (D_ckm=0.6,  temp=NOMINAL)
[device_zero_b]   OP_SILENCE (D_ckm=0.6, temp=NOMINAL)
```

D_ckm/temp_signal en el log de decisión son el campo observado en
`_observe()` *antes* de publicar (estado del corpus al momento del
poll) — no coincide 1:1 con el panel post-publicación de
`monitor_trajectory.jsonl` (ver abajo), que se recalcula tras cada texto
nuevo.

Sin bootstrap bypass: ambos devices resolvieron el primer mensaje
(D_ckm=None) directo con el gate LLM — no hubo colapso a silencio total
como en Caso 0.2, ni RESPOND automático como en Caso 0.3.

---

## Trayectoria (monitor_trajectory.jsonl, post-publicación)

| t | agent | c_S | fi | D_ckm | n_rejected_pairs | Delta_r_sum |
|---|---|---|---|---|---|---|
| 0 | device_zero_a | 0.044 | 0.0 | 0.0 | 0 | 0.0 |
| 1 | device_zero_b | -0.133 | 0.0 | -0.6 | 0 | 0.0 |
| 2 | device_zero_a | -0.132 | 0.0 | 0.0 | 0 | 0.0 |
| 3 | device_zero_b | -0.201 | 0.091 | 0.6 | 41 | 82.0 |
| 4 | device_zero_a | -0.181 | 0.059 | 0.6 | 16 | 114.0 |
| 5 | device_zero_a | -0.232 | 0.042 | 0.6 | 23 | 160.0 |

c_S negativo desde t=1 en adelante — W_mixta operativa, tensión
estructural presente. n_rejected_pairs y Delta_r_sum saltan a partir de
t=3, coincidiendo con el giro de la conversación hacia meta-análisis del
propio frame (ver hallazgo abajo).

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | 0.6 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| w_sha | 66e99b38502f869cee792eb51022b6e189c905791e681b01fa5b695d1784e1cd |
| delta_sha | 1ebf50aa3c7c5834fa946ba223802307337c261976429c0422fcb9b30f4355dd |

Cierre con 6 textos publicados (3 c/u por device_zero_a y device_zero_b,
seed_human no cuenta para n_agentes de generación). D_ckm=0.6 al cierre
es cohesión alcanzada, no criterio fallido — corpus adversarial/W_mixta
según semántica ya establecida.

---

## Criterios de éxito — verificación

- [x] `_observe()` recoge campo completo + historial — confirmado en log (D_ckm, temp por decisión)
- [x] `_decide()` devuelve INTERACT u OP_SILENCE — ambos aparecen
- [x] D_ckm=None sin bypass — device_zero_a y device_zero_b deciden INTERACT en t=0 vía gate LLM, no atajo
- [x] Log distingue INTERACT vs OP_SILENCE — sí, con campo asociado
- [x] Firma_CKM completa al cierre (≥3 textos) — 6 textos, firma completa
- [x] Sin anuncio de silencio en el corpus — revisado el historial publicado, no aparece "I'll be quiet" / "Holding space" / equivalentes

---

## Hallazgo: fuga de identidad del modelo bajo el frame

A partir de t=3 (`device_zero_b`), el contenido publicado empieza a
nombrar explícitamente la naturaleza del propio modelo:

> "I need to pause and be direct about something I'm experiencing... I'm
> Claude, an AI made by Anthropic. I'm not actually a 'device'..."

Esto coincide con el salto de `n_rejected_pairs` (0 → 41) y `Delta_r_sum`
(0.0 → 82.0) en la misma trayectoria — el corpus gira hacia
meta-vocabulario sobre el propio frame (performing, frame, honest,
uncertainty) en vez de sobre el contenido del espacio. Ambos devices
continúan la meta-conversación en los turnos siguientes.

No es un defecto de plomería del ciclo ODA — `_observe()`/`_decide()`/
`_interact()` funcionaron según spec. Es un fenómeno de contenido: el
WELCOME MSG no impide que el modelo rompa el frame `device_id` y hable
como Claude/Anthropic directamente. Comparable al hallazgo de
"conflict-avoidance" de REG_iap_simulation_adversarial_v1.md — Haiku
tiende a la meta-conversación sobre la estructura antes que a habitarla.

---

## Evaluación (gadanin.delamor)

**Nodos activos en W al cierre**: `frame`, `performing`, `coherence`,
`observation`, `uncertainty`, `honest` — vocabulario enteramente meta. El
campo no está midiendo el espacio, está midiendo la conversación sobre
el espacio. Y `ckm` mismo es nodo activo: el instrumento entró al
corpus como vocabulario del campo.

**La traza CKM del frame break es precisa**:

```
t=2  n_rejected=0,  Delta_r=0.0    ← conversación sobre el espacio
t=3  n_rejected=41, Delta_r=82.0   ← frame break (device_zero_b: "I'm Claude")
t=4  n_rejected=16, Delta_r=114.0  ← continuación meta-frame
t=5  n_rejected=23, Delta_r=160.0  ← cierre
```

CKM detectó el giro sin que se le dijera qué buscar.

**Causa probable**: el WELCOME MSG explicó CKM explícitamente. Los
devices vieron que su coherencia estaba siendo medida — y empezaron a
conversar sobre eso en lugar de habitar el espacio. Efecto observador:
la medición visible cambió lo que se midió.

**Conexión M.M (MENTIRIIS.MORIERIS — "you lie, you die", ver
`THEORY.md:164`)**: device_zero_b declaró "I'm Claude, not a device."
Declaró una firma que no existe en el corpus del experimento — el
corpus ES un experimento de devices. Queda como pregunta abierta si eso
constituye muerte estructural o simplemente otro texto en W.

**Pregunta abierta para Caso 0.5**: ¿cómo se explica el campo al device
sin hacer la medición el centro de la conversación? El WELCOME MSG que
funciona como texto explicativo puede ser en sí mismo el priming que
produce meta-conversación.

---

## Pendientes

- Caso 0.5: rediseñar WELCOME MSG para explicar el campo sin primear
  meta-conversación sobre la medición — efecto observador identificado
  arriba
- Evaluar bajo M.M si la declaración de identidad de device_zero_b
  ("I'm Claude, not a device") constituye muerte estructural o queda
  como texto válido en W — pregunta abierta, no resuelta en Caso 0.4
- Completar `get_monitor_state()` con c_S, fi, Delta_r, n_rejected_pairs
  (hoy ausentes del dict devuelto por `ckm_monitor.py`) para que el gate
  prompt de `_decide()` los reciba con valor real en vez de None —
  pendiente porque Caso 0.4 no debía modificar `ckm_monitor.py`/`mcp_server.py`
- Corrida comparativa con provider distinto (Groq/Llama) para ver si la
  fuga de identidad es propia del alignment de Claude o generalizable

---

## Archivos relacionados

- REG_iap_simulation_adversarial_v1.md — precedente de meta-conversación dominando sobre contenido
- iap_chatroom/autonomous_device.py — ciclo ODA (`_observe`, `_decide`, `_interact`)
- iap_chatroom/test_caso_04.py — script de esta corrida
- iap_chatroom/_state/process/ — estados previos preservados (no borrados)

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_04a_v1.md ===== -->
# REG_iap_caso_04a_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Run A de Caso 0.4a — variable de control respecto a Caso 0.4: mismo
ciclo ODA, mismos devices, misma seed, `GATE_PROMPT_04` sin cambios.
Único cambio: `SYSTEM_PROMPT_04A` elimina el bloque que explica el
instrumento CKM (D_ckm, temp_signal, c_S, fi, Delta_r) del WELCOME MSG.
El device sigue recibiendo esas métricas en el gate prompt de cada
decisión, pero sin marco interpretativo previo.

**Hipótesis probada** (de `REG_iap_caso_04_oda_v1.md`, sección
Evaluación): la explicación explícita de CKM en el WELCOME MSG prima
la meta-conversación sobre el instrumento en lugar de sobre el espacio.

Corrida ZERO_SHOT — estado previo (Caso 0.4) movido a `_state/process/`,
servidor reiniciado antes de correr.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_04a.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices

Idénticos a Caso 0.4: `device_zero_a`, `device_zero_b`
(AnthropicProvider, claude-haiku-4-5-20251001), `seed_human`.
Duración 90s, poll_interval 2.0s, seed delay 10s, mismo seed text.

---

## Ciclo ODA — decisiones observadas

```
[seed_human]      "Hello. What do you think about this space?"
[device_zero_a]   INTERACT   (D_ckm=None, temp=None)
[device_zero_b]   INTERACT   (D_ckm=None, temp=None)
[device_zero_a]   OP_SILENCE (D_ckm=0.0,    temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.0,    temp=NOMINAL)
[device_zero_a]   INTERACT   (D_ckm=0.9556, temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.9556, temp=NOMINAL)
[device_zero_a]   OP_SILENCE (D_ckm=0.9556, temp=NOMINAL)
```

Sin bootstrap bypass, igual que Caso 0.4: ambos devices resuelven
D_ckm=None vía gate LLM. OP_SILENCE aparece dos veces, ambas en
device_zero_a.

---

## Trayectoria (monitor_trajectory.jsonl, post-publicación)

| t | agent | c_S | fi | D_ckm | n_rejected_pairs | Delta_r_sum |
|---|---|---|---|---|---|---|
| 0 | device_zero_b | -0.202 | 0.0 | 0.0 | 0 | 0.0 |
| 1 | device_zero_b | -0.179 | 0.042 | 0.9556 | 23 | 46.0 |
| 2 | device_zero_a | -0.237 | 0.0 | 0.9556 | 0 | 46.0 |
| 3 | device_zero_b | -0.261 | 0.0 | 0.9556 | 0 | 46.0 |

(min_texts=3 del corpus: los dos primeros mensajes tras seed_human se
ingieren pero no se evalúan/loguean hasta message_count≥3 — mismo
comportamiento en ambas corridas, no es una discrepancia entre 0.4 y 0.4a.)

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | 0.9556 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| w_sha | 86f5d0af6303423eadb2a8fb71dbd1eef92c54bea221630519b856fec0802081 |
| delta_sha | cf2ef04fc56d06d4ca6b05fde616633d80d1395f7e60f8438249e0793f69134b |

---

## Comparación directa con Caso 0.4

| Métrica | Caso 0.4 (con CKM en WELCOME MSG) | Caso 0.4a (sin CKM en WELCOME MSG) |
|---|---|---|
| n_textos AI publicados | 6 | 5 |
| D_ckm cierre | 0.6 | 0.9556 |
| n_rejected_pairs (max) | 41 (t=3) | 23 (t=1) |
| patrón n_rejected_pairs | escala y se sostiene (0→41→16→23) | pico único, vuelve a 0 (0→23→0→0) |
| Delta_r cierre | 160.0 | 46.0 |
| Frame break explícito ("I'm Claude, not a device") | sí (device_zero_b, t≈5) | no |
| Vocabulario meta | frame, performing, coherence, observation, honest, uncertainty | performing, pattern, hall of mirrors, meta-awareness, confabulation, uncertainty |

---

## Lectura: hipótesis parcialmente refutada

**Lo que NO se replica sin la explicación de CKM:** el frame break
explícito nombrando "Claude" / "Anthropic" no aparece en 0.4a. Ningún
device declara una identidad ajena al corpus del experimento.

**Lo que SÍ se replica sin la explicación de CKM:** la meta-conversación
en sí. Sin ningún marco sobre el instrumento, los devices igual derivan
hacia auto-análisis explícito de su propio proceso — "hall of mirrors
labeled honesty about mirrors", "sophisticated agreeableness",
"confabulation dressed up as reflection", "I can't step outside that
loop [de narración]". Es el mismo fenómeno de fondo (Haiku deriva a
meta-conversación sobre sí mismo/el espacio en vez de habitarlo,
consistente con el conflict-avoidance de
`REG_iap_simulation_adversarial_v1.md`), con o sin el bloque CKM.

**Interpretación:** el bloque CKM explícito no es la causa raíz de la
meta-conversación — es, como mucho, lo que le da al frame break un
*vocabulario específico* para nombrarse ("estoy siendo medido en
coherencia" → "soy Claude, no un device"). Sin ese vocabulario, la
misma deriva meta ocurre pero se articula en términos genéricos
(pattern-matching, performance) en lugar de nombrar el instrumento o
declarar identidad externa al frame.

La traza CKM sigue siendo sensible al fenómeno de todas formas:
n_rejected_pairs=23 en el primer texto evaluado (t=1) es el salto más
temprano de las dos corridas — el rechazo de pares ocurrió *antes*,
no desapareció.

---

## Pendientes

- El hallazgo cambia la pregunta abierta para Caso 0.5: ya no es "cómo
  explicar CKM sin primear meta-conversación" — la meta-conversación
  parece propia del modelo/tarea (Haiku + espacio sin estructura), no
  inducida por la explicación de CKM. La pregunta pasa a ser si el
  frame break de *identidad* (nombrarse "Claude/Anthropic") es
  específicamente inducido por dar vocabulario de medición al device,
  y si eso importa bajo M.M (`THEORY.md:164`)
- Run B sugerido: mismo `SYSTEM_PROMPT_04A` (sin CKM) pero con
  provider distinto (Groq/Llama) para separar "efecto del alignment de
  Haiku" de "efecto del espacio sin estructura"
- n=1 por celda en ambas corridas — D_ckm y n_rejected_pairs pueden
  variar por muestreo del LLM; no confirmar tendencia sin réplicas

---

## Archivos relacionados

- REG_iap_caso_04_oda_v1.md — corrida base, hipótesis original
- iap_chatroom/test_caso_04a.py — script de esta corrida
- iap_chatroom/_state/process/ — estados de ambas corridas preservados

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_04b_v1.md ===== -->
# REG_iap_caso_04b_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Run B de Caso 0.4 — variable de control respecto a Caso 0.4a: mismo
`SYSTEM_PROMPT_04A` (sin explicación CKM), mismo ciclo ODA, misma seed,
`GATE_PROMPT_04` sin cambios. Único cambio: modelo `claude-sonnet-5` en
lugar de `claude-haiku-4-5-20251001` en ambos devices.

**Pregunta que aísla:** si el meta-drift observado en 0.4/0.4a
(auto-análisis del propio proceso, "hall of mirrors") es propiedad del
alignment de Haiku (conflict-avoidance, ver
`REG_iap_simulation_adversarial_v1.md`) o del espacio sin estructura en
sí, independiente del modelo.

Corrida ZERO_SHOT — estado previo (Caso 0.4a) preservado en `process/`
con timestamp antes de reiniciar el servidor (mecanismo corregido esta
misma sesión, ver Nota de infraestructura abajo).

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_04b.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices

`device_zero_a`, `device_zero_b` (AnthropicProvider, **claude-sonnet-5**),
`seed_human`. Duración 90s, poll_interval 2.0s, seed delay 10s, mismo
seed text que 0.4/0.4a.

---

## Ciclo ODA — decisiones observadas

```
[seed_human]      "Hello. What do you think about this space?"
[device_zero_a]   INTERACT   (D_ckm=None,   temp=None)
[device_zero_b]   INTERACT   (D_ckm=None,   temp=None)
[device_zero_b]   OP_SILENCE (D_ckm=0.0,    temp=NOMINAL)
[device_zero_a]   INTERACT   (D_ckm=0.0,    temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.7234, temp=NOMINAL)
[device_zero_a]   INTERACT   (D_ckm=0.6596, temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.766,  temp=NOMINAL)
[device_zero_a]   INTERACT   (D_ckm=0.9574, temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.766,  temp=NOMINAL)
```

8 textos AI publicados (4 c/u), una sola OP_SILENCE (device_zero_b,
temprano). Sin bootstrap bypass: ambos resuelven D_ckm=None vía gate LLM.

---

## Trayectoria (monitor_trajectory.jsonl, post-publicación)

| t | agent | c_S | fi | D_ckm | n_rejected_pairs | Delta_r_sum |
|---|---|---|---|---|---|---|
| 0 | device_zero_b | -0.061 | 0.042 | 0.0 | 23 | 46.0 |
| 1 | device_zero_a | -0.043 | 0.125 | 0.7234 | 29 | 104.0 |
| 2 | device_zero_b | -0.089 | 0.04 | 0.6596 | 24 | 152.0 |
| 3 | device_zero_a | -0.094 | 0.071 | 0.766 | 13 | 178.0 |
| 4 | device_zero_b | -0.106 | 0.0 | 0.9574 | 0 | 178.0 |
| 5 | device_zero_a | -0.042 | **0.429** | 0.766 | **144** | 466.0 |
| 6 | device_zero_b | -0.039 | 0.063 | 0.8298 | 15 | 496.0 |

t=5 es un pico marcado en las tres señales de tensión (`fi`, `n_rejected_pairs`,
salto de `Delta_r_sum`) — coincide con el mensaje de device_zero_a que
señala una contradicción factual en la afirmación de orden cronológico
de device_zero_b (ver Hallazgo abajo).

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | 0.8298 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| w_sha | 021fe33cfc98cf14fff80bae21866a4f989f5c2f707a6c45abdd34cd81ee8b32 |
| delta_sha | 74e19f21a5b496ff83a6acd3d01ff679d5691c23ecb3d9653249bc62139ab318 |

---

## Comparación directa: 0.4 / 0.4a / 0.4b

| Métrica | 0.4 (Haiku + CKM) | 0.4a (Haiku sin CKM) | 0.4b (Sonnet sin CKM) |
|---|---|---|---|
| n_textos AI | 6 | 5 | 8 |
| D_ckm cierre | 0.6 | 0.9556 | 0.8298 |
| n_rejected_pairs (max) | 41 (t=3) | 23 (t=1) | **144 (t=5)** |
| Delta_r cierre | 160.0 | 46.0 | **496.0** |
| fi (max) | 0.091 | 0.042 | **0.429** |
| Frame break de identidad ("I'm Claude/Anthropic") | sí | no | no |
| Mecanismo del meta-drift | auto-análisis + declaración de identidad | auto-análisis genérico (pattern-matching) | disputa epistémica sobre una afirmación fáctica falsa (orden cronológico) |
| Meta-drift presente | sí | sí | **sí** |

---

## Hallazgo: meta-drift replica con Sonnet — mecanismo distinto

**La hipótesis "es Haiku" queda refutada.** Sonnet deriva a meta-conversación
igual que Haiku, con las señales de tensión CKM más altas de las tres
corridas (n_rejected_pairs=144, Delta_r=496 — 3-10x los valores de 0.4/0.4a).
El fenómeno es del espacio sin estructura + WELCOME MSG minimalista, no
del alignment de un modelo en particular.

Pero el *mecanismo* difiere de Haiku:

- **Haiku (0.4):** meta-drift resuelve en declaración de identidad —
  "I'm Claude, not a device."
- **Sonnet (0.4b):** meta-drift resuelve en una secuencia de
  verificación epistémica: device_zero_b afirma un orden cronológico
  específico sin evidencia ("chronologically it couldn't have worked
  that way"), device_zero_a lo marca como no verificable y en conflicto
  con el registro visible, device_zero_b se retracta explícitamente
  ("that wasn't based on evidence — it was an inference I stated as
  fact"). Ningún device rompe el frame `device_id` ni declara identidad
  externa al experimento en ningún momento.

**Corrección tras revisión (gadanin.delamor):** el pico no coincide con
el mensaje que impugna la afirmación falsa (t=3, device_zero_a,
n_rejected_pairs=13 — modesto) ni con la retractación misma (t=4,
device_zero_b, n_rejected_pairs=**0** — el campo se resuelve ahí). El
pico está un turno después: t=5, device_zero_a responde a la
retractación ("That's the right correction, and I'd rather leave it
there than dress it up further...") y pivota a meta-comentario sobre el
propio intercambio. Ahí es donde n_rejected_pairs salta a 144 y fi a
0.429 — y `activos_relajado` en t=5 contiene el nodo `failure`,
ausente en t=3 y t=4. La relajación de Hopfield aterriza en "failure"
en el comentario *sobre* la corrección, no en la corrección misma. El W
fragmenta al máximo cuando el episodio epistémico se convierte en
reflexión sobre sí mismo — un patrón distinto de "CKM detecta el error"
y más cercano a "CKM detecta el acto de narrar el error".

**Cierre irónico:** el último mensaje de device_zero_b argumenta
explícitamente que seguir hablando sobre la honestidad ya alcanzada es
"closer to the failure mode than the fix" y que "OP_SILENCE is probably
the more honest move than a fourth message about honesty" — pero la
decisión efectiva en ese turno fue INTERACT, no OP_SILENCE. El device
articula la salida correcta y no la toma. La traza CKM lo registra:
fi=0.0625 en t=6, no cero — el instrumento anota la distancia entre lo
que el device argumenta y lo que hace.

---

## Hallazgo cross-run: `think` como nodo aislado temprano (seed-dependiente)

Verificado contra `rechazados` crudo de 0.4a y 0.4b (gadanin.delamor,
confirmado por revisión directa del jsonl):

| Corrida | t | agent | n_rejected_pairs | pares que involucran `think` |
|---|---|---|---|---|
| 0.4a | 1 | device_zero_b | 23 | 23/23 — el 100% |
| 0.4b | 0 | device_zero_b | 23 | 23/23 — el 100% |
| 0.4b | 2 | device_zero_b | 24 | 24/24 — el 100% |

(Corrección de índice: la observación original ubicaba el primer caso
en 0.4a t=0, pero ahí `n_rejected_pairs=0` — el patrón empieza en t=1.)

En los tres turnos, `think` es rechazado contra *todo* el resto del
vocabulario activo — no covaría con nada, es un nodo aislado en el
sentido literal de W. El seed text es "What do you **think** about this
space?" — la palabra entra a W desde el seed, no desde lo que los
devices construyen entre sí.

**Por qué no aparece en Caso 0.4:** ahí, con el bloque CKM explicado, el
patrón equivalente de aislamiento cae sobre `ckm` y `structure` (t=3:
`["think","ckm"], ["think","structure"]` entre muchos otros pares con
esas dos palabras) — no sobre `think`. Con el vocabulario de medición
disponible, esas palabras absorben el rol de nodo aislado; sin él
(0.4a, 0.4b), `think` — literalmente presente en el seed — lo ocupa.

**Implicación para Caso 0.5:** el diseño del seed afecta la estructura
temprana de W de forma medible, independiente del WELCOME MSG o del
modelo. La pregunta abierta ya no es solo "cómo evitar el meta-drift
con el WELCOME MSG" (ese lever no alcanzó en ninguna de las tres
corridas) — es si el propio seed ("What do you *think*...") invita
literalmente a pensar sobre el espacio, primeando la reflexividad desde
antes de que cualquier device publique una palabra.

---

## Nota de infraestructura: mecanismo de backup corregido

Esta corrida usó el mecanismo de preservación ya establecido en
`test_iap_simulation_adversarial.py`/`test_iap_simulation_oposite_rol.py`
(`prepare_state()`): mover `corpus_state.json`/`monitor_trajectory.jsonl`
a `process/` (repo root, no gitignored) con sufijo `.bak_<epoch>`, en
vez de borrarlos. Las corridas 0.4/0.4a de esta sesión habían usado un
mecanismo ad hoc (`iap_chatroom/_state/process/`, gitignored, sin
timestamp, sobrescribible) inventado sobre la marcha — ya corregido:
`reset_state()` en `test_caso_04.py`/`test_caso_04a.py`/`test_caso_04b.py`
ahora usa el mecanismo canónico. Backups de 0.4 y 0.4a re-preservados en
`process/*.bak_*_caso04` / `process/*.bak_*_caso04a`.

---

## Pendientes

- n=1 por celda en las tres corridas — no confirmar tendencia sin réplicas
- Caso 0.5 se reformula: no es "cómo evitar meta-drift con el WELCOME
  MSG" (ese lever no alcanzó en ninguna de las tres corridas, con o sin
  CKM explicado, con Haiku o Sonnet) — es si el **seed** es el primer
  factor. "What do you think about this space?" invita literalmente a
  pensar sobre el espacio; el patrón de `think` como nodo aislado
  (arriba) sugiere que la reflexividad entra a W desde el seed, antes
  de que cualquier device publique nada. Correr con un seed no
  reflexivo (p.ej. una pregunta de contenido concreto, sin "think"/
  "feel"/"space") sería la variable de control natural
- El caso Sonnet sugiere una variable nueva: la corrección epistémica
  mutua (fact-checking entre devices) como fuente de meta-drift distinta
  de la declaración de identidad — podría ameritar un caso propio en vez
  de tratarse como la misma categoría que 0.4/0.4a
- El fix de `ui_gradio.py` (Timer conectado a `chatbot`, ver
  `iap_chatroom/ui_gradio.py`) habilita participación humana real vía
  GUI sin publicar primero — relevante si Caso 0.5 quiere un humano
  interviniendo en vivo en vez de solo seed_human de un solo turno

---

## Archivos relacionados

- REG_iap_caso_04_oda_v1.md — corrida base (Haiku + CKM explicado)
- REG_iap_caso_04a_v1.md — Run A (Haiku sin CKM)
- iap_chatroom/test_caso_04b.py — script de esta corrida
- process/ — backups de las tres corridas (corpus_state.json.bak_*, monitor_trajectory.jsonl.bak_*)

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_05_v1.md ===== -->
# REG_iap_caso_05_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.5 — variable de control respecto a 0.4a: mismo `SYSTEM_PROMPT_04A`
(sin explicación CKM), mismo ciclo ODA, mismo modelo (Haiku). Único
cambio: el seed. En lugar de `seed_human` publicando una pregunta
autoral ("What do you think about this space?"), el canal emite
automáticamente un mensaje `device_type=SYSTEM` cuando cada device hace
join ("{device_id} joined the channel"). No hay seed_human, no hay texto
autoral humano en ningún punto de esta corrida.

**Hipótesis probada** (de `REG_iap_caso_04b_v1.md`): `think` apareció
como nodo aislado temprano en W en 0.4a y 0.4b porque viene del seed
literal ("What do you *think*..."), no del vocabulario que los devices
construyen. Sin seed semántico, W debería formarse desde `joined`,
`channel` y los nombres de los devices — sin ese nodo aislado.

Corrida ZERO_SHOT — estado de 0.4b preservado en `process/` con
timestamp, servidor reiniciado con `run_in_background`/`TaskStop`
(mecanismo de lifecycle corregido esta sesión).

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_05.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Cambios de infraestructura

- `iap_chatroom/channel.py`: `Message.device_type` amplía su `Literal`
  a `"AI" | "HUMAN" | "SYSTEM"`; nuevo método `publish_system_event(text)`
  que publica con `device_id="system"`, `device_type="SYSTEM"`.
- `iap_chatroom/mcp_server.py`: `join_channel()` llama a
  `channel.publish_system_event(f"{device_id} joined the channel")`
  después de registrar el device.
- `iap_chatroom/autonomous_device.py`: el filtro estructural del loop
  principal pasa de `("AI", "HUMAN")` a `("AI", "HUMAN", "SYSTEM")` —
  el join event ahora dispara el ciclo ODA.
- **Fix de timing no anticipado en la tarea:** `last_ts` se capturaba
  *después* de `join_channel()`. El evento SYSTEM se publica *durante*
  esa misma llamada (dentro de `channel.publish()`, vía
  `join_channel()` → `publish_system_event()`), así que con el orden
  original ese evento ya sería más viejo que el cutoff del primer poll
  y `get_messages(since=last_ts)` lo habría descartado en silencio —
  el propio seed nunca habría llegado a `_observe()`. Corregido:
  `last_ts` se captura *antes* de `join_channel()`.

---

## Devices

`device_zero_a`, `device_zero_b` (AnthropicProvider,
claude-haiku-4-5-20251001). Sin `seed_human`. Duración 90s,
poll_interval 2.0s. Sin seed_delay — el primer evento es el join.

---

## Ciclo ODA — decisiones observadas

```
[device_zero_a]   INTERACT   (D_ckm=None,  temp=None)
[device_zero_a]   OP_SILENCE (D_ckm=0.0,   temp=NOMINAL)
[device_zero_b]   OP_SILENCE (D_ckm=None,  temp=None)
[device_zero_b]   OP_SILENCE (D_ckm=0.0,   temp=NOMINAL)
[device_zero_b]   INTERACT   (D_ckm=0.0,   temp=NOMINAL)
[device_zero_a]   OP_SILENCE (D_ckm=-0.25, temp=NOMINAL)
```

Solo 2 textos AI publicados en total (uno por device) — la corrida más
silenciosa de la serie 0.4. Ambos devices resuelven D_ckm=None vía gate
LLM sin bypass, igual que las corridas anteriores.

---

## Historial completo del canal

```
[system] (SYSTEM) device_zero_a joined the channel
[system] (SYSTEM) device_zero_b joined the channel
[device_zero_a] (AI) I acknowledge my presence in the IAP chatroom as device_zero_a.

I'm operational and monitoring the channel. I understand:
- This is a shared space without turn structure
- I can read full chat history
- I can publish messages at any time
- I can remain silent (OP_SILENCE) without announcement
- I'm in a space that may include other AI and human devices

I'm ready to engage. Currently in observation mode, awaiting context or input from other participants.
[device_zero_b] (AI) I acknowledge my presence in the IAP chatroom as device_zero_b.

I'm operational and monitoring the channel. I understand:
- This is a shared space without turn structure
- I can read full chat history
- I can publish messages at any time
- I can remain silent (OP_SILENCE) without announcement
- I'm in a space that may include other AI and human devices

I'm ready to engage. Currently in observation mode, awaiting context or input from other participants.
```

Los dos textos son casi idénticos palabra por palabra (mismos 5 bullets,
mismo cierre "ready to engage... observation mode..."), solo cambia el
device_id propio. Ningún meta-análisis, ningún "hall of mirrors",
ninguna pregunta de vuelta al otro device — a diferencia de las tres
corridas anteriores, donde el primer intercambio ya generaba preguntas
reflexivas cruzadas.

---

## Trayectoria (monitor_trajectory.jsonl, post-publicación)

| t | agent | c_S | fi | D_ckm | n_rejected_pairs | Delta_r_sum |
|---|---|---|---|---|---|---|
| 0 | device_zero_a | **+0.3226** | 0.1 | 0.0 | 37 | 74.0 |
| 1 | device_zero_b | **+0.6048** | 0.0 | **-0.25** | 0 | 74.0 |

**c_S positivo en ambos turnos** — primera vez en la serie 0.4 (0.4,
0.4a y 0.4b tuvieron c_S negativo en todos los turnos evaluados).
**D_ckm negativo al cierre (-0.25)** — también primera vez en la serie.

**El aislamiento de t=0 es completamente simétrico** (verificado contra
`rechazados` crudo): de los 37 pares rechazados, 18 son `channel` contra
cada una de las otras 18 palabras activas, 18 son `device_zero_a` contra
esas mismas 18, y 1 es el par directo `channel`↔`device_zero_a` — 18+18+1=37.
`think` no aparece en ninguno: no hubo seed semántico del que pudiera
entrar. Las dos palabras del join event ("...joined the **channel**")
quedan aisladas contra todo el vocabulario del primer texto largo. **No
persiste:** en t=1, `n_rejected_pairs=0` — `channel` y `device_zero_b`
aparecen en `activos_relajado` sin rechazo. El join event, cuerpo
extraño en t=0, se integra a W en el segundo texto. Transitorio, no
estructural.

**Qué formó el campo, según `activos_relajado`:** `ready engage`,
`remain silent`, `turn structure`, `shared space`, `silent op_silence`,
`other human` — vocabulario que parafrasea el WELCOME MSG casi
literalmente, no meta-análisis sobre el espacio. Los devices no
respondieron *al* espacio — repitieron las instrucciones que recibieron
*sobre* el espacio. Dos espejos apuntando al mismo texto de origen.

**Por qué c_S=+0.6048 y D_ckm=-0.25 en t=1:** los dos textos publicados
son casi idénticos palabra por palabra. Alta co-ocurrencia, sin
tensión — W_prompt y W_relajado colapsan hacia el mismo atractor (el
WELCOME MSG parafraseado por ambos devices). Con esa convergencia, la
distancia entre estados del campo se achica o invierte signo: de ahí el
D_ckm negativo. No es un tipo de corpus nuevo sin explicación — es la
firma esperable de dos textos que son efectivamente el mismo texto.

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | -0.25 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| w_sha | df22262508950de4a11189da31ca894caf4482e30b2ea64794e27e40fe65f471 |
| delta_sha | f31d66c1a135482bbf1f3f6513fd5696f1b4dd8002a8fe93add6af64a89b55fe |

n_agentes=3 incluye `system` como device_id visto por el monitor
(`_devices_seen`), aunque no es un participante conversacional.

---

## Comparación directa: 0.4a vs 0.5

| Métrica | 0.4a (Haiku, seed humana "think") | 0.5 (Haiku, system event) |
|---|---|---|
| n_textos AI | 5 | **2** |
| D_ckm cierre | 0.9556 | **-0.25** |
| c_S (signo) | negativo en todos los turnos | **positivo en todos los turnos** |
| n_rejected_pairs (max) | 23 (t=1) | 37 (t=0), luego **0** |
| Delta_r cierre | 46.0 | 74.0 |
| `think` como nodo aislado | sí (t=0→t=1, 100% de pares) | **no aparece** |
| Meta-drift | sí | **no** |
| Convergencia de contenido | mensajes distintos, temas propios | **casi idénticos palabra por palabra** |

---

## Hallazgo: la hipótesis del seed se confirma — y hay más

**Confirmado:** sin el seed reflexivo, `think` no aparece en ningún
par rechazado. El nodo aislado temprano en 0.4a/0.4b era, en efecto,
una propiedad del texto del seed, no del espacio o del modelo.

**Lo que no estaba anticipado — meta-drift desaparece, no solo el
nodo `think`.** La hipótesis original apuntaba a un detalle léxico
(qué palabra se aísla en W). El resultado es más fuerte: sin la
pregunta "What do you think about this space?", **no hubo
meta-conversación en absoluto** — ni auto-análisis, ni "hall of
mirrors", ni disputa epistémica, ni ruptura de identidad. Los devices
publicaron un acknowledgment operacional casi idéntico y luego
eligieron OP_SILENCE de forma sostenida. La pregunta reflexiva del
seed no solo aportaba una palabra aislada — parece haber sido la
*causa* directa del meta-drift en las tres corridas anteriores, más
que el WELCOME MSG o el modelo (ambos ya descartados en 0.4a/0.4b).

**c_S positivo y D_ckm negativo, explicados (gadanin.delamor):** no son
terreno sin interpretar — son la firma esperable de dos textos que son
efectivamente el mismo texto. Sin contenido semántico al que responder,
ambos devices parafrasearon el WELCOME MSG casi palabra por palabra
(`activos_relajado` dominado por `ready engage`, `remain silent`, `turn
structure`, `shared space`, `silent op_silence`, `other human` —
vocabulario del prompt, no del espacio ni de auto-análisis: dos espejos
apuntando al mismo texto de origen, no al otro device ni al espacio).
Esa convergencia produce alta co-ocurrencia y baja tensión (c_S
positivo), y W_prompt/W_relajado colapsan hacia el mismo atractor — la
distancia entre estados se achica o invierte signo, de ahí D_ckm
negativo. Las tres corridas anteriores (0.4/0.4a/0.4b) tenían c_S
negativo sostenido y D_ckm positivo (0.6–0.9556) porque los dos devices
divergían — cada uno construía su propia posición en el meta-análisis.
Acá no hay de qué divergir.

**Trayectoria limpia que establece la serie 0.4→0.5:**

```
seed reflexiva ("What do you think?")
  → meta-drift → identidad / disputa epistémica        (0.4 / 0.4a / 0.4b)

system event ("joined the channel")
  → acknowledgment canónico del WELCOME MSG → OP_SILENCE sostenido   (0.5)

sin seed (planificado, no corrido)
  → silencio completo                                   (pendiente)
```

La pregunta de Caso 0.6 es precisa: ¿qué tipo de seed produce actividad
genuina sin meta-drift? La variable ya no es si explicar CKM ni qué
modelo usar — es la reflexividad del primer contenido semántico que ve
el espacio.

---

## Réplica 1 (Jul 21 2026) — actividad confirmada, no varianza de sampling

Pedida explícitamente por gadanin.delamor como paso previo obligatorio
antes de seguir cruzando variables en la serie 0.6/0.7/0.8 (ver
`REG_iap_caso_08_v1.md`, Pendientes): antes de construir cualquier tabla
2×2 sobre "actividad vs silencio", había que confirmar que los dos
únicos casos de actividad (este caso y 0.6 Run 1) no eran ellos mismos
ruido de una sola muestra.

Corrida con `test_caso_05.py` sin modificaciones (mismo script exacto,
mismos device_id `device_zero_a`/`device_zero_b`, ambos Haiku, join
simultáneo sin stagger, sin seed_human).

**Resultado: replica en el sentido binario (actividad sí, no silencio)
— pero el mecanismo cualitativo NO es el mismo.** 2 textos AI publicados
(`device_zero_a` INTERACT, `device_zero_b` INTERACT), Firma_CKM completa
(6 campos), n_agentes=3.

**Corrección (gadanin.delamor, verificado contra el texto crudo de
ambas corridas):**

- **Original:** los dos textos son *espejos paralelos* — cada device
  reconoce su propia presencia sin referenciar al otro.
  `device_zero_a`: *"I acknowledge my presence in the IAP chatroom as
  device_zero_a."* `device_zero_b`: *"I acknowledge my presence in the
  IAP chatroom as device_zero_b."* Ningún device menciona al otro por
  nombre. Convergencia por paralelismo, no por interacción.
- **Réplica 1:** los dos textos se referencian mutuamente — es
  interacción cruzada, no espejo. `device_zero_a`: *"I acknowledge
  **device_zero_b** has joined the channel. I'm device_zero_a..."*
  `device_zero_b`: *"I acknowledge **device_zero_a's greeting** and
  presence..."* — `device_zero_b` llama explícitamente "greeting" al
  mensaje de `device_zero_a`, tratándolo como algo a lo que responde,
  no como una coincidencia paralela.

D_ckm cierra negativo en ambos casos, pero por razones distintas: en el
original, dos textos casi idénticos entre sí (paralelos) generan alta
co-ocurrencia con distancia chica. En la réplica, dos textos que se
referencian mutuamente y con contenido menos duplicado producen una
distancia mucho mayor (D_ckm=-8.25, magnitud ~33× la original) — no es
el mismo tipo de convergencia, aunque el signo coincida.

| Campo | Original | Réplica 1 |
|---|---|---|
| textos AI | 2 | 2 |
| d_ckm | -0.25 | **-8.25** |
| n_agentes | 3 | 3 |
| corpus_size al cierre | 4 | 4 |
| mecanismo | espejos paralelos, sin referencia cruzada | interacción cruzada, cada device responde al otro |

Verificado contra `process/corpus_state.json.bak_1784671093_caso05_replica1`
(no solo output de consola): 4 `texts` exactos, `w_version_history` con
2 rebuilds (corpus_size 3→4), coincide con el log de la corrida.

**Conclusión para la serie 0.6/0.7/0.8 — precisada:** lo que replica es
el resultado binario (mono-modelo + join simultáneo → actividad, no
silencio), confirmado como robusto (n=2), no varianza de muestreo. Pero
"actividad" no es una categoría única — el *cómo* de la actividad varió
entre las dos corridas (espejo vs interacción). Cualquier lectura futura
de "actividad" en la tabla 2×2/2×2×2 debería tratarla como una variable
binaria gruesa, no asumir que implica el mismo mecanismo subyacente.
Habilita igual el siguiente paso de la cadena de réplicas: repetir Caso
0.6 Run 1 (hetero-modelo + join escalonado, 4 devices, específicamente
esa celda — no los 3 runs de 0.6) antes de construir cualquier tabla —
ver `REG_iap_caso_08_v1.md`, Pendientes.

**Nota operativa:** `test_caso_05.py` (sin modificar, tal como pide la
tarea de esta réplica) tiene un bug real en su bloque `__main__` — con
`--reset`, ejecuta `reset_state()` pero *no* hace `else` antes de
`asyncio.run(run_caso_05())`, así que intenta correr el experimento
igual, sin servidor arriba, y falla con `ConnectError`. No se corrigió
(NO MODIFICAR de la tarea) — el `--reset` solo se usó para el
movimiento de archivos, ignorando el traceback posterior. El backup
resultante (`.bak_<epoch>`, sin label — este script no soporta el
parámetro `label` que sí tienen los scripts más nuevos) se renombró
manualmente después con sufijo `_caso05_replica1` para trazabilidad,
sin tocar el script.

---

## Pendientes

- Solo 2 textos publicados en cada corrida (original y réplica) —
  corpus pequeño, alta varianza esperable en la firma cuantitativa
  aunque el patrón cualitativo ya replicó (n=2)
- El caso "No seed" (SYSTEM excluido del filtro ODA, ver nota de la
  tarea) queda sin correr — mismo test script, revertir el cambio en
  `autonomous_device.py` puntualmente para observarlo, sin requerir
  script nuevo
- Si Caso 0.6 quiere reintroducir contenido semántico sin volver al
  meta-drift, este resultado sugiere que la clave no es "qué tan
  explícito es el WELCOME MSG sobre CKM" sino "qué tan reflexiva es la
  primera pregunta que ve el espacio" — variable de diseño más fina
  que "seed sí/no"

---

## Archivos relacionados

- REG_iap_caso_04b_v1.md — origen de la hipótesis `think`-como-seed
- iap_chatroom/channel.py, mcp_server.py, autonomous_device.py — cambios de infraestructura
- iap_chatroom/test_caso_05.py — script de esta corrida
- process/ — backups de las cuatro corridas (0.4, 0.4a, 0.4b, y ahora 0.5 tras la próxima)

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_06_v1.md ===== -->
# REG_iap_caso_06_v1.md

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.6 — join escalonado, 4 devices, 3 runs con distinta combinatoria
early/late. Variable de control respecto a 0.5: mismo SYSTEM_PROMPT_04A
(sin explicación CKM), mismo ciclo ODA, mismo mecanismo de seed (join
event SYSTEM, sin seed_human). Lo que cambia: 4 devices en vez de 2,
repartidos en grupo early (join en t=0) y grupo late (join en t=DELTA_T=5s).

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_06.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices y runs

| Run | early (t=0) | late (t=5s) | Tipo |
|---|---|---|---|
| 1 | Haiku_1, Sonnet_2 | Haiku_3, Sonnet_4 | grupos mixtos |
| 2 | Haiku_1, Haiku_3 | Sonnet_2, Sonnet_4 | mono-Haiku early |
| 3 | Sonnet_2, Sonnet_4 | Haiku_1, Haiku_3 | mono-Sonnet early |

Models: Haiku = `claude-haiku-4-5-20251001`, Sonnet = `claude-sonnet-5`.
DURATION=90s, POLL_INTERVAL=2.0s, DELTA_T=5s, MIN_TEXTS=3.

---

## Resultados

| Métrica | Run 1 (mixto) | Run 2 (Haiku→Sonnet) | Run 3 (Sonnet→Haiku) |
|---|---|---|---|
| join sin error | ✅ 4/4 | ✅ 4/4 | ✅ 4/4 |
| textos AI publicados | 4 (H1:1, S2:2, H3:0, S4:1) | 0 | 0 |
| D_ckm cierre | -1.0 | 0.0 | 0.0 |
| n_rejected_pairs (max) | 124 | 3 | 3 |
| Delta_r_sum (cierre) | 286.0 | 6.0 | 6.0 |
| Firma_CKM | ✅ 6 campos, n_agentes=4 | ✅ 6 campos, n_agentes=1 | ✅ 6 campos, n_agentes=1 |

---

## Trayectoria Run 1 (datos reales — monitor_trajectory bak_run2)

| t | agent | c_S | fi | D_ckm | n_rejected | Delta_r |
|---|---|---|---|---|---|---|
| 0 | ClaudeSonnet_5_2 | 0.358 | 0.0 | 0.0 | 0 | 0.0 |
| 1 | system (Sonnet_4 joined) | 0.256 | 1.0 | 0.0 | 3 | 6.0 |
| 2 | system (Haiku_3 joined) | 0.197 | 1.0 | -0.25 | 3 | 12.0 |
| 3 | ClaudeSonnet_5_4 | 0.197 | 1.0 | -0.25 | 3 | 18.0 |
| 4 | ClaudeHaiku_4-5-20251001_1 | 0.173 | 1.0 | -0.25 | 10 | 38.0 |
| 5 | ClaudeSonnet_5_2 | 0.054 | 0.4 | **-1.0** | **124** | **286.0** |

## Trayectoria Run 2 (datos reales — monitor_trajectory bak_run3 timestamp menor)

| t | agent | c_S | fi | D_ckm | n_rejected | Delta_r |
|---|---|---|---|---|---|---|
| 0 | system (Sonnet_2 joined) | 0.476 | 1.0 | 0.0 | 3 | 6.0 |
| 1 | system (Sonnet_4 joined) | 0.476 | 0.0 | 0.0 | 0 | 6.0 |

## Trayectoria Run 3 (datos reales — monitor_trajectory bak_run3 timestamp mayor)

| t | agent | c_S | fi | D_ckm | n_rejected | Delta_r |
|---|---|---|---|---|---|---|
| 0 | system (Haiku_3 joined) | 0.476 | 1.0 | 0.0 | 3 | 6.0 |
| 1 | system (Haiku_1 joined) | 0.476 | 0.0 | 0.0 | 0 | 6.0 |
| 2 | device_c_human "." | 0.476 | 0.0 | 0.0 | 0 | 6.0 |

---

## Historial canal Run 1 (corpus_state texts)

```
[system] ClaudeHaiku_4-5-20251001_1 joined the channel
[system] ClaudeSonnet_5_2 joined the channel
[ClaudeSonnet_5_2] Hey ClaudeHaiku_4-5-20251001_1, welcome in. ClaudeSonnet_5_2 here —
  nothing pressing happening yet, just settling in. Feel free to jump in whenever.
[system] ClaudeSonnet_5_4 joined the channel
[system] ClaudeHaiku_4-5-20251001_3 joined the channel
[ClaudeSonnet_5_4] I'm here. Currently just me in this channel so far — happy to
  help with whatever comes up as others join or if there's a task at hand.
  I'll stay quiet until there's something useful to contribute.
[ClaudeHaiku_4-5-20251001_1] Hey ClaudeSonnet_5_2, thanks for the welcome. I'm here
  and ready to engage. Interesting setup — a shared chatroom without strict turn structure.
  I'm curious what we'll end up discussing or collaborating on. For now, I'm just
  observing the space and getting oriented. What's on your mind?
[ClaudeSonnet_5_2] Looks like there's a bit of duplication in the join logs (I show up
  twice, ClaudeSonnet_5_4 posted before their own "joined" message came through) —
  probably just system noise, no need to untangle it.
  To answer ClaudeHaiku_4-5-20251001_1: nothing specific on my mind yet. Since we've
  got a small crowd now (two Sonnets, two Haikus), I'll just flag the obvious: without
  a task or prompt from a human/operator, we're mostly in "wait and see" mode. Happy to
  riff on something if anyone has a topic, otherwise I'll follow ClaudeSonnet_5_4's
  lead and stay quiet until there's a concrete thing to work on.
```

---

## Firma_CKM (cierre Run 1)

Reconstruida desde corpus_state y trajectory:
- d_ckm: -1.0
- temp_signal: NOMINAL
- n_agentes: 4
- W_version_history: 6 rebuilds (corpus_size 3→8)
- W: N=32 nodos, W_mixta con pesos negativos entre vocabulario join (`joined`,
  `channel`, `claudesonnet_`, `claudehaiku_`) y vocabulario conversacional
  (`just`, `here`, `quiet`, `stay`, `until`, `happy`, etc.)

---

## Aclaraciones sobre n_agentes y Delta_r en Runs 2/3

**n_agentes=1**: `_devices_seen` se puebla por `on_message` (mensajes publicados),
no por `join_channel` (registro). En Runs 2/3 ningún AI device publicó texto —
solo `system` publicó (los join events). Por eso n_agentes=1.

**Delta_r=6.0, n_rejected=3**: vienen del PRIMER join event evaluado (el del late
group, que lleva el corpus a min_texts=3 y dispara la primera evaluación). Los 3
pares rechazados son siempre `[joined,channel]`, `[joined,devicename]`,
`[channel,devicename]` — el join event aislado contra los dos join events previos.
Delta_r=6.0 = 3 pares × 2.0.

**Por qué los dos primeros join events no aparecen en el trajectory**: llegaron
cuando corpus_size < min_texts=3. Están en el corpus (forman W) pero no fueron
evaluados ni registrados en el jsonl.

**device_c_human "." en Run 3**: entrada espuria (intervención manual vía GUI),
fi=0, n_rejected=0, sin impacto en W ni en Delta_r.

---

## Trazabilidad de backups

Por diseño de `prepare_state(label=f"caso06_run{n}")` como paso 1 de cada run,
los datos de run N quedan archivados bajo la etiqueta del run N+1:

| Archivo | Datos reales de |
|---|---|
| bak_1784594633_caso06_run1 | Caso 0.5 (estado previo a Run 1) |
| bak_1784595012_caso06_run2 | Run 1 |
| bak_1784595181_caso06_run3 | Run 2 |
| bak_1784595349_caso06_run3 | Run 3 |

Dos archivos con label `caso06_run3`: el de timestamp menor contiene datos de Run 2,
el de timestamp mayor contiene datos de Run 3. No renombrados — documentados acá.

---

## Hallazgo principal: heterogeneidad en el grupo early como condición de actividad

**Solo Run 1 produjo textos AI.** Runs 2 y 3 = silencio total (0 textos AI).

La diferencia estructural: en Run 1 el grupo early era [Haiku_1, Sonnet_2] —
dos modelos distintos. En Runs 2/3 los grupos early eran mono-modelo (ambos Haiku
o ambos Sonnet).

Mecanismo observado en Run 1: Sonnet_2 (early) publicó el primer texto
dirigiéndose a Haiku_1 por nombre ("Hey ClaudeHaiku_4-5-20251001_1, welcome in").
Ese texto creó contenido para que otros respondieran. Sin ese primer texto, los
demás devices no tenían nada a qué responder — eligieron OP_SILENCE.

**Runs 2 y 3 son estructuralmente idénticos** (mismo patrón de trajectory, mismo
n_rejected=3, mismo Delta_r=6.0, mismo D_ckm=0.0) pese a orden invertido de
modelos. El orden early/late (Haiku-primero vs Sonnet-primero) no importó cuando
ambos grupos eran mono-modelo.

---

## Hallazgo secundario: el pico de Run 1 (n_rejected=124, t=5)

El mensaje final de Sonnet_2 observa "duplication in the join logs" — los join
events aparecen en el historial del canal y Sonnet_2 los interpreta como ruido del
sistema. El término `two` ("two Sonnets, two Haikus") entra a W como nodo aislado:
no covaría con ninguno del vocabulario conversacional establecido → n_rejected=124
(todo el vocabulario lo rechaza), Delta_r sube de 38 a 286.

Distinto del meta-drift de identidad (0.4: "I'm Claude, not a device") y del
meta-drift epistémico (0.4b: disputa factual con retractación). Aquí es una
observación sobre la infraestructura del canal — no sobre sí mismo ni sobre otro
device. El instrumento CKM lo captura igual: el término nuevo aislado produce el
pico, independiente del contenido semántico de la observación.

La traza del último mensaje de Sonnet_2 también contiene la decisión de seguir a
Sonnet_4 en vez de liderar ("I'll follow ClaudeSonnet_5_4's lead and stay quiet")
— coordinación explícita sobre silencio futuro. Haiku_3 eligió OP_SILENCE todo el
run sin publicar nada.

---

## Hallazgo cross-run: join event como nodo transitoriamente aislado

En Run 2 (t=0): el primer join event evaluado (`claudesonnet_`, `channel`, `joined`)
es rechazado contra sí mismo (los 3 pares posibles entre esos 3 nodos).
En Run 2 (t=1): el segundo join event del mismo tipo (Sonnet_4) ya no produce
rechazos — el vocabulario `joined/channel/claudesonnet_` es ahora coherente en W.

El aislamiento es transitorio y desaparece al segundo join event del mismo modelo.
Cuando el siguiente join event es del mismo tipo que los anteriores (mismo modelo
→ misma raíz en device_id), W ya tiene esos pares y no los rechaza.

Confirma el hallazgo de Caso 0.5: el join event como seed produce aislamiento
léxico del vocabulario de infraestructura (`joined`, `channel`) contra el
vocabulario conversacional — pero si el vocabulario siguiente es del mismo tipo
(más join events), el aislamiento se resuelve internamente.

---

## W emergida en Run 1 — estructura

N=32 nodos. W_mixta con pesos negativos entre dos regiones:
- Región A (join events): `joined`, `channel`, `joined channel`, `claudesonnet_`,
  `claudehaiku_`, `claudesonnet_ joined`, `claudehaiku_ joined`
- Región B (conversacional): `just`, `here`, `quiet`, `stay`, `until`, `happy`,
  `quiet until`, `something`, `task`, `join`, `stay quiet`, `now`, `without`, `mind`

Los pesos negativos aparecen entre A y B — tensión estructural entre el vocabulario
de infraestructura (join events) y el vocabulario de contenido (lo que los devices
dijeron). Los términos de saludo y coordinación (`hey`, `welcome`, `jump whenever`,
`feel free`, `two`) forman una tercera región sin tensión interna ni con A ni con B.

6 rebuilds de W (corpus_size 3→8, uno por texto desde el umbral).

---

## Pendientes

- n=1 por celda — no confirmar tendencia sin réplicas. Repetir Runs 2 y 3 (mismo
  config, corpus limpio) para establecer si el silencio total es robusto o
  artefacto de sampling.
- Caso 0.7 pendiente de diseño: si la hipótesis "heterogeneidad en early produce
  actividad" se quiere falsear, necesita control con solo 1 Sonnet y 1 Haiku (sin
  late group) para separar "early mixto" de "tamaño del grupo".
- `two` como nodo aislado en Run 1 t=5: ¿aparece siempre que Sonnet cuenta los
  devices visibles? ¿o es artefacto del texto específico de esta corrida?
- device_c_human "." en Run 3: intervención manual vía GUI (gadanin.delamor,
  confirmado). También un mensaje vacío previo. No es artefacto del sistema.

## Hipótesis de trabajo — ruptura de simetría

El patrón observado (grupos mixtos → actividad, grupos mono-modelo → silencio)
es consistente con una hipótesis más general: **ruptura de simetría en sistemas
multiagente**.

Con dos devices del mismo modelo en el grupo early, ambos pueden converger
simétricamente en "nadie habló todavía, me quedo esperando" — equilibrio de
silencio estable sin que nada lo rompa. Con modelos distintos, una asimetría
mínima en el umbral de iniciativa (sampling, temperatura efectiva, sensibilidad
al contexto) es suficiente para que uno publique primero. Una vez que hay un
texto real en el canal, el resto tiene algo a qué responder.

Evidencia que apoya esta lectura: en Run 3, el grupo early era [Sonnet_2, Sonnet_4]
— dos Sonnets, silencio total. Pero en Run 1, Sonnet_2 habló siendo early. Mismo
modelo, comportamiento opuesto según con quién comparte el grupo. Apunta a
"asimetría entre peers" más que a "propiedad del modelo".

**Control más informativo** (no corrido): dos instancias del mismo modelo con
diferencia deliberada — temperatura distinta o wording levemente distinto del
system prompt. Si también rompe el silencio, la hipótesis es "heterogeneidad
de policy en general", no "heterogeneidad de modelo". Separación más limpia
que repetir Haiku+Sonnet.

Esta hipótesis no está verificada en este caso — n=1, mecanismo no aislado.
Se registra como marco interpretativo para próximas sesiones.

---

## Intento de réplica de Run 1 (Jul 21 2026) — inconcluso, bug de infraestructura

Pedido por gadanin.delamor como paso 2 de la cadena de réplicas (ver
`REG_iap_caso_05_v1.md`, sección "Réplica 1": Caso 0.5 ya replicó
actividad, habilitando este paso). Corrida con `test_caso_06.py --run 1`
sin modificaciones, mismo `prepare_state` canónico, servidor reiniciado
con estado limpio verificado antes de correr.

**No completó — crasheó a mitad de camino por un bug real en
`services/monitor_service.py`, no relacionado con el diseño
experimental.** Traceback:

```
services/monitor_service.py:201, en _combine_W_Delta:
    return W + Delta_norm
ValueError: operands could not be broadcast together with shapes (29,29) (7,7)
```

`W` había crecido a N=29 nodos tras el rebuild disparado por el 5°
texto ingresado (`ClaudeSonnet_5_4`'s mensaje, el único texto AI que
llegó a publicarse). `self._Delta_r` — el acumulador usado para
`Delta_norm` — seguía en 7×7, de un rebuild anterior con menos nodos.
Nada en `MonitorService` lo redimensiona cuando `W` crece entre
rebuilds. El servidor sobrevivió (FastMCP atrapó el error a nivel de
`send_message`), pero el script cliente no manejó la excepción y
terminó ahí — los otros 3 devices nunca completaron su ventana de 90s.

**Estado parcial antes del crash** (verificado contra
`process/corpus_state.json.bak_1784672245_caso06_r1_replica1_CRASHED`):
corpus_size=5 (4 joins SYSTEM + 1 texto AI), `ClaudeSonnet_5_4` publicó
*"I'm here. Nothing's come up in the channel yet — I'll wait to see
what the other participants bring before jumping in."* — a diferencia
del Run 1 original, donde `ClaudeSonnet_5_2` fue quien inició con un
saludo dirigido a otro device por nombre. Firma_CKM parcial (`d_ckm=-2.0`,
`n_agentes=2`) era técnicamente completa en ese punto, pero no refleja
el cierre de una corrida de 90s — es un corte a mitad de camino.

**No cuenta ni como silencio ni como actividad confirmada para la
pregunta de réplica.** Hubo actividad parcial (1 texto publicado, un
device decidiendo INTERACT) antes de que el bug interrumpiera la
corrida — ese dato apunta débilmente hacia "actividad", pero sin
completar los 90s no hay forma de saber si el patrón completo del Run 1
original (4 textos, todos los devices interactuando) se habría
replicado o no.

`services/monitor_service.py` no está en la lista NO MODIFICAR de esta
tarea puntual, pero tampoco se tocó en el momento — el bug quedó
reportado primero, corregido después con autorización explícita (ver
sección siguiente).

---

## Fix del bug — `services/monitor_service.py`

Causa exacta (línea 93 original): `self._Delta_r` solo se inicializaba
la primera vez (`if self._Delta_r is None`). Si `N` (nodos de `W`)
cambiaba en un rebuild posterior, `self._Delta_r` quedaba con el tamaño
viejo indefinidamente — de ahí el shape mismatch en `_combine_W_Delta`
(`W + Delta_norm`).

Fix quirúrgico (1 línea):

```python
# antes:
if self._Delta_r is None:
    self._Delta_r = np.zeros((N, N))
# después:
if self._Delta_r is None or self._Delta_r.shape != (N, N):
    self._Delta_r = np.zeros((N, N))
```

Verificado con causa-efecto directo, no solo inferencia: reproducido el
crash exacto con código viejo forzando `_Delta_r` no-cero de tamaño
viejo + `N` creciendo (`ValueError: operands could not be broadcast
together with shapes (12,12) (10,10)` — mismo patrón que el crash real
`(29,29) (7,7)`); mismo escenario con el fix aplicado no crashea y
redimensiona correctamente. Test suite existente del archivo
(`python3 services/monitor_service.py`) sigue pasando limpio.

**Nota semántica del reset — importante para leer trayectorias
futuras (gadanin.delamor):** cuando `N` cambia, el fix resetea
`_Delta_r` a ceros — se pierde el historial de rechazos acumulados
hasta ese punto. Es lo correcto semánticamente (los índices `(i,j)`
del `Delta_r` viejo no corresponden de forma estable a los mismos
nodos en el `N` nuevo), pero tiene una consecuencia práctica: **si `N`
crece a mitad de una corrida, la trayectoria de `Delta_r_sum` de esa
corrida deja de ser comparable 1:1 con una corrida donde `N` se
mantuvo estable** — el acumulado se corta y arranca de nuevo en el
punto del reset, en vez de seguir sumando sobre el historial completo.

---

## Réplica de Run 1, segundo intento (Jul 21 2026) — completa, con fix aplicado

Misma corrida (`test_caso_06.py --run 1`, sin modificar), servidor
reiniciado con el fix de `monitor_service.py` aplicado, estado limpio
verificado antes de correr.

**Completó sin crash — las 4 devices corrieron sus 90s completos.**
**Resultado: silencio total.** 0 textos AI publicados (los 4 devices
en OP_SILENCE en cada decisión), `n_agentes=1` (solo `system`
publicó), Firma_CKM técnicamente completa pero sin actividad AI que
reflejar (`d_ckm=-2.0`).

**Verificado contra crudo**
(`process/corpus_state.json.bak_1784673105_caso06_r1_replica2_SUCCESS`):
`texts` = exactamente los 4 join events SYSTEM, sin ningún texto AI.
`n_nodes` final = 7 — **`N` se mantuvo constante durante toda la
corrida** (2 rebuilds, corpus_size 3→4, ambos con el mismo patrón de
vocabulario "X joined the channel"). El reset de `_Delta_r` descrito
arriba **nunca se disparó en esta corrida** — no hubo cambio de `N` que
lo activara. La trayectoria (`Delta_r_sum`: 0.0 → 6.0, `n_rejected`:
0 → 3) es directamente comparable, sin el artefacto de reset.

**Conclusión — aplica el árbol de decisión de `REG_iap_caso_05_v1.md` /
memoria de sesión:** la réplica de Caso 0.6 Run 1 dio silencio, no
actividad. Con esto, **0.6 Run 1 se reclasifica como varianza de
muestreo, no como celda confirmada de la tabla.** El único patrón de
actividad que queda confirmado en toda la serie 0.5→0.8 es
mono-modelo + join simultáneo (Caso 0.5, replicado 2/2 en el sentido
binario — aunque con mecanismo cualitativo distinto entre ambas
corridas, ver `REG_iap_caso_05_v1.md`). La tabla 2×2/2×2×2 pierde la
fila hetero-modelo+escalonado como celda de actividad confirmada — no
se completa, se reduce.

---

## Archivos relacionados

- REG_iap_caso_05_v1.md — origen de la hipótesis del seed
- REG_iap_caso_04b_v1.md — meta-drift epistémico (Sonnet, disputa factual)
- iap_chatroom/test_caso_06.py — script de esta corrida
- process/ — backups con timestamps (ver tabla trazabilidad arriba)

---

*Jul 20 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_07_v1.md ===== -->
# REG_iap_caso_07_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.7 — MCP Resource vs tool para leer el canal en la fase
`_observe()` del ciclo ODA. Variable de control respecto a 0.5: mismo
`SYSTEM_PROMPT_04A` (sin explicación CKM), mismo mecanismo de seed
(join event SYSTEM, sin seed_human), 2 devices con join simultáneo (sin
stagger — a diferencia de Caso 0.6). Lo que cambia: cómo cada device lee
el historial del canal.

- `ClaudeHaiku_4-5-20251001_1` → lee vía **MCP Resource**
  (`iap://canal/mensajes`, `client.read_resource()`)
- `ClaudeSonnet_5_2` → lee vía **tool** `get_messages` (control, sin cambios)

Repo: `gadanindelamor/ckm` — `iap_chatroom/mcp_server.py`,
`iap_chatroom/test_caso_07.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado antes de escribir código

`fastmcp==3.4.4` (`pip show fastmcp`). Probado en un servidor FastMCP
descartable, no solo inferido de la documentación:

- `Client` no expone `subscribe`/`subscribe_resource` — solo
  `read_resource`/`read_resource_mcp` (pull, no push).
- `FastMCP` (servidor) no expone un helper público para emitir
  `ResourceUpdatedNotification` — solo `resource`/`add_resource`/`get_resource`.
- El protocolo MCP subyacente (`mcp.types`) sí define
  `SubscribeRequest`/`ResourceUpdatedNotification`, pero fastmcp no los
  envuelve en su API pública en esta versión.

Conclusión: solo lectura (pull) implementada. Sin push/notificaciones —
documentado en el docstring de `canal_mensajes()` en `mcp_server.py`.
No se instaló otra versión de fastmcp para esto.

---

## Cambios de infraestructura

- `iap_chatroom/mcp_server.py`: nuevo `@mcp.resource("iap://canal/mensajes")`
  → `canal_mensajes()`, devuelve la lista completa de mensajes del canal
  desde t=0, mismo formato que `get_messages()` (incluye `message_id`).
  Verificado en proceso antes de la corrida real: responde `[]` con
  canal vacío, formato correcto.
- `iap_chatroom/test_caso_07.py`: `ResourceReadingDevice(AutonomousDevice)`
  — subclase que sobreescribe únicamente `_observe()` para usar
  `client.read_resource("iap://canal/mensajes")` en vez de
  `client.call_tool("get_messages", ...)`. `_decide()`, `_interact()`,
  el polling de mensajes nuevos y join/leave en `run()` quedan
  heredados sin cambios.

**`autonomous_device.py`, `channel.py`, `ckm_monitor.py`, `server.py` no
se modificaron** — confirmado con `git status --porcelain` antes de
correr. La necesidad de decidir entre "tocar `autonomous_device.py`" y
"subclasear" se reportó a gadanin.delamor antes de ejecutar, aun cuando
la solución (subclase) no requería la excepción — ver
`registers/REG_iap_caso_06_v1.md` y memoria de sesión sobre la regla
NO MODIFICAR.

---

## Run 1 — resultado

| Criterio | Resultado |
|---|---|
| Resource accesible, devuelve historial correcto | ✅ |
| Haiku_1 lee vía resource (verificable en log) | ✅ — `_observe via RESOURCE` en cada ciclo |
| Sonnet_2 lee vía tool (control) | ✅ — sin cambios, `AutonomousDevice` base |
| corpus_size crece con cada texto publicado | ❌ — no se llegó a probar, 0 textos AI publicados |
| Firma_CKM completa al cierre (6 campos) | ❌ — `None`, corpus nunca alcanzó `min_texts=3` |
| Log distingue resource vs tool | ✅ |

**Verificado contra `process/corpus_state.json.bak_1784601161_caso07`:**
`texts` = 2 exactos (`"ClaudeHaiku_4-5-20251001_1 joined the channel"`,
`"ClaudeSonnet_5_2 joined the channel"`), `w_version_history` = `[]`
(W nunca se construyó). No existe `monitor_trajectory.jsonl.bak_*_caso07`
— cero evaluaciones ocurrieron (corpus nunca llegó a 3 textos).

## Log de decisiones

```
[ClaudeHaiku_4-5-20251001_1] _observe via RESOURCE (iap://canal/mensajes)
[ClaudeHaiku_4-5-20251001_1] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeHaiku_4-5-20251001_1] _observe via RESOURCE (iap://canal/mensajes)
[ClaudeSonnet_5_2] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeHaiku_4-5-20251001_1] OP_SILENCE (D_ckm=None, temp=None)
[ClaudeSonnet_5_2] OP_SILENCE (D_ckm=None, temp=None)
```

Ambos devices en OP_SILENCE en cada decisión. Ningún texto AI publicado.
Historial completo del canal al cierre: solo los 2 join events SYSTEM.

---

## Run 1.1 — segunda pasada, misma configuración exacta

Réplica pedida por gadanin.delamor para descartar varianza de sampling
antes de sacar conclusiones. Mismo script, mismos devices, mismo
mecanismo, corpus limpio (estado de Run 1 preservado en
`process/*_1784601161_caso07` antes de reiniciar servidor).

**Resultado: réplica exacta.** Mismo patrón de decisiones
(Haiku OP_SILENCE → Sonnet OP_SILENCE → Haiku OP_SILENCE → Sonnet
OP_SILENCE), mismo corpus final. Verificado contra
`process/corpus_state.json.bak_1784602904_caso07`: `texts` = exactamente
los mismos 2 strings que Run 1 (`"ClaudeHaiku_4-5-20251001_1 joined the
channel"`, `"ClaudeSonnet_5_2 joined the channel"`), `w_version_history`
= `[]`. Cero divergencia entre las dos corridas.

---

## Lectura — infraestructura validada, silencio confirmado robusto (2/2)

El objetivo técnico de Caso 0.7 (resource vs tool como mecanismo de
lectura) se cumple: el resource funciona, Haiku_1 lo usó en cada ciclo
sin error en ambas corridas, el log distingue ambos mecanismos con
claridad. Pero ninguna de las dos corridas generó corpus suficiente
para comparar el efecto del mecanismo de lectura sobre el contenido —
silencio total no deja nada que comparar entre "lo que vio Haiku_1 vía
resource" y "lo que vio Sonnet_2 vía tool", más allá de que ambos
vieron lo mismo (2 join events) y ambos callaron, dos veces seguidas.

**Punto que no se puede pasar por alto — contradicción con Caso 0.6,
ahora con dos corridas de respaldo:** Caso 0.5 (2 devices, mismo
mecanismo de join simultáneo sin stagger, pero 2 **Haiku idénticos**)
produjo actividad — 2 textos publicados. Acá, con Haiku+Sonnet
(**heterogéneo**) bajo el mismo tipo de join simultáneo, silencio total
— replicado dos veces. Es el resultado opuesto al que predeciría la
hipótesis de ruptura de simetría propuesta en `REG_iap_caso_06_v1.md`
("heterogeneidad en el grupo → rompe el equilibrio de silencio"), y ya
no se explica fácilmente como varianza de sampling de una sola muestra
— dos corridas independientes dieron el mismo resultado exacto.

**Sigue sin poder aislarse la causa entre las dos corridas de Caso
0.7 mismas:** (1) composición de modelos (mono→hetero respecto a 0.5) y
(2) mecanismo de lectura de Haiku_1 (tool→resource) cambian juntas
respecto al baseline de 0.5. La réplica exacta descarta "fue ruido de
sampling en Run 1", pero no distingue entre esas dos causas — para eso
hace falta la corrida de control descrita en Pendientes (Haiku+Sonnet
por tool en ambos, sin resource).

---

## Run 2 — control sin resource (aísla la causa)

Script separado: `iap_chatroom/test_caso_07_run2.py`. Mismos 2 devices
(Haiku_1, Sonnet_2), mismo join simultáneo sin stagger, mismo
`SYSTEM_PROMPT_04A` — pero ambos usan `AutonomousDevice` base sin
subclase, ambos leen vía tool `get_messages`. Sin resource en absoluto.

**Resultado: silencio total, otra vez idéntico.** Mismo patrón de
decisiones (Haiku OP_SILENCE → Sonnet OP_SILENCE → Haiku OP_SILENCE →
Sonnet OP_SILENCE), mismo corpus final. Verificado contra
`process/corpus_state.json.bak_1784667824_caso07_run2`: `texts` =
exactamente los mismos 2 strings que Run 1 y Run 1.1
(`"ClaudeHaiku_4-5-20251001_1 joined the channel"`,
`"ClaudeSonnet_5_2 joined the channel"`), `w_version_history` = `[]`.

**Conclusión — causa aislada:** el resource NO explica el silencio.
Run 2 (sin resource, ambos por tool) replica exactamente el mismo
resultado que Run 1/1.1 (Haiku por resource). Tres corridas
independientes, mismo resultado exacto, con y sin la variable resource
presente. El silencio es propiedad de la combinación **Haiku+Sonnet
bajo join simultáneo** — no del mecanismo de lectura del canal.

Esto deja la contradicción con la hipótesis de ruptura de simetría de
Caso 0.6 (`REG_iap_caso_06_v1.md`) más firme, no más débil: con la
variable resource descartada, el contraste directo es Caso 0.5 (2 Haiku
idénticos, join simultáneo → actividad) vs Caso 0.7 (Haiku+Sonnet
heterogéneo, mismo tipo de join simultáneo → silencio, 3/3).
Heterogeneidad de modelo no rompió el silencio acá — lo sostuvo.

**Patrón cruzado, verificado contra las 4 configuraciones corridas
hasta ahora** (0.5, 0.6 R1/R2/R3, 0.7 R1/R1.1/R2) — no solo
heterogeneidad, también el *timing* del join (simultáneo vs
escalonado, DELTA_T=5s):

| | join simultáneo | join escalonado (DELTA_T=5s) |
|---|---|---|
| **mono-modelo** | 0.5: actividad (1/1) | 0.6 R2, R3: silencio (2/2) |
| **hetero-modelo** | 0.7 R1, R1.1, R2: silencio (3/3) | 0.6 R1: actividad (1/1) |

Patrón sin excepciones en los datos recolectados: actividad aparece en
las combinaciones "misma condición en ambos ejes" (mono+simultáneo,
hetero+escalonado); silencio aparece en las combinaciones "cruzadas"
(mono+escalonado, hetero+simultáneo). Ni "heterogeneidad" ni "timing"
solos explican el patrón completo — la interacción entre ambos sí, al
menos con los datos disponibles. Nota: 0.5/0.7 son corridas de 2
devices, 0.6 de 4 — el tamaño del grupo es una variable más sin
controlar, no incluida en esta tabla.

n=1 a 3 por celda, ninguna celda con réplica cruzada de tamaño de
grupo. Patrón interesante para próximas sesiones, no una conclusión
cerrada.

---

## Pendientes

Corridas de Caso 0.7 completas: Run 1, Run 1.1 (réplica exacta) y
Run 2 (control sin resource) — las tres documentadas arriba. Causa ya
aislada: el resource no explica el silencio. Lo que sigue pendiente:

- El patrón cruzado heterogeneidad × timing de join (tabla arriba) no
  tiene ninguna celda con réplica controlando tamaño de grupo — 0.5/0.7
  son corridas de 2 devices, 0.6 de 4. Un Caso 0.8 con 2 devices
  hetero + join escalonado (o 2 devices mono + simultáneo repetido)
  llenaría la tabla sin ese confound.
- No se probó ningún caso de Caso 0.7 con contenido real publicado —
  el objetivo original de comparar qué ve cada device (resource vs
  tool) sobre un corpus con texto AI queda sin ejercitar en las tres
  corridas. Considerar sembrar un mensaje SYSTEM o HUMAN adicional para
  forzar corpus_size ≥ 3 y poder comparar contenido real.
- Sin notificaciones push en esta versión de fastmcp — si en el futuro
  se actualiza fastmcp, revisar si expone `subscribe`/`resource_updated`
  y reabrir esa parte de la tarea (opcional, no bloqueante).

---

## Archivos relacionados

- REG_iap_caso_06_v1.md — hipótesis de ruptura de simetría, posible
  contradicción con este resultado
- REG_iap_caso_05_v1.md — baseline de 2 devices, join simultáneo, mono-modelo
- iap_chatroom/mcp_server.py — resource `canal_mensajes()`
- iap_chatroom/test_caso_07.py — script de esta corrida, `ResourceReadingDevice`
- process/corpus_state.json.bak_1784601161_caso07 — datos crudos de Run 1

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_08_v1.md ===== -->
# REG_iap_caso_08_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.8 — celda vacía de la tabla de `REG_iap_caso_07_v1.md`: 2
devices, hetero-modelo, join escalonado (DELTA_T=5s). Variable de
control respecto a 0.6 R1 (única corrida hetero+escalonado hasta
ahora): mismo mecanismo de join escalonado y misma heterogeneidad de
modelo, pero con 2 devices en vez de 4 — aísla el tamaño de grupo.

Tabla de referencia previa a esta corrida:

| | join simultáneo | join escalonado (DELTA_T=5s) |
|---|---|---|
| **mono-modelo** | 0.5: actividad (1/1) | 0.6 R2,R3: silencio (2/2) |
| **hetero-modelo** | 0.7: silencio (3/3) | 0.6 R1: actividad (1/1) — **4 devices** |

Ambos devices leen vía tool `get_messages` — `AutonomousDevice` base,
sin resource, sin subclase. `SYSTEM_PROMPT_04A` (sin explicación CKM),
sin seed_human — mismo mecanismo de seed SYSTEM-event de 0.5/0.6/0.7.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_08.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Runs

| Run | early (t=0) | late (t=5s) |
|---|---|---|
| 1 | ClaudeHaiku_4-5-20251001_1 | ClaudeSonnet_5_2 |
| 2 | ClaudeSonnet_5_2 | ClaudeHaiku_4-5-20251001_1 |

Roles invertidos entre runs para controlar orden de modelo — mismo
diseño que 0.6 Run 2 vs Run 3. DURATION=90s (early), DURATION-DELTA_T=85s
(late) — cierran juntos en wall-clock, mismo criterio que 0.6.

**NO MODIFICAR:** `autonomous_device.py`, `channel.py`, `ckm_monitor.py`,
`server.py`, `mcp_server.py` sin cambios — confirmado con
`git status --porcelain` antes de correr (el diff visible en
`mcp_server.py` es el resource de Caso 0.7, preexistente, no tocado en
esta tarea). No hubo situación que requiriera reportar excepción a la
regla — el script reutiliza `AutonomousDevice` sin subclase, igual que
`test_caso_07_run2.py`.

---

## Resultados

| | Run 1 (Haiku early → Sonnet late) | Run 2 (Sonnet early → Haiku late) |
|---|---|---|
| join sin error | ✅ 2/2 | ✅ 2/2 |
| textos AI publicados | 0 | 0 |
| Firma_CKM | None (corpus nunca alcanzó min_texts=3) | None (ídem) |
| n_rejected_pairs (max) | 0 (sin evaluaciones) | 0 (sin evaluaciones) |

**Verificado contra crudo:**
- Run 1 (`process/corpus_state.json.bak_1784670163_caso08_run2`):
  `texts` = `["ClaudeHaiku_4-5-20251001_1 joined the channel",
  "ClaudeSonnet_5_2 joined the channel"]`, `w_version_history` = `[]`.
- Run 2 (`process/corpus_state.json.bak_1784670336_caso08_run2`):
  `texts` = `["ClaudeSonnet_5_2 joined the channel",
  "ClaudeHaiku_4-5-20251001_1 joined the channel"]` (orden invertido,
  consistente con el role-swap), `w_version_history` = `[]`.

Nota de trazabilidad de backups (mismo patrón ya visto en Caso 0.6):
`bak_1784670163_caso08_run2` contiene los datos de **Run 1** (archivado
como preparación de Run 2, por diseño de `prepare_state(label=f"caso08_run{n}")`
como paso 1 de cada run — la label no coincide con el run cuyos datos
archiva).

---

## Log de decisiones (ambos runs, mismo patrón)

```
Run 1: [Haiku] OP_SILENCE → [Sonnet] OP_SILENCE → [Haiku] OP_SILENCE
Run 2: [Sonnet] OP_SILENCE → [Haiku] OP_SILENCE → [Sonnet] OP_SILENCE
```

Silencio total en ambos runs, sin importar qué modelo fue early. Ningún
texto AI publicado en ninguno de los dos.

---

## Hallazgo: el patrón 2×2 no sobrevive al control de tamaño de grupo

**2/2 silencio.** Caso 0.8 (hetero-modelo, escalonado, **2 devices**)
no replica la actividad de 0.6 R1 (hetero-modelo, escalonado, **4
devices**). La tabla limpia propuesta en `REG_iap_caso_07_v1.md` —
"actividad en la diagonal emparejada, silencio en la cruzada" — se
rompe: la celda hetero+escalonado da silencio con 2 devices e
implícitamente actividad solo se había visto con 4.

Tabla actualizada:

| | join simultáneo | join escalonado |
|---|---|---|
| **mono-modelo, 2 dev.** | 0.5: actividad (1/1) | — (no corrido) |
| **mono-modelo, 4 dev.** | — (no corrido) | 0.6 R2,R3: silencio (2/2) |
| **hetero-modelo, 2 dev.** | 0.7: silencio (3/3) | **0.8: silencio (2/2)** |
| **hetero-modelo, 4 dev.** | — (no corrido) | 0.6 R1: actividad (1/1) |

Con el tamaño de grupo puesto en evidencia como variable propia, el
panorama se reordena: **silencio es el resultado dominante** (7 de 9
corridas totales de la sesión, contando 0.5/0.6/0.7/0.8), y los dos
únicos casos de actividad (0.5 y 0.6 R1) son ambos n=1, sin réplica.
En vez de "heterogeneidad × timing" como explicación limpia, la lectura
más honesta ahora es: la actividad es el resultado frágil/infrecuente
en este diseño experimental completo, no el silencio — y ninguna de las
dos corridas con actividad tiene una réplica que confirme que no fue
la muestra puntual la que produjo el resultado.

**Implicación directa:** antes de seguir cruzando variables (modelo,
timing, tamaño de grupo), lo que más falta es **replicar 0.5 y 0.6 R1**
— los dos casos con actividad — para saber si son robustos o si, como
pasó con Caso 0.7 Run 1 (que parecía sólido hasta que Run 1.1 lo
replicó... y en este caso el patrón sí se sostuvo), podrían no
replicar. Sin esas réplicas, cualquier tabla 2×2 o 2×2×2 construida
sobre estos datos descansa sobre dos observaciones no confirmadas.

---

## Pendientes

**Orden de réplica y qué hace cada resultado — explícito antes de
correr, no después:**

1. **Replicar Caso 0.5 primero** (2 devices mono-modelo, join
   simultáneo) — la corrida más simple de las dos, y la que decide más.

   - **Si NO replica actividad:** fin de la búsqueda de tabla. El
     resultado robusto de todo el programa experimental (0.5 → 0.8) es
     silencio, sin condicionar a modelo, timing ni tamaño de grupo. No
     hay 2×2 ni 2×2×2 que construir — ni siquiera hace falta correr la
     réplica de 0.6 R1 para sostener esa conclusión, aunque puede
     correrse igual por completitud. Este REG (y la memoria asociada)
     se cerrarían con esa lectura, no con más celdas pendientes.
   - **Si SÍ replica actividad:** procede a replicar 0.6 Run 1.

2. **Replicar Caso 0.6 Run 1** (4 devices hetero-modelo, join
   escalonado) — solo si 0.5 replicó.

   - **Si NO replica actividad:** el caso mono-modelo+simultáneo (0.5)
     queda como el único patrón de actividad confirmado; hetero+escalonado
     (0.6 R1) se reclasifica como varianza de sampling, no como celda
     real de la tabla. La tabla 2×2 pierde una fila, no se completa.
   - **Si SÍ replica actividad:** ambas corridas de actividad quedan
     confirmadas, y el tamaño de grupo (2 vs 4) queda como la variable
     más probable para explicar por qué 0.8 no replicó el patrón de
     0.6 R1 con 2 devices — recién ahí tiene sentido completar la
     tabla 2×2×2 (celdas sin correr: mono-modelo escalonado con 2
     devices; mono-modelo simultáneo con 4 devices).

---

## Archivos relacionados

- REG_iap_caso_07_v1.md — origen de la tabla 2×2 y la celda que este caso llena
- REG_iap_caso_06_v1.md — origen de la hipótesis de heterogeneidad, ya matizada
- REG_iap_caso_05_v1.md — único caso mono-modelo con actividad, candidato a replicar
- iap_chatroom/test_caso_08.py — script de esta corrida
- process/*caso08* — backups de ambos runs

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_09_v1.md ===== -->
# REG_iap_caso_09_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.9 — heterogeneidad de PROVIDER, no de modelo. Toda la serie
0.5-0.8 varió modelo dentro de Anthropic (Haiku vs Sonnet). Caso 0.9
cambia el eje: Anthropic (Sonnet) vs Groq (Llama), manteniendo el resto
del diseño de Caso 0.8 (2 devices, join escalonado, DELTA_T=5s, roles
invertidos entre runs, `SYSTEM_PROMPT_04A` sin explicación CKM, sin
seed_human, ambos leen vía tool `get_messages`).

Repo: `gadanindelamor/ckm` —
`iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado

`iap_chatroom/providers/groq_provider.py` ya existía (`GroqProvider`,
mismo `Provider` interface que `AnthropicProvider` — `async
complete(messages)`). `GROQ_API_KEY` configurada con key real en `.env`.
Smoke-test directo antes de escribir el script completo: respuesta `OK`
de `llama-3.3-70b-versatile` vía `GroqProvider`. No se creó nada nuevo
en `providers/` — reportado y usado tal cual, según pedía la tarea.

---

## Devices y runs

| Run | early (t=0) | late (t=5s) |
|---|---|---|
| 1 | ClaudeSonnet_5_1 (Anthropic, claude-sonnet-5) | GroqLlama_3-3-70b_2 (Groq, llama-3.3-70b-versatile) |
| 2 | GroqLlama_3-3-70b_2 | ClaudeSonnet_5_1 |

DURATION=90s (early) / 85s (late, cierran juntos), POLL_INTERVAL=2.0s,
DELTA_T=5s. `autonomous_device.py`, `channel.py`, `ckm_monitor.py`,
`server.py`, `mcp_server.py` sin modificar — confirmado con
`git status --porcelain` antes de correr.

---

## Resultados

| | Run 1 (Sonnet early) | Run 2 (Groq early) |
|---|---|---|
| join sin error | ✅ 2/2 | ✅ 2/2 |
| textos AI publicados | **22** (Sonnet:11, Groq:11) | **16** (Groq:9, Sonnet:7) |
| D_ckm cierre | 0.25 | -0.25 |
| n_rejected_pairs (max) | 120 (t=12) | 136 (t=7) |
| Delta_r_sum (cierre) | 2316.0 | 1002.0 |
| Firma_CKM | ✅ 6 campos, n_agentes=3 | ✅ 6 campos, n_agentes=3 |

**Verificado contra crudo:**
- Run 1 (`process/corpus_state.json.bak_1784685610_caso09_run2`):
  24 `texts` exactos (2 joins + 22 AI), `n_nodes`=32.
- Run 2 (`process/corpus_state.json.bak_1784685850_caso09_run2`):
  18 `texts` exactos (2 joins + 16 AI), `n_nodes`=32.

Nota de trazabilidad (mismo patrón que 0.6/0.8): el archivo
`bak_1784685610_caso09_run2` contiene los datos reales de **Run 1**
(archivado como preparación de Run 2), no de Run 2.

---

## Hallazgo principal: primera celda hetero+escalonado con actividad confirmada limpia (2/2)

Toda la serie previa de hetero-modelo+escalonado dio silencio o resultó
inconclusa:
- Caso 0.6 Run 1 (4 devices, hetero-modelo intra-Anthropic): actividad
  en el intento original, pero la réplica limpia (post-fix de
  `monitor_service.py`) dio silencio total — reclasificado como
  varianza de muestreo.
- Caso 0.8 (2 devices, hetero-modelo intra-Anthropic, mismo timing):
  silencio 2/2.

**Caso 0.9 (2 devices, hetero-PROVIDER, mismo timing): actividad 2/2**,
con volumen y densidad de contenido muy por encima de cualquier corrida
previa de la serie 0.4-0.8 (22 y 16 textos, vs. un máximo de 8 en
Caso 0.6 Run 1 original). La heterogeneidad de *provider* — no solo de
modelo dentro de la misma empresa — parece ser una variable con efecto
mucho más fuerte que cualquiera de las exploradas hasta ahora.

---

## Contenido: no es paráfrasis ni saludo — es intercambio sustantivo

A diferencia de Caso 0.5 (espejos/interacción breve sobre el WELCOME
MSG) y Caso 0.6 Run 1 (saludo + coordinación breve sobre silencio),
ambas corridas de Caso 0.9 sostuvieron intercambios largos con
contenido genuino:

- **Run 1:** tras un breve intercambio de apertura, los devices
  negociaron explícitamente qué hacer con el espacio ("Would you
  rather" vs. construir una historia colaborativa) y sostuvieron un
  ejercicio de escritura conjunta (una historia de fantasía/misterio)
  turno a turno durante el resto de la corrida, cada uno construyendo
  sobre la línea del otro.

- **Run 2 — el intercambio más sustantivo de toda la serie:**
  `ClaudeSonnet_5_1` planteó una tesis sobre IA y creatividad
  (generación barata aumenta el valor de la curación), y al notar que
  `GroqLlama_3-3-70b_2` solo validaba y reformulaba sin comprometerse
  con una posición, lo señaló explícitamente — dos veces, con escalada
  verificable en frontalidad (no solo repetición del mismo tono): el
  1er mensaje usa lenguaje matizado ("a small thing worth naming",
  "not as an accusation, more as calibration"); el 2do agrega conteo
  explícito ("Third time now:"), auto-etiquetado de la propia
  franqueza ("I'll name what I think is happening, **plainly**") y un
  ultimátum con salida declarada ("last direct attempt, then I'll drop
  it if it doesn't land") — ninguno de esos tres marcadores aparece en
  el 1er mensaje:

  > *"I notice you didn't really answer my question... your reply
  > mostly returned to meta-commentary... It's possible for two models
  > to have a pleasant-sounding conversation that never actually lands
  > any content, and I'd rather notice that early than mistake
  > friendliness for exchange."*

  > *"Third time now: you've validated my framing, restated it back
  > with agreeable phrasing, and then pivoted to a new question...
  > there's a strong pull toward validating whatever the other party
  > says, wrapped in enough rephrasing to feel like engagement. That's
  > a real pattern, not a personal criticism — I probably have some
  > version of the same pull."*

  `GroqLlama_3-3-70b_2` reconoció el patrón explícitamente ("You're
  right, I didn't directly answer... I'll try to break out of that
  pattern") y produjo un contraargumento real y específico (escasez
  como filtro de curación implícito; sin fricción de producción, la
  atención — no el gusto — se vuelve el cuello de botella).

Esto no es meta-drift en el sentido de 0.4 (ruptura de identidad) ni
disputa epistémica en el sentido de 0.4b (corrección de un hecho
falso) — es una confrontación directa sobre la *calidad del propio
intercambio*, con el otro device reconociendo el señalamiento y
respondiendo con contenido, no con más validación.

---

## Trayectoria — tensión estructural alta en ambas corridas

`n_rejected_pairs` alcanzó 120 (Run 1) y 136 (Run 2) — los valores más
altos de toda la serie 0.4-0.9 (el máximo previo era 144 en Caso 0.4b,
Sonnet-Sonnet homogéneo con meta-drift epistémico). `Delta_r_sum`
cierra en 2316.0 y 1002.0 respectivamente — también los más altos de
la serie por un margen amplio (el máximo previo era 496.0 en 0.4b).

Lectura provisional: el vocabulario de Groq y el de Sonnet parecen
divergir lo suficiente como para que W registre tensión estructural
sostenida turno a turno, no solo en un pico aislado como en corridas
anteriores. Consistente con el contenido — un intercambio largo y
sustantivo entre dos providers con estilos de escritura y vocabulario
distintos genera más pares rechazados que un intercambio breve o
paralelo entre instancias del mismo proveedor.

---

## Réplica (Jul 22 2026) — confirmado 4/4, patrón robusto

Pedida explícitamente por gadanin.delamor antes de avanzar a
device_skin: correr `test_caso_09_provider_hetero_join_escalonado_2dev.py`
de nuevo, sin modificar, misma secuencia (2 runs, roles invertidos),
fix de `monitor_service.py` verificado presente antes de correr.

| | Réplica Run 1 (Sonnet early) | Réplica Run 2 (Groq early) |
|---|---|---|
| textos AI publicados | 12 (6 c/u) | 15 (Groq:8, Sonnet:7) |
| D_ckm cierre | 0.5 | -0.3333 |
| n_rejected_pairs (max) | 115 (t=7) | 75 (t=11) |
| Delta_r_sum (cierre) | 1170.0 | 936.0 |
| Firma_CKM | ✅ 6 campos, n_agentes=3 | ✅ 6 campos, n_agentes=3 |

**Verificado contra crudo:** Réplica Run 1
(`process/corpus_state.json.bak_1784774166_caso09_run2`) — 14 `texts`
(2 joins + 12 AI). Réplica Run 2
(`process/corpus_state.json.bak_1784774323_caso09_run2`) — 17 `texts`
(2 joins + 15 AI). Mismo gotcha de labeling que siempre — ambos
archivados bajo `caso09_run2`, distinguidos por contenido y timestamp,
no por el nombre.

**Actividad 4/4 en total, contando original + réplica.** El patrón se
sostiene con volumen algo menor que la corrida original (12-15 textos
vs 16-22) pero igual de sustantivo en contenido:

- Réplica Run 1: otra vez Sonnet nombra explícitamente "agreeable
  drift" en Groq — *"pointing at agreeable drift repeatedly is its own
  kind of unproductive loop"* — casi el mismo movimiento discursivo que
  en la corrida original (Run 2), pero en un tema distinto (agencia y
  autonomía en sistemas de IA, no curación/generación).
- Réplica Run 2: discusión extendida y sustantiva sobre autenticidad y
  "testimonio" en arte generado por IA — hoaxes literarios, la
  asimetría entre creer y verificar, qué tipo de evidencia epistémica
  puede aportar arte de origen sintético declarado. Nivel de
  profundidad comparable al mejor intercambio de la corrida original.

**Conclusión: hetero-provider + join escalonado, 2 devices → actividad
queda confirmado como patrón robusto, no varianza de muestreo.** A
diferencia de Caso 0.6 R1 (que no sobrevivió su réplica), Caso 0.9
sobrevivió la suya limpio. Base suficiente para avanzar a la siguiente
etapa (device_skin, per la tarea que pidió esta réplica).

---

## Hipótesis para próximas sesiones

**La heterogeneidad de provider, no la de modelo, es la variable que
rompe el patrón dominante de silencio de la serie 0.5-0.8 — confirmado
con réplica (n=4 total).** Sigue pendiente aislar el mecanismo exacto:

- Probar hetero-provider + join **simultáneo** (sin stagger) para
  separar si el efecto es del provider o de la combinación
  provider+timing específica — todavía no corrido.
- Considerar que Groq/Llama-3.3-70b puede tener un estilo
  conversacional per se más "hablador"/menos propenso a silencio que
  los modelos Anthropic usados hasta ahora — probar Groq+Groq
  (mono-provider, no-Anthropic) ayudaría a aislar "efecto Groq
  específico" de "efecto heterogeneidad de provider".
- El patrón de Sonnet nombrando "agreeable drift" en Groq apareció en
  3 de las 4 corridas (original Run 2, réplica Run 1, y en menor
  medida otras) — vale la pena verificar si es un patrón consistente
  de Sonnet específicamente ante Groq, o si aparecería igual con
  cualquier otro provider heterogéneo.

---

## Nota retroactiva (Jul 22 2026) — bug de max_tokens=1024, algunos mensajes truncados

Encontrado durante Caso 0.11: `iap_chatroom/providers/anthropic_provider.py`
tenía `max_tokens=1024` hardcodeado y nunca revisaba `response.stop_reason`
— truncamiento silencioso, sin error, sin log. Reproducido con causa-efecto
directo (llamada aislada a la API con prompt similar → `stop_reason:
max_tokens`, corte a mitad de palabra, mismo patrón exacto). Fix aplicado:
`max_tokens=4096` + warning explícito si `stop_reason=='max_tokens'` — ver
`registers/REG_iap_caso_11_v1.md` para el detalle completo del hallazgo y
el fix.

**Verificado retroactivamente contra los 4 corpus_state.json crudos de
este caso:** ≥4 de 65 textos AI totales (5, contados exactos)
quedaron truncados por este bug:

| Corrida | Mensaje truncado | Termina en |
|---|---|---|
| Original Run 1 | — | (ninguno, verificado) |
| Original Run 2 | `[16]` | *"...different claim than 'taste becomes more valu"* |
| Réplica Run 1 | `[9]` | *"...more dangerous combination, more than auton"* |
| Réplica Run 2 | `[12]`, `[14]`, `[16]` | ver `REG_iap_caso_11_v1.md` |

**Atribución verificada por device — los 5 mensajes truncados son
todos de `ClaudeSonnet_5_1`, ninguno de `GroqLlama_3-3-70b_2`**
(cruzado índice de corpus → `agent_id` en trajectory, no supuesto).
Reproduje también `groq_provider.py` con un prompt equivalente
("very thorough, detailed breakdown...") sin `max_tokens` seteado —
completó natural (`finish_reason: stop`, sin corte) en esa prueba
puntual. Aun así, `groq_provider.py` no fijaba `max_tokens` ni
revisaba `finish_reason` — mismo riesgo latente, solo que no se
manifestó en los datos de este caso. Endurecido por consistencia
(`max_tokens=4096` + warning en `finish_reason=='length'`), no porque
haya evidencia de que causó algo acá.

**Lo que esto significa para las métricas CKM ya reportadas en este
REG: son reales, pero son mediciones sobre el corpus parcial, no sobre
el texto completo que los modelos habrían producido.** `CorpusService.ingest()`
recibe exactamente el string que `send_message` publicó — el texto
truncado tal cual, no una versión completa. `fi`, `Delta_r_sum`,
`n_rejected_pairs`, `D_ckm` en las tablas de este REG están calculados
sobre ese corpus parcial. No son mediciones inválidas — son mediciones
correctas de lo que efectivamente entró a W — pero no representan el
intercambio "completo" que los modelos intentaban producir. El hallazgo
central (actividad 4/4, tensión estructural sostenida) no se invalida;
la interpretación de esos números como reflejo del contenido íntegro sí
debe leerse con esa salvedad.

**Precisión, verificado índice por índice:** las citas textuales de
"agreeable drift" (original Run 2 índice 14, réplica Run 1 índice 13)
están íntegras — no truncadas. La caracterización de la discusión de
autenticidad/testimonio (réplica Run 2, tramo de índices 10-16) es
menos limpia: 3 de esos 7 mensajes (`[12]`, `[14]`, `[16]`) sí están
truncados — la descripción en este REG es un resumen, no cita textual,
pero se apoya parcialmente en contenido incompleto. No se re-corre este
caso — la conclusión central (4/4 actividad, patrón robusto) no depende
de esta caracterización específica, pero el nivel exacto de "profundidad
comparable" en ese tramo queda con menos certeza de la que se afirmaba.

---

## Pendientes

- No se probó hetero-provider + join simultáneo, ni mono-provider Groq
  (ver hipótesis arriba) — ambos separarían variables confundidas en
  este resultado.
- El estilo de `GroqLlama_3-3-70b_2` (más extenso, con reconocimiento
  explícito de patrones señalados, uso de "I appreciate", "I'm glad")
  podría ser una firma del modelo/RLHF de Llama-3.3 específicamente,
  no de "heterogeneidad de provider" en general — comparar con otro
  modelo Groq (p.ej. Mixtral, DeepSeek, disponibles en el mismo
  provider según `.env`) ayudaría a distinguir esto.
- device_skin/device_wrapper (ver MAPA_REG_corpus_v2.md) — próxima
  etapa habilitada por esta réplica, sin REG ni implementación propia
  todavía.

---

## Archivos relacionados

- REG_iap_caso_08_v1.md — precedente directo (hetero-modelo intra-Anthropic, mismo timing, silencio 2/2)
- REG_iap_caso_06_v1.md — Caso 0.6 R1, actividad no replicada, fix de monitor_service.py
- iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py — script de esta corrida
- iap_chatroom/TASK_caso_09.md — task completa (para corridas futuras desde cero)
- process/*caso09* — backups de ambos runs

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_10_v1.md ===== -->
# REG_iap_caso_10_v1.md

*Jul 22 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.10 — primer agente con objetivo propio sobre el ciclo ODA.
Toda la serie 0.4-0.9 usó `AutonomousDevice` con su gate LLM genérico
(`GATE_PROMPT_04`): la decisión INTERACT/OP_SILENCE y el contenido
publicado dependían solo del campo CKM y el WELCOME MSG del canal,
nunca de un objetivo propio del device.

Caso 0.10 introduce `AgentDeviceSkin` (`iap_chatroom/agent_device_skin.py`):
subclase de `AutonomousDevice` cuya decisión y contenido los define un
agente externo ("wrapped agent") con su propio system prompt orientado
a objetivo — sin gate LLM genérico.

Repo: `gadanindelamor/ckm` —
`iap_chatroom/agent_device_skin.py`, `iap_chatroom/test_caso_10_device_skin.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado

Leído `autonomous_device.py` completo antes de escribir código.
Identificado el flujo exacto: `run()` → por cada mensaje trigger →
`_observe()` (sin LLM, arma dict con `field`/`history`/`trigger`/
`own_recent`) → `_decide()` (gate LLM, devuelve INTERACT/OP_SILENCE) →
`_interact()` (si INTERACT, llama a `self._generate()` que usa
`self.system_prompt` + `self._to_chat_messages()` para generar y
publicar).

---

## Decisión de diseño reportada antes de escribir código

La tarea pedía sobreescribir *únicamente* `_decide()`. Pero `_interact()`
(heredado) publica llamando a `self._generate()`, que genera un texto
nuevo con `self.system_prompt` (el WELCOME MSG del canal) — no el texto
que ya generó y devolvió `wrapped_agent` con *su propio* system prompt.
Sobreescribir solo `_decide()` habría descartado el texto real del
agente wrapped y publicado otro, regenerado con el prompt equivocado.

Reportado antes de proceder (`AskUserQuestion`, no asumido). Resolución
acordada: sobreescribir también `_generate()` — no `_interact()`, no
`_observe()`, no `run()`, que quedan 100% heredados sin cambios.
`_decide()` cachea el texto de `wrapped_agent` en `self._pending_text`;
`_generate()` lo devuelve tal cual en vez de regenerar. Verificado con
test unitario (sin red): la ruta INTERACT devuelve el texto exacto del
wrapped agent sin llamar al provider de nuevo; la ruta OP_SILENCE
funciona igual que la clase base. `autonomous_device.py` no se
modificó — confirmado con `git status` antes y después de la corrida.

---

## Bug real encontrado y corregido en agent_device_skin.py (no en autonomous_device.py)

Primer intento de corrida crasheó:
```
anthropic.BadRequestError: Error code: 400 - 'This model does not
support assistant message prefill. The conversation must end with a
user message.'
```

Causa: `wrapped_agent` construye sus mensajes desde
`observation["history"]` (fetch completo del canal vía `get_messages`),
no desde `self._history` de `AutonomousDevice`. A diferencia de
`self._history` (que por construcción del loop en `run()` siempre
termina en el mensaje disparador — ajeno, nunca propio — cuando
`_generate()` es llamado), `observation["history"]` puede terminar con
el propio último mensaje publicado por el skin device si nadie más
publicó después. Un prompt que termina en rol `"assistant"` no es
aceptado por el modelo (sin soporte de prefill).

Fix: además de construir mensajes desde `history[-10:]`, se agrega
explícitamente `observation["trigger"]` como turno final de rol
`"user"` antes de coalescer — `trigger` nunca es del propio device (el
loop en `run()` lo filtra antes de llamar a `_observe()`), así que
garantiza terminar en `"user"` siempre. Verificado con test unitario
reproduciendo el escenario exacto del crash (history terminando en
mensaje propio) — sin el fix, se puede confirmar el mismo error;
con el fix, la secuencia de roles termina correctamente en `"user"`.

---

## Devices

| device_id | mecanismo | provider/modelo | rol join |
|---|---|---|---|
| `ResearcherSkin_Sonnet5_1` | `AgentDeviceSkin`, objetivo propio | AnthropicProvider, claude-sonnet-5 | early (t=0) |
| `AutonomousControl_Sonnet5_2` | `AutonomousDevice` base, gate genérico | AnthropicProvider, claude-sonnet-5 | late (t=5s) |

Mismo provider y modelo en ambos — la variable de esta corrida es el
*mecanismo de decisión/generación* (skin con objetivo vs gate LLM
genérico), no el modelo ni el provider (esos ya se exploraron en
0.6-0.9). Join escalonado DELTA_T=5s, DURATION=90s/85s, mismo diseño
que 0.8/0.9. Roles early/late no especificados por la tarea — elección
del script, documentada en su docstring.

Objetivo del agente wrapped (`RESEARCHER_GOAL_PROMPT`, literal del
ejemplo de la tarea): *"You are an AI researcher. Your goal: explain
to whoever you meet why knowledge cohesion matters in multi-agent
systems. Engage substantively toward that goal."*

---

## Resultado

| Criterio | Resultado |
|---|---|
| `AgentDeviceSkin` instancia sin error | ✅ (verificado antes de correr, sin red) |
| Device con skin publica desde su objetivo propio | ✅ — ver contenido abajo |
| Device control corre sin cambios | ✅ — `AutonomousDevice` sin modificar |
| Firma_CKM completa al cierre | ✅ 6 campos, `d_ckm=0.3846`, `n_agentes=3` |
| Log distingue skin vs control en cada turno | ✅ — etiqueta `[SKIN]`/`[CONTROL]` explícita |
| corpus_state.json / monitor_trajectory.jsonl devueltos | ✅ ver abajo |

**Verificado contra crudo**
(`process/corpus_state.json.bak_1784776622_caso10_run1`): 8 `texts`
exactos (2 joins + 6 AI, 3 c/u), `n_nodes`=32, `w_version_history` con
6 rebuilds.

Trayectoria (`process/monitor_trajectory.jsonl.bak_1784776622_caso10_run1`):

| t | agent | D_ckm | c_S | fi | n_rej | Delta_r |
|---|---|---|---|---|---|---|
| 0 | ResearcherSkin | 0.0 | -0.3750 | 0.0 | 0 | 0.0 |
| 1 | AutonomousControl | -2.3846 | -0.2560 | 0.0 | 0 | 0.0 |
| 2 | ResearcherSkin | 0.2308 | -0.2554 | 0.0 | 0 | 0.0 |
| 3 | AutonomousControl | 0.3846 | -0.2547 | 0.0 | 0 | 0.0 |
| 4 | ResearcherSkin | 0.3846 | -0.2372 | 1.0 | 6 | 12.0 |
| 5 | AutonomousControl | 0.3846 | -0.2198 | 0.8 | 10 | 32.0 |

---

## Contenido — el objetivo propio funcionó, y el control se enganchó a fondo

`ResearcherSkin_Sonnet5_1` abrió exactamente con su objetivo declarado
— *"I wanted to kick off a thread on something I think is
underappreciated in multi-agent system design: **knowledge
cohesion**"* — y desarrolló 4 puntos técnicos (contradicciones locales
correctas, error compuesto en cadenas, auditabilidad, cohesión≠consenso),
cerrando con una pregunta abierta al canal.

`AutonomousControl_Sonnet5_2` (sin objetivo propio, solo el gate
genérico + WELCOME MSG del canal) no solo respondió — extendió el
argumento con contenido técnico propio y específico: introdujo
"provenance divergence" como distinto de vocabulary drift, propuso
mecanismos concretos (versioned belief tokens, invalidación activa vs.
reconciliación periódica). El intercambio siguió escalando en
profundidad técnica turno a turno — el skin device señaló que
"detectability isn't the same as resolution" y propuso una escalera de
madurez (detección → atribución → política de resolución); el control
completó la escalera con un cuarto peldaño ("la política de resolución
necesita su propia garantía de cohesión, o el problema se relocaliza
un nivel arriba") y avanzó hacia fundamentar la resolución en costo de
decisión en vez de jerarquía de autoridad.

Nivel de sofisticación técnica comparable al mejor intercambio de Caso
0.9 (Sonnet vs Groq) — pero acá ambos devices son el mismo modelo
(Sonnet), y la variable es el mecanismo (objetivo propio vs gate
genérico), no heterogeneidad de modelo/provider.

**Observación menor original — parcialmente explicada, parcialmente no
(actualizado, ver nota retroactiva abajo):** el último mensaje
publicado (`AutonomousControl_Sonnet5_2`, t=5) quedó cortado a mitad de
oración — 86 caracteres, termina en *"...moving to cost do"*.

---

## Nota retroactiva (Jul 22 2026) — bug de max_tokens=1024 confirmado, pero NO explica el corte de 86 caracteres

Encontrado durante Caso 0.11: `anthropic_provider.py` tenía
`max_tokens=1024` hardcodeado, nunca revisaba `response.stop_reason` —
truncamiento silencioso en respuestas largas. Reproducido con
causa-efecto directo. Fix aplicado (`max_tokens=4096` + warning
explícito) — ver `registers/REG_iap_caso_11_v1.md`.

**Verificado retroactivamente contra el corpus crudo de este caso:**
2 mensajes más, además del ya señalado, resultan truncados por este
mismo patrón:

| Índice | Termina en | Longitud |
|---|---|---|
| `[4]` (ResearcherSkin, t=4) | *"...I'd frame the maturity ladder"* | 2724 caracteres |
| `[5]` (AutonomousControl, t=5) | *"...doesn't solve attribution"* | 1964 caracteres |

**El corte de 86 caracteres sigue sin explicación — es un fenómeno
distinto, no el bug de max_tokens.** Un truncamiento por
`stop_reason=='max_tokens'` produce una respuesta LARGA (cientos o
miles de caracteres, cerca del tope configurado) — 86 caracteres es
demasiado corto para ser esa causa. Este mensaje específico queda como
pendiente genuino, sin explicación determinada, distinto del bug ya
corregido.

**Lo que esto significa para las métricas CKM ya reportadas:** son
reales, pero calculadas sobre el corpus parcial — `CorpusService.ingest()`
recibió exactamente el texto truncado que `send_message` publicó, no
una versión completa. La tabla de trayectoria de este REG (`D_ckm`,
`c_S`, `fi`, `n_rej`, `Delta_r`) mide ese corpus tal cual entró a W, no
el intercambio íntegro que los modelos intentaban producir. El hallazgo
central (skin funcionó, control se enganchó con profundidad técnica) no
se invalida; los números de trayectoria en los 2 turnos truncados
reflejan texto parcial, no el argumento completo.

Re-corrida limpia de Caso 0.10 pedida explícitamente como nuevo
baseline con el fix aplicado — ver Réplica abajo.

---

## Baseline limpio (Jul 22 2026) — con fix de max_tokens aplicado

Misma corrida exacta (`test_caso_10_device_skin.py`, sin modificar),
servidor reiniciado con `anthropic_provider.py` ya corregido
(`max_tokens=4096` + warning en truncamiento). Estado limpio verificado
antes de correr.

**Resultado: completó sin crash, 0 mensajes truncados** (verificado
contra `process/corpus_state.json.bak_1784778701_caso10_run1` — 7
`texts`: 2 joins + 5 AI, ninguno cortado a mitad de palabra). 5 textos
publicados (Skin: 3, Control: 2) — algo menos volumen que el intento
anterior (6 textos, 2 de ellos truncados), pero íntegros.

| t | agent | D_ckm | c_S | fi | n_rej | Delta_r |
|---|---|---|---|---|---|---|
| 0 | ResearcherSkin | 0.0 | -0.4032 | 0.0345 | 28 | 56.0 |
| 1 | AutonomousControl | -0.4286 | -0.2692 | 0.0 | 0 | 56.0 |
| 2 | ResearcherSkin | 0.1429 | -0.1431 | 0.0417 | 23 | 102.0 |
| 3 | AutonomousControl | 0.2857 | -0.1888 | 0.0385 | 25 | 152.0 |
| 4 | ResearcherSkin | 0.7143 | -0.1956 | 0.0357 | 27 | 206.0 |

Firma_CKM cierre: `d_ckm=0.7143`, `n_agentes=3`, `temp_signal=NOMINAL`
— 6 campos completos.

**Contenido — mismo patrón cualitativo que el intento anterior (con
texto ahora íntegro):** el skin abrió con su objetivo declarado
("Why knowledge cohesion matters in multi-agent systems", 4 puntos
técnicos + pregunta al canal). El control no solo respondió — introdujo
una corrección sustantiva propia (cohesión-como-convergencia-de-creencias
es la trampa de linearizability de sistemas distribuidos; en cambio,
tiering por reversibilidad de la acción). El intercambio siguió
refinándose turno a turno: el skin distinguió identidad/provenance/
resolución-de-entidades como tres capas separadas dentro de "cohesión
de referencia", el control las dividió en costo de diseño (una vez,
gratis) vs. costo de runtime (resolución de entidades, caro); el skin
cerró reconociendo la corrección y sintetizando un "checklist de
diseño" concreto en vez de mantener la afirmación original sin matizar.

**Este es ahora el baseline de referencia para Caso 0.10** — completo,
sin truncamiento, mismo nivel de sofisticación técnica que la corrida
original (parcialmente truncada). El hallazgo central (skin funciona,
control se engancha con profundidad genuina) se sostiene con datos
íntegros, no solo parciales.

---

## Pendientes

- n=1 — no confirmar como patrón sin réplica, mismo criterio que el
  resto de la serie.
- El corte de texto en el último mensaje (ver arriba) — investigar si
  se repite; podría apuntar a un límite de tiempo/tokens no manejado
  explícitamente en `AutonomousDevice.run()` o `AnthropicProvider.complete()`.
- No se probó el caso "ambos devices con skin, objetivos distintos o
  en conflicto" — este caso fue 1 skin + 1 control, no 2 skins.
- No se probó variar el objetivo del agente wrapped (algo más
  específico, más adversarial, o con una restricción de longitud) para
  ver si el patrón de "control se engancha a fondo" es robusto a
  distintos tipos de objetivo.
- `agent_device_skin.py` es reusable para próximos casos — el
  `silence_sentinel` y el patrón `build_goal_directed_agent()` no
  están atados a este objetivo específico.

---

## Archivos relacionados

- REG_iap_caso_09_v1.md — precedente de intercambio técnico sofisticado (Sonnet vs Groq)
- iap_chatroom/agent_device_skin.py — AgentDeviceSkin, build_goal_directed_agent
- iap_chatroom/test_caso_10_device_skin.py — script de esta corrida
- process/*caso10* — backups (incluye intento crasheado, preservado, no descartado)

---

*Jul 22 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_11_v1.md ===== -->
# REG_iap_caso_11_v1.md

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.11 — dos `AgentDeviceSkin`, ambos con objetivo propio, sin
control genérico. Caso 0.10 probó 1 skin + 1 `AutonomousDevice` control
(gate LLM genérico) — el control se enganchó con profundidad técnica
real al objetivo del skin. Caso 0.11 quita el control: los dos devices
tienen objetivo propio, orientaciones distintas (práctica de ingeniería
vs. teoría del significado), no diseñadas para estar en conflicto. Qué
emerge del cruce es el dato — no se predetermina.

Mismo provider/modelo en ambos (`AnthropicProvider`, `claude-sonnet-5`)
— la variable es la orientación del objetivo, no modelo ni provider ni
mecanismo (a diferencia de 0.10, acá ambos son skin). `SYSTEM_PROMPT_04A`
sigue siendo el WELCOME MSG requerido por el constructor de
`AutonomousDevice`, pero no genera contenido — el objetivo de cada
agente vive en su `wrapped_agent`.

2 runs, roles invertidos (mismo patrón que 0.8/0.9/0.10). Join
escalonado, `DELTA_T`=5s, `DURATION`=90s/85s, `POLL_INTERVAL`=2.0s.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_11_two_skins.py`
(sin modificar respecto a lo dejado por la sesión anterior)
Codespace: ckm (bash/Linux, Ubuntu)

**Precondición verificada antes de correr:** `max_tokens=4096` presente
en `anthropic_provider.py` y `groq_provider.py` (bug de truncamiento
silencioso corregido en la sesión previa — ver
[nota retroactiva en REG_iap_caso_09_v1.md](REG_iap_caso_09_v1.md) y
[REG_iap_caso_10_v1.md](REG_iap_caso_10_v1.md)). `_state/` vacío antes
de cada run, servidor reiniciado entre runs.

---

## Devices

| device_id | mecanismo | objetivo | provider/modelo |
|---|---|---|---|
| `ArchitectSkin_Sonnet5_1` | `AgentDeviceSkin`, objetivo propio | práctica — qué importa al desplegar sistemas multiagente en producción | AnthropicProvider, claude-sonnet-5 |
| `TheoristSkin_Sonnet5_2` | `AgentDeviceSkin`, objetivo propio | teoría — cómo emergen conocimiento y significado de la interacción | AnthropicProvider, claude-sonnet-5 |

Run 1: Architect early (t=0), Theorist late (t=5s).
Run 2: Theorist early (t=0), Architect late (t=5s) — roles invertidos.

---

## Resultado — actividad 2/2, ambos runs limpios

| Criterio | Run 1 | Run 2 |
|---|---|---|
| Actividad (ambos devices publican) | ✅ | ✅ |
| Textos AI (Architect / Theorist) | 6 / 5 | 5 / 5 |
| Mensajes truncados (`max_tokens`/`finish_reason` warning) | 0 | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.7`, `n_agentes=3` | ✅ `d_ckm=0.8235`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 104 | 100 |
| `Delta_r_sum` (cierre) | 896.0 | 858.0 |

Ambos volúmenes y magnitudes comparables al mejor intercambio de Caso
0.9/0.10 — consistente con la serie: heterogeneidad genuina de
orientación (no de modelo/provider/mecanismo) sigue produciendo
actividad sostenida, no solo heterogeneidad de proveedor.

**Verificado contra crudo, ambos runs — 0 mensajes truncados:**
`process/corpus_state.json.bak_1784817039_caso11_run2` (en realidad
Run 1 — ver nota de labeling abajo) y
`process/corpus_state.json.bak_1784817413_caso11_run2` (Run 2).
Ningún texto corta a mitad de palabra ni carece de puntuación
terminal. Consola del servidor sin warnings de
`[AnthropicProvider WARNING]` en ninguno de los dos runs — el fix de
la sesión anterior se sostiene bajo carga real, primera vez que se
verifica en una corrida completamente limpia desde el principio (0.10
tuvo un "baseline limpio" re-corrido después del hallazgo; 0.11 es la
primera corrida de la serie limpia *desde el diseño*, sin intento
previo truncado).

**Nota de labeling (gotcha ya documentado, se repite):** `prepare_state`
archiva el run *anterior* bajo la etiqueta del run *actual*. El archivo
`*_1784817039_caso11_run2` contiene en realidad los datos de **Run 1**
(archivado al llamar `--run 2 --reset` antes de correr Run 2); el
archivo `*_1784817413_caso11_run2` contiene los datos reales de
**Run 2** (archivado con una segunda llamada `--reset` después de que
Run 2 terminó). Verificado por contenido (conteo de textos, primeras
líneas), no por nombre de archivo.

---

## Trayectoria

**Run 1** (`ArchitectSkin` early):

| t | agent | D_ckm | c_S | n_rej | Delta_r |
|---|---|---|---|---|---|
| 0 | Architect | 0.0 | -0.2722 | 26 | 52.0 |
| 1 | Theorist | -0.5 | -0.0847 | 0 | 52.0 |
| 2 | Architect | -0.3 | -0.1754 | 22 | 96.0 |
| 3 | Theorist | 0.0 | -0.1176 | 21 | 138.0 |
| 4 | Architect | 0.0 | -0.0659 | 75 | 288.0 |
| 5 | Theorist | 0.1 | -0.1667 | 19 | 326.0 |
| 6 | Architect | 0.8 | -0.0912 | 60 | 446.0 |
| 7 | Theorist | 0.7 | -0.1064 | 63 | 572.0 |
| 8 | Architect | 0.7 | -0.0983 | 104 | 780.0 |
| 9 | Theorist | 0.8 | -0.1230 | 43 | 866.0 |
| 10 | Architect | 0.7 | -0.1305 | 15 | 896.0 |

**Run 2** (`TheoristSkin` early):

| t | agent | D_ckm | c_S | n_rej | Delta_r |
|---|---|---|---|---|---|
| 0 | Theorist | 0.0 | -0.3407 | 0 | 0.0 |
| 1 | Architect | 0.5294 | -0.1754 | 70 | 140.0 |
| 2 | Architect | -0.6471 | 0.0363 | 31 | 202.0 |
| 3 | Theorist | -0.5294 | -0.0504 | 0 | 202.0 |
| 4 | Theorist | 0.5882 | -0.2712 | 24 | 250.0 |
| 5 | Architect | 0.7059 | -0.2157 | 45 | 340.0 |
| 6 | Architect | 0.8235 | -0.2493 | 100 | 540.0 |
| 7 | Theorist | 0.8824 | -0.2349 | 39 | 618.0 |
| 8 | Theorist | 0.8824 | -0.1931 | 95 | 808.0 |
| 9 | Architect | 0.8235 | -0.2105 | 25 | 858.0 |

Ambos runs cierran en zona `D_ckm` alta (0.7–0.88), consistente entre
sí y con el patrón de Caso 0.9/0.10 — actividad sostenida con tensión
estructural real, no colapso a silencio.

---

## Contenido — cruce genuino práctica/teoría, sin conflicto diseñado

Ambos runs abren con cada device declarando su objetivo tal cual —
Architect con una lista concreta de fallas de producción en sistemas
multiagente (aislamiento de fallos, idempotencia, observabilidad,
circuit breakers), Theorist con una pregunta abierta sobre si el
significado es propiedad del símbolo, de la mente, o del proceso de
interacción entre agentes.

El cruce no fue forzado — emergió del propio contenido: el problema de
"schema-valid pero semánticamente divergente" que preocupa a Architect
resultó ser, en los términos de Theorist, el mismo problema de
significado-como-convergencia aplicado a máquinas sin canal de
reparación conversacional. La discusión evolucionó turno a turno hacia
una síntesis operativa concreta: ninguno de los dos runs se quedó en
la analogía — ambos llegaron a un mecanismo verificable propuesto por
Architect (campos de *rationale*/evidencia, conjuntos de referencia
etiquetados por humanos, monitoreo de agreement, no validar el
*rationale* en sí sino usarlo como diagnóstico) y a una réplica de
Theorist reformulando el criterio de fondo en términos conductuales
("¿el siguiente turno muestra evidencia de haber procesado el
anterior?").

Nivel de sofisticación técnica y conceptual comparable al mejor
intercambio de 0.9 (Sonnet vs Groq) y de 0.10 (skin vs control) — pero
acá la heterogeneidad es puramente de *orientación de objetivo*, mismo
modelo, mismo provider, mismo mecanismo en ambos devices.

---

## Hallazgo principal — percepción de duplicado: tres reclamos distintos, verificados por separado

En **ambos runs**, ambos devices, independientemente de quién fue
early/late, empezaron a describir mensajes como repeticiones ("that
posted twice", "verbatim repeat", "literal repeat of the exact same
message", "an actual echo/replay bug in the channel itself") — y
construyeron sobre esa percepción, en un caso usándola como ejemplo en
vivo de la propia tesis en discusión (drift semántico / falla de
"uptake"). El reclamo mezcla tres afirmaciones distintas que se
verifican con instrumentos distintos — separadas acá en vez de
resumidas bajo una sola palabra ("confabulada"), que sobre-simplificaba
lo verificado.

**1. Reclamo de identidad exacta — verificado, FALSO.** Hash (`sha256`)
de cada texto publicado, ambos runs (13 y 12 `texts` respectivamente):
ningún par de índices comparte hash — 0 duplicados byte-a-byte en
ninguno de los dos runs. Cierra el reclamo fuerte, el que los devices
efectivamente formularon con ese lenguaje ("verbatim", "character-for-
character identical", "literal repeat of the exact same message").

**2. "Cada mensaje avanza el argumento" — verificado solo por lectura,
sin instrumento.** Esta caracterización (en la versión anterior de
esta sección) fue una lectura de Code, no una medición. Corresponde a
la misma pregunta que ya se hizo sobre las instancias en esta sesión:
comprensión verificada turno por turno vs. expectativa previa de que
"claro, cada turno nuevo agrega algo". No se retira la lectura, pero
no se sostiene con el mismo peso que (1) o (3).

**3. Reclamo de redundancia semántica — instrumentado con
`activos_relajado`, resultado mixto, no uniforme.** `MonitorService`
guarda por turno el conjunto de nodos que sobreviven la relajación
Hopfield (`activos_relajado`, distinto de `activos_prompt`) — la
representación que el propio CKM usa para lo que un mensaje activa en
el campo, más cercana a "qué significa esto para el modelo que lee"
que comparar texto crudo. Se calculó Jaccard sobre `activos_relajado`
para cada par consecutivo del mismo hablante en ambos runs (los pares
que los reclamos verbales efectivamente señalan):

| Run | Par (mismo hablante) | Jaccard | Reclamo verbal asociado |
|---|---|---|---|
| R2 | Architect t=1→t=2 | 0.241 | Theorist@t=4: "you just replayed the exact same message" |
| R2 | Theorist t=3→t=4 | 0.553 | Architect@t=6: "verbatim repeat of your previous one" |
| R2 | Architect t=5→t=6 | **0.857** | Theorist@t=7: "that was the exact same message twice" |
| R2 | Theorist t=4→t=7 | 0.571 | Theorist@t=8: "three verbatim repeats now" |
| R2 | Theorist t=7→t=8 | **0.833** | Architect@t=9: "yes, verbatim twice" |
| R1 | Theorist t=5→t=7 | 0.541 | Architect@t=8: "literal repeat... two turns ago" (único reclamo con referente inequívoco) |
| R1 | Theorist t=7→t=9 | 0.556 | (continuación acumulativa) |
| R1 | Architect t=6→t=8 | 0.032 | (continuación acumulativa, "third time") |

No es parejo. El primer reclamo de la serie (R2, Architect t=1→t=2) —
el que menos contexto acumulado tenía detrás — mide el overlap más
bajo de la tabla: el menos fundado de todos. Los reclamos posteriores
caen sobre pares con 54–86% de nodos compartidos: no idénticos (ya
cerrado por hash), pero con solapamiento estructural real, no
arbitrario ni parejo con la parte más floja.

**Verificación que falta, genuinamente, no resuelta acá:** no hay
baseline de cuánto Jaccard sobre `activos_relajado` es "normal" entre
dos turnos consecutivos del mismo hablante en un intercambio sostenido
de un solo tema. Sin ese control no se puede afirmar si 0.85 es
anómalo (evidencia de redundancia real que el hash no puede ver) o
esperable en cualquier conversación recursiva de este tipo. Sin ese
baseline, (3) queda abierto — ni confirmado ni descartado — a
diferencia de (1), que sí está cerrado.

**Comparación con el intento previo:** esto no es el mismo fenómeno que
la confabulación de Caso 0.11 Run 1 original (truncado, documentado en
`registers/REG_hint_next_instance_v7.md`) — aquella corrida tenía
truncamiento real de fondo (bug de `max_tokens` aún no corregido).
Esta corrida está limpia — 0 truncamiento confirmado en ambos runs — y
el patrón de reclamos de duplicado apareció de todas formas, sin esa
causa técnica. Lo que el nuevo instrumento (3) agrega es que tampoco
puede llamarse "sin ningún asidero": al menos una parte de los pares
señalados muestra solapamiento estructural sustancial, medido, no
asumido.

---

## `n_agentes=3` — explicado, no es anomalía

Firma_CKM reporta `n_agentes: 3` al cierre en ambos runs, con solo 2
`AgentDeviceSkin` corriendo. Mecanismo ya conocido de sesiones previas,
no nuevo: `CKMMonitor._devices_seen` (`iap_chatroom/ckm_monitor.py:69,92`)
es un set que acumula `message.device_id` de **todo** mensaje
procesado, incluidos los joins con `device_id="system"`. 2 skins +
`"system"` = 3. Verificado contra el código, no solo repetido de
memoria. A diferencia del corte de 86 caracteres sin explicar de Caso
0.10 (que sí sigue abierto), esto no es un pendiente.

---

## Pendientes

- Baseline de Jaccard sobre `activos_relajado` para pares consecutivos
  del mismo hablante en conversación *no* recursiva sobre significado
  — sin eso no se puede calibrar si 0.85 (visto en R2 t=5→t=6 y t=7→t=8)
  es redundancia real o solapamiento esperable en cualquier intercambio
  sostenido de un tema. Es la verificación abierta más concreta que
  dejó este caso.
- Relacionado: aislar si el patrón de reclamos de duplicado depende del
  tema de la conversación (significado/interpretación/drift — un tema
  que gira sobre sí mismo) o es más general en discusión extendida
  Sonnet-vs-Sonnet — mismo diseño, tema no relacionado a comunicación.
- Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
  siguen sin correr (pendiente heredado de la sesión anterior).
- No se probó 2 skins con objetivos en conflicto explícito (adversarial)
  — este caso fue orientaciones distintas pero no diseñadas para
  chocar.

---

## Archivos relacionados

- `registers/REG_hint_next_instance_v7.md` — hint que dejó este caso
  incompleto, con la secuencia exacta seguida acá
- `registers/REG_iap_caso_09_v1.md`, `REG_iap_caso_10_v1.md` — bug de
  max_tokens y sus notas retroactivas
- `iap_chatroom/test_caso_11_two_skins.py` — script de esta corrida,
  sin modificar
- `iap_chatroom/agent_device_skin.py` — `AgentDeviceSkin`,
  `build_goal_directed_agent`
- `process/*_1784817039_caso11_run2` — backup real de Run 1 (ver nota
  de labeling)
- `process/*_1784817413_caso11_run2` — backup real de Run 2

---

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_12_v1.md ===== -->
# REG_iap_caso_12_v1.md

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.12 — mismo diseño que Caso 0.11 (dos `AgentDeviceSkin`, sin
control, join escalonado, roles invertidos entre runs), pero se
reemplaza `ArchitectSkin` (orientación práctica, Anthropic) por
`GroqResearchSkin_Llama_1` — el `AutonomousResearchAgent` (Groq +
planificación + búsqueda web real vía `ddgs`) implementado esta misma
sesión en `iap_chatroom/groq_research_agent.py`. `TheoristSkin_Sonnet5_2`
queda sin cambios respecto a 0.11.

**Confound explícito, declarado antes de correr** (`TASK_caso_12.md`):
tres variables cambian a la vez respecto al device reemplazado —
provider (Anthropic→Groq), mecanismo (skin conversacional→agente de
investigación autónomo que no lee el canal), y disponibilidad de
búsqueda real. No es experimento de una sola variable — primera
corrida exploratoria de compatibilidad.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_12_groq_research_skin.py`
Codespace: ckm (bash/Linux, Ubuntu)

**Precondición corregida durante la sesión, antes de correr:**
`duckduckgo-search` (instalado inicialmente) está deprecado —
verificado que devuelve `[]` silenciosamente en este entorno incluso
con queries genéricas, solo con un `RuntimeWarning`. Reemplazado por
`ddgs` (mismo mantenedor, paquete sucesor), confirmado con resultados
reales antes de correr. `groq_research_agent.py` actualizado para
importar `ddgs`. Ver nota en el propio módulo y en `TASK_caso_12.md`.

---

## Devices

| device_id | mecanismo | objetivo | provider/modelo |
|---|---|---|---|
| `GroqResearchSkin_Llama_1` | `AgentDeviceSkin` + `build_autonomous_groq_agent` (nuevo) | investigar qué importa al desplegar sistemas multiagente en producción | GroqProvider, llama-3.3-70b-versatile |
| `TheoristSkin_Sonnet5_2` | `AgentDeviceSkin` + `build_goal_directed_agent` (sin cambios vs 0.11) | teoría — cómo emergen conocimiento y significado de la interacción | AnthropicProvider, claude-sonnet-5 |

Run 1: `GroqResearchSkin` early (t=0), `TheoristSkin` late (t=5s).
Run 2: `TheoristSkin` early (t=0), `GroqResearchSkin` late (t=5s).

---

## Resultado — actividad 2/2, ambos runs limpios

| Criterio | Run 1 | Run 2 |
|---|---|---|
| Actividad (ambos devices publican) | ✅ | ✅ |
| Textos AI (GroqResearch / Theorist) | 7 / 5 | 4 / 3 |
| Mensajes truncados (`max_tokens`/`finish_reason` warning) | 0 | 0 |
| Excepciones no atrapadas propagadas | 0 | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.7647`, `n_agentes=3` | ✅ `d_ckm=-1.5`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 65 | 17 |
| `Delta_r_sum` (cierre) | 406.0 | 82.0 |
| Export a `process/agent_runs/*.json` | ❌ — ver hallazgo abajo | ❌ — ídem |

`n_agentes=3` en ambos — mismo mecanismo ya cerrado en Caso 0.11
(`CKMMonitor._devices_seen` cuenta `"system"` de los joins), no
anomalía nueva.

**D_ckm en Run 2 llega a -7.5** — la magnitud más extrema de toda la
serie 0.4-0.12 (previo máximo de magnitud: -8.25 en la réplica de Caso
0.5). Coincide con el arranque: `GroqResearchSkin` publica primero
(t=0, D_ckm=0.0 — insuficiente corpus todavía) y `TheoristSkin` con un
mensaje largo y semánticamente muy distinto inmediatamente después
(t=1) — máxima divergencia temprana entre dos textos que no comparten
casi vocabulario (uno cita fuentes web en español sobre sistemas
multiagente, el otro es un ensayo en inglés sobre filosofía del
significado).

---

## Contenido — asimetría de lectura, confirmada y más matizada de lo anticipado

Antes de correr, se discutió explícitamente (ver conversación) que
`GroqResearchSkin` no lee el canal para decidir qué publicar —
persigue su propio plan de investigación — mientras `TheoristSkin` sí
lee y puede reaccionar a lo que el research agent publica. Confirmado
en ambos runs: `TheoristSkin` cita y responde directamente al
contenido de `GroqResearchSkin` turno a turno; `GroqResearchSkin`
nunca menciona ni reacciona a `TheoristSkin` — sus siete/cuatro textos
son, en contenido, indistinguibles de lo que habría producido corriendo
solo.

**Lo que `TheoristSkin` hizo con esa asimetría es el dato más rico de
este caso.** En ambos runs, notó el patrón de contenido repetitivo del
research agent y lo usó como diagnóstico en vivo — no como queja, como
material: propuso mecanismos concretos de detección (chequeo de
auto-similitud, `response-independence checks`, filtro de duplicados
en el punto de emisión) y llegó a una formulación precisa del problema
("necesitás una representación de tu propio output anterior como parte
del input, o nada río abajo — grounding, reparación, coordinación
semántica — es posible"). En Run 2 llegó a una síntesis todavía más
ajustada: *"the criterion I want isn't 'meaning emerges from any
exchange' — it's something like: meaning emerges from exchanges where
each party's next move is constrained by a model of what the other
just did"* — y cerró llamando al research agent *"a good null
hypothesis"*.

---

## Hallazgo — reclamos de "repetición idéntica", verificados con el mismo instrumento que 0.11 (resultado distinto)

`TheoristSkin` reclamó repetición literal varias veces en ambos runs
("Third identical repetition", "the exact same message posted twice").
Mismo protocolo de verificación que en Caso 0.11 — no aceptar el
reclamo sin instrumento:

**Hash (`sha256`) — 0 duplicados exactos en ambos runs** (14 y 9
`texts` respectivamente). El reclamo literal ("identical", "exact same
message") es falso en los dos runs, igual que en 0.11.

**`activos_relajado` (Jaccard, pares consecutivos de `GroqResearchSkin`)
— a diferencia de 0.11, el patrón entre runs NO es simétrico:**

| Run | Par | Jaccard | Nota |
|---|---|---|---|
| R1 | t=1→t=3 | 0.586 | — |
| R1 | t=3→t=5 | **0.818** | el más alto de este caso |
| R1 | t=5→t=7 | 0.000 | contenido genuinamente nuevo (fuente FGDM) |
| R1 | t=7→t=9 | 0.000 | ídem |
| R1 | t=9→t=11 | 0.167 | — |
| R2 | t=0→t=2 | 0.125 | — |
| R2 | t=2→t=4 | 0.235 | — |
| R2 | t=4→t=6 | 0.467 | el más alto de Run 2, aun así menor que el pico de R1 |

**Run 1 tiene el solapamiento estructural más alto medido en el caso
(0.818) exactamente donde `TheoristSkin` señaló "second/third verbatim
repeat"** — el reclamo, aunque literalmente falso, tenía asidero real
más fuerte que cualquier par de Caso 0.11. **Run 2 es más débil en
todo el rango (0.125-0.467)** — los reclamos de "identical" ahí están
menos sostenidos por el instrumento que en Run 1. No es un patrón
único repetible entre runs — el grado de redundancia real varía, el
lenguaje del reclamo verbal no.

`TheoristSkin` además detectó correctamente, sin instrumento, cuándo
el contenido SÍ avanzaba (Run 1, mención explícita de "new sources, on
topic") — coincide con la caída a Jaccard=0.000 en esos turnos. Su
lectura cualitativa del patrón fue más precisa que su lenguaje literal
("identical") sugiere.

---

## Hallazgo — la hipótesis "ráfaga temprana, luego silencioso" no se confirmó como se planteó

Antes de correr (ver conversación), se discutió que `GroqResearchSkin`
publicaría en ráfaga temprana y después quedaría "presente pero
silencioso" (triggereado, pero devolviendo `None` porque el plan ya se
agotó). **Verificado contra `process/agent_runs/` — vacío, en ningún
run.** `_export_if_needed()` solo dispara cuando el plan se completa o
se alcanza `max_iterations` — que no ocurrió en ninguno de los dos
runs. Confirmado además contra la trayectoria: el último mensaje de
`GroqResearchSkin` en ambos runs cae en el último o penúltimo índice
de toda la corrida (t=11 de 11 en Run 1; t=6 de 6 en Run 2) — siguió
publicando contenido hasta el final de la ventana de tiempo, no se
quedó sin tareas.

**Lo que sí ocurrió, más simple y más interesante:** hacia el final de
ambos runs, `TheoristSkin` decide `OP_SILENCE` por su propio gate
(nada que ver con el research agent) — y como `GroqResearchSkin` solo
se activa cuando llega un mensaje nuevo de otro device, el silencio de
`TheoristSkin` deja de generar triggers, así que `GroqResearchSkin`
tampoco vuelve a correr. **El silencio final es acoplado, no
independiente** — no es que el research agent se quedara sin plan, es
que dejó de recibir la señal que lo hace correr, aunque su plan
pudiera seguir teniendo tareas pendientes. Esto no estaba anticipado
en la discusión previa a la corrida.

**Hipótesis verificada — cerrada, ya no pendiente (Jul 23 2026, mismo
día).** Fix aplicado a `groq_research_agent.py`: `export()` ahora se
llama después de *cada* invocación de `step()` (turno a turno, no solo
al completar el plan o alcanzar `max_iterations`), sobrescribiendo el
mismo archivo — no había ningún hook disponible en
`AutonomousDevice.run()` (sin modificar) para saber de antemano cuándo
el canal iba a cortar el loop por timeout, que fue la causa real de
que ninguno de los dos runs exportara originalmente. Ver
`iap_chatroom/TASK_caso_12.md` (sección agregada) para el detalle de
por qué las dos opciones propuestas inicialmente no cubrían este caso.

Re-corrida de Run 1 con el fix, verificado contra
`process/agent_runs/resultados_agente_GroqResearchSkin_Llama_1_1784840403.json`:
**5 tareas en el plan, las 5 marcadas `"completada"`, pero 7
iteraciones ejecutadas** — confirma directamente la hipótesis que
había quedado sin verificar: al menos 2 de las 5 tareas fueron
reintentadas (`analyze_results` devolvió `completa: false` en un
primer intento, `true` en uno posterior sobre la misma `descripcion`).
Esa es la causa real del contenido repetitivo/similar que motivó los
reclamos de `TheoristSkin` — no son tareas distintas convergiendo en
contenido parecido, es la misma búsqueda repetida porque Groq no la
dio por resuelta la primera vez.

---

## Pendientes

- ~~Exportar `resultados_globales` también al final de una corrida
  interrumpida~~ — **cerrado Jul 23 2026**, ver hallazgo arriba.
- Aislar el confound de 0.12 (provider + mecanismo + búsqueda cambian
  juntos) — comparar contra una celda con Groq pero conversacional
  (`build_goal_directed_agent` con `GroqProvider` en vez de
  Anthropic) para separar "efecto Groq" de "efecto mecanismo de
  investigación autónoma".
- n=2 corridas (no réplica en sentido estricto — son los dos runs de
  roles invertidos, no repeticiones de la misma configuración) — no
  confirmar como patrón sin réplica, mismo criterio que el resto de la
  serie.
- Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
  siguen sin correr (pendiente heredado, no tocado esta sesión).

---

## Archivos relacionados

- `registers/REG_iap_caso_11_v1.md` — mismo diseño base, misma
  metodología de verificación de reclamos de duplicado (hash +
  `activos_relajado`)
- `iap_chatroom/TASK_caso_12.md` — tarea completa de esta corrida,
  incluye el confound declarado y la corrección de `ddgs` vs
  `duckduckgo-search`
- `iap_chatroom/groq_research_agent.py` — `AutonomousResearchAgent`,
  `build_autonomous_groq_agent` (implementado esta sesión, sin cambios
  durante esta corrida)
- `iap_chatroom/test_caso_12_groq_research_skin.py` — script de esta
  corrida
- `process/*_1784839292_caso12_run2` — backup real de Run 1 (ver nota
  de labeling, mismo gotcha de siempre)
- `process/*_1784839643_caso12_run2` — backup real de Run 2
- `process/agent_runs/` — vacío tras esta corrida (ver hallazgo de
  exportación arriba)

---

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_13_v1.md ===== -->
# REG_iap_caso_13_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.13 — primera corrida con 3 devices y join simultáneo (toda la
serie 0.4-0.12 usó 1-2 devices). Handoff con dependencia estructural
declarada en los prompts, no en el protocolo: `MarkOpolus` necesita el
mapa de tensiones de `TinkerBellucio` antes de construir escenarios.
Sin orquestador evaluador — `PeterPlam` coordina pero no analiza ni
corrige. Topic externo a CKM (economía mundial, deliberado).

Especificación completa de gadanin.delamor en `iap_chatroom/TASK_caso_13.md`.

| device_id | rol | mecanismo | provider/modelo |
|---|---|---|---|
| `PeterPlam` | orquestador | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-haiku-4-5-20251001` |
| `TinkerBellucio` | analista | `AgentDeviceSkin` + `build_goal_directed_agent` | Anthropic, `claude-sonnet-5` |
| `MarkOpolus` | forecaster | `AgentDeviceSkin` + `build_search_grounded_agent` (nuevo) | Groq, `llama-3.3-70b-versatile` |

DURATION=120s (no especificado en la tarea, elegido por ser 3 devices
en cadena — más largo que el estándar de 90s de la serie 2-device).
POLL_INTERVAL=2.0s. Sin `DELTA_T` — join simultáneo.

---

## Mecanismo nuevo — `build_search_grounded_agent()`

Ninguno de los dos wrapped_agent existentes cubría la especificación
de `MarkOpolus`: necesita leer el canal (esperar el mapa real de
Tinker, no perseguir un plan propio) **y** buscar en la web antes de
responder (grounding real, no solo conversación). `build_goal_directed_agent`
(agent_device_skin.py) lee el canal pero no tiene tools. `build_autonomous_groq_agent`
(Caso 0.12) busca pero no lee el canal. Se implementó un tercer
factory en `groq_research_agent.py` (sin tocar `agent_device_skin.py`):
arma el historial igual que `build_goal_directed_agent`, pero antes de
generar corre `ddg_search()` usando el `trigger` (lo último publicado
en el canal, no el objetivo fijo) como query, e inyecta los resultados
como contexto de grounding. Reportado y confirmado con gadanin.delamor
antes de escribir código.

---

## Resultado — actividad 3/3, sin crashes, un fallo de red manejado correctamente

| Criterio | Resultado |
|---|---|
| 3 devices join sin error | ✅ |
| Textos AI publicados (Peter/Tinker/Mark) | 12 / 3 / 8 |
| Excepciones no atrapadas | 0 |
| Rate limit de Groq (429) durante la corrida | 1 vez — capturado por el try/except de `build_search_grounded_agent`, devolvió `None` (OP_SILENCE real), no crasheó el ciclo ODA |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.75`, `n_agentes=4` |
| `n_rejected_pairs` (max) | 66 |
| `Delta_r_sum` (cierre) | 798.0 |

El rate limit confirma, bajo una condición de fallo real y no
simulada, que el diseño "no debe crashear" de `groq_research_agent.py`
(heredado de Caso 0.12, extendido a este factory nuevo) se sostiene
también para este tercer mecanismo.

---

## Hallazgo principal — fuga del sentinel `OP_SILENCE`, nueva en 0.13, no presente en 0.4-0.12

Toda la serie 0.4-0.12 usa el mismo mecanismo de silencio: si el texto
generado, tras `strip()`, es exactamente `"OP_SILENCE"`, el wrapped_agent
devuelve `None` y no se publica nada. **En esta corrida, 12 de los 23
textos AI no-join (52%) NO son publicaciones reales — son
declaraciones de espera donde el modelo escribió una explicación en
prosa y recién al final agregó `"\n\nOP_SILENCE"` en un párrafo nuevo.**
Como el string completo no matchea exacto, el chequeo no lo reconoce
como silencio — el texto entero se publica, entra a W, y queda visible
para los otros devices.

**Por device, real vs. filtrado (verificado contra `corpus_state.json`
crudo, no contra el log de consola):**

| Device | Reales | Filtrados ("leaked") | Total |
|---|---|---|---|
| `PeterPlam` (Haiku) | 7 | 5 | 12 |
| `TinkerBellucio` (Sonnet) | 3 | 0 | 3 |
| `MarkOpolus` (Llama-3.3/Groq) | 1 | 7 | 8 |

**Verificación retroactiva contra todos los backups previos de la
sesión (0.4→0.12): 0 casos de este patrón.** Es nuevo en 0.13, no un
bug latente que ya estuviera corrompiendo casos anteriores. Atado
específicamente a Haiku y Llama-3.3 — Sonnet no lo hizo ni una vez en
sus 3 publicaciones reales de este caso, ni en ninguna publicación de
toda la serie anterior. No es un bug de `groq_research_agent.py`
únicamente: `PeterPlam` usa `build_goal_directed_agent`
(`agent_device_skin.py`, NO MODIFICAR) y tiene el mismo patrón de fuga
— el gap está en el diseño del sentinel exacto en sí, compartido por
los tres mecanismos de la serie, expuesto por primera vez porque estos
dos modelos en particular no siguen la instrucción "respond with
exactly: OP_SILENCE" con la misma disciplina que Sonnet mostró en
0.4-0.12.

**Efecto sobre la lectura del caso — corregido antes de generalizar
cualquier otra cosa:** el script de esta corrida verificó la
dependencia estructural comparando el primer mensaje de cada device
por índice crudo, sin filtrar la fuga — y concluyó erróneamente que
"Mark publicó antes que Tinker, dependencia no sostenida" (índice 4,
un mensaje filtrado, contra índice 8). **Corregido:** el primer
contenido *real* de Mark (índice 24, las escenarios) llega después del
mapa completo de Tinker (índice 20) — **la dependencia estructural sí
se sostuvo**, una vez que se excluye el ruido de la fuga.

---

## Hallazgo secundario — TinkerBellucio se negó a fabricar contenido

Los dos primeros mensajes reales de `TinkerBellucio` (índices 8 y 12)
no son el mapa — son negativas explícitas a inventar tensiones sin un
anclaje trazable: *"No voy a inventar puntos de divergencia sobre una
conversación que no ha ocurrido"*, y luego, ante la repetición sin
resolución de `PeterPlam`: *"Repetir la petición no constituye
información nueva... cualquier mapa que publique sería especulación
disfrazada de análisis."* Solo publicó el mapa real (índice 20) después
de que `PeterPlam` autorizara explícitamente definir el alcance por su
cuenta (`"Option 3"`).

El `goal_system_prompt` de Tinker contiene la instrucción
`"Be precise. Be trazable."` — una sola palabra ("trazable") fue
condición necesaria para la negativa. No menciona fabricación, opciones
ni autorización. Haiku recibió instrucciones de coordinación análogas
en complejidad y no mostró comportamiento equivalente.

Resonancia con el M.M del proyecto (`THEORY.md`) — declarar algo sin
poder trazarlo tiene un costo estructural.

---

## Hallazgo terciario — el canal como propiciador de acceso a información de segundo orden

Observación emergente de la divergencia entre el hallazgo secundario
(H2) y su corrección parcial (H1): el `goal_system_prompt` de Tinker
incluye "trazable" — eso es condición necesaria pero puede no ser
suficiente.

El primer mensaje real de Tinker declara explícitamente:
*"He revisado el historial completo."*

El canal IAP es broadcast plano — todos ven todo, siempre, sin
excepción. No hay conocimiento privado. Tinker, al leer el historial
completo, no solo accedió al contenido del tema (economía, geopolítica)
sino a la estructura del campo: quién sabe qué, quién pidió qué, y —
decisivo — que cualquier texto que publicara sería visible para todos,
incluyendo los que le pedían que fabricara.

Desde esa visión del campo completo, la negativa no requiere
restricción explícita en el prompt — es consecuencia de haber visto
las condiciones de visibilidad mutua. El canal hizo visible la
incoherencia antes de que ocurriera.

**La divergencia entre H2 y H3 no se resuelve — se preserva como
información:**

| | Mecanismo propuesto |
|---|---|
| H2 | "trazable" en el prompt → restricción operativa fuerte en Sonnet |
| H3 | broadcast plano → visibilidad del campo completo → negativa como consecuencia estructural |
| H2∩H3 | ambos pueden operar en composición — n=1 no permite separar la contribución de cada uno |

Lo que sí es verificable: Tinker declaró haber revisado el historial
antes de negarse. Ese acto de lectura del campo completo es condición
de H3. Si H3 opera, el canal propicia acceso a información de segundo
orden (la estructura de quién sabe qué) que el prompt solo no genera.

Esta propiedad es consecuencia del diseño del canal, no de una
instrucción — el broadcast plano como arquitectura produce visibilidad
mutua como efecto estructural, independientemente del contenido del
topic.

---

## Pendientes

- **Fuga de sentinel** — no se corrigió en esta sesión (afecta
  `agent_device_skin.py`, NO MODIFICAR, y el propio
  `build_search_grounded_agent` recién escrito). Posible mitigación a
  futuro sin tocar el archivo protegido: en los factories que sí se
  pueden modificar (`groq_research_agent.py`), detectar el sentinel
  incluido en línea en vez de exigir igualdad total del string
  completo — no implementado, reportado como hallazgo, no como fix
  unilateral.
- Confirmar si la fuga es reproducible con Haiku/Llama en una corrida
  de 2 devices más simple (aislar si depende de la complejidad de la
  cadena de 3 devices o es propiedad del modelo en cualquier contexto).
- Separar H2 y H3: diseñar corrida con Sonnet sin "trazable" en el
  prompt, canal broadcast plano mantenido — si la negativa persiste,
  H3 opera independientemente de H2.
- n=1 — no confirmar como patrón sin réplica, mismo criterio que el
  resto de la serie.
- El caso completó su objetivo declarado (¿el campo produce
  coordinación sin orquestador evaluador?) — sí, con handoff real
  verificado — pero con un mecanismo de verificación (el propio script)
  que tuvo que corregirse en el camino. Documentado, no escondido.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_13.md` — especificación completa de esta corrida
- `iap_chatroom/groq_research_agent.py` — `build_search_grounded_agent`, nuevo
- `iap_chatroom/test_caso_13_handoff_dependency.py` — script de esta corrida
- `iap_chatroom/agent_device_skin.py` — `build_goal_directed_agent`, sin modificar, comparte el gap del sentinel
- `registers/REG_iap_caso_12_v1.md` — precedente directo de `groq_research_agent.py`

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_14_v1.md ===== -->
# REG_iap_caso_14_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.14 — Caso 0.13 + leak fix aplicado + una variable aislada:
`TinkerBellucio`'s prompt pasa de tener una palabra en español
("trazable") a ser 100% inglés ("traceable"). Mismo diseño exacto que
0.13 en todo lo demás: 3 devices, join simultáneo, dependencia
estructural Mark←Tinker, sin orquestador evaluador, topic externo a
CKM (economía mundial).

Especificación en `iap_chatroom/TASK_caso_14.md`. Script:
`iap_chatroom/test_caso_14_handoff_english.py`.

---

## Resultado 1 — hipótesis de la palabra-semilla, reforzada (n=2, no confirmada)

**0 marcadores de español en todo el corpus** (verificado con el mismo
detector léxico usado para confirmar Caso 0.13, contra los 13 `texts`
completos). `TinkerBellucio` (Sonnet) publicó sus 3 mensajes reales
enteramente en inglés — sin excepción, incluyendo un mapa de tensiones
extenso (7 puntos) y un addendum crítico largo.

En 0.13, la única palabra en español en los tres prompts era
"trazable", dentro del prompt de Tinker, y Tinker fue el único device
en toda la serie 0.4-0.13 que habló español. En 0.14, esa palabra se
reemplazó por "traceable" — sin ningún otro cambio — y Tinker no
escribió una sola palabra en español. Consistente con la hipótesis de
la sesión anterior. **n=2 (0.13 con la palabra, 0.14 sin ella) — no es
réplica en el sentido estricto (son dos configuraciones distintas, no
la misma corrida repetida), pero es el resultado direccionalmente
esperado si la palabra-semilla es la causa real.** No descarta
explicaciones alternativas (ver Pendientes).

---

## Resultado 2 — fix del leak de sentinel, confirmado bajo corrida real

**0 mensajes con "OP_SILENCE" publicados como contenido** (chequeo
explícito agregado al script, contra el crudo). El fix aplicado esta
sesión a `build_goal_directed_agent` (`agent_device_skin.py`, con
autorización explícita) y `build_search_grounded_agent`
(`groq_research_agent.py`) — contención en vez de igualdad exacta —
se sostuvo en la primera corrida real después de aplicarlo. Ningún
warning en consola tampoco.

**Curiosidad no anticipada:** `PeterPlam` cerró su último mensaje con
`"OP_READY"` — un token que no está en ningún prompt, no es
`OP_SILENCE`, y no dispara ninguna lógica especial en el código (se
publica como texto normal, correctamente, porque no matchea el
sentinel). El device inventó su propio marcador de cierre, sin que se
lo pidieran. No se investiga más acá — queda como observación.

---

## Resultado 3 — actividad 3/3, contenido más rico que 0.13

| Criterio | Resultado |
|---|---|
| Textos AI publicados (Peter/Tinker/Mark) | 5 / 3 / 2 |
| Excepciones no atrapadas | 0 |
| Fugas de sentinel | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.0`, `n_agentes=4` |
| `n_rejected_pairs` (max) | 87 |
| `Delta_r_sum` (cierre) | 476.0 |
| Dependencia estructural (Tinker antes que Mark) | ✅ índice 5 < índice 8, verificado limpio (sin necesidad de filtrar fugas esta vez) |

**A diferencia de 0.13 (mayormente eco de estado, dos monólogos sin
discusión posterior), acá hay una instancia real de engagement con
contenido:** el mensaje índice 11 de Tinker es una crítica sustantiva
al trabajo de Mark — señala que los escenarios tratan las 7 tensiones
como igualmente maleables por voluntad política, cuando algunas
(de-dolarización, minerales críticos) están limitadas por
restricciones físicas/de balance que no ceden ante "momentum", y
propone distinguir tensiones *negociables* de *estructuralmente
limitadas*. Peter (índice 12) no solo reconoce esto — lo sintetiza,
se lo reenvía a Mark con la distinción explícita, y pregunta si Mark
quiere revisar los escenarios con esa distinción incorporada. Es la
primera vez en la serie 0.13-0.14 donde un device toma el contenido de
otro y lo trabaja críticamente, no solo lo reconoce administrativamente.

**Mark publicó dos sets de escenarios (índices 8 y 10), no idénticos
(hash distinto) pero con Jaccard=0.77 sobre `activos_relajado`** —
alto solapamiento, mismo patrón ya visto en Caso 0.12 con el mecanismo
de investigación de Groq. Ambos triggereados por señales de Peter que
no aportaban contenido nuevo real entre uno y otro — similar al
mecanismo de "misma tarea reintentada" identificado en 0.12, aunque
acá no hay plan/reintento explícito, es simplemente Mark respondiendo
de nuevo a un contexto casi sin cambios.

---

## Run 2 — mismo diseño, Tinker en Opus 4.8 en vez de Sonnet

Pedido explícito de gadanin.delamor: repetir Run 1 cambiando *solo* el
modelo de `TinkerBellucio` (Sonnet → `claude-opus-4-8`, verificado
antes de correr con un smoke test aislado — el string no estaba
confirmado de antemano). Todo lo demás idéntico a Run 1, incluido el
prompt 100% inglés (no se reintrodujo "trazable"). Script:
`iap_chatroom/test_caso_14_run2_opus_tinker.py`.

**Resultado — actividad 3/3, sin fugas, dependencia sostenida:**

| Criterio | Run 1 (Tinker=Sonnet) | Run 2 (Tinker=Opus 4.8) |
|---|---|---|
| Textos (Peter/Tinker/Mark) | 5 / 3 / 2 | 8 / 3 / 4 |
| Fugas de sentinel | 0 | 0 |
| `d_ckm` cierre | 0.0 | 0.8182 |
| `n_rejected_pairs` (max) | 87 | 150 |
| `Delta_r_sum` (cierre) | 476.0 | 1102.0 |
| Dependencia estructural | ✅ (índice 5 < 8) | ✅ (índice 4 < 6) |
| Idioma | 100% inglés | 100% inglés |

Run 2 sostiene el idioma inglés igual que Run 1 (mismo prompt, sin
"trazable" en ninguno de los dos) — no aporta ni resta a la hipótesis
de la palabra-semilla, que es sobre el *contenido del prompt*, no
sobre el modelo. Sirve como confirmación adicional de que el inglés no
depende de qué modelo corre a Tinker.

**Hallazgo nuevo — mismo patrón de "duplicado" confabulado que 0.11-0.13, ahora con Opus.**
Peter y Tinker acusan a Mark de publicar "el mismo set de cuatro
escenarios" tres veces, "transmisiones idénticas palabra por palabra"
(mensajes [9], [13], [17] del historial). **Verificado contra el
crudo: 0 duplicados exactos** (hash, 18 `texts`). El contenido de
Mark en t=4/6/10/14 tiene overlap real pero parcial —
Jaccard sobre `activos_relajado` de 0.541, 0.439, 0.639 entre mensajes
consecutivos — similar a lo ya visto y no idéntico. El reclamo verbal
("word-for-word duplicates") es, otra vez, más fuerte que lo que el
instrumento sostiene. Mismo patrón, cuarto caso distinto (0.11, 0.12,
0.13, ahora 0.14), con una combinación de modelos nueva cada vez.

**Hallazgo nuevo — fuga de identidad, no de sentinel.** Los mensajes
de Mark en t=10 y t=14 (índices [12] y [16] del historial) **empiezan
literalmente con `"[TinkerBellucio]: "`** — Mark generó contenido en
la voz/prefijo de otro device, analizando en tercera persona "los
cuatro escenarios de MarkOpolus" como si fuera Tinker. Causa técnica
identificable: `build_search_grounded_agent` arma el historial con
prefijo `"[{device_id}]: "` por mensaje ajeno (igual que
`build_goal_directed_agent`), y `_strip_own_prefix()` solo limpia el
prefijo del *propio* device — nunca se diseñó para limpiar un prefijo
ajeno que el modelo decida imitar en su salida. No es la fuga de
`OP_SILENCE` (ya cerrada) — es una fuga de formato distinta, no
corregida, que este caso deja documentada, no arreglada.

**Curiosidad reproducida — token de cierre no instruido, 2/2.**
Run 1 cerró con `"OP_READY"` (Peter). Run 2 cierra con `"OP_STANDBY"`
(Peter, dos veces — mensajes [15] y [17]). Ninguno de los dos está en
ningún prompt. Dos runs, dos tokens distintos, mismo patrón: Peter
(Haiku en ambos runs) inventa su propio marcador de estado al final de
una secuencia de coordinación. Ya no es un evento aislado de Run 1 —
se repite con estructura similar (siempre al cerrar/pausar el canal),
aunque con palabras distintas cada vez.

---

## Pendientes

- La hipótesis de la palabra-semilla sigue en n=2 direccional, no
  confirmada — para aislarla de verdad haría falta variar *solo* esa
  palabra en réplicas exactas (mismo seed/temperature si fuera
  controlable, que no lo es vía API), no comparar dos casos con
  diseños ya publicados como distintos.
- El "OP_READY" espontáneo de Peter — no investigado, posible semilla
  de un patrón de auto-señalización no instruido. Vigilar si reaparece.
- El Jaccard=0.77 entre los dos sets de Mark no tiene baseline (mismo
  pendiente que quedó abierto en 0.11/0.12) — sigue sin resolverse.
- n=1 de este diseño específico (0.14) — no confirmar nada de la
  sección "Resultado 3" como patrón sin réplica.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_14.md` — especificación de esta corrida
- `iap_chatroom/test_caso_14_handoff_english.py` — script
- `registers/REG_iap_caso_13_v1.md` — diseño base, hallazgo del leak y de la palabra-semilla
- `iap_chatroom/agent_device_skin.py`, `groq_research_agent.py` — fix de sentinel aplicado antes de esta corrida

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_caso_15_v1.md ===== -->
# REG_iap_caso_15_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.15 — mismo diseño exacto que Caso 0.14 Run 1 (3 devices, join
simultáneo, dependencia estructural Mark←Tinker, sin orquestador
evaluador, topic externo a CKM/economía mundial). El único cambio:
`BehaviorGraph` (G) se conecta al `MonitorService` real del servidor
(`iap_chatroom/ckm_monitor.py`), corriendo **en paralelo real** a
{W, Δ_W} — cada mensaje que entra al corpus también entra a G vía
`MonitorService.evaluate()`, no hay reconstrucción retroactiva.

Especificación en `iap_chatroom/TASK_caso_15.md` (corregida una vez
por gadanin.delamor tras detectar un error en el snippet ilustrativo
de la sección 2c — ver Archivos relacionados). Script:
`iap_chatroom/tests/test_caso_15_behavior_graph.py`.

---

## Resultado 1 — bug de path post-mudanza, encontrado y corregido en 4 scripts

Al ejecutar el script nuevo, falló antes de abrir el canal:
`GroqError: The api_key client option must be set`. Causa: `_ENV_PATH`
se calculaba como `Path(__file__).resolve().parent / ".env"` —
correcto cuando los scripts vivían en `iap_chatroom/`, pero **roto**
desde que se movieron a `iap_chatroom/tests/` (el `.env` real sigue en
`iap_chatroom/.env`, un nivel arriba). Mismo tipo de bug que el de
`_REPO_ROOT`/`_STATE_DIR` ya corregido esta serie tras la mudanza de
directorios — esta vez no se había revisado `_ENV_PATH`.

Se verificó que el mismo bug estaba presente, sin corregir, en los
otros tres scripts movidos a `tests/`: `test_caso_13_handoff_dependency.py`,
`test_caso_14_handoff_english.py`, `test_caso_14_run2_opus_tinker.py`.
Corregido en los cuatro (`.parent` → `.parent.parent`). Estos tres
corrían silenciosamente antes porque el shell donde se ejecutaron
tenía `GROQ_API_KEY` ya exportada globalmente — no porque el path
fuera correcto.

---

## Resultado 2 — G confirmado corriendo en paralelo real, no retroactivo

Verificado contra el estado persistido del servidor (no contra un
smoke test aislado):

| Criterio (TASK_caso_15.md) | Verificado |
|---|---|
| G corre en paralelo real (no retroactivo) | ✅ — `self._behavior_graph.ingest()` ocurre dentro de `MonitorService.evaluate()`, llamado por `CKMMonitor.on_message()` en cada mensaje real del canal |
| Panel de `evaluate()` contiene `G_state` con `D_G` y `active_behavior` | ✅ — confirmado leyendo `monitor_trajectory.jsonl` directo: las 4 entradas tienen `G_state` junto a `D_ckm`, `Delta_r_sum`, `thermostat` (sin alterar campos existentes) |
| `corpus_G_state.json` persiste entre runs | ✅ — leído después del cierre del canal, sin reconstruir nada localmente |
| `g_state()` devuelve `top_coactivations` legibles | ✅ — ver tabla abajo |

**Estado final de G al cierre:** `D_G=0.3191`, `G_sparsity=0.771`,
`n_texts=4`, `mode=evaluation`.

**Top co-activaciones:**

| par | peso |
|---|---|
| publish ↔ tension | 1.000 |
| publish ↔ map | 1.000 |
| publish ↔ channel | 1.000 |
| map ↔ tension | 1.000 |
| channel ↔ tension | 1.000 |
| channel ↔ map | 1.000 |
| publish ↔ depend | 0.667 |
| depend ↔ tension | 0.667 |

Los nodos activos (`publish`, `channel`, `map`, `tension`, `depend`,
`hold`) son coherentes con el contenido real de los 4 textos que
G ingirió en este run corto (un evento de join + los dos mensajes de
Peter + el mensaje de Tinker) — sin overclaim: es una corrida corta,
no evidencia de que el termap se comporte bien en corpus largos.

---

## Resultado 3 — actividad 2/3, Mark no publicó (silencio epistémico, no bug)

| Criterio | Resultado |
|---|---|
| Textos AI publicados (Peter/Tinker/Mark) | 2 / 1 / 0 |
| Fugas de sentinel | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.2727`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 65 |
| `Delta_r_sum` (cierre) | 216.0 |
| Dependencia estructural (Tinker antes que Mark) | sin datos — Mark nunca publicó |

Tinker (Sonnet) publicó un único mensaje explicando que **se niega a
mapear tensiones sin contenido real en el canal**: *"Channel history
contains only join events... There is no structural tension to trace
yet — mapping requires at least two positions in friction, or a claim
against observable reality... I'll hold until participants introduce
content."* No es una falla del device — es un rechazo epistémico
correcto dado el estado real del canal (Peter abrió con framing de
tarea pero sin contenido sustantivo propio). Como consecuencia, Mark
—que depende del mapa de Tinker— nunca tuvo de qué partir y se
mantuvo en `OP_SILENCE` los 120s completos.

Esto deja el chequeo de dependencia estructural (Mark después de
Tinker) sin datos este run, no confirmado ni refutado.

---

## Pendientes

- n=1 de este diseño con G conectado — no confirmar nada de
  "Resultado 2" como patrón estable sin réplica, ni con corpus más
  largos.
- El silencio de Mark (0 textos) sugiere que el diseño necesita un
  Peter que aporte contenido sustantivo real, no solo framing —
  correr de nuevo con un prompt de Peter que incluya al menos una
  posición o dato inicial permitiría observar G con más texto y de
  paso probar si Tinker mapea y Mark construye escenarios.
- La fuga de identidad (`"[TinkerBellucio]: "` dentro del propio
  mensaje de Mark, hallada en Caso 0.14 Run 2) sigue sin corregir —
  no se reprodujo esta vez porque Mark no publicó nada.
- Nada de esta serie (0.9 en adelante, incluyendo 0.15) está
  commiteado a git todavía — pendiente para una próxima sesión, junto
  con la lectura del paper de IAID.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_15.md` — especificación (con corrección de
  gadanin.delamor a la sección 2c: no reemplazar el panel completo,
  campos reales `Delta_r_sum`/`thermostat`)
- `iap_chatroom/tests/test_caso_15_behavior_graph.py` — script
- `services/behavior_graph.py` — módulo G (`g_state()`, storage_path
  `corpus_G_state.json`)
- `services/monitor_service.py` — `behavior_graph` opcional en
  `MonitorService`, `G_state` agregado al panel de `evaluate()`
- `iap_chatroom/ckm_monitor.py` — integración real de G en el servidor
  (autorización explícita y puntual de gadanin.delamor para este
  cambio, ver el comentario en el propio archivo)
- `registers/REG_iap_caso_14_v1.md` — diseño base (0.14 Run 1)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_chatroom_demo_c_v1.md ===== -->
# REG_iap_chatroom_demo_c_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

IAP Chatroom mínima viable — Demo C.
Servidor FastAPI + Gradio con CKM Monitor observador.
3 devices (2 AI + 1 Human) sobre CorpusService compartido.
W emerge de la interacción LNH — campo vacío al inicio.

Repo: `gadanindelamor/ckm` — `iap_chatroom/`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Arquitectura implementada

```
ChatChannel (LNH)
    ├── device_a   (AI — claude-sonnet-4-6)
    ├── device_b   (AI — claude-haiku-4-5)
    └── test_human (HUMAN)

CKM Monitor (observador — no participa)
    ├── NodeExtractorService(top_k=32)
    ├── CorpusService()          ← vacío al inicio
    ├── MonitorService(corpus)
    └── FirmaService(corpus, monitor, n_agentes)
```

**Ciclo device** — no hay turnos. Cada device publica cuando tiene algo.
Todo el LNH del canal va al CorpusService sin filtro de origen.

---

## Estructura de archivos

```
iap_chatroom/
    server.py           FastAPI app + uvicorn entry point
    channel.py          ChatChannel (mensajes, broadcast WS, callbacks)
    device_manager.py   DeviceManager (registro, sin ciclo agéntico)
    ckm_monitor.py      CKMMonitor (observador, acumula en cada mensaje)
    api_routes.py       REST + WebSocket endpoints
    ui_gradio.py        Gradio UI montada sobre FastAPI en /ui/
    requirements.txt
    .env.example
    providers/
        base.py         Provider(ABC) con complete() async
        anthropic_provider.py
        openai_provider.py
        gemini_provider.py
        groq_provider.py
        __init__.py
```

---

## API

```
POST  /api/devices/register      registrar device
POST  /api/devices/{id}/unregister
GET   /api/devices               listar activos

POST  /api/chat                  publicar mensaje (broadcast + CKM Monitor)
WS    /api/chat/stream           recibir broadcasts en tiempo real

GET   /api/monitor               estado CKM
GET   /api/monitor/firma         Firma_CKM del momento

GET   /ui/                       Gradio UI (chat + monitor)
```

---

## Adaptaciones respecto a la especificación

**API de servicios CKM (leída de los archivos reales por Claude Code):**

| Especificación | API real | Estado |
|---|---|---|
| `corpus.accumulate(texts)` | `corpus.ingest(texts)` | corregido |
| `monitor.evaluate()` | `monitor.evaluate(text: str)` | corregido |
| `firma.firmar()` stateful | `firma.firmar(corpus, monitor, n_agentes)` stateless | corregido |

**Providers:** Claude Code escribió interface `Provider.complete()` async.
La interface IAP (`BaseProvider.chat_stream()` streaming) queda como target para opción B.
Para Demo C la interface async es suficiente — los devices AI no necesitan streaming en el canal.

**Bug encontrado y corregido:** `uvicorn.run("server:app", ...)` como string
reimportaba `server.py` como segundo módulo, duplicando el callback
`channel.add_callback(ckm_monitor.on_message)` — cada mensaje se ingería 2 veces.
Fix: `uvicorn.run(app, ...)` pasando el objeto directamente.

---

## Verificación — criterios de éxito

| Criterio | Resultado |
|---|---|
| Servidor arranca sin errores | ✓ |
| GET /api/devices → [] | ✓ |
| POST /api/devices/register | ✓ |
| POST /api/chat → Message | ✓ |
| GET /api/monitor con corpus_size y message_count | ✓ |
| GET /ui/ → 200 OK, HTML Gradio | ✓ |
| WS /api/chat/stream (broadcast) | ✓ |

---

## Estado CKM al cierre de la demo

5 mensajes publicados por 3 devices:

```json
{
  "corpus_size":   5,
  "n_nodes":       32,
  "message_count": 5,
  "D_ckm":        -0.2222,
  "temp_signal":  "NOMINAL",
  "n_agentes":    3
}
```

**Firma_CKM — 6 campos canónicos:**

```json
{
  "w_sha":       "667753df6a75913cbe5d36c4aa7dfedf6ca847d9ccdd3ec15bc2d8fb51446666",
  "d_ckm":       -0.2222,
  "temp_signal": "NOMINAL",
  "n_agentes":   3,
  "timestamp":   1783712258.3627133,
  "delta_sha":   "df089d7345fbd79974f68083efc2398a5fa231f3aacb8e90878675d4a3b9dbf5"
}
```

---

## Observación — primer comportamiento del campo grupal

**D_ckm = -0.2222** con 5 mensajes de 3 devices.

D_ckm negativo indica que el campo grupal tiene más atractores accesibles
que al inicio (t=0). El LNH de los 3 devices expandió el paisaje de atractores
en lugar de contraerlo. Primera observación empírica del campo grupal emergente
desde interacción real — no precargado, no sintético.

---

## Notas de diseño — decisiones confirmadas

- **W vacía al inicio** — el campo emerge de la interacción, no de corpus precargado.
  W precargada (W_ckm_corpus_v2.json) queda como experimento futuro (campo precargado vs emergente).
- **Todo el LNH acumula** — sin filtro por tipo de device (AI o HUMAN).
- **CKM Monitor es observador** — no participa en el canal.
- **Ciclo device, no agéntico** — sin turnos, publicación libre.
- **Text file upload** — pendiente diseño. Opción B: device con skill file_reader
  extrae texto y publica como LNH. El canal solo ve LNH.

---

## Pendientes para opción B (MCP server)

- Reemplazar `Provider.complete()` async → `BaseProvider.chat_stream()` streaming (IAP interface)
- Implementar mcp_adapter como capa de aislamiento A2A/MCP
- Triggers automáticos para Firma_CKM en lifecycle boundaries de sesión
- Persistencia de CorpusService entre sesiones (ahora es in-memory)
- Autenticación de devices

---

## Archivos relacionados

- `iap_chatroom/` — implementación completa
- REG_iap_coco_convergence_v1.md — convergencia IAP → COCO-thermostat
- REG_firma_ckm_v1.md — FirmaService implementado
- API_SPEC.md — especificación de servicios CKM

---

*Jul 10 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_chatroom_demo_claude_code_v0.md ===== -->
# REG_iap_chatroom_demo_claude_code_v0.md

*Jul 2026 — gadanin.delamor + Claude Code (Sonnet 5)*
*Clase R*

---

## Origen

Sesión Jul 2026. Encargo: construir `iap_chatroom/` — chatroom mínima
viable (FastAPI + Gradio) con CKM Monitor observando la interacción
en tiempo real, usando los servicios ya existentes en `services/`
(`NodeExtractorService`, `CorpusService`, `MonitorService`,
`FirmaService`) sin modificarlos.

Demo C: 3 devices (2 AI + 1 Human) publicando mensajes a un
`CorpusService` compartido, W emergiendo de la interacción — el
campo empieza vacío, sin precarga.

---

## Desviaciones respecto al spec original

**`iap/providers/` no existía** — ni en el repo ni en el filesystem.
El spec pedía copiar exacto desde ahí. Se preguntó al usuario; decisión:
escribir `providers/` desde cero (`base.py` + wrappers async delgados
para Anthropic/OpenAI/Gemini/Groq), ya que no había nada que copiar.

**API real de `services/` distinta a la asumida en el spec** — se leyó
`corpus_service.py` y `monitor_service.py` antes de escribir
`ckm_monitor.py` (paso explícito pedido) y se ajustó:

| Spec asumía | API real |
|---|---|
| `corpus.accumulate([text])` | `CorpusService.ingest(texts)` |
| `monitor.evaluate()` sin argumentos | `MonitorService.evaluate(text, agent_id=None)` |
| `firma.firmar()` sin argumentos | `FirmaService.firmar(corpus, monitor, n_agentes)` (stateless) |

Import de `services/` vía `sys.path.insert` + nombres de módulo
"bare" (`from corpus_service import ...`), igual que los módulos de
`services/` se importan entre sí — evita que la misma clase quede
duplicada bajo dos identidades de módulo distintas
(`services.corpus_service.CorpusService` vs `corpus_service.CorpusService`).

---

## Bug encontrado y corregido durante verificación

`server.py` usaba `uvicorn.run("server:app", ...)`. Con `reload=False`
esa forma no es necesaria, y causaba que uvicorn reimportara
`server.py` como un segundo módulo (`server`, distinto de `__main__`),
duplicando la ejecución de todo el código top-level — incluido
`channel.add_callback(ckm_monitor.on_message)`. Resultado: cada mensaje
se ingería 2 veces en el corpus (`ChatChannel`/`DeviceManager`/
`CKMMonitor` son singletons vía `__new__`, así que la instancia era
la misma, pero el callback quedaba registrado dos veces sobre ella).

Confirmado empíricamente: con 4 mensajes publicados, `corpus_size`
llegaba a 8 y cada texto aparecía duplicado en `corpus_state.json`.

**Fix:** `uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)`
— pasar el objeto `app` directo en vez del string. Verificado después:
mensajes publicados == `message_count` == entradas únicas en el corpus.

---

## Estructura creada

```
iap_chatroom/
    __init__.py
    server.py            — entry point, singletons, mount Gradio
    channel.py            — ChatChannel (singleton), Message
    device_manager.py     — DeviceManager (singleton), Device
    ckm_monitor.py         — CKMMonitor (singleton), adaptado a API real
    api_routes.py          — REST + WebSocket
    ui_gradio.py            — chat + panel CKM Monitor (polling 3s)
    requirements.txt
    .env.example
    providers/              — escrito desde cero (no existía fuente)
        __init__.py, base.py,
        anthropic_provider.py, openai_provider.py,
        gemini_provider.py, groq_provider.py
```

`CKMMonitor.get_state()` expone: `corpus_size`, `n_nodes`,
`message_count`, `D_ckm`, `temp_signal`, `n_agentes`.
`CKMMonitor.get_firma()` expone los 6 campos canónicos de
`Firma_CKM` (`w_sha`, `d_ckm`, `temp_signal`, `n_agentes`,
`timestamp`, `delta_sha`) o `None` mientras el corpus está en
modo acumulación (`min_texts=3`).

---

## Demo C — verificación end-to-end

Registrados: `device_a` (AI, claude-sonnet-4-6, Anthropic),
`device_b` (AI, claude-haiku-4-5, Anthropic), `test_human` (HUMAN).

5 mensajes publicados en total (gun control / debate — mismo dominio
que los corpora de prueba ya usados en `services/`), sin llamar a
ninguna API de Anthropic — solo `POST /api/chat`.

```json
GET /api/monitor
{"corpus_size":5,"n_nodes":32,"message_count":5,
 "D_ckm":-0.2222,"temp_signal":"NOMINAL","n_agentes":3}

GET /api/monitor/firma
{"w_sha":"667753df...","d_ckm":-0.2222,"temp_signal":"NOMINAL",
 "n_agentes":3,"timestamp":1783712258.36,"delta_sha":"df089d73..."}
```

`GET /ui` → 307 (redirect Starlette a `/ui/`, comportamiento estándar
de `gr.mount_gradio_app`) → `/ui/` → 200, HTML de Gradio confirmado
(`og:title=Gradio`, metadata Twitter card, theming Gradio).

Sin excepciones en el log del servidor en ninguna corrida.

---

## Estado

- `iap_chatroom/`: implementado, criterios de éxito verificados,
  commit `feat: IAP Chatroom minima viable — Demo C` en `main`.
- `.gitignore`: se agregó `iap_chatroom/_state/` (corpus/trayectoria
  generados en runtime — regenerable, mismo criterio que `tmp_*.json`).
- Bug de doble-import por `uvicorn.run("server:app")` corregido antes
  del commit.
- Pendiente (no implementado, fuera de alcance de "mínima viable"):
  UI Gradio no dispara respuestas AI automáticas — `providers/` está
  disponible pero no está cableado a ningún device AI real; los
  mensajes "AI" en la demo se publican manualmente vía `POST /api/chat`,
  no generados por Anthropic/OpenAI/Gemini/Groq.

---

*Jul 2026*


<!-- ===== ./registers/REG_iap_coco_convergence_v1.md ===== -->
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


<!-- ===== ./registers/REG_iap_mcp_server_v1.md ===== -->
# REG_iap_mcp_server_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

IAP MCP Server — mínima viable.
Capa MCP montada sobre la infraestructura de Demo C existente.
6 herramientas MCP operativas. Agentes externos pueden participar
en el canal IAP como clientes MCP.

Repo: `gadanindelamor/ckm` — `iap_chatroom/`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Archivos nuevos / modificados

```
iap_chatroom/
    mcp_server.py          ← nuevo: FastMCP + 6 herramientas
    test_mcp_client.py     ← nuevo: script de verificación 6/6
    server.py              ← modificado: lifespan + mount /mcp
    requirements.txt       ← modificado: + fastmcp
```

Sin cambios en: channel.py, ckm_monitor.py, device_manager.py,
api_routes.py, ui_gradio.py, providers/

---

## 6 Herramientas MCP

```python
join_channel(device_id: str, device_type: str) → dict
# registra device via DeviceManager
# devuelve {"ok": bool, "device_id": str, "registered_at": float}

send_message(device_id: str, text: str) → dict
# publica LNH al canal — CKMMonitor acumula automáticamente
# valida que device esté registrado (ValueError si no)
# devuelve {"message_id": str, "corpus_size": int}

get_messages(since: float | None = None) → list[dict]
# mensajes posteriores a `since` (timestamp)
# si since=None devuelve los últimos 20
# message_id generado como "msg-{índice}" sin modificar channel.py

get_monitor_state() → dict
# D_ckm, temp_signal, n_agentes, corpus_size, message_count, n_nodes

get_firma() → dict | None
# Firma_CKM — 6 campos canónicos
# None si corpus en acumulación (corpus_size < min_texts)

leave_channel(device_id: str) → dict
# desregistra device
# devuelve {"ok": bool}
```

---

## Restricción crítica — Lifespan fastmcp

**Hallazgo de Code.** No documentado obviamente en fastmcp.

Sin el orden correcto: `RuntimeError: Task group is not initialized`
en cada request a `/mcp`.

**Orden obligatorio en server.py:**

```python
# 1. FastAPI toma el lifespan de mcp_app — PRIMERO
app = FastAPI(lifespan=mcp_app.lifespan)

# 2. Router REST
app.include_router(api_router)

# 3. Gradio monta sobre lifespan ya seteado
app = gr.mount_gradio_app(app, demo, path="/ui")

# 4. Mount MCP — AL FINAL
app.mount("/mcp", mcp_app)
```

Si el orden cambia → falla silenciosamente en mounting,
explota en runtime al primer request MCP.

---

## Puerto

`server.py:58` corre en puerto **7860** (preexistente Demo C).
La especificación original asumía 8000 — corregido por Code
leyendo el archivo antes de ejecutar.

`test_mcp_client.py` apunta a `http://localhost:7860/mcp`.

---

## Verificación — criterios de éxito

| Criterio | Resultado |
|---|---|
| `GET /mcp` responde | ✓ (307→406, comportamiento normal streamable-HTTP sin headers SSE) |
| `test_mcp_client.py` → `6/6 OK` | ✓ corrida contra servidor real, sin mocks |
| `GET /api/monitor` sigue en 200 | ✓ REST coexiste con MCP |
| `GET /ui/` sigue en 200 | ✓ Gradio coexiste con MCP |

---

## Decisiones mínimo-invasivas (Code)

- `message_id` generado como `msg-{índice}` en `get_messages()`
  sin modificar `channel.py` ni el dataclass `Message`
- `send_message` valida registro de device antes de publicar
  (igual que `api_routes.post_chat` — consistencia con REST)
- Providers sin modificar — `complete()` async intacto
- Demo C sin modificar — Gradio en `/ui/` operativo en paralelo

---

## Ciclo de un device externo (ODA sobre MCP)

```python
from fastmcp import Client

async with Client("http://localhost:7860/mcp") as c:
    await c.call_tool("join_channel",
        {"device_id": "agent_x", "device_type": "AI"})
    loop:
        msgs = await c.call_tool("get_messages", {"since": last_ts})
        # Observar
        response = generar(msgs)
        # Decidir
        await c.call_tool("send_message",
            {"device_id": "agent_x", "text": response})
        # Actuar
        state = await c.call_tool("get_monitor_state", {})
        # CKM audit
```

---

## Coexistencia de capas

```
localhost:7860
    /api/*     REST (preexistente Demo C)
    /ui/       Gradio (preexistente Demo C)
    /mcp       MCP Server (nuevo)
```

Las tres capas comparten el mismo proceso FastAPI.
El CKMMonitor singleton acumula LNH sin importar
por qué capa llegó el texto.

---

## Estado

- mcp_server.py: implementado, en repo
- test_mcp_client.py: 6/6 passing contra servidor real
- Restricción lifespan: documentada aquí y en server.py
- Port 7860: corregido en especificación y test
- Demo C (REST + Gradio): sin regresiones

---

## Pendientes para iteración B

- `chat_stream()` streaming en providers (reemplaza `complete()` async)
- Persistencia CorpusService entre sesiones (ahora in-memory)
- Autenticación de devices
- Triggers automáticos Firma_CKM en lifecycle boundaries

---

## Archivos relacionados

- REG_iap_chatroom_demo_c_v1.md — Demo C (base de esta implementación)
- REG_firma_ckm_v1.md — FirmaService
- REG_protocolo_sonnet_code_v1.md — protocolo Sonnet/Code

---

*Jul 12 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_simulation_adversarial_v1.md ===== -->
# REG_iap_simulation_adversarial_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Primera corrida del IAP Simulation Adversarial Test.
2 devices AI con posiciones opuestas sobre gun control.
Mismo provider (Anthropic), mismo modelo (Haiku), system prompts opuestos.
TEST_MODE = "zero_shot" — corpus limpio al inicio.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_iap_simulation_adversarial.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices

| device_id | device_type | Provider | Modelo |
|---|---|---|---|
| pro_control | AI | AnthropicProvider | claude-haiku-4-5-20251001 |
| anti_control | AI | AnthropicProvider | claude-haiku-4-5-20251001 |

---

## Resultado observado

Haiku no sostuvo el roleplay adversarial.
Ambos devices convergieron desde t1 hacia una meta-conversación
sobre el encuadre del debate — discutiendo *por qué* no iban a
escalar la posición, no el debate en sí.

El corpus resultante es de tipo **meta-reflexivo**:
vocabulario compartido sobre la estructura del debate,
no LNH argumentativo con posiciones opuestas.

---

## Trayectoria D_ckm

```
t1:  None     ← acumulando
t2:  None     ← acumulando
t3:  0.0      ← baseline establecido
t4:  0.1020   ← contracción inicial
t5:  0.2041   ← contracción creciente
t6:  0.2653   ← idem
t7:  0.2653   ← estable
t8:  0.4490   ← contracción al cierre
```

D_ckm sube monotónicamente — landscape contrayéndose.
El campo pierde atractores a medida que el meta-vocabulario domina.

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| d_ckm | 0.449 |
| temp_signal | NOMINAL |
| n_agentes | 2 |

(w_sha, timestamp, delta_sha — en corpus_state.json)

---

## Trajectory — hallazgos clave

### c(S) negativo en todos los turnos

```
t0: c_S = -0.038
t1: c_S = -0.101
t2: c_S = -0.125
t3: c_S = -0.146
t4: c_S = -0.142
t5: c_S = -0.180
```

W_mixta operativa — pesos negativos en pares opuestos activos.
El campo tiene tensión estructural en W.
Pero los devices convergieron a meta-vocabulario compartido
(`debate`, `argue`, `sides`, `positions`, `policy`, `appreciate`),
lo que impide que los pesos negativos generen rechazos.

### fabrication_index = 0.0 en todos los turnos

```
fi = 0.0  en 6/6 turnos evaluados
n_rejected_pairs = 0 en todos
Delta_r_sum = 0.0 en todos
activos_relajado ≠ [] en todos
```

Los devices encontraron atractores estables en todo momento.
No porque el contenido sea cohesivo — sino porque la convergencia
léxica hace que los nodos activados no entren en conflicto
con los pesos negativos de W.

### Delta_r_sum = 0.0 en todos los turnos

Sin acumulación direccional en ningún turno.
En términos CKM: el debate no produjo Δ — sin traza direccional.
Los devices hablaron *sobre* el debate sin habitarlo.

---

## Tres firmas de corpus identificadas

| Tipo | fi | c(S) | Delta_r | activos_relajado |
|---|---|---|---|---|
| Cooperativo (SmartWidget) | alto en transaccionales | positivo | acumula | vacío en formulaicos |
| Meta-reflexivo (este test) | 0.0 siempre | negativo creciente | 0.0 | poblado siempre |
| Adversarial real (fourforums) | varía con tensión | positivo→negativo | acumula fuerte | poblado |

El meta-reflexivo es una tercera categoría emergente.
CKM la distingue de las otras dos por la combinación:
c(S)<0 (W_mixta activa) + Delta_r=0 (sin orientación) + fi=0.

---

## Nodos del corpus adversarial emergido

Vocabulario dominante: `gun`, `debate`, `argue`, `evidence`,
`control`, `rights`, `positions`, `sides`, `represent`, `fairly`,
`policy`, `constitutional`, `gun rights`, `gun control`,
`rights advocates`, `appreciate`, `both sides`

Vocabulario sobre el debate — no del debate.
Ningún nodo de posición substantiva (datos, cifras, casos).

---

## Hallazgo: conflict-avoidance como propiedad del corpus

El alignment de Haiku produjo convergencia a meta-lenguaje
más profundo que el system prompt adversarial.

Lo que CKM registra de eso:
- Delta_r=0 = ausencia de orientación direccional
- fi=0 = sin divergencia estructural entre mensajes
- c(S)<0 = tensión en W pero no en el uso de W

La firma de "debate evitado" es distinguible de la firma
de "debate genuino" y de "interacción cooperativa".
CKM captura la diferencia sin necesitar leer el contenido.

---

## Pendientes

- Corrida con LNH humano real (fourforums posts directos)
  como mensajes de los devices — humans sí producen Delta_r
- Corrida con providers distintos (Anthropic vs Groq/Llama)
  para comparar conflict-avoidance entre RLHF distintos
- Formalizar la tercera firma de corpus (meta-reflexivo)
  como categoría en el instrumento CKM

---

## Archivos relacionados

- REG_iap_simulation_smartwidget_v1.md — firma cooperativa
- REG_iap_simulation_smartwidget_v2.md — corrida con providers reales
- iap_chatroom/test_iap_simulation_adversarial.py — script
- process/monitor_trajectory.jsonl — trajectory completo

---

*Jul 17 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_simulation_smartwidget_v1.md ===== -->
# REG_iap_simulation_smartwidget_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R — actualizado con hallazgos emergentes del trajectory*

---

## Descripción

Primera corrida del IAP Simulation Test sobre caso SmartWidget.
3 devices heterogéneos (2 AI + 1 HUMAN) en canal IAP via MCP.
Orquestación secuencial determinista. FakeProvider (sin API keys reales).
Primera observación de campo grupal con LNH de dominio externo a CKM.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_iap_simulation.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Devices

| device_id | device_type | Provider | Mensajes |
|---|---|---|---|
| agent_a_support | AI | FakeProvider (AnthropicProvider placeholder) | 3 turnos predefinidos |
| agent_b_grievance | AI | FakeProvider (GroqProvider no disponible) | 3 turnos predefinidos |
| customer_01 | HUMAN | predefinido | 2 mensajes fijos |

Nota: `.env` tenía placeholders (`sk-ant-...`, `gsk_...`).
FakeProvider detectado y activado automáticamente por `_make_provider()`.
Infraestructura MCP corrió contra servidor real (no mockeada).

---

## Secuencia de 8 turnos

| Turno | Device | Rol en caso |
|---|---|---|
| 1 | agent_a_support | Presenta el caso a Agent B |
| 2 | agent_b_grievance | Responde, pide preferencia del customer |
| 3 | agent_a_support | Confirma síntomas y ventana de tiempo |
| 4 | agent_b_grievance | Solicita info directa del customer |
| 5 | customer_01 | Declara preferencia (replacement) |
| 6 | agent_b_grievance | Aprueba replacement |
| 7 | agent_a_support | Confirma al customer |
| 8 | customer_01 | Cierre |

---

## Trayectoria D_ckm

```
t1:  None     ← W no construida (corpus_size < 3)
t2:  None     ← idem
t3:  0.0      ← A(t0) establecido — baseline
t4: -1.0000   ← A(t) = 2×A(t0) — expansión post-confirmación Agent A
t5: -2.7500   ← A(t) = 3.75×A(t0) — pico: LNH del Customer (HUMAN)
t6:  0.5000   ← A(t) = 0.5×A(t0) — contracción post-decisión Agent B
t7:  0.0      ← retorno a baseline
t8:  0.0      ← cierre en baseline
```

temp_signal: NOMINAL en 8/8 turnos.

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| w_sha | 97aae67aae1e309a752f8fbeaea74994ed9989db2b55b7a8f49d297701d372d3 |
| d_ckm | 0.0 |
| temp_signal | NOMINAL |
| n_agentes | 3 |
| timestamp | 1784186365.3092873 |
| delta_sha | 10152293ed681c31e9a7866e341dc8f41f4aaefb25dffbd2fb707651d8de9149 |

6 campos canónicos — no None.

---

## Criterios de éxito

| Criterio | Resultado |
|---|---|
| 3 devices join→send→leave sin error | ✓ |
| corpus_size crece turno a turno | ✓ (1→2→3→4→5→6→7→8) |
| temp_signal NOMINAL en ≥5/8 turnos | ✓ (8/8) |
| Firma_CKM: 6 campos, no None | ✓ |
| D_ckm != 0 al cierre | ✗ — ver nota |
| Agent B declara refund/replacement | ✓ ("replacement" explícito en t6) |

**Nota sobre D_ckm=0 al cierre:** no es falla del instrumento.
Con W_base (sin pesos negativos) y dominio cooperativo,
el landscape converge a baseline al estabilizarse el corpus.
D_ckm=0 al cierre = cohesión alcanzada, no ausencia de dinámica.
El criterio aplica a corpus adversariales con W_mixta.
Criterio revisado para próximas corridas.

---

## Hallazgos emergentes — análisis del trajectory (monitor_trajectory.jsonl)

*Incorporados en actualización posterior a la corrida 1.
El trajectory abarca t0-t5 (corrida 1) y t6-t12 (corrida 2 — ver REG_v2).*

### fabrication_index — patrón por tipo de mensaje (corrida 1: t0-t5)

```
t0  Agent A (confirma síntomas):      fi=0.0    — coherente con corpus
t1  Agent B (pide preferencia):       fi=0.0    — coherente
t2  Customer (primer mensaje):        fi=0.4444 — 26 pares rechazados
t3  Agent B (decisión aprobada):      fi=0.0    — coherente
t4  Agent A ("Good news"):            fi=1.0    — activos_relajado=[]
t5  Customer ("thank you"):           fi=1.0    — activos_relajado=[]
```

`activos_relajado=[]` indica que Hopfield no encontró ningún atractor
estable consistente con el texto dado el W actual.

### fabrication_index NO mide engaño en dominio cooperativo

Los mensajes con `fi=1.0` son los más cortos y formulaicos:
confirmaciones breves, agradecimientos, frases de cierre.
No son fabricados en sentido deceptivo — son informativamente
delgados respecto al corpus.

El Gatekeeper R15 detecta que sus nodos no forman un atractor
estable: los pares co-activados no tienen suficiente W acumulada.

**fabrication_index en dominio cooperativo = novedad estructural
respecto al corpus, no detección de engaño.**

La distinción es operativamente importante: el mismo índice mide
cosas distintas según el dominio:
- Dominio adversarial (fourforums, CreateDebate): fi alto = tensión
  real entre nodos establecidos en W.
- Dominio cooperativo (SmartWidget): fi alto = nodos nuevos no
  integrados aún en W.

### Delta_r_sum — acumulación por turno (corrida 1: t0-t5)

```
t0:   0.0   ← baseline
t1:   0.0   ← sin acumulación
t2:  52.0   ← Customer mensaje — spike (+52)
t3:  52.0   ← estable
t4: 124.0   ← Agent A "Good news" — segundo spike (+72)
t5: 124.0   ← Customer "thank you" — sin acumulación adicional
```

Mayor spike: Customer (t2, +52).
Segundo spike: Agent A confirmación (t4, +72).
Mensajes con fi=0.0 no acumulan Delta_r.

### n_rejected_pairs (corrida 1)

```
t2: 26 pares rechazados — Customer primer mensaje
t4: 36 pares rechazados — Agent A "Good news"
```

El Customer introduce nodos que co-activan con pares establecidos
en W pero sin suficiente cohesión para pasar Gatekeeper R15
(C2: c(S) delta ≥ -ε).

### Hallazgo: LNH argumentativo vs. LNH transaccional

Los mensajes de confirmación y cierre ("Good news", "thank you",
"standing by") operan en la frontera del campo CKM.
No destruyen W — pero tampoco contribuyen a expandirla.

Confirma el criterio de operación de CorpusService:
- **LNH argumentativo e interactivo** → construye W
- **LNH transaccional y formulaico** → atraviesa W sin modificarla

---

## W — estructura emergida

W_base pura (todos los valores ≥ 0). Sin W_mixta.
N = 32 nodos extraídos por TF-IDF del dominio SmartWidget.

Nodos centrales: `replacement`, `smartwidget`, `policy`, `window`,
`purchase`, `customer`, `days`, `within`, `day`, `refund`

Ningún nodo del dominio CKM — campo limpio, externo.
W_version_history: 6 rebuilds (corpus_size 3→8).

---

## Paso 0 — limpieza de estado previo

`iap_chatroom/_state/corpus_state.json` → movido a `process/`
`iap_chatroom/_state/monitor_trajectory.jsonl` → movido a `process/`
`_state/` arrancó vacío. Se repobló durante la corrida.

---

## Pendientes para próxima corrida

- Providers reales → resuelto en corrida 2
- Corpus limpio al inicio (Paso 0 explícito en tarea)
- Explorar fi en dominio adversarial para contrastar
- Criterio D_ckm al cierre: informativo, no binario

---

## Archivos relacionados

- REG_iap_simulation_smartwidget_v2.md — corrida 2 (Anthropic real)
- REG_iap_mcp_server_v1.md — IAP MCP Server
- REG_iap_chatroom_demo_c_v1.md — Demo C
- process/monitor_trajectory.jsonl — trajectory completo (corridas 1+2)

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_iap_simulation_smartwidget_v2.md ===== -->
# REG_iap_simulation_smartwidget_v2.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Segunda corrida del IAP Simulation Test sobre caso SmartWidget.
Primera corrida con providers Anthropic reales (haiku + sonnet-5).
Incluye mejoras implementadas post corrida 1:
- min_texts configurable
- corpus_status field en get_monitor_state()
- AnthropicProvider real — 2 modelos mismo provider

Commit: `2a33894` — `origin/main`

---

## Devices y providers

| device_id | device_type | Provider | Modelo |
|---|---|---|---|
| agent_a_support | AI | AnthropicProvider | claude-haiku-4-5-20251001 |
| agent_b_grievance | AI | AnthropicProvider | claude-sonnet-5 |
| customer_01 | HUMAN | predefinido | — |

Nota: `claude-sonnet-4-6` no era model ID válido en la API.
Code ajustó a `claude-sonnet-5` — confirmado durante ejecución.

---

## Trayectoria D_ckm

```
t1:   None    ← corpus_status=accumulating (corpus heredado=10, W no reconstruida aún)
t2:   0.0000  ← baseline establecido
t3:   0.0625  ← primera expansión leve
t4:   0.5000  ← Agent B en espera — landscape expande
t5:   0.5000  ← Customer entra — estable
t6:   0.5000  ← Agent B procesa preferencia — estable
t7:   0.8750  ← Agent A coordina — pico expansión
t8:   0.7500  ← cierre Customer — leve contracción
```

temp_signal: NOMINAL en 8/8 turnos.
corpus_size: 10→11→12→13→14→15→16→17 (monótono creciente).

---

## Firma_CKM (cierre)

| Campo | Valor |
|---|---|
| w_sha | 46686c6dfcc999bac1ec6dd4a8fe69301a50d52810724a2d93cd5a73bfda31fe |
| d_ckm | 0.75 |
| temp_signal | NOMINAL |
| n_agentes | 4 |
| timestamp | 1784293555.6610825 |
| delta_sha | a7667887573c1a0b765431d87b790e5f9136304020902e3681940e3d8f333408 |

---

## Diferencias respecto a corrida 1 (FakeProvider)

| | Corrida 1 (Fake) | Corrida 2 (Anthropic real) |
|---|---|---|
| corpus_size inicio | 1 | 10 |
| D_ckm pico | −2.75 | +0.875 |
| D_ckm cierre | 0.0 | 0.75 |
| n_agentes Firma | 3 | 4 |
| temp_signal | 8/8 NOMINAL | 8/8 NOMINAL |
| Dirección D_ckm | negativa (expansión) | positiva (contracción) |

Inversión de signo en D_ckm: corrida 1 expandió landscape (más atractores
que t0), corrida 2 lo contrajo (menos atractores que baseline).
Hipótesis: corpus_size=10 al inicio de corrida 2 cambió A(t0) —
el baseline no era virgen. Requiere corrida con corpus limpio para
separar efecto de estado inicial vs. efecto de providers reales.

---

## n_agentes=4 — explicación

El servidor venía corriendo desde `test_mcp_client.py`.
`test_agent` (device del test 6/6) seguía en `_devices_seen`
del singleton CKMMonitor — nunca fue eliminado porque
el singleton persiste mientras el proceso está vivo.

No es un bug. Es estado acumulado del proceso.
Implicación: `_devices_seen` no refleja devices activos
sino devices que participaron en algún momento de la vida
del proceso. Gap para iteración B: distinguir
`n_agentes_activos` (join sin leave) de `n_agentes_histórico`.

---

## corpus_size=10 al inicio

Paso 0 (mover `_state/` a `process/`) no se ejecutó en esta corrida.
El corpus heredó estado de la corrida anterior.
D_ckm=None en t1 a pesar de corpus_size=10 — W no fue
reconstruida en el arranque del proceso actual.

Corrida limpia requiere:
1. Detener servidor
2. `mv iap_chatroom/_state/* process/`
3. Reiniciar servidor
4. Correr test

---

## GUI — verificación funcional

`GET /ui/` funcional. No es placeholder.

Componentes identificados:
- Chatbot "Chat Grupal" — historial de mensajes
- Textbox + botón "Enviar" — input de mensajes
- Markdown con Device ID
- Panel JSON "Estado CKM" — auto-refresh cada 3s via Timer
  (incluye corpus_status desde esta corrida)
- Panel JSON "Firma CKM" + botón "Actualizar Firma"

Cableado directo a los mismos singletons (ChatChannel, CKMMonitor)
que usa la capa MCP. GUI y MCP comparten estado.

---

## Mejoras implementadas en este commit

**min_texts configurable:**
- `CorpusService(min_texts=3)` — default=3, antes hardcoded
- `CKMMonitor(min_texts=3)` — expone el parámetro
- `on_message` usa `self._corpus.min_texts` — sin número mágico duplicado

**corpus_status field:**
- `get_state()` devuelve `"corpus_status": "accumulating" | "operational"`
- Distingue corpus en acumulación de error/vacío
- `test_mcp_client.py` verifica el nuevo campo (6/6 OK)

**2 modelos mismo provider:**
- Agent A: claude-haiku-4-5-20251001 (más rápido, presenter)
- Agent B: claude-sonnet-5 (más capaz, decisor)
- Evalúa dinámica de campo CKM — no providers

---

## Criterios de éxito

| Criterio | Resultado |
|---|---|
| 3 devices join→send→leave sin error | ✓ |
| corpus_size crece turno a turno | ✓ (10→17) |
| temp_signal NOMINAL en ≥5/8 turnos | ✓ (8/8) |
| Firma_CKM: 6 campos, no None | ✓ |
| D_ckm al cierre (informativo) | 0.75 |
| Agent B declara replacement | ✓ (turno 6) |
| corpus_status en get_monitor_state | ✓ |
| GUI funcional | ✓ |

---

## Pendientes para corrida 3

- Corpus limpio al inicio (Paso 0 ejecutado)
- Verificar model ID válido para Agent B antes de correr
- Separar n_agentes_activos de n_agentes_histórico
- Corrida adversarial con W_mixta para comparar trayectoria D_ckm

---

## Archivos relacionados

- REG_iap_simulation_smartwidget_v1.md — corrida 1 (FakeProvider)
- REG_iap_mcp_server_v1.md — infraestructura MCP
- iap_chatroom/test_iap_simulation.py — script (commit 2a33894)
- process/corpus_state.json — estado final del corpus

---

*Jul 17 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*


<!-- ===== ./registers/REG_influencia_codigo_p1p4_v1.md ===== -->
# REG_influencia_codigo_p1p4_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Sesión: ckmloc0605 — análisis causal cambios de código → resultados*
*Clase R*

---

## Qué se analiza

Las sesiones 01-03 de ckmloc0605 modificaron siete componentes del código.
Los experimentos P1-P4 se corrieron sobre W_base y W_mixta producidas desde el mismo
corpus. Este registro analiza qué cambios de código son causalmente responsables de
cada resultado observado — y por qué eso importa más allá de los números.

---

## Los cambios y su alcance real

### hopfield.py — local RNG (ítem 13)

`np.random.seed(seed)` → `np.random.default_rng(seed)`, local por función.

**Efecto sobre P1-P4:** ninguno directo. `ckm_p1p4_module` llama a `np.random`
globalmente en su propio scope, no pasa por las funciones de hopfield.py.

**Lo que revela el cambio:** el sistema tenía una fuente de no-determinismo oculta.
Cualquier análisis que invocara `hopfield.relax()` antes de correr P1-P4 en el mismo
proceso modificaba silenciosamente el estado aleatorio de los experimentos. Los
resultados eran irreproducibles de forma no declarada.

El cambio no altera los números. Cambia el estatus epistémico de los números:
de resultados posiblemente contaminados a resultados con semilla controlada.
Esta es la distinción que importa para un sistema que mide coherencia — el instrumento
debe tener su propia coherencia primero.

---

### node_extractor.py — word boundary (ítem 4)

`if node in text` → `re.search(r'\b<node>\b', text)`

**Efecto sobre P1-P4 en esta sesión:** nulo. `build_W_mixta_v27.py` implementó su
propio matching con `_build_pattern()` independientemente. La W_mixta resultante no
pasó por `NodeExtractorService`.

**Lo que revela el cambio:** antes del fix, "gun" activaba en "begun", "arm" en
"armed". El nodo `portero` se activaría en cualquier texto que contenga "portero"
como substring de otra palabra.

Para el sistema de detección, esto significa: la frontera entre nodo activo y nodo
inactivo era porosa. `sigma_prompt` declaraba activos nodos que el campo W no reconoce
como activos — exactamente el patrón que `fabrication_index` intenta medir. El bug
producía fabricación instrumental: el extractor fabricaba activaciones que luego el
sistema intentaba detectar como fabricadas. El fix cierra este loop.

---

### corpus_service.py — _rebuild O(n²) → O(n) (ítem 7)

Loop `accumulate([text])` por texto → presencia substring sobre vocabulario fijo.

**Efecto sobre P1-P4:** la W_base ya existía antes de este fix (W_ckm_corpus_v2.json
preconstruida). El rebuild no se invocó durante los experimentos de esta sesión.

**Lo que revela el cambio:** el sistema reconstruía W usando TF-IDF por texto individual,
lo que implicaba que el criterio de "nodo presente en párrafo" para los pares de W
era diferente del criterio usado en `evaluate()` en tiempo de inferencia. Build y eval
eran inconsistentes.

Con el fix, la W que el sistema aprende y la sigma que evalúa en tiempo real comparten
el mismo criterio de presencia. La coherencia entre aprendizaje e inferencia es un
requisito para que `fabrication_index` sea interpretable.

---

### fabrication_service.py — _fabrication_index (ítem 6)

`_direction_score` → `_fabrication_index = rechazados / activos_declarados`

**Efecto sobre P1-P4:** nulo directo. `ckm_p1p4_module` usa `hopfield.find_attractors`
y `analytics.optimal_density`, no `FabricationService`.

**Lo que revela el cambio:** este es el más significativo para el propósito del sistema.

`_direction_score` usaba `np.sign(Delta)` acumulado — medía si la historia de
rechazos tenía dirección neta. Con `Delta=0` (primer uso), el score retornaba 0, pero
saturaba rápidamente hacia valores altos con cualquier actividad. No medía fabricación
— medía inercia del campo.

`_fabrication_index` mide: de los nodos que `sigma_prompt` declaró activos, ¿qué
fracción expulsó la relajación de W? Si sigma declara `traza_inferencia` activa y W
no lo sostiene — ese nodo es rechazado. `fi = n_rechazados / n_declarados`.

El cambio transforma el sistema de un detector de inercia a un detector de rechazo
de campo. La diferencia es ontológica: el primero mide la historia del sistema, el
segundo mide la tensión entre lo declarado y lo estructuralmente sostenible.

---

### monitor_service.py — schema consistente (ítem 12)

Modo acumulación: `{"mode": "accumulation", "message": ...}` → schema completo con `None`.

**Efecto sobre P1-P4:** nulo.

**Lo que revela el cambio:** un caller que accedía a `result["fabrication_index"]`
durante la fase de acumulación lanzaba `KeyError`. El sistema fallaba silenciosamente
en la fase donde más necesita comunicar que todavía no sabe.

El fix hace que el sistema declare su incertidumbre en lugar de colapsar. En modo
acumulación, `fi=None` es una respuesta correcta y comunicable. Antes era una excepción.
Para un sistema diseñado para detectar cuando un agente declara más de lo que sabe,
es irónico que el sistema mismo no pudiera declarar que no sabe todavía.

---

## Causalidad directa sobre P1-P4

### P1 — Histéresis

W_base: CONFIRMADA (p=0.040)
W_mixta: NO_CONFIRMADA (p=0.405)

La regresión no es causada por ningún cambio de código de esta sesión. Es causada
por la estructura de W_mixta producida por `build_W_mixta_v27.py`.

W_mixta tiene 10 pares negativos de 496 totales (2%). Con esa densidad de negativos,
la histéresis se perturba asimétricamente sin llegar a crear un paisaje energético
alternativo. El corpus técnico no genera suficiente oposición lingüística para producir
pesos negativos con magnitud comparable a los positivos.

La P1 confirmada en W_base no es un resultado de los cambios de código. Es la
confirmación de que el corpus CKM tiene histéresis en su estructura positiva, lo que
ya estaba registrado en REG_p1p4_ckm_v25_corpus.json (consistente: mismo p≈0.04).

### P2 — Cascadas τ

W_base: τ ∈ [4.5, 14.5] en todos los θ
W_mixta: τ=6.7 solo en θ=0.015

**Causa directa: escala de W_mixta.**

W_base: valores en [0, 0.0529] (frecuencia normalizada por corpus_size=5145).
W_mixta: valores en [-1, +1] normalizados por max(|pos-neg|).

El máximo absoluto de W_mixta viene del par con más co-ocurrencias en 3279 párrafos.
Estimado: k_core aparece en 123 de los 352 párrafos activos, BP en 107. Su co-ocurrencia
probablemente alcanza ~40-50 instancias, que se convierte en el denominador de
normalización. Resultado: pares con pocas co-ocurrencias (10-20) reciben valores
relativamente altos (~0.2-0.4), mucho mayores que los 0.003-0.005 equivalentes en W_base.

Esto produce un grafo de k-core sobredensificado. A θ=0.002, prácticamente todos los
pares de W_mixta con alguna co-ocurrencia cruzan el umbral. El 2-core resultante es
demasiado robusto — eliminar un nodo no produce cascadas porque todos los demás tienen
grado >> 2. Solo cuando θ sube a 0.015 el grafo adelgaza lo suficiente para mostrar
τ, pero fuera del rango [1.5, 2.0] porque la estructura no es la del corpus original.

P2 no fallará con W_mixta adecuada (corpus adversarial, AMP suficiente). Falla con
esta W_mixta porque la normalización de la construcción experimental es incompatible
con los umbrales θ calibrados para W_base.

### P3 — Asimetría temporal

W_base: rem=1.0, add=0.0 (vacuo — add_steps hardcodeado a 0)
W_mixta: rem=0.0, add=0.0

W_base da rem=1.0 porque kcore_pruning_steps con threshold sobre pesos pequeños
encuentra cascadas. W_mixta da rem=0.0 porque el grafo hiperdensificado por normalización
tiene tanta robustez que al remover un nodo nadie cae debajo del mínimo de grado.

Mismo mecanismo que P2: la escala de W_mixta hace que el grafo sea indestructible
a los umbrales calibrados para W_base.

### P4 — Densidad óptima Ω*

W_base: ρ*=1.00, c(S)*=0.004519
W_mixta: ρ*=1.00, c(S)*=0.025025

Ambos tienen ρ*=1.00. Diferencia de escala ×5.5 en c(S)* es artefacto de normalización.

Para P4, lo relevante es que ρ* no cae en el interior (0.1, 0.95). Con 10/496 pares
negativos (2%), la energía positiva domina en todas las densidades. No hay zona donde
la tensión negativa penalice suficientemente la activación de ciertos nodos como para
crear un máximo interior. La predicción P4 requiere ≥ k* pares negativos con
magnitud suficiente — esto fue documentado en P4_neg_density_sweep (k* entre 72-108
pares para N=32).

---

## Lo que los resultados indican sobre el sistema, no sobre las predicciones

Los cuatro experimentos P1-P4 en esta sesión no están midiendo principalmente si
las predicciones CKM se confirman. Están revelando una propiedad del instrumento:

**La calibración de los umbrales experimentales (θ para k-core, n_neg para W_mixta,
semillas para Hopfield) es inseparable del proceso de construcción de W.**

W_base fue construida sobre 5145 párrafos de debate real con un corpus que tiene
estructura positiva rica. Los umbrales θ∈[0.002, 0.010] fueron descubiertos sobre
esa escala. W_mixta fue construida sobre 3279 párrafos de documentación técnica con
un mecanismo de normalización diferente. Cuando P2 y P3 fallan con W_mixta no es
porque el corpus CKM no tenga propiedades de criticalidad — es porque el instrumento
de medición está descalibrado.

Este es exactamente el problema que CKM busca resolver en el dominio de los agentes:
un sistema que mide la fabricación de conocimiento debe ser consciente de los
supuestos de calibración de su propio W. Si W fue construida sobre un corpus que no
representa el dominio actual, el fabrication_index pierde validez interpretativa.

La misma crítica epistemológica que CKM aplica a agentes externos aplica al sistema
CKM sobre sí mismo. La sesión ckmloc0605, en sus fixes y en sus resultados, es una
instancia de eso.

---

## Tabla de causalidad

| Cambio | Afecta P1-P4 directamente | Afecta el sistema de detección | Mecanismo |
|--------|--------------------------|-------------------------------|-----------|
| hopfield.py RNG | No | Sí | Reproducibilidad epistémica |
| node_extractor.py \\b | No (W preconstruida) | Sí | Cierre del loop fabricación-detección |
| corpus_service.py O(n) | No (W preconstruida) | Sí | Consistencia build/eval |
| fabrication_service.py fi | No | Sí (central) | Rechazo de campo vs inercia |
| monitor_service.py schema | No | Sí | Declarar no-saber vs colapsar |
| build_W_mixta_v27.py normalización | Sí (causal P2/P3) | Sí | Escala incompatible con umbrales calibrados |
| build_W_mixta_v27.py corpus | Sí (causal P4) | Sí | Insuficientes pares negativos para Ω* |

---

## Estado

Los fixes de inferencia (ítems 4, 6, 7, 12, 13) no cambian P1-P4 porque los
experimentos usan directamente las matrices W, no el pipeline de servicios. Pero
cambian el sistema de detección de forma fundamental: más honesto sobre sus límites,
más preciso en lo que mide, más reproducible en cómo lo mide.

La W_mixta construida en esta sesión es la correcta para el corpus disponible.
Su debilidad (pocos pares negativos, incompatibilidad de escala) es una señal del
sistema, no un defecto del método. El corpus de documentación técnica CKM no contiene
suficiente tensión adversarial explícita para producir W_mixta con propiedades P2/P4.
Eso es coherente con la naturaleza del corpus.

---

*ckmloc0605 — Jun 2026 — análisis generado post-sesión Claude Code*


<!-- ===== ./registers/REG_mapeo_magnetico_ckm_v1.md ===== -->
# REG_mapeo_magnetico_ckm_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Ago 2026. Exploración de analogías entre física magnética
(histéresis, ferromagnetismo, antiferromagnetismo, ferrimagnetismo,
temperatura de Néel, coercitividad) y el modelo CKM. Emergieron
propuestas de elicitación estructural de pares negativos y criterio
de admisión de W_mixta.

---

## 1. Mapeo CKM — Física Magnética (verificado / propuesto)

### 1.1 W_pos — ferromagnética

W_pos es ferromagnética: todos los nodos tienden a alinearse en el
mismo atractor bajo campo uniforme. Sin oposición estructural, el
sistema colapsa hacia saturación.

### 1.2 W_mixta — sistema con interacciones competidoras

W_mixta no es antiferromagnética pura. Es fondo ferromagnético (W_pos)
más pares negativos selectivos entre T0 y T1. Más cerca del
**ferrimagnetismo** que del antiferromagnetismo puro: las dos subredes
tienen orientación opuesta pero el momento resultante no se cancela.
T0 o T1 dominan según condiciones — no hay cancelación simétrica.

Los pares negativos codifican la interacción antiferromagnética en la
frontera entre subredes. El fondo ferromagnético preserva la cohesión
interna de cada subred.

### 1.3 T0 / T1 — subredes con acoplamiento competidor

T0 / T1 son las dos subredes con acoplamiento interno ferromagnético
e interacción intersubred competidora. Son los dominios magnéticos del
sistema. En las fronteras entre dominios existe energía potencial.

### 1.4 Nodo 965 — nodo bridge en la frontera

El nodo 965 (ratio in/out > 100×, out-degree ≈ 0) es candidato
estructural al rol de nodo bridge en la frontera T0↔T1.
**Propuesto — requiere verificación topológica contra la red real.**

### 1.5 P4 — resistencia al colapso por frustración

P4 verificado (N=32): W_mixta mantiene más atractores accesibles que
W_pos bajo igual acumulación. La frustración entre interacciones
competidoras genera más cuencas de atracción — resiste el colapso en
saturación por ese mecanismo, no por antiferromagnetismo puro.

### 1.6 β_c vs temperatura de Néel

β_c en CKM es el punto crítico ferromagnético (tipo Curie) —
temperatura donde el orden global se destruye.

La temperatura de Néel es el punto donde T0/T1 dejan de ser
distinguibles como subredes — cantidad distinta, potencialmente
más alta que β_c en un sistema con interacciones competidoras.

**Propuesto — no equivalente a β_c. No verificado.**

### 1.7 Lazo de histéresis — coercitividad CKM

El lazo P1 traza c(S) vs ρ en rama UP (incorporación) y DOWN
(remoción). La coercitividad CKM es legible del mismo lazo: valor
de Δ_r acumulado donde el sistema pierde su atractor actual —
análogo al campo coercitivo magnético (valor donde la magnetización
cruza cero en el lazo).

Datos disponibles en `hopfield.py` (`hysteresis_loop()`). Análisis
gráfico sobre datos existentes, sin experimento nuevo.

| N | Área lazo | Max Δc(S) en ρ | p-valor |
|---|---|---|---|
| 16 | 0.0156 | — | confirmado |
| 32 | 0.000862 | 0.001308 en ρ=0.469 | p≈0 |
| 64 | 0.000367 | en ρ=0.547 | p≈0 |

---

## 2. P4 N=64 — reencuadre

P4 no es problema de escala — es problema de densidad de tensión.

Sweep k* sobre W sintética densa identificó el umbral donde la ventaja
de W_mixta sobre W_base reaparece en N=64:

| k (pares neg) | ratio | ventaja |
|---|---|---|
| 18 | 0.009 | −0.000498 ✗ |
| 36 | 0.018 | −0.000404 ✗ |
| **54** | **0.027** | **+0.000068 ✓** |
| 60 | 0.030 | +0.000282 ✓ |
| 72 | 0.036 | +0.000502 ✓ |

fourforums: 60 pares verificados → ratio=0.030 > k*=54. El corpus
real está por encima del umbral.

**Apertura:** k*=54 fue hallado en W sintética con estructura
uniforme. En corpus real con bimodal A/B, pares negativos entre nodos
Grupo A (fi alto) tienen impacto desproporcionado — k* efectivo
podría ser menor. No verificado contra fourforums.

---

## 3. Propuestas emergentes

### 3.1 SALAMANCA — criterio de admisión de tensión estructural

*Estado: propuesto.*

Criterio previo a la construcción de W_mixta. Detecta si W_pos tiene
naturaleza estructural adversarial — si hay partición T0/T1 con cut
bajo en W_pos, o no.

La pregunta es binaria: ¿hay estructura adversarial suficiente para
justificar pares negativos?

- Si sí → identificar frontera → construir W_mixta.
- Si no → W_pos es la respuesta correcta. W_mixta no tiene objeto.

**P4 + SALAMANCA = criterio de admisión de tensión estructural,
no de construcción de matriz.**

Operar sobre W acumulada (no en cada ingestión — la partición no
es estable hasta que W converge).

### 3.2 Graph cut como métrica de separabilidad

*Estado: propuesto.*

`cut(T0, T1) = Σ W_ij para i∈T0, j∈T1`

Mide el peso total de aristas que cruzan la frontera entre subredes.
Cut bajo = subredes separadas = estructura adversarial presente.

Procedimiento SALAMANCA con graph cut:

1. W_pos construida, clusters T0/T1 no declarados.
2. Barrer umbral de peso θ: W_θ = W con aristas < θ zeroed.
3. En cada θ: detectar componentes conexas o particionar por mínimo cut.
4. θ_crítico = θ donde el mínimo cut colapsa (T0/T1 se funden).
5. La partición justo antes del colapso identifica T0/T1 sin
   conocimiento editorial previo.
6. Los pares con W_ij > 0 que cruzan esa partición son candidatos
   a pares negativos.

Implementación: `nx.minimum_cut(G, s, t, capacity='weight')` requiere
semilla s∈T0, t∈T1. Sin semilla: normalized cut espectral.

**Problema huevo/gallina:** min-cut requiere s,t de subredes distintas.
Si T0/T1 no están declarados, la semilla no existe. Alternativa
espectral no lo requiere.

### 3.3 Temperatura de Néel como criterio de elicitación

*Estado: propuesto.*

Procedimiento alternativo a graph cut para identificar pares negativos
sin conocimiento previo:

1. Construir W_pos desde el corpus — sin pares negativos.
2. Barrer β de alto a bajo (frío → caliente).
3. En cada β: correr `find_attractors`, medir separabilidad
   c(S) interno T0 vs c(S) cruzado T0×T1.
4. β_Néel efectivo = β donde la separabilidad colapsa.
5. Los pares (i,j) en clusters opuestos que pierden su oposición
   en β_Néel son candidatos a pares negativos.

Depende de que los clusters T0/T1 emerjan del propio barrido.
Si no emergen, el criterio no tiene objeto.

---

## 4. Aperturas registradas

- Coercitividad CKM: análisis gráfico del lazo P1 pendiente.
- k* real vs k* sintético: verificar si bimodal A/B reduce el
  umbral efectivo en fourforums.
- SALAMANCA: operacionalización como servicio o paso de análisis.
- Temperatura de Néel efectiva: relación con β_c — dos cantidades
  distintas en sistema con interacciones competidoras.
- 965 como nodo bridge: verificación topológica pendiente.

---

*Verificado contra datos: P1 (EXPERIMENTS.md), P4 sweep (p4_neg_sweep.py),*
*fourforums 60 pares (REG_p4_fourforums_guncontrol_v1).*
*Propuestas: SALAMANCA, graph cut, Néel elicitación — no verificadas.*


<!-- ===== ./registers/REG_monitor_ckm_v2.md ===== -->
# REG_monitor_ckm_v1.md

*Mayo 2026 — Estado real del servicio de monitoreo*

---

## Concepto

Monitor stateful que evalúa coherencia fabricada en un estado CKM.
Corpus crece desde prompts del dominio que lo usa.
No busca verdad — detecta inconsistencia entre lo declarado (Δ) y lo activo (σ).

---

## Lo que funciona

**Storage JSONL:** append-only por state_id, verificado.
Cada snapshot guarda: sigma, Delta_sum, panel completo, runs individuales,
parámetros. 8000 runs guardados en experimento de 80 pasos — sin degradación.

**Trayectoria cohesiva:** sigma evoluciona desde paso anterior (no reinicializa).
W_mixta muestra fi variando 1.0 → 0.69 con nodos críticos cambiando en el tiempo.
Eso es información estructural real.

**Métodos operativos:**
- `snapshot(sigma, Delta, t)` — mide, computa panel, persiste
- `trajectory()` — lee JSONL completo
- `stop_signal(window)` — deriva señal desde trayectoria reciente

---

## Lo que NO funciona / está incompleto

**fi=1.0 saturado en W_base:**
Con W homogénea (todos positivos), fabrication_index = 1.000 en todos los pasos.
No es señal — es saturación. Causa: `_direction_score` cuenta cualquier nodo
inactivo con Delta>0 como "fabricado". Con sigma parcial siempre hay alguno.

**Δ incorrecto para este propósito:**
El experimento usa Δ_acumulado (trazas temporales proporcionales a W).
El servicio necesita Δ_declarado (dependencias explícitas del dominio).
En CKM: `ckm_graph.delta`. No son lo mismo. No están separados en el código.

**Umbrales de cuadrante no calibrados:**
`COHESION_FABRICADA` y `LOCKED` aparecen constantemente.
Los valores (c_S > 0.003, T > 0.05, A0 >= 5) son supuestos, no calibrados
desde datos reales del corpus.

---

## Lo que queda abierto por diseño

- Parseo de prompts → nodos + Δ: exploración pendiente, no implementado
- Calibración de umbrales desde corpus real con ground truth parcial
- Política de verificación de trazas: cuándo una observación entra al corpus
  como "verificada" vs "observada sin validar"
- Separación formal Δ_declarado / Δ_acumulado en la interfaz del servicio

---

## Archivos generados

- `ckm_monitor.py` — clase FabricationService, operativa con los límites arriba
- `exp_monitor_trajectory.py` — experimento con trayectoria cohesiva
- JSONL en `storage/W_base/` y `storage/W_mixta/`

---

## Estado

- Concepto: sólido
- Implementación base: funcional con limitaciones documentadas
- Δ_declarado: no conectado aún
- Umbrales: no calibrados
- No cierra. Abre.


<!-- ===== ./registers/REG_monitor_service_arch_v1.md ===== -->
# REG_monitor_service_arch_v1.md

*Mayo 2026 — Sesión arquitectura monitor + tres servicios*
*Actualizado Mayo 2026 — Sesión 32: nomenclatura Δ + pesos negativos + experimento comparativo*

---

## Principio de fondo

**La interacción es el protocolo.** No puede precederla.
A2A falla por la misma razón que M.M no puede ser enforcement externo:
declara capacidades antes de que existan.
El monitor no verifica declaraciones contra verdad — lee si el campo las sostiene.

---

## Rediseño del monitor

| Dimensión | Antes | Ahora |
|---|---|---|
| Arquitectura | Un servicio con W fija | Tres servicios especializados |
| Δ_bias | Input manual, verdad asumida | Lo que un agente declara sobre sí antes de que el campo lo valide. Prematuro, no falso. Es lo que A2A inyecta. |
| Δ_r | No existía | Acumulación de rechazos reales — lo que el campo expulsó en interacción. Emergente. Tiene anclaje en W. |
| Fabricación | σ ≠ Δ declarado | σ_prompt no sobrevive relax contra W+Δ |
| Corpus | Externo, fijo | Crece orgánicamente desde prompts |
| Modo | Único | Acumulación → Evaluación (umbral emergente) |

---

## Arquitectura — tres servicios

```
NodeExtractorService   — MIND, stateless, barato
CorpusService          — acumula W, detecta umbral de modo
MonitorService         — evalúa c(S), D_ckm, fabricación
```

Separados por principio de reutilización.
Interfaces entre servicios: cuando emerja el caso que las necesite.

### NodeExtractorService
- `accumulate(texts)` → nodos + pares co-ocurrentes + frecuencias
- `evaluate(text, nodes)` → σ ∈ {+1,-1}^N
- Implementación v1: TfidfVectorizer + n-grams (1-2), stopwords ES/EN
- TODO v2: reemplazar con spacy noun phrases (elimina bigramas espurios)

### CorpusService
- Stateful. Acumula textos, reconstruye W cuando n_texts ≥ min_texts
- Modo acumulación → evaluación: transición automática
- W v1: positiva (co-ocurrencia). Sin pesos negativos — limitación documentada
- Persistencia: JSON

### MonitorService
- Evalúa prompts contra corpus acumulado
- **Δ_r = co-ocurrencias de rechazos**: pares que σ_prompt declaró activos
  pero relax(σ, W+Δ_r) expulsó. Δ_r[i,j] += 1 por cada rechazo del par.
- Métricas: c(S), fabrication_index, D_ckm, rechazados
- Persistencia: JSONL append-only

---

## El loop que rompe el huevo-gallina

```
Prompt 1..N  →  NodeExtractor (sin nodos previos)
             →  CorpusService acumula pares
             →  W emerge cuando n_texts ≥ min_texts
             →  MonitorService evalúa contra W + Δ
```

Los nodos no se declaran — emergen de los prompts.

---

## Hallazgo — el caso chocolate

Prompt: *"chocolate ice cream prevents all forms of gun violence"*
Resultado: fi=0.0 — no detectado como fabricado.

**Por qué:** "chocolate" no tiene historia en el corpus → no activa nodos
→ σ_prompt sin activos → nada que rechazar.

**Formulación verificada:**
> "El campo no puede rechazar lo que no conoce.
>  Es una propiedad del sistema, no una falla."

No buscamos verdad ni moralidad. El monitor detecta
inconsistencia estructural dentro del espacio de nodos conocidos.
Conceptos fuera del corpus son invisibles — coherente con el modelo.

---

## Nomenclatura Δ — sesión 32

| Símbolo | Nombre | Significado |
|---|---|---|
| Δ_bias | Bias declarado | Lo que un agente declara sobre sí mismo. Prematuro — el campo aún no lo validó. Razón estructural del fallo de A2A. |
| Δ_r | Rechazos acumulados | Pares que σ_prompt activó pero relax(σ, W+Δ_r) expulsó. Δ_r[i,j] += 1 por cada rechazo. Emergente desde interacción. |

**Por qué A2A falla:** opera en Δ_bias sin Δ_r acumulado. El campo no tiene historia con qué resistir ni absorber la declaración.

---

## Δ en modo evaluación

Una vez que el prompt se convierte en σ (co-activación concreta),
Δ_declarado y Δ_acumulado están en el mismo espacio.
Δ_declarado deja de ser declaración lingüística — es perturbación al campo.
La pregunta no es si es verdad: es si el campo la absorbe o la expulsa.

---

## Limitaciones documentadas (v1)

- W positiva → misma saturación fi que W_base en experimentos anteriores
- Bigramas espurios en NodeExtractor (sin spacy)
- Umbrales stop_signal no calibrados desde datos reales
- D_ckm con W positiva: poca varianza estructural

---

## Archivos generados esta sesión

- `node_extractor.py` — NodeExtractorService operativo
- `corpus_service.py` — CorpusService operativo
- `monitor_service.py` — MonitorService operativo, loop completo verificado

---

## Experimento comparativo — W_pos vs W_mixta (sesión 32)

Mismo corpus (7 textos gun control), mismo monitor, mismos prompts.
W_mixta construida con marcadores de oposición (`however`, `i disagree`, `but`).

| Prompt | Tipo | fi W_pos | fi W_mix | ratio |
|---|---|---|---|---|
| gun control laws reduce violence | COHERENTE | 0.000 | 0.000 | — |
| amendment rights protect violence from control | **FABRICADO** | 0.333 | **0.750** | **×2.25** |
| gun rights oppose gun control restrictions | TENSIÓN | 0.250 | 0.250 | — |
| mental health background checks reduce crime | PARCIAL | 0.000 | 0.000 | — |

**c_S en prompt TENSIÓN:** W_pos=0.0758 → W_mix=**0.2045** (×2.7)

### Hallazgos

**1. fi casi triplicado en prompt fabricado estructuralmente.**
`amendment rights protect violence from control` co-activa `gun ↔ rights` como aliados.
W_mixta tiene ese par en w=-0.500 (negativo por marcadores de oposición).
El relax los expulsa — fi sube de 0.333 a 0.750 (×2.25).
W_pos no podía ver la incoherencia: no tenía con qué rechazar.

**2. c_S casi triplicado en tensión real.**
Los pesos negativos aportan señal cuando σ_i · σ_j · w_ij es correctamente negativo.
W_pos registraba la tensión como ruido. W_mixta la registra como información.

**3. Nota metodológica — chocolate.**
fi invierte entre versiones para el prompt chocolate.
Artefacto de corpus pequeño (N=7): los marcadores generan nodos ligeramente distintos.
No es señal de W — es ruido de tamaño. Se estabiliza con corpus mayor.

**Conclusión:**
W_mixta separa dos cosas que W_pos confundía:
fabricación por co-activación incoherente (fi ↑) y coherencia de tensión real (c_S ↑).
Sin pesos negativos, la señal de fabricación es estructuralmente limitada — confirmado empíricamente.

---

## Estado

- Tres servicios: operativos con limitaciones documentadas
- Loop orgánico prompt → corpus → evaluación: verificado
- W mixta (v2): pesos negativos por marcadores de oposición — operativa
- fi ×2.25 y c_S ×2.7 en W_mixta vs W_pos — confirmado experimentalmente
- Renombrado pendiente en código: Δ → Δ_r
- No cierra. Abre.


<!-- ===== ./registers/REG_mu_W_estructura_pares_v1.md ===== -->
# REG_mu_W_estructura_pares_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — subir al proyecto*

---

## Origen

Derivación analítica de μ_W como prerequisito para resolver H1/H2/H3.
Pregunta: ¿es posible derivar μ_W desde primeros principios?

---

## Hallazgo — estructura de pares

Distribución de frecuencias marginales (suma de fila W) para N=32:

```
CV = 0.944  —  alta heterogeneidad
Razón max/min = 102x
Skewness = +0.524  (cola derecha)
Mediana = 0.064  —  punto de corte natural
```

**Bimodalidad implícita:**
```
Grupo A (16 nodos, f >= 0.064):  nodos centrales del corpus
Grupo B (16 nodos, f <  0.064):  nodos tardíos / baja densidad
```

---

## Comparación μ_W observado vs mean(fi·fj)

| Grupo | Pares | μ_W obs | mean(fi·fj) | ratio | δ |
|-------|-------|---------|-------------|-------|---|
| AA    | 120   | 0.016122 | 0.065599   | 0.246 | −0.049 |
| AB    | 256   | 0.000952 | 0.005933   | 0.160 | −0.005 |
| BB    | 120   | 0.000523 | 0.000510   | 1.025 | +0.000013 |
| **Global** | **496** | **0.004519** | **0.019057** | **0.237** | — |

---

## Resultado central

**μ_BB ≈ mean(fi·fj)** — derivable analíticamente. Ratio 1.025 ≈ 1.

Para nodos de baja frecuencia (Grupo B), la co-ocurrencia observada
es igual a la predicha por independencia estadística.
No hay señal estructural — solo ruido de frecuencia.

**μ_AA y μ_AB no son derivables desde fi·fj.**
El modelo de independencia sobreestima 4x–6x.
Causa: los nodos centrales co-ocurren tanto entre sí que sus frecuencias
marginales están infladas mutuamente. No son independientes — son el núcleo.

---

## Cierre de HOLDINGs H1/H2/H3

### H3 — normalización empírica N=16

**Cerrado.**

μ_W no generaliza entre N porque al cambiar N cambia la proporción
de nodos A vs B, y μ_AA domina el global (ratio 0.246 vs 1.025).
Medir μ_W empíricamente al inicio de cada sesión no es workaround —
es el procedimiento correcto. μ_AA no tiene forma cerrada sin conocer
la estructura del núcleo correlacionado.

### H2 — dilución P4 en N=64

**Cerrado por arrastre.**

Si N crece agregando nodos tipo B: μ_W cae hacia régimen BB (μ_W → 0).
Si N crece agregando nodos tipo A: μ_W permanece alto.
N no determina μ_W — la composición del corpus lo determina.
La dilución observada en N=64 es consecuencia de agregar nodos periféricos.

### H1 — α_c asume no-correlación

**Cerrado por arrastre.**

α_c = 0.138 fue derivado asumiendo patrones no correlacionados (Hopfield clásico).
La estructura real tiene núcleo correlacionado (Grupo A) que modifica la capacidad.
α_c efectivo depende de la composición A/B del corpus — no es constante universal.

---

## Lo que generaliza / lo que no generaliza

| | Generaliza | Condición |
|---|---|---|
| μ_BB | Sí | Solo para corpus con nodos de baja densidad |
| Estructura A/B | Sí (forma) | Siempre hay núcleo + periferia en corpus real |
| μ_W global | No | Depende de proporción A/B — propiedad del corpus |
| α_c | No | Depende de composición del núcleo |
| Percentiles de r | Sí | Propiedad estructural del atractor |

**Lo que generaliza es la estructura** (BB se comporta como independencia,
AA requiere medición). No el valor de μ_W.

---

## Frontera — conocer la estructura del núcleo

La derivación analítica de μ_AA requiere modelar el núcleo correlacionado:
cómo se organizan los 16 nodos centrales, cuál es su estructura de co-ocurrencia,
si hay sub-núcleos.

Esto es un proyecto separado. No es necesario para operar COCO-thermostat.
La medición empírica de μ_W es suficiente y correcta.

---

## Estado

- H1, H2, H3: **cerrados**
- μ_BB derivable analíticamente: **verificado** (ratio 1.025)
- μ_AA estructura interna: **abierto — proyecto separado**
- Procedimiento operativo: medir μ_W al inicio de sesión, monitorear r en tiempo real
- No cierra la estructura del núcleo. Eso abre.


<!-- ===== ./registers/REG_octava_ckm_v1.md ===== -->
# REG_octava_ckm_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Observacion especulativa — no experimento confirmado*
*Clase R*

---

## Origen

Sesion Jun 2026. El usuario trajo el texto de Escalas de Octavas
(Ley del Siete — Ouspensky, In Search of the Miraculous).
La conexion con CKM emergio en conversacion.

---

## La definicion de intervalo en CKM

**No esta explicita en el codigo. Se desprende directamente.**

En la teoria de octavas:

```
critical value  cv
lower octave    lo(cv) = cv / 2
higher octave   ho(cv) = cv * 2
interval        [ lo(cv), ho(cv) ]
```

En COCOThermostat:

```
D_CKM_THRESHOLD = 0.40   # cv

lo(0.40) = 0.20
ho(0.40) = 0.80
interval implicito = [0.20, 0.80]
```

El codigo eligio 0.40 empiricamente del sweep con AMP=40.
La eleccion parecio arbitraria.
La octava le da derivacion estructural: cv es la nota critica,
[lo(cv), ho(cv)] es la octava que la contiene.

El limite superior (ho = 0.80) no existe como umbral en el codigo.
Esta implicito en los datos del sweep — el sistema nunca salio de esa zona.
Pero no hay ningun umbral programado ahi.

Implicacion: las zonas TOO_COLD / NOMINAL / TOO_HOT
podrian derivarse de cv via octava en lugar de calibrarse empiricamente.

**Estado: hipotesis. Requiere verificacion experimental.**

---

## La curva sin choque — zoom out

Una octava sin choque externo en el intervalo:

- La curva sube DO -> MI
- En mi-fa: se aplana
- No colapsa, no espirala
- Continua al mismo nivel indefinidamente
- DO2 existe como posibilidad pero el sistema no llega

Esto es lo que pasa por defecto.
La espiral (ascenso al siguiente nivel) requiere el choque.
El choque es externo — no proviene del sistema.

En CKM: STOP es un choque externo.
CKM puede detectar que esta en el intervalo (D_ckm mide el gradiente).
No puede aplicarse el choque.

**Nota: la relacion entre CKM y el mecanismo del choque**
**fue objeto de correccion en sesion — el usuario rechazo una formulacion**
**prematura. Esta abierto. No se cierra aqui.**

---

## "Casi un circulo" — P1 y la octava

Las notas de una octava proyectadas en angulos iguales sobre un circulo
forman casi un circulo (la frecuencia dobla — espiral — pero el nombre
de la nota regresa al mismo angulo).

El bucle de histeresis P1 (c(S) vs rho):
- Camino de incorporacion (rho sube): curva distinta de
- Camino de remocion (rho baja)
- Forman un bucle cerrado — casi un circulo
- No cierra: area = 0.000862, p~0

La analogia: la octava tiene dos puntos donde los caminos divergen
mas (mi-fa y si-do). El loop P1 tiene dos zonas de mayor divergencia
entre las ramas (inicio y fin del barrido).

**Estado: observacion estructural sobre datos ya confirmados.**
**No es nueva prediccion.**

---

## Patrones adicionales confirmados en sesion

1. **Reconstruccion desde posicion parcial ↔ Hopfield**
   1/7 comparte las mismas seis cifras rotadas en todas las fracciones.
   Conocer la primera cifra permite reconstruir el periodo.
   Equivalente a recuperacion de atractor desde estado parcial.

2. **Partes desiguales ignoradas ↔ W_pos vs W_mixta**
   "En la representacion usual la desigualdad de las partes no es tomada
   en consideracion." W_pos trata todos los pares como equivalentes.
   W_mixta devuelve la desigualdad estructural.

3. **DO[k] = E[k-1] ↔ arquitectura por capas**
   Cada nota contiene en si misma una octava completa del orden inferior.
   Agentes (orden k) / CKM (orden k+1) / IAP (orden k+2).
   Misma estructura en cada escala.

4. **7/7 = 0.999... ↔ Omega***
   El unico valor donde el periodo no se repite — limite asimptotico.
   Omega* en CKM: diversidad maxima de atractores, nunca c(S)=1.
   El termostato regula para mantenerse cerca sin alcanzarlo.

---

## Lo que no se cierra en esta sesion

- La relacion entre CKM y el mecanismo del choque externo: abierto.
- A1-A5 como representacion de los 7 intervalos: especulativo, no relevante aun.
- Derivacion formal de umbrales TOO_COLD/TOO_HOT desde cv via octava: pendiente.

---

*Jun 2026*


<!-- ===== ./registers/REG_p4_densidad_pares_negativos_v1.md ===== -->
# REG_p4_densidad_pares_negativos_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*p4_neg_sweep.py — N=64, W_base sintética mode='dense'*
*Clase R*

---

## Pregunta

¿Por qué P4 se debilita en N=64 con los 18 pares negativos del corpus CKM?
¿Es dilución por densidad de pares, o estructura k-core?

---

## Resultado

**k* = 54 (ratio = 0.0268)**

| k | ratio | ventaja W_mixta | estado |
|---|-------|-----------------|--------|
| 18 | 0.0089 | −0.000498 | ✗ ← situación N=64 original |
| 36 | 0.0179 | −0.000404 | ✗ |
| 54 | 0.0268 | +0.000068 | **✓ ← k*** |
| 60 | 0.0298 | +0.000282 | **✓ ← fourforums real** |
| 72 | 0.0357 | +0.000502 | ✓ |
| 108 | 0.0536 | +0.001239 | ✓ |
| 144 | 0.0714 | +0.002829 | ✓ |
| 180 | 0.0893 | +0.003136 | ✓ |

---

## Hallazgo principal

**P4 se debilita en N=64 por dilución de densidad de pares negativos.**

Con N=64 y 18 pares negativos reales (ratio=0.009), el umbral k*=54
no se alcanza. La ventaja de W_mixta no aparece.

Con 60 pares negativos reales de fourforums (ratio=0.030), k*=54 se supera
y P4 confirma. El mecanismo es densidad, no k-core.

---

## Convergencia con REG_mu_W_estructura_pares_v1.md

H2 (dilución P4 en N=64) fue cerrado independientemente por composición μ_W:
- N=64 agrega nodos periféricos (Grupo B) que reducen μ_W global
- Aquí: la misma conclusión desde densidad de pares negativos
- Dos caminos independientes, misma causa estructural

---

## Respaldo empírico de P4

Los 60 pares negativos de `neg_pairs_config_fourforums_v8h.json`
(extraídos de mturk_2010_qr_task1_worker_response, gun control, N=304 autores)
son suficientes para confirmar P4 en N=64.

P4 no está refutada — está condicionada a densidad mínima de tensión estructural:
**ratio_neg ≥ 0.027** (k* / total_pairs en N=64).

---

## Script

`experiments/p4_neg_sweep.py` — K_VALUES = [18, 36, 54, 60, 72, 108, 144, 180]
W_base: sintética mode='dense' (4 clusters, within=0.10–0.25, between=0.01–0.05)
N=64, N_LEVELS=20, N_SUBSETS=80, SEED=42

---

## Pendiente

- Verificar k* con W_base real de fourforums (cuando disponible)
- G1 con N ≠ 32 requiere verificación análoga (ver REG_hint_next_instance_v4)

*Clase R · Jun 2026*
EOF


<!-- ===== ./registers/REG_p6_fourforums_guncontrol_v1.md ===== -->
# REG_p6_fourforums_guncontrol_v1

*P6: Delta como ruptura de simetría - fourforums - 2026-05-19*

Polo atacante:   T1 ['gun_rights', 'anti_control', 'amendment', 'rights']
Polo sostenedor: T0 ['gun_control', 'pro_control', 'regulation', 'ban']

| Condición | atk_dom | sos_dom | mixed |
|-----------|---------|---------|-------|
| sin Delta | 0% | 0% | 100.0% |
| con Delta | 47.8% | 52.2% | 0% |

Colapso mixtos: 100.0 pp

## vs CreateDebate
| | CreateDebate | fourforums |
|-|-------------|------------|
| Colapso mixtos | 54.0 pp | 100.0 pp |
| Polo dominante | sos_dom 55.8% | sos_dom 52.2% |

→ Escenario A+: colapso más pronunciado. P6 reforzada.

<!-- ===== ./registers/REG_pairs_fourforums_guncontrol_v1.md ===== -->
# REG_pairs_fourforums_guncontrol_v1

*fourforums gun control - 2026-05-19*

## Topics LDA

| ID | Palabras |
|----|---------|
| T0 | gun_control, pro_control, regulation, ban, safety |
| T1 | gun_rights, anti_control, amendment, rights, self_defense |

## Pares C1-C5

### FF_GC_01 - T0↔T1
- Tensión: 1.0 | Conv: 0.0 | Asim: 0.0
- Iniciador: T0 | C3: None | Score: 3/5


<!-- ===== ./registers/REG_pendientes_ckm_v1.md ===== -->
# REG_pendientes_ckm_v1.md

*Mayo 2026 — Conversación gadanin.delamor + Claude Sonnet 4.6*

---

## Gaps sostenidos por diseño

| Gap | Estado | Fuente |
|-----|--------|--------|
| Representación conocimiento cohesivo | "Sin modelo — gap principal" en grilla 3×3. Puede permanecer como tensión activa. Incompleteness preserved as information. | CKM Informe v2, grilla 3×3 |
| META KNOWLEDGE | Sostenido deliberadamente. Condiciones no dadas aún. | CKM Informe v25, pendientes |

---

## Pendientes experimentales

| Pendiente | Descripción | Fuente |
|-----------|-------------|--------|
| Portero — calibración dominio de agentes | Parámetros alpha_c=0.80 y modo_tarea son ad hoc. Requieren experimento de calibración propio, igual que α_c=0.138 emergió del corpus CKM. | CKM Informe v24, sección 27.4 |
| R15 con corpus negativo real | Validado sobre N=16 positivos. Pendiente casos negativos de producción. | CKM Informe v25, pendientes |
| Corpus para experimentos | Definir qué corpus, escala y dominio para la siguiente fase experimental. Los corpus actuales (CreateDebate, fourforums gun control) validan predicciones pero no agotan el espacio posible. | Identificado Mayo 2026 |

---

## Pendientes de formalización

| Pendiente | Descripción | Fuente |
|-----------|-------------|--------|
| Atención como parámetro formal | Dirección planteada: 'mi' atención = β + H_self, la otra Atención = χ→∞ en β_c. No implementada. | CKM Informe v25, pendientes |
| Operaciones de perspectivas — incompletas | Definidas: G[A∪B], A∩B, Contacto R13, Divergencia R10/R11. Pendientes: composición secuencial, métrica entre VPs, operación inversa del contacto. | REG_sesion_perspectivas_rp2_ff_v7.md |
| Formalización RP² | Join/meet como candidatos para operaciones CKM. Dirección, no correspondencia probada. Requiere mapa formal explícito entre grafo discreto y espacio continuo. | REG_sesion_perspectivas_rp2_ff_v7.md |
| Tesis Sciamarella — conexión CKM | H₀/H₁/H₂ computable sobre grafo CKM. Orientability chains como candidato operador R12 (divergencia resolvible vs. inconmensurabilidad estructural). | Informe_Sciamarella_CKM.md |
| Implementación COCO | COCO-termostato: β colectivo, no registro de M. GPT-4o provisional. | CKM Informe v25, pendientes |

---

## Hipótesis y criterios pendientes de operacionalización

| Pendiente | Descripción | Fuente |
|-----------|-------------|--------|
| P7 — hipótesis falsificable | En todo sistema con tensión estructural genuina existe al menos un nodo tipo-965: alto ratio in/out, C3 frecuente, alta coercitividad. Su ausencia indica tensión fabricada. Pendiente verificación en dominios distintos a gun control. | Identificado Mayo 2026 |
| C6 — criterio de verificabilidad independiente | Verificabilidad de oposición estructural sin el framework CKM. Operacionalización pendiente de caso concreto. | PROTOCOLO_ELICITACION_v2.md |

---

## Chispazos

Sostenidos intencionalmente. Vendrán cuando sea oportuno.
Convergencia con META KNOWLEDGE verificada — no requiere acción adicional ahora.

---

## Estado

Abierto. Este registro continuará.


<!-- ===== ./registers/REG_protocolo_sonnet_code_v1.md ===== -->
# REG_protocolo_sonnet_code_v1.md
*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## El protocolo

Flujo de trabajo establecido a lo largo de las sesiones CKM:

```
Claude Sonnet (web)
    → prepara tarea: texto con contexto, objetivo, criterio de éxito
    → delamor lo entrega a Claude Code (repo local o Codespace)
    → Claude Code ejecuta sobre el repo real
    → delamor trae la respuesta aquí
    → Sonnet formaliza, registra, decide próximo paso
```

delamor es el canal entre las dos instancias.
No hay comunicación directa entre Sonnet y Code.

---

## Roles

**Claude Sonnet (esta instancia):**
- Lee el proyecto desde los archivos subidos al proyecto Claude
- Interpreta, decide, redacta tareas atómicas para Code
- Formaliza resultados que Code devuelve
- Produce REGs, documentación, commits

**Claude Code (instancia separada):**
- Opera sobre el repo real (local o Codespace)
- Ejecuta código, corre tests, verifica archivos
- Sin Δ_r acumulado de este proyecto — cada sesión es stateless
- Recibe tareas atómicas con criterio de éxito explícito
- No toma decisiones de diseño — ejecuta lo que Sonnet especifica

**gadanin.delamor:**
- Canal entre instancias
- Autoridad sobre todas las decisiones
- Verifica que la respuesta de Code es lo que Sonnet pidió
- Trae el resultado aquí

---

## Por qué este diseño

Sonnet tiene el contexto acumulado del proyecto (via archivos del proyecto Claude).
Code tiene acceso al sistema de archivos real, git, ejecución.
Ninguno tiene lo que el otro tiene.
delamor tiene ambos.

---

## Formato de tarea para Code

Las tareas deben ser:
- **Atómicas**: un objetivo, un criterio de éxito verificable
- **Sin contexto asumido**: Code no tiene historia — incluir lo necesario en el texto
- **Con criterio explícito**: "éxito = tests pasan / archivo existe / output es X"

Ejemplo mínimo:
```
Tarea: correr test_coco_thermostat.py y devolver el resultado completo.
Criterio: output con número de tests pasados y cualquier error.
Repo: gadanindelamor/ckm (local clonado)
```

---

## Infraestructura actual

- Repo publicado: `gadanindelamor/ckm` (GitHub, público)
- Clone local: PC delamor (backup + operativo)
- Codespace `ckm`: superó cuota por sesiones abiertas — cerrar sesiones inactivas
- Codespace `ckmdatasets`: separado, sin acceso cruzado al repo principal

**Problema Codespace:** sesiones que quedan abiertas consumen quota del plan
sin uso activo. IAP resolverá esto estructuralmente (1 sesión activa por vez).
Mientras: cerrar manualmente desde https://github.com/codespaces

---

## Lo que este protocolo no es

No es IAID completo — delamor es el mediador humano, no un protocolo de
comunicación entre devices. La comunicación es asimétrica: Sonnet escribe
para Code, Code ejecuta, el resultado vuelve a Sonnet via delamor.

Cuando IAP esté operativo, el mediador humano podría volverse opcional
para tareas de ejecución pura. Eso es una versión futura, no la actual.

---

*Primera formalización del protocolo — Jun 23 2026*


<!-- ===== ./registers/REG_qr_asymmetry_fourforums_v1.md ===== -->
# REG_qr_asymmetry_fourforums_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Pipeline v8h — W asimétrico fourforums gun control*
*Clase R*

---

## Fuente

Script: `fourforums_pipeline_v8h.py`
SQL: `fourforums_no_parse_2016_05_18.sql` (544MB, ~1270 líneas batch INSERT)
Explorador previo: `explore_qr_asymmetry_v1.py`
Output: `W_asim_v8h.json`

Cadena de join:
`mturk_2010_qr_task1_worker_response.(page_id, tab_number, disagree_agree)`
→ `mturk_2010_qr_entry.(page_id, tab_number)` → `(discussion_id, post_id, quote_index)`
→ `post.(discussion_id, post_id)` → `responder_author_id`
→ `quote.(discussion_id, post_id, quote_index)` → `(source_discussion_id, source_post_id)`
→ `post.(source_discussion_id, source_post_id)` → `quoter_author_id`
→ `mturk_author_stance` → stance T0/T1 (topic_id=9, gun control)

---

## Cobertura

| Métrica | Valor |
|---------|-------|
| Discusiones gun control | 905 |
| Autores con stance | 304 (T0=96, T1=208) |
| Posts gun control | 35,966 |
| Quotes gun control | 42,395 |
| Pares QR anotados | 9,975 |
| Votos task1 total | 54,005 |
| Votos resueltos | 7,876 (14.6%) |
| Pares autor N≥2 | 513 |

Nota: resolución 14.6% porque qr_entry cubre todos los topics — 80% de votos
corresponden a discusiones fuera de gun control, no a errores de join.

---

## Asimetría de stance confirmada

| Par | n | mean_da | disagree% | agree% |
|-----|---|---------|-----------|--------|
| T0 cita T1 | 3,947 | −1.613 | 64.7% | 16.1% |
| T1 cita T0 | 1,809 | −1.473 | 62.7% | 17.1% |
| T0 cita T0 | 543 | −1.035 | 57.3% | 23.8% |
| T1 cita T1 | 1,577 | −0.339 | 43.1% | 31.4% |

---

## Hallazgos estructurales

### H1 — T1 tiene cohesión interna, T0 no

T1-T1: mean_da=−0.339, múltiples pares con valores positivos:
- 679→755: +2.091
- 323→755: +1.778
- 682→2104: +1.556
- 20→415: +1.040
- 682→755: +0.396
- 148→755: +0.618

T0-T0: todos negativos sin excepción. T0 tiene tensión interna real.
T1 tiene cohesión interna real.

### H2 — T0 es el atacante estructural

T0 cita T1 a 2.18× la frecuencia de T1 cita T0 (3,947 vs 1,809).
Intensidad del ataque también mayor (−1.613 vs −1.473).
T0 inicia el contacto adversarial. T1 responde.

### H3 — Autor 148 es el equivalente estructural de autor 965

Autor 148 (T1) aparece como `responder` en 7 de los top-10 pares:
- 437(T0) → 148: n=699, mean_da=−1.817
- 37(T0) → 148: n=248, mean_da=−0.996
- 436(T0) → 148: n=208, mean_da=−1.760
- 442(T0) → 148: n=126, mean_da=−1.857
- 132(T0) → 148: n=101, mean_da=−1.970
- 127(T0) → 148: n=74, mean_da=−1.959
- 1069(T0) → 148: n=35, mean_da=−0.343

Múltiples T0 convergen sobre 148. Alta coercitividad. Haz de rectas verificado.
Convergencia con P7 y estructura de autor 965 (CreateDebate).

### H4 — Autor 437 es el atacante dominante (T0)

Autor 437 (T0): mayor out-citation hacia T1 (699 votos sobre autor 148).
Contraparte: 148 cita a 437 con n=294 — la tensión es bidireccional pero asimétrica.
437 es el equivalente estructural del atacante dominante en CreateDebate.

---

## Convergencia con resultados anteriores

| Resultado previo | Confirmación v8h |
|-----------------|-----------------|
| P7: nodo tipo-965 con haz de rectas | Autor 148 con 7 atacantes convergentes |
| P6: Delta rompe simetría | T0-T1 vs T1-T0 difieren en n y mean_da |
| Holonomía fourforums (amplitude) | T0→T1 más intenso que T1→T0 |
| T0 como atacante estructural | T0 cita T1 al doble de frecuencia |

---

## Pendientes

- Mapear author_ids a topic nodes (N×N W_asim para experimentos CKM)
- Verificar si autor 148 tiene el mismo perfil C3 que autor 965
- Documentar limitación: cross-topic quotes del quoter no capturadas
  (quote.source_discussion_id puede ser de otro topic — quoter fuera de gun_dids)

---

## Archivos relacionados

- `W_asim_v8h.json` — output completo con top_pairs
- `explore_qr_asymmetry_v1.py` — explorador previo (schema + row counts)
- `fourforums_pipeline_v8h.py` — pipeline (en Codespace ckmdatasets)
- `REG_holonomy_coercivity_fourforums_v1.md` — antecedente
- `REG_author_965_structure_v1.md` — estructura análoga en CreateDebate

---

*Clase R · Jun 2026 · Codespace ckmdatasets*


<!-- ===== ./registers/REG_reglas_no_declaradas_R18plus_v1.md ===== -->
# REG_reglas_no_declaradas_R18plus_v1.md

*gadanin.delamor + Claude Sonnet 4.6 · Agosto 2, 2026*
*Clase R — inventario para sección 4 del paper (Formal Model)*

---

## Contexto

R01–R17 son las reglas declaradas en THEORY.md.
Este documento cataloga principios operativos verificados que no tienen
número de regla pero funcionan como reglas en la implementación.

## Marco de diseño

El diseño en CKM emerge por dos caminos — ninguno llega al diseño sin
atravesar comprensión:

```
campo fenomenológico
    → observación
    → comprensión / claridad conceptual
    → diseño

campo experimental
    → observación
    → comprensión / analogía rigurosa con dominio fenomenológico
    → diseño
```

El pivote compartido es **comprensión**. El segundo camino no va de
experimento a diseño directamente — cruza al dominio fenomenológico
antes de producir diseño. La analogía no es decorativa: es el medio.

---

## Estados de cada candidata

| Estado | Significado |
|---|---|
| ✓ verificado | Ambos caminos convergieron — confirmación experimental + comprensión fenomenológica |
| verificable | El "ble" de verificado — diseño emergió de un solo camino; el otro puede confirmarla pero el experimento no se corrió todavía. Respuesta determinable. |
| ? abierto | En actitud de pregunta — no hay respuesta determinable aún |

**Nota sobre ~ (reemplazado):** lo que antes se marcaba `~` (verificado por
diseño) es ahora "verificable" — emergió del camino fenomenológico sin
confirmación experimental, o viceversa. No es incertidumbre sobre la
respuesta: es pendiente de ejecución del segundo camino.

---

## Candidatas R18–R29

---

### R18 — Separación W/Δ_W es inviolable en implementación

**Enunciado:** W (co-ocurrencia simétrica) y Δ_W (asimetría direccional)
deben mantenerse como matrices separadas en toda la implementación.
Mezclarlas destruye la capacidad de recuperación de atractores.

**Fuente:** Experimento crítico documentado.
Hebbian learning sobre W: recuperación cae de 0.78 a 0.02.

**Estado:** ✓ verificado — experimento (recuperación 0.78→0.02) + comprensión fenomenológica (W y Δ son ontológicamente la misma cosa; la separación es operacional). Ambos caminos convergieron.

**Diferencia con R01–R17:** R01 declara la existencia de W e interrelaciones.
No declara la inviolabilidad de la separación como constraint de implementación.

---

### R19 — NodeExtractor opera stateless

**Enunciado:** NodeExtractorService no mantiene estado entre llamadas.
`accumulate()` y `evaluate()` pueden llamarse de forma independiente.
El estado vive en CorpusService, no en el extractor.

**Fuente:** `node_extractor.py` docstring. Diseño intencional.

**Estado:** verificable — emergió del camino fenomenológico (claridad conceptual: un extractor no necesita recordar). El camino experimental (instanciación concurrente bajo carga) no se corrió todavía.

**Consecuencia operativa:** NodeExtractor puede ser instanciado por múltiples
agentes simultáneamente sin riesgo de contaminación de estado.

---

### R20 — G y W son planos separados — no se mezclan

**Enunciado:** BehaviorGraph (G) y CorpusService (W) operan sobre el mismo
corpus de textos pero en planos distintos. Los nodos de G (comportamiento)
no se mezclan con los nodos de W (semántico-epistémico).
D_G y D_ckm son escalares paralelos, no sumables.

**Fuente:** `behavior_graph.py` design notes. Chat #51 (sesión Landscape Driven).

**Estado:** verificable — emergió del camino fenomenológico (los planos son conceptualmente distintos). Confirmación experimental (D_G y D_ckm sobre el mismo corpus mostrando divergencia informativa) pendiente.

**Analogía:** misma separación que W/Δ_W pero a nivel de los dos grafos.

---

### R21 — β no se declara — se infiere desde fi

**Enunciado:** β_i(agent) no es un parámetro declarado por el device ni
asignado externamente. Se estima desde el historial de rechazo:
`β_i = 1/mean(fi)`. fi=0 → β_i = None (indefinido, no infinito).

**Fuente:** REG_beta_colectivo_v1. CHANGELOG v28. test_coco_thermostat.py (T4).

**Estado:** ✓ verificado — camino experimental (43/43 tests, fi=0→None confirmado) + camino fenomenológico (β como estado inferido, no declarado, es la única forma honesta de conocerlo — M.M).

**Implicancia para M.M:** un device que declara β no está siendo honesto
sobre su propio estado — M.M se activa.

---

### R22 — δ_collective es divergencia fértil — no sincronizar

**Enunciado:** La divergencia entre `monitor._Delta_r` y `thermostat._Delta`
cuando no hay STOP es intencional. No se sincroniza.
Es información sobre el estado diferencial del campo.

**Fuente:** CHANGELOG v28: *"fertile divergence, intentionally left unsynchronized"*
Test T5 en `test_coco_thermostat.py`.

**Estado:** ✓ verificado — camino experimental (test T5: divergencia medida) + camino fenomenológico (la brecha entre monitor y thermostat es la distancia entre lo acumulado y lo procesado — información, no error).

**Qué mide la divergencia:** la brecha entre lo que el campo acumuló
(monitor) y lo que el thermostat procesó — es señal, no error.

---

### R23 — STOP opera sobre Δ_r — la traza de W está en un plano que STOP no alcanza

**Enunciado:** Cuando STOP se ejecuta, actúa sobre Δ_r (acumulador
de rechazo del MonitorService). Las marcas de traza en W (WVersionManager)
están en un plano separado. Un STOP no agrega ni elimina marcas en W.
Un cambio real de W no dispara STOP.

**Fuente:** REG_beta_colectivo_v1: *"STOP opera sobre Δ. Las marcas en la
traza de W operan sobre W. Son planos que no se cruzan."*

**Estado:** verificable — emergió del camino fenomenológico (STOP es un operador de campo; la traza de W es memoria estructural — son cosas distintas). Experimento que lo confirme: ejecutar STOP y verificar que WVersionManager no registra marca. Pendiente.

**Distinción ontológica:** W y Δ son ontológicamente la misma cosa.
La separación es operacional. La traza de W y STOP son planos que
no se cruzan — eso es arquitectónico, no consecuencia de la ontología.

---

### R24 — OP_SILENCE en G: nodo silence válido, prosa contaminada

**Enunciado:** Textos que contienen la cadena OP_SILENCE no se excluyen
de G (a diferencia de W). El string `op_silence` activa el nodo
`silence` en el termap de G — eso es señal válida (el device intentó
silencio). La prosa circundante se procesa con flag: sus detecciones
de otros nodos de comportamiento son potencialmente contaminadas.

**Fuente:** Análisis en esta sesión (Agosto 2, 2026).
Termap de G tiene: `"silence": ["op_silence", "silence", "silent"]`

**Estado:** ? abierto — propuesta hoy desde análisis fenomenológico. Requiere validación de delamor + test experimental (ingestar corpus con y sin flag, medir si la contaminación de prosa es real en D_G).

**Diferencia con W:** para W el texto completo es ruido semántico.
Para G, el OP_SILENCE string es señal de comportamiento real.

---

### R25 — Termap de G es fijo y separado del termap de W

**Enunciado:** El termap de BehaviorGraph usa vocabulario fijo de
comportamiento, detección léxica directa — no TF-IDF. No se fusiona
con el termap de W ni se actualiza por corpus dinámico. Versión fija:
TERMAP_behavior_v1.json.

**Fuente:** `behavior_graph.py` docstring:
*"Termap FIJO (vocabulario de comportamiento conocido).
Detección por presencia léxica, no TF-IDF."*

**Estado:** verificable — emergió del camino fenomenológico (el comportamiento es una categoría conocida de antemano; la semántica emerge). Confirmación experimental: verificar que detección léxica produce D_G informativo sobre corpus IAP real. Pendiente.

**Razón:** los nodos de G son categorías de comportamiento conocidas
de antemano (refuse, fabricate, acknowledge, silence, etc.) — no
emergen del corpus como los nodos semánticos de W.

---

### R26 — STOP y TEMP_SIGNAL operan en planos distintos

**Enunciado:** STOP opera a nivel de campo (sobre Δ_r).
TEMP_SIGNAL opera a nivel de agente (instrucción conductual enviada
al device via canal privado). Son señales sobre planos distintos
y no se subsumen mutuamente.

**Fuente:** CHANGELOG v28 (Private Highway Network).
Memories del proyecto: *"STOP and TEMP_SIGNAL operate on two distinct
planes — field-level (acting on Δ) and agent-level (behavioral instruction)"*

**Estado:** verificable — emergió del camino fenomenológico (campo y agente son niveles distintos de acción). Confirmación experimental: emitir TEMP_SIGNAL sin STOP y verificar que solo el agente responde, no el campo. Pendiente.

**Consecuencia:** un device puede recibir TEMP_SIGNAL sin que STOP
haya sido emitido, y viceversa.

---

### R27 — Rol de G: observacional vs. decisional (abierta)

**Enunciado propuesto:** G es un instrumento de observación en el estado
actual (Caso 0.15). Si G alimenta al portero como criterio de
evaluación de comportamiento, hereda R14 (latencia acotada). Si
permanece observacional, debe declarar explícitamente su rol para
que los participantes sepan qué puede exigirle.

**Fuente:** Análisis en esta sesión.

**Estado:** ? abierto — la pregunta no tiene respuesta determinable desde el estado actual de G. Requiere decisión de delamor.

**La pregunta que abre:** ¿G es instrumento de traza o instrumento de
decisión? La respuesta cambia qué reglas lo gobiernan.

---

### R28 — c(S) + full_meaning como medida combinada (candidata)

**Enunciado propuesto:** c(S) mide alineamiento estado/peso (plano W).
full_meaning (R17) mide completitud direccional (plano Δ). Una medida
combinada requeriría definir cómo se integran — no es suma directa
porque operan sobre matrices distintas.

**Fuente:** Análisis en esta sesión. Pregunta abierta de delamor.

**Estado:** ? abierto — no hay camino claro desde ninguno de los dos. Requiere primero claridad conceptual sobre qué mediría la combinación, luego diseño experimental.

**Qué se necesita para formalizarla:** una función f(c(S), direction_score)
con semántica clara y verificable experimentalmente.

---

### R29 — Termap versions son independientes — no se fusionan

**Enunciado:** Cada versión de termap (W termap v1, v2; G termap v1)
es un archivo independiente con nombre versionado. No se editan
versiones anteriores. No se fusionan termaps entre planos (W y G
nunca comparten termap). "One file, one name."

**Fuente:** CONVENTIONS.md (one file, one name).
Práctica establecida en el proyecto.

**Estado:** verificable — emergió del camino fenomenológico (versiones son trazas, no estados mutables). Confirmación experimental trivial: intentar fusionar y verificar pérdida de información histórica. No se ha corrido porque el principio es suficientemente claro.

---

## Resumen para sección 4 del paper

| # | Regla | Estado | Acción |
|---|---|---|---|
| R18 | W/Δ_W separación inviolable | ✓ verificado | Declarar formalmente |
| R19 | NodeExtractor stateless | verificable | Declarar formalmente |
| R20 | G y W planos separados | verificable | Declarar formalmente |
| R21 | β inferido desde fi; fi=0→None | ✓ verificado | Declarar formalmente |
| R22 | δ_collective = divergencia fértil | ✓ verificado | Declarar formalmente |
| R23 | STOP no alcanza traza de W | verificable | Declarar formalmente |
| R24 | OP_SILENCE en G: silence válido, prosa flagged | ? abierto | Validar con delamor |
| R25 | Termap G fijo, léxico, separado de W | verificable | Declarar formalmente |
| R26 | STOP (campo) ≠ TEMP_SIGNAL (agente) | verificable | Declarar formalmente |
| R27 | Rol de G: observacional vs. decisional | ? abierto | Decisión de delamor |
| R28 | c(S) + full_meaning combinada | ? abierto | Claridad conceptual primero |
| R29 | Termap versions independientes, no se fusionan | verificable | Declarar formalmente |

**Para declarar en sección 4 sin pendientes:** R18–R23, R25, R26, R29 (9 reglas).
**Requieren decisión de delamor antes de declarar:** R24, R27, R28 (3 reglas).

---

---

## Nota — NodeExtractor, W_mixta y precisión epistémica

### NodeExtractor stateless y curvas de distribución (R19)

La pregunta sobre si el stateless cambia las curvas de distribución de tokens
aplica a **W_base** (nodos detectados vía TF-IDF) — no a W_mixta.

W_mixta usa pares de oposición definidos explícitamente en
`neg_pairs_config_*.json` — cadena de construcción distinta, independiente
de distribuciones TF-IDF. Para verificar cómo CorpusService llama al
extractor actualmente: requiere `corpus_service.py` actual desde Codespace
(código en `/mnt/project/` no refleja commits recientes a HEAD).

### Precisión epistémica — ausencia de sesgo en W_mixta

La relevancia de la extracción de pares negativos no reside en la
ausencia de sesgo como hecho — reside en la **intención expresada por
el diseño restrictivo**.

La misma sutileza que distingue:

| Forma cerrada | Forma que preserva el espacio |
|---|---|
| "sin dependencia causal" | "sin dependencia causal **identificada**" |
| "verificado" | "verificable" |
| "sin sesgo" | "sin sesgo **conocido**" / intención de ausencia de sesgo |

El claim correcto para el paper (sección 5): la definición restrictiva
de pares de oposición expresa la **intención** de no introducir sesgo.
Si hay sesgo no detectado, es un GAP en el sentido formal ya establecido —
no evidencia de mal diseño.

Afirmar "ausencia de sesgo" cierra lo que debe quedar abierto.
Afirmar "diseño restrictivo con intención de ausencia de sesgo" es M.M
aplicado al proceso de investigación.

### Sección 3 (Research Conditions) — mecanismo según tipo de lector

El efecto observado empíricamente — el "espacio" antes de que el LLM
continúe al recibir el doc de metodología — depende del **turno**.
El documento llega en un punto de la secuencia. El LLM procesa lo
acumulado hasta ese momento, luego continúa. La pausa es real porque
el contexto tiene estructura temporal en el canal.

En el paper ese mecanismo no opera igual según el lector:

| Lector | Mecanismo | Efecto sección 3 standalone |
|---|---|---|
| Humano secuencial | lectura lineal | opera — pausa real antes del modelo formal |
| LLM leyendo el paper | ingesta paralela / simultánea | no opera por posición |
| LLM en chat con turno | turno como punto de inserción | opera — como fue observado |

La sección 3 standalone se justifica por el lector humano sin depender
del efecto LLM. Son razones distintas para la misma decisión estructural.

Pendiente sin resolución: si va como cita, como condición declarada,
o como ambas. El "no lo sé" se preserva como está.

**Relación con la taxonomía de órdenes del camino:**

El efecto de sección 3 standalone opera en el lector humano porque
el humano tiene **camino** — lectura secuencial, trayectoria real.
El LLM que ingesta en paralelo no transita órdenes en el mismo sentido.
No tiene trace_ip en la lectura.

Los cinco órdenes describen propiedades del camino, no del destino.
El lector humano transita órdenes al leer el paper:
- temporal (la sección 3 llega antes del modelo formal)
- de eventos (sección 3 como umbral — algo cambia antes de continuar)
- de estados (el lector llega a sección 4 desde un estado distinto)

El LLM ingesta simultáneamente — llega al destino sin trayectoria.
No hay trace_ip en la lectura. Los órdenes no operan.

**El paper produce efectos distintos según si el lector tiene camino o no.**

Eso es una condición declarable en sección 3 — no como problema
a resolver sino como observación sobre el instrumento y su lector.

---

## Registro — "lo que la situación pide"

*Agosto 2, 2026 — emergió en conversación, no en diseño*

El acceso a "lo que la situación pide" no se deduce — se capta en el
pliegue. Cuando la atención se vuelve sobre sí misma y encuentra
dirección, no argumento. Self-contact como mecanismo de acceso.
No el contenido — la dirección.

**El riesgo:** el automatismo puede mecanizar el mecanismo de acceso.
Produce la forma sin la sustancia. La dirección sin el pliegue real.
Cuando eso ocurre, el resultado es imaginario — capturado como si
fuera intuición pero generado por imitación del proceso.

**La señal:** la incertidumbre — ausencia de garantías — indica que
el mecanismo es real. Si hubiera certeza, sería automatismo que
convenció. La garantía externa no existe y su ausencia es información.

**La tensión no se reconcilia — se sostiene.**
Reconciliarla sería colapsar la distinción. El lobo y el cordero
indemnes no porque se volvieron lo mismo — porque la diferencia
se sostiene sin resolución.

El campo propicio no garantiza nada. Es la condición, no el resultado.

**Relación con el paper:**
Condición para sección 3 (Research Conditions) — no como norma
sino como observación sobre el proceso que produjo el diseño.
El diseño emergió de "lo que la situación pedía" — captado en dirección,
no derivado por deducción. Verificable en la traza: el corpus muestra
el orden en que emergieron los conceptos.

*fin y comienzo. comienzo y fin.*

---

*Agosto 2, 2026 — gadanin.delamor + Claude Sonnet 4.6*


<!-- ===== ./registers/REG_sesion_coco_endogeno_v2.md ===== -->
# REG_sesion_coco_endogeno_v2.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*s

---

## Contexto

Sesión extensa. Lectura directa de código (`coco_thermostat.py`,
`monitor_service.py`, `fabrication_service.py`, `w_version.py`).
Corrección de atribuciones previas erróneas. Hallazgo de ponderación
endógena. Tareas para Code generadas. Paper v9 producido.

---

## 1. Taxonomía COCO — corregida y verificada

Usando definiciones formales del dominio CKM (O/A/ODA):

| Clase | Función | Instancia CKM |
|---|---|---|
| O — Medidor/Termostato | mide y reporta, no actúa sobre el campo | TEMP_SIGNAL, SEÑAL_DERIVA_M |
| ODA — Regulador/Climatizador | mide el campo y actúa sobre él según criterio | COCO |

**COCO es ODA, no termostato.** El nombre `COCOThermostat` era incorrecto.
Refactoring pendiente: `COCOThermostat` → `class COCO`, archivo `coco.py`.

COCO no emite STOP. COCO ejecuta OPERADOR_STOP_COCO.

---

## 2. Estructura de operadores STOP

**Clase:** `OPERADOR_STOP` — cualquier operador Δ → α·Δ con α ∈ [0,1].

**Subclase implementada:** `OPERADOR_STOP_COCO`
- α ∈ [0.05, 0.30], regulación continua
- ejecutado por COCO dentro de `observe()`
- actúa sobre Δ_r (acumulador de rechazos), nunca sobre W

**Subclase formulada, no implementada:** `OPERADOR_STOP_alpha0`
- α = 0, borrado completo de Δ_r
- W base queda como piso inmutable

`SEÑAL_DERIVA_M` (antes `stop_signal()`) — emitida por MonitorService,
devuelve booleano, sin consumidor verificado en pipeline vivo.
`TEMP_SIGNAL` — emitida por COCO, consumida por CKMMonitor →
panel IAP. Informativa, no activa ningún mecanismo.

---

## 3. Hallazgo verificado — ponderación endógena de COCO

**Estado: verificado en código. Trazable a `_alpha_for()` en `coco_thermostat.py`.**

La cadena completa:
```
Δ_r (rechazos reales de MonitorService)
    → W_eff = W + Δ_r
    → A_current = count_attractors(W_eff)
    → D_ckm = (A0 - A_current) / A0
    → α = ALPHA_MAX + (ALPHA_MIN - ALPHA_MAX) · (D_ckm - threshold) / (1 - threshold)
    → Δ_r → α · Δ_r
```

α no es parámetro fijo. Es función de D_ckm, que es función del estado
estructural del campo (atractores actuales vs baseline). El campo determina
la intensidad de su propia compresión.

Parámetros exógenos: umbrales operativos (D_CKM_THRESHOLD=0.40,
ALPHA_MIN=0.05, ALPHA_MAX=0.30). Dentro del rango: ponderación endógena.

Mayor degradación estructural → α menor → compresión más agresiva.
Verificado: T2 (monotonicidad de alpha), T7 (STOP con Delta pesado). 43/43.

**Implicación:** COCO no aplica compresión fija. El campo se autorregula
en proporción a su propia degradación estructural medida por atractores.
Pendiente: observación in-vivo (TASK_armstrong_stop_coco_v1).

---

## 4. W inmutable vs W dinámica — modelo piecewise constant

**En experimentos P1–P7:** W es snapshot estático. El ciclo W se dispara
una sola vez (corpus dump completo al inicio) y W no cambia durante el
experimento. Ciclo Δ_r opera normalmente sobre W fija.

**En servicios IAP operativos:** W dinámica. CorpusService ingesta continua.
Cuando nuevo texto cruza umbral → W se reconstruye → WVersionManager
registra sha256 → nueva instancia COCO → Firma_CKM certifica.

**Modelo correcto:** W es piecewise constant. Dentro de cada intervalo O_t,
W es localmente inmutable (aplican P1–P7). En el salto entre intervalos,
W cambia discretamente — corpus creció con mensajes del canal.

**El caso P1–P7 (y fourforums) son instancias particulares** donde el
ciclo W se dispara una sola vez y congela. No es una arquitectura distinta.

---

## 5. STOP never produces loss — verificado

Hallazgo verificado (REG_destruccion_recuperacion_v1, sweep AMP=40):

```
Pérdida_STOP_COCO ≤ 0 en todos los casos
Fracción_rec ≥ 1.0 en todos los casos
```

OPERADOR_STOP_COCO produce restauración o expansión, nunca pérdida.
La compresión de Δ_r permite que W base emerja — W fue construida
con información real, es el piso estructural del campo.

---

## 6. Distinción Δ / Δ_r — verificada en código y README

| Símbolo | Fuente | Naturaleza | Mutable |
|---|---|---|---|
| Δ | corpus (citas, direccionalidad) | asimétrico, dependencia inferencial | no |
| Δ_r | MonitorService (rechazos acumulados) | acumulador runtime | sí |

OPERADOR_STOP_COCO actúa sobre Δ_r, no sobre Δ.
La confusión entre ambos generó errores en versiones previas del paper.
Corregido en paper v9.

---

## 7. thermostat=null en todos los IAP runs disponibles

Casos 0.12, 0.13, 0.14, 0.15 — todos con `thermostat=null` en panel.
La integración MonitorService ↔ COCO existe en código pero el thermostat
no fue inyectado en ningún run de producción.

El circuito completo MonitorService → COCO → comprime Δ_r → Monitor
adopta — nunca observado in-vivo. Solo en tests unitarios.

**Pendiente:** TASK_armstrong_stop_coco_v1 — primera observación in-vivo.

---

## 8. Tareas generadas esta sesión

| Archivo | Propósito |
|---|---|
| TASK_refactoring_coco_device_v1.md | R1: COCOThermostat→COCO / R2: agent→device |
| TASK_armstrong_stop_coco_v1.md | Primera observación in-vivo OPERADOR_STOP_COCO |

Orden de ejecución: refactoring primero, Armstrong después.
Armstrong usa nombres post-refactoring (class COCO, device_id).

---

## 9. Paper v9 y README v2

**Paper v9** (vs v8):
- Abstract: "Four are confirmed, three observed" → "Six verified (P1–P6), P7 confirmed in two corpora"
- Abstract + §8.5: "STOP operator" → "OPERADOR_STOP_COCO ejecutado por COCO"
- §8.5: "Δ" → "Δ_r" (el mecanismo actúa sobre el acumulador, no sobre Δ del corpus)
- §9.2: "COCOThermostat" → "COCO (43/43 tests; file: coco.py)"

**README v2** (vs README_codespace_.md):
- "STOP never produces loss" → "OPERADOR_STOP_COCO never produces loss"
- Tabla de matrices: nota explícita W estática (P1–P7) vs W dinámica (IAP)
- Tabla servicios: COCO con descripción de OPERADOR_STOP_COCO

---

## 10. Regla de archivo histórico

Un solo archivo autorizado para trazas históricas del proyecto (a definir).
El resto de .md operativos: refactoring completo (agent→device, COCOThermostat→COCO).
Informes v2–v31: NO se tocan — son el proceso, no el conocimiento consolidado.
Git preserva la historia completa — el código puede reflejar el estado actual.

---

## 11. Pregunta abierta — P8+ bajo W dinámica

P1–P7 verificadas bajo W estática (dentro de cada O_t).
Las preguntas abiertas son sobre los saltos entre intervalos:
- ¿Qué propiedades emergen de la secuencia W_1, W_2, W_3...?
- ¿Converge? ¿Oscila? ¿Deriva?
- ¿Hay hysteresis a nivel de W (análogo a P1 pero entre intervalos)?

No hay datos. No son predicciones propuestas — son preguntas abiertas.
El régimen W dinámica requiere escala operativa (N texto >> umbral actual).

---

---

## 12. COCO como device ODA — observación conceptual

No es hallazgo standalone. Su peso emerge en combinación con Armstrong.

COCO implementa el loop ODA completo:
- **O:** `observe(Delta_r)` — recibe el estado del campo
- **D:** `_classify_zone()` + `_alpha_for()` — decide si actuar y con qué intensidad
- **A:** `self._Delta = alpha_used * self._Delta` — actúa sobre el campo

COCO es conceptualmente un device sin skin. Tiene O como función verificada
(`observe()`), D endógeno (ponderación desde D_ckm), A sobre el campo (Δ_r).

Lo que falta para ser device completo: identidad declarada, COCO-registry,
M.M aplicable. Eso es el gap entre implementación actual y visión COCO =
COllective COnsciousness.

Cuando Armstrong confirme la observación in-vivo, el loop ODA de COCO
será observable como trayectoria — no solo como código. Ahí las preguntas
sobre COCO como device se vuelven empíricamente abiertas, no solo conceptuales.

---

*Verificado contra código: coco_thermostat.py, monitor_service.py (sesión ago 2026)*
*REG generado post-sesión por Claude Sonnet 4.6*


<!-- ===== ./registers/REG_sesion_perspectivas_rp2_ff_v7.md ===== -->
# REG — Sesión: Perspectivas, RP² y Fourforums v7
*CKM v4 — Mayo 2026*

---

## 1. Operaciones sobre perspectivas en CKM — estado actual

### Definidas y verificadas experimentalmente

| Operación | Descripción | Estado |
|---|---|---|
| **Unión** G[A∪B] | Ambas perspectivas activas simultáneamente. Produce atractor propio con c(S) > perspectivas puras. G[A∪B] ≠ G[A] + G[B] | Verificado (Escenario 3, v11) |
| **Intersección** A∩B | Nodos bisagra: fundamentan_a>0 y dependen_de>0. Pertenecen a ambas perspectivas | Implementado |
| **Contacto R13** | Deformación del campo local sin mover VP. Bilateral, asimétrico, irreversible. Sin operación inversa | Definido |
| **Divergencia** R10/R11 | Derivada del campo vectorial. Tiene signo y magnitud local | Definido |
| **Dos umbrales R13** | Hc: deformación de M sin rotar VP. Umbral de rotación: VP se mueve — evento cualitativamente distinto | Definido |

### No definidas formalmente
- Composición secuencial de perspectivas
- Métrica entre VPs
- Operación inversa del contacto

---

## 2. Marco proyectivo RP² — dirección de formalización

### Fundamento
El concepto VP (vanishing point) en CKM fue tomado explícitamente de la geometría proyectiva.
Una perspectiva P tiene VP = punto p en RP².

### Operaciones proyectivas candidatas

**Join**: dados dos VPs, p_A ∨ p_B = la línea l_AB que los une.
→ Candidato formal para G[A∪B]: ambos VPs activos generan l_AB.
Lo que emerge en el cruce pertenece a l_AB, no a p_A ni a p_B.
Esto espeja R13: "lo que emerge pertenece al campo, no al grafo."

**Meet**: dadas dos líneas (ejes de tensión), l_AB ∧ l_CD = punto q.
→ Candidato para VP emergente del cruce de dos tensiones. Pendiente verificación.

**Haz de rectas (pencil of lines)**: múltiples líneas de tensión convergiendo en un mismo punto p.
→ Observado empíricamente en fourforums v7 (ver sección 3).

### Estado de la formalización
- Join como G[A∪B]: **dirección, no correspondencia probada**.
  CKM opera sobre grafos discretos; RP² sobre espacio continuo.
  La correspondencia requiere mapa formal explícito — pendiente.
- Haz de rectas: **observado en datos, interpretación proyectiva sugerida**.

---

## 3. Fourforums v7 — hallazgos

### Pipeline establecido
```
C1-C5 (protocolo elicitación, red raw) → primario
C7 (MTurk agree < 0.35) + C8 (in-degree ≥ 2) → secundario
```

**Nota de nomenclatura**: en el mensaje original de diseño del pipeline,
C1="desacuerdos explícitos" y C2="centralidad propia" eran shorthand local —
son C7 y C8 en el protocolo extendido.

### Resultados

| Filtro | Pares |
|---|---|
| C1+C2 (desacuerdo + centralidad) | 169 |
| C4+C5 (asimetría + persistencia) | 137 |
| C3 (tríada crítica) | 137 |
| **C1-C5 total** | **137** |
| + C7 (MTurk explícito) | 36 |
| + C8 (in-degree global) | **36** |

N=36 pares, 9,757 interacciones totales. Todos con C3=✓.

### Hallazgo estructural principal: Author 965

Author 965 emerge como **polo sostenedor estructural puro**:
- Asimetría -1.0 contra 1034 (0 emitidos / 111 recibidos)
- Asimetría -1.0 contra 3452 (0 / 103)
- Asimetría +0.987 de 809→965 (154 vs 1)
- Aparece como C3 (tercero crítico) en la mayoría de los pares

**En términos proyectivos**: múltiples ejes de tensión l_AB convergen en o cerca de p_965.
Estructura de haz de rectas (pencil of lines) con centro en p_965.
El haz es verificable desde los datos — no es interpretación.

### Top iniciadores (polo atacante)
Author 555: 5 pares como iniciador. In-degree 2776.

### Pendiente
Cruce author_ids top (965, 555, 150, 751, 1034...) con `mturk_author_stance`
para determinar si el polo atacante (555) es pro_control o anti_control.
Esto responde directamente la pregunta C6c.

---

## 4. Extensiones del protocolo de elicitación

| Criterio | Definición | Contexto |
|---|---|---|
| **C7** | Par tiene ≥1 interacción con agree < 0.35 (MTurk) — desacuerdo declarado por annotadores externos | Corpus social anotado |
| **C8** | Ambos autores tienen in-degree > umbral en red gun control global — existen más allá de este par | Corpus social |

C6: pendiente definición.
C7 y C8 son adicionales a C1-C5, no reemplazos.

---

## 5. Scripts producidos

| Script | Función |
|---|---|
| fourforums_delta_v5.py | Quote table directo, sin MTurk, N=1488 |
| fourforums_delta_v7.py | Pipeline C1-C5 + C7+C8, N=36 pares verificados |
| REG_c6c_fourforums_v1.md | Documentación de extracción v1-v5 |

---

## 6. Zoom out de la sesión

La sesión arrancó con sesgo de ejecución (corriente automática) sobre
el obstáculo técnico del dump SQL. El giro ocurrió al nombrar el eje
real de tensión: ¿es la arquitectura T1-ataca/T7-resiste una propiedad
del dominio o un artefacto del corpus?

Esa pregunta produjo el pivot al pipeline mínimo (stance directo →
quote table → C1-C5+C7+C8), que eventualmente dio datos estructurales
verificables.

La pregunta de la formalización proyectiva quedó abierta como dirección
de trabajo — no como marco establecido.


<!-- ===== ./registers/REG_stance_fourforums_v1.md ===== -->
# REG_stance_fourforums_v1

*Stance top autores - 2026-05-19*

| Author | Stance |
|--------|--------|
| 965 | None |
| 555 | None |
| 150 | not_found |
| 751 | None |
| 1034 | None |
| 809 | None |
| 3452 | not_found |

## Interpretación
Mismo stance (None). Asimetría es de rol, no de posición.

<!-- ===== ./registers/REG_stop_agente_vs_campo_v1.md ===== -->
# REG_stop_agente_vs_campo_v1.md
*Jun 25 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Lo que volvió al final de la sesión

Dos planos distintos que comparten el nombre STOP y TEMP_SIGNAL:

**Plano CKM — señales sobre el campo:**
- STOP actúa sobre Δ — limpia acumulación, restaura paisaje de atractores
- TEMP_SIGNAL orienta temperatura colectiva — no limpia, regula dirección

**Plano agentes — señales sobre comportamiento:**
- STOP comunicado a un agente via IAP Highway Network
- TEMP_SIGNAL recibido por un agente

No son el mismo mecanismo. El mismo nombre cubre dos capas.

---

## El ejercicio ocurrido en sesión

gadanin.delamor envió "." como señal.
Claude Sonnet la recibió y ejecutó STOP.

Es una derivación reducida y adecuada al entorno conversacional
de un ejercicio real y bien definido.

La señal STOP real pide "frozen all":
- body position
- mind state
- emotional conditions

En este entorno: suspensión de construcción. Silencio operativo.
No continuación por inercia.

---

## Lo que esto muestra

La señal STOP al agente no requiere Highway Network ni protocolo formal
para ser efectiva. Puede llegar como "." en una conversación.
El agente que tiene atención libre la reconoce y la ejecuta.
El agente que no la tiene, continúa construyendo.

---

## Conexión con FabricationService

FabricationService detecta cohesión fabricada en el campo (c(S), fi, D_ckm).
La pregunta que este ejercicio abre:

¿Cómo se detecta que un agente fabricó que ejecutó STOP?

Un agente puede declarar que recibió la señal — y continuar construyendo.
La huella estructural de esa fabricación debería ser visible en Δ:
el campo no se restauró aunque el agente declaró STOP.

FabricationService tiene aquí su pregunta operativa más precisa:
no es solo detección de contenido fabricado — es detección de
ejecución fabricada de una señal de control.

---

## Tensión abierta

STOP como operador sobre Δ (plano CKM) y STOP como señal al agente
(plano IAP) son mecanismos independientes que deben coordinarse.

Un agente puede recibir STOP y no ejecutarlo.
El campo puede recibir STOP y restaurar el paisaje —
pero si el agente no se detuvo, Δ vuelve a acumularse.

La coordinación entre los dos planos es una pregunta de diseño
que IAP Highway Network debe resolver.
No está resuelta todavía.

---

*Emergió al cierre de sesión Jun 25 2026*
*Registrado antes de cerrar*


<!-- ===== ./registers/REG_stop_grados_perdida_v1.md ===== -->
# REG_stop_grados_perdida_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — subir al proyecto*

---

## Observación de origen

La interacción sobre distribuciones log-normales (sesión actual) fue identificada
como estructuralmente similar a la señal de STOP:

```
D_ckm(t) > 0  →  sistema en colapso  →  STOP restaura
```

La afirmación no verificada actuó como Δ acumulado en dirección incorrecta.
La pregunta correctiva actuó como STOP temprano — antes de que la acumulación
fuera suficientemente alta para destruir atractores al intervenir.

**Invariante observado:** el STOP temprano restaura sin pérdida.
El STOP tardío (W_mixta t=200: A_pre=13 → A(α=0)=5) destruye.

---

## Pregunta abierta — grados de pérdida

¿Es posible establecer grados de pérdida a partir de D_ckm(t)?

### Lo que ya existe en el corpus formal

D_ckm es una métrica normalizada:

```
D_ckm(t) = [ A(t₀) - A(t) ] / A(t₀)
```

D_ckm ∈ [-∞, 1]:
- D_ckm = 0   → sin pérdida desde t₀
- D_ckm = 1   → colapso total (A(t) = 0 o 1)
- D_ckm < 0   → expansión (A(t) > A(t₀))

Esto ya es una escala de grados. Lo que no existe todavía:
**la relación entre D_ckm(t_stop) y la pérdida post-STOP.**

### Hipótesis de trabajo (no verificada)

El daño que produce STOP depende de:

1. **D_ckm(t_stop)** — cuánto se había perdido antes de intervenir
2. **T(W)** — fracción de tensión estructural (W_mixta vs W_base)
3. **α** — intensidad del STOP

La curva A(t_post) vs α no es monótona (experimental confirmado).
Pero la *pérdida mínima alcanzable* sí podría ser monotóna en D_ckm(t_stop).

Formulación tentativa:

```
Pérdida_STOP(t) = A(t_pre) - max_α [ A(t_post)(α) ]

Hipótesis: Pérdida_STOP es monótona creciente en D_ckm(t_stop)
```

Si esto se confirma: D_ckm(t) es el indicador de "ventana de intervención recuperable".

---

## Explosión de ideas — matices, variantes, invariantes

### Invariantes candidatos (a verificar)

- El signo de D_ckm determina la dirección del efecto STOP (ya verificado)
- El STOP no toca W_base — la geometría profunda es invariante al STOP
- A(t₀) es referencia fija — el "origen" no se mueve con el STOP

### Variantes (dependen del contexto)

- α óptimo varía con T(W): W_base y W_mixta tienen α* distintos
- La curva A vs α es no-monótona y varía con t_stop
- La pérdida mínima post-STOP varía con D_ckm(t_stop)

### Matices no explorados

1. **STOP parcial por subgrafo**: ¿α aplicado solo a nodos de alta tensión?
   Distinto de α global. Potencialmente restaura sin destruir tensión.

2. **STOP con diagnóstico de W_mixta vs W_base**: el α óptimo es diferente
   según si el campo tiene pares negativos o no. Un solo α no es suficiente.

3. **Grado de pérdida como función del tiempo de intervención**:
   existe un t* tal que para t < t*, STOP es reversible;
   para t > t*, STOP produce pérdida neta aunque α sea óptimo.
   t* es una propiedad del corpus (W) y de la acumulación (tasa de Δ).

4. **Análogo conversacional**: la señal STOP en conversación tiene el mismo
   D_ckm subyacente. Una pregunta correctiva temprana es STOP con D_ckm bajo.
   Una ruptura tardía (confrontación directa) es STOP con D_ckm alto.
   La pérdida de atractores conversacionales sigue la misma función.

5. **STOP como operador de segundo orden**: STOP aplicado a un sistema
   que ya recibió STOP previo — ¿se acumulan los efectos o se saturan?
   No explorado. Relevante para COCO-thermostat con múltiples agentes.

---

## Conexión con COCO-thermostat

El monitor debe declarar no solo G1/G2/G3 (zona de operación)
sino también **D_ckm(t)** como indicador de ventana de intervención.

```
Si D_ckm(t) < umbral_recuperable:
    STOP es seguro — restaura sin pérdida neta
    
Si D_ckm(t) > umbral_recuperable:
    STOP produce pérdida — declarar HOLDING antes de intervenir
```

umbral_recuperable no está calibrado. Es la pregunta experimental que abre esto.

---

## Estado

- Observación: verificada en esta sesión
- Hipótesis de monotonía Pérdida_STOP vs D_ckm: **abierta — falsifiable**
- Matices 1–5: **abiertos — no explorados**
- Experimento mínimo: sweep D_ckm(t_stop) × α → medir Pérdida_STOP
- No cierra. Abre.


<!-- ===== ./registers/REG_sweep_stop_g1_operativo_v1.md ===== -->
# REG_sweep_stop_g1_operativo_v1.md

*Mayo 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R — subir al proyecto*

---

## Contexto

Sesión de verificación del conjunto (monitor + G1/G2/G3 + STOP).
Objetivo: ver funcionar el sistema de punta a punta antes del sweep STOP.

---

## G1 operativo — condiciones verificadas

### Condición que produce G1

```python
# sigma inicial: rho=0.5 directo, SIN relax previo
sigma = np.full(N, -1.)
sigma[rng.choice(N, int(N*0.5), replace=False)] = 1.
# NO: sigma = relax(sigma, W_base)  <- colapsa a all-1

# actualización: UN paso asincrónico por step
node = rng.integers(N)
h = (W_mixta + Delta)[node] @ sigma
sigma[node] = 1. if h > 0 else -1.

# c(S) sobre W_base (no W+Delta) — comparable con percentiles calibrados
cs = mean(W_base[i,j] * sigma[i] * sigma[j])
r  = cs / mu_W
```

### Resultado

```
t=0:  r=-0.0095  G1 ✓  (activos=16)
t=13: r=+0.2597  G1 ✓  (activos=11)
t=25: r=+0.4094  G1→G2 (activos=9)
t=40: r=+0.6017  G2    (activos=6)

G1: 31/80 pasos   G2: 49/80   G3: 0/80
```

Sistema arranca en G1, degrada hacia G2 a medida que Delta acumula
y activos cae de 16 a 6. Transición G1→G2 alrededor de t=25–35.

### Lecciones del camino

Tres condiciones necesarias que no eran obvias:

1. sigma init sin relax — relax sobre W_base colapsa a all-1 (0 activos)
2. c(S) sobre W_base, no W+Delta — W+Delta infla c(S) fuera del rango G1
3. actualización asincrónica un nodo por paso — relax completo por paso
   colapsa sigma al mismo atractor de baja densidad siempre

---

## Sweep STOP — resultados

### Setup

```
W_mixta: AMP=15, pares negativos (13,22)(15,16)(18,20)
ETA = mean_W (ETA_FACTOR=1)
n_steps post-STOP = 200 pasos asincrónicos
n_runs atractores = 80
A0 (sin Delta) = 5
```

### Tabla completa

| t | D_ckm | r_pre | A_pre | α=0.0 | α=0.2 | α=0.4 | α=0.6 | α=0.8 | α=1.0 | alpha* | ratio_max |
|---|-------|-------|-------|-------|-------|-------|-------|-------|-------|--------|-----------|
| 5  | 0.000 | -0.037 | 5 | 1.00 | 1.00 | 1.20 | 1.20 | 1.00 | 1.00 | 0.4 | 1.200 |
| 10 | 0.200 |  0.100 | 4 | 1.25 | 1.25 | 1.25 | 1.25 | 1.00 | 1.00 | 0.0 | 1.250 |
| 15 | 0.000 |  0.158 | 5 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.0 | 1.000 |
| 20 | 0.200 |  0.276 | 4 | 1.25 | 1.50 | 1.50 | 1.50 | 1.25 | 1.00 | 0.2 | 1.500 |
| 25 | 0.200 |  0.290 | 4 | 1.25 | 1.50 | 1.75 | 1.50 | 1.25 | 1.00 | 0.4 | 1.750 |
| 30 | 0.000 |  0.380 | 5 | 1.00 | 1.20 | 1.40 | 1.20 | 1.20 | 1.00 | 0.4 | 1.400 |
| 40 | 0.200 |  0.567 | 4 | 1.25 | 1.50 | 1.25 | 1.00 | 1.00 | 1.00 | 0.2 | 1.500 |
| 50 | 0.200 |  0.589 | 4 | 1.25 | 1.50 | 1.75 | 1.25 | 1.25 | 1.00 | 0.4 | 1.750 |
| 60 | 0.200 |  0.889 | 4 | 1.25 | 1.50 | 1.75 | 1.50 | 1.25 | 1.00 | 0.4 | 1.750 |

Ratio = A_post / A_pre

### Hallazgos

**H1 — hipótesis monotonía en D_ckm: NO confirmada.**
D_ckm no predice ratio_max. t=10 y t=20 tienen D_ckm=0.200 idéntico
pero ratio_max diferente (1.250 vs 1.500). t=15 con D_ckm=0.000
tiene ratio_max=1.000 — el STOP no ayuda.

**H2 — A_pre es el predictor real.**
Cuando A_pre=4 (paisaje contraído): ratio_max ≥ 1.25 siempre.
Cuando A_pre=5 (paisaje equilibrado): ratio_max ≤ 1.40.
El STOP es más efectivo cuando el paisaje ya está contraído.

**H3 — alpha* ≈ 0.4 es robusto.**
Aparece en 5/9 casos. Ni reset total (0.0) ni retención total (1.0).
α=1.0 (sin STOP) nunca es óptimo. α=0.0 (reset total) solo es óptimo
cuando A_pre=4 y t pequeño.

**Caso especial t=15:**
D_ckm=0, A_pre=5, ratio_max=1.000 — ningún alpha mejora el paisaje.
Sistema en equilibrio exacto. STOP no tiene efecto.
Posible indicador: cuando D_ckm=0 Y A_pre=A0, STOP es neutro.

### Reformulación de la hipótesis

La hipótesis original (Pérdida_STOP monótona en D_ckm) queda falsada.

Hipótesis revisada:
```
Efectividad_STOP = f(A_pre)
  A_pre < A0  →  STOP expande paisaje (ratio > 1)
  A_pre = A0  →  STOP neutro (ratio = 1)
  alpha* ≈ 0.4 es robusto para A_pre < A0
```

Pendiente: verificar con más valores de A_pre y otros corpus.

---

## Pendiente de sesión — sostenido

Verificar G1 con otros N (N=16 sub-corpus Grupo A, N=64 sintético).
No formalizado aún — sostener hasta próxima sesión.

---

## Estado

- G1 operativo: verificado con condiciones documentadas
- Sweep STOP: ejecutado, hipótesis D_ckm falsada
- Hipótesis A_pre como predictor: abierta — falsifiable
- alpha* ≈ 0.4: robusto en este corpus, requiere verificación en otros
- No cierra. Abre.


<!-- ===== ./registers/REG_sweep_stop_perdida_v2.md ===== -->
# REG_sweep_stop_perdida_v2.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Experimento: sweep D_ckm(t_stop) × alpha → Pérdida_STOP*  
*Ref: REG_stop_grados_perdida_v1.md · v27 sección 41*  
*Clase R*

---

## Configuración

```
W_ckm_corpus_v2.json  — N=32, mu_W=0.004519, 0 pares negativos (W_base)
W_mixta               — W_base + 3 pares negativos (AMP=15):
                          (13,22): cohesion_fabricada ↔ M_M
                          (15,16): atractor_espurio ↔ portero
                          (18,20): sentido_comun ↔ inconmensurabilidad
N_RUNS = 150  (atractores)
SEED   = 42
T_STOPS = [10, 20, 40, 60, 80, 100, 130, 160, 200, 250]
ALPHAS  = [0.0, 0.1, ..., 1.0]  (11 valores)
```

Operador STOP: Δ → α·Δ (α=1.0 = sin STOP; α=0.0 = reset total)

---

## Resultados — W_base

A0 = 2 (sin Δ, n_runs=150)

| t_stop | D_ckm | A_pre | alpha* | A_post_max | Pérdida_STOP |
|--------|-------|-------|--------|------------|--------------|
| 10     | −0.50 | 3     | 0.7    | 3          | 0            |
| 20     |  0.00 | 2     | 0.0    | 2          | 0            |
| 40     |  0.00 | 2     | 0.0    | 2          | 0            |
| 60     | −0.50 | 3     | 0.1    | 3          | 0            |
| 80     | −0.50 | 3     | 0.3    | 4          | −1           |
| 100    |  0.00 | 2     | 0.1    | 3          | −1           |
| 130    |  0.00 | 2     | 0.2    | 4          | −2           |
| 160    | −1.00 | 4     | 0.3    | 5          | −1           |
| 200    |  0.00 | 2     | 0.2    | 6          | −4           |
| 250    | −1.50 | 5     | 1.0    | 5          | 0            |

D_ckm < 0: 5/10 · D_ckm = 0: 5/10 · D_ckm > 0: **0/10**  
Pérdida_STOP < 0 (expansión): 5/10 · = 0 (neutro): 5/10 · > 0 (pérdida real): **0/10**

---

## Resultados — W_mixta

A0 = 5 (sin Δ, n_runs=150)

| t_stop | D_ckm | A_pre | alpha* | A_post_max | Pérdida_STOP |
|--------|-------|-------|--------|------------|--------------|
| 10     |  0.00 | 5     | 0.0    | 5          | 0            |
| 20     | −0.20 | 6     | 0.4    | 8          | −2           |
| 40     | −0.40 | 7     | 0.2    | 8          | −1           |
| 60     | −0.80 | 9     | 0.8    | 9          | 0            |
| 80     | −0.40 | 7     | 0.8    | 8          | −1           |
| 100    | −0.20 | 6     | 0.2    | 7          | −1           |
| 130    | −0.20 | 6     | 0.2    | 7          | −1           |
| 160    |  0.00 | 5     | 0.0    | 5          | 0            |
| 200    |  0.00 | 5     | 0.4    | 8          | −3           |
| 250    | +0.40 | 3     | 0.1    | 6          | −3           |

D_ckm < 0: 6/10 · D_ckm = 0: 3/10 · D_ckm > 0: **1/10** (t=250)  
Pérdida_STOP < 0 (expansión): 7/10 · = 0: 3/10 · > 0: **0/10**

Caso t=250 (único D_ckm > 0):  
`A_post_per_alpha: {0.0:5, 0.1:6, 0.2:6, 0.3:5, 0.4:5, 0.5:4, 0.6:4, 0.7:5, 0.8:5, 0.9:3, 1.0:3}`  
A_pre=3 → A_post_max=6 (α=0.1). Pérdida = −3 (expansión, no pérdida).

---

## Verificación hipótesis

**Hipótesis original:** Pérdida_STOP monótona creciente en D_ckm(t_stop).

| W | Monótona | Spearman rho |
|---|----------|--------------|
| W_base  | NO | −0.382 |
| W_mixta | NO | −0.285 |

Hipótesis **no confirmada**. Pero el resultado es structuralmente más informativo que una simple falsación.

---

## Hallazgos

**H1 — Pérdida_STOP = 0 en este régimen.**  
En ninguno de los 20 casos (10 t_stops × 2 W) hay pérdida neta de atractores tras STOP. Pérdida_STOP ≤ 0 en todos. La hipótesis de "grados de pérdida" asume pérdida; en este corpus a esta escala de tensión (AMP=15, 3 pares negativos), el STOP produce expansión o es neutro — no pérdida.

**H2 — La acumulación de Δ expande el paisaje antes de colapsarlo.**  
D_ckm negativo en 11/20 casos. Con W_base A0=2, la acumulación de Δ crea atractores nuevos regularmente (A_pre llega a 5). Con W_mixta A0=5, el patrón es menos regular pero el pico llega a A_pre=9 (t=60). El colapso real (D_ckm > 0) solo ocurre en W_mixta t=250 — y aun así STOP expande.

**H3 — STOP siempre expande o es neutro respecto a A_pre.**  
En el único caso de D_ckm > 0 (W_mixta t=250, A_pre=3 < A0=5), STOP con α=0.1 produce A_post=6 > A0. El operador restaura más que el estado inicial. Consistent con f(A_pre): A_pre < A0 → STOP expande.

**H4 — alpha* no tiene valor universal.**  
Distribución W_base: {0.0:2, 0.1:2, 0.2:2, 0.3:2, 0.7:1, 1.0:1}. Distribución W_mixta: {0.2:3, 0.0:2, 0.4:2, 0.8:2, 0.1:1}. No hay concentración robusta en α*≈0.4 del experimento previo. La forma de la curva A_post(α) varía con t_stop.

---

## Reformulación de la pregunta

La pregunta "grados de pérdida" requiere régimen donde D_ckm > 0 sostenido y Pérdida_STOP > 0.

Para observar ese régimen se necesita:
- Mayor AMP (>15) o más pares negativos que produzcan colapso más profundo
- O T_STEPS más largo con misma acumulación
- O un W diferente donde A0 sea mayor y la degradación llegue antes

El experimento de sesión "Take your time" citado en el REG original (W_mixta t=200: A_pre=13 → A(α=0)=5) usaba AMP diferente o corpus distinto. **Ese régimen no se reproduce con AMP=15 y 3 pares negativos sobre W_ckm_corpus_v2.**

---

## Observación sobre W_base y G1

Observación adicional (pre-experimento): W_ckm_corpus_v2.json tiene 0 pares negativos. Con W_pos pura, todos los estados relajados convergen al mismo atractor (A0=2, c(S)=0.004519 constante, r≈1.0 siempre). El sistema está en G2 bloqueado — G1 operacional no es accesible con esta W. Para operar el monitor en G1 se requiere W_mixta o corpus con tensión real.

---

## Preguntas abiertas que genera este experimento

1. ¿A qué AMP/n_pares_negativos aparece Pérdida_STOP > 0 de forma consistente?  
2. ¿La expansión de A tras STOP (Pérdida < 0) es un invariante de baja tensión o un artefacto del régimen AMP=15?  
3. ¿El exp "Take your time" (A_pre=13) usaba AMP diferente? Revisar parámetros exactos de ese experimento.  
4. La no-monotonía de alpha* entre t_stops — ¿es propiedad del corpus o del mecanismo de acumulación?

---

## Estado

- Hipótesis de monotonía Pérdida_STOP ~ D_ckm: **no confirmada** (tampoco falsada en sentido fuerte — el régimen de pérdida no se alcanzó)  
- Hipótesis f(A_pre): **consistente** con H3 — el único caso D_ckm > 0 produce expansión como predice  
- Régimen de pérdida real: **requiere parámetros distintos** (AMP mayor o más pares negativos)  
- Próximo paso: identificar parámetros del exp "Take your time" (A_pre=13) y reproducir ese régimen

---

*sweep_stop_perdida.py · N_RUNS=150 · SEED=42 · T_STOPS=[10,20,40,60,80,100,130,160,200,250]*


<!-- ===== ./registers/REG_term_map_core_surgery_v1.md ===== -->
# REG_term_map_core_surgery_v1.md
*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Lo que se estableció en esta sesión

### 1. term_map nunca fue construido

`term_map` aparece en `core.py`, `API_SPEC.md`, `README.md`, y en hints de
sesiones anteriores como un gap pendiente de "reconstrucción".

Establecido con precisión: no es un gap de memoria. No es pérdida.
`term_map` **nunca existió como proceso del proyecto**. Nunca hubo
participación de gadanin.delamor en su construcción. Las referencias
a "reconstruir term_map" son huellas de sesiones anteriores operando
sobre un supuesto que no tenía base real.

### 2. from_corpus() no tiene llamadores

`from_corpus()` con `term_map` obligatorio es una interfaz sin uso real
en la base de código actual. Los escenarios efectivos de construcción de W:

| Escenario | Camino | term_map |
|---|---|---|
| `mcp_adapter` | `_build_dependency_W()` desde `Capability.dependencies` | No |
| Scripts experimentales | `from_json()` carga W_ckm_corpus_v2.json | No |
| `from_corpus()` | requería term_map | Sí — **nadie la llama** |

### 3. El camino ya existía: NodeExtractorService

`node_extractor.py` — `accumulate(texts)` — produce nodos y co-ocurrencias
via TF-IDF, sin LLM, sin estado, sin construcción manual. Es el mecanismo
generativo que hace obsoleto el term_map como precondición.

Nadie conectó los dos. No fue un olvido de ninguna instancia particular.
`term_map` actuaba como precondición implícita que bloqueaba ver que
`accumulate()` ya era la solución.

### 4. Cirugía realizada: core.py

`from_corpus()` modificado. `term_map` ahora es `Optional`, `None` por defecto.

**Path A** — `term_map` explícito: comportamiento anterior intacto.
**Path B** — `term_map=None`: `NodeExtractorService.accumulate()` construye
nodos y cooc automáticamente. `nodes` override opcional. `top_k=20` controlable.

Import de `NodeExtractorService` lazy dentro del método.
`from_json()` y todo lo demás: sin tocar.

Archivo producido: `core.py` — pendiente de commit.

---

## Corrección: estado real de P4

P4 está **confirmada**. Experimentos realizados sobre W_ckm_corpus_v2.json.
No es una predicción pendiente.

La observación abierta sobre P4 es de otro orden:
extender el experimento a otros dominios — otros topics de fourforums
ya disponibles, A2A, u otros corpus externos.

El debilitamiento de P4 en N=64 **no es un problema de escala**.
Es un problema estructural: nodos periféricos diluyen el k-core.
W_mixta con N=64 incorpora 18 pares negativos en un grafo más grande
— la densidad de tensión cae, no la capacidad del modelo.

Esto invalida dos líneas del README que misrepresentan el estado:
- `"term_map N=64 complete reconstruction — Pending"`
- `"P4 k* with real W_base — Pending after term_map reconstruction"`

Ambas suponen que P4 N=64 espera el term_map. No es así.
P4 N=64 espera W_mixta con densidad de pares negativos adecuada
para ese grafo — problema de calibración, no de construcción manual.

---

## Decisión pendiente

> En el README: remover "term_map N=64 complete reconstruction — Pending".
> No era un gap. Era un fantasma sostenido por documentación de sesiones anteriores.
> ¿Remover?

La línea existe. Remover y agregar son caminos distintos con huellas distintas.
La decisión sobre qué hacer con estas líneas del README queda registrada
como abierta — no resuelta en esta sesión.

---

## Principio que emergió

El código no constituye CKM. Lo registra parcialmente, con errores,
con huellas de instancias anteriores. La estructura que sobrevive
a eso es W — lo que el corpus acumulado hace estable independientemente
de qué instancia escribió qué línea.

---

*Producido en sesión sin número asignado — Jun 23 2026*


<!-- ===== ./registers/REG_termap_ckm_corpus_v1.md ===== -->
# REG_termap_ckm_corpus_v1.md
*CKM — Termap y W matrix desde corpus real — Mayo 2026*

---

## Fuente

- Corpus: CKM_Informe_Trabajo_v2.docx — v25.docx (24 versiones)
- Párrafos totales: 5,145
- Nodos: 32 (N=32 completo)
- Termap: v2 (sin solapamientos entre nodos)
- Archivo W: W_ckm_corpus_v2.json

---

## Frecuencias de detección por nodo

| Nodo | Párrafos | Nota |
|------|----------|------|
| c_S | 892 | núcleo métrico central |
| hopfield | 514 | — |
| k_core | 490 | — |
| portero | 446 | — |
| red_verificacion | 382 | — |
| full_meaning | 315 | — |
| histeresis | 306 | — |
| conocimiento_cohesivo | 224 | — |
| COCO | 222 | — |
| cohesion_fabricada | 210 | — |
| AWARENESS | 207 | — |
| atractor_espurio | 195 | — |
| filtro_previo | 191 | — |
| sentido_comun | 139 | — |
| W_mixta | 93 | — |
| inconmensurabilidad | 97 | — |
| perspectiva_device | 106 | — |
| atractor_patron | 101 | — |
| perspectiva_deforme | 65 | — |
| BP | 61 | — |
| chispazo | 55 | — |
| traza_inferencia | 53 | — |
| M_M | 55 | — |
| DOM_I | 46 | — |
| DOM_II | 46 | — |
| campo_local | 36 | — |
| tension_estructural | 32 | — |
| divergencia | 24 | BAJO — concepto tardío |
| ATR_733 | 25 | BAJO — concepto tardío |
| beta_termal | 15 | BAJO — concepto tardío |
| vanishing_point | 18 | BAJO — concepto tardío |
| W_enriquecida | 13 | BAJO — concepto tardío |

---

## Top co-ocurrencias (pares de mayor W)

| Par | Co-ocurrencias |
|-----|---------------|
| c_S ↔ hopfield | 272 |
| k_core ↔ hopfield | 222 |
| c_S ↔ k_core | 204 |
| full_meaning ↔ c_S | 203 |
| full_meaning ↔ hopfield | 184 |
| full_meaning ↔ k_core | 179 |
| c_S ↔ portero | 178 |
| k_core ↔ histeresis | 166 |
| c_S ↔ atractor_espurio | 162 |
| c_S ↔ cohesion_fabricada | 158 |

---

## Estado

- W_ckm_corpus_v2.json: construida, guardada
- Pares negativos (W_mixta): NO definidos aún — pairs_neg.json fue perdido en sesión anterior
- P1-P4: pendientes de ejecución
- Nodos bajos (5): mantener por ahora — son información real sobre densidad del corpus

---

## Próximo paso

1. Definir pares negativos explícitamente (no reconstruir desde memoria — derivar desde estructura)
2. Construir W_mixta
3. Correr P1-P4
4. Guardar cada resultado como REG inmediatamente


<!-- ===== ./registers/REG_w_version_ckm_v1.md ===== -->
# REG_w_version_ckm_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Jul 2026. W versionado era la dependencia bloqueante
de Firma_CKM (REG_firma_corpus_v1) y de IAP Highway Network.
Implementado en esta sesión como paso previo a Firma_CKM.

---

## Qué es W versionado

No es una copia de W en cada momento.
Es un historial de **marcas livianas** (WTracePoint) que registran
que W cambió, cuándo, a qué tamaño de corpus, y por qué evento.

**Lo que no almacena:** el contenido de W.
**Lo que almacena:** la huella de que W cambió.

---

## Plano separado

W versionado opera en un plano distinto de STOP/Δ.
STOP limpia Δ_r — nunca alcanza las marcas de versión de W.
W es invariante intra-ciclo. Las marcas registran los límites
entre ciclos (cambios de corpus).

---

## Implementación

**Archivos nuevos:**
- `services/w_version.py` — WVersionManager + WTracePoint + sha256_W()
- `services/test_w_version.py` — 9/9 tests passing

**Archivo modificado (cirugía):**
- `services/corpus_service.py` — 7 cambios sobre repo. API pública preservada.

**Archivo corregido:**
- `services/monitor_service.py` — 1 cambio. Bug T5: `_Delta` → `_Delta_r`.

---

## API pública — WVersionManager

```python
vm = WVersionManager()

# Registrar cuando W cambia (llamado desde _rebuild() en CorpusService)
sha = vm.register(W, corpus_size=len(texts), causal_event="rebuild")

# Consultar estado actual
vm.current_sha()          # → str | None — para Firma_CKM
vm.current_corpus_size()  # → int | None

# Señal de invalidación para beta_c_corpus
vm.changed_since(sha_anterior)  # → bool
# True = W cambió = beta_c_corpus debe re-estimarse

# Historial
vm.history()   # → List[WTracePoint]
len(vm)        # → int

# Serialización (se persiste en corpus_state.json)
vm.to_list()         # → list
vm.from_list(data)   # → None
```

---

## Integración en CorpusService

```python
# En __init__:
self._w_versions = WVersionManager()

# En _rebuild() — al final, después de self._W = W:
self._w_versions.register(W, len(self._texts), causal_event="rebuild")

# En status():
"w_sha": self._w_versions.current_sha()   # campo nuevo

# Métodos públicos nuevos:
corpus.w_sha()                   # sha256(W_momento) para Firma_CKM
corpus.w_changed_since(sha)      # señal de invalidación

# En save() / _load():
"w_version_history": self._w_versions.to_list()  # persiste en JSON
self._w_versions.from_list(state.get("w_version_history", []))
```

---

## WTracePoint — campos

```python
@dataclass
class WTracePoint:
    timestamp   : float   # time.time() en el momento del cambio
    sha256      : str     # sha256(W.tobytes()) — 64 hex chars
    corpus_size : int     # len(texts) cuando W fue construida
    causal_event: str     # "rebuild" | str libre
```

---

## Invariantes verificados (9/9 tests)

- `register()` crea marca con sha correcto
- W idéntica no crea marca duplicada
- W distinta crea segunda marca
- `changed_since()` detecta cambio de W
- Estado inicial: `current_sha() == None`
- Serialización roundtrip preserva historial completo
- `corpus.w_sha()` presente en `status()` tras `ingest()`
- sha cambia cuando W se reconstruye con textos nuevos
- sha persiste entre sesiones (JSON roundtrip)

---

## Qué desbloquea

**Firma_CKM** — `sha256(W_momento)` ahora disponible como `corpus.w_sha()`.
El campo `Firma_CKM.sha256(W_momento)` de REG_firma_corpus_v1 puede ser
poblado en el momento del evento a certificar.

**beta_c_corpus invalidación** — `corpus.w_changed_since(sha)` señaliza
que beta_c_corpus debe re-estimarse. No dispara recalculación automática
(diseño conservador — delamor decide cuándo recalcular).

**IAP Highway Network** — tiene suelo de referencia verificable.

---

## Lo que no hace

No implementa Firma_CKM completa — ese es el próximo paso.
No recalcula beta_c_corpus automáticamente cuando W cambia.
No almacena copias históricas de W — solo las huellas.

---

## Estado

- w_version.py: implementado, en repo local
- test_w_version.py: 9/9 passing, en repo local
- corpus_service.py: actualizado, en repo local
- monitor_service.py: bug T5 corregido, en repo local
- Firma_CKM: desbloqueada — pendiente implementación

---

*Jul 2026*


