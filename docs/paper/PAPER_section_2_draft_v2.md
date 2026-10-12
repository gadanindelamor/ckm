# Section 2 — Related Work (Draft v2)

*Draft v2 — Section 2 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*
*v2: §2.1 updated with Venkatesh & Bu 2025 citation + trajectory distinction;
 §2.7 added — J-Space / Global Workspace (Gurnee et al., Anthropic, Jul 6 2026)*

*Epistemic conventions as in prior sections.*
*— "verified": confirmed experimentally under stated conditions*
*— "observed": documented without controlled verification*
*— "proposed": theoretical framing, not yet tested*
*— [AUTO]: marks where automatism was noticed and resisted*
*— [CITATION]: placeholder — reference to be supplied*
*— [CLAIM]: novelty claim that requires comparison with specific prior work to hold;
   held provisionally until that comparison is done.*

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
performance." Their proposed remedy is *trajectory assessment* — evaluating
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
discriminates cases that the others pass. *[Verified: C3 in particular
detects common-sense attractors with c(S) identical to cohesive attractors —
a case that C1 and C2 do not separate. See Section 5.]*

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
accumulation. See REG_destruccion_recuperacion_v1.md and Section 5.]*

This allows W to represent genuine structural tension rather than proximity
alone — a property required for analyzing debate corpora where opposition
is a primary structural feature, not an exception.

A separate matrix Δ encodes asymmetric directional dependency: Δ_ij ≠ Δ_ji.
This is structurally equivalent to directed graphs with asymmetric adjacency
matrices [CITATION], but with a specific semantic role: Δ captures inference
orientation (who cites whom, in which direction) rather than general
directionality. The separation W/Δ is not a design choice — it was
established empirically. *[Verified: combining W and Δ into a single matrix
drops attractor recovery from 0.78 to 0.02. See Section 4.]*

### 2.4 Structural Role Detection in Debate Networks

Stance detection in debate corpora is typically framed as a supervised
classification task: given labeled stance data (pro/con, agree/disagree),
train a classifier to assign stances to unlabeled texts or authors
[CITATION]. The state of the art includes transformer-based models fine-tuned
on stance datasets [CITATION], which achieve high accuracy when labeled data
is available.

CKM identifies a distinct structural phenomenon — the Type-965 node — without
supervision and without stance labels. Type-965 nodes are characterized by
extreme asymmetry in the directional matrix Δ (in/out ratio ≥ 100×): they
receive citations from a large number of distinct sources but initiate almost
none. In the fourforums gun control corpus, Author 965 has ratio 455× (out=1,
in=455). In CreateDebate gun control, Author 204 has ratio 296×. Both are
present as the third node (C3) in 89% of the identified tension pairs across
both corpora.

*[Verified: triads containing a Type-965 node maintain coercivity = 0 at up
to 50% noise; triads without a Type-965 node collapse at noise = 0.
See REG_author_965_structure_v1.md and Section 5.]*

The structural role captured by Type-965 detection — tension anchor, never
initiator — is not a stance. It is a topological property of the citation
network that is not targeted by stance classifiers. *[CLAIM: this role has
not, to our knowledge, been identified in the debate analysis literature as
a distinct structural category. Requires literature review to confirm.]*

### 2.5 Criticality in Argument and Knowledge Networks

Self-organized criticality (SOC) [CITATION: Bak et al., 1987] predicts a
power-law cascade distribution P(s) ∝ s^{-τ} with a single critical
parameter value at the phase transition. In the analysis of complex networks,
this has been used to characterize information propagation and cascade
behavior in social and debate networks [CITATION].

In CKM's internal corpus (N=32), the power-law distribution P(s) ∝ s^{-τ}
with τ ∈ [1.5, 2] is maintained across an extended zone θ ∈ [0.002, 0.010],
not at a single critical point. *[Verified: N=32 confirmed, N=64 τ=1.775.
See Section 5 (P2).]*

