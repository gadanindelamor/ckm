# TASK_ckm_trust_rule_v1

*11 oct 2026. Escrito por Opus (Cowork), por pedido de delamor: "el código de criterio_local no sería más que instanciar la regla CKM TRUST, escrita en código; respetemos nombres de rótulos en inglés". Para Code, en el Codespace.*

## Por qué

La regla CKM TRUST está escrita (`REG_regla_ckm_trust_v1`, 4 oct) y tiene una forma (doc "La regla CKM TRUST", 11 oct). En el código no existe como objeto: aparece repartida, entera en un sitio y a medias en otros.

- **`criterio_local.py` (CP2b)** es donde está más entera. Tiene campo con registro, conservación, piso, auditoría con tasa nombrada, `SKIP` y `None` declarado.
- **`should_rebuild`** es la misma decisión de estado pero con la regla a medias: criterios en cascada, origen en `causa`, valores sin origen.
- **`calibrate`** es la regla aplicada a los parámetros de otra regla.
- **`NodeExtractor._seleccionar`** tiene corte, `TOL_EMPATE` y selección anterior.

Lo que dijo delamor (11 oct):

- **La regla es sobre órdenes**, con dependencias entre órdenes contiguos y recursión: condiciones_i → calibrar → condiciones_{i+1}.
- **El criterio local decide si escalar al orden siguiente** (el LLM, la decisión).


**delamor, 11 oct (admisible, no verificado):** *"si fuese admisible, al menos: este engine de la regla puede ser algo que emerge en el modelo, desde el modelo, como su propia metodología de proyecto, que lo está formando como instrumento. ERGO: se trata de identificar los órdenes de escala y, al instanciarla, el engine de la regla sabe qué hacer."* Calibrar, decidir en ODA y revisar el alineamiento (PoC) serían instancias. El protocolo de trabajo (Code → ALTO → Opus → delamor) también. Escalar a una instancia del **mismo** orden no es escalar: ↑k tiene que ser otro orden.

**ε, delamor (11 oct):** *"épsilon en la regla, el definido en su formulación. El nombre deja el que tenga ahora, tolerancia. Me refiero a que NO olvidemos a épsilon."*

- ε es la **tolerancia de la regla** (I3, sin cambios), y **no se omite en ninguna instancia**.
- Hoy falta en `criterio_local` y en `should_rebuild`. Si no se conoce, va **`None` declarado**, nunca 0. Un empate sin ε declarado es un empate que nadie ve.
- delamor: *"sin épsilon el engine no va a funcionar"*. Para el código, eso quiere decir que `tolerance` es un **argumento obligatorio, sin default**, igual que `causa` en `rebuild_por_decision` y que `piso_vueltas <= 0 → ValueError`. Si es `None` declarado, toda decisión cerca del corte lo lleva en su registro (`tolerance_unknown`): no se decide como si fuera 0.
- delamor: *"si no se conoce, tal cual: se declara, y LA REGLA lo descubre al instanciarse en el proceso de calibración. Y allí el bucle elipse que escala al orden espiral, y así, y así."*
  - ε = `None` en el orden k es un candidato del orden ↑k. Calibrar es Regla_{k+1} aplicada a los parámetros de Regla_k, así que lo descubre y lo devuelve en condiciones_{i+1}.
  - La **elipse** es el bucle cerrado dentro de un orden; la **espiral**, la escalada de un orden al siguiente.
- **Precisión de la regla** (delamor): está hecha de la precisión del intervalo que define ε, la identificación de los órdenes, las condiciones y las trazas. **Lo importante es no olvidar ε.**
- **No confundir con `TOL_EMPATE = 1e-12`** de NodeExtractor, que es tolerancia numérica.
- *(Se deja como traza: delamor también dijo "o yo le llamaría de confianza, quizás". Queda **abierto** si su valor puede salir de la incertidumbre de la medición.)*

## Forma a implementar (propuesta de Opus; la valida delamor)

