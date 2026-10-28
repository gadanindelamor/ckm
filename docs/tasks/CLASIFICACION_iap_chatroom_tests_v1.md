# Clasificación de `iap_chatroom/tests/` — v1

*28 oct 2026. La levanta Code por el **punto 2a del texto para Code 16**. delamor, 27 oct:
*"iap_chatroom/tests/ es process. ¿sostiene REGs?, ¿o sostiene declaraciones en DEFS, en paper?
freezar el resto que no sostiene. y es historia… el punto es no agregar tests allí en esa carpeta, o
bien abrir la estructura del repo para que sea precisa"*.*

**Nada se movió. Esto es la tabla y una propuesta.** Mover es estructura del repo: lo lee Opus y da
el OK, o lo sube a delamor.

---

## 0. El dato que cambia la pregunta: 21 de los 34 ya están freezados

De los 34 `.py`, **21 son byte a byte idénticos** a su copia en
`process/iap_series_freeze_20261008/tests/` (verificado con `cmp` archivo por archivo). Para esos
21, "mover a `process/`" **no es mover: es borrar una copia**, porque la historia ya está preservada
y no se perdería nada.

Y las DEFS v19 ya lo dicen con ese número: *"Los **21** `test_caso_*` del canal no son tests de
pytest (recogen 0 items) y necesitan claves de provider que el Codespace no tiene: punto ciego
declarado"* (§ línea 1111). Los 21 de las DEFS son exactamente estos 21.

Los **13** restantes no están en el freeze, y cinco de ellos **los cita código vivo**.

---

## 1. Los 21 `test_caso_*` — duplicados exactos del freeze

| archivo | qué es | qué sostiene (cita) | quién lo usa vivo | propuesta |
|---|---|---|---|---|
| `test_caso_cero.py` | driver del vivo 0 (serie 1) | nada propio; la serie entera está en `META_REG_consolidado_*` | nadie | **borrar la copia viva** (idéntica al freeze) |
| `test_caso_01.py` | driver de un vivo | ídem | nadie | ídem |
| `test_caso_02.py` | driver de un vivo | ídem | nadie | ídem |
| `test_caso_03.py` | driver de un vivo | ídem | nadie | ídem |
| `test_caso_04.py` | driver de un vivo | `META_REG_consolidado_v2/v4/v6`; su REG propio está **en el freeze** (`process/iap_series_freeze_20261008/registers/REG_iap_caso_04a_v1.md`) | nadie | ídem |
| `test_caso_04a.py` | driver de un vivo | `REG_iap_caso_04a_v1` (en el freeze) | nadie | ídem |
| `test_caso_04b.py` | driver de un vivo | `REG_iap_caso_04b_v1` (**también en `registers/`**) | nadie | ídem |
| `test_caso_05.py` | driver de un vivo | `REG_iap_caso_05_v1` (freeze), `REG_hint_next_instance_v5` | nadie | ídem |
| `test_caso_06.py` | driver de un vivo | `REG_iap_caso_06_v1` (freeze) | nadie | ídem |
| `test_caso_07.py` | driver de un vivo | `REG_iap_caso_07_v1` (freeze) | nadie | ídem |
| `test_caso_07_run2.py` | réplica del 07 | `REG_iap_caso_07_v1` (freeze) | nadie | ídem |
| `test_caso_08.py` | driver de un vivo | `REG_iap_caso_08_v1` (freeze) | nadie | ídem |
| `test_caso_09_provider_hetero_join_escalonado_2dev.py` | driver del caso 0.9 | `REG_iap_caso_09_v1` (freeze) — el caso que **confirmó** la heterogeneidad de provider | nadie | ídem |
| `…_2dev_PREGENERADO.py` | variante con textos pregenerados | **nada**: ningún REG lo nombra, ningún archivo vivo tampoco | nadie | ídem (el único sin ninguna cita) |
| `test_caso_10_device_skin.py` | driver del caso 0.10 | `REG_iap_caso_10_v1` (freeze) | nadie | ídem |
| `test_caso_11_two_skins.py` | driver del caso 0.11 | `REG_iap_caso_11_v1` (freeze), `REG_hint_next_instance_v8` | nadie | ídem |
| `test_caso_12_groq_research_skin.py` | driver del caso 0.12 | `REG_iap_caso_12_v1` (freeze) | nadie | ídem |
| `test_caso_13_handoff_dependency.py` | driver del caso 0.13 | `REG_iap_caso_13_v1` (freeze) — el del `OP_SILENCE` que se filtraba | nadie | ídem |
| `test_caso_14_handoff_english.py` | driver del caso 0.14 | `REG_iap_caso_14_v1` (freeze) | nadie | ídem |
| `test_caso_14_run2_opus_tinker.py` | réplica del 0.14 | `REG_iap_caso_14_v1`, `REG_iap_caso_15_v1` (freeze) | nadie | ídem |
| `test_caso_15_behavior_graph.py` | driver del caso 0.15 | `REG_iap_caso_15_v1` (freeze) | nadie | ídem |

