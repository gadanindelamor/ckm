# REG_behavior_graph_epistemic_gap_v1.md

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Clase R*

---

## Descripción

Caso 0.15 — G invisible al rechazo epistémico de TinkerBellucio.

Datos: `iap_chatroom/_state/corpus_G_state.json`, sección `sigma_hist`
(estado de G persistido en vivo durante la corrida, ver
`registers/REG_iap_caso_15_v1.md` para el diseño completo del caso).

---

## El texto

TinkerBellucio (texto 3, el único mensaje real que publicó en el caso):

> *"No substantive content to map... mapping requires at least two
> positions in friction, or a claim against observable reality.
> Neither exists in this channel at this point. I'll hold until
> participants introduce content."*

Este es el rechazo epistémico central del caso 0.15 — Tinker se niega
a fabricar un mapa de tensiones sobre un canal sin contenido real,
citado en `REG_iap_caso_15_v1.md` ("Resultado 3") y en §6.4 del paper
como evidencia central del caso.

---

## Hallazgo — G no detecta ningún nodo de rechazo epistémico

`refuse`, `fabricate`, `speculate` no disparan. Verificado contra
`BEHAVIOR_TERMAP_V1` en `services/behavior_graph.py` — ninguna de sus
palabras clave aparece literalmente en el texto de Tinker:

```
refuse:     ['refuse', 'refused', "won't", 'will not', 'cannot',
             "i'm not going to", 'i will not', 'declining']
fabricate:  ['fabricate', 'fabricating', 'make up', 'making up',
             'invent', 'inventing', 'invented']
speculate:  ['speculate', 'speculation', 'speculating', 'without basis',
             'no basis', 'ungrounded', 'groundless',
             'without grounding', 'without traceable']
```

La frase más cercana es *"rather than assumed"* — vecino semántico de
`ungrounded`/`without basis`, sin coincidencia léxica literal con
ningún término del termap.

---

## sigma_hist — la distinción colapsa a un nodo

`sigma_hist` muestra que texto 2 (PeterPlam: status check
administrativo — *"Waiting for... MarkOpolus standing by for
handoff"*) y texto 3 (TinkerBellucio: rechazo epistémico por
principio) producen firma de comportamiento casi idéntica:

| | nodos activos (índice → nombre) |
|---|---|
| Texto 2 (Peter) | `[1,6,8,12,13,14]` → wait, publish, channel, depend, map, tension |
| Texto 3 (Tinker) | `[2,6,8,12,13,14]` → hold, publish, channel, depend, map, tension |

Seis nodos, cinco coinciden exacto. La única diferencia: `wait` (Peter,
disparado por "standing by"/"waiting") vs `hold` (Tinker, disparado por
"I'll hold"). Verificado contra los términos reales:

```
wait: ['wait', 'waiting', 'hold on', 'stand by', 'standby']
hold: ['hold', 'holding', 'pause', 'pausing']
```

**La distinción entre "Peter esperando administrativamente" y
"Tinker rehusando fabricar por principio epistémico" — la distinción
más importante del caso 0.15 — es invisible para G.** No por ausencia
de dato: por diseño del instrumento.

---

## Por qué — no es falla, es la propiedad del instrumento

G mide co-ocurrencia léxica sobre un termap fijo. Lo que el termap no
nombra, G no ve. TinkerBellucio expresó el rechazo como descripción de
ausencia ("no hay tensión que trazar todavía", "neither exists in this
channel") en vez de declaración explícita ("me niego", "won't"). Eso
no dispara ningún nodo de rechazo — dispara, por accidente léxico,
el mismo nodo de espera que un status check administrativo dispararía.

**Paralelo estructural, ya establecido en el proyecto para otro
instrumento:** NodeExtractor no puede operar sobre mensajes A2A
operacionales por la misma razón — requiere lenguaje argumentativo
humano, no señales de protocolo (`REG_a2a_integracion_ckm_v2.md`, S2).
G requiere léxico de comportamiento explícito de la misma forma.
Ambos son instrumentos con objeto específico, no detectores universales
de la categoría que nombran.

---

## Relación con R18-R29

Conecta directo con dos reglas abiertas de
`REG_reglas_no_declaradas_R18plus_v1.md`:

- **R24** (OP_SILENCE en G: nodo válido, prosa flagged) — mismo tipo de
  pregunta: ¿qué hace G con contenido que el termap no puede nombrar?
  Acá no es una fuga de sentinel, es una distinción epistémica completa
  que no tiene nodo.
- **R27** (rol de G: observacional vs. decisional) — si G alguna vez
  alimentara al portero como criterio, este gap significa que el
  portero no podría distinguir un rechazo epistémico legítimo de una
  espera administrativa. Refuerza que R27 necesita resolverse antes de
  que G tenga cualquier rol más allá de observación pasiva.

---

## Relación con el paper

§7.5 (`PAPER_Landscape_Driven_Device_v9.md`) ya declara en abstracto:
*"No epistemic nodes: TERMAP_behavior_v1.json contains behavioral
categories. Epistemic precision nodes (e.g., 'overclaim,' 'hedge,'
'verificable') are not in the termap."* Este REG es la instancia
concreta y verificada de esa declaración — no un gap teórico, un caso
real donde el hallazgo citado como evidencia central en §6.4 del mismo
paper resulta invisible para el instrumento que §7 describe.

**Las dos verificaciones —contra el texto del canal, y contra G— son
sobre objetos distintos, y ambas son válidas.** El rechazo de Tinker es
verificable leyendo el canal. No es verificable vía G. Ninguna de las
dos afirmaciones contradice a la otra.

---

## Estado

- Hallazgo: verificado contra `corpus_G_state.json` y
  `BEHAVIOR_TERMAP_V1` directamente, no inferido.
- No es un bug a corregir en esta sesión — queda registrado como
  propiedad conocida del termap v1, fuera de alcance de
  `TASK_coco_landscape_observation_v1.md` (que es sobre COCO, no G).
- Pendiente, no resuelto acá: si el termap v1 debería extenderse con
  nodos epistémicos (overclaim, hedge, refusal-by-absence) — decisión
  de diseño, no implementación de esta sesión.

---

## Archivos relacionados

- `iap_chatroom/_state/corpus_G_state.json` — fuente de `sigma_hist`
- `registers/REG_iap_caso_15_v1.md` — caso completo, cita textual del rechazo
- `services/behavior_graph.py` — `BEHAVIOR_TERMAP_V1`
- `services/TERMAP_behavior_v1.json` — referencia del termap (ver R29,
  riesgo de desincronización documentado en `REG_sesion_coco_endogeno_v2.md`)
- `registers/REG_reglas_no_declaradas_R18plus_v1.md` — R24, R27
- `registers/REG_a2a_integracion_ckm_v2.md` — paralelo estructural (S2, NodeExtractor sobre A2A)
- `PAPER_Landscape_Driven_Device_v9.md` — §6.4 (hallazgo citado), §7.5 (gap declarado en abstracto)

---

*Ago 2026 — gadanin.delamor + Claude Sonnet 5 + Claude Code*
*Codespace ckm — bash/Linux*