```
Regla_k = ⟨ C_k, f_k, R_k, κ_k, ε_k, T_k, P_k, g_k, ↑k ⟩

1. |f_k(c) − κ_k| > ε_k             → decide f_k              origin = FIELD
   · (CP4, 13 oct: acá estaba la exención por capacidad, y SE FUE)
2. empate y existe T_k               → decide T_k (conserva)   origin = TRACE
   · si 2 se repite P_k veces sin campo → 3
3. no hay T_k (o se cumplió el piso) → NO_TRACE:
   · ¿se aplicó f_k? no → 1
   · sí → escala la duda a ↑k                                origin = ESCALATED
4. no hay ↑k, o ↑k no decide         → g_k nombrado            origin = CONTEXT
```

**Recursión:** los parámetros de Regla_k (κ_k, ε_k, P_k) son candidatos de Regla_{k+1}, es decir, calibrar. **Caso base:** el orden sin ↑k decide con g declarado. Es el arranque en frío.

## Nombres de código (identificadores `.py` en inglés, como los servicios)

- **Módulo:** `services/ckm_trust_rule.py`.
- **Tipos:**
  - `Origin`, con los valores `FIELD`, `TRACE`, `ESCALATED`, `CONTEXT`;
  - `RuleParams`, con `cut`, `tolerance`, `floor`, `calibrated`;
  - `Decision`, con `value`, `origin`, `record`, `reason`;
  - el estado del paso 3 se llama `NO_TRACE` (en la forma escrita, *SIN_TRAZA*);
  - `CkmTrustRule`, con `field_criterion`, `trace`, `context`, `escalate_to`.
- **No se renombra nada de lo que existe.** `criterio_local.py`, sus constantes (`VIA_*`, `MOTIVO_*`, `DECISION_SKIP`) y `UmbralesCriterioLocal` quedan como están. El mapeo de una cosa a la otra se declara, no se reescribe.

## Desalineamientos ya encontrados (entrada del CP0)

delamor: *"el campo continuo no salta; salta la medición; el instrumento NO salta"*. Cada desalineamiento es un lugar donde una instancia de la regla tiene un casillero roto: la medición discretiza o normaliza y el contexto entra como campo. La columna **casillero** dice qué elemento de la forma rompe.

| de dónde | qué | casillero | fuente |
|---|---|---|---|
| **discretizar** | presencia por texto entero; W ≥ 0, sin canal para la ausencia → T = 0 por construcción | f (sin signo) | TASK_tests_instrumento CP3, 10 oct |
| discretizar | marcadores de oposición por substring ("distri**but**ion") aplicados al texto entero | g sin nombre, presentado como f | TASK_tests_instrumento CP1 |
| discretizar | `top_k`, pool `top_k·3`, idf, `TOL_EMPATE`; orden alfabético en el empate | κ, ε; g (I4) | `node_extractor._seleccionar`, REG regla §4 |
| discretizar | dinámica síncrona con N par → órbitas de período 2; el "colapso" de calibrate no colapsa (N_eff ≥ 2 por Z₂) | el patrón de calibrate depende de la paridad de N | juguete de Opus, 10–11 oct (doc tejido) |
| **normalizar** | `W / max_abs` en CorpusService | escala de la medición | `corpus_service.py:332-335` |
| normalizar | `Δ / max(Δ)` dentro de la meseta | escala que salta dentro de la meseta | DECISIONES 10 oct (4): se fija al nacer el ciclo |
| normalizar | **las medias, tres convenciones**: sobre `W>0`, sobre `≠0`, sobre todos | regla desalineada entre sitios | BANDEJA `7abc160` |
| normalizar | `coco._beta_c` → `inf` y `beta_c_landscape` → `None` para el mismo caso | I2 (ausencia como valor) | BANDEJA `7abc160` |
| **el signo** | Δ se **suma** a W (`_combine_W_Delta`, `coco.observe`): el rechazo del campo entra como co-ocurrencia | origen del negativo | DECISIONES `20247ee` |
| **valores sin origen** | `min_texts=3` (era 10), factor 2, `n=3`, `MAX_CICLOS=10` "provisional", `piso_vueltas=12`, `dt_minimo_s=5.0` | κ, P puestos por alguien: g | DECISIONES `c2a0f1b`, BANDEJA `f3f8cc7` |
| valores sin origen | `min_texts=0` leído como valor → `2·0 = 0` → volumen siempre verdadero | I2: el nulo escrito como 0 | DECISIONES 11 oct |
| **cascada** | estructural > volumen > tiempo en `elif`: el criterio con valor sin origen tapa a los otros | orden de los pasos no es de la regla | `ckm_monitor.py:314-321` |

