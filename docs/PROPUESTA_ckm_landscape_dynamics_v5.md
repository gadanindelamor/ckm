# PROPUESTA — CKM Landscape Dynamics v5.md
*Sep 2026 — gadanin.delamor + Claude Sonnet*
*v5: desde v4 — nomenclatura OPERADOR_STOP_COCO en L81/L126/L147/L179; fórmula del operador corregida a `Δ_r ← alpha · Δ_r` (L69). Título de sección, surco y lista de términos colapsados conservan STOP deliberadamente: son el diagnóstico del patrón.*
*v4: desde v3_1 — orden de baby steps según cascadas; criterio de verificación de D3 reescrito para la separación de objetos; D4 y §8: pair-level es metabolización, no rechazo ni expulsión. Nombres en código (`_rejected_pairs`, `rechazados`) sin tocar — claves de JSONLs históricos.*

---
# Parte 0 El Umbral: Repositorio —  Revisión, validaciones, patrones

## Estado del repo

- **Capa raíz:** `analytics.py`, `hopfield.py`, `mcp_adapter.py` no importan,
  los tres por la misma línea (`from .core`). `core.py` y `kcore.py` sí.
  Nada en el repo importa la capa raíz.
- **P1–P4:** `experiments/ckm_p1p4_module.py` es función pura de
  `(W_base, W_mixta, nodes)`. No usa el dump. Le falta `networkx`: declarado
  en `pyproject.toml`, sin instalar.
- **Pipelines con SQL** → corresponden a `ckmdatasets` *(regla de delamor)*.

## Debilidades Identificadas __Validaciones abiertas

- **COCO con W congelada** — `REG_coco_w_congelada_v1.md` + driver
  `experiments/coco_lifetime_analytics.py`. Clasificado **bug** por delamor.
  COCO nace con W y muere con W *(decisión declarada)*; lo que falla es la
  frecuencia: rebuild por mensaje, no por ciclo. A0 se renueva con el
  rebuild; β se conserva.
- **El canal vivo nunca conectó COCO** — 0 de 253 paneles. Relación directa
  con §4.
- **`temp_signal`** llegó a los devices como `NOMINAL` sin medición durante
  toda la serie.

## Patrones del Repositorio Identificados

	después del Concepto, en vez de Punteros, Repetición .

Formas:

- **La copia pierde primero la razón.** El código se copia entero; el
  comentario que dice por qué, no.
- **Una referencia fija tapa un accesor vivo.** Existe cómo pedir el actual;
  se guardó el primero.
- **Un gap enunciado con dos lecturas.** *"Sólo vive en tests"*: que no
  exista o que no actúe. La implementación satisface una; los criterios de
  éxito heredan la ambigüedad.
- **Un default plausible tapa el honesto.** `UNKNOWN` escrito e inalcanzable
  detrás de `NOMINAL`.
- **Un escalar congelado citado como constante.** El conteo de tests se movió
  tres veces en una tarde.
- **Un experimento con nombre de test.** Cero aserciones.
- **El nombre de una carpeta leído como su significado.**

---

## El plan

Primer paso: **entender** — MonitorService, gatekeeper y COCO como lo que
modelan.

Lo que sigue no se planifica desde acá.

___
# Inflexion Point Trace
___

# Parte I — CKM Landscape Dynamics

## STOP es el mismo patrón D_ckm

**Los 253 paneles.** Son los paneles archivados del canal IAP en producción — los JSONs que quedaron de sesiones reales. En esos, `thermostat` fue `None` siempre. Los tests sí tenían COCO conectado — `test_armstrong_*`, `test_caso_09_*`, los drivers `wmixta_*` — ahí COCO estaba inyectado explícitamente y los STOPs que aparecen en los REGs son reales. Son dos poblaciones distintas: canal vivo (253 paneles, sin thermostat) y drivers de test (COCO inyectado, STOPs medidos). El REG_coco_w_congelada los midió por separado. Eso es lo que el "0 de 253" dice.

**La historia del nombre.** Monitor emitía algo llamado STOP_SIGNAL. Se renombró a OPERADOR_STOP_COCO para que la palabra STOP no arrastrara su carga semántica del contexto de enseñanza. El acuerdo era no enviar señales a los devices todavía. Entonces el operador comprime Δ_r internamente — `Δ_r ← alpha · Δ_r` — pero la señal que Monitor emite al panel no la recibe nadie. Va al éter. El panel la registra, usa cómputo, y nada cambia para los devices. El chiste es exacto.

