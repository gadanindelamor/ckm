# CKM — Cohesive Knowledge Model

**Status:** Research · v29 · Jun 2026  
**Author:** gadanin.delamor  
**License:** MIT

---

## What is CKM

CKM is a formal model for knowledge graph dynamics in multi-agent systems. Its core problem: how to evaluate whether new knowledge is genuinely interdependent with an existing knowledge body — not just semantically proximate, not just from a trusted source.

The model uses a Hopfield attractor architecture over a weighted knowledge graph, with a coherence measure derived from ferromagnetic physics. It distinguishes three layers:

- **W** — symmetric co-occurrence weight matrix (N×N). Structural memory.
- **Δ** — asymmetric directional dependency matrix (N×N). Inference orientation.
- **c(S)** — coherence measure = mean(W_ij · σ_i · σ_j) over all pairs i<j. Negative normalized Hopfield energy. Measures W/state alignment.

**W and Δ are kept strictly separate.** Mixing them destroys attractor recovery capacity (verified: recovery drops from 0.78 to 0.02).

---

## Architecture

```
Agent produces knowledge node
        ↓
  Gatekeeper (R15)        ← O(N) per node, binary, bounded time
  C1: minimum connection weight
  C2: c(S) delta ≥ -ε
  C3: direction score > 0  (M.M criterion)
  C4: capacity < α_c · N
        ↓
  Knowledge graph (W + Δ)
        ↓
  Hopfield relaxation      ← async update, finds stable attractor
        ↓
  Continuous verification  ← recalibrates weights, chain propagation
```

**Coherence function:**
```python
def cS(sigma, W):
    pairs = [(i,j) for i in range(N) for j in range(i+1, N)]
    return np.mean([W[i,j] * sigma[i] * sigma[j] for i,j in pairs])
```

**W_mixta:** W_base + structural negative weights on opposed pairs. Required at N≥32 — W≥0 produces spurious saturation.

---

## Verified Predictions

Six falsifiable predictions, confirmed experimentally on internal corpus (N=32, N=64) and two independent external domains (CreateDebate gun control, fourforums gun control).

| # | Prediction | Status | Notes |
|---|-----------|--------|-------|
| P1 | Hysteresis loop in c(S): incorporating ≠ removing at identical density | ✓ Confirmed | N=32, N=64, external domains. p≈0. |
| P2 | Cascade distribution P(s) ∝ s^-τ, τ∈[1.5,2] | ✓ Confirmed | N=32 extended zone, N=64 τ=1.775 |
| P3 | Temporal asymmetry: relaxation after removal > after addition | ✓ Confirmed | N=32 p<0.0001, N=64 p≈0 |
| P4 | Interior optimal density Ω* in W_mixta | ✓ Confirmed | N=32 W_ckm_corpus_v2. Ω* interior confirmed. N=64 dilution is structural: 18 neg. pairs in 2016-pair graph — k-core density problem, not scale. Open: extend to other domains (fourforums topics, A2A). |
| P5 | Polarized corpus: attractors ~50%N, polarization collapses state diversity | ✓ Confirmed | fourforums gun control. 8 attractors, 50%N. |
| P6 | Delta (asymmetric initiation) acts as symmetry-breaking mechanism | ✓ Confirmed | CreateDebate: 54pp collapse of mixed states. fourforums: 80pp collapse. |

**P4 open question:** negative pair density sweep shows W_mixta advantage reappears between k=72 and k=108 at N=64. k* threshold requires W_mixta with adequate negative pair density for that graph size — calibration problem, not construction.

**P7 (confirmed — open to new domains):** every system with genuine structural tension has at least one type-965 node — high in/out ratio, frequent in frustrated triads, high coercivity. Its absence indicates fabricated tension. Confirmed: CreateDebate (author 965, ratio 455×) and fourforums gun control (author 204, ratio 296×). Falsifiable in any new domain.

---

## Key Experimental Findings

**N=32 internal corpus:**
- 88 distinct attractors. Saturated attractor disappears completely.
- `traza_inferencia` is the only core-invariant node (84% of attractors).
- 4 co-presence clusters: contact · tension · motor · ground.
- Perfect structural oppositions: cohesion_fabricada↔M_M, atractor_espurio↔portero, sentido_comun↔inconmensurabilidad.
- Attractor size is a property of W, not of initial state.

**External validation — fourforums gun control (414K posts):**
- Author 965: out=1, in=455, ratio 455x. Never initiates. Present in C3 (frustrated triad) in 89% of pairs.
- 32 tension axes converge on Author 965 (verified projective bundle).
- Triads containing Author 965: coercivity = 0 at up to 50% noise. Triads without 965: coercivity = 0 at noise = 0 (already collapsed).
- Holonomy confirmed: path A→B vs B→A produces same dominant attractor but different amplitude (+0.176 fraction active in 4/8 asymmetric pairs).

---

## Repository Structure

