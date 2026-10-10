# Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction

> **v28 BORRADOR — Opus 5.5 (Cowork), 10 oct 2026, sobre v27 (7 oct). Este bloque se retira antes de publicar.**
> Cada cambio está marcado *[v28]* y es propuesta: entra cuando delamor lo confirma. Criterios de delamor (10 oct): (1) lo que tiene demostración, en citas o en la ciencia, se expone sólo como referencia; nada insinúa corroboración propia; el intento es desde la humildad. (2) Son aportes a la ciencia: lo que no aporta ni da sentido a lo que aporta, sale; sin aportes no se publica.
> Cambios: §4.1.1 (no-co-ocurrencia y origen del signo); §4.2 (el campo es continuo; el corpus es instrumento; los saltos son de la representación); §5.1 (de dónde viene el signo de fourforums; IAP y W_pos contra las trazas); §5.2 P1/P3 (referencias en lugar de exposición); §6.2 (condiciones del instrumento en la serie); §8.5 (ausencia como segunda representación; tests del instrumento); §9 (tres referencias [VERIFY]). Abstract: una propuesta mínima, marcada.
> Conteos de tests retirados del cuerpo; nueva sección Code Availability: el resultado de la suite se verifica y se anota al congelar el release (delamor, 10 oct).
> No se tocó lo demás.

**Pablo E. Gadano**  
*gadanin.delamor*  
Independent researcher  
*Preprint — September 2026*

---


## Abstract

The Cohesive Knowledge Model (CKM) is a formal instrument for measuring structural properties of semantic fields in multi-agent AI interaction. Its central contribution is **N_eff = 1/Σm_i²** — the inverse Simpson diversity index over basin masses of a Hopfield landscape — as a convergent estimator of field diversity. Basin masses converge under sufficient sampling; attractor counts do not. The non-convergence of count-based estimators (D_ckm) is not a failed metric: it is the diagnostic that established which estimator is appropriate.

A second contribution is the endogenous emergence of β_collective — the collective thermal parameter of the field regulator (COCO) — as a median of individual device parameters under interaction, without external calibration. β_collective is implemented as an observation — computed, not yet acting on the field — and its regulatory role remains open. It is presented as a direction toward field self-observation.

CKM operates on two matrices derived from a corpus: W (symmetric co-occurrence weights) and Δ (asymmetric directional dependencies). Four predictions of the static hybrid model (P1–P4) are not testable on a non-negative W snapshot: P1 and P4 are decided by the premise W ≥ 0, and the k-core form of P3 is reversible by construction (§5.2); P2 is not measurable at N = 32. *[v28: "(all three shown mathematically)" → "(§5.2)" — criterio 1.]* Three observations (P5–P7) are tested against external adversarial debate corpora (fourforums, CreateDebate; N = 32–64). P5–P6 are verified; P7 is confirmed in two independent corpora, and its domain universality remains open.

The IAP test series documents field behaviors in live multi-agent operation — sentinel leaks, coupled silence, refusal to fabricate from an empty channel — as field observations. Being live, the series cannot be reproduced and its cases are not comparable. The observations are reported without causal attribution to specific mechanisms.

The paper presents CKM as a landscape instrument, not a behavioral evaluator. What it measures is the geometry of co-occurrence structure and how that geometry changes under interaction.


## Outline

```
1. Introduction
2. Related Work
3. Research Conditions
4. Formal Model
5. Empirical Validation — External Corpus
6. IAP Test Series
7. Discussion
8. Conclusions and Future Work
9. References
Appendix A. Writing Trace
```

---
## 1. Introduction

Multi-agent AI systems are increasingly deployed in configurations where several devices interact over a shared channel — producing text, making decisions, building on each other’s outputs. Evaluating whether this interaction constitutes genuine coordination or parallel activity requires measuring something most existing approaches do not capture: the structural field that emerges from interaction itself.

Most existing approaches measure what individual agents produce or whether their outputs agree. Neither captures the geometry of co-dependencies, directional flows, and attractor states that characterize the shared knowledge state of the group at a given moment.

This paper presents the Cohesive Knowledge Model (CKM), a formal instrument for measuring structural properties of semantic fields in multi-agent interaction. CKM does not interpret semantic content. It measures the geometry of the co-occurrence landscape and how that geometry changes under interaction.

**The central contribution** is N_eff = 1/Σm_i² — the inverse Simpson diversity index [Hill, 1973] over basin mass distributions of a Hopfield landscape — as a convergent estimator of field diversity. The path to this estimator required establishing that count-based estimators (attractor counts, D_ckm) do not converge in sign under sampling variation. That non-convergence is not a failed metric: it is the diagnostic.

**A second contribution** is the observation that β_collective — the collective thermal parameter of the field regulator — emerges as a function of individual device parameters under interaction, without external calibration. β_collective is implemented as an observation — computed, not yet acting on the field — and its regulatory role remains open. It is presented as a direction toward field self-observation.

CKM makes seven falsifiable predictions (P1–P7). The four of the static hybrid model (P1–P4) are not testable on a non-negative W snapshot (§5.2). P5–P7 were tested against two independent external adversarial debate corpora: P5–P6 are verified; P7 is confirmed in two corpora, and its domain universality remains open.

The IAP test series documents field behaviors in live operation: sentinel leaks, coupled silence, refusal to fabricate from an empty channel. These are field observations, reported without causal attribution.

---

## 2. Related Work

### 2.1 Multi-Agent Evaluation

Most existing frameworks for evaluating multi-agent AI systems operate at the level of individual agent behavior: task completion rates, response latency, output volume [Zhu et al., 2025]. A second class measures semantic agreement between agents — cosine similarity between outputs, embedding-space distance, topic overlap [Zhu et al., 2025]. Neither class measures the structural field that emerges from interaction: the pattern of co-dependencies that characterizes the shared knowledge state of the group.

CKM does not replace behavioral or agreement metrics. It measures something orthogonal to both.

### 2.2 Knowledge Representation and Signed Weights

Knowledge graphs typically represent relations as positive-weight edges encoding similarity, co-occurrence, or inferential support [Speer et al., 2017; Hogan et al., 2021]. Negative weights, when they appear, are introduced through explicit annotation or post-hoc linguistic processing. They are not, generally, derived from the structural pattern of the corpus as a whole.

CKM derives signed weights directly from corpus structure: texts that frame two concepts in explicit opposition reduce the corresponding W_ij entry. The sign is a corpus property derived from structure, not an editorial assignment.

### 2.3 Hopfield Networks and Attractor Structure

