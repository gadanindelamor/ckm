# NOTA_orden_tasks_06oct_v1

*6 oct 2026. Pregunta de delamor: "¿en qué orden serían? ¿Podemos armar algo conjunto? Tal vez se pueda hacer en paralelo, no sé." Redacta Claude Opus 5.5 (Cowork). Leído contra `eddb4b0` y el árbol sin commitear.*
*Es una nota y no una TASK. El orden es una propuesta; lo que decide delamor está marcado **[delamor]**.*

---

## 1. Las cinco piezas y su estado

| # | pieza | estado leído en el repo |
|---|---|---|
| 1 | **LandscapeConfig: get / set** | Hoy está en v1 (`dataclass(frozen=True)`). Monitor la recibe y la serializa en cada panel (D6, `6606b7c`), pero **no toma de ella** n_runs, θ_W ni nada más (get: no). **`TASK_CKMlandscapeConfig_v2` ya existe** (`cc690db`) y no está ejecutada. Propone ciclos `c_0…c_k`, con **I2: "Ciclo vigente único… ningún servicio detecta el cambio de ciclo por su cuenta"** e **I6: t_señal / t_rebuild / deriva**. Le faltan dos decisiones de delamor (§"A decidir antes de ejecutar"). |
| 2 | **Monitor + COCO, un solo ciclo de vida** | `TASK_monitor_coco_ciclo_orbita_v1` (5 oct). El hallazgo que la motiva, los 56 negativos, es **el mismo** que motivó la Config v2. Las dos TASKs piden lo mismo desde lados distintos. |
| 3 | **D_ckm / D_masa_cuencas** | **Cerrado en lo que hacen.** `dabd1ed` (5 oct): `d_ckm` delega en `d_masa_cuencas` = 1 − ln N_eff / ln N_eff0. El panel lleva **el mismo número** en las dos claves, y la forma lineal quedó como `deprecated_d_ckm`. Ver `registers/REG_d_ckm_formula_canonica_v1.md`. **Queda abierto (lo dice el REG):** los umbrales de COCO no se recalibraron sobre la escala nueva (`coco.py` L17–18: D_CKM_THRESHOLD = 0.40 y FRAC_REC_MIN = 0.60 vienen de la forma lineal). También está el vacío disfrazado (None → "stable"), que ya figura en el CP0 de la #2. |
| 4 | **Calibración por caso** | No hay TASK. Los umbrales están en `coco.py` L93–109 (D_CKM_THRESHOLD, ALPHA_*, FRAC_REC_MIN, BETA_*), y θ_W, n_runs y sampling_mode llegan sueltos. |
| 5 | **Canal IAP: CLOCK + ODA continuo** | `TASK_canal_iap_clock_iniciativa_v1` (6 oct). |

## 2. Lo que aparece al ponerlas juntas

