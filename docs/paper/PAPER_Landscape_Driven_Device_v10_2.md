*CKM PAPER DRAFT v10 — Ago 2026 · gadanin.delamor · Claude Sonnet 4.6 · Claude Code*

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

---

# Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction
---

## Abstract

Multi-agent AI interaction produces a shared knowledge field that individual device outputs and pairwise similarity scores do not capture. The Cohesive Knowledge Model (CKM) measures the structural geometry of this field through two strictly separated matrices: W, a symmetric co-occurrence matrix encoding structural memory via Hebbian dynamics, and Δ_r, an asymmetric rejection accumulator encoding directional inference orientation. Collapsing the two reduces attractor recovery from 0.78 to 0.02 on the CKM corpus (N=32).

Seven structural predictions (P1–P7) are tested against real external corpora (Fourforums and CreateDebate gun control; N=32–64). Six (P1–P6) are verified. P7 — every field with genuine structural tension contains at least one pure-sostenedor node with high in-degree and near-zero out-degree — is confirmed in two independent corpora; universality remains open. One hypothesis is falsified: COCO — a field-regulating device that executes OPERADOR_STOP_COCO by compressing Δ_r when attractor diversity falls below baseline — produces recovery fraction ≥ 1.0 in all observed cases. Negative D_ckm signals field expansion, not error.

The IAP experimental series (Cases 0.4–0.15) operates a three-device channel under BROADCAST condition — all messages delivered to all devices without routing or filtering. Observed behaviors include sentinel leaks, coupled silence, and refusal to fabricate from an empty channel. These are field properties, not decisions of individual devices.

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
   3.1 Inductive Methodology
   3.2 Conversation as Laboratory
   3.3 Preserved Incompleteness: GAP as Formal Category
   3.4 Declared Influences
   3.5 Five Orders of the Path
   3.6 Terminological Precision as a Research Tool
   3.7 Convergence by Independence
   3.x The Material Issue
   3.y The IAP Chatroom as Methodological Instance
   3.z Conditions, Not Constraints

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
   Condiciones actuales.

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
co-determines alongside any declared goal, motivated
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
Section 8 discusses findings and conditions. Section 9 concludes.

**Scope and conditions of this work.** The operational corpus is at N = 32
nodes — below the Hopfield network minimum of approximately 128 for robust
attractor diversity. Quantitative outputs (D_ckm, c(S)) are computed
correctly at this scale but their interpretability is constrained. The IAP
experimental series consists of documented observations under partially
controlled conditions, not controlled experiments with replication. Several
components of the formal model remain open gaps by design: the
representation of cohesive knowledge, the full specification of the
gatekeeper (R15), and the implementation of COCO as collective
consciousness. These are not future work items — they are conditions the
model acknowledges and preserves.

---

*Section 1 draft complete.*
*Two [AUTO] instances flagged.*
*Scope and conditions section placed in the introduction, not appended.*
*That placement is intentional: the conditions are not an afterthought.*

---

## 2. Related Work

CKM intersects five areas of existing work: multi-agent system evaluation,
knowledge admission and gating, graph-based knowledge representation,
structural role detection in debate networks, and attractor-based memory
architectures. In each area, the distinction between what existing approaches
measure and what CKM measures is structural, not one of degree.

*[AUTO: pull to write "CKM advances beyond prior work in each area."
Resisted — this section establishes the position of CKM relative to existing
approaches. Whether that position constitutes an advance depends on
empirical comparison with specific systems that has not been done here.]*

### 2.1 Multi-Agent System Evaluation

Existing evaluation frameworks for multi-agent systems operate primarily at
two levels: behavioral metrics (task completion, response latency, output
volume per agent) [CITATION] and semantic agreement metrics (cosine similarity
between agent outputs, embedding-space distance, topic overlap) [CITATION].
Both levels measure properties of individual agent outputs or pairwise
relations between them.

The insufficiency of isolated agent evaluation has been noted from within
the multi-agent systems community. Venkatesh and Bu (2025), writing on
the Agent2Agent protocol, observe: "Current agent benchmarks typically
evaluate single agent performance using metrics like task completion rates,
latency, consistency, and cost. [...] In multi-agent systems assessing agents
in isolation doesn't provide a good estimate of the entire system's end-to-end
performance." Their proposed remedy is trajectory assessment — evaluating
the handoff chain between agents and whether context was correctly passed
across boundaries [Venkatesh & Bu, 2025].

