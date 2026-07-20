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