The Hopfield network [Hopfield, 1982] provides the energy formalism CKM uses for relaxation and attractor analysis. Modern extensions [Ramsauer et al., 2021] increase storage capacity but preserve the core attractor geometry. CKM uses this formalism as a relaxation tool, not as a pattern-retrieval mechanism. In early experiments with Hebbian weights [Hebb, 1949] (N = 16), incorporating the directional asymmetry directly into the weights (W + Δ/2) reduced pattern recovery from 0.78 (symmetric W) to 0.02: without symmetric weights there is no Lyapunov function. *[Working Report v11, §14.6.]* CKM does not use Hebbian pattern storage: W encodes corpus co-occurrence, and its attractors are minima of a frustrated energy landscape, not stored patterns. What these frameworks do not address is the distribution of basin masses — how much of the state space falls into each attractor — as a convergent diversity estimator.

Count-based estimators of attractor diversity suffer from coupon-collector bias: the count grows monotonically with sampling. Basin masses converge. N_eff = 1/Σm_i² — the inverse Simpson index over basin mass distributions — is the convergent estimator that count-based approaches cannot provide.

The closest published work to CKM's base architecture is Aiyappa, Flammini and Ahn [Aiyappa et al., 2024], who model contagion dynamics over weighted belief networks using Hopfield-like energy minimization with all-positive weights. That work maps closely to W_base (W_pos): co-occurrence weights, Hopfield relaxation, attractor analysis. CKM extends this base in one structural direction: W_mixta introduces negative weights where the text itself carries opposition markers (§5.1).

### 2.4 Diversity Estimation in Dynamical Systems

The inverse Simpson index is established in ecology as a measure of effective species richness [Hill, 1973]. Estimating basin volumes by sampling initial conditions is an established tool for multistable dynamical systems — basin stability [Menck et al., 2013] — and entropy over basin volumes has been proposed as a measure of uncertainty in dynamical systems [Daza et al., 2016]. CKM applies this family of measures to Hopfield landscapes built from semantic co-occurrence fields. The connection is structural: basin masses in a Hopfield landscape are analogous to species abundances in an ecosystem. N_eff is the number of equally-abundant basins that would produce the observed concentration. When q = 2, the Hill number equals the inverse Simpson concentration — the effective number of dominant attractors in the landscape.

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

The [AUTO] markers are the visible surface of this condition: moments where automatism was noticed and resisted during writing. They are not rhetorical. They are part of what the trace looks like when made explicit. To preserve readability, the markers appear in the text as short references (AUTO-n) and are collected in full in Appendix A.

### 3.5 What the Instrument Cannot Register

Δ_r accumulates pairs that σ_prompt declared active but relaxation expelled. The condition of entry is that the pair was written and evaluated. What is not written does not pass through the field — it generates no rejection, leaves no trace in Δ_r.

Consequence: the alternative discarded before writing is invisible to the instrument. Δ_r cannot distinguish between “the field rejected this combination” and “this combination was never considered.” This is not a correctable limitation. It is a structural condition of any instrument that measures what occurred: it cannot measure what did not occur because there was no observer who opened the possibility.

*[The first two observations above are verifiable in the code: `_rejected_pairs`, Δ_r accumulation. The third — on the act of opening and its relation to what appears in Δ_r — is an observation about the observer. Registered as* **admissible***, not verified.]*

### 3.6 Preserved Incompleteness

Several components of the formal model are open gaps by design. The representation of cohesive knowledge beyond hysteresis is undefined. COCO as collective consciousness is unimplemented. The Gatekeeper operates in the domain of declared agent capabilities; its extension to corpus concepts is *proposed*, not verified.

These are not future work items. They are conditions the model names and preserves. A gap declared is not a gap concealed.

### 3.7 Material Conditions

The operational corpus is at N = 32 nodes. The IAP test series consists of documented observations of live interaction. It cannot be reproduced, and its cases are not comparable. COCO was never connected to the live IAP channel — in none of the 253 documented panels; it was exercised only in test drivers. Results are reported under these conditions, not against an ideal that was not reached.

### 3.8 Epistemic Conventions

Throughout this paper:

- **verified** — confirmed experimentally under stated conditions
- **implemented** — exists in code; correct operation not evaluated
- **proposed** — theoretical framing, not yet tested
- **open** — no verified answer; the space is preserved
- **uncertain** — known to be problematic; pending resolution
- **admissible** — neither verifiable nor discardable; an unnamed space
- **[AUTO]** — marks moments where automatism was noticed and resisted during writing (collected in Appendix A)

---

## 4. Formal Model