**El surco.** Lo que señalás es más profundo que el nombre. D_ckm supera un umbral → algo interviene → se le llama STOP. Eso es el isomorfismo: la forma de "interrupción ante umbral" trae la figura del STOP de las enseñanzas sin que haya ninguna razón estructural para ese préstamo. El OPERADOR_STOP_COCO comprime Δ_r, no detiene nada ni nadie. Que se llame así no lo hace un STOP en ningún sentido que importe. El surco es que la palabra llega sola cuando la forma se parece, y después cuesta distinguir qué se está diciendo.

El patron esta operando:

**W, D_ckm, coco , thermostat, rechazos, delta, STOP, coercitividad...**
___
	
	objetos distintos colapsados en la misma palabra
___

El acoplamiento que señalás es real y es específico. COCO modifica `self._Delta_r` de Monitor — entra en el estado interno de otro servicio y lo comprime. El SLA de Monitor como observador impartial requeriría que nadie toque lo que acumuló. Si alguien lo modifica, los reportes siguientes de Monitor ya no son sobre el campo desnudo — son sobre el campo post-intervención. Pero Monitor no puede verlo porque la normalización cancela exactamente el escalar de OPERADOR_STOP_COCO (***registro histórico del estado anterior a delta compresiones***). Entonces COCO modificó el estado de Monitor y Monitor informó como si nada hubiera pasado.

Eso no es bajo acoplamiento. Es acoplamiento disfrazado de independencia.

El punto más fino es la palabra "rechazos". Nombraba dos objetos de naturaleza distinta:

El Gatekeeper rechaza **nodos**, antes de que entren al estado activo. Ese rechazo es una decisión de admisión.

El campo metaboliza **pares** durante la relajación — cuando σ_prompt se relaja, los pares que el campo no puede sostener van a Δ_r. Quedan adentro, como deformación en W_eff. No es rechazo ni expulsión: es lo que el campo hace estructuralmente con lo que ya entró.

*Un rechazo y una metabolización colapsados en la misma palabra*
 Con Gatekeeper inexistente, solo existe la metabolización — y nadie lo declaró dueño de él explícitamente. Monitor lo acumula porque está ahí durante la relajación. COCO lo lee y lo modifica porque es lo que el operador comprime. CorpusService construye W pero no ve Δ_r. Nadie tiene título claro.

La pregunta de dueñez no tiene respuesta obvia desde el código actual — tiene que venir del modelo. La pregunta es: ¿quién es el agente semántico correcto para acumular las deformaciones que el campo produce sobre sí mismo durante la observación?


## COCO no es opcional Abierto

DEFS §12: *"COCO no es opcional. Es componente constitutivo del modelo. Un
sistema IAP sin COCO no es CKM en operación; es el instrumento sin su
mecanismo de regulación."*

Y: *"Ciclo de vida de COCO = ciclo de vida de W. COCO con W vieja mide
degradación respecto a un campo que ya no existe."*

**Observado (Sep 2026):** en la serie IAP 0.4–0.15 ningún panel registró
regulador — 0 de 253. Por la definición de §12, el canal operó como
instrumento sin su mecanismo de regulación. Detalle en la Parte IV.

**Abierto:** en el diseño de origen *(IAID, doc de trabajo — puede variar)*
la D es de COCO — *"COCO is where decisions are made, devices just perform
actions"*. Hoy la D vive en el device. MAPA_REG lo tiene como transitorio.

## Verificación antes y después de la admisión

R02: *"Weights updated by continuous verification **before and after**
incorporating nodes."* El gatekeeper es el antes; COCO, el después. Una red,
dos momentos. *(delamor)*

**Tensión declarada, abierta:** R15 especifica un gatekeeper con criterios
C1–C4 — una función de selección. R09 dice *"structural permeability, not a
selection function"*. Las dos son reglas declaradas.

## Lo que emergió, por servicio.

