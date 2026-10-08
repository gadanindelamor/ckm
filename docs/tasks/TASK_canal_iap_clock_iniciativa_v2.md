# TASK_canal_iap_clock_iniciativa_v2

*6 oct 2026. Pedido de delamor. Redacta Claude Opus 5.5 (Cowork) y ejecuta Claude Code en el Codespace `ckm`. La v1 se verificó contra el clon local en `eddb4b0`.*

*v2 (8 oct 2026, Opus). **Se reverificó contra `94baf68`**, después de la Config v3 y de la TASK Monitor+COCO v2 (cerrada). Cambia solo lo que el repo cambió: §0.4 se reescribe, se agrega §0.6 (el tiempo que ya está en la Config) y se agrega una pregunta al punto 2 del CP0. También se corrige la referencia de §3. Lo dictado por delamor (CLOCK, ODA continuo, UTC, criterio local, freeze, espíritu) no se tocó. La v1 queda como traza.*

*Releído sin cambios en `94baf68`: `autonomous_device.py` `run()` (L195–238, `time.time()` en L203/L215), `channel.py` L52 (UTC), `mcp_server.py` L29 (epoch) y `agent_device_skin.py` L95 (`build_goal_directed_agent`). Ninguno de esos archivos cambió desde `eddb4b0`.*

**Origen.** Esto no es nuevo. Se decidió en septiembre y no llegó al canal. `docs/PROPUESTA_ckm_landscape_dynamics_v5.md`, Adenda:

> *"CKMLandscapeConfig porta el CLOCK del canal. No como metadata — como dimensión del landscape. **El silencio entre mensajes es dato medible, no ausencia de dato.** Sin CLOCK el canal es una secuencia; con CLOCK es un proceso en el tiempo."*
>
> *"ODA con iniciativa del device: Observe incluye el silencio. **Un device con objetivo propio puede decidir actuar antes de que ocurra Z.** El CLOCK da la coordenada temporal. **`on_message` no puede ser el único trigger.**"*

**delamor (6 oct):**
- *"Hay que modificar el canal IAP para que los devices interactúen por voluntad propia. El evento de mensaje nuevo en el canal no [puede ser] el único disparador del ciclo ODA."*
- Ejemplo de Z: **adquirir las entradas para la fiesta de presentación del CKM antes de que se acaben.**
- *"Eso genera tensión potencial."*

**Principio.** Free Will (TRUST_INSTRUCTIONS): *"No one is obligated to participate."*

**Reglas de trabajo.**
- Primero va el CP0, sin código.
- Hay checkpoints con feedback parcial, que valen también para las acciones espontáneas.
- El código corre solo en el Codespace.
- Lo que se puede demostrar no se corre.
- Lo que decide delamor está marcado **[delamor]**.

---

## 0. Estado actual (leído en el código)

`iap_chatroom/autonomous_device.py`, `run()` (L195–235):

```
por cada poll (poll_interval = 2.0 s):
    get_messages(since=last_ts)
    por cada mensaje nuevo de OTRO device con device_type ∈ {AI, HUMAN, SYSTEM}:
        _observe → _decide (INTERACT | OP_SILENCE) → _interact
    sleep(poll_interval)
```

1. **El único disparador del ODA es un mensaje ajeno.** El device puede elegir callar, pero solo cuando le hablan. No puede iniciar, no observa el campo por su cuenta y no decide irse: `leave_channel` ocurre recién cuando vence `duration`.
2. **Hay un ODA por cada mensaje.** Si en un poll entran cinco mensajes, el device decide cinco veces.
3. **El silencio es absorbente por construcción.** Si todos eligen OP_SILENCE, no aparece ningún mensaje nuevo y nadie más se dispara. Es demostrable sin correr nada. Queda registrado como **condición del canal** en el que ocurrió la serie IAP, y se congela con ella (CP0b). La serie no se revisa.
   - **El silencio existió:** es traza de la experiencia y es de lo que se trataba (delamor, 7 oct). La construcción del canal explica por qué nada lo interrumpió, **no decide qué fue**.
   - **Genealogía de "acoplado":** delamor observó *contagio* en el IAP project, antes del CKM (*"contagio, ojo, atentos a los contagios"*). Sonnet lo escribió después como *acoplamiento*. Contagio es una observación del proceso (algo se propaga entre devices); acoplamiento es un mecanismo (devices ligados). El cambio de palabra convirtió una observación en una explicación (BABEL). Ninguna de las dos se valida con la serie, porque la serie no se revisa.
