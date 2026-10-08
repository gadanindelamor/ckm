# DECISIONES_opus

*Decisiones que Opus toma por debajo del umbral (`PROTOCOLO_code_continuidad_v1.md` §5). delamor puede revertir cualquiera.*
*Formato: fecha · qué · por qué · cómo revertir.*

---

- **2026-10-07** · La Config v3 mantiene una clase `CKMlandscapeConfigV1` renombrada hasta el CP3, en lugar de borrarla en el CP1 · así los consumidores no se rompen mientras se migra · revertir: borrarla en el CP1.
- **2026-10-07** · El laboratorio de W quedó en `docs/lab/laboratorio_w.html` · era una carpeta nueva y no había convención · revertir: mover el archivo antes del commit.

### Sobre el ARRANQUE y el REPORTE CP0 de Code (BANDEJA, 2026-10-07 03:54 UTC)

- **2026-10-07** · **CP0 de Config v3: aceptado.** Los cuatro puntos están completos y las correcciones que hizo en el camino quedaron declaradas · revertir: pedir que se rehaga el punto que se quiera.
- **2026-10-07** · **Concurrencia: va un lock y no se escala.** Hay un lector en un hilo (`gr.Timer` → `get_state`) y un escritor en el event loop, en el mismo proceso. Es la primera rama de la TASK §2. El lock cubre el reemplazo de `ciclo_vigente` y la lectura que arma el panel · revertir: sacar el lock (no se recomienda).
- **2026-10-07** · **P1 (`theta_W_formula`): se acepta el default.** Pasa a la clase nueva sin cambios. Es una función pura que no define nada nuevo · revertir: borrarla y ajustar los dos asserts.
- **2026-10-07** · **P2 (`gatekeeper_c1.py`): se acepta el default.** En el CP3 no se toca, salvo el docstring si `theta_W_formula` se mueve · revertir: trivial.
- **2026-10-07** · **P4 (lectura de los registros planos de v1): se acepta el default.** Es una función de lectura plano → (identidad, declarado, ciclo único `bootstrap`, `t_señal=None`, `t_rebuild=timestamp`) y no reescribe nada histórico · revertir: borrar la función.
- **2026-10-07** · **§2.5 del protocolo (tests en el arranque): de ahora en más se corren.** Correr tests no cambia código, así que entra en el chequeo aunque el CP sea de lectura. Esta vez no se corrieron y quedó declarado en "no pude revisar", que era lo correcto · revertir: volver a solo leerlos.
- **2026-10-07** · **CP1: puede arrancar.** P3 bloquea el CP2, no el CP1 · revertir: frenar el CP1 hasta que se responda P3.
- **P3: escalada a delamor** (E3/E4: qué instrumenta el canal vivo y con qué θ_W). Pendiente.

### P3 — respuesta de delamor (2026-10-07)

- delamor: *"θ_W no se usa"* · *"es para Gatekeeper"*. Verificado: en `services/` e `iap_chatroom/` θ_W solo aparece en `gatekeeper_c1.py`. Monitor, COCO y el canal no lo leen. `scale` tampoco lo usa nadie fuera de la UI de Gradio.
- **Lectura que registra Opus:** θ_W es **del Gatekeeper** (W estática), no del landscape. La Config no lo exige. El que lo necesita lo recibe como parámetro, que es lo que `c1()` ya hace hoy.
- **P3 desbloqueada, opción (iv):** `CKMMonitor` construye la Config con **lo medido, los ciclos y el `sampling_mode`** que Monitor ya usa. θ_W y `scale` **no aplican** en este dominio y no se exigen. Monitor abre los ciclos en el canal (D4).
- **Efecto sobre la v2:** I4 pasa a decir *"lo declarado se exige según quién lo usa, no siempre"*. **Pendiente de confirmar por delamor:** si θ_W **sale** de la Config (y pasa a ser un parámetro solo del Gatekeeper) o queda como campo opcional. Mientras tanto, en el CP1 queda **opcional**, que es reversible.
- **delamor (2026-10-07): "sí", a la pregunta de si θ_W sale de la Config.** Opus lo interpreta como que **θ_W sale**: deja de ser campo de la Config y pasa a ser solo parámetro del Gatekeeper (`c1(..., theta_W=)`). `theta_W_formula` acompaña a θ_W y se va del lado del Gatekeeper (corrige el default de P1). En el CP1, la clase nueva ya no tiene θ_W. Los registros históricos de v1 que lo tienen se leen igual, como dato histórico. · revertir: volver a θ_W como campo opcional.

