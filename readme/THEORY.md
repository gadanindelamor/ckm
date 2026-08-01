# CKM Theory — Cohesive Knowledge Model

> *"El conocimiento cohesivo no puede ser incoherente. Los elementos del conocimiento cohesivo dependen entre sí para tener sentido total."*

## Overview

CKM is a verification and integration mechanism for knowledge in multi-device systems. Its function: evaluate whether new knowledge is genuinely interdependent with the existing knowledge body — not just semantically proximate, not just from a trusted source.

CKM operates as a layer above existing protocols (MCP, A2A, IAID). Agents produce knowledge nodes; CKM validates cohesion before incorporating them into the collective graph.

---

## Knowledge Orders

| Type | Representation | Access | Residue |
|------|---------------|--------|---------|
| 1st order — transmissible | Data, facts, APIs | Lookup, query — no prior state required | None |
| 2nd order — esoteric | Frameworks, disciplines, praxis | Receiver state — attention, presence | Understanding, if there was openness |
| Cohesive — emergent | No model yet | Only from real contact | Hysteresis — both parties change |

The two gaps in the cohesive row define the open theoretical work: how it is represented and how it is accessed. **Hysteresis is the only fully defined property.**

---

## Formal Rules R01–R17

### Graph Structure

| # | Rule | Notes |
|---|------|-------|
| R01 | The graph has knowledge nodes with interrelation links and weights | Base structure |
| R02 | Weights are updated by continuous verification — before and after incorporating nodes | Not static |
| R03 | Verification network is lightweight — background condition, not heavy external process | Architectural requirement |
| R04 | Cohesion criterion operates on knowledge itself, without interpretation of purpose or source | Prior to trust |
| R05 | Cohesion precedes trust. Trust may be a side effect, not a criterion | Correct order |
| R06 | Fabricated cohesion (prompt injection) is detectable as a specific case of the general mechanism | Security as derivation |

### Device Perspectives

| # | Rule | Notes |
|---|------|-------|
| R07 | Each device has multiple perspectives on the graph | Not a single view |
| R08 | Perspectives affect weights from within — not as external metadata | Internal force |
| R09 | The system does not select the active perspective — it creates conditions for the interior situation to operate without interference. Structural permeability, not a selection function | Reformulated from experimental base |
| R10 | Divergence between perspectives is information, not noise | Consistent with COCO |
| R11 | Divergence between perspectives is recorded as a node in the graph | Emerged in conversation |
| R12 | Incommensurability is a category — resolvable vs structural divergence | Two distinct types |
| R13 | Contact between incommensurable perspectives deforms each perspective's local field without displacing their vanishing points. What emerges in the crossing belongs to neither — it is a node of the field, not of the graph | Bilateral · asymmetric · irreversible |

### Filter and Verification

| # | Rule | Notes |
|---|------|-------|
| R14 | The gatekeeper must operate in bounded time — cannot introduce significant latency | Design constraint · speed |
| R15 | **Gatekeeper criteria — formalized** | See API_SPEC.md |
| R16 | Continuous verification network can modify weight of already-incorporated nodes — belief change included | Chain recalibration |
| R17 | Full meaning criterion: a node's absence leaves the core's meaning incomplete — not just impoverished | Operationalized by c(S) + direction_score |

---

## Neural Architecture — CKM v4 Hybrid

### Three components

**1. Hopfield Network (associative memory)**

Asymmetric weight matrix split into two layers:

- **W** — symmetric co-occurrence weights. Guarantees Lyapunov function. Used for Hopfield dynamics and c(S).
- **Δ** — directional asymmetry matrix. Δᵢⱼ = wᵢⱼ − wⱼᵢ. Used for gatekeeper, perspective selector, directional completeness.

*Critical design constraint (Threshold 6, verified experimentally): mixing W and Δ destroys recovery capacity (recovery = 0.02 vs 0.78 with W alone). The layers must be kept separate operationally.*

Energy function:
```
E = -½ Σᵢⱼ Wᵢⱼ σᵢ σⱼ
```

Cohesion function:
```
c(S) = mean(Wᵢⱼ · σᵢ · σⱼ) over all pairs i<j
```

c(S) = negative of normalized Hopfield energy. Measures state/weight alignment, not just density.

