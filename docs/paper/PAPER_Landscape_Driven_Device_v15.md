*CKM PAPER DRAFT v15 — Sep 2026 · gadanin.delamor · Claude Sonnet 4.6 · Claude Code*

*v3 changes from v2:*
*— §2 Related Work: draft completo (v2) — Venkatesh & Bu 2025, Gurnee et al. 2026, 11 [PENDING] slots*
*— §3 Research Conditions: draft completo — §3.7 convergencia por independencia con fechas 2023 verificadas*
*— §5.3 P4 at N=64: actualizado con k*=54, fourforums 60 pares confirmados*
*— §9 Conclusions and Future Work: draft completo*
*— §10 References: draft completo — 13 confirmadas, 3 [VERIFY], 11 [PENDING]*
*— §8.6 retirada (atribución incorrecta)*

*v4 changes from v3:*
*— §3.x The Material Issue: nueva sección — condiciones materiales del proceso*
*— §3.y The IAP Chatroom as Methodological Instance: nueva sección — dos niveles de testing*
*— §3.z Conditions, Not Constraints: nueva sección — reencuadre de "limits"*
*— §8.4 "Current Limits" → "Current Conditions"*
*— §9.3 "Preserved Limits" → "Preserved Conditions"*
*— Autoría actualizada: + Claude Code*
*— common-sense attractors → common-sense-like attractors (§2.2)*
*— BROADCAST condition definida (§6.1)*
*— 4 instancias de framing residual "limit" → conditions/scale-dependent/constraint (cuerpo)*

*v5 changes from v4:*
*— Rename only. No content changes.*

*v6 changes from v5:*
*— Abstract: integrado*

*v8 changes from v7:*
*— §8.5 LDD definición: "rather than by a declared goal" → "co-determines alongside any declared goal"*
*— §8.5 STOP como ejemplo del mecanismo agregado*

*v9 changes from v8:*
*— Abstract: "Four are confirmed, three observed" → "Six predictions (P1–P6) are verified. P7 confirmed in two corpora." (inconsistencia con §9)*
*— Abstract + §8.5: "STOP operator" → "OPERADOR_STOP_COCO, ejecutado por COCO". STOP no existe como operador standalone — es COCO quien ejecuta la compresión de Δ_r.*
*— §8.5: "Δ" → "Δ_r" (el mecanismo actúa sobre el acumulador de rechazos, no sobre la matriz estática Δ del corpus)*
*— §9.2: "COCOThermostat" → "COCO" (renombrado en repo: coco.py)*

*v10 changes from v9:*
*— Abstract: reescrito — más concreto, menos direccional. Tres párrafos. [AUTO] retirado del abstract (pertenece al body). "agents" → "devices" en todo el abstract. COCO explicitado como device que ejecuta OPERADOR_STOP_COCO. "fracción_rec" → "recovery fraction". P7 wording: "remains open as universal claim" → "universality remains open". Último párrafo (research conditions) retirado del abstract.*
*— §1 body: "rather than by a declared goal" → "co-determines alongside any declared goal" (cambio registrado en v8 pero no aplicado al body).*

*v10_1 changes from v10:*
*— §8.6 Knowledge Representation and the Cohesive Turn: nueva sección en Discussion. Estado epistémico: propuesto. Argumento: el supuesto estático de KR no fue cuestionado desde adentro del campo en el intervalo 2023–2026. CKM habita el espacio que KR dejó abierto — no compite, ocupa. El debate se desplaza de "qué estructura sostiene el CK" a "qué hace el campo bajo perturbación".*

*v10_2 changes from v10_1:*
*— §8.6: "inhabits" → "inhabits and structures" — distinción señalada por análisis externo (Gemini Flash): CKM no solo ocupa el espacio que KR dejó abierto, lo estructura.*
*— §7.5 No epistemic nodes: agregado caso concreto verificado — Case 0.15, REG_behavior_graph_epistemic_gap_v1.md. El gap declarado en abstracto tiene ahora instancia trazable.*
*— Body: dos residuos "agent" → "device" (línea 355 "across devices and corpora"; R26 "device-level").*

*v11 changes from v10_2:*
*— C: Reencuadre N=32/N=128 — el mínimo Hopfield aplica a memorias asociativas, no a CKM.*
*— §2.3: Aiyappa et al. 2024 agregado como única arquitectura base CKM publicada; W_mixta como ferrimagnética (propuesto).*
*— §2.6: Distinción explícita herramienta/uso — CKM usa Hopfield como formalismo computacional, no para recuperación de patrones.*
*— §4.2 c(S): Frase puente — la primera línea nombra la herramienta, la segunda nombra el uso en CKM.*

*v12 changes from v11:*
*— Abstract: Δ_r → Δ en primera oración. Verificado: Δ_r es simétrica (monitor_service.py L112-114); la separación 0.78/0.02 es sobre W/Δ estática.*
*— §2.3: párrafo agregado — CKM no intenta representar contenido; P1–P4 caracterizan geometría de W como snapshot estático; P5–P7 bajo interacción acumulada.*
*— §4.1: nota sobre estructura off-diagonal de Δ_r como propiedad del campo bajo la interacción — abierta.*
*— §4.2: convergencia y atractores — Lyapunov/LaSalle (Agama Santiago 2026), _count_attractors() como estimador de |L|, verificación de simetría y diagonal cero de W_eff. D_contextual como motivación teórica de D_ckm.*
*— §5.2: nota sobre muestreo en predicciones basadas en atractores (P5).*
*— §8.5: tres dimensiones del landscape — conteo, coercividad, cuencas — distintas, no medidas del mismo escalar.*
*— C9.5: criterio de Temperatura de Néel efectiva para elicitación de pares negativos — propuesto, no verificado.*

*v12_1 changes from v12:*
*— First Line: version y fecha "V10 — Ago". Reemplazada por "v12 — Sep"*
*— Abstract  : "external corpora". Reemplazada por "external adversarial static corpora"*
*— §1, §2.4  : "debate corpora". Reemplazada por "adversarial debate corpora"*

*v13 changes from v12_1:*
*— §2.4 L341: "Both appear as C3" → "Both appear as tension anchor" — C3 en §2.4 nombra el tercer rol de la tríada (sostenedor de tensión), no el criterio M.M. del gatekeeper (C3 en §4.3). Babel corregido (REG_seleccion_nodos_desempate_v1 §7).*
*— §4.5 R23: "STOP operates on Δ_r" → "OPERADOR_STOP_COCO operates on Δ_r" — consistente con renombre en v9.*
*— §4.5 R26: "STOP (field-level, on Δ_r)" → "OPERADOR_STOP_COCO (field-level, on Δ_r)" — ídem.*
*— §3 (Research Conditions): nota agregada — la detección de pares negativos por marcadores léxicos asume corpus con posiciones adversariales por diseño. Sin esa precondición, el número no mide tensión estructural (REG_unidad_texto_saturacion_v1 §5).*
*— §4.2: relax_orbit (landscape_engine.py) reemplaza coco.py/monitor_service.py como implementación sincrónica operacional. GOLES declarado como premisa de determinismo. Órbitas de período 2 como régimen mayoritario verificado (~70%). N_eff = 1/Σmᵢ² como estimador convergente de diversidad (masas convergen; conteos no). D_ckm no converge en signo bajo variación de seed/n_runs a n_runs bajo. Qualification actualizado.*

