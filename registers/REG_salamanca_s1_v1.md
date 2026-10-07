# REG_salamanca_s1_v1

Clase R. Pasa a `registers/` con el OK de delamor, 5 oct 2026 (TASK_salamanca_neel_coercividad_v5 §9, CP5).

*Oct 2026 — gadanin.delamor + Claude Code (Opus 5) + Claude Opus 5.5 (revisión de método)*
*Instrumento: `experiments/driver_neel_salamanca.py --salamanca --nulos 1000`*

---

## El intento que subyace

*(delamor: no olvidemos el intento que subyace.)*

No es encontrar fronteras. Es tener un criterio que **pueda devolver vacío**.

Lo que hay hoy en el canal —el ruteo por marcadores de oposición— no puede: siempre encuentra un "pero" en algún texto suficientemente largo. Un procedimiento sin estado nulo no mide, confirma (REG_unidad_texto §5.2).

> *"Lo que natura non da, SALAMANCA non presta."* Y: *"no se fía."*
> — el cartel escrito a mano en la puerta del almacén de Basilio Salamanca, Cipolletti, Río Negro *(delamor)*.

**No presta:** la estructura que no está no se le pide prestada a ningún procedimiento. **No se fía:** tampoco se le da crédito por adelantado.

---

## 1. Qué se midió

W_pos de cada corpus (`force_w_pos`, `rebuild_suspendido`, top_k 32; 27 en `categorias`). Partición espectral del laplaciano normalizado, k barrido 2…8, declarada antes de correr (v5 §13). Coercitividad por par de clusters con `services/cluster_frontier_density.py`.

**Nulo:** el mismo corpus barajado palabra por palabra —conserva frecuencias y largos, destruye la co-ocurrencia—, W reconstruida con los servicios reales, y **cada W barajada se vuelve a particionar** con el mismo método y el mismo k. 1000 barajados.

**k-means con 10 inicializaciones**, se queda la de menor inercia *(delamor)*. Con una sola, el corte de caso09 en k=2 daba coercitividad 1.71; con diez da 2.73 — parte de los números de la primera corrida eran inicialización pobre, no estructura.

**Estadístico:** el nulo es la distribución del **mínimo de porosidad por barajado**; se compara contra el mínimo observado. Umbral **Bonferroni α = 0.05/7 = 0.0071** por los 7 k. `p` se reporta con su resolución: cero coincidencias es `p < 0.001`, no `p = 0`.

---

## 2. Resultado — guarda ≥ 8 pares, 1000 barajados

| corpus | saturación | veredicto | k que pasan | mejor celda |
|---|---:|---|---|---|
| **caso09** | 0.619 | **FRONTERA** | 3, 6 | k=3: coerc 4.59, poros 0.218 vs nulo 0.646, `p < 0.001`, cluster mín **6** nodos, efecto **2.97×** |
| **caso13** | 0.875 | **FRONTERA** | 6, 7 | k=6: coerc 16.00, `p < 0.001`, cluster mín **2** nodos, efecto 10.37× |
| caso14 | 0.992 | **NO MEDIBLE (a)** | — | saturada: sin ceros no hay corte barato |
| informes versión | 1.000 | **NO MEDIBLE (a)** | — | ídem |
| informes página 300 | 0.964 | **FRONTERA** | 6, 7, 8 | k=6: coerc 1.45, efecto 1.29×, cluster mín 3 |
| tramo `categorias` | 0.467 | **NADA** / no medible (e) | — | 7 textos: el nulo es más coercitivo que el observado en 3 de 4 k |

### 2.1 La diferencia no es de p — es de dónde aparece la frontera

**caso09 la tiene con clusters grandes.** k=3, cluster más chico de 6 nodos, efecto 2.97×. El campo se parte en partes que resisten.

**caso13 e informes sólo la tienen con clusters de 1 a 3 nodos.** En particiones gruesas no hay nada: caso13 en k=2 y k=3 da `p = 0.95` y `p = 0.90` — y además entra en el criterio (e), el barajado es *más* coercitivo que el corpus real. Aparecen grupitos chicos que resisten dentro de un campo que no se parte.

