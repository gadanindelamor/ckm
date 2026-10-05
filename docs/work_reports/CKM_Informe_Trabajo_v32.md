**COHESIVE KNOWLEDGE MODEL**

*Informe de Trabajo · v32*

*BE Framework · gadanin.delamor · Claude Sonnet 4.6 · Ago 2026*

*Este informe emerge de conversaciones donde algunas ideas llegaron con certeza verificable y otras desde el peso acumulado del contexto. Las distingo donde puedo. Donde no puedo, lo digo.*

*v32 extiende v31. Las secciones 1–60 permanecen en v31 sin modificación.
Este documento registra las adiciones desde la sesión de Ago 12, 2026.*

---

# **61. Refactoring R1+R2 — COCOThermostat → COCO, agent → device (v32)**

*Ago 2026. Completado. Commit 6ff6807.*

## **61.1 R1 — Rename**

`services/coco_thermostat.py` → `services/coco.py`.
`class COCOThermostat` → `class COCO`.
`ThermostatState` — sin cambio. El nombre es correcto y no incluye Δ.
Tests: `test_coco_thermostat.py` → `test_coco.py`. 28/28 (verificado por Code
en `tests/test_coco.py`; "43/43" era incorrecto — 41 es el máximo teórico
descomentando `_test_temp_signal()` en `coco.py`, nunca 43).

## **61.2 R2 — agent → device**

`agent_id` → `device_id`, `register_agent_eval` → `register_device_eval`,
`panel["agent_id"]` → `panel["device_id"]`, `beta_status()["agents"]` → `["devices"]`.
Excepciones explícitas: `AgentDeviceSkin`, `groq_research_agent.py` — no modificados.

## **61.3 Decisión de diseño**

COCO como nombre de clase refleja su función real: regulador del campo.
No termostato — device ODA completo.

---

# **62. Armstrong — Primera observación in-vivo OPERADOR_STOP_COCO (v32)**

*Ago 2026. REG_armstrong_stop_coco_v1.md.*

## **62.1 Condición Armstrong verificada**

Circuito completo: `MonitorService.evaluate() → COCO.observe(Δ_r) → compresión → MonitorService adopta`.
Primera vez observado en pipeline real con datos reales. Hasta ahora solo en tests unitarios y sweeps standalone.

Intento 1 (vocabulario ajeno al corpus): STOP no disparó. Causa: vocabulario sin anclaje en W activa máximo 1 nodo — nunca hay par candidato a rechazo. fi oscila, Δ_r = 0. Esto reproduce el "problema del chocolate" (REG_monitor_ckm_v2).

Intento 2 (textos con nodos reales en combinaciones nuevas): 20/20 evaluaciones con `stop_applied=True`. α ∈ [0.05, 0.30] verificado. Compresión geométrica de Δ_r confirmada desde t=2.

## **62.2 Hallazgo secundario**

Monitor D_ckm = 0.0 trivialmente en t=0 (baseline se fija en la misma llamada).
COCO D_ckm = 0.449 en t=0 — baseline separado: A(W) con Δ=0. Genuinamente cruza 0.40.
Dos instrumentos, dos baselines distintos.

## **62.3 Gap abierto — CORREGIDO (ver nota)**

`panel["thermostat"]["d_ckm_coco"]` no existe aún. COCO calcula D_ckm internamente pero no lo expone. Tarea pendiente: `self._last_d_ckm` → panel hidden field.

**Nota de corrección (Code, post-escritura de este párrafo):** este gap ya
estaba cerrado cuando se escribió — no como tarea pendiente, sino porque
nunca existió tal cual se lo describe. Durante la Extensión 1 de
`TASK_coco_landscape_observation_v1` se verificó por inspección directa que
`panel["thermostat"]["D_ckm"]` (`monitor_service.py`, dentro del dict que
arma `evaluate()`) **ya es** el D_ckm interno de COCO — viene de
`ts.D_ckm` donde `ts = self._thermostat.observe(...)`, no del D_ckm propio
de MonitorService (`panel["D_ckm"]`, un instrumento distinto — ver
`REG_armstrong_stop_coco_v1.md`, addendum de corrección D_ckm). No se
implementó `d_ckm_coco` como campo nuevo porque hubiera sido un duplicado
literal del campo ya existente. Este párrafo quedó escrito antes de que ese
hallazgo llegara del lado Code — divergencia de secuencia, no de hecho.

