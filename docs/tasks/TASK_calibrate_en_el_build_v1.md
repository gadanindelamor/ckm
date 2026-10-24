# TASK_calibrate_en_el_build_v1

*24 oct 2026. Pedida por delamor (*"TASK para vos mismo con propuesta de build
similar a rebuild en cuanto a calibrate"*). La escribe Code (Claude Opus 5)
para Code. Antecedente medido: `docs/REG_borrador_calibrate_no_corre_en_el_build.md`.*

**Estado: PROPUESTA. No se ejecuta sin el OK de delamor.**

---

## 0. Qué cierra, en una línea

El build de la primera W **no pasa por el punto de calibración** y el rebuild
sí, así que **el COCO del primer ciclo corre siempre con los defaults**
(`D_CKM_THRESHOLD = 0.40`, `FRAC_REC_MIN = 0.60`) por construcción. Medido:
11 de 51 evaluaciones del intento 2 y 4 de 27 del intento 3.

## 1. Por qué es de delamor y no mía

**E3** del protocolo: *"cambia la semántica del modelo: W, W_eff, Δ_r,
métricas, **calibración**"*. Code no decide esto. La TASK propone, mide y
deja la decisión escrita; **el CP1 no se toca sin OK**.

Y hay una razón de fondo, no sólo de regla: calibrar el primer ciclo **cambia
con qué umbrales COCO lee el campo desde su primera evaluación**. En el
intento 3, con umbrales calibrados, tres filas no habrían sido `stable`. Esto
no es plomería.

## 2. La asimetría, y por qué resultó más chica de lo que escribí

`calibrate` corre hoy **sobre la W candidata, antes de instalarla** (delamor,
19 oct; `ckm_monitor:463-469`). **Para la primera W eso no se puede hacer sin
mover de lugar el build**, porque la construye `ingest()` (`:368`) y cuando el
bloque de la decisión se evalúa la W **ya está instalada**.

**La primera versión de esta TASK decía que mover el build *"toca el límite
`ingest`/rebuild… es el cambio más grande y puede mover cuándo nace W"*. Eso
estaba mal**, y lo encontró una pregunta de delamor (*"mover el build, ¿es en
el bloque de código unas líneas? ¿o qué implica?"*). Tres cosas que no había
mirado:

1. **Monitor construye el corpus con `rebuild_suspendido=True`** (`:243`). En
   `ingest` (`corpus_service:168-172`) ese flag deja `_rebuild()` alcanzable
   **sólo cuando `W is None`**: ingest construye **exactamente una** W, la
   primera. Todas las demás **ya vienen** del bloque de la decisión.
2. **El camino de la decisión ya sabe construir la primera.**
   `no_rebuild_reason` (`corpus_service:385-399`) distingue
   `corpus_en_acumulacion` de `primer_W_no_habilitado`, y
   `rebuild_por_decision(causa, allow_first_W)` existe. **No hay maquinaria que
   escribir: está.**
3. **El volumen ya vota desde el mensaje 10**, porque `_textos_desde_rebuild`
   nunca se reseteó —no hubo rebuild antes—. Así que en el mensaje donde el
   corpus llega a 30 con ≥ 2 devices, `reason` pasa a `None` y el bloque
   dispara **solo**, sin agregarle nada.

Con eso, **la asimetría no hay que declararla: se puede eliminar**, y la
propuesta cambia de opción.

## 3. Las dos opciones, con su costo

### Opción B — que `ingest` no construya la primera W *(PROBADA Y REFUTADA, 24 oct)*

> **CP1 la implementó y la suite la tumbó el mismo día: 30 failed, 6 errors.**
> El bloque de la decisión construye la primera W **sólo si algún criterio
> vota**, y el de volumen pide `_textos_desde_rebuild >= rebuild_every`. En el
> vivo se cumple (`min_texts = 30` contra `rebuild_every = 10`), pero **donde
> `min_texts < rebuild_every` W nace más tarde o no nace** — y media suite
> corre con `min_texts = 3` o `5`.
>
> **Lo que la suite agregó y esta TASK no tenía:** `ingest` no es sólo una
> segunda puerta. Es lo que hace que W nazca **cuando el corpus alcanza su
> umbral, independientemente del ritmo del rebuild**. Sacarla **acopla el
> nacimiento de W al `rebuild_every`**.
>
> **Para que B funcione haría falta** que el camino de la decisión pueda
> disparar **cuando el corpus cruza `min_texts` y todavía no hay W**,
> independiente del volumen: una **causa nueva**. Eso es nomenclatura nueva y
> **E3**, así que es de delamor y no se decide acá.
>
> Lo de abajo queda como estaba escrito, para que se vea qué se creyó.



Una línea en el sitio de llamada:

```python
# ckm_monitor.on_message:368
self._corpus.ingest(
    [message.text],
    landscape_signal=signal,
    allow_first_W=False,        # antes: len(self._devices_seen) >= min_devices
)
```

La condición de los ≥ 2 devices **no se pierde**: sigue viva donde decide, en
`no_rebuild_reason(allow_first_w)` (`:460-467`), que es la que gobierna el
rebuild por decisión. Lo único que cambia es que **ingest deja de ser una
segunda puerta** por la que W puede nacer.

- **Qué conserva:** el momento (`"antes del rebuild, sobre la W candidata"`)
  **con un solo valor**, el registro con la misma forma, y el camino del
  rebuild intacto. La primera W pasa **por la misma puerta** que las otras.
- **Qué cuesta, y es lo único:** `evaluate` corre en `:414`, **antes** del
  bloque de `:458`. Hoy, en el mensaje donde nace W, el panel se calcula
  **con** W —es el primer panel de evaluación—; con B se calcularía **sin**
  ella —sería el último de acumulación— y W nace en **ese mismo mensaje**, un
  paso después en el orden. **Se corre una fila de la trayectoria.** No se
  mueve cuándo nace W; se mueve cuál es el primer panel que la ve.
- **Borde que hay que declarar:** hoy `ingest` es la red de seguridad. Con B,
  si el bloque de la decisión quedara sin criterios que voten
  (`criterios_rebuild` vacío), **W no nacería nunca**. Hoy nacería igual.
- **Reversible:** volviendo el argumento.

### Opción A — calibrar la primera W **después** de que `ingest` la construye

Era la que proponía la v1 de esta TASK. Agrega la rama en `:396` sólo para
`sha_before is None`, calibra después de instalar, y **obliga a que el campo
`moment` tenga dos valores** —uno por camino— para no llamar igual a dos cosas
distintas.

- **Qué conserva:** el orden del panel exactamente como está hoy; ninguna fila
  se corre.
- **Qué cuesta:** deja **dos momentos** de calibración conviviendo, que es
  precisamente la asimetría que B elimina. Y mantiene las dos puertas por las
  que W puede nacer.
- **Queda como alternativa**, no como propuesta: es la que elegiría delamor si
  prefiere **no tocar ninguna fila de la trayectoria** y pagar la asimetría.

### Lo que las dos comparten

Las dos son **una llamada más a `calibrate` por corrida**, que es bloqueante y
tardó **0,0866 s y 0,1326 s** en el intento 3.

## 4. Lo que esta TASK NO toca

**La definición del margen.** Que `margen = d_colapso − d_sin_cambio` mire
**sólo los extremos** y descarte el máximo interno está medido en el REG que
acompaña —en el intento 3 el `d_max` cae en λ=0.25 en los tres rebuilds, y el
del primero (0.0280) ya era **4,9× el umbral que finalmente se adoptó**—, pero
**es otra decisión y es de delamor**. Si se mezclan, después no se sabe cuál de
las dos movió qué.

## 5. Los checkpoints

### CP0 — qué habría dado, medido antes de tocar nada *(no necesita OK)*

Reconstruir **la primera W de los intentos 2 y 3** desde los textos
preservados —los primeros 30 de cada corpus, con el extractor declarado— y
correr `calibrate` sobre ellas, con `n_runs=200` y `seed=0`, que son las
condiciones que el vivo usó.

**Se escribe la predicción ANTES de correr** (política de tests del 21 oct).
La mía, para que quede falsable: **las dos van a dar `no_calibrado`**, porque
en el intento 2 los cuatro rebuilds dieron `d_max = 0` y porque en el intento 3
el `d_max` **crecía** con los rebuilds (0.0280 → 0.1760 → 0.2312), así que el
primero debería estar por debajo de 0.0280 y el margen por debajo de −0.2492.

**Qué decide el CP0:** si las dos dan `no_calibrado`, la opción A **no habría
cambiado ninguna de las dos corridas**, y eso hay que decirlo antes de pedir el
cambio. Si alguna separa, el cambio tiene un efecto medido.

### CP0b — los tres docstrings que ya están mal *(NO BLOQUEA; se puede cerrar sin decidir nada de esta TASK)*

Chequeados a pedido de delamor (*"no olvidar los docstrings al chequear"*).
**No dependen de la decisión**: están mal hoy.

1. `ckm_monitor.py:82-83` (docstring del módulo) y 2. `ckm_monitor.py:326`
   (comentario del atributo) dicen que el punto de `calibrate` *"existe y **no
   hace nada**"*. Es la versión anterior del mecanismo: corre desde el 19 oct y
   en el intento 3 **produjo los umbrales que COCO usó**.
3. `ckm_monitor.py:552` nombra la clave **`w_sha_vigente_al_calibrar`**; la que
   el código escribe (`:573`) y la que está en los datos es
   **`w_sha_live_at_calibration`**. El docstring nombra algo que no existe.

**Recomiendo cerrarlas antes que el resto**, y por separado: son correcciones
de lo que ya hay, y si entran en el mismo commit que el cambio de
comportamiento después no se distingue qué movió qué. **Default declarado:
no las toco hasta que delamor diga**, porque son archivos de IAP y hoy la
sesión está en pausa de ejecución.

### CP1 — la implementación *(BLOQUEA: necesita el OK de delamor)*

La opción B, con:

- `allow_first_W=False` en la llamada a `ingest` (`:368`), y **nada más** en
  ese punto;
- **nada nuevo en el registro**: el `moment` conserva su único valor, que es el
  punto de B frente a A;
- **docstrings**, que son parte del cambio y no un anexo (delamor: *"y luego
  de modificar"*): `_calibrate` y `on_message` con la asimetría declarada —
  que el primer ciclo también calibra y **en qué momento**—, y las tres del
  CP0b si todavía no se cerraron;
- tests: que el build deje registro de calibración (hoy deja `None`), que la
  condición de los ≥ 2 devices **siga gobernando** desde `no_rebuild_reason`,
  que W nazca **en el mismo mensaje** que hoy, y **la inversión**: que el
  camino del rebuild siga dando exactamente lo de antes;
- y el borde declarado: con `criterios_rebuild` vacío, **W ya no nacería**. Un
  test que lo fije, para que el día que alguien vacíe esa tupla se entere acá y
  no en un vivo.

### CP2 — la corrida *(BLOQUEA: un vivo no se corre sin orden explícita)*

El intento 4, igual que el 3 salvo esto, para que lo que cambie sea
atribuible. Con la expectativa escrita antes de correr.

## 6. Cómo se revierte

CP1 es **un argumento** y los docstrings: se vuelve el argumento a su
expresión anterior y el comportamiento es exacto el de hoy.
CP0 no toca el repo —mide sobre copias— y CP2 no se corre sin orden.
