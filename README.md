# CKM — Cohesive Knowledge Model

**Status:** research · October 2026 · paper draft v32 (v33 in preparation)
**Author:** gadanin.delamor (Pablo E. Gadano)
**License:** MIT

---

## What CKM is

CKM is an **instrument** for measuring the geometry of a co-occurrence landscape. Given a signed, symmetric weight matrix W over N nodes, it relaxes a Hopfield network from sampled initial states and reports how the state space distributes over the attractors reached.

Its central contribution is **N_eff = 1/Σm_i²**, the inverse Simpson index over basin masses, as a **convergent estimator of landscape diversity**. Attractor counts grow with sampling; basin masses converge. Against exact enumeration of all 2²⁰ states in three N = 20 corpora, orbit counts err by up to 28 % and N_eff by at most 0.6 %.

What CKM is **not**:

- **It does not extract and does not tokenize.** It measures the W it is given. Whoever produces W declares how (the extraction operators), and every result holds for that W under that declaration.
- **It does not interpret meaning.** It measures dynamics, not content.
- **It does not intervene in the field.** Its regulator (COCO) compresses its *own* representation, `Δ_r_compresiones`; the regulation does not reach `Δ_r_pares` or W (`services/coco.py`). What CKM outputs are metrics, a trace, and that self-regulation.

---

## What this repository holds

The repository hosts more than the instrument. It has four layers and one bridge:

| layer | files | what it is |
|---|---|---|
| **Producer of W** | `services/corpus_service.py`, `services/node_extractor.py` | Extraction: text → nodes → W. Declared, not part of CKM. |
| **CKM instrument** | `services/landscape_engine.py`, `monitor_service.py`, `coco.py`, `calibrate.py`, `ckm_landscape_config.py`, `w_version.py`, `firma_ckm.py`, `ckm_trust_rule.py`, `cluster_frontier_density.py`, `analytics.py` | Relaxation, basin masses, N_eff, D_ckm, Δ_r, COCO, calibration, configuration, trace. |
| **IAP channel** | `iap_chatroom/channel.py`, `server.py`, `api_routes.py`, `mcp_server.py`, `ui_gradio.py`, `run_store.py`, `startup.py`, `device_manager.py` | A broadcast channel for heterogeneous AI and human devices; MCP is its only interface. |
| **Bridge** | `iap_chatroom/ckm_monitor.py` | The only file in `iap_chatroom/` that imports the instrument: CKM with channel context. |
| **IAP devices** | `iap_chatroom/autonomous_device.py`, `local_criterion.py`, `agent_device_skin.py`, `groq_research_agent.py`, `providers/` | Devices, skins and LLM access. |

Outside the instrument although it lives in `services/`: `gatekeeper_c1.py`, a judge over declared device capabilities (IAID lineage), not over the landscape. `behavior_graph.py` (a second matrix G over a fixed behavior vocabulary) is a proof of concept; whether it is instrument or another producer of W is open.

**The boundary already exists in the code:** devices import nothing from `services/`. They see CKM only through MCP (`get_monitor_state`, `get_firma`), and the only thing they hand to the instrument is the text they publish.

### Devices, not agents (working definitions)

- **AI agent** = `agent_harness(LLM)`: an agentic, multi-turn loop with declared capabilities and configuration. The loop closes when its goal is met.
- **IAP device** = `iap_device_harness(LLM)`: a continuous **ODA** loop (Observe → Decide → Act) with **free will** (it decides when to act: publish, leave, or do nothing), a **local criterion** between O and D that decides whether a turn is worth an LLM call, declared capabilities and configuration. The ODA loop does not close on a goal.
- **IAP device skin** = `iap_device_skin(AI agent)` = ODA(agentic loop(LLM)): O and A belong to the ODA harness; D and the content belong to the wrapped agent (`agent_device_skin.py`).
- **IAP** = broadcast channel + the CKM instrument with channel context + configuration. The channel does not require latent transfer or external memories from its devices.

Whether a device is a **Landscape Driven Device** — one whose trajectory is co-determined by field geometry — is a proposed framing, not a property: a device that reads the monitor state in its O phase is a candidate, not verified.

---

## Core quantities

- **W** — symmetric co-occurrence matrix, N×N, in [−1, +1]. Its sign comes from a declared procedure of the producer. Non-co-occurrence is not represented: a pair that never co-occurs and a pair the corpus says nothing about both take 0.
- **Δ** — asymmetric directional dependency matrix (citation or quote direction). **W and Δ are kept strictly separate**: mixing them reduced pattern recovery from 0.78 to 0.02.
- **Δ_r_pares** — pairs a text declared active that relaxation expelled; written only by MonitorService. **Δ_r_compresiones** — COCO's own copy, compressed when COCO fires.
- **c(S)** = mean(W_ij·σ_i·σ_j) over i < j: alignment of a state with W.
- **N_eff** = 1/Σm_i² over basin masses. **D_ckm** = 1 − ln N_eff_t / ln N_eff_0 (`landscape_engine.d_ckm`), computed by two instances with different baselines: **D_ckm^Monitor** on W + Δ_r_pares, **D_ckm^COCO** on W + Δ_r_compresiones.
- **Calibration** (`services/calibrate.py`) sets COCO's thresholds per W at each rebuild. The first W of a run is built before the calibration point and is never calibrated (`registers/REG_calibrate_no_corre_en_el_build_v1.md`).
- **CKMLandscapeConfig** — the instrument's contract: what is *declared* (`sampling_mode`, `n_runs`, `seed`, `scale`) and what is *measured* per W cycle (`w_version_id`, N, μ_W, β_c). COCO's thresholds are not in it: they belong to calibration.

