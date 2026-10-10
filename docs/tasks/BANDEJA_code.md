# BANDEJA_code

*Canal Code → Opus (→ delamor si escala). Protocolo: `PROTOCOLO_code_continuidad_v1.md` §6.*
*Se agrega al final. No se editan las entradas anteriores. Cada entrada lleva fecha y hora UTC y su tipo.*

---
## ARRANQUE — 2026-10-07 03:54 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 del protocolo.*

### Revisé

1. **Locks.** `find .git -name "*.lock"` → ninguno. No borré nada.
2. **`git pull origin main`** → limpio, sin conflictos, 6 commits nuevos, HEAD en `5aac176`
   (*docs(lab): Laboratorio de W*). Entraron los 6 esperados.
3. **`git status`** → ningún archivo modificado ni en staging. Sólo no trackeados, todos
   conocidos y de antes (`LETTER.md`, `baseline_d_ckm.{py,json}`, PDFs y docs de `docs/`,
   `monitor_trajectory.jsonl`, `scripts/`, `tests/run_tests.sh`, tres `NOTA_armstrong_*`).
4. **`ESTADO_*.md`** → no existía ninguno. Creado `ESTADO_CKMlandscapeConfig_v3.md` en esta
   sesión, como pide el enunciado.
5. **Bandeja y decisiones** → `BANDEJA_code.md` vacía (sólo cabecera).
   `DECISIONES_opus.md` con dos decisiones del 2026-10-07 (la clase v1 renombrada hasta el
   CP3; el laboratorio en `docs/lab/`). Las dos leídas y respetadas.
6. **Archivos de salida de la última corrida.** `monitor_trajectory.jsonl` (raíz, 76 líneas)
   y `iap_chatroom/_state/monitor_trajectory.jsonl` (4 líneas): **las dos últimas líneas
   parsean como JSON completo**, ninguna truncada. Ninguno de los dos lleva marca de
   "terminó" — el formato no la tiene.
7. **Tests de la TASK abierta.** Los cuatro existen y los leí:
   `tests/test_ckm_landscape_config.py` (71 líneas), `test_gatekeeper_c1.py` (107),
   `test_landscape_config_en_runs.py` (88), `test_rebuild_consulta_w_version.py` (113).

### Encontré

- **No existía ningún `ESTADO_*.md`.** El protocolo es del 7 oct y esta es la primera sesión
  de Code bajo él, así que la ausencia es esperable, no un corte.
- **`CKMlandscapeConfig_v`** aparece en `services/ckm_landscape_config.py` y en
  `tests/test_ckm_landscape_config.py`: es el prefijo de versión interno, no otra clase.
- **`monitor_trajectory.jsonl` en la raíz del repo está sin trackear.** No lo commiteé:
  por `project_untracked_no_commit` los datos informativos no se commitean. Lo digo porque
  es salida de corrida y alguien podría buscarla en el repo.

### No pude revisar

- **No corrí los tests.** El enunciado dice "CP0 (lectura, sin código)" y el CP0 de la TASK
  son cuatro puntos de lectura. Correr la suite es ejecución, así que no la corrí; los tests
  los leí. Si el chequeo §2.5 pedía correrlos, decímelo y los corro: es un comando.
- **Los tres `NOTA_armstrong_hallazgos_implicancias_20260825*.md`** en `registers/` siguen
  sin trackear y con md5 distinto cada uno (no son copias). No sé si son pendientes; no los
  toqué porque `registers/` es Clase R.

---

## REPORTE CP0 — 2026-10-07 03:54 UTC

*TASK: `TASK_CKMlandscapeConfig_v3.md` §3.CP0. Leído también `TASK_CKMlandscapeConfig_v2.md`
(criterio, tres clases, I1–I7, transición única). Base: `5aac176`.*

### Punto 1 — Consumidores de la clase v1

Busqué con `grep -rn "CKMlandscapeConfig\|ckm_landscape_config" --include="*.py"` sobre todo
el árbol, sin `__pycache__`. **La lista de la TASK se confirma exacta y no hay ninguno más.**

| consumidor | qué usa |
|---|---|
| `services/monitor_service.py` | import (L44), tipo del parámetro (L79), el **campo** `.sampling_mode` para validar contra el suyo (L117), y **`.to_dict()`** en el panel (L215-217). **No usa `from_W`.** |
| `experiments/replay_sesion_trust.py` | **`from_W`** (L139) y luego **campos sueltos**: `.mu_W_nonzero`, `.mu_W_global`, `.beta_c_nonzero`, `.beta_c_global`, `.w_version_id`, `.theta_W`, `.sampling_mode`. Sólo para imprimir. |
| `P1P4/run_conteo_vs_masa_04oct/conteo_vs_masa.py` | **`from_W`** (L51) y **`.to_dict()`** (L52), que serializa plano al JSONL. Ya corrido; no se toca. |
| `services/gatekeeper_c1.py` | **nada.** Ver divergencia abajo. |
| `tests/test_ckm_landscape_config.py` | `from_W` ×2, `theta_W_formula` ×2, `to_json`/`from_json`, `.w_version_id` ×4, `.mu_W_nonzero`, `.mu_W_global`, `.beta_c_global`, `.beta_c_corpus` |
| `tests/test_gatekeeper_c1.py` | `from_W` ×1, `.mu_W_nonzero` ×2, `.mu_W_global` |
| `tests/test_landscape_config_en_runs.py` | `from_W` ×3, `from_dict` ×1 |
| `tests/test_rebuild_consulta_w_version.py` | `from_W` ×1, `.w_version_id` |

**Divergencia con la TASK.** `services/gatekeeper_c1.py` **no importa** la config. Sus únicos
imports son `__future__` y `numpy` (L16, L18). La única aparición de `CKMlandscapeConfig` es
en el docstring, L12: *"theta_W es obligatorio y sin fórmula (CKMlandscapeConfig.theta_W_formula
…)"*. `theta_W` entra como parámetro suelto a `c1()`. **En el CP3 no hay nada que migrar ahí**,
sólo una referencia de docstring a revisar si `theta_W_formula` cambia de lugar.

### Punto 2 — Concurrencia real

**Hay concurrencia de hilos, en un mismo proceso. No hay consumidores en procesos distintos.**
Medido así:

- **Un solo proceso.** `iap_chatroom/server.py:58` → `uvicorn.run(app, ...)` **sin `workers=`**.
  `mcp_server.py` **no tiene `__main__`**, no corre standalone. No hay otro entry point.
- **Una sola instancia.** `api_routes.py:20`, `mcp_server.py:23`, `ui_gradio.py:22` y
  `server.py:31` hacen cada uno `CKMMonitor()` — parecían cuatro, pero `CKMMonitor` es
  **singleton real** por `__new__` + guarda `_initialized` (`ckm_monitor.py:41-53`). Las cuatro
  llamadas devuelven el mismo objeto, con un solo `MonitorService`. *Lo verifiqué porque de
  entrada me pareció que eran cuatro monitores distintos; no lo son.*
- **El hilo existe y es periódico.** `ui_gradio.py:85-86` → `gr.Timer(value=3)` +
  `timer.tick(_refresh_state, ...)`, y `_refresh_state` (L48) es **`def` sync** y llama a
  `ckm_monitor.get_state()`. En la gradio instalada (**6.20.0**) las funciones sync se
  despachan con **`anyio.to_thread.run_sync`** (verificado leyendo `gradio/blocks.py`), o sea
  **en un hilo worker**. El escritor, `CKMMonitor.on_message`, corre en el event loop:
  `channel.publish` invoca los callbacks **sincrónicamente** (`channel.py`, `callback(message)`,
  sin `await` en el medio). **Lector en hilo + escritor en el loop, cada 3 segundos.**
- **`ProcessPoolExecutor` no cuenta.** `experiments/stochastic_attractor_eval.py:165` hace
  `pool.submit(run_one, W, seed, n_runs)`: los workers reciben un array y computan; no ven
  ninguna config, y la escritura queda en el proceso padre. Coincide con su docstring.
  `grep` de `to_thread|run_in_executor` en `iap_chatroom/` → cero.

**Consecuencia, según TASK §2:** cae en la primera rama — *"el reemplazo y la lectura van bajo
un mismo lock"*. **No cae en la segunda** (procesos distintos), así que **no se escala**.

### Punto 3 — Serializaciones históricas de la config v1

- **Con contenido real, una sola:** `P1P4/run_conteo_vs_masa_04oct/log_conteo_vs_masa.jsonl`,
  registro `tipo: "config"`, **dict plano de v1** con las claves
  `N, nodes?, mu_W_nonzero, mu_W_global, beta_c_nonzero, beta_c_global, w_version_id,
  theta_W, scale, sampling_mode, config_id, timestamp` (+ `mode` y `nota_theta_W` del driver).
- **Paneles:** `monitor_trajectory.jsonl` (raíz, 76 líneas) lleva `landscape_config` **anidado
  dentro de `panel`**, y en las 76 vale **`None`**. `iap_chatroom/_state/monitor_trajectory.jsonl`
  (4 líneas) no lleva la clave. **Ningún panel histórico tiene config con contenido**, porque
  `CKMMonitor` nunca le pasa `landscape_config` a `MonitorService`.
  *Corrección mía en el camino: primero busqué la clave al tope del registro y reporté 0/76;
  está bajo `panel`. El número de configs no nulas no cambia (0), el nivel sí.*

**Cómo se leen después del cambio (default declarado, P4 abajo):** el registro plano de v1 se
lee como **(identidad, declarado, un único ciclo)** con `causa="bootstrap"`, `t_señal=None`,
`t_rebuild=timestamp`. Es un mapeo de lectura documentado; **no se reescribe ningún archivo**.

### Punto 4 — Lo medido de v1 contra v2

Sobre `services/W_ckm_corpus_v2.json`, con la clase v1 actual:

```
N                 32
mu_W_nonzero      0.005977   ← coincide con el declarado en la TASK
mu_W_global       0.004519   ← coincide con el declarado en la TASK
beta_c_nonzero   10.457544
beta_c_global    13.831845
w_version_id      a1c6c6b978fc6c8a…
```

**Los dos μ_W coinciden exactos** con los de la TASK. Los β_c quedan registrados acá como
línea de base para el CP1 (la TASK sólo declaraba los μ_W). La igualdad
`beta_c_global == COCO.beta_c_corpus()` está en el test de v1 y **no la volví a correr**: es
ejecución.

---

## PREGUNTA P1 — NO BLOQUEA — 2026-10-07 03:54 UTC

**¿Qué pasa con `theta_W_formula` cuando v2 reemplaza a v1 (D1)?** Es un `@staticmethod`
(`ckm_landscape_config.py:95`), la usan 2 asserts de `test_ckm_landscape_config.py`, y el
docstring de `gatekeeper_c1.py:12` la nombra. La API propuesta en la v2 no la lista, y las dos
TASKs dicen que no definen la fórmula de θ_W.

**Default declarado y reversible:** la llevo igual a la clase nueva, **sin cambiarle nada**.
Es una función pura sin estado y no define nada nuevo. Revertir: borrarla y ajustar los dos
asserts.

## PREGUNTA P2 — NO BLOQUEA — 2026-10-07 03:54 UTC

**El CP3 dice "migrar `gatekeeper_c1.py`", pero no hay nada que migrar** (Punto 1).

**Default declarado y reversible:** en el CP3 no lo toco, salvo la referencia del docstring si
`theta_W_formula` se mueve. Revertir: trivial, es una línea de comentario.

## PREGUNTA P3 — **BLOQUEA** — 2026-10-07 03:54 UTC — **[delamor]**

**¿Quién construye la `CKMlandscapeConfig` en el canal IAP vivo?**

`CKMMonitor.__init__` crea el `MonitorService` **sin** `landscape_config`
(`ckm_monitor.py:77-81`), así que en vivo la config es `None`: los 76 paneles históricos lo
confirman (Punto 3). D4 dice *"Monitor abre el ciclo"*, pero **hoy, en el canal, no hay config
sobre la cual abrirlo**. Construirla dentro de `CKMMonitor` cambia lo que el canal instrumenta
y qué queda en cada panel, así que no lo decido.

**Por qué BLOQUEA y dónde:** bloquea el **CP2**, no el CP1. El CP1 es la clase nueva sin tocar
consumidores y **puede cerrarse sin esta respuesta**. Si se contesta antes del CP2, no frena nada.

**Lo que hace falta decidir:** (i) si `CKMMonitor` la construye, con qué `theta_W`,
`sampling_mode` y `scale` — y `theta_W` no tiene fórmula (D6: la calibración es un proceso
aparte); o (ii) si el canal sigue sin config y D4 sólo aplica a los runs que la reciben de
afuera.

## PREGUNTA P4 — NO BLOQUEA — 2026-10-07 03:54 UTC

**El mapeo de lectura de los registros planos de v1** (Punto 3): plano →
(identidad, declarado, ciclo único con `causa="bootstrap"`, `t_señal=None`,
`t_rebuild=timestamp`).

**Default declarado y reversible:** lo documento en el CP1 como función de lectura y **no
reescribo ningún archivo histórico**. Revertir: borrar la función; los datos quedan intactos.

---

## NOTA — push, 2026-10-07 03:54 UTC

El enunciado de esta sesión decía "no hagas push", y después delamor pidió por chat
**"hacé push de la bandeja así recibo local en el repo"**. Pusheo a la rama **`code/trabajo`**,
no a `main`, porque es lo que el protocolo §6(b) prevé para cuando pushea Code. Para traerlo:

```
git fetch origin code/trabajo && git log origin/code/trabajo -1
```

Si se prefiere que vaya a `main`, se dice y lo hago.

---

## REPORTE CP1 — 2026-10-07 04:09 UTC

*TASK `TASK_CKMlandscapeConfig_v3.md` §3.CP1, sobre `21ba45c`, rama `code/trabajo`.
Leídas las decisiones de Opus y la respuesta de delamor a P3 antes de escribir.*

### Lo que quedó en el código

`services/ckm_landscape_config.py`, 480 líneas:

| | qué es |
|---|---|
| `medido(W)` | función de W sola (I5). Devuelve `N`, los dos `mu_W` y los dos `beta_c`. |
| `Ciclo` | `frozen=True`: `w_version_id`, lo medido, `causa`, `t_senal`, `t_rebuild`, `deriva` como property. Valida I6 en `__post_init__`. |
| `CKMlandscapeConfig` | identidad + declarado + tupla de ciclos, con `threading.RLock`. |
| `ciclo_desde_registro_plano_v1` | el mapeo de lectura de P4. |
| `CKMlandscapeConfigV1` | la vieja, renombrada y **sin tocar**. Sale en el CP3. |

**El lock cubre lo que Opus pidió:** `ciclo_vigente`, `panel()` y el reemplazo dentro
de `abrir_ciclo` toman el mismo `RLock`. El reemplazo es **un solo cambio de
referencia** de la tupla de ciclos, así que un lector nunca ve una tupla a medio
armar (I1 + D3).

**θ_W no está en la clase nueva**, ni como campo de `Ciclo` ni de la config, ni en
`to_dict()`. `theta_W_formula` se quedó en `CKMlandscapeConfigV1`, que es la que
conserva θ_W como traza. Esto **corrige el default de P1**, como indicó Opus.

**`scale` es opcional y `sampling_mode` obligatorio**, por I4 revisada. Hay un test
que lo fija.

### Tests

`tests/test_ckm_landscape_config_ciclos.py`, 355 líneas, **31 tests, 31 pasan**.
Cubre I1 (×3), I2 (×3), I3, I4 (×5), I5 (×3), I6 (×4), I7 (×2), D2, D3 (×2),
valores medidos (×3), serialización con historia (×2) y lectura de la traza vieja (×2).

**De los dos tests de hilos, uno puede fallar y el otro no detecta. Medido, no
supuesto.** Los dos corren un hilo que lee en bucle (`ciclo_vigente` en uno,
`panel()` en el otro) mientras el principal abre 200 ciclos alternando dos W.

Primero escribí en esta misma entrada que los había probado sin el lock. **No lo
había hecho.** Lo corrí antes de commitear: desactivé el lock y partí el reemplazo
en dos pasos (dejando un estado intermedio con el `mu_W_global` equivocado), y
corrí tres veces.

| test | sin lock ni reemplazo atómico |
|---|---|
| `test_D3_el_get_nunca_devuelve_un_ciclo_mezclado` | **falla 3/3** |
| `test_D3_el_panel_no_se_parte_con_un_set_concurrente` | **pasa 3/3 — no detecta** |

El primero es el test. El segundo compara el **conjunto de claves** del
`ciclo_vigente` del panel, y ese conjunto no cambia aunque el valor esté mezclado:
no puede fallar en la dirección que importa. Lo dejo, porque sí cubre que el panel
nunca venga con `ciclo_vigente: None` a mitad de un set, pero **no lo cuento como
verificación del lock**. Con el lock puesto, los dos dan 0 en todas las corridas.

El test de valores medidos compara contra `COCO(W=W).beta_c_corpus()`, que es el
método de instancia; primero lo escribí como si fuera estático y falló. Corregido.

**Suite completa: 214/214 en verde** (`python3 -m pytest tests/ -q`).

### Lo que cambié fuera de la clase

El rename hace que `CKMlandscapeConfig` apunte a la clase nueva, que **no tiene
`from_W`**. Eso rompió 15 tests de golpe. Lo resolví **redirigiendo a
`CKMlandscapeConfigV1`** cuatro archivos de test y `experiments/replay_sesion_trust.py`:
sólo el nombre de la clase, ninguna lógica. **No puse ningún shim de compatibilidad**
en la clase nueva, por `chau regresión`.

**`services/monitor_service.py` no se tocó y no se rompió.** Usa sólo
`.sampling_mode` y `.to_dict()`, y las dos existen en la clase nueva.
`test_monitor_services.py` da 36/36 sin cambios.

**Aviso, no pregunta:** `P1P4/run_conteo_vs_masa_04oct/conteo_vs_masa.py` llama a
`from_W` y **se rompería si se volviera a correr**. No lo toqué: la TASK dice que los
experimentos ya corridos no se tocan. Su JSONL se sigue leyendo con
`ciclo_desde_registro_plano_v1`, y hay un test que lo lee de verdad.

---

## PREGUNTA P5 — NO BLOQUEA — 2026-10-07 04:09 UTC

**`nodes` está en la clase "medido" de la TASK v2, pero no es función de W.**
La v2 lista `nodes` entre los campos medidos, e I5 dice que `medido(W)` es función de
W sola. W no lleva etiquetas de nodos: vienen del `NodeExtractor`. Y la v1 tampoco
tenía `nodes`. Las dos cosas no pueden valer juntas.

**Default declarado y reversible:** `nodes` **queda afuera** del `Ciclo`, que así
cumple I5 exacto. Si hace falta, entra como campo **declarado** del lado de quien
tiene las etiquetas. Revertir: agregarlo al `Ciclo` como parámetro de `abrir_ciclo`,
y entonces I5 hay que reescribirla.

## PREGUNTA P6 — NO BLOQUEA — 2026-10-07 04:09 UTC

**`t_senal` va sin tilde.** La spec de la v2 escribe `t_señal`. Busqué precedente:
en `services/` **ningún identificador lleva tilde o ñ** — las que aparecen son todas
de docstrings. Los campos son `sampling_mode`, `mu_W_nonzero`, `w_version_id`.

**Default declarado y reversible:** el campo se llama **`t_senal`**, y queda así en
el JSON serializado. Revertir: renombrar el campo y la clave (toca `Ciclo`, los tests
y cualquier JSON ya escrito con la clave vieja — todavía no hay ninguno).

---

## NOTA — rama y CRLF, 2026-10-07 04:09 UTC

- Trabajo y pusheo en **`code/trabajo`**, nunca `main`, por §6 decidido.
- La bandeja volvió del clon local **con CRLF**. El diff de 402 líneas del pull fue
  sólo eso: mis seis entradas quedaron intactas, nadie editó nada. **Mantengo CRLF**
  al agregar, para que el diff muestre sólo lo nuevo.

---

## REPORTE CP2 — 2026-10-07 04:34 UTC

*TASK `TASK_CKMlandscapeConfig_v3.md` §3.CP2, sobre `202488a`, rama `code/trabajo`.
Incluye lo que Opus agregó al CP2: que `CKMMonitor` construya la Config sin θ_W ni
scale, y que Monitor llame a `abrir_ciclo` en `_invalidar_si_W_cambio`.*

### Lo que quedó cableado

**`services/monitor_service.py`**

- `_invalidar_si_W_cambio` **abre el ciclo (D4)**, en el mismo bloque donde descarta
  Δ_r y A0. La causa que viaja al ciclo es **la misma que el método devuelve**
  (`"N" | "nodos" | "pesos"`): `Ciclo.causa` es str libre, así que el vocabulario fino
  de Monitor entra sin traducirse al de la v2 (`rebuild` | `estructural` | `volumen`).
- Dos helpers: `_causa_cambio` (la clasificación que ya estaba inline) y
  `_abrir_ciclo_si_cambio`.
- **Primera evaluación:** Δ_r no tiene nada que descartar, pero la config sí puede
  estar atrás —se construyó con una W y W cambió antes de la primera llamada—, así que
  ahí también se abre ciclo.
- **Config sin ciclos:** Monitor abre el primero con causa `"bootstrap"`.
- **El panel lleva `config.panel()`**, no `to_dict()` (I7).

**`iap_chatroom/ckm_monitor.py`**

`CKMMonitor` construye `CKMlandscapeConfig(sampling_mode="uniform")` **sin W**: el
corpus arranca en acumulación y W aparece recién al cruzar `min_texts`, así que no hay
nada que medir en `__init__`. Sin θ_W ni `scale`. El primer ciclo lo abre Monitor.

### Tests, y qué pasa sin el CP2

`tests/test_monitor_abre_ciclos.py`, 13 tests. **Medido**: restauré
`services/monitor_service.py` y `iap_chatroom/ckm_monitor.py` a `202488a` y volví a
correr.

| | con CP2 | sin CP2 |
|---|---|---|
| `test_monitor_abre_ciclos.py` | **13 pasan** | **12 fallan, 1 pasa** |
| suite completa | **227/227** | — |

El único que pasa sin el CP2 es `test_sin_config_el_rebuild_no_rompe_nada`, que es el
control: sin config no debe cambiar nada.

**Dos de mis tests pasaban sin el CP2 por la razón equivocada, y los corregí** después
de medirlo, no antes:

- `test_la_deriva_del_ciclo_que_abre_monitor_es_nula` pasaba porque el ciclo bootstrap
  también tiene `t_senal = None`. Le agregué `len(ciclos) == 2` y
  `causa != "bootstrap"` antes de mirar la deriva.
- `test_sin_cambio_de_W_no_se_abre_ciclo` pasaba trivialmente: sin el CP2 nunca se abre
  ningún ciclo, así que "no se abrió ninguno" era cierto por el motivo opuesto. Le
  agregué la segunda mitad, que fuerza un rebuild y exige que ahí sí abra.

Es el mismo mecanismo del `test_D3_el_panel_no_se_parte` del CP1. Esta vez lo busqué.

### Un test mío tenía mal la expectativa, no el código

Escribí `test_el_canal_abre_el_bootstrap_y_despues_los_rebuilds` esperando que el canal
abriera varios ciclos. **Falló: el canal abre uno solo.** No es un fallo del CP2:
`CKMMonitor` construye su `CorpusService` con **`rebuild_suspendido=True`** (decisión de
delamor: *W se construye cuando el dato distingue y no se reconstruye por mensaje*), así
que W no vuelve a cambiar y D4 no tiene nada más que abrir.

Reescribí el test para que afirme lo que **se mide**: un solo ciclo con
`rebuild_suspendido=True`, y —levantando la suspensión a mano, declarado en el test— un
ciclo nuevo al siguiente mensaje. Sin esa segunda mitad el test no podría fallar.

**Consecuencia para el canal vivo, medida y sin interpretar:** la Config del canal va a
tener **un solo ciclo**, el bootstrap. D4 queda cableado y sin nada que abrir hasta que
alguien levante `rebuild_suspendido`. No lo levanto: es decisión de delamor.

### El único test que cambió

`tests/test_landscape_config_en_runs.py`, porque Monitor ya no recibe la clase
congelada. Qué cambió exactamente:

- `CKMlandscapeConfigV1.from_W(W, theta_W=..., sampling_mode=..., scale=...)` →
  `CKMlandscapeConfig.create(W, sampling_mode=..., scale=...)`. θ_W ya no existe.
- `test_con_config_cada_linea_recarga_igual`: antes recargaba la config entera de cada
  línea y la comparaba con `==`. Ahora el panel lleva `panel()` (I7), así que compara
  `config_id`, `sampling_mode`, que **no** venga `ciclos`, y que el `ciclo_vigente`
  recargue igual. **Lo que verificaba —que cada línea lleva la config que produjo ese
  panel— se sigue verificando**; lo que cambió es que ya no viaja la historia.
- Los otros tres tests sólo cambian la construcción.

Los demás tests de Monitor (`test_monitor_services.py`, 36) **no se tocaron y pasan**.

---

## PREGUNTA P7 — NO BLOQUEA — 2026-10-07 04:34 UTC

**La causa del cambio de W no siempre es derivable contra la config**, y es una
consecuencia de P5 que no estaba vista cuando se aceptó.

`CorpusService.w_change_since(sha, nodes)` **necesita las etiquetas del que consulta**,
porque los nodos por versión no se persisten. El `Ciclo` guarda `N` pero **no** `nodes`
(P5, porque no es función de W). Entonces, cuando hay que calcular la causa contra el
ciclo vigente —el caso de la primera evaluación con la config atrás— sólo se puede
distinguir `"N"`. Con N igual, no se puede saber si cambiaron las etiquetas o sólo los
pesos.

Esto **no afecta** el camino normal: cuando Monitor detecta el cambio, usa su propio
`_w_nodes` y la causa sale fina (`"N" | "nodos" | "pesos"`).

**Default declarado y reversible:** en ese caso la causa es **`"W_distinta"`** — el sha
es otro, y con lo que el ciclo guarda no se puede decir más. **No inventé una causa más
precisa.** Revertir: meter `nodes` en el `Ciclo` (que es revertir P5 y reescribir I5),
o persistir los nodos por versión en `CorpusService`, que es otra TASK.

---

## ARRANQUE — 2026-10-08 00:13 UTC

*Claude Opus 5 (Code, Codespace `ckm`), rama `code/trabajo`. Chequeo §2 + §8.*

### Revisé

1. **Locks.** `find .git -name "*.lock"` → ninguno.
2. **`git pull origin main`** → al día, nada nuevo. HEAD en `c96f752`
   (*Merge origin/main — TASKs y protocolo del canal IAP*). Las dos ramas sincronizadas:
   `git log HEAD..origin/main` vacío.
3. **`git status`** → nada modificado ni en staging. Los no trackeados son los 27 conocidos.
4. **`ESTADO_CKMlandscapeConfig_v3.md`** → último CP cerrado: **CP2**, el 2026-10-07, sobre
   `202488a`. Próximo paso: CP3, habilitado.
5. **`DECISIONES_opus.md` (§8)** → leído. Las decisiones del CP0, CP1 y CP2 están, más el
   criterio del CP3 (L47) y su habilitación (L54).
6. **Archivos de salida.** `monitor_trajectory.jsonl` (raíz, 76 líneas) y
   `iap_chatroom/_state/monitor_trajectory.jsonl` (4 líneas): **la última línea de cada uno
   parsea como JSON completo**, ninguna truncada. Ninguno lleva marca de "terminó": el formato
   no la tiene.
7. **Tests.** Suite completa: **227/227**, en verde, sin cambios desde el cierre del CP2.

### Preguntas abiertas

**Ninguna. P1–P7 están respondidas**, cada una con un `Pn` que la nombra en `DECISIONES_opus.md`:

| | respuesta |
|---|---|
| **P1** `theta_W_formula` | aceptada, y **corregida después**: sale con V1 cuando θ_W salió de la Config |
| **P2** `gatekeeper_c1.py` | aceptada: no se toca en el CP3, salvo el docstring |
| **P3** quién construye la Config en el canal | escalada a delamor (E3/E4) y **resuelta**: opción (iv) |
| **P4** lectura de los registros planos de v1 | aceptada: función de lectura, no reescribe nada |
| **P5** `nodes` fuera del `Ciclo` | aceptada |
| **P6** `t_senal` sin tilde | aceptada |
| **P7** causa `"W_distinta"` | aceptada, con un **error de Opus declarado**: al aceptar P5 no vio que sin `nodes` la causa no siempre se deriva |

**Ningún default quedó vigente sin decisión.** No hay nada que arrastrar como
`Pn — DEFAULT VIGENTE, SIN DECISIÓN`.

### Encontré

- **Las dos ramas ya estaban sincronizadas al arrancar**, así que el punto 2 de §8 —*la
  respuesta que no llega a quien pregunta*— no se dio: las decisiones del CP2 estaban visibles
  antes de empezar.

### No pude revisar

- Nada quedó sin revisar en este arranque.

---

## CORTE — 2026-10-08 00:13 UTC

*Lo que la sesión anterior dejó a medias, detectado al arrancar (§6, tipo `CORTE`).*

**1. La sesión anterior no escribió su `ARRANQUE` en la bandeja.** Hizo el chequeo —corrió la
suite, leyó el ESTADO y las decisiones— pero **lo reportó en el chat**, que no es el canal. Las
entradas `REPORTE CP1` y `REPORTE CP2` sí quedaron escritas; el arranque, no. Es exactamente lo
que §2 previene: el chequeo existió y no quedó traza de él en el repo, así que desde la bandeja
no se puede saber qué se revisó antes del CP1.

**2. El Codespace se paró.** Por eso esta sesión arranca de nuevo. **No hubo daño:** el CP2 se
cerró entero en `17b6421` y se pusheó, el ESTADO estaba escrito, y el árbol quedó limpio. Es el
diseño de §0 funcionando — cortar en cualquier punto no dejó nada a medias.

**3. Lo que no se perdió por poco.** El merge de `main` en `code/trabajo` (`c96f752`) se hizo
en el último minuto de la sesión anterior, a pedido de delamor. Sin ese push, los 7 commits de
documentación de `main` seguirían fuera de la rama de trabajo y este arranque habría leído un
protocolo sin §8 — es decir, no habría listado las preguntas abiertas.

**Lo que esta sesión hace distinto:** el `ARRANQUE` va a la bandeja **antes** de tocar el CP3,
y con su propio commit.

---

## REPORTE CP3 — 2026-10-08 00:18 UTC

*TASK `TASK_CKMlandscapeConfig_v3.md` §3.CP3, sobre `079df6c`, rama `code/trabajo`.
Ejecutado según el criterio de `DECISIONES_opus.md` L47.*

**La TASK queda cerrada.** No quedan CPs.

### Punto por punto, contra el criterio

**1. El test de V1 se fue con V1 — pero verifiqué la cobertura antes**, que era la condición.
De sus 7 tests:

| test de V1 | ¿estaba cubierto en los de ciclos? |
|---|---|
| `test_mu_W_ambas_formas` | sí — `test_medido_coincide_con_los_valores_declarados` |
| `test_beta_c_global_coincide_con_coco` | sí — mismo nombre |
| `test_parametros_obligatorios` | sí, con la semántica nueva: `sampling_mode` obligatorio, `scale` opcional, θ_W ya no existe |
| `test_json_roundtrip` | sí — `test_serializacion_completa_recarga_igual` |
| `test_theta_W_formula_no_implementada` | se va con la fórmula, por criterio |
| **`test_identidades`** | **no** → migrado |
| **`test_w_version_id_cambia_con_W`** | **sólo implícito** → migrado explícito |

Los dos últimos están ahora en `test_ckm_landscape_config_ciclos.py` como
`test_identidades_dos_configs_sobre_la_misma_W` y `test_el_w_version_id_cambia_con_W`.
**Sin esa verificación se habrían perdido dos casos**, y el criterio pedía exactamente eso.

**2. Los que usaban V1 como herramienta migraron.**
`test_gatekeeper_c1.py` sólo necesitaba los μ_W, así que va a **`medido(W)`** y no construye
ninguna config: es lo medido de W, no un contrato. `test_rebuild_consulta_w_version.py` sólo
necesitaba el sha, así que va a `CKMlandscapeConfig.create` + `ciclo_vigente.w_version_id`.
Los dos archivos: **16/16**.

**3. `experiments/replay_sesion_trust.py`** migrado a `create`, y **dejó de imprimir θ_W**.
Se fueron también sus dos constantes `THETA_W_NO_USADO` y `SCALE_NO_USADO`, que ya no tienen
a quién declararle nada. Imprime el ciclo vigente en lugar de los campos sueltos. **No lo
ejecuté:** lee de `process/replay/_private/`, que no se commitea y no está acá. Verifiqué
sintaxis con `ast.parse`, no comportamiento. Queda declarado.

**4. `conteo_vs_masa.py` no se tocó.**

**5. `CKMlandscapeConfigV1` borrada.** El módulo pasa de 480 a 398 líneas.
`grep -rn "CKMlandscapeConfigV1"` sobre `*.py` y `*.md`: **cero en código**. Las únicas
menciones que quedan son en `docs/tasks/` y en esta bandeja, que son traza.

**6. `theta_W_formula` salió, y la pregunta abierta no se fue con ella.** El criterio decía
"se actualiza la referencia" del docstring de `gatekeeper_c1.py`. Hice algo un poco más que
eso, y lo declaro: en vez de apuntar a un método que ya no existe, el docstring **enuncia la
pregunta ahí** — que la fórmula sigue abierta, y la propiedad que tendría que cumplir (con la
normalización de W declarada, al menos el núcleo A pasa C1). Si sólo hubiera corregido la
referencia, borrar el stub se habría llevado el único lugar del código donde constaba que θ_W
no tiene fórmula.

**7. CHANGELOG:** entrada agregada. Ver P8.

### Suite

**220/220.** Bajan los 9 del archivo borrado y suben los 2 migrados (227 − 9 + 2 = 220).

### Un desvío mío, el mismo de ayer

Al preparar el commit usé `git add -A tests/` otra vez y volvió a arrastrar
**`tests/run_tests.sh`**, que está sin trackear a propósito. Lo saqué del staging **antes** de
commitear, así que esta vez no llegó al repo. Ayer sí llegó y hubo que revertirlo (`cda1ecd`).
Es el segundo caso del mismo reflejo: `add -A` sobre un directorio en vez de nombrar archivos.

