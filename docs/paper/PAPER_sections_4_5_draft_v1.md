# Landscape Driven Devices: A Cohesive Knowledge Model for Semantic Field Analysis in Multi-Agent Interaction

*Draft — Sections 4–5 · Ago 2026 · gadanin.delamor + Claude Sonnet 4.6*

*Epistemic convention used in this draft:*
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

W has two operational modes:

- *Fixed corpus mode (experimental validation):* W is built once from a
  pre-assembled corpus and does not change during the analysis run.
  Used in all P1–P7 validation experiments.

- *Live ingestion mode (IAP channel):* W is rebuilt each time CorpusService
  crosses the `min_texts` threshold as new messages arrive. Each rebuild
  is recorded by WVersionManager as a lightweight trace point (timestamp,
  sha256, corpus_size). FirmaService captures `sha256(W_momento)` at any
  given moment. W is invariant within a cycle; it changes between cycles.

In both modes, W remains separate from Δ and Δ_r.

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
