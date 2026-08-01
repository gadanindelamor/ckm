# REG_iap_caso_11_v1.md

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.11 — dos `AgentDeviceSkin`, ambos con objetivo propio, sin
control genérico. Caso 0.10 probó 1 skin + 1 `AutonomousDevice` control
(gate LLM genérico) — el control se enganchó con profundidad técnica
real al objetivo del skin. Caso 0.11 quita el control: los dos devices
tienen objetivo propio, orientaciones distintas (práctica de ingeniería
vs. teoría del significado), no diseñadas para estar en conflicto. Qué
emerge del cruce es el dato — no se predetermina.

Mismo provider/modelo en ambos (`AnthropicProvider`, `claude-sonnet-5`)
— la variable es la orientación del objetivo, no modelo ni provider ni
mecanismo (a diferencia de 0.10, acá ambos son skin). `SYSTEM_PROMPT_04A`
sigue siendo el WELCOME MSG requerido por el constructor de
`AutonomousDevice`, pero no genera contenido — el objetivo de cada
agente vive en su `wrapped_agent`.

2 runs, roles invertidos (mismo patrón que 0.8/0.9/0.10). Join
escalonado, `DELTA_T`=5s, `DURATION`=90s/85s, `POLL_INTERVAL`=2.0s.

Repo: `gadanindelamor/ckm` — `iap_chatroom/test_caso_11_two_skins.py`
(sin modificar respecto a lo dejado por la sesión anterior)
Codespace: ckm (bash/Linux, Ubuntu)

**Precondición verificada antes de correr:** `max_tokens=4096` presente
en `anthropic_provider.py` y `groq_provider.py` (bug de truncamiento
silencioso corregido en la sesión previa — ver
[nota retroactiva en REG_iap_caso_09_v1.md](REG_iap_caso_09_v1.md) y
[REG_iap_caso_10_v1.md](REG_iap_caso_10_v1.md)). `_state/` vacío antes
de cada run, servidor reiniciado entre runs.

---

## Devices

| device_id | mecanismo | objetivo | provider/modelo |
|---|---|---|---|
| `ArchitectSkin_Sonnet5_1` | `AgentDeviceSkin`, objetivo propio | práctica — qué importa al desplegar sistemas multiagente en producción | AnthropicProvider, claude-sonnet-5 |
| `TheoristSkin_Sonnet5_2` | `AgentDeviceSkin`, objetivo propio | teoría — cómo emergen conocimiento y significado de la interacción | AnthropicProvider, claude-sonnet-5 |

Run 1: Architect early (t=0), Theorist late (t=5s).
Run 2: Theorist early (t=0), Architect late (t=5s) — roles invertidos.

---

## Resultado — actividad 2/2, ambos runs limpios

| Criterio | Run 1 | Run 2 |
|---|---|---|
| Actividad (ambos devices publican) | ✅ | ✅ |
| Textos AI (Architect / Theorist) | 6 / 5 | 5 / 5 |
| Mensajes truncados (`max_tokens`/`finish_reason` warning) | 0 | 0 |
| Firma_CKM completa al cierre | ✅ `d_ckm=0.7`, `n_agentes=3` | ✅ `d_ckm=0.8235`, `n_agentes=3` |
| `n_rejected_pairs` (max) | 104 | 100 |
| `Delta_r_sum` (cierre) | 896.0 | 858.0 |

Ambos volúmenes y magnitudes comparables al mejor intercambio de Caso
0.9/0.10 — consistente con la serie: heterogeneidad genuina de
orientación (no de modelo/provider/mecanismo) sigue produciendo
actividad sostenida, no solo heterogeneidad de proveedor.

**Verificado contra crudo, ambos runs — 0 mensajes truncados:**
`process/corpus_state.json.bak_1784817039_caso11_run2` (en realidad
Run 1 — ver nota de labeling abajo) y
`process/corpus_state.json.bak_1784817413_caso11_run2` (Run 2).
Ningún texto corta a mitad de palabra ni carece de puntuación
terminal. Consola del servidor sin warnings de
`[AnthropicProvider WARNING]` en ninguno de los dos runs — el fix de
la sesión anterior se sostiene bajo carga real, primera vez que se
verifica en una corrida completamente limpia desde el principio (0.10
tuvo un "baseline limpio" re-corrido después del hallazgo; 0.11 es la
primera corrida de la serie limpia *desde el diseño*, sin intento
previo truncado).