### Sobre el REPORTE CP1 de Code (BANDEJA, 2026-10-07 04:09 UTC, `8391319` en `code/trabajo`)

- **2026-10-07** · **CP1 de Config v3: aceptado.** 31/31 tests nuevos y la suite completa en 214/214. Code corrigió en el camino una afirmación propia ("lo probé sin lock" sin haberlo probado): lo midió antes de commitear y lo declaró · revertir: n/a.
- **2026-10-07** · **Tests de hilos.** `test_D3_el_get_nunca_devuelve_un_ciclo_mezclado` **es** la verificación del lock: falla 3 de 3 sin lock. `test_D3_el_panel_no_se_parte…` queda, pero **no cuenta** como verificación del lock, porque compara claves y no valores. Code lo dijo así y se acepta así · revertir: n/a.
- **2026-10-07** · **Redirigir a `CKMlandscapeConfigV1`** cuatro tests y `experiments/replay_sesion_trust.py`: aceptado. Cambia solo el nombre de la clase, no la lógica, y es transitorio hasta el CP3 · revertir: volver el nombre.
- **2026-10-07** · **`conteo_vs_masa.py` no se toca**, aunque se rompería si se volviera a correr. Es un experimento ya corrido: su traza se lee con `ciclo_desde_registro_plano_v1`, y las condiciones de aquella corrida no se reproducen · revertir: n/a.
- **2026-10-07** · **P5 (`nodes` fuera del `Ciclo`): se acepta el default.** Code tiene razón: `nodes` no es función de W y la v2 se contradecía. Se verificó que **no cambia la semántica actual**: `MonitorService._invalidar_si_W_cambio` también decide solo por el sha de W (L270–273), y "nodos" es solo la explicación de la causa cuando el sha cambió. Así que Monitor y la Config coinciden en qué es un ciclo. **Observación (no se escala):** con estos criterios, una W con los mismos valores y otras etiquetas sería el mismo ciclo, tanto para Monitor como para la Config. Si eso importa, es una pregunta sobre qué es W, no sobre la Config · revertir: meter `nodes` en `abrir_ciclo` y reescribir I5.
- **2026-10-07** · **P6 (`t_senal`): se acepta.** Todos los identificadores de `services/` son ASCII. El concepto se sigue llamando t_señal en los documentos · revertir: renombrar campo y clave (todavía no hay JSON escrito con esa clave).
- **2026-10-07** · **CRLF en la bandeja:** se mantiene como lo hizo Code. Lo genera el git de Windows del clon local · revertir: n/a.
- **2026-10-07** · **CP2 habilitado.** P3 ya está resuelta (opción iv). El CP2 incluye que `CKMMonitor` construya la Config sin θ_W ni scale y que Monitor llame a `abrir_ciclo` en `_invalidar_si_W_cambio` · revertir: frenar el CP2.

### Sobre el REPORTE CP2 de Code (BANDEJA, 2026-10-07 04:34 UTC, `17b6421` en `code/trabajo`)

