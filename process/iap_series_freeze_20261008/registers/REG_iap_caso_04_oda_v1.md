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
