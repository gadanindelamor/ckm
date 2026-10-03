# TASK_salamanca_neel_coercividad_v2

*Clase T — Oct 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Antecedentes: DEFS_CKM_estado_actual_v12 §14–§16 y línea 118; REG_mapeo_magnetico_ckm_v1 §3.1–3.3; REG_unidad_texto_saturacion_v1 §3–§5; PROPUESTA_capa_analisis_services_v1 (Parte 5, pasos 1–4).*
*Reemplaza el diseño de TASK_neel_separabilidad_v1, que queda como registro de lo que se descartó y por qué.*
*v2 (delamor): alcance = pasos 0 → 1 → 2 sobre los corpus que ya están. El paso 3 se separa, porque la W de fourforums del paper es relacional y el control positivo necesita otra W.*

---

## 1. Qué entendí

**El nombre es la definición.** *(delamor: Basilio Salamanca, almacenero de Cipolletti, Río Negro. En la puerta, a la derecha, un cartel escrito a mano: "Lo que natura non da, SALAMANCA non presta". Y: "no se fía".)*

- **No presta** — la estructura que no está en el corpus no se le pide prestada a ningún procedimiento.
- **No se fía** — tampoco se le da crédito por adelantado. El ruteo por marcadores fía: asume la tensión y después la cobra en pares negativos.

**No es oposición** *(delamor)*. DEFS línea 118 ya lo dice: *"Coercitividad de frontera ≠ oposición binaria. Es gradiente por par de clusters. Alta coercitividad = la frontera resiste el cruce. **Nada es opuesto** — hay fronteras con distintos valores de resistencia."*

**Oposición supone exactamente dos** *(delamor: no hay oposición entre 33 clusters, ni entre más o menos de dos T)*. Por eso no se busca oposición: es una precondición que el dato cumple o no.

**k lo dice el dato** *(delamor: T0 y T1 tienen que existir primero)*. Un corte espectral por signo del Fiedler devuelve dos siempre. Encontrar dos no es hallazgo: es la forma de la pregunta.

**Se lee por la cola** *(delamor: no soy adepto a los promedios, ni a las distribuciones normales inexistentes; habito las colas)*. En un W denso y saturado el centro no informa: todo correlaciona por construcción. Lo que informa son los pocos pares que no.

## 2. Estado del repo — verificado leyendo, sin ejecutar

**Existe y está en `services/`:**
- `cluster_frontier_density.py` — coercitividad por par de clusters, `min(intra_a, intra_b) / inter`, con los bordes resueltos: `inf` si no hay aristas inter-cluster, `"oposicion"` si `inter < 0`, cluster de un nodo anotado como poroso. **Ya separa el régimen de oposición de la coercitividad**, desde antes de esta conversación.

**Existe, en la capa que no está en uso:**
- `cluster_nodes()` en `process/initial_static_model/analytics.py`. Agrupa nodos por **co-movimiento en el espacio de atractores** (copresencia + Ward + `fcluster`), no por los pesos de W. Toma `n_clusters` fijo, default 4. `analytics.py` hoy no importa (ImportError por import relativo; PROPUESTA Parte 2). scipy 1.17.1 disponible.

**La W de fourforums del paper no es de términos** *(delamor)*. Verificado en `process/experiments/fourforums_pipeline_v8g.py`: `SKIP_TABLES` incluye `'text'`, con el comentario *"contenido posts - enorme, no necesario"*, y W se arma desde `mturk_2010_qr_entry` (anotaciones quote/response) más `mturk_author_stance`. **Los nodos son autores**, no términos — por eso el nodo Type-965 del paper §5.2 es el *Author* 965. Y el dump `fourforums_no_parse_2016_05_18.sql` **no está en el filesystem**.

**No existe en ningún archivo del repo:**
- SALAMANCA como criterio: la partición más el ensemble nulo que decide si la frontera existe.
- Néel: el barrido de β.
- Lo medido el 20 de septiembre y el 3 de octubre sobre estos dos criterios corrió en scripts sueltos **que no se guardaron**. Está sólo en los REG y en la conversación.

**Lo que hay en `experiments/driver_neel_salamanca.py`** es el diseño **descartado**: k = 2 forzado, partición por signo del Fiedler, separabilidad leída por la media. Se reescribe, no se extiende.

## 3. Lo que ya se midió y no hay que volver a medir