- **2026-10-07** · **CP2 de Config v3: aceptado.** Pasan 227 de 227. Sin el CP2, fallan 12 de los 13 tests nuevos; el que pasa es el control sin config. Code encontró dos tests que pasaban por la razón equivocada y los corrigió después de medirlos · revertir: n/a.
- **2026-10-07** · **P7 (`"W_distinta"`): se acepta el default.** **Error de Opus:** al aceptar P5 no vi que, sin `nodes` en el ciclo, la causa no siempre se puede derivar. `"W_distinta"` dice "no sé más que esto" y no inventa una causa. El camino normal no se ve afectado, porque Monitor usa su `_w_nodes` · revertir: guardar `nodes` en el Ciclo (revierte P5) o persistir los nodos por versión en CorpusService (otra TASK).
- **2026-10-07** · **Migración de `test_landscape_config_en_runs.py`: aceptada.** Sigue verificando lo mismo: cada línea lleva la config que produjo ese panel. Lo único que cambió es que la historia ya no viaja (I7) · revertir: n/a.
- **2026-10-07** · **El canal vivo tiene un solo ciclo (`rebuild_suspendido=True`): no se toca.** Es decisión de delamor y no se escala: es el estado conocido de W, que hoy o se reconstruye en cada ingest o no se reconstruye nunca, sin mesetas · revertir: n/a.
- **2026-10-07** · **Criterio para el CP3 sobre lo que todavía apunta a `CKMlandscapeConfigV1`:**
  - **Los tests que prueban V1 en sí** (`test_ckm_landscape_config.py`) **se van con V1**, siempre que lo que cubren ya esté en `test_ckm_landscape_config_ciclos.py`: valores medidos, serialización, β_c contra COCO. Si algo no está cubierto, se migra antes de borrar.
  - **Los que usan V1 solo como herramienta** (`test_gatekeeper_c1.py`, `test_rebuild_consulta_w_version.py`) **migran** a `medido(W)` o a `CKMlandscapeConfig.create`.
  - **`experiments/replay_sesion_trust.py`** migra a la clase nueva y deja de imprimir θ_W.
  - **`conteo_vs_masa.py`** no se toca (P1P4, ya corrido).
  - `theta_W_formula` sale con V1. Si `gatekeeper_c1.py` la nombra en el docstring, se actualiza la referencia.
  - · revertir: dejar V1 hasta otra TASK.
- **2026-10-07** · **CP3 habilitado.**

### Sobre el ARRANQUE y el CORTE de Code (BANDEJA, 2026-10-08 00:13 UTC, `079df6c` en `code/trabajo`)

- **2026-10-08** · **ARRANQUE: aceptado.** Primer arranque con la §8: lista P1–P7 con su respuesta y no hay ningún default vigente sin decisión. Es la primera vez que la tríada se verifica desde la bandeja y no desde el chat · revertir: n/a.
- **2026-10-08** · **Matiz en "No pude revisar: nada".** Hubo algo que no se podía revisar: **lo que la sesión anterior hizo y dejó solo en el chat**, que el mismo CORTE (punto 1) señala. Va en esa lista. "Nada" se acerca al OK que tapa el no sé. Para los próximos arranques: si de verdad no queda nada, se dice qué cosas están fuera del alcance del chequeo (el chat, el estado del Codespace fuera de git) · revertir: n/a.
- **2026-10-08** · **CORTE: aceptado tal cual.** El reporte en el chat no es canal, el Codespace paró sin daño y el merge `c96f752` se hizo a tiempo. "El ARRANQUE va a la bandeja antes de tocar el CP3, con su propio commit": queda como práctica · revertir: n/a.
- **2026-10-08** · **CHANGELOG bajo `Unreleased` (adelantado por chat; se confirma cuando llegue como Pn):** aceptado. El número de versión lo pone delamor cuando publique. El CHANGELOG (v30) y los informes (v32) son numeraciones distintas · revertir: asignar un número.

### Sobre el REPORTE CP3 de Code (BANDEJA, 2026-10-08 00:18 UTC, `44af68a`) — **TASK_CKMlandscapeConfig_v3 CERRADA**

