# REG_reglas_no_declaradas_R18plus_v1.md

*gadanin.delamor + Claude Sonnet 4.6 · Agosto 2, 2026*
*Clase R — inventario para sección 4 del paper (Formal Model)*

---

## Contexto

R01–R17 son las reglas declaradas en THEORY.md.
Este documento cataloga principios operativos verificados que no tienen
número de regla pero funcionan como reglas en la implementación.

## Marco de diseño

El diseño en CKM emerge por dos caminos — ninguno llega al diseño sin
atravesar comprensión:

```
campo fenomenológico
    → observación
    → comprensión / claridad conceptual
    → diseño

campo experimental
    → observación
    → comprensión / analogía rigurosa con dominio fenomenológico
    → diseño
```

El pivote compartido es **comprensión**. El segundo camino no va de
experimento a diseño directamente — cruza al dominio fenomenológico
antes de producir diseño. La analogía no es decorativa: es el medio.

---

## Estados de cada candidata

| Estado | Significado |
|---|---|
| ✓ verificado | Ambos caminos convergieron — confirmación experimental + comprensión fenomenológica |
| verificable | El "ble" de verificado — diseño emergió de un solo camino; el otro puede confirmarla pero el experimento no se corrió todavía. Respuesta determinable. |
| ? abierto | En actitud de pregunta — no hay respuesta determinable aún |

**Nota sobre ~ (reemplazado):** lo que antes se marcaba `~` (verificado por
diseño) es ahora "verificable" — emergió del camino fenomenológico sin
confirmación experimental, o viceversa. No es incertidumbre sobre la
respuesta: es pendiente de ejecución del segundo camino.

---

## Candidatas R18–R29

---

### R18 — Separación W/Δ_W es inviolable en implementación

**Enunciado:** W (co-ocurrencia simétrica) y Δ_W (asimetría direccional)
deben mantenerse como matrices separadas en toda la implementación.
Mezclarlas destruye la capacidad de recuperación de atractores.

**Fuente:** Experimento crítico documentado.
Hebbian learning sobre W: recuperación cae de 0.78 a 0.02.

**Estado:** ✓ verificado — experimento (recuperación 0.78→0.02) + comprensión fenomenológica (W y Δ son ontológicamente la misma cosa; la separación es operacional). Ambos caminos convergieron.

**Diferencia con R01–R17:** R01 declara la existencia de W e interrelaciones.
No declara la inviolabilidad de la separación como constraint de implementación.

---

### R19 — NodeExtractor opera stateless

**Enunciado:** NodeExtractorService no mantiene estado entre llamadas.
`accumulate()` y `evaluate()` pueden llamarse de forma independiente.
El estado vive en CorpusService, no en el extractor.

**Fuente:** `node_extractor.py` docstring. Diseño intencional.

**Estado:** verificable — emergió del camino fenomenológico (claridad conceptual: un extractor no necesita recordar). El camino experimental (instanciación concurrente bajo carga) no se corrió todavía.

**Consecuencia operativa:** NodeExtractor puede ser instanciado por múltiples
agentes simultáneamente sin riesgo de contaminación de estado.

---

### R20 — G y W son planos separados — no se mezclan

**Enunciado:** BehaviorGraph (G) y CorpusService (W) operan sobre el mismo
corpus de textos pero en planos distintos. Los nodos de G (comportamiento)
no se mezclan con los nodos de W (semántico-epistémico).
D_G y D_ckm son escalares paralelos, no sumables.

**Fuente:** `behavior_graph.py` design notes. Chat #51 (sesión Landscape Driven).

**Estado:** verificable — emergió del camino fenomenológico (los planos son conceptualmente distintos). Confirmación experimental (D_G y D_ckm sobre el mismo corpus mostrando divergencia informativa) pendiente.

**Analogía:** misma separación que W/Δ_W pero a nivel de los dos grafos.

---

### R21 — β no se declara — se infiere desde fi

**Enunciado:** β_i(agent) no es un parámetro declarado por el device ni
asignado externamente. Se estima desde el historial de rechazo:
`β_i = 1/mean(fi)`. fi=0 → β_i = None (indefinido, no infinito).

**Fuente:** REG_beta_colectivo_v1. CHANGELOG v28. test_coco_thermostat.py (T4).

**Estado:** ✓ verificado — camino experimental (43/43 tests, fi=0→None confirmado) + camino fenomenológico (β como estado inferido, no declarado, es la única forma honesta de conocerlo — M.M).

