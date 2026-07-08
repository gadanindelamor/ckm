# CKM — Cohesive Knowledge Model

**Status:** Research · v28 · June 2026  
**Author:** gadanin.delamor  
**License:** MIT

---

## What is CKM

CKM is a formal model for knowledge graph dynamics in multi-agent systems. Its core problem: how to evaluate whether new knowledge is genuinely interdependent with an existing knowledge body — not just semantically proximate, not just from a trusted source.

The model uses a Hopfield attractor architecture over a weighted knowledge graph, with a coherence measure derived from ferromagnetic physics. It distinguishes three layers:

- **W** — symmetric co-occurrence weight matrix (N×N). Structural memory. Invariant ground.
- **Δ** — asymmetric directional dependency matrix (N×N). Inference orientation. Trace goes to Δ, not to W.
- **c(S)** — coherence measure = mean(W_ij · σ_i · σ_j) over all pairs i<j. Negative normalized Hopfield energy.

**W and Δ are kept strictly separate.** Hebbian learning on W destroys the structural tension that produces attractor diversity (verified: recovery drops from 0.78 to 0.02). Hebbian learning on Δ preserves W intact.

Designed to operate as a layer over existing protocols (MCP, A2A).

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
  MonitorService           ← D_ckm, Δ_r accumulation, STOP signal
        ↓
  COCOThermostat           ← beta_collective, temp_signal (TOO_COLD/NOMINAL/TOO_HOT)
