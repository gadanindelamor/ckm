# INVENTARIO de defaults — v1

*28 oct 2026. Lo levanta Code por el **punto 4 del texto 15**
(`docs/opus/TEXTO_PARA_CODE_15_REPO_CKM_hacia_el_proximo_vivo_27oct2026.md`), como insumo de la TASK
de defaults. **Sólo lectura: no se implementa nada y no se decide nada.***

Las tres columnas las pidió delamor el 26 oct:

- **(a) ¿dónde se declara antes de que empiece un flujo?** — o "no se declara".
- **(b) ¿aparece en la traza o el panel como default?** — con su valor y de dónde sale.
- **(c) si no se declara: por qué, y qué impacto tiene.**

---

## 0. Alcance, y qué quedó afuera

Censo con AST sobre `services/*.py`, `iap_chatroom/*.py` e `iap_chatroom/providers/*.py` (sin
`tests/`, sin `experiments/`, como pide el punto):

| | cuántos |
|---|---|
| constantes de módulo | **117** |
| de ésas, **numéricas** (un valor que podría ser otro) | **25** |
| de ésas, nombres, rutas, prompts, nombres de archivo, dicts de mapeo | **92** |
| defaults de argumento de función o método | **171** |
| campos de dataclass con valor por default | **10** |

**Queda afuera de la tabla, declarado:**

- Las **92 constantes no numéricas** que son **nombres**: las 23 de `ckm_trust_rule` (`FIELD`,
  `MEASURED`, `REASON_*`), las 14 de `local_criterion` (`DECISION_SKIP`, `MOTIVO_*`, `VIA_*`), las 7
  de `run_store` (nombres de archivo), los prompts (`GATE_PROMPT_04`, `PLAN_PROMPT_TEMPLATE`), los
  `_STOPWORDS` y el `_OPPOSITION_RE`. No son defaults en el sentido de la pregunta: **no hay otro
  valor que declarar**, son la constante que le da nombre a una cosa. Si alguna se cambia, cambia el
  nombre de un estado, no el régimen de una corrida.
- Los defaults de `None` que son **el UNKNOWN del parámetro** y no un valor: `clock=None`,
  `device_id=None`, `w_sha=None`, `causa=None`, `t_senal=None`. Su ausencia ya viaja declarada (el
  caso canónico: `reloj: "desconocido"` cuando `calibrate` no recibe `clock`).
- `services/analytics.py` (`n_clusters=4`, `threshold=-0.9`, `rho_steps=30`, `n_samples=300`,
  `seed=42`) y `basin_distance` (`k_max=4`, `k_exhaustivo=2`, `n_muestras=500`, `seed=0`): **no están
  en el camino vivo**. Si alguna vez entran, entran a esta tabla.

---

## 1. Muestreo de σ₀ — lo que resolvió el texto 13