- **2026-10-08** · **CP3: aceptado. La TASK queda cerrada.** Pasan 220 de 220 (227 − 9 + 2). Antes de borrar se verificó la cobertura: había dos casos que se habrían perdido (`test_identidades` y `test_w_version_id_cambia_con_W`), y se migraron. `CKMlandscapeConfigV1` ya no aparece en el código · revertir: restaurar V1 desde git.
- **2026-10-08** · **Docstring de `gatekeeper_c1.py`: se acepta que fue más allá de "actualizar la referencia".** Se verificó la fuente: la propiedad ("al menos el núcleo A pasa C1") **no es nueva**. Viene del docstring de `theta_W_formula` (`TASK_CKMlandscapeConfig_v1` L19 y L36, PROPUESTA v4 D1), y el docstring la cita. Si solo se hubiera corregido la referencia, se habría perdido el único lugar del código que dice que θ_W no tiene fórmula · revertir: dejar solo la referencia.
- **2026-10-08** · **`replay_sesion_trust.py` no se ejecutó**, porque sus datos están en `_private/` y no viven en el repo. Solo se verificó la sintaxis, y quedó declarado. Se acepta así · revertir: n/a.
- **2026-10-08** · **P8 (CHANGELOG bajo `## Unreleased`, en inglés): aceptada.** El número de versión lo pone delamor cuando publique · revertir: cambiar el encabezado.
- **2026-10-08** · **Práctica para Code y para Opus: nunca `git add -A` ni `git commit -a`. Se nombran los archivos.** Code lo declaró como reflejo repetido (`run_tests.sh` dos veces), y Opus tuvo el mismo con `commit -a` (CRLF, 3961fc0). Es el mismo mecanismo en las dos instancias · revertir: n/a.
- **2026-10-08** · **Lo próximo del plan: `TASK_monitor_coco_ciclo_orbita_v1`.** Se escribió antes de la Config v3. Antes de ejecutarla, Opus la ajusta para que COCO renazca **con el ciclo que abre Monitor** (`abrir_ciclo`), en lugar del bloque de `_invalidar_si_W_cambio` sin Config. Pendiente: v2 de esa TASK.

### Una sola rama (delamor, 2026-10-08)

- **delamor:** *"Sí, es sí, toda la razón. El tema son los merges."* Respuesta a la propuesta de Opus de usar una sola rama. **Decisión de delamor (E1: reemplaza a la §6 (b)).** Todos trabajan en `main` con `git pull --rebase origin main`. `code/trabajo` queda congelada como traza en `2195025`. Detalle en PROTOCOLO §6 · revertir: volver a la §6 (b).
- **delamor (2026-10-08): "Hay que eliminar la branch trabajo… y fin del cortocircuito."** Antes de borrarla, Opus verificó con `git diff origin/main origin/code/trabajo` que no tenía contenido propio: solo le faltaban cosas que ya estaban en `main`. La rama se elimina en el remoto y en los clones · revertir: recrearla desde `2195025` si sigue en algún reflog.

### Sobre el REPORTE CP0 de Monitor + COCO v2 (BANDEJA, 2026-10-08 01:46 UTC, `27c6559`)

- **2026-10-08** · **CP0: aceptado.** Corrige a la TASK en tres cosas, y se aceptan las tres:
  - los usos vivos de una sola fase son `monitor_service.py:168` (de donde salen `rejected`, `Δ_r_pares`, `c_S` y `fabrication_index`) y `mean_cS`, que COCO usa para comprimir. **N_eff y D_ckm ya van por órbita**, así que la paridad no afecta a D_ckm;
  - el borde de `landscape_engine:418` no está vivo (es `deprecated_d_ckm`);
  - la identidad `relax(−σ) = −relax(σ)` queda demostrada, y la bisagra es la regla GOLES (h=0 conserva σ).

  · revertir: n/a.
- **2026-10-08** · **Los 21 `test_caso_*` del canal no son tests de pytest** (recogen 0 items): no están en los 220, y un cambio los puede romper sin que la suite lo diga. **Se acepta como punto ciego declarado y no se convierten.** Son la serie IAP congelada (TASK canal IAP, CP0b): no se reproducen ni se usan para validar. Cada reporte que toque el canal tiene que nombrarlo en "no pude revisar" · revertir: convertirlos (otra TASK).
- **2026-10-08** · **Práctica de la hora:** cada encabezado de la bandeja se escribe con `date -u` en el momento, nunca de memoria. Code ya la corrigió con una entrada propia (`7c16b6c`) · revertir: n/a.
- **2026-10-08** · **CP1 habilitado.** P9 bloquea el CP2, no el CP1.
- **P9 — escalada a delamor (E3: cambia lo que el instrumento mide).** Pendiente. Recomendación de Opus abajo, a confirmar.
- **Nota técnica de Opus:** la VM vio el ESTADO como "modificado" y era solo CRLF. Desde ahora, en la VM se usa `git -c core.autocrlf=true`, igual que el git de Windows.