*[Structure v27: one model — the hybrid model (`docs/CKM_Modelo_Hibrido.md`). A model has no domain; domains are interpretations of the model. M.M's domain is given by its own definition (declarations of functions and events); every other interpretation — text corpora, debate corpora, the IAP channel — carries its own status (tested, proposed, potential), declared where it is used. What is static or dynamic is W, not the model: a static W is a snapshot of W. Section 4.3 (landscape) is defined after 4.1 and 4.2, as their conjunction. Premise identifiers pending.]*

The criterion is whether W changes. Each regime of W is given by its characteristics and by its differences from the other.

*[Landscape (4.3): pending — defined once 4.1 and 4.2 are known, as their conjunction, not their sum (R13: G[A∪B] ≠ G[A] ∪ G[B]).]*

### 4.1 Static W (snapshot)

**Characteristics**

- **A photo.** The world moves continuously; the photo does not. Its weights, its size N and its nodes do not change. Nothing enters it.
- **A simulated world.** On the photo, actions and events are simulated — relaxing σ, clamping nodes, adding a weight or removing a node on a copy — to verify whether the premises of the Model hold under stated conditions. The copy is discarded; the photo stays.
- **What it verifies: premises.** Its properties are properties of the Model when W is static.
- **One interpretation — the domain of interpretation of M.M: declarations of device capabilities.** (The model has no domain. M.M's own definition gives its domain: *"devices MUST NOT publish events they can't yet generate nor functions they can not attend"* — declarations of functions and events, IAID 2024.) The Gatekeeper is a judge, not a door: it evaluates whether a declaration is coherent with the field (C1–C4) and returns a sentence: **valid or not valid**, with grounds. It does not admit anything: it lets nothing in and keeps nothing.
- **Components:** Gatekeeper, relaxation, c(S).

**Differences from dynamic W**

- Nothing is ingested; in dynamic W, the corpus ingests and W is rebuilt.
- Events are simulated, not real: what is simulated here is not the real dynamics of the field, but the dynamics of a world that does not move.
- It has no time: no before and after of W, no cycles, no trace.
- It can say *coherent*, not *true*: veracity (M.M) needs the trace, and the trace exists only under dynamic W.

#### 4.1.1 Knowledge Graph

CKM operates on a weighted graph G = (V, E, W, Δ) where V is a set of N knowledge nodes and two matrices encode distinct structural properties.

**W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes co-presence of nodes i and j in the same corpus unit, normalized to [−1, +1]. Positive when co-occurrence is unmarked; negative when the containing text carries an explicit opposition marker. The sign is a corpus property derived from structure, not an editorial assignment.

*[v28 — What W does not represent.* Co-occurrence is counted as presence. Non-co-occurrence is not represented: a pair that never co-occurs and a pair about which the corpus says nothing both take W_ij = 0. In CorpusService the only source of negative weight is the opposition marker, matched as a substring of the text and applied to every pair of that text. Absence relative to expectation, as a second representation of W, is left to future work (§8.5).*]

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes directional weight from node i toward node j, derived from citation or quote directionality. W and Δ must be maintained as strictly separate matrices. Mixing them destroys attractor geometry (§2.3: incorporating Δ into the weights reduced recovery from 0.78 to 0.02).

*[Negative weights (W_mixta, adversarial corpora) are a property of the sign of W, not a separate model: they can occur under static or dynamic W.]*

#### 4.1.2 Relaxation and Convergence

CKM uses Hopfield relaxation as a computational primitive. With symmetric W and asynchronous update, relaxation is guaranteed to converge to a fixed point by Lyapunov descent [Hopfield, 1982]. The synchronous implementation (`relax_orbit`, landscape_engine.py) carries a separate LaSalle guarantee: convergence to the maximal invariant set of period-2 orbits.

**GOLES condition** — The Goles theorem [Goles-Chacc et al., 1985] establishes that under symmetric W, synchronous dynamics converge to either a fixed point or a period-2 limit cycle; no cycles of period > 2 occur. The tiebreaking rule — when h_i = 0, node i retains its current state σ_i — is the precise mathematical modification that preserves this guarantee without indeterminate states. This is a required premise of the instrument: without it, two runs from similar σ₀ converging to the same period-2 orbit may return different terminal states. With it, the output is deterministic given (W, σ₀, seed). *[Verified: REG_orbitas_conjuntos_invariantes_v1; REG_seleccion_nodos_desempate_v1 §2.]*

Period-2 orbits dominate in the two N = 20 IAP corpora measured — 141/200 and 136/200 trajectories terminate in orbits rather than fixed points — but this is a property of those corpora, not of the synchronous dynamics: in the N = 32 working corpus the same measurement gives 3/200. Prevalence is corpus-dependent and is reported with the corpus. Ending in an orbit is orbital stability, not instability. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §2.]*

#### 4.1.3 Cohesion

c(S) = mean(W_ij · σ_i · σ_j) over all pairs i < j. Measures alignment of the active state with the co-occurrence structure. Negative of normalized Hopfield energy. The field can sustain states with high c(S) that destroy existing attractors — C2 of the Gatekeeper addresses this.

#### 4.1.4 The Gatekeeper

The Gatekeeper operates in the domain of declared agent capabilities, not corpus concepts. C3 — the M.M. criterion — evaluates whether a declared capability’s dependencies are satisfied in the active state. If not: the declaration fails verification. The Gatekeeper is a static model over MCP-declared capabilities (`process/initial_static_model/mcp_adapter.py`), verified in that domain at 0.092 ms per evaluation. Its extension to corpus concept admission is *proposed*, not verified.

*[Placement decided by the author: the Gatekeeper belongs to static W — its domain is the validation of capability declarations.]*

**Domains of application** (DEFS v14, delamor):

- **Declarations of device capabilities — its domain.** Defined by M.M (IAID 2024): functions a device can attend, events it can generate. Here nodes are capabilities (`mcp_adapter.py`: *"Nodes = declared capabilities, not concepts"*). Status: implemented; verified in that domain at 0.092 ms per evaluation.
- **Corpus concept nodes — transfer, open.** Applying C1–C4 to concept nodes is a transfer of the criterion to another domain. What is measured there (e.g. 0/16 nodes passing C1 at θ_W = 0.10; 16/16 at θ_W ≤ 0.01399) informs about the transfer, not about the Gatekeeper in its own domain.
- **Not a service.** No instance, state or lifecycle: it is a criterion. It returns a sentence; it does not let anything in. Node selection (elicitation of what exists) is not admission.

#### 4.1.5 Premises

### 4.2 Dynamic W

**Characteristics**

- **The world that moves.** The corpus ingests; W does not. At a rebuild W changes in one of three ways — its weights, its size N, or which node occupies each row (the three causes recorded by MonitorService: "pesos", "N", "nodos").
- **Plateaus and jumps.** Between rebuilds W is a plateau — a photo; at a rebuild it jumps. The criterion is the change of W, not the type of ingestion.
- *[v28 — delamor, 10 Oct.]* **The field does not jump; it is continuous.** What jumps is its representation. The corpus already belongs to the instrument — it samples the field in discrete texts — and extraction and W are further representations. A jump between two W is attributed to the instrument unless shown otherwise. The working proposal is to **align** the instrument's discontinuities — normalization of W by its largest entry, the selection borders of node extraction, whole-text sign routing, the extractor version, the per-cycle baseline of D_ckm, a θ_W that does not follow the scale of W — so that all of them fall on the rebuild, where whatever depends on scale is reborn or recalibrated.
- **Real events, observed.** Nothing is simulated: events happen, are observed, and leave a trace.
- **Components:** services with a lifecycle — CorpusService, NodeExtractor, WVersionManager, MonitorService and COCO, Firma_CKM, CKMLandscapeConfig.
- The corpus has phases — accumulation (no W yet) and evaluation. They are phases of the corpus, not of W.
- The IAP test series (§6) ran on dynamic W, in a live channel.

**Differences from static W**

- W changes; a static W never does.
- It observes instead of simulating: what happens cannot be undone, and it stays in the trace.
- It has time: cycles delimited by rebuilds (`w_version_id`), and a before and after across which metrics need a declared base.
- Veracity becomes verifiable: whether a device does what it declared (M.M) is in the trace.

#### 4.2.1 COCO and Field Regulation

COCO is a field regulator, not a field observer. It maintains `Δ_r_compresiones` — its own representation of accumulated metabolization, independent of Monitor’s `Δ_r_pares`. When D_ckm (§4.3.1) crosses its threshold, COCO applies OPERADOR_STOP_COCO: `Δ_r_compresiones ← alpha · Δ_r_compresiones`. Moving the trigger to D_masa_cuencas, which converges, is an open model decision (§8.3).

β_collective — the collective thermal parameter — emerges as a median of individual device parameters under interaction, without external calibration. It is implemented as an observation — computed, not yet acting on the field — and presented as a direction toward field self-observation: the field’s regulatory temperature derived endogenously from the interaction it regulates. *[Implemented as observation; regulatory role open. COCO was exercised in test drivers and was never connected to the live IAP channel.]*

#### 4.2.2 Δ_r and Metabolization

`Δ_r_pares` accumulates pairs that σ_prompt declared active but that did not survive relaxation. Leaving the fixed point does not remove them from the field: they persist as deformation of W_eff — the field metabolizes them. MonitorService is the sole writer of `Δ_r_pares`. COCO operates only on its own `Δ_r_compresiones`. The separation is a design property, not a constraint.

#### 4.2.3 Instrument Architecture

*[Descriptions taken from the module docstrings in `services/`.]*

- **CorpusService**: stateful; accumulates texts and builds W from co-activations, with negative contributions where the text itself carries an opposition marker (W ∈ [−1, +1]). Transitions automatically from accumulation to evaluation when enough data is present.
- **NodeExtractorService**: stateless, no LLM. Turns text into co-activations: `accumulate(texts)` yields co-occurring node pairs and counts; `evaluate(text, nodes)` yields σ ∈ {+1, −1}^N over known nodes. It decides which nodes exist.
- **CKMLandscapeConfig**: living contract of the landscape — N, μ_W, θ_W, threshold, β_c, sampling_mode, w_version_id. β_c is recalibrated at each rebuild as a function of μ_W and N.
- **WVersionManager**: lightweight trace marks of W versions (sha256, corpus size) — not a copy of W, the trace that W changed. W is invariant within a cycle; a change between corpus instances invalidates β_c without triggering recalculation.
- **MonitorService**: impartial observer; sole writer of `Δ_r_pares`; blind to regulation by object separation.
- **COCO**: field regulator over its own `Δ_r_compresiones`; triggers on D_ckm; executes OPERADOR_STOP_COCO. Exercised only in test drivers; never connected to the live IAP channel.
- **Gatekeeper**: static model over MCP-declared capabilities (`mcp_adapter.py`); 0.092 ms per evaluation.
- **Firma_CKM** (FirmaService): records the shape of the field at a given moment — sha256(W), D_ckm(t), temperature signal (TOO_COLD / NOMINAL / TOO_HOT), number of agents, timestamp, sha256(accumulated Δ_r). No content, no exchanged text, no agent names unless declared. It does not produce the trace; it makes the existing trace legible.

#### 4.2.4 Premises

*[Not everything that happens is a premise. Premises under dynamic W are chosen from the selected findings (§6.4) — or none, if that is the case. Pending author decision.]*

### 4.3 Landscape Model

#### 4.3.1 Basin Masses and N_eff

`count_attractors` is a Monte Carlo estimator of the maximal invariant set L. It samples initial states σ₀ and identifies distinct orbits reached after relaxation.

Count-based estimators suffer from coupon-collector bias: the count grows monotonically with n_runs. Basin masses — the fraction of sampled trajectories falling into each orbit — converge. With n_runs ≥ 1000, basin masses are stable to within ±1–5% across seeds in IAP corpora.

**N_eff = 1/Σm_i²** — the inverse Simpson diversity index [Hill, 1973] over the basin mass distribution — is the convergent estimator of landscape diversity; it equals exp(H₂), where H₂ is the Rényi entropy of order 2 over the basin-mass distribution. Its distance form is D_masa_cuencas = 1 − ln N_eff_t / ln N_eff_0. N_eff ∈ [1, |L|]. N_eff = 1 is total collapse to a single attractor. N_eff = |L| is perfect equidistribution, unreachable under real W. The non-convergence of D_ckm under sampling variation established that count-based approaches are not appropriate for this measurement. N_eff is the result of that diagnostic.

**Validation against exact enumeration.** For three N = 20 corpora from the IAP series, all 2²⁰ = 1,048,576 states were enumerated (≈16 s per corpus with trajectory memoization), giving exact basin volumes under the uniform reference measure on {−1,+1}^N. Against this ground truth, with a sampling budget of 100,000 initial states:

| Basin-mass regime | Error of orbit count | Error of N_eff |
|---|---:|---:|
| Flat mass | 0% | 0.3% |
| Intermediate mass | 15% | 0.6% |
| Concentrated mass | 28% | 0.0% |

With a budget of 1,000 in the concentrated regime, the orbit count errs by 91% while N_eff errs by 0.4%. N_eff behaves as a count — the number of effectively occupied basins — but converges as a mass. *[Verified: REG_orbitas_conjuntos_invariantes_v1 §10; CRITERIOS_diversidad_formulacion_v1 §C.2.]*

#### 4.3.2 Premises

---

## 5. Empirical Validation

### 5.1 Corpus and Conditions

Two external adversarial debate corpora: fourforums gun control (IAC v2) and CreateDebate gun control. N = 32 nodes (fourforums), N = 64 nodes (CreateDebate). Both corpora were constructed from genuine adversarial debate — positions in structural opposition by design. W_mixta is applicable in this domain.

Fourforums is distributed as part of the Internet Argument Corpus v2 [Abbott et al., 2016]: 414,453 posts, 539,658 citations, 3,453 authors, 905 gun-control discussions; stance labels from crowd annotation, 304 authors labeled (T0 = 96 pro-control, T1 = 208 anti-control).

*[Condition — negative pair detection: opposition-marker routing assigns negative weights when lexical markers appear in texts. The procedure has no null outcome — it always finds markers in sufficiently long texts. The resulting negative weights measure structural tension only when the corpus was elicited with opposing positions by design. In single-author records or coordination corpora — including the IAP channel — the same markers function as discourse connectors, not structural opposition; such corpora are treated as W_pos. Verified: REG_unidad_texto_saturacion_v1 §5.]*

*[v28 — Two points to state.* (1) In the fourforums pipeline v8h the sign does not come from lexical markers but from crowd annotation of quote–response pairs (MTurk disagree/agree, −5…+5), and its nodes are authors: 60 negative directed pairs, all crossing stance. Which W each of P5–P7 rests on — marker-routed terms or annotated authors — should be named in §5.2. (2) "Treated as W_pos" is a reading convention; in the preserved IAP traces CorpusService did route markers, and some negative weights there come from a substring ("but" inside "distri**but**ion") and from narrative connectors. See §6.2.]*

All results in §5 are from static W snapshots built from complete corpus dumps. Dynamic reconstruction (CorpusService) was not used. The validations test properties of W, not properties of W under continuous accumulation.

### 5.2 Predictions and Results

**P1 — Hysteresis.** The field exhibits path-dependent c(S) under node incorporation and removal. Branch UP ≠ branch DOWN. *Not testable on a non-negative W snapshot (mathematical).* With W ≥ 0 there is no frustration [Harary, 1953; Toulouse, 1977]: the all-+1 state is a global, absorbing minimum, and the DOWN branch cannot leave it. Measured: m_down ≡ 1.0 in three runs on `W_ckm_corpus_v2` (N = 32, min W = 0). The statistic then reduces to 1 − mean(m_up) — how far the UP branch is from saturation — and is not a loop area. The April figures have no recoverable code. P1 remains open on a W that evolves.

**P2 — Cascade distribution.** k-core removal produces cascade sizes following power-law P(s) ∝ s^-τ with τ ∈ [1.5, 2.0] in the critical zone [Bak, Tang & Wiesenfeld, 1987]. *Not measurable at N = 32 (experimental).* At thresholds θ in the 0.3, 0.5 and 0.7 quantiles of the positive weights, each graph yields fewer than 10 cascades of size ≥ 2 (6, 4, 0 and 2, 5, 7); a fit needs at least 10, and the range does not reach 1.2 decades. Measuring it requires k ≥ 3 and N of 50–100 or more.

**P3 — Temporal asymmetry.** Incorporating a node produces measurable asymmetry in c(S) relative to removing it. The field does not undo. *Not tested (mathematical).* The k-core form — remove a node and count pruning rounds, re-add it and count bootstrap rounds — follows from the uniqueness of the k-core of a fixed graph [Seidman, 1983]: re-addition recovers in reverse order what removal pruned, and the equal rounds and recovery 1.000 observed in six graphs are what that result predicts. *[v28: "cannot fail… is a theorem, not a finding" → referencia — criterio 1.]* The temporal form, with relaxation times, requires dynamics that a snapshot does not have.

**P4 — Optimal density.** W_mixta produces a maximum of c(S) at an interior density ρ* < 1. *Not testable with random subsets on a W snapshot (mathematical).* By linearity, E[c(S)] = mean(W)·g(ρ), with g the same for every pair, so an interior ρ* occurs if and only if mean(W) < 0, regardless of where the negative pairs are (operator check: 20 negative pairs → ρ* = 1.0; 30 → 0.509; 60 → 0.541). With W ≥ 0, ρ* = 1.0 always. The protocol measures the sign of mean(W), not the effect of frustration.

*[P1–P4: BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1 (5 Oct 2026); INFORME_verificacion_P1_P4_v2 §3–§5; OBS_P1_run_P1_y_coercitividad_04oct_v1 §6.]*

**P5 — Diversity collapse.** Adversarial corpus produces two dominant attractor clusters. High-tension W_mixta reduces N_eff significantly compared to W_pos on the same corpus. *Verified.* *[Verified under uniform σ₀ sampling. In low-density, discrete-weight corpora, tie-breaking can dominate the count rather than basin structure; P1–P4 are not affected — they do not use the attractor count.]*

**P6 — Directional flow.** Δ encodes directional asymmetry not captured by W. Direction_score discriminates attractor types that c(S) alone cannot separate. *Verified.*

**P7 — Type-965 node.** Every field with genuine structural tension contains at least one node with high in-degree and near-zero out-degree in Δ — a structural *sostenedor* (sustaining node). Confirmed in fourforums (Author 965, ratio 455×) and CreateDebate (Author 204, ratio 296×). Both appear as tension anchor in 89% of identified tension pairs across both corpora. *Confirmed in two independent corpora. Domain universality: open.*

### 5.3 What P1–P7 Establish

These predictions were formulated on the CKM working corpus and tested on external corpora without modification to the model. The structural properties hold across distinct adversarial debate domains. Whether they hold outside adversarial debate is an open question — the corpora used were selected precisely for structural tension, and W_mixta requires that precondition to measure what it claims to measure.

---
## 6. IAP Test Series

*The IAP series ran on dynamic W (4.2) and is reported apart. It is an experience, not an experiment: what was evaluated was the live channel itself.*

*Framing (delamor, 7 Oct 2026).* The series is neither good nor bad, nor is it set aside as error: it is part of the project's trace. The instrument conditions found later (an `on_message`-only trigger that makes collective silence absorbing by construction, a fallback that read NOMINAL by absence, two COCO instances, a single relaxation phase chosen by the parity of `max_iter`) are reported as the conditions under which the series occurred, not as faults that invalidate it. They were seen *through* the series. The series is frozen and is not reproducible; it is not re-interpreted and it is not used to validate later changes, each of which is validated by its own tests under declared conditions. What happened in it, the silence included, stands as trace.

### 6.1 Channel Design

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
(§2.3). CKM's effective minimum has not been established; N=32 is treated
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
whose pair-extraction was corrected in September 2026. The case-series
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

*[v28 — Further conditions of the instrument during the series* (read on
preserved traces, 10 Oct 2026). SYSTEM join messages entered the corpus as
texts and became nodes (`joined`, `joined channel`); W was rebuilt at every
ingest, one W per text, so D_ckm moved while the channel was still empty;
device names and formatting bigrams entered as nodes; in replayed runs each
message was counted as a distinct device; and marker routing produced
negative weights from a substring and from narrative connectors. They are
listed as conditions under which the observations of §6.4 were taken, not as
corrections of them.*]

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

**Coupled silence (Case 0.12):**
A device that does not read the channel still depends on it for execution
rhythm — triggers arrive only when new messages appear. Inactivity and
silence are not equivalent. A device can be silent (OP_SILENCE) while
actively participating in the field's timing structure. This was observed,
not designed. It is a property of the channel architecture, not a behavior
chosen by the device.

**Sentinel leak (Case 0.13):**
The OP_SILENCE sentinel was leaking into published text rather than
suppressing publication. 52% of texts in that run were unrecognized silences
that reached the corpus. The fix was verified in Case 0.14. The leaked texts
contaminate W for that run — the structural trace of Case 0.13 is not
interpretable as a field observation.

**TinkerBellucio refusal (Case 0.15):**
TinkerBellucio (Sonnet 4.6) declined to produce a tension map when the
channel was empty. The refusal was epistemically appropriate — a tension
map requires tension content to analyze. The absence of fabrication left
MarkOpolus (Opus) without the material it expected.

*What this demonstrates:* that a device can refuse to generate content
when the request lacks traceable grounding.

*[AUTO-1 — see Appendix A]*

*What this does not demonstrate:* that this behavior is general, that it
would occur without the project context contamination, or that it constitutes
a validated test of FabricationService's detection capacity. FabricationService
was not the mechanism of refusal — the device itself refused. The service
detects fabrication when it occurs; it did not need to activate here.

**D_ckm negative values:**
D_ckm = (A0 − A_actual) / A0. When D_ckm < 0, A_actual > A0: the field
has more accessible attractors than at baseline. This is not a deficit or
an error — the sign reflects the direction of change, not a quality judgment.

In Case 0.12, D_ckm = −7.5 was recorded in the first live group-channel run.
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

*[AUTO-2 — see Appendix A]*

**trace_ip:**
The monitoring infrastructure identifies a moment t_i in the trajectory
where accumulated interactions show distributional pattern changes.
The action a_{t_i} is observable in the trace. Whether a device
recognized that moment and acted from that recognition is not verifiable
by the instrument. trace_ip is a concept with a documentable instance —
it is not yet an operationalized measure.

### 6.5 What the Series Does Not Establish

The IAP series is a set of tests run live. It cannot be reproduced —
each run is a distinct live interaction — and its cases are not comparable. The following claims are not supported by
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

BehaviorGraph G — a second behavioral matrix over a fixed vocabulary (TERMAP_behavior_v1.json, 18 nodes) — was integrated in Case 0.15 as a proof of concept. It is not included as a standalone section in this paper. The matrix exists in the repository; its interpretability at current corpus scale has not been established, and D_G has not been analyzed against a baseline. *[Implemented; not validated.]*



## 7. Discussion

### 7.1 What CKM Measures That Existing Instruments Do Not

Behavioral metrics for multi-agent systems typically measure what individual
agents produce — output volume, task completion, response latency — or
whether agents agree with each other, via semantic similarity or embedding
distance. These measurements are valid for what they target. They do not
capture the structural state of the shared knowledge field: the pattern
of co-dependencies between active concepts, the directional flows of
citation and argument, the distribution and diversity of stable attractor
states accessible to the field as a whole.

CKM measures the geometry of that structure. c(S) measures alignment between the active state and the weight structure of the field. N_eff = 1/Σm_i² measures effective attractor diversity over basin masses — the convergent estimator; D_ckm was the path to establishing it. Cluster frontier coercivity measures structural resistance to state reversal. These are structural quantities — they describe the landscape, not the content.

*[AUTO-3 — see Appendix A]*

What can be stated: these quantities are not derivable from behavioral
or semantic similarity metrics alone. Whether they are informative under
the conditions of real deployment remains an empirical question beyond
the scope of this work.

### 7.2 The observe() Tension

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

### 7.3 D_ckm Negative Values

D_ckm = (A0 − A_actual) / A0. Negative values mean A_actual > A0:
more attractors accessible than at baseline.

The name "D_ckm" suggests distance — and distances are non-negative by
convention. D_ckm is a ratio of change in attractor capacity relative to a
fixed baseline; the sign encodes direction, not magnitude of a deficiency.
The *d* does name a distance, however: D_ckm is term-by-term the D_contextual
introduced in May 2026. What does not hold is the reading of positive
values as "degradation" — that is an interpretation attached to the label.

In Case 0.12 the first live group-channel run produced D_ckm = −7.5. Earlier
drafts read this as the expected signature of a field that gained structural
complexity through interaction. That reading is withdrawn (§6.4): the sign of
D_ckm does not converge at the n_runs used in the IAP series, so the run
does not establish the direction it appeared to show. The general point is
unaffected — a negative D_ckm is not an anomaly — but it no longer rests on
that measurement.

The convergent quantity is N_eff over basin masses, and its distance form
D_masa_cuencas is now computed per evaluation. Re-analyzing the recorded IAP texts
over N_eff at n_runs ≥ 1000 is the step that would settle what Case 0.12
showed.

The naming carries a bias. Recognizing that bias is part of reading the
instrument correctly.

### 7.4 Current Conditions

**Scale:** the predictions P1–P7 were verified at N = 32 — the verification
is real. What is constrained is the interpretability of D_ckm and c(S) as
field-level quantities at that scale. The ~128 associative minimum of
classical Hopfield networks is not the applicable reference: it governs
Hebbian storage of uncorrelated patterns, and CKM stores no patterns (§2.3). CKM's own effective minimum is undetermined and depends on corpus
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
in September 2026 and one remains open. All results in this paper
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
verified in unit tests and test drivers; it was never connected to the
live IAP channel. Whether the field can know itself — not as a thermostatic
function but as the emergent property of real contact between agents —
is a conceptual gap the model names and preserves. It is not addressable
by further implementation without first resolving what form that
self-knowledge would take.

### 7.5 The Landscape Driven Devices Framing — What It Does and Does Not Claim

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

*[AUTO-4 — see Appendix A]*

### 7.6 Knowledge Representation and the Cohesive Turn

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

*[AUTO-5 — see Appendix A]*

---
## 8. Conclusions and Future Work

### 8.1 What This Work Establishes

CKM is a formal framework for measuring structural field properties
in multi-agent knowledge systems. It measures the geometry of the
co-occurrence landscape — how that geometry changes under interaction,
and whether it has the structural properties associated with genuine
interdependence rather than fabricated coherence.

Seven predictions were tested:

| Prediction | Status | N verified |
|---|---|---|
| P1 — Macroscopic hysteresis: incorporating ≠ removing | Not testable on a non-negative W snapshot (mathematical): W ≥ 0 makes all-+1 absorbing; the DOWN branch is constant. Open on an evolving W | — |
| P2 — Cascade distribution P(s) ∝ s^{-τ}, τ∈[1.5,2] | Not measurable at N = 32 (experimental): fewer than 10 cascades of size ≥ 2 per graph | — |
| P3 — Temporal asymmetry: removal relaxation > incorporation | Not tested (mathematical): the k-core form is reversible by uniqueness of the k-core; the temporal form was not run | — |
| P4 — Interior optimal density Ω* in W_mixta | Not testable with random subsets (mathematical): interior Ω* ⇔ mean(W) < 0 | — |
| P5 — Adversarial corpus collapses attractor diversity | Verified | 32 |
| P6 — Δ as symmetry-breaking for ambiguous states | Verified (T0 cites T1 at 2.18×, T1 internal cohesion 3.05×) | fourforums |
| P7 — Type-965 node present in systems with genuine structural tension | Confirmed in two independent corpora; open as universal claim | CreateDebate + fourforums |

One hypothesis was falsified: H_STOP (monotonicity of D_ckm under STOP)
did not hold; reformulated as function of A_pre, not D_ckm.

*[AUTO-6 — see Appendix A]*

The empirical results establish structure at small scale (N=32). They are
treated as orientation findings, not population-level claims. The scale
condition is CKM's own and undetermined; the ~128 Hopfield associative
minimum is not the reference (§7.4).

### 8.2 What the Infrastructure Establishes

The following services are operational. *[v28 — counts of passing tests are not reported in the body; the test suite and its result are recorded with the frozen release cited in Code Availability (delamor, 10 Oct).]*

- **COCO** (coco.py): β inferred from rejection history, not declared; β_c derived analytically from μ_W and N and recalibrated at each rebuild through CKMLandscapeConfig. Executes OPERADOR_STOP_COCO — compresses `Δ_r_compresiones` by α ∈ [0.05, 0.30] — when D_ckm (basin-mass form) crosses a threshold. *[v28 — confirmed by delamor, 10 Oct.]* The firing rule is verified by a sweep over threshold values against known D_ckm inputs. Threshold values are set by calibration, which, as in any instrument, is performed whenever the conditions of use require it — for a given corpus, unit or regime — and not once for every possible case. Calibration is implemented as a mechanism of the instrument, and whether it calibrates is itself verified. Its operation on the live IAP channel is pending. *[v28: retirado el ejemplo β_c ≈ 13.83, que salía de la W v2 de origen UNKNOWN.]*
- **FabricationService**: *[v28 — confirmado por delamor, 10 Oct.]* being rewritten from the fabrication index already used by MonitorService and COCO — the fraction of nodes a text declares active that the field's relaxation rejects. Further detection is analyzed on the rewritten service.
- **Firma_CKM**: certifies structural trace (six canonical fields) — analogous to a notary, not a Certificate Authority.
- **WVersionManager**: lightweight trace — records when W changed, enables sha256(W_momento).
- **IAP Chatroom**: FastAPI + Gradio, MCP server (6 tools), n_agentes detection including passive human presence.
- **MonitorService**: accumulates Δ_r; trace_ip identified as a formal concept.

These services constitute a working implementation of a structural field
measurement layer for multi-agent systems. They are a research instrument
whose calibration is documented, not a product.

### 8.3 Preserved Conditions

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
and the Hopfield associative minimum does not supply it (§7.4). All empirical
results carry this qualification.

**Which quantity drives regulation.** COCO triggers on D_ckm, computed from
attractor counts, which do not converge. D_masa_cuencas, computed from basin
masses, does converge and is already reported per evaluation. The operator
has not been moved. Whether it should is a model decision, not an
implementation one.

### 8.4 Convergences by Independence

Three structural convergences were identified retrospectively:

- **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Verifiable from dated working documents.
- **CKM attractor architecture → J-space (Gurnee et al., July 2026):** Shared structural features arrived at independently. *[Observed: structural analogy, not formal correspondence.]*
- **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025):** Same structural problem.

