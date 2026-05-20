# CKM — Cohesive Knowledge Model

**Status:** Research · v26 · May 2026  
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
| P4 | Interior optimal density Ω* in W_mixta | ~ Partial | Confirmed N=32. Ω* exists at N=64 (ρ*≈0.509) but W_mixta advantage diluted — 18 neg. pairs in 2016-pair graph. Open: negative pair density threshold. |
| P5 | Polarized corpus: attractors ~50%N, polarization collapses state diversity | ✓ Confirmed | fourforums gun control. 8 attractors, 50%N. |
| P6 | Delta (asymmetric initiation) acts as symmetry-breaking mechanism | ✓ Confirmed | CreateDebate: 54pp collapse of mixed states. fourforums: **100pp** collapse. Directional role structure preserved across independent corpora. |

**P4 open question:** negative pair density sweep shows W_mixta advantage reappears between k=72 and k=108 at N=64. k* with real corpus W pending term_map reconstruction.

**P7 (confirmed v26):** every system with genuine structural tension has at least one type-965 node — high in/out ratio, never initiates, high coercivity. Confirmed in both corpora: Author 965 (CreateDebate, ratio=455×) and Author 204 (fourforums, ratio=296×). Its absence indicates fabricated tension. Open: falsification in other IAC domains.

---

## Key Experimental Findings

**N=32 internal corpus:**
- 88 distinct attractors. Saturated attractor disappears completely.
- `traza_inferencia` is the only core-invariant node (84% of attractors).
- 4 co-presence clusters: contact · tension · motor · ground.
- Perfect structural oppositions: cohesion_fabricada↔M_M, atractor_espurio↔portero, sentido_comun↔inconmensurabilidad.
- Attractor size is a property of W, not of initial state.

**External validation — fourforums gun control (414K posts, v26):**
- Pipeline `fourforums_pipeline_v8g.py` on 570MB SQL dump. Critical fix: `post_id` is local per discussion — composite key raised mapped posts from 468 to 35,966.
- 905 gun control discussions, 304 authors with stance, 42,395 interactions, 26,346 cross-stance (62%).
- Author 204: out=0, in=148, ratio=296×. Structural analog of Author 965. ≥5 pure sustainer nodes, both stances.
- P6 collapse: **100pp** (vs 54pp CreateDebate). Directional role structure (sustainer/attacker) is a property of the gun control domain, not a corpus artifact.

---

## Repository Structure

```
ckm/
├── core.py                         # CKMGraph: W+Δ, c(S), Gatekeeper R15
├── ckm_p1p4_module.py              # P1–P4 reusable module
├── ckm_topology_module.py          # Topological invariants H0/H1/H2, orientability chains
├── CLAUDE.md                       # Coding guidelines
├── THEORY.md                       # Formal rules R01–R17, knowledge orders
├── EXPERIMENTS.md                  # Full experimental methodology and results
├── METHODOLOGY.md                  # Project methodology — inductive, documented
├── CHANGELOG.md                    # Version history v1–v26
├── CONVENTIONS.md                  # Naming and structural conventions
├── ENTRY_POINT.md                  # Onboarding guide for new agents/readers
├── API_SPEC.md                     # API specification for agent integration
├── experiments/
│   ├── p4_neg_sweep.py             # P4 negative pair density sweep
│   ├── fourforums_pipeline_v8g.py  # fourforums IAC 2010 pipeline (final)
│   ├── fourforums_delta_v7.py      # Delta (asymmetry) computation
│   ├── find_965_v3.py              # Type-965 node detection
│   ├── explore_tables.py           # IAC SQL schema exploration
│   ├── test_ckm_p1p4.py            # P1–P4 test suite
│   └── c6c_fourforums_extraction.py
├── registers/
│   ├── REG_pairs_createdbate_guncontrol_v1.md
│   ├── REG_pairs_fourforums_guncontrol_v1.md
│   ├── REG_c6c_comparison_guncontrol_v1.md
│   ├── REG_p6_fourforums_guncontrol_v1.md
│   ├── REG_stance_fourforums_v1.md
│   ├── REG_holonomy_coercivity_fourforums_v1.md
│   ├── REG_author_965_structure_v1.md
│   └── REG_sesion_perspectivas_rp2_ff_v7.md
├── logs/
│   ├── run_v8g.log                 # fourforums pipeline v8g run evidence
│   └── find_965_v3.log
└── docs/
    └── CKM_Informe_Trabajo_v26.docx  # Full working report
```

**Topology module — first results (v26):**
- H0=1 at all thresholds: corpus is a single connected component.
- H1=0 at all thresholds: no independent cycles — tree-like complex.
- Cilindro (orientable) at all thresholds: no Möbius torsion. Structural tensions are resolvable divergences. R12 (incommensurability) not present in current corpus.
- H2≈845 (approximate): large cavity count — candidate signature of missing intermediate knowledge.
- Bug fixed in `check_orientability`: boundary formula sign correction. Verified on K4 and C5.

---

**Requirements:** Python 3.10+, numpy, scipy, matplotlib

```bash
pip install numpy scipy matplotlib
```

**Core usage:**
```python
from core import CKMGraph, CKMConfig
import numpy as np

# Build graph from corpus
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

## Open Gaps

These are documented as gaps, not concealed:

| Gap | Status |
|-----|--------|
| term_map N=64 complete reconstruction | Pending — requires dedicated session |
| W_base_n64.npy (real corpus W) | Depends on term_map |
| R15 gatekeeper: formal criteria for portero admission | Partially formalized (C1–C4); semantic criteria open |
| Knowledge cohesive: representation model | Open — hysteresis is the only defined property |
| P4 k* with real W_base | Pending after term_map reconstruction |
| P7 falsification in other IAC domains | Confirmed gun control — open: abortion, climate, evolution |
| W asymmetric fourforums | Pending — requires MTurk labels (mturk_2010_qr_task1_worker_response) |
| Author 204 content verification | Identified by ratio; content analysis pending |
| COCO implementation | Unimplemented central hypothesis |

---

## Methodology Note

The CKM was developed through a process of **phenomenology as first step of engineering**: conceptual clarity precedes specification. The working reports (v2–v26) are not documentation of a separate process — they are the process. The conversation is the corpus.

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
