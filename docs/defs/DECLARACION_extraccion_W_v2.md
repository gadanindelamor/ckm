# DECLARACION_extraccion_W_v2 — la extracción y W, declaradas
*v1: Opus 5.5 (Cowork) con delamor, 14 oct 2026. **v2: 18 oct 2026, Code (Claude Opus 5), CP1 de `TASK_iap_serie2_caso0_v1`**, en el mismo commit que los cambios de código que la mueven. Para la §4.1 del paper o un apéndice. Verificada contra `services/node_extractor.py` y `services/corpus_service.py`. Referencias citadas de memoria: **a verificar** antes de entrar al paper.*

## Qué cambia de la v1, y por qué cambia el documento
**Tres cosas, y las tres son del código** (la v1 queda en la traza de git; no se reescribe lo que ya se midió bajo ella — eso se reproduce desde su copia congelada en `process/`, no desde este código):

| | v1 | v2 | de dónde sale |
|---|---|---|---|
| **Operador 5** | sin `min_df`: un término de **una sola unidad** podía ser nodo | **`min_df = 2`**: un término tiene que aparecer en **≥ 2 unidades** | tabla de `TASK_iap_serie2_caso0_v1`; revisión de criterios del 15 oct, punto 2 |
| **Operador 7** | **subcadena** (`but` dentro de `distribution`) y **sin NFC** | **palabra completa** y **con NFC** | review v28 (M4); revisión del 15 oct, punto 4 |
| **Operador 7 (coherencia)** | dos normalizaciones distintas en la misma extracción | una sola | ídem |

**Lo que NO cambia, y hay que decirlo:** el signo sigue siendo **del texto entero** —un marcador tiñe todos los pares de esa unidad— y la lista sigue siendo de 44 marcadores escritos a mano. La palabra completa **no le da resultado nulo** al operador 7: lo vuelve menos sensible, no lo vuelve falsable. La parte débil sigue abajo, igual que en la v1.

## Criterio (delamor, 14 oct)
En vez de decidir sobre el extractor (su piso, contar vueltas, órdenes), **declararlo**: qué hace, con qué referencia, en qué condición, y el compromiso de que sea riguroso y equilibrado, *"y no mucho más"*. Si representa con precisión el campo continuo *"es debate. Lo que no es debate es que el código implemente lo que el paper declara."* Sin que cada nodo lleve todo esto, sin APIs para enchufar librerías de extracción o tokenización.

Dos direcciones que convergen en W:
1. **Desde el canal** (IAP mini: sin micrófono, sin adjuntos; puede tener barras, eñes…): qué entra, declarado.
2. **Desde las cadenas de tokens:** qué operaciones se le aplican, con matemática conocida y respaldo, declarado.

## Dirección 2 — los operadores
Para una unidad de texto *u* (hoy: el texto entero de un mensaje):