### 8.5 Future Work

*[v28]* **Absence as a second representation of W.** Presence leaves
non-co-occurrence unrepresented. A representation by absence relative to
expectation (φ, PMI) would give negative weights from the corpus itself,
without lexical markers. An exploratory run, outside the repository
extractor, compared the fraction of frustrated triangles of such W with a
permutation null on the working-reports corpus and two IAP traces, and found
it below the null in the three; it is reported only as a direction, to be
measured with the repository extractor.

*[v28]* **Instrument before field.** Tests of the instrument precede new
field claims: marker matching, SYSTEM messages, stability under a neutral
ingest, declaration of each W (extractor, unit, normalization), and a planted
field whose sign is set when the corpus is generated — a known-answer pattern
for any representation of sign. The fourforums annotation is the external
known-answer corpus for the same question.

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
so far. Objectives and tasks must require sustained coordination
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
## Code Availability

*[v28]* The implementation, the test suite and the data used in §5 are available at the repository release that freezes this version of the paper: [RELEASE — tag, commit hash, DOI — se completa al congelar]. The result of running the full test suite on that release, with date and environment, is recorded in its release notes.

## Acknowledgments and Disclosure of AI Assistance

This work was developed in sustained interaction with AI systems, a condition
described in §3.2. Claude Sonnet 4.6 (Anthropic), used through chat interfaces
and through Claude Code, took part in the conceptual development, the
implementation of the experimental code, the execution and analysis of
experiments, and the drafting of earlier versions of this manuscript. Claude
Opus 5.5 (Anthropic) was used for editorial revision of this version and for
re-verification of the bibliographic references. The author has reviewed all
content, verified all references, and takes full responsibility for the
manuscript, including any remaining errors. In accordance with arXiv policy,
AI systems are not listed as authors.

