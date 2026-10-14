# Revisión de TASKs y CPs con el marco del 14 oct
*Opus 5.5 (Cowork), a pedido de delamor: "revisás las tareas y los CP y su sentido y utilidad con este marco; reformularlas luego de evaluar, o continuar con o sin ajuste si así la evaluación lo indica". Leído en la PC (sólo lectura, `fb2b87a`): `docs/tasks/TASK_*.md` abiertos, `ESTADO_*`, BANDEJA (reportes), lista de `tests/`. Es **propuesta**: cada cierre, pausa o reformulación la confirma delamor.*

## El marco (todo de hoy, con cita en `decisiones_en_el_acto.md`)
- **M1 Foco:** cerrar el proyecto para publicar el paper; después TRUST.
- **M2 Aporte:** N_eff sobre masas de cuenca (convergente, validado contra enumeración exacta); CKM mide la geometría de "lo que sea"; **interpreta dinámica, no significado**.
- **M3 Declarar, no decidir:** extracción, tokenización y signo son entrada; se declaran con su referencia (`declaracion_extraccion_W_14oct2026.md`). Lo que no se debate: el código hace lo que el paper declara.
- **M4 Sin regresiones ni compatibilidad hacia atrás; la única versión es la actual.**
- **M5 Estabilidad:** primero estable, declarada "dentro de este rango, con estas dependencias"; después suites con drivers matemáticos.
- **M6 Dirección abierta:** histéresis / dinámica a través de ciclos de W (no medido).
- **M7** El silencio no es observable en W; la tensión es interpretación del signo.

## Corrección previa (A3)
La "§9" de ayer (8 de 12 unidades = joins) era una foto **anterior al filtro F3b** (9 oct): hoy SYSTEM no entra al corpus (`ckm_monitor.py:284-312`). No era hallazgo nuevo; y el conteo estaba mal (8 joins, no 7). Corregido en `nodo_y_W_desde_abajo_13oct2026.md` §9 y en `aporte_vs_rueda_14oct2026.md`.

## Evaluación, TASK por TASK

| TASK | estado leído | con el marco | propuesta |
|---|---|---|---|
| `should_rebuild_conectado_v1` | **cerrada** (CP1–CP5) | — | nada |
| `monitor_coco_ciclo_orbita_v2` | **cerrada** | — | nada |
| `CKMlandscapeConfig_v3` | **cerrada** | los ciclos que existen son la base de M6 | nada |
| `node_extractor_regla_v1` | CP0a, CP0, CP1 hechos; CP-S: S0, S1, S0b hechos; **CP2** (reloj n1, exención, N > top_k) y **S3, S2a/b, S4, S5** pendientes; decisión "perfil distinto → A1.PAUSA" sin código | M3: la extracción es rueda; se declara. M4: la decisión del perfil se apoyaba en estados viejos | **Cerrar.** Lo hecho queda. Sale lo pendiente (CP2, S2–S5) → OPUSDELAMOR, después. La decisión del perfil: **retirarla** (pregunta abierta a delamor desde hoy). Lo único que sigue vive en la TASK reformulada de abajo (CP-D) |
| `ckm_trust_rule_v1` | CP0a, CP0b, CP0, CP1–CP4 hechos; CP0b con 3 entradas abiertas | La regla no está en el paper (grep v28). Es TRUST | **Pausa → TRUST.** Sin CPs nuevos ahora |
| `calibrate_mecanismo_v1` | CP1 hecho (mecanismo, tres estados); patrón del canal vivo y nombres abiertos | Calibra umbrales de COCO; COCO no es núcleo del paper | **Pausa.** En el paper: una línea en condiciones |
| `fabrication_service_v2` | **sin empezar** | Su CP2 es un **test de regresión** (M4 lo saca). El servicio no es aporte | **Reformular a lectura:** sólo la pregunta para el paper — ¿qué código corrió en el Caso 0.11? Sin reescribir el servicio |
| `canal_iap_clock_iniciativa_v2` | CP0, CP0b (freeze), CP1 (reloj), CP2 (ODA continuo, criterio local, vivos) hechos; **CP3 caso Z** pendiente [delamor] | IAP es prueba del instrumento. El reloj del canal es donde vive el silencio (M7) | **Pausa** (CP3 cuando haya serie nueva, después del paper o en TRUST) |
| `tests_instrumento_v1` | **CP6 hecho** (campo plantado, 12 oct); CP1–CP5 y CP7 **sin archivos** en `tests/` | Es la TASK que más sirve al paper, reformulada | **Reformular** (abajo) |