**Lo que los 21 tienen en común:** son drivers de vivos de la serie 1, ya corridos y ya registrados;
**nada de afuera de la carpeta los importa ni los invoca**; y **su copia idéntica ya vive en el
freeze**, junto con los REG que los sostienen.

*Precisión de la columna "quién lo usa vivo": dice "nadie" por **fuera** de la carpeta. Adentro
algunos se nombran entre sí en sus docstrings —`test_caso_01.py` nombra a `test_caso_cero.py`,
`test_caso_03.py` a `test_caso_02.py`—, y eso se va junto con ellos: son citas entre archivos del
mismo grupo, no una dependencia viva.*

🔸 **Borrar es irreversible: E2.** No lo hago. Lo que propongo es borrar la **copia**, no el archivo
—el archivo sigue en `process/`— y la verificación byte a byte está hecha y es repetible con
`cmp iap_chatroom/tests/<x> process/iap_series_freeze_20261008/tests/<x>`. Si se prefiere no borrar
nada, la alternativa sin pérdida es mover los 21 a un `process/iap_tests_duplicados_<fecha>/`, que
deja dos copias en `process/` y ninguna viva.

---

## 2. Los 6 `armstrong_*` — sostienen REGs **y los cita código vivo**

| archivo | qué es | qué sostiene (cita) | quién lo usa vivo | propuesta |
|---|---|---|---|---|
| `test_armstrong_stop_coco.py` | driver de experimento (COCO sobre corpus Armstrong) | `REG_armstrong_stop_coco_v1`, `META_REG_consolidado_v3/v4/v5` | **`services/ckm_trust_rule.py:175`** lo cita con línea: *"autor único escrito a mano (`test_armstrong_stop_coco.py:35`)"* | **no mover hasta la revisión [delamor]** (abajo) |
| `test_armstrong_n_runs_sweep.py` | sweep de `n_runs` (60→70) | `REG_n_runs_sweep_armstrong_v1`, `META_REG_consolidado_v5/v6` | **`services/corpus_service.py:203`** (*"esos tests son traza"*) y **`services/coco.py:188`** (el docstring que corregí hoy, texto 15 punto 5) | ídem |
| `test_armstrong_via_corpus_v3.py` | réplica vía corpus | **DEFS v19 (línea 1112)**: *"`test_armstrong_via_corpus_v3.py:34` (`assert corpus.coco is not None`) **roto a sabiendas** por el CP4; va con la revisión de las seis salidas `armstrong_*`, de origen UNKNOWN [delamor]"* | **`services/corpus_service.py:202`** | ídem |
| `test_armstrong_boltzmann_comparison.py` | comparación de muestreos | `REG_armstrong_boltzmann_comparison_v1`, `REG_coco_w_congelada_v1` | nada vivo lo cita | ídem |
| `test_armstrong_wmixta_forced_wpos.py` | contrafáctico `force_w_pos` | `process/experiments/wmixta_forced_wpos/ABORTADA_LEEME.md` (corrida abortada) | **`services/corpus_service.py:610`** | ídem |
| `test_armstrong_replica_seed123.py` | réplica con otra semilla | **ningún REG**; `docs/tasks/TASK_armstrong_replica_addendum_v1.md` y `TASK_armstrong_replica_seed123_via_corpus_v3.md` | `test_armstrong_n_runs_sweep.py` lo nombra | ídem |

