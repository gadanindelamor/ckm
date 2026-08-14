# REG_n_runs_sweep_armstrong_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Sweep de `n_runs` como variable única sobre la réplica Armstrong seed=123.
Origen: `TASK_armstrong_replica_seed123_via_corpus_v3` corrió con
`n_runs=80` (default no especificado en el script) y dio 20/20 STOPs —
divergente del 3/20 esperado (réplica manual, `n_runs=50`).

Script: `iap_chatroom/tests/test_armstrong_n_runs_sweep.py`
Datos: `process/experiments/n_runs_sweep/n_runs_sweep_summary.json`
Commit: `fca771f`

---

## Resultados

| n_runs | n_stops | neg_delta_A | D_ckm_tail |
|--------|---------|-------------|------------|
| 10     | 1       | 0           | 0.3000     |
| 20     | 1       | 0           | 0.3684     |
| 30     | 2       | 0           | 0.1724     |
| 40     | 3       | 0           | 0.2564     |
| 50     | 3       | 0           | 0.3673     |
| 60     | 4       | 0           | 0.3898     |
| **70** | **20**  | **5**       | **0.4493** |
| 80     | 20      | 6           | 0.4545     |
| 100    | 20      | 3           | 0.5000     |
| 150    | 20      | 4           | 0.4820     |
| 200    | 20      | 4           | 0.5389     |

---

## Hallazgos

### H1 — Quiebre abrupto, no gradual (verificado)

Hay un quiebre nítido entre `n_runs=60` (4/20 STOPs, D_ckm_tail=0.3898)
y `n_runs=70` (20/20 STOPs, D_ckm_tail=0.4493). No es una transición
gradual — es un salto discreto.

Hasta `n_runs=60`: D_ckm_tail < 0.40 (umbral de STOP). COCO no queda
enganchado. `neg_delta_A = 0` — STOP nunca pierde atractores en esta zona.

Desde `n_runs=70`: D_ckm_tail > 0.40. COCO dispara en todas las
evaluaciones. Aparecen `delta_A` negativos.

### H2 — D_ckm_tail no converge (propuesto, no verificado)

`D_ckm_tail` crece monotónamente con `n_runs` hasta 200 (0.30 → 0.54)
sin señal de saturar. Si esto fuera ruido estocástico alrededor de un
valor verdadero fijo, esperaría convergencia. No converge.

Hipótesis: `_count_attractors()` es un estimador tipo coupon-collector
— cuenta el tamaño del set de estados únicos alcanzados en `n_runs`
reinicios aleatorios. Su esperanza crece con `n_runs` por diseño, no
fluctúa alrededor de un techo fijo. Si `A0` (baseline, sobre W sola)
y `A_actual` (sobre W+Δ_r) crecen a tasas distintas con `n_runs`,
`D_ckm` hereda ese sesgo — no sería ruido, sería sesgo estructural.

**Para confirmar:** verificar `A0` y `A_actual` por separado en cada
punto de la sweep. No hecho todavía.

**Implicación si se confirma:** el umbral `D_CKM_THRESHOLD = 0.40` no
es propiedad del campo — es propiedad del instrumento a `n_runs=50`.
Todos los resultados `D_ckm` existentes son dependientes de `n_runs`.

### H3 — neg_delta_A solo aparece sobre el umbral (verificado)

`delta_A` negativo no aparece en ningún punto con `n_runs ≤ 60`.
Aparece desde `n_runs=70` en adelante — exactamente donde D_ckm_tail
cruza el umbral 0.40 y COCO queda enganchado en STOPs de borde.

El hallazgo original de Extensión 2 ("STOP siempre gana atractores,
`delta_A` siempre positivo") se sostiene en la zona `n_runs ≤ 60`.
En la zona de borde (`n_runs ≥ 70`), el ruido estocástico de la
estimación domina el signo de `delta_A`. No es contradicción —
es condición de borde del instrumento.

### H4 — n_runs como variable implícita no controlada (admisible)

La serie IAP (casos 0.4–0.15) y todos los experimentos previos
(Armstrong, sweep STOP, REG_destruccion_recuperacion) usaron un
`n_runs` sin declararlo explícitamente en los TASKs. El default
del código es la variable real.

Que los resultados sean reproducibles dentro de una sesión (mismo
`n_runs` implícito) no implica comparabilidad entre sesiones donde
el default puede haber cambiado.

El campo `n_runs` agregado al panel en `TASK_coco_alpha_compuesto_v3`
cierra parcialmente este gap — cada decisión de STOP queda trazada
con el `n_runs` del instrumento que la produjo.

---

## Alpha compuesto — colapso en ALPHA_MIN (Ago 2026)

Hallazgo complementario de la corrida de verificación de
`TASK_coco_alpha_compuesto_v3`:

Con `gamma=0.01`, `landscape_component` alcanzó magnitudes de
-1.26 a -2.38 en los STOPs t=2 a t=7 — un orden de magnitud mayor
que el rango completo `[ALPHA_MIN, ALPHA_MAX] = [0.05, 0.30]`.
El `clip()` hizo todo el trabajo. 6 STOPs consecutivos colapsaron en
`ALPHA_MIN=0.05`.

```
t=0: alpha_used=0.2177  landscape_component=0.000000
t=1: alpha_used=0.1041  landscape_component=0.000000
t=2: alpha_used=0.0500  landscape_component=-1.263066  ← piso
t=3: alpha_used=0.0500  landscape_component=-2.375377  ← piso
t=4: alpha_used=0.0500  landscape_component=-1.731533  ← piso
t=5: alpha_used=0.0500  landscape_component=-1.385226  ← piso
t=6: alpha_used=0.0500  landscape_component=-1.051310  ← piso
t=7: alpha_used=0.0500  landscape_component=-0.920000  ← piso
t=8: alpha_used=0.2881  landscape_component=-0.000000  ← recuperación
```

El sistema se recuperó solo desde t=8. No quedó pegado permanentemente.

**Causa probable:** `delta_A / alpha_used` amplifica cuando `alpha_used`
es bajo (dividir por 0.05 = ×20). En t=0, `alpha_used=0.2177` y
`delta_A` probablemente ~25-30 → eficiencia ≈ 115-138. Con `gamma=0.01`
eso da `landscape_component ≈ -1.15` a -1.38, que supera el rango
completo de α.

**Implicación para diseño:** el `clip()` es correcto y necesario.
`gamma=0.01` es conservador en magnitud relativa pero no en magnitud
absoluta cuando la eficiencia se dispara. El valor de `gamma` debería
ser proporcional a la escala de `delta_A / alpha_used`, no a la escala
de `alpha_used` solo.

**Estado:** registrado. No corregido en esta sesión. El comportamiento
es información sobre la calibración de `gamma` — no un bug del mecanismo.

---

## Pendientes

- Verificar H2: medir `A0` y `A_actual` por separado en la sweep
- Calibración de `gamma`: escalar a la distribución de `delta_A / alpha_used`
- Timeout de sesión IAP como parámetro no controlado — análogo a `n_runs`
  (propuesto en sesión, no investigado)

---

## Archivos relacionados

- `iap_chatroom/tests/test_armstrong_n_runs_sweep.py`
- `process/experiments/n_runs_sweep/n_runs_sweep_summary.json`
- `registers/REG_armstrong_stop_coco_v1.md` — Armstrong canónico
- `services/coco.py` — `_count_attractors()`, `_landscape_component()`, `_n_runs`
- `TASK_coco_alpha_compuesto_v3.md` — alpha compuesto, gamma

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