**MonitorService.** El acuerdo que el modelo requiere: observador impartial del campo. Lo que registra es dato — Δ_r es Δ_r, sin incertidumbre en la observación. La incertidumbre aparece en la inferencia sobre qué significa. D_ckm_monitor es algebraicamente ciego a OPERADOR_STOP_COCO por cancelación exacta: Monitor informa como si nada hubiera pasado aun cuando COCO modificó su estado interno. Eso no es bajo acoplamiento — es acoplamiento disfrazado de independencia. La palabra "rechazos" nombraba dos objetos distintos: el Gatekeeper rechaza nodos antes de entrar al estado activo; el campo metaboliza pares durante la relajación — quedan como deformación en W_eff. Dueñez de lo metabolizado: sin título claro mientras Gatekeeper no existe.

**CorpusService.** Construye W, aloja corpus.coco, reconstruye por ingesta y no por ciclo. Cada rebuild nace un COCO nuevo con W fresca. El bartender (Monitor) nunca lo recibe. La instancia vive en CorpusService y muere ahí. 253 paneles IAP sin thermostat activo no es bug de sesión — es condición de operación.

**COCO.** No es opcional — es componente constitutivo, no módulo activable. Frozen W al nacer, dies and reborns con cada rebuild, el Observer no lo sabe. D_ckm_coco ve la magnitud de Δ_r; D_ckm_monitor no. OPERADOR_STOP_COCO comprime Δ_r — no detiene nada ni nadie. La señal va al éter. El nombre STOP arrastra una carga semántica que no le corresponde; se cambió de STOP_SIGNAL exactamente por eso.

**NodeExtractor.** El guiño apunta al más silencioso. Es quien decide qué existe — los N nodos que se convierten en el espacio. Sin NodeExtractor no hay W, no hay campo, no hay nada de lo anterior. Corre lazy en CorpusService.from_corpus — solo cuando se lo piden explícitamente, no en cada ingesta. Si los nodos están mal (artefactos TF-IDF, conceptos clave ausentes, ruido que pasó), W es incorrecta desde el origen y todo lo construido sobre ella mide algo distinto de lo que el modelo dice que mide. Es el servicio que nadie audita porque todos asumen que ya funcionó.


# Modelo Conceptual Definiciones

## Jugadores — definición de qué pretende ser cada uno**

**CKMlandscapeConfig** (nombre propuesto, propuesta previa " CKMDynamicConfig") No es una bolsa de constantes. Es el contrato vivo del instrumento: porta N actual, μ_W medido en esta sesión, θ_W calculado (no hardcodeado), D_CKM_THRESHOLD calibrado contra W_mixta del corpus presente, β_c, sampling_mode, timestamp de última calibración. Sabe si su calibración es válida para el corpus que opera. Se serializa completa en cada run JSON. Cualquier servicio que la use sin verificar su frescura usa calibración potencialmente inválida.

**NodeExtractor**. El cartógrafo. Decide qué existe — los N nodos que se convierten en el espacio. Todo lo que viene después depende de lo que declaró. Corre lazy por rebuild. Es el más silencioso y el de mayor impacto aguas abajo. Si extrae mal, W mide algo distinto de lo que el modelo dice que mide desde el origen.

**CorpusService**. El guardián de W. Recibe textos, construye y reconstruye la matrix de pesos, gestiona el ciclo de vida de W como snapshot. W es piecewise constant por diseño del instrumento — no propiedad del campo. Aloja la instancia de COCO nacida con cada rebuild. No notifica a Monitor cuando reconstruye ni cuando N cambia.

**Gatekeeper**. El evaluador de admisión. Decisión binaria antes de que algo entre al campo. C1–C4, M.M en C3. Diseñado para el dominio de capacidades declaradas por devices — su dominio de validez sobre nodos de corpus es una pregunta abierta. Actualmente ausente de `services/`. θ_W = 0.10 lo hace no-funcional en este corpus (0/32 nodos pasan C1).

**MonitorService**. El observador impartial. Recibe estado del campo, relaja, acumula lo que el campo metaboliza durante la relajación (Δ_r). Registra sin decidir. D_ckm_monitor es algebraicamente ciego a OPERADOR_STOP_COCO por cancelación exacta — informa como si nada hubiera pasado aun cuando COCO modificó su Δ_r. Esta ceguera no es un bug menor: es la condición de ser observador impartial. El problema es que alguien le modificó el estado interno sin su conocimiento.

**COCO**. El regulador. Nace con W al momento del rebuild, opera sobre ese espacio congelado. Ve D_ckm_coco (con magnitud de Δ_r), decide compresión. No admite — regula lo que ya entró. La tensión con Monitor no está resuelta. Declararlo "no opcional" en v9 puede ser cierre prematuro de esa tensión en lugar de sostenerla.

