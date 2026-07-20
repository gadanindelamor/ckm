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
