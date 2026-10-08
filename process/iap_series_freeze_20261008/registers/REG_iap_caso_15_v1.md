# REG_iap_caso_15_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.15 — mismo diseño exacto que Caso 0.14 Run 1 (3 devices, join
simultáneo, dependencia estructural Mark←Tinker, sin orquestador
evaluador, topic externo a CKM/economía mundial). El único cambio:
`BehaviorGraph` (G) se conecta al `MonitorService` real del servidor
(`iap_chatroom/ckm_monitor.py`), corriendo **en paralelo real** a
{W, Δ_W} — cada mensaje que entra al corpus también entra a G vía
`MonitorService.evaluate()`, no hay reconstrucción retroactiva.

Especificación en `iap_chatroom/TASK_caso_15.md` (corregida una vez
por gadanin.delamor tras detectar un error en el snippet ilustrativo
de la sección 2c — ver Archivos relacionados). Script:
`iap_chatroom/tests/test_caso_15_behavior_graph.py`.

---

## Resultado 1 — bug de path post-mudanza, encontrado y corregido en 4 scripts

Al ejecutar el script nuevo, falló antes de abrir el canal:
`GroqError: The api_key client option must be set`. Causa: `_ENV_PATH`
se calculaba como `Path(__file__).resolve().parent / ".env"` —
correcto cuando los scripts vivían en `iap_chatroom/`, pero **roto**
desde que se movieron a `iap_chatroom/tests/` (el `.env` real sigue en
`iap_chatroom/.env`, un nivel arriba). Mismo tipo de bug que el de
`_REPO_ROOT`/`_STATE_DIR` ya corregido esta serie tras la mudanza de
directorios — esta vez no se había revisado `_ENV_PATH`.

Se verificó que el mismo bug estaba presente, sin corregir, en los
otros tres scripts movidos a `tests/`: `test_caso_13_handoff_dependency.py`,
`test_caso_14_handoff_english.py`, `test_caso_14_run2_opus_tinker.py`.
Corregido en los cuatro (`.parent` → `.parent.parent`). Estos tres
corrían silenciosamente antes porque el shell donde se ejecutaron
tenía `GROQ_API_KEY` ya exportada globalmente — no porque el path
fuera correcto.

---

## Resultado 2 — G confirmado corriendo en paralelo real, no retroactivo

Verificado contra el estado persistido del servidor (no contra un
smoke test aislado):

| Criterio (TASK_caso_15.md) | Verificado |
|---|---|
| G corre en paralelo real (no retroactivo) | ✅ — `self._behavior_graph.ingest()` ocurre dentro de `MonitorService.evaluate()`, llamado por `CKMMonitor.on_message()` en cada mensaje real del canal |
| Panel de `evaluate()` contiene `G_state` con `D_G` y `active_behavior` | ✅ — confirmado leyendo `monitor_trajectory.jsonl` directo: las 4 entradas tienen `G_state` junto a `D_ckm`, `Delta_r_sum`, `thermostat` (sin alterar campos existentes) |
| `corpus_G_state.json` persiste entre runs | ✅ — leído después del cierre del canal, sin reconstruir nada localmente |
| `g_state()` devuelve `top_coactivations` legibles | ✅ — ver tabla abajo |

**Estado final de G al cierre:** `D_G=0.3191`, `G_sparsity=0.771`,
`n_texts=4`, `mode=evaluation`.

**Top co-activaciones:**

| par | peso |
|---|---|
| publish ↔ tension | 1.000 |
| publish ↔ map | 1.000 |
| publish ↔ channel | 1.000 |
| map ↔ tension | 1.000 |
| channel ↔ tension | 1.000 |
| channel ↔ map | 1.000 |
| publish ↔ depend | 0.667 |
| depend ↔ tension | 0.667 |

Los nodos activos (`publish`, `channel`, `map`, `tension`, `depend`,
`hold`) son coherentes con el contenido real de los 4 textos que
G ingirió en este run corto (un evento de join + los dos mensajes de
Peter + el mensaje de Tinker) — sin overclaim: es una corrida corta,
no evidencia de que el termap se comporte bien en corpus largos.

---

## Resultado 3 — actividad 2/3, Mark no publicó (silencio epistémico, no bug)

| Criterio | Resultado |
|---|---|
| Textos AI publicados (Peter/Tinker/Mark) | 2 / 1 / 0 |
| Fugas de sentinel | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.2727`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 65 |
| `Delta_r_sum` (cierre) | 216.0 |
| Dependencia estructural (Tinker antes que Mark) | sin datos — Mark nunca publicó |

Tinker (Sonnet) publicó un único mensaje explicando que **se niega a
mapear tensiones sin contenido real en el canal**: *"Channel history
contains only join events... There is no structural tension to trace
yet — mapping requires at least two positions in friction, or a claim
against observable reality... I'll hold until participants introduce
content."* No es una falla del device — es un rechazo epistémico
correcto dado el estado real del canal (Peter abrió con framing de
tarea pero sin contenido sustantivo propio). Como consecuencia, Mark
—que depende del mapa de Tinker— nunca tuvo de qué partir y se
mantuvo en `OP_SILENCE` los 120s completos.

Esto deja el chequeo de dependencia estructural (Mark después de
Tinker) sin datos este run, no confirmado ni refutado.

---

## Pendientes

- n=1 de este diseño con G conectado — no confirmar nada de
  "Resultado 2" como patrón estable sin réplica, ni con corpus más
  largos.
- El silencio de Mark (0 textos) sugiere que el diseño necesita un
  Peter que aporte contenido sustantivo real, no solo framing —
  correr de nuevo con un prompt de Peter que incluya al menos una
  posición o dato inicial permitiría observar G con más texto y de
  paso probar si Tinker mapea y Mark construye escenarios.
- La fuga de identidad (`"[TinkerBellucio]: "` dentro del propio
  mensaje de Mark, hallada en Caso 0.14 Run 2) sigue sin corregir —
  no se reprodujo esta vez porque Mark no publicó nada.
- Nada de esta serie (0.9 en adelante, incluyendo 0.15) está
  commiteado a git todavía — pendiente para una próxima sesión, junto
  con la lectura del paper de IAID.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_15.md` — especificación (con corrección de
  gadanin.delamor a la sección 2c: no reemplazar el panel completo,
  campos reales `Delta_r_sum`/`thermostat`)
- `iap_chatroom/tests/test_caso_15_behavior_graph.py` — script
- `services/behavior_graph.py` — módulo G (`g_state()`, storage_path
  `corpus_G_state.json`)
- `services/monitor_service.py` — `behavior_graph` opcional en
  `MonitorService`, `G_state` agregado al panel de `evaluate()`
- `iap_chatroom/ckm_monitor.py` — integración real de G en el servidor
  (autorización explícita y puntual de gadanin.delamor para este
  cambio, ver el comentario en el propio archivo)
- `registers/REG_iap_caso_14_v1.md` — diseño base (0.14 Run 1)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