---

## 9. References


### Primary Sources — Project Documents

gadanin.delamor. (2023). *MENTIRIS.MORIERIS: Interaction of Artificial
Intelligent Devices based on Neural Call Protocol.* Working documents:
LEONARDO.txt, README (timestamp 7/10/23), Informe_MM.docx.

gadanin.delamor. (2026). *CKM — Cohesive Knowledge Model: Working
Reports v2–v31.* Unpublished. Repository: gadanindelamor/ckm.

### Attractor Networks

Hebb, D.O. (1949). *The Organization of Behavior: A Neuropsychological
Theory.* New York: Wiley.

Hopfield, J.J. (1982). Neural networks and physical systems with emergent
collective computational abilities. *PNAS*, 79(8), 2554–2558.

Ramsauer, H., Schäfl, B., Lehner, J., Seidl, P., Widrich, M., Adler, T.,
... & Hochreiter, S. (2021). Hopfield Networks is All You Need.
*International Conference on Learning Representations (ICLR 2021)*.
https://openreview.net/forum?id=tL89RnzIiCd

### Graph Structure and Criticality

Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core
percolation on complex networks. *Physical Review E*, 73(5), 056101.

Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality.
*Physical Review Letters*, 59(4), 381–384.

*[v28]* Harary, F. (1953). On the notion of balance of a signed graph.
*Michigan Mathematical Journal*, 2(2), 143–146. [VERIFY]