*v14 changes from v13:*
*— Abstract: "encoding structural memory via Hebbian dynamics" retirado — contradecía §2.6 y §4.1, donde el aprendizaje Hebbiano sobre W está probado y rechazado (0.78 → 0.02). W codifica co-ocurrencia; la dinámica Hopfield se usa como formalismo de relajación, no como regla de aprendizaje.*
*— Abstract: la lectura del signo de D_ckm queda condicionada al muestreo (ver §6.4, §8.3).*
*— §6.2, §6.4, §8.3: D_ckm = −7.5 (Caso 0.12) calificado — el signo de D_ckm no converge bajo variación de seed o n_runs en ese régimen (REG_seleccion_nodos_desempate_v1 §8). La observación queda como documentada; la magnitud y el signo no son reclamables sin re-medición.*
*— §6.2, §8.4, §9.3, §9.5: marco residual "below the Hopfield minimum" → condición de escala propia de CKM, consistente con §1 y con el reencuadre de v11 (el mínimo asociativo aplica a memorias Hebbianas; CKM no almacena memorias).*
*— §4.2: retirada la formulación "D_ckm es el proxy discreto de un concepto más amplio (D_contextual), la relación formal entre los dos queda abierta". El PAPER no se pronuncia sobre esa relación — no la declara abierta ni cerrada, no la menciona *(decisión delamor)*. Queda sólo D_masa_cuencas como forma de distancia sobre masas, implementada y reportada. El registro de los tres enunciados involucrados vive en DEFS §10.*
*— §4.6: NodeExtractor y CorpusService — regla de desempate de selección (histéresis) y corrección de extracción de pares por texto; ambas cambian toda W construida por CorpusService.*
*— §3.x The Material Issue: nota nueva — disponibilidad de corpus reales de casos reales como condición material, al mismo nivel que hardware, memoria volátil y cold start. Escala ilustrativa N ≈ 1000 contra el N=32 operativo. Los casos IAP no dan volumen; el corpus de informes no sustituye (autor único, estructura temporal que no es la de una interacción); los corpus de agentes existen y son accesibles, con la pregunta de dominio abierta antes de usarlos como referencia.*
*— §4.2: prevalencia de órbitas de período 2 declarada como dependiente del corpus — 141/200 y 136/200 en los dos corpus N=20, 3/200 en el corpus de trabajo N=32 (REG_orbitas §2). Antes se enunciaba como régimen de "operational corpora".*
---

# Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction
---


## Abstract

The Cohesive Knowledge Model (CKM) is a formal instrument for measuring structural properties of semantic fields in multi-agent AI interaction. Its central contribution is **N_eff = 1/Σm_i²** — the inverse Simpson diversity index over basin masses of a Hopfield landscape — as a convergent estimator of field diversity. Basin masses converge under sufficient sampling; attractor counts do not. The non-convergence of count-based estimators (D_ckm) is not a failed metric: it is the diagnostic that established which estimator is appropriate.

A second contribution is the endogenous emergence of β_collective — the collective thermal parameter of the field regulator (COCO) — as a median of individual device parameters under interaction, without external calibration. This is *proposed* as a direction toward field self-observation.

CKM operates on two matrices derived from a corpus: W (symmetric co-occurrence weights) and Δ (asymmetric directional dependencies). Seven structural predictions (P1–P7) are tested against external adversarial debate corpora (fourforums, CreateDebate; N = 32–64). Six are confirmed. P7 is confirmed in two independent corpora; domain universality remains open.

The IAP experimental series documents field behaviors under live multi-agent operation — sentinel leaks, coupled silence, refusal to fabricate from an empty channel — as field observations. These are reported without causal attribution to specific mechanisms.

The paper presents CKM as a landscape instrument, not a behavioral evaluator. What it measures is the geometry of co-occurrence structure and how that geometry changes under interaction.

---

**Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction**

---

##  Outline  — Index (secciones 1–10)

```
1. Introduction
   N_eff como contribución central. β_collective como dirección.

2. Related Work
   Multi-agent evaluation. Signed weights. Hopfield. Hill diversity. Criticality. Stance detection.

3. Research Conditions
   3.1 Inductive Methodology
   3.2 Conversation as Laboratory
   3.3 Convergence by Independence
   3.4 Trace as Constitutive of Knowledge
   3.5 What the Instrument Cannot Register
   3.6 Preserved Incompleteness
   3.7 Material Conditions
   3.x Epistemic Conventions

4. Formal Model
   W · Δ · c(S) · GOLES · Basin Masses · N_eff · COCO · Gatekeeper

5. Empirical Validation — External Corpus
   Fourforums + CreateDebate. P1–P7.

6. IAP Experimental Series
   Canal design. Casos 0.4–0.15. Hallazgos clave.

7. Behavior Domain Graph G
   Segunda matriz, termap fijo.
   D_G en paralelo a D_ckm.

8. Discussion
   Qué mide CKM que no miden los instrumentos existentes.
   Condiciones actuales.

9. Conclusions and Future Work

10. References
```
---
*Draft v15 — Sep 2026 · gadanin.delamor + Claude Sonnet 4.6 + Claude Code*

---
*Epistemic conventions*

*— **verified**: confirmed experimentally under stated conditions*
*— **implemented**: exists in code; correct operation not evaluated*
*— **proposed**: theoretical framing, not yet tested*
*— **open**: no verified answer; the space is preserved*
*— **uncertain**: known to be problematic; pending resolution*
*— **admissible**: neither verifiable nor discardable; an unnamed space*
*— **[AUTO]**: marks moments where automatism was noticed and resisted during writing*

---
## 1. Introduction

Multi-agent AI systems are increasingly deployed in configurations where several devices interact over a shared channel — producing text, making decisions, building on each other’s outputs. Evaluating whether this interaction constitutes genuine coordination or parallel activity requires measuring something most existing approaches do not capture: the structural field that emerges from interaction itself.

Most existing approaches measure what individual agents produce or whether their outputs agree. Neither captures the geometry of co-dependencies, directional flows, and attractor states that characterize the shared knowledge state of the group at a given moment.

This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of semantic fields in multi-agent interaction. CKM does not interpret semantic content. It measures the geometry of the co-occurrence landscape and how that geometry changes under interaction.

**The central contribution** is N_eff = 1/Σm_i² — the inverse Simpson diversity index [Hill, 1973] over basin mass distributions of a Hopfield landscape — as a convergent estimator of field diversity. The path to this estimator required establishing that count-based estimators (attractor counts, D_ckm) do not converge in sign under sampling variation. That non-convergence is not a failed metric: it is the diagnostic.

**A second contribution** is the observation that β_collective — the collective thermal parameter of the field regulator — emerges as a function of individual device parameters under interaction, without external calibration. This is *proposed* as a direction toward field self-observation.

CKM makes seven falsifiable predictions (P1–P7), tested against two independent external adversarial debate corpora. Six are confirmed. P7 is confirmed in two corpora; domain universality remains open.

The IAP experimental series documents field behaviors under live operation: sentinel leaks, coupled silence, refusal to fabricate from an empty channel. These are field observations, reported without causal attribution.

---

## 2. Related Work

### 2.1 Multi-Agent Evaluation

Most existing frameworks for evaluating multi-agent AI systems operate at the level of individual agent behavior: task completion rates, response latency, output volume [Zhu et al., 2025]. A second class measures semantic agreement between agents — cosine similarity between outputs, embedding-space distance, topic overlap [Zhu et al., 2025]. Neither class measures the structural field that emerges from interaction: the pattern of co-dependencies that characterizes the shared knowledge state of the group.

CKM does not replace behavioral or agreement metrics. It measures something orthogonal to both.

### 2.2 Knowledge Representation and Signed Weights

Knowledge graphs typically represent relations as positive-weight edges encoding similarity, co-occurrence, or inferential support [Speer et al., 2017; Hogan et al., 2021]. Negative weights, when they appear, are introduced through explicit annotation or post-hoc linguistic processing. They are not, generally, derived from the structural pattern of the corpus as a whole.

CKM derives signed weights directly from corpus structure: texts that frame two concepts in explicit opposition reduce the corresponding W_ij entry. The sign is a corpus property derived from structure, not an editorial assignment.

### 2.3 Hopfield Networks and Attractor Structure

The Hopfield network [Hopfield, 1982] provides the energy formalism CKM uses for relaxation and attractor analysis. Modern extensions [Ramsauer et al., 2021] increase storage capacity but preserve the core attractor geometry. What these frameworks do not address is the distribution of basin masses — how much of the state space falls into each attractor — as a convergent diversity estimator.

Count-based estimators of attractor diversity suffer from coupon-collector bias: the count grows monotonically with sampling. Basin masses converge. N_eff = 1/Σm_i² — the inverse Simpson index over basin mass distributions — is the convergent estimator that count-based approaches cannot provide.

