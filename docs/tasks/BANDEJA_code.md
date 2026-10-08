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
