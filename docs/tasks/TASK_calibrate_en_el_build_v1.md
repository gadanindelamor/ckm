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

## 2. La asimetría, dicha antes de proponer nada

`calibrate` corre hoy **sobre la W candidata, antes de instalarla** (delamor,
19 oct; `ckm_monitor:463-469`). **Para la primera W eso no se puede hacer sin
mover de lugar el build**, porque la construye `ingest()` (`:368`) y cuando el
bloque de la decisión se evalúa la W **ya está instalada**.

O sea: cualquier propuesta elige entre

- **conservar el momento** ("antes de instalar") y **mover el build**, o
- **conservar el build donde está** y **cambiar el momento** para el primer
  ciclo ("después de instalar, antes de la primera evaluación").

No hay una tercera que preserve las dos cosas. Esto es lo que hay que decidir.

## 3. Las dos opciones, con su costo

### Opción A — calibrar la primera W **después** de que `ingest` la construye *(la que propongo)*

Dónde: en `on_message`, en la rama `if sha_after != sha_before` (`:396`),
**sólo cuando `sha_before is None`** —el build, no un rebuild— y **antes** de
que corra `evaluate` (`:415`), que es quien arma el panel del que COCO toma
sus umbrales.

- **Qué conserva:** el build donde está, `ingest()` intacto, el camino del
  rebuild intacto, el registro con la misma forma (`punto_calibrate` y
  `coco.calibration`).
- **Qué cambia, y hay que declararlo:** para el primer ciclo el momento es
  **"después de instalar"**, no "antes". El registro tiene que **decirlo en el
  campo `moment`**, que hoy dice siempre *"antes del rebuild, sobre la W
  candidata"*. Dos momentos distintos con el mismo rótulo sería justo el tipo
  de cosa que este repo no hace.
- **Costo medido:** `calibrate` es bloqueante y tardó **0,0866 s y 0,1326 s**
  en el intento 3. Es **una** llamada más por corrida.
- **Reversible:** quitando la rama.

### Opción B — mover el build al bloque de la decisión

Que la primera W también se construya desde el camino del rebuild, para que
pase por el mismo punto y el `moment` siga siendo uno solo.

- **Qué conserva:** la simetría completa.
- **Qué cambia:** toca el límite `ingest` / rebuild, que es donde viven
  `_textos_desde_rebuild`, `_ciclos_sin_rebuild`, `allow_first_w` y
  `no_rebuild_reason`. **Es el cambio más grande de los dos y el que puede
  mover el momento en que nace W**, que es lo que todas las corridas anteriores
  tienen fijado en `MIN_TEXTS_FIRST_W = 30`.
- **No la propongo** para esta TASK: el beneficio es de forma y el riesgo es
  sobre cuándo nace W.

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

La opción A, con:

- la rama en `on_message`, **sólo** para `sha_before is None`;
- el `moment` del registro diciendo cuál de los dos momentos fue —sin nombres
  nuevos: el campo ya existe y hoy tiene un solo valor—;
- **docstrings**, que son parte del cambio y no un anexo (delamor: *"y luego
  de modificar"*): `_calibrate` y `on_message` con la asimetría declarada —
  que el primer ciclo también calibra y **en qué momento**—, y las tres del
  CP0b si todavía no se cerraron;
- tests: que el build deje registro de calibración (hoy deja `None`), que el
  `moment` distinga los dos casos, y **la inversión**: que el camino del
  rebuild siga dando exactamente lo de antes.

### CP2 — la corrida *(BLOQUEA: un vivo no se corre sin orden explícita)*

El intento 4, igual que el 3 salvo esto, para que lo que cambie sea
atribuible. Con la expectativa escrita antes de correr.

## 6. Cómo se revierte

CP1 es una rama y un docstring: se quita y el comportamiento vuelve exacto.
CP0 no toca el repo —mide sobre copias— y CP2 no se corre sin orden.