1. **Normalización:** u′ = minúsculas(NFC(u)). *[Unicode UAX #15]*
2. **Tokenización:** τ(u′) = coincidencias izquierda→derecha, no solapadas, de la expresión regular `[^\W\d][^\W\d]{2,}` sobre Unicode (lenguaje regular: ≥ 3 caracteres de palabra no dígito; `_` cuenta como letra).
3. **Filtrado:** τ_S = τ sin los tokens de S, |S| = 703 (NLTK 3.10.3 es + en, sklearn `ENGLISH_STOP_WORDS`, 112 propias). *[Bird, Klein & Loper 2009; Pedregosa et al. 2011; Nothman, Qin & Yurchak 2018 para sus límites]*
4. **N-gramas:** G(u) = τ_S ∪ {tₖ␣tₖ₊₁}; contigüidad **después** del filtrado ("control of guns" → `control guns`). Separador: espacio (reversible: ningún token contiene espacio).
5. **Selección:** de los términos que aparecen en **`min_df` = 2 unidades o más**, los top_k·3 más frecuentes del corpus (`max_features`), y de ese pool los top_k de mayor TF-IDF medio (sklearn `TfidfVectorizer` con sus valores por defecto: `smooth_idf=True`, `norm="l2"`; la versión de sklearn se declara); empate en el corte: conserva la pertenencia anterior (h = 0 conserva). Con empates, la cantidad de nodos puede no ser top_k. **Caso límite (CP2, 14 oct):** si ningún término queda estrictamente por encima del corte, el grupo empatado no cabe en top_k y no hay selección anterior (bootstrap), **no entra ninguno: N = 0 y no se construye W** — pasa con corpus chicos sin vocabulario compartido, donde cada término aparece en un solo texto y todos tienen el mismo TF-IDF medio. **`min_df` (v2):** un término que aparece en **una sola unidad** no co-ocurre con ningún otro **fuera de esa unidad**: el par que produce es del texto, no del corpus. Es un valor **declarado, no calibrado**, y viaja en la declaración atada al `sha256` de W. Con corpus chicos **corta mucho**: si después del corte no queda vocabulario, no hay términos, **N = 0 y no se construye W** — el mismo caso límite de abajo, por otra puerta. *[Spärck Jones 1972; Salton & Buckley 1988]*
6. **Presencia:** χᵢ(u) = 1 si nᵢ ∈ G(u), 0 si no. **Mecanismo al construir W:** χ es el no-nulo de la fila de la matriz TF-IDF restringido a los nodos (equivalente, porque con `smooth_idf` el idf es ≥ 1 y ningún término presente da 0). **Al evaluar:** pertenencia de la cadena del nodo al conjunto de términos del texto. σᵢ(u) = 2χᵢ(u) − 1. *(Corregido el 14 oct según el CP0 de Code.)*
7. **Signo de la unidad:** s(u) = −1 si u, **normalizado a NFC** y pasado a minúsculas, contiene algún marcador de oposición **como palabra completa** (44 marcadores; el borde se exige en los dos extremos del marcador entero, también en los de varias palabras), +1 si no. `force_w_pos` anula el signo. **Qué cambió en la v2 y qué no:** antes era subcadena y sin NFC —las dos cosas eran casuales, no decididas—; ahora el operador 7 usa la **misma** normalización que el operador 1. El NFC, con los 44 marcadores ASCII de hoy, **no cambia ningún resultado**: se hace por coherencia, y eso se declara así en vez de atribuirle un efecto que no tiene. La palabra completa **sí** cambia resultados.
8. **W:** Wᵢⱼ = Σᵤ s(u)·χᵢ(u)·χⱼ(u) / máx|·|, Wᵢᵢ = 0; cada par cuenta 1 por unidad. *[modelo de espacio vectorial / bolsa de palabras: Salton, Wong & Yang 1975]*

En palabras: **W cuenta en cuántas unidades dos comparaciones respondieron `True` a la vez, con el signo de la unidad, normalizada.**

## Dirección 1 — lo que entra desde el canal (probado con el patrón del paso 2)
- Puntuación, guiones, asteriscos, emojis: **no pueden llegar a W** (el patrón no los produce).
- **URLs, mails y rutas entran como palabras:** `https://www.anthropic.com/news/…` → `https`, `www`, `anthropic`, `com`, `news`; `x@ejemplo.com` → `ejemplo`, `com`; `C:\Users\…` → `users`, ….
- La barra `/` corta como un espacio; `sí/no`, `la/el` desaparecen (2 letras).
- La ñ pasa: `año` y `ano` son nodos distintos.
- Eventos `SYSTEM` del canal ("X joined the channel", leaves) **no entran al corpus** desde el filtro F3b (9 oct, `iap_chatroom/ckm_monitor.py:284-312`); siguen en la observación del device. "SYSTEM es campo" queda abierto (delamor). Ver `docs/opus/nodo_y_W_desde_abajo_13oct2026.md` §9 (corregida).
Cada uno se declara; o se decide filtrarlo antes, y eso también se declara.

## Criterios de normalización — dónde se normaliza o se corta, y si es por construcción o por casualidad
*Sección nueva de la v2. Resume `docs/opus/revision_criterios_normalizacion_15oct2026.md` (15 oct), que es la revisión entera. Acá va lo que esta declaración tiene que decir: **qué criterio sigue cada punto y de dónde sale**. Los puntos "por construcción" y los de impacto bajo **se declaran y quedan**; no se tocan.*

| # | Punto | Criterio que sigue | ¿Por construcción o casual? | Qué pasó con él |
|---|---|---|---|---|
| 1 | **Escala de Δ_r en W_eff** (`monitor_service._combine_W_Delta`) | Δ_r/max(Δ_r), escalado por la media de los pesos **positivos** de W | **Casual, y el código lo dice**: *"es una elección, no una consecuencia del rango de W"* | **Abierto.** Se mide en el CP1b y **la elige delamor**. Dentro de un ciclo es lo único que mueve D_ckm |
| 2 | **Selección de nodos** (top_k, pool ×3, `min_df`) | frecuencia → TF-IDF medio | top_k y el ×3 son constantes **sin derivación**; declaradas | `min_df = 2` entra en la v2; top_k y pool quedan declarados como están |
| 3 | **Unidad = mensaje, conteos enteros chicos** | 1 por par por unidad | declarado; el tamaño del corpus es casual | Queda. Se acota por afuera: la Serie 2 no construye W con menos de 30 mensajes |
| 4 | **Signo por texto entero** | lista de 44 marcadores | la lista y "texto entero" son decisiones declaradas; **subcadena y falta de NFC eran casuales** | **Corregido en la v2** |
| 5 | **Stopwords (703)** | NLTK es+en + sklearn + 112 propias | declarado; la mezcla es una elección | Queda |
| 6 | **Baseline N_eff₀ por ciclo** | D_ckm = 1 − ln N_eff / ln N_eff₀, se resetea con cada W | **por construcción**, coherente con "W es el instante" | Queda. Consecuencia que hay que leer: **D_ckm no se compara entre ciclos** |
| 7 | **β_c = 1/(ρ*·N·μ_W)** | μ_W = media de W ya normalizada | **casual por acople**: μ_W depende de cuál par sea el máximo; con signo mixto μ_W ≤ 0 ⇒ β_c = ∞ | Queda y **se muestra**: el panel declara μ_W y el ∞ en vez de ocultarlo |
| 8 | **W normalizada por max\|·\|** | W ∈ [−1,1] | **por construcción para N_eff**: la relajación usa el signo de h, que no cambia al escalar | Queda |
| 9 | **Rebuild** | gradiente de D_ckm (3 pasos) > volumen > tiempo | umbrales **sin calibrar**, declarado | Queda; en la Serie 2 el volumen es cada 10 mensajes |
| 10 | **Desempate h = 0 conserva** | la regla de la relajación | **por construcción** (teorema) | Queda |
| 11 | **n_runs = 1000, seed** | converge: 7–9 % entre 10 seeds (CP-E) | por construcción | Queda |
| 12 | **NFC, minúsculas, regex** (op. 1–2) | el perfil declarado `PERFIL_ES_EN` | por construcción, **salvo idiomas sin espacios** | Queda, con su alcance escrito |
| 13 | **TF-IDF sólo para elegir; W usa presencia** | op. 5 elige, op. 6 mide | **por construcción** (teorema de presencia, CP-T) | Queda |
| 14 | **Umbrales sin calibrar** | `calibrado=False` viaja en el registro | declarado | En la Serie 2, `calibrate` corre en cada rebuild y su resultado **se ve**; si no calibra, se ve que no calibró |

**La regla de esta sección:** un criterio casual que queda, queda **dicho**. La diferencia entre la v1 y la v2 no es que haya menos casualidad: es que las dos que se podían sacar sin decidir nada nuevo —la subcadena y el NFC del operador 7— se sacaron, y las que quedan están nombradas con su impacto.

## La parte débil: el paso 7 (review v28, M4)
El review: *"The sign of W rests on a procedure the paper itself shows has no null outcome."* La búsqueda de marcadores **siempre encuentra algo en textos suficientemente largos**, y y hasta la v1 **por subcadena** ("but" dentro de "distri**but**ion"; corregido en la v2, que exige palabra completa). Sobre ese signo descansan W_mixta, P5, P7 y el programa de §8.5. Propuesta del review: un **control de densidad de marcadores** — barajar los marcadores entre textos (rompe la correspondencia texto–oposición) y mostrar que el efecto de W_mixta desaparece; o correr lo mismo sobre un corpus no adversarial y mostrar que la estructura negativa cambia cualitativamente. Sin eso, "verificado" para P5 es *verificado bajo el procedimiento de marcadores*.

## Referencias (a verificar)
- Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly.
- Nothman, J., Qin, H., & Yurchak, R. (2018). Stop Word Lists in Free Open-source Software Packages. *NLP-OSS*. https://aclanthology.org/W18-2502/
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12.
- Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management* 24(5).
- Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM* 18(11).
- Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation* 28(1).
- Unicode Standard Annex #15, Unicode Normalization Forms.
