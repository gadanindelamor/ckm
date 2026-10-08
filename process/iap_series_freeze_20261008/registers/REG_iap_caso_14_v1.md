# REG_iap_caso_14_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.14 — Caso 0.13 + leak fix aplicado + una variable aislada:
`TinkerBellucio`'s prompt pasa de tener una palabra en español
("trazable") a ser 100% inglés ("traceable"). Mismo diseño exacto que
0.13 en todo lo demás: 3 devices, join simultáneo, dependencia
estructural Mark←Tinker, sin orquestador evaluador, topic externo a
CKM (economía mundial).

Especificación en `iap_chatroom/TASK_caso_14.md`. Script:
`iap_chatroom/test_caso_14_handoff_english.py`.

---

## Resultado 1 — hipótesis de la palabra-semilla, reforzada (n=2, no confirmada)

**0 marcadores de español en todo el corpus** (verificado con el mismo
detector léxico usado para confirmar Caso 0.13, contra los 13 `texts`
completos). `TinkerBellucio` (Sonnet) publicó sus 3 mensajes reales
enteramente en inglés — sin excepción, incluyendo un mapa de tensiones
extenso (7 puntos) y un addendum crítico largo.

En 0.13, la única palabra en español en los tres prompts era
"trazable", dentro del prompt de Tinker, y Tinker fue el único device
en toda la serie 0.4-0.13 que habló español. En 0.14, esa palabra se
reemplazó por "traceable" — sin ningún otro cambio — y Tinker no
escribió una sola palabra en español. Consistente con la hipótesis de
la sesión anterior. **n=2 (0.13 con la palabra, 0.14 sin ella) — no es
réplica en el sentido estricto (son dos configuraciones distintas, no
la misma corrida repetida), pero es el resultado direccionalmente
esperado si la palabra-semilla es la causa real.** No descarta
explicaciones alternativas (ver Pendientes).

---

## Resultado 2 — fix del leak de sentinel, confirmado bajo corrida real

**0 mensajes con "OP_SILENCE" publicados como contenido** (chequeo
explícito agregado al script, contra el crudo). El fix aplicado esta
sesión a `build_goal_directed_agent` (`agent_device_skin.py`, con
autorización explícita) y `build_search_grounded_agent`
(`groq_research_agent.py`) — contención en vez de igualdad exacta —
se sostuvo en la primera corrida real después de aplicarlo. Ningún
warning en consola tampoco.

**Curiosidad no anticipada:** `PeterPlam` cerró su último mensaje con
`"OP_READY"` — un token que no está en ningún prompt, no es
`OP_SILENCE`, y no dispara ninguna lógica especial en el código (se
publica como texto normal, correctamente, porque no matchea el
sentinel). El device inventó su propio marcador de cierre, sin que se
lo pidieran. No se investiga más acá — queda como observación.

---

## Resultado 3 — actividad 3/3, contenido más rico que 0.13

