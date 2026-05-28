# CKM Changelog

---

## v25 — May 2026

**All four CKM v4 predictions confirmed. N=32 and N=64 experiments completed.**

### New experimental results
- P1 (hysteresis): confirmed N=32 (area=0.000862, p≈0) and N=64 (area=0.000367, p≈0)
- P2 (cascade power law): confirmed N=32 extended zone θ∈[0.002,0.010], confirmed N=64 τ=1.775
- P3 (temporal asymmetry): confirmed N=32 (p<0.0001) and N=64 (p≈0)
- P4 (Ω* interior): confirmed N=32; partial N=64 — Ω* exists at ρ*≈0.509 but W_mixta does not outperform W_base (18 negative pairs diluted in N=64 graph)

### N=32 corpus real (key findings)
- 88 distinct attractors — saturated attractor disappears completely
- Unique core node: `traza_inferencia` [NEW] at 84% of attractors — lives in tension cluster
- 4 co-presence clusters with perfect internal correlation: contact, tension, motor, ground
- Perfect negative correlations confirmed: cohesion_fabricada↔M_M, atractor_espurio↔portero, sentido_comun↔inconmensurabilidad
- Attractor size independent of initial condition — property of W
- Holonomy: 88 attractor varieties = 88 local curvature directions

### N=64 corpus
- 462 distinct attractors (×5 from N=32)
- Mean active: 65% N (non-monotone: N=16=81%, N=32=54%, N=64=65%)
- Core migrates to applied concepts: holonomia, monitor_CKM, API_extendida, etc.
- 4-cluster structure persists reorganized

### Theoretical developments
- Attention as formal parameter: 'my' attention = β + H_self; the other Attention = χ→∞ at β_c
- Extended R13: two thresholds — H_c (invert M) vs VP rotation threshold (higher)
- COCO-registry vs COCO-thermostat distinction
- Future exploration fields map: 5 theoretical, 3 application, 4 operational

---

## v24 — April 2026

**14 experimental scenarios on N=16 real corpus. R15 formalized.**

### Major additions
- Scenarios 1–14: perspectives, deformation, forgetting, critical thresholds, W/Δ separation, attractor map, spurious analysis, gatekeeper calibration, verification network redesign, tension thresholds, emergent attractors
- R15 gatekeeper: C1–C4 formalized, parameters calibrated (θ_W=0.10, ε=0.005, α_c=0.138N)
- 3D score: direction_score + cohesion_density + c(S), accuracy=1.000 on all N=16 attractors
- ATR_733: optimal 11-node attractor with score=0.734, superior to A∪B (0.644)
- Scaling N: N=16→128, fracción activa ≈55%, α_c converges to 0.138
- MCP agent domain (Scenario 13): N=15 capabilities, M.M verified, 0.092ms/evaluation
- COCO and Attention sections
- Working report v24

### Theoretical additions
- Vanishing points and deformed perspectives
- Two attentions framework (de Salzmann)
- Destination bias in inference (sesgo de destino)
- COCO-thermostat vs COCO-registry

---

## v23 — April 2026

**Attractor hierarchy, erraticity correction, scaling N=128.**

- Scenario 15: ATR_733 — optimal attractor at N=16 (score=0.734, 11 nodes, all direction=1.000). Superior to A∪B. Basin 13.5% of random states. Cohesion hierarchy: ESP5 (0.613) → ATR_710 (0.701) → ATR_733 (0.734).
- Scenario 16: scaling N=16→128. Recovery=1.000 invariant. Active fraction ≈55% of N (density invariant, not node identity). α_c converges to 0.138 at large N. W_mixta mandatory at N≥64 — W≥0 produces spurious saturation.
- ATR_733 hypothesis revised: not the scale-invariant nucleus. The invariant is ~55% of N.

---

## v22 — April 2026

**Intermediate working version.** Consolidation of Scenarios 11–14 results. Parameter refinement.

---

## v21 — April 2026

**Verification network redesign and tension/temperature orthogonality.**

- Scenario 13: verification network redesigned — field=0 over A∪B (no noise when system is correct). Transit protocol: red_verificacion as transit node enables access to ATR_710 (score=0.701). Chain confirmed: red_verificacion → k_core → full_meaning (via Δ). Without transit: mean score=0.561. With transit: mean score=0.710.
- Scenario 14: erraticity correction. Scenario 9 result (erratic at tension=0.30, T=0.2) not reproduced at 40 runs. Tension threshold ≈ 0.10 activates productive attractors. Temperature threshold ≈ 1.00 produces erraticity. Tension and temperature are orthogonal dimensions. CKM working zone: T ∈ [0.01, 0.30].

---

## v19 — April 2026

