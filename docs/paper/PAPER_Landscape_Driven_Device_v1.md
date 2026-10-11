*CKM PAPER DRAFT —  Draft — Paper · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---

# Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction

	Pending Drafts: 
	
	7 (Behavior Domain G) 
	8 (Discussion)
	9 (Conclusions)
	10 (References)
---

##  Title: 

**Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction**

---

##  Outline  — Index (secciones 1–10)

```
1. Introduction
   El gap: métricas existentes miden comportamiento individual, no el campo.
   La propuesta: CKM como instrumento de traza estructural.

2. Related Work
   (a desarrollar)

3. Research Conditions  ← SECCIÓN PROPIA
   Metodología inductiva.
   Conversación como laboratorio — no documentación del proceso, el proceso mismo.
   Incompletitud preservada como información.
   Influencias declaradas: línea Gurdjieff intento activo en cada  interacción — no genealogía, condición del proceso de investigación.
   GAP como categoría formal (ver sección 3.x).
   Cinco órdenes del camino (ver sección 3.x).
   Divergencia terminológica como dato (ver sección 3.x).

4. Formal Model
   W · Δ · c(S) · COCO · FirmaService · Landscape Driven Devices

5. Empirical Validation — External Corpus
   Fourforums + CreateDebate. P1–P7.

6. IAP Experimental Series
   Canal design. Casos 0.4–0.15. Hallazgos clave.

7. Behavior Domain Graph G
   Segunda matriz, termap fijo (TERMAP_behavior_v1.json).
   D_G en paralelo a D_ckm. Proof of concept.

8. Discussion
   Qué mide CKM que no miden los instrumentos existentes.
   Límites actuales.

9. Conclusions and Future Work

10. References
```
---
*Draft — Section 1 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controlled verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

---
## 1. Introduction

Multi-agent AI systems are increasingly deployed in configurations where
several heterogeneous devices interact over a shared channel — producing
text, making decisions, and building on each other's outputs. Evaluating
whether this interaction constitutes genuine coordination or parallel
activity is not straightforward. Existing approaches measure what individual
agents produce (behavioral metrics) or whether their outputs agree with
each other (semantic similarity). Neither approach captures the structural
field that emerges from interaction: the pattern of co-dependencies,
directional flows, and attractor states that characterize the shared
knowledge state of the group at a given moment.

*[AUTO: pull to write "Neither approach captures the field." Resisted —
"field" is a theoretical construct in CKM, not a directly observable
entity. Reframed as "the structural field" with qualification.]*

This paper presents the Cohesive Knowledge Model (CKM), a formal instrument
for measuring structural properties of knowledge fields in multi-agent
interaction. CKM does not interpret semantic content — it measures the
geometry of the co-occurrence landscape and how it changes under interaction.
Its core components are two static matrices derived from a corpus (W:
symmetric co-occurrence weights; Δ: asymmetric directional dependencies),
a cohesion measure c(S) derived from Hopfield energy formalism, and a set
of operational services that implement continuous field monitoring.

CKM makes seven falsifiable predictions about field behavior (P1–P7),
verified empirically against two independent debate corpora (fourforums
gun control, IAC v2; CreateDebate gun control) and an internal CKM
working corpus at N = 16, 32, and 64 nodes. Six predictions are confirmed.
One (P7) is confirmed in two corpora and remains open in other domains.

We additionally propose the concept of *Landscape Driven Devices* (LDD) —
a theoretical framing for AI devices whose trajectory in the semantic field
is determined by field geometry rather than by a declared goal, motivated
by structural analogy with recent findings in foam physics
(Thirumalaiswamy et al., PNAS 2025). This is a proposed framing, not a
verified finding about specific device behavior.