```

**Coherence function (vectorized):**
```python
ii, jj = np.triu_indices(N, k=1)
c_S = float(np.mean(W[ii, jj] * s[ii] * s[jj]))
```

**W_mixta:** W_base + structural negative weights on opposed pairs. Required at N≥32 — W≥0 produces spurious saturation. Interior Ω* at ρ*≈0.5–0.8 is structurally guaranteed by σ→−σ symmetry (proven: relax(−s)=−relax(s), verified 450/450 paired samples).

**MENTIRIIS.MORIERIS (M.M):** If an agent declares knowledge that the field cannot validate — it declared false. No punishment. Structural consequence.

---

## Verified Predictions

Seven predictions, six confirmed experimentally on internal corpus (N=32, N=64) and two independent external domains (CreateDebate gun control, fourforums gun control, IAC v2).

| # | Prediction | Status | Notes |
|---|-----------|--------|-------|
| P1 | Hysteresis loop in c(S): incorporating ≠ removing at identical density | ✓ Confirmed | N=32 area=0.000862 p≈0. N=64. External domains. |
| P2 | Cascade distribution P(s) ∝ s^−τ, τ∈[1.5,2] | ✓ Confirmed | N=32 extended zone. N=64 τ=1.775. |
| P3 | Temporal asymmetry: relaxation after removal > after addition | ✓ Confirmed | N=32 p<0.0001. N=64 p≈0. |
| P4 | Interior optimal density Ω* in W_mixta | ✓ Confirmed | N=32. Interior peak structurally guaranteed by σ→−σ symmetry. W_mixta c(S) 13× greater than W_pos in external domain. |
| P5 | Polarized corpus: attractors ~50%N, polarization collapses state diversity | ✓ Confirmed | fourforums gun control. 8 attractors ≈ 50%N. |
| P6 | Delta (asymmetric initiation) acts as symmetry-breaking mechanism | ✓ Confirmed | CreateDebate: 54pp collapse. fourforums: 100pp collapse. Polo sos_dom dominant in both. |
| P7 | Every system with genuine structural tension has at least one 965-type node | Hypothesis | Author 965 (CreateDebate, ratio 455×) and Author 204 (fourforums, ratio 296×) as confirmed instances. Absence indicates fabricated tension. Falsifiable in any new domain. |

**P4 open question (N=64):** negative pair density threshold k* between k=72–108 (ratio 0.036–0.054). Real W_base_n64.npy requires term_map reconstruction session.

---

## Key Experimental Findings

**N=32 internal corpus (W_ckm_corpus_v2.json, N=32, corpus_size=5145):**
- 88 distinct attractors. Saturated attractor disappears completely.
- `traza_inferencia` is the only core-invariant node (84% of attractors).
- 4 co-presence clusters: contact · tension · motor · ground.
- Perfect structural oppositions: cohesion_fabricada↔M_M, atractor_espurio↔portero, sentido_comun↔inconmensurabilidad.
- Attractor size is a property of W, not of initial state.

**External validation — fourforums gun control (414K posts, IAC v2):**
- Author 965 (CreateDebate): out=1, in=455, ratio 455×. Present in C3 (frustrated triad) in 89% of pairs.
- 32 tension axes converge on Author 965 (verified projective bundle).
- Triads containing Author 965: coercivity = 0 at up to 50% noise. Triads without 965: coercivity = 0 at noise = 0.
- Holonomy confirmed: path A→B vs B→A produces same dominant attractor, different amplitude (+0.176 fraction active).

**STOP operator:**
- STOP invariant: fraccion_rec ≥ 1.0 always. W is invariant ground — STOP clears Δ, ground re-emerges.
- Effectiveness = f(A_pre): when A_pre < A0 → STOP expands landscape (ratio > 1). alpha*≈0.4 robust.
- Does not interrupt A2A task execution. Operates on Δ accumulation within CKM stack.

**COCOThermostat (43/43 tests):**
- beta_collective = median beta_i of active agents, inferred from rejection history — not declared.
- beta_c_corpus = 1/(ρ* · N · μ_W) = 13.83 (N=32, μ_W=0.004519).
- temp_signal: TOO_COLD (paranoia/starvation) / NOMINAL (Ω* zone) / TOO_HOT (intoxication).

---

## Services Architecture

```
services/
├── monitor_service.py      # MonitorService: D_ckm, Δ_r, STOP signal
├── corpus_service.py       # CorpusService: W_mixta construction, persistence
├── node_extractor.py       # NodeExtractor: TF-IDF n-gram extraction (v1)
└── mcp_adapter.py          # MCP/A2A envelope → text extraction → MonitorService
```

**COCOThermostat** (`coco_thermostat.py`): optional injection into MonitorService. `evaluate(text, agent_id=None)`.

**IAP — Intel Access Point** (concept, implementation pending): CKM Chatrooms for multi-agent interaction over MCP. Private Highway Network for STOP and TEMP_SIGNAL — high-priority internal channel, separate from A2A routing.

---

## Repository Structure

```
ckm/
├── core.py                              # CKMGraph: W+Δ, c(S), Gatekeeper R15
├── CLAUDE.md                            # Coding guidelines
├── CONVENTIONS.md                       # Naming and structural conventions
├── THEORY.md                            # Formal rules R01–R17, knowledge orders
├── EXPERIMENTS.md                       # Experimental methodology and results
├── METHODOLOGY.md                       # Project methodology
├── CHANGELOG.md                         # Version history v2–v28
├── API_SPEC.md                          # API specification for agent integration
├── services/
│   ├── monitor_service.py
│   ├── corpus_service.py
│   ├── node_extractor.py
│   ├── coco_thermostat.py
│   └── mcp_adapter.py
├── experiments/
│   ├── fourforums_pipeline_v8g.py       # fourforums IAC v2 pipeline
│   ├── fourforums_pipeline_v8h.py       # W_asim + neg pairs
│   ├── p4_neg_sweep.py                  # P4 negative pair density sweep
│   ├── calibrate_W_mixta.py             # AMP sweep (sharp transition AMP=40→45)
│   ├── explore_qr_asymmetry_v2.py       # QR asymmetry / holonomy
│   ├── exp_monitor_trajectory.py        # MonitorService trajectory experiments
│   └── test_coco_thermostat.py          # 43/43 tests
├── registers/
│   ├── REG_pairs_createdbate_guncontrol_v1.md
│   ├── REG_p6_fourforums_guncontrol_v1.md
│   ├── REG_holonomy_coercivity_fourforums_v1.md
│   ├── REG_author_965_structure_v1.md
│   ├── REG_beta_colectivo_v1.md
│   ├── REG_firma_corpus_v1.md
│   ├── REG_coco_thermostat_proto_v1.md
│   ├── REG_stop_grados_perdida_v1.md
│   ├── REG_octava_ckm_v1.md
│   └── [full register list: MAPA_REG_corpus_v1.md]
└── docs/
    ├── CKM_Informe_Trabajo_v28.docx
    └── informe_tecnico_ckm_loc0530_.md