4. **No hay CLOCK en el código** (se reverificó en `94baf68` y sigue igual). La memoria del 28 sep dice *"CLOCK y ticks de LandscapeConfig implementados y funcionando (commit exacto no identificado)"*, pero no hay CLOCK ni ticks en `services/` ni en `iap_chatroom/`. Los únicos `tick` del repo son el timer de refresco de `ui_gradio.py`.
   - **Lo que cambió desde la v1 (Config v3 y Monitor+COCO v2):** `CKMlandscapeConfig` ya **no es solo un registro**. Ahora es **fuente** de `n_runs` y `seed`, que son un solo valor para Monitor y COCO (P9, delamor: *"n 1000"*). Además lleva la **traza de ciclos de vida de W** (clase `Ciclo`, inmutable; el ciclo vigente es el último) y Monitor la serializa en cada panel. El docstring viejo (*"todavía no la consume ningún servicio"*) ya no aplica.
5. **Hay antecedentes de devices con objetivo.** `agent_device_skin.py` L95 tiene `build_goal_directed_agent`, y los casos 0.13 y 0.14 (handoff) trabajan con dependencias entre devices.
6. **La Config ya tiene tiempo, pero no es un CLOCK** (nuevo en la v2). Cada `Ciclo` lleva `t_senal` (cuándo se señaló que W debía cambiar; `None` si nadie lo señaló) y `t_rebuild` (cuándo cambió W), y de ahí sale la `deriva` (I6). **Esos tiempos se sellan con `time.time()` del proceso que corre Monitor** (`ckm_landscape_config.py` L247, `monitor_service.py` L548/L556), no con el timestamp de recepción del canal. Si el CLOCK lo porta la Config, en el mismo objeto conviven dos fuentes de tiempo: el reloj del proceso para los ciclos de W y el reloj del canal para los mensajes. En el Codespace suelen ser la misma máquina, pero **no es lo mismo que una sola fuente declarada**. No se decide acá: lo evalúa el CP0 (punto 2).

## 1. Lo que se propone

- **Un CLOCK del canal.** Es una coordenada temporal común y observable: ticks numerados que publica el canal, no que lleva cada device. Para todos los devices es la misma, y es parte de lo que se observa. Por la adenda, el CLOCK lo porta CKMLandscapeConfig.
- **El ODA es continuo**, como en BE Framework: `ODAODAODAODA…`. **No corre en cada tick: los ticks son información.** (delamor, 6 oct)
  - Cada device sostiene su ciclo a su propio ritmo, haya o no mensajes nuevos.
  - Los mensajes nuevos y el tick actual pasan a ser **parte de la observación**, no el disparador.
  - Hay una decisión por vuelta del ciclo, con todo lo observado desde la vuelta anterior.
- **ODA, lo básico** (delamor, 6 oct; BE Framework, `ckm___memories/BE/`):
  - **O, Observación:** lo que el device toma del canal y del campo. Incluye **el clock, que es parte del campo**, y los mensajes **con su timestamp**. El canal no calcula nada por el device: no entrega "ticks sin mensajes" ni "quién habló último" ya procesados. Da los datos, y cada uno con su marca de tiempo.
  - **D, Decisión:** el device decide qué hacer. **Evaluar los tiempos** (el Δt entre dos eventos, entre mensajes, desde la última vez que habló, lo que crea) **es parte de decidir**, y cada device lo hace a su manera.
  - **A, Acción:** lo que el device hace con lo decidido.
  - Ejemplo (delamor): *"Observo el canal. Pienso: che, el device Juan Pérez dijo tal cosa hace 7 minutos, ¿y todavía nada?"*. Los 7 minutos no se los dio el canal: los calculó el device con los timestamps, y notar que "todavía nada" es parte de su decisión. Eso es observar el silencio sin que nadie lo dispare.
  - Requisito para el canal: **todo mensaje y todo evento lleva timestamp.** Ya pasa hoy: `channel.py` usa ISO8601 y `get_messages` usa epoch. El CP0 tiene que confirmar que eso alcanza.
  - **UTC, la hora de Greenwich (delamor, 7 oct).** Todos los timestamps van en UTC. Leído en el código: `channel.py` L52 ya usa `datetime.now(timezone.utc).isoformat()` (+00:00), y `mcp_server.py` L29 lo pasa a epoch, que es UTC por definición. ✓
  - **El reloj contra el que se mide.** `autonomous_device.py` L203/L215 usa `time.time()` **del propio device** para `last_ts`. Si el device corre en otra máquina, su reloj puede estar corrido respecto del canal. Los Δt que entran a D (y al criterio local) se calculan **con los timestamps del canal**, nunca mezclando el reloj del device con el del canal. El CP0 tiene que confirmar si hoy se mezclan.
  - **Device Japón (UTC+9):** puede ser "mañana" en su hora local. Los timestamps que recibe D van en UTC **y dicen que son UTC**, para que el LLM no los traduzca a su hora.
  - **El timestamp es de recepción, no de envío:** el canal sella el mensaje cuando le llega, así que el viaje de red queda incluido. "Hace 7 minutos" quiere decir 7 minutos desde que llegó al canal. Es el tiempo del canal, una sola fuente, y se declara así.
