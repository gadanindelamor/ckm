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