**Traza previa (delamor, 11 oct):** la revisión ya había empezado. `REG_regla_ckm_trust_v1` §4 (4 oct) es una tabla de los sitios donde la regla ya opera, verificada leyendo. Ahí están `_seleccionar`, el bootstrap, el `NOMINAL` por defecto (paso 4 subrepticio), la cancelación de α, el bootstrap = 12 (sesgo de destino) y los casos de Salamanca. Su §7 dejó para Code un CP1, el inventario de sitios de decisión en `services/` e `iap_chatroom/`, que **nunca se ejecutó** (no aparece en la BANDEJA). El CP0 de este TASK parte de esa tabla y retoma ese inventario: es paso 2, decide la traza. El REG está en la carpeta de delamor (`antropic/trust___project/structure_topology/`), no en el repo. Subirlo es decisión de delamor.

**La PoC del volumen** (la orden de delamor del 11 oct) todavía no está en `origin/main`. Cuando Code la suba, sus hallazgos entran a esta tabla.

## Un solo corazón (delamor, 11 oct)

*"Que evite duplicar el corazón en cada aplicación de la regla, como `criterio_local.py`."*

- El engine (pasos 1–4, empate con ε, piso, origen, registro) vive **una sola vez**, en `services/ckm_trust_rule.py`.
- Cada aplicación es una **instancia**: le pasa al engine sus C, f, κ, ε, T, P, g y ↑k, y **no reimplementa ningún paso**.
- `criterio_local.py` hoy tiene su propio corazón: es la traza de cómo era antes. No se toca hasta el CP3 (orden de delamor). Hasta entonces, el CP2 lo expresa como instancia en un test.
- Test estructural (CP1): ningún otro módulo implementa la lógica de empate, piso u origen. Si aparece una segunda copia, el test falla.

**Primera instancia real, CP1b:** la PoC de marcadores. delamor: *"PoC, y regla CKM, en un módulo"*.
- **C:** hoy (substring sobre el texto entero), saneado (palabra entera) y separado (W de contexto propia, declarada).
- **f:** falsos positivos contra los casos reales registrados (CP1 de `TASK_tests_instrumento`), con su registro.
- **ε:** declarado, o `None` registrado.
- **T:** la variante vigente.
- **↑k:** delamor.
- **g:** nombrado, si se llega al paso 4.
- **Reporta:** la decisión con su origen. Es la decisión de "¿sanear o separar?" para la rama operativa (`paper`) frente a la rama `trust`, y no la toma Code: la toma la regla, o la escala.

## Reglas del TASK

1. **Gate `f96c234`.** Ningún comportamiento vivo cambia. El módulo nuevo es puro y nadie lo llama hasta el CP3.
2. **I2:** la ausencia no tiene valor por defecto. `tolerance` y `floor` faltantes son `None` declarado: nunca 0, nunca un default.
3. **I5:** el paso 3 no resuelve, escala. Sin `escalate_to`, devuelve `ESCALATED` con `escalate_to=None` y quien llama decide. No cae al paso 4 solo.
4. **Docstrings en el mismo commit** (regla del 10 oct). Si el código y el docstring difieren, se declara.
5. **Archivos nombrados uno por uno** al commitear, sin `git add -A`.

## Checkpoints

