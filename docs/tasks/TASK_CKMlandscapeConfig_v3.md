# TASK_CKMlandscapeConfig_v3

*7 oct 2026. Decisiones de delamor del 6 oct (`NOTA_orden_tasks_06oct_v1.md` §6–§8). Redacta Claude Opus 5.5 (Cowork) y ejecuta Claude Code en el Codespace `ckm`. Leído contra `eddb4b0`.*
*Continúa `TASK_CKMlandscapeConfig_v2.md` (`cc690db`), que no llegó a ejecutarse. **El criterio, las tres clases, la estructura de ciclos, las invariantes I1–I7 y la transición única de la v2 siguen vigentes; hay que leerlos ahí.** Esta v3 agrega lo que delamor decidió y responde las dos preguntas que la v2 dejó en "A decidir".*
*Se trabaja según `docs/tasks/PROTOCOLO_code_continuidad_v1.md`.*

---

## 1. Lo que decidió delamor

| # | decisión | efecto |
|---|---|---|
| D1 | *"Si config v2 suma lo de v1, la reemplaza. Solo v2."* | `ckm_landscape_config.py` queda con la versión de ciclos. La clase v1 congelada desaparece del código vivo y queda en git. |
| D2 | **El set es síncrono, por ahora.** | `abrir_ciclo` es una llamada síncrona: cuando retorna, el ciclo nuevo ya es el vigente. No hay sets diferidos ni en cola. |
| D3 | **El get debe ser consistente para todos los players.** *"No dejar un estado del instrumento inconsistente, causado por independencia de accesos, de get concurrentes."* | El get devuelve un `Ciclo` **entero e inmutable** (I1) en una sola operación. No hay getters por campo que se puedan intercalar con un set. |
| D4 | **Monitor abre el ciclo.** | Monitor llama a `abrir_ciclo`, en el mismo bloque que `_invalidar_si_W_cambio`. Ningún otro servicio lo llama. El primer ciclo es `"bootstrap"`. |
| D5 | **El CLOCK no va en la Config** (provisional, con cautela: *"no caer en el mínimo local 'va al entorno'"*). | Esta TASK no implementa clock ni ticks. La Config no los setea. |
| D6 | **La calibración es un proceso aparte** (*"Calibración de CKM"*). | Esta TASK no calibra nada. Lo declarado (θ_W, sampling_mode, scale) entra como parámetro y queda inmutable durante el run. |

## 2. Lo que agrega la v3 a la v2

- **Get consistente (D3):** `config.ciclo_vigente` devuelve el objeto `Ciclo` completo. El cambio de ciclo es **un solo reemplazo de referencia**. Si en el CP0 aparece concurrencia real (hilos), el reemplazo y la lectura van bajo un mismo lock. Si los consumidores están en **procesos distintos**, una config en memoria no se comparte, y eso se **escala** (no se resuelve en esta TASK).
- **Tiempos de I6:** `t_señal` y `t_rebuild` quedan en tiempo de pared (`time.time()`), como en la v2. Si algún día hay ticks, se pueden registrar **como traza** y no como medida: el ciclo de W y el tick son de órdenes distintos, y el grano de uno no mide al otro (NOTA §8).
- **El panel (I7):** la clave `landscape_config` del panel de Monitor pasa a llevar `config.panel()`, es decir identidad + declarado + ciclo vigente, sin la historia.

## 3. Checkpoints

### CP0. Lectura, sin código

1. **Consumidores de la clase v1.** Hasta ahora se leyeron: `services/monitor_service.py` (L44, L79, L117, L215), `services/gatekeeper_c1.py`, `experiments/replay_sesion_trust.py`, `P1P4/run_conteo_vs_masa_04oct/conteo_vs_masa.py`, y los tests `test_ckm_landscape_config.py`, `test_landscape_config_en_runs.py`, `test_rebuild_consulta_w_version.py` y `test_gatekeeper_c1.py`. Confirmar la lista y decir qué usa cada uno: `from_W`, `to_dict`, campos sueltos.
2. **Concurrencia real.** ¿Hay hilos o procesos que lean la config al mismo tiempo? (canal IAP, `ckm_monitor.py`, drivers). Hay que responderlo antes del CP1, porque decide si hace falta un lock y si hay algo para escalar (§2).
3. **Experimentos y REG históricos que serializaron la config v1** (JSONL, paneles). No se reescriben. Hay que decir cómo se leen después del cambio.
4. **Lo medido de v1 contra v2:** confirmar que `medido(W)` da los mismos valores (μ_W 0.005977 / 0.004519 sobre `W_ckm_corpus_v2.json`).

**Alto. Reportar en la bandeja.**

### CP1. La clase nueva, sin tocar a los consumidores

- `Ciclo` (inmutable) y la config con ciclos, según la v2 + D1–D3. La clase v1 sigue existiendo, renombrada (`CKMlandscapeConfigV1`), solo hasta el CP3.
- Tests: los de la v2 (I1–I7, valores medidos, serialización con historia, un rebuild con nodos distintos y el mismo N) **más**:
  - el get devuelve siempre un `Ciclo` completo, nunca uno mezclado (si hubo concurrencia en el CP0, con un test de hilos que puede fallar);
  - `abrir_ciclo` es síncrono: después de que retorna, `ciclo_vigente` es el nuevo.

**Commit. Alto.**

### CP2. Monitor consume la config

- Monitor recibe la config nueva, llama a `abrir_ciclo` en `_invalidar_si_W_cambio` (D4) y lee su ciclo de `ciclo_vigente`.
- El panel lleva `config.panel()`.
- `test_landscape_config_en_runs.py` y los tests de Monitor quedan en verde; si alguno cambia, se reporta cuál y por qué.
- **No toca a COCO.** Que COCO renazca con el ciclo es `TASK_monitor_coco_ciclo_orbita_v1`.

**Commit. Alto.**

### CP3. Los demás consumidores, y v1 sale

- Migrar `gatekeeper_c1.py` y los drivers vivos. Los experimentos y P1P4 ya corridos **no se tocan**: si importan v1, se reporta.
- Se borra `CKMlandscapeConfigV1` y se agrega una entrada al CHANGELOG.

**Commit. Alto.**

## 4. Lo que esta TASK NO hace

- No implementa clock ni ticks (D5).
- No calibra nada, ni le pone defaults a lo declarado (D6).
- No hace renacer a COCO (eso es `TASK_monitor_coco_ciclo_orbita_v1`).
- No conecta CorpusService a la config.
- No define la fórmula de θ_W.
- No resuelve la config compartida entre procesos (si aparece, se escala).