| parámetro | valor | (a) dónde se declara | (b) en la traza | (c) si no se declara |
|---|---|---|---|---|
| **`n_runs`** ✅ texto 13 | 200 | `ckm_landscape_config.N_RUNS_DEFAULT`, **un solo lugar** para Monitor, COCO y la copia de W; se lee con `sampling_for(caso)` | **Sí**, dos veces: `panel.landscape_config.n_runs` y `panel.condicion_W.n_runs`; y `panel.coco.calibrate_declarado.n_runs` | — |
| **`seed`** ✅ texto 13 | 0 | ídem, `sampling_for(caso)` | **Sí**: `panel.landscape_config.seed`, `panel.condicion_W.count_seed`, `calibrate_declarado.seed` | — |
| `n_runs_attractors` (MonitorService) | `None` | `None` **quiere decir "lo trae la Config"** (`monitor_service.py:108-113`) | sí, resuelto, en `condicion_W.n_runs` | — |
| `count_seed` (MonitorService) | `None` | ídem | sí, en `condicion_W.count_seed` | — |
| `n_runs=80` (firma de `COCO.__init__`) | 80 | **nadie lo usa en un vivo**: `monitor_service.py:849-850` lo sobrescribe con `sampling_for("coco")` y, sin Config, con `self._n_runs` (`:854`) | el valor efectivo sí; **el 80 no aparece nunca** | el 80 es un default **inalcanzable** en el camino vivo. Impacto hoy: ninguno. Riesgo: quien lea la firma lee 80 y el vivo corre 200 |
| `seed=0` (firma de `COCO.__init__`) | 0 | ídem | ídem | ídem |
| **`sampling_mode`** | `'uniform'` | `CKMlandscapeConfig` lo lleva (`panel.landscape_config.sampling_mode`), y es también default de firma en `MonitorService.__init__` y `COCO.__init__` | **Sí el valor** (`panel.sampling_mode` y `landscape_config.sampling_mode`) — **no** si fue default o declarado | **`calibrate` no lo lee**: su copia de W cuenta siempre en `uniform` (lo declaró Opus el 27 oct, E3, abierto). Y "uniform" no es la medida del paper: ver texto 14 punto 3 |
| `n_warmup` | `None` → `N` | `None` en las tres firmas; el engine resuelve `n_w = n_warmup or W.shape[0]` (`landscape_engine.py:252`) | **No** | sólo entra con `boltzmann=True`, que hoy no corre. Impacto hoy: ninguno; si alguna vez se usa Boltzmann, el calentamiento queda sin declarar |
| `weighted` / `boltzmann` | `False` / `False` | sólo la firma; el modo efectivo lo decide `sampling_mode` arriba | **No** como banderas; sí indirectamente vía `sampling_mode` | dos caminos para decir lo mismo (las banderas y el modo). `REG_orbitas…` §10(c) midió que `weighted` **es otra cantidad**, no un estimador peor |
| `max_iter` (`relax`, `relax_orbit`) | 200 | sólo la firma, en cuatro lugares (`landscape_engine.py:37,148`, `coco.py:650,654`, `monitor_service.py:942,946`) | **No** | la salida defensiva de `relax_orbit` (órbita no cerrada) **no se observó nunca** (0 de 800 runs, su docstring). Impacto: con N grande podría cortar sin que nada lo diga |

---

## 2. COCO — el único grupo que declara su propio default en el panel

| parámetro | valor | (a) | (b) | (c) |
|---|---|---|---|---|
| `D_CKM_THRESHOLD` | 0.4 | `coco.py:94`; lo puede reemplazar la calibración | **Sí, y dice que es default**: `panel.coco.thresholds.source = "default"`, `calibrated: false`, y `origen.d_ckm_threshold.source = "default de coco.py — no_calibrado:sin_separacion"`, con `provenance: DECLARED` | — |
| `FRAC_REC_MIN` | 0.6 | ídem | ídem, con su `origen` | — |
| `ALPHA_STAR` | 0.1 | `coco.py:95` | el `alpha_used` efectivo viaja en el estado | con `dynamic_alpha=True` (el default) el α se calcula; el 0.1 es el piso de la rama estática |
| `ALPHA_MIN` / `ALPHA_MAX` | 0.05 / 0.3 | `coco.py:99-100` | el α usado sí; los bordes **no** | el rango que acota el α no se declara. Impacto: un α pegado a un borde se lee como decisión y es el clip |
| `dynamic_alpha` | `True` | sólo la firma | **No** | dos regímenes de α y la traza no dice en cuál corrió |
| `gamma` | 0.01 | sólo la firma | **No** | — |
| `BETA_TOO_COLD` / `BETA_TOO_HOT` | 2.0 / 0.5 | `coco.py:113-114` | la `temp_signal` resultante sí (`TOO_COLD` en el intento 4); los cortes **no** | los dos umbrales que parten la señal de temperatura no viajan. Impacto: `TOO_COLD` no es reconstruible desde la traza sin leer el código |
| `epsilon` (`beta_i`) | 1e-06 | sólo la firma | **No** | guarda numérica, no régimen |
| `RHO_STAR` / `BETA_RHO_STAR` | 0.5 / 0.5 | `ckm_landscape_config.py:50`, `landscape_engine.py:32` | `panel.landscape_config` lleva `beta_c_*`, no ρ* | ρ* = 0.5 es la identidad algebraica `relax(−σ) = −relax(σ)`, no un parámetro libre |