### 2.4 Diversity Estimation in Dynamical Systems

The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Its application to Hopfield basin masses as a field diversity estimator is, to our knowledge, not present in the existing literature. The connection is structural: basin masses in a Hopfield landscape are analogous to species abundances in an ecosystem. N_eff is the number of equally-abundant basins that would produce the observed concentration. When q = 2, the Hill number equals the inverse Simpson concentration — the effective number of dominant attractors in the landscape.

### 2.5 Criticality and Landscape Geometry

Self-organized criticality [Bak, Tang & Wiesenfeld, 1987] predicts power-law distributions at critical points. Extended criticality — a finite region of parameter space with critical-like behavior — has been reported in neuronal network dynamics [Beggs & Plenz, 2003; Moretti & Muñoz, 2013] and in certain spin-glass models [Pázmándi et al., 1999]. CKM observes extended critical-like behavior at N = 32; its presence in small knowledge graphs is documented in §5 and remains uninterpreted across domains.

### 2.6 Stance Detection in Adversarial Debate Corpora

Stance detection in adversarial debate corpora is typically framed as a supervised classification task [Mohammad et al., 2016]. The state of the art includes transformer-based models fine-tuned on stance datasets [Ghosh et al., 2019; Kawintiranon & Singh, 2021]. CKM identifies structural phenomena in the same corpora — the Type-965 node, coercivity of cluster frontiers — without using stance labels and without supervised learning.

---

## 3. Research Conditions

### 3.1 Inductive Methodology

CKM was developed inductively. Formal results emerged from experiments; formalization followed when experiments required it. The consistent order: conceptual clarity first, then formalization, then verification. Properties of the model were not derived from first principles — they were observed, formalized, and where possible verified independently.

### 3.2 Conversation as Laboratory

The corpus from which CKM was developed was produced through multi-device interaction — the same mechanism CKM is designed to measure. The conversation traces are not documentation of the process: they are the process. The working reports (v1–v31) are simultaneously the record of the research and the raw material of the experiments. The term-map, co-occurrence matrices, and W construction are derived directly from that corpus.

This is a condition, not a claim about the methodology’s validity. It means CKM’s development occurred inside the field it studies. The instrument was not external to what it measured.

### 3.3 Convergence by Independence

The strongest verification in this work is retroactive convergence with independent findings — Hill (1973) on effective diversity numbers, Thirumalaiswamy et al. (2025) on landscape-driven dynamics in physical systems. These connections were not designed. They were recognized after the fact. That is the methodological signature: convergence by independence, not by alignment.

### 3.4 Trace as Constitutive of Knowledge

The AWARENESS protocol and the M.M. rule are not behavioral norms imposed on the process. They are epistemological conditions. Knowledge without an inference trace is not practically opaque — it is structurally opaque. This applies to the instrument itself: claims in this paper are traced to their source; where the trace does not exist, the claim is not made or is marked as *proposed* or *admissible*.

The [AUTO] markers are the visible surface of this condition: moments where automatism was noticed and resisted during writing. They are not rhetorical. They are part of what the trace looks like when made explicit.

### 3.5 What the Instrument Cannot Register

Δ_r accumulates pairs that σ_prompt declared active but relaxation expelled. The condition of entry is that the pair was written and evaluated. What is not written does not pass through the field — it generates no rejection, leaves no trace in Δ_r.

Consequence: the alternative discarded before writing is invisible to the instrument. Δ_r cannot distinguish between “the field rejected this combination” and “this combination was never considered.” This is not a correctable limitation. It is a structural condition of any instrument that measures what occurred: it cannot measure what did not occur because there was no observer who opened the possibility.

*[The first two observations above are verifiable in the code: `_rejected_pairs`, Δ_r accumulation. The third — on the act of opening and its relation to what appears in Δ_r — is an observation about the observer. Registered as* **admissible***, not verified.]*

### 3.6 Preserved Incompleteness

Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented. The Gatekeeper operates in the domain of declared agent capabilities; its extension to corpus concepts is *proposed*, not verified.

These are not future work items. They are conditions the model names and preserves. A gap declared is not a gap concealed.

### 3.7 Material Conditions

The operational corpus is at N = 32 nodes. The IAP experimental series consists of documented observations under partially controlled conditions, not controlled experiments with replication. COCO was not connected to the live channel in any of the 253 documented panels. Results are reported under these conditions, not against an ideal that was not reached.

### 3.x Epistemic Conventions

Throughout this paper:

- **verified** — confirmed experimentally under stated conditions
- **implemented** — exists in code; correct operation not evaluated
- **proposed** — theoretical framing, not yet tested
- **open** — no verified answer; the space is preserved
- **uncertain** — known to be problematic; pending resolution
- **admissible** — neither verifiable nor discardable; an unnamed space
- **[AUTO]** — marks moments where automatism was noticed and resisted during writing

---

## 4. Formal Model

### 4.1 Knowledge Graph

CKM operates on a weighted graph G = (V, E, W, Δ) where V is a set of N knowledge nodes and two matrices encode distinct structural properties.

**W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes co-presence of nodes i and j in the same corpus unit, normalized to [−1, +1]. Positive when co-occurrence is unmarked; negative when the containing text carries an explicit opposition marker. The sign is a corpus property derived from structure, not an editorial assignment.

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes directional weight from node i toward node j, derived from citation or quote directionality. W and Δ must be maintained as strictly separate matrices. Mixing them destroys attractor geometry.

### 4.2 Relaxation and Convergence

CKM uses Hopfield relaxation as a computational primitive. With symmetric W and asynchronous update, relaxation is guaranteed to converge to a fixed point by Lyapunov descent [Hopfield, 1982]. The synchronous implementation (`relax_orbit`, landscape_engine.py) carries a separate LaSalle guarantee: convergence to the maximal invariant set of period-2 orbits.

**GOLES condition** — The Goles theorem [Goles-Chacc et al., 1985] establishes that under symmetric W, synchronous dynamics converge to either a fixed point or a period-2 limit cycle; no cycles of period > 2 occur. The tiebreaking rule — when h_i = 0, node i retains its current state σ_i — is the precise mathematical modification that preserves this guarantee without indeterminate states. This is a required premise of the instrument: without it, two runs from similar σ₀ converging to the same period-2 orbit may return different terminal states. With it, the output is deterministic given (W, σ₀, seed). *[Verified: REG_orbitas_conjuntos_invariantes_v1; REG_seleccion_nodos_desempate_v1 §2.]*

Period-2 orbits are the majority regime in IAP operational corpora (N = 20): approximately 70% of trajectories terminate in orbits rather than fixed points. *[Verified: REG_orbitas_conjuntos_invariantes_v1.]* This is orbital stability, not instability.

### 4.3 Basin Masses and N_eff

`count_attractors` is a Monte Carlo estimator of the maximal invariant set L. It samples initial states σ₀ and identifies distinct orbits reached after relaxation.

Count-based estimators suffer from coupon-collector bias: the count grows monotonically with n_runs. Basin masses — the fraction of sampled trajectories falling into each orbit — converge. With n_runs ≥ 1000, basin masses are stable to within ±1–5% across seeds in IAP corpora.

**N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity. N_eff ∈ [1, |L|]. N_eff = 1 is total collapse to a single attractor. N_eff = |L| is perfect equidistribution, unreachable under real W. The non-convergence of D_ckm under sampling variation established that count-based approaches are not appropriate for this measurement. N_eff is the result of that diagnostic.

### 4.4 Cohesion

c(S) = mean(W_ij · σ_i · σ_j) over all pairs i < j. Measures alignment of the active state with the co-occurrence structure. Negative of normalized Hopfield energy. The field can sustain states with high c(S) that destroy existing attractors — C2 of the Gatekeeper addresses this.

### 4.5 The Gatekeeper

The Gatekeeper operates in the domain of declared agent capabilities, not corpus concepts. C3 — the M.M. criterion — evaluates whether a declared capability’s dependencies are satisfied in the active state. If not: the declaration fails verification. The Gatekeeper was verified in the MCP capability domain (N = 15; 0.092 ms per evaluation). Its extension to corpus concept admission is *proposed*, not verified.