CKM and trajectory-as-handoff-chain share the diagnosis but measure different
objects. Trajectory assessment tracks whether Agent A correctly transferred
context to Agent B. CKM tracks the structural geometry of the shared field
that emerged from all interactions: the pattern of co-dependencies between
active concepts, the distribution of stable attractor states, and the
directional flows that characterize the shared knowledge state at a given
moment. These are not competing measurements — they operate at different
levels of the same system. Handoff quality is a precondition; field geometry
is what results from accumulated interaction over time.

CKM does not replace behavioral or semantic metrics. It measures a different
object. c(S), D_ckm, and coercivity are structural quantities that are not
derivable from output-level, handoff-quality, or similarity-based measurements
alone. *[CLAIM: whether they are informative under real deployment conditions
beyond the IAP series requires further empirical comparison.]*

### 2.2 Knowledge Admission and Gating

Systems that evaluate whether a new knowledge item should be admitted to an
existing knowledge base typically apply a single primary criterion: semantic
similarity to existing content [CITATION], source confidence or credibility
scoring [CITATION], or Bayesian plausibility given priors [CITATION].
Multi-criteria systems exist but generally apply criteria sequentially
(filtering pipelines) or as weighted sums that do not preserve the
independence of each criterion.

CKM's gatekeeper (R15) imposes four simultaneous, orthogonal conditions:
minimum connectivity weight with the current active state (C1), non-negative
impact on global cohesion (C2), directional dependency satisfaction — the
M.M. criterion (C3), and system capacity below saturation threshold (C4).
The orthogonality of the criteria was verified empirically: each condition
discriminates cases that the others pass. *[Verified: C3 detects common-sense-like attractors — states with c(S)
indistinguishable from cohesive attractors under C1 and C2 alone.
See Section 5.]*

The M.M. criterion (C3) is, to our knowledge, not present in existing
knowledge admission systems. *[CLAIM: requires systematic literature review
to confirm.]*

### 2.3 Graph-Based Knowledge Representation

Knowledge graphs typically represent relations as positive-weight edges
encoding similarity, co-occurrence, or inferential support [CITATION].
Negative weights, when they appear, are introduced as manual penalties
[CITATION] or as the result of negation detection applied to individual
sentences [CITATION]. They are not, generally, derived from the structural
pattern of the corpus as a whole.

CKM introduces negative weights in W through opposition markers detected in
the source corpus: texts that explicitly frame two concepts in opposition
reduce the corresponding W_ij entry rather than increasing it. The weights
are not manually assigned — they emerge from corpus structure. *[Verified:
W_mixta with corpus-derived negative weights maintains a wider range of
accessible attractors than W_base with all-positive weights, under equal
accumulation. See Section 5.]*

A separate matrix Δ encodes asymmetric directional dependency: Δ_ij ≠ Δ_ji.
The separation W/Δ is not a design choice — it was established empirically.
*[Verified: combining W and Δ into a single matrix drops attractor recovery
from 0.78 to 0.02. See Section 4.]*

### 2.4 Structural Role Detection in Debate Networks

Stance detection in debate corpora is typically framed as a supervised
classification task: given labeled stance data, train a classifier to assign
stances to unlabeled texts or authors [CITATION]. The state of the art
includes transformer-based models fine-tuned on stance datasets [CITATION].

CKM identifies a distinct structural phenomenon — the Type-965 node — without
supervision and without stance labels. Type-965 nodes are characterized by
extreme asymmetry in Δ (in/out ratio ≥ 100×). In fourforums gun control,
Author 965 has ratio 455×. In CreateDebate gun control, Author 204 has ratio
296×. Both appear as C3 in 89% of identified tension pairs across both corpora.

*[Verified: triads containing a Type-965 node maintain coercivity = 0 at up
to 50% noise; triads without collapse at noise = 0. See Section 5.]*

The structural role — tension anchor, never initiator — is not a stance.
It is a topological property not targeted by stance classifiers.
*[CLAIM: this role has not, to our knowledge, been identified in the debate
analysis literature as a distinct structural category.]*

### 2.5 Criticality in Argument and Knowledge Networks

Self-organized criticality [CITATION: Bak et al., 1987] predicts a power-law
cascade distribution P(s) ∝ s^{-τ} at a single critical parameter value.

