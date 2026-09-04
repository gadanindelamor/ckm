# REG_boltzmann_sampling_v1.md

*Ago 2026 — gadanin.delamor + Claude Code*
*Clase R*

---

## Addendum — corrección de dos afirmaciones de este mismo REG

*Agregado Ago 2026, misma sesión. El cuerpo original queda intacto abajo:
lo que sigue no lo reemplaza, lo corrige por encima. La divergencia entre
lo que se afirmó y lo que se midió después es parte de la traza.*

La sección **"Hallazgo no previsto — β_c depende de la escala de W"** del
cuerpo de este REG afirma dos cosas que la medición posterior contradice.

### Corrección 1 — el muestreo YA es invariante de escala

El cuerpo dice que β_c queda determinado por la escala numérica de los
pesos, y presenta una tabla de β_c contra W×10, ×100 como si eso cambiara
el muestreo. **No lo cambia.** Lo único que entra a la probabilidad de
transición es el producto β_c·h, y ese producto es exactamente invariante:

β_c ∝ 1/μ_W y h ∝ μ_W — se cancelan.

Medido, `n_runs=50`, `n_warmup=32`:

| W_eff | β_c | β_c·\|h\| | A boltzmann |
|---|---:|---:|---:|
| `W_ckm_corpus_v2` ×1 | 10.4575 | 0.0650 | 2 |
| ×10 | 1.0458 | 0.0650 | 2 |
| ×100 | 0.1046 | 0.0650 | 2 |
| ×0.01 | 1045.7544 | 0.0650 | 2 |
| W densa+hub ×1 | 0.0844 | 10.2025 | 19 |
| W densa+hub ×100 | 0.0008 | 10.2025 | 19 |

Cuatro órdenes de magnitud, conteo idéntico. El β_c aislado no es una
temperatura legible; β_c·h sí.

### Corrección 2 — la interpretación estaba invertida

El cuerpo dice que en la W con hub la temperatura era tan alta que el
calentamiento "se acerca a tirar una moneda por nodo", y que por eso el
conteo de 20 podía ser ruido térmico. **Es al revés.**

| paisaje | β_c·\|h\| | 2β_c·\|h\| | p(σ_i=+1) | régimen |
|---|---:|---:|---:|---|
| W densa+hub | 10.20 | 20.4 | ≈ 1 ó ≈ 0 | casi **determinista** |
| `W_ckm_corpus_v2` | 0.065 | 0.13 | ≈ 0.53 | casi **aleatorio** |

El calentamiento casi-aleatorio ocurre en el corpus real, no en la W
sintética. Y el conteo de 20 en la W con hub **no** es ruido térmico: el
calentamiento ahí es cuasi-determinista y funciona como una prerrelajación
que deposita σ₀ en cuencas distintas antes del relax.

### Qué se sostiene y qué no, del cuerpo original

| afirmación del cuerpo | estado |
|---|---|
| Implementación, firmas, precedencia boltzmann > weighted | se sostiene |
| Sin regresión (28/28, 35/35, default == histórico) | se sostiene |
| Conteos medidos: corpus 2/1/2 — hub 13/8/20 | se sostiene |
| Boltzmann es el primer modo que sube el conteo | se sostiene |
| Los dos β_c (13.83 vs 10.46) son cantidades distintas | se sostiene |
| "β_c depende de la escala numérica de los pesos" | **corregido — β_c·h es invariante** |
| "el 20 es compatible con calentamiento casi aleatorio" | **corregido — es casi determinista** |
| "μ_W crece con Δ_r → el modo se calienta solo" | **no se sostiene por esta vía** — sigue sin medirse el efecto de Δ_r sobre la *forma* de W_eff, que es lo único que puede mover β_c·h |

### Consecuencia sobre la normalización propuesta

Sobre esta corrección se evaluó normalizar W_eff antes de
`_beta_c_landscape()`. Análisis, no ejecutado:

- Normalizar **sólo para β_c** (h desde W cruda) *introduce* una
  dependencia de escala que hoy no existe.
- Normalizar y usar la W normalizada **para β_c y para el warmup** es
  algebraicamente idéntico a lo actual — no-op.
- Normalizar por **μ_W** deja `mean(W'[W'>0]) = 1` por construcción, con lo
  cual β_c ≡ 2/N para todo paisaje: pierde toda información de geometría.
  Por **máximo** conserva β_c ∝ max/μ_W, medida de heterogeneidad.