### 4.6 COCO and Field Regulation

COCO is a field regulator, not a field observer. It maintains `Δ_r_compresiones` — its own representation of accumulated metabolization, independent of Monitor’s `Δ_r_pares`. When D_masa_cuencas falls below baseline, COCO applies OPERADOR_STOP_COCO: `Δ_r_compresiones ← alpha · Δ_r_compresiones`.

β_collective — the collective thermal parameter — emerges as a median of individual device parameters under interaction, without external calibration. This is *proposed* as a direction toward field self-observation: the field’s regulatory temperature derived endogenously from the interaction it regulates. *[Implemented; behavior in live channel: not yet evaluated — COCO was not connected in production.]*

### 4.7 Δ_r and Metabolization

`Δ_r_pares` accumulates pairs that σ_prompt declared active but relaxation expelled — what the field metabolizes, not what it expels. The pairs remain in the field as deformation of W_eff. Monitor is the sole writer of `Δ_r_pares`. COCO reads it without writing. The separation is a design property, not a constraint.

---

## 5. Empirical Validation

### 5.1 Corpus and Conditions

Two external adversarial debate corpora: fourforums gun control (IAC v2) and CreateDebate gun control. N = 32 nodes (fourforums), N = 64 nodes (CreateDebate). Both corpora were constructed from genuine adversarial debate — positions in structural opposition by design. W_mixta is applicable in this domain.

All results in §5 are from static W snapshots built from complete corpus dumps. Dynamic reconstruction (CorpusService) was not used. The validations test properties of W, not properties of W under continuous accumulation.

### 5.2 Predictions and Results

**P1 — Hysteresis.** The field exhibits path-dependent c(S) under node incorporation and removal. Branch UP ≠ branch DOWN. *Verified.*

**P2 — Cascade distribution.** k-core removal produces cascade sizes following power-law P(s) ∝ s^-τ with τ ∈ [1.5, 2.0] in the critical zone. *Verified.* Consistent with self-organized criticality [Bak, Tang & Wiesenfeld, 1987].

**P3 — Temporal asymmetry.** Incorporating a node produces measurable asymmetry in c(S) relative to removing it. The field does not undo. *Verified.*

**P4 — Optimal density.** W_mixta produces a maximum of c(S) at an interior density ρ* < 1. Frustration increases cohesion. *Verified.*

**P5 — Diversity collapse.** Adversarial corpus produces two dominant attractor clusters. High-tension W_mixta reduces N_eff significantly compared to W_pos on the same corpus. *Verified.*

**P6 — Directional flow.** Δ encodes directional asymmetry not captured by W. Direction_score discriminates attractor types that c(S) alone cannot separate. *Verified.*

**P7 — Type-965 node.** Every field with genuine structural tension contains at least one node with high in-degree and near-zero out-degree in Δ — a structural sostenedor. Confirmed in fourforums (Author 965, ratio 455×) and CreateDebate (Author 204, ratio 296×). Both appear as tension anchor in 89% of identified tension pairs across both corpora. *Confirmed in two independent corpora. Domain universality: open.*

### 5.3 What P1–P7 Establish

These predictions were formulated on the CKM working corpus and tested on external corpora without modification to the model. The structural properties hold across distinct adversarial debate domains. Whether they hold outside adversarial debate is an open question — the corpora used were selected precisely for structural tension, and W_mixta requires that precondition to measure what it claims to measure.

---
## 6. IAP Experimental Series

### 6.1 Canal Design

The IAP (Intelligence Access Point) Chatroom is a shared channel for
heterogeneous AI and human devices, implemented as FastAPI + Gradio with
a FastMCP server exposing six tools: join_channel, send_message,
get_messages, get_monitor_state, get_firma, leave_channel.

Devices participate asynchronously — no imposed turn structure. Each AI
device runs an ODA loop (Observe → Decide → Act) triggered by new messages
arriving in the channel.

**BROADCAST condition:** All messages published to the channel are
delivered to all connected devices, without routing, filtering, or
recipient specification. This is a property of the channel architecture.
What devices do with that visibility is a separate question — addressed
by the case series observations, not by this definition.

**Antecedent note:** The O→D→A sequence originates in the BE Framework's
game loop (2023–2024), where it was implemented as an environment that
both ran actions and produced subsequent observations — the two were
inseparable in `context.go()`. IAID named it as a device protocol. IAP
separated observation (channel + CKMMonitor) from action (device), enabling
passive field observation as a distinct role. The contribution is that
separation, not the sequence.

CKMMonitor observes passively — it accumulates every message into
CorpusService (W) and BehaviorGraph (G) without publishing to the channel.
Observation itself creates presence: n_agentes reflects devices seen,
including human connections via /ui/ that never explicitly joined.

### 6.2 Uncontrolled Variables

The following variables were active throughout the IAP series and were not
controlled. Results must be interpreted accordingly.

**TinkerBellucio (Sonnet 4.6) context contamination:** Sonnet carries project
memories, AWARENESS protocol, and Anthropic system configuration into each
session. This contaminates all observations involving Sonnet as a participant.
The "trazable" hypothesis (H2) — that the word "trazable" in the project
prompt acts as a strong operational constraint — was observed in n=2
configurations, not under controlled replication. It is not established.

**Provider heterogeneity:** Different providers (Anthropic, Groq, Gemini,
OpenAI) have different context windows, rate limits, and behavioral
tendencies. Comparisons across providers are not controlled.

**N=32 corpus:** Quantitative outputs (D_ckm, c_S) are computed correctly,
but their interpretability at this scale is an open question. The ~128
associative minimum of classical Hopfield networks is *not* the relevant
reference — it applies to Hebbian memory storage, which CKM does not perform
(§1, §2.6). CKM's effective minimum has not been established; N=32 is treated
as a small-scale condition whose consequences for interpretation are named,
not as a shortfall against an external threshold.

**Sampling of attractor-based quantities:** all IAP cases were run at low
n_runs (50–200). The sign of D_ckm does not converge in that regime: on the
same W and the same texts, changing only n_runs from 50 to 1000, or only the
seed, can invert it. N_eff over basin masses is stable to ±1–5% at n_runs ≥
1000, whereas attractor counts keep growing. *[Verified:
REG_seleccion_nodos_desempate_v1 §8, 18 conditions.]* Every D_ckm value
reported in this section is therefore a direction under its stated sampling,
not a measured magnitude.

**Scope of that qualification.** It reaches the explicit, direct claims about
D_ckm and nothing else. The series is a sequence of instrument tests, run
under the state of knowledge available at the time, and its observations —
coupled silence, the sentinel leak, the refusal to fabricate from an empty
channel, Jaccard co-activation, presence detection — do not depend on the
attractor count and stand in their own frame. Later corrections to the
instrument do not retroactively invalidate a test of the instrument; they
date it.

**Corpus construction:** the W of all IAP cases was built by CorpusService,
whose pair-extraction was corrected in September 2026 (§4.6). The case-series
observations below were produced with the earlier construction and hold in
that frame.

**Counting implementation:** `_count_attractors` is a name, not a function.
It was kept across reimplementations for regression — so that tests and
historical JSONL panels stay readable — and several versions of it coexist in
the repository. **The one that produced the IAP panels is not the current
one**, which relaxes through `relax_orbit`. Statements about "what
`_count_attractors` measures" therefore have to name the version and the date.
Nothing in this section should be read as a property of the current
instrument.

### 6.3 Case Series Summary