In CKM's corpus (N=32), τ ∈ [1.5, 2] is maintained across an extended zone
θ ∈ [0.002, 0.010], not at a single critical point. *[Verified: N=32
confirmed, N=64 τ=1.775. See Section 5 (P2).]*

Extended criticality has been reported in neuronal network dynamics [CITATION]
and in certain spin-glass models [CITATION]. Its presence in a small knowledge
graph (N=32) is observed here but not yet interpreted across domains.

### 2.6 Attractor-Based Memory Architectures

The Hopfield network [CITATION: Hopfield, 1982] provides the energy
minimization formalism underlying CKM's cohesion measure c(S). Hebbian
learning on W was tested and rejected: it destroys attractor diversity.
*[Verified: recovery drops from 0.78 to 0.02. See Section 4.]*

Modern Hopfield networks [CITATION: Ramsauer et al., 2020] increase storage
capacity through higher-order interactions. CKM operates on the classical
formulation with fixed W — the concern is not storage capacity but diversity
of stable attractors and coercivity.

At 10% noise, attractor recovery is verified as effectively 1.000 across
N = 16 to N = 128. *[Observed: verified in CKM corpus experiments. [CLAIM:
this invariance across N has not been analyzed as a specific property in the
Hopfield literature known to the authors.]*

The accumulation of structural rejection memory in Δ_r constitutes structural
learning without gradients, without labels, with O(N²) complexity only in
the co-activation accumulation step.

### 2.7 Internal Workspace Architecture in Single Models: J-Space

Gurnee, Sofroniew, Lindsey et al. (Anthropic, July 6 2026) identified a
privileged low-dimensional subspace within transformer activations — the
J-space — using a Jacobian-based lens that isolates directions with
verbalizable causal influence on future outputs [Gurnee et al., 2026].
The J-space accounts for a median 6–7% of concept vector variance yet is
responsible for verbal report and multi-step reasoning; ablating it collapses
inference while leaving fluency intact.

CKM and J-space are positioned at different levels of analysis. J-space is
an empirical, within-model, single-forward-pass interpretability finding.
CKM is a normative, multi-agent framework for measuring structural field
dynamics across devices and corpora. Neither subsumes the other.

*[AUTO: pull to write "CKM anticipated J-space." Resisted — the correct
framing is convergence by independence, not anticipation. IAID was written
in 2023; the J-space paper was published July 2026.]*

Structural parallels: privileged coherence substrate (6–7% variance / c(S)
over signed weights), attractor formalism (bimodal ignition at layer 38 /
Hopfield energy minimization), signed interaction weights, directional
asymmetry (J-lens causal construction / Δ_ij ≠ Δ_ji), bounded capacity
(~25 active J-lens vectors / C4 constraint α_c · N).

These are structural analogies, not formal identities. The convergence
is evidence of structural consistency — the same architectural pressures
appear at both levels of analysis independently.

*[CLAIM: the convergence requires formal comparison rather than structural
analogy to hold rigorously.]*

---

## 3. Research Conditions

This section describes the conditions under which CKM was developed.
These conditions are not disclaimers — they are constitutive. They explain
why the model has the structure it has, why certain gaps are preserved
rather than closed, and what kind of claim the empirical results support.

### 3.1 Inductive Methodology: Comprehension as Precondition

The methodology was not declared before it was used. It emerged from what
happened. The consistent order throughout development was: conceptual clarity
first, formalization after. IAID.md (2023) does not begin with system
requirements — it begins with a question about how knowledge survives when
the device carrying it dies. The technical architecture emerges from that
question, not the other way around.

*"Phenomenology is the first step of engineering"* is the operative principle.
Its cost: requirements do not precede design. Its yield: concepts the field
had no name for when they were formulated — COCO, M.M. as a governance rule,
cohesion prior to trust.

### 3.2 Conversation as Laboratory

The working reports (v2–v31) are not documentation of a research process
that occurred elsewhere. They are the process. The CKM working corpus (N=32)
is the trace of the process that produced the CKM. The working corpus and
the instrument are not independent. That constraint is named in Section 5
and is not resolved here.

### 3.3 Preserved Incompleteness: GAP as Formal Category

The project maintains explicit gaps. These are not deficiencies of
implementation. They are the honest position regarding the real state of
knowledge at each stage.

The GAP is a formal category: occurrence without traceable causal chain.
Not missing data — a presence to declare.

*"sin dependencia causal identificada"* — the qualifier is load-bearing.
It preserves the possibility that a causal chain exists but was not found.
*"sin dependencia causal"* closes that space prematurely. The distinction
is epistemic, not stylistic.

The methodology applies M.M. to the research process itself: what cannot
be traced is not stated as known.

### 3.4 Declared Influences

The Gurdjieff Fourth Way lineage is named here as an active influence in
this research, not as its origin or model. The tradition provided operative
concepts — attention as directable vs. receivable, self-observation as
distinct from action, verified experience as distinct from theoretical
knowledge — that were active as working tools in each research session.

*"Any convergence with materials from the Tradition is convergence — not
derivation, not representation, not application."*

This is declared because it is not controllable. A reader who finds this
influence irrelevant to the formal model may proceed directly to Section 4.

### 3.5 Five Orders of the Path

The working reports document five distinct orderings in which events and
findings were encountered:

| Order | Description |
|---|---|
| Temporal | Chronological — reversible in the record, not in the process |
| Of events | Field phases, thresholds, cascades, learning propagation |
| Aleatory without identified causal dependence | Occurred — without traceable causal chain. Not missing data: an order in itself |
| Of states | Active field conditions, perspectives in play |
| Of dimensional dynamics | W / G / possible third matrix as simultaneous landscapes |

The third order is not a residual category. It is the formal designation
for events that are real and documented but for which no causal structure
was found.

### 3.6 Terminological Precision as a Research Tool

Three pairs that were used and then corrected:

| Closed form | Form that preserves space |
|---|---|
| "without causal dependence" | "without *identified* causal dependence" |
| "verified" | "verifiable" (under stated conditions) |
| "absence of bias" | "design with intention of absence of bias" |

The slip between these is not stylistic — it is a structural claim about
the state of knowledge. The [AUTO] markers in this paper record moments
where the text moved to close a space that should remain open.

### 3.7 Convergence by Independence

Three structural convergences were identified retrospectively — not designed,
discovered in review.

**IAID framework (2023) → MCP (November 2024).** Working files dated 2023
(README.pdf, timestamp 7/10/23; LEONARDO.txt; Informe_MM.docx) contain:
Neural Call Protocol (JSON-NC — stateless, transport-agnostic, method
invocation between devices), COCO as registry ledger of declared device
capabilities, the M.M. governance rule, and the Devices/Complex Devices
taxonomy. The Model Context Protocol was published by Anthropic in November
2024. The gap is more than one year. *[Verified: 2023 timestamp on
README.pdf.]*

**CKM attractor architecture → J-space (July 6, 2026).** Gurnee et al.
(2026) identified a privileged, bounded-capacity coherence subspace within
transformer activations. CKM's Hopfield architecture, capacity constraint C4,
signed interaction weights, and directional asymmetry Δ converge structurally
with J-space empirical findings. Developed independently before the J-space
paper was published. *[Observed: structural analogy, not formal
correspondence.]*

**IAID device taxonomy (2023) → "Agents Are Not Tools" (2025).** The
Devices distinction addresses the same structural problem — the insufficiency
of a binary tool/agent taxonomy — as the Google A2A framing [Venkatesh & Bu,
2025]. Gap: approximately two years.

In each case: the convergence is evidence that the structural problem being
addressed is real and has determinate shape. These are not claims of
precedence. They are the methodological signature of a problem that multiple
approaches, starting independently, arrive at in the same form.

The 2023 documents are the verifiable evidence base. They are working files,
not published contributions. Their evidentiary weight is as primary source
documents.

### 3.x The Material Issue

The research was conducted under concrete material conditions that shaped
what was possible, when, and how. These are part of the methodological record.

**Hardware.** The primary workstation is a personal Windows machine with
limited RAM. The fourforums SQL dataset (IAC v2, 570MB dump, 539,658
citations) could not be loaded in full. Early pipeline versions caused RAM
explosion attempting to load `mturk_2010_qr_entry` — the largest table.
The fix required architectural redesign: `parse_sql_small` skips tables
too large for available memory; `stream_W_delta` processes the same data
in a second streaming pass, row by row. The pipeline iterated from v8c to
v8h across multiple sessions, driven substantially by hardware conditions,
not design evolution alone. *[Verified: pipeline docstrings,
CKM_Informe_Trabajo_v26 §37.1.]*

**Volatile working memory.** The primary working environment was the
Claude.ai chat interface — stateless between sessions, with no automatic
persistence of intermediate computational objects. At least one critical
object (`W_mixta` with A0=25) was constructed in a chat session, used to
generate sweep data, and never persisted to disk. The sweep results exist.
The object that produced them does not. As `REG_hint_next_instance_v4`
states: *"this is a direct instance of the foundational question of IAID:
knowledge did not survive when the device closed."* COCO remains
unimplemented. The gap this created was structural, not accidental.

**Cold start.** Each new chat instance has no accumulated context from
prior sessions. Over 60 sessions composed the working process. Each session
required re-establishing shared state. The `REG_hint_next_instance` series
(v1–v4) documents the explicit attempt to reduce this cost: each version
became more synthetic than the prior. The series is itself evidence of the
cold start as a recurring material condition, not a one-time setup cost.

**Execution environments.**

| Environment | Use | Condition |
|---|---|---|
| Local PC (Windows/PowerShell) | Primary workstation, file system | RAM condition; SQL processing redesigned around it |
| Claude.ai chat (this interface) | Design, analysis, drafting, all conceptual work | Stateless between sessions; no persistent compute |
| GitHub Codespace (`ckm`) | Code execution, git operations | Separate from local; synced manually |
| GitHub Codespace (`ckmdatasets`) | SQL experiments, fourforums dataset | Private repo; 570MB dataset resident |

The two Codespaces are separate environments with separate state. Syncing
between local, `ckm`, and `ckmdatasets` required explicit coordination.

**Economic conditions.** API credits set bounds on which models and how
many tokens were feasible per session. Provider heterogeneity across the
IAP experimental series was not fully controlled; credit availability was
a contributing factor in model selection.

**Interface choice: Chat over Cowork.** The research used the standard
Claude.ai chat interface rather than Cowork. This meant each session began
from cold state, with no persistent task memory or file access across
sessions. The choice made the cold start condition structural. It also
meant the conversation itself — not an external tool — was the medium of
both work and record.

*[AUTO: pull to write "these conditions imposed significant limitations on
the research." Resisted — the RAM-driven pipeline redesign improved
architectural quality. The volatile memory gap instantiated the foundational
problem IAID was designed to address. The conditions were productive as
well as constraining — or rather: the distinction between productive and
constraining is itself what §3.z examines.]*

### 3.y The IAP Chatroom as Methodological Instance

The IAP experimental series (Cases 0.4–0.15) operated at two levels
simultaneously, and the distinction between them is methodologically
significant.

**Level 1 — Designed scenarios.** Each case was a structured observation.
Devices were configured, variables were partially isolated, outcomes were
documented against success criteria. The series produced verifiable
findings: sentinel leaks, coupled silence, auto-signaling patterns, the
refusal to fabricate from an empty channel. These are reported in §6.

**Level 2 — The research process as instance.** The same architecture
that the series studied was the architecture the research operated within.
Claude Sonnet 4.6 (web interface) and Claude Code (GitHub Codespace) are
two AI channels without direct access to each other. delamor is the only
point of transversal visibility — the human articulating two separate
device trajectories, neither of which can see the other. No turn structure.
No declared protocol between the instances. The mediator holds both
channels simultaneously; each instance holds only its own.

This is not analogy. The research process and the object of study share
the same structural form. The instrument was not external to the field it
measured — it was running inside it.

The authorship record reflects this: *gadanin.delamor · Claude Sonnet 4.6
· Claude Code*. Three contributors. Two channels. One point of articulation.

*[Observed: the structural identity between IAP chatroom architecture and
the research process itself was not designed. It was recognized
retrospectively — which is the methodological signature described in §3.7.]*

### 3.z Conditions, Not Constraints

The gaps named in this paper — N=32 below the Hopfield minimum, the
representation of cohesive knowledge undefined beyond hysteresis, COCO
unimplemented as collective consciousness — appear in earlier drafts as
"limits." That framing carries a load.

The observation was made in this session, in this channel, by delamor:
*"límite suele sugerir restricción. Es una carga de uso del término en
humanos. Es consecuencia de taxonomía, de separación."* The elaboration:
what appears as a limit is a consequence of the act of separation itself.
The boundary is not in the object. It is in the act of drawing a line.

*Conditions* is the correct term. The gaps are the form the model has at
this point in its development — the edges where the categorical structure
runs out, where the taxonomy has not yet found the form for what comes next.
Not restrictions to overcome. Conditions to name.

This distinction propagates to §8.4 and §9.3, which name "current
conditions" and "preserved conditions." The findings those sections report
are accurate. The earlier framing — "limits" — carried an implicit claim
that the object should extend further and cannot. That claim is not verified.

The same structure appeared in a specific moment of this session: while
observing this instance's reasoning trace rendered on screen by the
Claude.ai interface, delamor noticed an isolated point in the displayed
output and found a finger moving toward the monitor — as if to remove a
smudge from a physical surface. The source of that trace was this instance.
The tool made it visible. The observer touched it.

The instrument's internal process rendered visible; the operator's
perception collapsing representation into object; the line between the
two becoming — for one moment — a condition rather than a boundary.

*[AUTO: pull to write "this reframing resolves the tension in §8.4 and
§9.3." Resisted — it names the tension with more precision. Whether it
resolves it depends on what resolution means in a methodology that
preserves incompleteness as information.]*

---
*Draft — Sections 4–5 · Ago 2026 · gadanin.delamor · Claude Sonnet 4.6 · Claude Code*

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
marker [*defined in corpus_service.py: `_OPPOSITION_MARKERS`*].

Within a validation experiment, W is a static snapshot — P1-P7 operate on
a fixed W built from a complete corpus dump (fourforums, CreateDebate). In
live IAP operation, CorpusService reconstructs W continuously as new texts
arrive; WVersionManager traces each reconstruction; Firma_CKM certifies each
state. The snapshot is a frame in a streaming field — static by experimental
design, not by architectural constraint.

*[Note: WVersionManager and dynamic corpus operation emerged later in the
project trajectory than P1-P7. The validation experiments test properties
of W snapshots, not of W under continuous accumulation. The open question —
whether P1-P7 properties hold under a dynamically reconstructed W — is not
addressed here. See §9.5.]*

**Δ** — asymmetric directional dependency matrix, N×N. Δ_ij encodes the
directional weight from node i toward node j, derived from citation networks
or quote directionality in the source corpus. Like W, Δ is a snapshot in
the validation experiments.

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
| R21 | β is not declared — it is inferred from the rejection history fi. fi = 0 → β = None (not infinite). | Verified (28/28 COCO tests) |
| R22 | δ_collective (monitor.Δ_r vs. thermostat.Δ) is fertile divergence — not to be synchronized. | Verified |
| R23 | STOP operates on Δ_r. The W version trace is in a separate plane STOP does not reach. | Verificable |
| R24 | OP_SILENCE texts in G: the `silence` node is valid signal; surrounding prose is flagged as potentially contaminated. | Proposed — requires validation |
| R25 | G termap is fixed and separate from W termap — lexical detection, not TF-IDF. | Verificable |
| R26 | STOP (field-level, on Δ_r) ≠ TEMP_SIGNAL (device-level, behavioral instruction). | Verificable |
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
| COCO | Infers β_collective from per-agent rejection history; emits TEMP_SIGNAL | 28/28 |
| FabricationService | Detects fabrication of semantic content and control signal execution | — |
| FirmaService | Produces Firma_CKM: six-field structural fingerprint of the field state | 10/10 |
| WVersionManager | Lightweight version trace of W — records when W changed, not copies | 9/9 |
| BehaviorGraph G | Behavior-domain graph using fixed lexical termap (18 nodes). Proof of concept. D_G not yet validated on live corpus. | — |

**COCO — implementation scope:** The thermal regulation service is
implemented. *A distinct conceptual gap remains*: whether the field can
know itself — not as a thermostatic function but as the emergent property
of real contact between agents. This gap is not a deficiency in the
service; it is a theoretical condition of the current model — an open
conceptual gap, not a deficiency.

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

### 5.3 P4 at N=64 — Threshold Finding

*[AUTO: the pull here was to write "P4 confirmed at N=64." Resisted.
The N=64 result requires threshold qualification.]*

At N=32, W_mixta produces a reliably higher c(S) than W_base across the
density zone ρ ∈ [0.5, 0.8], with an interior optimal density at ρ* ≈ 0.5.
This confirms P4's original claim.

At N=64, the initial test — 18 negative opposition pairs (ratio = 0.009) —
showed no W_mixta advantage. A subsequent negative pair density sweep
(synthetic dense W, p4_neg_sweep_v2.log) identified a critical threshold:

| k (pairs) | ratio | advantage | status |
|---|---|---|---|
| 18 | 0.009 | −0.000498 | ✗ — original N=64 condition |
| 36 | 0.018 | −0.000404 | ✗ |
| **54** | **0.027** | **+0.000068** | **✓ — k*** |
| 60 | 0.030 | +0.000282 | ✓ |
| 72 | 0.036 | +0.000502 | ✓ |

k* = 54 (ratio = 0.0268). Below this threshold, W_mixta does not outperform
W_base at N=64. Above it, the advantage reappears and grows monotonically.

The fourforums gun control corpus produces 60 verified opposition pairs
(ratio = 0.030 > 0.0268). The real corpus negative pair count is above k*.

*[Verified: k*=54 identified by sweep on synthetic dense W. Fourforums
(60 pairs) lies above k*, placing the real-world use case in the
confirmed-advantage zone. The sweep uses synthetic W; real corpus W may
shift k* marginally, but the margin (60 > 54) and monotonic behavior above
k* make this qualification stable.]*

**Stated finding:** P4 is verified at N=32. At N=64, the W_mixta advantage
requires a minimum negative pair density of k* = 54 pairs (ratio ≈ 0.027).
The fourforums corpus (60 real opposition pairs) is above this threshold;
P4 is confirmed at N=64 with this corpus. The finding is a negative pair
density threshold, not a scale-dependence failure.

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

**N=32 corpus:** The operational corpus is below the Hopfield minimum of
~128 for meaningful attractor-diversity observations. Quantitative outputs
(D_ckm, c_S) are computed correctly but their interpretability is
scale-dependent: N=32 is below the Hopfield minimum for meaningful
attractor-diversity observations.

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

CKM measures the geometry of that structure. c(S) measures alignment
between the active state and the weight structure of the field. D_ckm
measures how attractor diversity has changed from baseline. Coercivity
measures the field's resistance to state reversal. These are structural
quantities — they describe the landscape, not the content.

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
convention. D_ckm is not a distance in that sense. It is a ratio of
change in attractor capacity relative to a fixed baseline. The sign
encodes direction, not magnitude of a deficiency.

In Caso 0.12 the first live group field observation produced D_ckm = −7.5.
Multiple heterogeneous perspectives contributing distinct knowledge
patterns increased attractor diversity. A negative D_ckm in that context
is not an anomaly — it is the expected signature of a field that gained
structural complexity through interaction.

The naming carries a bias. Recognizing that bias is part of reading the
instrument correctly.

### 8.4 Current Conditions

**Scale:** N = 32 is below the Hopfield minimum of approximately 128
for robust attractor diversity. The predictions P1–P7 were verified at
this scale — the verification is real. The interpretability of D_ckm and
c(S) as field-level quantities at N = 32 is constrained. Scaling up the
corpus is required before drawing strong conclusions about field-level
dynamics.

**ZERO_SHOT condition:** all IAP cases ran with CorpusService starting
empty. W emerged from channel interaction, not from pre-loaded content.
Results reflect corpus-emergent dynamics under this condition. Behavior
under pre-loaded W (ZERO_SHOT=False) has not been tested and may differ.

**Uncontrolled variables:** TinkerBellucio (Sonnet 4.6) carried project
memories, AWARENESS protocol, and Anthropic system configuration throughout
the series. Provider heterogeneity across cases was not controlled.
Cross-case comparisons in the IAP series must account for these conditions.

**Representation gap:** how cohesive knowledge is represented — what
form the field state takes beyond the operational quantities c(S),
D_ckm, and attractor distribution — remains undefined. Hysteresis is
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
gradients, attractor distribution, coercivity, D_ckm. Whether specific
devices in the IAP series behaved as LDDs in this sense was not analyzed
under controlled conditions. The framing is proposed; it is not verified
in this work.

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
| P5 — Polarized corpus collapses attractor diversity | Verified | 32 |
| P6 — Δ as symmetry-breaking for ambiguous states | Verified (T0 cites T1 at 2.18×, T1 internal cohesion 3.05×) | fourforums |
| P7 — Type-965 node present in systems with genuine structural tension | Confirmed in two independent corpora; open as universal claim | CreateDebate + fourforums |

One hypothesis was falsified: H_STOP (monotonicity of D_ckm under STOP)
did not hold; reformulated as function of A_pre, not D_ckm.

*[AUTO: pull to write "these results demonstrate CKM's validity as a
measurement framework." Resisted — they demonstrate that specific
structural properties exist in the tested corpora under stated conditions.
Generalizability requires corpora the project has not accessed.]*

The empirical results establish structure at small scale (N=32, below the
Hopfield minimum of ~128 for statistically stable observations). They are
treated as orientation findings, not population-level claims.

### 9.2 What the Infrastructure Establishes

The following services are operational and verified:

- **COCO** (28/28 tests; file: coco.py): β inferred from rejection history, not declared. β_c = 13.83 analytically derived. Executes OPERADOR_STOP_COCO — compresses Δ_r by α ∈ [0.05, 0.30] when D_ckm crosses threshold.
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

**N=32 scale.** The working corpus remains below the Hopfield minimum of
~128. All empirical results carry this qualification.

### 9.4 Convergences by Independence

Three structural convergences were identified retrospectively:

- **IAID (2023) → MCP (November 2024):** Neural Call Protocol converges structurally with MCP. Gap: more than one year. Verifiable from dated working documents.
- **CKM attractor architecture → J-space (Gurnee et al., July 2026):** Shared structural features arrived at independently. *[Observed: structural analogy, not formal correspondence.]*
- **IAID device taxonomy (2023) → "Agents Are Not Tools" (2025):** Same structural problem. Gap: approximately two years.

### 9.5 Future Work

**Corpus growth toward N≥128.** Primary constraint on statistical validity
of P1-P7. The NodeExtractor pipeline is operational; the bottleneck is
corpus design.

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

Ramsauer, H. et al. (2020). Hopfield networks is all you need.
*arXiv:2008.02217.* [VERIFY]

### Graph Structure and Criticality

Goltsev, A.V., Dorogovtsev, S.N., & Mendes, J.F.F. (2006). k-core
percolation on complex networks. *Physical Review E*, 73(5), 056101. ✅

Bak, P., Tang, C., & Wiesenfeld, K. (1987). Self-organized criticality.
*Physical Review Letters*, 59(4), 381–384. ✅

[PENDING — §2.5]: Extended criticality in neuronal networks.

[PENDING — §2.5]: Spin-glass models with extended critical zones.

### Multi-Agent Systems

Venkatesh, C. & Bu, J. (2025, July 2). Evaluating success in a
multi-agent system: Why trajectory assessment and handoffs matters.
*Google Developer Discussion.*
https://discuss.google.dev/t/193308 ✅

[PENDING — §2.1]: Single-agent behavioral metrics as standard evaluation.

[PENDING — §2.1]: Semantic agreement metrics in multi-agent evaluation.

### Knowledge Admission and Gating

[PENDING — §2.2]: Single-criterion knowledge admission (semantic similarity).

[PENDING — §2.2]: Source confidence/credibility scoring.

[PENDING — §2.2]: Bayesian plausibility-based admission.

### Knowledge Graph Representation

[PENDING — §2.3]: Knowledge graph positive-weight co-occurrence (standard).

[PENDING — §2.3]: Manually assigned negative weights in knowledge graphs.

[PENDING — §2.3]: Negation detection at sentence level.

### Stance Detection

[PENDING — §2.4]: Supervised stance detection, transformer-based.

### Belief Propagation

Yedidia, J.S., Freeman, W.T., & Weiss, Y. (2003). Understanding belief
propagation and its generalizations. *Exploring AI in the New Millennium*, 8. ✅

### Landscape-Driven Dynamics

Thirumalaiswamy, A. et al. (2025). [Full reference pending — PNAS 2025,
foam systems, D_f ≈ 1.45.] [VERIFY]

### Global Workspace and Interpretability

Gurnee, W., Sofroniew, N., Lindsey, J., et al. (2026, July 6).
Verbalizable representations form a global workspace in language models.
*Anthropic Transformer Circuits Thread.* ✅

Baars, B.J. (1988). *A Cognitive Theory of Consciousness.*
Cambridge University Press. [VERIFY]

### Declared Influences

de Salzmann, M. (2014). *La otra atención.* Sennin Editores. ✅

Fremantle, C. (1993). *On Attention.* Indications Press. ✅

---
*13 confirmed · 3 [VERIFY] · 11 [PENDING]*
*11 pending slots concentrated in §2.2–2.5 — where CKM claims novelty.*
*Resolving pending = resolving [CLAIM] markers in §2.*
---