*[v28]* Seidman, S. B. (1983). Network structure and minimum degree.
*Social Networks*, 5(3), 269–287. [VERIFY]

*[v28]* Toulouse, G. (1977). Theory of the frustration effect in spin glasses: I.
*Communications on Physics*, 2, 115–119. [VERIFY]

Beggs, J. M., & Plenz, D. (2003). Neuronal avalanches in neocortical circuits.
*Journal of Neuroscience*, 23(35), 11167–11177.
https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003

Moretti, P., & Muñoz, M. A. (2013). Griffiths phases and the stretching of
criticality in brain networks. *Nature Communications*, 4, 2521.
https://doi.org/10.1038/ncomms3521

Pázmándi, F., Zaránd, G., & Zimányi, G. T. (1999). Self-organized criticality
in the hysteresis of the Sherrington-Kirkpatrick model. *Physical Review
Letters*, 83(5), 1034–1037. https://doi.org/10.1103/PhysRevLett.83.1034

### Multi-Agent Systems

Zhu, K., et al. (2025). MultiAgentBench: Evaluating the Collaboration and
Competition of LLM agents. *Proceedings of ACL 2025 (Long Papers)*.
arXiv:2503.01935.
https://arxiv.org/abs/2503.01935

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N.,
... & Kiela, D. (2020). Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing
Systems*, 33, 9459–9474.


