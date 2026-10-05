"""
test_coco.py
CKM — Tests suite: COCO

Ancla de simulación: exp_coco_thermostat_v1.png
  W_mixta AMP=40 · 3 pares · N=32 · seed=0 · n_runs=80 → A0=20
  (reproducido en esta sesión con calibrate_W_mixta.py + W_ckm_corpus_v2.json)

Ejecutar:
    pytest test_coco.py -v
    python test_coco.py   # modo standalone
"""

from __future__ import annotations
import sys
import json
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent / "services"))
from coco import (
    COCO, ThermostatState,
    D_CKM_THRESHOLD, ALPHA_STAR, FRAC_REC_MIN, ALPHA_MIN, ALPHA_MAX,
)
from landscape_engine import basin_masses, deprecated_count_attractors

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


# ── Fixtures ────────────────────────────────────────────────────────────────

def make_W_small(N=8, seed=1):
    """W simétrica pequeña para tests rápidos (sin dependencia de archivos)."""
    rng = np.random.default_rng(seed)
    W = rng.uniform(0, 0.05, (N, N))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0.0)
    return W


def make_W_mixta_amp40():
    """
    W_mixta AMP=40 desde W_ckm_corpus_v2.json.
    3 pares negativos: (13,22), (15,16), (18,20).
    Ancla: A0=20 (seed=0, n_runs=80).
    """
    candidates = [
        Path(__file__).parent / "W_ckm_corpus_v2.json",
        Path(__file__).parent.parent / "services" / "W_ckm_corpus_v2.json",
        Path("W_ckm_corpus_v2.json"),
    ]
    for p in candidates:
        if p.exists():
            data   = json.loads(p.read_text())
            W_base = np.array(data["W"])
            W      = W_base.copy()
            for i, j in [(13, 22), (15, 16), (18, 20)]:
                W[i, j] = -W_base[i, j] * 40
                W[j, i] = -W_base[i, j] * 40
            return W
    return None


# ══════════════════════════════════════════════════════════════════════
# GRUPO 1 — API y contrato de tipos
# ══════════════════════════════════════════════════════════════════════

class TestAPI:

    def setup_method(self):
        self.W  = make_W_small()
        self.N  = self.W.shape[0]
        self.th = COCO(W=self.W, n_runs=20, seed=0)

    def test_observe_returns_thermostat_state(self):
        state = self.th.observe(np.zeros((self.N, self.N)))
        assert isinstance(state, ThermostatState)

    def test_thermostat_state_has_required_fields(self):
        state = self.th.observe(np.zeros((self.N, self.N)))
        for field in ("t", "D_ckm", "A_current", "A0",
                      "frac_rec", "stop_applied", "alpha_used", "zone"):
            assert hasattr(state, field), f"Campo faltante: {field}"

    def test_zone_is_valid_string(self):
        state = self.th.observe(np.zeros((self.N, self.N)))
        assert state.zone in ("stable", "degrading", "deep")

    def test_status_has_required_keys(self):
        self.th.observe(np.zeros((self.N, self.N)))
        s = self.th.status()
        for key in ("t", "A0", "A_current", "D_ckm",
                    "frac_rec", "zone", "stop_applied", "alpha_used"):
            assert key in s, f"Clave faltante en status(): {key}"

    def test_history_empty_before_observe(self):
        th = COCO(W=self.W, n_runs=20, seed=0)
        assert th.history() == []

    def test_delta_state_returns_array(self):
        ds = self.th.delta_state()
        assert isinstance(ds, np.ndarray)
        assert ds.shape == (self.N, self.N)

    def test_t_increments(self):
        for i in range(3):
            state = self.th.observe(np.zeros((self.N, self.N)))
        assert state.t == 3

    def test_history_grows(self):
        for _ in range(4):
            self.th.observe(np.zeros((self.N, self.N)))
        assert len(self.th.history()) == 4


# ══════════════════════════════════════════════════════════════════════
# GRUPO 2 — Clasificación de zonas (analítico, sin Hopfield)
# ══════════════════════════════════════════════════════════════════════

