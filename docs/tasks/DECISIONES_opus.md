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