Extended criticality — in contrast to a single critical point — has been
reported in neuronal network dynamics [CITATION] and in certain spin-glass
models [CITATION]. Its presence in a small knowledge graph (N=32) is observed
here but not yet interpreted. *[Observed, not verified across domains.
P2 is confirmed at N=32 and N=64; its generalization to other corpora
is stated as an open prediction.]*

### 2.6 Attractor-Based Memory Architectures

The Hopfield network [CITATION: Hopfield, 1982] provides the energy
minimization formalism underlying CKM's cohesion measure c(S) and its
attractor dynamics. The original Hopfield formulation uses Hebbian learning
to update the weight matrix during operation. In CKM, Hebbian learning on W
was tested and rejected: it destroys attractor diversity.
*[Verified: recovery drops from 0.78 to 0.02. See Section 4.]*

Modern Hopfield networks [CITATION: Ramsauer et al., 2020] significantly
increase storage capacity through higher-order interactions. CKM operates on
the classical Hopfield formulation with fixed W — the concern is not storage
capacity but diversity of stable attractors and resistance to coherence
collapse (coercivity).

A property not explicitly discussed in the standard Hopfield literature is
the invariance of attractor recovery across scale. In CKM, at 10% noise,
attractor recovery is verified as effectively 1.000 across N = 16 to N = 128.
*[Observed: verified in CKM corpus experiments. The invariance across N has
not been analyzed as a specific property in the Hopfield literature known
to the authors — [CLAIM: requires confirmation against relevant literature].]*
In embedding-based retrieval systems, retrieval quality degrades continuously
with noise [CITATION]. The Hopfield attractor architecture offers a distinct
guarantee: exact recovery within the basin of attraction, with the basin
boundary set by W structure, not by noise magnitude alone.

A second property relevant to CKM's use case is the accumulation of
structural rejection memory in Δ_r. As interactions proceed, co-activation
pairs that are repeatedly rejected by Hopfield relaxation accumulate in Δ_r.
This constitutes a form of structural learning — without gradients, without
labels, with O(N²) complexity only in the co-activation accumulation step,
not in individual evaluation. The resulting system progressively learns which
concept combinations are incoherent given the field, from evidence produced
by the field itself. This mechanism has structural analogy with spike-timing
dependent plasticity [CITATION] but operates at the level of co-occurrence
rejection rather than firing timing.

### 2.7 Internal Workspace Architecture in Single Models: J-Space

Gurnee, Sofroniew, Lindsey et al. (Anthropic, July 6 2026) identified a
privileged low-dimensional subspace within transformer activations — the
J-space — using a Jacobian-based lens (J-lens) that isolates directions
with verbalizable causal influence on future outputs [Gurnee et al., 2026].
The J-space accounts for a median 6–7% of concept vector variance yet is
"almost entirely responsible" for verbal report and multi-step reasoning;
ablating it collapses inference and translation while leaving fluency intact.

The paper demonstrates that the J-space satisfies five functional criteria
associated with Bernard Baars's Global Workspace Theory: verbal report,
directed modulation, internal reasoning, flexible generalization, and
selectivity. The J-space operates as a broadcast hub: MLP gain on J-space-
aligned directions rises to approximately 10× within the workspace band
(layers ~38–92 on a normalized 0–100 depth scale), and the top 1% of
attention heads relay J-space content between positions. Commitment is
bimodal: for ambiguous inputs, early layers track proportionally, but from
layer 38 onward the representation snaps discretely to one attractor-like
endpoint at a threshold value.

CKM and J-space are positioned at different levels of analysis. J-space is
an empirical, within-model, single-forward-pass interpretability finding
about one transformer's internal activations — it describes how coherent
cognition is organized inside a model. CKM is a normative, multi-agent
framework for measuring structural field dynamics *across* agents and
corpora — it describes how shared knowledge is organized across an ensemble
of interacting devices. Neither subsumes the other.