### Knowledge Graph Representation

Speer, R., Chin, J., & Havasi, C. (2017). ConceptNet 5.5: An open multilingual
graph of general knowledge. *Proceedings of AAAI-17*, pp. 4444–4451.
https://doi.org/10.1609/aaai.v31i1.11164

Hogan, A., et al. (2021). Knowledge graphs. *ACM Computing Surveys*, 54(4),
Article 71. https://doi.org/10.1145/3447772

Mohammad, S., Kiritchenko, S., Sobhani, P., Zhu, X., & Cherry, C. (2016).
SemEval-2016 Task 6: Detecting stance in tweets. *Proceedings of SemEval-2016*,
pp. 31–41. https://doi.org/10.18653/v1/S16-1003

Hill, M. O. (1973). Diversity and evenness: A unifying notation and its
consequences. *Ecology*, 54(2), 427–432.

Goles-Chacc, E., Fogelman-Soulié, F., & Pellegrin, D. (1985). Decreasing energy functions as a tool for studying threshold networks. *Discrete Applied Mathematics*, 12(3), 261–277.

Ghosh, S., Singhania, P., Singh, S., Rudra, K., & Ghosh, S. (2019). Stance
detection in web and social media: A comparative study. *CLEF 2019*, LNCS
11696, pp. 75–87. https://doi.org/10.1007/978-3-030-28577-7_4

