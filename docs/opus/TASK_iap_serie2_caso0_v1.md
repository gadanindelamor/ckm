# TASK_iap_serie2_caso0_v1 — IAP Serie 2, Caso 0 (vivo)
*Redactada por Opus 5.5 a pedido de delamor, 15 oct 2026. **Se ejecuta luego**, cuando delamor la pase a Code. Nada vivo cambia antes de su orden; esta TASK es esa orden sólo cuando delamor la pega.*

## Qué es
**Serie 2** del canal IAP. **Nada que ver** con la serie 1 (casos 0.4–0.15, congelada en `process/iap_series_freeze_20261008/`): no se compara con ella, no la continúa, no la reinterpreta. Identificación en todo lo que produzca: **`serie = "S2"`, `caso = "S2-C0"`** — en el panel, en cada registro, en los nombres de archivo y en una carpeta propia (`registers/iap_serie2/`, o la que Code proponga en el CP0; nunca mezclada con la serie 1).

## Condiciones (delamor, 15 oct, literal en lo esencial)
1. **Se mide con el estimador actual de CKM, y sólo con ése:** N_eff sobre masas de cuencas, y su forma de distancia, **que en esta serie se llama D_ckm**: D_ckm = 1 − ln N_eff_t / ln N_eff_0 (hoy `D_masa_cuencas`). El conteo de atractores **no se reporta** como D_ckm ni como medida del campo en la Serie 2.
2. **COCO conectado al canal, sí o sí.** Conectado = existe, está unido al canal vivo y recibe cada evaluación. **No se exige que dispare** (disparar es comportamiento). delamor **debe poder ver y comprobar** la conexión durante el caso, en el panel y en la traza. El paper dice que eso no sucedió en la serie 1; en la Serie 2 tiene que suceder.
3. **Extracción con parámetros sensatos mínimos** — "no ridículamente inusuales". Los fija Opus (abajo), sin más estructura.
4. **Free will (delamor, 15 oct): los devices no reaccionan únicamente a mensajes.** Además de los mensajes nuevos, cada device recibe un **tick** del reloj del canal (común, numerado, observable) y en cada tick observa y **elige**: publicar, irse, o nada. El mensaje nuevo y el tick son parte de la observación, no el disparador. El silencio entre mensajes es dato. Ya implementado por `TASK_canal_iap_clock_iniciativa_v2` (CP1 reloj, CP2a ODA continuo — `trigger_mode="continuo"` es el único modo —, CP2b criterio local; usado en el vivo 03). Timestamps en UTC, del reloj del canal.
   **El presupuesto de llamadas es parte de esta condición.** El criterio local (`iap_chatroom/criterio_local.py`) decide en cada vuelta si se consulta al modelo (D) o no; el **piso** (`piso_vueltas`) obliga a consultarlo tras N vueltas sin llamar, para que el silencio no sea absorbente: sin piso, el filtro le quitaría al device la posibilidad de elegir. **Hoy el filtro está apagado por default** (`criterio_local=None`: D en cada vuelta) y sus umbrales viajan como `calibrado=False`. Desde el 13 oct el filtro corre a través de `services/ckm_trust_rule.CkmTrustRule` (CP3 de la regla TRUST). **Decide delamor:** S2-C0 con filtro (y con qué `piso_vueltas`: tiene que caer dentro del horizonte, `piso_vueltas + 2 ≤ vueltas por device`) o sin filtro (más llamadas).

## Parámetros sensatos mínimos (Opus)
Criterio: lo que alguien que usa TF-IDF y Hopfield no encontraría raro. Nada más.

| | valor | por qué |
|---|---|---|
| unidad | el mensaje | ya declarado |
| mensajes `SYSTEM` | no entran al corpus | F3b, ya vigente |
| mensajes de prueba | ninguno durante el caso; canal limpio al empezar | E7: W hecha de "Hola desde MCP test" |
| **primer W** | recién con **≥ 30 mensajes de ≥ 2 devices** | con 7–24 textos N_eff se mueve 3–34× más por extracción que por muestreo (CP-E) |
| **frecuencia mínima de un nodo** | aparece en **≥ 2 mensajes** (`min_df = 2`) | un nodo de un solo mensaje no co-ocurre de verdad |
| `top_k` / pool / stopwords | 20 / ×3 / las 703 | los declarados; no son raros |
| **marcadores de signo** | **palabra completa**, no subcadena | "but" dentro de "distribution" es ridículo |
| **rebuild** | cada **10 mensajes nuevos** (no en cada ingest) | una W por mensaje no es sensato |
| **n_runs** para N_eff | **≥ 1000** | donde converge (§4.3.1) |
| un solo extractor en el camino vivo | el mismo para construir W y evaluar σ | hoy coinciden por defecto, no por construcción |