**Por qué "no mover" y no una propuesta propia:** las DEFS v19 (1112) dejan **las seis salidas
`armstrong_*` marcadas `[delamor]`**, como revisión pendiente de origen UNKNOWN. Mover los archivos
antes de esa revisión cambiaría las rutas que la revisión va a buscar. Y moverlos obliga a tocar
**tres docstrings de `services/`** que los citan con ruta y línea.

---

## 3. Los 2 `wmixta_*` — sostienen un REG cada uno

| archivo | qué es | qué sostiene (cita) | quién lo usa vivo | propuesta |
|---|---|---|---|---|
| `test_wmixta_natural_paso2.py` | driver de experimento (W mixta natural) | `REG_wmixta_natural_paso2_v1`, `REG_monitor_service_unificar_rutinas_v1`, `META_REG_consolidado_v6` | nada vivo lo cita | **queda**, en el lugar que se declare para "drivers que sostienen un REG" (§6) |
| `test_wmixta_forzado_paso3.py` | ídem, forzado | `REG_wmixta_forzado_paso3_v1`, `REG_monitor_service_unificar_rutinas_v1` | **`services/corpus_service.py:610`** | ídem |

---

## 4. Los 3 `iap_simulation*` — historia, sin REG propio

| archivo | qué es | qué sostiene (cita) | quién lo usa vivo | propuesta |
|---|---|---|---|---|
| `test_iap_simulation.py` | simulación de turnos (anterior al device autónomo) | `META_REG_consolidado_v2/v4/v6`; ningún REG propio | **`iap_chatroom/autonomous_device.py:5`** lo cita como lo anterior: *"simulación (`test_iap_simulation*.py`), que orquestan turnos en secuencia"* | **va a `process/` (freeze)**, y el docstring de `autonomous_device.py` se actualiza con la ruta nueva |
| `test_iap_simulation_adversarial.py` | ídem, adversarial | `META_REG_consolidado_v2/v3/v4` | ídem (el glob los cubre) | ídem |
| `test_iap_simulation_oposite_rol.py` | ídem, roles opuestos | `META_REG_consolidado_v2/v3/v5` | ídem | ídem |

---

## 5. Los 2 que quedan

| archivo | qué es | qué sostiene (cita) | quién lo usa vivo | propuesta |
|---|---|---|---|---|
| `test_mcp_client.py` | smoke test del server real por MCP (6/6) | `CHANGELOG.md:118`: *"test_mcp_client.py: 6/6 OK against real server (port 7860, no mocks)"* — traza fechada; `META_REG_consolidado_v2/v4/v6` | nada lo invoca | **dos lecturas, decide Opus**: (a) es historia y va al freeze; (b) es el **único** chequeo del server real que hay y encaja en el `--check` del `correr_caso0.sh`, que hoy hace su propia verificación por MCP inline. No propongo fusionarlo: eso cambia el script del vivo |
| `test_caso_serie2_caso0.py` | **driver del próximo vivo** | el caso de la serie 2; sus cuatro intentos están en `registers/REG_iap_serie2_caso0_intento4_v1.md` y en los REG borrador | **`iap_chatroom/correr_caso0.sh:57`** (`CASO=…`) y **`tests/test_caso_serie2_caso0_diseno.py`**, que lo lee por ruta | **queda vivo**, y §6 dice dónde debería vivir. **No lo muevo** (lo pide el punto 2a) |

---

## 6. Propuesta (sólo propuesta) de una estructura precisa

El pedido de delamor tiene dos mitades: *"no agregar tests allí"* **o** *"abrir la estructura del
repo para que sea precisa"*. Esto es la segunda, y lo que la hace precisa es que **el mecanismo no
sea la memoria de nadie**.

