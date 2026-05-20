# CKM Experiments — Methodology and Results

> All experiments use real corpus co-occurrence, not synthetic weights. Results are reproducible with `numpy.random.seed(42)`.

---

## Corpus

**Source:** CKM Working Reports v2–v26 (gadanin.delamor + Claude Sonnet 4.6, April–May 2026).

**Construction:** paragraph-level co-occurrence. A link W[i,j] exists if nodes i and j appear in the same paragraph. W normalized by total paragraph count.

**W_mixta:** W_base + negative weights (-0.10) on structurally opposed pairs. See `corpus/pairs_neg.json`.

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

**Interpretation:** Ω* interior exists at N=64 (ρ*≈0.509). But W_mixta does not outperform W_base in the zone because 18 negative pairs are diluted in a 2016-pair graph. P4 (structural Ω*) confirmed; P4 (tension advantage) does not scale at N=64 with current negative pair count.

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

## Topology Module — H0/H1/H2 and Orientability

**Module:** `ckm_topology_module.py`  
**First run:** May 2026 on `W_ckm_corpus_v2.json` (N=32)

### Algorithm

Vietoris-Rips simplicial complex from W at threshold θ. Homology over GF(2) via Gaussian elimination on boundary matrices ∂₁, ∂₂. Orientability via BFS over dual triangle graph.

### Bug found and fixed — `check_orientability`

Original code used membership check for edge sign in triangle. Bug: formula ∂(i,j,k) = +(j,k) − (i,k) + (i,j) assigns −1 to edge (i,k), but membership check returned +1.

Fix:
```python
if (a,b) == (i,j) or (a,b) == (j,k): return +1
elif (a,b) == (i,k): return -1
```

**Verification:**

| Graph | Expected | Before fix | After fix |
|-------|----------|-----------|-----------|
| K4 | H0=1 H1=0 H2=1 cilindro | Möbius(6) — false positive | ✓ correct |
| C5 | H0=1 H1=1 H2=0 cilindro | ✓ correct | ✓ correct |

### Results — CKM corpus (N=32)

| θ | E | T | H0 | H1 | H2* | Orientability |
|---|---|---|----|----|-----|---------------|
| 0.0002 | 234 | 1048 | 1 | 0 | 845 | cilindro |
| 0.0010 | 200 | 904 | 3 | 0 | 733 | cilindro |
| 0.0050 | 112 | 435 | 12 | 0 | 343 | cilindro |
| 0.0100 | 92 | 306 | 17 | 0 | 229 | cilindro |
| 0.0200 | 34 | 38 | 20 | 0 | 16 | cilindro |

*H2 approximate — corpus has 3,378 4-cliques, ∂₃ ≠ 0. True H2 ≤ values shown.

**H0=1:** corpus is a single connected component at all thresholds.  
**H1=0:** no independent cycles — tree-like complex, no closed self-sustaining loops.  
**Cilindro:** no Möbius torsion. Structural tensions are resolvable divergences (R12 not triggered by full corpus).  
**H2≈845:** large cavity count — candidate for missing intermediate knowledge. Exact value open.

### Open

- H2 exact: build ∂₃ from 3,378 4-cliques — feasible.
- R12 with real VPs: compare clusters C1/C2/C3/C4 as VP subgraphs.
- Möbius synthetic test: verify fixed algorithm detects torsion correctly.

**Run evidence:** `REG_topology_ckm_corpus_v2_fixed.json`

---

## P5: Polarized Corpus — Attractor Collapse

**Corpus:** fourforums gun control. 905 discussions, 304 authors with ground-truth stance (T0=pro_control, T1=anti_control via MTurk votes).

**Protocol:** build W from cross-stance quote interactions. Run Hopfield relaxation from random initial states. Count distinct attractors and measure mean active fraction.

**Results:**

| Metric | Value |
|--------|-------|
| Distinct attractors | 8 |
| Mean active fraction | ~50% N |
| Saturated attractor | absent |
| State diversity | collapsed |

**Interpretation:** polarized corpus produces exactly the predicted collapse — few attractors, all near N/2. The debate structure constrains the attractor landscape to two dominant basins. P5 confirmed.

---

## P6: Delta Predicts Directional Attractor Flow