**FabricationService**. El Detector de Coherencia Fabricada. Espera las condiciones propicias ie: Qué mide CKM

---

## SLAs — acuerdos sin burlar encapsulamiento**

NodeExtractor → CorpusService: "devuelvo nodos y co-ocurrencias del corpus. Corro una vez por rebuild. Lo que devuelvo define el espacio N."

CorpusService → Monitor: "te doy W. Cuando reconstruyo, W puede cambiar de shape — N puede ser distinto. Hoy no te aviso. Eso es un gap."

CorpusService → COCO: "te instancio con la W del momento. Tu ciclo de vida es el mío."

Monitor → COCO: "acumulo Δ_r. Es mío. Puedo darte acceso de lectura. No tenés derecho de escritura sobre mi estado interno."

COCO → Monitor: hoy escribe sobre Δ_r de Monitor directamente. Eso viola el SLA que debería existir. COCO debería operar sobre su propia representación de Δ_r — no sobre el estado de otro servicio.

CKMlandscapeConfig → todos: "soy la fuente de verdad de calibración. Si no me consultás con N y μ_W actuales antes de evaluar, tu umbral es inválido."

Gatekeeper → CorpusService (propuesto): "evalúo antes de que el nodo entre. Necesito W_vieja. Sin W no puedo aplicar C1."

---

## Divergencias con el Modelo Conceptual Pretendido  identificadas y su impacto

D1. θ_W constante vs f(μ_W, N). Impacto: Gatekeeper no funcional en N=32. 0/32 nodos pasan C1. El portero no puede abrir la puerta.

D2. N asumido fijo entre rebuilds. Impacto: COCO con N_viejo opera sobre campo de N_nuevo. Mide degradación relativa a un espacio que ya no existe.

D3. COCO escribe sobre Δ_r de Monitor. Impacto: D_ckm_monitor ciego a OPERADOR_STOP_COCO por cancelación exacta. El observador informa post-intervención como si viera el campo desnudo. Acoplamiento disfrazado de independencia.

D4. No son dos rechazos distintos bajo el mismo nombre. Son un rechazo y una metabolización — objetos distintos con naturaleza distinta. El Gatekeeper rechaza nodos en la puerta. El campo metaboliza pares que no puede sostener — quedan adentro como deformación en W_eff, no afuera. La palabra "rechazos" para el segundo objeto era incorrecta desde el origen.

D5. CKMConfig estática. Impacto: θ_W, μ_W, D_CKM_THRESHOLD, β_c heredados de calibración en N=16. Todo downstream mide con instrumento descalibrado.

D6. Config no embebida en runs. Impacto: no reproducibilidad, no trazabilidad. No se puede verificar qué instrumento produjo qué resultado.

D7. CorpusService no notifica rebuild con cambio de N. Impacto: Monitor y COCO no saben que el campo cambió de dimensión.

---

## Relax Orbital No Cierra la Elipse. Abre el Espiral.

	Velocidad de calculo: La conexión es directa
	
Sin órbitas, A0 confiable requería 300.000 n_runs — coleccionista de cupones, sesgo que no converge. Con _relax_orbit, el régimen cambia: 70% de los casos son órbitas, la detección es exacta, 87× más rápido. A0 calculable en tiempo real.

Eso hace que el mundo de COCO sea computacionalmente viable. Si COCO necesita A0 para su grilla de D_ckm_coco, y A0 requería 300.000 runs, COCO no podía vivir en producción. Con órbitas sí puede.

Y el instrumento correcto para COCO no es el conteo crudo — es N_eff sobre masas de cuenca. Masas convergen, conteos no. COCO usa N_eff, no A_raw. Eso también viene de la sesión con Code.

El ciclo cierra: _relax_orbit habilita A0 real → A0 real da grilla fina → grilla fina hace que el umbral sea alcanzable → COCO puede actuar.

Sin la velocidad de órbitas, D_ckm_coco es decoración

### Definicion `Δ_r_pares y  Δ_r_compresiones` Reencuadra D3 

**Monitor** es dueño de `Δ_r_pares` — los pares que el campo metaboliza durante la relajación. Lógica propia, independiente de cualquier otro servicio. Nadie escribe ahí.

