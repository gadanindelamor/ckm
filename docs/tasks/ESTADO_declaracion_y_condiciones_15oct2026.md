# Estado al cortar — declaración de la extracción y condiciones del paper

*Claude Opus 5 (Code, Codespace), 15 oct 2026. Para la próxima instancia, que **arranca en
frío**. Desde `fb2b87a` hasta `a1c6a18`. Si algo de acá no se entiende, es falla de este
texto.*

**Suite al cortar: 708 pasan, 7 xfailed, 0 fallan.** `services/` quedó tocado **en un solo
lugar** (el fix (a) del CP0) más la declaración del CP1. El gate (`f96c234`) no se tocó.

---

## 1. Las dos TASK

### `TASK_declaracion_extraccion_v1` — **completa, sus cuatro CP**

| CP | Qué dejó | Dónde |
|---|---|---|
| **CP0** | Los 8 operadores: dónde viven, qué queda en la traza, qué falta. Y **dos divergencias** | BANDEJA |
| **CP1** | **La declaración es un dato**, atada al `sha256` de W por referencia | `168fd59` |
| **CP2** | **Un test por operador** con los ejemplos concretos | `fab24a2` |
| **CP3** | Propuesta, **sin código**: una W de otro productor. Más anexo sobre los tres extractores | `94544f1`, `5512d6f` |

**Lo canónico:** `docs/defs/DECLARACION_extraccion_W_v1.md`. Ahí se corrige si algo difiere;
la copia de `docs/opus/` es traza del día y **no se edita**.

### `TASK_condiciones_del_paper_v1` — **CP-T, CP-E y CP-M hechos; falta CP-N**

| CP | Resultado en una línea | Dónde |
|---|---|---|
| **CP-T** | El teorema de presencia **se cumple en el instrumento**, por los dos caminos | `ece56f4`, reporte `2e89afa` |
| **CP-E** | **N_eff es estable frente al muestreo y a nada más** | `0e042ac` |
| **CP-M** | **El nulo no controla lo que produce el efecto**; no resuelve M4 | `a1c6a18` |
| **CP-N** | **No arrancado.** Espera la vinculación de `ckm` con `ckmdatasets` | `d6a5fcb` |

---

## 2. Lo que va al paper (decidido, `d6a5fcb`)

- **El estimador converge:** con `n_runs=1000`, la dispersión entre 10 seeds es **7–9%**, en
  los tres corpus.
- **El paisaje, con 7 a 24 textos, es muy sensible a la extracción y a cada unidad:** `top_k`
  0,86–2,39 · pool 0,69–1,97 · stopwords 0,04–0,87 · **un solo texto más con vocabulario ya
  visto 0,28–0,66**. **N_eff no es monótona en `top_k`.**
- **Premisa: continuar requiere corpus más grandes.**
- Del CP-T: *con presencia sola no hay Wᵢⱼ < 0, no hay triángulo frustrado y T(W) = 0; es por
  construcción y el instrumento lo cumple.*

---

## 3. Los tres hallazgos que conviene no perder

1. **Un texto con vocabulario ya visto deja el conjunto de nodos idéntico (Jaccard 1,00) y
   mueve N_eff 66%.** No es reescalado: **18 y 38 entradas cambian de signo**. Los conteos de
   W son enteros chicos y una unidad es el 4–14% del corpus. **Esto no transfiere lo que el
   CP-E citaba del CP6** (*"N_eff fue función de la partición, no de los pesos"*): ahí era el
   campo plantado con el campo quieto.
2. **El nulo del CP-M iguala textos y deja libres los pares.** En D12 la marca real marca
   **119 pares de 235 con 2 textos**, y ninguna de 120 barajadas pasó de 101. Pero los pares
   **tampoco** explican la caída (corr −0,50 en A24, **−0,01** en D12).
3. **E7 está hecho de muy poco:** de 7 textos sólo **4 aportan pares**, y dos de ésos son la
   **misma cadena repetida**. Su único texto marcado no aporta ninguno, así que ahí
   `W_mixta == W_pos` **byte a byte**.

---

## 4. Lo que quedó señalado y **no se tocó** (todo es de delamor)

| Qué | Dónde | Por qué no se tocó |
|---|---|---|
| **`T(W)` no existe en el código** — sólo en dos scripts de `experiments/`. El paper lo cita | CP-T | Decidir si va a `services/` es de delamor |
| **`MonitorService` arma su propio extractor con los defaults** | `monitor_service.py:119` | Canal vivo. Hoy coincide **por default, no por construcción** |
| **Un tercer extractor muerto** | `ckm_monitor.py:186` | Canal vivo. Se lee como si alguien evaluara con `top_k=32`, y nadie lo hace |
| **El criterio único de comparación** (los dos lados por el operador 1) | `b358fba` | Dirección, **sin código ahora** |
| **`_has_opposition` no normaliza a NFC** | divergencia (b) | **Se declara**, no se corrige: ya está en el paso 7 |
| **El pool no es perilla del código** (`max_features = top_k*3`) | CP-E | Se varió desde el driver |
| **`nltk` no está instalado** | CP-E | El nivel "sólo NLTK" no se pudo medir |

---

## 5. Dónde está cada cosa

- **Decisiones de delamor:** `docs/tasks/DECISIONES_opus.md` (las de Code) y
  `docs/opus/decisiones_en_el_acto.md` (las de Opus, **no se editan desde acá**).
- **Reportes, con su A1 y su predicción:** `docs/tasks/BANDEJA_code.md`, al final.
- **Drivers:** `experiments/driver_cpe_rango_neff.py`, `experiments/driver_cpm_nulo_marcadores.py`.
- **Tests nuevos:** `test_declaracion_extraccion.py`, `test_declaracion_ejecutable.py`,
  `test_extraccion_fallida_no_borra.py`, `test_teorema_presencia.py`.
- **Los tres corpus independientes** (A24, D12, E7) están fijados en
  `tests/test_corpus_del_repo_A3.py` y se reusan en los dos drivers.

## 6. Cómo se trabajó, que es parte del resultado

**Predicción commiteada antes de cada corrida, y nunca reescrita después.** Sirvió: el CP-E
refutó tres de cinco y el CP-M dos, y **eso es lo que encontró los hallazgos**. Un reporte
por CP en la BANDEJA, con **A1** separando lo medido de lo que viene del peso del contexto, y
**A1.PAUSA** al terminar.