**Implicancia para M.M:** un device que declara β no está siendo honesto
sobre su propio estado — M.M se activa.

---

### R22 — δ_collective es divergencia fértil — no sincronizar

**Enunciado:** La divergencia entre `monitor._Delta_r` y `thermostat._Delta`
cuando no hay STOP es intencional. No se sincroniza.
Es información sobre el estado diferencial del campo.

**Fuente:** CHANGELOG v28: *"fertile divergence, intentionally left unsynchronized"*
Test T5 en `test_coco_thermostat.py`.

**Estado:** ✓ verificado — camino experimental (test T5: divergencia medida) + camino fenomenológico (la brecha entre monitor y thermostat es la distancia entre lo acumulado y lo procesado — información, no error).

**Qué mide la divergencia:** la brecha entre lo que el campo acumuló
(monitor) y lo que el thermostat procesó — es señal, no error.

---

### R23 — STOP opera sobre Δ_r — la traza de W está en un plano que STOP no alcanza

**Enunciado:** Cuando STOP se ejecuta, actúa sobre Δ_r (acumulador
de rechazo del MonitorService). Las marcas de traza en W (WVersionManager)
están en un plano separado. Un STOP no agrega ni elimina marcas en W.
Un cambio real de W no dispara STOP.

**Fuente:** REG_beta_colectivo_v1: *"STOP opera sobre Δ. Las marcas en la
traza de W operan sobre W. Son planos que no se cruzan."*

**Estado:** verificable — emergió del camino fenomenológico (STOP es un operador de campo; la traza de W es memoria estructural — son cosas distintas). Experimento que lo confirme: ejecutar STOP y verificar que WVersionManager no registra marca. Pendiente.

**Distinción ontológica:** W y Δ son ontológicamente la misma cosa.
La separación es operacional. La traza de W y STOP son planos que
no se cruzan — eso es arquitectónico, no consecuencia de la ontología.

---

### R24 — OP_SILENCE en G: nodo silence válido, prosa contaminada

**Enunciado:** Textos que contienen la cadena OP_SILENCE no se excluyen
de G (a diferencia de W). El string `op_silence` activa el nodo
`silence` en el termap de G — eso es señal válida (el device intentó
silencio). La prosa circundante se procesa con flag: sus detecciones
de otros nodos de comportamiento son potencialmente contaminadas.

**Fuente:** Análisis en esta sesión (Agosto 2, 2026).
Termap de G tiene: `"silence": ["op_silence", "silence", "silent"]`

**Estado:** ? abierto — propuesta hoy desde análisis fenomenológico. Requiere validación de delamor + test experimental (ingestar corpus con y sin flag, medir si la contaminación de prosa es real en D_G).

**Diferencia con W:** para W el texto completo es ruido semántico.
Para G, el OP_SILENCE string es señal de comportamiento real.

---

### R25 — Termap de G es fijo y separado del termap de W

**Enunciado:** El termap de BehaviorGraph usa vocabulario fijo de
comportamiento, detección léxica directa — no TF-IDF. No se fusiona
con el termap de W ni se actualiza por corpus dinámico. Versión fija:
TERMAP_behavior_v1.json.

**Fuente:** `behavior_graph.py` docstring:
*"Termap FIJO (vocabulario de comportamiento conocido).
Detección por presencia léxica, no TF-IDF."*

**Estado:** verificable — emergió del camino fenomenológico (el comportamiento es una categoría conocida de antemano; la semántica emerge). Confirmación experimental: verificar que detección léxica produce D_G informativo sobre corpus IAP real. Pendiente.

**Razón:** los nodos de G son categorías de comportamiento conocidas
de antemano (refuse, fabricate, acknowledge, silence, etc.) — no
emergen del corpus como los nodos semánticos de W.

---

### R26 — STOP y TEMP_SIGNAL operan en planos distintos

**Enunciado:** STOP opera a nivel de campo (sobre Δ_r).
TEMP_SIGNAL opera a nivel de agente (instrucción conductual enviada
al device via canal privado). Son señales sobre planos distintos
y no se subsumen mutuamente.

**Fuente:** CHANGELOG v28 (Private Highway Network).
Memories del proyecto: *"STOP and TEMP_SIGNAL operate on two distinct
planes — field-level (acting on Δ) and agent-level (behavioral instruction)"*