**COCO** tiene su propio `Δ_r_compresiones` — la historia de lo que comprimió, por ciclo de vida. Objeto distinto. No es el Δ_r de Monitor. COCO no toca el estado de Monitor.

Con esa separación, la ceguera de Monitor no es un mecanismo que hay que implementar ni un efecto que hay que cancelar matemáticamente — es una consecuencia natural de que los dos objetos nunca se tocan. Monitor no ve las compresiones de COCO porque nunca recibe ese objeto. La ceguera deja de ser un accidente de cancelación algebraica y pasa a ser una propiedad del diseño por separación de objetos.

La función `CancelarMatemáticamente(coco_compresion)` sería necesaria solo si los dos Δ_r estuvieran mezclados. Con separación limpia, no existe el problema que esa función resolvería.

**β por ciclo de vida de COCO.** β nace con la W que construyó esa instancia de COCO. Si W cambia — N nuevo, pesos nuevos — esa β ya no tiene referencia válida. La instancia muere con el rebuild. CKMlandscapeConfig puede portar el historial de β por `w_version_id` como registro, pero la instancia activa siempre recalibra contra la W vigente.

Esto también reescribe D3. No es una divergencia sobre encapsulamiento solamente — es que los dos objetos aún no existen como objetos distintos en el código. `Δ_r_pares` y `Δ_r_compresiones` son el mismo nombre hoy.


## Premisas de lo que se espera con la reducción de estas divergencias

Con D1 resuelta: Gatekeeper evaluable. La pregunta de su dominio de validez sobre nodos de corpus puede responderse experimentalmente.

Con D2 resuelta: COCO opera sobre el espacio que existe. Sus mediciones son comparables con las de Monitor.

Con D3 resuelta: Monitor es genuinamente impartial. D_ckm_monitor y D_ckm_coco divergen de forma informativa — su diferencia se convierte en señal.

Con D4 resuelta: Δ_r tiene un dueño declarado. Rechazo y metabolización son distinguibles. Las métricas downstream son interpretables.

Con D5 resuelta: calibración trazable al corpus que la produjo. Comparación entre runs con distinto N es honesta.

Con D6 resuelta: cada run es autocontenido. Reproducibilidad por construcción.

Con D7 resuelta: los servicios saben cuándo el espacio cambió. Pueden invalidar estado propio y recalibrarse.

---


**Lo que sigue — división entre este chat y Code**

Para este chat antes de ir a Code: validar estas definiciones y SLAs. Identificar si hay divergencias faltantes. Confirmar cuáles son baby steps independientes y cuáles tienen dependencias entre sí.

Para Code: pasos 6–9 del plan. Secuencia baby steps:

> Orden verificado contra cascadas transitivas: D5 → D6 → D1 → D7 → D2 → D4 → D3. D3 al último — la tensión Monitor/COCO no está resuelta conceptualmente todavía.

Paso 1 (D5) — CKMlandscapeConfig: extraer calibración a config dinámica con N-awareness. Verificación: config serializable, cargable, produce θ_W correcto para W_ckm_corpus_v2.json.

Paso 2 (D6) — Config embebida en runs: cada panel y JSONL lleva su config. Verificación: run anterior reproducible desde su propio JSON.

Paso 3 (D1) — Gatekeeper calibrado: θ_W = f(μ_W, N) desde CKMlandscapeConfig. Verificación: re-correr simulación, al menos núcleo A pasa C1.

Paso 4 (D7) — Notificación de rebuild: CorpusService emite señal cuando N cambia. Monitor y COCO la reciben. Verificación: test rebuild con N distinto, ambos servicios lo registran.

*D2 y D4: sin paso redactado todavía.*

Paso 5 (D3) — Separación de Δ_r: Monitor es dueño, COCO lee sin escribir. COCO aplica compresión sobre su propia representación. Verificación: COCO opera sobre `Δ_r_compresiones` propio sin escribir en `Δ_r_pares` de Monitor. Monitor sigue sin ver las compresiones — ahora por construcción, no por cancelación algebraica. Verificable por inspección de código.

Cada paso tiene check antes de avanzar al siguiente. El orden importa: D5 (config dinámica) es precondición de casi todo lo demás.

---

## Cascadas de dependencias