---

## 3. `calibrate` — la grilla y el patrón

| parámetro | valor | (a) | (b) | (c) |
|---|---|---|---|---|
| `grilla_lambda` | `(0, .25, .5, .75, 1)` | `calibrate.GRILLA_LAMBDA_DEFAULT`; la Config puede traer `calibrate_grilla` | **Sí**: `condiciones.grilla_lambda` en cada registro, y `calibrate_declarado.grilla_lambda` | — (medido en el texto 14 punto 1: λ=0,75 y λ=1,0 dan **conteos idénticos** en las 14 curvas, así que la grilla de 5 tiene 4 puntos distintos) |
| `representacion` | `'presencia'` | firma de `calibrate` | **Sí**: `condiciones.representacion` | — |
| `FRACCION_EXPANSION_DEFAULT` | 0.5 | `calibrate.py:137` | **No** | `extremo_expansion` **no la llama `calibrate`** hoy (sólo el extremo de colapso entra a la curva). Impacto hoy: ninguno |
| `seed` de `extremo_expansion` | 0 | firma | **No** | son **dos `seed` con el mismo nombre** y distinto referente (una elige pares, la otra sortea σ₀): BABEL, abierto con delamor |
| `N_RUNS_DEFAULT` de `calibrate` | 200 | `calibrate.py:143`, **default de la función** para quien la llame sin declarar (tests, offline) | el registro dice `n_runs` efectivo | coincide con el de la Config **y son dos lugares distintos**: su docstring lo dice (`:108-112`). Que coincidan no los une |
| `escala_desde_traza` | `None` | firma | **Sí**: `condiciones.escala_desde_traza` (null = primer ciclo) | — |

---

## 4. Corpus, nodos y W

| parámetro | valor | (a) | (b) | (c) |
|---|---|---|---|---|
| `top_k` | 20 | `ckm_monitor.TOP_K = 20` se lo pasa a `CorpusService`; la firma también dice 20 | **Sí**, en la declaración de extracción (`declaracion_extraccion`), cuyo sha viaja en cada versión de W (`declaracion_sha`) | — |
| `min_df` | 2 | `node_extractor.MIN_DF` | **Sí**, en la misma declaración | — |
| `ngram_max` | 2 | firma (`CorpusService`, `NodeExtractorService`) | **Sí**, en la declaración | — |
| `window` | 1 | firma de `NodeExtractorService` | **Sí**, en la declaración | — |
| `perfil` | `PERFIL_ES_EN` | `node_extractor.py:284` | **Sí**: la declaración lleva `perfil.nombre = "es_en_v1"` y su `alcance`, que dice *"fuera de esto: NO SE SABE"* | — |
| `min_texts` (CorpusService) | 3 (firma) / **30** en el vivo | `ckm_monitor.MIN_TEXTS_FIRST_W = 30` | el 30 viaja en el log del caso (`declarado`) | el 3 de la firma es el default de la clase y **no corre en un vivo** |
| `min_texts` (BehaviorGraph) | 5 (firma) | `ckm_monitor` le pasa el mismo `min_texts` del canal | `panel.G_state` lleva el estado de G | el 5 de la firma no corre en el vivo |
| `force_w_pos` | `False` | firma; es **flag de desarrollo**, su comentario lo dice | **Sí**: `corpus_state.json` persiste `forced_w_pos`, y la W queda marcada en `causal_event` | — (el ejemplo de un default que **sí** declara que lo tocaron) |
| `rebuild_suspendido` | `False` (firma) / **True** en el vivo | `ckm_monitor.py:282`, con la razón escrita | **No directamente**; se infiere de los `causal_event` | el default de la firma es el contrario del que corre. Impacto: quien lea la firma lee el régimen equivocado |
| `should_rebuild(n=3)` | 3 | firma | `rebuild_state.json` lleva `d_ckm_history` y `ciclos_sin_rebuild` | la ventana de la condición no se declara como tal |
| `allow_first_W` | `True` | lo pasa `CKMMonitor` según sus condiciones (≥30 mensajes de ≥2 devices) | la causa del primer W sí (`causal_event: "rebuild"`, `causa: "bootstrap"`) | — |
| `REBUILD_EVERY` | 10 | `ckm_monitor.py:215` | **Sí**, en `causal_event: "rebuild_por_decision:volumen"` y en `corpus_size` | — |
| `MIN_DEVICES_FIRST_W` | 2 | `ckm_monitor.py:214` | en el log del caso | — |
| `MAX_CICLOS` | 10 | `ckm_monitor.py:148` | `panel.coco_generacion` cuenta los ciclos | el techo no viaja. Impacto: si se alcanzara, el corte se leería como el fin de los rebuilds |
| `CRITERIOS_POR_DEFAULT` | `(estructural, volumen, tiempo)` | `ckm_monitor.py:170`, `criterios_rebuild=None` → esa tupla | la causa del rebuild sí; **la lista de criterios activos, no** | no se distingue "corrió con los tres" de "corrió con uno y ése disparó" |
| `causal_event` (`w_version.register`) | `'rebuild'` | firma | **Sí**: `w_version_history[].causal_event` | — |
| `storage_path` (corpus, monitor, G) | `'corpus_state.json'`, `'monitor_trajectory.jsonl'`, `'corpus_G_state.json'` | `CKMMonitor` los arma con su `state_dir` | el log del caso lista `archivos_del_state_dir` | ver el `state_dir` abajo (**E1**) |

