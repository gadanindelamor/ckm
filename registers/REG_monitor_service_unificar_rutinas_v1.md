# REG_monitor_service_unificar_rutinas_v1.md

*Sep 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

`MonitorService` pasa a usar las rutinas de muestreo y relajación de COCO,
eliminando la implementación paralela que tenía. Ejecutado según
`TASK_monitor_service_unificar_rutinas_v1.md`, opción **C** (copiar y
ajustar defaults, todo dentro de `monitor_service.py`) por decisión de
delamor: aísla la pregunta numérica de la arquitectónica.

Origen: desajuste identificado por delamor sobre `REG_wmixta_consolidado_v1`
— la condición `sin_thermostat` ejecuta rutinas propias de MonitorService,
con distribución de σ₀ uniforme hardcodeada.

Archivo modificado: `services/monitor_service.py` únicamente.
`coco.py` **no fue tocado**.

---

## Las cuatro divergencias — estado antes y después

| | antes | después |
|---|---|---|
| `_relax` `max_iter` | 100 | **200** (unificado) |
| seed del conteo | `default_rng(0)` hardcodeado | `count_seed`, **default 0** |
| distribución de σ₀ | uniforme hardcodeada | `sampling_mode`, **default `"uniform"`** |
| W sobre la que cuenta | `_combine_W_Delta(W, Δ_r)` | **sin cambio — sigue igual** |

Las tres primeras se unifican. **La cuarta se preserva deliberadamente**
(ver sección propia abajo).

---

## Implementado

En `services/monitor_service.py`:

- `_relax`: `max_iter` 100 → 200.
- `_node_probs`, `_beta_c_landscape`, `_sample_s0`, `_boltzmann_warmup`:
  copiados de `coco.py`.
- `_count_attractors(W, weighted=None, boltzmann=None, n_warmup=None)`:
  la rutina de COCO. Con los tres en `None` toma `self._sampling_mode`;
  pasarlos explícitos permite un conteo puntual en otro modo sin cambiar la
  configuración del servicio.
- Constructor: `count_seed=0`, `sampling_mode="uniform"`, `n_warmup=None`.
  `sampling_mode` inválido lanza `ValueError`.
- Panel: `panel["sampling_mode"]` — el del **Monitor**, distinto de
  `panel["thermostat"]["sampling_mode"]`, que es el de COCO. Son dos
  contadores independientes y ahora los dos declaran su modo.

**Única adaptación respecto de COCO:** allí `N` es fijo al construir
(`self.N`); acá W se reconstruye con el corpus, así que `N` sale de
`W.shape[0]` en cada llamada. Anotado en el bloque copiado.

**Contrato de firmas cumplido:** todo parámetro que la rutina de COCO tiene
y la de MonitorService no tenía es opcional o con default. Ningún sitio de
llamada existente cambió — los tres (`evaluate`, `_D_ckm`, el loop interno)
siguen pasando sólo `W`.

---

## Verificación

### 1. Tests

`tests/test_monitor_services.py` 35/35 · `tests/test_coco.py` 28/28 ·
`tests/test_firma_ckm.py` 10/10 · `tests/test_w_version.py` 9/9 ·
`python services/coco.py` T1–T13 OK. **Sin tocar ningún archivo de test.**

### 2. Replay contra la versión previa

24 textos de `caso09_run2`, régimen natural, `n_runs_attractors=50`.
Se corrió el `monitor_service.py` de `HEAD` y el nuevo sobre el mismo
corpus, comparando `D_ckm`, `c_S`, `fabrication_index`,
`n_rejected_pairs`, `Delta_r_sum` y `activos_relajado`:

**0 diferencias en las 24 evaluaciones, en los 6 campos.**
`Delta_r` final 632.0 en las dos versiones.

### 3. Replicación de las corridas completas — la verificación fuerte

Se re-ejecutaron los **dos drivers commiteados** (`test_wmixta_natural_paso2.py`
y `test_wmixta_forzado_paso3.py`) con el MonitorService unificado,
redirigiendo `OUT_DIR` para no pisar los resultados originales, y se
comparó archivo por archivo contra los resultados producidos con el
MonitorService **anterior**.

Se reutilizaron los drivers tal cual —importados y con `OUT_DIR`
reasignado— para que la replicación corriera el mismo código, no una
reimplementación.

| archivo | resultado |
|---|---|
| `wmixta_paso2_natural/result_natural_uniform.json` | IDÉNTICO |
| `wmixta_paso2_natural/result_natural_weighted.json` | IDÉNTICO |
| `wmixta_paso2_natural/result_natural_boltzmann.json` | IDÉNTICO |
| `wmixta_paso2_natural/result_natural_sin_thermostat.json` | IDÉNTICO |
| `wmixta_forzado_paso3/result_forzado_uniform.json` | IDÉNTICO |
| `wmixta_forzado_paso3/result_forzado_weighted.json` | IDÉNTICO |
| `wmixta_forzado_paso3/result_forzado_boltzmann.json` | IDÉNTICO |
| `wmixta_forzado_paso3/result_forzado_sin_thermostat.json` | IDÉNTICO |

**8 archivos, 2152 comparaciones, 0 diferencias.**
(8 × [24 evaluaciones × 11 campos + 5 campos de cabecera].)

Campos comparados por evaluación: `D_ckm_panel`, `D_ckm_coco`, `A_actual`,
`A0`, `frac_rec`, `zone`, `stop_applied`, `alpha_used`, `delta_A`,
`Delta_r_sum`, `c_S`. De cabecera: `n_stops`, `W_neg`, `W_pos`, `N`,
`n_texts`.

