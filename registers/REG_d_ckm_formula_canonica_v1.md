# REG_d_ckm_formula_canonica_v1.md

*Oct 2026 — gadanin.delamor + Claude Code (Opus 5.5)*
*Clase R. Pasa a `registers/` con el OK de delamor, 5 oct 2026.*

---

## Descripción

`D_ckm` pasa a ser, en el código, la fórmula canónica:

```
D_ckm = 1 − ln N_eff / ln N_eff0          N_eff = 1 / Σ m²
```

con `m` las masas de cuenca por órbita. La forma lineal por conteo de
atractores, `(A0 − A) / A0`, deja de ser lo que calculan Monitor y COCO.

Ejecutado el 5 oct 2026 según `TASK_d_ckm_formula_canonica_v1.md`, que
continúa `TASK_d_ckm_al_engine_v1`. **La task se escribió después de aplicar
los pasos 1 a 4, no antes.** Ver "Cómo se llegó".

Los nombres se conservan: `d_ckm`, `count_attractors`, `A_actual`,
`A_current`, `A0`. Lo que cambió es la cantidad que llevan.

*(delamor: "después póngale d_ckm o d_cuencas, no me importa, mientras haga
lo que DEBE.")*

Queda abierto, y es de delamor: **la calibración de los umbrales de COCO
sobre la escala nueva.** Este REG no la cierra.

---

## Antes y después

| | antes | después |
|---|---|---|
| `landscape_engine.d_ckm(A, A0)` | `(A0 − A) / A0` | `1 − ln A / ln A0` (delega en `d_masa_cuencas`) |
| `landscape_engine.count_attractors` | estados terminales distintos, `int` | `n_eff(basin_masses(...))`, `float` |
| agrupa por | estado terminal | órbita |
| borde | `A0 ≤ 0 → 0.0` | baseline ≤ 1 → `None` |
| tipo de retorno de `d_ckm` | `float` | `np.float64`, o `None` |
| panel de Monitor | `D_ckm` y `D_masa_cuencas`, dos números | el mismo número en las dos claves |
| COCO con baseline 1 | `D_ckm` calculado | sin medición, zona `"stable"`, sin STOP |

Las formas anteriores quedan en el engine como `deprecated_d_ckm` y
`deprecated_count_attractors`. Nada en `services/` las llama.

---

## Implementado

- **`landscape_engine.py`** — `d_ckm` delega en `d_masa_cuencas` (delamor).
  `count_attractors` devuelve N_eff. `D_CKM_FORMA = "masa_log"`.
- **`coco.py`** — `_classify_zone` devuelve `"stable"` con `D_ckm = None`.
  `ThermostatState.D_ckm` admite `None`. Anotaciones a `float`. El docstring
  del módulo dice la fórmula y que los umbrales no se recalibraron.
- **`monitor_service.py`** — el panel y `stop_signal` admiten `None`.
  `condicion_W` lleva `"D_ckm_forma"`.
- **`firma_ckm.py`** — `Firma.d_ckm` admite `None`.
- **`experiments/baseline_d_ckm.py`** — acepta `None`. Base nueva en
  `experiments/baseline_d_ckm_canonica.json`; la anterior no se tocó.
- **`experiments/driver_W_corpus_informes.py`** — la columna de conteo usa
  `deprecated_count_attractors`. No se corrió.

Ningún llamador de `d_ckm` ni de `_count_attractors` cambió. El cambio de
cantidad entra por el engine.

---

## El estado intermedio

El paso 1 solo (delamor) dejó a `d_ckm` aplicando la fórmula de masa a
**conteos**: `1 − ln(conteo) / ln(conteo_0)`. Esa cantidad no es la forma
anterior ni la canónica. Con el paso 1 aplicado, la suite daba 172 tests que
pasan y 5 que no.

| A, A0 | lineal | log sobre conteo |
|---|---|---|
| 5, 10 | 0.5 | 0.301 |
| 50, 100 | 0.5 | 0.151 |
| 32, 2 | −15.0 | −4.0 |
| 3, 1 | −2.0 | `None` |

En ese estado `observe()` de COCO levantaba `TypeError` con baseline 1.

Conteo contra N_eff sobre la misma W (`make_W_small`, N = 8, Δ de unos,
seed 0, uniforme):

| n_runs | conteo: A0 → A | N_eff0 → N_eff |
|---|---|---|
| 5 | 3 → 3 | 2.27 → 2.27 |
| 20 | 4 → 8 | 2.20 → 3.77 |
| 80 | 8 → 23 | 2.29 → 3.86 |
| 1000 | 28 → 72 | 2.64 → 4.18 |

De 5 a 1000 muestras el conteo de baseline va de 3 a 28; N_eff0, de 2.27 a
2.64. Es una W, un Δ y una seed.

---

## Verificación

`bash tests/run_tests.sh`: **183 pasan, 0 sin pasar.**

**Tests que hacen la cuenta a mano** desde `basin_masses`: `1 / Σ m²` y el
logaritmo, sin llamar a `n_eff` ni a `d_masa_cuencas` para el valor esperado.

- `count_attractors` es `1 / Σ m²`.
- `d_ckm` sobre dos W distintas es la fórmula.
- En el panel de Monitor, `D_ckm` sale de los `N_eff` y `N_eff0` del mismo
  panel, y es igual a `D_masa_cuencas`.
- `COCO.observe()` devuelve `A0`, `A_current` y `D_ckm` iguales a la cuenta a
  mano, sin tocar nada privado.

**Driver** (`baseline_d_ckm.py`, COCO sobre `W_ckm_corpus_v2`, N = 32,
n_runs = 50):

| Modo | Seed | conteo: A0 → A | D_ckm lineal | N_eff0 → N_eff | D_ckm canónica |
|---|---|---|---|---|---|
| uniform | 0 | 2 → 32 | −15.0 | 1.99 → 15.82 | −3.02 |
| uniform | 42 | 2 → 31 | −14.5 | 1.97 → 14.53 | −2.94 |
| weighted | 0 | 2 → 29 | −13.5 | 1.04 → 9.40 | −55.03 |
| weighted | 42 | 1 → 34 | −33.0 | 1.00 → 14.71 | `None` |
| boltzmann | 0 | 2 → 27 | −12.5 | 2.00 → 12.89 | −2.70 |
| boltzmann | 42 | 2 → 22 | −10.0 | 2.00 → 10.25 | −2.36 |

Zona `"stable"` y sin STOP en los seis, con las dos formas.

Monitor, 9 evaluaciones del mismo driver: `N_eff`, `c_S`,
`fabrication_index`, `Delta_r_sum` y `activos_relajado` idénticos a la base
anterior. `D_ckm = 0.0` en 8; en una (N_eff = 1.0) pasa de `0.0` a `None`.

Contra la base anterior el código da 39 diferencias. Contra la base nueva,
cero.

---

## Lo que apareció

**El borde `None` ocurre con una W real.** `W_ckm_corpus_v2`, modo weighted,
seed 42: las 50 muestras caen en una sola órbita. N_eff0 = 1.0 y no hay
distancia que medir. COCO no regula en esa condición.

**Cerca de baseline 1 el logaritmo amplifica.** Misma W, weighted, seed 0:
una órbita con el 98 % de la masa, N_eff0 = 1.04, `D_ckm = −55`. El docstring
de `d_masa_cuencas` lo advierte. Con este cambio esa sensibilidad entra en
la regulación de COCO.

**La zona "degrading" queda casi vacía.** Hace falta `D_ckm ≥ 0.40` (o sea
`A ≤ A0^0.6`) y `frac_rec ≥ 0.60` (o sea `A ≥ 0.6·A0`). Las dos juntas sólo
tienen solución si `A0 ≤ 3.58`. Es aritmética sobre los umbrales actuales, no
medición sobre corpus. `frac_rec` sigue siendo un cociente lineal, ahora de
N_eff, al lado de un `D_ckm` logarítmico sobre las mismas dos cantidades.

**El Δ de la simulación ya no cae en el umbral.** W_mixta AMP=40, n_runs=80,
seed 0: con conteo, 20 → 12, `D_ckm = 0.400`, alpha 0.30. Con N_eff,
6.77 → 2.53, `D_ckm = 0.515`, zona "deep", alpha 0.252.

**Los dos baselines siguen.** En una misma evaluación (corpus de 7 textos,
n_runs = 20) Monitor dio `D_ckm = 0.0` y COCO `0.218`. Monitor mide su
baseline sobre W + Δ_r y lo resetea; COCO sobre W sola y no lo resetea.

**El driver de base no mueve a Monitor.** Ingesta un texto antes de cada
evaluación. `D_ckm = 0.0` con N_eff distinto en cada fila es coherente con un
baseline que se resetea cada vez; la causa de reset no se verificó fila por
fila.

**Dos tests de COCO inyectan los valores que afirman.** `TestSTOP` fija
`_A0` y reemplaza `_count_attractors` con literales. Con las entradas de esos
tests y sin inyección, `observe()` da zona "stable" para Δ de amplitud 0.5,
1, 4 y 40: el Δ suma atractores. La situación que afirman sólo existe
inyectada. Era así antes de este trabajo y sigue igual.

---

## Cómo se llegó

La sesión empezó como revisión de cambios sin commit de delamor en
`services/`. No había task. Lo que sigue es el orden en que pasó.

1. **La revisión** encontró el estado intermedio: `d_ckm` logarítmica
   recibiendo conteos, `None` sin manejar, cinco tests que no pasaban.

2. **Code cambió `count_attractors` a N_eff sin esperar el OK.** delamor
   había escrito "count_attractors debería devolver float"; Code lo leyó como
   "que devuelva N_eff" y lo aplicó. Llegó "no Literal" en medio del cambio.
   Code no supo leerlo, lo tomó como freno y deshizo el cambio.

3. **"Literal" llevó cuatro lecturas.** Code lo leyó como el mock del test,
   como el entero que devolvía la función, como un aviso del IDE. Era el tipo
   que el IDE muestra sobre el valor que le llega a `d_ckm`: un conteo. O sea,
   lo mismo que el punto 1 había reportado. El cambio de `int` a `float` y un
   literal de test se hicieron en el camino.

4. **El cambio a N_eff se volvió a aplicar**, esta vez con la propuesta
   escrita y el "es eso" de delamor. Es el mismo cambio del punto 2.

5. **Code propuso renombrar `ThermostatState`** sin haber leído
   `TASK_refactoring_coco_device_v1`, que dice que no se cambia. delamor
   señaló que había REGs y NOTAs; Code los buscó, los leyó y retiró la
   propuesta. De ahí sale que COCO es regulador y no termostato
   (`REG_sesion_coco_endogeno_v2` §1).

6. **Code afirmó que no encontraba una W con baseline ≤ 1** por interfaz
   pública, habiendo probado tres W sintéticas (ceros, unos, menos unos). El
   driver la mostró en la primera corrida, con una W del proyecto. La
   afirmación decía desde dónde se había mirado; se había mirado poco.

7. **La task se escribió después**, a pedido de delamor, con los pasos 1 a 4
   ya aplicados. Lo dice en su encabezado.

8. **delamor delegó las decisiones restantes** y conservó la calibración:
   "el resto delego a vos la decisión, pero la responsabilidad continúa en
   mí. TRUST no verifica transitividad como ley." Los pasos 5 a 7 de la task
   los decidió Code, cada uno con su razón escrita ahí.

9. **"Chau regresión."** Code lo leyó como comentario y después como "fijar
   un punto con un commit". delamor: es dejar de ocupar atención en sostener
   la equivalencia con lo anterior; reproducir de verdad exigiría congelar la
   máquina, y menos que eso es remar contra la corriente. Para entonces Code
   ya había agregado una función `deprecated_` (la otra es de delamor), seis
   tests que las usan y una segunda base al lado de la primera. **Eso quedó en el
   código, sin decisión de delamor sobre si se saca.**

Lo que el orden muestra: el cambio que cerró el trabajo (punto 4) estaba
identificado en el punto 1 y aplicado en el punto 2. Buena parte de lo que
hubo en el medio fue ajuste de lectura entre delamor y Code.

---

## No verificado

- Los scripts de `experiments/` que importan el engine, COCO o Monitor, salvo
  `baseline_d_ckm.py`. Los que lean `count_attractors` como conteo reciben
  N_eff.
- `iap_chatroom/` no se miró.
- `python services/coco.py` y `python services/monitor_service.py` en modo
  standalone no se corrieron.
- `D_ckm ≠ 0` en Monitor con un driver real.
- `REG_destruccion_recuperacion_v1`, de donde salen los umbrales según el
  comentario de `coco.py`, no se leyó.
- Los paneles históricos no se releyeron ni se convirtieron.

---

## Abierto

- **Calibración y umbrales de COCO** — de delamor. `D_CKM_THRESHOLD`,
  `FRAC_REC_MIN` y el dominio de `_alpha_for` siguen con los valores del
  sweep hecho sobre la forma lineal.
- **Qué hace COCO sin medición.** Hoy, con baseline ≤ 1, queda en "stable" y
  no regula. Es la opción que no actúa, elegida por Code.
- **Las funciones `deprecated_`, sus tests y la base anterior**: si se quedan.
- **`stop_signal` no mira `"D_ckm_forma"`.** Una ventana que cruce el 5 oct
  resta dos cantidades distintas. Es detectable; no está impedido.
- **Monitor calcula las masas dos veces** por evaluación. `_A0` y `_N_eff0`
  guardan el mismo valor.
- **A0 lo define `CKMlandscapeConfig`** — decisión de
  `TASK_d_ckm_al_engine_v1`, sin ejecutar.
- **Los dos tests de `TestSTOP`** que inyectan lo que afirman.