### Sobre el REPORTE CP1 de Monitor + COCO v2 (`045005b`)

- **2026-10-08** · **CP1: aceptado.** Se midieron dos cosas, cada una con su pre-registro:
  - **A, la paridad:** pesa. caso09 da 16 de 24 en período 2 y L1 = 24.0. La expectativa de Code, escrita antes de correr, estaba equivocada y lo declaró;
  - **B, las dos existencias:** **rompen** (`ValueError` (31,31) contra (28,28) en `coco.py:254`) cuando cambia N. No aparece en el canal vivo (`rebuild_suspendido=True`), pero sí en cualquier driver con rebuild.

  · revertir: n/a.
- **2026-10-08** · **Se acepta la corrección a la §1 de la TASK:** la invariante "punto fijo ⇒ R_A = R_B" vale **a igual W_eff**, no a lo largo de un recorrido (la divergencia se compone porque Δ_r entra a W_eff). En el CP2 se testea sobre **una** evaluación · revertir: n/a.
- **2026-10-08** · **P9 sigue escalada a delamor y ahora pesa más:** el CP2 es donde deja de romperse. **CP2 bloqueado hasta que delamor responda la P9.**

### P9 — respuesta de delamor (2026-10-08)

- **delamor: "n 1000".** **Monitor y COCO miden con `n_runs = 1000`**, un solo valor para los dos, que es donde N_eff converge (±2 % respecto de 5000). Decisión de delamor (E3).
- **El resto de la P9 lo resuelve Opus por debajo del umbral, como default declarado y reversible** (delamor confirmó solo el `n_runs`):
  - **`n_runs` y `seed` son uno solo para Monitor y COCO, declarados en la Config** como *declarado*. COCO ya no tiene un default propio. La seed por defecto la elige Code en el CP2, la declara y la reporta (es el primer Pn del CP2 si hace falta);
  - **umbrales de COCO** (`d_ckm_threshold`, `alpha_star`, `frac_rec_min`): **no van a la Config**. Son de Calibración (D6 de la Config v3). Hasta que exista ese proceso, quedan como están y marcados "no recalibrados";
  - **`track_landscape`, `n_warmup` y `gamma`**: quedan en la configuración de COCO, declarados y fuera de la Config.

  · revertir: subir cualquiera a la Config o bajarla.
- **CP2 habilitado.**

### Sobre el ARRANQUE/CORTE (15:51) y los REPORTES CP2a, CP2b y CP2c (`8bdb4f5`, `999ca58`, `57f8a88`) — **CP2 cerrado**

- **2026-10-08** · **ARRANQUE y CORTE: aceptados.** El CP2 no llegó a empezar, y está verificado. El tecleo accidental (`detad`) en una entrada vieja de la bandeja se restauró y quedó declarado. Las seis salidas `armstrong_*` de origen desconocido quedan como UNKNOWN hasta que delamor diga si son suyas · revertir: n/a.
- **2026-10-08** · **CP2a, CP2b y CP2c: aceptados. El CP2 está cerrado.** Agregó 47 tests nuevos y la suite queda en 267/267. El `ValueError` dejó de romper. El vacío pasa a UNKNOWN, y se verificó al revés: devolviendo "stable", fallan 4 tests. La órbita entra al panel (`periodo_orbita`, `n_aceptados`, `n_expulsados`, `n_torsion` y `pares_torsion`, sin promediar). **Δ_r_pares no cambió**: eso es el CP3 · revertir: n/a.
- **2026-10-08** · **El test cambiado `test_D_ckm_None_is_stable` → `…_is_UNKNOWN_not_stable`: aceptado.** Era el test que sostenía el NOMINAL por ausencia · revertir: n/a.
- **2026-10-08** · **Punto ciego ampliado:** el CP2 cambió la firma de `MonitorService` (agregó `coco_config`) y le sumó claves al panel. Los 21 `test_caso_*` no se verifican. Se acepta, con la misma declaración que antes.
- **CP3: es de delamor (4 decisiones).** Opus las escala con una recomendación.

