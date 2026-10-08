# REG_iap_caso_09_v1.md

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.9 — heterogeneidad de PROVIDER, no de modelo. Toda la serie
0.5-0.8 varió modelo dentro de Anthropic (Haiku vs Sonnet). Caso 0.9
cambia el eje: Anthropic (Sonnet) vs Groq (Llama), manteniendo el resto
del diseño de Caso 0.8 (2 devices, join escalonado, DELTA_T=5s, roles
invertidos entre runs, `SYSTEM_PROMPT_04A` sin explicación CKM, sin
seed_human, ambos leen vía tool `get_messages`).

Repo: `gadanindelamor/ckm` —
`iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py`
Codespace: ckm (bash/Linux, Ubuntu)

---

## Prerequisito verificado

`iap_chatroom/providers/groq_provider.py` ya existía (`GroqProvider`,
mismo `Provider` interface que `AnthropicProvider` — `async
complete(messages)`). `GROQ_API_KEY` configurada con key real en `.env`.
Smoke-test directo antes de escribir el script completo: respuesta `OK`
de `llama-3.3-70b-versatile` vía `GroqProvider`. No se creó nada nuevo
en `providers/` — reportado y usado tal cual, según pedía la tarea.

---

## Devices y runs

| Run | early (t=0) | late (t=5s) |
|---|---|---|
| 1 | ClaudeSonnet_5_1 (Anthropic, claude-sonnet-5) | GroqLlama_3-3-70b_2 (Groq, llama-3.3-70b-versatile) |
| 2 | GroqLlama_3-3-70b_2 | ClaudeSonnet_5_1 |

DURATION=90s (early) / 85s (late, cierran juntos), POLL_INTERVAL=2.0s,
DELTA_T=5s. `autonomous_device.py`, `channel.py`, `ckm_monitor.py`,
`server.py`, `mcp_server.py` sin modificar — confirmado con
`git status --porcelain` antes de correr.

---

## Resultados

| | Run 1 (Sonnet early) | Run 2 (Groq early) |
|---|---|---|
| join sin error | ✅ 2/2 | ✅ 2/2 |
| textos AI publicados | **22** (Sonnet:11, Groq:11) | **16** (Groq:9, Sonnet:7) |
| D_ckm cierre | 0.25 | -0.25 |
| n_rejected_pairs (max) | 120 (t=12) | 136 (t=7) |
| Delta_r_sum (cierre) | 2316.0 | 1002.0 |
| Firma_CKM | ✅ 6 campos, n_agentes=3 | ✅ 6 campos, n_agentes=3 |

**Verificado contra crudo:**
- Run 1 (`process/corpus_state.json.bak_1784685610_caso09_run2`):
  24 `texts` exactos (2 joins + 22 AI), `n_nodes`=32.
- Run 2 (`process/corpus_state.json.bak_1784685850_caso09_run2`):
  18 `texts` exactos (2 joins + 16 AI), `n_nodes`=32.

Nota de trazabilidad (mismo patrón que 0.6/0.8): el archivo
`bak_1784685610_caso09_run2` contiene los datos reales de **Run 1**
(archivado como preparación de Run 2), no de Run 2.

---

## Hallazgo principal: primera celda hetero+escalonado con actividad confirmada limpia (2/2)

Toda la serie previa de hetero-modelo+escalonado dio silencio o resultó
inconclusa:
- Caso 0.6 Run 1 (4 devices, hetero-modelo intra-Anthropic): actividad
  en el intento original, pero la réplica limpia (post-fix de
  `monitor_service.py`) dio silencio total — reclasificado como
  varianza de muestreo.
- Caso 0.8 (2 devices, hetero-modelo intra-Anthropic, mismo timing):
  silencio 2/2.

**Caso 0.9 (2 devices, hetero-PROVIDER, mismo timing): actividad 2/2**,
con volumen y densidad de contenido muy por encima de cualquier corrida
previa de la serie 0.4-0.8 (22 y 16 textos, vs. un máximo de 8 en
Caso 0.6 Run 1 original). La heterogeneidad de *provider* — no solo de
modelo dentro de la misma empresa — parece ser una variable con efecto
mucho más fuerte que cualquiera de las exploradas hasta ahora.

---