---

## 5. El canal y los devices

| parámetro | valor | (a) | (b) | (c) |
|---|---|---|---|---|
| **`state_dir` de `CKMMonitor`** 🔸 **E1** | `None` → `iap_chatroom/_state` (`ckm_monitor.py:142`) | `iap_chatroom/startup.py` guarda el pedido y **distingue "me pidieron el default" de "no me pidieron nada"** (`_was_requested`) | **Sólo en el stdout del server**: `server.py:56` imprime `state_dir = … (pedido por --state-dir)` o `(default)`. **No está en el panel ni en ningún `.jsonl`** | El docstring de `startup.py:43-47` dice *"el panel tiene que poder decir cuál de las dos fue"*, y hoy **el panel no lo dice**: el único consumidor de `declaracion()` es ese `print`. Impacto medido: el residuo de 2 líneas del 22 oct (P13) y la línea de tick que deja `--check` (P17). **Decisión de delamor, abierta** |
| `state_dir` de `AutonomousDevice` | `None` | firma; el caso se lo pasa | **Sí**: `costo().state_dir` en el `device_log` de cada device | el device **sí** lo declara; el monitor no. Dos mitades del mismo flujo con distinta visibilidad |
| `poll_interval` | 2.0 (firma) / **5.0** en el vivo | el caso se lo pasa | **Sí el valor** (`run_start.poll_interval_s = 5.0` y `ritmo_declarado`) — no si fue default | el 2.0 de la firma no corre en un vivo |
| `duration` (`run`) | 60.0 (firma) / **1200.0** en el vivo | el caso (`DURATION`), con tests que lo afirman | **Sí el valor**: `run_start.duration_s` | ídem |
| `trigger_mode` | `'continuo'` | firma; el caso lo pasa igual | **Sí**: `run_start.trigger_mode` y en cada decisión | — |
| `mcp_url` | `'http://localhost:7860/mcp'` | firma | **Sí**: `run_start.mcp_url` | el puerto está cableado también en `server.py:86` (abajo): **dos lugares con el 7860** |
| `local_criterion` | `None` | firma; el caso 0 no lo pasa | **Sí, y como ausencia**: `panel_criterio()` es `None` y `costo().local_criterion` es `None`, no un panel en cero | — (el otro ejemplo bien resuelto; con tests desde el 28 oct, texto 15 punto 3) |
| `LocalCriterionThresholds` | `dt_minimo_s=5.0`, `piso_vueltas=12`, `tasa_auditoria=0.1`, `tasa_auditoria_pase=0.1`, **`calibrado=False`** | `local_criterion.py:189` | **Sí**, los umbrales y el `calibrado: False` viajan en cada registro y en el panel | — (declara que no está calibrado, como COCO) |
| `VENTANA_GATE` / `VENTANA_GENERATE` | 4 / 10 | `autonomous_device.py:107,115` | **No** | cuántos mensajes ve el gate y cuántos la generación no viaja. Impacto: la decisión no es reconstruible desde la traza sin el código |
| `n_devices` (`ritmo_declarado`) | 1 | firma | **Sí**: el bloque `ritmo_declarado` del costo | el 1 es por device, y ya hubo una lectura de un agregado como si fuera por unidad (test del vivo 02). Está dicho en el propio bloque |
| `TICK_PERIODO_S` | 1.0 | `channel.py:37` | **Sí**: cada tick lleva `reloj: "channel"` y su `t`; el período lo trae el clock | — |
| `silence_sentinel` | `'OP_SILENCE'` | firma de `build_goal_directed_agent` y de `build_search_grounded_agent` | **No** como parámetro | es el centinela que el caso 0.13 mostró que se filtraba (REG). Hoy el skin no corre en el caso 0 |
| `search_results` | 3 | firma de `build_search_grounded_agent` | **No** | no corre en el caso 0 |
| `DEFAULT_CONFIG` (research agent) | `groq_model`, `max_iterations=8`, … | `groq_research_agent.py:84`, con `load_config(path=None)` | el agente escribe su propio resultado en `process/` | no corre en el caso 0 |

