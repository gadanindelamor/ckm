# REG_armstrong_boltzmann_comparison_v1.md

*Ago 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

Experimento Armstrong corrido con los tres modos de muestreo de σ₀ de COCO
(`uniform` / `weighted` / `boltzmann`) más un baseline sin thermostat, con
`n_runs = 200` fijo en **los dos** contadores. Única variable: el modo de σ₀.

Spec: `TASK_armstrong_boltzmann_comparison_v1.md`.
Driver: `iap_chatroom/tests/test_armstrong_boltzmann_comparison.py` — nuevo,
patrón de `test_armstrong_n_runs_sweep.py`. **`test_armstrong_stop_coco.py`
no fue modificado**: se importa y se reusan `WARMUP_TEXTS` y `TEXTS`.
Datos: `process/experiments/boltzmann_comparison/comparison_20260830T181555.json`.

**Los dos `n_runs` en 200** (decisión de delamor): `COCO._n_runs` y
`MonitorService._n_runs_attractors`. Son contadores independientes con
implementaciones distintas — el de MonitorService
(`monitor_service.py:276`) tiene `default_rng(0)` hardcodeado, no acepta
modos, y normaliza con `_combine_W_Delta`. Se registran los dos D_ckm por
evaluación.

**Nota de trazabilidad (agregada Sep 2026, no altera el cuerpo).** Esta
corrida se ejecutó con `TEXTS` conteniendo dos typos accidentales —
`Structuralf` (i=12) y `devicfe` (i=19)—, introducidos por cambio de foco de
panel entre entornos y revertidos después de la corrida. Impacto medido: el
primero es inocuo (el extractor sigue activando `structural`, 12 nodos con y
sin typo); el segundo hace perder el nodo `device` en esa evaluación — 13
nodos activos en vez de 14. Afecta la última de las 20 evaluaciones. El
archivo en el repo ya no los contiene, así que re-ejecutar este driver hoy
no reproduce exactamente el i=19 de estos datos.

**La comparación no es pareada.** El calentamiento Boltzmann consume
tiradas extra del RNG, así que con la misma semilla la secuencia de σ₀
diverge de la de `uniform` desde el primer run. Mismo seed ≠ mismos σ₀.

Corpus: `WARMUP_TEXTS` (20 textos) → **N=20**, densidad de W = 0.126,
valores no-nulos ∈ {0.5, 1.0}. 20 evaluaciones Armstrong.

---

## Resultado principal — el modo de muestreo decide cuántos STOP ocurren

| condición | STOPs | A0 | A_final | D_ckm final | zona a partir de i=4 |
|---|---:|---:|---:|---:|---|
| uniform | **20/20** | 174 | 71 | 0.5920 | `deep` |
| weighted | **4/20** | 94 | 64 | 0.3191 | `stable` |
| boltzmann | **20/20** | 173 | 93 | 0.4624 | `deep` |
| sin thermostat | 0/20 | — | — | — | — |

Mismo corpus, mismos textos, mismo seed, mismo `n_runs`. **Cambiando sólo
la distribución de la que se sortea σ₀, COCO pasa de comprimir Δ_r en las
20 evaluaciones a hacerlo en 4.**

`weighted` dispara STOP en i=0,1,2,3 y a partir de i=4 el campo queda
clasificado `stable`. Los otros dos nunca salen de `deep`.

---

## Por qué — la cuenta cierra exactamente

`D_ckm = (A0 − A_actual)/A0`, con `D_CKM_THRESHOLD = 0.40`:

| modo | A0 | A_actual | (A0−A)/A0 | vs 0.40 |
|---|---:|---:|---:|---|
| uniform | 174 | 71 | **0.5920** | encima → STOP |
| weighted | 94 | 64 | **0.3191** | **debajo → sin STOP** |
| boltzmann | 173 | 93 | **0.4624** | encima → STOP |

Los tres `A_actual` saturan en un valor parecido (64–93). Lo que separa a
`weighted` de los otros dos **es su A0 más bajo** (94 contra 174/173). El
modo no cambia tanto lo que mide del campo perturbado; cambia el
**denominador**.

---

## Hallazgo — A0 está inflado por empates, y el mecanismo es verificable

`COCO._relax` conserva σ_i cuando el campo local es exactamente cero:

```python
s2 = np.where(h > 0, 1., np.where(h < 0, -1., sigma))
```

En este corpus eso no es un caso de borde: W tiene **332 ceros exactos
fuera de la diagonal** (densidad 0.126) y sólo dos valores no-nulos
(0.5 y 1.0), así que **el 33.6% de los h son exactamente 0** en el primer
paso. Los nodos empatados quedan congelados en su valor de σ₀ y viajan
hasta el estado terminal.

Medido sobre la misma W, `n_runs=200`, seed=42:

| regla de empate | count(W) |
|---|---:|
| conservar σ (la actual) | **174** |
| resolver a +1 | 61 |
| resolver a −1 | 60 |

**A0 = 174 no cuenta 174 cuencas: cuenta en buena medida diversidad de σ₀
propagada por coordenadas congeladas.** Con los empates resueltos, el mismo
paisaje da ~60. El factor es ~3.

Esto le da mecanismo concreto a la observación ya declarada en
`DEFS_CKM_estado_actual_v7.md` §11 — que el modo uniforme puede estar
midiendo velocidad de expulsión y no diversidad. El mecanismo es **el
empate**, no sólo la distribución de σ₀.

---

## Hallazgo — cualquier Δ_r ≠ 0 rompe los empates, y ahí satura

Agregando a W una Δ_r de forma fija y magnitud decreciente:

| W_eff | count |
|---|---:|
| W + 1.0·D | 6 |
| W + 0.30·D | 23 |
| W + 0.05·D | 62 |
| W + 1e−6·D | 65 |
| W + 1e−14·D | **64** |
| W (sin D) | **174** |

Entre 1e−14 y 1e−6 el conteo no se mueve: **por debajo de ~0.05 lo único
que hace Δ_r es romper empates**, y romperlos cuesta lo mismo con
magnitud 1e−14 que con 1e−6. Por encima de 0.05, Δ_r sí compite con W y
el conteo cae de verdad (62 → 23 → 6).

`ALPHA_MIN`–`ALPHA_MAX` = [0.05, 0.30] cae justo en la zona donde la
compresión todavía tiene efecto real.

---

## Consecuencia — el estado absorbente de COCO en modo uniforme

Trayectoria de `Δ_r.sum()` en la corrida `uniform`:

| i | 0 | 1 | 2 | 3 | 5 | 10 | 19 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Δ_r.sum() | 24.0 | 95.5 | 7.98 | 0.399 | 1.0e−3 | 1.0e−8 | **1.4e−14** |

Después de ~5 STOPs Δ_r está numéricamente muerta. Pero **su soporte sigue
siendo el mismo** — STOP multiplica por α, y multiplicar por un escalar no
puede cambiar qué entradas son distintas de cero. Como en ese régimen el
conteo depende del soporte y no de la magnitud, `A_actual` queda clavado en
~64–71 y `D_ckm` en ~0.59: siempre por encima de 0.40.

**COCO no puede salir de la zona `deep`.** Sigue aplicando STOP en las 20
evaluaciones sobre una Δ_r que ya no cambia nada. El piso de D_ckm en modo
uniforme es (174−64)/174 = **0.632**, estructuralmente por encima del
umbral.

`weighted` escapa por la única vía disponible: bajando A0.

Esto **no contradice** "OPERADOR_STOP_COCO nunca produce pérdida"
(`frac_rec ≥ 1.0`, `REG_destruccion_recuperacion_v1`). Lo reencuadra: en
este corpus, pasado cierto punto, tampoco produce ganancia — produce nada.
`delta_A < 0` en 4/20 STOPs (uniform), 6/20 (boltzmann), 0/20 (weighted).

---

## Hallazgo — el D_ckm del panel no puede ver a STOP

`D_ckm` del panel de MonitorService, por evaluación:

| i | uniform | weighted | boltzmann | sin thermostat |
|---|---:|---:|---:|---:|
| 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 1–19 | **0.8857** | **0.8857** | **0.8857** | 0.9143 |

Idéntico en los tres modos, en las 20 evaluaciones — mientras `Δ_r.sum()`
difiere entre ellos por **catorce órdenes de magnitud** (1.4e−14 contra
1.9e−2).

La causa está en `_combine_W_Delta`, que normaliza `Δ_r / max(Δ_r)` antes
de combinar. STOP es exactamente `Δ_r ← α·Δ_r`, un escalado uniforme — y
dividir por el máximo lo cancela por construcción. **El D_ckm del panel es
invariante a la compresión que COCO aplica.** No es saturación ni ruido: es
una cancelación algebraica exacta.

La diferencia con `sin_thermostat` (0.9143) no viene de la magnitud sino de
la **forma**: sin STOP, los rechazos posteriores se acumulan sobre una Δ_r
distinta, y el soporte resultante difiere.

Consecuencia práctica: en la traza persistida, el `D_ckm` del panel y el
`D_ckm` del thermostat responden a cosas distintas. **No son la misma
cantidad medida dos veces.**

---

## Lo que este REG no establece

- **Cuál modo mide mejor.** Cuarta vez que se registra. Sin conteo
  exhaustivo no hay referencia. Lo que sí queda establecido es que la
  elección de modo **decide el número de STOPs** en corpus real — deja de
  ser un parámetro interno del instrumento.
- **Que A0 con empates esté "mal".** Está medido que infla el conteo ~3× y
  que el mecanismo es el empate. Si conservar σ en h=0 es la regla correcta
  para CKM es una decisión del modelo, no de esta corrida. La regla actual
  es además la que hace válida la garantía Lyapunov/LaSalle citada en
  DEFS §4 — cambiarla no es un ajuste local.
- **Que esto generalice más allá de N=20 / `WARMUP_TEXTS`.** La densidad
  0.126 y los dos únicos valores no-nulos son lo que hace los empates tan
  frecuentes. Un corpus más denso o con pesos más variados tendría menos
  empates y el efecto sería otro. No se midió.
- **Nada se cambió en el código.** `sampling_mode` sigue en `"uniform"` por
  default; `_combine_W_Delta`, `_relax`, `D_CKM_THRESHOLD` y la lógica de
  STOP quedaron intactos. Sin commit.

---

## Archivos

- `iap_chatroom/tests/test_armstrong_boltzmann_comparison.py` — driver (nuevo)
- `process/experiments/boltzmann_comparison/` — 4 corpus, 4 trayectorias, 1 JSON de resultados
- `registers/REG_boltzmann_sampling_v1.md` — implementación del modo boltzmann + addendum de corrección
- `registers/REG_stochastic_eval_v2.md` — sensibilidad de D_ckm al modo, a n_runs fijo
- `registers/REG_h2_a0_vs_aactual_v1.md` — A0 vs A_actual bajo uniforme
- `iap_chatroom/tests/TASK_armstrong_boltzmann_comparison_v1.md` — spec

---

*Ago 2026 — Codespace ckm — bash/Linux*
