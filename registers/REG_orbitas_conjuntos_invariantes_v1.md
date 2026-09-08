# REG_orbitas_conjuntos_invariantes_v1.md

*Sep 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Descripción

Contar **órbitas** (conjuntos invariantes) en vez de estados terminales, y
qué pasa con la diversidad cuando se lo hace. Incluye verdad de terreno por
enumeración exhaustiva de los 2²⁰ estados en tres corpus N=20 — no
estimación: conteo completo.

Origen: la conversación sobre convergencia. `_count_attractors` cuenta el
estado devuelto tras `max_iter` pasos. Si la trayectoria queda en una órbita
de período > 1, ese estado es **una fase** de la órbita, no la órbita.

Instrumento: `_relax_orbit` en `services/coco.py` y
`services/monitor_service.py`, commit `1e14274`.

---

## 1. El instrumento — `_relax_orbit`

```
_relax_orbit(sigma, W, max_iter) -> (orbita, periodo, cola, estado_en_max_iter)
```

`orbita` es un `frozenset` de estados, **sin orden**. Detección exacta, no
heurística: el espacio es finito y el mapa determinista, así que toda
trayectoria entra en una órbita en tiempo finito. Se guarda cada estado
visto con su paso; al repetirse uno, la órbita es el tramo entre las dos
apariciones. **0 fallos de detección en todas las corridas de este REG.**

`_relax` delega y devuelve `estado_en_max_iter`, reconstruido como
`cola + ((max_iter − cola) mod periodo)` en vez de recorrer el ciclo.

**Impacto cero, verificado:** 82/82 tests; `coco.py` T1–T13; replicación de
los dos drivers commiteados (8 condiciones × 24 evaluaciones × 11 campos):
**8/8 archivos idénticos, 0 diferencias**; `_count_attractors` idéntico
contra `HEAD` en tres corpus a n_runs 200 y 1000.

**Aceleración medida contra `HEAD`:**

| corpus | n_runs | HEAD | nuevo | speedup |
|---|---:|---:|---:|---:|
| WARMUP (N=20) | 200 | 0.884s | 0.010s | **87×** |
| WARMUP (N=20) | 1000 | 4.055s | 0.074s | 55× |
| caso09 natural (N=20) | 200 | 0.719s | 0.010s | 71× |
| `W_ckm_corpus_v2` (N=32) | 200 | 0.038s | 0.008s | 4.6× |

Dos fuentes independientes: salida temprana al cerrar la órbita, y reemplazo
de `np.allclose` por comparación exacta de bytes (los estados son ±1, no hay
tolerancia que ganar). La segunda explica sola el 4× del corpus N=32.

---

## 2. Corrección de una afirmación previa (commit `5f2ec6c`)

El docstring de `_relax` en `monitor_service` decía:

> *"Verificado: 0 de 200 estados finales distintos entre `max_iter` 100 y
> 200 — la relajación converge muy por debajo de 100."*

**La medición era correcta; la conclusión no.** 100 y 200 son ambos **pares**,
y una órbita de período 2 devuelve la misma fase en los dos. El test que
separa los casos es **100 contra 101**:

| corpus | runs | llegan a punto fijo | quedan en órbita |
|---|---:|---:|---:|
| WARMUP (N=20) | 200 | 59 | **141 (70.5%)** |
| caso09 natural (N=20) | 200 | 64 | **136 (68%)** |
| `W_ckm_corpus_v2` (N=32) | 200 | 197 | 3 (1.5%) |

Las órbitas no son un caso de borde: son el régimen mayoritario en los
corpus operativos N=20.

---

## 3. Solo períodos 1 y 2 — Goles confirmado con la regla de empate

En los cuatro corpus del proyecto **no aparece ningún período mayor que 2**.
Es el teorema de Goles, y queda confirmado **con la regla de empate
"conserva σ"**, que no es la función signo estándar y por la cual no se
podía asumir.

Cierra con número el pendiente de `DEFS_CKM_estado_actual_v7.md` §18:
*"prevalencia de ciclos período-2 en relajación sincrónica en W_mixta: no
evaluada"*.

**Sobre el rótulo.** "Ciclo de período 2" nombra la cosa por lo que no es —
por no ser punto fijo — y de ahí sale tratarla como algo a evitar. Es una
**órbita**; el punto fijo es la órbita de un elemento. Lo que el principio de
invariancia de LaSalle selecciona es la **invariancia**, no la quietud.

Consecuencia sobre una decisión del proyecto: en CS, "usar actualización
asíncrona" se presenta como *evitar ciclos*. Lo que hace es elegir una
dinámica cuyos miembros de M son todos singletons. No corrige nada —
degenera las órbitas. Que eso sea lo deseable es decisión de modelado.

---

## 4. Tres cantidades distintas, no dos

