# TASK_extraccion_una_rama_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: REG_hipotesis_distancia_contextual_v4; `5aa3504`. Lupa sobre NodeExtractorService.*

---

## Hallazgo

La extracción tiene dos ramas que deberían reconocer los mismos nodos en el mismo texto:

| rama | quién la usa | cómo reconoce un nodo |
|---|---|---|
| `accumulate` | CorpusService → **W** | TF-IDF: regex, minúsculas, sin stopwords, bigramas armados *después* de sacar stopwords |
| `evaluate` | MonitorService → **σ_prompt** | **substring crudo** |

caso09, bootstrap 12 (12 textos): 5 activaciones en W y no en σ ("joined **the** channel" → bigrama `joined channel` que el substring no encuentra); 14 en σ y no en W (`now` por "k**now**", `here` por "w**here**").

*(delamor: está desde hace meses; se actualizó la rama donde estaba la atención y la otra quedó. La extracción no es sutil: es inadvertida — se da por correcta.)*

**Llega a Δ_r:** un nodo que σ declara por substring entra como declarado; si el campo no lo sostiene, sus pares se metabolizan y suben `fabrication_index`.

## Qué hacer

- Un solo constructor del vectorizador (`_vectorizer`) con los parámetros de tokenización. `accumulate` lo usa para ajustar; `evaluate` usa **su analizador** sobre el texto y activa σ_i si el nodo i está entre los términos que el analizador produce.
- Test de paridad: para todo texto, los nodos activos según `accumulate` y según `evaluate` son **el mismo conjunto**.

## Verificación

- Paridad en caso09 (24 textos) y en los textos de los tests.
- Antes/después sobre caso09 bootstrap 12, W congelada: activos de σ_prompt, `fabrication_index`, `n_rejected_pairs`, `Delta_r_sum`, D_ckm.
- Tests existentes: los que dependan de σ por substring pueden cambiar — se revisan uno por uno.

## Consecuencia declarada

Cambia σ_prompt en todo panel. `fabrication_index`, Δ_r y D_ckm previos valen en su marco: σ por substring.

## Qué no hace

- No cambia `max_features = top_k·3` (criterio declarado; se corrige el docstring que lo omite).
- No resuelve bigramas que contienen unigramas nodo.
- No amplía stopwords.
