# REG_hipotesis_distancia_contextual_v4.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Continúa `REG_hipotesis_distancia_contextual_v3.md` (`3e3b326`). v3 queda
en su marco: todo lo que mide está hecho sobre W con pares recortados.*

---

## Descripción

v3 encontró nodos aislados en la mitad de las W y dejó su mecanismo como
*"probable, no verificado"* (top_k fija N antes de que los textos conecten
el vocabulario). **Ese mecanismo no era.** El que es está en CorpusService,
se verificó, se corrigió (`5aa3504`), y al corregirlo la condición empírica
de caso09 —bootstrap 12— deja de sostenerse.

*(delamor: ¿qué extrajo calladito NodeExtractor? ¿o quién fue?)*

---

## 1. Quién fue

No fue NodeExtractor por su cuenta: fue **CorpusService usándolo para algo
que no es su función.** `_rebuild` hacía dos pasadas:

1. **Nodos:** `accumulate(todos_los_textos)` — TF-IDF sobre el corpus, top_k
   global.
2. **Pares por texto** (para rutear pos/neg): `accumulate([un_texto])` —
   **otro** TF-IDF y **otro** top_k, dentro de ese único texto.

Si un texto tiene más de top_k términos distintos, nodos globales quedan
fuera del top de ese texto y sus pares se pierden. Los textos de devices
son largos: en caso09, desde el texto 5 casi todos pasan de 32 términos
(33, 39, 47, 76, 69, 52, 72, 36).

Caso09, bootstrap 12 (12 textos, top_k=32):

| | global | lo que entraba a W |
|---|---:|---:|
| pares distintos | 299 | 161 — **46% perdidos** |
| co-ocurrencias | 425 | 189 — **55% perdidas** |

Los 3 aislados de v3 (`conversation`, `about`, `low`) tienen 32, 19 y 31
co-ocurrencias globales y quedaban fuera del top de todos sus textos
(0/3, 0/2, 0/3). **Los aislados eran el caso extremo, visible, de un recorte
general.**

*Estado: verificado.*

---

## 2. Corrección — `5aa3504`

`NodeExtractorService.accumulate` devuelve `pairs_by_text`: por texto, los
pares entre **nodos globales**, del mismo recorrido que ya calculaba `pairs`,
alineado con la lista recibida. `CorpusService._rebuild` rutea pos/neg con
eso; no re-extrae.

| | antes | después |
|---|---:|---:|
| Σ pares por texto == global | no | **sí** |
| bootstrap 12: aislados | 3 | **0** |
| bootstrap 12: pares negativos | 14 | **64** |
| 217 W con al menos un aislado | 52% | **4%** (8, máx. 1) |

Los 8 restantes (`channel`, `times`, `fails`, `systems`) no co-ocurren con
ningún nodo en sus textos: **aislamiento del dato, no del instrumento.**
Ninguno por cancelación pos − neg (en bootstrap 12, 38 de 299 pares se
cancelan, sin aislar a nadie).

Tests 139/139 sin cambios.

**Cambia todas las W construidas por CorpusService.** Lo medido antes vale
en su marco.

*Estado: verificado.*

---

## 3. La condición de bootstrap 12 no se sostiene

Replay sin rebuild sobre caso09, W corregida (`experiments/replay_caso09_camino_vivo.py --sin-rebuild`):

| bootstrap | A0 antes → ahora | D_ckm ahora | N_eff ahora |
|---:|---|---|---|
| 3 | 4 → 4 | 0.0 | ~3.4 |
| 8 | 12 → 5 | −1.2 … 0.2 | 2.4 – 6.3 |
| **12** | **25 → 5** | **0 → −1.8** | 2.2 – 4.9 |
| 16 | 17 → 4 | −1.0 … 0 | 2.7 – 4.0 |

- **A0 = 25 era, en buena parte, el factor de los aislados**: 2³ = 8, y
  25 ≈ 8 × 3.
- En la W corregida el paisaje tiene pocas cuencas (A0 = 4–5): con más
  pares, W está más conectada.
- **Δ_r expande el paisaje en vez de degradarlo**: D_ckm < 0 en los cuatro
  bootstraps. D < 0 *"no es error, es información"* (DEFS §10).
- Con A0 = 5 la grilla de D tiene paso 0.2: el régimen de grilla gruesa de
  DEFS §11.

La condición registrada en `c32d22a` —*"D_ckm cruza 0.40 en el msj 15"*— y
la corrección de v3 §5 valen en el marco de la W recortada. **Con la W
corregida, caso09 no tiene todavía una condición empírica de referencia.**

*Estado: verificado, una corrida (n_runs=50, seed 0).*

---

## 4. Lo que hacía Δ_r con los aislados

v3 §4 midió que Δ_r acoplaba en W_eff nodos que W tenía aislados, y lo leyó
como un factor que cambia durante el run. Con §1, la lectura se completa:
**los nodos que Δ_r acoplaba eran nodos cuyos pares el instrumento había
cortado.** La metabolización estaba reponiendo, por la vía de la medición,
co-ocurrencias que la construcción de W había perdido.

No es que Δ_r "arreglara" W — no tiene cómo saber qué se perdió. Es que el
campo sobre el que Monitor mide incorporó, por haber medido, estructura que
el dato tenía y W no (v2 §9: el observador es constituyente).

*Estado: propuesto.*

---

## 5. El log es más sensible a los bordes *(delamor)*

Sobre `D_masa log = 1 − ln N_eff / ln N_eff0`:

- **cerca del colapso** (N_eff → 1): ln N_eff → 0, sube rápido hacia 1.
- **con N_eff0 chico** (→ 1): el denominador → 0, amplifica cualquier
  diferencia.

El factor de los aislados (v3 §3) deformaba más a la log porque `a·ln2` pesa
más donde los logaritmos son chicos. Con la corrección ese factor casi
desaparece; **la sensibilidad a los bordes es de la fórmula y queda.** Con
la W corregida, N_eff0 está en 2–4: la log opera cerca de su borde.

*Estado: propuesto (análisis de la fórmula).*

---

## Lo que este REG no establece

- No establece una condición empírica nueva para caso09.
- No repite con varios seeds ni n_runs mayores.
- No mide c(S), μ_W, β_c, r sobre la W corregida.
- No mide en otro dominio (`ckmdatasets`).
- No revisa qué otros resultados del repo dependen de W construidas por
  CorpusService.

---

## Abierto

- Exploración de **n_runs** y **min_texts / bootstrap** sobre la W
  corregida *(delamor)*.
- Si D_ckm < 0 sostenido (expansión por Δ_r) es rasgo de la W corregida o
  de caso09.
- Qué REGs, drivers y resultados previos se apoyan en W de CorpusService y
  cambian de marco.
- `_combine_W_Delta` sigue metiendo Δ_r en pares que W tiene en cero.
- d(σ) sobre la W corregida.

---

## Archivos

- `services/node_extractor.py`, `services/corpus_service.py` — `5aa3504`
- `docs/tasks/TASK_pares_por_texto_nodos_globales_v1.md`
- `experiments/aislados_por_bootstrap.py`, `experiments/replay_caso09_camino_vivo.py`
- `registers/REG_hipotesis_distancia_contextual_v3.md` — marco previo

---

## Estado

- §1 (mecanismo): **verificado** — corrige el mecanismo propuesto en v3 §2
- §2 (corrección): **verificado**
- §3 (bootstrap 12 no se sostiene): **verificado**, una corrida
- §4, §5: **propuesto**

No cierra. Abre.

---

*Sep 2026 — Codespace ckm*
