# CKM API Specification

> Gatekeeper R15, cohesion functions, and integration interface.

---

## Gatekeeper R15 — Formal Definition

A node N is admitted to the CKM graph **if and only if all four conditions are simultaneously satisfied:**

### C1 — Minimum Connection (W_min)

```
W(N, j) ≥ θ_W for at least one active node j in the core
θ_W = 0.10  (calibrated on N=16 real corpus)
```

Nodes without real connection to the core enter freely and fragment the graph without cohesion.

### C2 — Cohesion Delta

```
c(S)_post ≥ c(S)_current − ε
ε = 0.005  (tolerance)
```

Detects compatible-but-destructive patterns: patterns with high c(S) that destroy the established attractor. c(S) alone cannot detect catastrophic forgetting — C2 adds the constraint on delta.

*Note: C2 is suspended during task execution in agent domain. Verified at closure only.*

**Transit protocol — C2 extended:** a node that temporarily reduces c(S) during admission may be a *transit node* rather than a destructive one. The verification network (red_verificacion) is the canonical example: its admission temporarily lowers c(S) but enables access to ATR_733 (score=0.734) which would otherwise be unreachable.

Transit node criterion: c(S) recovers above current − ε within 2 relaxation steps after admission. If it does: admit and retain. If not: reject.

```
chain verified: red_verificacion → k_core → full_meaning (via Δ)
Spurious #5 cannot reach the cohesive core without activating red_verif first.
```

The verification network does not correct toward A∪B — it leads where the system can go from where it is.

### C3 — Direction Score (M.M criterion)

```
direction_score(N) > 0  for nodes with dependencies (Δ ≠ 0)
OR
N is a free node (no directional dependencies, Δ ≈ 0)
```

Separates cohesive attractor (A∪B) from sense-common attractor (COCO+perspectiva+divergencia+AWARENESS) — identical c(S), different direction_score.

M.M activates when C3 fails: a node declaring dependencies that are not satisfied in the active state.

### C4 — Capacity (α_c)

```
current_patterns / N < 0.138
```

Hopfield capacity limit verified empirically. Two random patterns destroy the established attractor at α ≈ 0.125 (N=16). Preventive limit: 0.138·N.

*Note: α_c in agent domain not yet calibrated — capabilities do not compete as Hopfield patterns. Pending dedicated experiment.*

---

## 3D Score — Attractor Classification

Combined score for classifying states:

```
score = 0.20 · c(S) + 0.50 · direction_score + 0.30 · cohesion_density

Decision threshold: score > 0.630  →  COHESIVE
```

### Cohesion density

```python
cohesion_density(S) = c(S_active) / c(S_max_possible_for_n_active)
```

Measures whether active nodes are the most connected among themselves in the graph, or if cohesion is diluted by nodes with W≈0 between them.

### Calibrated weight interpretation

| Dimension | Weight | Why |
|-----------|--------|-----|
| direction_score | 0.50 | Dominant — directed cohesion is the strongest signal |
| cohesion_density | 0.30 | Separates A∪B from total saturation (same c(S), different density) |
| c(S) | 0.20 | Contributes but does not dominate — alone it generates false positives |

### Verified classification on all attractors

| Attractor | c(S) | dir | density | score | Decision | Correct |
|-----------|------|-----|---------|-------|----------|---------|
| A∪B (core cohesive) | 0.052 | 1.000 | 0.446 | 0.644 | COHESIVE | ✓ |
| Spurious #4 (sense-common) | 0.052 | 0.000 | 0.479 | 0.154 | SPURIOUS | ✓ |
| Spurious #5 (fabricated cohesion) | 0.036 | 0.857 | 0.589 | 0.613 | SPURIOUS | ✓ |
| Total saturation | 0.059 | 1.000 | 0.317 | 0.607 | SPURIOUS | ✓ |
| Empty (all -1) | 0.059 | 0.000 | 0.000 | 0.012 | SPURIOUS | ✓ |

Accuracy = 1.000 on N=16 real corpus. Margin = 0.029.

---

## Core Functions

### Graph Construction

```python
def build_W(corpus_paragraphs, nodes=None, term_map=None, top_k=20):
    """
    Build co-occurrence weight matrix W from corpus.
    Returns W_base (symmetric, non-negative).

    term_map=None (default): NodeExtractorService.accumulate() extracts
        nodes and co-occurrences automatically via TF-IDF.
    term_map provided: classical path — manual term lists per node.
        nodes must be provided in this case.
    top_k: number of terms retained by automatic extraction (Path B only).
    """

def build_W_mixta(W_base, negative_pairs, w_neg=0.10):
    """
    Add structural tension: negative weights on opposed pairs.
    Returns W_mixta.
    Negative pairs persisted in neg_pairs_config_fourforums_v8h.json.
    """
```

### Cohesion