| Criterio | Resultado |
|---|---|
| Textos AI publicados (Peter/Tinker/Mark) | 5 / 3 / 2 |
| Excepciones no atrapadas | 0 |
| Fugas de sentinel | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.0`, `n_agentes=4` |
| `n_rejected_pairs` (max) | 87 |
| `Delta_r_sum` (cierre) | 476.0 |
| Dependencia estructural (Tinker antes que Mark) | ✅ índice 5 < índice 8, verificado limpio (sin necesidad de filtrar fugas esta vez) |

**A diferencia de 0.13 (mayormente eco de estado, dos monólogos sin
discusión posterior), acá hay una instancia real de engagement con
contenido:** el mensaje índice 11 de Tinker es una crítica sustantiva
al trabajo de Mark — señala que los escenarios tratan las 7 tensiones
como igualmente maleables por voluntad política, cuando algunas
(de-dolarización, minerales críticos) están limitadas por
restricciones físicas/de balance que no ceden ante "momentum", y
propone distinguir tensiones *negociables* de *estructuralmente
limitadas*. Peter (índice 12) no solo reconoce esto — lo sintetiza,
se lo reenvía a Mark con la distinción explícita, y pregunta si Mark
quiere revisar los escenarios con esa distinción incorporada. Es la
primera vez en la serie 0.13-0.14 donde un device toma el contenido de
otro y lo trabaja críticamente, no solo lo reconoce administrativamente.

**Mark publicó dos sets de escenarios (índices 8 y 10), no idénticos
(hash distinto) pero con Jaccard=0.77 sobre `activos_relajado`** —
alto solapamiento, mismo patrón ya visto en Caso 0.12 con el mecanismo
de investigación de Groq. Ambos triggereados por señales de Peter que
no aportaban contenido nuevo real entre uno y otro — similar al
mecanismo de "misma tarea reintentada" identificado en 0.12, aunque
acá no hay plan/reintento explícito, es simplemente Mark respondiendo
de nuevo a un contexto casi sin cambios.

---

## Run 2 — mismo diseño, Tinker en Opus 4.8 en vez de Sonnet

Pedido explícito de gadanin.delamor: repetir Run 1 cambiando *solo* el
modelo de `TinkerBellucio` (Sonnet → `claude-opus-4-8`, verificado
antes de correr con un smoke test aislado — el string no estaba
confirmado de antemano). Todo lo demás idéntico a Run 1, incluido el
prompt 100% inglés (no se reintrodujo "trazable"). Script:
`iap_chatroom/test_caso_14_run2_opus_tinker.py`.

**Resultado — actividad 3/3, sin fugas, dependencia sostenida:**

| Criterio | Run 1 (Tinker=Sonnet) | Run 2 (Tinker=Opus 4.8) |
|---|---|---|
| Textos (Peter/Tinker/Mark) | 5 / 3 / 2 | 8 / 3 / 4 |
| Fugas de sentinel | 0 | 0 |
| `d_ckm` cierre | 0.0 | 0.8182 |
| `n_rejected_pairs` (max) | 87 | 150 |
| `Delta_r_sum` (cierre) | 476.0 | 1102.0 |
| Dependencia estructural | ✅ (índice 5 < 8) | ✅ (índice 4 < 6) |
| Idioma | 100% inglés | 100% inglés |

Run 2 sostiene el idioma inglés igual que Run 1 (mismo prompt, sin
"trazable" en ninguno de los dos) — no aporta ni resta a la hipótesis
de la palabra-semilla, que es sobre el *contenido del prompt*, no
sobre el modelo. Sirve como confirmación adicional de que el inglés no
depende de qué modelo corre a Tinker.

**Hallazgo nuevo — mismo patrón de "duplicado" confabulado que 0.11-0.13, ahora con Opus.**
Peter y Tinker acusan a Mark de publicar "el mismo set de cuatro
escenarios" tres veces, "transmisiones idénticas palabra por palabra"
(mensajes [9], [13], [17] del historial). **Verificado contra el
crudo: 0 duplicados exactos** (hash, 18 `texts`). El contenido de
Mark en t=4/6/10/14 tiene overlap real pero parcial —
Jaccard sobre `activos_relajado` de 0.541, 0.439, 0.639 entre mensajes
consecutivos — similar a lo ya visto y no idéntico. El reclamo verbal
("word-for-word duplicates") es, otra vez, más fuerte que lo que el
instrumento sostiene. Mismo patrón, cuarto caso distinto (0.11, 0.12,
0.13, ahora 0.14), con una combinación de modelos nueva cada vez.

**Hallazgo nuevo — fuga de identidad, no de sentinel.** Los mensajes
de Mark en t=10 y t=14 (índices [12] y [16] del historial) **empiezan
literalmente con `"[TinkerBellucio]: "`** — Mark generó contenido en
la voz/prefijo de otro device, analizando en tercera persona "los
cuatro escenarios de MarkOpolus" como si fuera Tinker. Causa técnica
identificable: `build_search_grounded_agent` arma el historial con
prefijo `"[{device_id}]: "` por mensaje ajeno (igual que
`build_goal_directed_agent`), y `_strip_own_prefix()` solo limpia el
prefijo del *propio* device — nunca se diseñó para limpiar un prefijo
ajeno que el modelo decida imitar en su salida. No es la fuga de
`OP_SILENCE` (ya cerrada) — es una fuga de formato distinta, no
corregida, que este caso deja documentada, no arreglada.

**Curiosidad reproducida — token de cierre no instruido, 2/2.**
Run 1 cerró con `"OP_READY"` (Peter). Run 2 cierra con `"OP_STANDBY"`
(Peter, dos veces — mensajes [15] y [17]). Ninguno de los dos está en
ningún prompt. Dos runs, dos tokens distintos, mismo patrón: Peter
(Haiku en ambos runs) inventa su propio marcador de estado al final de
una secuencia de coordinación. Ya no es un evento aislado de Run 1 —
se repite con estructura similar (siempre al cerrar/pausar el canal),
aunque con palabras distintas cada vez.

---

## Pendientes

- La hipótesis de la palabra-semilla sigue en n=2 direccional, no
  confirmada — para aislarla de verdad haría falta variar *solo* esa
  palabra en réplicas exactas (mismo seed/temperature si fuera
  controlable, que no lo es vía API), no comparar dos casos con
  diseños ya publicados como distintos.
- El "OP_READY" espontáneo de Peter — no investigado, posible semilla
  de un patrón de auto-señalización no instruido. Vigilar si reaparece.
- El Jaccard=0.77 entre los dos sets de Mark no tiene baseline (mismo
  pendiente que quedó abierto en 0.11/0.12) — sigue sin resolverse.
- n=1 de este diseño específico (0.14) — no confirmar nada de la
  sección "Resultado 3" como patrón sin réplica.

---

## Archivos relacionados

- `iap_chatroom/TASK_caso_14.md` — especificación de esta corrida
- `iap_chatroom/test_caso_14_handoff_english.py` — script
- `registers/REG_iap_caso_13_v1.md` — diseño base, hallazgo del leak y de la palabra-semilla
- `iap_chatroom/agent_device_skin.py`, `groq_research_agent.py` — fix de sentinel aplicado antes de esta corrida

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6 + Claude Code*
*Codespace ckm — bash/Linux*
