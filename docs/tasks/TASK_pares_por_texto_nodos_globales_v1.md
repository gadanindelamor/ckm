# TASK_pares_por_texto_nodos_globales_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: REG_hipotesis_distancia_contextual_v3 §2 — mecanismo de los nodos aislados, verificado en esta sesión.*

---

## Hallazgo

`CorpusService._rebuild` hace dos pasadas:

1. **Nodos:** `accumulate(todos_los_textos)` — TF-IDF sobre el corpus, top_k global.
2. **Pares por texto** (para rutear a pos/neg): `accumulate([un_texto])` — **otro** TF-IDF y **otro** top_k, dentro de ese único texto. Si el texto tiene más de top_k términos distintos, nodos globales quedan fuera del top del texto y sus pares se pierden.

Medido en caso09, bootstrap 12 (12 textos, top_k=32):

| | global | por texto (lo que entra a W) |
|---|---:|---:|
| pares distintos | 299 | 161 — 46% perdidos |
| co-ocurrencias | 425 | 189 — 55% perdidas |

Los 3 nodos aislados (`conversation`, `about`, `low`) tienen 32, 19 y 31 co-ocurrencias globales y 0 en W: no entran al top de ninguno de sus textos. Los aislados son el caso extremo del mismo recorte.

## Qué hacer

- `NodeExtractorService.accumulate` devuelve además `pairs_by_text`: por cada texto, los pares entre **nodos globales** presentes en él — el mismo recorrido que ya hace para `pairs`.
- `CorpusService._rebuild` rutea a pos/neg usando `pairs_by_text[k]` del texto k. No vuelve a extraer.

Pares y nodos salen de la misma tokenización y el mismo conjunto de nodos. Σ pos + neg = pares globales, por construcción.

## Verificación

- Σ (pos + neg) de todos los textos == `pairs` global.
- caso09 bootstrap 12: aislados 3 → medir; pares perdidos → 0.
- `aislados_por_bootstrap.py` antes/después sobre los 217 W.
- Tests existentes: los que dependan de valores de W pueden cambiar — se revisan uno por uno.

## Resultado

- Σ pares por texto == pares globales: verificado.
- caso09 bootstrap 12: aislados 3 → **0**; pares negativos 14 → 64; pares no nulos 261 (de 299 globales: 38 se cancelan por pos = neg).
- 217 W (`aislados_por_bootstrap.py`): con aislados **52% → 4%** (8/217, máx. 1). Los 8 restantes no co-ocurren con ningún nodo en sus textos — aislamiento del dato, no del instrumento. Ninguno por cancelación pos − neg.
- Tests: 139/139 sin cambios. `corpus_service.py` y `node_extractor.py` self-test OK.

## Consecuencia declarada

**Cambia todas las W del proyecto construidas por CorpusService.** Resultados previos (REGs, drivers, paneles) valen en su marco: W construida con pares recortados por texto.

## Qué no hace

No cambia la selección de nodos (top_k global), ni la regla de marcadores de oposición, ni la normalización `/ max|pos − neg|`.