**Nota sobre el alcance de esta verificación.** Antes de correrla se
anticipó que los campos del lado de COCO (`D_ckm_coco`, `A_actual`, `zone`,
`alpha_used`) coincidirían "por construcción" al no haberse tocado
`coco.py`. **Eso era incorrecto.** Esos campos salen de COCO observando
`Δ_r`, y `Δ_r` la produce el `_relax` de MonitorService vía los pares
rechazados. Si el trasplante hubiera alterado la relajación, `Δ_r` habría
cambiado y los valores de COCO con ella. Son verificación genuina, indirecta
pero real — la replicación cubre más de lo previsto, no menos.

### 4. El modo está conectado, no es decorativo

Sobre `_combine_W_Delta(W, Δ)` del corpus natural, `n_runs=50`:

| `sampling_mode` | A | COCO(seed=0) equivalente |
|---|---:|---:|
| `uniform` | 24 | 24 |
| `weighted` | 23 | 23 |
| `boltzmann` | 16 | 16 |

Los tres modos dan conteos distintos —el parámetro opera— y los tres
coinciden exactamente con COCO sobre la misma W.

---

## Lo que se preserva: la W sobre la que cuenta cada instrumento

`_combine_W_Delta` **no fue tocada**, por decisión explícita. La divergencia
que sostiene no es un defecto a corregir: es lo que distingue a los dos
instrumentos.

```
COCO:            W_eff = W + Δ_r
MonitorService:  W_eff = W + (Δ_r / max(Δ_r)) · mean(W>0)
```

Medido sobre el corpus natural de `caso09_run2`:

**Invariancia de escala.** Multiplicando Δ_r por un factor k:

| k | COCO `A(W+kΔ)` | Monitor `A(combine)` |
|---:|---:|---:|
| 0.05 | 30 | **24** |
| 1 | 27 | **24** |
| 100 | 32 | **24** |
| 10⁶ | 32 | **24** |

`Δ_r/max(Δ_r)` es una proyección: colapsa toda la semirrecta
`{λ·Δ_r : λ>0}` a un representante. Como `OPERADOR_STOP_COCO` es
exactamente `Δ_r ← α·Δ_r` con α>0, opera **dentro** de esa clase de
equivalencia. El Monitor mide sobre el cociente.

**Efecto de STOP**, α ∈ [0.05, 0.30]:

| α | COCO | Monitor |
|---:|---:|---:|
| 0.30 | 33 | **24** |
| 0.05 | 30 | **24** |

El `D_ckm` del panel no puede ver STOP. No es baja sensibilidad —
es cancelación algebraica exacta.

**Cota estructural.** El factor `· mean(W>0)` acota el aporte máximo de Δ_r
al paisaje del Monitor, y la cota **no depende de cuánto acumule Δ_r**:

| Δ_r × | aporte máximo de Δ_r | max\|W\| |
|---:|---:|---:|
| 1 | 0.5758 | 1.000 |
| 10 | 0.5758 | 1.000 |
| 1000 | **0.5758** | 1.000 |

En el paisaje del Monitor, Δ_r **nunca puede dominar a W**: el techo lo fija
la propia W. En COCO no hay cota y `W + Δ_r` puede cruzar al régimen donde
la perturbación supera al acoplamiento.

**Resumen de qué mide cada uno:**

| | COCO | MonitorService |
|---|---|---|
| ve la escala de Δ_r | sí | **no** |
| ve la forma de Δ_r | sí | sí, módulo escala |
| ve el efecto de STOP | sí | **no** |
| Δ_r puede dominar W | sí | **no** |

**Monitor observa la dirección de Δ_r; COCO observa dirección y magnitud.**
Un regulador tiene que ver aquello sobre lo que actúa; un observador que
viera lo mismo dejaría de ser independiente del regulador. Monitor no domina
ni regula. COCO sí.

Los dos `W_eff` son simétricas y de diagonal cero — `_combine_W_Delta`
preserva ambas, porque escalar no rompe simetría.

---

## Lo que este REG no establece

- **No establece que la unificación mejore nada.** Establece que no cambia
  nada: 2152 comparaciones sin una diferencia. El valor es sacar la
  duplicación y dar capacidad de modo, no mejorar una medición.
- **No cierra la duplicación de raíz.** La opción C copia el código: ahora
  hay dos implementaciones sincronizadas a mano en `services/`, más las de
  `experiments/` y `fabrication_service.py`. Es el patrón que produjo este
  desajuste. La opción A —extraer a módulo compartido— sigue pendiente y
  requiere autorización para tocar `coco.py`.
- **`fabrication_service.py` tiene una tercera copia de `_relax`**
  (líneas 74 y 85), y una de las dos lo llama con **un solo argumento** —
  otra firma distinta. Fuera del alcance de esta task; anotado.
- **No verifica la unificación fuera de `caso09_run2`.** Dos regímenes del
  mismo corpus, `n_runs=50`. Otros corpus no se probaron.
- **No toca `_combine_W_Delta`.** Es deliberado, no pendiente.
- **Sin commit.**

---

## Archivos

- `services/monitor_service.py` — modificado
- `iap_chatroom/tests/TASK_monitor_service_unificar_rutinas_v1.md` — spec
- `process/experiments/replica_unificacion/` — resultados de la replicación
- `registers/REG_wmixta_consolidado_v1.md` — origen del desajuste
- `registers/REG_wmixta_natural_paso2_v1.md`, `REG_wmixta_forzado_paso3_v1.md` — corridas replicadas

---

*Sep 2026 — Codespace ckm — bash/Linux*
