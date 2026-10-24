# REG (BORRADOR) — `calibrate` no corre en el build de la primera W

**Borrador. Fuera de `registers/` por la regla de Clase R: los REG nuevos se
entregan como borrador y delamor decide si entran.**

- **Fecha:** 2026-10-24. **Medido por:** Code (Claude Opus 5), por pregunta de
  delamor: *"luego de la fase de acumulación a evaluación, ¿podés verificar si
  el build de W calibra tal como lo hace el rebuild?"*
- **Qué es esto:** una verificación, no una corrida. **No se cambió nada.**
- **Datos:** `experiments/_state_S2-C0/monitor_trajectory.jsonl` (intento 3) y
  `process/monitor_trajectory.jsonl.bak_1792649008_serie2_caso0` (intento 2).
- **Código:** `30e0084`.

---

## 1. La respuesta: no

El build de la primera W **no pasa por el punto de calibración**. Sólo los
rebuilds lo hacen. Medido en las dos corridas vivas que existen.

| corrida | W | estado de `calibration` | causa | margen | `d_max` | λ(`d_max`) | umbral que usó COCO |
|---|---|---|---|---|---|---|---|
| 2 | `6e666d09` **(build)** | **None** | — | — | — | — | default 0.40 |
| 2 | `fa1d1864` | `no_calibrado` | `sin_separacion` | −0.270535 | **0.0000** | **0.0** | default |
| 2 | `18138650` | `no_calibrado` | `sin_separacion` | −0.269075 | **0.0000** | **0.0** | default |
| 2 | `3d2e8f1d` | `no_calibrado` | `sin_separacion` | −0.249751 | **0.0000** | **0.0** | default |
| 2 | `c049d2e8` | `no_calibrado` | `sin_separacion` | −0.266888 | **0.0000** | **0.0** | default |
| 3 | `7093ad0f` **(build)** | **None** | — | — | — | — | default 0.40 |
| 3 | `5d657507` | `no_calibrado` | `sin_separacion` | −0.249215 | 0.0280 | 0.25 | default |
| 3 | `698d0f3f` | `no_calibrado` | `sin_separacion` | −0.048469 | 0.1760 | 0.25 | default |
| 3 | `bdb98f5b` | **`calibrado`** | — | **+0.011418** | 0.2312 | 0.25 | **`calibrate` 0.00571** |

La primera W de cada corrida tiene **`estado: None`**: no hay registro de
calibración, **ni siquiera `nulo_calibrado`** —que es el valor para *"no se
ejecutó"*—. **No es que corriera y no separara: nunca se la intentó.**

## 2. El mecanismo, en el código

```
ckm_monitor.on_message:
  :361   sha_before = self._corpus.w_sha()
  :368   self._corpus.ingest(...)        ← LA PRIMERA W SE CONSTRUYE ACÁ
  :378   sha_after  = self._corpus.w_sha()
  :394   self._textos_desde_rebuild += 1
  :396   if sha_after != sha_before:     ← "rebuild por ingesta (la primera W…)"
  :400       self._textos_desde_rebuild = 0
  …
  :458   if self._last_rebuild_signal:   ← el bloque de la decisión
  :467       reason = self._corpus.no_rebuild_reason(allow_first_w)
  :469       if reason is None: self._punto_calibrate = self._calibrate(clock)
```

Dos hechos encadenados:

1. **La primera W la construye `ingest()`** (`:368`), que corre **antes** del
   bloque de la decisión. El propio código lo dice en `:397`: *"rebuild por
   ingesta (**la primera W**, o el régimen no suspendido)"*.
2. En ese mismo mensaje, `_textos_desde_rebuild` **se acaba de resetear a 0**
   (`:400`), así que el criterio de volumen no puede votar,
   `_last_rebuild_signal` queda en `False` y el bloque de `:458` no se entra.

**Consecuencia, por construcción y no por el corpus: el COCO del primer ciclo
corre siempre con los defaults `D_CKM_THRESHOLD = 0.40` y
`FRAC_REC_MIN = 0.60`.**

Cuánto dura ese primer ciclo, medido: **11 de 51 evaluaciones** en el intento 2
(filas 0–10) y **4 de 27** en el intento 3 (filas 0–3).

## 3. Lo que esto le agrega al REG del intento 2