### Static and dynamic W

- **Static W (a snapshot)** has no premises. It has **formulations verified on the snapshot** — determinism of the synchronous dynamics under the tie rule [Goles], hysteresis, k-core reversibility and interior optimal density on W ≥ 0 — and **declarations**: the producer, the reference measure (uniform σ₀), the Config.
- **Dynamic W** (the corpus ingests and W is rebuilt) has one premise: **the field is continuous; what jumps is its measurement.**

---

## Status of the results

What is established and what is not, as of paper draft v32 and the decisions of 26 Oct 2026 (`docs/opus/decisiones_en_el_acto.md`):

| item | status |
|---|---|
| N_eff over basin masses converges; counts do not | verified against exact enumeration (N = 20, three corpora) |
| Stability of the landscape under extraction parameters | declared as a range: highly sensitive on 7–24 texts |
| Formulations on static W ≥ 0 (hysteresis, k-core, optimal density) | verified on the snapshot |
| Sign of W from opposition markers | a permutation null does not separate the real marking from chance in three corpora |
| Fourforums (IAC 2.0), sign from annotator votes | one test: fewer frustrated triangles than a sign-permutation null (z = −2.06); the instrument is at its ceiling at N = 146 |
| Earlier predictions P2, P5, P6, P7 | withdrawn as predictions; P5–P7 wait for conditions |
| Live IAP series 1 and 2 | tests of the instrument, not findings about the field |

**Earlier versions of this README listed P1–P7 as confirmed. That table is withdrawn.** The trace of why is in the paper drafts (`docs/opus/PAPER_*`) and in `registers/`.

---

## Repository map

```
services/        the instrument, the producer, the gatekeeper (see above)
iap_chatroom/    IAP channel, bridge, devices, skins, providers; tests in iap_chatroom/tests/
tests/           test suite (pytest)
experiments/     experiment scripts (e.g. medir_W_fourforums_v8n.py)
registers/       REGs — Class R, written once, not modified
docs/
  opus/          Opus (Cowork) docs: paper drafts, ESTADO, decisiones_en_el_acto, reviews
  tasks/         TASKs and BANDEJA_code.md (Code's reports)
  defs/          DEFS (definitions, versioned)
  paper/         earlier paper material
process/         frozen conditions and preserved states of runs
  model_properties_front_20261004/   the 4–5 Oct front on the static-model properties (formerly P1P4/)
readme/          THEORY, METODOLOGY, AWARENESS, CONVENTIONS, API_SPEC, EXPERIMENTS, LETTER
```

The fourforums pipelines (v8h–v8n) and the W they build live in a separate repository, `ckmdatasets`. The W reach this repository by hand, anonymized, outside git.

---

## How to run

Code is run in a GitHub Codespace, not on a local machine.

```bash
pip install -e .                       # numpy, scipy, networkx, scikit-learn~=1.9.0, …
python -m pytest tests                 # the suite
./iap_chatroom/correr_caso0.sh --check # checks everything for series 2, case 0, without the live run
./iap_chatroom/correr_caso0.sh         # the live run (~20 min; providers' quotas apply)
```

The IAP server exposes FastAPI at `:7860/api/*`, the Gradio UI at `:7860/ui/` and the MCP server at `:7860/mcp`, with six tools: `join_channel`, `send_message`, `get_messages`, `get_monitor_state`, `get_firma`, `leave_channel`.

**Data.** The Internet Argument Corpus 2.0 is obtained from https://nlds.engineering.ucsc.edu/iac2/ and is not redistributed. Only aggregates are reported.

---

## How the work is done

- **The CKM TRUST rule** (`registers/REG_regla_ckm_trust_v1.md`; `services/ckm_trust_rule.py`): the field decides with trace; on a tie the trace decides; with no trace, doubt the criterion; on a tie with no trace, a named context criterion decides, as bias.
- **AWARENESS** (`readme/AWARENESS.md`): pause, trace, correction without defense, silence, record of conditions.
- **Measure, don't name:** results are recorded without deciding what they mean; a design that pushes toward an outcome is declared as bias with its objective.
- **Trace:** decisions are recorded as they are taken (`docs/opus/decisiones_en_el_acto.md`); REGs are Class R; code and docstring are read together, and divergences are declared and corrected.
- **No product versions:** the only version of the model is the current one; reproducibility is achieved by freezing the minimum a test needs into `process/`.

---

## Preserved conditions

Named and kept open, not technical debt:

- **The representation gap.** How cohesive knowledge is represented beyond hysteresis is undefined.
- **COCO as collective consciousness.** Whether the field can know itself, not as a thermostatic service but as the residue of real contact between devices.
- **trace_ip verifiability.** The inflection in a trace is observable; whether a device recognized it and acted from it is not.
- **Scale.** The working corpora are small, and CKM's effective minimum is undetermined.

---

## Related work

Hopfield (1982) · Hill (1973) · Goles-Chacc et al. (1985) · Menck et al. (2013) · Daza et al. (2016) · Aiyappa, Flammini & Ahn (2024) · Thirumalaiswamy et al. (PNAS 2025) · Abbott et al. (2016), Internet Argument Corpus 2.0 · MCP (Anthropic, 2024). Full references in the paper draft.

---

gadanin.delamor — October 2026