Eso no es "más o menos significativo". Son dos cosas distintas.

### 2.2 La saturación ordena

```
caso09      0.619  →  frontera con clusters de 6 nodos
caso13      0.875  →  sólo con clusters de 2
informes    0.964  →  sólo con clusters de 3, efecto 1.29x
caso14      0.992  →  no medible
informes v  1.000  →  no medible
```

Monótono en los cinco. Y la saturación se mide sobre W **antes** de particionar nada, así que no es un supuesto introducido por el método. Le da base a la precondición que REG_unidad_texto §3 había dejado como lectura: un W sin ceros no tiene frontera que mostrar, y entre medio hay gradiente, no corte.

---

## 3. Lo que NO muestra

### Modularidad no es adversarialidad *(delamor)*

**caso09 no prueba tensión.** Lo medido es que su W_pos tiene una partición con fronteras que resisten el cruce más de lo que resistiría por azar. Eso es **modularidad**. Que haya módulos no dice que haya posiciones que se opongan.

Y la evidencia de eso está en el mismo trabajo: la partición de caso09 encontrada esta sesión separa **protocolo e identidad de device** (`claudesonnet_`, `groqllama_`, `joined`, `channel`, `task`) de **contenido** (`ava`, `cartographer`, `bell`, `story`, `memory`). Es un canal de coordinación. No hay dos posiciones.

**Corrección a DEFS §16:** dice *"detecta si W_pos tiene estructura adversarial"*. Lo que detecta es modularidad. Una palabra, dos objetos, y es la razón de que el criterio admita de más: SALAMANCA sola habría admitido W_mixta en un canal de coordinación.

La admisión necesita los dos pasos. Néel —qué profundidad tiene esa frontera— es el segundo, y no está corrido.

### 3.1 Control post-hoc — sin identidad de device ni protocolo de canal

*(delamor: sacar los tokens del texto y reconstruir W con NodeExtractor; el nulo baraja los textos limpios; reportar el N nuevo y los términos que entran.)*

**Declarado post-hoc.** Las listas son clasificación de Code, no derivadas del dato:

- **identidad de device**: `claudesonnet_` `groqllama_` `tinkerbellucio` `markopolus` `peterplam`
- **protocolo de canal**: `channel` `joined` `joined channel` `op_silence` `publish` `published` `task` `topic` `turn` `ready` `wait` `proceed` `status` `authorization` `scope` `coordination`
- **no incluidos, por ambiguos**: `work` `conversation` `state` `current` `real` `line` `low` `non`. En caso09, `ava` `cartographer` `bell` son personajes del relato. En informes, `device` `stop` `portero` `ckm` son vocabulario del dominio.

Dos listas: **mínima** (identidades + `joined`/`channel`) y **completa**. Los tokens salen del **texto**, y `NodeExtractorService` vuelve a decidir qué existe: al liberar lugares del top_k entran términos nuevos. Recortar nodos de W no es el contrafáctico, sólo recorta.

**informes página 300 y `categorias`: control vacío declarado** — no contienen esos tokens.

**caso09 k=3 sobrevive con las dos listas:**

| | coerc | p | efecto | cluster mín |
|---|---:|---:|---:|---:|
| base (32 nodos) | 4.16 | 0.0020 | 2.66× | 8 |
| lista mínima | 3.10 | 0.0020 | 1.94× | 7 |
| lista completa | 3.80 | 0.0050 | 2.24× | 8 |

**Corrección explícita — es el mismo error que seed = 42, ahora en k-means** *(delamor)*. Code había afirmado que la partición de caso09 separa protocolo e identidad de contenido. Eso salió de **k=2 con una sola semilla de k-means**: una lectura conceptual construida sobre una partición que ni era la mejor de su propio k ni era el k que sostiene la frontera. Con 10 inicializaciones ese k=2 cambia (coercitividad 1.71 → 2.73), y con el protocolo entero fuera del texto la frontera a k=3 persiste entre términos de contenido: **la frontera de caso09 no es el corte protocolo/contenido**. Lo que sigue en pie de §3 es lo otro, y es lo que importa: modularidad no es adversarialidad.