```
ckm/
├── core.py                         # CKMGraph: W+Δ, c(S), Gatekeeper R15
├── CLAUDE.md                       # Coding guidelines
├── THEORY.md                       # Formal rules R01–R17, knowledge orders
├── EXPERIMENTS.md                  # Full experimental methodology and results
├── METHODOLOGY.md                  # Project methodology — inductive, documented
├── CHANGELOG.md                    # Version history v1–v29
├── CONVENTIONS.md                  # Naming and structural conventions
├── API_SPEC.md                     # API specification for agent integration
├── experiments/
│   ├── p4_neg_sweep.py             # P4 negative pair density sweep
│   ├── fourforums_pipeline_v8b.py  # fourforums IAC 2010 pipeline
│   ├── fourforums_delta_v5.py      # Delta (asymmetry) computation
│   └── c6c_fourforums_extraction.py
├── registers/
│   ├── REG_pairs_createdbate_guncontrol_v1.md
│   ├── REG_c6c_fourforums_v1.md
│   ├── REG_p6_fourforums_guncontrol_v1.md
│   ├── REG_holonomy_coercivity_fourforums_v1.md
│   ├── REG_author_965_structure_v1.md
│   └── REG_sesion_perspectivas_rp2_ff_v7.md
└── docs/
    └── docs/CKM_Informe_Trabajo_v29.md  # Full working report
```

---

## How to Run

**Requirements:** Python 3.10+, numpy, scipy, matplotlib

```bash
pip install numpy scipy matplotlib
```

**Core usage:**
```python
from core import CKMGraph, CKMConfig
import numpy as np

# Build graph from corpus — automatic extraction (no term_map required)
graph = CKMGraph.from_corpus(
    paragraphs=paragraphs,
    negative_pairs=neg_pairs
)

# Or with explicit term_map (Path A — manual control)
graph = CKMGraph.from_corpus(
    paragraphs=paragraphs,
    nodes=nodes,
    term_map=term_map,
    negative_pairs=neg_pairs
)

# Evaluate a node
result = graph.gatekeeper("traza_inferencia")
print(result)  # GatekeeperResult(admitted=True, ...)

# Measure coherence
print(graph.cS())
```

**P4 density sweep:**
```bash
python experiments/p4_neg_sweep.py
# Output: p4_neg_density_sweep.png + .csv
```

---

## Current State — v29

What exists and operates:

| Component | Status |
|-----------|--------|
| P1–P7 | ✓ All confirmed — see Verified Predictions |
| HOLDINGs H1/H2/H3 | ✓ Closed analytically via AA/AB/BB pair structure |
| COCOThermostat | ✓ Operational — 43/43 tests. STOP + TEMP_SIGNAL. β_collective via endogenous weighting (real rejection, not declared). |
| NodeExtractorService | ✓ Operational — TF-IDF, stateless, no LLM |
| from_corpus() Path B | ✓ Automatic extraction — term_map no longer required |
| Firma del Corpus | Concept established — implementation pending |
| IAP Highway Network | Concept established — implementation pending |
| β_collective active regulation | Observable — not yet acting on the field. Next step. |

## Open

Gaps documented by nature, not by urgency:

**Completeness** — the system knows how; execution pending:

| Item | Status |
|------|--------|
| W_base N=64 | N=64 corpus extraction — independent of term_map |
| P4 k* at N=64 | W_mixta calibration for N=64 graph density — not a scale problem |

**Exploration** — falsifiable in new territory:

| Item | Status |
|------|--------|
| P7 in new domains | Confirmed: gun control (CreateDebate + fourforums). Open: abortion, climate, evolution. FabricationService articulates P7 (topology) with field dynamics (c(S), fi, D_ckm) — connection not yet formalized. |

**Formalization** — exists implicitly; form is the question:

| Item | Status |
|------|--------|
| R15 gatekeeper | C1–C4 structural criteria formalized. Semantic criteria open. |
| Knowledge cohesive representation | c(S) + attractor landscape is the representation. Not yet named as such in KR terms. Whether explicit formalization is necessary: open. |

**Direction** — architectural decision pending:

| Item | Status |
|------|--------|
| Versioned W | Shared dependency of Firma del Corpus and IAP. Threshold between concepts established and implementations. |

---

## Methodology Note

The CKM was developed through a process of **phenomenology as first step of engineering**: conceptual clarity precedes specification. The working reports (v2–v29) are not documentation of a separate process — they are the process. The conversation is the corpus.

IAID.md (the parent architecture) was written in 2024, before MCP existed. The convergence with MCP, A2A, and related protocols was discovered in review, not designed. This is treated as validation by independence, not alignment.

---

## Related Work

- Hopfield (1982): associative memory via energy minimization
- Sciamarella & Mindlin (2001): topological analysis of dynamics (BraMAH)
- IAC Internet Argument Corpus (Abbott et al., 2016): fourforums dataset
- Dung (1995): abstract argumentation frameworks
- MCP (Anthropic, Nov 2024): Model Context Protocol

---

## Contact

gadanin.delamor — May 2026