**L es el conjunto máximo invariante — un conjunto de estados.** Las órbitas
son su descomposición en subconjuntos invariantes mínimos, no sus elementos.
Formalmente son dos objetos: **L** y **L/~**.

| | qué es |
|---|---|
| **\|L\|** | cantidad de **estados** en el conjunto máximo invariante |
| **órbitas** | subconjuntos invariantes mínimos — las clases de L/~ |
| **terminales** | lo que devuelve `_count_attractors` |

Ordenan siempre así: `órbitas ≤ terminales ≤ |L|`.

| corpus | n_runs | \|L\| | órbitas | terminales |
|---|---:|---:|---:|---:|
| WARMUP | 200 | 280 | 164 | 174 |
| caso09 natural | 200 | 83 | 53 | 64 |
| `W_ckm_corpus_v2` | 200 | 8 | 5 | 5 |

**Corrección a lo que este REG afirmaba en versiones previas de la sesión:**
DEFS §11 dice que `_count_attractors` es *"un estimador de |L|"*. **Lo es** —
por debajo: los terminales son estados de L, y se ven solo las fases que las
colas alcanzaron. Lo que **no** estima es el número de órbitas. Antes se
dijo que estimaba mal |L|; estima |L| por defecto, y no estima la otra cosa.

---

## 5. El `frozenset` no pierde información

Preocupación planteada: para p ≥ 3 el mismo conjunto de estados podría
recorrerse en órdenes distintos, y el `frozenset` los colapsaría.

**No ocurre, y no puede ocurrir.** El mapa es determinista: cada estado tiene
**un** sucesor. Que {A,B,C} se recorriera como A→B→C→A *y* como A→C→B→A
exigiría que A tuviera dos sucesores. Por lo mismo, dos órbitas no pueden
compartir un estado. El conjunto identifica unívocamente a la órbita.

Verificado sobre cinco W **asimétricas** (Goles exige simetría; sin ella
aparecen períodos largos), 400 runs cada una:

| W | períodos hallados | \|frozensets\| | \|ciclos ordenados\| | estados compartidos |
|---|---|---:|---:|---:|
| #0 | 1, 2, 15, 28 | 6 | 6 | 0 |
| #1 | 2, 6, 10, 30 | 6 | 6 | 0 |
| #2 | 6 | 2 | 2 | 0 |
| #3 | 16 | 1 | 1 | 0 |
| #4 | 1, 10, 14 | 4 | 4 | 0 |

**Consecuencia no prevista: la regla de empate es lo que sostiene el
determinismo.** Si el empate se resolviera al azar en vez de conservar σ, el
mapa dejaría de ser determinista, el `frozenset` perdería información y la
detección de órbita dejaría de ser exacta. La regla no es solo una decisión
de modelado sobre conteos — es la condición de la representación.

---

## 6. Predicción propia, falsada

Se predijo: *"la distribución de cuencas dice de antemano cuál va a saturar
y cuál no"* — WARMUP, con 83% de órbitas vistas una sola vez a n_runs=200,
no saturaría; `W_ckm_v2`, con dos cuencas dominantes, ya estaba saturado.

**Al revés en los dos casos:**

| corpus | n_runs | órbitas | d(órb)/d(n) |
|---|---:|---:|---:|
| WARMUP | 3.000 | 776 | 0.139 |
| | 10.000 | 1014 | 0.034 |
| | 30.000 | **1104** | **0.0045** ← satura |
| caso09 natural | 30.000 | 394 | 0.0045 ← satura |
| `W_ckm_v2` (N=32) | 3.000 | 27 | 0.0080 |
| | 30.000 | 205 | 0.0066 |
| | 100.000 | 744 | 0.0077 |
| | 300.000 | **1994** | **0.00625** ← pendiente constante |

**Por qué la lectura era mala:** la fracción de singletons a n_runs bajo no
mide cuántas órbitas faltan encontrar — mide cuántas quedan sin ver
*relativo al tamaño de la muestra*. Con 164 vistas de ~1136 existentes, casi
todas aparecen una vez porque la muestra es chica, no porque haya infinitas.

Y en N=32 pasó lo contrario: `[104, 93, 1, 1, 1]` no era "dos cuencas más
tres rarezas" sino "dos cuencas más una cola sin fondo" — el espacio es 2³²
contra 2²⁰.

**Lo que esto tira abajo es mayor que la predicción.** Se había planteado que
`A` no satura porque cuenta instancias y que `|L|` sí saturaría porque cuenta
cupones. Para el corpus real del proyecto, **contar órbitas tampoco satura**.
El sesgo `n_runs` sobrevive entero al cambio de instrumento: no era un
problema de contar fases, es que hay muchísimos cupones.

---

## 7. El conteo depende del muestreo, no solo del campo

`W_ckm_corpus_v2`, n_runs = 100.000, **misma W**:

| modo | \|L\| | órbitas | d(órb)/d(n) 10k→100k |
|---|---:|---:|---:|
| uniform | 1486 | **744** | 0.00746 |
| weighted | 200 | **101** | 0.00097 |
| boltzmann | 184 | **93** | 0.00088 |

**Factor 7–8× con el campo idéntico.** El número de órbitas no es propiedad
de W: es propiedad de **(W, distribución de σ₀, n_runs)**.

---

## 8. Barrido AMP — A y forma de cuencas se desacoplan

`W_ckm_corpus_v2` con los 3 pares negativos de `calibrate_W_mixta.py`,
n_runs=2000:

| AMP | A (órbitas) | H norm | cuenca máx | cola media | c(S) medio |
|---:|---:|---:|---:|---:|---:|
| 0 | 19 | 0.258 | 0.515 | 2.72 | 0.00001 |
| 5 | **23** ↑ | **0.247** ↓ | 0.518 | 2.90 | −0.00018 |
| 10 | **21** ↓ | **0.459** ↑↑ | 0.338 | 2.51 | 0.00038 |
| 15 | 22 | 0.438 | 0.367 | 2.55 | 0.00033 |
| 20–35 | 26 | 0.575 | 0.259 | ~2.6 | ~0.00087 |
| 40 | 40 | 0.676 | 0.203 | 2.78 | 0.00129 |
| 50 | 115 | 0.867 | 0.046 | 2.61 | 0.00278 |
| 60–80 | 140 | 0.902 | 0.023 | 2.56 | 0.00284 |

**De AMP 5 a 10, A baja mientras la entropía de cuencas casi se duplica.** Se
mueven en direcciones opuestas: no son la misma medida. En la zona alta sí
correlacionan. Dos dimensiones que comparten una causa parcial.

**La cola queda plana (2.5–2.9) en todo el barrido** — no sigue a ninguna de
las dos. Tercera dimensión, o mal proxy de profundidad.

**Sobre la proposición del paper "cuencas pequeñas y profundas en sistema
frustrado":**
- **Pequeñas: verificado.** Cuenca máxima 0.515 → 0.023 con AMP.
- **Profundas: no verificado** con el proxy de cola.

En **AMP 20–35 los tres números son idénticos**, no parecidos. El paisaje no
cambia en ese tramo.

---

## 9. Las masas convergen, los conteos no

`W_mixta`, n_runs de 1.000 a 100.000:

| | AMP=0 | AMP=40 | AMP=80 |
|---|---|---|---|
| **A** | 9 → 735 (**×82**) | 33 → 841 (×25) | 125 → 955 (×7.6) |
| **H norm** | 0.338 → 0.120 | 0.714 → 0.379 | 0.919 → 0.660 |
| **cuenca máx** | 0.515 → **0.498** | 0.214 → **0.198** | 0.024 → **0.021** |

La cuenca máxima varía 3.5%, 8% y 12% mientras A varía ×82.

**Razón estructural, no accidente del corpus:** la fracción de cuenca es una
**probabilidad** — P(σ₀ cae ahí). Más muestras la estiman mejor, no la hacen
crecer. `A` es un **conteo de resultados distintos vistos**: en un espacio de
2³², más muestras siempre encuentran más.

La entropía normalizada queda en el medio porque se normaliza por `log(A)` y
arrastra el crecimiento de A. No es candidata.

---

## 10. Verdad de terreno — enumeración exhaustiva de 2²⁰

Los tres corpus N=20 enumerados completos (1.048.576 estados, ~16s cada uno
con memoización de trayectorias):

| corpus | **órbitas reales** | **\|L\| real** | vol máx | top-3 | top-10 |
|---|---:|---:|---:|---:|---:|
| WARMUP | **1136** | 2112 | 0.0037 | 0.0110 | 0.0366 |
| caso09 natural | **573** | 940 | 0.0912 | 0.2423 | 0.5673 |
| caso09 forzado | **170** | 330 | 0.4898 | 0.9846 | 0.9929 |

Contra esa verdad, cada muestreo a n_runs=30.000:

| corpus | muestreo | órbitas halladas | error vol máx | error top-10 |
|---|---|---:|---:|---:|
| **WARMUP** | hipercubo | 98% | 26.5% | **16.0%** |
| | uniform (banda) | 97% | 51.1% | 33.9% |
| | boltzmann | 97% | 48.4% | 33.9% |
| | weighted | 24% | **1669%** | **845%** |
| **caso09 natural** | hipercubo | 73% | 3.6% | **0.6%** |
| | uniform | 69% | 2.6% | 0.7% |
| | boltzmann | 70% | 9.1% | 0.6% |
| | weighted | 62% | 57.5% | 18.0% |
| **caso09 forzado** | hipercubo | 52% | **0.0%** | **0.0%** |
| | uniform | 45% | 0.4% | 0.1% |
| | boltzmann | 34% | 0.5% | 0.3% |
| | weighted | 34% | 42.3% | 0.3% |