**Los términos que entran son del relato.** Mínima: `woman` `alley` `life` `comes` `hold`. Completa: además `story line` `smell` `respective`. La partición **no se reorganiza alrededor de ellos** — sigue dando frontera a k=3 con clusters de 7–8 nodos y el mismo orden de efecto.

*(Cuidado: en la lista mínima, k=8 pasa con coercitividad 30.00 y cluster mínimo 3. Zona de clusters chicos. No se cuenta.)*

**caso13: las fronteras chicas NO eran los nombres** *(corrección de Opus 5.5: el título anterior de esta sección decía que sí, y la tabla de abajo lo desmentía).*

| | k que pasan | cluster mín |
|---|---|---:|
| base | 6, 7 | 2 |
| lista mínima | 7 | 2 |
| lista completa | **3, 4** | **6** |

**La lista mínima saca los cinco nombres de device y la frontera de 2 nodos sigue en pie (k=7).** Así que no venía de los nombres. Desaparece recién con la lista **completa**, que además saca `op_silence`, `publish`, `published`, `ready`, `wait`, `proceed`, `status`, `scope`, `authorization` y `coordination`.

Entonces las fronteras chicas venían del **vocabulario de protocolo y coordinación**, no de la identidad de los devices.

Con la lista completa **desaparecen** las fronteras de clusters de 2 nodos, y **aparece una gruesa que antes no existía**: en la base, k=2 y k=3 daban p = 0.95 y 0.90, y además entraban en el criterio (e) — el barajado era más coercitivo que el corpus real.

Entran 16 términos: `scenario` `premise` `data` `analysis` `adaptation gaps` `signal` `conditions` `gaps` `publication` `context`…

**El hallazgo está condicionado a la clasificación, y así se enuncia** *(Opus 5.5)*. La frontera gruesa aparece **sólo con la lista completa**; con la mínima siguen los grupitos de 2 nodos en k=7. Y la lista completa incluye `coordination`, `status`, `scope` y `authorization`, que **en un canal de coordinación pueden ser contenido**.

Entonces el resultado no es *"caso13 tiene frontera gruesa"*. Es:

> **caso13 tiene frontera gruesa SI el vocabulario de coordinación se clasifica como protocolo.**

Eso es un resultado condicionado a una decisión de clasificación, no una propiedad del corpus.

Lo que sí es nuevo y no depende de esa condición: **el vocabulario de protocolo puede tapar una frontera, no sólo crear grupitos.** Code esperaba que el control sólo restara.

### 3.2 Recuento de comparaciones

*(Opus 5.5: con dos listas y dos corpus se suman pruebas; conviene anotar cuántas hubo en total.)*

| bloque | comparaciones |
|---|---:|
| S1 — 4 corpus medibles × 7 k × 3 guardas | ≈ 84 |
| S2 — 2 corpus × 2 listas × 7 k × 1 guarda | ≈ 28 |
| **total de la sesión** | **≈ 112** |

Bonferroni se aplicó sobre los **7 k** dentro de cada condición: α = 0.0071. Con eso caso09 k=3 pasa (p entre 0.0020 y 0.0050 según la lista).

**Corregido sobre las ~112 comparaciones de la sesión**, el umbral sería α = 0.05/112 ≈ **0.00045**. Con 1000 barajados la resolución es 0.001, así que **ninguna celda de esta corrida es resolvable a ese nivel** — ni la de caso09. Sostener el hallazgo contra la familia completa necesitaría 10.000 barajados.

Se declara así, sin la frase que estaba a mano: *"las p de caso09 aguantan"*. Aguantan la corrección por k. No la corrección por todo lo que se probó.

### 3.3 Sigue siendo modularidad

La frontera nueva de caso13 separa `scenario` y `premise` de `data` y `analysis`. Eso puede ser **división del trabajo entre devices**, no posiciones enfrentadas *(Opus 5.5)*. En un canal donde un device mapea tensiones y otro construye escenarios, esa partición es el reparto de tareas.