`registers/REG_iap_serie2_caso0_intento2_v1.md` dice `calibrated: false` y
`causa: sin_separacion` como **un estado final**. Tres cosas que no dice:

1. **Que el primer ciclo no podía calibrarse.** Leído como está, el
   `calibrated: false` se atribuye a esa W. Para el primer ciclo es
   **estructural**.
2. **Que en el intento 2 no había información en ninguna parte de la curva.**
   Los cuatro rebuilds dieron **`d_max = 0.0000` en `λ = 0.0`**: el máximo de la
   curva era la W sin tocar, y la curva **nunca subió**. Eso es más fuerte que
   *"no separó"* — y es coherente con la aritmética de esa W: 366 de 380 pares
   positivos, ninguno negativo, así que interpolar hacia *"todo positivo"*
   **sólo agrega** atractores.
3. **Que los umbrales fueron `default` en las 51 evaluaciones.** Sin eso, los
   `triggers: 0` se leen como un dato del campo.

## 4. El contraste con el intento 3

| | intento 2 | intento 3 |
|---|---|---|
| `d_max` por rebuild | 0.0000 · 0.0000 · 0.0000 · 0.0000 | **0.0280 · 0.1760 · 0.2312** |
| λ del `d_max` | 0.0 (los cuatro) | **0.25 (los tres)** |
| `curva_monotona` | — | `False` (los tres) |
| margen (extremos) | −0.2705 · −0.2691 · −0.2498 · −0.2669 | −0.2492 · −0.0485 · **+0.0114** |

En el intento 3 el máximo de la curva **está adentro** (λ=0.25) en los tres
rebuilds y **crece**, mientras el margen —que mira **sólo los extremos**— cruza
el cero recién en el último.

**El número que cierra el punto: el máximo interno del primer rebuild (0.0280)
ya era 4,9× el umbral que finalmente se adoptó (0.00571).** La señal estaba
desde el primer rebuild, y la definición del margen la descartó tres veces.

## 5. Los docstrings, chequeados (pedido de delamor)

*"No olvidar los docstrings al chequear y luego de modificar"*. Chequeados, y
**tres no dicen lo que el código hace**. Las tres son de hoy y **no dependen de
esta TASK**: están mal con o sin el cambio.

| # | dónde | dice | hace |
|---|---|---|---|
| 1 | `ckm_monitor.py:82-83` (docstring del módulo) | *"El punto donde iría `calibrate` existe, está marcado en el panel y **no hace nada**"* | corre desde el 19 oct, y en el intento 3 **produjo los umbrales que COCO usó** |
| 2 | `ckm_monitor.py:326` (comentario del atributo) | *"El lugar donde va `calibrate`. **Existe y no hace nada**: declarado."* | ídem |
| 3 | `ckm_monitor.py:552` (docstring de `_calibrate`) | nombra la clave **`w_sha_vigente_al_calibrar`** | la clave que escribe es **`w_sha_live_at_calibration`** (`:573`), y es la que está en los datos |

Las dos primeras son la **versión anterior** del mecanismo, de cuando el punto
era un marcador vacío (`TASK_calibrate_mecanismo_v1`). La tercera es un nombre
que **no existe**: quien busque `w_sha_vigente_al_calibrar` en los logs no lo
encuentra.

Y una cuarta, que es la de esta verificación: **el docstring de `_calibrate`
describe el camino del rebuild como si fuera el único**, y no declara la
consecuencia —que el primer ciclo queda sin calibrar—. No es falso; es
incompleto, y es justo lo que hizo falta medir para contestar la pregunta.

## 6. Lo que este registro NO dice

- **No dice qué habría dado `calibrate` sobre la primera W.** Nunca corrió. Es
  medible offline —las dos primeras W se reconstruyen desde los textos
  preservados— y es el CP0 de la TASK que acompaña a este REG.
- **No propone cambiar la definición del margen.** Que el margen mire los
  extremos y no el máximo interno es una decisión sobre qué mide el
  instrumento (E3) y es de delamor. Acá sólo queda medido lo que descarta.
- **No afirma que calibrar el primer ciclo hubiera cambiado los `triggers`.**
  Con los umbrales calibrados del intento 3, tres filas no habrían sido
  `stable`; pero esas filas son de **otro** ciclo y de **otra** W.
- **Dos corridas. Nada acá es replicación** — aunque el `estado: None` de la
  primera W es del código, no del muestreo.
