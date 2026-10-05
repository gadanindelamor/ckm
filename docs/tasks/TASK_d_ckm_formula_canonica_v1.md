# TASK_d_ckm_formula_canonica_v1.md

*Oct 2026 — gadanin.delamor + Claude Code (Opus 5.5)*
*Continúa `TASK_d_ckm_al_engine_v1`. Ejecuta lo que esa task dejó anotado en "Abierto": "reemplazaremos D_ckm por N_eff, o como se llame en el engine; el nombre queda" (delamor).*

**Esta task se escribió el 5 oct 2026 con los pasos 1 a 4 ya aplicados en el árbol de trabajo, sin commit.** La sesión empezó como revisión de cambios de delamor y siguió con cambios pedidos por él en el momento. El documento registra lo hecho, cómo se verificó y lo que falta. Quien la retome empieza por "Estado".

---

## Qué hacer

Que `D_ckm` sea, en el código, la fórmula canónica:

```
D_ckm = 1 − ln N_eff / ln N_eff0          N_eff = 1 / Σ m²
```

con `m` las masas de cuenca por órbita (`basin_masses`). La forma lineal por conteo, `(A0 − A) / A0`, deja de ser lo que el código calcula.

*(delamor: "me tengo que asegurar que definitivamente el código haga lo que definimos. Después póngale d_ckm o d_cuencas, no me importa, mientras haga lo que DEBE.")*

Los nombres se conservan por regresión. `A_actual`, `A_current` y `A0` **son** `N_eff` y `N_eff0`: sólo se llaman distinto.

## Alcance

**Entra:** `services/landscape_engine.py`, `services/coco.py`, `services/monitor_service.py`, `services/firma_ckm.py`, `tests/test_coco.py`, `tests/test_neff_y_frontera.py`.

**No entra:**
- Los umbrales de COCO (`D_CKM_THRESHOLD = 0.40`, `FRAC_REC_MIN = 0.60`) y el dominio de `_alpha_for`. Se calibraron sobre la forma lineal (REG_destruccion_recuperacion_v1) y quedan como están. Ver "Abierto".
- De dónde sale A0. Sigue siendo una cantidad con dos baselines: COCO sobre `self.W` sola y sin reset, Monitor sobre W + Δ_r y con reset. La decisión de `TASK_d_ckm_al_engine_v1` (A0 lo define `CKMlandscapeConfig`) no se ejecuta acá.
- Los nombres. `ThermostatState` no se renombra: `TASK_refactoring_coco_device_v1` R1 lo fija. COCO es regulador, no termostato (REG_sesion_coco_endogeno_v2 §1); en texto nuevo se escribe así.
- `experiments/` y `process/`, salvo lo que el paso 6 declare.

## Estado

| Paso | Qué | Estado |
|---|---|---|
| 1 | `d_ckm` delega en `d_masa_cuencas`; la forma lineal queda en `deprecated_d_ckm` | aplicado (delamor) |
| 2 | Tipos: `_A0`, `A_current`, `A0` anotados `float`; `count_attractors` devuelve `float` | aplicado |
| 3 | `count_attractors` devuelve `n_eff(basin_masses(...))`; el conteo queda en `deprecated_count_attractors` | aplicado |
| 4 | Borde `None` en los cuatro consumidores | aplicado |
| 5 | El test de alpha afirma lo que el código hace, con los dos renglones en el docstring | aplicado (decisión de Code) |
| 6 | Driver de línea de base acepta `None`; base nueva al lado de la anterior | aplicado (decisión de Code) |
| 7 | `condicion_W` declara la forma de `D_ckm` | aplicado (decisión de Code) |
| 8 | REG | **pendiente** |
| — | Calibración y umbrales de COCO | **de delamor** |

Suite: `bash tests/run_tests.sh` → **183 pasan, 0 sin pasar**. `python tests/test_coco.py` → 30 pasan.