## La TASK reformulada: lo que el paper necesita del código
Nombre propuesto: `TASK_condiciones_del_paper_v1` (reemplaza a `tests_instrumento_v1`; ésta queda como traza). Todos los CPs producen **números o propiedades que van al paper como condición declarada**; ninguno arregla nada.

| CP | de dónde viene | qué hace | para el paper |
|---|---|---|---|
| **CP-D** Declaración ejecutable | `node_extractor_regla` + tests_instrumento CP5 | Un test por operador de `declaracion_extraccion_W_14oct2026.md` (los 8 pasos): el código hace exactamente lo declarado. Si difiere, se corrige **la declaración**, no el código | §4.1: "el código implementa lo que el paper declara" |
| **CP-M** Nulo de marcadores (review M4) | tests_instrumento CP1 | Barajar marcadores entre textos (y el caso de subcadena como condición declarada, no como bug). ¿Desaparece el efecto de W_mixta? | P5, P7, W_mixta: "verificado bajo el procedimiento de marcadores", con su nulo |
| **CP-T** Teorema de presencia | tests_instrumento CP3 | W ≥ 0 sin marcadores → 0 negativos, 0 triángulos frustrados, T = 0 | §4/§5.2: propiedad del modelo (P1/P4), no de un corpus |
| **CP-E** Rango de estabilidad (M5) | tests_instrumento CP4 + CP6 | Variar top_k, pool, lista de stopwords, un texto más: ¿cuánto se mueve N_eff? Ya medido en CP6: ‖ΔW‖ decae como 1/n (de 0,34 a 0,02 con el campo quieto); N_eff fue función de la partición, no de los pesos, desde el paso 5 | §4.3: "N_eff estable dentro de este rango, con estas dependencias" |
| **CP-N** Nulos de P5/P7 (review M7) | review v28 | P5: réplicas por seed con su dispersión. P7: nulo que preserva grados en Δ | P5–P7 con incertidumbre. **Usa fourforums/CreateDebate: requiere orden de delamor (ckmdatasets)** |

Sale: tests_instrumento **CP2** (SYSTEM: ya en código desde F3b; "SYSTEM es campo" queda abierto, sin apuro) y **CP7** (disparo de COCO: COCO no es núcleo; pausa con calibrate).

## Lo que no es TASK todavía
- **Histéresis a través de ciclos de W (M6).** Dirección abierta, no medida. Si delamor la quiere en este paper: un CP0 sin código (qué ciclos y qué rebuilds existen hoy para incorporar y quitar textos y medir N_eff de ida y de vuelta). Si no: va a §8.5, trabajo futuro, con las tres referencias.
- **Paper v29.** Es el trabajo principal (ESTADO 10 oct: "lo más atrasado"). Lo de hoy entra ahí: abstract y título alrededor del estimador; §4.1 con la declaración; P7 sin "genuine structural tension"; §6 con el silencio como observación del canal; review M1–M9.

## Orden propuesto
1. **Paper v29: encuadre** (Opus redacta, delamor decide), con lo que ya hay.
2. **CP-D, CP-T, CP-E** (Code; no tocan nada vivo; dan números al paper).
3. **CP-M** (Code).
4. **CP-N** sólo con orden de delamor sobre los datasets.
5. **M6** según decida delamor: CP0 ahora, o §8.5.

## Para delamor
1. ¿Se cierran `node_extractor_regla_v1` y se retira la decisión "perfil distinto → A1.PAUSA"?
2. ¿Pausan `ckm_trust_rule_v1`, `calibrate_mecanismo_v1`, `canal_iap_clock` CP3?
3. ¿`fabrication_service_v2` queda sólo como la pregunta del Caso 0.11?
4. ¿`TASK_condiciones_del_paper_v1` con esos CPs, y en ese orden?
5. ¿La histéresis entra en este paper o va a trabajo futuro?
