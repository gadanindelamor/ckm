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