*(delamor, 5 oct: "calibrar y umbrales, esto me interesa; el resto delego a vos la decisión, pero la responsabilidad continúa en mí. TRUST no verifica transitividad como ley.")* Los pasos 5 a 7 los decidió Code bajo esa delegación. Cada decisión está abajo con su razón, para que se pueda revisar.

## Los pasos

### Paso 1 — `d_ckm` es la forma logarítmica *(delamor)*

`landscape_engine.d_ckm(A_actual, A0)` devuelve `d_masa_cuencas(A_actual, A0)`. La función anterior quedó entera como `deprecated_d_ckm`, con su docstring.

### Paso 2 — tipos

`count_attractors` devolvía `len(attractors)`, un `int`, y los wrappers de COCO y Monitor anotaban `-> int`. Con `_A0` y `A_current` anotados `float`, en ejecución seguían siendo `int`. Ahora la función devuelve `float` y las anotaciones coinciden.

### Paso 3 — `A_actual` es N_eff

Con el paso 1 solo, `d_ckm` aplicaba la fórmula de masa a conteos: `1 − ln(conteo) / ln(conteo_0)`. No era ni la forma anterior ni la canónica.

`count_attractors` pasó a devolver `n_eff(basin_masses(...))`, con el mismo muestreo (misma seed, mismas σ₀). Sin tocar los llamadores, todo lo que sale de ahí es N_eff: `A_actual`, `A_current`, `A0`, y también `frac_rec`, `A_antes`, `A_despues` y `delta_A` de COCO.

Dos diferencias con el conteo, además del valor: agrupa por **órbita** y no por estado terminal (una órbita de período 2 es una entrada, no dos), y pesa cada órbita por su masa.

El conteo de estados terminales distintos sigue disponible como `deprecated_count_attractors`.

**Consecuencia en Monitor:** el panel lleva el mismo número en `"D_ckm"` y en `"D_masa_cuencas"`.

### Paso 4 — el borde `None`

`d_ckm` devuelve `None` cuando el baseline es ≤ 1: con una sola cuenca efectiva de partida no hay distancia que medir. La forma anterior devolvía `0.0` en su borde, que dice "sin cambio" donde no hubo medición. `TASK_d_ckm_al_engine_v1` lo había dejado como decisión aparte; acá queda tomada por el paso 1.

| Consumidor | Con `D_ckm = None` |
|---|---|
| `COCO._classify_zone` | zona `"stable"`: sin medición no se aplica STOP |
| `ThermostatState.D_ckm` | `None` |
| Panel de Monitor, clave `"D_ckm"` | `None` |
| `MonitorService.stop_signal` | sin señal si falta un extremo de la ventana; `"D_trend": None` |
| `Firma.d_ckm` | `None` |

Antes de este paso, `observe()` de COCO levantaba `TypeError` con baseline 1.

### Paso 5 — el test de alpha

`tests/test_coco.py::TestSimulationAnchor::test_alpha_at_threshold_is_alpha_max` arma un Δ que en la simulación llevaba `D_ckm` al umbral y espera `alpha ≈ ALPHA_MAX`.

| Sobre ese Δ (W_mixta AMP=40, n_runs=80, seed=0) | A0 | A | D_ckm | zona | alpha |
|---|---|---|---|---|---|
| Conteo, forma lineal | 20 | 12 | 0.400 | degrading | 0.30 |
| N_eff, forma canónica | 6.77 | 2.53 | 0.515 | deep | 0.252 |

El código hace lo que la fórmula dice. Lo que ya no vale es que ese Δ caiga en el umbral.

**Decisión (Code):** el test pasó a llamarse `test_alpha_sale_de_D_ckm_sobre_el_Delta_de_la_simulacion`. Afirma `D_ckm = 0.515`, que hubo STOP, y que `alpha_used` es el que sale de hacer a mano la interpolación con `D_CKM_THRESHOLD`, `ALPHA_MAX` y `ALPHA_MIN` (0.252). Los dos renglones de la tabla están en su docstring.