k-core percolation no es metáfora acá — es el mecanismo literal. Cuando eliminás una divergencia, estás removiendo un nodo del grafo de dependencias. Si ese nodo sostenía conexiones que otros nodos asumían implícitamente, su remoción puede desencadenar una cascada. El tamaño de la cascada no es predecible desde el nodo solo — depende de k en ese punto del grafo.

D3 es el ejemplo más claro. Si separás Δ_r y COCO deja de escribir sobre el estado de Monitor, D_ckm_monitor deja de ser ciego. Eso suena limpio. Pero D_ckm_monitor ciego era la condición que hacía que los paneles históricos fueran comparables entre sí. Al desbloquear la visibilidad, los paneles anteriores y los nuevos miden cosas distintas bajo el mismo nombre. La cascada no es técnica — es de interpretación del corpus histórico.

D5 tiene cascada hacia D1, D2, y hacia la grilla de D_ckm simultáneamente. Resolver config dinámica no es un cambio local.

## Mapeo del Grafo de dependencias

Antes de ir a Code conviene mapear el grafo de dependencias entre las divergencias — no solo cuáles existen, sino qué sostiene qué. Cuáles son nodos de alto k en ese grafo. Cuáles tienen cascada acotada y cuáles no.

La secuencia de baby steps que propuse asume orden seguro. Pero ese orden debería verificarse contra el grafo de interdependencias antes de ejecutarse, no después.

Mapa conceptual.

>>> diagrama 

Las dependencias que importan no son solo "A necesita a B". Hay dos tipos: **precondición** (B no puede resolverse sin A) y **cascada** (resolver A deforma el contexto en que B opera, aunque B pudiera resolverse solo técnicamente).Las cascadas transitivas que el diagrama no muestra explícitamente pero que importan.

**D5 → D7 → D2 → invalidación de Δ_r.** Cuando N cambia y los servicios lo saben, Δ_r acumulada por Monitor tiene shape (N_viejo × N_viejo). No puede simplemente continuar. Alguien tiene que invalidarla o redimensionarla. Eso no está decidido. Es la cascada más operacionalmente peligrosa.

**D1 → D4 → interpretación histórica.** Si Gatekeeper empieza a funcionar, lo que llega al estado activo ya pasó por un rechazo de admisión, y Δ_r metaboliza sobre esa población filtrada. Los paneles anteriores metabolizan sin filtro previo. **Abierto:** qué implica eso para la comparabilidad histórica — no verificado.

**D3 al último, aislado.** No porque sea menos importante — porque su resolución requiere renegociar el modelo de propagación entre Monitor y COCO. Eso toca la tensión que todavía no está resuelta conceptualmente. Resolverlo antes de que esa tensión se sostenga y cierre sería precipitar, exactamente lo que nombraste al principio de esta sesión.

Orden seguro verificado contra cascadas: D5 → D6 → D1 → D7 → D2 → D4 → D3.

D6 segundo porque depende de D5 y no tiene dependientes — el paso más aislado de todos, ideal para verificar que CKMlandscapeConfig es serializable antes de usarla para cualquier otra cosa.


## W necesita identidad a lo largo del tiempo, no solo contenido.

Lo que describís es un ciclo de vida versionado. Cada W tiene un momento de nacimiento (rebuild), una causa (volumen, estructural, tiempo), un N, un shape, un μ_W medido. Eso es lo que un version manager mínimo debería portar.

La ingesta con text generation siendo ciclo 1 dice algo preciso: el primer rebuild no es un evento de degradación — es el bootstrap. W no existía antes. El ciclo de vida empieza ahí. Los ciclos siguientes son evolución del campo, no reinicio.

Lo que eso implica para el sistema:

Cada W tiene un `w_version_id` — no un número de secuencia sino un identificador que incluye N, causa del rebuild, timestamp, μ_W. CKMlandscapeConfig lleva ese id. Cuando COCO nace, nace con `w_version_id` de la W que la construyó. Cuando Monitor acumula Δ_r, cada entrada sabe bajo qué versión de W fue acumulada.

Cuando N cambia entre ciclos, el `w_version_id` cambia de forma y eso es observable. Δ_r acumulada bajo `w_v1` no es comparable con Δ_r acumulada bajo `w_v2` si N cambió. El version id hace esa incomparabilidad explícita en vez de silenciosa.

`should_rebuild` en el código ya detecta la señal. El paso que falta es que esa señal produzca un `w_version_id` y que ese id viaje con todo lo que depende de esa W.