| CP | qué | reporta |
|---|---|---|
| **CP0a** | Sin código. **Identificar los órdenes de escala** y su contigüidad. Criterio propuesto (Opus): un orden es lo que queda fijo mientras el de abajo varía. Por ejemplo σ por mensaje sobre W fija, W por meseta, condiciones por ciclo de calibración. | Lista de órdenes, qué queda fijo en cada uno, cuál es el ↑ de cada uno, y dónde no se pudo decir. |
| **CP0b** | Sin código. **Dónde falla la regla.** delamor: *"si una regla no verifica que existan condiciones donde ella misma falla… si nunca falla, ser inexorable consigo misma la extingue: deja de observar sentido alguno"*. Buscar instancias donde la regla, aplicada al pie de la letra, da un resultado equivocado o no entra. Casos ya vistos: el paso 2 sin piso hace absorbente al silencio; el patrón de calibrate supone colapso, y con Z₂ y N par no colapsa; NodeExtractor no tiene ↑k; restar sólo la dirección no recuperó nada. | Las condiciones de falla, y para cada una si la falla es de la forma o de la instancia. **Un CP0b vacío es un resultado que se sospecha, no un éxito.** delamor: *"falla" como fisura, no como error; "la falla señala una disrupción de orden de escala"*. Por eso cada falla del CP0b **marca un borde entre órdenes**, y vuelve como entrada al CP0a. |
| **CP0** | Sin código. Escribir cada instancia en la forma: `criterio_local`, `should_rebuild`, `calibrate`, `NodeExtractor._seleccionar`. Tabla con un casillero por elemento, citando archivo y línea. | Los casilleros vacíos, usando como entrada la tabla de desalineamientos (Opus vio: ε falta en criterio_local y en should_rebuild; P falta en calibrate; el volumen es un g sin nombre) y las instancias que **no entran en la forma**. Si una no entra, se reporta, no se fuerza: puede fallar la forma o la instancia. |
| **CP1** | `services/ckm_trust_rule.py`, puro, con tests de la forma: los cuatro orígenes, el empate con ε, **`tolerance` obligatoria (sin default; `None` sólo declarado y registrado)**, el piso que lleva de 2 a 3, `None` declarado, el paso 3 sin `escalate_to`. | Verde, xfail o lo que no se pudo testear. |
| **CP2** | Expresar `CriterioLocal` como instancia de `CkmTrustRule` **en un test**, sin tocar `criterio_local.py`. Mismas entradas, mismas decisiones, mismos motivos que hoy, sobre `experiments/vivo_03_criterio_local_log.json`. | Bit a bit igual, o la lista de diferencias. Cada diferencia es una diferencia entre la forma y la instancia, y se reporta sin elegir. |
| **CP3** | **Sólo con orden de delamor:** que `criterio_local.py` instancie el módulo. **Paso fijo, antes del ALTO: la sección "Lo que la forma no nombra"** (acordado el 12 oct, escrito el 13). | Las 24 decisiones de `vivo_03` iguales y la suite completa sin cambios, más **"Lo que la forma no nombra"**. |

## "Lo que la forma no nombra" — paso fijo de todo mapeo a la regla

*Acordado con delamor el 12 oct; quedó sin escribir y se escribe acá el 13. **Vale
para cada mapeo futuro de una instancia a la regla**, no sólo para el CP3.*

Un mapeo que sólo reporta lo que **entró** en los casilleros da por no existente lo
que quedó afuera. La forma `⟨C, f, R, κ, ε, T, P, g, ↑k⟩` tiene nueve casilleros, y
una instancia viva suele distinguir cosas que **ninguno** de los nueve nombra.

El reporte del mapeo lleva una sección con esa lista. Para **cada** elemento:

- **qué distinguía** la instancia,
- **dónde vivía**: `archivo:línea` **antes** del cambio,
- **dónde vive después**, o **"se pierde"** si se pierde.

**Si algo se pierde, no se resuelve: se reporta y ALTO.** Perder una distinción es
una decisión sobre el modelo, y no es de Code.

Un elemento puede quedar afuera de los nueve casilleros y **no** perderse: puede
sobrevivir como rótulo leído del registro, como insumo en `field_inputs`, o
alrededor del engine —la auditoría **mide** la regla y por eso no es un casillero
de la regla—. Eso también se declara, con su lugar nuevo.

**La distinción que importa, y que el reporte tiene que hacer explícita:** no es lo
mismo perder una **decisión** que perder un **rótulo**. Perder una decisión es ALTO.
Perder un rótulo —la instancia distinguía dos razones y la forma escribe una sola—
se declara **como pérdida**, con su nombre, y lo resuelve delamor. Un reporte que
dice "nada se pierde" porque ninguna decisión cambió está tapando la segunda
(corrección de Opus, 13 oct, sobre el reporte del CP3).