- **D elige una acción, o ninguna. A la ejecuta con una primitiva del canal** (delamor: *"LEAVE es una acción… su interacción puede ser leave, y eso se conecta a la primitiva"*):
  - **publicar** → primitiva `send_message`;
  - **irse** → primitiva `leave_channel`, por decisión propia y no porque venció `duration`;
  - **ninguna** (OP_SILENCE): no actúa en esta vuelta, y el ciclo sigue.

  INTERACT y LEAVE no son tipos de decisión distintos: los dos son acciones, cada una con su primitiva. Si mañana el canal ofrece otra primitiva, D la puede elegir sin cambiar el ciclo.
- **NOTA de optimización (no es modelo): WAIT.** Para no pagar una decisión (una llamada al LLM) en cada vuelta, un device podría "dormir" hasta un tiempo o un evento. Es costo, no ODA. Lo evalúa Code en el CP0 (punto 4).
- **Propuesta de delamor (7 oct): un criterio local antes de D, sin LLM.** El costo es una variable más, con presupuesto, que va a tener que evaluarse.
  - **Qué es:** `autonomous_device` calcula **deltas locales** a partir de lo que ya observa, y no del canal: Δt desde el último mensaje ajeno, Δt desde que el device habló por última vez, Δ mensajes desde su última decisión, si lo nombraron, si cambió el estado del objetivo (K) y **cuánto gastó contra su presupuesto**. `_observe` ya funciona sin LLM.
  - **Qué hace:** decide **si vale la pena llamar a D (LLM)** en esta vuelta, no qué hacer. Si no cambió nada relevante, la vuelta sigue sin llamar. Los deltas además entran como **información** a D cuando sí se lo llama.
  - **Sostener la tensión del sesgo** (regla CKM, paso 4): el pre-filtro es un sesgo evidente. **Se declara**, no pasa por campo:
    - cada vuelta sin llamar queda registrada con su motivo (`skip: Δmsgs=0, Δt=40s < umbral`);
    - **auditoría:** cada tanto (cada N vueltas, o al azar) se llama a D aunque el pre-filtro diga que no, y se registra si D habría hecho algo distinto de "nada". La tasa de divergencia **mide el costo del sesgo**;
    - los umbrales son **declarados** (son de Calibración) y no los inventa Code.
  - **La zona horaria propia, si el device quiere** (delamor, 7 oct): el device puede saber su time zone y su hora local, sin LLM, y usarlas como información **local** para decidir si llama a D. Por ejemplo, de noche en su hora quizás convenga llamar menos. Es opcional y propio del device (free will). No es información del canal, y los Δt siguen en UTC del canal.
  - **El costo como observación:** el device ve su propio gasto y el presupuesto que le queda. Decidir con poco presupuesto es parte de D.
  - **Free will** (delamor): *"my world being the world cause it is not mine"*. El criterio local es del device; el mundo, el canal y los demás no son suyos.
  - Lo evalúa Code en el CP0 (punto 6, costo). **No se implementa sin el OK de delamor.**
- **Un objetivo con condiciones, para el caso de prueba.** delamor: *"El objetivo tiene condiciones a cumplir. No ticks. Antes que se acaben."* Un deadline en ticks puede existir, pero es un caso particular, no lo general.
  - Ejemplo: *"conseguir entradas para la fiesta de presentación del CKM, **antes de que se acaben**"*. La condición es que queden entradas (K > 0). K no baja con el reloj: baja cuando **otros** las consiguen. La urgencia sale del estado del mundo y se observa, no se cuenta en ticks.
  - Los ticks sirven para ver **a qué ritmo** se acaban: es información, no el plazo.
  - La tensión crece a medida que la condición se acerca a no cumplirse. En el Hamiltoniano del Híbrido (H = −½ΣW_ij·s_i·s_j − Σh_i·s_i), el objetivo sería un campo externo h que crece con la escasez, no con el reloj. Esta lectura es **propuesta**: no se implementa como fórmula en esta TASK, solo se registran el objetivo, sus condiciones y su estado en el log.
