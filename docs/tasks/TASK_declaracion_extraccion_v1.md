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