**Decisión de delamor: no se normaliza.** El análisis de la interpretación
precede al cambio de código; el código no se tocó.

---

## Descripción

Tercer modo de muestreo de σ₀ en `_count_attractors()` de `services/coco.py`:
calentamiento estocástico a temperatura β_c antes del relax determinístico.
Ejecutado según `TASK_boltzmann_sampling_count_attractors_v3_1.md`.

Los tres modos quedan disponibles y son mutuamente excluyentes:

| modo | distribución de σ₀ | usa campo local |
|---|---|---|
| `uniform` (default) | P(nodo) = 1/N | no |
| `weighted` | P(nodo) ∝ \|W_eff\|.sum(axis=1) | no |
| `boltzmann` | σ₀ uniforme + calentamiento a β_c | **sí** |

`boltzmann=True` tiene precedencia sobre `weighted` (verificado).

---

## Paso 0

`hopfield.py` (raíz del repo) tiene la rama estocástica de `relax()` en la
línea 51: `p = 1/(1+exp(-2·β·h))`. `kcore.py` no toca ninguno de estos
caminos — no hay interferencia.

**No se importó `hopfield.py`.** Las razones están verificadas y
documentadas en `docs/VERIF_repo_boltzmann_paso0_v1.md` (reporte del Paso 0
de la v1 de esta TASK): import relativo sin `__init__.py` en la raíz — no es
importable desde `services/` —, firma sobre `CKMGraph` en vez de matriz, y
uso de `np.random.seed()`/`np.random.rand()` (estado **global** de numpy).
Este último es el determinante: `_count_attractors` usa un
`default_rng(self._seed)` aislado, y ese aislamiento es la propiedad de la
que dependen `experiments/stochastic_attractor_eval.py` y
`REG_stochastic_eval_v1/v2` para que una corrida sea reproducible por
`(seed, n_runs, W)`.

La fórmula se reimplementó en `_boltzmann_warmup()` sobre el RNG aislado.
**La duplicación es deliberada y está declarada en el docstring**, con
puntero a `hopfield.py:51`: si esa línea cambia, hay que revisar ésta a mano.
No hay mecanismo que lo detecte.

---

## Implementado

En `services/coco.py`:

- `_beta_c_landscape(W_eff)` — β_c = 1/(ρ*·N·μ_W) con μ_W = `mean(W_eff[W_eff>0])`,
  ρ* = `BETA_RHO_STAR` = 0.5. Se computa **una vez por llamada**, no por run.
  Devuelve `None` si W_eff no tiene pesos positivos → cae a uniforme sin error.
- `_boltzmann_warmup(rng, sigma, W_eff, beta, n_warmup)` — `n_warmup`
  actualizaciones asíncronas de **un nodo por vez**, con reposición.
- `_count_attractors(W_eff, weighted=False, boltzmann=False, n_warmup=None)`.
- `_mean_cS(...)` — mismos tres parámetros, para que A y c(S) sigan
  describiendo las mismas muestras.
- `COCO(..., sampling_mode="uniform", n_warmup=None)` — modo con el que
  `observe()` cuenta. `sampling_mode` inválido lanza `ValueError`.
- `sampling_mode()` — accessor público.

En `services/monitor_service.py`: `panel["thermostat"]["sampling_mode"]` y
`["n_warmup"]` (este último `None` salvo en modo boltzmann).

**Sin regresión, verificado explícitamente:** el conteo con los defaults se
comparó contra una reimplementación del loop histórico sobre
`W_ckm_corpus_v2.json` — mismo resultado. `tests/test_coco.py` 28/28,
`tests/test_monitor_services.py` 35/35.

---

## Resultado — y aquí el modo se comporta al revés que el ponderado

`W_ckm_corpus_v2.json` (N=32, todo-positiva, densidad 0.73), n_runs=50:

| modo | A |
|---|---|
| uniforme | 2 |
| ponderado | 1 |
| boltzmann (n_warmup 8/16/32/64/128) | 2 / 2 / 2 / 2 / 2 |

El corpus real no discrimina: siendo W todo-positiva, casi toda relajación
converge al mismo atractor. Ningún generador de σ₀ puede cambiar eso.

W sintética densa con hub (N=32, fila/col 0 ×20), n_runs=50:

| modo | A |
|---|---|
| uniforme | 13 |
| ponderado | 8 |
| **boltzmann** | **20** (n_warmup 8/32/128 → 19/20/21) |

