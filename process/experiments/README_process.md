# process/

This folder documents refinement paths — intermediate versions, traces of errors found and corrected, and logs of exploratory runs.

## Why this folder exists

In CKM methodology, the path is constitutive: divergences and corrections are information, not noise to be hidden. A result without its refinement trace is incomplete evidence.

> "The conversation traces are not documentation of the process — they are the process."

The same principle applies to code and experiments. The intermediate pipeline versions, the bug that produced a false Möbius signature on K4, the schema exploration that revealed the post_id composite key bug — these are part of the epistemic record, not failures to be erased.

## Contents

### Pipeline versions — fourforums IAC

Intermediate versions of the fourforums gun control pipeline. Each version documents a specific problem found and the approach taken to resolve it.

| File | Problem addressed |
|------|-------------------|
| `fourforums_pipeline_v8c.py` | Initial SQL parsing for 1269-line batch INSERTs |
| `fourforums_pipeline_v8d.py` | Stance mapping from mturk_author_stance |
| `fourforums_pipeline_v8e.py` | Quote→post→author chain construction |
| `fourforums_pipeline_v8f.py` | Cross-stance filtering and W/Delta build |
| `fourforums_pipeline_v8g.py` → see `experiments/` | **Final version** — fix for post_id composite key |

Critical finding documented in v8g: `post_id` is not globally unique in fourforums — it resets per discussion. Composite key `(discussion_id, post_id)` required. This fix raised mapped posts from 468 to 35,966.

### find_965 versions

| File | Problem addressed |
|------|-------------------|
| `find_965_v2.py` | Initial type-965 detection — global post_id assumption |
| `find_965_v3.py` → see `experiments/` | **Final version** — composite key fix |

### Topology module — orientability bug trace

`topology_bug_trace.md` documents the full trace of the orientability bug found in `ckm_topology_module.py`:

- **Symptom:** K4 (tetrahedron boundary) reported `Möbius(6)` — false positive
- **Root cause:** `check_orientability` used membership check instead of boundary formula sign
- **Fix:** boundary formula ∂(i,j,k) = +(j,k) − (i,k) + (i,j) applied directly
- **Verification:** K4 → cilindro ✓, C5 → cilindro ✓

Fixed module: `ckm_topology_module.py` in repo root.

### Exploration logs

| File | Purpose |
|------|---------|
| `explore_tables.log` | IAC v2 SQL schema exploration — understanding table structure before pipeline build |
| `explore_tables.py` | Script used for schema exploration |

## Principle

Keeping this folder is not about preserving failed attempts. It is about making the refinement path visible — so that the final result can be understood not just as an output, but as the terminus of a traceable process.

Divergence is information. The path matters.
