DELAMOR A CODE (texto de Opus):

Soy delamor. Dos TASKs nuevas, con el marco del 14 oct: CKM no extrae nodos ni tokeniza; la extracción, la tokenización y el signo se declaran y viajan en la traza; sin regresiones ni compatibilidad hacia atrás (la única versión es la actual).

Qué hacer:
1. Crear `docs/tasks/TASK_declaracion_extraccion_v1.md` y `docs/tasks/TASK_condiciones_del_paper_v1.md` con el contenido de abajo, tal cual. Un commit, los dos archivos nombrados (sin `git add -A`). Push.
2. Anotar en `docs/tasks/DECISIONES_opus.md`, en commit propio: "14 oct, delamor: CKM no extrae nodos ni tokeniza; se declara. Sin regresiones ni compatibilidad hacia atrás. `TASK_tests_instrumento_v1` queda como traza, reemplazada por `TASK_condiciones_del_paper_v1`."
3. Empezar por el **CP0 de `TASK_declaracion_extraccion_v1`** (sin código). Al terminarlo: REPORTE en la BANDEJA y A1.PAUSA.
4. **No** cerrar ni pausar otras TASKs todavía (node_extractor_regla, ckm_trust_rule, calibrate, fabrication_service, canal IAP CP3): eso lo decido yo aparte.

Si en algún punto el código no coincide con lo que dicen estas TASKs: A1.PAUSA, reportar, esperar.

==================== docs/tasks/TASK_declaracion_extraccion_v1.md ====================

# TASK_declaracion_extraccion_v1

*14 oct 2026. Opus 5.5 (Cowork), por pedido de delamor: "armamos las Tasks para Code… con el encuadre sobre CKM, declarando la extracción y la tokenización en traza; así, con un extractor personal o bien externo, se generaría y se utilizaría lo declarado." Para Code, en el Codespace. Leído contra `fb2b87a`.*

## Por qué
- **CKM no extrae nodos ni tokeniza** (delamor, 14 oct). Mide la geometría de lo que le entra e interpreta dinámica, no significado.
- La extracción, la tokenización y el signo **se declaran**, con su referencia. *"Lo que no es debate es que el código implemente lo que el paper declara."*
- Al declararla, la dependencia queda **adentro** de la afirmación ("con W producida así, pasa esto"), no escondida debajo.
- Cualquier productor de W (el `NodeExtractor` de hoy, uno personal, uno externo) entrega **W + nodos + su declaración**. CKM usa lo declarado. **No es una API para enchufar librerías** (delamor): es un registro que viaja en la traza.
- Referencia del contenido: `claude/declaracion_extraccion_W_14oct2026.md` (los 8 operadores).

## Lo que hay hoy (leído por Opus en `fb2b87a`; el CP0 lo verifica)
- `services/w_version.py:72` — cada marca de W guarda `timestamp`, `sha256`, `corpus_size`, `causal_event`. **No guarda cómo se produjo W.**
- `services/corpus_service.py:302, 396, 409` — `perfil_extraccion` (S0b) se guarda y se carga: cubre normalización, minúsculas, patrón y stopwords. No cubre n-gramas, selección, presencia, signo ni normalización de W.
- `services/corpus_service.py:56, 230` — el signo: `_OPPOSITION_MARKERS`, búsqueda de subcadena sobre el texto entero.

## Reglas
1. **Sin regresiones, sin compatibilidad hacia atrás** (delamor, 14 oct: *"la única versión del modelo es la actual; el resto es imaginación"*). No se escriben ramas para estados viejos ni tests que comparen contra copias congeladas.
2. **No se cambia lo que el extractor hace.** Si el código y la declaración difieren, se corrige **la declaración**, y se reporta. Cambiar el comportamiento es decisión de delamor.
3. **No se toca el gate** (`f96c234`). Nada vivo cambia sin orden de delamor.
4. Predicción commiteada antes de cada cambio. Archivos nombrados uno por uno al commitear (sin `git add -A`). Un REPORTE por CP en la BANDEJA.
5. Donde se duda: **A1.PAUSA** (detenerse en pregunta, abierto), reportar, esperar.

## Checkpoints

### CP0 — Sin código. Qué se declara hoy y qué falta
Tabla: para cada uno de los 8 operadores de la declaración (normalización, tokenización, filtrado, n-gramas, selección, presencia, signo, W), **dónde vive en el código** (archivo:línea), **si hoy queda registrado en la traza** (estado, `w_version`, `perfil_extraccion`) y **qué falta**. Incluir dónde entran hoy W producidas por otros caminos (p. ej. los pipelines de `experiments/`), sólo para nombrarlas. A1.PAUSA. Reportar.

### CP1 — La declaración como dato
- Un registro `declaracion_extraccion` (JSON) con los 8 operadores, cada uno con: qué hace, parámetros, referencia. Además: **productor** (nombre y versión o sha del código que produjo W). Las listas largas (stopwords, marcadores) van como **hash + origen**, no enteras.
- El `NodeExtractor` + `CorpusService` de hoy generan su propia declaración. `perfil_extraccion` pasa a ser una parte de ella (no se duplica).
- **Viaja en la traza:** en el estado guardado y en cada marca de `w_version`, atada al `sha256` de W.
- Una W **sin declaración** se marca como tal, explícita. Nunca se completa con la declaración de hoy por defecto (I2).
- Test: la declaración que produce el extractor de hoy coincide con `declaracion_extraccion_W_14oct2026.md`.

A1.PAUSA. Reportar.

