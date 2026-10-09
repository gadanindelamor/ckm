# ESTADO_canal_iap_clock_iniciativa_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-09 23:38 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**VIVO 03 — el criterio local en vivo.** Corrido el 2026-10-09. **23 → 9 llamadas** (7 al gate
+ 2 de `_generate`), 62.5 s, 12 vueltas por device, 0 errores. El piso disparó en los dos
devices (vueltas 12 y 10, no la 8 predicha: `criterio` reseteó el contador por los joins y los
mensajes — estaba escrito como "no es teorema"). `piso_dentro_del_horizonte = True` en los dos.

**La auditoría disparó en uno solo** (1 y 0): el piso sostuvo la iniciativa de los dos, la
auditoría dejó el costo del sesgo de uno sin medir (`tasa = None`, no `0.0`). **El muestreo de
la cara del pase midió cero en los dos**; el **censo** dice 0.667 — si esa cara fuera sólo
muestreo, el vivo no reportaría nada de ella.

F3b y F4 confirmados en vivo: 4 mensajes, 2 al corpus (los 2 joins afuera), `n_agentes = 2`.
Ningún SKIP publicó.

**Dos hallazgos, no corregidos (orden: reportar y ALTO):** (1) el corpus se construyó con un
string **vacío** y con **`[assistant]`** — `_interact:532` chequea `if text is None` y un vacío
no es None; (2) **F3a no era alcanzable desde el camino vivo** (los dos entry points construyen
`CKMMonitor()` sin argumentos), resuelto con un launcher por vivo que gana la carrera del
singleton, sin tocar `server.py` ni `mcp_server.py`.

Sin W: 2 textos y `min_texts = 3`. Es el precio del `state_dir` aislado, declarado.

Antes: **CP2b — el criterio local, con los cuatro ajustes de Opus.** Cerrado el 2026-10-09. Suite
**418/418**. Ajustes: `piso_ticks`→`piso_vueltas` (el nombre decía ticks y medía vueltas);
`ValueError` si `piso_vueltas ≤ 0` (el docstring decía "no opcional" y el constructor dejaba
apagarlo); publicar exige `INTERACT` explícito (`_interact` ya no cae a publicar); `-1` → `None`
para "nunca llamó". Cuatro inversiones, las cuatro rompen. Control de Opus verificado: al valor
0 no se llega por construcción.

**El enunciado de la absorción cambió y dice más:** con el `> 0` fuera de `evaluar`, un `0`
dispararía el piso *siempre*. La absorción se exhibe con un **piso fuera del horizonte** — que
el piso sea finito no alcanza, tiene que caer dentro de la ventana observada. Umbral a
Calibración, medida: **`piso_vueltas + 2 ≤ vueltas por device`** — y las vueltas son **por
device**, no el total del vivo. El vivo 02 tuvo **11 y 12** por device (23 era el total entre los
dos: leí un agregado como conteo por unidad). Con el default 12 harían falta **14**, así que el
piso por default **no habría disparado nunca** en un vivo de 60 s con poll 5: tiene que ser ≤ 9. El panel declara `piso_dentro_del_horizonte`: si hubo skips y el piso no disparó, la
corrida **no puede decir** si el silencio era absorbente.

Antes: **CP2b sin los ajustes.** Suite **412/412**, 33 tests nuevos en
`tests/test_criterio_local.py`, módulo nuevo `iap_chatroom/criterio_local.py`, **cinco
inversiones** (la del piso rompe 5 tests, no 1). Las cuatro propiedades de Opus cubiertas:
registra el salto con su motivo y distinguible de `OP_SILENCE` (`DECISION_SKIP`, tercer valor);
el **piso determinístico** deja pasar a D con el canal callado; la auditoría mira **las dos
caras**; los umbrales se declaran **no calibrados en el panel**.

Hallazgo del instrumento: **`_interact` cae por default a publicar**, así que el skip publicaba
un mensaje. Corregido con su rama; el fallthrough queda reportado y no corregido de paso.

Divergencia medida con Opus: las dos tasas van declaradas, pero el muestreo de la **cara del
pase no cuesta una llamada** (ya se hizo), así que esa cara lleva muestra **y** censo.

El filtro queda **apagado por default**: con él puesto por default, la línea de base del vivo 02
dejaría de ser comparable sin que nada lo dijera.