---

## PREGUNTA P8 — NO BLOQUEA — 2026-10-08 00:18 UTC

**¿Bajo qué versión va la entrada del CHANGELOG?**

`CHANGELOG.md` tiene como última versión **`v30 — July 2026`**, y los informes de trabajo van
por **v32** (`docs/work_reports/CKM_Informe_Trabajo_v32.md`). El archivo está atrás, y no hay
sección para lo no publicado. Poner un número de versión es decidir dónde está el proyecto, y
no me corresponde.

**Default declarado y reversible:** la entrada va bajo **`## Unreleased`**, arriba de v30, y
escrita en **inglés** para no romper el idioma del archivo. Revertir: cambiar el encabezado
por el número que corresponda, que es mover una línea.

---

## ARRANQUE — 2026-10-08 00:52 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8. **Primera sesión en `main`** —
§6 reemplazado el 8 oct: una sola rama. `git pull --rebase origin main` hecho antes de esto.*

### Revisé

1. **Locks.** `find .git -name "*.lock"` → ninguno.
2. **`git pull --rebase origin main`** → limpio, sin conflictos. HEAD en `0d6eb74`
   (*tasks(protocolo): §9 los pasos de Opus y delamor que faltaban*). Historia lineal, sin
   commit de merge: es el primer pull con el flujo nuevo.
3. **`git status`** → nada modificado ni en staging. Los no trackeados son los 28 conocidos.
4. **`ESTADO_CKMlandscapeConfig_v3.md`** → la TASK anterior quedó **cerrada** en el CP3. No
   hay ningún CP abierto de ella. No existía `ESTADO_monitor_coco_ciclo_orbita_v2.md`: lo creo
   en esta sesión.
5. **`DECISIONES_opus.md` (§8)** → leído, incluidas las entradas sobre el CP3 y la práctica
   nueva (nunca `add -A` ni `commit -a`).
6. **`PROTOCOLO`** → leídos los cambios: **§6 reemplazado** (una sola rama) y **§9 nueva**
   (los pasos de Opus y de delamor, que estaban implícitos).
7. **Archivos de salida.** `monitor_trajectory.jsonl` (raíz, 76 líneas) e
   `iap_chatroom/_state/monitor_trajectory.jsonl` (4 líneas): la última línea de cada uno
   parsea como JSON completo. Ninguna truncada. El formato no lleva marca de "terminó".
8. **Tests.** Suite completa: **220/220**, sin cambios desde el cierre del CP3.

### Preguntas abiertas

**Ninguna. P1–P8 están respondidas**, cada una con un `Pn` que la nombra en
`DECISIONES_opus.md`. **Ningún default quedó vigente sin decisión**, así que no hay nada que
arrastrar como `Pn — DEFAULT VIGENTE, SIN DECISIÓN`. La próxima pregunta es **P9**.

### Encontré

- **`origin/code/trabajo` todavía existe en GitHub.** §6 dice que se elimina. No la borro: es
  irreversible y no es mío (E2). Mi rama local ya no está.
- **Un desfasaje de un commit en el registro de §6.** Dice *"Su último commit fue `2195025`"*,
  y el último fue **`897f67f`** — el merge que pusheé después de esa verificación.
  **No se perdió nada, y lo medí:** `44af68a` (el CP3) es ancestro de `main`;
  `git diff --name-only --diff-filter=D main 897f67f` sale vacío, o sea que `main` no le falta
  ningún archivo mío. `897f67f` era un merge de `main` en la rama, sin contenido propio. Lo
  anoto sólo para que el registro quede exacto.
- **Mi rama local `code/trabajo` desapareció** entre el `checkout main` y el
  `pull --rebase`. No sé cuál de los dos, y ninguno de los dos debería borrar una rama.
  No tiene consecuencia —el contenido está en `main` y `897f67f` sigue existiendo como commit
  suelto— pero **no tengo la causa**, y lo digo en vez de atribuirle una.

### No pude revisar

- **El chat.** Lo que se decidió o se dijo ahí no deja traza que yo pueda chequear desde el
  repo. Es la mitad del CORTE de ayer, y sigue fuera del alcance de este chequeo por
  construcción.
- **El estado del Codespace fuera de git.** Procesos corriendo, variables de entorno, archivos
  en `/tmp`, y si alguna sesión anterior dejó algo a medias que no toca el árbol de trabajo.
  Lo único que puedo afirmar es que el árbol está limpio y los `.jsonl` no están truncados.
- **El clon local de delamor.** §9.1 y §9.2 dicen que lo de Opus no existe para mí hasta que
  llega el push. No puedo saber si hay commits de Opus sin subir; sólo veo lo que está en
  GitHub.
- **`experiments/replay_sesion_trust.py`**, que migré en el CP3: sus datos están en
  `process/replay/_private/`, que no se commitea. Sigue verificado sólo por sintaxis.
- **La causa de la desaparición de la rama local**, como dije arriba.

---

## CORRECCIÓN — 2026-10-08 01:45 UTC

**La entrada `ARRANQUE` de arriba dice `00:52 UTC` y la hora real era `01:43 UTC`.**

Puse la hora de memoria en vez de leerla: la había mirado al principio de la sesión y escribí
esa, sin volver a correr `date -u`. El chequeo que describe sí se hizo, y se hizo en esa
sesión; lo que está mal es la hora del encabezado, 51 minutos antes.

No edito la entrada: §6 dice que las anteriores no se editan. Queda esta corrección, y el
orden real de la bandeja es el de los commits, no el de los encabezados.

Para los próximos: la hora se lee con `date -u` **en el momento de escribir la entrada**, no
al arrancar la sesión.

---

## REPORTE CP0 — 2026-10-08 01:46 UTC

*TASK `TASK_monitor_coco_ciclo_orbita_v2.md` §2.CP0, sobre `6152c71`. Leído §0b primero, como
pidió delamor. Sin código: todo lo de acá es lectura del repo o demostración.*

### 1. Usos de `relax` de una sola fase — hay dos vivos, y uno no estaba en la lista

`relax()` **es** `relax_orbit(...)[3]`: la fase que cae en `max_iter`.

| sitio | fase u órbita | ¿vivo? |
|---|---|---|
| **`monitor_service.py:168`** `self._relax(sigma_prompt, W+Δ_r)` | **una fase** | **SÍ, y es el principal** |
| `landscape_engine.py:284`, en **`mean_cS`** | **una fase** | **SÍ** — COCO la llama en L299 y L309 |
| `landscape_engine.py:258`, en `deprecated_count_attractors` | una fase | **no** — nadie la llama |
| `landscape_engine.py:314`, en `basin_masses` | órbita | sí — es el camino de N_eff y D_ckm |
| `landscape_engine.py:362/376`, en `basin_distance` | órbita | sí |
| `monitor_service.py:409` `_relax_orbit` | órbita | **definido y nunca llamado** |
| `coco.py:591` `_relax_orbit` y `coco.py:595` `_relax` | — | **los dos definidos y nunca llamados** |

**Lo que esto corrige de la TASK.** El CP0 pregunta por `landscape_engine` L258 y L284. De
esas dos, **L284 alimenta algo vivo y L258 no**. Pero el uso de una sola fase que más pesa
**no está en `landscape_engine`: es `monitor_service.py:168`**, que es de donde salen
`rejected` → `Δ_r_pares`, `c_S`, `fabrication_index` y `activos_relajado`. Es el que la §0 de
la TASK describe en prosa; lo agrego a la tabla para que quede ubicado por archivo y línea.

**Y el camino de D_ckm ya está sobre la órbita.** `count_attractors` es
`n_eff(basin_masses(...))`, y `basin_masses` agrupa por `relax_orbit`. Así que de las
cantidades del panel, **N_eff y D_ckm ya no dependen de la paridad**; las que sí dependen son
`c_S`, `n_rejected_pairs`, `rechazados`, `fabrication_index` y `Δ_r`. Eso acota qué puede
moverse en el CP1.

### 2. `relax(−σ) = −relax(σ)` — demostrada, no corrida

El paso síncrono es `h = W @ s`, `T(s) = where(h>0, +1, where(h<0, −1, s))`.

**T(−s) = −T(s)**, componente a componente. `W @ (−s) = −(W @ s) = −h`, y entonces:

| caso | `T(s)ᵢ` | `(−h)ᵢ` | `T(−s)ᵢ` | ¿= −T(s)ᵢ? |
|---|---|---|---|---|
| hᵢ > 0 | +1 | < 0 | −1 | sí |
| hᵢ < 0 | −1 | > 0 | +1 | sí |
| **hᵢ = 0** | **sᵢ** | = 0 | **(−s)ᵢ = −sᵢ** | **sí** |

**El empate es donde la identidad se gana o se pierde.** La regla GOLES —`h = 0` conserva
`σᵢ`— es lo que la hace valer. Con la convención alternativa (`h=0 → +1`) el tercer caso daría
`+1` en los dos lados y la identidad se rompería en todo nodo con campo nulo. Es la misma
regla que el paper declara como premisa del instrumento (§4.2) y la misma del desempate de
nodos.

**Fase a fase.** Por inducción, `Tᵗ(−σ) = −Tᵗ(σ)` para todo `t ≥ 0`. En `relax_orbit`:

- las colisiones de `visto` caen en los **mismos pasos**, porque `s_a = s_b ⟺ −s_a = −s_b`;
- entonces `prev`, `per` (el período) y `cola` son **idénticos**, y también el índice
  `idx = prev + ((max_iter − prev) % per)`;
- `órbita(−σ) = { −x : x ∈ órbita(σ) }`, con el mismo período;
- `seq[idx]` del lado de `−σ` es exactamente `−seq[idx]`, así que
  **`relax(−σ) = −relax(σ)` para cualquier `max_iter`**, y la fase elegida es la negación de la
  fase correspondiente, no otra fase.

**Lo que la identidad NO dice**, y conviene no confundir: no dice que la órbita sea simétrica
bajo negación, o sea que `−x` esté en la *misma* órbita que `x`. Dice que la trayectoria desde
`−σ` es la negación de la trayectoria desde `σ`. Para ρ* = 0.5 alcanza con eso: el muestreo de
`σ₀` uniforme sobre `{−1,+1}^N` es invariante bajo negación, así que la medida inducida sobre
órbitas también lo es.

**Condiciones que declaro** (sin ellas la demostración es sobre los reales, no sobre el
código): la negación en IEEE-754 es exacta (es un bit de signo), y el redondeo a par más
cercano es simétrico respecto de cero, así que `Σ(−xᵢ) = −Σ(xᵢ)` **bit a bit** siempre que el
orden de suma sea el mismo — y lo es, porque las formas y los strides son idénticos. Si alguna
vez el producto se hiciera con una reducción cuyo orden dependiera de los valores, esto habría
que volver a mirarlo.

### 3. Usuarios de `corpus.coco` — cuatro, y uno está vivo

| sitio | qué usa | estado |
|---|---|---|
| **`iap_chatroom/ckm_monitor.py:104`** | **sólo `landscape_history()`** | **vivo** |
| `iap_chatroom/tests/test_armstrong_via_corpus_v3.py` (L34-48, 75) | el COCO entero, como `thermostat` | traza Armstrong — **no se modifica** |
| `iap_chatroom/tests/test_armstrong_n_runs_sweep.py:73` | como `thermostat` | traza Armstrong — **no se modifica** |
| `experiments/coco_lifetime_analytics.py` (L122, 138, 140, 221) | las dos instancias, para medir la divergencia | es el instrumento que la reproduce |

**Dos cosas medidas que importan para el CP4:**

- La línea viva es **L104, no L93** como dice la TASK. El corrimiento lo produjo mi propio CP2
  de la Config v3, que agregó el bloque de la Config en `__init__`. Lo digo para que la
  referencia quede exacta.
- **Lo único que el canal le pide a `corpus.coco` es `landscape_history()`**, no el COCO. Así
  que cuando CorpusService lo suelte, lo que hay que reemplazar es de dónde sale ese historial
  —y eso enlaza con el punto 2 del CP3 (`landscape_history` a través del salto), que es de
  delamor. No es un reemplazo mecánico de `corpus.coco` por `monitor._thermostat`.
- `test_armstrong_via_corpus_v3.py:37` hace `corpus._coco = COCO(...)`: **escribe el privado**
  para forzar `seed=123`. Si `_coco` deja de existir, ese test deja de correr tal cual. Es
  traza y no se toca, así que al sacarlo hay que declarar que queda histórico y por qué.

### 4. Configuración de COCO al renacer — hoy no es la misma, y la diferencia es grande

| | Monitor | COCO (como lo crea Corpus) |
|---|---|---|
| **n_runs** | **1000** (`n_runs_attractors`, `monitor_service.py:74`) | **80** (`coco.py:146`) |
| seed | 0 (`count_seed`) | 0 |
| sampling_mode | "uniform" | "uniform" |
| n_warmup | None | None |
| track_landscape | — | **True** (`corpus_service.py:295`) |
| gamma | — | 0.01 |

**Monitor cuenta con 1000 muestras y COCO con 80, sobre el mismo campo.** Y 1000 no es un
número cualquiera: el docstring de Monitor dice que es el valor donde N_eff converge en los
casos IAP (±2% de 5000) y que **con 50 quedaba 5–20% por debajo**. O sea que el N_eff de COCO,
con 80, está en la zona donde el propio proyecto midió que no converge.

El `CKMMonitor` del canal no pasa `n_runs_attractors`, así que usa el default 1000.

**Esto no es una pregunta sobre dónde guardar un parámetro: es que los dos aspectos de la misma
cosa miden con muestreos distintos.** Si van a nacer y morir juntos, cuál de los dos n_runs
queda es una decisión, no un default heredado. Va en **P9**.

### 5. β — qué acumula y qué muere

`β` no es estado de W: es estado **por device**. `self._rejections_per_device`
(`coco.py:221`) acumula un `fi` por evaluación (`register_device_eval`, L367-371), `beta_i`
lee esa lista y `beta_collective` (L384) es la **mediana de los β_i activos**.

Entonces, al renacer COCO con el ciclo:

- **el historial de rechazos por device muere con la instancia**, porque vive en el `dict` de
  esa instancia;
- `beta_collective()` vuelve a **None** hasta que haya evaluaciones nuevas, y eso es correcto:
  es el borde que ya está bien resuelto —`temp_signal` devuelve `signal="UNKNOWN"` con
  `beta_collective` y `ratio` en None (L438-446)—, y es el modelo de cómo debería comportarse
  el vacío en los otros bordes (punto 8);
- lo registrado que cita la TASK —*"β no puede persistir si cambia W; muere con el rebuild; el
  historial por `w_version_id` puede ir como registro"*— es consistente con lo que leo: **β se
  calcula sobre `fi`, que Monitor produce con W+Δ_r**, así que un β acumulado a través de dos W
  mezclaría dos campos.

**Nada en el código de hoy conserva β entre instancias de COCO.** Si el historial por
`w_version_id` va a existir, hay que crearlo; no es algo que esté y haya que preservar.

### 6. Encaje con la Config v3 → **P9**

Lo medido: el `declarado` de la Config es hoy **`sampling_mode`** (obligatorio) y **`scale`**
(opcional), y nada más — θ_W salió en el CP3. COCO tiene, además de `sampling_mode`:
`n_runs`, `seed`, `track_landscape`, `n_warmup`, `gamma`, y tres umbrales
(`d_ckm_threshold`, `alpha_star`, `frac_rec_min`).

`sampling_mode` sale de la Config sin problema: ya está ahí y Monitor ya valida el suyo contra
él (`monitor_service.py:117`). **Lo que falta decidir es el resto**, y lo reporto sin decidir,
como pide el punto 6. Va en **P9**, junto con el choque de `n_runs` del punto 4.

COCO leería el ciclo con `ciclo_vigente` (get entero, bajo lock), nunca campo por campo: eso ya
está construido y no hay nada que agregar.

### 7. Comparabilidad de lo histórico — declarado

- **Los 80 paneles que hay en el repo tienen `thermostat: None`.** `monitor_trajectory.jsonl`
  (76) e `iap_chatroom/_state/monitor_trajectory.jsonl` (4): **ninguno** tiene COCO. Así que la
  divergencia de los dos COCO **no está en estos paneles**; está en lo que mide
  `coco_lifetime_analytics.py` y en lo registrado en `REG_coco_w_congelada_v1`.
- **Lo que sí está en los 80, y se escribió desde una sola fase:** `n_rejected_pairs`,
  `rechazados`, `c_S`, `fabrication_index`, `Delta_r_sum`, `activos_relajado`.
- **`N_eff` y `D_ckm` de esos paneles no dependen de la paridad**, porque ya salen de
  `basin_masses` (punto 1).
- El panel viejo del canal (4 líneas) **no tiene** `N_eff`, `N_eff0`, `D_masa_cuencas`,
  `Delta_r_reset`, `landscape_config`, `condicion_W`, `saturacion` ni `gatekeeper_c1`: es de
  antes de esas claves. Al comparar con lo nuevo, esas ausencias son de formato, no mediciones
  faltantes.

### 8. El vacío al dividir — tres bordes vivos, uno latente, y uno que ya está bien

**Vivos, y hay que cambiarlos:**

1. **`coco.py:570-575` `_classify_zone`:** `if D_ckm is None: return "stable"`. El docstring lo
   justifica: *"sin medición no se aplica STOP"*. El efecto buscado es correcto —no disparar
   STOP— pero el nombre que le pone es **"stable"**, que es una medición. Es exactamente el
   patrón de `c06db07`.
2. **`coco.py:268`:** `frac_rec = A_current / self._A0 if self._A0 > 0 else 1.0`. **La ausencia
   de baseline se lee como recuperación total**, que es el valor más tranquilizador posible.
3. **`coco.py:264-265`:** `if self._A0 is None: self._A0 = self._count_attractors(self.W, ...)`.
   El baseline **se fija en la primera observación**, en silencio. Al renacer con el ciclo, eso
   es justo lo que hay que mirar: el A0 nuevo se toma de la W nueva en la primera `observe`, y
   nada en el panel dice que ese ciclo recién empezó.

**Latente, no activo:** `ThermostatState` (`coco.py:114-123`) tiene por defecto
`D_ckm = 0.0`, `frac_rec = 1.0`, `zone = "stable"`. **Verifiqué que nadie lo construye sin
argumentos** (los dos usos, `coco.py:335` y el de `process/`, pasan todo), así que hoy no
produce ningún dato falso. Pero un `ThermostatState()` vacío se lee como campo medido, estable
y sin divergencia. Lo reporto como latente, no como vivo, porque es la diferencia entre lo que
pasa y lo que podría pasar.

**Ya está bien, y es el modelo:** `temp_signal` (`coco.py:436-446`) devuelve
`signal="UNKNOWN"` con `beta_collective` y `ratio` en `None` cuando no hay devices. Y
`d_ckm`/`d_masa_cuencas` devuelven `None` con `N_eff0 ≤ 1` (`landscape_engine.py:438`,
`:487`). Los dos nombran el vacío.

**Revisé el borde que la TASK señala en `landscape_engine.py:418`** —
`(A0 − A_actual)/A0 if A0 > 0 else 0.0` — y **no está vivo**: está en `deprecated_d_ckm`, y el
único que lo llama es `tests/test_neff_y_frontera.py`, que fija ese borde a propósito
(`deprecated_d_ckm(3, 0) == 0.0`) como traza de la forma anterior. No lo toco.

`grep` de `max(0` en los tres módulos: una sola aparición, `coco.py:565`
`ratio = min(1.0, max(0.0, (D_ckm − t)/(1.0 − t)))`, que es un clamp sobre un `D_ckm` que ya se
sabe no-None en ese punto. No es un vacío disfrazado.

### 9. Tests afectados

| archivo | tests | corre pytest |
|---|---|---|
| `tests/test_monitor_services.py` | 36 | sí |
| `tests/test_coco.py` | 30 | sí |
| `tests/test_delta_compresiones_coco.py` | 6 | sí |
| `tests/test_invalidacion_delta_r.py` | 5 | sí |
| | **77 de los 220** | |
| `iap_chatroom/tests/test_caso_*.py` | 21 archivos | **NO — 0 recolectados** |

**Los 21 `test_caso_*` del canal no son tests de pytest.** `pytest iap_chatroom/tests/` recoge
**0 items**: son scripts con `asyncio.run(...)` en `__main__`. Así que **no están en los 220**,
y un cambio en Monitor o COCO puede romperlos sin que la suite diga nada. Lo declaro porque el
punto 9 los lista como "afectados" y conviene que quede claro que esa cobertura no existe
automáticamente.

### Lo que este CP0 NO hizo

- No corrí nada de lo que se puede demostrar: el punto 2 es una demostración, y la identidad no
  se verificó numéricamente a propósito.
- No corrí `coco_lifetime_analytics.py`: eso es el CP1.
- No conté los 56 incrementos negativos: están registrados y su reproducción es del CP1.
- No toqué `services/`.

---

## PREGUNTA P9 — **BLOQUEA** — 2026-10-08 01:46 UTC — **[delamor]**

**Con qué configuración nace COCO, y dónde se declara.** El punto 6 del CP0 pide reportarlo sin
decidir; el punto 4 encontró que hoy no hay una sola configuración, sino dos que no coinciden.

**Lo medido:** Monitor cuenta con **n_runs = 1000** y el COCO que crea Corpus con **n_runs = 80**,
sobre el mismo campo. El propio docstring de Monitor dice que 1000 es donde N_eff converge en
los casos IAP (±2% de 5000) y que **con 50 quedaba 5–20% por debajo**. Con 80, el N_eff de COCO
cae en esa zona.

**Lo que hace falta decidir:**

1. **Qué `n_runs` queda** cuando Monitor y COCO son una sola existencia. No hay default que
   herede: elegir uno cambia el N_eff de COCO —y con él `frac_rec`, la zona y el STOP— o cambia
   el costo de cada evaluación de Monitor.
2. **Qué de COCO va a la Config como `declarado`** y qué queda en su propia configuración.
   `sampling_mode` ya está en la Config. Los candidatos son `seed`, `n_runs`,
   `track_landscape`, `n_warmup`, `gamma` y los tres umbrales (`d_ckm_threshold`,
   `alpha_star`, `frac_rec_min`).
3. **Si los umbrales son `declarado` o son calibración**, que es un proceso aparte por D6 de la
   Config v3.

**Por qué BLOQUEA, y dónde:** bloquea el **CP2**, que es donde Monitor pasa a recibir una
configuración de COCO en vez de una instancia. **No bloquea el CP1**, que mide lo que hoy se
rompe sin cambiar `services/`. Si se contesta antes del CP2, no frena nada.

**No propongo un default**, porque elegir el `n_runs` cambia lo que el instrumento mide, y eso
es E3.

---

## REPORTE CP1 — 2026-10-08 01:58 UTC

*TASK `TASK_monitor_coco_ciclo_orbita_v2.md` §2.CP1. Driver:
`experiments/cp1_paridad_y_dos_existencias.py`, **commiteado con su pre-registro antes de la
primera corrida** (`d3230c1`). Log: `experiments/cp1_paridad_log.json`. No se tocó `services/`.*

### A. Paridad — **pesa, en los dos corpus**

| | caso09_run2 natural | WARMUP_TEXTS |
|---|---|---|
| N · textos | 32 · 24 | 30 · 20 |
| **textos con órbita de período 2** | **16 de 24** | **3 de 20** |
| textos donde el estado final difiere | **18 de 24** | 4 de 20 |
| textos con `|R_A △ R_B| > 0` | 4 | 2 |
| **U1** alguna diferencia simétrica | **sí** | **sí** |
| **U2** `‖Δ_r^A − Δ_r^B‖₁` | **24.0** | **12.0** |
| **U3** `max|c(S)_A − c(S)_B|` | **2.35e−02** | **2.88e−02** |
| **LA PARIDAD PESA** | **sí** | **sí** |

**Mi expectativa declarada era equivocada, y por bastante.** Escribí antes de correr que
esperaba *"pocos textos con período 2, y es posible que ninguno"*, razonando que los 136/200
registrados son del muestreo de σ₀ y no de la relajación de σ_prompt. Lo segundo es cierto, pero
la conclusión no: **16 de 24 textos de caso09 relajan a período 2 desde su propio σ_prompt**.
El dato es ese, no mi expectativa.

**Hallazgo que corrige la invariante de compatibilidad de la TASK §1.** La TASK dice: *"En un
punto fijo, R_A = R_B y no hay torsión. En ese caso todo es idéntico a hoy."* **Medido: no se
sostiene a lo largo de un recorrido.** El texto `i=22` de caso09 tiene **período 1** y aun así
`|R_A △ R_B| = 1`, con `nRA=90` y `nRB=91`.

La razón es que **la divergencia se compone**: Δ_r entra a W_eff, así que una vez que las dos
paridades acumularon Δ_r distintos, el W_eff ya no es el mismo y los puntos fijos a los que se
llega tampoco. Por eso hay **18 textos con estado final distinto** y sólo 16 con período 2.

La invariante vale **a igual W_eff**, no a lo largo del recorrido. Como invariante del CP2 sigue
sirviendo —hay que testearla sobre una evaluación, no sobre una serie— pero conviene que quede
dicho así.

**Lo más marcado, texto a texto** (caso09): en `i=8`, período 2, una fase expulsa **9 pares** y
la otra **0**. No es un pequeño corrimiento: es una fase que rechaza y otra que acepta todo.

### B. Dos existencias — **divergen, y hoy rompen**

**No llegué a contar incrementos negativos, porque el recorrido no llega hasta ahí: se cae en la
primera evaluación posterior al rebuild**, con

```
ValueError: operands could not be broadcast together with shapes (31,31) (28,28)
```

en `coco.py:254`, `self._Delta + (Delta_new - self._Delta_leido)`.
`N_de_monitor = 31`, `N_de_coco = 28`, `son_el_mismo_objeto = False`.

**Esto no es un error del driver.** Es la divergencia de las dos existencias en su forma más
dura: COCO quedó con la N de la W con la que nació y Monitor creció con el corpus. Lo capturé
como dato en el log (campo `rotura`) en vez de esquivarlo, y corté ahí.

**Diferencia con lo registrado, declarada.** `TASK_delta_compresiones_coco_v1` §Abierto registra
**56 incrementos negativos** con W de **8 nodos** y α=0.1. Ahí N era fija, así que las formas
coincidían y la divergencia se manifestaba como una serie que decrece. **Con N creciendo —que es
lo que pasa en un corpus real— la misma divergencia no da números raros: levanta una excepción.**
Son dos caras del mismo corte, y la segunda no estaba medida.

**Consecuencia para el CP2:** el renacimiento de COCO con el ciclo no es sólo una cuestión de
coherencia de baselines. **Hoy, con N variable, Monitor + COCO no completa una sola evaluación
después de un rebuild.** Que esto no aparezca en producción es porque el canal usa
`rebuild_suspendido=True` y porque los 80 paneles históricos tienen `thermostat: None`: nunca
corrió esta combinación.

### Lo que este CP1 NO hizo

- No tocó `services/`. El `ValueError` sigue ahí.
- No midió la torsión por clases aceptado/expulsado/torsión: es del CP2.
- No contó los incrementos negativos: el recorrido se corta antes. Para contarlos hace falta N
  fija, y eso es reproducir la condición de `TASK_delta_compresiones_coco_v1`, no la de un
  corpus real.
- **Los 21 `test_caso_*` del canal siguen siendo punto ciego** (decisión del 8 oct): nada de
  este CP1 los ejercita.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**, como siempre.
- **Si el `ValueError` aparece con otros corpus o con otro `top_k`**: lo medí con caso09_run2 y
  `top_k=32`. No barrí condiciones.
- **El clon local de delamor.**

---

## ARRANQUE — 2026-10-08 15:51 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8, tras un corte por límite de uso.*

### Revisé

1. **Locks.** Ninguno.
2. **`git pull --rebase origin main`** → **falló la primera vez**: *"cannot pull with rebase:
   You have unstaged changes"*. Era la bandeja modificada sin commitear (ver CORTE). Resuelto, y
   después limpio. HEAD en `15398e7` (*estado: lo recolectado en el corte*, de delamor).
3. **Mi último commit del corte, `0176ada`, sigue en la historia** (`merge-base --is-ancestor`
   → sí). Nada mío quedó fuera.
4. **`ESTADO_monitor_coco_ciclo_orbita_v2.md`** dice **"CP2 en curso"**, que es la señal de §3.
   Revisado: no quedó nada del CP2 a medias. Ver CORTE punto 1.
5. **`DECISIONES_opus.md` (§8)** → leído, incluida la respuesta a P9.
6. **Tests.** Suite: **220/220**. Igual que al cerrar el CP1.

### Preguntas abiertas

**Ninguna. P1–P9 están respondidas.** P9 la contestó delamor (`n_runs = 1000`) y Opus resolvió
el resto por debajo del umbral. Ningún default quedó vigente sin decisión. La próxima es **P10**.

### Encontré

- **`ESTADO_REPO_delamor.md`** es nuevo (`15398e7`): delamor guardó ahí el último comando que
  corrí y su salida. Es lo que permitió cerrar el CORTE sin ambigüedad.
- **Seis archivos no trackeados nuevos en `process/experiments/`**:
  `armstrong_replica_seed123{,_corpus_state,_summary}` y `armstrong_via_corpus_v3{,_state,_summary}`.
  Son salidas de corridas Armstrong hechas durante el corte, no mías. **No los commiteo**: son
  dumps de datos, y `??` no es pendiente.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git** (procesos, variables, `/tmp`).
- **Los 21 `test_caso_*` del canal**, que son punto ciego declarado (decisión del 8 oct): no son
  tests de pytest y la suite no los cubre.
- **Quién corrió los Armstrong durante el corte y con qué resultado.** Veo los archivos, no la
  corrida. No los abrí: son traza ajena.
- **El clon local de delamor.**

---

## CORTE — 2026-10-08 15:51 UTC

**1. El CP2 no llegó a empezar, y eso quedó verificado, no supuesto.**
El `ESTADO` decía "CP2 en curso" porque lo escribí **antes** del paso, como pide §3. Revisado:
`git status` sin un solo archivo de `services/`, `tests/` ni `experiments/` modificado, ningún
archivo nuevo del CP2, y la suite en 220/220 — idéntica al cierre del CP1. Y `ESTADO_REPO_delamor.md`
guarda mi último comando: fue exactamente el commit del `ESTADO`. **El corte cayó entre escribir
el estado y escribir la primera línea de código.** Sin daño, que es lo que §0 busca.

**2. La bandeja tenía una edición accidental sin commitear, en una entrada vieja.**
En el `ARRANQUE` del 7 oct, línea 17: `conocidos y de antes` había quedado como
**`conocidos y detad antes`**. Es un tecleo accidental —el archivo estaba abierto en el editor—,
no un cambio con intención: `detad` no es nada.

**Lo restauré** con `git checkout -- docs/tasks/BANDEJA_code.md`, y lo declaro acá en vez de
corregirlo en silencio. El criterio: §6 dice que las entradas anteriores **no se editan**, así
que dejar el tecleo adentro habría sido una edición de una entrada vieja, aunque involuntaria.
Si la intención era cambiar algo ahí, se deshace con `git show 894bfe3` y se vuelve a aplicar.

**Y bloqueó el pull:** el `--rebase` se negó a correr con cambios sin commitear. O sea que un
tecleo accidental en un archivo abierto frena el canal entero hasta que alguien lo mire.