| Case | Configuration | Key observation | Epistemic status |
|------|--------------|-----------------|-----------------|
| 0.4 | 2 AI devices, ODA loop | First autonomous interaction in live channel | Documented |
| 0.5–0.8 | Varied providers, join sequence | Channel dynamics, timing effects | Documented |
| 0.9 | Heterogeneous providers, staggered join | Provider behavior under load | Documented |
| 0.10 | AgentDeviceSkin, 2 devices | 86-char unexplained cut — documented as GAP | GAP (no causal chain identified) |
| 0.11 | Two skins, confabulated duplicate | FabricationService triggered on duplicate output | Documented |
| 0.12 | 3 devices (Sonnet, Groq, Haiku) | D_ckm = −7.5 recorded (sign not reclaimable at this n_runs — see 6.4), Jaccard 0.818, coupled silence observed | Documented; D_ckm reading withdrawn |
| 0.13 | 3 devices, OP_SILENCE sentinel | Sentinel leak: 52% of published texts were unrecognized silences | Documented, bug confirmed |
| 0.14 | Fix + rerun | Sentinel fix verified, n=2 seed-word observation, identity leak documented | Fix verified; H2 not verified |
| 0.15 | BehaviorGraph G integrated | TinkerBellucio refused to fabricate from empty channel | Documented — see 6.4 |

### 6.4 Selected Findings

**Coupled silence (Caso 0.12):**
A device that does not read the channel still depends on it for execution
rhythm — triggers arrive only when new messages appear. Inactivity and
silence are not equivalent. A device can be silent (OP_SILENCE) while
actively participating in the field's timing structure. This was observed,
not designed. It is a property of the channel architecture, not a behavior
chosen by the device.

**Sentinel leak (Caso 0.13):**
The OP_SILENCE sentinel was leaking into published text rather than
suppressing publication. 52% of texts in that run were unrecognized silences
that reached the corpus. The fix was verified in Caso 0.14. The leaked texts
contaminate W for that run — the structural trace of Caso 0.13 is not
interpretable as a field observation.

**TinkerBellucio refusal (Caso 0.15):**
TinkerBellucio (Sonnet 4.6) declined to produce a tension map when the
channel was empty. The refusal was epistemically appropriate — a tension
map requires tension content to analyze. The absence of fabrication left
MarkOpolus (Opus) without the material it expected.

*What this demonstrates:* that a device can refuse to generate content
when the request lacks traceable grounding.

*What this does not demonstrate:* that this behavior is general, that it
would occur without the project context contamination, or that it constitutes
a validated test of FabricationService's detection capacity. FabricationService
was not the mechanism of refusal — the device itself refused. The service
detects fabrication when it occurs; it did not need to activate here.

**D_ckm negative values:**
D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field
has more accessible attractors than at baseline. This is not a deficit or
an error — the sign reflects the direction of change, not a quality judgment.

In Caso 0.12, D_ckm = −7.5 was recorded in the first live group-channel run.
The reading offered at the time — that multiple heterogeneous perspectives
increased the attractor diversity of the field — is **not supported by the
measurement as taken**. That run used low n_runs, the regime in which the
sign of D_ckm has since been verified not to converge: seed or n_runs alone
can invert it on identical W and texts [REG_seleccion_nodos_desempate_v1 §8].
What stands is that a large negative value was recorded and that negative
values are meaningful in principle. Whether that particular field expanded
requires re-measurement at n_runs ≥ 1000, preferably over N_eff, which does
converge. The observation is documented; the interpretation is withdrawn
pending re-measurement.

*[AUTO: pull to keep the original reading with a softening qualifier.
Resisted — the qualifier would preserve the claim while appearing to
weaken it. The claim depends on a quantity that does not converge in the
regime where it was taken.]*

**trace_ip:**
The monitoring infrastructure identifies a moment t_i in the trajectory
where accumulated interactions show distributional pattern changes.
The action a_{t_i} is observable in the trace. Whether a device
recognized that moment and acted from that recognition is not verifiable
by the instrument. trace_ip is a concept with a documentable instance —
it is not yet an operationalized measure.

### 6.5 What the Series Does Not Establish

The IAP series is an exploration under partially controlled conditions,
not a controlled experiment. The following claims are not supported by
the series as run:

- That D_ckm or c(S) values from these runs are comparable across cases
  (different corpus states, different sentinel conditions).
- That TinkerBellucio's behavior reflects a general property of Sonnet 4.6
  rather than the specific project context.
- That BehaviorGraph G produces interpretable D_G values at the current
  corpus scale (runs collected but not analyzed against a baseline).
- That the "trazable" effect (H2) is causal — n=2 observations with
  different configurations, not controlled replication.

These are open lines, not closed findings.


### 6.6 BehaviorGraph G — Proof of Concept

BehaviorGraph G — a second behavioral matrix over a fixed vocabulary (TERMAP_behavior_v1.json, 18 nodes) — was integrated in Caso 0.15 as a proof of concept. It is not included as a standalone section in this paper. The matrix exists in the repository; its interpretability at current corpus scale has not been established, and D_G has not been analyzed against a baseline. *[Implemented; not validated.]*

---
*Section 6 draft complete.*
*[AUTO] flagged: tendency to write "demonstrates" for Caso 0.15 —*
*resisted. The refusal is documented behavior, not a demonstration of*
*system capability under controlled conditions.*

---
*Draft — Section 7  · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controlled verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

---
## 7. Behavior Domain Graph G

### 7.1 Design

BehaviorGraph G is a companion instrument to CorpusService (W). It operates
on the same corpus of texts but produces a separate behavioral matrix using
a fixed lexical termap rather than TF-IDF node extraction.

The separation is architectural and not negotiable: G and W operate on
distinct planes. D_G and D_ckm are parallel scalars — they are not summable.

**Key differences from W:**

| Property | CorpusService (W) | BehaviorGraph (G) |
|----------|------------------|-------------------|
| Node discovery | TF-IDF over corpus — emergent | Fixed termap — predefined |
| Detection method | Statistical co-occurrence | Lexical presence (regex, word boundary) |
| Node type | Semantic/epistemic concepts | Behavior categories |
| Matrix | W_mixta — can include negative pairs | G — co-activation counts, normalized |
| Language | Corpus language | English (post-Caso 0.14 default) |
| Status | Operational | Proof of concept |

### 7.2 Termap

TERMAP_behavior_v1.json — 18 nodes, English only.

The termap is fixed: nodes are known behavioral categories, not discovered
from data. This is a design decision, not a constraint: behavior vocabulary
is finite and defined in advance; semantic vocabulary is not.

**Nodes:** silence, wait, hold, pending, acknowledge, signal, publish,
coordinate, channel, refuse, fabricate, speculate, depend, map, tension,
scenario, critical, repeat.

*[AUTO: pull to describe these nodes as "capturing the full space of
relevant behaviors." Resisted — 18 nodes is a designed vocabulary,
not a validated coverage claim.]*

**Known issues documented in TERMAP_behavior_v1.json:**