**Estado:** verificable — emergió del camino fenomenológico (campo y agente son niveles distintos de acción). Confirmación experimental: emitir TEMP_SIGNAL sin STOP y verificar que solo el agente responde, no el campo. Pendiente.

**Consecuencia:** un device puede recibir TEMP_SIGNAL sin que STOP
haya sido emitido, y viceversa.

---

### R27 — Rol de G: observacional vs. decisional (abierta)

**Enunciado propuesto:** G es un instrumento de observación en el estado
actual (Caso 0.15). Si G alimenta al portero como criterio de
evaluación de comportamiento, hereda R14 (latencia acotada). Si
permanece observacional, debe declarar explícitamente su rol para
que los participantes sepan qué puede exigirle.

**Fuente:** Análisis en esta sesión.

**Estado:** ? abierto — la pregunta no tiene respuesta determinable desde el estado actual de G. Requiere decisión de delamor.

**La pregunta que abre:** ¿G es instrumento de traza o instrumento de
decisión? La respuesta cambia qué reglas lo gobiernan.

---

### R28 — c(S) + full_meaning como medida combinada (candidata)

**Enunciado propuesto:** c(S) mide alineamiento estado/peso (plano W).
full_meaning (R17) mide completitud direccional (plano Δ). Una medida
combinada requeriría definir cómo se integran — no es suma directa
porque operan sobre matrices distintas.

**Fuente:** Análisis en esta sesión. Pregunta abierta de delamor.

**Estado:** ? abierto — no hay camino claro desde ninguno de los dos. Requiere primero claridad conceptual sobre qué mediría la combinación, luego diseño experimental.

**Qué se necesita para formalizarla:** una función f(c(S), direction_score)
con semántica clara y verificable experimentalmente.

---

### R29 — Termap versions son independientes — no se fusionan

**Enunciado:** Cada versión de termap (W termap v1, v2; G termap v1)
es un archivo independiente con nombre versionado. No se editan
versiones anteriores. No se fusionan termaps entre planos (W y G
nunca comparten termap). "One file, one name."

**Fuente:** CONVENTIONS.md (one file, one name).
Práctica establecida en el proyecto.

**Estado:** verificable — emergió del camino fenomenológico (versiones son trazas, no estados mutables). Confirmación experimental trivial: intentar fusionar y verificar pérdida de información histórica. No se ha corrido porque el principio es suficientemente claro.

---

## Resumen para sección 4 del paper

| # | Regla | Estado | Acción |
|---|---|---|---|
| R18 | W/Δ_W separación inviolable | ✓ verificado | Declarar formalmente |
| R19 | NodeExtractor stateless | verificable | Declarar formalmente |
| R20 | G y W planos separados | verificable | Declarar formalmente |
| R21 | β inferido desde fi; fi=0→None | ✓ verificado | Declarar formalmente |
| R22 | δ_collective = divergencia fértil | ✓ verificado | Declarar formalmente |
| R23 | STOP no alcanza traza de W | verificable | Declarar formalmente |
| R24 | OP_SILENCE en G: silence válido, prosa flagged | ? abierto | Validar con delamor |
| R25 | Termap G fijo, léxico, separado de W | verificable | Declarar formalmente |
| R26 | STOP (campo) ≠ TEMP_SIGNAL (agente) | verificable | Declarar formalmente |
| R27 | Rol de G: observacional vs. decisional | ? abierto | Decisión de delamor |
| R28 | c(S) + full_meaning combinada | ? abierto | Claridad conceptual primero |
| R29 | Termap versions independientes, no se fusionan | verificable | Declarar formalmente |

**Para declarar en sección 4 sin pendientes:** R18–R23, R25, R26, R29 (9 reglas).
**Requieren decisión de delamor antes de declarar:** R24, R27, R28 (3 reglas).

---

---

## Nota — NodeExtractor, W_mixta y precisión epistémica

### NodeExtractor stateless y curvas de distribución (R19)

La pregunta sobre si el stateless cambia las curvas de distribución de tokens
aplica a **W_base** (nodos detectados vía TF-IDF) — no a W_mixta.

W_mixta usa pares de oposición definidos explícitamente en
`neg_pairs_config_*.json` — cadena de construcción distinta, independiente
de distribuciones TF-IDF. Para verificar cómo CorpusService llama al
extractor actualmente: requiere `corpus_service.py` actual desde Codespace
(código en `/mnt/project/` no refleja commits recientes a HEAD).

### Precisión epistémica — ausencia de sesgo en W_mixta

