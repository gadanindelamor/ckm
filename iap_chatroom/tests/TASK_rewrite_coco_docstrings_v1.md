# TASK_rewrite_coco_docstrings_v1.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*

---

## Objetivo

Reemplazar los docstrings de `services/coco.py` por versiones orientadas
a developer. Los originales están archivados en
`docs/DOC_coco_drift_docstrings_v1.md` — no se pierden.

**Solo tocar docstrings.** Cero cambios a lógica, imports, constantes,
o firmas de métodos.

---

## Docstrings nuevos — aplicar con str_replace

### Module docstring

```python
"""
coco.py — Field regulator for CKM multi-device systems.

Monitors Δ_r (rejection accumulator from MonitorService) and compresses
it when attractor diversity falls below baseline. Emits thermal signal
(TOO_COLD / NOMINAL / TOO_HOT) relative to the field's critical β.

Quick start:
    coco = COCO(W=corpus.get_W())           # corpus must be in evaluation mode
    state = coco.observe(monitor._Delta_r)  # evaluate field and act
    if state.stop_applied:
        monitor._Delta_r = coco.delta_state()

W is fixed at instantiation — structural baseline of the field.
If W rebuilds (corpus grew), create a new COCO instance.

Ref: REG_destruccion_recuperacion_v1.md, REG_beta_colectivo_v1.md
"""
```

### class COCO

```python
class COCO:
    """
    Collective field regulator.

    Triggers STOP (Δ_r → α·Δ_r) when attractor diversity loss D_ckm
    exceeds threshold (default 0.40). α is dynamic: deeper degradation
    → smaller α → more aggressive compression.

    Also emits a thermal signal comparing β_collective to the field's
    critical β_c (TOO_COLD / NOMINAL / TOO_HOT).

    Does not track individual devices or their identities.
    Sees only what the field collectively rejected (Δ_r).
    """
```

### `__init__`

```python
    def __init__(
        self,
        W: np.ndarray,
        n_runs: int = 50,
        seed: int = 42,
        dynamic_alpha: bool = True,
    ):
        """
        Args:
            W:             Symmetric co-occurrence matrix from CorpusService.
                           Must be in evaluation mode:
                               assert corpus.mode == "evaluation"
                               coco = COCO(W=corpus.get_W())
                           W=None raises ValueError.
            n_runs:        Hopfield relaxation runs for attractor counting.
            seed:          RNG seed for reproducibility.
            dynamic_alpha: If True, α scales with D_ckm. If False, uses
                           ALPHA_STAR constant.
        """
```

### `observe()`

```python
    def observe(self, Delta_new: np.ndarray) -> ThermostatState:
        """
        Evaluate field state and apply STOP if degradation threshold crossed.

        Args:
            Delta_new: Current Δ_r from MonitorService (NxN float array).

        Returns:
            ThermostatState with fields:
                .stop_applied (bool)   — True if STOP fired this cycle.
                .alpha_used   (float)  — Compression factor applied (None if no STOP).
                .D_ckm        (float)  — Attractor diversity loss vs baseline [0, 1].
                                         Negative = field expanded (not an error).
                .zone         (str)    — "nominal" | "degrading" | "deep"
                .temp_signal  (dict)   — Thermal state (see temp_signal()).

        Side effect:
            If stop_applied, internal Δ is updated to α·Δ_new.
            Retrieve with delta_state() and assign back to MonitorService.
        """
```

### `beta_c_corpus()`

```python
    def beta_c_corpus(self) -> float:
        """
        Critical β of the corpus: the point of maximum attractor diversity (Ω*).

        β_c = 1 / (ρ* · N · μ_W)

        Returns a float. Example: N=32, μ_W=0.004519 → β_c ≈ 13.83.
        """
```

### `temp_signal()`

```python
    def temp_signal(self) -> dict:
        """
        Thermal state of the collective field.

        Returns dict with keys:
            signal          (str):   "TOO_COLD" | "NOMINAL" | "TOO_HOT" | "UNKNOWN"
            beta_collective (float): Median β across active devices.
            beta_c_corpus   (float): Critical β from W structure.
            ratio           (float): beta_collective / beta_c_corpus.

        TOO_COLD (ratio > 2.0): field too rigid — rejects everything, starves.
        TOO_HOT  (ratio < 0.5): field too permissive — accepts everything, loses discrimination.
        NOMINAL  (ratio ≈ 1.0): field at Ω*, gatekeeper discriminates well.
        UNKNOWN: no active devices registered yet.
        """
```

### `delta_state()`

```python
    def delta_state(self) -> np.ndarray:
        """
        Returns current Δ after any STOP compressions applied.

        Call this after observe() when stop_applied is True to retrieve
        the compressed Δ_r for assignment back to MonitorService.
        """
```

### `_alpha_for()`

```python
    def _alpha_for(self, D_ckm: float) -> float:
        """
        Maps D_ckm to compression factor α (internal).

        D_ckm at threshold → α = ALPHA_MAX (soft stop).
        D_ckm at 1.0       → α = ALPHA_MIN (aggressive stop).
        Linear interpolation between the two.
        Returns ALPHA_STAR if dynamic_alpha=False.
        """
```

---

## Criterio de éxito

```bash
python services/test_coco.py   # 43/43
grep -n '"""' services/coco.py  # confirmar que todas las funciones tienen docstring
```

## NO modificar

- Lógica de ningún método
- Constantes (D_CKM_THRESHOLD, ALPHA_MIN, ALPHA_MAX, etc.)
- Firmas de métodos
- `ThermostatState` (clase de datos — no tiene docstring extenso actualmente)

---

*Repo: gadanindelamor/ckm · Codespace: ckm*
