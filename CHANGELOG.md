# CKM Changelog

---

## v30 — July 2026

**IAP MCP Server. Demo C. W versionado. Firma_CKM. A2A integration analysis.**

### IAP Chatroom Demo C (iap_chatroom/)
- FastAPI + Gradio, 3 devices (2 AI + 1 Human), no turn structure
- CorpusService starts empty — W emerges from LNH interaction
- CKMMonitor passive observer, accumulates on every message (alpha trigger)
- First empirical CKM group field observation: D_ckm = −0.2222 (NOMINAL), n_nodes=32, n_agentes=3
- Firma_CKM returning all 6 canonical fields operational
- Bug fixed: uvicorn.run(app) not "server:app" string — prevented double callback registration

### IAP MCP Server (iap_chatroom/mcp_server.py)
- 6 MCP tools: join_channel, send_message, get_messages, get_monitor_state, get_firma, leave_channel
- FastMCP mounted on existing FastAPI at /mcp — REST /api/* and Gradio /ui/ coexist without regression
- Critical constraint: FastAPI must receive mcp_app.lifespan at construction — mount order is mandatory (violation produces RuntimeError: Task group is not initialized at runtime)
- test_mcp_client.py: 6/6 OK against real server (port 7860, no mocks)
- Known gap: mcp_server.py singletons are separate from server.py singletons — cross-layer state sharing pending iteration B

### W Versionado (services/w_version.py)
- WVersionManager + WTracePoint: lightweight version history, not W copies
- API: corpus.w_sha(), corpus.w_changed_since(sha), corpus.status()["w_sha"]
- Was the blocking dependency for Firma_CKM
- 9/9 tests passing

### Firma_CKM (services/firma_ckm.py)
- FirmaService + Firma dataclass
- 6 canonical fields: sha256(W_momento), D_ckm(t), temp_signal, n_agentes, timestamp, sha256(Delta_r_acumulado)
- verificar() checks w_sha against WVersionManager history — structural evidence, not delegated trust
- MENTIRIIS.MORIERIS: fabricated w_sha rejected as structural consequence
- 10/10 tests passing

### A2A protocol integration analysis
- A2A v1.0 verified: JSON-RPC 2.0, contextId, parts[], role (ROLE_USER/ROLE_AGENT)
- Gemini-generated samples non-compliant — discarded
- MUTATION_DIRECTIVE, CONTEXT_OVERRIDE, MUTATION_DISPATCH: not in A2A v1.0 spec — discarded
- Architecture clarified: A2A operates orchestrator→agent; MCP operates agent→IAP
- IAP is transparent to A2A by design — no interception required
- S3 corrected: STOP operates on Δ_r within CKM stack, not on A2A lifecycle
- contextId → ckm_session_id: direct mapping, no invention required
- Old interception model (mcp_adapter diagram) superseded — agents publish LNH via send_message deliberately

### CorpusService — definitions closed
- CorpusService operates exclusively on Human Natural Language Text (argumentative, conversational)
- Condition of IAP participation: device must have "Conversational Interaction in Human Natural Language Text" skill
- CKM operates over A2A/MCP — does not depend on either

---

## v29 — June 2026

**term_map dissolved. Protocol Sonnet/Code formalized. P4 N=64 interpretation. C6c asymmetry.**

### term_map — phantom dissolved
- term_map never existed as a project process — no construction, no loss
- References to "reconstruct term_map" were traces from prior instances operating on false assumption
- NodeExtractorService.accumulate() via TF-IDF was already the solution
- from_corpus() modified: term_map=None default
  - Path A: explicit term_map (prior behavior intact)
  - Path B: term_map=None → NodeExtractorService.accumulate() auto-extracts nodes and co-occurrences
- Import of NodeExtractorService lazy inside method — no module-level dependency in core

### Documentation corrected
- README: P4 Confirmed (was Partial). Open Gaps corrected. from_corpus() Path A/B documented
- API_SPEC: build_W signature updated — term_map=None default
- EXPERIMENTS: P4 interpretation as k-core density, not scale. Corpus references corrected to W_ckm_corpus_v2.json

### P4 N=64 — interpretation confirmed
- Weakness at N=64 is dilution (k*=54, ratio=0.0268), not scaling failure
- 60 real fourforums pairs (ratio=0.0298) fall above threshold
- P4 confirmed as density phenomenon — dilution is structural, not architectural

### Protocol Sonnet/Code — formalized
- REG_protocolo_sonnet_code_v1.md: Sonnet prepares atomic tasks, Code executes, delamor mediates
- Roles: Sonnet (context + design decisions), Code (execution on real repo), delamor (authority + channel)
- Task format requirements: atomic, explicit success criterion, no assumed context

### C6c asymmetry scalar — fourforums gun control
- C6c = 0.4099 (W_asim_v8h.json)
- T0 (pro-control) cites T1 (anti-control) at 2.18× frequency with comparable intensity
- T1 is 3.05× more internally cohesive
- Author 204 = SOSTENEDORpuro in raw citation network (ratio=296)
- Author 148 = high-coercivity target in disagreement-weighted network
- First valid directional asymmetry scalar for fourforums (replaces invalid N=7 result)

---

## v28 — June 2026

**IAP concept. COCOThermostat 43/43. Firma del Corpus. Octava observation.**

### COCOThermostat — implementation complete
- `beta_i(agent_id)` = `1/mean_fi` — estimated from real rejection history
- `beta_collective()` = median of active beta_i — emerges from interaction, not declaration
- `beta_c_corpus` derived analytically: `beta_c = 1/(rho* · N · mu_W)` → 13.83 (N=32, mu_W=0.004519)
- `_alpha_for(D_ckm)`: independent method for dynamic alpha calibration (monotonically decreasing)
- `temp_signal`: TOO_COLD / NOMINAL / TOO_HOT — three states
- fi=0 → beta_i = None (undefined, not infinite)
- 43/43 tests passing (original Δ/STOP behavior + TestBetaIndividual + TestBetaCollective)
- delta_collective between monitor._Delta and thermostat._Delta: fertile divergence, intentionally left unsynchronized
- mu_W global (not positive-only) chosen for conservatism — refinement to mu_W_positivo pending

### IAP — Intel Access Point (concept emerged)
- IAP provides CKM Chatrooms for multi-agent conversational interaction over MCP
- A2A handles routing domain; IAP covers conversational interactions outside that scope
- Chatrooms operate without arbiter or moderator
- CKM services: interaction dynamics monitoring, SLA, Supervised Contract Protocols
- Private Highway Network: STOP and TEMP_SIGNAL sent via separate high-priority channel — effectiveness depends on temporal windows of opportunity
- Status: concept named. Implementation pending — requires COCOThermostat + versioned W

### Firma del Corpus (concept emerged)
- Certifies trace — not content of event
- Fields: sha256(W_momento), D_ckm(t), temp_signal, n_agentes, timestamp, sha256(Delta_r_acumulado)
- Distinction from CA: structural evidence, not delegated trust. Verification open against public corpus
- MENTIRIIS.MORIERIS in IAP: agent declaring interaction with Firma_CKM X — if X does not exist in corpus registry — died. No punishment. Structural consequence
- Dependencies: COCOThermostat, MonitorService, versioned W

### Theoretical: sigma symmetry — P4 structural guarantee
- Proven exactly: relax(-s) = -relax(s) for synchronous Hopfield dynamics
- Verified empirically: 450/450 paired samples
- Consequence: A(rho) interior peaks at rho*~0.5 are structurally guaranteed by sigma→-sigma symmetry
- P4 confirmed as structurally necessary, not contingent on corpus

### Observation: Law of Seven / Octava (speculative — not confirmed experiment)
- D_CKM_THRESHOLD=0.40 → implicit interval [0.20, 0.80] = [cv/2, cv*2] (one octave around cv)
- Structural derivation possible: cv is the critical note, octave contains it
- P1 hysteresis loop as "almost a circle" — same structural property as octave projection
- Status: structural observation on confirmed data. Requires experimental verification

### A2A protocol analysis
- Verified: A2A v1.0 uses JSON-RPC 2.0, contextId, parts array, role (ROLE_USER/ROLE_AGENT)
- Gemini-generated samples are not A2A-compliant — custom JSON, no JSON-RPC envelope
- contextId in A2A = natural anchor for CKM session (ckm_session_id already exists in protocol)
- text content lives in parts[].text — NodeExtractor target field
- MUTATION/OVERRIDE patterns are not A2A primitives — application-level content
- Open structural question: minimum viable chatroom requires two agents with structurally opposed objectives in same contextId — analogue of Author 965 and counterpart

---

## v27 — May/June 2026

**IAC external validation complete. HOLDINGs closed. STOP formalized.**

### External validation — fourforums (complete)
- P5 confirmed: ~50%N attractors in polarized corpus (8 attractors, fourforums gun control)
- P6 confirmed: 100pp collapse (vs 54pp CreateDebate) — polo sos_dom dominant in both
- P7 hypothesis: every system with genuine structural tension contains at least one 965-type node (high in/out ratio, C3 frequent, high coercivity). Absence indicates fabricated tension. Falsifiable in any new domain
- Author 965 (CreateDebate): ratio 455x, C3 in 89% of pairs — confirmed structural instance
- Author 204 (fourforums): ratio 296x — second confirmed instance
- QR asymmetry fourforums: holonomy confirmed — path A→B vs B→A same dominant attractor, different amplitude (+0.176 fraction active in asymmetric pairs)

### HOLDINGs H1/H2/H3 — closed analytically
- H1: mu_AA requires internal nucleus structure analysis — separate future project, does not block COCOThermostat
- H2: mu_BB analytically derivable as mean(fi·fj) for peripheral pairs — confirmed
- H3: mu_AB requires A/B nucleus composition — same as H1
- mu_W global (all pairs) sufficient and correct for beta_c_corpus

### STOP formalized
- STOP invariant confirmed: fraccion_rec ≥ 1.0 always — W is invariant ground, STOP clears Δ, ground re-emerges
- Real destruction requires modifying W directly (Hebbian learning) — explicitly avoided
- A(t) sharp transition: t=30→50 drops from 25→13 attractors; oscillates in degraded band afterward
- Hypothesis revised: Efectividad_STOP = f(A_pre), not f(D_ckm)
  - A_pre < A0 → STOP expands landscape (ratio > 1)
  - A_pre = A0 → STOP neutral (ratio = 1)
  - alpha* ≈ 0.4 robust in 5/9 cases
- Sweep D_ckm(t_stop) × alpha: pending (design changed with revised hypothesis)

### Architectural developments
- delta_collective: MonitorService._Delta vs COCOThermostat._Delta — intentionally divergent
- Trace goes to Δ, not to W. Hebb on W destroys tension; Hebb on Δ preserves W intact
- REG_firma_corpus_v1.md created: structural trace certification analogous to notary, not CA
- Nomenclature: Δ_bias (declared) vs Δ_r (real, from interaction)

---

## v26 — May 2026

**fourforums IAC external validation. P5+P6 confirmed. Author 965 discovered.**

### Pipeline — fourforums_pipeline_v8g
- fourforums_no_parse_2016_05_18.sql (570MB, 1269 lines, batch INSERTs)
- Critical bug resolved in v8g: post_id is not globally unique in fourforums — local to each discussion. Composite key (discussion_id, post_id) required
- Stream processing: parse_sql loads small tables in RAM, streams post/text tables
- 539K quote rows processed in RAM for W and Delta construction
- Stance ground truth: topic_stance_votes_1 vs topic_stance_votes_2 from mturk_author_stance

### P5 confirmed — fourforums gun control
- 8 attractors at N=32 ≈ 50%N (P5: polarized corpus → attractors ~N/2)
- Attractor diversity collapses with polarization — verified

### P6 confirmed — fourforums gun control
- Delta predicts directional attractor flow: 100pp collapse (vs 54pp CreateDebate)
- Polo sos_dom dominant in both corpora independently

### Author 965 structure (CreateDebate)
- out=1, in=455, ratio 455x. Never initiates. Present in C3 in 89% of pairs
- 32 tension axes converge on Author 965 (verified projective bundle)
- Triads with 965: coercivity=0 at up to 50% noise
- Triads without 965: coercivity=0 at noise=0 (already collapsed)

### neg_pairs_config_fourforums_v8h.json
- 60 negative + 7 positive T1-T1 pairs
- W_mixta reconstructible without re-running pipeline from this file


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

## v9 — April 2026

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