### Lo que la verdad de terreno establece

**a) Masas convergen, conteos no — ahora contra verdad, no entre estimaciones.**
`caso09 forzado` recupera el volumen de cuenca con **0.0% de error** habiendo
encontrado solo el **52%** de las órbitas. Las que faltan no pesan. WARMUP
encuentra el 98% de las órbitas y aun así tiene 16% de error en top-10.

**b) Dos regímenes.** Con masa concentrada (`forzado`, top-10 = 99.3%), la
masa converge rápido y el conteo es irrelevante. Con masa plana (WARMUP,
top-10 = 3.7%), el conteo es alcanzable pero cada masa individual es ruidosa.

**c) `weighted` no es un estimador peor del volumen de cuenca — es otra
cantidad.** 1669% de error, 24% de las órbitas.

**d) `boltzmann` es redundante con `uniform`.** Resultado negativo: se
propuso como muestreo termodinámicamente fundamentado que respeta la
anisotropía de W; contra verdad de terreno da prácticamente lo mismo que el
uniforme en los tres corpus. No incorrecto — redundante.

**e) El modo `uniform` no es la referencia canónica.** Sortea
`n_act ~ U(0.3N, 0.7N)` — uniforme sobre una *banda de activación*, no sobre
`{−1,+1}^N`. La diferencia con el hipercubo es consistente pero chica
(16% contra 34% en el peor caso).

**f) `vol_max` estimado por muestreo tiene sesgo hacia arriba** cuando las
cuencas son parecidas: es el máximo de estimaciones ruidosas, y el máximo del
ruido supera al máximo real. Por eso WARMUP da 26.5% de error en `vol_max` y
16% en top-10 — al agregar, se cancela.

---

## 11. Criterio operativo propuesto

Para medir diversidad en CKM:

1. **Declarar la medida de referencia sobre σ₀.** Sin eso, ni el conteo ni la
   masa son propiedades de W: son propiedades de (W, referencia, n_runs).
2. **Usar masa agregada (top-k), no conteos.** Las masas convergen con
   `n_runs`; los conteos no, y no lo harán en espacios de este tamaño.
3. **No usar el máximo individual** — tiene sesgo hacia arriba con cuencas
   parecidas. Agregar cancela ese sesgo.
4. **Para N ≤ 20, no estimar: enumerar.** 2²⁰ completo son ~16 segundos.

*Estado: propuesto. Las mediciones que lo sostienen son verificadas; que
este criterio sea el adecuado para el modelo es decisión abierta.*

---

## Lo que este REG no establece

- **No dice qué debería contar `D_ckm`.** LaSalle define L; no dice si el
  modelo debe medir L, L/~ o masas. Esa es decisión del modelo.
- **No resuelve el sesgo `n_runs`** — lo reubica. Contar órbitas no lo
  elimina; usar masas sí lo evita, pero cambia lo que se mide.
- **No establece profundidad de cuenca.** La cola es plana en todo el
  barrido AMP; el c(S) por órbita se midió pero no se contrastó contra nada.
  "Pequeñas y profundas" queda con la primera mitad verificada.
- **No mide coercividad.** Es el tercer vértice de la pregunta abierta del
  paper (A / coercividad / cuencas) y no se tocó. `d_analytics.py` tiene
  `cluster_frontier_density` como coercividad operativa entre clusters,
  pendiente de medición.
- **La enumeración exhaustiva es sólo para N=20.** `W_ckm_corpus_v2` (N=32,
  2³² ≈ 4·10⁹) no es enumerable con este método.
- **Todo lo de la sección 8 usa muestreo uniforme de banda**, que la sección
  10 muestra que no es la referencia canónica. Los números del barrido AMP
  son válidos como comparación interna, no como volúmenes.
- **Sin commit del REG.** El instrumento sí está commiteado (`1e14274`), sin push.

---

## Archivos

- `services/coco.py`, `services/monitor_service.py` — `_relax_orbit` (commit `1e14274`)
- `registers/REG_count_attractors_bias_v1.md` — sesgo de uniformidad en σ₀
- `registers/REG_stochastic_eval_v1.md`, `v2` — sesgo `n_runs`, origen del coleccionista de cupones
- `registers/REG_boltzmann_sampling_v1.md` — implementación del modo boltzmann
- `registers/REG_monitor_service_unificar_rutinas_v1.md` — unificación previa
- `experiments/calibrate_W_mixta.py` — pares negativos y protocolo AMP
- `docs/DEFS_CKM_estado_actual_v7.md` §4, §11, §18 — lo que este REG toca

---

*Sep 2026 — Codespace ckm — bash/Linux*
