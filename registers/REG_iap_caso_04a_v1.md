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
