# El review frío del v34, comparado con lo que ya estaba "a punto" (v28 y v32) — 30 oct 2026 (Opus 5.5)

*delamor (30 oct): "hay una versión… que ya tuvo un review… que dice que le faltaba corregir cosas y era publicable… ¿cómo puede ser que otro review ahora haga toda la lista esa? Partamos de lo que ya estaba a punto."*

## 1. Lo que dijeron los reviews anteriores (citados textualmente)
- **v28** (`docs/opus/REVIEW_REPORT_PAPER_Landscape_Driven_Device_v28.md`, 12 oct): *"Verdict: Major revision. The core result is real and publishable."*, y *"Publishable as a preprint after M1–M4, M6, and the minor items"*. Se revisó **con contexto**: AWARENESS, CKM_Modelo_Hibrido, DEFS v15, LETTER, METODOLOGY_v3, OTHERWAY, THEORY y el paper v6.
- **v32** (`docs/opus/REVIEW_REPORT_PAPER_v32.md`): *"Recommendation: minor revision, conditional on M1; address M2–M4 before freeze… If the verification items close, this version is releasable as a preprint"*. Se revisó **con** el v28 y el v29, los reviews anteriores, los documentos de sesión y los bloques de cambios.
- **v34, review frío** (`docs/opus/REVIEW_PAPER_Landscape_Driven_Device_v34_print_30oct2026.md`): 62 ítems. Sólo vio el documento, con una lista de qué buscar (Babel, afirmaciones sin sostén, ausencias, interpretación, contradicciones) y *"answer as a list"*. Empieza diciendo: *"The paper's strongest result holds up: the convergence claim and the margin arithmetic check out when recomputed."*

## 2. Lo medido: ¿cuántos de los 62 ítems señalan texto que ya estaba en el v28 o en el v32?
Para cada ítem, las citas entre comillas se buscaron (los primeros 60 caracteres, sin distinguir mayúsculas) en el cuerpo del v28, del v32 y del v34. Script: lectura, en la PC, sin cambiar nada.

| dónde está el pasaje citado | mayores | moderados | menores | total |
|---|---:|---:|---:|---:|
| ya en el **v28** | 0 | 16 | 9 | **25** |
| en el **v32**, no en el v28 | 2 (1, 38) | 5 | 6 | **13** |
| **sólo en el v34** | 1 (13) | 0 | 2 (14, 31) | **3** |
| la cita no se encontró (paráfrasis) | 0 | 6 | 4 | 10 |
| sin cita textual | 1 (34) | 5 | 5 | 11 |

**Lectura (A2: la cadena, sin interpretar más):**
- De los 45 ítems con cita encontrada, **38 señalan pasajes que ya estaban** en versiones que esos reviews llamaron publicables, o casi. El review frío no encontró otro paper: leyó el mismo con otro instrumento. Recibió sólo el documento y una lista de búsqueda exhaustiva; los anteriores recibieron el contexto que explica los términos, y una pregunta de veredicto. *"Veamos qué miden, en vez de decidir qué miden"*: el review frío mide Babel y ausencias, y eso con contexto no aparece.
- **Lo que de verdad es nuevo:**
  - el **13**, un error de Opus del v34, ya corregido;
  - el **38**, una inconsistencia que creó el v34 al pasar §4.3.2 a los números de hoy y dejar §5.2 con los viejos;
  - el **54** y el **56**, el intento 5 a medio integrar;
  - el **3**, la α que introdujo el v34;
  - el **34**, la comparación con Chao1 y Good–Turing, que ningún review anterior pidió y que vale para todas las versiones.
  Los cinco primeros van en el v35, que corrige los errores propios. El 34 va a la lista de delamor.
- La coincidencia entre los tres reviews: el núcleo, el estimador y su validación, se sostiene.

## 3. Lo que hace el v35 con esto
Parte del v34, que es el v32 más los ítems de verificación cerrados (R1–R4). No reescribe a partir de la lista. Corrige sólo los errores del v34, lo que el v34 dejó inconsistente, lo que afirma algo que el código no hace (*"pero no con fanatismo"*) y lo que ya está decidido en los registros. El detalle, ítem por ítem, está en el bloque de arriba del v35.

## 4. Límites de esta comparación
- Buscar por los primeros 60 caracteres de una cita es aproximado: una cita que cambió levemente cuenta como "no hallada".
- "Ya estaba en el v28" no dice que el review del v28 lo haya visto y lo aceptara: dice que estaba en el texto que ese review leyó.