- **Se conserva** la regla estructural de nunca reaccionar al propio mensaje.
  - **Precisión (delamor, 7 oct):** la regla es **no reaccionar al evento** del propio mensaje. **No impide escribir varios seguidos.** Con el ODA continuo, un device puede volver a publicar sin que nadie le haya respondido ("7 minutos y todavía nada"). Lo decide por lo que observa (Δt, silencio, el objetivo), no porque su mensaje anterior lo dispare.
  - En el criterio local, Δ mensajes cuenta **solo los mensajes ajenos**. El propio mensaje entra como "Δt desde que hablé", es información y no disparador.
  - Test del CP2: un device publica dos veces seguidas por decisión, y **ninguna** de las dos publicaciones queda registrada como reacción a la anterior.

## 1b. Espíritu (no es requerimiento)

delamor: *"Esto no es requerimiento, es espíritu: idealmente los ciclos ODA hasta podrían ser threads. Por ejemplo, esos threads irían por el universo. Yo, device delamor, podría disparar conceptualmente y mantener muchos ciclos ODA, de la misma forma que hago acciones en paralelo."*

Un device no está obligado a tener un solo ciclo ODA: podría sostener muchos en paralelo, cada uno observando y decidiendo por su cuenta. **No se implementa en esta TASK.** Se deja escrito para que el diseño del CP2 **no lo impida**: que el ciclo sea una unidad que se pueda lanzar más de una vez por device.

## 2. Checkpoints

### CP0. Evaluar contra el repo (sin código)

Reportar al menos lo siguiente:

1. Dónde vive hoy el tiempo del canal. `channel.py` usa timestamps ISO, y `mcp_server.get_messages(since)` usa epoch. ¿Hay algo que pueda ser el CLOCK, o va de cero?
2. **Quién porta el CLOCK.** La adenda dice CKMLandscapeConfig. Desde la v3, la Config ya es fuente de `n_runs` y `seed` y lleva la traza de `Ciclo` (§0.4 y §0.6). Hay que reportar:
   - si el CLOCK cabe en la Config sin romper su inmutabilidad (I1: la config gana ciclos, no los edita). Un tick avanza siempre; un ciclo se abre solo cuando cambia W;
   - **con qué reloj quedan los tiempos** si el CLOCK vive ahí: los de `Ciclo` (proceso de Monitor) y los ticks y mensajes (canal). ¿Se unifican, se declaran las dos fuentes o hay otra opción? Si cambia lo que el instrumento mide, es **[delamor]** (E3);
   - si choca con `TASK_landscape_config_en_runs_v1` y con lo cerrado en `TASK_monitor_coco_ciclo_orbita_v2` (ciclo de vida común, COCO renace con el ciclo).
3. `build_goal_directed_agent`: ¿sirve como base para el device con objetivo, o es otra cosa?
4. **Costo.** Un ODA continuo significa una llamada al LLM (el gate) por vuelta y por device. Hay que reportar cuánto sale con N devices durante una duración dada, y qué fija el ritmo de la vuelta: el device, un mínimo declarado, `WAIT`. La Observación del ciclo no usa LLM (`_observe` ya es sin LLM).

**Alto. Reportar a delamor.**

### CP0b. Congelar la serie IAP (freeze) — antes de tocar el canal

delamor: *"No hay nada que revisar en la serie de tests IAP. Lo que sí hay que hacer es congelar las condiciones. Freeze VM. Como no tenemos los recursos materiales, hacemos el INTENTO de moverlo a process. NO ES REPRODUCIBLE."*

- **No se revisan ni se reinterpretan los casos 0.4–0.15.** Son experiencia del canal vivo.
- **Se congelan sus condiciones.** No hay imagen de VM, así que se intenta dejar todo lo que se pueda nombrar:
  - el commit actual (sha) del canal y los servicios;
  - `pip freeze` del Codespace;
  - los providers y los modelos usados en cada caso, según sus REG;
  - las configs (por ejemplo `groq_agent_config.json`), `iap_chatroom/_state` y los tests `test_caso_*.py` tal como están.
