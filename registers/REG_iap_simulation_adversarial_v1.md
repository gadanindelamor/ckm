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
