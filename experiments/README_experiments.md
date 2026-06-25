# Cohesive Knowledge Model — Datasets Experiments and Tests

## CKM Tools

### Módulo P1-P4 ckm_p1p4_module.py

CKM — Módulo P1-P4 con protocolos correctos

Uso desde cualquier pipeline:

    from ckm_p1p4_module import run_all
    results = run_all(W_base, W_mixta, nodes, label="fourforums_guncontrol")

Protocolos según EXPERIMENTS.md:
    P1: sweep up/dowsn, medir c(S) en cada paso, Wilcoxon zona ρ∈[0.35,0.70]
    P2: cascadas k-core, MLE estimador τ, buscar zona τ∈[1.5,2.0]
    P3: pasos de poda k-core tras remoción vs adición, Mann-Whitney
    P4: c(S) de estados ALEATORIOS en 30 niveles de densidad ρ∈[0.05,1.0]

Requisitos:
    pip install numpy scipy networkx

### fourforums_pipeline_v8g.py

fix: clave compuesta (discussion_id, post_id) - post_id no es global en fourforums.

Cambios respecto a v8c:
  - parse_sql_small: carga todo EXCEPTO mturk_2010_qr_entry (evita 10GB RAM)
  - stream_W_delta: segunda pasada streaming - procesa qr_entry row a row
  - build_W_delta refactored: usa stream_W_delta internamente
  - mturk_2010_qr_entry vuelve a SKIP_TABLES para parse_sql_small

Uso:
    python fourforums_pipeline_v8g.py --sql fourforums_no_parse_2016_05_18.sql --log run.log
    python fourforums_pipeline_v8g.py --sql ... --skip_p1p4 --log run.log
    # PEG LOG & CONSOLE
    python fourforums_pipeline_v8g.py --sql fourforums_no_parse_2016_05_18.sql --log run_v8g.log | Tee-Object -FilePath run_v8e_console.log

### find_965_v3.py

Candidatos a polo sostenedor puro en fourforums - clave compuesta (disc_id, post_id).
Usa todos los autores activos en gun_disc_ids.