# TASK_landscape_engine_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: REG_monitor_service_unificar_rutinas_v1 — "no cierra la duplicación de raíz. La opción A —extraer a módulo compartido— sigue pendiente y requiere autorización para tocar `coco.py`." Autorización dada (Sep 2026).*

---

## Qué hacer

Extraer las rutinas de paisaje a `services/landscape_engine.py` como funciones puras. COCO y MonitorService delegan; ninguno conserva su copia.

## Alcance

- `services/coco.py` y `services/monitor_service.py` **únicamente**.
- `fabrication_service.py` tiene una tercera copia de `_relax` y **queda afuera**: se reescribe de cero cuando esto termine *(decisión delamor)*.
- Las copias de `experiments/` no entran.

## Qué se extrae

`relax_orbit`, `relax`, `node_probs`, `beta_c_landscape`, `boltzmann_warmup`, `sample_s0`, `count_attractors`, `mean_cS`, y la constante `BETA_RHO_STAR` (ρ* = 0.5, estaba declarada en los dos lados).

N sale de `W_eff.shape[0]`: en COCO es fijo al construir, en Monitor se reconstruye con el corpus.

## Qué NO se unifica

`_combine_W_Delta`. La W sobre la que cuenta cada instrumento es lo que los distingue:

```
COCO:            W_eff = W + Δ_r
MonitorService:  W_eff = W + (Δ_r / max(Δ_r)) · mean(W>0)
```

COCO ve dirección y magnitud de Δ_r; Monitor sólo dirección. Decisión declarada en REG_monitor_service_unificar_rutinas_v1, no pendiente.

Los wrappers de cada servicio se conservan (`self._relax`, `self._count_attractors`, …): las firmas y el estado de instancia —`_n_runs`, `_seed` / `_count_seed`, `_sampling_mode`, `_n_warmup`— no cambian, así que ningún sitio de llamada se toca.

## Verificación

- Impacto numérico cero contra una línea de base tomada **antes** de la extracción: 9 casos (COCO × 3 modos × 2 seeds sobre `W_ckm_corpus_v2` + Δ sintética; Monitor × 3 modos sobre corpus real, comparando `D_ckm`, `c_S`, `fabrication_index`, `n_rejected_pairs`, `Delta_r_sum`, `activos_relajado`).
- `tests/` completo sin regresión.
- `python services/coco.py` (T1–T13) y `python services/monitor_service.py` OK.

## Abierto

- Tercera copia en `fabrication_service.py` — hasta su reescritura.
- Copias en `experiments/`.