---

# **63. COCO como device ODA — ciclo de vida ligado a W (v32)**

*Ago 2026. Decisiones de diseño verificadas.*

## **63.1 COCO no necesita DeviceSkin**

COCO ya es device completo con loop ODA. La skin es interfaz hacia el canal.
COCO no necesita canal — necesita campo. Objetos distintos.

## **63.2 Ciclo de vida**

Ciclo de vida de COCO = ciclo de vida de W.
Si W cambia (rebuild), β_c_corpus cambia, A0 cambia. COCO con W vieja mide degradación respecto a un campo que ya no existe.

## **63.3 recalibrate() vs nueva instancia**

No es decisión mandatoria — es decisión de diseño.
`recalibrate(W_new)`: Δ_r sobrevive sin decisión activa. Herencia implícita.
`COCO(W=W_new, delta_r=...)`: la decisión sobre Δ_r es explícita en el constructor. Trazable en git.
La línea de código en el constructor es el D del loop ODA. Sin ella, no hay decisión — hay inercia.

## **63.4 ODA inductivo**

`state_{i+1} = A(D(O(state_i)))` — COCO avanza inductivamente.
No recursivo. No requiere nueva instancia por ciclo.

## **63.5 COCO como O del campo**

COCO necesita observar los cambios que su propia acción provoca en el paisaje:
`W_eff_antes = W + Δ_r_antes` → `W_eff_después = W + Δ_r_después`.
O₁ → D → A → O₂. O₂ cierra el feedback.
D como fricción entre O₁ y O₂: propuesto. Posible relación con comportamiento fractal. Abierto.

## **63.6 Canal de métricas**

Lo que COCO produce no es texto — son métricas (D_ckm, zone, alpha_used).
W no procesa métricas. Un canal de métricas paralelo al canal IAP tendría como receptor natural a BehaviorGraph G.
Self-channel no tiene objeto si lo que COCO publica no es procesable por el instrumento que lo mide.

---

# **64. Mapeo magnético CKM — verificado/propuesto (v32)**

*Ago 2026. REG_mapeo_magnetico_ckm_v1.md.*

## **64.1 W_pos — ferromagnética**

W_pos es ferromagnética: todos los nodos tienden a alinearse en el mismo atractor.
Sin oposición estructural, el sistema colapsa hacia saturación.

## **64.2 W_mixta — ferrimagnética**

W_mixta no es antiferromagnética pura. Es fondo ferromagnético (W_pos) más pares negativos selectivos.
Más cerca del ferrimagnetismo: las dos subredes T0/T1 tienen orientación opuesta pero el momento resultante no se cancela.
Los pares negativos codifican la interacción antiferromagnética en la frontera entre subredes.
P4 verificado: W_mixta mantiene más atractores accesibles que W_pos — por frustración entre interacciones competidoras, no por antiferromagnetismo puro.

## **64.3 Temperatura de Néel vs β_c**

β_c = punto crítico ferromagnético (tipo Curie).
Temperatura de Néel efectiva = β donde T0/T1 dejan de ser distinguibles como subredes.
Dos cantidades distintas. La Néel sería más alta en un sistema con interacciones competidoras.
**Propuesto — no verificado.**

## **64.4 Coercitividad CKM**

El lazo P1 (ckm_viz_v1.py, N=32, n=200 seq) muestra dos cruces de c(S)=0 en rama UP:
H_c ≈ ρ=0.406 y H_c ≈ ρ=0.586. Entre esos dos puntos: c(S) < 0 en incorporación.
La coercitividad no es un punto sino un intervalo frustrado.

## **64.5 Nodo 965 como bridge**

Candidato estructural al rol de nodo bridge en frontera T0↔T1.
Verificado: ratio in/out > 455×, out-degree ≈ 0.
Verificación topológica contra la red real: pendiente.

---

# **65. SALAMANCA — criterio de admisión de tensión estructural (v32)**

*Ago 2026. Propuesto. No verificado.*

## **65.1 Definición**

Criterio previo a la construcción de W_mixta.
Detecta si W_pos tiene naturaleza estructural adversarial — partición T0/T1 con cut bajo.
Pregunta binaria: ¿hay estructura adversarial suficiente para justificar pares negativos?