```

---

## How to Run

**Requirements:** Python 3.10+, numpy, scipy, matplotlib, scikit-learn

```bash
pip install numpy scipy matplotlib scikit-learn
```

**MonitorService:**
```python
from services.monitor_service import MonitorService
from services.coco_thermostat import COCOThermostat

thermostat = COCOThermostat(W)
monitor = MonitorService(W, thermostat=thermostat)

result = monitor.evaluate("texto del agente", agent_id="agent_001")
print(result)  # MonitorResult(admitted=True, D_ckm=..., temp_signal=...)
```

**COCOThermostat:**
```python
from services.coco_thermostat import COCOThermostat

thermostat = COCOThermostat(W)
print(thermostat.beta_c_corpus())   # 13.83
print(thermostat.temp_signal())     # NOMINAL / TOO_COLD / TOO_HOT
print(thermostat.beta_collective()) # median beta_i of active agents
```

**P4 density sweep:**
```bash
python experiments/p4_neg_sweep.py
# Output: p4_neg_density_sweep.png + .csv
```

**W_mixta calibration:**
```bash
python experiments/calibrate_W_mixta.py
# Sharp phase transition at AMP=40→45 (A0: 25→79)
```

---

## Open Gaps

| Gap | Status |
|-----|--------|
| term_map N=64 complete reconstruction | Pending — requires dedicated session with delamor validation |
| W_base_n64.npy (real corpus W) | Depends on term_map |
| P4 k* with real W_base N=64 | Pending after term_map reconstruction (k* between 72–108) |
| P7 falsification in new domain | Hypothesis only |
| NodeExtractor v2 (spaCy noun phrases) | Pending — network constraints during v1 implementation |
| Sweep D_ckm(t_stop) × alpha | Design revised (f(A_pre) not f(D_ckm)) — experiment pending |
| mu_W refinement (global → positive-only) | For beta_c_corpus — intentional conservatism, deferred |
| IAP Highway Network implementation | Requires COCOThermostat + versioned W |
| Firma del Corpus implementation | Requires COCOThermostat + MonitorService + versioned W |
| IAP chatroom minimum viable design | Open: requires two agents with structurally opposed objectives |

---

## Methodology Note

CKM was developed through **phenomenology as first step of engineering**: conceptual clarity precedes specification. The working reports (v2–v28) are not documentation of a separate process — they are the process. The conversation is the corpus.

IAID.md (the parent architecture) was written in 2024, before MCP existed. The convergence with MCP, A2A, and related protocols was discovered in review, not designed. This is treated as validation by independence, not alignment.

**"La interacción es el protocolo, no su precursor."**

---

## Related Work

- Hopfield (1982): associative memory via energy minimization
- Sciamarella & Mindlin (2001): topological analysis of dynamics (BraMAH)
- IAC Internet Argument Corpus (Abbott et al., 2016): fourforums, CreateDebate datasets
- Dung (1995): abstract argumentation frameworks
- MCP (Anthropic, Nov 2024): Model Context Protocol
- A2A Protocol v1.0 (Linux Foundation, 2026): Agent-to-Agent communication standard
- de Salzmann, M. (2014): La otra atención
- Ouspensky, P.D. (1949): In Search of the Miraculous

---

## Contact

gadanin.delamor — June 2026