## CP4 — la exención del paso 1 salió de la regla

*Orden de delamor, 13 oct: **"bueno vamos por sacar la exención de la regla"**,
citando a Opus: *"la exención sólo entra en juego cuando hay una capacidad, un número
de lugares, como `top_k` en `_seleccionar`"*.*

**Fundamento:** la **tercera entrada del CP0b**. Donde hay empate el campo **calla**
—`|f − κ| ≤ ε` es exactamente *"el campo no distingue"*—, y la exención le daba esa
decisión a la **capacidad**, un número declarado por el orden de arriba. **Por la
regla, donde el campo calla decide la traza.**

**Qué se fue:** la salida del paso 1 por capacidad (`len(tied) <= free → FIELD ·
tie_fits_free_slots`).

**Qué se queda:** `capacity` y `free`, que los usan el **paso 2** —si lo que la traza
conserva no cabe, el paso 2 no decide: `REASON_TRACE_SHORT`— y el **paso 4**. Y la
constante `REASON_TIE_FITS`, **sin producirse**: hay registros ya escritos donde
`reason` vale `"tie_fits_free_slots"`, y borrar el nombre deja ese dato sin a qué
resolver.

**Divergencia declarada:** `node_extractor._seleccionar` **conserva su propia copia
de la exención** hasta el **CP2 de `TASK_node_extractor_regla_v1`**. Hasta entonces,
el engine y esa instancia **no coinciden en ningún régimen de empate** (medido: el
barrido del CP1 pasó de 30/60 a **0/90**).

**Alcance:** `services/ckm_trust_rule.py` y lo que lo describe. **`_seleccionar` no
se tocó.**

## CP0b — entradas registradas, sin resolver

*Se va llenando a medida que aparecen. Cada una **marca un borde entre órdenes** y
vuelve como entrada al CP0a (del TASK que corresponda).*

### 1. El pool de `NodeExtractor` escribe `C` **y** `f` de la misma regla

*Entrada del 13 oct, desde el CP1 de `TASK_node_extractor_regla_v1`. **Falla de la
forma**, no de la instancia.*

`max_features = top_k·3` (`node_extractor.py:218`) hace **dos** cosas sobre
`_seleccionar`:

- le **arma el `C`**: corta por frecuencia qué términos son candidatos;
- le **mueve el `f`**: `TfidfVectorizer` aplica `max_features` en el
  `CountVectorizer`, **antes** del transform, así que la norma l2 de cada documento
  se calcula **sólo sobre los términos del pool**. Recortar el pool **no filtra:
  re-puntúa**.

**Medido** (CP0 g, 13 oct): con los **mismos** candidatos y cambiando sólo sobre qué
vocabulario se normaliza, en `armstrong_replica_seed123` y `armstrong_via_corpus_v3`
**cambian el orden y el conjunto**, con **6 términos** que entran o salen.

**Por qué es de la forma.** En `⟨C, f, R, κ, ε, T, P, g, ↑k⟩`, `C` y `f` son
**casilleros distintos de la misma regla**, y la forma no tiene cómo escribir *"algo
que llena `C` y al hacerlo cambia `f`"*. **Un `C` que cambia el `f` del paso
siguiente no es un `C`.**

**delamor, 13 oct:** *"el pool, cautela, con el pool, no hay inocencia allí. La
inocencia de hoy, 'el pool no decide qué entra y qué no', sigue siendo responsable
de la confusión dentro de un mes."* La lectura *"el pool es `C`"* queda **descartada**.

**Sin resolver.** Si es un **segundo `f` en n1** o **algo que la forma no nombra**,
sigue abierto.

**Lo que NO es entrada del CP0b:** **κ como cuantil de `C`** dentro de n1. Parecía
falla porque el registro decía *"todo κ lo produce el orden de arriba"*, y delamor
corrigió el 13 oct que esa frase era **redacción del registro**, no suya: *"nada es
producido… mucho menos por un orden contiguo"*. Queda como **condición declarada**.

