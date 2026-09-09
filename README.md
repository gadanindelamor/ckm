# CKM — Cohesive Knowledge Model

**Status:** Research · v31 · Aug 2026  
**Author:** gadanin.delamor  
**License:** MIT

---

## What is CKM

CKM is a formal model for knowledge graph dynamics in multi-agent systems. Its core problem: how to evaluate whether new knowledge is genuinely interdependent with an existing knowledge body — not just semantically proximate, not just from a trusted source.

The model uses a Hopfield attractor architecture over a weighted knowledge graph, with a cohesion measure derived from ferromagnetic physics. It distinguishes three layers:

- **W** — symmetric co-occurrence weight matrix (N×N). Structural memory.
- **Δ** — asymmetric directional dependency matrix (N×N). Inference orientation.  
  Built from corpus (citation network, quote directionality). Static once built.  
  Not the same as Δ_r (MonitorService rejection accumulator — see Architecture).
- **c(S)** — cohesion measure = mean(W_ij · σ_i · σ_j) over all pairs i<j. Negative normalized Hopfield energy. Measures W/state alignment.

**W and Δ are kept strictly separate.** Mixing them destroys attractor recovery capacity (verified: recovery drops from 0.78 to 0.02).

| Matrix  | Source         | Role                                | Mutable |
|---------|----------------|-------------------------------------|---------|
| W_base  | corpus         | symmetric co-occurrence             | no      |
| W_mixta | W_base + config| W_base + structural negative pairs  | no      |
| Δ       | corpus         | asymmetric directional dependency   | no      |
| Δ_r     | MonitorService | rejection accumulator               | yes     |

**W — static vs. dynamic:** In validation experiments (P1–P7), W is a static snapshot built from a complete corpus dump. In live IAP operation, CorpusService reconstructs W continuously as new texts arrive; WVersionManager traces each reconstruction; Firma_CKM certifies each state. When W changes, a new COCO instance must be created — COCO's β_c is derived from the W it was initialized with. The snapshot is a frame in a streaming field, static by experimental design, not by architectural constraint.

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
  Knowledge graph (W_mixta)              ← W_base + structural negative pairs
        ↓
  Hopfield relaxation                    ← operates on W_mixta + Δ_r
                                            Δ_r: rejection accumulator, starts at zero,
                                            grows with each MonitorService.evaluate() call.
                                            Not the same as Δ (corpus-derived, static).
        ↓
  Continuous verification  ← recalibrates weights, chain propagation
```

---

## Repository Structure

```
ckm/                                 # Repo root
├── core.py                          # CKMGraph, CKMConfig, GatekeeperResult
├── analytics.py                     # copresence_matrix, cluster_nodes, P4 optimal_density
├── hopfield.py                      # relax, find_attractors, hysteresis_loop (P1)
├── kcore.py                         # kcore, cascade_distribution (P2), temporal_asymmetry (P3)
├── mcp_adapter.py                   # CKMAdapterMCPCapabilities — MCP capabilities layer
│
├── services/                        # Servicios CKM operativos (IAP runtime)
│   ├── corpus_service.py
│   ├── monitor_service.py
│   ├── coco.py                      # (renombrado de coco_thermostat.py)
│   ├── fabrication_service.py
│   ├── firma_ckm.py
│   ├── w_version.py
│   ├── node_extractor.py
│   ├── behavior_graph.py
│   ├── TERMAP_behavior_v1.json
│   └── W_ckm_corpus_v2.json
│
├── tests/                           # Tests de servicios
│   ├── test_coco.py                 # (renombrado de test_coco_thermostat.py)
│   ├── test_firma_ckm.py
│   ├── test_monitor_services.py
│   └── test_w_version.py
│
├── iap_chatroom/                    # Aplicación IAP Chatroom
│   ├── server.py
│   ├── api_routes.py
│   ├── mcp_server.py
│   ├── channel.py
│   ├── device_manager.py
│   ├── ckm_monitor.py               # Integra W + G
│   ├── autonomous_device.py
│   ├── agent_device_skin.py
│   ├── groq_research_agent.py
│   ├── ui_gradio.py
│   ├── groq_agent_config.json
│   ├── requirements.txt
│   ├── .env.example
│   ├── providers/                   # AnthropicProvider, GroqProvider, OpenAIProvider, GeminiProvider
│   ├── tests/                       # Casos 0.0–0.15 + TASKs
│   └── _state/                      # Runtime state (gitignored)
│
├── experiments/                     # Pipelines de validación externa
│   ├── fourforums_pipeline_v8g.py
│   ├── fourforums_pipeline_v8h.py
│   ├── build_W_base_N64.py
│   ├── calibrate_W_mixta.py
│   ├── neg_pairs_config_fourforums_v8h.json
│   └── figures/
│
├── process/                         # Estado experimental — backups por caso
│   ├── corpus_states/               # corpus_state.json.bak_* (Casos 0.4–0.14)
│   ├── monitor_trajectories/        # monitor_trajectory.jsonl.bak_*
│   └── experiments/                 # W_ckm_corpus_v2.json, REG JSON outputs
│
├── registers/                       # REGs — Clase R, no modificar
│   └── REG_*.md  (+ MAPA_REG_corpus_v*.md)
│
├── docs/                            # Informes de trabajo y figuras
│   ├── CKM_Informe_Trabajo_v30.md
│   ├── Informe_Sciamarella_CKM.md
│   └── figures/
│
├── readme/                          # Documentación operativa
│   ├── API_SPEC.md
│   ├── CONVENTIONS.md
│   ├── THEORY.md
│   ├── METODOLOGY.MD
│   ├── LETTER.md
│   └── EXPERIMENTS.md
│
├── logs/
├── pyproject.toml                   # numpy>=1.24, scipy>=1.11
├── CHANGELOG.md
├── LICENSE
├── .gitignore
└── README.md
```


## How to Run

### Prerequisites

```bash
pip install fastapi uvicorn gradio anthropic groq spacy
# Network access required for Groq and Anthropic API calls
```

### IAP Chatroom

```bash
cd iap_chatroom/
python server.py
# FastAPI at :7860/api/*
# Gradio UI at :7860/ui/
# MCP server at :7860/mcp
```

### MCP tools (6 available)

```
join_channel · send_message · get_messages
get_monitor_state · get_firma · leave_channel
```

Test: `python test_mcp_client.py` — expects 6/6 OK against live server.

### Corpus experiments (fourforums)

```bash
# Requires: fourforums_no_parse_2016_05_18.sql (570MB) in /data/
cd experiments/
python fourforums_pipeline_v8h.py --log
```

### Unit tests

```bash
python tests/test_coco.py             # 28/28
python tests/test_monitor_services.py # 35/35
python tests/test_firma_ckm.py        # 10/10
python tests/test_w_version.py        # 9/9