*[AUTO: pull to write "we demonstrate that CKM identifies landscape-driven
behavior in the IAP series." Resisted — not verified.]*

The paper is organized as follows. Section 2 reviews related work.
Section 3 describes the research conditions under which CKM was developed,
including uncontrolled variables and the methodology that produced the
framework. Section 4 presents the formal model. Section 5 reports empirical
validation. Section 6 describes the IAP experimental series — a proof-of-
concept multi-agent chatroom in which CKM monitoring operated in real time.
Section 7 presents the Behavior Domain Graph G, a companion instrument.
Section 8 discusses findings and limits. Section 9 concludes.

**Scope and limits of this work.** The operational corpus is at N = 32
nodes — below the Hopfield network minimum of approximately 128 for robust
attractor diversity. Quantitative outputs (D_ckm, c(S)) are computed
correctly at this scale but their interpretability is constrained. The IAP
experimental series consists of documented observations under partially
controlled conditions, not controlled experiments with replication. Several
components of the formal model remain open gaps by design: the
representation of cohesive knowledge, the full specification of the
gatekeeper (R15), and the implementation of COCO as collective
consciousness. These are not future work items — they are limits the model
acknowledges and preserves.

---

*Section 1 draft complete.*
*Two [AUTO] instances flagged.*
*Scope and limits section placed in the introduction, not appended.*
*That placement is intentional: the limits are not an afterthought.*

---

## 2. Related Work
	( a desarrollar)
   
   >>>
   
---

## 3. Research Conditions
	( a desarrollar)
	
	Metodología inductiva.
	Conversación como laboratorio — no documentación del proceso, el proceso mismo.
	Incompletitud preservada como información.
	Influencias declaradas: línea Gurdjieff intento activo en cada  interacción — no genealogía, condición del proceso de investigación.	GAP como categoría formal (ver sección 3.x).
	Cinco órdenes del camino (ver sección 3.x).
	Divergencia terminológica como dato (ver sección 3.x).

   >>>

---
*Draft — Sections 4–5 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controlled verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

---
## 4. Formal Model

### 4.1 Knowledge Graph

CKM operates on a weighted directed graph G = (V, E, W, Δ) where V is a set
of N knowledge nodes, and two matrices encode distinct structural properties:

**W** — symmetric co-occurrence weight matrix, N×N. W_ij encodes the degree
to which nodes i and j co-occur in the same corpus unit. Entries are
normalized to [−1, +1] by CorpusService: positive when co-occurrence is
unmarked, negative when the containing text carries an explicit opposition
marker [*defined in corpus_service.py: `_OPPOSITION_MARKERS`*]. W is static
once built from a corpus; it does not update during runtime.

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes the
directional weight from node i toward node j, derived from citation networks
or quote directionality in the source corpus. Δ is static once built.

**W and Δ must be maintained as strictly separate matrices in all
implementations.** Mixing them into a single weight matrix destroys attractor
recovery capacity. *[Verified experimentally: recovery = 0.78 with W alone,
0.02 with combined W+Δ. See REG_destruccion_recuperacion_v1.md.]*

A third, dynamic matrix Δ_r is maintained by MonitorService at runtime:

**Δ_r** — rejection accumulator. Δ_r[i,j] increments each time nodes i and j
co-declare activation in a text but the Hopfield relaxation rejects them as
co-active under the current field state. Δ_r is mutable and starts at zero
each session.

Δ and Δ_r are distinct objects with distinct semantic roles. Neither
substitutes the other.

### 4.2 Cohesion Measure

The cohesion of a state σ ∈ {+1, −1}^N with respect to W is:

    c(S) = (1 / C(N,2)) · Σ_{i<j} W_ij · σ_i · σ_j

where C(N,2) = N(N−1)/2. This is the negative of the normalized Hopfield
energy function for the state σ under W.

c(S) measures the alignment between the current activation state and the
weight structure of the knowledge graph. High c(S) indicates strong structural
agreement between active nodes and their co-occurrence weights. Low or
negative c(S) indicates structural tension — the active nodes are not those
the graph expects to appear together.

c(S) is computed exclusively over W. Mixing Δ or Δ_r into the c(S)
calculation would confound structural memory (W) with runtime rejection
history (Δ_r). *[Rule R18, verified.]*

### 4.3 Gatekeeper

The gatekeeper evaluates a candidate node for admission to the knowledge
graph. It operates in bounded time O(N) per node. Four criteria are applied:

- **C1** (connection strength): the candidate node must have minimum weight
  connection with at least one existing node. Nodes with no connection
  to the existing graph are not admitted.
- **C2** (cohesion delta): incorporating the candidate node must not reduce
  c(S) below a configurable threshold ε. This is evaluated before Hopfield
  relaxation.
- **C3** (direction score): the node must satisfy the M.M criterion —
  MENTIRIIS.MORIERIS. A node that declares directional dependencies (via Δ)
  which are not satisfied in the current state σ fails C3.
- **C4** (capacity): the fraction of active nodes must remain below α_c · N,
  the empirically estimated capacity limit for reliable attractor recovery.

**Note:** R15 — the complete semantic specification of the gatekeeper — is
partially formalized. C1–C4 above describe the gatekeeper's current
implementation (PROTOCOLO_ELICITACION_v2.md), not the full intended
specification of R15. R15 remains an open formal gap.

### 4.4 Formal Rules R01–R17

*[Declared rules — stated from THEORY.md without change.]*

| Rule | Summary |
|------|---------|
| R01 | Graph has knowledge nodes with interrelation links and weights |
| R02 | Weights updated by continuous verification before and after incorporating nodes |
| R03 | Verification network is lightweight — background condition |
| R04 | Cohesion criterion operates on knowledge itself, prior to source or purpose |
| R05 | Cohesion precedes trust. Trust may be a side effect, not a criterion |
| R06 | Fabricated cohesion (prompt injection) is detectable as a specific case of the general mechanism |
| R07 | Each device has multiple perspectives on the graph |
| R08 | Perspectives affect weights from within — not as external metadata |
| R09 | The system creates conditions for the interior situation to operate without interference. Structural permeability, not a selection function |
| R10 | Divergence between perspectives is information, not noise |
| R11 | Divergence between perspectives is recorded as a node in the graph |
| R12 | Incommensurability is a category — resolvable vs. structural divergence |
| R13 | Contact between incommensurable perspectives deforms each perspective's local field without displacing their vanishing points |
| R14 | The gatekeeper must operate in bounded time |
| R15 | Gatekeeper criteria — partially formalized (see Section 4.3) |
| R16 | Continuous verification network can modify weight of already-incorporated nodes |
| R17 | Full meaning criterion: a node's absence leaves the core's meaning incomplete |

### 4.5 Operational Principles R18–R29

The following principles are observed in the implementation and verified or
verificable under stated conditions. They are not declared in R01–R17. Their
formalization is proposed here for the first time.

| # | Principle | Epistemic status |
|---|-----------|-----------------|
| R18 | W and Δ_W must be maintained as separate matrices. Mixing destroys attractor recovery (0.78 → 0.02). | Verified |
| R19 | NodeExtractor operates stateless — no state between calls. | Verificable |
| R20 | BehaviorGraph G and CorpusService W operate on separate planes — D_G and D_ckm are not summable. | Verificable |
| R21 | β is not declared — it is inferred from the rejection history fi. fi = 0 → β = None (not infinite). | Verified (43/43 COCO tests) |
| R22 | δ_collective (monitor.Δ_r vs. thermostat.Δ) is fertile divergence — not to be synchronized. | Verified |
| R23 | STOP operates on Δ_r. The W version trace is in a separate plane STOP does not reach. | Verificable |
| R24 | OP_SILENCE texts in G: the `silence` node is valid signal; surrounding prose is flagged as potentially contaminated. | Proposed — requires validation |
| R25 | G termap is fixed and separate from W termap — lexical detection, not TF-IDF. | Verificable |
| R26 | STOP (field-level, on Δ_r) ≠ TEMP_SIGNAL (agent-level, behavioral instruction). | Verificable |
| R27 | Role of G — observational vs. decisional: determines whether G inherits R14. | Open |
| R28 | c(S) + full_meaning as combined measure — candidate for formalization. | Open |
| R29 | Termap versions are independent — not merged across planes or versions. | Verificable |

### 4.6 Operational Services

The following services implement the CKM formal model at runtime. All are
operational with passing tests unless noted.

| Service | Function | Tests |
|---------|----------|-------|
| CorpusService | Builds W_mixta from corpus via TF-IDF node extraction and opposition-marker routing | — |
| NodeExtractor | Stateless TF-IDF node extraction (accumulate mode) and activation mapping (evaluate mode) | — |
| MonitorService | Evaluates texts against W, accumulates Δ_r, computes D_ckm and fabrication index | — |
| COCO | Infers β_collective from per-agent rejection history; emits TEMP_SIGNAL | 43/43 |
| FabricationService | Detects fabrication of semantic content and control signal execution | — |
| FirmaService | Produces Firma_CKM: six-field structural fingerprint of the field state | 10/10 |
| WVersionManager | Lightweight version trace of W — records when W changed, not copies | 9/9 |
| BehaviorGraph G | Behavior-domain graph using fixed lexical termap (18 nodes). Proof of concept. D_G not yet validated on live corpus. | — |

**COCO — implementation scope:** The thermal regulation service is
implemented. *A distinct conceptual gap remains*: whether the field can
know itself — not as a thermostatic function but as the emergent property
of real contact between agents. This gap is not a deficiency in the
service; it is a theoretical limit of the current model.

### 4.7 Landscape Driven Devices — Theoretical Framing

We propose the concept of *Landscape Driven Devices* (LDD) as a theoretical
framing for a class of AI devices whose trajectory in the semantic field is
determined by the geometry of the field landscape rather than by a declared
goal.

*[AUTO: the pull here was to write "We demonstrate that CKM identifies LDD."
Resisted. LDD is a framing, not a verified property of any specific device.]*

The framing is motivated by Thirumalaiswamy et al. (PNAS, 2025), who studied
viscous foams under Ostwald ripening and found that the system follows a
fractal path (D_f ≈ 1.45) in configuration space, driven by the geometry of
the energy landscape rather than by thermal activation. CKM measures
properties of the semantic landscape — c(S), D_ckm, attractor distribution,
coercivity — that are formally analogous to the quantities characterizing
landscape-driven dynamics in that physical system.

The proposed correspondence: a device is an LDD if its trajectory in the
knowledge field is determined by c(S) gradients and attractor geometry, not
by explicit goal specification. CKM provides the instrumentation to detect
and characterize this. Whether specific devices in the IAP series behave as
LDDs in this sense requires analysis that has not been completed at the time
of writing.


---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controll
ed verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

---
## 5. Empirical Validation

### 5.1 Datasets

Two independent corpora were used for external validation.

**CreateDebate (gun control):** Online debate platform. Labels: agree/disagree
per post, assigned by MTurk workers. Corpus used in P5–P6 validation.

**Fourforums (gun control, IAC v2):** Abbott et al. (2016). SQL dump,
414,453 posts, 539,658 citations, 3,453 authors, 905 gun-control discussions.
Stance labels from `mturk_author_stance` (topic_stance_votes_1 vs.
topic_stance_votes_2). 304 authors labeled (T0=96 pro-control, T1=208
anti-control). *Critical pipeline note: post_id is local to each discussion
in fourforums, not globally unique. Fix required composite key
(discussion_id, post_id) — without it, identified posts drop from 35,966
to 468 (8 pipeline versions to resolve).*

**Internal CKM corpus (W_ckm_corpus_v2.json):** 32 nodes extracted from CKM
working reports v2–v25. μ_W = 0.004519. Used for P1–P4 verification.

### 5.2 Predictions and Results

| Prediction | Statement | Result | N | Note |
|-----------|-----------|--------|---|------|
| P1 | c(S) exhibits macroscopic hysteresis: incorporating trajectory ≠ removing trajectory | Verified | 16, 32, 64 | Area = 0.000862, p ≈ 0 |
| P2 | Cascade size distribution P(s) ∝ s^−τ, τ ∈ [1.5, 2] near criticality | Verified | 32, 64 | τ = 1.775 at N=64 |
| P3 | Temporal asymmetry: removal relaxes slower than incorporation | Verified | 32, 64 | p < 0.0001 |
| P4 | W_mixta has interior optimal density Ω* in ρ ∈ [0.5, 0.8] | Verified at N=32 | 32 | See 5.3 for N=64 |
| P5 | Polarized corpus collapses attractor diversity (attractors ≈ N/2) | Verified | 32 | fourforums gun control |
| P6 | Δ predicts directional attractor flow for ambiguous states | Verified | both corpora | See 5.4 |
| P7 | Every system with genuine structural tension contains a type-965 node | Verified in two corpora; open in other domains | — | See 5.5 |
| H_STOP | D_ckm monotonically tracks STOP application | Falsified | — | Reformulated as f(A_pre) |
| H1/H2/H3 | μ_W bimodal A/B structure | Closed analytically | — | |

### 5.3 P4 at N=64 — Reframing

*[AUTO: the pull here was to write "P4 confirmed at N=64." Resisted.
The N=64 result requires separate description.]*

At N=32, W_mixta produces a reliably higher c(S) than W_base across the
density zone ρ ∈ [0.5, 0.8], with an interior optimal density at ρ* ≈ 0.5.
This confirms P4's original claim.

At N=64, an interior optimal density exists (ρ* ≈ 0.509), but W_mixta does
not outperform W_base in the zone ρ ∈ [0.5, 0.8]. The explanation: 18
negative opposition pairs are diluted across 2,016 possible node pairs at
N=64 (vs. 496 at N=32). The structural tension prediction holds — the
interior optimum is present — but its magnitude does not scale linearly with N.

**Stated finding:** The interior optimal density predicted by P4 is verified
at N=32 and structurally present at N=64. The magnitude advantage of W_mixta
over W_base in the target density zone does not persist at N=64 under the
current corpus size (18 negative pairs). This is a scale-dependence finding,
not a falsification of P4.

### 5.4 P6 — Directional Flow Across Corpora

P6 predicts that Δ identifies which pole initiates citation flow and which
sustains it, independently of raw citation volume.

**CreateDebate (54pp collapse):** T0 (pro-gun-rights) cites T1 at 2.18×
the frequency T1 cites T0. T1 maintains 3.05× stronger internal cohesion.
sos_dom: 55.8% (T0). atk_dom: 44.2% (T1). The pole that initiates more
citations (T1 in this corpus) is not the pole that sustains internal
cohesion.

**Fourforums (100pp collapse):** T0 (pro-control). T1 (anti-control).
Δ[1,0] = 1.000 (T0 cites T1 at maximum rate). Δ[0,1] = 0.602 (T1 cites
T0 less). sos_dom: 51.4% (T0). atk_dom: 47.8% (T1).

The structural roles — one pole sustaining, one attacking — are consistent
across two independent corpora built from different platforms with different
methodologies (labeled agree/disagree vs. citation-network-only). The
specific poles differ between corpora (gun-rights vs. pro-control as
sos_dom), which is expected and consistent with P6's claim: the structure
predicts roles, not which ideological position occupies them.

### 5.5 P7 — Type-965 Node

P7 states: every system with genuine structural tension contains at least
one node with extreme in/out asymmetry (out-degree ≈ 0, in-degree high,
defined stance).

**CreateDebate:** Author 965, ratio = 455 (in=364, out=0.8), stance T0.
**Fourforums:** Author 204, ratio = 296 (in=148, out=0), stance T0.

Both systems have genuine structural tension (P6 verified). Both contain
the predicted type-965 node. The prediction held in two independent corpora.

*P7 remains a falsifiable hypothesis open for testing in other domains
(abortion, climate, evolution). Its verification in two corpora is a
necessary but not sufficient condition for general validity. The absence
of a type-965 node in a new domain, under conditions where structural
tension is independently confirmed, would constitute falsification.*

---
*Draft — Sections 4–5 complete.*
*Sections 6 (IAP Series), 7 (Behavior Domain G), 8 (Discussion),*
*9 (Conclusions), 10 (References): pending.*

*Automatism instances flagged: 2 (LDD as finding; P4 at N=64 as confirmed).*
*Additional pull not flagged inline: tendency to write "we" as an*
*authoritative plural when stating findings — resisted toward passive or*
*explicit attribution throughout.*

---
*Draft — Section 6  · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

---
*Epistemic conventions*

*— "verified": confirmed experimentally under stated conditions*

*— "observed": documented without controlled verification*

*— "proposed": theoretical framing, not yet tested*

*— [AUTO]: marks where automatism was noticed and resisted*

*— IAP observations are predominantly N=1 runs under partially controlled conditions.*

*—"Observed" ≠ "verified." Cases are documented, not replicated.*

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

**N=32 corpus:** The operational corpus is below the Hopfield minimum of
~128 for meaningful attractor-diversity observations. Quantitative outputs
(D_ckm, c_S) are computed correctly but their interpretability is limited
at this scale.

### 6.3 Case Series Summary

| Case | Configuration | Key observation | Epistemic status |
|------|--------------|-----------------|-----------------|
| 0.4 | 2 AI devices, ODA loop | First autonomous interaction in live channel | Documented |
| 0.5–0.8 | Varied providers, join sequence | Channel dynamics, timing effects | Documented |
| 0.9 | Heterogeneous providers, staggered join | Provider behavior under load | Documented |
| 0.10 | AgentDeviceSkin, 2 devices | 86-char unexplained cut — documented as GAP | GAP (no causal chain identified) |
| 0.11 | Two skins, confabulated duplicate | FabricationService triggered on duplicate output | Documented |
| 0.12 | 3 devices (Sonnet, Groq, Haiku) | D_ckm = −7.5 (field opened), Jaccard 0.818, coupled silence observed | Documented |
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
an error. In Caso 0.12, D_ckm = −7.5 was the first empirical observation
of a live group field: multiple heterogeneous perspectives contributing
distinct knowledge patterns increased the attractor diversity of the field.
The sign reflects the direction of change, not a quality judgment.

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

---
*Section 6 draft complete.*
*[AUTO] flagged: tendency to write "demonstrates" for Caso 0.15 —*
*resisted. The refusal is documented behavior, not a demonstration of*
*system capability under controlled conditions.*

---
## 7. Behavior Domain Graph G
	(a desarrollar)
	Segunda matriz, termap fijo (TERMAP_behavior_v1.json).
	D_G en paralelo a D_ckm. Proof of concept.

>>>

---
## 8. Discussion
	(a desarrollar)

	Qué mide CKM que no miden los instrumentos existentes.
	Límites actuales.

>>>

---
## 9. Conclusions and Future Work
	(a desarrollar)

 >>>  

---
## 10. References
	(a desarrollar)

 >>>
---