---

## 6. El server y los providers

| parámetro | valor | (a) | (b) | (c) |
|---|---|---|---|---|
| `port` | **7860**, literal en `server.py:86` | no es ni un default de función: es una constante en la llamada a `uvicorn.run` | **No**; aparece en el stdout de uvicorn (`Uvicorn running on http://0.0.0.0:7860`) | **P14 punto 2**: el puerto es una de las tres cosas que los drivers saben y IAP no declara. Está cableado en `server.py:86` y otra vez en el `mcp_url` del device. Impacto: dos lugares que pueden divergir, y ningún archivo de la corrida dice en qué puerto corrió |
| `host` | `"0.0.0.0"`, literal, ídem | no se declara | **No** | expone el puerto a toda interfaz; en un Codespace eso es lo que la sonda externa del intento 4 encontró (28 `Invalid HTTP request`, texto 15 punto 2) |
| `reload` | `False`, literal | — | **No** | — |
| `model` (anthropic) | `'claude-sonnet-5'` | firma | **Sí**: el device declara `provider` y `model` en `run_start` y en `costo()` | — |
| `model` (gemini) | `MODELO_POR_DEFAULT = 'gemini-2.5-flash'` | `gemini_provider.py:14` | ídem | el caso 0 pasa `gemini-3.5-flash-lite` explícito; el default del módulo **no es el que corre**, y es un modelo con cuota de 20/día medida |
| `model` (groq) | `'llama-3.3-70b-versatile'` | firma | ídem | quedó registrado en una sesión anterior que la cuenta de Groq **no sirve los modelos `llama`** — **no lo verifiqué hoy** (verificarlo gasta una llamada). Si sigue así, quien llame sin modelo falla, y el error es de provider y no de configuración |
| `model` (openai) | `'gpt-4o-mini'` | firma | ídem | no se usa en la serie 2 |
| `MAX_TOKENS_POR_DEFAULT` (groq) | 512 | `groq_provider.py:99`, con `MAX_TOKENS_POR_MODELO` por modelo | **No** el límite; **sí** el truncamiento, desde el arreglo de oct (los dos vivos 3 y 4 dieron 0 truncamientos) | es el parámetro que **ya causó** una divergencia silenciosa (casos 0.9/0.10 truncados sin aviso). Hoy el aviso existe; el valor sigue sin viajar |
| `MAX_OUTPUT_TOKENS` (gemini) | 4096 | `gemini_provider.py:19` | ídem | ídem |
| `REASONING_EFFORT_POR_MODELO` | `low` para dos modelos | `groq_provider.py:104` | **No** | dos devices del caso 0 corren con `reasoning_effort` bajo y la traza no lo dice |
| `api_key` | `None` → variable de entorno | firma de `Provider.__init__` | **No** (correcto: es un secreto) | la **key** no, pero **cuál** key / cuenta tampoco: el log dice `limite_de_la_cuenta: "UNKNOWN — se lee en la consola del provider"` |