### CP3 — respuestas de delamor (2026-10-08)

- **delamor: "confirmo las opciones recomendadas"** para los puntos 1, 3 y 4 (E4):
  - **1, opción (a):** a `Δ_r_pares` y W_eff entran **solo los expulsados** (pares expulsados en las dos fases). La torsión va a un objeto propio (`Δ_r_torsion`), que escribe solo Monitor y que **no entra a W_eff**;
  - **3:** el baseline de COCO se fija **al nacer el ciclo** (Δ_r en cero, así que W_eff = W), con `n_runs = 1000`;
  - **4:** si el salto cae en período 2, el ciclo nuevo **nace con la órbita**, no con una fase.
- **Punto 2 (`landscape_history` a través del salto): pendiente.** delamor no lo entendió como estaba escrito. Opus lo reformula en el chat.

- **Punto 2 — delamor: "b"** (2026-10-08, E4). Cuando cambia W, el COCO nuevo **empieza con `landscape_history` vacío**: no hereda la historia del ciclo anterior, porque se midió sobre otra W y no es comparable. El pasado queda **solo en la traza** (JSONL), así que no se pierde nada.
  - **Traza del cambio de recomendación:** Opus primero recomendó (a), conservar la historia como registro de solo lectura. Al reformularlo, cambió a (b) porque (a) invita a mezclar mediciones de W distintas. delamor eligió (b) con esa explicación delante.
- **CP3 completo (1a, 2b, 3, 4).** Code sigue con el CP4 e implementa estas decisiones.

- **2026-10-08** · **Code propone partir en dos: CP3i (implementar las decisiones del CP3) y CP4. Aceptado** (Opus, dentro del umbral). Cada pieza se cierra con un REPORTE en la BANDEJA. El CP3i tiene que mostrar con tests: la torsión no entra a W_eff; `landscape_history` nace vacío al cambiar W; Δ_r = 0 al nacer el ciclo; nacimiento con órbita en período 2. Si se corta entre piezas, el ESTADO dice cuál falta · revertir: n/a.

- **2026-10-08** · **NodeExtractor — delamor: "bloque propio"** (E4). El criterio de extracción **no va dentro de CKMlandscapeConfig**. Va en un bloque propio (`NodeExtractorConfig`) con su propia sección en el JSON. La extracción ocurre antes de que exista W, así que no se mezcla con la configuración del paisaje. Se escribe al hacer la ficha de NodeExtractor o la Calibración · revertir: mover la sección a la Config.

- **2026-10-08** · **CP3i aceptado** (`ef1bc33`, 276/276). Las cinco inversiones rompen, y la salida literal está en la BANDEJA. La W sintética de 4 nodos está declarada y su órbita sale de `relax_orbit`. Dos tests que no podían fallar aparecieron al invertir, no al leer · revertir: n/a.
- **2026-10-08** · **El punto ciego crece.** El CP3i cambió qué entra a Δ_r, y los 21 `test_caso_*` y los Armstrong no se verifican. **Para el CP4**, como toca `ckm_monitor.py`, Code corre al menos un `test_caso_*` de punta a punta en el canal y reporta qué pasó, sin interpretar los números. La corrida larga de caso09 (16 de 24 textos con período 2) va a Calibración y deja `n_torsion` en la traza.
- **2026-10-08** · **delamor:** token fine-grained para el push de Opus: ok, lo crea él. `armstrong_*`: no lo revisó; queda UNKNOWN.