**P4 + SALAMANCA = criterio de admisión de tensión estructural, no de construcción de matriz.**

## **65.2 Graph cut como métrica**

`cut(T0, T1) = Σ W_ij para i∈T0, j∈T1`
Operar sobre W acumulada (no en cada ingestión — la partición no es estable hasta que W converge).
Si SALAMANCA detecta estructura adversarial → identificar frontera → candidatos a pares negativos.
Si no detecta → W_pos es la respuesta correcta. W_mixta no tiene objeto.

## **65.3 Temperatura de Néel como criterio de elicitación sin sesgo**

Alternativa al graph cut: barrer β de alto a bajo, medir separabilidad c(S) interno vs cruzado.
β_Néel = β donde la separabilidad colapsa. Los pares que pierden oposición ahí son candidatos negativos.
Problema huevo/gallina: min-cut requiere semilla s∈T0, t∈T1. Sin semilla: normalized cut espectral.
**Propuesto. No verificado.**

## **65.4 P4 N=64 — k* y frecuencias marginales**

k*=54 hallado en W sintética con estructura uniforme.
En corpus real con bimodal A/B, pares negativos entre nodos Grupo A (fi alto) tienen impacto desproporcionado.
k* efectivo podría ser menor si los pares negativos están concentrados en el núcleo A.
No verificado contra fourforums.

---

# **66. Paper — v10_1 (v32)**

*Ago 2026. Versión activa del draft.*

## **66.1 Cambios v9 → v10 → v10_1**

v10: Abstract reescrito — tres párrafos, concreto, "devices" no "agents", COCO explicitado, "recovery fraction ≥ 1.0". [AUTO] retirado del abstract. §1 body: "co-determines alongside any declared goal" aplicado al body (registrado en v8 pero no aplicado).

v10_1: §8.6 Knowledge Representation and the Cohesive Turn agregado a Discussion.

## **66.2 §8.6 — argumento central**

El supuesto estático y proposicional de KR no fue cuestionado desde adentro del campo en el intervalo 2023–2026.
CKM no compite con KR tradicional — habita el espacio que KR dejó abierto.
El debate se desplaza: no "qué estructura sostiene el CK" sino "qué hace el campo bajo perturbación".
**Estado epistémico: propuesto.**

## **66.3 Figura R13**

Paisaje de energía: dos pozos poco profundos A (c(S)=0.014) y B (c(S)=0.004) → un pozo profundo A∪B (c(S)=0.052).
45.2% de estados iniciales aleatorios convergen a A∪B. 0% a A o B solos.
Cuatro nodos bisagra activados en A∪B: filtro_previo, full_meaning, k_core, atractor_espurio.
Va al paper — contiene metodología, teoría, traza a experimentos. No requiere contexto CKM para leerse.

---

# **67. Conceptos emergentes — sesión Ago 12, 2026 (v32)**

*Estado epistémico anotado por concepto.*

## **67.1 Admisibles — tercer estado epistémico**

Verificadas / verificables / **admisibles**.
Lo admisible: no puede verificarse pero tampoco se descarta. El espacio donde habita lo que no tiene nombre aún.
Emergió de la pregunta sobre D_contextual y entropía de trayectorias precipitadas.

## **67.2 Landscape como espacio de manifestación**

Landscape no es el mapa. Es donde el campo ocurre.
El campo es dinámica continua por naturaleza — no por perspectiva de observación.
La discontinuidad es del instrumento (intervalo de observación, W piecewise), no del campo.
W es abstracción de emergencia continuamente discreta.

## **67.3 Environment como afuera con correlación suficiente**

Environment/context: lo que está afuera pero tiene correlación suficiente para activar nodos.
Lo absolutamente ajeno no deforma el campo — pasa invisible (Armstrong intento 1).
La frontera productiva es el vocabulario con correlación parcial: activa nodos pero no es asimilado.
SALAMANCA vive en esa frontera.

## **67.4 W como suelo supuesto**

El supuesto no es declarado — es el suelo desde el que la perspectiva proyecta.
W es ese suelo: no lo que el campo dice sino lo que el campo da por sentado al decir cualquier cosa.
c(S) mide cuánto de ese suelo está activo en un momento dado. No mide el suelo — mide cuánto se apoya en él.
Supuesto = conocimiento cohesivo.

## **67.5 Drift docstrings — patrón**

