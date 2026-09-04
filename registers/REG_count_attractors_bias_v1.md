# REG_count_attractors_bias_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Ejecución de `TASK_count_attractors_bias_v1.md`. Documenta el segundo
sesgo de `_count_attractors()` (`services/coco.py`) — uniformidad sobre
nodos en la generación de σ₀ — y agrega un modo de muestreo ponderado
opcional (`weighted=True`) que no altera el comportamiento por defecto.

Archivo modificado: `services/coco.py` únicamente.

---

## Paso 0 — Verificación previa

**Firma anterior:** `_count_attractors(self, W_eff: np.ndarray) -> int`
— un solo parámetro. `seed` y `n_runs` son atributos de instancia
(`self._seed`, `self._n_runs`), no parámetros del método.

**Firma anterior:** `_mean_cS(self, W_eff: np.ndarray) -> float`.
**Comparte el loop de muestreo:** sí — verificado literalmente. Ambos
métodos abren `np.random.default_rng(self._seed)` e iteran `self._n_runs`
veces con el mismo cuerpo (`rng.uniform(0.3, 0.7)` → `n_act`;
`rng.choice(self.N, n_act, replace=False)`). Misma semilla, misma
secuencia de σ₀. Por eso la Tarea 3 aplica.

**Llamadas externas directas a `_count_attractors`:**

| Origen | Forma de llamada | Impacto |
|---|---|---|
| `tests/test_coco.py:233,250` | monkeypatch `th._count_attractors = lambda W_eff: 5` | ninguno — las llamadas internas siguen pasando un solo argumento posicional |
| `experiments/stochastic_attractor_eval.py:53,183,184` | `coco._count_attractors(W)` | ninguno — el nuevo parámetro tiene default |

No hay llamadas externas a `_mean_cS`. Los otros hits del grep
(`monitor_service.py`, `fabrication_service.py`, `process/experiments/`,
`experiments/monitor_service*.py`) son implementaciones homónimas
independientes en otras clases — no tocadas.

**Conteo de tests:** `python tests/test_coco.py` → **28 passed, 0 failed**,
confirmado antes de tocar nada. (El README declara 43/43 para
`services/test_coco.py`; ese archivo no existe. La cifra 28/28 de la TASK
es la correcta.)

**Bloqueo explícito — no disparado.** Agregar `weighted` no requirió
tocar la firma de `observe()`, `delta_state()` ni ningún otro método
público. Las llamadas internas en `observe()` quedaron sin cambios.

---

## Tarea 1 — Docstring del sesgo de uniformidad

Agregado al docstring de `_count_attractors`, con el texto de la TASK
más una línea: los dos sesgos (n_runs y uniformidad) son independientes
— `weighted=True` no corrige el primero.

---

## Tarea 2 — Modo ponderado

`_count_attractors(self, W_eff, weighted: bool = False)`.

Refactor mínimo en dos helpers privados nuevos, para que
`_count_attractors` y `_mean_cS` sigan consumiendo el RNG en la misma
secuencia — propiedad de la que depende el docstring de `_mean_cS`:

- `_node_probs(W_eff, weighted) -> Optional[np.ndarray]` — `None` si
  `weighted=False`; si no, `fi / fi.sum()` con `fi = |W_eff|.sum(axis=1)`.
- `_sample_s0(rng, probs) -> np.ndarray` — cuerpo del loop original,
  con `p=probs` (`p=None` reproduce el muestreo uniforme exacto).

**Dos fallbacks a uniforme, sin error:**

1. `fi.sum() <= 0` — `W_eff` completamente cero (el pedido en la TASK).
2. `count_nonzero(fi) < round(0.7·N)` — **hallazgo no previsto en la
   TASK**: `rng.choice(..., replace=False, p=probs)` lanza `ValueError`
   si hay menos nodos con probabilidad no nula que `n_act`. Con `W_eff`
   sparse-por-bloques (el caso que la TASK motiva como problemático) esto
   se dispara. Se compara contra el `n_act` máximo posible (0.7·N) y no
   contra el `n_act` del sorteo, para que la decisión no dependa del
   estado del RNG — si dependiera, `weighted=True` produciría
   alternancia uniforme/ponderada dentro de una misma corrida.

---

## Tarea 3 — `_mean_cS`

Comparte el loop → se agregó `weighted: bool = False` con la misma
lógica, vía los mismos helpers. Docstring ampliado: para que `A` y `c(S)`
sigan describiendo las mismas muestras hay que pasar el mismo valor de
`weighted` a los dos métodos.

`observe()` no fue modificado: llama a ambos sin el parámetro, es decir
`weighted=False`. El modo ponderado hoy es de uso manual/experimental,
no está cableado a la regulación.

---

## Criterio de éxito — verificado

```
python tests/test_coco.py  →  28 passed, 0 failed
```

**Sin regresión (verificación explícita):** se reimplementó el loop
histórico en un script aparte y se comparó contra el default nuevo sobre
`W_ckm_corpus_v2.json` — mismo conteo. El default no es "equivalente por
inspección": es el mismo consumo de RNG.

**Prueba manual del path ponderado:**

| W_eff | uniform | weighted | nota |
|---|---|---|---|
| `W_ckm_corpus_v2.json` (N=32, real) | 2 | 2 | probs ≠ None — se ejecutó el path ponderado |
| densa N=32 con hub (fila/col 0 ×20) | 13 | 8 | conteos distintos |
| todo cero (N=32) | — | 50 | fallback 1 → uniforme |
| bloque 5×5 en N=32 | — | 50 | fallback 2 → uniforme |

`_mean_cS` sobre el corpus real: 0.004519 en ambos modos. No es
coincidencia ni evidencia de que el path no corriera — `W_ckm_corpus_v2`
es todo-positiva, así que toda relajación converge al mismo atractor
(σ = +1) y `c(S) = μ_W = 0.004519`, el valor calibrado del corpus. Con
un solo atractor accesible, el generador de σ₀ no puede cambiar el
resultado.

---

## Lo que este REG no establece

- **Que `weighted=True` mida mejor la diversidad del paisaje.** El único
  caso donde los conteos difieren es una W sintética con hub, y ahí el
  conteo ponderado es *menor* (8 < 13). La TASK argumenta que el muestreo
  uniforme sobremuestrea zonas muertas y por eso subestima; en esta única
  prueba el efecto observado va en la dirección opuesta. Un conteo menor
  es consistente tanto con "concentra el muestreo en pocas cuencas
  reales" como con "pierde diversidad". No hay criterio en esta corrida
  para distinguir.
- **Que el corpus CKM real se beneficie.** Con `A=2` sobre
  `W_ckm_corpus_v2`, el corpus no discrimina entre modos.
- **El caso que motiva la TASK — W_mixta con nodo tipo-965 — no fue
  probado.** No hay una W_mixta con tipo-965 cargada en `services/`. La
  W sintética con hub es un sustituto estructural, no ese caso.

El código está en su lugar y es reversible por default. El valor
experimental de `weighted=True` está abierto.

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