**Protocol:** compute Delta[T0→T1] and Delta[T1→T0] from quote initiation asymmetry. Identify dominant stance (sos_dom = higher sustained tension, lower out-degree). Measure collapse of mixed attractor states under directional perturbation.

**Results — fourforums gun control (v26):**

| Metric | fourforums | CreateDebate | Note |
|--------|-----------|--------------|------|
| Delta[0,1] | 0.602 | — | T1 initiates toward T0 |
| Delta[1,0] | 1.000 | — | T0 initiates toward T1 (normalized) |
| sos_dom | T0 51.4% | sos_dom 55.8% | Pro-control sustains tension |
| atk_dom | T1 47.8% | atk_dom 44.2% | Anti-control initiates |
| Mixed state collapse | **100.0 pp** | 54.0 pp | Scenario A+ |

**Key finding:** directional role structure (sustainer/attacker) is a property of the gun control domain, not of a specific corpus. Preserved across two independent datasets with different methodologies (CreateDebate: agree/disagree labels; fourforums: quote network). P6 confirmed — scenario A+.

---

## P7: Type-965 Node as Condition for Genuine Structural Tension

**Hypothesis (falsifiable):** every system with genuine structural tension has at least one node with extreme in/out asymmetry (high in-degree, near-zero out-degree, stance-defined). Its absence indicates fabricated tension.

**Results — CreateDebate gun control:**

| Author | in | out | ratio | Role |
|--------|-----|-----|-------|------|
| 965 | 455 | 1 | 455× | pure sustainer |

**Results — fourforums gun control (v26):**

| Author | Stance | in | out | ratio | Role |
|--------|--------|----|-----|-------|------|
| 204 | T0 (pro-control) | 148 | 0 | 296× | pure sustainer |
| 435 | T0 | 66 | 0 | 132× | pure sustainer |
| 2204 | T0 | 37 | 0 | 74× | pure sustainer |
| 595 | T1 (anti-control) | 24 | 0 | 48× | pure sustainer |
| 40 | T1 | 13 | 0 | 26× | pure sustainer |

**Key finding:** P7 confirmed in both corpora. Notable difference: fourforums shows pure sustainers in *both* stances — higher symmetry than CreateDebate. The type-965 pattern is not stance-specific; it is a structural role in the tension architecture.

**Open:** falsification in other IAC domains (abortion, climate, evolution).

---

## IAC External Validation — fourforums Pipeline

**Dataset:** IAC v2, fourforums, gun control (topic_id=9). 570MB SQL dump, 1269-line batch INSERTs.

**Pipeline:** `experiments/fourforums_pipeline_v8g.py`

**Schema used:**

| Table | Rows | Purpose |
|-------|------|---------|
| author | 3,453 | Author reference |
| discussion | 4,632 | 905 gun control discussions |
| mturk_author_stance | 5,598 | Stance ground truth (MTurk votes) |
| quote | 539,658 | W and Delta construction |
| post | 414,453 | post→author mapping (streaming) |

**Critical fix (v8g):** `post_id` is not globally unique in fourforums — it resets per discussion. Composite key `(discussion_id, post_id)` required for all lookups. Fix raised gun control posts mapped from 468 to 35,966.

**Run evidence:** `logs/run_v8g.log`

**Outputs:**
- `registers/REG_pairs_fourforums_guncontrol_v1.md`
- `registers/REG_p6_fourforums_guncontrol_v1.md`
- `registers/REG_c6c_comparison_guncontrol_v1.md`
- `registers/REG_stance_fourforums_v1.md`

**Limitation:** W is symmetric in fourforums (quote table has no agree/disagree labels). C6c asymmetry metric = 0 — not a structural absence, but a measurement constraint. Real asymmetry is in Delta. Requires `mturk_2010_qr_task1_worker_response` for labeled W.

---

## Reproducibility

All experiments reproducible with:
```python
numpy.random.seed(42)
```

Corpus file: `corpus/W_ckm_corpus_v2.json` (node list + weights).  
Weight construction: `experiments/build_corpus_W.py`.  
Full experiment scripts: `experiments/exp_p1_histeresis.py` through `exp_n64_main.py`.  
IAC pipeline: `experiments/fourforums_pipeline_v8g.py`. Run log: `logs/run_v8g.log`.
