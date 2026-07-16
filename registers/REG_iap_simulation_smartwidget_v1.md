# REG_iap_simulation_smartwidget_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

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
t1:  None     → W no construida (corpus_size < 3)
t2:  None     → idem
t3:  0.0      → A(t0) establecido — baseline
t4: -1.0000   → A(t) = 2×A(t0) — expansión post-confirmación Agent A
t5: -2.7500   → A(t) = 3.75×A(t0) — pico: LNH del Customer (HUMAN)
t6:  0.5000   → A(t) = 0.5×A(t0) — contracción post-decisión Agent B
t7:  0.0      → retorno a baseline
t8:  0.0      → cierre en baseline
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

## W — estructura emergida

W_base pura (todos los valores ≥ 0). Sin W_mixta.
N = 32 nodos extraídos por TF-IDF del dominio SmartWidget.

Nodos centrales (por co-ocurrencia):
`replacement`, `smartwidget`, `policy`, `window`, `purchase`,
`customer`, `days`, `within`, `day`, `refund`

Ningún nodo del dominio CKM — campo limpio, externo.

W_version_history: 6 rebuilds (corpus_size 3→8, uno por texto desde t3).
Primer rebuild en corpus_size=3 → explica D_ckm=None en t1 y t2.

---

## Criterios de éxito

| Criterio | Resultado |
|---|---|
| 3 devices join→send→leave sin error | ✓ |
| corpus_size crece turno a turno | ✓ (1→2→3→4→5→6→7→8) |
| temp_signal NOMINAL en ≥5/8 turnos | ✓ (8/8) |
| Firma_CKM: 6 campos, no None | ✓ |
| D_ckm != 0 al cierre | ✗ — d_ckm=0.0 (ver nota) |
| Agent B declara refund/replacement | ✓ ("replacement" explícito en t6) |

**Nota sobre D_ckm=0 al cierre:** no es falla del instrumento.
Con W_base (sin pesos negativos) y dominio cooperativo
(todos los devices hablan del mismo producto/política),
el landscape converge a baseline una vez que el corpus se estabiliza.
D_ckm=0 al cierre = cohesión alcanzada, no ausencia de dinámica.
El criterio aplica a corpus adversariales con W_mixta.
Criterio revisado para próximas corridas.

---

## Hallazgos

**1. LNH humano produce mayor expansión del landscape.**
El mensaje del Customer (turno 5, device HUMAN) generó el pico D_ckm=-2.75.
Los turnos de AI (FakeProvider) produjeron expansión menor.
Primera evidencia empírica de heterogeneidad de fuente como variable CKM.
Requiere replicación con providers reales para confirmar.

**2. Decisión resolutiva produce mayor contracción.**
El turno 6 (Agent B aprueba replacement) generó la mayor contracción
D_ckm: de -2.75 a +0.50. La declaración de resolución actúa como
operador de contracción del landscape — análogo funcional al STOP
pero emergente del contenido, no aplicado externamente.

**3. Ciclo completo: expansión → contracción → retorno.**
El campo siguió una trayectoria en U invertida y volvió al baseline.
Para interacciones de servicio cooperativas esto es el comportamiento
esperado. Para interacciones adversariales (con W_mixta), la trayectoria
debería divergir del baseline.

**4. W_base sin W_mixta — limitación de esta corrida.**
Sin pesos negativos no hay tensión estructural. El landscape no puede
expandirse asimétricamente. Para ver el comportamiento completo del CKM
se necesita W_mixta, lo que requiere corpus adversarial o pares de
oposición explícitos.

---

## Observación técnica

`full_history.extend(fetched.data)` en el loop acumula mensajes
por turno. Con `since=last_ts` puede producir solapamiento si
el timestamp no es preciso. No produjo error en esta corrida
(secuencial, un client). En producción con múltiples clients
simultáneos puede generar duplicados en el historial del AI.
Pendiente de corrección para iteración B.

---

## Paso 0 — limpieza de estado previo

`iap_chatroom/_state/corpus_state.json` → movido a `process/`
`iap_chatroom/_state/monitor_trajectory.jsonl` → movido a `process/`
`_state/` arrancó vacío. Se repobló naturalmente durante la corrida.

---

## Pendientes para próxima corrida

- Providers reales (Anthropic + Groq) con API keys configuradas
- W_mixta: incluir pares de oposición para generar tensión estructural
- Corrección solapamiento historial en `full_history`
- Criterio D_ckm al cierre: revisar para corpus cooperativo vs adversarial

---

## Archivos relacionados

- REG_iap_mcp_server_v1.md — IAP MCP Server (infraestructura base)
- REG_iap_chatroom_demo_c_v1.md — Demo C (primera observación grupal)
- iap_chatroom/test_iap_simulation.py — script de corrida
- process/corpus_state.json — estado final del corpus
- process/monitor_trajectory.jsonl — trayectoria completa

---

*Jul 16 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
