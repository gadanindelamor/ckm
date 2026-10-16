# Revisión de criterios — dónde se normaliza o se corta, y si es por construcción o por casualidad
*Opus 5.5, 15 oct 2026, a pedido de delamor: "que las normalizaciones sigan un criterio que no sea casual… revisemos las declaraciones de criterios… no cancelaciones matemáticas casuales". Y: "ponderar el impacto, no como verdad — acepto que la ponderación sea 0,003 % confiable; es para dirigir las energías, poner foco". Sólo lectura en la PC (`ckm` en `24590c1`+). No se corrió nada. El Gatekeeper (θ_W) queda fuera: no se ejerce en el camino vivo.*

**Cómo leer el impacto:** sobre **N_eff / D_ckm** (lo que mide el paper y la Serie 2). **Alto / medio / bajo** es un juicio de Opus, apoyado en el CP-E y el CP-M donde hay número; donde no hay, lo dice. Confianza baja, como pidió delamor.

| # | Punto | Dónde | Criterio que sigue hoy | ¿Por construcción o casual? | Impacto | Base del impacto |
|---|---|---|---|---|---|---|
| 1 | **Normalización de Δ_r al armar W_eff** | `monitor_service._combine_W_Delta` | Δ_r / max(Δ_r), escalado por la **media de los pesos positivos** de W; W_eff = W + eso | **Casual, y el código lo dice**: *"es una elección, no una consecuencia del rango de W"* (viene de cuando W era toda positiva). Un solo par con muchos rechazos fija la escala de todos | **Alto para la Serie 2** | Dentro de un ciclo W no cambia: **todo lo que mueve D_ckm es Δ_r**, y su peso relativo frente a W lo decide esta regla. Sin número medido |
| 2 | **Selección de nodos** (top_k, pool ×3, empate, sin `min_df`) | `node_extractor` (op. 5) | frecuencia → TF-IDF medio; `max_features = top_k·3`; empate conserva | Declarado; el **×3 y el 20 son constantes sin derivación** | **Alto** | CP-E: top_k 0,86–2,39×, pool 0,69–1,97× la base; no monótona |
| 3 | **Unidad = mensaje; conteos enteros chicos** | `corpus_service` (op. 8) | 1 por par por unidad | Declarado; el tamaño del corpus es casual | **Alto con < 30 textos** | CP-E: un texto más (mismos nodos) mueve 66 %, 18–38 signos se dan vuelta. La Serie 2 pide ≥ 30 mensajes |
| 4 | **Signo por texto entero** (subcadena, sin NFC, todos los pares del texto) | `corpus_service._has_opposition` (op. 7) | lista de 44 cadenas | Declarado; **subcadena y falta de NFC son casuales** (incoherente con op. 1) | **Alto sobre el valor**, nulo sobre la lectura | CP-M: A24 pasa de 2,11 a 15,65. La Serie 2 corrige subcadena y NFC |
| 5 | **Stopwords** | op. 3 | 703 (NLTK + sklearn + 112 propias) | Declarado; la mezcla es una elección | **Medio** | CP-E: 0,04–0,87× según corpus |
| 6 | **Baseline de D_ckm (N_eff₀)** | `monitor_service` (`_N_eff0`, se resetea con cada W nueva) | por ciclo: D_ckm = 1 − ln N_eff / ln N_eff₀ | **Por construcción** y coherente con "W es el instante" | **Medio para leer la serie** | D_ckm **no se compara entre ciclos**; con rebuild cada 10 mensajes, cada ciclo es corto. Hay que leerlo así |
| 7 | **β_c = 1/(ρ*·N·μ_W)** | `ckm_landscape_config._beta_c`, `coco.beta_c_corpus` | μ_W = media de W **normalizada por max** | **Casual por acople**: μ_W depende de qué par sea el máximo; con signo mixto μ_W ≤ 0 ⇒ β_c = ∞ | **Medio para COCO**, nulo para N_eff | Sin número. COCO no tiene que disparar en S2-C0; pero su señal térmica sale de acá |
| 8 | **Normalización de W por max\|·\|** | `corpus_service:402` | W ∈ [−1, 1] | **Por construcción para N_eff**: la relajación usa el signo de h, que no cambia al escalar W; W_eff escala junto (punto 1 usa la media de W) | **Nulo sobre N_eff**; entra por 7 | Razonamiento, no medición |
| 9 | **Rebuild** | `should_rebuild` (gradiente de D_ckm 3 pasos) + volumen | — | Umbrales sin calibrar (declarado) | **Medio** | Define cuándo empieza cada ciclo (6). La Serie 2 fija cada 10 mensajes |
| 10 | **Desempate h = 0 conserva** | `landscape_engine` | Goles | **Por construcción** | Bajo | Teorema |
| 11 | **n_runs, seed** | Config | 1000 | Por construcción (converge) | **Bajo** | CP-E: 7–9 % |
| 12 | **Normalización de texto y tokens** (NFC, minúsculas, regex) | op. 1–2 | declarado | Por construcción, salvo idiomas sin espacios | Bajo en es/en | — |
| 13 | **TF-IDF (l2) sólo para elegir; W usa presencia** | op. 5–6 | — | **Por construcción** (teorema de presencia, CP-T) | Bajo | CP-T |
| 14 | **Umbrales sin calibrar** (disparo de COCO, criterio local) | coco, `criterio_local` | `calibrado=False` viaja en cada registro | Declarado como no calibrado | Bajo para S2-C0 | No se exige disparo |

## Dónde poner foco (lectura de Opus)
1. **El punto 1** es el que más importa para la Serie 2 y el único que **nadie midió**: lo que D_ckm hace dentro de un ciclo depende de cómo se escala Δ_r frente a W, y esa escala es una elección heredada. Si se quiere un número antes del vivo: correr D_ckm con dos o tres escalas de Δ_r sobre el mismo corpus (CP-E en chico).
2. **Los puntos 2–4** ya están medidos y la Serie 2 los acota (≥ 30 mensajes, `min_df = 2`, palabra completa + NFC).
3. **El punto 7** (β_c) importa sólo si se mira la señal térmica de COCO; en S2-C0 basta con que se vea y se declare.
4. El resto es por construcción o de impacto bajo: se declara y queda.