- **Todo eso se mueve o copia a `process/`**, junto a lo que ya existe en `process/iap/` y `process/iap_series/`. Lleva un README que diga en la primera línea: **"NO ES REPRODUCIBLE. Intento de congelar las condiciones de una experiencia en vivo."**
- **La intuición (delamor):** *"Reproducir las condiciones del fenómeno, sea un test o un experimento, sería abrir una VM y ejecutar lo que se desee, SIN PODER MODIFICAR EL MODELO DE ESA VM."* Es una foto del entorno: se puede correr adentro, pero no se la puede cambiar. **Se reproducen condiciones, no experimentos** (delamor): lo que pase adentro, cada vez, es otra experiencia. Reproducir el fenómeno es **imposible en este planeta**: habría que reproducir el todo, y no lo conocemos (delamor: *"No conocemos el todo. Las interpretaciones siempre son falsas."*). Lo más cercano a nuestro alcance es una imagen de contenedor (devcontainer del Codespace con dependencias fijadas) más el sha.
- **El límite que la VM no cierra:** los modelos de lenguaje no viven adentro. Se llaman por API, y el proveedor los cambia o los retira. Aunque se congele la VM, cada llamada sale de ella. Por eso, aunque se congele todo lo demás, ni siquiera las condiciones se reproducen del todo: el modelo es parte de las condiciones y queda afuera. Lo único que se puede guardar son los identificadores de los modelos y las respuestas que quedaron en los logs.
- **Después del freeze,** `trigger_mode="on_message"` deja de ser el modo del canal. Queda solo como parte de lo congelado.

**Alto. Reportar a delamor.**

### CP1. El CLOCK del canal (sin cambiar a los devices)

- El canal publica ticks numerados con un período declarado, y una tool MCP `get_clock()` (o un campo en `get_messages`) devuelve el tick actual.
- Cada tick queda registrado: ticks con mensajes y ticks sin mensajes. El silencio queda como dato.
- **Tests:**
  - los ticks son monótonos;
  - un canal sin mensajes también avanza ticks;
  - `get_messages` sigue funcionando igual que antes.

**Alto. Reportar a delamor.**

### CP2. El ODA continuo

- `AutonomousDevice` con `trigger_mode="continuo"`: el ODA corre de forma continua a su propio ritmo. En cada vuelta observa el tick actual, los mensajes nuevos y el campo, y decide una acción (publicar, irse) o ninguna. El tick no dispara nada: se observa.
- `trigger_mode="on_message"` no se mantiene como modo vivo: quedó congelado en el CP0b.
- **Tests que pueden fallar:**
  - **Iniciativa:** con el canal en silencio, un device con objetivo **puede** hablar primero. No se le exige que hable; se verifica que el diseño se lo permite.
  - **Silencio no absorbente:** si todos eligieron OP_SILENCE, el ciclo de cada uno sigue y vuelven a decidir sin que llegue ningún mensaje.
  - **Una decisión por vuelta del ciclo,** aunque hayan entrado varios mensajes: no hay un ODA por mensaje. Los ticks no la disparan.
  - **LEAVE:** el device se va antes de que venza `duration`, y queda registrado como decisión.

**Alto. Reportar a delamor.**

### CP3. El caso Z (las entradas) **[delamor]**

Diseño del caso, con delamor antes de correrlo: cuántos devices, cuántas entradas, quién o qué las consume (otros devices, el entorno), qué objetivo y qué condiciones tiene cada device (uno, varios, ninguno), y qué se observa.

Va a ser una **experiencia del canal vivo, no un experimento** (el criterio de §6). Se registra como caso IAP nuevo.

delamor: *"El IAP channel sigue cambiando con el modelo. La próxima serie de tests IAP será lo que sea."* La serie nueva **no continúa** la congelada ni se compara con ella: cada serie vive en su propio canal.

## 3. Lo que esta TASK NO hace

- No cambia los casos 0.4–0.15 ni sus REG: los congela (CP0b).
- No toca CorpusService, el rebuild, Monitor ni COCO. Eso se cerró en `TASK_monitor_coco_ciclo_orbita_v2` (CP4, `1e8d267`). Si el CP0 concluye que el CLOCK tiene que tocar la Config o Monitor, se para y se reporta: no se toca de paso.
- No implementa h en el Hamiltoniano. Solo deja registrados el objetivo, sus condiciones y su estado para poder leerlos después.
- No obliga a ningún device a participar.