**Razón:** dejarlo sin pasar mantenía la suite en un estado que no distingue esta diferencia conocida de una nueva. Y no afirma nada sobre dónde *debería* caer ese Δ: eso es calibración. Si los umbrales cambian, este test se mueve y lo dice.

### Paso 6 — el driver de línea de base

`experiments/baseline_d_ckm.py --comparar experiments/baseline_d_ckm.json` se detiene en la línea 102: hace `float(s.D_ckm)` y COCO devuelve `None` en el caso weighted / seed 42.

**Decisión (Code):**
- La línea 102 acepta `None`.
- La base anterior, `experiments/baseline_d_ckm.json`, se conserva sin tocar: es la referencia de `TASK_d_ckm_al_engine_v1`. El código de hoy da 39 diferencias contra ella, que es lo esperado.
- Base nueva al lado: `experiments/baseline_d_ckm_canonica.json`. `--comparar` contra ella da cero diferencias.
- `experiments/driver_W_corpus_informes.py:93`: la columna `A_{n_runs}` es de conteo y se imprime como entero; pasó a `int(deprecated_count_attractors(...))`. **Ese driver no se corrió**, sólo se verificó que parsea.

Nota de ubicación: esa task dice que la base está en `process/baseline_d_ckm/base.json`. Mirando desde la raíz del repo el 5 oct, ese directorio no existe; el archivo está en `experiments/baseline_d_ckm.json`.

### Paso 7 — declarar la cantidad en `condicion_W`

Los paneles históricos llevan la forma por conteo bajo la clave `"D_ckm"`; los nuevos llevan la canónica bajo la misma clave. `TASK_d_ckm_al_engine_v1` ya lo pedía: "la cantidad declarada en la config o en `condicion_W`, porque los 253 paneles históricos llevan la de conteo bajo la misma clave".

**Decisión (Code):** `landscape_engine.D_CKM_FORMA = "masa_log"`, y `condicion_W` de cada panel lo lleva bajo `"D_ckm_forma"`. Un panel **sin** esa clave es de la forma por conteo. Cubierto en `test_panel_declara_condicion_W`.

**Lo que no hace:** `stop_signal` resta `D_ckm` entre extremos de una ventana y no mira `"D_ckm_forma"`. Una ventana que cruce el 5 oct sigue restando dos cantidades distintas; ahora es detectable, no está impedido.

### Paso 8 — REG

Después de la calibración de umbrales, para que registre el cierre completo y no la mitad. Borrador fuera de `registers/`.

## Verificación

**Tests que hacen la cuenta a mano.** Calculan `1 / Σ m²` y el logaritmo desde `basin_masses` y comparan con lo que devuelve el código, sin llamar a `n_eff` ni a `d_masa_cuencas` para el valor esperado:

- `test_count_attractors_es_n_eff_sobre_masas`
- `test_d_ckm_es_la_formula_canonica_sobre_masas`
- `test_panel_D_ckm_es_la_formula_canonica`: en el panel, `D_ckm` sale de los `N_eff` y `N_eff0` del mismo panel y es igual a `D_masa_cuencas`.
- `TestSimulationAnchor::test_D_ckm_es_la_formula_canonica`: `observe()` devuelve `A0`, `A_current` y `D_ckm` iguales a la cuenta a mano, sin tocar nada privado de COCO.
- `TestZoneClassification::test_D_ckm_None_is_stable`
- `test_d_ckm_es_d_masa_cuencas`: valores y borde.

**Tests movidos al nombre `deprecated_`**, con la razón en el docstring de cada uno: los cuatro de la operación lineal, el de órbitas contra terminales, y el ancla histórica A0 = 20 (que sigue verificada como conteo; sobre la misma W, N_eff0 = 6.7653).

**Test con literales cambiados:** `TestSTOP::test_degrading_zone_stop_applied` pasó de A0 = 10, A = 5 a A0 = 4, A = 2, que con la forma logarítmica vuelve a dar 0.5. Con esos valores la zona es "deep", no "degrading"; el test ya aceptaba las dos.