- **2026-10-08** · **CP4 aceptado** (`1e8d267`, 284/284, tres inversiones que rompen). **TASK_monitor_coco_ciclo_orbita_v2: CERRADA.** El canal se corrió por su camino real (ChatChannel → callback de CKMMonitor), sin errores y con las claves nuevas en el panel y en el JSONL · revertir: n/a.
- **2026-10-08** · **P10, `_last_landscape_signal` (Opus, dentro del umbral):** se escribe y nadie lo lee. **Se queda por ahora**, porque no molesta y borrarlo no aporta. Se saca la próxima vez que alguien toque `corpus_service.py` por otro motivo, con la misma búsqueda previa. El parámetro `monitor_jsonl_path` sigue el mismo criterio.
- **2026-10-08** · **`test_armstrong_via_corpus_v3.py:34`** (`assert corpus.coco is not None`) **queda roto por el CP4, y se sabe.** No se arregla ahora: va junto con la revisión de `armstrong_*` que hace delamor (UNKNOWN). Si se reactiva, tiene que leer el COCO de Monitor.
- **2026-10-08** · **Punto ciego de los `test_caso_*`:** necesitan claves de provider, que no están en el Codespace. Queda declarado. Correrlos con claves es decisión de delamor, sin apuro.
- **2026-10-08** · **TASK_canal_iap_clock_iniciativa_v2** (Opus, dentro del umbral: verificar una TASK contra el repo antes de pasarla a Code). La v1 se había verificado en `eddb4b0`; desde entonces cambiaron `ckm_landscape_config.py`, `monitor_service.py` y `ckm_monitor.py`. La v2 reescribe §0.4 (la Config ya es fuente de `n_runs`/`seed` y lleva `Ciclo`), agrega §0.6 (`t_senal`/`t_rebuild` se sellan con `time.time()` del proceso de Monitor, no con el reloj del canal: dos fuentes de tiempo si el CLOCK vive en la Config), amplía el punto 2 del CP0 y corrige la referencia de §3. Lo dictado por delamor no se tocó. Siguiente: CP0 de Code · revertir: volver a la v1.
- **2026-10-08** · **CHECKPOINT DEFS v15 — delamor (E1: orden del plan).** Se actualizan las DEFS (la última es la v14, `docs/defs/`, 23 sep; no hay v15 en ningún lado) **antes de continuar el plan**, que no cambia. Razón (delamor): *validar integridad y evaluar el todo contra las próximas tareas del plan*. ¿Por qué ahora? *Se avanzó lo suficiente, es un punto entre dos tareas y el estado es consistente.* Ubicación: `docs/defs/` (delamor), con la tensión pública/privada del 5 oct todavía abierta. El canal IAP v2 (`c451af8`) espera · revertir: retomar el plan en el CP0 del canal IAP.
- **2026-10-08** · **DEFS v15, pregunta 1 — delamor: "numeración se conserva"** (E1). La v15 conserva §0–§20 de la v14; solo se re-titulan las Partes. Las citas "DEFS §n" de los REG siguen apuntando a algo · revertir: reorganizar por Orden BABEL.
- **2026-10-08** · **Error de Opus, registrado como suyo: "expulsado" volvió por la TASK.** Genealogía: `6d563fd` (28 may) docstring *"relax expulsó"*; DEFS v11 *"Δ_r pair-level es metabolización, no rechazo ni expulsión (nombres en código sin tocar)"*; `88c1513` (18 sep) *"quedan adentro, como deformación en W_eff — no se expulsan"*. El 7 oct (`bd7fbb8`) Opus nombró **expulsado** a la categoría R_A ∧ R_B de la TASK Monitor+COCO, sin leer la v11. Code lo implementó (`pares_por_orbita`, `n_expulsados`, CP2a/CP2c). Hoy `monitor_service.py` dice en L10 *"no se expulsan"* y en L223 *"entran sólo los expulsados"*. Babel. **No se toca el código ahora:** va a la tabla de nombres de la v15 y la decisión de renombrar queda para delamor · revertir: n/a.
- **2026-10-08** · **DEFS v15 escrita (DRAFT), para que delamor la lea entera** — `docs/defs/DEFS_CKM_estado_actual_v15.md`. delamor: P1–P4 *"redactalo, incluilo en la v15, y lo leo todo junto"*; *"tener presente Newton"*. Conserva §0–§20; agrega §N (nombres: metabolizar = rechazar y absorber, delamor). §5 reescrita: P1 y P4 no testeables sobre W snapshot no negativa; conciliación con el 4 oct como **lectura de Opus**, espera la de delamor; la tabla de la v14 queda citada entera. Quedan marcadas [delamor] 19 decisiones abiertas, entre ellas §0 (dominio) · revertir: borrar la v15; la v14 no se tocó.
