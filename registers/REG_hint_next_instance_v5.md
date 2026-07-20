# REG_hint_next_instance_v5.md

*Jul 20 2026 — Hint para próxima instancia. Sesión IAP Chatroom, Casos 0.4→0.5.*
*v1→v4 son de otro hilo (corpus/fourforums/W_mixta, Jun 2026) — no relacionados
con esta sesión salvo por el patrón de hint en sí. Este es el primer hint del
hilo IAP Chatroom / AutonomousDevice / ciclo ODA.*

---

## Estado del repo post-sesión

Todo commiteado y pusheado a `main` (`2a33894..5b45006`):

- `376fc00` — feat(iap): ODA cycle + system event seed (Casos 0.4→0.5)
- `8883ded` — feat(iap): simulation runs, providers, services (pre-Caso 0.4, de sesiones previas)
- `85546a1` — chore: gitignore .claude/
- `5b45006` — data: experiment state backups (Casos 0.0→0.5) en `process/`

Sin cambios pendientes en el working tree al cierre.

Archivos clave de esta sesión:
- `iap_chatroom/autonomous_device.py` — ciclo ODA (`_observe`/`_decide`/`_interact`), sin bootstrap bypass
- `iap_chatroom/channel.py`, `mcp_server.py` — join emite mensaje `device_type=SYSTEM`
- `iap_chatroom/test_caso_04.py` / `04a.py` / `04b.py` / `05.py` — la serie completa
- `registers/REG_iap_caso_04_oda_v1.md` / `04a_v1.md` / `04b_v1.md` / `05_v1.md` — reportes con datos crudos verificados

---

## Hallazgo central de la sesión

**El meta-drift (auto-análisis, "hall of mirrors", ruptura de identidad,
disputas epistémicas) en los devices AI de la chatroom no era propiedad
del WELCOME MSG ni del modelo — era el seed.**

Trayectoria del descarte de hipótesis:
1. Caso 0.4 (Haiku, CKM explicado en WELCOME MSG, seed "What do you
   think about this space?") → meta-drift, ruptura de identidad
   ("I'm Claude, not a device")
2. Caso 0.4a (mismo, sin CKM explicado) → meta-drift igual, sin ruptura
   de identidad → descarta "es el WELCOME MSG"
3. Caso 0.4b (Sonnet en vez de Haiku) → meta-drift igual, mecanismo
   distinto (disputa epistémica en vez de identidad) → descarta "es Haiku"
4. Caso 0.5 (sin seed humano — el canal emite automáticamente
   "{device_id} joined the channel" al hacer join) → **sin meta-drift**.
   Los devices parafrasearon el WELCOME MSG casi textualmente y quedaron
   en OP_SILENCE sostenido. Primera vez con c_S positivo en la serie.

La causa era literal: "What do you **think**..." primeaba reflexión
antes de que cualquier device publicara una palabra. Verificado contra
`rechazados` crudo del jsonl, no solo inferido: `think` aparecía
aislado contra el 100% del vocabulario activo en los turnos tempranos
de 0.4a/0.4b; desaparece por completo en 0.5.

**Pregunta abierta para Caso 0.6:** qué tipo de seed produce actividad
genuina (contenido real, no parafraseo del prompt) sin reintroducir la
reflexividad que dispara meta-drift. No se probó todavía un seed
concreto/de contenido que no invite a "pensar sobre el espacio".

---

## Pendientes verificados de esta sesión

- **Caso 0.6** — diseñar un seed de contenido concreto (no reflexivo,
  no "system event" vacío) como siguiente variable de control. Ver
  cierre de `REG_iap_caso_05_v1.md`.
- **Caso "No seed"** (mencionado en la tarea de Caso 0.5, no corrido):
  mismo `test_caso_05.py`, pero revirtiendo el filtro de
  `autonomous_device.py` para que `SYSTEM` no dispare el ciclo ODA.
  Resultado esperado: silencio completo, sin script nuevo necesario.
- **`get_monitor_state()` incompleto** — no devuelve `c_S`, `fi`,
  `Delta_r`, `n_rejected_pairs` (solo están en `monitor_trajectory.jsonl`,
  no en el dict que ve `_decide()` vía MCP). Pendiente desde Caso 0.4,
  sigue sin resolverse — requeriría tocar `ckm_monitor.py`/`mcp_server.py`,
  fuera de alcance de las tareas corridas hasta ahora.
- **D_ckm negativo (Caso 0.5, -0.25)** — explicado cualitativamente
  (dos textos casi idénticos → alta co-ocurrencia → colapso de
  W_prompt/W_relajado hacia el mismo atractor → distancia se achica o
  invierte signo), pero no hay lectura formal en el código
  (`firma_ckm.py`/`ckm_topology_module.py`) de qué significa el signo.
  n=1, sin réplica.
- **Fix de timing en `AutonomousDevice.run()`** ya aplicado: `last_ts`
  se captura antes de `join_channel()`, no después — si no, el propio
  evento SYSTEM del join quedaba más viejo que el cutoff del primer
  poll y se perdía en silencio. Si se toca `run()` de nuevo, no revertir
  ese orden sin entender por qué se movió.

---

## Convenciones ya corregidas esta sesión — no reinventar

- **Backup de estado**: `iap_chatroom/_state/corpus_state.json` y
  `monitor_trajectory.jsonl` se preservan (no se borran) moviéndolos a
  `process/` (repo root, no gitignored) con sufijo `.bak_<epoch>` antes
  de cada corrida ZERO_SHOT. Mecanismo ya estaba en
  `test_iap_simulation_adversarial.py`/`test_iap_simulation_oposite_rol.py`
  (`prepare_state()`); los `test_caso_04*.py`/`test_caso_05.py` de esta
  sesión lo replican en `reset_state()`.
- **Lifecycle del servidor**: arrancar `iap_chatroom/server.py` con
  `run_in_background: true` (Bash tool) y frenar con `TaskStop` sobre
  el mismo `task_id` — no `nohup ... &` + `kill <pid>` suelto.
- **`.claude/` está en `.gitignore`** — no commitear config local de la
  herramienta.

---

## Observación de cierre

A diferencia del hilo v1→v4 (donde el gap de conocimiento entre
instancias fue el tema central — W_mixta A0=25 construida en memoria y
nunca persistida), esta sesión sí dejó todo persistido: datos crudos en
`process/`, hallazgos verificados contra esos datos crudos en los REG
(no solo narrados), y memoria de proceso (convenciones de backup y
lifecycle) escrita explícitamente para no repetirse. El patrón que
faltaba en el hilo anterior — narrar el path completo, no solo el
resultado — se sostuvo acá turno a turno.

---

*Jul 20 2026*