Antes: **CP2v — preparación del primer vivo.** Cerrado el 2026-10-09. Suite **360/360**, nueve
inversiones (dos repetidas porque no se habían aplicado). Llamadas contadas y no inferidas; las
dos ausencias de `_decide` a UNKNOWN; la respuesta cruda con su causa; el 429 por `status_code`
con el método declarado; el ritmo declarado sin inventar el límite. **El `ProviderStub` agotado
fabricaba decisiones** y se corrigió. **Un cambio del gate: el timestamp ausente pasó de `[?]` a
`[UNKNOWN]`** — delamor lo lee antes del vivo.

Antes: **CP2a″ — la ventana en tiempo. Con esto el CP2a queda cerrado.** Cerrado el 2026-10-09.
Suite **338/338**. `since = t − periodo_s`: el borde `timestamp == since` se cierra sin tocar
`get_messages`. Dos preguntas de delamor cambiaron el diseño: el fallback `or 0.0` reintroducía
el agujero, y levantar mataba el instrumento — quedó **UNKNOWN y el corte no avanza**.

Antes: **CP2a′ — el borde de T2, el join y dos devices.** Cerrado el 2026-10-09. Suite **326/326**.
Implementado el solape de una vuelta que propuso Opus. **El test con reloj congelado que pidió
no puede pasar con el solape, y lo medí**: con el reloj quieto todos los cortes son el mismo
número, así que mover cuál se usa no cambia nada. Escrito midiendo el agujero, no evitándolo.
**Escalado: el arreglo sería `>=` en `get_messages`, que el enunciado excluyó.**

Antes: **CP2a — el ODA continuo, sin criterio local.** Cerrado el 2026-10-09. Suite **321/321**,
ocho inversiones. `trigger_mode="continuo"` como único modo, una decisión por vuelta, el
silencio no absorbente, LEAVE como decisión, y el `since` del reloj del canal leído antes de
`get_messages`. **La inversión 19 no rompía porque `_observe` pedía el clock y el loop lo
sobreescribía**: código redundante que ningún test podía distinguir. Arreglado en el código.
**Tocó sólo `iap_chatroom/`.**

Antes: **CP1 — el CLOCK del canal.** Cerrado el 2026-10-08. Suite **304/304**, cinco inversiones.
El canal genera los ticks con su reloj de pared UTC, la Config los registra, y cada tiempo
declara su procedencia. **La inversión 10 no rompía**: nada protegía que el reloj del canal
fuera el que sella los mensajes. Cerrado con dos tests nuevos.

Antes: **CP0b — freeze de la serie IAP.** Cerrado el 2026-10-08.
Copia en `process/iap_series_freeze_20261008/` (67 archivos, 620 KB), verificada por `diff`.
**Los originales no se tocaron**: `git status` sobre `iap_chatroom/` y `registers/` da vacío.

Antes: **CP0 — evaluar contra el repo, sin código.** Cerrado el 2026-10-08, commit `8151298`,
aceptado en `2ad873e`.


## Qué espera, y de quién

- **Nada bloqueante.** El borde se cerró con la ventana en tiempo, sin tocar `get_messages`: el
  `>=` ya no hace falta y no se escala.

- **Nada bloqueante.** El CLOCK quedó decidido (E3, `f07a9dc`) e implementado en el CP1.
- Sin implementar hasta el OK de delamor: **el criterio local sin LLM** y **WAIT** (TASK §1).

## Próximo paso

**El primer vivo con Groq**, que **no es mío**: necesita la clave como secret del Codespace, el
límite de la cuenta, y que delamor lea el gate. Después, **CP2b**.

Lo que sigue después del vivo: **CP2b — el criterio local encima** (OK de delamor, `e737e78`): `skip` registrado con su motivo,
auditoría **al azar sobre las dos caras**, umbrales declarados "no calibrados", y el test que
pide delamor: en silencio y con objetivo, el filtro **igual** deja pasar a D alguna vez — que el
filtro no vuelva absorbente el silencio.

Los tres requisitos del CP2 quedaron cumplidos en el CP2a: el `since` del canal, el clock
observado en silencio, y `get_messages` probado con el `since` real del device.

**Después:** el CP3 (el caso Z, de delamor) y la corrida viva, que espera las claves. El costo
estimado está reportado y lo decide delamor.

## Base

`eb32605`. Suite al arrancar 284/284, al cerrar el CP1 **304/304**.

## Nada quedó a medias

El CP1 se cerró entero. `grep -c INVERSION` sobre `channel.py`, `ckm_landscape_config.py`,
`monitor_service.py` y `ckm_monitor.py` → 0, 0, 0, 0.
Y la diferencia 64/67 del CP0b quedó resuelta con nombre: eran **6** `.pyc` de
`providers/__pycache__/`, borrados; la carpeta quedó en 62 y 62.