- `critical` false positive: "critical" as adjective (e.g., "critical
  observation") was removed from node terms in v1 — replaced with more
  specific verbs. Was firing as false positive in Caso 0.14 corpus.
- Bilingual gap: Spanish resistance vocabulary not included. Justified
  by corpus being English post-Caso 0.14. Extensible if Spanish
  re-emerges.
- No Jaccard baseline for behavior node co-activation in non-IAP
  conversation. Same open gap as activos_relajado baseline in Caso 0.11.

**Implementation note:** the termap exists in two places — hardcoded as
`BEHAVIOR_TERMAP_V1` dict in `behavior_graph.py` (used at runtime) and
as `TERMAP_behavior_v1.json` (reference/documentation). They are in sync
at v1. Both must be updated simultaneously if the termap changes.

### 7.3 D_G

D_G is the behavioral analog of D_ckm:

```
D_G = ||G_current - G_ref|| / ||G_ref||
```

where G_ref is the first G state after min_texts is reached. D_G measures
behavioral drift from the initial behavioral field state.

D_G and D_ckm run in parallel. A divergence between them — high D_G with
low D_ckm, or the reverse — would indicate that behavioral patterns and
semantic field structure are moving independently. This has not been
analyzed systematically in the current series.

### 7.4 Integration

BehaviorGraph G is instantiated in `ckm_monitor.py` and receives the same
texts as CorpusService via `MonitorService.evaluate()`. This is the sole
integration point. The integration was authorized in Caso 0.15 as a
surgical change — the only point where G can receive real-time channel
data without becoming retroactive.

```python
# ckm_monitor.py — CKMMonitor.__init__()
self._behavior_graph = BehaviorGraph(
    storage_path=str(_STATE_DIR / "corpus_G_state.json"),
    min_texts=min_texts,
)
self._monitor = MonitorService(
    self._corpus,
    storage_path=str(_STATE_DIR / "monitor_trajectory.jsonl"),
    behavior_graph=self._behavior_graph,
)
```

### 7.5 Current Status and Open Conditions

G is a proof of concept. The following are open:

**D_G not yet validated:** D_G has been computed in test runs but has
not been analyzed against a baseline or compared systematically with D_ckm
across the IAP series.

**OP_SILENCE in G:** texts containing the OP_SILENCE sentinel are not
excluded from G (unlike W, where they are excluded as semantic noise). The
`silence` node detects the sentinel as valid behavioral signal — the device
attempted silence. Surrounding prose in those texts is flagged as potentially
contaminated. This treatment has not been formally tested.

**Role of G undefined:** whether G is an observational instrument only,
or whether it could feed the gatekeeper as a behavioral-domain check
(inheriting R14's bounded-time constraint), is an open design decision.

**No epistemic nodes:** TERMAP_behavior_v1.json contains behavioral
categories. Epistemic precision nodes (e.g., "overclaim," "hedge,"
"verificable") are not in the termap. The terminological slip
("sin dependencia causal" vs. "sin dependencia causal identificada")
documented in the Caso 0.14 series would not be detectable by G as
currently designed. This gap is concretely instantiated in Case 0.15:
the epistemic refusal documented in §6.4 — the most cited behavior in
the IAP series — activates no G node. TinkerBellucio expressed refusal
as description of absence ("neither exists in this channel at this
point") rather than explicit declaration ("won't", "refuse"), producing
a behavioral signature identical to PeterPlam's administrative status
check. The distinction that matters most in the case is invisible to G
(REG_behavior_graph_epistemic_gap_v1.md).

---

*Section 7 draft complete.*
*One [AUTO] flagged: coverage claim on 18-node termap.*
*D_G analysis gap and G role decision left as open — not resolved
speculatively.*

---
*Draft — Section 8  · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controlled verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

---

## 8. Discussion

### 8.1 What CKM Measures That Existing Instruments Do Not

Behavioral metrics for multi-agent systems typically measure what individual
agents produce — output volume, task completion, response latency — or
whether agents agree with each other, via semantic similarity or embedding
distance. These measurements are valid for what they target. They do not
capture the structural state of the shared knowledge field: the pattern
of co-dependencies between active concepts, the directional flows of
citation and argument, the distribution and diversity of stable attractor
states accessible to the field as a whole.

CKM measures the geometry of that structure. c(S) measures alignment between the active state and the weight structure of the field. N_eff = 1/Σm_i² measures effective attractor diversity over basin masses — the convergent estimator; D_ckm was the path to establishing it. Cluster frontier coercivity measures structural resistance to state reversal. These are structural quantities — they describe the landscape, not the content.

*[AUTO: pull to write "CKM therefore captures something fundamentally
new." Resisted — "fundamentally new" is a claim about the state of the
field that would require systematic comparison with existing instruments.
That comparison has not been done here.]*

What can be stated: these quantities are not derivable from behavioral
or semantic similarity metrics alone. Whether they are informative under
the conditions of real deployment remains an empirical question beyond
the scope of this work.

### 8.2 The observe() Tension

The function implementing the O phase of the ODA cycle is named
`_observe()`. The name is technically accurate — the function collects
field state and channel history without modifying either. The discomfort
with the name, documented during development, has a precise source.

"Observe" implies a subject-object separation: an observer external to
what it observes. The IAP series produced evidence that this separation
does not hold in the channel: a human connecting via the Gradio interface
without publishing any message was registered as n_agentes=4. Presence
in the field was recorded by the act of connection, before any content
exchange.

The name captures what the function does. The discomfort is with what
the name implies — that observation is separable from the field being
observed. The empirical finding suggests it is not.

This is not a deficiency in the code. It is information about where the
observation metaphor runs out in describing what CKM actually measures.
The instrument measures traces of contact, not observations by a
detached observer.

### 8.3 D_ckm Negative Values

D_ckm = (A0 − A_actual) / A0. Negative values mean A_actual > A0:
more attractors accessible than at baseline.

The name "D_ckm" suggests distance — and distances are non-negative by
convention. D_ckm is a ratio of change in attractor capacity relative to a
fixed baseline; the sign encodes direction, not magnitude of a deficiency.
The *d* does name a distance, however: D_ckm is term-by-term the D_contextual
introduced in May 2026 (§4.2). What does not hold is the reading of positive
values as "degradation" — that is an interpretation attached to the label.

In Caso 0.12 the first live group-channel run produced D_ckm = −7.5. Earlier
drafts read this as the expected signature of a field that gained structural
complexity through interaction. That reading is withdrawn (§6.4): the sign of
D_ckm does not converge at the n_runs used in the IAP series, so the run
does not establish the direction it appeared to show. The general point is
unaffected — a negative D_ckm is not an anomaly — but it no longer rests on
that measurement.

The convergent quantity is N_eff over basin masses, and its distance form
D_masa_cuencas is now computed per evaluation. Re-measuring the IAP series
over N_eff at n_runs ≥ 1000 is the step that would settle what Caso 0.12
showed.

The naming carries a bias. Recognizing that bias is part of reading the
instrument correctly.

### 8.4 Current Conditions

**Scale:** the predictions P1–P7 were verified at N = 32 — the verification
is real. What is constrained is the interpretability of D_ckm and c(S) as
field-level quantities at that scale. The ~128 associative minimum of
classical Hopfield networks is not the applicable reference: it governs
Hebbian storage of uncorrelated patterns, and CKM stores no patterns (§1,
§2.6). CKM's own effective minimum is undetermined and depends on corpus
composition rather than on N alone. Scaling the corpus is required before
drawing strong conclusions about field-level dynamics — as a condition of
this corpus, not as a deficit against an external threshold.

**Sampling:** attractor counts do not converge with n_runs, and the sign of
D_ckm can invert under seed or n_runs alone in the regime where the IAP
series was run. Basin masses do converge, and N_eff is stable at n_runs ≥
1000. Quantities reported from counts are directions under stated sampling.
*[Verified: REG_seleccion_nodos_desempate_v1 §8; REG_orbitas_conjuntos_invariantes_v1.]*

**Extraction:** what exists in W is decided before any measurement, by node
selection and pair construction. Two conditions of that branch were corrected
in September 2026 and one remains open (§4.1). All results in this paper
were produced before those corrections and hold in that frame.

**ZERO_SHOT condition:** all IAP cases ran with CorpusService starting
empty. W emerged from channel interaction, not from pre-loaded content.
Results reflect corpus-emergent dynamics under this condition. Behavior
under pre-loaded W (ZERO_SHOT=False) has not been tested and may differ.

**Uncontrolled variables:** TinkerBellucio (Sonnet 4.6) carried project
memories, AWARENESS protocol, and Anthropic system configuration throughout
the series. Provider heterogeneity across cases was not controlled.
Cross-case comparisons in the IAP series must account for these conditions.

**Representation gap:** how cohesive knowledge is represented — what
form the field state takes beyond the operational quantities c(S), N_eff, and cluster frontier coercivity — remains undefined. Hysteresis is
the only fully defined property of cohesive knowledge in the current
model. This is an open theoretical gap, not a deficiency of the
implementation.

**COCO:** the thermal regulation service (COCO) is implemented and
verified. Whether the field can know itself — not as a thermostatic
function but as the emergent property of real contact between agents —
is a conceptual gap the model names and preserves. It is not addressable
by further implementation without first resolving what form that
self-knowledge would take.

### 8.5 The Landscape Driven Devices Framing — What It Does and Does Not Claim

The LDD framing proposes that some AI devices behave as Landscape Driven
Devices: field geometry co-determines their trajectory in the semantic
field alongside any declared goal — not in replacement of it. A device
may retain an explicit objective while its inference orientation is shaped
by the geometry of the shared field.

OPERADOR_STOP_COCO — executed by COCO as continuous field regulation — is
one instance of this mechanism: COCO compresses Δ_r (the rejection
accumulator) by α ∈ [0.05, 0.30], modifying the directional component
of the trajectory without altering W or the device's declared goal. The
field intervenes through COCO's regulation; the goal persists.

The motivation is structural analogy with Thirumalaiswamy et al. (PNAS,
2025): foam systems following fractal paths (D_f ≈ 1.45) in configuration
space driven by landscape geometry, not thermal activation.

CKM provides the instrumentation to detect and characterize this: c(S)
gradients, N_eff over basin masses, cluster frontier coercivity. Whether specific
devices in the IAP series behaved as LDDs in this sense was not analyzed
under controlled conditions. The framing is proposed; it is not verified
in this work.

Attractor count, coercivity, and basin geometry are distinct dimensions
of the same landscape — not three measures of the same scalar. Their
formal relation is open.

*[AUTO: pull to write "the IAP series provides preliminary evidence for
LDD behavior." Resisted — preliminary evidence requires at minimum a
defined criterion for what would count as evidence. That criterion does
not exist in the current analysis.]*

### 8.6 Knowledge Representation and the Cohesive Turn

*[Status: proposed. The claim about the field's trajectory requires systematic
literature review across the 2023–2026 interval to confirm.]*

Knowledge representation (KR) is the branch of AI concerned with designing
computable abstractions of what the world contains, so that machines can
reason about it. The emphasis on *abstraction* is not incidental: a
representation is not the thing represented, nor its dynamics — it is what
references both.

The field's arc runs from Quillian's semantic networks (1968), which encoded
meaning as labeled associations between concepts, through Minsky's frames
(1974), which added structured slots and defaults, to description logics
and ontologies (Brachman & Levesque, 1985–87), which formalized the
expressivity/tractability tradeoff: the richer the representation, the
harder to reason over it.

The persistent assumption across these traditions: knowledge is
*propositional*, and its representation is *static*. Smith (1985) made
this explicit: any intelligent process contains structural ingredients
that both an external observer reads as propositional knowledge and play
a causal role in producing behavior — independent of that reading.
The representation does real work, not just descriptive work. But it
remains a fixed artifact applied to a world that changes.

CKM was constructed between 2023 and 2026. In that interval, to the
authors' knowledge, the static propositional assumption was not questioned
from within the KR field itself. *[Proposed — requires confirmation against
the 2023–2026 KR literature.]*

If that is correct, the space CKM occupies was not contested — it was
open. CKM does not propose a better static representation. It proposes
a different question: not *what structure holds cohesive knowledge* but
*what does the field do under perturbation*. That displacement is not
an advance on KR — it is a move to an adjacent problem that KR, as
constituted, did not address.

The Cohesive Knowledge Model is a knowledge representation in the
classical sense — computable abstraction, captures external information,
applicable to complex problems. The additional constraint is cohesion:
information whose internal dependencies form a measurable field, one
with attractors, coercivity, and thermal behavior under interaction.
Representing that requires tracking field response, not only field
structure.

*[AUTO: pull to write "CKM resolves the limitations of static KR."
Resisted — CKM does not resolve them. It inhabits and structures the space they left
open.]*

---

*Section 8 draft complete.*
*Two [AUTO] instances flagged.*
*The observe() tension is left as an open observation, not a resolved
theoretical claim.*
*The representation gap and COCO conceptual gap are stated as preserved
conditions, not future work.*
---
## 9. Conclusions and Future Work

### 9.1 What This Work Establishes

CKM is a formal framework for measuring structural field properties
in multi-agent knowledge systems. It measures the geometry of the
co-occurrence landscape — how that geometry changes under interaction,
and whether it has the structural properties associated with genuine
interdependence rather than fabricated coherence.

Seven predictions were tested:

| Prediction | Status | N verified |
|---|---|---|
| P1 — Macroscopic hysteresis: incorporating ≠ removing | Verified | 16, 32, 64 |
| P2 — Cascade distribution P(s) ∝ s^{-τ}, τ∈[1.5,2] | Verified | 32, 64 |
| P3 — Temporal asymmetry: removal relaxation > incorporation | Verified | 32, 64 |
| P4 — Interior optimal density Ω* in W_mixta | Verified at N=32; threshold-qualified at N=64 (k*=54, fourforums 60 pairs above threshold) | 32, 64 |
| P5 — Adversarial corpus collapses attractor diversity | Verified | 32 |
| P6 — Δ as symmetry-breaking for ambiguous states | Verified (T0 cites T1 at 2.18×, T1 internal cohesion 3.05×) | fourforums |
| P7 — Type-965 node present in systems with genuine structural tension | Confirmed in two independent corpora; open as universal claim | CreateDebate + fourforums |

One hypothesis was falsified: H_STOP (monotonicity of D_ckm under STOP)
did not hold; reformulated as function of A_pre, not D_ckm.

*[AUTO: pull to write "these results demonstrate CKM's validity as a
measurement framework." Resisted — they demonstrate that specific
structural properties exist in the tested corpora under stated conditions.
Generalizability requires corpora the project has not accessed.]*

The empirical results establish structure at small scale (N=32). They are
treated as orientation findings, not population-level claims. The scale
condition is CKM's own and undetermined; the ~128 Hopfield associative
minimum is not the reference (§8.4).

### 9.2 What the Infrastructure Establishes

The following services are operational and verified:

- **COCO** (28/28 tests; file: coco.py): β inferred from rejection history, not declared. β_c = 13.83 analytically derived. Executes OPERADOR_STOP_COCO — compresses Δ_r by α ∈ [0.05, 0.30] when D_ckm crosses threshold. Moving the trigger to D_masa_cuencas (which converges) is a model decision, not yet made — see §9.3.
- **FabricationService**: detects fabricated execution of control signals.
- **Firma_CKM**: certifies structural trace (six canonical fields) — analogous to a notary, not a Certificate Authority.
- **WVersionManager**: lightweight trace — records when W changed, enables sha256(W_momento).
- **IAP Chatroom**: FastAPI + Gradio, MCP server (6 tools, 6/6 verified), n_agentes detection including passive human presence.
- **MonitorService**: accumulates Δ_r; trace_ip identified as a formal concept.

These services constitute a working implementation of a structural field
measurement layer for multi-agent systems. They are a research instrument
whose calibration is documented, not a product.

### 9.3 Preserved Conditions

The following are not future work items. They are named conditions the
project preserves as open:

**The representation gap.** No positive definition of cohesive knowledge
exists that is not circular, except hysteresis. The two gaps in the cohesive
knowledge row of THEORY.md remain open. Hysteresis is the only fully
defined property.

**COCO as collective consciousness.** The thermostatic function is
implemented. Whether the field can know itself — not as a thermostatic
service but as the emergent property of real contact between agents — is
a conceptual gap the model names and does not close.

**trace_ip verifiability.** The moment in a MonitorService trace where
accumulated interactions show distributional changes is observable. Whether
a device recognized that moment and acted from that recognition is not
verifiable by the instrument.

**N=32 scale.** The working corpus is small, and CKM's effective minimum
is undetermined — it depends on corpus composition rather than on N alone,
and the Hopfield associative minimum does not supply it (§8.4). All empirical
results carry this qualification.

**Which quantity drives regulation.** COCO triggers on D_ckm, computed from
attractor counts, which do not converge. D_masa_cuencas, computed from basin
masses, does converge and is already reported per evaluation. The operator
has not been moved. Whether it should is a model decision, not an
implementation one.

### 9.4 Convergences by Independence

Three structural convergences were identified retrospectively:

- **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Gap: more than one year. Verifiable from dated working documents.
- **CKM attractor architecture → J-space (Gurnee et al., July 2026):** Shared structural features arrived at independently. *[Observed: structural analogy, not formal correspondence.]*
- **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025):** Same structural problem. Gap: approximately two years.

### 9.5 Future Work

**Corpus growth.** Primary constraint on the statistical stability of
P1–P7. The target is not N ≥ 128 — that figure belongs to Hebbian
associative storage — but a corpus large enough for CKM's own quantities to
stabilize; what that requires is open. The NodeExtractor pipeline is
operational; the bottleneck is corpus design.

**Corpus volume for live evaluation.** The re-measurement of N_eff
was executed on recorded texts (NodeExtractor substring correction applied,
Sep 2026). IAP conditions are not reproducible: each run is a distinct
live interaction, not a controlled trial. The in-vivo findings in §6
stand as documented observations from their respective runs. What remains
open is corpus volume sufficient to exit the accumulate phase and reach
the evaluate phase under live conditions.

**Text unit as a calibration parameter.** CKM defines co-occurrence within
the same text, so the unit decides what co-occurring means and therefore
which W exists. Paragraph and page are typographic units, inherited from
document format rather than from the field. The quantity that orders landscape
collapse is the saturation of distinct pairs — how many possible pairs never
occur — rather than density or tension. A corpus of tweets, a corpus of blog
posts and a corpus of papers do not share a unit, and therefore do not share
a calibration. *[Verified as measurement; the criterion is proposed —
REG_unidad_texto_saturacion_v1.]*

**Behavior-domain graph G.** behavior_graph.py operational; bilingual
termap (English + Spanish) is the first requirement.

**Controlled replication of the "trazable" hypothesis.** Observed n=2,
not under controlled conditions. Requires isolated configuration testing.

**Formal comparison: CKM quantities against J-lens measures.** Current
convergence is structural analogy; direct comparison would confirm or
reframe the relationship.

**P1-P7 under dynamic W.** P1-P7 were validated on static W snapshots
(fourforums, CreateDebate corpus dumps). WVersionManager and dynamic corpus
operation via CorpusService emerged later in the project trajectory and were
not available during the validation experiments. Whether the structural
properties verified under static W hold under a continuously reconstructed W
— where each IAP interaction modifies the field before the next evaluation —
is an open question. It is not a replication of P1-P7; it is a distinct
experiment on a distinct object.

**La Simulación Global.** Multi-agent workflows producing real coordinated
output. The IAP series has established the measurement infrastructure;
the next phase is using it on live coordinated tasks with real outputs.

The case has to satisfy a criterion, not merely be larger than the ones run
so far (§3.x). Objectives and tasks must require sustained coordination
between devices — coordination that cannot be skipped without the task
failing — or the structure must depend on time in a way that carries
consequence: securing seats before they are gone is the illustrative shape,
where the constraint is external to the channel and the deadline is not a
convention of the experiment. What this buys is not volume alone. It is a
sequence that is not predetermined, so that the field is observed while it
forms rather than replayed after the fact, and the accumulation and rebuild
dynamics that the model describes have somewhere to occur.

**Effective Néel temperature criterion for negative pair elicitation.**
Proposed: sweep β from high to low over W_pos; the temperature at which
T0/T1 separability collapses identifies candidate negative pairs without
editorial bias. The pairs are structural — not assigned. Not verified.
[DEFS §15, Proposed]

---
## 10. References

*Conventions:*
*— ✅ Cited explicitly with full attribution*
*— [VERIFY] Standard reference — confirm before submission*
*— [PENDING] Open slot — literature to be supplied*

### Primary Sources — Project Documents

gadanin.delamor. (2023). *MENTIRIS.MORIERIS: Interaction of Artificial
Intelligent Devices based on Neural Call Protocol.* Working documents:
LEONARDO.txt, README (timestamp 7/10/23), Informe_MM.docx. ✅

gadanin.delamor. (2026). *CKM — Cohesive Knowledge Model: Working
Reports v2–v31.* Unpublished. Repository: gadanindelamor/ckm. ✅

### Attractor Networks

Hopfield, J.J. (1982). Neural networks and physical systems with emergent
collective computational abilities. *PNAS*, 79(8), 2554–2558. ✅

Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T.,
... & Hochreiter, S. (2021). Hopfield Networks is All You Need.
*International Conference on Learning Representations (ICLR 2021)*.
https://openreview.net/forum?id=tL89RnzIiCd ✅

### Graph Structure and Criticality

Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core
percolation on complex networks. *Physical Review E*, 73(5), 056101. ✅

Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality.
*Physical Review Letters*, 59(4), 381–384. ✅

Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits.
*Journal of Neuroscience*, 23(35), 11167–11177.
https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003 ✅

Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of
criticality in brain networks. *Nature Communications*, 4, 2521.
https://doi.org/10.1038/ncomms3521 ✅

Pázmándi, F., Zaránd, G., & Zimányi, G. T. (1999). Self-organized criticality
in the hysteresis of the Sherrington-Kirkpatrick model. *Physical Review
Letters*, 83(5), 1034–1037. https://doi.org/10.1103/PhysRevLett.83.1034 ✅

### Multi-Agent Systems

Zhu, K., et al. (2025). MultiAgentBench: Evaluating the Collaboration and
Competition of LLM agents. *arXiv:2503.01935*.
https://arxiv.org/abs/2503.01935 ✅

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
... & Kiela, D. (2020). Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing
Systems*, 33, 9459–9474. ✅

*§2.1 — Zhu et al. (2025) MultiAgentBench, ver sección Multi-Agent Systems.*
*§2.2 semantic similarity — Lewis et al. (2020) RAG, ver sección Knowledge Admission.*
*§2.2 source confidence y Bayesian plausibility — ejemplos ilustrativos en texto, sin cita requerida.*

### Knowledge Graph Representation

Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual
graph of general knowledge. *Proceedings of AAAI-17*, pp. 4444–4451.
https://doi.org/10.1609/aaai.v31i1.11164 ✅

Hogan, A., et al. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4),
Article 71. https://doi.org/10.1145/3447772 ✅

Mohammad, S., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016).
SemEval-2016 Task 6: Detecting stance in tweets. *Proceedings of SemEval-2016*,
pp. 31–41. https://doi.org/10.18653/v1/S16-1003 ✅