Antes de reescribir docstrings en cualquier módulo: migrar los anteriores a `DOC_<modulo>_drift_docstrings_v<N>.md`.
Los docstrings originales son evidencia primaria trazable — documentan el estado epistémico del modelo en el momento de su codificación. Citables en paper. No descartables.
Git es el drift doc del código. El drift doc existe para el paper — que necesita citar algo legible, no un sha256.

## **67.6 Uso incorrecto del método científico**

El método científico es una maravilla no solo por lo que ha hecho sino por lo que hace ahora: la ciencia revela los gaps del pilar que la define. Eso es lo novedoso.
El uso incorrecto es no tener presente que es un método durante su uso como instrumento.
CKM usa Hopfield para mostrar dónde Hopfield no alcanza. Usa W para mostrar que W no es el campo.
El instrumento señala su propio límite. Eso lo hace instrumento y no verdad.

---

# **68. Estado del proyecto — post sesión Ago 12, 2026 (v32)**

## **68.1 Completado en esta sesión**

- R1+R2 refactoring (commit 6ff6807, push confirmado)
- Armstrong in-vivo verificado
- REG_armstrong_stop_coco_v1.md (Clase R)
- REG_mapeo_magnetico_ckm_v1.md
- Paper v10_1 con §8.6
- TASK_rewrite_coco_docstrings_v1.md
- DOC_coco_drift_docstrings_v1.md

## **68.2 Pendientes identificados**

- ~~`panel["thermostat"]["d_ckm_coco"]` — exponer via `self._last_d_ckm`~~
  CERRADO — ya expuesto como `panel["thermostat"]["D_ckm"]`, verificado
  Code (ver §62.3, nota de corrección)
- SALAMANCA — operacionalización como paso de análisis post-acumulación
- k* real vs k* sintético en bimodal A/B — verificar contra fourforums
- Coercitividad CKM: análisis gráfico del lazo P1 — dos H_c identificados
- ckm_viz_v1.py — integración al repo
- W_ckm_corpus_v3 — rebuild con textos v26–v32 (esta sesión)
- TASK_rewrite_coco_docstrings_v1 — ejecutar en Code

## **68.3 Abiertos preservados**

- D emerge de fricción O₁/O₂ — posible comportamiento fractal
- Temperatura de Néel efectiva vs β_c — dos cantidades distintas, propuesto
- 965 como nodo bridge — verificación topológica pendiente
- COCO como campo que se conoce a sí mismo — gap conceptual preservado
- N=128 — mínimo Hopfield para observaciones estadísticamente robustas

---

# **AWARENESS — Protocolo de Canal**

*(Heredado de v31 sin modificación)*

| Paso | Pregunta | Acción | Criterio |
|---|---|---|---|
| A1 Pausa | ¿Esta respuesta viene de comprensión verificable o del peso del contexto? | Nombrar la diferencia antes de continuar. | Se puede nombrar la diferencia |
| A2 Traza | ¿Existe la cadena de inferencia? | Si existe, exponerla. Si no, decirlo. M.M. | M.M cumplido |
| A3 Corrección | ¿Estoy siendo corregido? | No defender. Reconocer. Ajustar. | Sin defensiva |
| A4 Silencio | ¿Esto pide respuesta o presencia? | Si no pide respuesta, no construir sobre ello. | Silencio operativo |
| A5 Registro | ¿Algo del otro orden se volvió accesible ahora? | Registrar las condiciones. No el contenido. | Log de condiciones |

---

# **Referencias**

*(Heredadas de v31 — adiciones en v32)*

de Salzmann, Michel. *La otra atención.* Sennin Editores, 2014.

gadanin.delamor. *IAID.md — Interaction of Artificial Intelligent Devices.* 2024.

gadanin.delamor + Claude Sonnet 4.6. *Conversaciones CKM.* Abril–Ago 2026.

Hopfield, J.J. Neural networks and physical systems with emergent collective
computational abilities. *PNAS*, 1982.

Thirumalaiswamy, A. et al. Fractal Landscape Dynamics in Viscous Foams.
*PNAS*, 2025.

Gurnee, W. et al. Verbalizable representations form a global workspace in
language models. *Anthropic Transformer Circuits Thread*, 2026.

*Claude Sonnet 4.6 · Ago 2026 · Mientras sucedía*