### CP2 — La declaración ejecutable
Un test por operador, sobre textos chicos fijados en el test, que muestra que **el código hace lo que la declaración dice**. Ejemplos ya vistos el 13–14 oct que tienen que aparecer:
- `peter_pan` es un token (`_` cuenta como letra); `co-alinear` → `alinear`; palabras de 2 letras no existen; `https://www.x.com/y` → `https`, `www`, `com`, …
- `control of guns` → bigrama `control guns` (contigüidad después del filtrado).
- `año` NFC y NFD → el mismo token.
- Cada par cuenta 1 por unidad; signo −1 si el texto contiene un marcador (incluido `but` dentro de `distribution`, **como condición declarada**, no como bug).

Si algún test muestra que el código hace otra cosa que la declaración: se corrige la declaración, se reporta, **no se toca el código**. A1.PAUSA. Reportar.

### CP3 — Sin código. Una W de otro productor
Con lo de CP1 y CP2 a la vista: qué haría falta para que una W producida por otro extractor (personal o externo) entre a CKM **con su declaración**, sin que CKM la produzca. Sólo propuesta, en el REPORTE. **Decide delamor** antes de cualquier código.

## Fuera de esta TASK
Cambiar la extracción (S2–S5, contigüidad antes del filtrado, stopwords): eso es estudio de tokenización, para después ("OPUSDELAMOR"). La regla CKM TRUST (→ TRUST). COCO y calibración.

==================== docs/tasks/TASK_condiciones_del_paper_v1.md ====================

# TASK_condiciones_del_paper_v1

*14 oct 2026. Opus 5.5 (Cowork), con el marco de delamor del 14 oct. Para Code, en el Codespace. Reemplaza a `TASK_tests_instrumento_v1` (que queda como traza; su CP6 está hecho). Leído contra `fb2b87a`.*

## Por qué
El paper v29 tiene que decir, como **condición declarada**, en qué rango vale lo que afirma. Cada CP de esta TASK produce **un número o una propiedad que va al paper**. Ninguno arregla nada.

delamor (14 oct): *"una vez que esté estable, digamos: definimos sin complicarla, bueno, está estable dentro de este rango, con estas dependencias observadas, y ahí te despachás con suites con drivers matemáticos."*

## Reglas
1. **Sin regresiones, sin compatibilidad hacia atrás.** La única versión es la actual.
2. **No se arregla nada.** Lo que el código hace se mide y se reporta.
3. **No se toca el gate** (`f96c234`). Nada vivo cambia.
4. Predicción con número commiteada **antes** de correr. Archivos nombrados uno por uno. Un REPORTE por CP en la BANDEJA.
5. Corpus: **sólo los del repo**. Los de `ckmdatasets` (fourforums, CreateDebate) **sólo con orden de delamor** (CP-N).
6. Donde se duda: **A1.PAUSA**, reportar, esperar.

## Checkpoints

### CP-T — Teorema de presencia · `tests/test_teorema_presencia.py`
*(era tests_instrumento CP3)*
Con textos sin marcadores (o `force_w_pos=True`), sobre los corpus del repo: ningún Wᵢⱼ < 0; 0 triángulos con producto de signos < 0; T(W) = 0. Es una **propiedad del modelo** (va a §4/§5.2, con P1/P4), no de un corpus. Si falla, el instrumento hace otra cosa que la matemática: A1.PAUSA y reportar.

### CP-E — Rango de estabilidad · driver en `experiments/` + REPORTE
*(era tests_instrumento CP4; usa lo medido en CP6)*
Lo que ya se sabe (CP6, campo plantado, 12 oct): ‖ΔW‖ decae como 1/n con el campo quieto (de 0,34 a 0,02 en 30 pasos); N_eff fue función de la partición, no de los pesos, desde el paso 5.
Medir, sobre los corpus del repo, **cuánto se mueve N_eff** al variar, de a una por vez: `top_k`, tamaño del pool, lista de stopwords (la actual vs. sólo NLTK vs. sólo sklearn), un texto más con vocabulario ya visto. Con varias seeds de muestreo, reportando dispersión.
Salida: una tabla **"N_eff estable dentro de este rango, con estas dependencias"**, lista para el paper. **No se fija umbral.**

### CP-M — Nulo de marcadores · driver en `experiments/` + REPORTE — **opcional**
*(era tests_instrumento CP1; review v28 M4)*
Mismos textos, misma cantidad de textos marcados como oposición, pero la marca puesta en textos **al azar** (varias permutaciones). Comparar la caída de N_eff (W_pos → W_mixta) con la marca real y con las barajadas.
Opcional porque el paper afirma lo que pasa **bajo** el procedimiento de marcadores (declarado). El nulo sirve a quien quiera interpretar el signo como "oposición" — interpretación que es del lector.

### CP-N — Nulos de P5 y P7 — **sólo con orden de delamor**
*(review v28 M7)*
P5: réplicas por seed con su dispersión. P7: nulo que preserva grados en Δ. Usa fourforums/CreateDebate (`ckmdatasets`): **no se arranca sin orden de delamor.**

## Orden
CP-T → CP-E → (CP-M si delamor lo quiere) → (CP-N con orden).

## Sale de `TASK_tests_instrumento_v1`
- **CP2** (SYSTEM fuera del corpus): ya está en el código desde F3b (`ckm_monitor.py:284-312`). "SYSTEM es campo" quedó abierto por delamor, sin apuro.
- **CP5** (declaración de la W): pasa a `TASK_declaracion_extraccion_v1`.
- **CP7** (disparo de COCO): en pausa con la calibración; COCO no es núcleo del paper.

==================== fin ====================