- **get = Config v2 con I2.** Cuando Monitor y COCO **leen** su ciclo de la config, el ciclo de vida común (#2) deja de ser un acuerdo entre dos servicios y pasa a ser una sola fuente. "Monitor y COCO, aspectos de lo mismo": lo mismo sería el ciclo vigente.
- **set = calibración.** Lo que la Config v2 llama **declarado** (θ_W, scale, sampling_mode, y si se agregan, los umbrales de COCO y n_runs) es justo lo que se calibra por caso (#4). Calibrar un caso es declarar su config. *Esto es una lectura, no una decisión.*
- **CLOCK.** La adenda v5 pone el CLOCK en la config. La Config v2 ya trae el tiempo de W (I6: t_señal, t_rebuild, deriva). El CLOCK del canal (#5) es otro tiempo: ticks del canal y no ciclos de W. **[delamor]** ¿Viven en el mismo objeto?
- **Calibrar antes de #2 no sirve.** Mientras haya dos COCO con dos baselines y Δ_r escrito desde una sola fase, cualquier umbral se ajusta sobre una medida rota ("no hay métricas si no es así").

## 3. Orden propuesto

```
Carril A (services/)                     Carril B (iap_chatroom/)
────────────────────                     ────────────────────────
0. CP0 de #1, #2, #5 — solo lectura, los tres a la vez
   │                                        │
1. Config v2: decisiones [delamor]          5.CP1  CLOCK del canal
   + ejecución (get)                        5.CP2  ODA continuo
   │                                        │
2. Monitor+COCO: CP1 (medir) ─ puede ir     │
   en paralelo con 1; CP2 usa el            │
   ciclo vigente de 1                       │
   │                                        │
   CP3 [delamor] → CP4                      │
   │                                        │
4. Calibración por caso (set) ──────────►  5.CP3  caso Z (entradas) [delamor]
   incluye umbrales de COCO (#3)            usa lo calibrado si mide con Monitor
```

**En paralelo se puede:**
- los tres CP0, porque son solo lectura;
- el carril B entero hasta su CP3: toca `channel.py`, `mcp_server.py` y `autonomous_device.py`, no `services/`;
- el CP1 de #2 (driver en `experiments/`, sin tocar `services/`) junto con la ejecución de #1.

**En serie, sí o sí:**
- #1 antes del CP2 de #2;
- #2 (hasta su CP4) antes de #4;
- #4 antes del caso Z, si el caso Z se mide con Monitor y COCO.

**Único archivo compartido entre carriles:** `iap_chatroom/ckm_monitor.py`. Lo toca el CP4 de #2 (lee COCO desde Monitor) y el carril B no debería tocarlo. Si dos sesiones de Code trabajan a la vez, conviene que sean dos ramas.

## 4. Lo que decide delamor para arrancar

1. **Config v2 §"A decidir" 1:** ¿v2 reemplaza a v1 o convive con ella?
2. **Config v2 §"A decidir" 2:** ¿quién llama a `abrir_ciclo`? `TASK_monitor_coco_ciclo_orbita_v1` §1 supone que el reloj es el cambio de W visto desde Monitor. Si la respuesta es "Monitor", las dos TASKs encajan sin cambios.
3. **¿El CLOCK del canal va en la config o aparte?** (§2)
4. **¿Una TASK de calibración nueva, o se agrega como CP a la Config v2?**

## 5. Ajustes menores que deja esta nota

- `TASK_monitor_coco_ciclo_orbita_v1`, CP0 punto 6: además de `TASK_landscape_config_en_runs_v1`, debe nombrar `TASK_CKMlandscapeConfig_v2` (I2).
- `TASK_canal_iap_clock_iniciativa_v1`, CP0 punto 2: lo mismo, por I6.

No se hicieron. Esperan el OK.

## 6. Decisiones de delamor (6 oct)

- **El primer paso es LandscapeConfig.** *"Estuve pensando esto y el primer paso es ese."*
- **v2 reemplaza a v1.** *"Si config v2 suma lo que decís a config v1, entonces la reemplaza. Solo v2."*
- **El set es síncrono por ahora.**
- **El get debe ser consistente para todos los players** (los componentes del modelo): *"No dejar un estado del instrumento inconsistente, causado por independencia de accesos, de get concurrentes."*
  - Lectura técnica, a validar en el CP0: el get devuelve **un ciclo entero e inmutable** (I1), no campos sueltos. Así, ningún player puede quedar con la mitad de un ciclo y la mitad del otro. El set (`abrir_ciclo`) reemplaza el ciclo vigente de una sola vez.
- **Monitor abre el ciclo** (llama a `abrir_ciclo`). Encaja con `TASK_monitor_coco_ciclo_orbita_v1` §1 sin cambios.
- ~~**El CLOCK va en la Config**~~ → **corregido más tarde, mismo día (ver §8).**
- **La calibración no es un CP de la Config.** delamor: *"Calibración es un tema… debería ser parte de un proceso más controlado, el de Calibración de CKM."* Ejemplo: hoy `experiments/calibrate_W_mixta.py` es un script suelto.
  - Lo que se leyó del script (`7f08770`): calibra AMP → A0 con el **protocolo viejo** (A0 = cantidad de atractores distintos, N_RUNS = 150, SEED = 42), que hoy es `deprecated_count_attractors`. Sus anclas (AMP 0 → 2, 15 → 5, 40 → 25) están en la escala anterior a `dabd1ed`, igual que los umbrales de COCO. Lo usan `orbit_analytics.py` y varios REG.
  - Relación con la Config: el proceso de Calibración **produce** lo declarado, y la Config lo **porta** (set síncrono). La Config no calibra.

## 7. Corrección al §3: un solo device delamor

delamor: *"Yo soy device delamor. No me multiplico, no trabajo en paralelo ni simultáneo, salvo pensar o funciones autónomas como respirar."*

Los carriles del §3 pueden ser paralelos en el código, pero **cada checkpoint termina en "Alto. Reportar a delamor"**, y ese que recibe es uno solo. Dos carriles a la vez mandarían reportes al mismo tiempo, y eso es un get concurrente sobre delamor: el mismo problema que se le pide resolver a la Config.

**Regla:** los reportes a delamor van **de a uno, en serie**. Un carril puede adelantar trabajo que no requiere decisión (lectura, drivers sin tocar `services/`), pero se detiene en su checkpoint hasta que delamor cierre el anterior. El orden de los reportes sigue el del §3: primero el carril A, después el B.

## 8. El CLOCK, por ahora, en el entorno (provisional)

> **Cautela (delamor):** *"La cautela de no empezar a caer en el mínimo local 'va al entorno'."* Que el clock vaya al entorno es el paso cauto de hoy, **no una cuenca donde quedarse**. Queda abierto. Las TASKs no se reescriben para fijarlo: el CP0 de cada una lo evalúa como pregunta.


delamor: *"Me da la impresión de que el clock es del entorno, que no lo setea Config y tal vez no lo porta."* · *"Si avanzamos con cautela, que vaya al entorno. En todo caso Config solo tendrá get, como para ofrecer el reloj, si fuese requerido."*

- **El clock es del entorno:** del canal en IAP, del driver fuera de IAP. Es el mismo patrón que BE/Pygame, donde el reloj era del loop del entorno y no de los devices. El motivo del §6 (*"usarlo con drivers fuera de IAP"*) se sigue cumpliendo, porque el driver es el entorno.
- **La Config no lo setea.** A lo sumo ofrece un **get** del reloj, solo si algún player lo necesita, y nunca lo escribe.
- **Corrige** a la adenda de `PROPUESTA_ckm_landscape_dynamics_v5.md` (*"CKMLandscapeConfig porta el CLOCK"*) y al §6 de esta nota.

**Sugerencias de Opus que delamor aceptó (1, 3, 4, 5):**
1. El clock tiene **un solo escritor**, el entorno, y no es ningún player. Monitor abre ciclos y el entorno avanza ticks.
3. **Lectura consistente:** `(ciclo_vigente, tick)` se lee junto. Como son dos fuentes (Config y entorno), la lectura la arma el entorno **dentro de su paso**, como un frame.
4. `t_señal` y `t_rebuild` (I6) también se registran **en ticks**, para que la deriva quede en la unidad del campo.
5. **El tick no dispara nada:** es información.

Lo que la sugerencia 2 (fuente inyectable en la Config) proponía, ahora lo resuelve el hecho de que el clock sea del entorno.

**Abierto:** el período del tick en el canal vivo, y si los eventos llevan tick + timestamp de pared o uno solo (Opus: los dos).

**Observación de delamor sobre el §8:** *"Pasar complejidad a un fantasma todopoderoso que resuelve. EL ENTORNO."*

- En el §8, "el entorno" carga con todo: escribir el clock, armar la lectura consistente (sugerencia 3) y ofrecer el tiempo a todos. Es un nombre que no tiene definición, y en cada caso apunta a un objeto distinto: `channel.py` en IAP, el script del driver fuera de IAP.
- Antes de darle responsabilidades, **"entorno" necesita su ficha** (`FICHAS_elementos_ckm`): qué objeto es en cada caso, qué escribe y qué ofrece. Si no, es Babel.
- La sugerencia 3 es el caso más claro de complejidad que se pasa al fantasma: dice *quién* arma la lectura, pero no *cómo*.

**La cadencia del entorno no es neutral.** delamor: *"Pygame, usado como entorno, tiene una cadencia en su estructura que rige el universo de lo que se modele. No digo que sea la única, pero no es menor… FRAMES. Es un juego que renderiza imágenes."*

- En un entorno de frames, lo que ocurre entre dos frames no existe para nadie. El tiempo del universo modelado es el del render.
- En el CKM ya hay cadencias de este tipo: el **paso síncrono** de la relajación (todos a la vez, como un frame), la **paridad de `max_iter=200`**, que elige una cara del período 2 (`TASK_monitor_coco_ciclo_orbita_v1`), y los **rebuilds**. Un período 2 solo se ve con un paso síncrono, así que la cadencia define parte de lo que se puede observar.
- Para la ficha de "entorno": **su cadencia es parte de la ficha.** Hay que declarar qué es un paso en cada entorno (frame, tick del canal, iteración del driver) y qué queda fuera de la observación entre paso y paso.

**Órdenes de paso.** delamor: *"Y hay un orden de pasos: los pasos de relajación de COCO para calcular lo que fuere son parte de un paso de orden siguiente, en escala. Ojo con la ley de 7."*

Escala leída en el código (propuesta, a revisar):

| orden | paso | lo contiene |
|---|---|---|
| 1 | un paso síncrono de relajación (σ → σ') | una relajación completa |
| 2 | una relajación completa (hasta `max_iter` o la órbita) | una evaluación (Monitor) / una muestra (COCO, n_runs) |
| 3 | una evaluación de un texto / una observación de COCO | un paso del entorno (tick, mensaje, iteración del driver) |
| 4 | un paso del entorno | un ciclo de W (entre rebuilds) |
| 5 | un ciclo de W | un run |

- **Ley de 7 (cautela):** el paso de un orden al siguiente no se transmite entero. Hay un intervalo donde el proceso se desvía, salvo que algo lo complete. Hay un caso ya leído en el código: entre el orden 1 y el 2, `max_iter=200` corta en una fase, y **el período 2 se pierde en el pasaje**. Puede que haya otros intervalos así entre los demás órdenes. Para buscarlos, no para suponerlos.
- Para la ficha de "entorno": declarar **en qué orden está su paso**.

**El grano no se transfiere entre órdenes.** delamor: *"El ojo es que el grano del orden Oi, en una escala de 7 donde se duplica la frecuencia de vibración dentro de la escala, no es el grano del Oi−1. Una escala de 7 entra toda en una nota de orden superior."*

- En la tabla, "lo contiene" no significa un paso dentro de otro paso. Significa que **una escala entera del orden inferior entra en una sola nota del orden superior**. Además, dentro de una escala los pasos no son iguales entre sí: la frecuencia cambia de nota a nota.
- Consecuencia: **no medir un orden con el grano de otro.** Contar pasos del Oi−1 no da la medida del Oi.
- **Revisar la sugerencia 4 del §8**, que delamor aceptó: registrar `t_señal` y `t_rebuild` (ciclo de W, orden 4–5) en ticks (orden 3–4) mide un evento con el grano de otro orden. Registrarlo como traza no hace daño; usar la deriva en ticks como medida sí puede hacerlo.
- Lo mismo con `max_iter=200`: un conteo de grano del orden 1 decide lo que ve el orden 2.
- **Precisión (delamor):** *"Respetar la ley de 7, no hay por qué hacerlo a priori. Pero la relación entre órdenes de grano o notas, sea 7 o lo que fuere, existe."* No se impone el 7. Lo que se afirma es que **existe una relación entre los granos de órdenes vecinos**. Cuál es en cada pasaje no se supone: se descubre o se declara.
- delamor: *"La relación es una CO-RELACIÓN de órdenes."* Es el mismo "co" de co-ocurrencia, co-presencia y co-alineamiento (`NOTAS_co_flexion_angular_05oct_v1`), pero esta vez entre órdenes de grano y no entre nodos.

## 9. El plan supone continuidad, y no la hay

delamor: *"No va a funcionar el plan. Intuyo que continúa el cuello de botella. ¿Es grave? Puede serlo. Disponibilidad del device delamor. Eventos impredecibles. El evento de restart del Codespace no es controlable."*

**Tarea (Opus): protocolo de continuidad.** Primeras ideas, a discutir:

1. **El estado vive en el repo, no en la sesión.** Cada TASK lleva un archivo de estado (`ESTADO_<task>.md`) con el último CP cerrado, qué se hizo, qué espera y de quién. Un restart del Codespace no borra nada que importe.
2. **Cada checkpoint deja el repo consistente.** Se commitea al cerrar cada CP, nunca a mitad. Es el mismo principio que el get de la Config: ningún evento, ni restart ni ausencia, deja al instrumento a medias.
3. **Pasos idempotentes.** Correr de nuevo un CP después de un restart da lo mismo, o detecta que ya estaba hecho.
4. **Los reportes no se empujan: se encolan.** Un solo lugar (`docs/tasks/BANDEJA_delamor.md`) donde Code deja cada reporte con su fecha. delamor lee cuando está disponible, de a uno y en orden. Es un get de delamor, no un push sobre delamor.
5. **Decisiones bloqueantes y no bloqueantes.** Cada pregunta a delamor dice si frena el trabajo o no. Lo que no frena sigue con un default declarado y reversible, y queda marcado para revisión.

## 10. Delegación: Opus decide y escala a delamor por encima de un umbral

delamor: *"La tarea es que VOS tomes decisiones, y escales situaciones y decisiones a mí cuando superen un umbral."*

**Umbral propuesto (a confirmar por delamor).** Opus **escala** si se cumple alguno de estos:

- **E1. Toca lo que decidió delamor** o un principio: TRUST, AWARENESS, Orden BABEL, nombres de conceptos, decisiones registradas.
- **E2. Es irreversible o difícil de revertir:** borrar algo, reescribir REG o traza, push al repo público, cambiar la historia.
- **E3. Cambia la semántica del modelo:** qué entra a W, W_eff o Δ_r; definiciones de métricas; valores de calibración o umbrales; premisas, P1–P4, afirmaciones del paper.
- **E4. Está marcado [delamor]** en una TASK.
- **E5. Un resultado contradice algo registrado**, o sorprende tanto que cambiaría el rumbo.
- **E6. Cambia el alcance:** abrir una TASK nueva o abandonar una.

Opus **decide solo**: los detalles de implementación dentro del alcance declarado de una TASK, el orden interno, el detalle de los tests, los nombres internos (no los de conceptos), los defaults reversibles, el análisis de los CP0 y las correcciones de sus propios errores.

**Cada decisión de Opus queda registrada** en `docs/tasks/DECISIONES_opus.md`, con fecha, qué se decidió, por qué y cómo revertirlo. delamor la lee cuando quiere y puede revertir cualquiera.

**Límite real:** Opus no está presente entre sesiones. Decide cuando hay una sesión abierta (o una tarea programada, si se arma). Lo que llega a la bandeja mientras tanto espera a la próxima sesión, no a delamor.

**§9, agregado. El stop del Codespace no se previene: se diseña para que no haga daño.**

delamor: *"La inactividad no es tan simple de medir… no garantiza que no se stopee. En realidad ese es el evento incontrolable, el stop del Codespace. Probamos con scripts que simulen actividad y no logramos embocarle al criterio de stopping."* (antecedente: `tools/keepalive.sh`)

- **Criterio:** no se pelea contra el stop. Se lo trata como un evento que puede llegar en cualquier momento, como un corte de luz. Se diseña para que **pararse en cualquier punto sea inofensivo** (es lo que se llama diseño *crash-only*).
- **Al arrancar, chequeo de consistencia:** locks huérfanos (`.git/index.lock`), `git status`, tests y la última línea de cada log y JSONL.
- **Escritura atómica:** los resultados se escriben primero a un archivo temporal y después se renombran. Así nunca queda un JSONL a medias.
- **CPs chicos y commit al cerrar cada uno:** cuanto más corto es el CP, menos se pierde con un stop.
- **Retención:** un Codespace detenido se borra a los 30 días por defecto, y con él los commits sin push. Hacer push es decisión de delamor (E2).
- **Hipótesis de delamor (no verificada):** *"Una cierta inestabilidad de la plataforma… su causa es bastante más profunda… su diseño. Fue pensado para otro escenario: solo devices humanos. Desbalanceos de carga, controles de seguridad y coordinaciones de la plataforma fallan, eventualmente. Eso conlleva que algunas acciones no le son permitidas a agentes."*
  - Lo observado es compatible con esa hipótesis: el criterio de idle parece medir interacción humana, y `keepalive.sh` no pudo cumplirlo. Pero la causa no es visible desde adentro.
  - Consecuencia para el diseño: el Codespace es el **entorno de Code**, y su cadencia y sus criterios (stop, límites, permisos) **no están declarados**. Va en la ficha de "entorno" como entorno opaco. El protocolo de continuidad no depende de conocer la causa.
- **Cierre (delamor):** *"Para este plan alcanza con tener presente que puede haber imprevistos… sin atribuir causas."* El protocolo cuenta con imprevistos y no les asigna causa.
- **El chequeo de arranque no dice "OK".** delamor: *"El OK tapa el NO LO SÉ."* El chequeo reporta **qué revisó, qué encontró y qué no puede revisar**. Es el mismo patrón que el vacío disfrazado (`_classify_zone`: None → "stable") y que el NOMINAL por ausencia (`c06db07` → UNKNOWN). La paradoja del simulacro: repetir un "OK" genera una confianza mecánica.