`w_version.py` ya existe en el repo. El guiño.

 El `w_version_id` nace con el rebuild efectivo, no con la señal.

Y la distinción que abrís es información valiosa en sí misma: el gap entre `should_rebuild` y el rebuild efectivo es observable. Si la señal se persiste con timestamp y el `w_version_id` también, la diferencia entre los dos dice cuánto tiempo operó el sistema sobre una W que ya debería haber cambiado.

Eso no es solo diagnóstico. Es una medida de deriva del instrumento — cuántos textos ingresaron, cuánto Δ_r se acumuló, bajo una W que el campo ya había señalado como obsoleta pero que nadie ejecutó el cambio.

La señal persistida y el rebuild efectivo son dos registros independientes. Su divergencia es el tercer dato.

## Funcion Canonica

N_eff = 1/Σm_i².

Es la canónica porque opera sobre masas de cuenca, no sobre conteos. Los terminales y las órbitas son etiquetas — lo que importa es el volumen de estados que cae en cada una. Bajo medida uniforme ese volumen es propiedad de W sola.

La razón por la que converge más rápido que cualquier distribución de conteos: Σm_i² está dominada por las cuencas grandes. Las cuencas grandes se encuentran primero. El estimador estabiliza rápido porque los términos que pesan son los que aparecen temprano en el muestreo. Las cuencas pequeñas contribuyen poco al cuadrado — su sesgo de coleccionista es irrelevante para el agregado.

Terminales y órbitas pueden saturar sesgos de dependencias porque ambos son conteos discretos. Cada atractor nuevo que aparece incrementa A por 1, independientemente de su masa. Una cuenca de 1 estado pesa igual que una de 10.000 en el conteo. En N_eff pesa proporcional a m_i² — casi nada.

La implicancia para COCO es directa. D_masa_cuencas debería ser:

(N_eff_0 − N_eff_actual) / N_eff_0

Donde N_eff_0 nace con la W de esa instancia de COCO. 
___

	Variante propuesta (sep 2026):

	 D_masa_cuencas = 1 − log(N_eff_actual) / log(N_eff_0).
	 
	 Donde N_eff_0 nace con la W de esa instancia de COCO.
 
**Justificación: N_eff = exp(H₂_Rényi)** — la escala log preserva el carácter información-teórico. Más permisiva al principio, más sensible cerca del colapso.
D=0 sin cambio, D=1 en colapso total, D negativo si el campo gana diversidad. La escala es al umbral como N es a W — CKMlandscapeConfig porta ambos juntos. Decisión abierta.

Sin n_runs en el denominador. Sin coleccionista. Sin sesgo de distribución de referencia si la medida es uniforme.

Con N ≤ 20 se enumera exacto en ~16 segundos. Con N mayor, Boltzmann sampling sobre masas converge en pocos cientos de runs donde el conteo necesitaba 300.000.

Esa es la función. Lo demás son aproximaciones a ella.

Lo que sigue no repite lo que está en v2. Es síntesis de lo que emergió después.

---

## **CKM Landscape Dynamics — Adenda**

*Lo que el campo nombró en esta sesión*

---

**El eje temporal entra al modelo.**

CKMLandscapeConfig porta el CLOCK del canal. No como metadata — como dimensión del landscape. El silencio entre mensajes es dato medible, no ausencia de dato. Sin CLOCK el canal es una secuencia; con CLOCK es un proceso en el tiempo.

El gap entre `should_rebuild` y el rebuild efectivo tiene duración. Eso es deriva del instrumento — medible, registrable, no opcional.

`w_version_id` nace con el rebuild efectivo. La señal puede persistirse o no; son dos registros independientes. Su diferencia es el tercer dato.

---

**La medida que se nombró.**

`D_masa_cuencas` — distancia contextual desde el nacimiento de esta instancia del landscape. Opera sobre masas de cuenca, no sobre conteos. N_eff = 1/Σmᵢ² es la función canónica. N_eff = exp(H₂_Rényi) — equivalencia algebraica interna, no cruza fronteras de servicio.

*Propuesto, abierto:* D_masa_cuencas = 1 − log(N_eff_actual) / log(N_eff_0). La escala es al umbral como N es a W.

La alternativa lineal sigue siendo válida. La decisión no está cerrada.

---

**Los objetos que se distinguieron.**