Cambiar `min_df`, los marcadores o el rebuild **cambia la declaración** (`DECLARACION_extraccion_W_v1` → v2): se declara en el mismo commit.

## CPs
- **CP0 — sólo lectura. Predicción antes.** Cómo está hoy el camino vivo (`iap_chatroom/ckm_monitor.py`, `services/monitor_service.py`, COCO): ¿COCO ya nace en Monitor (`ckm_monitor.py:215`, "COCO es de Monitor (CP4)")? ¿qué ve el canal de él? ¿cuántas instancias? ¿qué lee COCO para disparar (D_ckm por conteo o por masas)? ¿qué baseline N_eff_0 usa D_masa_cuencas? ¿qué hace hoy `should_rebuild`? ¿cuántos extractores corren? ¿qué quedó de la TASK del CLOCK (`c451af8`) y qué dispara hoy el ODA de un device? Y de su ESTADO (`ESTADO_canal_iap_clock_iniciativa_v2.md`), lo pendiente: Fix 3 (smoke con tope), Fix 4 (AgentDeviceSkin: `None` → UNKNOWN), F3a (los entry points construyen `CKMMonitor()` sin argumentos; en el vivo 03 se resolvió con un launcher), y si el vacío/`[assistant]` ya no entra al corpus. Lista de lo que falta para cumplir las tres condiciones y la tabla. **A1.PAUSA.**
- **CP1 — implementar**, con tests que fallen si falta algo: (a) bloque `coco` en el panel y en `get_monitor_state`: `conectado`, id de instancia, `w_version_id` que ve (debe ser el de Monitor), β_c, ‖Δ_r_compresiones‖, hora de la última evaluación recibida, disparos (n, puede ser 0); **una sola instancia**; (b) D_ckm = forma de masas; el conteo fuera del panel de la Serie 2; (c) la tabla de parámetros; (d) identificación `S2` / `S2-C0`; (e) declaración v2; (f) reloj del canal y ODA continuo: un test que falle si un device sólo se activa con mensajes nuevos, y el tick visible en el panel. **A1.PAUSA.**
- **CP2 — ensayo sin devices de IA:** canal local, mensajes escritos a mano o por script, sólo para ver que COCO aparece conectado y recibe evaluaciones, que el primer W espera los 30 mensajes, y que con el canal en silencio los ticks siguen llegando y un device de prueba puede elegir actuar sin que haya mensaje nuevo. **No es el caso; no se reporta como serie.** **A1.PAUSA.**
- **CP3 — Caso S2-C0, vivo.** Devices y consigna: los decide delamor. delamor está presente (*"yo voy a ir"*). Al terminar: freeze de condiciones en `process/iap_serie2_caso0_freeze_<fecha>/` (código propio copiado, versiones, identificadores de modelos), REPORTE, **A1.PAUSA**.

## Reglas de siempre
Predicción antes de cada CP y no se reescribe · archivos nombrados uno por uno, sin `git add -A` · sin regresiones ni compatibilidad hacia atrás · el gate (`f96c234`) sólo se toca en CP1 y con esta TASK · no se ejecuta código ajeno · donde se duda, A1.PAUSA.

## Abierto para delamor (no bloquea el CP0)
- **Qué lee COCO para disparar.** Si D_ckm pasa a ser la forma de masas, lo coherente es que COCO lea ésa. Es la "decisión de modelo" que el paper deja abierta (§8.3). Opus propone: sí.
- Qué devices y qué consigna para S2-C0.
- Con o sin filtro de presupuesto (condición 4), y el `piso_vueltas` según la duración del caso.