class TestZoneClassification:

    def setup_method(self):
        W  = make_W_small()
        self.th = COCO(W=W, n_runs=5, seed=0)

    def test_D_ckm_None_is_stable(self):
        """Baseline ≤ 1: d_ckm devuelve None, no hay medición y no hay STOP."""
        z = self.th._classify_zone(None, 1.0)
        assert z == "stable"

    def test_negative_D_ckm_is_stable(self):
        z = self.th._classify_zone(-0.1, 0.9)
        assert z == "stable"

    def test_below_threshold_is_stable(self):
        z = self.th._classify_zone(D_CKM_THRESHOLD - 0.01, 0.5)
        assert z == "stable"

    def test_zero_D_ckm_is_stable(self):
        z = self.th._classify_zone(0.0, 1.0)
        assert z == "stable"

    def test_above_threshold_high_frac_is_degrading(self):
        z = self.th._classify_zone(D_CKM_THRESHOLD + 0.01, FRAC_REC_MIN + 0.01)
        assert z == "degrading"

    def test_above_threshold_low_frac_is_deep(self):
        z = self.th._classify_zone(D_CKM_THRESHOLD + 0.01, FRAC_REC_MIN - 0.01)
        assert z == "deep"

    def test_exactly_at_threshold_high_frac_is_degrading(self):
        z = self.th._classify_zone(D_CKM_THRESHOLD, FRAC_REC_MIN + 0.01)
        assert z == "degrading"


# ══════════════════════════════════════════════════════════════════════
# GRUPO 3 — Calibración dinámica de alpha
# ══════════════════════════════════════════════════════════════════════

class TestAlphaFor:

    def setup_method(self):
        W = make_W_small()
        self.th_dyn   = COCO(W=W, dynamic_alpha=True,  n_runs=5)
        self.th_fixed = COCO(W=W, dynamic_alpha=False, n_runs=5)

    def test_alpha_at_threshold_equals_alpha_max(self):
        a = self.th_dyn._alpha_for(D_CKM_THRESHOLD)
        assert abs(a - ALPHA_MAX) < 1e-9

    def test_alpha_at_one_equals_alpha_min(self):
        a = self.th_dyn._alpha_for(1.0)
        assert abs(a - ALPHA_MIN) < 1e-9

    def test_alpha_is_monotonically_decreasing(self):
        vals = [self.th_dyn._alpha_for(d)
                for d in np.linspace(D_CKM_THRESHOLD, 1.0, 10)]
        for i in range(len(vals) - 1):
            assert vals[i] >= vals[i + 1] - 1e-9

    def test_alpha_in_valid_range(self):
        # tolerancia 1e-9 en ambos extremos por aritmética flotante
        for d in np.linspace(D_CKM_THRESHOLD, 1.0, 20):
            a = self.th_dyn._alpha_for(d)
            assert ALPHA_MIN - 1e-9 <= a <= ALPHA_MAX + 1e-9, \
                f"alpha={a:.8f} fuera de [{ALPHA_MIN}, {ALPHA_MAX}] en D_ckm={d:.4f}"

    def test_fixed_alpha_returns_alpha_star(self):
        for d in [0.4, 0.6, 0.9]:
            a = self.th_fixed._alpha_for(d)
            assert abs(a - ALPHA_STAR) < 1e-9


# ══════════════════════════════════════════════════════════════════════
# GRUPO 4 — Operador STOP
# ══════════════════════════════════════════════════════════════════════

