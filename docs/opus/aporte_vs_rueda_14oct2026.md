# Qué aporta CKM hoy / qué no reinventamos — 14 oct 2026
*Opus 5.5 (Cowork), a pedido de delamor: "1. qué aporta hoy ckm. 2. separar conscientemente, sabiendo que tal línea no existe, lo que aporta de lo que NO REINVENTEMOS LA RUEDA. En este último grupo está corpus y node extractor." Primero se escribió sin buscar; después delamor: "busca todo lo que necesites, ahora sí sos libre".*

**Qué se leyó (alcance):** paper v27 (abstract, §1, §7.1, §8.1); `REVIEW_REPORT_PAPER_..._v28.md` (12 oct) completo; v28 borrador sólo con grep (GOLES, enumeración exacta, TRUST); docstrings de `services/*.py`; lista de archivos del repo que mencionan "token" o usan TF-IDF/NLTK. Todo en la PC, sólo lectura, repo en `fb2b87a`. No se leyó el v28 entero.

## 1. Lo que aporta CKM hoy
| | qué | estado según el paper/review |
|---|---|---|
| **A1** | **N_eff = 1/Σm² sobre masas de cuenca** como estimador **convergente** de diversidad del paisaje; que contar atractores (D_ckm) no converja es el diagnóstico que llevó ahí. Validado contra **enumeración exacta** de 2²⁰ estados en tres corpus N = 20: conteo de órbitas erra hasta 28 % (91 % con poco presupuesto), N_eff ≤ 0,6 % (v28 §4.3.1). | verificado; el review lo llama "el núcleo publicable… nuevo en su aplicación" |
| **A2** | **Instrumento de paisaje sobre "lo que sea":** mide la geometría de la co-ocurrencia de comparaciones, sin saber qué son los nodos. delamor: *"ckm mide la geometría de lo que sea… ese es el aporte, uno de ellos"*; *"cKM no extrae nodos"*; *"ckm no tokeniza"*. | es la última frase del abstract v27; el review: "let it lead" |
| **A3** | **P7, nodo Type-965** (sostenedor: in-degree alto, out-degree ~0 en Δ) — afirmación estructural falsable. | confirmado en dos corpus; **sin nulo** (review M7, pregunta 2) |
| **A4** | **El método epistémico** (verificado / implementado / propuesto / abierto; traza AUTO; retirar en vez de suavizar). | el review lo llama "contribución a la metodología"; **decide delamor** si va como aporte |
| **A5** | **β_collective** emergente, sin calibración externa. | **implementado, no verificado**; el review pide bajarlo a una cláusula (M3). Dirección, no aporte cerrado |

## 2. No reinventamos la rueda (se usa, se declara, se cita)
- **Corpus y extracción de nodos** (delamor). `services/node_extractor.py` (TF-IDF de sklearn, stopwords NLTK + sklearn), `services/corpus_service.py` (arma W de las presencias). Hay **varios tokenizadores** en el repo, uno por intento: ~22 archivos `.py` mencionan "token" (pipelines de fourforums v8–v8g, `find_965_v3`, `driver_unidad_texto`, `node_extractor_dev`, `sintetico_campo_plantado`, …); 6 usan TF-IDF/CountVectorizer/NLTK. Campo de referencia: RAKE, C-value, listas de stopwords (ver `traza_externa_extraccion_13oct2026.md`).
- **El signo de W** (`_OPPOSITION_MARKERS`, substring sobre el texto). Es entrada, no instrumento; la detección de postura es un campo propio. El review (M4) marca que **no tiene resultado nulo** ("but" dentro de "distribution").
- **La base matemática:** Hopfield / Ising; teorema de Goles (1985); Simpson / Hill (1973); estabilidad de cuencas (Menck 2013), entropía de cuencas (Daza 2016); balance (Harary 1953). **Arquitectura base:** Aiyappa et al. (2024). Todo como referencia (criterio 1 de delamor: humildad).

## 3. Donde la línea no existe (como dijo delamor)
- **P5, P7 y W_mixta dependen de una entrada declarada: el signo** (paso 7, marcadores). Lo que afirman vale *bajo ese procedimiento*. *(Corregido el 14 oct a pedido de delamor: antes decía "se apoyan en la rueda", que no aclara nada — "todo se apoya en ruedas: Einstein, Newton, Galileo… es la base del tejido de la ciencia".)* El review pide un **nulo**: mismos textos, misma cantidad de textos marcados como oposición, pero la marca puesta en textos **al azar**; si el efecto (p. ej. la caída de N_eff en P5) aparece igual, venía de tener negativos, no de dónde está la oposición; si sólo aparece con la marca real, depende de la oposición real.
- **GOLES / desempate h = 0 conserva:** el teorema es rueda; nombrarlo como **premisa del instrumento** (determinismo dado W, σ₀, seed) es condición que da sentido a A1, no aporte en sí.
- **La serie IAP:** prueba del instrumento, no hallazgo del campo. El estado del canal leído (8 de 12 joins) es **anterior al filtro F3b** del 9 oct; hoy SYSTEM no entra al corpus (corrección en `nodo_y_W_desde_abajo_13oct2026.md` §9).

## 4. Fuera del paper (después, o TRUST)
- **Regla CKM TRUST** (campo → traza → sube → contexto): no aparece en el v28 (grep). Va con TRUST.
- **Gatekeeper:** dominio MCP, nunca ejercido en el trabajo reportado → apéndice de procedencia (review M8).
- BehaviorGraph G, COCO como operador: prueba de concepto / abierto.

## 5. Para delamor
1. ¿A4 (el método) va como aporte o como condición?
2. ¿A3 (P7) y P5 entran como aporte con su condición declarada, o esperan el nulo?
3. El review (12 oct) es de un sistema de IA sin acceso al repo; lo verificado por Opus el 12 oct está en `verificacion_review_kimi_12oct2026.md`. Lo citado acá del review es lo que el review dice, no verificado de nuevo.
