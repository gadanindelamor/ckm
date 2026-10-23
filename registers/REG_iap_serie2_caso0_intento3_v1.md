# REG_iap_serie2_caso0_intento3_v1 — serie2_caso0, intento 3

Clase R. **Pasa a `registers/` con el OK de delamor** (23 oct 2026). Borrador original: `docs/REG_borrador_serie2_caso0_intento3.md`.

- **Caso:** `serie2_caso0` (técnico) / `S2-C0`.
- **Fecha:** 2026-10-22. **Duración real:** 1204,61 s. **Modo:** `ZERO_SHOT`
  desde corpus 0 (verificado por MCP: `corpus_size = 0`, canal en 0).
- **Ejecutado por Code**, por orden explícita de delamor (tarea autónoma del
  22 oct, ítem 6).
- **Datos:** `experiments/serie2_caso0_intento3_log.json` (commiteado) y
  `experiments/_state_S2-C0/` (10 archivos, no se commitea; el intento 2 quedó
  preservado en `process/` con timestamp `1792649008`).
- **Código:** `8c963b2` más el cambio de modelo de device B (en el mismo commit
  que este REG).

---

## 1. Para qué corrió, y qué cambió respecto del intento 2

No es por el objetivo del intento 2 —**COCO ya se conectó**—, sino para medir
los arreglos de los ítems 1 y 2 **con lo demás igual**. Lo que cambió:

| | intento 2 | intento 3 |
|---|---|---|
| techo de salida Groq | 512 plano | **512 / 512 / 256 por modelo** |
| `reasoning_effort` | no se pasaba | **`"low"` en los dos `gpt-oss`, nada en qwen** |
| device B | `gemini-2.5-flash` | **`gemini-3.5-flash-lite`** |
| log del canal | la ventana de 20 | **el registro entero** |
| lo demás | — | igual (`DURATION`, ventanas, consigna, umbrales de CKM) |

## 2. Los números

| | intento 2 | intento 3 |
|---|---|---|
| textos de device | 80 | **56** |
| mensajes del canal | 84 | **60** (56 + 4 joins SYSTEM) |
| versiones de W | 6 | **4** |
| rebuilds (corpus) | 40, 50, 60, 70, 80 | **33, 43, 53** |
| evaluaciones de COCO | 51 | **27** |
| `coco.connected` | `true` | **`true`** |
| **errores del provider** | **71** | **0** |
| **truncamientos** | **17** | **0** |
| respuestas no usables | 17 (las 17 vacías) | **2** (1 vacía, 1 de 374 chars) |
| `triggers` | 0 | 0 |

**Por device:**

| device | modelo | vueltas | llamadas | 429 | decisiones |
|---|---|---|---|---|---|
| A | `gpt-oss-120b` | 223 | 89 | **0** | INTERACT 25 · OP_SILENCE 38 · SKIP 159 · END_OF_CASE 1 |
| B | `gemini-3.5-flash-lite` | 209 | 68 | **0** | INTERACT 7 · OP_SILENCE 54 · SKIP 148 |
| C | `gpt-oss-20b` | 225 | 91 | **0** | INTERACT 23 · OP_SILENCE 43 · SKIP 157 · UNKNOWN 2 |
| D | `qwen3.8-27b` | **2** | 2 | 0 | **LEAVE 1** · OP_SILENCE 1 |

675 vueltas, 250 llamadas, **55 publicados** (el 56.º entró durante el cierre;
ver §6). `action_result`: `no_action` 602 · `published` 55 · `left` 1 ·
`did_not_happen: end of case` 1.

## 3. Las expectativas declaradas, contra lo que pasó

**Ítem 1 — cumplida.** Lo declarado antes de correr: *"0 vacíos en
`gpt-oss-20b` y la misma presión de TPM que el intento 2, que tuvo cero
`413`"*.

- **0 truncamientos** (17 en el intento 2, los 17 de ese modelo).
- **0 `413`** y **0 errores del provider de ningún tipo**.
- Respuestas no usables de device C: **2** contra 17, y **sólo una vacía**. La
  otra tiene 374 caracteres: el modelo contestó un párrafo donde el gate pide
  una palabra. **No es el techo** —no hubo truncamiento— así que es otra causa,
  y queda abierta.

**Ítem 2 — cumplida y verificable en el log.** `canal.n_mensajes: 59`,
`n_mensajes_segun: "channel_messages.jsonl"`, **59 mensajes guardados** (con sus
textos, que ahora sí entran a la traza del repo) y `mensajes_por_MCP: 20` al
lado. El contraste 59 contra 20 **hace visible** el hueco que antes era
invisible.

**Ítem 3 — la expectativa que declaré era equivocada, y en la dirección
conservadora.** Escribí que el tope de 20/día es por modelo y que cambiar de
modelo *"compra otros 20, no más"*. Medido: **device B hizo 68 llamadas con 0
errores**. O sea que el límite diario de `gemini-3.5-flash-lite` es **≥ 68**, no
20 — el tope de 20/día que medí es de `gemini-2.5-flash` y **no se generaliza**.
device B dejó de ser intermitente: 7 INTERACT contra 11 en el intento 2, pero
con **0 errores** contra 69.

## 4. Tres primeras veces

**1. `calibrate` separó: `state: "calibrado"`.** Nunca había pasado en un vivo.