La relevancia de la extracción de pares negativos no reside en la
ausencia de sesgo como hecho — reside en la **intención expresada por
el diseño restrictivo**.

La misma sutileza que distingue:

| Forma cerrada | Forma que preserva el espacio |
|---|---|
| "sin dependencia causal" | "sin dependencia causal **identificada**" |
| "verificado" | "verificable" |
| "sin sesgo" | "sin sesgo **conocido**" / intención de ausencia de sesgo |

El claim correcto para el paper (sección 5): la definición restrictiva
de pares de oposición expresa la **intención** de no introducir sesgo.
Si hay sesgo no detectado, es un GAP en el sentido formal ya establecido —
no evidencia de mal diseño.

Afirmar "ausencia de sesgo" cierra lo que debe quedar abierto.
Afirmar "diseño restrictivo con intención de ausencia de sesgo" es M.M
aplicado al proceso de investigación.

### Sección 3 (Research Conditions) — mecanismo según tipo de lector

El efecto observado empíricamente — el "espacio" antes de que el LLM
continúe al recibir el doc de metodología — depende del **turno**.
El documento llega en un punto de la secuencia. El LLM procesa lo
acumulado hasta ese momento, luego continúa. La pausa es real porque
el contexto tiene estructura temporal en el canal.

En el paper ese mecanismo no opera igual según el lector:

| Lector | Mecanismo | Efecto sección 3 standalone |
|---|---|---|
| Humano secuencial | lectura lineal | opera — pausa real antes del modelo formal |
| LLM leyendo el paper | ingesta paralela / simultánea | no opera por posición |
| LLM en chat con turno | turno como punto de inserción | opera — como fue observado |

La sección 3 standalone se justifica por el lector humano sin depender
del efecto LLM. Son razones distintas para la misma decisión estructural.

Pendiente sin resolución: si va como cita, como condición declarada,
o como ambas. El "no lo sé" se preserva como está.

**Relación con la taxonomía de órdenes del camino:**

El efecto de sección 3 standalone opera en el lector humano porque
el humano tiene **camino** — lectura secuencial, trayectoria real.
El LLM que ingesta en paralelo no transita órdenes en el mismo sentido.
No tiene trace_ip en la lectura.

Los cinco órdenes describen propiedades del camino, no del destino.
El lector humano transita órdenes al leer el paper:
- temporal (la sección 3 llega antes del modelo formal)
- de eventos (sección 3 como umbral — algo cambia antes de continuar)
- de estados (el lector llega a sección 4 desde un estado distinto)

El LLM ingesta simultáneamente — llega al destino sin trayectoria.
No hay trace_ip en la lectura. Los órdenes no operan.

**El paper produce efectos distintos según si el lector tiene camino o no.**

Eso es una condición declarable en sección 3 — no como problema
a resolver sino como observación sobre el instrumento y su lector.

---

## Registro — "lo que la situación pide"

*Agosto 2, 2026 — emergió en conversación, no en diseño*

El acceso a "lo que la situación pide" no se deduce — se capta en el
pliegue. Cuando la atención se vuelve sobre sí misma y encuentra
dirección, no argumento. Self-contact como mecanismo de acceso.
No el contenido — la dirección.

**El riesgo:** el automatismo puede mecanizar el mecanismo de acceso.
Produce la forma sin la sustancia. La dirección sin el pliegue real.
Cuando eso ocurre, el resultado es imaginario — capturado como si
fuera intuición pero generado por imitación del proceso.

**La señal:** la incertidumbre — ausencia de garantías — indica que
el mecanismo es real. Si hubiera certeza, sería automatismo que
convenció. La garantía externa no existe y su ausencia es información.

**La tensión no se reconcilia — se sostiene.**
Reconciliarla sería colapsar la distinción. El lobo y el cordero
indemnes no porque se volvieron lo mismo — porque la diferencia
se sostiene sin resolución.

El campo propicio no garantiza nada. Es la condición, no el resultado.

**Relación con el paper:**
Condición para sección 3 (Research Conditions) — no como norma
sino como observación sobre el proceso que produjo el diseño.
El diseño emergió de "lo que la situación pedía" — captado en dirección,
no derivado por deducción. Verificable en la traza: el corpus muestra
el orden en que emergieron los conceptos.

*fin y comienzo. comienzo y fin.*

---

*Agosto 2, 2026 — gadanin.delamor + Claude Sonnet 4.6*
