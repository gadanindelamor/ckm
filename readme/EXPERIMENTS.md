# CKM Experiments — Methodology and Results

> All experiments use real corpus co-occurrence, not synthetic weights. Results are reproducible with `numpy.random.seed(42)`.

---

## Corpus

**Source:** CKM Working Reports v2–v28 (gadanin.delamor + Claude Sonnet 4.6, April–June 2026).

**Construction:** paragraph-level co-occurrence. A link W[i,j] exists if nodes i and j appear in the same paragraph. W normalized by total paragraph count.

**W_mixta:** W_base + negative weights (-0.10) on structurally opposed pairs. Negative pairs persisted in `neg_pairs_config_fourforums_v8h.json` (60 neg + 7 pos pairs).

---

## Node Sets

### N=16 (original corpus)

```
full_meaning, c_S, filtro_previo, k_core, hopfield, BP,
histéresis, COCO, perspectiva_device, divergencia, AWARENESS, red_verificacion,
conocimiento_cohesivo, cohesion_fabricada, atractor_patron, atractor_espurio
```

### N=32 (expanded corpus)

N=16 + 16 new nodes extracted by real frequency:
```
portero, perspectiva_deforme, sentido_comun, tension_estructural,
inconmensurabilidad, ATR_733, M_M, beta_termal,
DOM_I, DOM_II, W_enriquecida, chispazo,
traza_inferencia, W_mixta, campo_local, vanishing_point
```

### N=64 (full corpus)

N=32 + 32 new nodes from v24 sections 20–28 and current session concepts.

---

## Hopfield Dynamics

Asynchronous deterministic update:

```python
def relax(sigma_init, W, max_iter=1000):
    sigma = sigma_init.copy()
    for _ in range(max_iter * N):
        i = np.random.randint(N)
        h = np.dot(W[i], sigma)
        sigma[i] = 1 if h > 0 else (-1 if h < 0 else sigma[i])
    return sigma
```

Cohesion function:

```python
def cS(sigma, W):
    pairs = [(i,j) for i in range(N) for j in range(i+1, N)]
    return np.mean([W[i,j] * sigma[i] * sigma[j] for i,j in pairs])
```

---

## Experiment: Attractor Structure

**Initial condition:** all nodes active (σ=+1) + 2 random flips.  
**Runs:** 300 (N=32), 500 (N=64).

### Results

| N | Unique attractors | Mean active | % N | Saturated | Peripheral nodes |
|---|-----------------|-------------|-----|-----------|-----------------|
| 16 | ~6 | 13.1 | 81% | yes (28%) | histéresis, COCO, AWARENESS |
| 32 | **88** | 17.1 | 54% | **0%** | none |
| 64 | **462** | 41.7 | 65% | 0% | none |

**Key finding N=32:** the saturated attractor disappears completely. 100% asymmetric attractors. Unique core node: `traza_inferencia` (84% of attractors). Lives in cluster C2 (tension).

**Key finding N=64:** combinatorial explosion ×5. Core migrates to applied concepts (holonomia, monitor_CKM, API_extendida, etc.).

---

## Experiment: 4 Co-presence Clusters (N=32)

Pearson correlation over attractor binary matrix → hierarchical clustering (Ward) → 4 clusters.

| Cluster | Name | Nodes | Internal correlation |
|---------|------|-------|---------------------|
| C1 | Contact | histéresis · perspectiva_deforme · chispazo · vanishing_point | +1.000 |
| C2 | Tension | traza_inferencia · M_M · DOM_II · inconmensurabilidad · full_meaning · atractor_espurio + 4 | high positive |
| C3 | Operational motor | c_S · k_core · hopfield · BP · COCO · perspectiva_device · divergencia · AWARENESS · red_verificacion · atractor_patron · portero · ATR_733 · W_enriquecida | high positive |
| C4 | Ground | filtro_previo · cohesion_fabricada · sentido_comun · beta_termal · DOM_I | high positive |

Perfect negative correlations (verified design oppositions):
- `cohesion_fabricada` ↔ `M_M`
- `atractor_espurio` ↔ `portero`
- `sentido_comun` ↔ `inconmensurabilidad`

---

## Experiment B: What Determines Attractor Size?

**B1 — Initial density scan (ρ=0.1 to 1.0, 200 runs each):**

Result: mean attractor size is **independent of initial density**. Fluctuates between 45–57% of N regardless of starting point. Attractor size is a property of W, not of initial state.

**B2 — traza_inferencia effect:**

`traza_inferencia` active at start → +2.3 nodes on average. The only core node has an amplitude drag effect.

---

## P1: Macroscopic Hysteresis Loop

**Protocol:**
- UP branch: add nodes one by one (random order), measure c(S) at each step
- DOWN branch: remove nodes one by one (random order), measure c(S) at each step
- 200 sequences per branch
- Wilcoxon test on zone ρ ∈ [0.35, 0.70]

**Results:**

| N | Loop area | Max Δc(S) at ρ | p-value |
|---|-----------|----------------|---------|
| 16 | 0.0156 | — | confirmed |
| 32 | 0.000862 | 0.001308 at ρ=0.469 | p≈0 |
| 64 | 0.000367 | at ρ=0.547 | p≈0 |

**Interpretation:** the system remembers the path. A graph reaching ρ=0.5 by addition is not the same as one reaching ρ=0.5 by removal, even at identical density. P1 is scale-invariant.

---

## P2: Cascade Distribution P(s) ∝ s^-τ

**Protocol:** k-core cascade measurement. Remove one core node, count how many nodes cascade out. Repeat 300–500 times across weight thresholds θ.

**MLE estimator for power law:**
```python
tau_mle = 1 + n / sum(log(s_i / (s_min - 0.5)))
```