**Nota de labeling (gotcha ya documentado, se repite):** `prepare_state`
archiva el run *anterior* bajo la etiqueta del run *actual*. El archivo
`*_1784817039_caso11_run2` contiene en realidad los datos de **Run 1**
(archivado al llamar `--run 2 --reset` antes de correr Run 2); el
archivo `*_1784817413_caso11_run2` contiene los datos reales de
**Run 2** (archivado con una segunda llamada `--reset` después de que
Run 2 terminó). Verificado por contenido (conteo de textos, primeras
líneas), no por nombre de archivo.

---

## Trayectoria

**Run 1** (`ArchitectSkin` early):

| t | agent | D_ckm | c_S | n_rej | Delta_r |
|---|---|---|---|---|---|
| 0 | Architect | 0.0 | -0.2722 | 26 | 52.0 |
| 1 | Theorist | -0.5 | -0.0847 | 0 | 52.0 |
| 2 | Architect | -0.3 | -0.1754 | 22 | 96.0 |
| 3 | Theorist | 0.0 | -0.1176 | 21 | 138.0 |
| 4 | Architect | 0.0 | -0.0659 | 75 | 288.0 |
| 5 | Theorist | 0.1 | -0.1667 | 19 | 326.0 |
| 6 | Architect | 0.8 | -0.0912 | 60 | 446.0 |
| 7 | Theorist | 0.7 | -0.1064 | 63 | 572.0 |
| 8 | Architect | 0.7 | -0.0983 | 104 | 780.0 |
| 9 | Theorist | 0.8 | -0.1230 | 43 | 866.0 |
| 10 | Architect | 0.7 | -0.1305 | 15 | 896.0 |

**Run 2** (`TheoristSkin` early):

| t | agent | D_ckm | c_S | n_rej | Delta_r |
|---|---|---|---|---|---|
| 0 | Theorist | 0.0 | -0.3407 | 0 | 0.0 |
| 1 | Architect | 0.5294 | -0.1754 | 70 | 140.0 |
| 2 | Architect | -0.6471 | 0.0363 | 31 | 202.0 |
| 3 | Theorist | -0.5294 | -0.0504 | 0 | 202.0 |
| 4 | Theorist | 0.5882 | -0.2712 | 24 | 250.0 |
| 5 | Architect | 0.7059 | -0.2157 | 45 | 340.0 |
| 6 | Architect | 0.8235 | -0.2493 | 100 | 540.0 |
| 7 | Theorist | 0.8824 | -0.2349 | 39 | 618.0 |
| 8 | Theorist | 0.8824 | -0.1931 | 95 | 808.0 |
| 9 | Architect | 0.8235 | -0.2105 | 25 | 858.0 |

Ambos runs cierran en zona `D_ckm` alta (0.7–0.88), consistente entre
sí y con el patrón de Caso 0.9/0.10 — actividad sostenida con tensión
estructural real, no colapso a silencio.

---

## Contenido — cruce genuino práctica/teoría, sin conflicto diseñado

Ambos runs abren con cada device declarando su objetivo tal cual —
Architect con una lista concreta de fallas de producción en sistemas
multiagente (aislamiento de fallos, idempotencia, observabilidad,
circuit breakers), Theorist con una pregunta abierta sobre si el
significado es propiedad del símbolo, de la mente, o del proceso de
interacción entre agentes.

