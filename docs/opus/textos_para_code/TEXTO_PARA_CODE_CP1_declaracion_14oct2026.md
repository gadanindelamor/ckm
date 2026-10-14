DELAMOR A CODE (texto de Opus):

Soy delamor. Leí el CP0 de `TASK_declaracion_extraccion_v1` (`6d39165`). Decido:
1. **Divergencia (a) — se corrige.** Una extracción fallida no puede borrar el perfil ni el `registro_borde` de la W que sigue viva.
2. **Divergencia (b) — se declara.** `_has_opposition` no normaliza a NFC; hoy sin efecto (44 marcadores ASCII). No se toca el código.
3. **Sí al CP1.**

**Antes de empezar:** `git pull`. Desde el 14 oct la traza de Opus vive en el repo, en `docs/opus/` (la escribe Opus desde la PC; Code no la edita).

Orden de trabajo. Cada paso con su REPORTE en la BANDEJA. Archivos nombrados uno por uno al commitear (sin `git add -A`). Sin regresiones ni compatibilidad hacia atrás: la única versión es la actual. No se toca el gate (`f96c234`).

**Paso 0 — Decisiones.** En `docs/tasks/DECISIONES_opus.md`, commit propio: "14 oct, delamor, sobre el CP0 de declaracion_extraccion: (a) se corrige; (b) se declara; CP1 sí."

**Paso 1 — La declaración entra al repo.** El CP0 citó `docs/tasks/declaracion_extraccion_W_14oct2026.md`, pero ese archivo no existía en el repo: vivía en el proyecto. Fue falta del texto de Opus, no tuya. Crear `docs/defs/DECLARACION_extraccion_W_v1.md` con el contenido de abajo, tal cual (ya incluye lo que encontraste en el CP0: el mecanismo real de χ en el paso 6, la condición (b) en el paso 7, los defaults de sklearn en el paso 5). Commit propio. Corregir en la TASK la ruta de referencia para que apunte a ese archivo (hoy, por `c0bcdc5`, apunta a `docs/tasks/declaracion_extraccion_W_14oct2026.md`, que no está en el repo).
**Una sola versión viva:** `docs/defs/DECLARACION_extraccion_W_v1.md` es la canónica; ahí se corrige si el CP1 encuentra diferencias. La copia que Opus subió en `docs/opus/declaracion_extraccion_W_14oct2026.md` es traza del día: no se edita. Si en el Codespace quedó una copia **sin trackear** en `docs/tasks/declaracion_extraccion_W_14oct2026.md`, borrarla (es una versión anterior) y decirlo en el REPORTE.

**Paso 2 — Corregir (a).** Primero la predicción, commiteada: qué test nuevo falla hoy y por qué. Después el test (`tests/test_extraccion_fallida_no_borra.py`): con una W viva y su perfil, un rebuild cuya extracción falla deja **intactos** la W, `nodes`, `_perfil_extraccion` y `_registro_borde`. Después el cambio mínimo en `CorpusService._rebuild` (no tocar el resto). Suite completa. REPORTE y **A1.PAUSA**.

**Paso 3 — CP1, la declaración como dato** (lo dice la TASK, con lo que encontraste en el CP0). Primero la predicción, commiteada. Después:
- Un registro `declaracion_extraccion` (JSON) con los 8 operadores del `DECLARACION_extraccion_W_v1.md`, cada uno con qué hace, sus parámetros y su referencia, más el **productor** (nombre, sha del código).
- Tiene que incluir lo que hoy es invisible: **`ngram_max` y `top_k`**; **hash + origen** de la lista de stopwords y de la de marcadores (más el conteo); los **defaults de TF-IDF** y las **versiones de sklearn y de Python**; la **fórmula de W** (suma por unidad, normalización por máx|·|, diagonal 0).
- `perfil_extraccion` pasa a ser una parte de la declaración, sin duplicarse.
- **Se ata al `sha256` de W:** cada marca de `w_version` guarda su declaración (o una referencia a ella). Ya no queda una sola por estado.
- Una W sin declaración se marca explícitamente como tal. Nunca se completa con la de hoy por defecto (I2). No se escriben ramas para estados viejos.
- Test: la declaración que produce el extractor de hoy coincide con `docs/defs/DECLARACION_extraccion_W_v1.md`. Si no coincide, se corrige el documento, se reporta, y **no se cambia el comportamiento del extractor**.
- Suite completa. REPORTE y **A1.PAUSA**.

Si algo no coincide con lo que dice este texto: A1.PAUSA, reportar, esperar.

==================== docs/defs/DECLARACION_extraccion_W_v1.md ====================

# Declaración de la extracción y de W — 14 oct 2026
*Opus 5.5 (Cowork), con delamor. Revisada el 14 oct con el CP0 de Code (`6d39165`). Para la §4.1 del paper o un apéndice. Pasos verificados contra el código en `fb2b87a` (`services/node_extractor.py`, `services/corpus_service.py`), sólo lectura. Referencias citadas de memoria: **a verificar** antes de entrar al paper.*

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
5. **Selección:** de los top_k·3 términos más frecuentes del corpus (`max_features`), los top_k de mayor TF-IDF medio (sklearn `TfidfVectorizer` con sus valores por defecto: `smooth_idf=True`, `norm="l2"`; la versión de sklearn se declara); empate en el corte: conserva la pertenencia anterior (h = 0 conserva). Con empates, la cantidad de nodos puede no ser top_k. *[Spärck Jones 1972; Salton & Buckley 1988]*
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

==================== fin ====================