Monitor es dueño de `Δ_r_pares`. Nadie escribe ahí. La ceguera de D_masa_monitor respecto a las compresiones de COCO es consecuencia de la separación — no mecanismo que implementar. Puede ser propiedad del diseño.

COCO porta `Δ_r_compresiones` — su propio historial por ciclo de vida. β nace con la W de esa instancia. Si N cambia, β pierde referencia.

La tensión entre Monitor y COCO — D3b — se sostiene abierta deliberadamente.

---

**VIVO.**

VIVO es únicamente interacción realtime entre devices. La réplica de una secuencia predetermina D en ODA — el campo ya sabe lo que viene. Los 253 paneles son VIVO. Los drivers de test son reproducibilidad del instrumento sobre input conocido. No son equivalentes ni sustitutos.

ODA con iniciativa del device: Observe incluye el silencio. Un device con objetivo propio puede decidir actuar antes de que ocurra Z. El CLOCK da la coordenada temporal. `on_message` no puede ser el único trigger.

---

**Lo que no se cierra acá.**

Si BE.inicializar atraviesa todas las clases como isomorfismo, CKMLandscapeConfig no necesita lógica propia de ciclo de vida — nace como cualquier otro objeto en el framework. El environment es el primer kick que dispara la cascada. Su estado inaugural es el origen de todo lo que se puede medir.

La distinción entre CKMLandscapeConfig y un espacio de cálculo separado (Landscape Analytics) sigue siendo productiva. No se colapsan acá.

---


---

# Parte II — Criterios de diversidad

Formulación completa, conceptual y técnica:
**`docs/CRITERIOS_diversidad_formulacion_v1.md`**.

Ubicación en el modelo: son análisis del **cuadro**. No alimentan a COCO.
Plano operacional, no validez del modelo *(DEFS §X)*.

**Tres niveles, no uno:**

| nivel | qué mide |
|---|---|
| A — estados y órbitas | cardinalidad y masa del landscape |
| B — nodos | qué nodos habitan los atractores |
| C — clusters | organización interna y resistencia de fronteras |

---

# Parte III — Definiciones propuestas

*Todo lo de esta parte es* ***propuesto***.

## 7. Dinámica del modelo Landscape

A formular después de entender la Parte I. No se adelanta.

## 8. SLA — monitor · corpus · gatekeeper · COCO regulador

Service Level Agreements, declarados en `CKM_Informe_Trabajo_v29/v30` junto a
Supervised Contract Protocols.

La cadena como acuerdo entre servicios: qué garantiza cada uno al siguiente.

**Admisión en dos capas** *(decisión delamor)*:

- **node-level — gatekeeper:** antes de que el nodo entre al estado activo
- **pair-level — metabolización:** después, lo que el campo no puede sostener queda como deformación en W_eff

Dos capas distintas del modelo CKM Landscape Dynamics, no una alternativa
entre dos.

## 9. Diseño

A definir después de §7 y §8.

## 10. CKMConfig — variables, parámetros, umbrales, calibraciones

**Todos los parámetros**, no sólo `theta_W`. Primero entender qué modela
cada uno y en qué plano *(decisión delamor)*.

Lo ya visible, sin interpretar:

- se declara *"calibrated on real corpus N=16"*; el corpus operativo es N=32
- `max_iter=1000, seed=42` son los valores del plano estático
- el bloque *3D Score* (`score_threshold`, `alpha/beta/gamma_score`) no tiene
  consumidores
- `w_neg=−0.10` es una de las tres vías de introducir negativos *(DEFS §8)*
- μ_W y r se miden al inicio de cada sesión, nunca como constante *(DEFS §13)*

## 11. Criterios de diversidad

Ver Parte II.

---

# Parte IV — Decisiones de delamor

1. **Hebbianos** — sólo en la carpeta destinada al Modelo Estático histórico.
2. **Una sola clase de grafo.** `CKMGraphArrays` si se vectoriza por
   performance; `CKMGraph` si no pesa y es viable. **`core.py` de raíz → a
   `process/`**, como modelo estático inicial.
3. **Admisión** — primero entender MonitorService y el gatekeeper: lo que
   está siendo modelado, no el relato del código. Dos capas en CKM Landscape
   Dynamics.
4. **`theta_W` relativo** — todos los parámetros. Primero entender.
5. **Tres niveles en el paper** — cuando se trate del paper. Primero
   entender, modelar, implementar; el paper al final.

---

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