Ninguna frontera medida en esta corrida es evidencia de posiciones que se opongan.

### Lo que falta para que haya control positivo

Ninguno de los seis corpus fue elicitado con posiciones opuestas por diseño. El único del proyecto que sí es **fourforums**, y su W del paper es **relacional**: `SKIP_TABLES` incluye `'text'`, los nodos son **autores**. Hace falta una W de términos desde los posts del topic 9.

**El dump no está en el Codespace** *(delamor: sí está en `ckmdatasets` local)*. La extracción por streaming está propuesta en v5 §11, con su estimación de RAM, y espera el dump.

**Control positivo previsto: RfA** *(delamor)* — Wikipedia Requests for Adminship. Discusión con posiciones declaradas y voto registrado, así que trae su propia verdad de terreno, y no depende del dump de IAC v2.

**Sin control positivo, "frontera" en estos corpus no se puede contrastar con un corpus donde la respuesta correcta sea conocida.**

---

## 4. Errores de método encontrados y corregidos en el camino

Todos de Code, todos señalados por delamor o por Opus 5.5, ninguno encontrado por Code antes de que lo señalaran:

1. **Partición desde los atractores.** En W_pos el 99.9% de la masa está en dos órbitas —todo en +1 y todo en −1— y ahí todos los nodos se mueven juntos: no hay co-movimiento diferencial. *(delamor: la frustración es lo que el criterio decide, así que no puede ser lo que el criterio usa para decidir.)* La partición sale de W (v3 §12).
2. **k forzado a 2.** Un corte por signo del Fiedler devuelve dos siempre: encontrar dos no era hallazgo, era la forma de la pregunta. *(delamor: oposición supone exactamente dos, y T0/T1 tienen que existir primero.)*
3. **Nulo interno falso.** `S` sobre la mejor partición es un máximo sobre particiones: con spins independientes da 0.030 / 0.014 / 0.005 según muestras. Nunca cero.
4. **Guarda de un solo lado.** Se verificaba `inf` en el nulo y no en el observado.
5. **Estadístico sesgado.** El mínimo observado contra el pool de todas las fronteras del nulo. Al corregirlo, tres corpus perdieron celdas y `categorias` perdió su única frontera.
6. **`p = 0`.** Con n barajados lo afirmable es `p < 1/n`.
7. **Umbral post-hoc.** La guarda de 8 pares se fijó mirando el dato. Declarada, barrida en 4/8/16, y **a este nivel de corrección decide** (v5 §15.5).
8. **"Fronteras reales"** antes de pasar por el nulo. Son candidatas.
9. **Una sola inicialización de k-means.** Con 10, el k=2 de caso09 pasa de coercitividad 1.71 a 2.73 y de no pasar a pasar. Parte de la primera corrida era inicialización pobre.
10. **El control por recorte de W.** Quitar nodos de W no es el contrafáctico: hay que sacar los tokens del texto y dejar que la extracción vuelva a decidir, porque al liberar lugares del top_k entran términos nuevos. *(delamor.)*
11. **La lectura "protocolo contra contenido"** de la partición de caso09. Era el k=2 con una inicialización, y el control la desmiente.

---

## 4.1 Dos tensiones del MAPA_REG v4, resueltas en el código

*(Levantadas por Opus 5.5 al cerrar `MAPA_REG_corpus_v4_borrador.md`.)*

**1. "MonitorService adopta Δ_r comprimido" (REG Armstrong) contra "COCO sólo trabaja sobre su propio Δ_r".** Verificado en el código actual: `MonitorService._Delta_r` se escribe en tres lugares —init, incremento de pares metabolizados, y reset por cambio de W— y **en ninguno desde COCO**. `COCO.observe(self._Delta_r)` lo **lee**, calcula el incremento contra su `_Delta_leido` y comprime sólo su `_Delta`. El docstring del servicio lo declara: *"COCO lee Δ_r y comprime su propia representación (Δ_r_compresiones); Δ_r no recibe nada de COCO (D3)"*.