**Es el primer modo que produce más estados terminales que el uniforme.**
El ponderado bajaba el conteo en 92/100 pares (`REG_stochastic_eval_v2`);
éste lo sube. Las tres direcciones son distintas entre sí.

No se afirma que sea mejor cobertura de cuencas. Ver §"lo que no establece".

---

## Hallazgo no previsto — β_c depende de la escala de W

β_c = 1/(ρ*·N·μ_W) es inversamente proporcional a μ_W, así que **la
temperatura de muestreo queda determinada por la escala numérica de los
pesos**, no sólo por la geometría del paisaje:

| W_eff | μ_W (no-nulos) | β_c |
|---|---:|---:|
| `W_ckm_corpus_v2` | 0.00598 | 10.46 |
| ×10 | 0.05977 | 1.05 |
| ×100 | 0.59765 | 0.10 |
| sintética densa+hub | ~0.5 | **0.084** |

Una W con pesos grandes recibe un β_c muy chico — es decir, temperatura
**alta**: el calentamiento se acerca a tirar una moneda por nodo. Eso es
consistente con el conteo alto observado arriba en la W con hub (20), y
significa que ese número puede estar diciendo "el calentamiento fue casi
aleatorio" y no "el muestreo cubrió más cuencas". Los dos son compatibles
con lo medido.

`W_eff = W + Δ_r` acumula rechazos sin normalizar, así que **μ_W crece
durante una sesión y β_c baja**: el modo boltzmann se calienta solo a
medida que Δ_r se acumula. No fue evaluado.

`hopfield.py:32-33` declara una zona de trabajo `beta ∈ [3, 100]`. El β_c
del corpus real (10.46) cae dentro; el de la W sintética (0.084) queda dos
órdenes por debajo. No hay chequeo de rango en la implementación — no se
agregó porque la TASK no lo pide y porque no está establecido que esa zona
aplique a este uso.

---

## Los dos β_c

| | fórmula | valor en W_ckm_corpus_v2 | para qué |
|---|---|---|---|
| `beta_c_corpus()` | μ_W sobre triángulo superior, **incluyendo ceros** | **13.83** | referencia de TEMP_SIGNAL |
| `_beta_c_landscape()` | μ_W sobre **pesos no-nulos**, sobre W_eff | **10.46** | temperatura de muestreo |

Razón 0.756. La TASK v3_1 especifica explícitamente "media de W sobre pesos
no-nulos" (línea 40), así que se implementó así. Son dos cantidades
distintas con el mismo nombre corto; el docstring de `_beta_c_landscape` lo
dice para que no se confundan. `beta_c_corpus()` **no fue tocada** y 13.83
sigue siendo el valor de referencia del proyecto.

---

## Lo que este REG no establece

- **Que boltzmann cubra mejor las cuencas.** Sin conteo exhaustivo de
  atractores no hay referencia contra la cual llamar mejor a ningún modo.
  Es la tercera vez que se registra esto (uniforme, ponderado, boltzmann).
- **Que el conteo alto en la W con hub sea cobertura y no ruido térmico.**
  Con β_c = 0.084 las dos lecturas son compatibles. Distinguirlas requiere
  un barrido de β independiente de μ_W, que no se corrió.
- **n_warmup óptimo.** En el corpus real es indistinguible (2 en todo el
  rango 8–128); en la W sintética varía poco (19–21). Ninguna de las dos
  observaciones alcanza para elegir un valor. Sigue abierto, como declara
  la TASK.
- **Comportamiento bajo W_eff con Δ_r acumulado.** Sólo se probó sobre W
  sola y sobre una W sintética. El efecto de escala descrito arriba dice que
  esto importa; no se midió.
- **Nada quedó cableado.** `sampling_mode` default sigue siendo `"uniform"`:
  ninguna decisión de STOP cambia de comportamiento por esta task. El modo
  es de uso explícito.

---

## Archivos

- `services/coco.py` — `_beta_c_landscape`, `_boltzmann_warmup`, tres modos, `sampling_mode`
- `services/monitor_service.py` — `sampling_mode` / `n_warmup` en el panel
- `docs/VERIF_repo_boltzmann_paso0_v1.md` — por qué no se importa `hopfield.py`
- `iap_chatroom/tests/TASK_boltzmann_sampling_count_attractors_v3_1.md` — spec ejecutada
- `registers/REG_stochastic_eval_v2.md` — modos uniforme y ponderado
- `hopfield.py:51` — fuente de la fórmula, no importada

---

*Ago 2026 — Codespace ckm — bash/Linux*