class TestSTOP:

    def setup_method(self):
        self.W = make_W_small()
        self.N = self.W.shape[0]

    def _thermostat_with_forced_zone(self, zone):
        """Crea thermostat con umbral ajustado para forzar zona."""
        if zone == "stable":
            return COCO(
                W=self.W, d_ckm_threshold=0.99, n_runs=20, seed=0
            )
        elif zone == "degrading":
            return COCO(
                W=self.W, d_ckm_threshold=0.0, frac_rec_min=0.0, n_runs=20, seed=0
            )

    def test_stable_zone_no_stop(self):
        th    = self._thermostat_with_forced_zone("stable")
        Delta = np.ones((self.N, self.N)) * 0.5
        np.fill_diagonal(Delta, 0)
        state = th.observe(Delta)
        assert state.stop_applied is False
        assert state.alpha_used == 1.0

    def test_degrading_zone_stop_applied(self):
        """Cuando D_ckm >= threshold, stop_applied=True.

        observe() llama _count_attractors DOS veces en la primera invocación
        (una para A_current, otra para A0 si es None). Para controlar el
        resultado se fija _A0 directamente y se parchea solo A_current.

        Los literales eran A0=10, A=5 con la forma lineal (D_ckm=0.5). Desde
        el 5 de octubre de 2026 d_ckm es 1 - ln A / ln A0 y esos valores dan
        0.301, por debajo del umbral. Con A0=4, A=2 vuelve a dar 0.5.
        """
        th = COCO(W=self.W, n_runs=5, seed=0)
        N  = self.N
        # A0=4 fijo; _count_attractors devuelve 2 → D_ckm = 1 − ln2/ln4 = 0.5
        # frac_rec = 0.5 < FRAC_REC_MIN → deep
        th._A0 = 4.0
        th._count_attractors = lambda W_eff: 2.0
        Delta = np.ones((N, N))
        np.fill_diagonal(Delta, 0)
        state = th.observe(Delta)
        assert state.A0 == 4.0
        assert state.A_current == 2.0
        assert state.D_ckm == pytest.approx(0.5) if HAS_PYTEST else abs(state.D_ckm - 0.5) < 1e-9
        assert state.zone in ("degrading", "deep")
        assert state.stop_applied is True
        assert state.alpha_used < 1.0

    def test_stop_scales_delta(self):
        """Después de STOP, delta_state() contiene Delta escalado."""
        th = COCO(W=self.W, n_runs=5, seed=0)
        N  = self.N
        # A0=10, A_current=2 → D_ckm = 1 − ln2/ln10 = 0.699 → deep
        th._A0 = 10.0
        th._count_attractors = lambda W_eff: 2.0
        Delta = np.ones((N, N)) * 4.0
        np.fill_diagonal(Delta, 0)
        state = th.observe(Delta)
        assert state.stop_applied is True
        ds = th.delta_state()
        assert ds.max() < Delta.max(), "Delta debe ser reducido por STOP"
        assert ds.max() > 0, "Delta no debe colapsar a cero"

    def test_delta_after_stop_nonnegative(self):
        th    = self._thermostat_with_forced_zone("degrading")
        Delta = np.abs(np.random.default_rng(0).normal(0, 1, (self.N, self.N)))
        np.fill_diagonal(Delta, 0)
        th.observe(Delta)
        assert th.delta_state().min() >= 0


# ══════════════════════════════════════════════════════════════════════
# GRUPO 5 — W es inmutable
# ══════════════════════════════════════════════════════════════════════

class TestWImmutable:

    def test_W_not_modified_by_stop(self):
        W  = make_W_small()
        W0 = W.copy()
        # threshold=0 → siempre STOP
        th    = COCO(W=W, d_ckm_threshold=0.0,
                               frac_rec_min=0.0, n_runs=20, seed=0)
        Delta = np.ones_like(W) * 2.0
        np.fill_diagonal(Delta, 0)
        th.observe(Delta)
        np.testing.assert_array_equal(
            th.W, W0,
            err_msg="W fue modificada por STOP — debe ser inmutable"
        )

    def test_W_not_modified_by_multiple_observes(self):
        W  = make_W_small()
        W0 = W.copy()
        th = COCO(W=W, d_ckm_threshold=0.0,
                            frac_rec_min=0.0, n_runs=20, seed=0)
        for _ in range(5):
            Delta = np.abs(np.random.default_rng(0).normal(0, 1, W.shape))
            np.fill_diagonal(Delta, 0)
            th.observe(Delta)
        np.testing.assert_array_equal(th.W, W0)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 6 — Ancla de simulación (requiere W_ckm_corpus_v2.json)
# ══════════════════════════════════════════════════════════════════════