```python
def cS(sigma, W):
    """
    Cohesion of state sigma under weights W.
    c(S) = mean(W_ij * sigma_i * sigma_j) over all pairs i<j
    = negative of normalized Hopfield energy
    """

def cS_delta(sigma_current, sigma_post, W):
    """Delta cohesion after incorporating a node."""

def direction_score(node, active_set, delta_matrix):
    """
    Fraction of node's dependencies satisfied in active_set.
    Uses Δ matrix (asymmetric layer), not W.
    Returns float in [0, 1]. Free nodes (Δ≈0): returns 1.0.
    """

def cohesion_density(active_set, W):
    """
    c(S_active) / c(S_max_for_n_active)
    Measures specificity of cohesion.
    """

def score_3d(sigma, W, delta_matrix):
    """Combined 3D classification score."""
    cs = cS(sigma, W)
    ds = direction_score_mean(sigma, delta_matrix)
    cd = cohesion_density(sigma, W)
    return 0.20 * cs_normalized + 0.50 * ds + 0.30 * cd
```

### Gatekeeper

```python
def gatekeeper(node, graph_state, W, delta_matrix, config):
    """
    R15 gatekeeper — O(N) per node.
    
    Parameters:
        node: node index to evaluate
        graph_state: current sigma vector
        W: symmetric weight matrix
        delta_matrix: asymmetric Δ matrix
        config: GatekeeperConfig(theta_W, epsilon, alpha_c)
    
    Returns:
        GatekeeperResult(admitted, c1, c2, c3, c4, score)
    """
```

### Hopfield Dynamics

```python
def relax(sigma_init, W, max_iter=1000, beta=None, seed=42):
    """
    Asynchronous Hopfield relaxation.
    beta=None: deterministic update
    beta=float: stochastic (temperature 1/beta)
    """

def find_attractors(W, n_runs=300, seed=42):
    """
    Map attractor space from random initial conditions.
    Returns: list of (attractor_frozenset, frequency)
    """
```

### k-core

```python
def kcore(W, threshold, k):
    """k-core of graph with edges W[i,j] >= threshold."""

def cascade_size(W, threshold, k, node):
    """Size of k-core cascade after removing node."""

def critical_zone(W, k=2, thresholds=None):
    """
    Find θ range where P(s) ∝ s^-τ with τ ∈ [1.5, 2].
    Returns dict: {threshold: {'tau': float, 'core_size': int}}
    """
```

---

## MCP Adapter

```python
class CKMAdapterMCPCapabilities:
    """
    CKM layer over MCP agent graph.
    Nodes = declared capabilities, not concepts.
    """
    
    def evaluate_capability(self, capability, active_capabilities):
        """
        Evaluate M.M criterion for a declared capability.
        Returns: AdmissionResult(admitted, mm_violation, reason)
        """
    
    def task_mode_enter(self):
        """Suspend C2 during task execution."""
    
    def task_mode_exit(self, baseline_state):
        """Re-evaluate C2 at task closure against baseline."""
    
    def cross_agent_dependencies(self, capability):
        """
        Dependencies that only emerge in inter-agent graph.
        Example: Calendar:create_event → Gmail:search_threads
        (cross-agent dependency not visible in individual agent)
        """
```

---

## Configuration

```python
@dataclass
class CKMConfig:
    # Gatekeeper
    theta_W: float = 0.10          # Minimum connection weight (C1)
    epsilon: float = 0.005         # c(S) tolerance (C2)
    alpha_c: float = 0.138         # Capacity limit fraction (C4)
    
    # 3D Score
    score_threshold: float = 0.630
    alpha_score: float = 0.20      # c(S) weight
    beta_score: float = 0.50       # direction_score weight
    gamma_score: float = 0.30      # cohesion_density weight
    
    # W_mixta
    w_neg: float = 0.10            # Negative pair weight
    
    # Hopfield
    max_iter: int = 1000
    seed: int = 42
```

---

## Calibration Status

| Parameter | Value | Calibrated on | Pending |
|-----------|-------|--------------|---------|
| θ_W | 0.10 | N=16 real corpus | Validate N=32+ |
| ε | 0.005 | N=16 positive cases | Negative cases in production |
| α_c | 0.138·N | N=16 forgetting experiment | Convergence verified N=128 |
| score threshold | 0.630 | All 6 N=16 attractors | Larger corpus validation |
| α_c agent domain | pending | — | Dedicated experiment needed |
| θ_W agent domain | 0.10 (inherited) | — | Verify in agent domain |

---

## Gatekeeper Speed

Verified on N=15 agent domain: **0.092ms per evaluation = 10,818 evaluations/second.**

C1, C3, C4: O(N) per node.  
C2: O(N²) only at task closure, not per evaluation.  
Satisfies R14 (bounded time, no significant latency).