| | |
|---|---|
| Máximo sobre particiones | Con spins **independientes**, S de la mejor partición da 0.030 (200 muestras), 0.014 (1000), 0.005 (5000). Nunca cero: es un máximo, positivo aunque no haya nada. |
| λ₁ del laplaciano normalizado contra 20 barajados | caso09 0.425 / nulo 0.741 · caso13 0.759 / 0.870 · caso14 0.850 / 0.970 · informes pág300 0.898 / 0.980 · informes versión 0.947 / 0.990. **p = 0.00 en los cinco: todos tienen estructura. Ninguno sostiene k = 2.** |
| Coercitividad por par, k = 3, contra 10 barajados | caso09 máx **4.59** contra nulo p90 1.63, y las 3 fronteras sobre el nulo. caso13 máx 1.11 contra 1.23: **debajo** del nulo. informes versión máx 1.09 contra 1.04: pegado. |
| Cola de Néel en caso09 (k=2, partición vieja) | De los 20 pares menos correlacionados, persisten en 3 semillas: 1, 0 y 0 según β, contra 0.03 por azar. **La cola era ruido.** |
| Artefacto a evitar | Con k = 5 y k = 6 la coercitividad llega a 16–18 por clusters chicos donde `inter → 0`, y el nulo también. **La lectura vale donde el nulo es estable.** |

## 4. Lo que hace Code

**Orden: 0 → 1 → 2 → 3.** Cada paso es un checkpoint.

### Paso 0 — traer la partición
Seguir los pasos 1–2 de PROPUESTA_capa_analisis_services_v1: `analytics.py` → `services/` con imports planos, y `core.py` si `analytics` lo necesita. Criterio del proyecto: **impacto cero por default, replicación exacta** de lo que ya corría.

No reescribir `cluster_nodes`. Se usa como está, con una sola cosa agregada afuera: cómo se elige `n_clusters` (paso 1).

**Precondición del paso 1, desprendida en CP1:** la representación de atractores que entra a `cluster_nodes` no coincide con la que devuelve `relax_orbit`. Va en **TASK_representacion_atractores_adaptador_v1**, que tiene que cerrar antes.

### Paso 1 — SALAMANCA: ¿existe la frontera?
1. W_pos del corpus (`force_w_pos=True`, `rebuild_suspendido=True`, estado aislado).
2. Atractores → `cluster_nodes(attractors, nodes, n_clusters=k)` para un **rango** de k (2…8). No se fija k de antemano.
3. Para cada k, `cluster_frontier_density` → coercitividad de **cada par** de clusters.
4. **Ensemble nulo prestado**: el mismo corpus barajado palabra por palabra (conserva frecuencias y largos de texto, destruye la co-ocurrencia), W reconstruida con los servicios reales, mismo pipeline. N barajados.
5. Una frontera **existe** si su coercitividad cae fuera de la distribución nula de su mismo k. Si ninguna, en ningún k: **no pasa nada**, y W_pos es la respuesta.

**Salida: la matriz completa de coercitividad por par y por k, con su nulo.** Continua. La categoría se deriva al leer, como el `registro_borde`.

### Paso 2 — Néel: ¿qué profundidad tiene?
Solo sobre las fronteras que el paso 1 dejó en pie, y con la partición **fija** (reajustarla por β es reajustarla al ruido, §3).

Para cada β de frío a caliente: muestrear estados con `boltzmann_warmup`, `C_ij = ⟨σ_i σ_j⟩`, y registrar **C_ij por par cruzante** *(delamor: qué sucede entre ellos)*. No la media.

- β_Néel **por par**: los pares no sueltan todos juntos. La frontera es un perfil, no una línea.
- Lectura por **cola con persistencia**: los K pares que más resisten, y cuántos siguen ahí con otras semillas. Cola que se rebaraja = ruido.

### Paso 3 — correr sobre los corpus que ya están
`caso09`, `caso13`, `caso14`, `informes_version`, `informes_pagina300` y el tramo **`categorias`** del replay (N=27, W_pos, sha256 `c11409bc8a8afc3a…`, 7 textos).

**El control positivo queda fuera de esta TASK** y se propone en §11: necesita una W de términos construida desde el texto de los posts del topic 9, que no existe.

## 5. Pre-registro — declarado antes de correr

| corpus | posiciones | paso 1 debe dar |
|---|---|---|
| caso09 IAP | coordinación | ya dio 4.59 sobre nulo 1.63 con k=3 — hay que ver si sobrevive con la partición por co-movimiento |
| caso13, caso14 IAP | coordinación | nada, o debajo del nulo |
| informes CKM | **autor único** | nada |
| tramo `categorias` | dos interlocutores, **sin posiciones opuestas** | nada |

