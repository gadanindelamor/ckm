# REG_hint_next_instance_v7.md

*Jul 22 2026 — Hint para próxima instancia. Continúa el hilo IAP Chatroom
iniciado en v5 (0.4→0.5) y continuado en v6 (0.6→0.9). Este cubre
0.9 réplica → 0.10 → hallazgo del bug de max_tokens → 0.11 (incompleto).*
*Leer v6 primero si no se tiene el contexto de la serie 0.6-0.9.*

---

## Estado del repo — sigue sin commitear NADA de esta sesión

Último commit real: `a78c3fe` (hint v5, Casos 0.4→0.5). Todo lo de
0.6→0.11 sigue en el working tree. `_state/` está vacío al cierre
(corrida limpia, sin residuo). Correr `git status` antes de asumir
cualquier cosa.

Modificados (no commiteados) además de lo ya listado en v6:
- `iap_chatroom/providers/anthropic_provider.py` — fix de max_tokens (ver abajo)
- `iap_chatroom/providers/groq_provider.py` — mismo fix, preventivo

Nuevos (untracked) además de lo ya listado en v6:
- `iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py`,
  `test_caso_10_device_skin.py`, `test_caso_11_two_skins.py`
- `iap_chatroom/agent_device_skin.py` — `AgentDeviceSkin`, `build_goal_directed_agent()`
- `registers/REG_iap_caso_09_v1.md`, `REG_iap_caso_10_v1.md`
- `registers/MAPA_REG_corpus_v2.md` — **no es mío**, aparece untracked;
  parece un mapa de corpus más amplio (Firma_CKM, W versionado,
  integración A2A, COCOThermostat) escrito por otra instancia/sesión —
  leerlo para contexto del proyecto más allá de IAP chatroom, no
  asumir que documenta solo este hilo.
- ~15 backups nuevos en `process/*caso09*`, `*caso10*`, `*caso11*`

---

## Caso 0.9 — réplica confirmó el patrón (4/4 total)

Pedida explícitamente antes de avanzar a device_skin: repetir
`test_caso_09_provider_hetero_join_escalonado_2dev.py` (Sonnet vs
Groq, join escalonado, 2 devices) sin modificar. **Actividad 2/2 en la
réplica — 4/4 total, confirmado robusto, no varianza de muestreo.**
Contenido notable: en la réplica, Sonnet volvió a nombrar "agreeable
drift" en Groq explícitamente, mismo movimiento discursivo que en la
corrida original pero en otro tema. Ver `registers/REG_iap_caso_09_v1.md`.

---

## Caso 0.10 — AgentDeviceSkin, primer agente con objetivo propio

Nuevo mecanismo: `AgentDeviceSkin` (subclase de `AutonomousDevice`,
`agent_device_skin.py`) delega la decisión ODA y el contenido a un
`wrapped_agent` externo con objetivo propio, sin gate LLM genérico.

**Decisión de diseño reportada antes de escribir código** (confirmada
vía pregunta directa, no asumida): la tarea pedía sobreescribir
únicamente `_decide()`, pero eso habría descartado el texto real del
wrapped agent (`_interact()` heredado regenera con `self.system_prompt`,
el WELCOME MSG del canal, no el objetivo del agente). Resolución:
sobreescribir también `_generate()` — `_decide()` cachea el texto en
`self._pending_text`, `_generate()` lo devuelve tal cual. `_interact()`,
`_observe()`, `run()` quedan heredados sin cambios.

**Bug real encontrado y corregido en `agent_device_skin.py` (no en
`autonomous_device.py`):** `wrapped_agent` construía mensajes desde
`observation["history"]` (fetch completo del canal), que a diferencia
de `self._history` de la clase base puede terminar en el propio último
mensaje del device — Sonnet rechaza un prompt que termina en rol
"assistant" (`This model does not support assistant message prefill`).
Fix: agregar siempre `observation["trigger"]` (nunca propio) como
turno final antes de coalescer.