**Medición con el driver** (mismas mediciones de `baseline_d_ckm.py`, sin la conversión de la línea 102, corridas fuera del repo):

COCO, `W_ckm_corpus_v2`, N = 32, n_runs = 50:

| Modo | Seed | Base: A0 → A | Base: D_ckm | Ahora: N_eff0 → N_eff | Ahora: D_ckm |
|---|---|---|---|---|---|
| uniform | 0 | 2 → 32 | −15.0 | 1.99 → 15.82 | −3.02 |
| uniform | 42 | 2 → 31 | −14.5 | 1.97 → 14.53 | −2.94 |
| weighted | 0 | 2 → 29 | −13.5 | 1.04 → 9.40 | −55.03 |
| weighted | 42 | 1 → 34 | −33.0 | 1.00 → 14.71 | `None` |
| boltzmann | 0 | 2 → 27 | −12.5 | 2.00 → 12.89 | −2.70 |
| boltzmann | 42 | 2 → 22 | −10.0 | 2.00 → 10.25 | −2.36 |

Zona "stable" y sin STOP en los seis, antes y ahora.

Monitor, 9 evaluaciones: `N_eff`, `c_S`, `fabrication_index`, `Delta_r_sum` y `activos_relajado` idénticos a la base. `D_ckm = 0.0` en 8, igual que la base; en la evaluación 3 (N_eff = 1.0) pasa de `0.0` a `None`. Ese driver ingesta un texto antes de cada evaluación, y no produce ningún `D_ckm ≠ 0` en Monitor.

**No verificado:**
- Ninguno de los nueve scripts de `experiments/` que importan el engine, COCO o Monitor, fuera del driver de arriba. Los que lean `count_attractors` como conteo ahora reciben N_eff. `driver_W_corpus_informes.py:93` llena columnas `A_{n_runs}` con esa función.
- `iap_chatroom/` no se miró.
- `python services/coco.py` y `python services/monitor_service.py` en modo standalone no se corrieron.
- `D_ckm ≠ 0` en Monitor con un driver real.

## Bloqueo explícito

Si un test sólo pasa cambiando lo que afirma, o si cerrar un paso exige tocar los umbrales de COCO o la política de A0: **detener y reportar**. No encadenar cambios.

## Abierto

- **Los umbrales de COCO sobre la escala nueva.** Para caer en "degrading" hacen falta `D_ckm ≥ 0.40` (o sea `A ≤ A0^0.6`) y `frac_rec ≥ 0.60` (o sea `A ≥ 0.6·A0`). Las dos juntas sólo tienen solución si `A0 ≤ 3.58`. Por encima de ese baseline, todo lo que cruza el umbral cae directo en "deep". Es aritmética sobre los umbrales actuales, no una medición sobre corpus.
- **El log cerca de baseline 1.** Con N_eff0 = 1.04 (una órbita con el 98 % de la masa) `D_ckm` da −55. El docstring de `d_masa_cuencas` ya lo advierte; ahora esa sensibilidad gobierna la regulación de COCO.
- **`frac_rec` es ahora un cociente de N_eff**, lineal, al lado de un `D_ckm` logarítmico sobre las mismas dos cantidades.
- **Los dos baselines** de `TASK_d_ckm_al_engine_v1` siguen. En la misma evaluación Monitor dio `D_ckm = 0.0` y COCO `0.218`.
- **Monitor calcula las masas dos veces** por evaluación, una en `_D_ckm` y otra en `_N_eff`, con el mismo resultado. `_A0` y `_N_eff0` guardan el mismo valor.
- **`d_ckm` devuelve `np.float64`**, no `float` de Python.
- **Los dos tests de `TestSTOP`** siguen fijando `_A0` y reemplazando `_count_attractors` desde afuera, con literales. Era así antes de esta task.
- **El docstring de `d_ckm` en el engine** lleva el texto anterior completo bajo un bloque "DEPRECATED", duplicado del de `deprecated_d_ckm`.