### 6.1 Lo que hoy hace que un archivo caiga ahí

`iap_chatroom/tests/` **parece** la carpeta de tests del paquete y no lo es: `pyproject.toml:71`
declara `testpaths = ["tests"]`, así que nada de ahí entra a la suite —y **no puede entrar**:
`tests/test_caso_serie2_caso0_diseno.py:534` dice que *"si alguien agregara `iap_chatroom/tests` a
`testpaths`, la suite dispararía el vivo"*. O sea: la carpeta tiene nombre de tests, contenido de
drivers, y una prohibición implícita de ser colectada.

### 6.2 La propuesta, en tres lugares y una regla de nombre

| qué | dónde | por qué |
|---|---|---|
| **la suite** | `tests/` (como hoy) | es lo único que `pytest` colecta |
| **los drivers de los vivos de ahora en adelante** | **`iap_chatroom/cases/`** (nuevo, rótulo en inglés) con un `README_cases.md` que declare la regla | un driver de un vivo **no es un test**: gasta cuota, dura 20 minutos y toca el canal |
| **lo que ya corrió y está registrado** | `process/<freeze>/` | lo que ya hace el freeze de octubre |

**Y la regla de nombre, que es el mecanismo:** un driver de un vivo **no se llama `test_*.py`**. Con
`python_files = ["test_*.py"]` (`pyproject.toml:72`), un archivo llamado `caso_serie2_caso0.py` **no
lo colecta pytest aunque alguien agregue el directorio a `testpaths`**. Hoy la protección es que el
directorio esté afuera; con el nombre, la protección viaja con el archivo.

Si esto se adopta, el movimiento es: `iap_chatroom/tests/test_caso_serie2_caso0.py` →
`iap_chatroom/cases/caso_serie2_caso0.py`, y hay que tocar **tres** lugares que lo nombran por ruta:
`iap_chatroom/correr_caso0.sh:57`, `tests/test_caso_serie2_caso0_diseno.py` (su `CASO_PATH` y los dos
asserts que citan la ruta) y los docs vivos que lo nombren. **No lo hice**: el punto 2a dice "decí
dónde tendría que vivir, pero no lo muevas".

### 6.3 Lo que esta propuesta **no** resuelve

- **Los seis `armstrong_*` y los dos `wmixta_*` no son drivers de un vivo ni tests**: son drivers de
  experimento sobre corpus fijos, que sostienen REGs y que `services/` cita con ruta y línea. No
  entran en ninguno de los tres lugares de arriba. Si hay un cuarto —algo como
  `experiments/corpus/`— lo decide quien defina la estructura; yo lo dejo nombrado como el hueco que
  es. Y los `armstrong_*` están marcados `[delamor]` (§2).
- **Qué parte de `iap_chatroom/tests/` entra a la suite**: ninguna, hoy, y la propuesta no cambia
  eso. Lo que sí propone es que deje de parecer que podría.

---

## 7. Resumen de las propuestas

| grupo | cuántos | propuesta | quién decide |
|---|---|---|---|
| `test_caso_*` idénticos al freeze | **21** | borrar la copia viva (o moverla a `process/iap_tests_duplicados_<fecha>/`) | **E2, irreversible** → Opus o delamor |
| `armstrong_*` | 6 | **no mover** hasta la revisión marcada `[delamor]` (DEFS v19, 1112) | delamor |
| `wmixta_*` | 2 | quedan, en el lugar que se declare para drivers de experimento | Opus |
| `iap_simulation*` | 3 | al freeze, actualizando el docstring de `autonomous_device.py:5` | Opus |
| `test_mcp_client.py` | 1 | al freeze, **o** reconocerlo como el chequeo del server real | Opus |
| `test_caso_serie2_caso0.py` | 1 | queda vivo; `iap_chatroom/cases/caso_serie2_caso0.py` si se adopta §6 | toca dónde viven los casos → delamor |