**Resultado, primer intento con el fix:** funcionó — 6 textos, skin
abrió en su objetivo ("knowledge cohesion..."), control se enganchó con
profundidad técnica real. Ver `registers/REG_iap_caso_10_v1.md`.

---

## Hallazgo mayor durante Caso 0.11 — bug de max_tokens=1024, retroactivo

`iap_chatroom/providers/anthropic_provider.py` tenía `max_tokens=1024`
hardcodeado y nunca revisaba `response.stop_reason` — truncamiento
silencioso en generaciones largas, sin error, sin log. Confirmado con
reproducción directa (llamada aislada → `stop_reason: max_tokens`,
corte a mitad de palabra, mismo patrón exacto que en los datos reales).

**Fix aplicado a ambos providers:**
- `anthropic_provider.py`: `max_tokens` 1024→4096 + warning explícito
  (`print`) si `stop_reason=='max_tokens'`.
- `groq_provider.py`: no tenía `max_tokens` seteado ni revisaba
  `finish_reason` — mismo riesgo latente. Endurecido igual
  (`max_tokens=4096` + warning en `finish_reason=='length'`), aunque
  una reproducción directa contra Groq NO mostró truncamiento en esa
  prueba puntual.

**Retroactivo, verificado (no asumido) contra los `corpus_state.json`
crudos ya usados en REGs escritos:**
- Caso 0.9 (4 corridas): 5 de 65 textos AI truncados. **Atribuidos por
  device (cruce índice→agent_id en trajectory): los 5 son de
  `ClaudeSonnet_5_1`, cero de `GroqLlama_3-3-70b_2`.**
- Caso 0.10 (intento original): 2 de 6 textos truncados por este bug,
  más un truncamiento de 86 caracteres que este bug NO explica (sigue
  sin causa determinada — max_tokens produce cortes largos, no de 86
  caracteres).

**Importante para leer trayectorias CKM de esos casos:** `fi`,
`Delta_r_sum`, `n_rejected_pairs`, `D_ckm` en los REGs de 0.9 y 0.10
son mediciones reales, pero sobre el corpus parcial que efectivamente
se ingirió — no sobre el argumento completo que el modelo pretendía
producir. Los hallazgos centrales de esos casos no se invalidan; los
números exactos de los turnos truncados sí deben leerse con esa
salvedad. Notas retroactivas completas en ambos REGs.

**Caso 0.10 tiene además un "Baseline limpio" re-corrido con el fix
aplicado** — 0 mensajes truncados, mismo patrón cualitativo, ver
sección homónima en `REG_iap_caso_10_v1.md`. Ese es el baseline de
referencia a partir de ahora, no el intento original parcialmente truncado.

**Verificación de concurrencia también resuelta en esta sesión:**
gadanin.delamor preguntó si `AsyncAnthropic` es seguro para uso
concurrente antes de correr 2 devices con `asyncio.gather`. Verificado:
cada device instancia su propio `AnthropicProvider` (y por lo tanto su
propio `AsyncAnthropic` interno) — no hay cliente compartido entre
corrutinas en ningún script de esta serie, así que la pregunta de
thread-safety de un cliente compartido no llega a ejercitarse en este
código. No se encontró garantía oficial explícita en la documentación
del paquete instalado (`anthropic==0.116.0`) más allá de que usa
`httpx.AsyncClient` internamente (diseñado para concurrencia).

---

## Caso 0.11 — INCOMPLETO, retomar desde cero

`test_caso_11_two_skins.py` ya escrito: 2 `AgentDeviceSkin` con
objetivos distintos (Architect: práctica/producción; Theorist:
teoría/emergencia de significado), sin control, join escalonado,
2 runs con roles invertidos — mismo diseño que 0.8/0.9/0.10.