**Sin control positivo, un resultado de "nada en todos" no distingue entre *no hay fronteras en estos corpus* y *el criterio no detecta fronteras*.** Esa es la razón de §11, y queda declarada como límite de esta TASK.

**Precondición de REG_unidad_texto §3:** un W saturado no tiene ceros, y sin ceros no hay frontera que separar. caso09 está al 62% de pares distintos; informes versión al 100%. Si los saturados dan nada, hay que distinguir *no hay estructura* de *no hay resolución*. Se declara, no se resuelve acá.

## 6. Decisiones

**Tomadas:**
1. k sale del dato, barriendo un rango. No se fija.
2. Coercitividad por par de clusters, cualquier k. No oposición binaria.
3. Néel se lee por par y por cola con persistencia, no por la media.
4. SALAMANCA necesita nulo prestado y eso queda declarado: es un nivel, y un nivel necesita contra qué compararse.
5. `cluster_nodes` se usa como está.

**Abiertas, son del modelo:**
6. **Cómo se elige `n_clusters`.** Barrer 2…8 y leer la matriz es lo que propongo, pero si hay que elegir uno solo, falta el criterio.
7. **El nulo**: barajar el corpus (más fiel, probado) o barajar los pesos de W conservando el grado (más barato). Esta TASK usa el primero; el segundo queda abierto.
8. **Qué hacer con los pares que el paso 2 identifique.** Esta TASK los **lista**. No los incorpora a W. Construir W_mixta desde ahí es otra decisión.
9. **Babel a resolver antes de que entren juntas a un criterio** (PROPUESTA paso 4): hay **dos coercividades** — la de P1 (el ρ donde c(S) cruza cero, campo coercitivo, DEFS §14) y la de frontera de cluster. Comparten nombre y no son lo mismo.

## 7. Corrección a los DEFS, a aplicar si el paso 1 lo confirma

**§16 dice** *"detecta si W_pos tiene estructura adversarial"*. Lo que detecta es **modularidad**. Una palabra, dos objetos. Es la razón de que el criterio admita de más: SALAMANCA sola habría admitido W_mixta en un canal de coordinación. La admisión requiere los dos pasos.

*(delamor: modularidad no es adversarialidad.)*

## 8. Lo que Code NO hace

- No construye W_mixta ni cambia el ruteo por marcadores.
- No reescribe `cluster_nodes` ni `cluster_frontier_density`.
- No conecta nada al canal vivo.
- No interpreta: mide y registra.
- Toda acción fuera de esta TASK es un checkpoint: se detiene, reporta y espera.

## 9. Checkpoints

**Por qué:** la precisión sobre la propia mecanicidad no se intenta desde adentro. Se construye como par.

**Formato:** qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo hasta ahora.

| CP | Después de | Reporta |
|---|---|---|
| **CP0** | leer | Tensiones con el repo. *(Hecho: §2 y §3 de esta TASK.)* |
| **CP1** | paso 0 | *(Hecho. `analytics.py` → `services/`, diff de 2 hunks del import, suite 172. `core.py` no se movió. Registro completo en el anexo de TASK_representacion_atractores_adaptador_v1.)* |
| **CP2** | paso 1 sobre **un** corpus | Matriz de coercitividad por par y por k, con el nulo. Dónde el nulo deja de ser estable |
| **CP3** | paso 1 sobre todos | La tabla contra el pre-registro, salga como salga |
| **CP4** | paso 2 sobre la primera frontera que quedó en pie | Curva por par, β_Néel por par, persistencia de la cola |
| **CP5** | todo | REG borrador fuera de `registers/` |

## 10. Criterio de cierre

- Tests: que `analytics` importe y replique; el nulo; la coercitividad contra un caso a mano; el barrido de k.
- REG borrador entregado.
- Según CONVENTIONS: ¿qué test debería haber cambiado con esto? Declarar los huecos.
- Si el paso 1 da vacío en todos los corpus menos fourforums, **eso es el resultado**, y el REG lo dice así.


---

## 11. Propuesta — W de términos para fourforums (requiere OK, no ejecutada)

*(delamor: el control positivo necesita una W de términos desde el texto de los posts del topic 9, con extracción por streaming. Proponé cómo, con estimación de RAM, y esperá el OK.)*

### Condición material medida