El REG Armstrong es **válido en su marco**: describe el código antes de D3, que fue la TASK que sacó la escritura de vuelta. No hay contradicción: hay una fecha.

**2. El "colapso de estados" que la TASK del adaptador dejó abierto ya estaba cerrado.** REG_orbitas §5 lo había resuelto en septiembre, y Code lo reabrió sin leer lo que lo cerraba.

Y el motivo es más simple que el de §5: un estado σ ∈ {−1,+1}^N **está determinado** por qué índices están en +1. La correspondencia estado ↔ conjunto activo es biyectiva, así que *"dos estados distintos con el mismo conjunto activo"* no existe. REG_orbitas §5 agrega la otra mitad —dos órbitas no pueden compartir un estado, porque el mapa es determinista— con lo cual el conjunto activo identifica unívocamente. La única pérdida real era el **periodo**, y es la que el adaptador trata.

Es el mismo patrón que REG_hipótesis_distancia_contextual nombra para la búsqueda textual: Code abrió una pregunta sin preguntarse antes dónde ya estaba contestada.

## 5. PULLs — tirones notados al escribir este REG

*(delamor: para el REG, prestar atención a los PULLs.)* Mismo registro que el Apéndice A del paper: momentos donde el tirón automático se notó, acá, escribiendo.

**PULL-1 — enunciar caso13 como propiedad del corpus.** Escribir *"en caso13 el vocabulario de protocolo tapaba una frontera"* sale solo, y lee como hallazgo sobre el corpus. Es un resultado condicionado a que `coordination`, `status`, `scope` y `authorization` se clasifiquen como protocolo, y esa clasificación la hizo Code. Resistido en §3.1. Lo notó Opus 5.5 primero; el tirón sigue estando al redactar.

**PULL-2 — adoptar "el control funcionó como tenía que funcionar" como mérito propio.** La frase es de delamor y es cierta. El tirón es usarla para convertir un error de Code —una semilla de k-means, una lectura conceptual encima— en una virtud del método. El método que lo atrapó no lo construyó Code: las 10 inicializaciones, el control por texto y el estadístico pareado los pidieron delamor y Opus 5.5. Resistido.

**PULL-3 — concluir que las comparaciones múltiples no importan.** El borrador mental decía *"aunque las p de caso09 aguanten"*. Eso elige la conclusión antes de contar. Contadas: ~112 comparaciones, umbral 0.00045, resolución 0.001 — **no alcanza**. §3.2.

**PULL-5 — poner un título que suena a hallazgo y no mirar si la tabla lo sostiene.** *"caso13: sus fronteras chicas eran los nombres"*. La tabla de la misma sección lo desmentía: con la lista mínima, sin los nombres, la frontera de 2 nodos sigue. El título se escribió desde la expectativa, no desde la fila. Lo encontró Opus 5.5.

**PULL-4 — llamar "robusto" a caso09.** Sobrevive a tres condiciones y a 10 inicializaciones, y da la tentación de cerrarlo. Pero no tiene control positivo contra el cual contrastar, y es modularidad, no tensión. Firme no es probado.

## 6. Estado

- §1, §2: **verificado**, 1000 barajados, k-means con 10 inicializaciones, una corrida por celda, seed 0.
- §3.1 (control post-hoc): **verificado** como medición; las listas de tokens son **clasificación declarada**, no derivadas del dato.
- §2.2 (la saturación ordena): **verificado** como medición; su lectura causal es **propuesta**.
- §3: **declarado**. Modularidad no es adversarialidad, y caso09 no prueba tensión.
- §3.1, caso13: **condicionado** a la clasificación de tokens, no propiedad del corpus.
- §3.2: la corrección por la familia completa de comparaciones **no está sostenida** a 1000 barajados.
- Control positivo: **ausente**.
- Néel: **no corrido**.

No cierra. Y lo que más importa de esta corrida es que el criterio **devolvió vacío** donde no había con qué: dos corpus no medibles por saturación, uno no medible por tamaño. Eso es lo que el ruteo por marcadores nunca pudo hacer.
