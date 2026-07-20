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