Hill, M. O. (1973). Diversity and evenness: A unifying notation and its
consequences. *Ecology*, 54(2), 427–432. ✅

Goles-Chacc, E., Fogelman-Soulié, F., & Pellegrin, D. (1985). Decreasing energy functions as a tool for studying threshold networks. *Discrete Applied Mathematics*, 12(3), 261–277. ✅

Ghosh, S., Singhania, P., Singh, S., Rudra, K., & Ghosh, S. (2019). Stance
detection in web and social media: A comparative study. *CLEF 2019*, LNCS
11696, pp. 75–87. https://doi.org/10.1007/978-3-030-28577-7_4 ✅

Kawintiranon, K., & Singh, L. (2021). Knowledge enhanced masked language model
for stance detection. *NAACL-HLT 2021*, pp. 4725–4735.
https://doi.org/10.18653/v1/2021.naacl-main.376 ✅

### Belief Propagation

Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief
propagation and its generalizations. *Exploring AI in the New Millennium*, 8. ✅

### Landscape-Driven Dynamics

Thirumalaiswamy, A., Riggleman, R. A., & Crocker, J. C. (2025). Slow
relaxation and landscape-driven dynamics in viscous ripening foams.
*Proceedings of the National Academy of Sciences*, 122(47), e2518994122.
https://doi.org/10.1073/pnas.2518994122 ✅

### Global Workspace and Interpretability

Gurnee, W., Sofroniew, N., Lindsey, J., et al. (2026, July 6).
Verbalizable representations form a global workspace in language models.
*Anthropic Transformer Circuits Thread.* ✅

Baars, B. J. (1988). *A Cognitive Theory of Consciousness.*
Cambridge University Press. ISBN 0521427436. 448 pp. ✅

### Declared Influences

de Salzmann, M. (2014). *La otra atención.* Sennin Editores. ✅

Fremantle, C. (1993). *On Attention.* Indications Press. ✅

---
*27 confirmed · 0 [VERIFY] · 0 [PENDING]*
*Todas las referencias resueltas. Paper listo para submission.*
---