*[AUTO: pull to write "CKM anticipated J-space." Resisted — the correct
framing is convergence by independence, not anticipation. IAID was written
in 2024; the J-space paper was published July 2026. The convergence was
discovered in review, not designed in.]*

The structural parallels are nonetheless specific:

- **Privileged coherence substrate.** Both posit a small, privileged
  structure atop a much larger substrate that governs coherent higher-order
  cognition. J-space: 6–7% of variance in activations. CKM: c(S) computed
  over signed co-occurrence weights, separating "load-bearing structural
  coherence" from bulk representation.

- **Attractor formalism.** J-space's bimodal ignition at layer 38 — discrete
  commitment to one endpoint at a threshold — is precisely what Hopfield
  attractor dynamics predict. The modern Hopfield network literature already
  formalizes transformer attention as energy-minimizing attractor recovery
  [CITATION: Ramsauer et al., 2020]; CKM's use of Hopfield attractors to
  model field states is architecturally consistent with the dynamics J-space
  empirically documents.

- **Signed interaction weights.** CKM's c(S) = ⟨W_ij · σ_i · σ_j⟩ is an
  Ising-Hamiltonian-style object where negative W_ij entries encode structural
  opposition. J-space's broadcast-hub wiring — components that read from and
  write to J-space patterns with MLP gain ~10× — is the empirically measured
  analog of strong signed coupling between specific nodes.

- **Directional asymmetry.** CKM's Δ (asymmetric directional dependency,
  Δ_ij ≠ Δ_ji) parallels the J-lens's inherently directional, causal
  construction (∂ future-output / ∂ activation) — a forward-directed
  dependency measure, not a symmetric correlation.

- **Bounded capacity.** J-space maintains ~25 active J-lens vectors at
  occupancy plateau, evicting stale content on category switches.
  CKM's capacity constraint C4 (R15 gatekeeper) imposes an analogous bound:
  the system rejects new nodes that would push it past the structural
  saturation threshold α_c · N.

These convergences are structural analogies, not formal identities. The
mechanisms differ: J-space is an emergent property of training, measured
post-hoc with a probe; CKM's constraints are engineered and imposed. The
analogy is evidence of structural consistency — the same architectural
pressures (coherence maintenance, capacity bounding, directional asymmetry)
appear at both levels of analysis independently.

*[CLAIM: the convergence in architectural structure between J-space and CKM,
arrived at independently, is proposed as convergent validation. This claim
requires formal comparison rather than structural analogy to hold rigorously.]*

**Reference:** Gurnee, W., Sofroniew, N., Lindsey, J. et al. (2026).
"Verbalizable Representations Form a Global Workspace in Language Models."
Anthropic Transformer Circuits Thread, July 6, 2026.

---

*Section 2 draft v2 complete.*

*Citations confirmed:*
*— Venkatesh & Bu (2025) — Google Developer, A2A — fills [CITATION] §2.1*
*— Gurnee et al. (2026) — Anthropic Transformer Circuits Thread — fills §2.7*

*Six [CITATION] placeholders remain for incoming literature:*
*— §2.1: embedding-space agreement metrics (general)*
*— §2.2: single-criterion knowledge admission systems*
*— §2.3: knowledge graph representation, negation detection*
*— §2.4: stance detection transformers*
*— §2.5: SOC Bak et al. 1987; extended criticality in neuronal networks*
*— §2.6: Ramsauer et al. 2020 (modern Hopfield); STDP analog*

*Four [CLAIM] markers pending literature resolution:*
*— M.M. criterion absent from knowledge admission literature (§2.2)*
*— Type-965 as structural category not identified in debate analysis (§2.4)*
*— Recovery invariance across N not discussed as specific property (§2.6)*
*— J-space/CKM convergence as convergent validation — requires formal*
*   comparison beyond structural analogy (§2.7)*

*Item 5.7 (recovery invariance) appears in §2.6 — was not in any prior section of v2.*
*§2.7 is new to v2 — J-space not previously represented in the paper.*