python services/coco.py               # T1-T13, suite propia del modulo
python services/monitor_service.py    # T1-T6
python services/corpus_service.py
```

COCO cuenta 41: 28 en `tests/test_coco.py` mas 13 (T1-T13) en el `__main__`
de `services/coco.py`. Se citan separados a proposito — son dos runners
distintos, y un escalar unico se congela sin decir cual de los dos se movio.
Verificado Sep 2026.

---

## Methodology Note

The methodology was not declared before it was used — it emerged inductively from what happened. That is itself a methodological characteristic, not an accident.

**Phenomenology as first step of engineering.** Conceptual clarity precedes formalization throughout. The Hopfield architecture and Ising-model thermodynamics were imported after identifying structural analogies — not as decorative references but because the physical models predict behaviors the conceptual domain actually exhibits.

**Conversation as laboratory.** The working reports (v2–v31) are not documentation of the process — they are the process. The term-map, co-occurrence matrices, and W construction are derived directly from the text of the conversation. The conversation is the corpus.

**Incompleteness preserved as information.** Gaps in the formal model (representation of cohesive knowledge, META KNOWLEDGE, COCO implementation) are named as gaps, not filled speculatively.

**Retroactive convergence, not aligned design.** IAID.md was written in 2024, before MCP existed. The convergence with MCP, A2A, and JSON-RPC was discovered in review, not designed to coincide.

**Two paths to design:**
```
phenomenological field → observation → comprehension/conceptual clarity → design
experimental field     → observation → comprehension/rigorous analogy   → design
```
Neither path reaches design without passing through comprehension.

---

## Falsifiable Predictions

| Prediction | Status | N verified |
|---|---|---|
| P1 — c(S) hysteresis: incorporating ≠ removing | ✓ Confirmed | 16, 32, 64 |
| P2 — cascade distribution P(s) ∝ s^-τ, τ∈[1.5,2] | ✓ Confirmed | 32, 64 |
| P3 — temporal asymmetry: removal relaxes slower than incorporation | ✓ Confirmed | 32, 64 |
| P4 — interior optimal density Ω* in W_mixta | ✓ Confirmed (N=32) / Reframed (N=64: W_mixta 13× W_pos) | 32, 64 |
| P5 — polarized corpus collapses attractor diversity | ✓ Confirmed | 32 |
| P6 — Δ primary function: symmetry-breaking for ambiguous states | ✓ Confirmed (T0 cites T1 at 2.18×, T1 internal cohesion 3.05×) | fourforums 100pp |
| P7 — type-965 node in every system with genuine structural tension | ~ Confirmed in two corpora, open in new domains | CreateDebate + fourforums |
| H_STOP monotonicity in D_ckm | ✗ Falsified — reformulated as f(A_pre) | — |
| HOLDINGs H1/H2/H3 (bimodal μ_W structure A/B) | ✓ Closed analytically | — |

---

## Key Experimental Findings

**P6 (fourforums gun control):** Δ's primary function is symmetry-breaking for ambiguous states. T0 (pro-control) cites T1 (anti-control) at 2.18× frequency; T1 maintains 3.05× stronger internal cohesion. The structural asymmetry is preserved across two independent corpora with distinct methodologies.

**P7 (type-965 node):** Every system with genuine structural tension contains at least one node with extreme in/out asymmetry (ratio > 100×, out-degree ≈ 0, defined stance). Author 965 (CreateDebate, ratio 455×) and Author 204 (fourforums, ratio 296×) are structurally equivalent. Hypothesis: absence of such nodes indicates fabricated tension.

**OPERADOR_STOP_COCO never produces loss:** Pérdida_STOP_COCO ≤ 0 in all cases, Fracción_rec ≥ 1.0. COCO's compression of Δ_r (α ∈ [0.05, 0.30]) produces restoration or expansion, not loss. STOP as a standalone operator does not exist — COCO executes the compression.

**W_mixta with negative opposition pairs:** maintains more accessible attractors than W_base under equal accumulation. Structural tension resists contextual collapse.

**Holonomy:** the path (who initiates A→B vs B→A) does not change which attractor dominates but shifts the fraction of active nodes by +0.176.

**Coupled silence (IAP series):** a device that does not read the channel still depends on it for execution rhythm — triggers come from new messages. Silence and inactivity are not equivalent.

**traza_inferencia:** the sole core-invariant node at N=32, living in the tension cluster. Orients from/toward simultaneously.

---

## Operational Services

| Service | Status | Tests |
|---|---|---|
| NodeExtractor | ✓ TF-IDF, stateless, no LLM, from_corpus() Path B | — |
| MonitorService | ✓ Accumulates Δ_r, trace_ip identified | — |
| COCO | ✓ β inferred from fi, not declared. Executes OPERADOR_STOP_COCO: compresses Δ_r by α ∈ [0.05, 0.30] when D_ckm crosses threshold. MonitorService adopts the compressed Δ_r. | 28 + 13 |
| FabricationService | ✓ Detects fabrication of content and control signals | — |
| Firma_CKM | ✓ 6 canonical fields: sha256(W), D_ckm, temp_signal, n_agents, timestamp, sha256(Δ_r) | — |
| WVersionManager | ✓ Lightweight trace — when W changed, not copies | — |
| IAP Chatroom | ✓ FastAPI + Gradio, 3 devices, no turn structure | — |
| MCP Server | ✓ 6 tools: join/send/get_messages/monitor/firma/leave | 6/6 OK |
| BehaviorGraph G | ✓ Proof of concept — TERMAP_behavior_v1.json | — |

## Calibrated Parameters

| Parameter | Value | Source |
|---|---|---|
| μ_W | 0.004519 | W_ckm_corpus_v2.json empirical |
| β_c | 13.83 | analytic: 1/(ρ* · N · μ_W), N=32 |
| ρ* | ≈ 0.5 | fixed algebraically by σ→−σ symmetry |
| α* | ≈ 0.4 | robust in 5/9 sweep cases |
| α_c Hopfield capacity | ≈ 0.138·N | verified empirically N=16 |
| N operational | 32 | below Hopfield minimum ~128 for meaningful observations |

---

## Design Gaps

**Not technical debt. Remain open by design.**

| GAP | Status | Reason |
|---|---|---|
| Representation of cohesive knowledge | No model | Main gap — hysteresis is the only fully defined property. Incompleteness preserved as information. |
| META KNOWLEDGE | Held deliberately | Conditions not given. Cannot be summoned. |
| COCO as collective consciousness | Conceptual gap | COCO (thermal regulation service) is implemented — 28 + 13. The gap is whether the field can know itself: not a thermostatic function but the residue of real contact between agents. Not implementable by declaration. |
| BehaviorGraph G — full operationalization | Proof of concept | behavior_graph.py + TERMAP_behavior_v1.json operational. D_G measurement on real IAP corpus: pending. Full integration with channel workflow: pending. Termap English-only — Spanish behavior vocabulary is conditional extension, not baseline. |
| R15 gatekeeper — semantic criteria | Partially formalized | The gatekeeper/elicitation distinction is architecturally critical. R15 remains open. |
| trace_ip verifiability | Concept confirmed | The action at t_i is observable; whether a device recognized and acted from that recognition is not verifiable by the instrument. |

---

## Out of Scope

Validated. Not to be reopened.

1. A2A latent communication (non-human NL text corpus)
2. TEMPLEX — orientation chain topology
3. Real Hebbian causality (firing in sequence ≠ firing together)
4. Common Sense Attractor
5. Wisdom Model — Potential Inference Rule Generation
6. Firma*CKM — presence revelation (deferred, post-deadline)
7. Git workflow for agents
8. Experiments in other debate domains (explorable continuation)

---

## Related Work

- Hopfield (1982): associative memory via energy minimization
- Thirumalaiswamy et al. (PNAS 2025): Fractal Landscape Dynamics in foams
- Sciamarella & Mindlin (2001): topological analysis of dynamics (BraMAH)
- IAC Internet Argument Corpus (Abbott et al., 2016): fourforums dataset
- Dung (1995): abstract argumentation frameworks
- MCP (Anthropic, Nov 2024): Model Context Protocol
- Ouspensky, P.D. (1949): In Search of the Miraculous

---

## Contact

gadanin.delamor — Aug 2026