```
λ=0 : n_eff = 2.462144527883787   d_ckm = 0          frac_rec = 1
λ=1 : n_eff = 2.436944072133545   d_ckm = +0.011418  frac_rec = 0.98976
margen_separacion = +0.011418  →  CALIBRADO
D_CKM_THRESHOLD = 0.0057089516518649686
FRAC_REC_MIN    = 0.9948824174485196
```

Y separó **por donde la lectura del ítem 4 decía que podía separar**: en λ=1 la
matriz es **todo unos** y ya no depende de W, así que
`N_eff(λ=1) = 2.436944072133545` es una **constante** de N=20 y la seed —
aparece idéntica a 15 dígitos en tres mediciones independientes (la W de n=80
del intento 2, el registro del intento 2 y este vivo). La condición escrita era
*"mientras `N_eff(W) < 2.4369`, el margen es negativo por construcción"*; acá
`N_eff(W) = 2.4621 > 2.4369` por primera vez y el margen se dio vuelta.

**2. El criterio estructural votó.** Las 27 decisiones de rebuild: **26
`volumen` y 1 `estructural`**. En el intento 2 fueron 29 de 29 `volumen` y cero
estructural.

**3. COCO corrió con umbrales calibrados:** las últimas **3** de las 27
evaluaciones con `source: "calibrate"`, `calibrated: true`.

## 5. Lo que la calibración cambia, medido

Las 27 evaluaciones, por tramo:

| filas | `source` | `D_CKM_THRESHOLD` | `D_ckm` de COCO | zona |
|---|---|---|---|---|
| 0–23 | `default` | 0.40 | de −0.2796 a **+0.0465** | `stable` |
| 24–26 | `calibrate` | **0.00571** | 0.0, −0.0202, −0.0202 | `stable` |

**No hay contradicción:** el +0.0465 ocurrió bajo el umbral de 0.40, y los tres
valores bajo el umbral calibrado no lo cruzan (la comparación es **con signo**;
negativo significa más atractores que el baseline, que no es la dirección que
el umbral vigila).

**Y la aritmética del contrafáctico, que es el resultado:** si los umbrales
calibrados hubieran estado activos en las filas 1–3, `D_ckm` de COCO
(0.0329, 0.0438, 0.0465) habría sido **5,8× / 7,7× / 8,1× el umbral**, y
`frac_rec` (0.9761, 0.9682, 0.9663) habría estado **por debajo** de
`FRAC_REC_MIN = 0.99488`. Esas tres filas **no** habrían sido `stable`.

Es decir: **los `triggers: 0` de los intentos 2 y 3 son una propiedad del
default sin calibrar (0.40), no del campo.** El rango entero de `D_ckm` de COCO
en el intento 2 (0,18 de ancho) era **menos de la mitad** de ese umbral.

## 6. Los dos `D_ckm`, por separado

El intento 2 reportó uno solo, y eso era ambiguo: **son dos series con dos
baselines distintos** (señalado por delamor). El de Monitor sale de
`W_eff = W + Δ_r` y **se resetea cuando W cambia**; el de COCO sale de **W
sola** y se refija cuando renace su ciclo.

| | intento 2 (51 evals) | intento 3 (27 evals) |
|---|---|---|
| Monitor | [−0.0861, +0.0093] | **[−0.0202, +0.2335]** |
| COCO | [−0.1710, +0.0093] | **[−0.2796, +0.0465]** |
| filas donde difieren | 30 de 51 | **24 de 27** |

**La firma (`get_firma`) lleva el de Monitor** (`firma_ckm.py:116`), no el de
COCO. El que va contra `D_CKM_THRESHOLD` es el de COCO (`coco.py:294`).

## 7. Huecos del instrumento

**Nuevo: una carrera en el cierre.** El log dice `n_mensajes: 59` y `corpus_size:
55`; los archivos tienen **60 líneas y 56 textos**. El driver lee el registro
**antes** de que aterrice el último mensaje: `msg-59` se publicó a las
06:28:17, durante el cierre. Los dos números son correctos en su momento y
**ninguno de los dos es el final**. El del archivo sí.

**Y el último mensaje del canal fue `'.'`** — un carácter. Pasa el filtro (no
está vacío después del `strip()`) y **entra al corpus como un texto**, igual que
el `'2'` del intento 1. El panel declara `"unit": "el mensaje"`, así que es
coherente con lo declarado; la pregunta —si un `'.'` y un párrafo valen lo
mismo para W— es de delamor y sigue abierta.

Los tres de antes siguen igual: el aviso de truncamiento es un `print` (acá no
importó: hubo 0), `series`/`case` fuera de `monitor_trajectory.jsonl`, y la
línea de la decisión de rebuild no registra `textos_desde_rebuild` —que **sí**
está en el panel—.

## 8. Lo que este registro NO dice

- **No dice por qué hubo 56 textos y no 80.** Los OP_SILENCE subieron (38/54/43
  contra 21/1/20) y los INTERACT bajaron (55 contra 88). Qué de eso es del
  cambio de techo, qué del `reasoning_effort`, qué del modelo nuevo de B y qué
  de la varianza entre corridas, **no se separa con n = 1 de cada lado**.
- **No dice nada del `LEAVE` de `device_d` en su vuelta 2.** Se fue antes que en
  el intento 2 (vuelta 8), sin error, por decisión propia. Es del modelo.
- **No atribuye la respuesta de 374 caracteres** de device C en el gate.
- **No mide duplicación ni convergencia del contenido.** Para eso el
  instrumento propio es `activos_relajado` (nodos activos compartidos), no el
  ojo ni el `sha256`; no se corrió.
- **Una corrida por lado. Nada acá es replicación.**