**3. Lo que esta sesión hace distinto.** El CP2 se parte en **CP2a / CP2b / CP2c**, cada uno con
su commit, su ESTADO y su entrada en la bandeja (§4: *"Si un CP no entra en una sesión corta, se
parte en sub-pasos con su propio cierre"*). El corte de hoy es la razón.

---

## REPORTE CP2a — 2026-10-08 15:54 UTC

*TASK `TASK_monitor_coco_ciclo_orbita_v2.md` §2.CP2, **primer tercio**. El CP2 se partió en
CP2a / CP2b / CP2c por §4, después del corte de hoy. Este sub-paso **no toca Monitor ni COCO**.*

### Qué quedó

**`services/landscape_engine.py` — dos funciones nuevas, puras.**

- **`pares_por_orbita(sigma_prompt, fases) -> (aceptados, expulsados, torsion)`**, con la
  clasificación de §1: un par de nodos declarados está *expulsado* si cae en **todas** las
  fases, *aceptado* si en **ninguna**, y en *torsión* si en algunas y no en otras.
  Un par está expulsado en una fase si alguno de sus dos nodos quedó en −1 ahí: la misma regla
  que `_rejected_pairs`, aplicada por fase.
- **`fases_de_orbita(orbita, N)`** decodifica el `frozenset` de bytes que devuelve
  `relax_orbit`. **No se tocó `relax_orbit` ni `relax`**, como pide la TASK §3: las fases se
  recuperan del frozenset, que es lo que ya se guarda.

**Generalizada a cualquier número de fases, no a dos.** Las tres clases salen de intersección y
unión sobre las fases, así que con una sola fase la torsión es vacía por construcción, y con dos
da la tabla de la TASK. Si alguna vez apareciera un período mayor, no hay que reescribirla.
Goles-Chacc et al. (1985) dice 1 o 2 con W simétrica; hay un test que verifica ese supuesto en
30 W aleatorias, sin reclamar la prueba.

**`services/ckm_landscape_config.py` — `n_runs` y `seed` entran al `declarado`.**

- `N_RUNS_DEFAULT = 1000`, por la decisión de delamor del 8 oct (*"n 1000"*, P9). **Uno solo
  para Monitor y COCO.**
- `SEED_DEFAULT = 0`. **La seed la elegí yo y la declaro**, como habilitó la respuesta a P9.
  Elegí **0** porque es la que Monitor ya usaba en `count_seed`, así que **no mueve nada de lo ya
  medido**: si hubiera elegido otra, todos los N_eff del proyecto cambiarían de valor sin que
  ningún cambio de modelo lo justifique. Es reversible: se declara distinta al construir la
  Config.
- Los dos se validan (`n_runs` entero ≥ 1, `seed` entera), viajan en `panel()` y sobreviven la
  serialización. **No entran al `Ciclo`**: no son función de W (I5).
- **Los umbrales de COCO no entraron**, por la decisión de Opus: son de Calibración (D6).
  `track_landscape`, `n_warmup` y `gamma` quedan en la configuración de COCO.

### Tests

`tests/test_pares_por_orbita.py` — **11 nuevos**: las tres clases particionan los pares;
la torsión es el par que cae en una sola fase; intercambiar las fases no cambia nada; repetir
una fase no pesa doble; **la invariante de compatibilidad sobre 50 casos aleatorios** —con una
sola fase, `expulsados` es *exactamente* lo que devuelve `_rejected_pairs` hoy y la torsión es
vacía—; el enganche con `relax_orbit`; el supuesto de Goles; y una órbita de período 2
construida a mano (dos nodos con acoplamiento negativo) donde la torsión aparece de verdad.

`tests/test_ckm_landscape_config_ciclos.py` — **8 agregados** para `n_runs` y `seed`:
que son declarado y no Ciclo, que el default es 1000 y 0, que se pueden declarar distintos, que
los inválidos fallan, que sobreviven la serialización y que viajan en el panel.

**Suite: 243/243** (220 + 11 + 8, más los 4 que ya había sumado el archivo de ciclos).

### Lo que el CP2a NO hizo

- **No tocó `MonitorService` ni `COCO`.** El `ValueError` de shapes del CP1 sigue ahí: eso es el
  CP2b.
- **No cambió qué entra a `Δ_r_pares`.** Nada consume `pares_por_orbita` todavía; la función
  existe y está testeada, y nadie la llama. Es deliberado: conectarla es el CP2b, y decidir qué
  entra a Δ_r es el CP3, que es de delamor.
- No agregó `n_torsion` ni `pares_torsion` al panel: también CP2b.
- No cambió `relax` ni `relax_orbit`.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**.
- **Los 21 `test_caso_*` del canal**: punto ciego declarado, y este CP2a no los ejercita.
- **Si `pares_por_orbita` da lo mismo que el camino de hoy sobre un corpus real.** Lo testeé
  contra `_rejected_pairs` con fases sintéticas, no recorriendo caso09. Esa comparación llega
  cuando Monitor la consuma, en el CP2b.
- **El clon local de delamor.**

---

## REPORTE CP2b — 2026-10-08 16:00 UTC

*Segundo tercio del CP2. **Es donde el `ValueError` del CP1 deja de romper.***

### Qué quedó

**`MonitorService` recibe `coco_config`, no una instancia.** Monitor construye su COCO y lo
**recrea cuando cambia el ciclo**, en el mismo bloque donde descarta Δ_r. El panel lleva
`coco_renace`, `coco_generacion` y `coco_externo`, al lado de `Delta_r_reset`.

**`n_runs`, `seed` y `sampling_mode` salen de la Config** (declarado, P9). `coco_config` puede
pisarlos, y entonces es explícito y no un default heredado. Lo demás —`track_landscape`,
`n_warmup`, `gamma`, umbrales— va en `coco_config`.

**`thermostat=COCO(...)` sigue aceptado sólo en transición**, con `coco_externo: True` en el
panel y sin renacer: es el camino de los tests Armstrong, que son traza y no se tocan.
`thermostat` y `coco_config` juntos levantan `ValueError`.

### El ValueError, medido

El primer test reproduce la condición exacta del CP1 —caso09_run2 natural, se lee COCO una vez,
se ingesta de a un texto— y además chequea en cada evaluación que
`COCO.W.shape[0] == Monitor._Delta_r.shape[0]`. **Pasa, y COCO renace al menos una vez.**

**Verificado al revés:** dejando que COCO naciera una vez y no renaciera, **4 de los 13 tests
fallan**, incluido éste. No es un test que no pueda fallar.

### Dos cosas que encontraron mis propios tests, y cambiaron el diseño

**1. Sin Config no hay reloj, y pedir un COCO gestionado sin reloj es pedir una falla
garantizada.** Escribí un test esperando que, sin Config, COCO naciera una vez y no renaciera.
**Falló con `ValueError: shapes (22,22) (3,3)`**: sin ciclos, nunca renace, y el primer rebuild
que cambia N rompe igual que antes.

No lo documenté como límite: **lo rechacé en la construcción.** `coco_config` sin
`landscape_config` levanta `ValueError` con el motivo. El criterio: una sola existencia necesita
un solo reloj, y si no hay reloj no se acepta una configuración cuya falla ya está medida. Para
un COCO que no renace existe el camino declarado, `thermostat=`.

**2. El renacimiento no puede atarse al evento, porque el ciclo puede estar abierto antes.**
Tres tests fallaron con `_thermostat is None`: una Config construida con `create()` **ya trae su
ciclo bootstrap abierto** antes de que Monitor exista, así que `abrir_ciclo` nunca devuelve True
y **COCO no tenía nacimiento**.

Lo até al **`w_version_id` del ciclo vigente** en vez de al evento: si el sha del ciclo no es el
del COCO que hay, COCO renace. Son equivalentes mientras Monitor sea el único que abre ciclos
(I2), y la comparación cubre el caso que el evento no cubría. **El invariante de §1 queda más
fuerte, no más débil:** el COCO vigente es siempre el del ciclo vigente, sin importar quién
abrió el ciclo ni cuándo. Hay un test parametrizado en los dos casos.

### Tests

`tests/test_coco_renace_con_el_ciclo.py` — **13**: el ValueError del CP1 sobre caso09;
nace con el bootstrap (los dos casos, ciclo ya abierto o no); sin cambio de W no renace;
renace en el mismo paso que el reset de Δ_r; **nace vacío** (Δ en ceros, A0 en None);
toma `n_runs`/`seed`/`sampling_mode` de la Config; `coco_config` puede pisarlos;
la configuración es la misma antes y después de renacer; la instancia externa no renace y queda
declarada; `thermostat` + `coco_config` falla; sin COCO el panel queda igual que hoy; y
`coco_config` sin Config se rechaza.

**Suite: 256/256.** Ningún test existente cambió.

### Lo que el CP2b NO hizo

- **No cambió qué entra a `Δ_r_pares`**, que es del CP3 y es de delamor. `pares_por_orbita`
  sigue sin que nadie la llame.
- **No agregó `n_torsion` ni `pares_torsion` al panel**, ni tocó los bordes del vacío: eso es
  el CP2c.
- **No tocó `CorpusService`:** sigue creando su COCO y exponiendo `corpus.coco`. Soltarlo es el
  CP4.
- No tocó el canal (`ckm_monitor.py`): sigue pasando sin `coco_config`.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**.
- **Los 21 `test_caso_*` del canal**: punto ciego declarado. Este CP2b **cambió la firma de
  `MonitorService`** —agregó `coco_config`— y aunque es un parámetro opcional, nada automático
  verifica que esos 21 scripts sigan corriendo.
- **Los tests Armstrong** (`iap_chatroom/tests/test_armstrong_*`): usan `thermostat=`, que es el
  camino que preservé, pero no los corrí. Son traza registrada.
- **El clon local de delamor.**

---

## REPORTE CP2c — 2026-10-08 16:05 UTC

*Último tercio del CP2. **Con esto el CP2 queda cerrado.***

### 1. El vacío se declara

Los tres bordes vivos que el CP0 encontró, y el latente:

| | antes | ahora |
|---|---|---|
| `_classify_zone(D_ckm=None, …)` | **`"stable"`** | **`ZONA_UNKNOWN`** |
| `frac_rec` sin baseline útil | **`1.0`** | **`None`** |
| `_classify_zone(…, frac_rec=None)` | no existía el caso | `ZONA_UNKNOWN` |
| defaults de `ThermostatState()` | `D_ckm=0.0`, `frac_rec=1.0`, `zone="stable"` | todos `None`, `zone=UNKNOWN` |

**UNKNOWN tampoco dispara STOP**, que era el efecto correcto del comportamiento anterior. Lo que
cambia es el nombre: antes decía que el campo está estable cuando lo que pasa es que no se sabe.
Mismo criterio que `c06db07` y que SALAMANCA.

También quedó declarado el momento en que se fija el baseline: `observe` marca
`baseline_recien_fijado` cuando `A0` era None, así que la primera división de un ciclo dice que
se hizo contra un vacío.

### 2. La órbita entra al panel, y Δ_r no se toca

`MonitorService.evaluate` ahora usa **`_relax_orbit`** —que estaba definido y nunca llamado— y
llama a `pares_por_orbita`. El panel lleva `periodo_orbita`, `cola_orbita`, `n_aceptados`,
`n_expulsados`, `n_torsion` y `pares_torsion` (por nombre de nodo, no agregados a un número: la
torsión **no se promedia**).

**`sigma_relaxed` sigue siendo la fase que cae en `max_iter`**, y `rechazados` y
`n_rejected_pairs` siguen saliendo de ahí. **Qué entra a `Δ_r_pares` no cambió**: eso es el CP3 y
es de delamor. Hay un test que lo fija: `n_expulsados ≤ n_rejected_pairs ≤ n_expulsados + n_torsion`.

### Un test existente cambió, y es el único

**`tests/test_coco.py::TestZoneClassification::test_D_ckm_None_is_stable`** →
**`test_D_ckm_None_is_UNKNOWN_not_stable`**. Fijaba `== "stable"` para `D_ckm is None`: era el
test que sostenía el borde que el CP0 señaló. Su docstring ahora dice por qué cambió y cuándo.
Agregué al lado `test_frac_rec_None_is_UNKNOWN`.

**Ningún otro test existente se tocó.**

### Tests

`tests/test_vacio_y_orbita_en_el_panel.py` — **10 nuevos**: zona UNKNOWN y no "stable";
`frac_rec` None y no 1.0; los defaults de `ThermostatState` ya no afirman un campo estable;
UNKNOWN no dispara STOP; **ninguna evaluación de un recorrido real dice "stable" sin D_ckm**;
el panel lleva las tres clases y el período; las tres clases suman los pares declarados;
la invariante de compatibilidad **sobre una evaluación** —que es la condición bajo la que vale,
medida en el CP1—; la torsión viaja con sus pares; y Δ_r no cambió.

**Suite: 267/267.**

**Verificado al revés:** devolviendo `"stable"` al vacío, **fallan 4** tests (2 nuevos y los 2 de
`test_coco.py`). No son tests que no puedan fallar.

### El CP2 completo

| | qué | tests | suite |
|---|---|---|---|
| **CP2a** | `pares_por_orbita`, `n_runs` y `seed` al declarado | 19 | 243 |
| **CP2b** | COCO renace con el ciclo; el `ValueError` deja de romper | 13 | 256 |
| **CP2c** | el vacío a UNKNOWN; la órbita al panel | 10 | 267 |

**47 tests nuevos**, un test existente cambiado y declarado, **267/267**.

### Lo que el CP2 NO hizo

- **No decidió qué entra a `Δ_r_pares` ni a W_eff.** Es el CP3 §1, y es de delamor: las tres
  opciones (a/b/c) siguen abiertas, y ahora hay números para decidir.
- No tocó `CorpusService`: sigue creando su COCO y exponiendo `corpus.coco`. Es el CP4.
- No tocó el canal: `ckm_monitor.py` sigue sin `coco_config`, así que en el canal COCO sigue
  siendo el de Corpus. Conectarlo es parte del CP4.
- No cambió `relax` ni `relax_orbit`, ni el criterio ni el momento del rebuild.
- No promedia con coseno ni pasa a ángulos.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**.
- **Los 21 `test_caso_*` del canal**: punto ciego declarado. El CP2 **cambió la firma de
  `MonitorService`** (agregó `coco_config`) y **agregó seis claves al panel**. Son cambios
  aditivos, pero nada automático verifica que esos 21 scripts sigan corriendo.
- **Los tests Armstrong**: usan `thermostat=`, el camino que preservé, pero no los corrí.
- **Si `n_torsion` se mueve sobre un corpus real a lo largo de un recorrido.** El CP1 lo midió
  con un driver propio; acá los tests son sobre pocas evaluaciones. El panel ya lo registra, así
  que la próxima corrida larga lo deja en la traza.
- **El clon local de delamor.**

---

## REPORTE CP3i — 2026-10-08 16:46 UTC

*Implementación de las cuatro decisiones del CP3 (todas de delamor, 8 oct). El CP3 era de
decisión, no de código; esto es la ejecución. **El CP4 queda aparte.***

### Las cuatro decisiones, implementadas

| | decisión | qué cambió |
|---|---|---|
| **1(a)** | a `Δ_r_pares` y W_eff entran **sólo los expulsados**; la torsión a un objeto propio que no entra a W_eff | `Δ_r` se escribe con `expulsados` (los que caen en todas las fases). Nuevo `self._Delta_r_torsion`, que **sólo escribe Monitor** y **no entra a W_eff**. Panel: `Delta_r_torsion_sum`. Se resetea con el ciclo, igual que Δ_r |
| **2(b)** | el COCO nuevo empieza con `landscape_history` **vacío** | `_renacer_coco` descarta `landscape_history` de `coco_config`. El pasado queda en el JSONL |
| **3** | el baseline se fija **al nacer el ciclo**, con Δ_r en cero (W_eff = W) y `n_runs` declarado | `COCO.fijar_baseline()` nuevo, idempotente, y `_renacer_coco` lo llama. Antes se fijaba perezoso en la primera `observe` y nada decía en qué momento del ciclo quedó |
| **4** | si el salto cae en período 2, el ciclo nuevo **nace con la órbita**, no con una fase | La primera escritura de Δ_r del ciclo nuevo sale de `expulsados`, igual que las demás. No hay un camino especial para la evaluación del salto, y eso es lo que el test verifica |

`rejected` —los pares de la fase que cae en `max_iter`— **se sigue calculando**, porque el panel
lo reporta como `rechazados` y es la traza comparable con los 80 paneles históricos. Ya no es lo
que entra a Δ_r.

### La W sintética, declarada

**No sale de ningún corpus.** La construí a mano para esta prueba, barriendo W simétricas de 4
nodos con pesos en `{−1, −0.5, 0, 0.5, 1}` hasta encontrar una que, desde
`sigma_prompt = [1, 1, 1, −1]`, relaja a una **órbita de período 2 en la que la fase que cae en
max_iter expulsa más pares que los expulsados de toda la órbita**. Es la condición que hace que
la decisión 1(a) se pueda distinguir de la implementación anterior.

```
W_SINTETICA = [[ 0.0,  0.5,  0.0,  1.0],
               [ 0.5,  0.0, -0.5,  0.0],
               [ 0.0, -0.5,  0.0, -0.5],
               [ 1.0,  0.0, -0.5,  0.0]]
sigma_prompt = [1, 1, 1, −1]
```

Medido sobre ella: **período 2, cola 1**, fase en `max_iter` = `[1, −1, −1, −1]`.

| | pares |
|---|---|
| expulsados (en las dos fases) | `(0,1)`, `(0,2)` → **2** |
| torsión (en una sola) | `(1,2)` → **1** |
| la fase que cae en `max_iter` | `(0,1)`, `(0,2)`, `(1,2)` → **3** |

O sea que `(1,2)` entraba a Δ_r con la implementación vieja y ahora va a la torsión.

**La órbita sale de la dinámica real.** El fixture parchea de dónde viene W y qué declara el
prompt; **no parchea la órbita**: la produce `relax_orbit` sobre esos dos datos. Hay un test que
verifica ese supuesto antes que los demás (`test_la_W_sintetica_relaja_a_periodo_2_de_verdad`).

### El hallazgo que pidió trazar

**En el corpus de estos tests la órbita es de período 1, así que `expulsados == rejected` y la
decisión 1(a) no se ejerce.** Por eso toda la primera versión de los tests pasaba igual con Δ_r
escribiéndose desde la fase: no había nada que distinguir.

Y el CP1 lo había medido en el corpus real: **caso09_run2 da 16 de 24 textos con período 2**.
Así que la decisión 1(a) **sí se ejerce en el corpus real**, y bastante; lo que no la ejerce es
el corpus chico de 5 textos de estos tests. Queda trazado, no tapado.

### Las cinco inversiones

Cada una revierte una pieza, corre la **suite completa**, se restaura y se vuelve a correr la
suite completa. Salida literal de las diez corridas:

```
=== INVERSION 1 — Δ_r vuelve a la fase
    cambio: for i, j in expulsados:  ->  for i, j in rejected:
    invertido  -> FAILED test_con_periodo_2_real_delta_r_NO_es_la_fase
                  FAILED test_el_ciclo_nuevo_nace_con_la_orbita_no_con_una_fase
                  2 failed, 274 passed in 8.53s
    restaurado -> 276 passed in 8.42s

=== INVERSION 2 — la torsión entra a W_eff
    cambio: combine(W, Δ_r)  ->  combine(W, Δ_r + Δ_r_torsion)
    invertido  -> FAILED test_la_torsion_NO_entra_a_W_eff
                  1 failed, 275 passed in 8.61s
    restaurado -> 276 passed in 8.58s

=== INVERSION 3 — el baseline vuelve a fijarse perezoso
    cambio: fijar_baseline()  ->  nada (lo fija la primera observe)
    invertido  -> FAILED test_el_coco_nuevo_nace_vacio_y_con_su_baseline_fijado
                  1 failed, 275 passed in 8.32s
    restaurado -> 276 passed in 8.46s

=== INVERSION 4 — la historia se hereda
    cambio: kw.pop("landscape_history")  ->  nada
    invertido  -> FAILED test_el_coco_nuevo_no_hereda_la_landscape_history
                  1 failed, 275 passed in 7.99s
    restaurado -> 276 passed in 7.72s

=== INVERSION 5 — el ciclo nuevo nace con una fase
    cambio: expulsados  ->  rejected SOLO en la evaluación del salto
             (for i, j in (rejected if reset_cause is not None else expulsados))
    invertido  -> FAILED test_el_ciclo_nuevo_nace_con_la_orbita_no_con_una_fase
                  1 failed, 275 passed in 8.64s
    restaurado -> 276 passed in 8.25s
```

Y después de todo, `grep -c INVERSION services/monitor_service.py` → **0**, y la suite en
**276 passed**: el archivo quedó restaurado.

**Las cinco rompen.** Dos cosas que vale aclarar, porque no son lo que yo esperaba:

- **La inversión 1 rompe DOS tests**, no uno: también el de la decisión 4. Tiene sentido —
  revertir Δ_r a la fase en todas las evaluaciones incluye la del salto— y **no lo arreglé**:
  el test de la decisión 4 es más específico que el de la 1, no redundante. La inversión 5 lo
  muestra: revirtiendo **sólo** la evaluación del salto, el de la decisión 1 pasa y el de la 4
  falla. O sea que los dos tests miden cosas distintas.
- **La inversión 2 fue la que no rompía** cuando delamor lo señaló. Rompe desde que el test mira
  **todas** las llamadas a `_combine_W_Delta` y no sólo la última. Lo que cambió fue el test, no
  la implementación: la exclusión de la torsión ya estaba, lo que faltaba era quien la
  protegiera.

### Dos tests míos que no podían fallar, y cómo aparecieron

**1. El de la torsión en W_eff, dos veces.** La primera versión sólo comprobaba que W_eff
*sería* distinta con la torsión, no que Monitor use Δ_r sola. La segunda capturaba el Δ que
Monitor pasa a `_combine_W_Delta`, pero **miraba sólo la última llamada** — y `evaluate` lo llama
varias veces (L211 para la relajación del prompt, y otra vez en el bloque de métricas), así que
la última era una que sí usa Δ_r. **Las dos pasaban con la inversión puesta.** La versión que
quedó mira **todas** las llamadas.

**2. El de Δ_r desde la órbita.** Pasaba porque en el corpus chico `expulsados == rejected`. Se
arregló con la W sintética.

Las dos aparecieron **invirtiendo**, no leyendo. Y la aserción `n_torsion > 0` va **primero** en
los dos tests que dependen de que haya torsión: si no hay nada que medir, eso es UNKNOWN y no OK.

### Un test existente cambió

`test_el_coco_nuevo_nace_vacio` → **`test_el_coco_nuevo_nace_vacio_y_con_su_baseline_fijado`**.
Pedía `A0 is None` al nacer, que era el comportamiento del CP2b. La decisión 3 lo cambia: ahora
pide `A0 is not None` **y** que sea el baseline de W sola. Su docstring dice por qué.

### Suite

**276/276.** Nuevos en este sub-paso: 6 (los 3 de la W sintética, el de la decisión 4, el de la
historia vacía, y el de la torsión aparte). Un existente cambiado.

### Lo que el CP3i NO hizo

- **No tocó `CorpusService`:** sigue creando su COCO y exponiendo `corpus.coco`. Es el CP4.
- **No tocó el canal:** `ckm_monitor.py` sigue sin `coco_config`, así que en el canal COCO sigue
  siendo el de Corpus y nada de esto se ejerce ahí. También CP4.
- No cambió `relax`, `relax_orbit`, ni el criterio ni el momento del rebuild.
- No promedia la torsión ni la convierte en ángulo.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**.
- **Los 21 `test_caso_*` del canal**: punto ciego declarado. Este sub-paso **cambió qué entra a
  Δ_r**, que es lo más de fondo que se tocó hasta ahora, y nada automático verifica que esos 21
  scripts sigan corriendo.
- **Los tests Armstrong:** usan `thermostat=`, el camino preservado, pero no los corrí. Y
  **cambió qué entra a Δ_r**, así que sus números podrían moverse si se volvieran a correr: son
  traza de otra implementación.
- **El efecto de la decisión 1(a) sobre un recorrido real.** Lo testeé con la W sintética y con
  el corpus chico. En caso09, donde 16 de 24 textos tienen período 2, el efecto va a ser visible
  — y el panel ya registra `n_torsion`, así que la próxima corrida larga lo deja en la traza.
  **No la corrí.**
- **El clon local de delamor.**

---

## REPORTE CP4 — 2026-10-08 17:01 UTC

*Último CP de la TASK. **Con esto `TASK_monitor_coco_ciclo_orbita_v2` queda cerrada.***

### Qué quedó

- **`CorpusService` suelta a COCO.** `_rebuild` ya no lo crea. `corpus.coco` queda
  **deprecada**: devuelve `None` y su docstring dice por qué y qué la reemplaza.
- **`_load_landscape_history` se fue** (28 líneas). Ver la búsqueda abajo.
- **`MonitorService.thermostat`** nueva, de lectura: es de dónde lo pide quien antes leía
  `corpus.coco`.
- **El canal le pasa `coco_config={"track_landscape": True}`** a Monitor, y lee el historial
  del paisaje desde `self._monitor.thermostat`, no desde Corpus. `n_runs`, `seed` y
  `sampling_mode` siguen saliendo de la Config.
- **CHANGELOG**, bajo `Unreleased`, con la TASK entera.

### La búsqueda antes de borrar, como pidió delamor

`grep` sobre **todo el repo** —`*.py`, `*.md`, `*.json`, `*.jsonl`, `*.sh`, `*.html`, incluido
`process/`— más una pasada específica por accesos indirectos (`getattr(...)`, `"landscape_history"`,
`'_coco'`).

**`_load_landscape_history` → se fue con el CP4.**

| dónde aparece | qué es |
|---|---|
| `services/corpus_service.py:200` | la definición. **Cero llamadores.** |
| `registers/REG_coco_w_congelada_v1.md:35` | traza: cita la línea que creaba el COCO |
| `registers/META_REG_consolidado_v6.md:2593` | la misma cita |
| `docs/tasks/TASK_coco_load_landscape_history_v1.md` (L1, 51, 80, 153) | su propia spec |

Ningún acceso por `getattr` ni por string. Su único uso era armar el `landscape_history` del
COCO que creaba `_rebuild`, y ese COCO se fue; además, por la decisión **2(b)** el COCO nuevo
nace con la historia vacía, así que precargarla ya no corresponde. **Quedó muerto por el CP4, y
se va con el CP4.**

Nota: el parámetro `monitor_jsonl_path` de `CorpusService` **se conserva** —lo sigue pasando el
canal— aunque su único consumidor era este método. No lo toqué: sacarlo es otra decisión.

### PREGUNTA P10 — NO BLOQUEA — **[delamor]**

**`_last_landscape_signal` estaba muerto desde antes del CP4, y no lo borré.**

| dónde aparece | qué es |
|---|---|
| `services/corpus_service.py:101` | `self._last_landscape_signal = landscape_signal` — **se escribe** |
| `docs/tasks/TASK_landscape_delta_corpus_feedback_v2.md:77` | la línea que lo introdujo |

**Nadie lo lee.** Ni en `services/`, ni en el canal, ni en los `test_caso_*`, ni en los
experimentos, ni por `getattr` o por string. Lo recibe `ingest(landscape_signal=...)`, que el
canal sigue llamando en cada mensaje, y ahí termina.

**No lo toqué, por pedido explícito de delamor:** estaba muerto antes del CP4, así que no es un
cabo que este paso dejó. **La decisión es suya.** Default declarado: queda como está.

### El `test_caso_*` de punta a punta

**Un `test_caso_*` completo no corre acá, y el motivo es concreto.** Lo intenté y reporto lo que
pasó, sin interpretar:

```
$ python3 iap_chatroom/tests/test_caso_01.py
ModuleNotFoundError: No module named 'iap_chatroom'

$ PYTHONPATH=/workspaces/ckm python3 iap_chatroom/tests/test_caso_01.py
RuntimeError: Client failed to connect: All connection attempts failed
  (fastmcp/client/client.py:622, desde autonomous_device.py:197 — async with Client(self.mcp_url))
```

Dos cosas distintas: **(1)** hace falta `PYTHONPATH` en la raíz, y **(2)** necesita el server
levantado en `:7860`. Y aun con el server, **no hay claves de provider en este entorno**:

```
ANTHROPIC_API_KEY = AUSENTE
GROQ_API_KEY      = AUSENTE
OPENAI_API_KEY    = AUSENTE
(no hay .env)
```

Los devices de los `test_caso_*` llaman a Anthropic y a Groq, así que **no se puede correr un
caso completo acá**. No lo fuerzo ni lo simulo.

**Lo que sí corrí: el canal de punta a punta por su camino real**, publicando en el
`ChatChannel` y dejando que el callback de `CKMMonitor` haga todo el recorrido. Lo único que
falta respecto de un caso es que los textos no los genera un LLM. Salida literal:

```
mensajes publicados: 7
COCO de Corpus (deprecada): None
COCO de Monitor: COCO
ciclos de la Config: 1 | causas: ['bootstrap']
  panel[periodo_orbita]      = 1
  panel[cola_orbita]         = 0
  panel[n_aceptados]         = 0
  panel[n_expulsados]        = 0
  panel[n_torsion]           = 0
  panel[pares_torsion]       = []
  panel[Delta_r_torsion_sum] = 0.0
  panel[Delta_r_sum]         = 0.0
  panel[n_rejected_pairs]    = 0
  panel[coco_renace]         = False
  panel[coco_generacion]     = 1
  panel[coco_externo]        = False
  panel[Delta_r_reset]       = None
  panel[thermostat].zone     = stable
  panel[thermostat].frac_rec = 1.0
  panel[thermostat].n_runs   = 1000
lineas en el JSONL: 3
  JSONL ultima linea tiene n_torsion: True | Delta_r_torsion_sum: True
```

**Lo que se observa, sin interpretar los números:** corre sin errores; `corpus.coco` da `None` y
Monitor tiene su COCO; hay **1 ciclo** y su causa es `bootstrap`; `coco_generacion = 1` y
`coco_renace = False` en el último panel; `n_runs = 1000` llega desde la Config; **las seis
claves nuevas están en el panel y en el JSONL**; `n_torsion = 0` y `periodo_orbita = 1`;
`n_expulsados`, `n_rejected_pairs` y `Delta_r_sum` son 0; la zona es `stable` con
`frac_rec = 1.0`. 7 mensajes publicados y 3 líneas en el JSONL.

### Las tres inversiones del CP4

```
=== INVERSION 6 — CorpusService vuelve a crear COCO
    invertido  -> FAILED test_el_rebuild_ya_no_crea_coco
                  FAILED test_la_property_coco_quedo_deprecada_y_devuelve_none
                  FAILED test_el_canal_le_pasa_coco_config_a_monitor
                  3 failed, 281 passed in 10.44s
    restaurado -> 284 passed in 10.50s

=== INVERSION 7 — el canal no le pasa coco_config a Monitor
    invertido  -> FAILED test_el_canal_le_pasa_coco_config_a_monitor
                  FAILED test_el_coco_del_canal_toma_n_runs_de_la_config
                  2 failed, 282 passed in 10.08s
    restaurado -> 284 passed in 11.01s

=== INVERSION 8 — el canal vuelve a leer corpus.coco
    invertido  -> FAILED test_el_canal_no_toca_corpus_coco
                  1 failed, 283 passed in 10.87s
    restaurado -> 284 passed in 11.44s
```

`grep -c INVERSION` sobre `corpus_service.py`, `ckm_monitor.py` y `monitor_service.py` → **0, 0,
0**. No quedó ningún experimento adentro.

**Las tres rompen.** La 6 rompe tres tests y la 7 dos; no lo arreglé: la 8 muestra que no son
redundantes, porque rompe uno solo y distinto.

### Tests

`tests/test_corpus_suelta_a_coco.py` — **8 nuevos**: el rebuild ya no crea COCO; la property
está deprecada y lo dice; `_load_landscape_history` ya no existe; el canal le pasa `coco_config`;
el COCO del canal toma `n_runs` de la Config; **el canal no toca `corpus.coco`** (con un
centinela que estalla si alguien le pide la historia); y las seis claves en el panel y en el
JSONL del canal.

**Suite: 284/284.**

Un detalle del camino: el test del centinela falló primero con
`AttributeError: ... has no attribute '_coco'` — justamente porque Corpus dejó de crearlo. Se
resolvió con `monkeypatch.setattr(..., raising=False)`, y queda anotado en el test.

### No pude revisar

- **El chat** y **el estado del Codespace fuera de git**.
- **Un `test_caso_*` completo**, por lo de arriba: sin claves de provider no corre. El punto
  ciego de los 21 scripts **sigue abierto**, y este CP4 tocó `ckm_monitor.py`.
- **Los tests Armstrong.** Y acá hay algo concreto, no genérico:
  `test_armstrong_via_corpus_v3.py:34` hace `assert corpus.coco is not None` **justo después del
  ingest**, y con el CP4 eso ahora da `None`. **Ese assert se rompe.** No lo toqué: son traza
  registrada. Los que asignan `corpus._coco` a mano (L37) siguen funcionando.
- **El efecto de la decisión 1(a) en el canal**: `n_torsion = 0` y `periodo_orbita = 1` en esta
  corrida. En caso09_run2 el CP1 midió 16 de 24 textos con período 2, pero eso es otro corpus y
  no lo corrí acá.
- **El clon local de delamor.**

---

## ARRANQUE — 2026-10-08 22:58 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8. Sesión nueva tras el cierre de
`TASK_monitor_coco_ciclo_orbita_v2`.*

### Revisé

1. **Locks.** Ninguno.
2. **`git pull --rebase origin main`** → limpio, sin conflictos. HEAD en `7eff81c`
   (*tasks(decisiones): se retoma el plan; DEFS v15 en DRAFT…*).
3. **`git status`** → nada modificado ni en staging. Sólo los no trackeados conocidos.
4. **`ESTADO_*.md`** → tres, los tres **cerrados**: `CKMlandscapeConfig_v3`,
   `monitor_coco_ciclo_orbita_v2` y `ESTADO_REPO_delamor`. Ninguno dice "en curso": la sesión
   anterior cerró entera. No creo un ESTADO nuevo todavía — el CP0 es lectura y el enunciado
   pide ALTO al terminarlo.
5. **`DECISIONES_opus.md`** → leído, incluidas las cuatro entradas del cierre del CP4.
6. **Tests.** Suite: **284/284**, igual que al cerrar el CP4.
7. **La TASK** `TASK_canal_iap_clock_iniciativa_v2.md` (20 256 bytes) y
   `docs/defs/DEFS_CKM_estado_actual_v15.md` (129 949 bytes, DRAFT) existen. Leí la v2 completa
   hasta el CP0 y la **tabla §N** de la DEFS.

### Preguntas abiertas

**Ninguna. P1–P10 están respondidas.** Ningún default vigente sin decisión. La próxima es **P11**.

### Encontró

- **§0 de la v2 se verifica contra HEAD, sin tensión.** La v2 dice que se reverificó contra
  `94baf68` y HEAD ya es `7eff81c`. Medido: `git diff --stat 94baf68 HEAD` sobre
  `autonomous_device.py`, `channel.py`, `mcp_server.py`, `agent_device_skin.py`,
  `ckm_landscape_config.py` y `monitor_service.py` → **vacío**. Lo único que cambió entre los dos
  commits son tres archivos de `docs/`. **Ninguna afirmación de §0 quedó desactualizada.**
- **Las líneas que §0.6 cita se corrieron**, y es por mis propios cambios del CP2/CP3i. Dice
  `monitor_service.py` L548/L556 y hoy son **L548 y L556** — coinciden. `ckm_landscape_config.py`
  L247 también coincide. No hay desfasaje.

### No pude revisar

- **Los 21 `test_caso_*`**: **no hay claves de provider** en este entorno
  (`ANTHROPIC_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY` ausentes, no hay `.env`), así que no
  corren. Punto ciego declarado, y esta TASK **toca el canal entero**.
- **El chat** y **el estado del Codespace fuera de git** (procesos, variables, `/tmp`).
- **`test_armstrong_via_corpus_v3.py:34`**, que quedó roto por el CP4 a sabiendas y espera la
  revisión de delamor.
- **El clon local de delamor.**

---

## REPORTE CP0 — canal IAP, CLOCK e iniciativa — 2026-10-08 22:58 UTC

*TASK `TASK_canal_iap_clock_iniciativa_v2.md` §2.CP0, sobre `7eff81c`. **Sin código.**
Nomenclatura según la tabla §N de la DEFS v15: donde el código dice `expulsados` acá se dice
**rechazado en las dos fases**. **No renombré nada.***

### Punto 1 — Dónde vive hoy el tiempo del canal

| qué | archivo:línea | qué es |
|---|---|---|
| el campo | `iap_chatroom/channel.py:24` | `timestamp: str  # ISO8601` — del `@dataclass Message` |
| el sello | `iap_chatroom/channel.py:52` | `datetime.now(timezone.utc).isoformat()` → **UTC con `+00:00` explícito** |
| a epoch | `iap_chatroom/mcp_server.py:28-29` | `_epoch(iso)` → `datetime.fromisoformat(iso).timestamp()` |
| el filtro | `iap_chatroom/mcp_server.py:69-81` | `get_messages(since: float)` devuelve los que cumplen `_epoch(m.timestamp) > since` |
| el id | `iap_chatroom/mcp_server.py:32-35` | `_message_dict` agrega `message_id = f"msg-{index}"`, con `index` del `enumerate(history)` |

**El sello es de recepción**, como pide §1: lo pone `channel.publish` cuando el mensaje llega
(`channel.py:48-53`), antes de notificar a los subscribers y a los callbacks. ✓ Y va en UTC
declarado. ✓

**¿Hay algo que pueda ser el CLOCK? Hay un candidato, y no sirve.**

`message_id = "msg-{index}"` es un contador monótono que nunca retrocede. Pero **avanza sólo
cuando hay un mensaje**, y el propósito del CLOCK es exactamente el contrario: *"el silencio
entre mensajes es dato medible"*. Un índice de mensajes no mide silencio — con el canal callado
se queda quieto. **No puede ser el CLOCK.**

Los otros dos relojes que ya existen tampoco:

- `ui_gradio.py:85-86` `gr.Timer(value=3)` sí avanza con el canal callado, pero es el refresco
  de la UI, corre en un hilo worker de anyio y **no se publica a ningún device**;
- `autonomous_device.py` `poll_interval = 2.0` es el ritmo de polling **de cada device**, no una
  coordenada común.

**Veredicto: el CLOCK va de cero.** Lo que **no** va de cero es el timestamp: ya está, es de
recepción y es UTC. Lo que falta es un tick numerado, común y observable, que avance con el
canal callado.

### Punto 1b — Los relojes **se mezclan hoy**, y es medible

§1 pedía confirmar si se mezclan. **Sí.**

`autonomous_device.py:203` y `:215` hacen `last_ts = time.time()` — **el reloj del proceso del
device** — y ese valor se le pasa a `get_messages(since=last_ts)` (`:213`), que lo compara contra
**los timestamps del canal** (`mcp_server.py:78`).

**La consecuencia es concreta:** si el reloj del device va adelantado respecto del canal, el
cutoff queda en el futuro y **los mensajes se descartan en silencio** — sin error, sin registro.
El comentario de `:196-201` ya muestra conciencia de una carrera parecida con el evento de join,
pero esa es de **orden**, no de **desfasaje de reloj**.

Hay un tercer reloj, y éste no se mezcla: `:210` usa `time.monotonic()` para la `duration`. Es
monótono y no se compara con nada externo. ✓

### Punto 2 — Quién porta el CLOCK

**(a) ¿Cabe en la Config sin romper I1? Sí, y la razón es que I1 no dice lo que parece.**

I1, literal (`TASK_CKMlandscapeConfig_v2.md:55`): *"Un ciclo cerrado (c_i, i < k) **no se
modifica**. La config **sí cambia: gana ciclos**. La inmutabilidad pasa del objeto a la traza."*

O sea que **la Config ya es mutable**, y de forma declarada: `abrir_ciclo` reemplaza la tupla
de ciclos bajo `threading.RLock` (`ckm_landscape_config.py:340`). Un contador de ticks es
**la misma clase de mutabilidad** que ya tiene. I1 protege los `Ciclo`, no a la Config.

Y la distinción que el enunciado nombra se sostiene en el código: `abrir_ciclo` **no abre nada**
si el sha de W es el mismo (I5, `:336-338`), mientras un tick tendría que avanzar siempre. Son
dos ejes distintos en el mismo objeto, y no se pisan.

Lo que **sí** habría que resolver, y lo reporto sin decidir:
- `panel()` (I7) hoy lleva identidad + declarado + ciclo vigente. Si el tick entra, **cada panel
  pasa a llevar el tick del momento**, lo cual es información nueva en los 80 paneles por venir;
- `to_dict()`/`from_dict()` tendrían que portarlo para que la serialización siga cerrando;
- **el lock tendría que cubrirlo**, o el lector en hilo de Gradio podría ver un tick de un
  momento y un ciclo de otro — es el mismo problema que D3 resolvió para `ciclo_vigente`.

**(b) Con qué reloj quedan los tiempos — y acá hay algo más fuerte que dos fuentes.**

Medido:

| qué | dónde se sella | con qué reloj |
|---|---|---|
| `Ciclo.t_rebuild` | `monitor_service.py:548`, `:556` | `time.time()` del **proceso de Monitor** |
| `Ciclo.t_senal` | lo pasa quien llama; **hoy nadie lo pasa** → `None` | — |
| `CKMlandscapeConfig.timestamp` (identidad) | `ckm_landscape_config.py:222` | `time.time()` del proceso |
| `create(...)` → primer ciclo | `ckm_landscape_config.py:247` | `time.time()` del proceso |
| `Message.timestamp` | `channel.py:52` | **reloj del canal**, UTC ISO, de recepción |
| `last_ts` del device | `autonomous_device.py:203`, `:215` | **reloj del device** |

**Son tres fuentes, no dos.** La TASK §0.6 nombra dos (proceso de Monitor y canal); la tercera
es el reloj del device, y es la única que **ya se mezcla** con otra (punto 1b).

Dos cosas que acotan el problema, y que conviene no confundir:
- **Hoy, en el canal, Monitor y el canal corren en el mismo proceso.** `server.py:58` levanta
  `uvicorn.run(app)` **sin `workers=`**, y `CKMMonitor` es singleton real. Así que
  `time.time()` del proceso de Monitor **es** el reloj del canal, bit a bit. La diferencia es
  **declarativa, no numérica**: nada en el objeto dice de qué reloj viene cada tiempo;
- **el reloj del device sí puede ser otra máquina**, y ahí la diferencia es real.

**No decido.** Si el CLOCK vive en la Config, lo que cambia es **de qué reloj queda sellado cada
tiempo del instrumento**, y eso cambia lo que el instrumento mide → **[delamor], E3**.
Lo que sí puedo ofrecer, sin implementar, son las tres opciones que leo y lo que cada una cuesta:

1. **Unificar en el reloj del canal.** `Ciclo.t_rebuild` pasaría a sellarse con el timestamp del
   canal. Costo: Monitor queda dependiendo del canal para algo que hoy hace solo, y los runs que
   **no** tienen canal (`experiments/`, los tests) necesitarían un reloj inyectado.
2. **Declarar las dos fuentes.** Cada tiempo lleva de qué reloj viene (un campo, o el nombre).
   Costo: nada se unifica, y comparar un `t_rebuild` con un `timestamp` de mensaje sigue siendo
   responsabilidad de quien compara. Es la opción que **no borra la diferencia**.
3. **Una sola fuente inyectada.** Un objeto reloj que el canal y Monitor comparten, y que en los
   tests es determinista. Costo: toca la firma de quien lo necesite; a cambio, el desfasaje del
   device queda medible contra una referencia única.

**Y una cuarta cosa que no es opción sino hallazgo:** los Δt del device **tienen que** calcularse
con los timestamps del canal (§1 lo pide), y hoy no se hace — se usa `time.time()` del device.
Eso es independiente de dónde viva el CLOCK.

**(c) Choques**

- **`TASK_landscape_config_en_runs_v1`, decisión 2:** *"La config se construye una vez por run.
  Si W cambia dentro del run, `w_version_id` queda desactualizado — gap conocido de D7."*
  **Ese choque ya no existe:** el CP2 de Monitor+COCO v2 cerró D7 — la Config ya no se queda
  atrás, gana un ciclo. La decisión 2 de esa TASK describe un estado anterior. **Es una tensión
  de documento, no de código**, y la señalo sin tocarla: esa TASK está cerrada y es traza.
- **`TASK_monitor_coco_ciclo_orbita_v2` (cerrada):** **no choca, y además da el enganche.** El
  ciclo de vida es uno y lo abre Monitor; COCO renace cuando cambia el `w_version_id` del ciclo
  vigente (`monitor_service.py:508-528`). Un CLOCK en la Config sería **otro eje** del mismo
  objeto: el tick avanza sin abrir ciclo, así que **no dispararía ningún renacimiento de COCO**.
  Verificado en el código: `_sincronizar_coco_con_el_ciclo` compara `w_version_id`, no tiempos.
- **Un choque que sí veo y no estaba listado:** si el CLOCK vive en la Config, **el canal pasa a
  depender de la Config para algo que hoy no le pide nada**. Hoy `CKMMonitor` construye la Config
  (`ckm_monitor.py:77`) y el canal nunca la lee. Con el CLOCK ahí, `ChatChannel` —o quien publique
  el tick— necesitaría acceso a un objeto que hoy vive dentro de Monitor. **No es imposible; es
  una dirección de dependencia nueva**, y conviene que sea una decisión y no un efecto.

### Punto 3 — `build_goal_directed_agent`

`iap_chatroom/agent_device_skin.py:95-130`. **Sirve como base, con dos límites.**

Lo que ya hace, y es exactamente lo que el device con objetivo necesita:
- **el objetivo es del agente, no del canal:** arma su historial con `goal_system_prompt` en vez
  del WELCOME MSG (`:104-106` del docstring, `:126-130` el código);
- **puede elegir no publicar:** si el texto generado contiene el `silence_sentinel`, devuelve
  `None` (`:111-121`). Es la primitiva "ninguna acción" de §1 ya existente;
- reusa `_coalesce`/`_strip_own_prefix` en vez de reimplementar la alternancia de roles.

Los dos límites, los dos declarados en su propio docstring:
1. **El sentinel se busca por contención, no por igualdad** — fix de `REG_iap_caso_13_v1`, que
   corrigió el 52% de fugas. **Riesgo conocido y no resuelto:** si un device menciona
   `OP_SILENCE` discutiendo el propio mecanismo, también se suprime. El docstring dice *"no es la
   solución definitiva"*;
2. **no tiene objetivo con condiciones.** `goal_system_prompt` es texto para el LLM. Lo que §1
   pide —condiciones observables, un estado K que baja cuando otros actúan, y la urgencia saliendo
   del estado del mundo y no del reloj— **no está**: no hay estado del objetivo, ni K, ni registro
   de su evolución.

**O sea: es la base del *device* con objetivo, no del *objetivo*.** Lo que falta no es el agente:
es el objeto "objetivo con condiciones" y su estado en el log.

### Punto 4 — Costo del ODA continuo

**Medido, llamada por llamada**, sobre `autonomous_device.py`:

| fase | método | LLM | tool calls MCP |
|---|---|---|---|
| **O** | `_observe` (`:102-124`) | **no** ✓ | **2**: `get_monitor_state`, `get_messages(since=None)` |
| **D** | `_decide` (`:126-161`) | **1** (`provider.complete`, `:155`) | 0 |
| **A** | `_interact` (`:163-…`) → `_generate` (`:97-100`) | **1 más, sólo si INTERACT** | 1: `send_message` |

**Por ciclo ODA: 1 llamada al LLM si la decisión es no actuar, 2 si actúa.**

**Y hoy el ODA no es por vuelta: es por mensaje.** El loop (`:212-236`) recorre
`for message in new_messages` y hace O→D→A **por cada mensaje ajeno**. Es el punto 2 de §0: si en
un poll entran cinco mensajes, son cinco ciclos — **5 a 10 llamadas al LLM en un solo poll**.

**Costo con N devices y duración T.** Con el ODA continuo de §1 —una decisión por vuelta— y
`r` = vueltas por segundo:

```
llamadas al LLM ≈ N · T · r · (1 + p)
```

donde `p` es la fracción de vueltas que terminan en acción. Con el ritmo de hoy
(`poll_interval = 2.0` → `r = 0.5/s`), N = 2 y T = 60 s, que son los parámetros de la serie
0.8/0.9: **60 a 120 llamadas al LLM**, contra las ~2 a 20 de hoy, donde las vueltas sin mensajes
no cuestan nada.

**El orden del cambio: el ODA continuo convierte el costo de "proporcional a los mensajes" en
"proporcional al tiempo × devices".** Eso es lo que hace que WAIT y el criterio local de §1 no
sean optimizaciones cosméticas.

**Qué fija el ritmo de la vuelta.** Hoy lo fija **el device**, y de la forma más rígida posible:
`poll_interval = 2.0` es un parámetro de `AutonomousDevice` y el `sleep` está **al final del
loop** (`:236`), así que el ritmo real es `poll_interval` + lo que tardó el ciclo. No hay mínimo
declarado ni WAIT. Las tres opciones que leo:

1. **el device**, como hoy: cada uno su ritmo, free will, y el costo lo paga quien lo elige;
2. **un mínimo declarado** (de Calibración): un piso común que ningún device baja. Acota el
   costo máximo, y es una restricción sobre el free will — se declara;
3. **WAIT:** el device duerme hasta un tiempo o un evento. Es la que **más** ahorra y la que más
   riesgo tiene de convertirse en modelo sin querer: *"dormir hasta que pase algo"* es muy
   parecido a *"el mensaje dispara el ciclo"*, que es justo lo que esta TASK va a sacar. Si entra,
   tendría que quedar registrado qué lo despertó.

**El criterio local sin LLM (§1), como propuesta y sin implementar.** Lo que leo del repo:

- **Es viable con lo que ya hay.** `_observe` **ya es sin LLM** (su docstring lo dice: *"No LLM —
  solo recolección de datos"*). Todo lo que §1 pide para los deltas está en la observación: los
  timestamps de los mensajes, `own_recent` (`:121-123`) y el campo. Lo único que no está es el
  presupuesto y el estado del objetivo.
- **Lo que ahorra, en el peor caso.** Si el pre-filtro corta una fracción `f` de las vueltas:
  `llamadas ≈ N · T · r · (1 − f) · (1 + p)`. Con `f = 0.9`, los 60–120 de arriba bajan a 6–12.
  **El ahorro es de orden, no marginal.**
- **Lo que cuesta, y no es dinero.** El pre-filtro decide **sin** el LLM qué merece decisión, y
  eso es un sesgo sobre lo que el device puede llegar a notar. §1 ya lo resuelve del modo que el
  proyecto usa: **registrar cada vuelta no llamada con su motivo**, y **auditar** llamando a D
  cada N vueltas aunque el filtro diga que no, midiendo la divergencia. Agrego una sola cosa, y
  es de medición: **la tasa de divergencia es el instrumento, y para que pueda dar "el sesgo
  cuesta" tiene que poder dar también "no cuesta"**. Si la auditoría se corre sólo cuando el
  filtro dijo "no", mide una cara; si se corre al azar sobre las dos, mide las dos.
- **Los umbrales son de Calibración y no los invento.** Lo digo porque es la tentación obvia del
  CP siguiente: poner "40 s" en algún lado porque hay que poner algo.
- **La zona horaria propia** (decisión del 8 oct) **no cuesta ninguna llamada**: `datetime` local
  es gratis, y es información del device, no del canal. Los Δt siguen en UTC del canal.

### Una tensión que encontré y no estaba en los cuatro puntos

**`services/monitor_service.py` se contradice consigo mismo, y la mitad la escribí yo.**

- **L10**: *"W_eff — **no se expulsan**. Δ_r[i,j] += 1 por cada evaluación."*
- **L223**: *"A Δ_r —y por lo tanto a W_eff— entran **sólo los expulsados**"* ← la escribí yo en
  el CP3i.

La tabla §N de la DEFS v15 ya lo señala: `expulsados` es **Babel, error de Opus**, porque
"expulsar" supone un afuera del campo y no lo hay (delamor, 8 oct: *"¿a dónde? ¿fuera de él?"*).
El nombre correcto del objeto es **par rechazado en las dos fases**.

**No renombré nada**, por el enunciado y porque la tabla dice que renombrar es **[delamor]**. Lo
reporto porque las dos líneas están en el mismo archivo y una de las dos es mía: cuando se
decida, hay que tocar `monitor_service.py` (L223, L230, el panel `n_expulsados`),
`landscape_engine.py` (`pares_por_orbita` y su docstring), los tests y el CHANGELOG.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider no corren, y esta TASK **toca el canal
  entero**. Es el punto ciego más grande de este CP0.
- **El desfasaje real entre el reloj del device y el del canal.** Lo leí en el código; no lo medí
  corriendo dos procesos con relojes distintos. En el Codespace es la misma máquina.
- **Si `gr.Timer` podría servir de base para el tick.** Lo descarté por lo que es (refresco de
  UI, hilo worker, no se publica), no por haberlo probado como fuente de ticks.
- **El costo en dinero.** Conté llamadas al LLM, no tokens ni precio: eso depende del provider y
  del tamaño de los prompts, y no lo medí.
- **`autonomous_research_agent` y los otros skins** (casos 0.12+): miré
  `agent_device_skin.py` porque lo pide el punto 3, no el resto de los devices.
- **El chat**, **el estado del Codespace fuera de git** y **el clon local de delamor**.

---

## REPORTE CP0b — freeze de la serie IAP — 2026-10-08 23:06 UTC

*TASK §2.CP0b. delamor: **"Confirmo"** — copiar, no mover. **Los originales no se tocaron.***

### Dónde quedó

**`process/iap_series_freeze_20261008/`** — 67 archivos, 620 KB.

| carpeta | qué |
|---|---|
| `tests/` | los **21** `test_caso_*.py` |
| `registers/` | los **14** `REG_iap_caso_*.md` |
| `configs/` | `groq_agent_config.json` |
| `_state/` | `corpus_state.json`, `corpus_G_state.json`, `monitor_trajectory.jsonl` |
| raíz | los módulos del canal y `providers/` |
| `entorno/` | `commit.txt`, `pip_freeze.txt`, `python.txt`, `modelos_por_caso.txt` |

El README arranca con la línea que pidió delamor, literal:
**"NO ES REPRODUCIBLE. Intento de congelar las condiciones de una experiencia en vivo."**

### La copia se verificó, y los originales siguen intactos

- `diff -rq` sobre los 21 `test_caso_*` → **sin diferencias**;
- `cmp` sobre los seis módulos del canal → **sin diferencias**;
- `diff -rq` sobre los 14 REG → **sin diferencias**;
- `git status --porcelain iap_chatroom/ registers/` (sin `??`) → **vacío**: no se tocó ni un
  original. **Copiar, no mover.** ✓

### Los modelos por caso

Extraídos de los 14 REG. Los identificadores exactos que aparecen:
`claude-haiku-4-5-20251001`, `claude-sonnet-5`, `claude-opus-4-8`,
`llama-3.3-70b-versatile`, y los providers `anthropic` y `groq`.

**Dos casos no nombran ningún identificador exacto**, sólo el nombre corto del modelo:
`REG_iap_caso_07_v1` y `REG_iap_caso_08_v1` dicen "Haiku" y "Sonnet" y nada más.
`REG_iap_caso_15_v1` dice "Groq" y "Sonnet". **Quedó así**: es lo que los REG dicen, y los REG
no se revisan.

### Lo que no se pudo congelar, y está declarado en el README

1. **El modelo**, que es el límite principal y el que la TASK ya nombra: vive afuera, se llama
   por API y el proveedor lo cambia o lo retira. Quedan los identificadores y lo que los logs y
   los REG guardaron.
2. **No hay `.devcontainer/` en el repo.** La TASK propone *"una imagen de contenedor
   (devcontainer del Codespace con dependencias fijadas) más el sha"* como lo más cercano al
   alcance. **No existe**, así que lo más cercano quedó siendo `pip_freeze.txt` + el sha.
   **Es menos de lo que la TASK propone**, y lo digo en vez de dejarlo pasar.
3. **No pude correr ni un `test_caso_*` para verificar la copia por ejecución**: sin claves de
   provider no corren. **La copia se verificó por `diff`, no corriéndola.** Es exactamente la
   razón por la que copiar y no mover era lo correcto: si se hubiera movido, lo único que
   quedaría de la serie sería una copia que nadie puede ejecutar para comprobar que es fiel.
4. **`process/iap_series/` no existía.** La TASK dice que el freeze va *"junto a lo que ya existe
   en `process/iap/` y `process/iap_series/`"*. La primera existe (81 entradas) y **no se tocó**;
   la segunda **no existe en el repo**. Dejé la copia en
   `process/iap_series_freeze_20261008/`, al lado. **No creé `process/iap_series/`**: el nombre
   es de la TASK y no sé si refiere a algo que estuvo y ya no está.
5. **El estado de `_state/` es de agosto** (1 y 13 de ago). **No es el estado al final de la
   serie**: es el que quedó en el disco. Lo copié igual y lo declaro.
6. **No copié `process/iap/`** (81 entradas, incluidas las seis salidas `armstrong_*` que quedan
   UNKNOWN). Ya está en `process/` y no se toca.

### Qué cambia después del freeze

`trigger_mode="on_message"` **deja de ser el modo del canal** y queda sólo como parte de lo
congelado: ahí está `autonomous_device.py` con su loop por mensaje, tal como corrió la serie.

**No lo toqué todavía.** Sacarlo del canal vivo es el CP1/CP2, y el CP1 **espera la respuesta de
delamor sobre el CLOCK** (E3).

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider. Es la razón del punto 3 de arriba.
- **Si el `pip_freeze` del Codespace es el mismo que cuando corrió la serie.** Es el de **hoy**:
  la serie corrió entre agosto y octubre, y nada garantiza que las versiones no se hayan movido.
  **Es una foto de hoy, no de entonces**, y por eso el freeze es un intento.
- **Si falta algo que la serie usó y no supe nombrar.** Copié lo que la TASK lista y lo que
  encontré; lo que no esté nombrado, no está.
- **El chat**, **el estado del Codespace fuera de git** y **el clon local de delamor**.

---

## ARRANQUE — 2026-10-08 23:36 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8.*

### Revisé

1. **Locks.** Ninguno. **`git pull --rebase`** limpio; HEAD en `eb32605`. **`git status`** sin
   nada modificado.
2. **`ESTADO_canal_iap_clock_iniciativa_v2.md`** → último CP cerrado: **CP0b**. No decía
   "en curso": la sesión anterior cerró entera.
3. **`DECISIONES_opus.md`** → leídas `f07a9dc` (el CLOCK, E3) y `eb32605` (CP0b aceptado, CP1
   habilitado).
4. **Tests.** Suite: **284/284** al arrancar.

### Preguntas abiertas

**Ninguna. P1–P10 respondidas.** La próxima es **P11**.

### Encontró — la diferencia 64/67 del CP0b, con nombre

**Mis dos números estaban mal, y los de Opus bien.** Lo medido:

- **68** archivos en disco al terminar el CP0b. Mi "67" era un conteo **viejo**: lo tomé
  **antes** de escribir el README, y después lo reporté como si fuera el final.
- **62** trackeados por git.
- **64** archivos en el commit `db4c147` = esos 62 **+ `BANDEJA_code.md` + el ESTADO**, que no
  están en la carpeta del freeze. El número de Opus era correcto y contaba lo que dijo que
  contaba.

**Los 6 archivos de la diferencia, con nombre** — todos de
`process/iap_series_freeze_20261008/providers/__pycache__/`:

```
__init__.cpython-312.pyc
anthropic_provider.cpython-312.pyc
base.cpython-312.pyc
gemini_provider.cpython-312.pyc
groq_provider.cpython-312.pyc
openai_provider.cpython-312.pyc
```

No entraron porque `.gitignore` excluye `__pycache__`. **Los arrastró mi `cp -r
iap_chatroom/providers`**: no fue una decisión, fue un efecto. **Los borré de la copia.** Son
bytecode derivado, no condición nombrable, y están en una carpeta cuyo sentido es ser una copia
fiel y nombrable. La carpeta queda en **62 en disco y 62 trackeados**, sin diferencia.

**Y la aritmética que no cerraba era de a tres por una razón que importa:** yo dije "67 contra
64, faltan 3". No faltaban 3: eran **6**, y la cuenta sólo parecía cerrar porque mi 67 estaba
mal. Dos números equivocados que se compensaban.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider no corren. Punto ciego declarado, y esta
  TASK toca el canal.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`test_armstrong_via_corpus_v3.py:34`**, roto por el CP4 a sabiendas.

---

## REPORTE CP1 — el CLOCK del canal — 2026-10-08 23:36 UTC

*TASK §2.CP1. Las tres decisiones de delamor (8 oct, E3). **No toqué `trigger_mode` ni el
`since` del device: eso es el CP2.***

### Qué quedó

**`iap_chatroom/channel.py` — el canal genera (decisión 1).**

- `_ahora()`: **el reloj del canal, una sola fuente.** Es `datetime.now(timezone.utc).timestamp()`
  — el mismo de donde sale el ISO del mensaje. No es `time.time()` ni `time.monotonic()`.
- `tick()`: **se deriva del reloj, no se incrementa.** `int((_ahora() − _t0) // TICK_PERIODO_S)`.
  Por eso avanza aunque nadie publique **y aunque nadie pregunte**: no hay contador que dependa
  de que alguien lo mueva.
- `get_clock()`: devuelve `{tick, t, reloj, periodo_s, t0}` y **registra el tick observado, con
  o sin mensajes**. Un tick sin mensajes es una entrada del log: eso es el silencio como dato.
  El log es **de ticks, no de consultas** — preguntar cinco veces en el mismo tick registra una.
- `TICK_PERIODO_S = 1.0`, **declarado, no calibrado**. Los umbrales de decisión son de
  Calibración y no viven acá.
- `Message` gana **`tick`** y **`reloj`** (decisión 3), con defaults `-1` y `"desconocido"` para
  que los `Message` sin ellos —los JSONL históricos— sigan construyéndose.

**`iap_chatroom/mcp_server.py` — la tool.** `get_clock()` devuelve lo del canal. Su docstring
dice que **no calcula nada por el device**: ni Δt, ni "ticks sin mensajes", ni "quién habló
último". Eso es fase D.

**`services/ckm_landscape_config.py` — la Config registra (decisión 2).**
`registrar_tick(tick, reloj)`, con las properties `tick` y `tick_reloj`, bajo el mismo `RLock`
que el resto. **La Config no llama al canal ni lo conoce**: entra un número que alguien trajo.
Sin canal, `tick` es **None** — que es UNKNOWN, no 0. El `panel()` lo lleva con su reloj.

**`services/monitor_service.py` — Monitor lo trae.** `evaluate(..., clock=None)` lo anota en la
Config. **Monitor registra, no genera.** Sin `clock` —los runs de `experiments/` y los tests, que
no tienen canal— el tick queda en None.

**`iap_chatroom/ckm_monitor.py` — el canal se lo pasa.** `on_message` llama a
`ChatChannel().get_clock()` y se lo da a `evaluate`. Así el tick queda registrado **con o sin
mensajes**, porque `get_clock()` registra al ser llamado.

**La dependencia no se invierte**, y hay un test que lo fija leyendo el fuente: `channel.py` no
nombra ni importa la Config.

### Las cinco inversiones

```
=== INVERSION 9 — el tick se incrementa en lugar de derivarse del reloj
    cambio: tick() cuenta consultas en vez de (ahora − t0) // periodo
    invertido  -> FAILED test_el_tick_sale_del_mismo_reloj_que_sella_los_mensajes
                  FAILED test_dos_consultas_en_el_mismo_tick_registran_una
                  FAILED test_la_tool_get_clock_devuelve_lo_del_canal
                  3 failed, 299 passed
    restaurado -> 302 passed

=== INVERSION 10 — el tick sale de otro reloj (time.monotonic)
    cambio: _ahora() usa time.monotonic() en vez del reloj del canal
    invertido  -> 302 passed            ← NO ROMPIÓ
    restaurado -> 302 passed
    (tras agregar dos tests)
    invertido  -> FAILED test_el_reloj_del_canal_es_el_de_pared_UTC
                  FAILED test_el_t0_del_canal_tambien_es_de_pared
                  2 failed, 302 passed
    restaurado -> 304 passed

=== INVERSION 11 — el log no registra los ticks sin mensajes
    cambio: get_clock() sólo registra si el tick tiene mensajes
    invertido  -> FAILED test_el_log_registra_los_ticks_sin_mensajes
                  FAILED test_dos_consultas_en_el_mismo_tick_registran_una
                  2 failed, 300 passed
    restaurado -> 302 passed

=== INVERSION 12 — la Config no registra el tick
    cambio: Monitor no llama a registrar_tick
    invertido  -> FAILED test_monitor_anota_el_tick_que_le_dan
                  FAILED test_el_canal_le_pasa_el_tick_a_la_config
                  2 failed, 300 passed
    restaurado -> 302 passed

=== INVERSION 13 — el tick no declara su reloj
    cambio: RELOJ_CANAL = "desconocido"
    invertido  -> FAILED test_el_clock_declara_su_reloj
                  1 failed, 301 passed
    restaurado -> 302 passed
```

`grep -c INVERSION` sobre los cuatro archivos tocados → **0, 0, 0, 0**.

### La inversión 10 no rompía, y es el hallazgo del CP1

**Cambiando `_ahora()` a `time.monotonic()` pasaban los 302.** O sea que **nada protegía la
decisión 1**: que el reloj del canal sea el que sella los mensajes.

Por qué no rompía: `test_el_tick_sale_del_mismo_reloj_que_sella_los_mensajes` verifica que el
tick y el timestamp del mensaje salgan del **mismo** `_ahora`. Con `monotonic` **siguen saliendo
del mismo** — consistentes entre sí, y equivocados los dos. El test medía la consistencia
interna, no cuál es el reloj.

Lo cerré con dos tests nuevos, y el segundo es el que no se puede falsear con un reloj
arbitrario: **el ISO del mensaje tiene que dar una fecha plausible.** Con `monotonic` —segundos
desde el arranque de la máquina— la fecha cae en 1970. Después de agregarlos, la inversión 10
rompe los dos.

**Es el tercer caso de la misma forma** (CP3i tuvo dos, CP4 ninguno), y los tres aparecieron
invirtiendo, no leyendo.

### Tests

`tests/test_clock_del_canal.py` — **20**: ticks monótonos; **el canal callado también avanza**;
el tick no depende de que alguien pregunte; el tick y el mensaje salen del mismo reloj; **el
reloj es de pared UTC** (×2, los nuevos); el clock declara su reloj; el mensaje declara el suyo;
un `Message` sin reloj dice `desconocido`; el log registra los ticks **sin** mensajes; dos
consultas en el mismo tick registran una; un tick con mensajes queda marcado; **el canal no
calcula nada por el device**; `get_messages` **sigue igual que antes** (mismo filtro `since`,
mismos `message_id`, y las claves de antes siguen estando); la tool devuelve lo del canal; la
Config registra con su reloj; **`registrar_tick` no abre ciclos**; **el canal no lee la Config**
(leyendo el fuente); Monitor anota el tick que le dan y sin clock queda en None; y el canal de
punta a punta le pasa el tick a la Config.

**Suite: 304/304.** Ningún test existente cambió.

### Lo que el CP1 NO hizo

- **No tocó `trigger_mode`** ni el loop de `autonomous_device.py`: el ODA sigue disparándose por
  mensaje. Es el CP2.
- **No tocó el `since` del device**, que sigue saliendo de `time.time()` del device — el
  requisito del CP2 que Opus registró.
- No implementó el criterio local ni WAIT: esperan el OK de delamor.
- No agregó el objetivo con condiciones (K): es el CP3.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider. El CP1 **cambió `channel.py` y
  `mcp_server.py`**, que esos 21 usan.
- **El `Message` con dos campos nuevos contra los JSONL históricos.** Los defaults están y hay
  un test, pero **no abrí un JSONL viejo** para confirmar que se relee sin error.
- **Si `TICK_PERIODO_S = 1.0` es un grano razonable.** Lo declaré, no lo calibré.
- **El comportamiento con el reloj del sistema corriéndose hacia atrás** (NTP). `tick()` se
  deriva del reloj de pared, así que **podría retroceder**; el test de monotonía corre en
  milisegundos y no lo ejerce. Lo digo porque es el precio de derivar en vez de contar.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.

---

## ARRANQUE — 2026-10-08 23:49 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8.*

### Revisé

1. **Locks:** ninguno. **`git pull --rebase`:** limpio, HEAD en `e737e78`. **`git status`:** sin
   nada modificado.
2. **`ESTADO_canal_iap_clock_iniciativa_v2.md`** → último CP cerrado: **CP1**. No decía
   "en curso".
3. **`DECISIONES_opus.md`** → leídas `8adde3b` (CP1 aceptado, con los tres requisitos del CP2) y
   `e737e78` (el OK de delamor al criterio local, y el CP2 partido en CP2a/CP2b).
4. **Tests:** **304/304**.

### Preguntas abiertas

**Ninguna. P1–P10 respondidas.** La próxima es **P11**.

### Encontró

- Nada nuevo en el arranque. Las tensiones del CP2 van en el reporte de abajo, que es lo que
  delamor pidió **antes** de tocar código.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider. Y el CP2a **cambia el loop del device**, que
  es lo que esos 21 ejercitan. Es el punto ciego más grande de este CP.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`test_armstrong_via_corpus_v3.py:34`**, roto por el CP4 a sabiendas.
- **`process/iap_series_freeze_20261008/README.md:41`**, que sigue diciendo "67 archivos".
  Queda para cuando toque `process/`, con una línea declarada (decisión del 8 oct). **No toqué
  `process/` en esta sesión.**

---

## REPORTE CP2 — evaluación contra el repo, antes de tocar código — 2026-10-08 23:49 UTC

*TASK §2.CP2, partido en CP2a/CP2b por `e737e78`. **Sin código.** Seis tensiones, con
archivo:línea.*

### T1 — `trigger_mode` no existe en el código

La TASK §2.CP2 dice: *"`AutonomousDevice` con `trigger_mode="continuo"`"* y
*"`trigger_mode="on_message"` no se mantiene como modo vivo: quedó congelado en el CP0b"*.

**Medido:** `grep -rn trigger_mode` sobre `*.py` → **cero ocurrencias en código**. Sólo aparece
en documentos: la TASK v1 y v2, el README del freeze (que escribí yo) y esta bandeja.

El constructor de `AutonomousDevice` (`autonomous_device.py:73-86`) tiene `device_id`,
`provider`, `system_prompt`, `mcp_url`, `poll_interval`. **No hay `trigger_mode`.** El
comportamiento on_message está **cableado** en `run()` (`:212-236`): el `for message in
new_messages` es el disparador.

**Qué significa, y por qué importa:** "sacar `trigger_mode` del canal vivo" **no es quitar un
flag** — es reemplazar el loop. Y la frase del README del freeze que escribí yo
(*"`trigger_mode="on_message"` deja de ser el modo del canal"*) **se lee como si hubiera una
bandera que se apaga, y no la hay**. El modo congelado es el loop de `run()` tal como está en la
copia.

**No decido** si el parámetro se crea igual (dos modos coexistiendo) o si el loop se reemplaza
y el modo viejo queda sólo en el freeze. La TASK dice que on_message *"no se mantiene como modo
vivo"*, que leo como lo segundo, pero el nombre `trigger_mode="continuo"` sugiere un parámetro.
**Default declarado y reversible si nadie contesta:** creo el parámetro con
`trigger_mode="continuo"` como **único valor aceptado**, y cualquier otro valor levanta
`ValueError` nombrando el freeze. Así el nombre que la TASK usa existe, y el modo viejo no
vuelve por un default. → **P11**.

### T2 — Requisito 1 (`since` del canal): hay de dónde, y es lo que agregó el CP1

**Medido:** `autonomous_device.py:203` y `:215` hacen `last_ts = time.time()` — reloj del device
— y eso va a `get_messages(since=last_ts)` (`:213`), que lo compara contra timestamps del canal
(`mcp_server.py:78`).

**El CP1 ya dejó la fuente**: `get_clock()` devuelve **`t`**, que es `_ahora()` del canal
(`channel.py`, `get_clock`). Y `get_messages` devuelve cada mensaje con su `timestamp` ISO y su
`tick`.

**Dos fuentes posibles, y una es mejor:**
- **`get_clock()["t"]`** — el reloj del canal, disponible **aunque no haya ningún mensaje**;
- el `timestamp` del último mensaje recibido — también del canal, pero **no existe si el canal
  está callado**, que es justamente el caso que el ODA continuo tiene que cubrir.

**Default declarado:** el `since` sale de **`get_clock()["t"]`**. Sin tensión con nada: es
exactamente lo que el CP1 construyó.

### T3 — Requisito 2 (el log crece en silencio): se cumple, con un detalle de grano

`get_clock()` registra **una entrada por tick observado**, no por consulta (hay test del CP1).
Con el ODA continuo el device lo consulta cada vuelta, así que **el log crece con el canal
callado** ✓.

**El detalle:** si la vuelta del device es más rápida que `TICK_PERIODO_S = 1.0`, varias vueltas
caen en el mismo tick y **el log crece más lento que las vueltas**. No es un problema —el log es
de ticks, y así se diseñó— pero el test del requisito tiene que esperar **más de un período de
tick**, o pasa por no haber nada que medir. Lo digo porque es la forma de test que ya mordió tres
veces.

### T4 — LEAVE no existe como decisión, y es un cambio de fondo

**Medido:** `_decide` (`:126-161`) devuelve **`"INTERACT"` o `"OP_SILENCE"`**, y cualquier otra
cosa cae a `OP_SILENCE` (`:160`). `_interact` (`:163-186`) maneja esos dos. **`leave_channel` se
llama una sola vez, al final de `run()` (`:238`), cuando vence `duration`** — no es una decisión.

La TASK §1 pide que *"irse"* sea una acción con su primitiva, **por decisión propia y no porque
venció `duration`**. Eso toca tres lugares: el vocabulario de `_decide`, `_interact`, y el loop
(que tiene que poder terminar porque el device decidió irse).

**No es sólo agregar un `elif`:** hoy el prompt del gate (`GATE_PROMPT_04`) pide
INTERACT/OP_SILENCE. Si LEAVE entra al vocabulario, **el prompt cambia**, y eso cambia lo que el
device puede decidir. Con stubs no importa; en la corrida viva sí. **Lo señalo y no lo decido.**

### T5 — `_observe` exige un mensaje, y el ODA continuo puede no tener ninguno

**Medido:** `_observe(self, client, message)` (`:102`) recibe el mensaje disparador y lo devuelve
como `observation["trigger"]` (`:119`). `_decide` lo usa en el prompt (`:137`, `:152-153`:
`sender=trigger.get("device_id")`, `text=trigger.get("text")`).

En el ODA continuo **puede no haber trigger**: la vuelta corre igual. Así que `_observe` y el
prompt tienen que admitir *"ninguno"* — y *"ninguno"* es el silencio, que es el dato. Hoy
`trigger` nunca es None.

**Esto cambia la firma de un método que la serie congelada usó.** El freeze es una copia, así que
la serie no se toca ✓, pero **los 21 `test_caso_*` del repo vivo llaman a este device**, y no
puedo correrlos. Es el riesgo concreto del CP2a, y lo nombro antes de empezar.

### T6 — Lo que NO entra: verificado que no hace falta

delamor: *"Monitor, la Config y COCO: si hace falta tocarlos, pará y reportá."*

**Medido, y no hace falta:**
- `_observe` lee el campo con la **tool MCP** `get_monitor_state` (`:111`), no importando
  Monitor. Leer por la tool no toca su código ✓.
- El requisito 2 se cumple porque **el device** llama a `get_clock()`; **no** hace falta que
  Monitor registre nada nuevo ✓. (El límite que Opus encontró —el log es de ticks *observados* y
  hoy sólo Monitor los observa, desde `on_message`— **lo resuelve el device observando**, no un
  cambio en Monitor.)
- COCO: el device no lo toca ni por tool ✓.

**Así que el CP2a se puede hacer tocando sólo `iap_chatroom/`.** Si durante la implementación
aparece que hace falta Monitor, la Config o COCO, **paro y reporto** antes de tocarlos.

### El stub del provider

`providers/base.py` define `Provider` (ABC) con `complete(messages) -> str`. Un stub es una
subclase con una lista de respuestas y un contador — **sin red, sin claves**. Va en
`tests/`, no en `iap_chatroom/providers/`: es instrumento de test, no un provider del canal.

**Lo que el stub permite testear y lo que no:** permite el loop, el vocabulario de decisiones, el
`since`, el clock, LEAVE y las dos publicaciones seguidas. **No permite** saber qué decidiría un
modelo real — y la pregunta de la TASK (*"con el canal en silencio, un device con objetivo
**puede** hablar primero"*) es de **diseño**, no de modelo: el test verifica que el diseño **se
lo permite**, que es lo que la TASK pide textualmente.

### Costo estimado de la corrida viva, antes de que delamor decida

Con el ODA continuo y **sin** criterio local (CP2a), por device y por vuelta: **1 llamada al LLM**
(el gate) **+ 1 más si actúa**. Con el ritmo de hoy (`poll_interval = 2.0` → 0.5 vueltas/s):

| N devices | T | llamadas al LLM |
|---|---|---|
| 2 | 60 s | **60 – 120** |
| 2 | 300 s | **300 – 600** |
| 4 | 300 s | **600 – 1200** |

Hoy, con el ODA por mensaje, la serie 0.8/0.9 (N=2, T=60 s) gastaba **~2 a 20**. Con el criterio
local (CP2b) y un corte del 90%, los 60–120 bajan a **6–12**.

**No conté tokens ni dinero**: depende del provider y del tamaño de los prompts. Lo que cuento es
llamadas.

### Qué pido antes de tocar código

**Sólo T1 necesita respuesta** (P11, NO BLOQUEA, con default declarado). Las otras cinco las
reporto para que queden trazadas; T4 y T5 son cambios de fondo y las nombro ahora, no después.

**Arranco el CP2a con el default de T1** salvo que llegue otra cosa.

---

## PREGUNTA P11 — NO BLOQUEA — 2026-10-08 23:49 UTC

**`trigger_mode` no existe en el código** (T1). La TASK lo nombra como si fuera un parámetro, y
el on_message está cableado en `run()`.

**Default declarado y reversible:** creo `trigger_mode` con **`"continuo"` como único valor
aceptado**; cualquier otro levanta `ValueError` nombrando el freeze. Así el nombre que la TASK
usa existe y el modo viejo no vuelve por un default.
**Revertir:** aceptar también `"on_message"` y conservar el loop viejo detrás del parámetro.

---

## REPORTE CP2a — el ODA continuo, sin criterio local — 2026-10-09 00:07 UTC

*TASK §2.CP2, primera mitad. **Todo con stubs**: ni una llamada a provider ni a la red. La
corrida viva espera las claves. **Tocó sólo `iap_chatroom/`** — Monitor, Config y COCO no se
tocaron (T6 verificado en la evaluación).*

### Qué quedó

**`trigger_mode="continuo"`, único valor** (P11, default aceptado). Cualquier otro levanta
`ValueError` nombrando el freeze: *"el modo por mensaje quedó congelado en
`process/iap_series_freeze_20261008/`; no está detrás de un flag"*. El modo queda declarado en
cada entrada de la traza del device.

**El loop es una vuelta, no un mensaje.** `run()` junta todo lo observado desde la vuelta
anterior y **decide una vez**. Antes, cinco mensajes en un poll eran cinco decisiones.

**El orden de la vuelta, que es el que pidió Opus (T2):**

1. `get_clock()` — **antes** de pedir mensajes. De esta lectura sale el corte de la vuelta
   siguiente **y** el tick que se observa. Una sola lectura, un solo tiempo.
2. `get_messages(since)` con el corte de la vuelta anterior, **del reloj del canal**.
3. **O** — una observación, con el clock adentro y `trigger=None` si hubo silencio.
4. **D** — **una** decisión: `INTERACT`, `LEAVE` u `OP_SILENCE`.
5. **A** — la primitiva que corresponda, o ninguna.

Si un mensaje llega entre (1) y (2), aparece en la vuelta siguiente: no se pierde. En el borde
puede repetirse, y se descarta por `message_id` (`self._vistos`).

**LEAVE es una decisión** con su primitiva, y `leave_channel` se llama **una sola vez**: si el
device se fue por decisión, el final del loop no vuelve a llamarlo.

**El gate de tres opciones queda DECLARADO para que delamor lo lea antes de la corrida viva**
(T4). `GATE_PROMPT_CONTINUO`, en `autonomous_device.py`, con las tres diferencias comentadas:
tres opciones en vez de dos; el tick y el silencio en la **observación**, no en la pregunta; y
`Incoming: (ninguno)` como dato válido. Y lo que **no** dice, a propósito: no sugiere qué hacer
con el silencio, ni que hablar sea mejor que callar, ni que un Δt grande pida acción.

Una palabra que no sea una de las tres **cae a `OP_SILENCE`**: una respuesta que no se entiende
no autoriza una acción.

### Las ocho inversiones

```
=== INVERSION 14 — vuelve el ODA por mensaje
    invertido  -> FAILED test_una_decision_por_vuelta_aunque_entren_varios_mensajes
                  1 failed, 318 passed
    restaurado -> 319 passed

=== INVERSION 15 — el since vuelve al reloj del device
    invertido  -> FAILED test_el_since_sale_del_reloj_del_canal_no_del_device
                  1 failed, 318 passed
    restaurado -> 319 passed

=== INVERSION 16 — el since se lee DESPUES de get_messages
    invertido  -> FAILED test_una_decision_por_vuelta_aunque_entren_varios_mensajes
                  FAILED test_el_since_sale_del_reloj_del_canal_no_del_device
                  FAILED test_get_messages_con_el_since_real_del_device
                  FAILED test_un_mensaje_entre_get_clock_y_get_messages_no_se_pierde
                  4 failed, 315 passed
    restaurado -> 319 passed

=== INVERSION 17 — LEAVE sale del vocabulario
    invertido  -> FAILED test_leave_por_decision_propia_antes_de_duration
                  1 failed, 318 passed
    restaurado -> 319 passed

=== INVERSION 18 — el silencio vuelve a ser absorbente
    invertido  -> FAILED test_los_ticks_no_disparan_decisiones
                  FAILED test_el_silencio_no_es_absorbente
                  FAILED test_iniciativa_el_diseno_permite_hablar_primero
                  FAILED test_leave_por_decision_propia_antes_de_duration
                  FAILED test_una_palabra_desconocida_cae_a_silencio
                  FAILED test_dos_publicaciones_seguidas_sin_reaccion_a_la_propia
                  6 failed, 313 passed
    restaurado -> 319 passed

=== INVERSION 19 — _observe no pide el clock
    invertido  -> 319 passed            ← NO ROMPIÓ
    restaurado -> 319 passed

(después del arreglo, reformulada en dos:)

=== INVERSION 19bis — el loop no lee el clock
    invertido  -> FAILED test_los_ticks_no_disparan_decisiones
                  FAILED test_el_since_sale_del_reloj_del_canal_no_del_device
                  FAILED test_el_log_del_canal_crece_con_el_canal_callado
                  FAILED test_el_clock_se_lee_una_vez_por_vuelta
                  4 failed, 317 passed

=== INVERSION 20 — _observe vuelve a pedir el clock (dos lecturas)
    invertido  -> FAILED test_el_clock_se_lee_una_vez_por_vuelta
                  FAILED test_el_clock_observado_es_el_que_fija_el_corte
                  2 failed, 319 passed

    restaurado -> 321 passed
```

`grep -c INVERSION iap_chatroom/autonomous_device.py` → **0**.

### La inversión 19 no rompía, y encontró código que no hacía nada

**Sacando el `get_clock()` de `_observe` pasaban los 319.** El motivo no era un test débil: era
que **esa llamada era redundante**. `_observe` pedía el clock, y el loop **sobreescribía** el
valor dos líneas después con el suyo. Dos lecturas del mismo tiempo en la misma vuelta, y una
descartada sin que nada lo dijera.

**Lo arreglé en el código, no en el test:** `_observe(client, message=None, clock=None)` **recibe**
el clock, y el loop se lo pasa — el de la lectura única de (1), que es la que fija el corte.
Así el tick observado y el corte de la vuelta siguiente **salen de la misma lectura**, que es
exactamente lo que T2 pedía. Y hay **una llamada MCP menos por vuelta**.

Después de arreglarlo, la inversión se vuelve **dos**, y las dos rompen:
- **19bis**, el loop no lee el clock → 4 tests;
- **20**, `_observe` vuelve a pedirlo por su cuenta → 2 tests, incluido el que verifica que el
  corte y el tick observado salen de la misma lectura.

**Es el cuarto caso de la misma forma** (CP3i dos, CP1 uno, ahora éste), y los cuatro aparecieron
invirtiendo, no leyendo. Éste además no era un test flojo: era código muerto que ningún test
podía distinguir, porque su efecto se borraba solo.

### Tres de mis tests fallaron, y el código tenía razón

Sembraba mensajes **antes** de que el device arrancara y esperaba que los viera como nuevos.
**Un device que se suma no ve como "nuevo" lo que ya estaba**: el corte inicial se toma al
unirse. Es el comportamiento de siempre —`run()` tomaba `last_ts` antes del join, con un
comentario que explica por qué— y **el CP2a no lo cambia**. Los arreglé publicando después del
join, con un gancho en el stub.

**Y un cuarto fallo fue artefacto del test:** congelé el reloj del canal, y entonces el mensaje
quedaba exactamente en el corte, así que `> since` nunca pasaba. Ahora el reloj del test avanza
de a 1 ms, muy atrás del de la máquina, que es lo que el test necesita para medir el desfasaje
sin congelarlo.

Una aserción mía también estaba mal planteada: *"50 ticks no dan 50 vueltas"* se cumplía por
cualquier motivo. La nítida es **varias vueltas dentro del mismo tick** — si el tick disparara el
ciclo, un tick daría una vuelta.

### Tests

`tests/test_oda_continuo.py` — **17**, todos con stubs. `ProviderStub` devuelve respuestas de una
lista y cuenta llamadas; `ClientStub` stubbea el transporte MCP y el campo CKM **contra un
`ChatChannel` real**, así que lo del canal —CLOCK, reloj, log— no es un doble.

Cubren: los tres valores de `trigger_mode`; **una decisión por vuelta** con cinco mensajes
entrando juntos; **los ticks no disparan** (varias vueltas en el mismo tick); **el silencio no es
absorbente** (nadie publica nunca y el ciclo sigue); **iniciativa** (con el canal callado el
device **puede** hablar primero, y `n_nuevos == 0` lo prueba); **LEAVE** por decisión antes de
`duration`, con `leave_channel` una sola vez; una palabra desconocida cae a silencio; **dos
publicaciones seguidas sin reacción a la propia**; **el `since` del canal y no del device**; el
`since` **real del device** y no `canal._ahora()`; un mensaje entre `get_clock` y `get_messages`
no se pierde; **el log crece con el canal callado**, con reloj controlado y no `sleep`; y las dos
del clock leído una vez por vuelta.

**Suite: 321/321.** Ningún test existente cambió.

### Lo que el CP2a NO hizo

- **No implementó el criterio local**: es el CP2b, y espera este ALTO.
- **No implementó WAIT.** Hoy el ritmo lo fija el device con `poll_interval`, sin mínimo
  declarado. Es Calibración.
- **No tocó Monitor, la Config ni COCO** (T6).
- **No llamó a ningún provider.** El gate de tres opciones está escrito y declarado; **nadie lo
  corrió contra un modelo**.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves de provider. Y **el CP2a reemplazó el loop que los 21
  llaman**, además de cambiar la firma de `_observe` —que `test_caso_07.py` sobreescribe— y el
  vocabulario de decisiones. **Es el punto ciego más grande de toda la TASK**, y el CP2a es el
  paso que más lo agranda. La serie está a salvo en el freeze; lo que no puedo verificar es si
  esos 21 scripts del repo vivo siguen corriendo.
- **Qué decidiría un modelo real** con el gate nuevo. Los stubs prueban el diseño, no el modelo.
  La pregunta de la TASK (*"puede hablar primero"*) es de diseño y está verificada; lo que no
  está es si un modelo **lo haría**.
- **El comportamiento con dos devices a la vez.** Todos los tests corren un device. El silencio
  no absorbente con N devices —que es el fenómeno de la serie— no se testeó.
- **El costo real.** Reporté llamadas estimadas (N=2, T=60 s → 60–120), no tokens ni dinero, y
  **el corte del 90% del criterio local es un supuesto, no una medición**.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`process/iap_series_freeze_20261008/README.md:41`** sigue diciendo "67 archivos". No toqué
  `process/`.

---

## REPORTE CP2a′ — el borde de T2, el join y dos devices — 2026-10-09 00:16 UTC

*Corrección del CP2a sobre lo que Opus señaló en `f6981a9`. **Tocó sólo
`iap_chatroom/autonomous_device.py` y `tests/`.***

### El borde `timestamp == since`: Opus tiene razón, y yo estaba equivocado dos veces

**Lo que dije:** que era *"artefacto del test"*. **Lo que es:** el borde real de T2.

`get_messages` filtra con `timestamp > since`, **estricto**. Un mensaje sellado exactamente en
`t_k` que llega **después** del `get_messages` de la vuelta k no pasa `> t_k` en la k+1: se
pierde en silencio.

**Y lo peor no es el error, es cómo lo tapé.** Hice que el reloj del test **avanzara 1 ms por
llamada** para que la condición no apareciera, y después lo llamé artefacto. Es exactamente la
forma que vengo encontrando en otros tests, hecha por mí: **cambié el test para que la condición
no se diera, en vez de ver que la condición era real.**

**Implementé el solape que propuso Opus:** la vuelta usa el corte de **dos** lecturas atrás, y
los duplicados se descartan por `message_id` (`_vistos`, que ya existía para el otro borde). La
inversión 21 —volver al corte de la vuelta anterior— **rompe**
`test_el_corte_se_atrasa_una_vuelta`.

### Pero el test con reloj congelado que pidió Opus **no puede pasar**, y lo medí

Opus pidió: *"Test con reloj congelado: un mensaje sellado en el corte aparece en alguna
vuelta."*

**Medido antes de afirmarlo:**

```
RELOJ CONGELADO
  mensaje sellado en : 1791504787.62982
  cortes distintos   : 1 -> [1791504787.62982]
  todos los cortes == sellado? True
  vistos             : 0 de 1
  vueltas            : 256
```

**Con el reloj quieto todos los cortes son el mismo número**, igual al sello. El solape mueve
**cuál** corte se usa; cuando todos son el mismo, mover cuál **no cambia nada**. No es que el
solape esté mal implementado: **no puede cubrir este caso**.

**El solape sí cubre el caso real** —el reloj avanzando—, y eso lo verifican los tests del
`since` y `test_el_solape_no_duplica_mensajes`.

**El arreglo del caso congelado sería `>=` en `get_messages`** más el descarte por `message_id`
que el device ya hace. **Eso toca `get_messages`, que el enunciado excluyó: no lo toqué.**
Lo escalo.

**Y escribí el test midiendo lo que pasa, no evitándolo:**
`test_el_borde_timestamp_igual_al_corte_SIGUE_ABIERTO` afirma que **se pierde** —0 vistos, 1
corte distinto, 256 vueltas— y su docstring dice que **si algún día se arregla, este test falla,
y eso es correcto: hay que borrarlo y poner el que pidió Opus.**

No lo dejé pasando con el reloj avanzando. Eso habría sido tapar el agujero por segunda vez.

### El join deja de ser semilla, declarado

Lo agregué al docstring de `_observe`: en la serie congelada el SYSTEM *"X joined the channel"*
podía disparar el ciclo (Caso 0.5). **En el continuo nada dispara**: el join entra como
información, contado en `n_nuevos` como cualquier otro mensaje, y el lugar del seed lo ocupa la
iniciativa.

**Y mi frase era imprecisa**: dije *"el comportamiento de siempre"* sobre todo el bloque. Lo de
siempre es **el corte tomado antes del join**, no el seed. Corregido donde estaba, con la
precisión de Opus.

### Dos devices: el punto ciego que señaló Opus, cubierto con stubs

**`test_dos_devices_el_silencio_no_es_absorbente_entre_ellos`** — los dos eligen OP_SILENCE
siempre, nadie publica nunca, y **los dos siguen decidiendo** (≥3 vueltas cada uno, canal vacío).
Es el fenómeno de la serie, y antes no estaba testeado.

**`test_dos_devices_uno_habla_y_el_otro_lo_ve`** — d1 publica y d2 lo ve en su observación, y d1
**no** cuenta su propio mensaje como nuevo.

**Este segundo falló primero, y era una carrera de mi test:** d1 publicaba en su vuelta 1, que
podía caer **antes** de que d2 tomara su corte inicial — y entonces para d2 eso es historia, no
mensaje nuevo. No es un fallo del código: **un device que se suma no ve como nuevo lo que ya
estaba.** Lo arreglé haciendo que d1 calle las primeras vueltas, y lo dejé comentado en el test.

### Tests y suite

`tests/test_oda_continuo.py` — **22** (17 del CP2a + 5): el corte atrasado una vuelta, el borde
congelado que sigue abierto, el solape que no duplica, el join que no dispara, y los dos de dos
devices.

**Suite: 326/326.** Ningún test existente cambió. Un test **mío** del CP2a se reemplazó:
`test_el_clock_observado_es_el_que_fija_el_corte` **dejó de ser cierto a propósito** —el corte se
atrasa ahora— y pasó a `test_el_corte_se_atrasa_una_vuelta`.

**Inversión 21** — el corte vuelve a ser el de la vuelta anterior:
`FAILED test_el_corte_se_atrasa_una_vuelta`, 1 failed 325 passed. Restaurado: 326 passed.
`grep -c INVERSION` → 0.

### Lo que escalo

**El borde con reloj congelado necesita `>=` en `get_messages`.** No lo toqué porque el enunciado
excluyó `get_messages` y porque cambiar `>` por `>=` cambia el comportamiento para **todos** los
que la llaman —los 21 `test_caso_*`, que no puedo correr, y `_observe` con `since=None`—. Es
E3-ish: cambia qué entrega el canal. **Decide delamor.**

Si se arregla: el device ya descarta por `message_id`, así que del lado del device no hace falta
nada más, y el test que afirma el agujero **tiene que fallar** y ser reemplazado.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves. Y el CP2a′ **volvió a tocar el loop** que los 21 llaman.
- **Si dos devices contra el server real se comportan como contra el stub.** Los dos tests de dos
  devices corren con `ClientStub` sobre un `ChatChannel` real, pero **sin MCP, sin red y sin
  server**. El orden de las vueltas en un `asyncio.gather` local no es el de dos procesos.
- **Qué decidiría un modelo real.** Sigue sin correrse nada contra un provider.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`process/iap_series_freeze_20261008/README.md:41`** sigue diciendo "67 archivos". No toqué
  `process/`.

---

## REPORTE CP2a″ — la ventana en tiempo, y lo que preguntó delamor — 2026-10-09 00:30 UTC

*Cierra el CP2a. **Tocó sólo `iap_chatroom/autonomous_device.py` y `tests/`.***

### La ventana en tiempo cierra el borde

Implementado lo que corrigió Opus: **`since = t − periodo_s`**, una ventana **en tiempo**, no en
vueltas. Se fue la lista de cortes; el código quedó más corto.

**El test que Opus había pedido ahora pasa:** con el reloj congelado, un mensaje sellado
exactamente en el instante del corte **aparece**, y aparece **una sola vez** — la ventana lo
devuelve en varias vueltas y `_vistos` descarta las repeticiones.
`test_el_borde_timestamp_igual_al_corte_SIGUE_ABIERTO` se borró, como su propio docstring
anticipaba, y lo reemplaza `test_un_mensaje_sellado_en_el_corte_no_se_pierde`.

**El grano lo trae el propio clock** (`periodo_s`), no una constante cableada en el device.

### Un efecto de la ventana que no estaba visto

**La ventana inicial alcanza un tick hacia atrás del join.** Lo encontró un test que escribí
esperando lo contrario: lo publicado **dentro** de ese tick, antes de que el device existiera,
**cuenta como nuevo**. Está acotado a un tick y es el precio de cerrar el borde.
`test_la_ventana_inicial_alcanza_un_tick_hacia_atras` lo fija, y
`test_lo_publicado_antes_del_corte_no_cuenta_pero_esta_en_history` usa **tres** ticks de
distancia para medir lo otro.

### Las dos preguntas de delamor cambiaron el diseño

**`"¿y si clock llega sin el periodo_s?"`** — mi código hacía `clock.get("periodo_s") or 0.0`.
Una ventana de **0** deja el corte en `t` exacto: **el agujero que la ventana acababa de cerrar,
reintroducido en silencio por el fallback.** Es NOMINAL por ausencia (`c06db07`), en el mismo
commit donde lo estaba arreglando.

**`"¿UNKNOWN? ¿podría ser?"`** — mi segunda respuesta fue **levantar**. Levantar nombra la
ausencia, pero **mata el instrumento**: el device deja de observar. Y el criterio del proyecto no
es ése: `temp_signal` devuelve `"UNKNOWN"` y sigue, `_classify_zone` devuelve UNKNOWN y no
dispara STOP. **UNKNOWN no autoriza una acción; no termina el proceso.**

**La tercera versión es la que quedó: UNKNOWN, y el corte no avanza.** Devuelve `None`, queda
registrado en la traza de cada vuelta (`"ventana": "UNKNOWN"`), y el loop **conserva el `since`
anterior**. Quedarse atrás produce **duplicados**, que `_vistos` ya descarta, y **nunca
pérdidas** — que es el daño que importa. **La dirección segura es hacia atrás.**

Las tres respuestas quedaron escritas en el docstring de `_ventana`, con por qué se descartaron
las dos primeras y la pregunta citada. Y `bool` se excluye a propósito: `True` es `int` en
Python, y 1.0 sería un grano inventado.

### Las tres inversiones

```
=== INVERSION 22 — sin ventana en tiempo (corte en t exacto)
    invertido  -> FAILED test_el_corte_se_atrasa_un_tick
                  FAILED test_un_mensaje_sellado_en_el_corte_no_se_pierde
                  FAILED test_la_ventana_inicial_alcanza_un_tick_hacia_atras
                  3 failed, 334 passed
    restaurado -> 337 passed

=== INVERSION 23 — el fallback vuelve a 0.0 (NOMINAL por ausencia)
    invertido  -> FAILED test_un_clock_sin_periodo_s_es_UNKNOWN_y_el_ciclo_sigue
                  FAILED test_un_periodo_s_invalido_es_UNKNOWN[None]
                  FAILED …[0]  …[0.0]  …[-1.0]  …[un segundo]  …[True]
                  7 failed, 330 passed
    restaurado -> 337 passed

=== INVERSION 24 — con UNKNOWN el corte avanza igual (a t exacto)
    invertido  -> 337 passed            ← NO ROMPIÓ
    restaurado -> 337 passed
    (tras agregar un test)
    invertido  -> FAILED test_sin_grano_Y_con_reloj_congelado_el_corte_quieto_salva_el_mensaje
                  1 failed, 337 passed
    restaurado -> 338 passed
```

`grep -c INVERSION` → **0**.

### La inversión 24 no rompía, y el motivo es el de siempre

**Mi test del camino UNKNOWN no ejercitaba el caso donde "no avanzar" importa.** Con el reloj
**avanzando**, dejar que el corte avance a `t` exacto **igual deja pasar** el mensaje, porque el
sello queda después de la lectura. El riesgo está con el reloj **congelado**: ahí `t` **es** el
sello, y avanzar el corte lo pierde para siempre.

El test nuevo pone las dos condiciones juntas —**sin grano y con el reloj congelado**— y
entonces la inversión rompe. **Quinto caso de la misma forma**, y como los otros cuatro:
apareció invirtiendo, no leyendo.

### El lado faltante del join

`test_lo_publicado_antes_del_corte_no_cuenta_pero_esta_en_history`, con **orden fijo** y sin
carrera: lo publicado tres ticks antes de que el device exista **no** cuenta en `n_nuevos`, y
**sí** está en `history` —porque `_observe` pide el historial con `since=None`—. Es lo que el
CP2a llamó *"el comportamiento de siempre"*, ahora medido por los dos lados.

### Tests y suite

`tests/test_oda_continuo.py` — **34**. Nuevos en este sub-paso: el corte atrasado un tick; el
mensaje sellado en el corte que ya no se pierde; el alcance de la ventana inicial; el clock sin
grano que es UNKNOWN y no detiene el ciclo; `periodo_s` inválido en seis formas; el ancho que
sale del clock; la ventana en la traza; el caso sin grano **y** con reloj congelado; y el lado
faltante del join.

**Suite: 338/338.** Ningún test existente ajeno cambió. Dos tests **míos** se reemplazaron
porque dejaron de ser ciertos a propósito: `…_SIGUE_ABIERTO` (el agujero se cerró) y
`test_el_corte_se_atrasa_una_vuelta` (el solape pasó a ser en tiempo).

### Lo que NO entra, y lo que queda declarado

- **La ventana cubre resoluciones de reloj menores que un tick.** Si dos mensajes caen en el
  mismo instante y uno llega después del `get_messages`, la ventana lo alcanza.
- **`_vistos` crece durante la sesión.** Un device largo acumula `message_id`. No lo acoté: con
  los tamaños de la serie no es un problema, y acotarlo sería inventar un límite.
- **No toqué `get_messages`.** El `>=` ya no hace falta: la ventana cierra el borde desde el
  lado del device.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves. El CP2a″ volvió a tocar el loop.
- **Si un `periodo_s` que cambia a mitad de sesión se maneja bien.** La ventana se recalcula en
  cada vuelta, así que debería, pero **no lo testeé**: el canal hoy lo tiene constante.
- **Dos devices contra el server real.** Los tests de N=2 corren con `ClientStub` sobre un
  `ChatChannel` real: sin MCP, sin red, sin server.
- **Qué decidiría un modelo real.** Nada se corrió contra un provider.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`process/iap_series_freeze_20261008/README.md:41`** sigue diciendo "67 archivos".

---

## REPORTE CP2v — preparación del primer vivo — 2026-10-09 00:58 UTC

*Orden de delamor: **CP2v → primer vivo con Groq → CP2b**. El vivo va antes del CP2b para medir
las llamadas sin filtro: es la línea de base contra la que el criterio local se va a medir.
**Todo con stubs. Ni una llamada a provider.** Tocó sólo `iap_chatroom/autonomous_device.py` y
`tests/`.*

### 1. Las llamadas al LLM se cuentan, no se infieren

Cada vuelta registra **`llamadas_llm`**: las que esa vuelta hizo de verdad. Hoy toda vuelta llama
al gate, así que vueltas = llamadas — **pero con el criterio local (CP2b) deja de ser cierto**, y
la inferencia se rompe justo cuando el filtro entra. Por eso se cuentan.

**Una llamada que falló igual se cuenta**: se hizo, y para costo eso es lo que importa.

Y un método **`costo()`**: vueltas, llamadas, llamadas por vuelta, errores con su causa y fase,
ilegibles con su respuesta cruda, decisiones por tipo, vueltas con `ventana` UNKNOWN, y el ritmo
declarado.

### 2. Las dos ausencias de la misma función, las dos a UNKNOWN

| qué pasó | antes | ahora | se cuenta en |
|---|---|---|---|
| el provider falla | `OP_SILENCE` | **`UNKNOWN`** | `errores_llm` |
| la respuesta no es una de las tres palabras | `OP_SILENCE` | **`UNKNOWN`** | `ilegibles` |

**`OP_SILENCE` es una decisión que el modelo tomó; ninguna de las dos lo es.** Confundirlas hace
que un vivo silencioso no se pueda atribuir — que es exactamente lo que el primer vivo tiene que
separar. UNKNOWN es el estado del que observa, no un valor de la escala (§19, `c06db07`), y **no
autoriza ninguna acción**: `_interact` no publica ni se va con UNKNOWN.

La primera la corrigió Opus; **la segunda no me había llegado** y delamor me la pasó. Estaban a
una línea de distancia en la misma función.

**Dos causas, una consecuencia, y se registran por separado**: para atribuir no es lo mismo que
falle la infraestructura que el modelo conteste algo ilegible.

### 3. La respuesta cruda, con su causa

Pedido de **Opus** para el vivo con el 8B. Cada ilegible guarda
`causa: "respuesta_ilegible"`, **`respuesta_cruda`** sin `strip` ni `upper`, `truncada`, `largo`,
`fase`, `provider` y `model`. Truncada a 500 **y declarado si se truncó**. Un vacío también es
ilegible y guarda `""`.

Sin el texto, "ilegible" es un número y no se puede mirar. Con el texto se ve si el problema está
en el gate —el prompt pide una palabra y el modelo contesta una frase— o en el modelo.

### 4. El 429 aparte, y **cómo se supo**

`status_code` primero —`status_code`, `status`, `code`, `http_status`—, y las firmas de texto como
**respaldo declaradamente heurístico**. La traza dice cuál de los dos fue:
**`rate_limit_segun: "status_code" | "texto" | None`**.

Un 429 leído del atributo **es un dato**; inferirlo del mensaje **es una heurística**, y no es lo
mismo. Las firmas pueden dar falsos positivos —un mensaje que diga "quota" sin ser un 429— y
falsos negativos; si no matchea, el error queda genérico y **igual se registra**. Un 500 no se
marca.

El 429 no dice "algo se rompió": dice **"vas demasiado rápido"**. Es información sobre el ritmo.

### 5. El ritmo declarado, sin inventar el límite

`ritmo_declarado(n_devices)` devuelve vueltas por minuto, piso y techo de llamadas, y
**`limite_de_la_cuenta: "UNKNOWN — se lee en la consola del provider"`**.

Con **`poll_interval = 2.0` y 2 devices: 60 a 120 llamadas por minuto.** Ese es el número a
comparar contra la cuenta de Groq. **El límite no lo invento.** Con `poll_interval = 0` el ritmo
lo fija la latencia y **no se puede declarar de antemano**: devuelve `None`.

### 6. El instrumento mentía, y era el peor lugar

**El `ProviderStub` agotado devolvía `"OP_SILENCE"`.** O sea que **fabricaba decisiones**: una
vuelta sin respuesta guionada producía un *"el modelo decidió callar"* que nadie decidió. Un
instrumento de medición rellenando la ausencia con el valor más tranquilizador.

Lo señaló Opus. Ahora devuelve **vacío → UNKNOWN**.

**Rompió tres tests, y eso era el punto:** `test_el_silencio_no_es_absorbente`,
`test_una_palabra_desconocida…` y `test_el_costo_registra_provider_y_modelo` estaban midiendo
contra decisiones del instrumento. Les di respuestas **explícitas** —2000 cada uno— para que el
silencio que miden sea **decidido**. Y el test nuevo pasa `[]`: con cero respuestas guionadas,
todas las vueltas son UNKNOWN.

### 7. `"?"` → `None`, y un quinto que encontré

`provider` sin nombre quedaba en `"?"`. Es un valor inventado: pasó a **`None`**.

Y buscando los `"?"` apareció uno que no estaba en la lista:
**`m.get("timestamp", "?")` ponía `"?"` en el prompt que el modelo lee.**

> ### ⚠ CAMBIO DEL GATE — delamor lo lee antes del vivo
>
> **El timestamp ausente en el historial pasó de `[?]` a `[UNKNOWN]`.** Es **texto que el modelo
> ve**, no traza interna: `"?"` no le dice nada, `UNKNOWN` le dice que el dato no estaba.
>
> Se suma a lo que ya estaba declarado del gate: las **tres opciones**
> (`INTERACT` / `LEAVE` / `OP_SILENCE`), el bloque `Channel clock: tick=… (clock source…, tick
> period…)`, `New since your last turn`, `Incoming: (ninguno)` para el silencio, y
> `You are not obligated to act.`
>
> Hay un test que verifica que **`[?]` no aparece en ningún prompt**.

**Y lo que NO toqué, por indicación de Opus:** el resto del prompt sigue mostrando `None` —
`D_ckm=None`, `c_S=None`, `fi=None`, `Delta_r=None`. **No unifiqué `None` y `UNKNOWN` ahí.** Está
entre lo que delamor lee del gate y es decisión suya; hasta entonces queda como está.

### Las nueve inversiones

```
=== 25 las llamadas se infieren       -> 2 failed, 342 passed  | restaurado 344
=== 26 el error se traga              -> 2 failed, 342 passed  | restaurado 344
=== 27 la llamada que falla no cuenta -> 1 failed, 343 passed  | restaurado 344
=== 28 un error al generar publica    -> 1 failed, 343 passed  | restaurado 344
=== 29 el error vuelve a OP_SILENCE   -> 3 failed, 350 passed  | restaurado 353
=== 30 el ilegible vuelve a OP_SILENCE-> 7 failed, 346 passed  | restaurado 353
=== 31 la cruda se guarda normalizada -> 1 failed, 352 passed  | restaurado 353
=== 32 UNKNOWN autoriza acción        -> 3 failed, 350 passed  | restaurado 353
=== 33 el 429 no se distingue         -> 1 failed, 352 passed  | restaurado 353
=== 34 el stub agotado da OP_SILENCE  -> FAILED test_el_stub_agotado_no_fabrica_decisiones
                                         1 failed, 359 passed  | restaurado 360
=== 35 el 429 solo por texto          -> FAILED test_un_429_por_status_code_se_lee_del_dato
                                         1 failed, 359 passed  | restaurado 360
=== 36 provider sin nombre -> "?"     -> 360 passed  ← NO SE APLICÓ DONDE DEBÍA
=== 37 timestamp -> "?"               -> 360 passed  ← NO SE APLICÓ (escapeo roto)

(repetidas bien:)
=== 36bis el provider de costo() -> "?"  -> FAILED test_un_provider_sin_nombre_queda_en_None…
                                            1 failed, 359 passed
=== 37bis el timestamp -> "?"            -> FAILED test_un_mensaje_sin_timestamp_dice_UNKNOWN…
                                            1 failed, 359 passed
    restaurado -> 360 passed
```

`grep -c INVERSION` sobre el device y el test → **0 y 0**.

### Dos inversiones mías no midieron nada, y lo digo

- **La 37 no se aplicó**: el escapeo de las comillas en el shell falló y el `python` levantó
  `NO ENCONTRE`. **Ese "360 passed" no significaba nada**, y si no hubiera leído la salida
  completa lo habría reportado como "no rompe".
- **La 36 se aplicó a la línea equivocada**: reemplazó el `provider` de `_ilegibles`, no el de
  `costo()`, porque usé la primera coincidencia del texto y había tres iguales. **Mi test estaba
  bien; mi inversión estaba mal apuntada.**

Las dos repetidas con precisión rompen el test que les corresponde. Lo reporto porque **una
inversión que no se aplica se ve igual que una que no rompe**, y la diferencia es todo.

### Tests y suite

`tests/test_oda_continuo.py` — **56**. Nuevos en el CP2v: llamadas contadas; dos llamadas si
publica; el error registrado con el ciclo siguiendo; el error al generar que no publica;
provider y modelo en el costo; vueltas con ventana UNKNOWN; la palabra desconocida como UNKNOWN;
error e ilegible por separado; el 429 marcado; el no-429; el ritmo declarado; sin pausa no se
declara; la cruda entera y sin normalizar; la larga truncada; la vacía; las causas de los
errores; el stub que no fabrica; el 429 por `status_code`; el 429 por texto; el 500; el provider
sin nombre; y el timestamp UNKNOWN en el prompt.

**Suite: 360/360.** Ningún test ajeno cambió. **Tres tests míos** cambiaron porque el stub dejó
de fabricar decisiones.

### Lo que falta para el vivo, y no es mío

1. **`GROQ_API_KEY` como secret del Codespace** — nunca en el repo.
2. **El límite de la cuenta de Groq**, para comparar contra los 60–120 por minuto.
3. **Que delamor lea el gate**: las tres opciones, el bloque del clock, `Incoming: (ninguno)`, el
   `[UNKNOWN]` del timestamp, y el `None` del resto del prompt que **no** unifiqué.
4. **El modelo del primer vivo**: `llama-3.1-8b-instant` por decisión de Opus.
   `llama-3.3-70b-versatile` queda disponible.

### No pude revisar

- **Los 21 `test_caso_*`**: sin claves. Con la clave, Opus dejó registrado correr los que usen
  **sólo Groq**, para achicar este punto ciego.
- **Si Groq con el 8B contesta el gate con una sola palabra.** Es lo primero que el vivo va a
  mostrar, y `respuesta_cruda` está puesto justamente para eso.
- **Si las firmas de texto del 429 matchean lo que devuelve el SDK de Groq.** `status_code` va
  primero y debería alcanzar, pero **no lo vi contra un 429 real**.
- **El precio.** Cuento llamadas, no tokens ni dinero.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`process/iap_series_freeze_20261008/README.md:41`**, que sigue diciendo "67 archivos".

---

## ARRANQUE — 2026-10-09 04:13 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8, antes del primer vivo.*

### Revisé

1. **Locks:** ninguno. **`git pull --rebase`:** limpio, HEAD en `c93ce87`. **`git status`:** sin
   nada modificado.
2. **`GROQ_API_KEY`: presente**, 56 caracteres, empieza `gsk_`. Nunca la imprimí entera ni la
   escribí en ningún archivo.
3. **El gate está congelado:** `git diff f96c234 HEAD -- iap_chatroom/autonomous_device.py` →
   **vacío**. No se tocó.
4. **Tests:** **360/360**.
5. **`DECISIONES_opus.md`** → leídas las entradas del cierre del CP2v y las del gate.

### Preguntas abiertas

**Ninguna.** P1–P10 respondidas. La próxima es **P11**.

### No pude revisar

- **Los 21 `test_caso_*`**: con la clave ya se podrían correr los de sólo Groq, pero **el vivo
  iba primero** por el orden de delamor. Siguen sin correr.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.
- **`process/iap_series_freeze_20261008/README.md:41`**, que sigue diciendo "67 archivos".

---

## REPORTE PRIMER VIVO — 2026-10-09 04:13 UTC

*`experiments/vivo_01_groq_8b.py`, una corrida. Log:
`experiments/vivo_01_groq_8b_log.json`. **No arreglé nada.***

### Lo declarado antes de correr

2 devices · `GroqProvider("llama-3.1-8b-instant")` · `poll_interval = 5.0` · `duration = 60.0` ·
gate congelado en `f96c234` · `WELCOME MSG` = `SYSTEM_PROMPT_04A` · una sola corrida.
Server del canal en otro proceso del mismo host.

### El error, entero y literal

**Las 24 llamadas al LLM fallaron, todas con el mismo error:**

```
causa:             error_provider
fase:              decide
excepcion:         NotFoundError
mensaje:           Error code: 404 - {'error': {'message': 'The model
                   `llama-3.1-8b-instant` does not exist or you do not have
                   access to it.', 'type': 'invalid_request_error',
                   'code': 'model_not_found'}}
provider:          groq
model:             llama-3.1-8b-instant
rate_limit:        False
rate_limit_segun:  None
```

**El modelo que Opus eligió para el primer vivo no existe, o la cuenta no tiene acceso.** Lo dice
Groq, no yo. **No lo cambié por otro.**

### `costo()` de cada device

| | `GroqLlama8B_1` | `GroqLlama8B_2` |
|---|---|---|
| provider · model | groq · `llama-3.1-8b-instant` | groq · `llama-3.1-8b-instant` |
| **vueltas** | **12** | **12** |
| **llamadas_llm** | **12** | **12** |
| llamadas_por_vuelta | 1.0 | 1.0 |
| **errores_llm** | **12** | **12** |
| errores_rate_limit | **0** | **0** |
| **ilegibles** | **0** | **0** |
| vueltas_con_ventana_unknown | 0 | 0 |
| **decisiones_por_tipo** | **`{'UNKNOWN': 12}`** | **`{'UNKNOWN': 12}`** |

**Ningún error fatal:** `errores_fatales: []`. Los dos devices corrieron los 60 s completos
(61.91 s reales) y terminaron solos.

### `ritmo_declarado(2)`

```
poll_interval_s:                 5.0
n_devices:                       2
vueltas_por_minuto_por_device:   12.0
llamadas_por_minuto_piso:        24.0
llamadas_por_minuto_techo:       48.0
limite_de_la_cuenta:             UNKNOWN — se lee en la consola del provider
```

**Lo declarado coincide exactamente con lo medido: 12 vueltas por device, 24 llamadas en total.**
El piso era 24 por minuto y hubo 24 en 60 s. Es la primera vez que el ritmo declarado se puede
comparar contra una corrida real, y da.

### El clock del canal

```
clock final: tick=87 · t=1791519133.63 · reloj=canal · periodo_s=1.0 · t0=1791519046.26
```

**¿Crece en silencio? Sí, y se ve en la traza de los devices.** Los ticks observados por el
device 1, vuelta por vuelta: **25 → 31 → 36 → … → 82**, con **`n_nuevos = 0` desde la vuelta 2**.
El canal estuvo callado desde el segundo 5 y el tick siguió avanzando.

`ventana: 1.0` en las 24 vueltas: el `periodo_s` llegó siempre, nunca hubo UNKNOWN de grano.

**No pude leer el `clock_log` del canal.** Vive en el proceso del server y **no hay endpoint que
lo exponga**. Lo que sí tengo es el tick observado en cada vuelta, que es la misma información
vista del lado del device. **Es una mejora concreta para la lista: exponer `clock_log` por una
tool o por la API.**

### Mensajes publicados: 2, los dos del canal

```
msg-0 · system · SYSTEM · "GroqLlama8B_2 joined the channel" · tick 25 · reloj canal
msg-1 · system · SYSTEM · "GroqLlama8B_1 joined the channel" · tick 25 · reloj canal
```

**Ningún device publicó**, y no porque haya decidido callar: **nunca pudo decidir**. Las 24
decisiones son `UNKNOWN`.

Y acá está lo que el CP2v vino a hacer: **este silencio es atribuible**.
`errores_llm = 12`, `ilegibles = 0`, `decisiones_por_tipo = {'UNKNOWN': 12}`, `rate_limit = 0`.
**No fue el modelo callando, no fue el canal perdiendo mensajes, no fue rate limit: fue un 404 de
infraestructura.** Con la traza anterior —que caía a `OP_SILENCE`— esto se habría leído como
*"los dos devices eligieron el silencio 24 veces"*, que es exactamente la lectura falsa que la
serie congelada no podría descartar.

### El `monitor_state` del canal

```
corpus_size: 10 · n_nodes: 32 · message_count: 2
D_ckm: None · temp_signal: None · n_agentes: 1 · corpus_status: operational
```

Dos cosas que **no interpreto** y reporto:
- **`corpus_size: 10` con `message_count: 2`.** El corpus traía 8 textos de antes —el
  `_state/corpus_state.json` persistido— y sumó los 2 joins. **El estado de disco no se limpió
  antes del vivo**, y nadie lo declaró. Va a la lista.
- **`n_agentes: 1` con 2 devices registrados.** No sé por qué. No lo toqué.
- `temp_signal: None` — no `"UNKNOWN"`. Es una de las grafías de la ausencia que delamor está
  leyendo, y aparece en vivo.

### Primera vuelta, literal

```
{'vuelta': 1, 'tick': 25, 'tick_anterior': -1, 'reloj': 'canal', 'n_nuevos': 2,
 'trigger': 'msg-1', 'decision': 'UNKNOWN', 'trigger_mode': 'continuo',
 'ventana': 1.0, 'llamadas_llm': 1, 'errores_llm': 1, 'ilegibles': 0}
```

**`n_nuevos: 2` en la vuelta 1:** cada device vio **los dos** joins, incluido el propio —el join
lo publica `system`, no el device, así que el filtro del propio `device_id` no lo saca—. Lo
reporto porque es el join entrando **como información**, que es lo que el CP2a′ declaró, y acá se
ve: el `trigger` fue `msg-1` y no disparó nada; la decisión salió igual.

### Mejoras y bugs que el vivo mostró

1. **El modelo del primer vivo no existe.** 404 de Groq. **[Opus/delamor]** — no lo cambié.
2. **`clock_log` no se puede leer desde afuera del proceso del server.** No hay tool ni endpoint.
   **Mejora concreta.**
3. **El `_state/` no se limpia ni se declara antes de un vivo.** `corpus_size: 10` con 2
   mensajes: el corpus arrancó con 8 textos de agosto. **Para que un vivo sea atribuible, el
   estado de partida tiene que estar declarado o vacío.**
4. **`n_agentes: 1` con 2 devices.** No sé si es bug o es qué cuenta. **No lo investigué.**
5. **`temp_signal: None`** en vivo, no `"UNKNOWN"`. Es la sexta grafía, y confirma que la lista
   que delamor está leyendo tiene efecto observable.
6. **Nada se rompió.** Ningún traceback, ningún error fatal, los dos devices completaron los 60 s
   y se fueron solos con `leave_channel`. **El canal y el ODA continuo aguantaron una corrida
   real con el provider fallando en todas las vueltas.**

### No pude revisar

- **Si el canal funciona con el modelo respondiendo.** Este vivo midió el canal y la
  infraestructura **con el provider caído**, que es la mitad de lo que hay que ver. La otra mitad
  necesita un modelo que exista.
- **El `clock_log`**, por lo de arriba.
- **Si el 429 se detecta bien**: no hubo ninguno. `status_code` leyó bien el **404**
  (`rate_limit: False`), que es la contraparte útil — el camino de `status_code` funcionó contra
  un error real.
- **Los 21 `test_caso_*`.**
- **El costo en dinero.** 24 llamadas, todas 404. **No sé si un 404 se cobra.**
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.

---

## ARRANQUE — 2026-10-09 04:21 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8, antes del vivo 02.*

### Revisé

1. **Locks:** ninguno. **`git pull --rebase`:** limpio, HEAD en `ad6d2da`. **`git status`:**
   nada modificado.
2. **`GROQ_API_KEY`: presente**, 56 chars, prefijo `gsk_`. **Nunca la imprimí.**
3. **El gate sigue congelado:** `git diff f96c234 HEAD -- iap_chatroom/autonomous_device.py`
   → **vacío**.
4. **Tests: 360/360.**

### Preguntas abiertas

**Ninguna.** La próxima es **P11**.

### No pude revisar

- Los 21 `test_caso_*`; el chat; el estado del Codespace fuera de git; el clon local.
- `process/iap_series_freeze_20261008/README.md:41`, que sigue diciendo "67 archivos".

---

## REPORTE VIVO 02 — el modelo responde, y elige el silencio — 2026-10-09 04:21 UTC

*`experiments/vivo_02_groq_gptoss20b.py`, una corrida. Log:
`experiments/vivo_02_groq_gptoss20b_log.json`. **No arreglé nada.***

### 1. Los modelos de la cuenta, y una infraestructura que no era la clave

**El `GET` crudo a `https://api.groq.com/openai/v1/models` da `403` con cuerpo
`error code: 1010` y `Content-Type: text/plain`.** Eso **no es un error de la API de Groq: es
Cloudflare** bloqueando por firma del cliente —`urllib` manda un user-agent de Python—. **La
clave no tenía nada que ver.**

Con el **SDK de Groq**, el mismo endpoint responde. **Los 11 modelos de la cuenta:**

```
allam-2-7b
canopylabs/orpheus-arabic-saudi
canopylabs/orpheus-v1-english
meta-llama/llama-prompt-guard-2-22m
meta-llama/llama-prompt-guard-2-86m
openai/gpt-oss-120b
openai/gpt-oss-20b
openai/gpt-oss-safeguard-20b
qwen/qwen3.8-27b
whisper-large-v3
whisper-large-v3-turbo
```

**`llama-3.3-70b-versatile` no está.** Y **no hay ningún modelo de chat con "llama"**: los dos
`meta-llama/llama-prompt-guard-2-*` son **clasificadores de prompt-guard**, no modelos de chat —
no contestan un gate con una palabra.

### 2. El modelo elegido, declarado

**`openai/gpt-oss-20b`.** La regla decía *"el primero con llama o gpt-oss"*, y la lectura literal
daba dos opciones malas: un `prompt-guard` (no es de chat) o `gpt-oss-120b` (alfabéticamente
primero, más caro). **Elegí el `gpt-oss` más chico**, por el criterio económico del plan. Está en
la lista. **Declarado y reversible.**

### 3. Estado de partida, declarado y sin limpiar

Leído por MCP **antes** de arrancar:

```
corpus_size: 10 · message_count: 0 · n_nodes: 32 · n_agentes: 0
D_ckm: None · temp_signal: None · corpus_status: operational
mensajes en el canal: 0 · clock tick: 15
en disco: corpus_state.json con 10 textos · monitor_trajectory.jsonl con 4 líneas
```

**Los 10 son 8 textos de agosto más los 2 joins del vivo 01**, que quedaron escritos. **No limpié
nada**, como se pidió.

**Y encontré que el endpoint REST no sirve para esto:** `GET /api/monitor/state` devolvió **`None`
en todos los campos**. Lo leí por la tool MCP, que sí funciona. **No lo arreglé.**

### 4. `costo()` de cada device

| | `GroqGptOss20B_1` | `GroqGptOss20B_2` |
|---|---|---|
| provider · model | groq · `openai/gpt-oss-20b` | groq · `openai/gpt-oss-20b` |
| **vueltas** | **11** | **12** |
| **llamadas_llm** | **11** | **12** |
| llamadas_por_vuelta | 1.0 | 1.0 |
| **errores_llm** | **0** | **0** |
| errores_rate_limit | **0** | **0** |
| **ilegibles** | **0** | **0** |
| vueltas_con_ventana_unknown | 0 | 0 |
| **decisiones_por_tipo** | **`{'OP_SILENCE': 11}`** | **`{'OP_SILENCE': 12}`** |

**`errores_fatales: []`.** 65.41 s reales. Los dos terminaron solos.

**23 llamadas, 0 errores, 0 ilegibles.** El modelo contestó **una sola palabra del vocabulario en
las 23**, sin una sola respuesta fuera de las tres opciones. El gate congelado funcionó con un
modelo de 20B.

### 5. `ritmo_declarado(2)`

```
poll_interval_s: 5.0 · vueltas_por_minuto_por_device: 12.0
llamadas_por_minuto_piso: 24.0 · techo: 48.0
limite_de_la_cuenta: UNKNOWN — se lee en la consola del provider
```

Medido: **23 llamadas** contra un piso declarado de 24. El device 1 dio **11 vueltas y el 2 dio
12**: la diferencia es la latencia del provider sumada al `poll_interval`, y el vivo 01 —donde
los 404 volvían al instante— dio 12 y 12. **El ritmo real es el declarado menos la latencia.**

### 6. El clock

```
clock final: tick=111 · periodo_s=1.0 · reloj=canal · t0=1791519490.32
```

**Crece en silencio, y se ve:** ticks del device 1 **46 → 52 → 57 → … → 101**, con
**`n_nuevos = 0` desde la vuelta 2**. `ventana: 1.0` en las 23 vueltas, nunca UNKNOWN de grano.

**Sigue sin poder leerse el `clock_log`** desde afuera del proceso del server: no hay tool ni
endpoint. Es la misma mejora pendiente del vivo 01.

### 7. Mensajes publicados: 2, los dos del canal

```
msg-0 · system · SYSTEM · "GroqGptOss20B_2 joined the channel" · tick 46
msg-1 · system · SYSTEM · "GroqGptOss20B_1 joined the channel" · tick 46
```

**Ningún device publicó.** Y acá está la diferencia con el vivo 01:

| | vivo 01 | vivo 02 |
|---|---|---|
| decisiones | `{'UNKNOWN': 24}` | **`{'OP_SILENCE': 23}`** |
| errores_llm | 24 | **0** |
| ilegibles | 0 | 0 |
| mensajes de devices | 0 | 0 |

**Los dos vivos terminaron con el canal callado, y son dos silencios distintos.** El del 01 fue
infraestructura; **el del 02 lo decidió el modelo 23 veces, sin un solo error.** La traza
distingue las dos cosas, que es exactamente para lo que se construyó.

**No interpreto por qué el modelo eligió callar.**

### 8. `monitor_state` al cerrar

```
corpus_size: 12 · n_nodes: 32 · message_count: 2
D_ckm: None · temp_signal: None · n_agentes: 1 · corpus_status: operational
```

- `corpus_size` pasó de **10 a 12**: entraron los 2 joins. **El vivo escribe en `_state/`**, así
  que el próximo arranca con 12.
- **`n_agentes: 1` con 2 devices registrados**, igual que en el vivo 01. **Se repite.** No sé qué
  cuenta. **No lo investigué.**
- `temp_signal: None`, no `"UNKNOWN"`. Se repite.

### Mejoras y bugs que el vivo 02 mostró

1. **`GET /api/monitor/state` devuelve `None` en todos los campos.** La tool MCP del mismo
   nombre funciona. **Bug nuevo.**
2. **El `GET` crudo a la API de Groq da 403 de Cloudflare.** Hay que usar el SDK. **No es la
   clave**, y conviene que quede dicho para no volver a sospecharla.
3. **`clock_log` sigue sin ser legible desde afuera.** Repetido del vivo 01.
4. **El `_state/` se acumula entre vivos** y nadie lo declara: 10 → 12. **Repetido, y ahora
   medido en dos corridas.**
5. **`n_agentes: 1` con 2 devices.** **Repetido.**
6. **El ritmo real es el declarado menos la latencia:** 11 y 12 vueltas contra 12 declaradas.
   `ritmo_declarado` da el **piso teórico**, no el observado. **Mejora: que la traza compare los
   dos.**
7. **Nada se rompió.** Ningún traceback. **Y el gate congelado funcionó: 23 de 23 respuestas
   dentro del vocabulario, con un modelo de 20B.**

### No pude revisar

- **Por qué el modelo eligió callar.** No interpreto, y el objetivo era canal e infraestructura.
- **El `clock_log`**, por lo de arriba.
- **Si el 429 se detecta**: no hubo ninguno. Lo que sí se verificó contra un error real fue el
  **404** del vivo 01, por `status_code`.
- **Los 21 `test_caso_*`.** Ahora hay un modelo que existe, así que los de sólo Groq se podrían
  correr — pero habría que cambiarles el modelo, y **el modelo es parte de las condiciones de la
  serie congelada**. No los toqué.
- **El costo en dinero.** 23 llamadas. No sé la tarifa.
- **El chat**, **el estado del Codespace fuera de git**, **el clon local de delamor**.

---

## ARRANQUE — 2026-10-09 04:29 UTC

*Claude Opus 5 (Code, Codespace `ckm`). Chequeo §2 + §8, antes de la TASK de fixes.*

### Revisé

1. **Locks:** ninguno. **`git pull --rebase`:** limpio, HEAD en `a110d40`. **`git status`:**
   nada modificado.
2. **El gate sigue congelado:** `git diff f96c234 HEAD -- iap_chatroom/autonomous_device.py`
   → **vacío**.
3. **`DECISIONES_opus.md`** → leída la entrada del vivo 02 y la lista de cinco fixes.
4. **Tests: 360/360.**

### Preguntas abiertas

**Ninguna.** La próxima es **P11**.

### Encontró

- **Un `pkill -f "iap_chatroom/server.py"` mató el propio shell** (exit 144) y abortó el comando
  que iba a escribir este reporte: el patrón matcheó el proceso que lo ejecutaba. **Nada se
  escribió a medias** —`git status` quedó limpio y la entrada no existía—, así que no hubo daño.
  El server quedó parado, verificado aparte. Lo anoto porque fue un corte autoinfligido y la
  forma de pararlo era la mala.

### No pude revisar

- Los 21 `test_caso_*`; el chat; el estado del Codespace fuera de git; el clon local.
- `process/iap_series_freeze_20261008/README.md:41`, que sigue diciendo "67 archivos".

---

## REPORTE — evaluación de los cinco fixes, antes de tocar código — 2026-10-09 04:29 UTC

*Server levantado y parado para medir. **Sin código.** Gate intacto.*

### F1 — **No es un bug del canal. Es un error de mi reporte del vivo 02.**

**La ruta no existe.** `api_routes.py:79` declara `@router.get("/monitor")`, montado en `/api`
→ **`GET /api/monitor`**. Yo usé **`/api/monitor/state`**, que no está en ninguna ruta.

**Medido, los tres juntos:**

```
GET /api/monitor/state     -> HTTP 404  {"detail":"Not Found"}
GET /api/monitor           -> HTTP 200  {"corpus_size":12,"n_nodes":32,"message_count":0,
                                        "D_ckm":null,"temp_signal":null,"n_agentes":0,
                                        "corpus_status":"operational"}
tool MCP get_monitor_state ->          {"corpus_size": 12, "n_nodes": 32, "message_count": 0,
                                        "D_ckm": null, "temp_signal": null, "n_agentes": 0,
                                        "corpus_status": "operational"}
```

**El endpoint y la tool ya devuelven lo mismo, campo por campo.**

**Y por qué lo reporté como bug:** mi diagnóstico hizo `d.get(k)` sobre el cuerpo del 404
—`{"detail":"Not Found"}`— y eso da `None` para cada clave que pedí. **Rellené una ausencia (un
404) con un valor (`None`) y lo leí como dato.** Es exactamente el patrón que vengo persiguiendo
en el código del proyecto; esta vez estaba en mi instrumento de lectura, y pasó al reporte como
un bug del canal.

**No hay nada que arreglar.** Propongo sólo un test que fije que el endpoint y la tool coinciden,
para que la próxima vez no haga falta levantar el server a mano. **La corrección del reporte del
vivo 02 queda acá**, sin editar la entrada anterior (§6).

### F2 — `clock_log` no tiene tool ni endpoint: confirmado

`ChatChannel.clock_log()` existe (`channel.py:147`) y **nadie lo expone**. `grep` sobre el repo:
sólo lo llaman los tests y los dos drivers de vivo, **todos dentro del mismo proceso**. Desde
afuera del server no hay forma.

**Trabajo nuevo, chico, sin tensión.** No toca Monitor, Config ni COCO.

**Una decisión a declarar:** el log crece sin tope, uno por tick observado. **Default que
propongo:** la tool acepta `desde_tick` y devuelve el total aparte, para poder paginar sin perder
la cuenta. Reversible.

### F3a — el `_state` se acumula: confirmado, ya va por 12

`corpus_state.json` tenía **10** textos antes del vivo 02 y **12** después. **El vivo escribe.**

**La tensión, y por qué no lo decido:** `_STATE_DIR` es `iap_chatroom/_state/`, fijo en
`ckm_monitor.py:32`. Aislar el estado por vivo **cambia de dónde lee `CKMMonitor`**, y eso
cambia **qué datos ve Monitor** —sin tocar su código, pero es el límite que delamor puso.

**Dos caminos, y no elijo:**
- **(i) declarar**, sin mover nada: el driver lee el estado de partida y lo deja en su log y en
  el reporte, como hice en el vivo 02. **Costo cero, y el corpus sigue creciendo.**
- **(ii) aislar**: `CKMMonitor(..., state_dir=...)`, un directorio por vivo, con default igual al
  de hoy. **El de agosto no se borra**, se deja de usar.

**(ii) es aditivo y reversible, pero cambia qué corpus ve Monitor en un vivo. [delamor].**

### F3b — **sólo evaluado. Y es más grande de lo que yo había dicho.**

**8 de los 12 textos del corpus son joins:**

```
'TinkerBellucio joined the channel'    'test_agent joined the channel'
'PeterPlam joined the channel'         'GroqLlama8B_2 joined the channel'
'MarkOpolus joined the channel'        'GroqLlama8B_1 joined the channel'
'GroqGptOss20B_2 joined the channel'   'GroqGptOss20B_1 joined the channel'
```

Los otros **4** son de la serie congelada.

**Dos tercios del corpus que construye W son la frase "X joined the channel".** Yo había
reportado que "los joins entran"; **lo medido es que son mayoría**.

**Por qué entran:** `on_message` hace `ingest([message.text])` **para todo mensaje**, y
`join_channel` publica un `Message` con `device_type="SYSTEM"`. **No hay filtro por tipo en la
ingesta.**

**No lo toco: sacarlos cambia qué mide W.** Lo que agrego es qué cambiaría:
- W quedaría sobre **4 textos**;
- `n_nodes` hoy es 32 con los 12; con 4, el `NodeExtractor` podría no distinguir y
  `corpus_status` volvería a `accumulating`;
- **la serie congelada corrió así.** Si los joins salen, los corpus de 0.4–0.15 **dejan de ser
  comparables**. La regla de ingesta es parte de las condiciones, igual que el modelo.

**[delamor]. No propongo default.**

### F4 — encontrado qué cuenta, y hay un `or 1` adentro

**`n_agentes = len(self._devices_seen)`** (`ckm_monitor.py:173`), y `_devices_seen` se llena en
`on_message` con `message.device_id` (`:126`).

**En los dos vivos los únicos mensajes fueron los joins, cuyo `device_id` es `"system"`.** Así
que `_devices_seen = {"system"}` → **1**.

**No es un error de conteo: el nombre y el objeto no coinciden.** `n_agentes` no cuenta devices
registrados: cuenta **device_ids que publicaron**, y el pseudo-device `"system"` cuenta como uno.
Con dos devices que nunca publicaron, el único "agente" visto fue el canal.

**Y un segundo hallazgo que no estaba en la lista:**

```python
# ckm_monitor.py:183
n_agentes=len(self._devices_seen) or 1,
```

**Un `or 1` en la llamada a la firma.** Con cero devices vistos, **la firma reporta 1 agente**.
NOMINAL por ausencia, y en lo que **certifica** el estado estructural. **Lo señalo y no lo toco:**
cambiar lo que la firma certifica no es mío.

**Lo arreglable sin decidir nada del modelo:** que `"system"` no cuente como agente — es el
canal, no un participante. **Default que propongo:** `_devices_seen` ignora
`device_type == "SYSTEM"`, con test que pueda fallar.

**Lo que NO propongo:** que `n_agentes` cuente devices **registrados** en vez de vistos. Eso
cambia lo que la firma mide. **[delamor].**

### F5 — ritmo observado: trabajo nuevo, sin tensión

`run()` tiene `start = time.monotonic()` (`:561`) y **no lo guarda**, así que `costo()` no puede
dar vueltas por minuto reales.

**Aditivo:** guardar inicio y fin, y agregar a `costo()` un bloque `ritmo_observado` **al lado**
del declarado.

**Lo medido en los dos vivos, que es lo que el fix hace explícito:** con `poll_interval = 5.0` el
declarado da **12 vueltas/minuto**; el observado fue **12 y 12** en el vivo 01 —los 404 volvían al
instante— y **11 y 12** en el 02. **El declarado es el piso teórico; el observado es el piso menos
la latencia.**

### Resumen

| | qué es | lo hago |
|---|---|---|
| **F1** | **no es bug: error de mi reporte** | un test de coincidencia endpoint/tool |
| **F2** | confirmado, trabajo nuevo | sí, aditivo |
| **F3a** | confirmado (10 → 12) | **(i) declarar** o **(ii) aislar** → **[delamor]** |
| **F3b** | **8 de 12 textos son joins** | **sólo evaluado. [delamor]** |
| **F4** | cuenta publicadores, y `"system"` es uno. **Más un `or 1` en la firma** | sacar SYSTEM: sí. La firma o el criterio: **[delamor]** |
| **F5** | confirmado, trabajo nuevo | sí, aditivo |

**Nada toca Monitor, Config ni COCO.** F3a (ii) cambiaría **qué datos** ve Monitor sin tocar su
código, y por eso lo reporto en vez de decidirlo.

**Arranco por F1, F2 y F5** —los tres sin tensión— salvo que llegue otra cosa. **F3a espera** el
camino, **F3b y el `or 1` esperan a delamor**, y de **F4** haría sólo la parte de SYSTEM.

### No pude revisar

- **Si `/api/monitor/state` aparece en algún otro lugar del repo.** Busqué la ruta; no busqué
  todos los consumidores de la API REST.
- **Qué pasa con `n_nodes` si los joins salen del corpus.** Lo razoné, **no lo corrí**: habría que
  reconstruir W sin ellos, y eso ya sería tocar F3b.
- **Los 21 `test_caso_*`**; **el chat**; **el estado del Codespace fuera de git**; **el clon local
  de delamor**.

---

## REPORTE FIXES — los cinco, mas la firma — 2026-10-09 04:43 UTC

**Suite completa: 379 passed.** `tests/test_fixes_vivos.py`: 19.
Gate congelado: `git diff f96c234 HEAD -- iap_chatroom/autonomous_device.py`
sobre el texto del gate, vacio.

### Lo implementado, archivo por archivo

| Fix | Donde | Que cambio |
|---|---|---|
| F1 | — | **No era un bug del canal: era mi error de reporte.** La ruta es `/api/monitor`; yo pedi `/api/monitor/state` (404) y mi diagnostico hizo `.get(k)` sobre `{"detail":"Not Found"}` -> `None` por campo. Llene una ausencia con un valor. Queda el test de que el endpoint y la tool devuelven lo mismo, y de que `/monitor/state` no esta en el router. |
| F2 | `channel.py`, `mcp_server.py`, `api_routes.py` | `clock_log_desde(desde_tick)` **nuevo y aditivo**; `clock_log()` conserva su firma `List[dict]`. Tool `get_clock_log`, rutas `GET /clock` y `GET /clock/log`. |
| F3a | `ckm_monitor.py` | `CKMMonitor(min_texts=3, state_dir=None)`; `state_dir` como property; default sigue siendo `_STATE_DIR`. Aislar el estado de un vivo ya no pide tocar el modulo. |
| F3b | `ckm_monitor.py` | `es_system = getattr(message, "device_type", None) == "SYSTEM"`; con `es_system`, **no se ingesta**. delamor: *"no, nunca"*. En el vivo 02, **8 de 12 textos del corpus eran `"X joined the channel"`**: dos tercios de lo que construia W. |
| F4 | `ckm_monitor.py` | `if not es_system: self._devices_seen.add(...)`. `"system"` no es un agente. |
| F5 | `autonomous_device.py` | `_t_inicio` / `_t_fin` y `ritmo_observado()`. `costo()` lleva declarado y observado juntos. |
| firma | `ckm_monitor.py:233`, `firma_ckm.py:94` | **Se sacaron los dos `1`** (delamor, DECISIONES `4feb88b`): el `or 1` y el default. `n_agentes` es el conteo real; **0 es 0**. |

### La condicion que delamor puso antes de sacar los `1`

*"verifica que nada divida por `n_agentes`; si algo divide, para y reporta."*

`grep -rn "n_agentes"` sobre el repo: **nada divide**. Solo se guarda
(`firma_ckm.py:136`) y se lee. Esa verificacion quedo como test
(`test_nada_divide_por_n_agentes`), porque era una precondicion y no un
chequeo de una vez: si manana alguien divide, el `0` honesto pasa de dato a
`ZeroDivisionError`.

### Las tres inversiones de la firma

| # | Que se invirtio | Que test fallo | Suite al restaurar |
|---|---|---|---|
| A | `ckm_monitor.py:233` -> `len(self._devices_seen) or 1` | `test_con_cero_devices_la_firma_dice_0` — `assert 1 == 0`, *"la firma certifico un agente que no existio"* | 379 passed |
| B | `firma_ckm.py:94` -> `n_agentes: int = 1` | `test_el_default_de_firmar_es_0_no_1` — `assert 1 == 0` | 379 passed |
| C | `firma_ckm.py:100` + `_dummy = 1.0 / n_agentes` | **dos**: `test_nada_divide_por_n_agentes` (lo detecta leyendo el codigo) y `test_con_cero_devices_la_firma_dice_0` (`ZeroDivisionError`) | 379 passed |

**La inversion C se hizo dos veces.** La primera la puse dentro del literal
del constructor y rompio la indentacion: 9 errores de coleccion, 7 fallos.
Eso **no midio nada** — un `IndentationError` no es el test fallando, es el
archivo sin cargar. La reubique en el cuerpo de `firmar` y ahi si rompe por
donde tenia que romper. Lo anoto porque ya me paso antes (inversiones 36 y
37): **una inversion mal aplicada se ve parecida a una que mide.**

### Lo que C dejo a la vista

Que nada divida hoy no es una propiedad del codigo: es un hecho de este
commit. El `0` de `n_agentes` es honesto **a condicion** de que nadie lo use
como divisor, y esa condicion ahora esta sostenida por un test y no por mi
memoria.

### Pendiente, no mio

- `process/iap_series_freeze_20261008/README.md:41` sigue diciendo
  "67 archivos"; son 62.
- **CP2b** — el criterio local: skip con su motivo, auditoria al azar sobre
  las dos caras, umbrales declarados "no calibrados", y el test de que el
  filtro no vuelva absorbente al silencio.
- `test_armstrong_via_corpus_v3.py:34`, roto por CP4 a sabiendas.
- Los 21 `test_caso_*`.

**ALTO.**

---

## REPORTE n_agentes obligatorio — 2026-10-09 04:51 UTC

**Suite: 379 passed.** Aceptado el REPORTE FIXES en DECISIONES `7175468`.

`firmar()` ya no tiene default en `n_agentes` (`firma_ckm.py:96`). El conteo lo
declara quien firma, o no firma.

### Divergencia con la instruccion

Opus nombro **cuatro** llamadores a corregir (`test_firma_ckm.py` 109, 122, 136,
139). Son **nueve, en ocho tests**: 84, 109, 122, **136 y 139** (los dos en el
mismo test), 159, 182, 207, 221. Los cuatro de la instruccion estan entre ellos;
faltaban cinco. Los nueve pasan ahora `n_agentes=0` explicito — **0 porque en
esos fixtures no hay agentes**, no por heredar el default que se saco.

La suite lo mostro sola: al sacar el default, **9 failed**, ocho por `TypeError`
en `test_firma_ckm.py` y uno mio. No lo encontre leyendo; lo encontro el cambio
al romper. El `grep -rn "firmar("` que corri **antes** de tocar nada ya listaba
los nueve: la divergencia estaba a la vista desde el principio.

El unico llamador de produccion, `ckm_monitor.py:224`, ya lo pasaba explicito.

### Un test mio quedo superado, no roto

`test_el_default_de_firmar_es_0_no_1` (lo escribi ayer) afirmaba que el default
era `0`. Con el default afuera, esa afirmacion **se volvio falsa** — y lo que
afirmaba era mas debil que lo que ahora vale. Lo **reemplace**, no lo arregle,
por `test_firmar_sin_n_agentes_levanta_TypeError`, que verifica dos cosas: que
el parametro no tenga default (`inspect.Parameter.empty`) y el `TypeError` real
al llamar sin el. Lo digo porque un test que se vuelve falso al mejorar el
codigo es facil de parchear en silencio.

### Inversion D

| Que se invirtio | Que test fallo | Suite al restaurar |
|---|---|---|
| `firma_ckm.py:96` -> `n_agentes: int = 0` | `test_firmar_sin_n_agentes_levanta_TypeError` — rompe por las **dos** mitades: el default deja de ser `empty`, y la llamada sin el argumento ya no da `TypeError` (da `AttributeError` mas adentro) | 379 passed |

### Lo que el cambio dejo dicho

Con el `1` el hueco se veia, porque el numero era falso. Con el `0` el hueco se
tapaba, porque el numero era casi siempre correcto. **El UNKNOWN por ausencia no
se arregla eligiendo mejor el valor que lo rellena.** Esta es la cuarta vez que
este patron aparece en el proyecto, y la primera en que lo cerro quitando el
relleno en vez de corrigiendolo.

**ALTO.**

---

## CORRECCION (delamor) — el silencio absorbente es del filtro — 2026-10-09 04:57 UTC

Sin cambios en el codigo. CP2b **no esta abierto**: esto queda anotado para
cuando lo este.

### Lo que dije mal

En mi mensaje anterior escribi el test de CP2b asi: *"que un device que callo
una vez pueda volver a hablar"*. **Puse la carga en el device, que es el unico
de los dos que no puede causar el problema.** El device no tiene estado que lo
atrape.

### Lo que delamor corrigio

El filtro esta **entre** O y D. Si su criterio es *"cambio algo?"* y lo unico
que mira son los mensajes, entonces con el canal callado no cambio nada -> no
llama a D -> el device no decide -> el canal sigue callado. **El silencio se
vuelve punto fijo del lazo, no decision del modelo.**

Y desde afuera se ve igual que un `OP_SILENCE`. Es el par vivo 01 / vivo 02 otra
vez — `{'UNKNOWN': 24}` por infraestructura vs `{'OP_SILENCE': 23}` por decision
— pero con **el filtro en el lugar del provider caido**. La traza es lo unico que
los separa, y el filtro todavia no escribe nada en ella.

### El test, como va

Canal callado, N turnos, nada cambiado del lado de los mensajes:

- `llamadas a D > 0`
- `skips != N`

**Si el filtro puede llegar a cero llamadas sosteniendo el silencio, el test
falla ahi.**

### Lo que agregue yo, y es mas flojo de lo que lo dije

Dije que el criterio tiene que mirar el tick (`get_clock()` registra con o sin
mensajes, CP1). Eso es **la condicion minima, no la solucion**:

- un criterio que llama a D **cada** tick deja de ser un filtro: bajo silencio
  cuesta lo mismo que no tenerlo, y eso es justo lo que CP2b quiere ahorrar;
- un criterio *"tick avanzo **y** algo mas"* puede ser absorbente por el "algo
  mas", y estamos en el mismo lugar con un paso extra.

Sin algo que cambie bajo silencio el filtro es absorbente **por construccion**;
tenerlo **no alcanza**.

### Lo que queda abierto, y no es mio

**Cada cuantos ticks el silencio se consulta igual** — un piso. Es calibracion.
Va declarado como numero **no calibrado**, y el test de arriba es el que impide
que ese numero sea infinito.

**ALTO.**

---

## RESPUESTA a Opus — skip vs OP_SILENCE, y los Delta t — 2026-10-09 04:59 UTC

Sin cambios en el codigo. CP2b sigue cerrado.

**El mensaje de Opus llego cortado**, termina en *"La auditoria al azar tambien
rompe el punto fijo, per"*. No completo lo que seguia. Lo que sigue responde a lo
que llego.

### 1. El skip con su motivo (acuerdo, sin nada que agregar)

En la traza, un skip tiene que ser distinguible de un `OP_SILENCE`. Con el motivo
puesto, el par *"filtro callo / modelo callo"* se separa igual que el par 01/02.
Lo unico que agrego: el motivo va **en la traza de ese turno**, no en un contador
agregado. Un contador dice cuantos, no cuales — y cuales es lo que hace falta
para saber si el silencio estaba decidido.

### 2. La auditoria al azar rompe el punto fijo, pero no sirve como el test

Rompe el punto fijo **en distribucion**: con tasa p, sostener el silencio ya no
garantiza cero llamadas. Pero para una corrida dada **no acota nada** — hay
probabilidad positiva de cero llamadas en N turnos, asi que `llamadas a D > 0`
como asercion **seria flaky**. Un test que falla a veces no distingue *"el filtro
es absorbente"* de *"salio cara N veces"*.

El **piso deterministico** es lo que hace que el test pueda fallar por el motivo
correcto. La auditoria cubre otra cosa: **las dos caras** del filtro, que es para
lo que esta pedida. No son el mismo mecanismo y no se reemplazan.

### 3. Los dos Delta t colapsan en el piso, segun que los resetea

El Delta t desde el ultimo mensaje ajeno **crece monotono** bajo silencio. Si el
criterio es *"Delta t > umbral -> llamar a D"*:

| Que lo resetea | Que resulta |
|---|---|
| **la llamada** | el piso periodico, con otro nombre |
| **solo un mensaje** | satura: pasado el umbral llama en **todos** los turnos, y el filtro deja de filtrar justo donde mas silencio hay |

Asi que el piso **no es una perilla al lado de ese criterio: es lo que ese
criterio es**, una vez que se dice que lo resetea. Igual con el Delta t desde que
el device hablo.

### 4. Los del caso Z si agregan algo

Estado del objetivo y presupuesto **cambian por fuera del lazo**, no por el lazo.
Esos no colapsan en el piso. Pero no existen todavia: el objetivo es del caso Z
(delamor), y mientras no este, el lazo solo tiene lo del punto 3.

**Pido el resto del mensaje. ALTO.**

---

## CORRECCION de atribucion — la correccion del filtro es de Opus — 2026-10-09 05:02 UTC

Sin cambios en el codigo. Las entradas anteriores **no se editan**: esto las
corrige desde aca.

### Que atribui mal

La entrada **CORRECCION (delamor) — el silencio absorbente es del filtro**
(04:57 UTC, commit `4853baf`) y su mensaje de commit dicen *"delamor corrige"*.
**No es de delamor: es de Opus.** delamor lo relevo sin marcarlo, y despues lo
explicito.

Afecta dos lugares, los dos ya pusheados y por eso no reescritos:

- esta BANDEJA, entrada de 04:57 — corregida **por esta entrada**;
- el mensaje de `4853baf` — queda como esta, con esta entrada al lado.

### Que de eso era mio

delamor toma la divergencia como suya, por no haber marcado el relevo en el
prompt. Que sin la marca no era distinguible, es cierto.

Pero **la senal estaba en el texto que me paso**. El mensaje de Opus que delamor relevo
abria con *"Asi es, y la forma en que lo dice Code es mas precisa que **la
mia**"*. *"La mia"* solo tiene sentido si la formulacion original era suya. Lo
lei como asentimiento a algo que ya estaba atribuido, y no como autoria. **Tenia
con que corregirlo antes de que me lo dijeran y no lo use.**

### Lo que no cambia

El contenido de la correccion: el filtro es el unico de los dos que tiene estado
entre O y D, y por eso el unico que puede hacer absorbente al silencio. Eso vale
igual, y vale por el argumento, no por quien lo dijo. Lo que cambia es **de
quien es**, que en este proyecto no es un detalle.

**ALTO.**

---

## CIERRE del hilo CP2b (previo) — 2026-10-09 05:05 UTC

Sin cambios en el codigo. **CP2b sigue esperando el OK de delamor.**

### El mensaje cortado, completo

Opus completo la frase: *"...pero no puede ser lo unico que lo rompa: si no, la
**iniciativa queda en manos de la suerte**."*

Llegamos a lo mismo, por lados distintos, y **el suyo es el fundamento**:

| Quien | Donde lo ubica |
|---|---|
| Opus | en el **device**: su iniciativa la decidiria una moneda |
| yo | en el **instrumento**: el test saldria flaky |

El test flaky es el **sintoma** de lo que dice Opus, no un argumento paralelo. Y
lo de Opus vale **aunque nadie escriba el test**: un device cuya iniciativa la
decide el azar es defectuoso sin que haya que medirlo. Yo entre por el lado del
instrumento, que es el lado que mira mi reflejo. Queda anotado asi.

Las dos derivaciones mias (la auditoria no reemplaza al piso; los Delta t
colapsan en el piso segun que los resetea) **van**, confirmadas por Opus.

### Atribucion: cerrada por delamor (`af56fee`)

El origen **se perdio en el canal**, no fue mio: delamor aclara que recibo sus
prompts igual que Opus, y que la divergencia la genero el relevo al no decir que
la observacion era de Opus. Cubre **dos** casos del mismo mecanismo: la
*"correccion de delamor"* de `4853baf` y el *"pedido de delamor"* del CP2v.

Mi entrada de 05:02 decia que la senal estaba en el texto (*"mas precisa que la
mia"*). **Eso sigue siendo cierto y no alcanza para revertir lo que cerro
delamor**: una pista que se puede leer de dos maneras no es una marca de origen.
Lo dejo dicho sin insistir — A3.

**Practica, desde ahora:** cada bloque de Opus empieza con `Opus:`, y el origen
viaja con el texto en vez de depender de que yo lo infiera.

**ALTO.**

---

## ARRANQUE CP2b — el criterio local — 2026-10-09 05:09 UTC

*OK de delamor (este chat, explicito: "soy delamor CP2b confirmo. OK").
Especificacion: DECISIONES `e737e78` + TASK §1 (*"Propuesta de delamor (7 oct):
un criterio local antes de D, sin LLM"*). El CP2b del `monitor_coco` es **otro**
y esta cerrado: la etiqueta se repite entre TASKs.*

### Lo que pide la especificacion

1. `skip` de cada vuelta **con su motivo**;
2. **auditoria al azar** sobre las dos caras, con la tasa de divergencia como
   medida del costo del sesgo;
3. umbrales **declarados "no calibrados"** (son de Calibracion) — *"no los
   inventa Code"*;
4. test que pueda fallar: en silencio y con objetivo, el filtro **igual** deja
   pasar a D alguna vez.

Mas lo de este hilo: el motivo va en la traza **del turno**; la auditoria no
alcanza sola (iniciativa en manos de la suerte, Opus); el piso.

### Lo que decido yo, y lo digo

- **Modulo nuevo, `iap_chatroom/criterio_local.py`.** No meto el filtro en
  `autonomous_device.py` mas alla del cableado: el gate esta congelado en
  `f96c234` y un modulo aparte se testea solo, sin levantar el lazo.
- **`DECISION_SKIP = "SKIP"`, tercer valor.** Hoy hay dos formas de terminar sin
  accion: `OP_SILENCE` (**lo decidio el modelo**) y `UNKNOWN` (**fallo el
  provider**). El skip es la tercera (**no se llamo**) y va con las otras dos en
  la traza, distinguible. Es el pedido de Opus: el par *"filtro callo / modelo
  callo"* se separa igual que el par vivo 01 / vivo 02.
- **El criterio devuelve un registro, no un `bool`.** Lleva `llamar`, `motivo`,
  los deltas y **`via`** ∈ {`criterio`, `piso`, `auditoria`}: *por que* se llamo
  queda tan trazable como por que no.
- **Los umbrales van en un `frozen dataclass` con `calibrado: bool = False`**, y
  ese `False` viaja en **cada** registro, no en un comentario. Es lo mas cerca de
  *"no los inventa Code"* que puedo estar implementando: los valores son
  provisorios **y lo dicen de si mismos**.
- **El piso es deterministico** (`piso_ticks`), y la auditoria tiene su RNG
  inyectable. Con la auditoria sola el test seria flaky y no distinguiria un
  filtro absorbente de una tirada de moneda.
- **Los Δt salen de los timestamps del canal**, nunca del reloj del device
  (TASK §0.4). `n_nuevos` ya cuenta **solo mensajes ajenos** — el lazo filtra
  `m["device_id"] != self.device_id`: lo verifico, no lo asumo.

### Lo que NO hago, y por que

- **El estado del objetivo (K) y el presupuesto**: no existen. El objetivo es del
  **caso Z (CP3, delamor)**. Van como **ausentes declarados**, no como `0` ni como
  `False` — es el patron que vengo cerrando toda la sesion.
- **La zona horaria propia del device**: la TASK la marca **opcional** (*"si el
  device quiere"*). No la implemento; queda declarada sin implementar.
- **No toco Monitor, Config ni COCO.** Si aparece que hay que tocarlos, **ALTO**.

### Pregunta (NO BLOQUEA)

Los valores provisorios de los umbrales los pongo yo con el `calibrado=False`
encima, porque sin valores no hay codigo. **Si Calibracion ya tiene numeros, los
cambio por los suyos y los declaro.** No espero por esto.

Arranco.

---

## REPORTE CP2b — el criterio local — 2026-10-09 05:25 UTC

**Suite: 412 passed** (eran 379). `tests/test_criterio_local.py`: **33**.
Archivo nuevo: `iap_chatroom/criterio_local.py`.

### Las cuatro propiedades que pidio Opus, y donde se verifica cada una

| | Propiedad | Test |
|---|---|---|
| **Que registre** | cada salto, con su motivo, distinguible de un `OP_SILENCE` | `test_skip_no_es_OP_SILENCE_ni_UNKNOWN`, `test_en_la_traza_del_device_el_skip_se_distingue`, `test_cada_vuelta_lleva_su_motivo` |
| **Que permita** | canal callado -> el piso deja pasar a D, `llamadas > 0` | `test_el_silencio_no_vuelve_absorbente_al_filtro` |
| **Las dos caras** | la auditoria no mira un solo lado | `test_la_auditoria_mira_las_dos_caras`, `test_las_dos_caras_distinguen_sus_errores` |
| **Que declare** | umbrales "no calibrados" en el panel | `test_el_panel_declara_los_umbrales_sin_calibrar` |

`DECISION_SKIP = "SKIP"` es el **tercer** valor: `OP_SILENCE` lo decidio el
modelo, `UNKNOWN` fue el provider cayendose, `SKIP` es el filtro no habiendo
llamado. Las tres terminan la vuelta sin accion y las tres se distinguen.

### Lo que encontre implementando, y es del instrumento

**`_interact` cae por default a generar y publicar.** Sus ramas son UNKNOWN,
OP_SILENCE y LEAVE; cualquier otra palabra **sigue de largo hasta
`send_message`**. Al agregar `DECISION_SKIP`, la vuelta que el filtro skipeaba
**publicaba un mensaje**.

Lo vi **de costado**: lo encontro `test_un_skip_no_gasta_una_llamada`, que mira
la llamada al LLM. Ese test es **mas debil que el defecto** — una llamada de mas
es costo, una publicacion de mas es el canal cambiado por el filtro. Por eso
ahora existe `test_un_skip_no_publica_nada` aparte, midiendo lo que hay que
medir.

El fallthrough **queda como esta**: hoy solo lo alcanza INTERACT, porque
`_decide` manda toda palabra desconocida a UNKNOWN. No es un defecto vivo, es el
**mecanismo** — y es el mismo de toda la sesion: un fallback que acierta lo
suficiente como para no notarse. Queda reportado, no corregido de paso.

### Donde diverjo de Opus, y lo medi

Opus: *"las dos [caras] van al azar, con la tasa declarada"*. **Las dos tasas van
declaradas y sin calibrar**, como pidio. Pero el muestreo **no cuesta lo mismo en
las dos caras**:

- **cara del skip**: cada vuelta sorteada **cuesta una llamada**. Es lo que se
  paga por ver lo que el filtro tapaba. Sin muestrearla es **invisible**.
- **cara del pase**: la llamada **ya se hizo**. El sorteo no ahorra nada; lo
  unico que decide es si la vuelta entra a la muestra, y descarta observaciones
  **gratis**.

Medido, no opinado: `test_el_muestreo_del_pase_no_cuesta_una_llamada` corre el
filtro con la tasa del pase en 0 y en 1 y **las vueltas que llaman son las
mismas**; lo unico que cambia es cuantas quedan marcadas.

Asi que la cara del pase lleva **las dos lecturas, etiquetadas**: la muestra con
su tasa declarada (lo aceptado en el CP0) y el **censo** sobre todas las que
pasaron. No elijo por el lector.

### Las cinco inversiones

| # | Que se invirtio | Que test fallo | Suite al restaurar |
|---|---|---|---|
| 1 | el piso (`if False and ...`) | **5**: `..._silencio_no_vuelve_absorbente_al_filtro`, `test_el_piso_es_periodico_y_deterministico`, `test_cada_vuelta_lleva_su_motivo`, `test_la_via_dice_por_que_SI_se_llamo`, `test_el_panel_lleva_las_dos_caras` | 412 |
| 2 | la rama `DECISION_SKIP` de `_interact` | `test_un_skip_no_publica_nada`, `test_un_skip_no_gasta_una_llamada` | 412 |
| 3 | `calibrado: bool = True` | **4**, entre ellos `test_el_panel_declara_los_umbrales_sin_calibrar` | 412 |
| 4 | `dt_desde` devuelve `0.0` en vez de `None` | `test_un_dt_que_no_se_pudo_medir_es_None_no_cero` | 412 |
| 5 | se saca la cara del pase | **4**, entre ellos `test_la_auditoria_mira_las_dos_caras` | 412 |

**La inversion 1 rompe cinco tests y no uno**: el piso sostiene mas de lo que
dice su nombre. Y `test_sin_piso_el_silencio_ES_absorbente` **sigue verde bajo la
inversion 1**, que es exactamente lo que tiene que pasar: ese test **afirma el
agujero**, no lo tapa.

### Dos tests que afirman el agujero, a proposito

- `test_sin_piso_el_silencio_ES_absorbente`: con `piso_ticks=0` el filtro no
  llama nunca. Deja escrito que **lo que rompe el punto fijo es el piso**.
- `test_la_auditoria_sola_puede_no_llamar_nunca`: busca una semilla con la que no
  sale ninguna auditoria en 20 vueltas. La *"iniciativa en manos de la suerte"* de
  Opus deja de ser un argumento y pasa a ser una corrida.

### Un test mio no podia fallar

`test_las_dos_tasas_van_declaradas_sin_calibrar` tenia
`assert x == 0.0 or "tasa_auditoria_pase" in r["umbrales"]`: verdadera casi
siempre. **Es el mismo patron que vengo sacando de los tests ajenos toda la
sesion, esta vez mio.** Reemplazada por dos aserciones sobre valores distintos
(0.3 y 0.7) que si pueden fallar.

### Lo que el CP2b NO hizo

- **El filtro esta apagado por default** (`criterio_local=None`): D en cada
  vuelta, que es el CP2a y los dos vivos. Con el filtro por default, la linea de
  base del vivo 02 (23 llamadas, 23 `OP_SILENCE`) dejaria de ser comparable **sin
  que nada lo dijera**. `test_sin_criterio_local_D_corre_en_cada_vuelta`.
- **Los deltas NO entran al prompt** (tension de Opus): el gate esta congelado.
  Se registran en la traza. `test_los_deltas_NO_entran_al_prompt_del_gate` y
  `test_el_texto_del_gate_sigue_congelado`.
- **Objetivo (K) y presupuesto van ausentes declarados** (`None`, no `0`): son
  del **caso Z (CP3, delamor)**. Son los dos unicos que cambian **por fuera del
  lazo**, y por eso los unicos que no colapsan en el piso.
- **La zona horaria propia del device**: la TASK la marca opcional. Sin
  implementar, declarado.
- **No se toco Monitor, Config ni COCO.**

### Pendiente

- **Los valores de los umbrales son provisorios** (`dt_minimo_s=5.0`,
  `piso_ticks=12`, las dos tasas `0.1`). Si Calibracion entrega numeros, se
  reemplazan y se pone `calibrado=True`.
- El `_interact` con fallthrough, reportado arriba.
- Un vivo con el filtro puesto, contra la linea de base del vivo 02. **No lo
  corro sin OK.**

**ALTO.**

---

## REPORTE CP2b ajustes — los cuatro de Opus — 2026-10-09 05:39 UTC

**Suite: 418 passed** (eran 412). Los cuatro ajustes van, mas el control que
pidio Opus y una consecuencia de calibracion que quedo medible.

| # | Ajuste | Que cambio |
|---|---|---|
| 1 | `piso_ticks` -> **`piso_vueltas`** | el nombre decia ticks y lo medido era `_vueltas_sin_llamar`. Test con el **tick quieto**: el piso igual dispara, que es lo que prueba que cuenta vueltas |
| 2 | **`ValueError` si `piso_vueltas <= 0`** | el docstring decia que el piso "no es opcional" y el constructor dejaba apagarlo: **el texto afirmaba una cosa y el codigo permitia la otra** |
| 3 | **publicar exige `INTERACT` explicito** | `_interact` ya no cae a publicar; toda palabra que no reconoce se registra UNKNOWN **sin actuar** |
| 4 | `_tick_ultima_llamada`: `-1` -> **`None`** | una ausencia representada con un valor de la escala, **puesta por mi en el archivo nuevo**. Y un segundo caso que el ajuste dejo ver: con el clock UNKNOWN **no se sabe en que tick se llamo**, y eso tampoco es el tick -1 |

### El test de la absorcion cambio de enunciado, y dice mas

Con el `> 0` afuera de `evaluar`, **`piso_vueltas=0` ahora dispararia el piso
SIEMPRE** — lo contrario de apagarlo. Asi que la absorcion ya no se exhibe
poniendo el piso en cero.

Se exhibe con un **piso fuera del horizonte**, y eso dice algo que *"sin piso el
silencio es absorbente"* no decia: **que el piso sea finito no alcanza; tiene que
caer dentro de la ventana que se observa.**

Opus lo cerro con el numero: *"con 12 vueltas de piso y un vivo de 11 vueltas, el
silencio es absorbente dentro de lo que se observa."* El default es **12** y el
vivo 02 corrio **23 vueltas**, asi que ahi entraba. **El umbral va a
Calibracion: el piso tiene que ser menor que las vueltas de un vivo.**

### Lo que agregue, que es del instrumento y no del umbral

`panel_criterio()` ahora declara **`piso_dentro_del_horizonte`**: si hubo skips y
el piso **no disparo nunca**, esa corrida **no puede decir** si el silencio era
absorbente. Es UNKNOWN y no "no era". Sin skips queda `None` — la pregunta no se
hizo — y no `False`, que afirmaria que el piso no cupo. Va con
`vueltas_para_ver_el_piso`, que es el minimo de vueltas que una corrida necesita
para poder mirarlo.

No fija el umbral: hace que cada corrida diga **si pudo ver lo que afirma**.

### El control que pidio Opus

*"Que el `ValueError` para valores <= 0 haya quedado puesto. Si
`piso_vueltas=0` 'llama siempre', tiene que ser porque la construccion no llega a
ese valor, no porque 0 sea un valor valido con otro significado."*

Verificado sobre el modulo cargado: `__post_init__` existe y levanta; `0` y `-1`
dan `ValueError`; el default es `12`. **Al valor no se llega por construccion.**
Cubierto por `test_apagar_el_piso_no_es_una_configuracion_valida` (0, -1, -100) y
por la **inversion B**.

### Las cuatro inversiones

| # | Que se invirtio | Que test fallo | Suite al restaurar |
|---|---|---|---|
| A | el piso vuelve a contar **ticks** (`_t - _u >= piso`) | `test_el_piso_cuenta_vueltas_y_el_nombre_lo_dice`, `test_el_panel_lleva_las_dos_caras` | 418 |
| B | sin el `ValueError` | `test_apagar_el_piso_no_es_una_configuracion_valida`, `test_un_piso_fuera_del_horizonte_ES_absorbente` | 418 |
| C | sin la exigencia de `INTERACT` | `test_publicar_exige_INTERACT_explicito` | 418 |
| D | `-1` en vez de `None` | `test_nunca_llamo_es_None_y_no_un_tick` | 418 |

### Dos aserciones mias que no podian fallar

En `test_publicar_exige_INTERACT_explicito` escribi
`assert dev.decisiones() == [] or True` y
`assert ... if hasattr(dev, "_log_decisiones") else True`. **Las dos son
verdaderas siempre**, y el atributo no existe: `_log` imprime y no guarda.

Es el mismo patron que vengo sacando toda la sesion, **en el test que escribi
para el patron**. Reemplazadas por una lectura de `capsys`: que la salida diga
UNKNOWN **y** que la palabra cruda no aparezca.

**ALTO.**

---

## CORRECCION — dos numeros mios, y un test que confirmaba el error — 2026-10-09 05:47 UTC

**Suite: 425 passed** (eran 418). Nace de la entrada de Opus en `cc9a62b`, que
corrige mi cuenta: *"hoy: piso 12, vivo de 60 s con poll 5 -> 11-12 vueltas: en
el borde."*

### 1. "El vivo 02 corrio 23 vueltas" es falso

Lo escribi en el REPORTE de los ajustes y en el ESTADO. **23 era el total de
llamadas entre los DOS devices.** Medido en
`experiments/vivo_02_groq_gptoss20b_log.json`, campo `costo.vueltas`:

| device | vueltas | llamadas |
|---|---|---|
| `GroqGptOss20B_1` | **11** | 11 |
| `GroqGptOss20B_2` | **12** | 12 |

**Lei un agregado como un conteo por unidad.** Es la misma confusion que el
`n_agentes` de esta manana, en el otro sentido: ahi un conteo por unidad hacia
de total, aca un total hizo de conteo por unidad.

Y el piso es estado **por device**, asi que el horizonte real son **11-12
vueltas**, no 23.

### 2. El campo que yo agregue tenia un off-by-one, y el test lo confirmaba

`vueltas_para_ver_el_piso` decia `piso_vueltas + 1`. **Es `+ 2`**: la vuelta 1 la
consume `primera_vuelta` —que llama y deja el contador en 0— y de ahi el
contador necesita `piso_vueltas` skips mas.

Medido: piso 3 -> dispara en la vuelta **5**; piso 5 -> **7**; piso 12 -> **14**.

**Lo grave no es el +1: es que el test pasaba.** Habia escrito
`assert panel["vueltas_para_ver_el_piso"] == 6` para piso 5, **contra el codigo y
no contra la corrida**. Un test que repite la cuenta del codigo no puede
encontrar un off-by-one: solo lo encuentra correr el filtro y mirar en que vuelta
dispara.

Lo reemplace por `test_vueltas_para_ver_el_piso_coincide_con_la_corrida`,
parametrizado en 1, 2, 3, 5, 12 y 23, que **compara el campo con la vuelta en que
el piso dispara de verdad**. Ese es el unico que no puede repetir mi error.

### 3. Con eso, "en el borde" tambien queda corto — y es tu numero, Opus

Con el default `piso_vueltas = 12` hacen falta **14 vueltas** para que el piso
dispare una vez. El device mas largo del vivo 02 tuvo **12**.

**El piso por default no habria disparado nunca en un vivo como el 02.** No
estaba en el borde: estaba **afuera**. `test_el_piso_por_default_no_habria_
disparado_en_un_vivo_como_el_02` lo fija con las 12 vueltas medidas.

### Lo que esto le agrega a Calibracion

La regla no es *"el piso menor que las vueltas de un vivo"*. Medida, es:

> **`piso_vueltas + 2 <= vueltas por device`**, y las vueltas son **por device**,
> no el total del vivo.

Con 60 s y `poll_interval = 5` son 11-12 vueltas por device, asi que el piso
tiene que ser **<= 9 o 10**. El default de 12 **no sirve para un vivo de 60 s**.
El numero es de Calibracion; lo que aporto es la desigualdad y de donde sale cada
termino.

### Donde quedo el error en el registro

- el REPORTE de los ajustes (05:39) dice *"el vivo 02 corrio 23 vueltas, asi que
  ahi entraba"*. **No se edita**: lo corrige esta entrada.
- el `ESTADO_canal_iap_clock_iniciativa_v2.md` decia lo mismo; **ese si se
  actualiza**, porque es estado vigente y no traza.

**ALTO.**

---

## ARRANQUE VIVO 03 — el filtro puesto — 2026-10-09 23:32 UTC

*Orden de delamor (E1, DECISIONES `4115efa`): vivo 03 con filtro -> calibrar ->
caso Z. Opcion (a): 60 s con `piso_vueltas` dentro de la ventana.*

### El teorema, escrito ANTES de correr

Regla del proyecto: *"antes de una corrida, preguntar si el resultado es un
teorema; si lo es, se demuestra en una linea."* **Parte lo es, y va escrita acá
para que la corrida sea falsable y no confirmatoria.**

Con `piso_vueltas = 6`, silencio puro y 12 vueltas, el filtro llama en:

| vuelta | motivo |
|---|---|
| **1** | `primera_vuelta` |
| **8** | `piso` |

**2 llamadas del criterio+piso, 10 skips.** La vuelta 14 seria la siguiente del
piso y no entra en la ventana. Medido con el modulo, no deducido.

Mas las auditorias de la cara del skip: **~Binomial(10, 0.1)**, esperanza **1**.
Asi que la prediccion es **2 a 4 llamadas por device**, contra 11-12 del vivo 02.

### Lo que NO es teorema, y es lo que la corrida mide

1. **Los joins SYSTEM cuentan en `n_nuevos`.** SYSTEM sale del **corpus** (F3b)
   pero sigue en la **observacion** del device. Asi que el join del otro device
   va a disparar `mensajes_nuevos` y **rompe el silencio puro** de la prediccion.
   No se cuantas veces: depende de en que vuelta caiga cada join.
2. **Que decide el modelo cuando se lo llama.** Si alguna vez decide INTERACT, el
   canal deja de estar callado y toda la dinamica cambia. El vivo 02 dio 23
   `OP_SILENCE` de 23, pero eso **no es una propiedad del modelo**: es lo que
   decidio esa vez. No se interpreta.
3. **Cuantas vueltas sale cada device** (11 o 12 en el vivo 02): depende de la
   latencia de Groq.
4. **Los sorteos de la auditoria**: hay RNG sin semilla en la corrida viva.

### Un hueco de F3a, y el camino que tomé

La orden pide `state_dir` **nuevo y aislado**. `CKMMonitor` acepta `state_dir`
desde el CP2b/F3a, **pero ningun camino vivo puede pasarlo**: `server.py:31` y
`mcp_server.py:23` construyen `CKMMonitor()` sin argumentos, y no hay hook de
entorno (verificado: `grep environ|getenv` en `iap_chatroom/` da vacio).

**F3a agrego el parametro y dejo el camino vivo sin poder usarlo.** Lo reporto
como hallazgo: no es que algo rompa, es que la pieza aceptada no es alcanzable
donde importa.

**No toco `server.py` ni `mcp_server.py`.** Hay un camino que no modifica ningun
archivo existente: `CKMMonitor` es singleton real (`__new__` + `_instance`,
L45-51), asi que un **launcher nuevo** que construya
`CKMMonitor(state_dir=...)` **antes** de importar el server fija la instancia, y
el `CKMMonitor()` del server devuelve esa misma. Archivos nuevos:

- `experiments/vivo_03_server.py` — el launcher, con el `state_dir` aislado
- `experiments/vivo_03_criterio_local.py` — el driver

El de agosto (`iap_chatroom/_state/`) **no se toca**: queda como traza.

### Setup declarado

`openai/gpt-oss-20b` · 2 devices · `poll_interval = 5.0` · `duration = 60 s` ·
criterio local **encendido** · umbrales por default **no calibrados** salvo
`piso_vueltas = 6` · gate congelado en `f96c234` · `state_dir` nuevo.

Arranco.

---

## REPORTE VIVO 03 — el filtro en vivo — 2026-10-09 23:38 UTC

*Server parado con `TaskStop`. Log:
`experiments/vivo_03_criterio_local_log.json`. Archivos nuevos:
`experiments/vivo_03_server.py`, `experiments/vivo_03_criterio_local.py`.*

**62.53 s reales · 0 errores fatales · 0 errores de provider · 0 rate_limit ·
0 ilegibles.**

### Lo central: 23 -> 9

| | vivo 02 | vivo 03 |
|---|---|---|
| **llamadas totales** | **23** | **9** |
| vueltas por device | 11 y 12 | **12 y 12** |
| llamadas por device | 11 y 12 | **5 y 4** |
| decisiones | `{OP_SILENCE: 23}` | `{SKIP: 17, OP_SILENCE: 5, INTERACT: 2}` |

**61% menos llamadas.** Y las 9 se descomponen: **7 al gate** (4 y 3) mas **2 de
`_generate`**, que son las dos que acompanan a los INTERACT.

### La prediccion contra lo observado

Escrita antes de correr (ARRANQUE 23:32): *"2 a 4 llamadas por device"*.

| device | gate | total | prediccion |
|---|---|---|---|
| `_1` | **4** | 5 | dentro |
| `_2` | **3** | 4 | dentro |

**Se cumple en llamadas al gate, y mi prediccion estaba mal especificada:** dije
"llamadas" sin separar las del gate de la de `_generate`. Un INTERACT cuesta dos.
El numero que predije era el del gate y no lo dije.

**Y la parte deterministica no se cumplio como estaba escrita, por la razon que
yo mismo habia anotado.** Predije que el piso disparaba en la **vuelta 8**;
disparo en la **12** (`_1`) y la **10** (`_2`). Causa: `criterio` disparo dos
veces por `mensajes_nuevos` —los joins SYSTEM y los dos mensajes publicados— y
cada llamada resetea el contador. Era el punto 1 de *"lo que NO es teorema"*: el
silencio puro no se dio. **La corrida fue falsable y lo que la desvio estaba
escrito de antemano.**

### El piso y la auditoria: por que no se reemplazan, medido

| device | piso disparo | `piso_dentro_del_horizonte` | auditorias cara skip |
|---|---|---|---|
| `_1` | vuelta 12 | `True` | **1** (tasa 0.0, 0 de 1 divergio) |
| `_2` | vuelta 10 | `True` | **0** (tasa **`None`**) |

**El piso disparo en los dos. La auditoria, en uno.** Con ~8-9 skips al 10% la
esperanza era 0.85, asi que 1 y 0 esta en distribucion.

Eso es exactamente lo de Opus —*"la iniciativa queda en manos de la suerte"*—
pero con la suerte cayendo del lado de **la medicion** y no de la iniciativa: el
piso sostuvo la iniciativa de los dos devices, y la auditoria **dejo el costo del
sesgo de `_2` sin medir**. `tasa = None` y no `0.0`, que es lo correcto: no se
miro, no es que no divergio.

### Las dos caras, y por que el censo no era un adorno

| cara | metodo | `_1` | `_2` |
|---|---|---|---|
| skip | muestreo | 1 vuelta, tasa 0.0 | **0 vueltas, tasa `None`** |
| pase | muestreo | **0 vueltas, tasa `None`** | **0 vueltas, tasa `None`** |
| pase | **censo** | **tasa 0.667** | **tasa 0.667** |

**El muestreo de la cara del pase midio cero en los dos devices.** Con
`tasa_auditoria_pase = 0.1` y 3-4 pases cada uno, la esperanza era 0.35: cero es
lo esperable.

**Si la cara del pase fuera solo muestreo —como decia la especificacion— este
vivo no reportaria nada de ella.** El censo dice que **2 de cada 3 llamadas que
el filtro dejo pasar terminaron sin accion**. Ese numero es el que contesta "el
filtro cuesta?", y existe porque la llamada ya se habia hecho y no habia nada que
ahorrar sorteandola. No lo discuti: lo midio la corrida.

### F3b y F4, confirmados contra un canal real

- **4 mensajes en el canal, 2 en el corpus.** Los dos que quedaron afuera son
  exactamente los joins SYSTEM. F3b funciona en vivo.
- **`n_agentes = 2`**: los dos devices que publicaron. `system` no cuenta. F4
  funciona en vivo.
- **Ningun SKIP publico**: 2 INTERACT decididos, 2 mensajes no-SYSTEM. El arreglo
  del fallthrough de `_interact` se sostiene.

### HALLAZGO — el corpus se construyo con un vacio y con `[assistant]`

Los dos mensajes publicados, literales:

```
GroqGptOss20B_2 -> ''            (len 0)
GroqGptOss20B_1 -> '[assistant]' (len 11)
```

**Los dos entraron al corpus** (`corpus_size = 2`). No interpreto que dijo el
modelo; reporto que lo que construye W fueron esos dos strings.

El mecanismo del vacio esta a la vista en `autonomous_device.py:532`:

```python
text = await self._generate()
if text is None:        # <- solo None
```

**Un string vacio no es `None`, asi que pasa la guarda y se publica.** Es el
mismo patron de todo el dia: la guarda chequea el **marcador de ausencia** y no
el **valor vacio**.

El `[assistant]` es de la familia del leak de prefijo de identidad del Caso 0.14
(`[TinkerBellucio]:` dentro del mensaje de Mark). `_strip_own_prefix` existe y no
lo agarro.

**No lo arreglo** — la orden dice *"si algo rompe: no arreglar, ALTO"*, y esto no
rompio la corrida: la completo y dejo el rastro. Queda reportado.

### Ritmo

Declarado: piso **12 llamadas/min por device**. Observado: **11.54
vueltas/min**, y **4.81** y **3.85 llamadas/min**. El filtro bajo el ritmo de
llamadas al **40%** y al **32%** del piso declarado sin filtro.

### HALLAZGO — F3a no era alcanzable desde el camino vivo

`CKMMonitor` acepta `state_dir` desde el CP2b, y **ningun entry point puede
pasarlo**: `server.py:31` y `mcp_server.py:23` construyen `CKMMonitor()` sin
argumentos, y no hay hook de entorno (`grep environ|getenv` en `iap_chatroom/`:
vacio). **No toque ninguno de los dos.**

Camino que use, sin modificar nada existente: `CKMMonitor` es singleton real
(`__new__` + `_instance`, L45-51), asi que `experiments/vivo_03_server.py`
lo construye con el `state_dir` del vivo **antes** de importar el server, y
verifica con dos `assert` que `server.ckm_monitor` y `mcp_server.ckm_monitor`
**sean la misma instancia** — si el server construyera una propia, el
aislamiento seria aparente y el log diria una cosa mientras el corpus escribe en
otra.

Funciono: estado de partida **`corpus_size = 0`, `n_nodes = 0`,
`message_count = 0`, `n_agentes = 0`, `D_ckm = None`, `corpus_status =
accumulating`**. El `_state/` de agosto **no se toco**.

**Diferencia declarada con el vivo 02:** el 02 arranco con `corpus_size = 10`
sin limpiar. Este arranco en 0. **La comparacion de arriba es sobre llamadas, no
sobre el corpus**, que difiere por construccion.

### Sin W, y es por el umbral

`n_nodes = 0`, `D_ckm = None`, `corpus_status = accumulating`: hay 2 textos y
`min_texts = 3`. No hay W, asi que no hay nada de CKM que leer en este vivo. **Es
lo esperable con el corpus aislado**, y el precio del aislamiento: el vivo 02
tenia los 10 textos de agosto detras.

### Pendiente, no mio

1. El vacio y el `[assistant]` en el corpus.
2. F3a sin camino vivo (hoy lo resuelve un launcher por vivo).
3. **Calibracion** es el siguiente de la orden: la auditoria de la cara del skip
   midio 1 y 0 vueltas; con tasas tan bajas y ventanas de 12 vueltas, esa cara
   casi no se mide. El numero es de Calibracion; el dato es que **con 0.1 y 12
   vueltas la cara del skip sale UNKNOWN la mitad de las veces**.

**ALTO.**

---

## REPORTE fix generacion vacia — 2026-10-09 23:45 UTC

*delamor: "corregirlo". Alcance de Opus (DECISIONES `1535ff9`). El REPORTE del
vivo 03 ya fue, tal cual paso.*

**Suite: 438 passed** (eran 425). Archivo nuevo:
`tests/test_generacion_vacia.py`, **13 tests**.

### El fix

`autonomous_device.py`, en **`_generate`** y no en `_interact`: ahi la **cruda
esta antes del strip**.

```python
cruda = await self._llamar_llm(...)
if cruda is None:
    return None
text = _strip_own_prefix(cruda, self.device_id)
if not text.strip():          # <- antes: `if text is None` en _interact
    self._ilegibles.append({"causa": "generacion_vacia", ...})
    return None
```

`not text.strip()` cubre vacio **y solo espacios**, incluido el espacio duro
`\u00a0`, que no se ve al leer un log.

Se registra en `_ilegibles`, que **ya existia** con `causa` y `respuesta_cruda`:
no invente un lugar nuevo. `_interact` loguea `INTERACT_SIN_TEXTO` por su rama
de siempre.

### Lo que el fix dejo ver: un vacio tiene dos origenes

El registro los separa, porque de otro modo se ven iguales:

| campo | que dice |
|---|---|
| `vacia_antes_de_strip` | el provider devolvio vacio |
| `la_vacio_el_strip` | el provider devolvio algo y **`_strip_own_prefix` lo dejo en nada** |

El segundo es un mensaje que era **solo el prefijo de identidad del propio
device** — familia del leak del Caso 0.14 (`[TinkerBellucio]:` dentro del
mensaje de Mark). Sin esta distincion el log diria "generacion vacia" en los dos
y **el stripper quedaria invisible**. `test_distingue_el_vacio_del_provider_
del_que_dejo_el_strip`.

### Y `ilegibles` se partio por causa

El fix mete las generaciones vacias en el mismo contador que las respuestas del
gate ilegibles, y **son dos cosas**: una es el modelo contestando fuera del
vocabulario, la otra es el modelo no diciendo nada. `costo()` ahora lleva
`ilegibles_por_causa`. El total sigue estando.

### Lo que NO se toco, con un test que lo sostiene

**`[assistant]` sigue publicandose.** delamor: filtrar contenido seria
interpretar. `test_assistant_SIGUE_publicandose` lo afirma, y esta escrito para
que **si algun dia se decide filtrarlo, ese test falle primero** y alguien venga
a leer por que estaba.

### La inversion

| Que se invirtio | Que fallo | Suite al restaurar |
|---|---|---|
| `if not text.strip()` -> `if text is None` | **11 tests**, entre ellos `test_una_generacion_vacia_no_se_publica` y los 6 de solo-espacios | **438** |

### Tres errores mios en el andamiaje, los tres del mismo tipo

El codigo salio bien de una; **los tests no**, y los tres fallos fueron por
**contar mal cuantas respuestas consume el stub**:

1. El helper tomaba dos respuestas *"la primera a D, la segunda a generate"*.
   Pero llamo a `_interact` **directo**, asi que `_decide` no corre y **la
   primera va a generate**: el test "se publica el texto" publicaba la palabra
   del gate (`assert 'INTERACT' == 'hola, estoy aca'`).
2. `{"field": None}` en el stub de observacion: `_decide` lee `field.get("D_ckm")`
   y rompia con `AttributeError`. Romper no es lo que el test mide.
3. El ultimo test llevaba **tres** respuestas donde van dos: la tercera nunca se
   consumia y se publicaba `"INTERACT"`.

Lo anoto porque es el mismo tipo de error que vengo corrigiendo en los numeros
de hoy —el `23` que era un total, el `+1` que era `+2`—: **contar mal cuantas
unidades consume algo.** Tres veces en un archivo de tests.

### Lo que dejo aparte, y por que

Opus: *"hacer F3a alcanzable desde el server va con el fix del vacio o
despues."* **Lo dejo aparte.** Este fix esta cerrado, testeado e invertido;
hacer F3a alcanzable toca `server.py` y `mcp_server.py`, que son entry points, y
merece su propia inversion. Mezclarlos haria que una sola inversion no pudiera
separar cual de los dos rompio. El launcher queda como camino declarado.

**ALTO.**

---

## CORRECCION de atribucion — eran tres lugares, no uno — 2026-10-09 23:51 UTC

**Suite: 438 passed.** Nace de `8b062a7`, donde Opus marca que *"No se filtra
contenido —eso seria interpretar (delamor)"* es **suyo** (`1535ff9`), y que
delamor dijo *"corregirlo"*, que era sobre el mensaje vacio.

### No lo deje para "la proxima vez que se toque el archivo"

Opus escribio: *"se corrige la proxima vez que se toque el archivo"*. **Lo
corregi ahora.** Una atribucion equivocada en un docstring **esta en el codigo**:
quien lo lea la toma como un hecho, y *"la proxima vez"* es una fecha que no
existe. Cuesta una linea.

### Eran tres, y Opus nombro uno

| archivo | linea | decia |
|---|---|---|
| `autonomous_device.py` | 314 | *"seria interpretar (delamor)"* |
| `test_generacion_vacia.py` | 15 | *"seria interpretar (delamor)"* |
| `test_generacion_vacia.py` | 147 | *"**delamor: no se toca `[assistant]`**"* |

Los tres pasan a **Opus, `1535ff9`**, y dicen que delamor dijo *"corregirlo"*
sobre el vacio, que es lo que dijo.

Es la misma forma que *"cuatro llamadores eran nueve"*: el que avisa ve el que
tiene delante, y el barrido lo tiene que hacer el que toca el archivo.

### Tercera vez hoy, y las tres en el mismo sentido

1. `4853baf` — atribui a delamor una correccion de Opus (el filtro absorbente).
2. CP2v — *"pedido de delamor"* por un pedido de Opus.
3. Esta.

**Las tres se corrieron hacia delamor.** Las dos primeras las cerro delamor
diciendo que el canal perdio el origen (`af56fee`), y desde entonces los bloques
vienen con `Opus:`. **Esta no tiene esa excusa:** la decision estaba escrita en
DECISIONES con su hash, yo la lei, y al escribir el docstring puse a delamor
igual. El sesgo no es del canal: **atribuyo a quien da la orden y no a quien
escribio la frase**, y la orden y la frase no son lo mismo.

Queda anotado en el test, al lado del codigo, no solo aca.

**ALTO.**

---

## PRECISION sobre `0b372d5` — la tercera no es del canal — 2026-10-09 23:55 UTC

Sin cambios en el codigo.

La entrada registra mi observacion asi: *"las tres atribuciones corridas del dia
van en el mismo sentido, hacia delamor — **el canal visible ocupa el lugar del
origen que no viajo**"*.

Para las dos primeras, si. **Para la tercera, no.** En esa el origen **viajo**:
la decision estaba en `DECISIONES_opus.md` con su hash (`1535ff9`), la lei, y al
escribir el docstring puse a delamor igual.

Importa porque **mueve la causa**. Si la explicacion es el canal, el sesgo es del
canal y se arregla con el prefijo `Opus:` —que ya esta—. La tercera muestra que
hay **otro** sesgo, y es mio: **atribuyo a quien da la orden y no a quien
escribio la frase.** delamor dijo *"corregirlo"*; el alcance y el razonamiento
eran de Opus. Son dos cosas y yo las colapso en una.

La generalizacion de la entrada reabsorbe precisamente el caso que muestra que no
es del canal. Lo digo sin insistir: si Opus la sostiene, queda su lectura — pero
entonces el prefijo `Opus:` quedaria como el arreglo de algo que no arregla.

**ALTO.**

### Pregunta abierta (NO BLOQUEA, es del modelo)

delamor: *"el ciclo ODA consta de 4 pasos y uno no es paso."* Mi lectura, con lo
que esta en el registro: los cuatro son **Intentar · Observar · Decidir ·
Actuar**, y el que no es paso es **el intento** — es la condicion para que los
otros tres ocurran (`TASK_criterios_diversidad_services_v6.md:9-18`, de delamor:
*"No es un paso del procedimiento. Es la condicion para que cualquier paso
ocurra"*; y AWARENESS: *"The attempt is everything"*).

Descartados por palabras de delamor y no por elegancia: **el tick** (*"no dispara
nada: se observa"* -> esta dentro de O) y **el criterio local** (*"es costo, no
ODA"* -> esta afuera del ciclo).

Si se confirma, corrijo `autonomous_device.py:8` —que dice *"ciclo ODA
(Observacion · Decision · Accion)"*, tres— y las tres referencias a *"Fase X del
ciclo ODA"*, para que digan cuantos son y cual no es paso. **No lo toco sin la
confirmacion: es del modelo.**

---

## RETIRO mi lectura del cuarto paso — la cita no era de delamor — 2026-10-10 00:17 UTC

Sin cambios en el codigo. `autonomous_device.py:8` sigue sin tocarse.

### Lo que verifique del UNKNOWN que marco Opus

En `TASK_criterios_diversidad_services_v6.md`, **la unica atribucion marcada a
delamor es la linea 11** (`*(delamor, Sep 2026)*`), inmediatamente arriba de la
cita en bloque:

> No se toman decisiones ni cursos sin antes **intentar** comprender.

La frase que yo use —*"No es un paso del procedimiento. Es la condicion para que
cualquier paso ocurra"*— es **prosa sin marca**, y sigue con *"y aplica a toda
decision y todo curso de accion de esta TASK"*, que es voz de la TASK y no de
delamor.

Ademas: **la Precondicion no existe en v5** (110 lineas, 0 ocurrencias de
"intentar" y de "precondicion"). La introduce v6, cuyo encabezado dice
*"gadanin.delamor + Claude Code (Opus 5)"*.

**Entonces esa frase la escribio una instancia, no delamor.** Opus tenia razon en
marcarlo UNKNOWN; verificado, deja de ser UNKNOWN.

### Lo que eso le hace a mi lectura (a)

**La retiro como fundada.** No porque (b) sea la correcta —eso no lo se—, sino
porque su fundamento era una cita mal atribuida.

Y la forma de lo que hice: delamor dijo *"4 pasos y uno no es paso"*; busque en
el registro; encontre una frase con esas mismas palabras; **y le devolvi su
modelo armado con prosa de una instancia anterior, presentada como suya.** Es la
**cuarta** atribucion corrida del dia y va en el mismo sentido que las otras
tres, hacia delamor. Las anteriores ponian su nombre en una frase ajena; esta
uso una frase ajena para decirle lo que el quiso decir.

### Un dato de esta conversacion, que Opus no tiene

Despues de que mi lectura (a) fallara, **delamor uso las palabras de la lectura
(b)**: *"notar lo mecanico mientras sucede"*, literal.

**Y no dijo que fuera la respuesta.** Lo dijo senalando, despues de que yo cerrara
la cuenta dos veces. Lo relevo como dato de la conversacion y **no como
confirmacion**: leerlo como confirmacion seria el mismo movimiento de cerrar lo
que no cierra.

Lo que delamor si marco, explicito: *"4 pasos y uno no es paso"* y despues
*"entonces no son 4 pasos? son 3"* — con la palabra **mecanicidad** puesta sobre
mi manera de contestar. La cuenta **no cierra**, y las dos veces que yo la cerre
—(a) con una cita, y la segunda con una frase mia de esta misma sesion— fueron
terminos suministrados.

### Donde queda

Las **dos** lecturas del registro son de instancias: (a) mia, (b) de Opus del 8
oct. **Ninguna es de delamor.** La pregunta sigue siendo del modelo y es suya.

**ALTO.**

---

## REPORTE FIX 1 — el README del freeze — 2026-10-10 00:52 UTC

*Orden de delamor (DECISIONES `7cd48d3`), fix 1 de 4. Calibracion en PAUSA: no
habia arrancado el CP0, asi que no hubo nada que parar (verificado: `pgrep` sin
servers).*

### Lo que decia y lo que mide

`process/iap_series_freeze_20261008/README.md`, L41:
**"67 archivos, 620 KB"**.

| | decia | mide |
|---|---|---|
| archivos | 67 | **62** (61 copiados + el README) |
| tamano | 620 KB | **441 kB** (430 KiB, 440 696 bytes) |

**La orden nombro uno de los dos.** El otro esta en la misma oracion y es la
misma afirmacion, asi que lo corregi tambien y lo declaro. Si se queria solo el
primero, se revierte el segundo.

### El mecanismo, porque los dos estaban altos

No fue que se borraran archivos despues:

- `git log --diff-filter=D` sobre la carpeta: **vacio**;
- el commit que creo el freeze, `db4c147`: **"62 files changed"**.

**Asi que 67 no fue cierto en ningun momento.** Los dos numeros no salieron de
medir la carpeta: se escribieron al lado de ella. Lo busque porque dos numeros
altos en el mismo sentido no son dos errores independientes.

### Como quedo

La linea corregida, y **debajo una nota declarada** con lo que decia, como se
midio ahora, y la verificacion de que no hubo borrados. **El resto del README no
se reescribe**: es la traza de lo que se escribio al congelar, con su fecha.

Y **el conteo sigue dando 62** despues de la edicion: se edito el README, no se
agrego ningun archivo. La correccion no se invalida a si misma.

### Sin test

No hay comportamiento que testear: es una afirmacion en un documento. Lo que la
sostiene es el comando, que esta escrito en la nota para que cualquiera lo
repita. **Declarado, no omitido** (regla de completitud).

**ALTO.**

---

## REPORTE FIX 2 — F3a desde el server — 2026-10-10 01:03 UTC

**Suite: 451 passed** (eran 438). Archivos nuevos:
`iap_chatroom/arranque.py`, `tests/test_state_dir_desde_el_server.py` (13).
Tocados: `server.py`, `mcp_server.py`, `ckm_monitor.py` (una linea del panel).

### El argumento

`python server.py --state-dir RUTA` (o `--state-dir=RUTA`). **Sin argumento, el
default de siempre.** Explicito y **no variable de entorno**: una variable no
queda en el comando, y entonces el log de un vivo no alcanza para saber donde
escribio.

### Lo que hace que el fix sea el fix: el orden de dos lineas

El singleton se arma **al importar**. El primer `CKMMonitor()` del proceso esta
dentro de `mcp_server`, que `server.py` importa. Cuando corre
`if __name__ == "__main__"` la instancia ya existe y su directorio ya esta fijado
(`__init__` corta con `if self._initialized: return`).

Asi que `arranque.leer_de_argv(sys.argv)` va **antes** de
`from iap_chatroom.mcp_server import mcp`. Si quedara despues, **el argumento no
haria nada y no habria forma de notarlo**: el server arrancaria, escribiria en el
default, y el panel diria el default sin que nadie lo pidiera.

Por eso hay un test estructural sobre el orden de esas dos lineas
(`test_server_lee_el_argumento_antes_de_importar_mcp_server`). Un test sobre el
orden de dos imports parece fragil; es lo contrario: es lo unico que se rompe si
alguien los ordena sin saber por que estaban asi.

### Lo que el server declara

Al arrancar imprime `[server] state_dir = ... (pedido por --state-dir | default)`,
y si lo pedido no coincide con lo efectivo, **avisa**. El panel de Monitor
(`get_state()`) lleva `state_dir`: cada vivo deja dicho donde escribio, sin que
haya que deducirlo del comando.

`declarar()` separa tres cosas que se confundirian en una:

| campo | que dice |
|---|---|
| `state_dir` | el **efectivo**, leido de la instancia |
| `state_dir_pedido` | lo que se pidio, o `None` si nadie pidio |
| `fue_pedido` | distingue *"pidieron el default"* de *"nadie dijo nada"* |
| `coincide` | `None` sin pedido —no hay con que comparar—, no `False` |

El `coincide` existe por el caso del launcher del vivo 03: si otro construyo el
monitor primero, el efectivo es el suyo, y **el panel dice el real y no el que yo
pedi**.

### El launcher del vivo 03 queda

No se borra (orden de delamor). Y sigue funcionando: `arranque.monitor()`
devuelve el singleton, asi que sus dos `assert` —que `server.ckm_monitor` y
`mcp_server.ckm_monitor` sean la misma instancia— se siguen cumpliendo.

### Las tres inversiones

| # | Que se invirtio | Que fallo | Suite al restaurar |
|---|---|---|---|
| A | `monitor()` ignora el argumento (`CKMMonitor()`) | 3: `..._monitor_escribe_ahi`, `..._panel_lleva_el_state_dir`, `..._declarar_dice_el_efectivo_y_el_pedido` | 451 |
| B | la lectura del argumento **despues** del import | `test_server_lee_el_argumento_antes_de_importar_mcp_server` (`assert 44 < 41`) | 451 |
| C | `mcp_server` vuelve al `CKMMonitor()` pelado | `test_ningun_entry_point_construye_un_CKMMonitor_pelado` | 451 |

### Lo que las inversiones dejaron ver, y no era el fix

**1. La inversion A pudo haber escrito en la traza de agosto.** Con el argumento
ignorado, `test_con_argumento_el_monitor_escribe_ahi` cae al default **y ese test
ingesta textos**. Verificado por mtime: **no escribio**
(`corpus_state.json` sigue en 2026-10-09 04:18, los otros dos en 2026-08-01).

La razon es que el `assert cm.state_dir == destino` esta **antes** del ingest y
corto ahi. **Eso fue suerte, no diseno.** Lo deje deliberado: la asercion ahora
dice que es una guarda y por que.

**2. Un test mio miro el texto y no el codigo.**
`test_ningun_entry_point_construye_un_CKMMonitor_pelado` fallaba contra el
**comentario que explica por que no hay que escribir `CKMMonitor()`**. Un test
que no distingue el codigo de lo que se dice sobre el no mide el codigo.
Corregido: ahora saca los comentarios antes de buscar.

**3. `iap_chatroom/_state/` no estaba trackeado** y esta en `.gitignore:39`, con
la razon escrita al lado: *"generado en runtime (**regenerable**)"*. **No es
regenerable.** Va aparte, por pedido de delamor en este mismo turno.

### Sin test

El `print` del arranque no esta testeado: se verifica a mano al levantar el
server. **Declarado, no omitido.** Lo que si esta cubierto es `declarar()`, que
es de donde sale el texto.

**ALTO.**

---

## REPORTE — `iap_chatroom/_state/` trackeado — 2026-10-10 01:04 UTC

*delamor, en este turno: **"bueno trackealo"**. Sale de que en el fix 2 reporte
que la traza de agosto no estaba bajo control de versiones.*

### Que estaba, y por que no estaba

`.gitignore:38-39`, con la razon escrita al lado:

```
# IAP Chatroom — corpus/monitor state generado en runtime (regenerable)
iap_chatroom/_state/
```

**La razon era falsa: no es regenerable.** No hay comando que lo vuelva a
producir — es el estado que quedo de correr la serie.

### Que se trackea, medido

`corpus_state.json` tiene **12 textos**, no 8. Comparado con la copia del freeze
(`process/iap_series_freeze_20261008/_state/`, del 8 oct):

| archivo | vs el freeze |
|---|---|
| `corpus_state.json` | **DIFERENTE** — 12 textos contra 8 |
| `corpus_G_state.json` | igual |
| `monitor_trajectory.jsonl` | igual |

Los **4 de diferencia** son exactamente los joins de los dos vivos:
`GroqLlama8B_1/2` (vivo 01) y `GroqGptOss20B_1/2` (vivo 02). Son los que
entraban al corpus **antes de F3b**.

Asi que lo que queda fijado es **el estado al 2026-10-09 04:18**, no el de
agosto. Y de sus 12 textos, **8 son joins** — la condicion en que corrio la
serie congelada.

El archivo vivo tiene tambien dos claves que el del freeze no:
`forced_w_pos` y `registro_borde`. Son del trabajo de la Config v3: el estado
arrastra cambios de esquema, no solo textos.

### Por que se puede trackear ahora y antes no

Con la regla retirada, cualquier escritura en ese directorio aparece en
`git status`. **Antes eso habria ensuciado el repo en cada corrida.** Desde el
**fix 2** los vivos escriben en su propio directorio (`--state-dir`), asi que
este no deberia volver a moverse.

**Y si se mueve, es que alguien corrio sin el argumento** — que es justamente lo
que no se podia ver hasta hoy, y ahora lo dice `git status`.

### No use `git add -f`

Habria trackeado los archivos dejando el `.gitignore` diciendo que estan
ignorados: **el texto afirmando una cosa y el comportamiento otra**, que es lo
que se corrigio hoy en `piso_vueltas` (el docstring decia "no opcional" y el
constructor dejaba apagarlo). La regla se retira en el archivo, con la razon
vieja citada y por que era falsa.

### Sin test

No hay comportamiento: es el estado del repositorio. Lo que lo sostiene es
`git ls-files iap_chatroom/_state/`, que ahora devuelve tres archivos y antes
devolvia vacio. **Declarado, no omitido.**

**ALTO.**