---

## 7. Lo que el CP2 midió, y dónde más pasa

Medido en el CP2 (texto 11): **en la Config, un default y una declaración explícita del mismo valor
no se distinguen.** La pregunta del punto 4 es si pasa lo mismo en otros lugares. **Pasa en casi
todos**, y hay exactamente cuatro lugares donde no.

**Donde el valor viaja y el hecho de ser default NO viaja** (la mayoría): `sampling_mode`,
`poll_interval`, `duration`, `trigger_mode`, `mcp_url`, `top_k` y toda la declaración de extracción,
`grilla_lambda`, `representacion`, los umbrales de temperatura, el `n_runs` efectivo. En todos,
leyendo la traza se sabe **con qué valor corrió** y no se sabe **si alguien lo eligió**.

**Los cuatro lugares donde sí se distingue** — y son el patrón a mirar, porque los cuatro resuelven
lo mismo de cuatro maneras:

1. **`panel.coco.thresholds.source = "default"`** más `origen.<param>.source = "default de coco.py —
   no_calibrado:sin_separacion"` y `provenance: DECLARED`. El más completo: dice que es default, de
   qué archivo, y **por qué** (la calibración corrió y no separó).
2. **`calibrate_declarado.sin_declarar`** (lista, vacía en el intento 4). Declara **qué no se
   declaró**, en vez de declarar lo declarado. Es el único que nombra la ausencia como lista.
3. **`startup.was_requested()`** → `server.py:56` imprime `(pedido por --state-dir)` o `(default)`.
   Distingue las dos cosas y **se pierde**: va al stdout del server y no al panel ni a un `.jsonl`.
4. **`local_criterion = None`** → `panel_criterio()` es `None` y no un panel en cero. La ausencia
   como estado del observador, sin campo extra.

**Y uno que declara que lo tocaron**, que es el caso simétrico: `force_w_pos` queda en
`corpus_state.json` y marca la W en su `causal_event`.

---

## 8. Los seis defaults cuya firma dice un régimen distinto del que corre

No es una lista de errores: es una lista de lugares donde **leer el código y leer la corrida dan
distinto**, y por eso conviene que estén juntos.

| parámetro | la firma dice | el vivo corre | quién lo cambia |
|---|---|---|---|
| `COCO.n_runs` | 80 | 200 | `monitor_service.py:849` vía `sampling_for("coco")` |
| `CorpusService.min_texts` | 3 | 30 | `ckm_monitor.MIN_TEXTS_FIRST_W` |
| `BehaviorGraph.min_texts` | 5 | 30 | `ckm_monitor.py:293` |
| `CorpusService.rebuild_suspendido` | `False` | **`True`** | `ckm_monitor.py:282` |
| `AutonomousDevice.poll_interval` | 2.0 | 5.0 | el caso |
| `AutonomousDevice.run(duration)` | 60.0 | 1200.0 | el caso (`DURATION`) |

Y dos defaults de módulo que **no son el que corre**: `MODELO_POR_DEFAULT` de gemini
(`gemini-2.5-flash` contra el `gemini-3.5-flash-lite` del caso) y el modelo de groq
(`llama-3.3-70b-versatile`, que hoy no existe en la cuenta).

---

## 9. Qué no hace este inventario

- **No decide nada.** Ni el `state_dir` (E1), ni P14, ni qué default debería declararse. El texto 15
  lo pone en los NO y esto es su insumo.
- **No propone un mecanismo único.** Los cuatro lugares de §7 resuelven lo mismo de cuatro maneras;
  cuál es el patrón —si hay uno— es decisión de la TASK de defaults.
- **No mide impacto donde no lo midió nadie.** Donde la columna (c) dice "impacto", dice qué queda
  sin poder reconstruirse desde la traza; no afirma que haya cambiado un resultado, salvo en los dos
  casos donde está medido y registrado: el truncamiento de los casos 0.9/0.10 y los residuos de
  `state_dir` (P13, P17).
