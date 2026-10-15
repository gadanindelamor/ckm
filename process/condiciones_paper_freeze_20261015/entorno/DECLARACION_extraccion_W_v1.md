# Declaración de la extracción y de W — 14 oct 2026
*Opus 5.5 (Cowork), con delamor. Revisada el 14 oct con el CP0 de Code (`6d39165`) y con el CP2 (paso 5, caso límite). Para la §4.1 del paper o un apéndice. Pasos verificados contra el código en `fb2b87a` (`services/node_extractor.py`, `services/corpus_service.py`), sólo lectura. Referencias citadas de memoria: **a verificar** antes de entrar al paper.*

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
5. **Selección:** de los top_k·3 términos más frecuentes del corpus (`max_features`), los top_k de mayor TF-IDF medio (sklearn `TfidfVectorizer` con sus valores por defecto: `smooth_idf=True`, `norm="l2"`; la versión de sklearn se declara); empate en el corte: conserva la pertenencia anterior (h = 0 conserva). Con empates, la cantidad de nodos puede no ser top_k. **Caso límite (CP2, 14 oct):** si ningún término queda estrictamente por encima del corte, el grupo empatado no cabe en top_k y no hay selección anterior (bootstrap), **no entra ninguno: N = 0 y no se construye W** — pasa con corpus chicos sin vocabulario compartido, donde cada término aparece en un solo texto y todos tienen el mismo TF-IDF medio. *[Spärck Jones 1972; Salton & Buckley 1988]*
6. **Presencia:** χᵢ(u) = 1 si nᵢ ∈ G(u), 0 si no. **Mecanismo al construir W:** χ es el no-nulo de la fila de la matriz TF-IDF restringido a los nodos (equivalente, porque con `smooth_idf` el idf es ≥ 1 y ningún término presente da 0). **Al evaluar:** pertenencia de la cadena del nodo al conjunto de términos del texto. σᵢ(u) = 2χᵢ(u) − 1. *(Corregido el 14 oct según el CP0 de Code.)*
7. **Signo de la unidad:** s(u) = −1 si u, pasado a minúsculas, contiene algún marcador de oposición (búsqueda de subcadena, 44 marcadores), +1 si no. **Condición declarada (delamor, 14 oct):** el texto **no** se normaliza a NFC antes de buscar marcadores (a diferencia del paso 1); hoy sin efecto porque los 44 marcadores son ASCII. `force_w_pos` anula el signo.
8. **W:** Wᵢⱼ = Σᵤ s(u)·χᵢ(u)·χⱼ(u) / máx|·|, Wᵢᵢ = 0; cada par cuenta 1 por unidad. *[modelo de espacio vectorial / bolsa de palabras: Salton, Wong & Yang 1975]*

En palabras: **W cuenta en cuántas unidades dos comparaciones respondieron `True` a la vez, con el signo de la unidad, normalizada.**

## Dirección 1 — lo que entra desde el canal (probado con el patrón del paso 2)
- Puntuación, guiones, asteriscos, emojis: **no pueden llegar a W** (el patrón no los produce).
- **URLs, mails y rutas entran como palabras:** `https://www.anthropic.com/news/…` → `https`, `www`, `anthropic`, `com`, `news`; `x@ejemplo.com` → `ejemplo`, `com`; `C:\Users\…` → `users`, ….
- La barra `/` corta como un espacio; `sí/no`, `la/el` desaparecen (2 letras).
- La ñ pasa: `año` y `ano` son nodos distintos.
- Eventos `SYSTEM` del canal ("X joined the channel", leaves) **no entran al corpus** desde el filtro F3b (9 oct, `iap_chatroom/ckm_monitor.py:284-312`); siguen en la observación del device. "SYSTEM es campo" queda abierto (delamor). Ver `docs/opus/nodo_y_W_desde_abajo_13oct2026.md` §9 (corregida).
Cada uno se declara; o se decide filtrarlo antes, y eso también se declara.

## La parte débil: el paso 7 (review v28, M4)
El review: *"The sign of W rests on a procedure the paper itself shows has no null outcome."* La búsqueda de marcadores **siempre encuentra algo en textos suficientemente largos**, y por subcadena ("but" dentro de "distri**but**ion"). Sobre ese signo descansan W_mixta, P5, P7 y el programa de §8.5. Propuesta del review: un **control de densidad de marcadores** — barajar los marcadores entre textos (rompe la correspondencia texto–oposición) y mostrar que el efecto de W_mixta desaparece; o correr lo mismo sobre un corpus no adversarial y mostrar que la estructura negativa cambia cualitativamente. Sin eso, "verificado" para P5 es *verificado bajo el procedimiento de marcadores*.

## Referencias (a verificar)
- Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly.
- Nothman, J., Qin, H., & Yurchak, R. (2018). Stop Word Lists in Free Open-source Software Packages. *NLP-OSS*. https://aclanthology.org/W18-2502/
- Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *JMLR* 12.
- Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management* 24(5).
- Salton, G., Wong, A., & Yang, C. S. (1975). A vector space model for automatic indexing. *Communications of the ACM* 18(11).
- Spärck Jones, K. (1972). A statistical interpretation of term specificity and its application in retrieval. *Journal of Documentation* 28(1).
- Unicode Standard Annex #15, Unicode Normalization Forms.