| | |
|---|---|
| RAM total / disponible | **7 GB / 3 GB** |
| disco libre en `/workspaces` | 17 GB |
| dump `fourforums_no_parse_2016_05_18.sql` | **no está en el filesystem** |

El dump es el insumo que falta. IAC v2 se pide por formulario a UCSC; no se baja sin eso.

### Por qué no se puede hacer en una pasada

`NodeExtractorService.accumulate(texts)` recibe **la lista completa**: TF-IDF necesita frecuencias de documento sobre todo el corpus. No hay versión incremental, y escribir una toca `services/`, que está fuera de alcance.

Entonces el streaming no va *dentro* del extractor. Va antes: **del dump a un archivo de texto**, igual que `corpus_informes_limpio.py`. Ese camino ya está probado.

### Pase A — del dump a un archivo (streaming)

Reusa el parser de filas de `fourforums_pipeline_v8g.py` (`insert_re`, lectura línea a línea con `errors='replace'`).

1. `discussion_topic` en memoria (tabla chica) → ids de discusión con `topic_id = 9`.
2. `post` en streaming → claves `(discussion_id, post_id)` del topic 9. La clave es compuesta: `post_id` no es global en fourforums (v8g lo corrigió).
3. `text` en streaming → cada fila que matchea se limpia y se escribe como **una línea** en `process/corpus_fourforums/topic9_posts.txt`.

Limpieza declarada, no inferida al leer: des-escapar el SQL, sacar BBCode y bloques de quote, colapsar espacios, descartar menos de 40 caracteres (mismo umbral que los informes). Más un `README.md` con las reglas y los conteos, como el corpus de informes.

**RAM del pase A: < 300 MB.** Una fila a la vez; el pico es el `INSERT` más grande más el set de claves del topic 9 (si son ~100k posts, ~15 MB). El tamaño del dump no entra en RAM.

### Pase B — medir antes de construir

Contar posts, palabras y bytes del archivo. **Este número no lo tengo**: el paper dice 414.453 posts en 8 topics y 905 discusiones de gun control, pero no cuántos posts son del topic 9. Estimo **60k–120k**, y el pase B lo mide exacto.

### Pase C — extracción escalonada, con techo declarado

Acá está el riesgo real, y no es el texto: es el **vocabulario de bigramas**. `TfidfVectorizer` construye el diccionario completo y después poda por `max_features`.

Estimación para 100k posts, `ngram_range=(1,2)`, 703 stopwords:

| | |
|---|---:|
| texto en memoria (lista de str) | ~110 MB |
| tokens de contenido | ~9 M |
| bigramas únicos | ~5–6 M |
| diccionario `{término: idx}` | **600–900 MB** |
| CSR intermedia | ~150 MB |
| **pico estimado** | **1.0–1.5 GB** |

Contra 3 GB disponibles **entra, pero sin margen**, y si los bigramas son más diversos que lo estimado se duplica.

Por eso: correr `accumulate` sobre 1k, 5k, 20k, 50k posts y el total, midiendo RSS en cada escalón, y **parar si pasa 2 GB**. Se reporta la curva, no una afirmación.

### Si no entra — dos salidas, las dos declaradas

1. **Muestreo de discusiones con semilla.** Tomar discusiones completas (no posts sueltos: cortar una discusión rompe la co-ocurrencia dentro del hilo) hasta el tamaño que entre. Declarado en el REG con la semilla.
2. **`min_df`.** `_vectorizer(**extra)` ya lo expone, así que no toca `services/`. Pero **cambia qué existe**: subir `min_df` saca términos del pool antes de que compitan. Es decisión del modelo, no mía.

### La unidad de texto es el post

Un post es la unidad propia del dominio, como la versión en los informes. Mediana estimada ~100 palabras, que por REG_unidad_texto §2 es el régimen donde los pares distintos **todavía no saturan** (página 100 dio 487/496 con top_k=32, pero con N más grande el techo sube). Con N = 32 y 100k posts hay que esperar saturación total, así que **el top_k de este corpus es una decisión aparte**.

### Lo que este corpus permitiría además

Es el único corpus del proyecto donde la tensión existe. Entonces se puede **comparar las dos respuestas sobre el mismo texto**: qué fronteras encuentra SALAMANCA sobre W_pos, contra qué pares negativos produce el ruteo por marcadores. En los demás corpus esa comparación no tiene sentido porque no hay tensión que encontrar.

### Lo que falta para ejecutar

- El dump. No está, y no lo puedo bajar.
- Tu OK al pase A y al techo de 2 GB.