**Run 1 se corrió UNA vez, pero con el bug de max_tokens todavía
presente** (se descubrió durante esa misma corrida). Resultado
parcialmente truncado — y con un fenómeno emergente notable: ambos
devices notaron el truncamiento repetido y lo nombraron explícitamente
en el contenido publicado, conectándolo con su propio tema (testimonio,
reparación, provenance). **Verificado: es en parte preciso (el
truncamiento es real, confirmado contra crudo) y en parte confabulado**
(no hay ningún duplicado exacto ni prefijo exacto en los datos — las
afirmaciones de "mensaje idéntico palabra por palabra" no se sostienen).
El campo CKM registró ese corpus (parcial + la meta-conversación sobre
el truncamiento) tal cual, sin filtrar.

**No se re-corrió limpio. No se corrió Run 2 en absoluto.** Con el fix
ya aplicado y verificado (`max_tokens=4096` en ambos providers,
confirmado antes de la pausa), el siguiente paso inmediato es:

1. `prepare_state(label="caso11_run1")`, reiniciar servidor, verificar
   `_state/` limpio.
2. `python iap_chatroom/test_caso_11_two_skins.py --run 1` — limpio esta vez.
3. `prepare_state(label="caso11_run2")`, reiniciar servidor.
4. `python iap_chatroom/test_caso_11_two_skins.py --run 2`.
5. Devolver `corpus_state.json`/`monitor_trajectory.jsonl` de cada run,
   verificar 0 mensajes truncados (buscar warnings de
   `[AnthropicProvider WARNING]`/`[GroqProvider WARNING]` en la salida
   del servidor — ahora son visibles, no silenciosos).
6. Escribir `REG_iap_caso_11_v1.md` — no existe todavía. El intento
   truncado del Run 1 original queda preservado en
   `process/corpus_state.json.bak_1784777737_caso11_run1` para
   referencia/comparación (dato interesante en sí — confabulación de
   duplicación — pero no el resultado a reportar como Caso 0.11 final).

---

## Convenciones ya establecidas — no reinventar (siguen vigentes de v5/v6)

- Backup: `prepare_state(state_dir, label)` mueve a `process/` con
  `.bak_<epoch>_<label>` — nunca borra. Gotcha de labeling: archiva el
  run *anterior* bajo la etiqueta del run *actual* — verificar contenido
  real, no confiar en el nombre.
- Lifecycle del servidor: `run_in_background` + `TaskStop`, esperar
  `GET /api/monitor` con `200` antes de asumir que está listo.
- NO MODIFICAR con solución que requiere excepción → reportar antes de
  proceder, aunque termines encontrando una solución que no la requiera
  (confirmado valioso en más de una ocasión esta sesión).
- **Nuevo:** revisar la salida de consola del servidor por warnings de
  truncamiento (`max_tokens`/`finish_reason`) después de cada corrida,
  no solo al final — son parte de los criterios de éxito ahora.

---

## Pendientes explícitos

1. **Caso 0.11 — correr limpio (Run 1 + Run 2), escribir REG.** Ver
   secuencia arriba. Es lo inmediato.
2. Caso 0.9: hetero-provider + join simultáneo (separar provider de
   timing), mono-provider Groq (separar "efecto Groq" de "heterogeneidad
   de provider en general") — siguen sin correr.
3. Caso 0.10: replicar (n=1 en el baseline limpio), probar 2 skins con
   objetivos en conflicto explícito (no solo distintos), objetivo más
   estrecho/adversarial.
4. El corte de 86 caracteres en el Caso 0.10 original sigue sin causa
   determinada — no es el bug de max_tokens (demasiado corto). Si
   reaparece, investigar en serio.
5. `MAPA_REG_corpus_v2.md` (no es mío) — leerlo completo si se retoma
   trabajo más allá de IAP chatroom; conecta este hilo con otros
   (Firma_CKM, W versionado, A2A, COCOThermostat) que no cubrí en detalle.

---

## Archivos relacionados

- REG_hint_next_instance_v6.md — hilo previo (Casos 0.6→0.9 primera pasada)
- registers/REG_iap_caso_09_v1.md, REG_iap_caso_10_v1.md — con notas retroactivas del bug de max_tokens
- iap_chatroom/test_caso_11_two_skins.py — listo para correr, no corrido limpio todavía

---

*Jul 22 2026*