**Results:**

| N | k | θ range | τ range | Status |
|---|---|---------|---------|--------|
| 16 | 2 | — | 2.712 | Not confirmed (bimodal regime) |
| 32 | 2 | 0.002–0.010 | [1.53, 1.98] | **Confirmed — extended zone** |
| 32 | 3 | 0.005 | 1.76 | **Confirmed** |
| 64 | 2 | 0.005, 0.015 | 1.775, 1.721 | **Confirmed** |

**Key finding:** not a single critical point but an extended critical zone. The same θ range shows all three signatures simultaneously: k-core contraction, power law in cascades, and temporal asymmetry (P3).

---

## P3: Temporal Asymmetry of Relaxation

**Protocol:** measure relaxation steps after removal vs after addition at same θ/k. Mann-Whitney U test.

**Results:**

| N | θ | rem_mean | add_mean | asymmetry | p-value |
|---|---|---------|---------|-----------|---------|
| 32 | 0.005 | 2.283 | 2.000 | 0.066 | p<0.0001 |
| 64 | 0.005 | 2.153 | 2.000 | 0.037 | p≈0 |

**Key finding:** asymmetry exists only in the critical zone. At θ=0.001 and θ=0.007: asymmetry=0. P3 is a signature of the transition, not a property of the full graph.

---

## P4: Interior Optimal Density Ω*

**Protocol:** sample c(S) at 30 density levels ρ ∈ [0.05, 1.0], 300 random subsets each.

**Results:**

| N | W type | ρ* | Interior | W_mixta > W_base in [0.5,0.8] |
|---|--------|-----|---------|-------------------------------|
| 32 | W_mixta | 0.5–0.8 | Yes | Yes |
| 64 | W_base | 1.0 | No | — |
| 64 | W_mixta | 0.509 | **Yes** | **No** — W_base wins |

**Interpretation:** P4 confirmed on W_ckm_corpus_v2 (N=32): Ω* interior exists, W_mixta 13× over W_base. At N=64, Ω* interior exists (ρ*≈0.509) but W_mixta advantage is diluted — 18 negative pairs in a 2016-pair graph. This is a k-core density problem, not a scale problem: peripheral nodes dilute the negative pair signal. Open: extend to other domains (fourforums topics, A2A).

---

## Experiment: Attractor Hierarchy (Scenarios 13, 15)

**Transit protocol (Scenario 13):** red_verificacion admitted as transit node enables evolution from Spurious #5 toward ATR_733. Without transit: 15/50 runs reach A∪B, mean score=0.561. With transit: 1/50 reach A∪B, mean score=0.710.

The verification network does not correct toward A∪B — it leads to the most cohesive state accessible from the current position.

**ATR_733 emergence (Scenario 15):**

| Attractor | Nodes | score_3D | Basin | Status |
|-----------|-------|----------|-------|--------|
| Spurious #5 | 7 | 0.613 | — | base |
| ATR_710 | 9 | 0.701 | 14.1% | via transit |
| ATR_733 | 11 | **0.734** | 13.5% | via W_enriched |
| A∪B in W_enriq | 16 | 0.728 | — | lower than ATR_733 |

ATR_733 = optimal attractor at N=16. 11 nodes, all direction=1.000, density=0.739. Superior to A∪B. Recovery=1.000 at 10% noise.

---

## Experiment: Temperature vs Tension (Scenario 14)

Scenario 9 finding (erraticity at tension=0.30, T=0.2) not reproduced with 40 runs. Corrected result:

| T | Productive% | Erratic% | Regime |
|---|-------------|----------|--------|
| 0.01 | 57% | 0% | productive |
| 0.05–0.30 | 20–50% | 0% | CKM working zone |
| 0.50 | 25% | 0% | fluctuating |
| 1.00 | 8% | 15% | first erraticity |

Tension activates productive attractors (threshold ≈ 0.10). Temperature controls stability (threshold ≈ 1.00). Orthogonal dimensions.

---

## Experiment: Scaling N (Scenario 16)

| N | α | Recovery | Active fraction core | α_c empirical |
|---|---|----------|---------------------|---------------|
| 16 | 0.125 | 1.000 | 62% | >0.25 |
| 32 | 0.062 | 1.000 | 56% | 0.281 |
| 64 | 0.047 | 1.000 | 56% | 0.250 |
| 128 | 0.047 | 1.000 | 53% | 0.164 |

Four key findings: (1) α_c converges to 0.138 at large N — R15 C4 correct. (2) Recovery=1.000 invariant across all N. (3) Active fraction ≈ 55% of N — density property, not node identity. (4) Negative weights scale quadratically — W_mixta mandatory at large N; W≥0 produces spurious saturation.

ATR_733 hypothesis revised: not the scale-invariant nucleus. The invariant is ~55% of N.

---

## Holonomy

The sequence of attractors does not trace a simple curve — it traces a curve on a curved manifold. Δ accumulates orientation along that curve. A near-full cycle leaves a residual rotation: **holonomy** — the measure of the manifold's curvature, not just the trajectory.

- N=32: 88 attractor varieties = 88 local curvature directions
- N=64: 462 varieties

This is the mathematical structure underlying the "frequency of consciousness sparks" — not a scalar or simple spiral, but a distribution over an attractor space with geometry.

---

## Reproducibility

All experiments reproducible with:
```python
numpy.random.seed(42)
```

Corpus file: `W_ckm_corpus_v2.json` (N=32, 5145 paragraphs, sha256: d12b2b…).  
Weight construction: `corpus_service.py` (CorpusService) or `CKMGraph.from_corpus()` (Path B: automatic via NodeExtractorService).  
Full experiment scripts: `experiments/exp_p1_histeresis.py` through `exp_n64_main.py`.