class TestSimulationAnchor:
    """
    Ancla contra exp_coco_thermostat_v1.png:
      W_mixta AMP=40 · 3 pares · N=32 · seed=0 · n_runs=80 → A0=20

    Ese 20 es el CONTEO de estados terminales. Desde el 5 de octubre de 2026
    A0 es N_eff0 (masa de cuenca) y sobre la misma W da 6.7653.
    """

    def setup_method(self):
        self.W = make_W_mixta_amp40()

    def test_simulation_anchor_A0_equals_20(self):
        """El ancla histórica (conteo = 20) se verifica con
        deprecated_count_attractors; A0 de COCO es N_eff0 = 1 / Σ m² sobre
        las masas de cuenca de la misma W, hecho a mano."""
        if self.W is None:
            print("  [SKIP] W_ckm_corpus_v2.json no disponible")
            return
        N  = self.W.shape[0]
        th = COCO(W=self.W, n_runs=80, seed=0)
        state = th.observe(np.zeros((N, N)))
        assert deprecated_count_attractors(self.W, n_runs=80, seed=0) == 20
        masas = basin_masses(self.W, n_runs=80, seed=0)
        assert abs(state.A0 - 1.0 / float(np.sum(masas ** 2))) < 1e-9
        assert abs(state.A0 - 6.7653) < 1e-4

    def test_D_ckm_es_la_formula_canonica(self):
        """observe() devuelve D_ckm = 1 − ln N_eff / ln N_eff0, con N_eff
        sobre W + Delta y N_eff0 sobre W sola. La cuenta se hace a mano
        desde las masas de cuenca; no se toca nada privado de COCO."""
        if self.W is None:
            return
        N     = self.W.shape[0]
        rng   = np.random.default_rng(42)
        Delta = np.zeros((N, N))
        for _ in range(60):
            i, j = rng.integers(0, N, 2)
            Delta[i, j] += 1
            Delta[j, i] += 1
        th    = COCO(W=self.W, n_runs=80, seed=0)
        state = th.observe(Delta)
        m0 = basin_masses(self.W,         n_runs=80, seed=0)
        mt = basin_masses(self.W + Delta, n_runs=80, seed=0)
        n0 = 1.0 / float(np.sum(m0 ** 2))
        nt = 1.0 / float(np.sum(mt ** 2))
        a_mano = 1.0 - np.log(nt) / np.log(n0)
        assert abs(state.A0 - n0) < 1e-9
        assert abs(state.A_current - nt) < 1e-9
        assert abs(state.D_ckm - a_mano) < 1e-4      # el estado redondea a 4
        assert abs(state.D_ckm - 0.515) < 1e-3

    def test_delta_zero_gives_D_ckm_zero(self):
        """Delta=0 → A_current=A0 → D_ckm=0."""
        if self.W is None:
            return
        N  = self.W.shape[0]
        th = COCO(W=self.W, n_runs=80, seed=0)
        state = th.observe(np.zeros((N, N)))
        assert state.D_ckm == 0.0
        assert state.frac_rec == 1.0
        assert state.zone == "stable"
        assert state.stop_applied is False

    def test_alpha_sale_de_D_ckm_sobre_el_Delta_de_la_simulacion(self):
        """Sobre el Delta de la simulación, alpha_used es el que corresponde
        al D_ckm medido: ALPHA_MAX en el umbral, bajando lineal hasta
        ALPHA_MIN en D_ckm = 1. La cuenta se hace a mano con las constantes.

        Este test se llamaba test_alpha_at_threshold_is_alpha_max y afirmaba
        que ese Delta cae justo en el umbral. Valía con la forma por conteo
        y ya no vale con la canónica:

            conteo, forma lineal   A0=20    A=12    D_ckm=0.400  alpha=0.30
            N_eff, forma canónica  A0=6.77  A=2.53  D_ckm=0.515  alpha=0.252

        Los umbrales de COCO no se recalibraron sobre la escala nueva —
        abierto en TASK_d_ckm_formula_canonica_v1. Si se recalibran, los
        valores de acá se mueven y este test lo va a decir.
        """
        if self.W is None:
            return
        N  = self.W.shape[0]
        th = COCO(W=self.W, n_runs=80, seed=0)
        # fijar A0 primero
        th.observe(np.zeros((N, N)))
        # el Delta de la simulación
        rng   = np.random.default_rng(42)
        Delta = np.zeros((N, N))
        for _ in range(60):
            i, j = rng.integers(0, N, 2)
            Delta[i, j] += 1
            Delta[j, i] += 1
        state = th.observe(Delta)
        assert abs(state.D_ckm - 0.515) < 1e-3
        assert state.stop_applied is True
        ratio  = (state.D_ckm - D_CKM_THRESHOLD) / (1.0 - D_CKM_THRESHOLD)
        a_mano = ALPHA_MAX + (ALPHA_MIN - ALPHA_MAX) * ratio
        assert abs(state.alpha_used - a_mano) < 1e-3, \
            f"alpha_used={state.alpha_used} a mano={a_mano}"
        assert abs(state.alpha_used - 0.252) < 1e-3


# ══════════════════════════════════════════════════════════════════════
# Runner standalone
# ══════════════════════════════════════════════════════════════════════

def run_standalone():
    groups = [
        TestAPI,
        TestZoneClassification,
        TestAlphaFor,
        TestSTOP,
        TestWImmutable,
        TestSimulationAnchor,
    ]
    passed = failed = 0
    for cls in groups:
        for name in [m for m in dir(cls) if m.startswith("test_")]:
            obj = cls()
            if hasattr(obj, "setup_method"):
                obj.setup_method()
            try:
                getattr(obj, name)()
                print(f"  ✓  {cls.__name__}::{name}")
                passed += 1
            except Exception as e:
                print(f"  ✗  {cls.__name__}::{name}")
                print(f"      {type(e).__name__}: {e}")
                failed += 1
    print(f"\n{'─'*55}")
    print(f"  {passed} passed, {failed} failed")


if __name__ == "__main__":
    run_standalone()