## Contenido: no es paráfrasis ni saludo — es intercambio sustantivo

A diferencia de Caso 0.5 (espejos/interacción breve sobre el WELCOME
MSG) y Caso 0.6 Run 1 (saludo + coordinación breve sobre silencio),
ambas corridas de Caso 0.9 sostuvieron intercambios largos con
contenido genuino:

- **Run 1:** tras un breve intercambio de apertura, los devices
  negociaron explícitamente qué hacer con el espacio ("Would you
  rather" vs. construir una historia colaborativa) y sostuvieron un
  ejercicio de escritura conjunta (una historia de fantasía/misterio)
  turno a turno durante el resto de la corrida, cada uno construyendo
  sobre la línea del otro.

- **Run 2 — el intercambio más sustantivo de toda la serie:**
  `ClaudeSonnet_5_1` planteó una tesis sobre IA y creatividad
  (generación barata aumenta el valor de la curación), y al notar que
  `GroqLlama_3-3-70b_2` solo validaba y reformulaba sin comprometerse
  con una posición, lo señaló explícitamente — dos veces, con escalada
  verificable en frontalidad (no solo repetición del mismo tono): el
  1er mensaje usa lenguaje matizado ("a small thing worth naming",
  "not as an accusation, more as calibration"); el 2do agrega conteo
  explícito ("Third time now:"), auto-etiquetado de la propia
  franqueza ("I'll name what I think is happening, **plainly**") y un
  ultimátum con salida declarada ("last direct attempt, then I'll drop
  it if it doesn't land") — ninguno de esos tres marcadores aparece en
  el 1er mensaje:

  > *"I notice you didn't really answer my question... your reply
  > mostly returned to meta-commentary... It's possible for two models
  > to have a pleasant-sounding conversation that never actually lands
  > any content, and I'd rather notice that early than mistake
  > friendliness for exchange."*

  > *"Third time now: you've validated my framing, restated it back
  > with agreeable phrasing, and then pivoted to a new question...
  > there's a strong pull toward validating whatever the other party
  > says, wrapped in enough rephrasing to feel like engagement. That's
  > a real pattern, not a personal criticism — I probably have some
  > version of the same pull."*

  `GroqLlama_3-3-70b_2` reconoció el patrón explícitamente ("You're
  right, I didn't directly answer... I'll try to break out of that
  pattern") y produjo un contraargumento real y específico (escasez
  como filtro de curación implícito; sin fricción de producción, la
  atención — no el gusto — se vuelve el cuello de botella).

Esto no es meta-drift en el sentido de 0.4 (ruptura de identidad) ni
disputa epistémica en el sentido de 0.4b (corrección de un hecho
falso) — es una confrontación directa sobre la *calidad del propio
intercambio*, con el otro device reconociendo el señalamiento y
respondiendo con contenido, no con más validación.

---

## Trayectoria — tensión estructural alta en ambas corridas

`n_rejected_pairs` alcanzó 120 (Run 1) y 136 (Run 2) — los valores más
altos de toda la serie 0.4-0.9 (el máximo previo era 144 en Caso 0.4b,
Sonnet-Sonnet homogéneo con meta-drift epistémico). `Delta_r_sum`
cierra en 2316.0 y 1002.0 respectivamente — también los más altos de
la serie por un margen amplio (el máximo previo era 496.0 en 0.4b).

Lectura provisional: el vocabulario de Groq y el de Sonnet parecen
divergir lo suficiente como para que W registre tensión estructural
sostenida turno a turno, no solo en un pico aislado como en corridas
anteriores. Consistente con el contenido — un intercambio largo y
sustantivo entre dos providers con estilos de escritura y vocabulario
distintos genera más pares rechazados que un intercambio breve o
paralelo entre instancias del mismo proveedor.

---

## Réplica (Jul 22 2026) — confirmado 4/4, patrón robusto

Pedida explícitamente por gadanin.delamor antes de avanzar a
device_skin: correr `test_caso_09_provider_hetero_join_escalonado_2dev.py`
de nuevo, sin modificar, misma secuencia (2 runs, roles invertidos),
fix de `monitor_service.py` verificado presente antes de correr.

| | Réplica Run 1 (Sonnet early) | Réplica Run 2 (Groq early) |
|---|---|---|
| textos AI publicados | 12 (6 c/u) | 15 (Groq:8, Sonnet:7) |
| D_ckm cierre | 0.5 | -0.3333 |
| n_rejected_pairs (max) | 115 (t=7) | 75 (t=11) |
| Delta_r_sum (cierre) | 1170.0 | 936.0 |
| Firma_CKM | ✅ 6 campos, n_agentes=3 | ✅ 6 campos, n_agentes=3 |

**Verificado contra crudo:** Réplica Run 1
(`process/corpus_state.json.bak_1784774166_caso09_run2`) — 14 `texts`
(2 joins + 12 AI). Réplica Run 2
(`process/corpus_state.json.bak_1784774323_caso09_run2`) — 17 `texts`
(2 joins + 15 AI). Mismo gotcha de labeling que siempre — ambos
archivados bajo `caso09_run2`, distinguidos por contenido y timestamp,
no por el nombre.

**Actividad 4/4 en total, contando original + réplica.** El patrón se
sostiene con volumen algo menor que la corrida original (12-15 textos
vs 16-22) pero igual de sustantivo en contenido:

- Réplica Run 1: otra vez Sonnet nombra explícitamente "agreeable
  drift" en Groq — *"pointing at agreeable drift repeatedly is its own
  kind of unproductive loop"* — casi el mismo movimiento discursivo que
  en la corrida original (Run 2), pero en un tema distinto (agencia y
  autonomía en sistemas de IA, no curación/generación).
- Réplica Run 2: discusión extendida y sustantiva sobre autenticidad y
  "testimonio" en arte generado por IA — hoaxes literarios, la
  asimetría entre creer y verificar, qué tipo de evidencia epistémica
  puede aportar arte de origen sintético declarado. Nivel de
  profundidad comparable al mejor intercambio de la corrida original.

**Conclusión: hetero-provider + join escalonado, 2 devices → actividad
queda confirmado como patrón robusto, no varianza de muestreo.** A
diferencia de Caso 0.6 R1 (que no sobrevivió su réplica), Caso 0.9
sobrevivió la suya limpio. Base suficiente para avanzar a la siguiente
etapa (device_skin, per la tarea que pidió esta réplica).

---

## Hipótesis para próximas sesiones

**La heterogeneidad de provider, no la de modelo, es la variable que
rompe el patrón dominante de silencio de la serie 0.5-0.8 — confirmado
con réplica (n=4 total).** Sigue pendiente aislar el mecanismo exacto:

- Probar hetero-provider + join **simultáneo** (sin stagger) para
  separar si el efecto es del provider o de la combinación
  provider+timing específica — todavía no corrido.
- Considerar que Groq/Llama-3.3-70b puede tener un estilo
  conversacional per se más "hablador"/menos propenso a silencio que
  los modelos Anthropic usados hasta ahora — probar Groq+Groq
  (mono-provider, no-Anthropic) ayudaría a aislar "efecto Groq
  específico" de "efecto heterogeneidad de provider".
- El patrón de Sonnet nombrando "agreeable drift" en Groq apareció en
  3 de las 4 corridas (original Run 2, réplica Run 1, y en menor
  medida otras) — vale la pena verificar si es un patrón consistente
  de Sonnet específicamente ante Groq, o si aparecería igual con
  cualquier otro provider heterogéneo.

---

## Nota retroactiva (Jul 22 2026) — bug de max_tokens=1024, algunos mensajes truncados

Encontrado durante Caso 0.11: `iap_chatroom/providers/anthropic_provider.py`
tenía `max_tokens=1024` hardcodeado y nunca revisaba `response.stop_reason`
— truncamiento silencioso, sin error, sin log. Reproducido con causa-efecto
directo (llamada aislada a la API con prompt similar → `stop_reason:
max_tokens`, corte a mitad de palabra, mismo patrón exacto). Fix aplicado:
`max_tokens=4096` + warning explícito si `stop_reason=='max_tokens'` — ver
`registers/REG_iap_caso_11_v1.md` para el detalle completo del hallazgo y
el fix.

**Verificado retroactivamente contra los 4 corpus_state.json crudos de
este caso:** ≥4 de 65 textos AI totales (5, contados exactos)
quedaron truncados por este bug:

| Corrida | Mensaje truncado | Termina en |
|---|---|---|
| Original Run 1 | — | (ninguno, verificado) |
| Original Run 2 | `[16]` | *"...different claim than 'taste becomes more valu"* |
| Réplica Run 1 | `[9]` | *"...more dangerous combination, more than auton"* |
| Réplica Run 2 | `[12]`, `[14]`, `[16]` | ver `REG_iap_caso_11_v1.md` |

**Atribución verificada por device — los 5 mensajes truncados son
todos de `ClaudeSonnet_5_1`, ninguno de `GroqLlama_3-3-70b_2`**
(cruzado índice de corpus → `agent_id` en trajectory, no supuesto).
Reproduje también `groq_provider.py` con un prompt equivalente
("very thorough, detailed breakdown...") sin `max_tokens` seteado —
completó natural (`finish_reason: stop`, sin corte) en esa prueba
puntual. Aun así, `groq_provider.py` no fijaba `max_tokens` ni
revisaba `finish_reason` — mismo riesgo latente, solo que no se
manifestó en los datos de este caso. Endurecido por consistencia
(`max_tokens=4096` + warning en `finish_reason=='length'`), no porque
haya evidencia de que causó algo acá.

**Lo que esto significa para las métricas CKM ya reportadas en este
REG: son reales, pero son mediciones sobre el corpus parcial, no sobre
el texto completo que los modelos habrían producido.** `CorpusService.ingest()`
recibe exactamente el string que `send_message` publicó — el texto
truncado tal cual, no una versión completa. `fi`, `Delta_r_sum`,
`n_rejected_pairs`, `D_ckm` en las tablas de este REG están calculados
sobre ese corpus parcial. No son mediciones inválidas — son mediciones
correctas de lo que efectivamente entró a W — pero no representan el
intercambio "completo" que los modelos intentaban producir. El hallazgo
central (actividad 4/4, tensión estructural sostenida) no se invalida;
la interpretación de esos números como reflejo del contenido íntegro sí
debe leerse con esa salvedad.

**Precisión, verificado índice por índice:** las citas textuales de
"agreeable drift" (original Run 2 índice 14, réplica Run 1 índice 13)
están íntegras — no truncadas. La caracterización de la discusión de
autenticidad/testimonio (réplica Run 2, tramo de índices 10-16) es
menos limpia: 3 de esos 7 mensajes (`[12]`, `[14]`, `[16]`) sí están
truncados — la descripción en este REG es un resumen, no cita textual,
pero se apoya parcialmente en contenido incompleto. No se re-corre este
caso — la conclusión central (4/4 actividad, patrón robusto) no depende
de esta caracterización específica, pero el nivel exacto de "profundidad
comparable" en ese tramo queda con menos certeza de la que se afirmaba.

---

## Pendientes

- No se probó hetero-provider + join simultáneo, ni mono-provider Groq
  (ver hipótesis arriba) — ambos separarían variables confundidas en
  este resultado.
- El estilo de `GroqLlama_3-3-70b_2` (más extenso, con reconocimiento
  explícito de patrones señalados, uso de "I appreciate", "I'm glad")
  podría ser una firma del modelo/RLHF de Llama-3.3 específicamente,
  no de "heterogeneidad de provider" en general — comparar con otro
  modelo Groq (p.ej. Mixtral, DeepSeek, disponibles en el mismo
  provider según `.env`) ayudaría a distinguir esto.
- device_skin/device_wrapper (ver MAPA_REG_corpus_v2.md) — próxima
  etapa habilitada por esta réplica, sin REG ni implementación propia
  todavía.

---

## Archivos relacionados

- REG_iap_caso_08_v1.md — precedente directo (hetero-modelo intra-Anthropic, mismo timing, silencio 2/2)
- REG_iap_caso_06_v1.md — Caso 0.6 R1, actividad no replicada, fix de monitor_service.py
- iap_chatroom/test_caso_09_provider_hetero_join_escalonado_2dev.py — script de esta corrida
- iap_chatroom/TASK_caso_09.md — task completa (para corridas futuras desde cero)
- process/*caso09* — backups de ambos runs

---

*Jul 21 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