Kawintiranon, K., & Singh, L. (2021). Knowledge enhanced masked language model
for stance detection. *NAACL-HLT 2021*, pp. 4725–4735.
https://doi.org/10.18653/v1/2021.naacl-main.376

### Belief Networks and Contagion

Aiyappa, R., Flammini, A., & Ahn, Y.-Y. (2024). Emergence of simple and
complex contagion dynamics from weighted belief networks. *Science Advances*,
10(15), eadh4439. https://doi.org/10.1126/sciadv.adh4439

### Corpora

Abbott, R., Ecker, B., Anand, P., & Walker, M. (2016). Internet Argument
Corpus 2.0: An SQL schema for dialogic social media and the corpora to go
with it. *Proceedings of LREC 2016*. https://aclanthology.org/L16-1704/

### Basins of Attraction

Menck, P. J., Heitzig, J., Marwan, N., & Kurths, J. (2013). How basin
stability complements the linear-stability paradigm. *Nature Physics*, 9(2),
89–92. https://doi.org/10.1038/nphys2516

Daza, A., Wagemakers, A., Georgeot, B., Guéry-Odelin, D., & Sanjuán, M. A. F.
(2016). Basin entropy: a new tool to analyze uncertainty in dynamical systems.
*Scientific Reports*, 6, 31416. https://doi.org/10.1038/srep31416

### Belief Propagation

Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief
propagation and its generalizations. In *Exploring Artificial Intelligence in
the New Millennium*, Chapter 8, pp. 239–269. Morgan Kaufmann.

### Landscape-Driven Dynamics

Thirumalaiswamy, A., Riggleman, R. A., & Crocker, J. C. (2025). Slow
relaxation and landscape-driven dynamics in viscous ripening foams.
*Proceedings of the National Academy of Sciences*, 122(47), e2518994122.
https://doi.org/10.1073/pnas.2518994122

### Global Workspace and Interpretability

Gurnee, W., Sofroniew, N., Pearce, A., et al. (2026, July 6).
Verbalizable representations form a global workspace in language models.
*Transformer Circuits Thread*, Anthropic.
https://transformer-circuits.pub/2026/workspace/index.html

Baars, B. J. (1988). *A Cognitive Theory of Consciousness.*
Cambridge University Press. ISBN 0521427436. 448 pp.

### Declared Influences

Shaw, F. (2014). *La otra atención: Notas del trabajo con Michel de Salzmann
(Chandolin, 1993–2000).* Sennin Editores. ISBN 978-987-28459-7-1.

Fremantle, C. (1993). *On Attention.* Indications Press.

---

## Appendix A — Writing Trace

The following entries record moments during writing where an automatic pull was noticed and resisted (see §3.4). Each entry is referenced in the text as AUTO-n.

**AUTO-1** (§6.4) — tendency to write "demonstrates" for Case 0.15 — resisted. The refusal is documented behavior, not a demonstration of system capability under controlled conditions.

**AUTO-2** (§6.4) — pull to keep the original reading with a softening qualifier. Resisted — the qualifier would preserve the claim while appearing to weaken it. The claim depends on a quantity that does not converge in the regime where it was taken.

**AUTO-3** (§7.1) — pull to write "CKM therefore captures something fundamentally new." Resisted — "fundamentally new" is a claim about the state of the field that would require systematic comparison with existing instruments. That comparison has not been done here.

**AUTO-4** (§7.5) — pull to write "the IAP series provides preliminary evidence for LDD behavior." Resisted — preliminary evidence requires at minimum a defined criterion for what would count as evidence. That criterion does not exist in the current analysis.

**AUTO-5** (§7.6) — pull to write "CKM resolves the limitations of static KR." Resisted — CKM does not resolve them. It inhabits and structures the space they left open.

**AUTO-6** (§8.1) — pull to write "these results demonstrate CKM's validity as a measurement framework." Resisted — they demonstrate that specific structural properties exist in the tested corpora under stated conditions. Generalizability requires corpora the project has not accessed.