### 2. `NodeExtractor` no tiene ↑k: el hueco está abierto de un lado y tapiado del otro

*Entrada del 13 oct, desde el CP1 de `TASK_node_extractor_regla_v1`. delamor:
**"EXACTO"**.*

*"`NodeExtractor` no tiene ↑k"* ya figuraba como **ejemplo** en la fila del CP0b.
**Lo nuevo es la asimetría**, y está medida:

- **Del lado de la forma, el hueco está abierto.** La instancia del CP1 devuelve
  `ESCALATED · value=None` con `escalate_to=None` — *acá hacía falta decidir, del
  campo no salía, y arriba no habló nadie*. Eso es I5 funcionando: `escalate_to` es
  un **`str`**, el módulo lo **registra y nunca lo llama**, y por eso la duda **queda
  abierta** en vez de resolverse. La regla está construida para **no poder cerrarse
  sobre sí misma**.
- **Del lado del código, está tapiado.** `corpus_service.py:298-303` hace
  `nodes = result["nodes"]` y su **única** rama es `if not nodes: return`. **No hay
  rama para `value=None`.**
- **Y es peor que no tenerla.** `None` es *falsy*, así que esa única rama lo
  **tragaría como `if not nodes`**: *"no decidí"* y *"no hubo nodos"* salen por el
  mismo `return`, sin marca. **Es I2 en el orden del llamador** — la no-decisión
  leída como resultado vacío. Lo mismo que `self._nodes or None` hace una línea más
  arriba con `T`.

**Hoy `_seleccionar` decide igual** —*"afuera"*, o conserva—, y lo decide **sin
tener de dónde**: es el `g` que el código aplica sin declararlo (**F2**). La forma,
aplicada, **no agrega un problema: nombra uno que ya estaba.**

**Dónde está el ↑k que falta.** Existe: es **n2** —los parámetros de extracción— y
arriba **n3**, delamor. Lo que no existe es el **canal**. Es lo mismo que el CP0a
encontró y no conectó: *"n2 no tiene instancia en código… es una persona en un
commit"*, y `save()` no persiste nada suyo. **Un orden que no deja traza tampoco
puede recibir una duda.**

**Sin resolver.**

### 3. La exención del paso 1 deja decidir a la **capacidad** donde el campo calla

*Entrada del 13 oct. Sugerencia de Opus de medir y registrar; delamor: **"si de
acuerdo"**. **Sin resolver.***

El paso 1 tiene una exención: *"si el empate cabe en los lugares libres, no hay
empate que decidir"* → entran todos, `FIELD · tie_fits_free_slots`.

**Pero ahí el campo calla.** `h = 0` es exactamente *"el campo no distingue"*, y por
la regla eso es del **paso 2**: decide la traza. La exención se lo saca y lo entrega
a **`top_k`** —un valor **declarado**, de **n2**—. **La capacidad decide donde el
campo no habla.**

**Medido** (`58f6de4`): el régimen de la exención es el **21 %** de los rebuilds
reconstruidos. Y lo que cambiaría si ahí decidiera la traza (`1fb504e`):

| | |
|---|---|
| rebuilds de régimen (b) | **8** |
| empatados en total | **30**, de los cuales **16 (53 %)** venían de afuera |
| el conjunto **cambia** | **5 de 8** |
| `N` conservando | baja hasta **11** (con `top_k = 20`) |
| los **3** que no cambian | tenían la meseta **entera** ya adentro |

**No es diferencia de forma solamente: cambia la práctica en 5 de 8.**

**Origen de la exención:** `_seleccionar` (`TASK_desempate_seleccion_nodos_v1`), y de
ahí **pasó al engine**. **`criterio_local` no se afecta**: va con `capacity=None`, y
sin capacidad la exención no aplica.

**Si la exención se queda o se va es de delamor: no está decidido.**


## Fuera de este TASK

- `should_rebuild` y `calibrate` como instancias en código: se ven en el CP0, pero no se implementan.
- Elegir ε, P o cualquier valor sin origen: es calibración.
- El signo de Δ, las medias.