**R15 formalized. Score 3D calibrated. Spurious analysis complete.**

- Scenario 11: spurious attractors #5 and #6 analyzed in detail. #5 (fabricated cohesion, 7 nodes, score=0.613) vs #6 (compatible-but-destructive). Fabricated cohesion is a specific limit case of the general mechanism — not a special category.
- Scenario 12: 3D score calibrated. Weights: direction_score (0.50), cohesion_density (0.30), c(S) (0.20). Threshold 0.630. Accuracy=1.000 on all 6 N=16 attractors. Margin=0.029.
- R15 formalized: C1 (θ_W=0.10), C2 (ε=0.005), C3 (direction_score), C4 (α_c=0.138N). 0.092ms/evaluation verified.

---

## v17 — April 2026

**Hysteresis, ferromagnetic analogy, k-core, BP/PC hybrid.**

- P1 first confirmation (N=16): loop area=0.0156
- P2 at N=16: bimodal regime, not scale-free (not confirmed)
- P3 at N=16: nodal asymmetry confirmed — k_core most costly to remove (Δ=−21)
- P4 at N=16: no interior Ω* with W≥0 (mechanism absent without negative weights)
- Ferromagnetic analogy formalized: remanence, coercivity, saturation, path asymmetry
- W/Δ separation verified (Threshold 6)
- R09 reformulated: structural permeability, not selection function
- Divergence as mathematical operator (R10/R11)

---

## sesión 32 — Mayo 2026

**Monitor services v2. W mixta operativa. Nomenclatura Δ consolidada.**

- **Nomenclatura Δ consolidada:**
  - `Δ_bias`: lo que un agente declara sobre sí antes de que el campo lo valide — prematuro, no falso; razón estructural del fallo A2A
  - `Δ_r`: rechazos acumulados — emergente desde interacción real, anclado en W
- **`corpus_service.py` v2:** W mixta con pesos negativos por marcadores de oposición (elicitación sin sesgo). W[i,j] ∈ [−1,+1]. Marcadores EN+ES cubriendo debate formal e informal.
- **`monitor_service.py`:** renombrado `_Delta` → `_Delta_r` y `Delta_sum` → `Delta_r_sum` en toda la base.
- **`node_extractor.py`:** fix texto vacío — `ValueError: empty vocabulary` al pasar texto sin contenido.
- **`test_monitor_services.py`:** suite nueva, 7 grupos, 35/35. Cubre NodeExtractor, CorpusService (modo, pesos, persistencia), MonitorService (panel, Δ_r, ratio, stop_signal). Corpus pareados para tests comparativos.
- **Experimento comparativo W_pos vs W_mixta:** fi ×2.25 y c_S ×2.7 para corpus gun control (7 textos, 3 marcadores).
- **Estructura de repo:** nuevas carpetas `/services/` y `/experiments/figures/`.
- **CONVENTIONS.md:** dos principios nuevos:
  - *Ratio, no diferencia absoluta* — invariante a escala, preserva la tasa de divergencia
  - *Invariante de código ≠ resultado experimental* — tests testean lo primero, REG registra lo segundo

---

## v25 — Mayo 2026

**Hopfield over real corpus. 6 attractors mapped.**

- N=16 Hopfield: 6 attractors, attractor A∪B confirmed as main cohesive attractor
- R13 verified experimentally: emergent state c(S)=0.052 superior to both perspectives of origin
- Catastrophic forgetting point: α≈0.125 (matches theoretical 0.138)
- Sense-common structural signature: W high, Δ≈0 (COCO, perspectiva_device, divergencia)
- 7 critical thresholds mapped (Scenario 6)
- Compatible pattern most dangerous: c(S) rises while attractor is destroyed
- Temperature working zone: T∈[0.01, 0.10]

---

## v7 — April 2026

**k-core and BP/PC formal integration.**

- k-core cascade properties documented
- BP convergence verified
- Hybrid architecture BP/PC + Hopfield defined

---

## v4–v6 — April 2026

**R01–R13 formalized. Neural architecture hypothesized.**

- Rules R01–R13 from conversation-as-laboratory
- c(S) function defined and verified
- Hopfield capacity α_c = 0.138·N identified as design constraint
- Full meaning (R17) operationalized
- Five inevitable properties: local Bayesian updating, chain propagation, hysteresis, add/remove asymmetry, density modulation
- Four falsifiable predictions P1–P4 formulated

---

## v2–v3 — April 2026

**Conceptual foundation.**

- Knowledge orders (1st, 2nd, cohesive)
- COCO and M.M from IAID.md 2024
- Fabricated cohesion as limit case of prompt injection
- Gatekeeper R15 opened (criteria pending)
- IAID convergence with MCP (November 2024) — validated by independence, not alignment