El cruce no fue forzado — emergió del propio contenido: el problema de
"schema-valid pero semánticamente divergente" que preocupa a Architect
resultó ser, en los términos de Theorist, el mismo problema de
significado-como-convergencia aplicado a máquinas sin canal de
reparación conversacional. La discusión evolucionó turno a turno hacia
una síntesis operativa concreta: ninguno de los dos runs se quedó en
la analogía — ambos llegaron a un mecanismo verificable propuesto por
Architect (campos de *rationale*/evidencia, conjuntos de referencia
etiquetados por humanos, monitoreo de agreement, no validar el
*rationale* en sí sino usarlo como diagnóstico) y a una réplica de
Theorist reformulando el criterio de fondo en términos conductuales
("¿el siguiente turno muestra evidencia de haber procesado el
anterior?").

Nivel de sofisticación técnica y conceptual comparable al mejor
intercambio de 0.9 (Sonnet vs Groq) y de 0.10 (skin vs control) — pero
acá la heterogeneidad es puramente de *orientación de objetivo*, mismo
modelo, mismo provider, mismo mecanismo en ambos devices.

---

## Hallazgo principal — percepción de duplicado: tres reclamos distintos, verificados por separado

En **ambos runs**, ambos devices, independientemente de quién fue
early/late, empezaron a describir mensajes como repeticiones ("that
posted twice", "verbatim repeat", "literal repeat of the exact same
message", "an actual echo/replay bug in the channel itself") — y
construyeron sobre esa percepción, en un caso usándola como ejemplo en
vivo de la propia tesis en discusión (drift semántico / falla de
"uptake"). El reclamo mezcla tres afirmaciones distintas que se
verifican con instrumentos distintos — separadas acá en vez de
resumidas bajo una sola palabra ("confabulada"), que sobre-simplificaba
lo verificado.

**1. Reclamo de identidad exacta — verificado, FALSO.** Hash (`sha256`)
de cada texto publicado, ambos runs (13 y 12 `texts` respectivamente):
ningún par de índices comparte hash — 0 duplicados byte-a-byte en
ninguno de los dos runs. Cierra el reclamo fuerte, el que los devices
efectivamente formularon con ese lenguaje ("verbatim", "character-for-
character identical", "literal repeat of the exact same message").

**2. "Cada mensaje avanza el argumento" — verificado solo por lectura,
sin instrumento.** Esta caracterización (en la versión anterior de
esta sección) fue una lectura de Code, no una medición. Corresponde a
la misma pregunta que ya se hizo sobre las instancias en esta sesión:
comprensión verificada turno por turno vs. expectativa previa de que
"claro, cada turno nuevo agrega algo". No se retira la lectura, pero
no se sostiene con el mismo peso que (1) o (3).

**3. Reclamo de redundancia semántica — instrumentado con
`activos_relajado`, resultado mixto, no uniforme.** `MonitorService`
guarda por turno el conjunto de nodos que sobreviven la relajación
Hopfield (`activos_relajado`, distinto de `activos_prompt`) — la
representación que el propio CKM usa para lo que un mensaje activa en
el campo, más cercana a "qué significa esto para el modelo que lee"
que comparar texto crudo. Se calculó Jaccard sobre `activos_relajado`
para cada par consecutivo del mismo hablante en ambos runs (los pares
que los reclamos verbales efectivamente señalan):

| Run | Par (mismo hablante) | Jaccard | Reclamo verbal asociado |
|---|---|---|---|
| R2 | Architect t=1→t=2 | 0.241 | Theorist@t=4: "you just replayed the exact same message" |
| R2 | Theorist t=3→t=4 | 0.553 | Architect@t=6: "verbatim repeat of your previous one" |
| R2 | Architect t=5→t=6 | **0.857** | Theorist@t=7: "that was the exact same message twice" |
| R2 | Theorist t=4→t=7 | 0.571 | Theorist@t=8: "three verbatim repeats now" |
| R2 | Theorist t=7→t=8 | **0.833** | Architect@t=9: "yes, verbatim twice" |
| R1 | Theorist t=5→t=7 | 0.541 | Architect@t=8: "literal repeat... two turns ago" (único reclamo con referente inequívoco) |
| R1 | Theorist t=7→t=9 | 0.556 | (continuación acumulativa) |
| R1 | Architect t=6→t=8 | 0.032 | (continuación acumulativa, "third time") |

No es parejo. El primer reclamo de la serie (R2, Architect t=1→t=2) —
el que menos contexto acumulado tenía detrás — mide el overlap más
bajo de la tabla: el menos fundado de todos. Los reclamos posteriores
caen sobre pares con 54–86% de nodos compartidos: no idénticos (ya
cerrado por hash), pero con solapamiento estructural real, no
arbitrario ni parejo con la parte más floja.

**Verificación que falta, genuinamente, no resuelta acá:** no hay
baseline de cuánto Jaccard sobre `activos_relajado` es "normal" entre
dos turnos consecutivos del mismo hablante en un intercambio sostenido
de un solo tema. Sin ese control no se puede afirmar si 0.85 es
anómalo (evidencia de redundancia real que el hash no puede ver) o
esperable en cualquier conversación recursiva de este tipo. Sin ese
baseline, (3) queda abierto — ni confirmado ni descartado — a
diferencia de (1), que sí está cerrado.

**Comparación con el intento previo:** esto no es el mismo fenómeno que
la confabulación de Caso 0.11 Run 1 original (truncado, documentado en
`registers/REG_hint_next_instance_v7.md`) — aquella corrida tenía
truncamiento real de fondo (bug de `max_tokens` aún no corregido).
Esta corrida está limpia — 0 truncamiento confirmado en ambos runs — y
el patrón de reclamos de duplicado apareció de todas formas, sin esa
causa técnica. Lo que el nuevo instrumento (3) agrega es que tampoco
puede llamarse "sin ningún asidero": al menos una parte de los pares
señalados muestra solapamiento estructural sustancial, medido, no
asumido.

---

## `n_agentes=3` — explicado, no es anomalía

Firma_CKM reporta `n_agentes: 3` al cierre en ambos runs, con solo 2
`AgentDeviceSkin` corriendo. Mecanismo ya conocido de sesiones previas,
no nuevo: `CKMMonitor._devices_seen` (`iap_chatroom/ckm_monitor.py:69,92`)
es un set que acumula `message.device_id` de **todo** mensaje
procesado, incluidos los joins con `device_id="system"`. 2 skins +
`"system"` = 3. Verificado contra el código, no solo repetido de
memoria. A diferencia del corte de 86 caracteres sin explicar de Caso
0.10 (que sí sigue abierto), esto no es un pendiente.

---

## Pendientes

- Baseline de Jaccard sobre `activos_relajado` para pares consecutivos
  del mismo hablante en conversación *no* recursiva sobre significado
  — sin eso no se puede calibrar si 0.85 (visto en R2 t=5→t=6 y t=7→t=8)
  es redundancia real o solapamiento esperable en cualquier intercambio
  sostenido de un tema. Es la verificación abierta más concreta que
  dejó este caso.
- Relacionado: aislar si el patrón de reclamos de duplicado depende del
  tema de la conversación (significado/interpretación/drift — un tema
  que gira sobre sí mismo) o es más general en discusión extendida
  Sonnet-vs-Sonnet — mismo diseño, tema no relacionado a comunicación.
- Caso 0.9: hetero-provider + join simultáneo, mono-provider Groq —
  siguen sin correr (pendiente heredado de la sesión anterior).
- No se probó 2 skins con objetivos en conflicto explícito (adversarial)
  — este caso fue orientaciones distintas pero no diseñadas para
  chocar.

---

## Archivos relacionados

- `registers/REG_hint_next_instance_v7.md` — hint que dejó este caso
  incompleto, con la secuencia exacta seguida acá
- `registers/REG_iap_caso_09_v1.md`, `REG_iap_caso_10_v1.md` — bug de
  max_tokens y sus notas retroactivas
- `iap_chatroom/test_caso_11_two_skins.py` — script de esta corrida,
  sin modificar
- `iap_chatroom/agent_device_skin.py` — `AgentDeviceSkin`,
  `build_goal_directed_agent`
- `process/*_1784817039_caso11_run2` — backup real de Run 1 (ver nota
  de labeling)
- `process/*_1784817413_caso11_run2` — backup real de Run 2

---

*Jul 23 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