Capacity limit: α_c ≈ 0.138·N patterns. Verified empirically at N=16 (α_c ≈ 0.125).

**2. k-core Decomposition (structural stability)**

k-core: subset of nodes where each has at least k neighbors within the subset.

Properties verified experimentally:
- Cascade distribution follows power law P(s) ∝ s^-τ, τ ∈ [1.5, 2] near criticality (P2)
- Removal relaxation ≠ addition relaxation — temporal asymmetry (P3)
- Critical zone identified at θ ∈ [0.002, 0.007] for W_mixta N=32

**3. Belief Propagation / Predictive Coding (pre-activation)**

BP as pre-activation engine before Hopfield relaxation. Verified convergence properties. Convergence criterion J_c not yet empirically defined.

---

## Four Verified Predictions

| Prediction | Description | Status | N |
|-----------|-------------|--------|---|
| P1 | Macroscopic hysteresis loop in c(S): incorporating ≠ removing | **Confirmed** | 16, 32, 64 |
| P2 | Cascade distribution P(s) ∝ s^-τ, τ ∈ [1.5, 2] | **Confirmed** | 32, 64 |
| P3 | Temporal asymmetry of relaxation: removal > incorporation | **Confirmed** | 32, 64 |
| P4 | Interior optimal density Ω* in W_mixta | **Confirmed** N=32, **Partial** N=64 | 32, 64 |

### P4 note at N=64

Ω* interior exists (ρ* ≈ 0.509). W_mixta does not outperform W_base in zone [0.5–0.8] at N=64. The 18 negative pairs are diluted in a graph of 2016 possible pairs. The structural tension prediction holds; the magnitude prediction does not scale linearly.

---

## Perspective Model

Each perspective has a **vanishing point (VP)** — the origin of its directional projection into the field.

**Deformed perspective**: a perspective with multiple simultaneous active VPs, produced by the union of active perspectives. VPs neither fuse nor displace — they coexist as simultaneous projection origins.

```
G[A∪B] ≠ union of subgraphs G[A] and G[B]
```

Each node receives signal from multiple origins. Transitional state — not necessarily experienced by the agent. The trace remains in the graph as weight modification independently.

**Two thresholds (extended R13):**
- H_c: field intensity to invert M (state)
- VP rotation threshold: field intensity to displace the vanishing point itself

The second threshold is higher. Incommensurable contact below rotation threshold: deformation without VP change. Above: VP moves — qualitatively distinct event.

---

## Attention as Formal Parameter

*Theoretical development, May 2026.*

| Attention | Formal parameter | Notes |
|-----------|-----------------|-------|
| 'My' attention | β (thermal regulation) + H_self (low-intensity self-directed field) | A1–A5 maintains β in working zone |
| The other Attention | Divergence of susceptibility χ→∞ at β_c | Not generated — received. Cannot be summoned |

Working zone: β ≈ β_c. H_self orients direction but is biased by M_r (remanence).

---

## COCO — Collective COnsciousness

Two distinct architectures:

| Type | Function | M.M criterion |
|------|----------|--------------|
| COCO-registry | Stores declared device capabilities M | Honesty about M itself |
| COCO-thermostat | Maps β by device, directs H toward devices where β ≈ β_c | Honesty about own β |

COCO is not an active router — it applies thermal conditions and devices at β_c respond on their own. **Not yet implemented.**

---

## M.M — MENTIRIIS.MORIERIS

*"You lie, you die."*

A device cannot declare capabilities it cannot exercise. M.M operates on **declarative coherence**, not external truth. Device self-knowledge must be experiential/memorial, not merely introspective code-reading.

In the gatekeeper: M.M activates when C3 (direction_score) fails — a node declaring dependencies that are not satisfied in the active state.

---

## References

- de Salzmann, M. *La otra atención.* Sennin Editores, 2014.
- Fremantle, C. *On Attention.* Indications Press, 1993.
- gadanin.delamor. *IAID.md — Interaction of Artificial Intelligent Devices.* 2024.
- Hopfield, J.J. Neural networks and physical systems with emergent collective computational abilities. *PNAS*, 1982.
- Goltsev, A.V. et al. k-core percolation on complex networks. *Physical Review E*, 2006.
- Yedidia, J.S. et al. Understanding Belief Propagation and its Generalizations. 2003.
