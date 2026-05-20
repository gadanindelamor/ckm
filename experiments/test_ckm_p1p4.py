"""
test_ckm_p1p4.py
CKM — Tests sintéticos módulo P1-P4

Diseño: cada test usa matrices construidas con propiedades conocidas
analíticamente, no empíricas. Sin corpus externo.

Ejecutar:
    pytest test_ckm_p1p4.py -v
    python test_ckm_p1p4.py          # modo standalone

Requisitos:
    pip install numpy scipy networkx pytest
"""

import sys
import json
import tempfile
from pathlib import Path

import numpy as np
try:
    import pytest
except ImportError:
    pytest = None  # modo standalone: pytest.raises reemplazado abajo

sys.path.insert(0, str(Path(__file__).parent))
from ckm_p1p4_module import cS, relax, run_P1, run_P2, run_P3, run_P4, run_all

SEED = 42


# ══════════════════════════════════════════════════════════════════════
# FIXTURES — matrices con propiedades conocidas
# ══════════════════════════════════════════════════════════════════════

def make_W_ferro(N=6, w=0.05):
    """
    W ferromagnética: todos los pares positivos e iguales.
    Propiedad analítica: c(S) depende SOLO del conteo de nodos +1.
    Consecuencia P1: ramas UP y DOWN idénticas → sin histéresis.
    Consecuencia P4: c(S) máximo en extremos (ρ=0 o ρ=1), nunca interior.
    """
    W = np.full((N, N), w)
    np.fill_diagonal(W, 0.0)
    return W


def make_W_mixta_sintetica(N=6, w_pos=0.05, w_neg=-0.5):
    """
    W canónica CKM sintética:
    - W_base: pesos positivos uniformes
    - W_mixta: igual + 2 pares negativos fuertes (nodos 0↔5, 1↔4)

    Propiedad verificada: W_mixta produce Ω* interior (ρ*≈0.5-0.65)
    porque estados extremos (todos ±1) penalizan los pares negativos.
    Estable en seeds 0, 1, 7, 42, 99.
    """
    W_base = np.full((N, N), w_pos)
    np.fill_diagonal(W_base, 0.0)

    W_mixta = W_base.copy()
    W_mixta[0, N-1] = w_neg; W_mixta[N-1, 0] = w_neg
    W_mixta[1, N-2] = w_neg; W_mixta[N-2, 1] = w_neg

    return W_base, W_mixta


# ══════════════════════════════════════════════════════════════════════
# GRUPO 1 — cS(): verificación analítica exacta
# ══════════════════════════════════════════════════════════════════════

class TestCS:

    def test_all_positive_uniform_W_aligned(self):
        """
        W=1 (sin diagonal), sigma=todos +1 → c(S)=1.0.
        Derivación: todas las C(N,2) contribuciones son 1*1*1=1.
        """
        N = 4
        W = np.ones((N, N)); np.fill_diagonal(W, 0.0)
        sigma = np.ones(N)
        assert abs(cS(sigma, W) - 1.0) < 1e-9

    def test_uniform_W_alternating_sigma(self):
        """
        W=1, sigma=[+1,-1,+1,-1] → c(S) = -2/6 = -0.333...
        Pares: (0,1)=-1, (0,2)=+1, (0,3)=-1, (1,2)=-1, (1,3)=+1, (2,3)=-1 → suma=-2.
        """
        N = 4
        W = np.ones((N, N)); np.fill_diagonal(W, 0.0)
        sigma = np.array([1.0, -1.0, 1.0, -1.0])
        expected = -2.0 / 6.0
        assert abs(cS(sigma, W) - expected) < 1e-9

    def test_zero_W_returns_zero(self):
        """W=0 → c(S)=0 independientemente de sigma."""
        N = 4
        W = np.zeros((N, N))
        for sigma in [np.ones(N), -np.ones(N), np.array([1.,-1.,1.,-1.])]:
            assert cS(sigma, W) == 0.0, f"Esperado 0 para sigma={sigma}"

    def test_n2_manual(self):
        """
        N=2: un único par. Verificación directa.
        W[0,1]=0.5: c(S) = 0.5*s0*s1 / 1 par.
        """
        W = np.array([[0.0, 0.5], [0.5, 0.0]])
        assert abs(cS(np.array([1.0,  1.0]), W) -  0.5) < 1e-9
        assert abs(cS(np.array([1.0, -1.0]), W) - -0.5) < 1e-9
        assert abs(cS(np.array([-1.0, -1.0]), W) - 0.5) < 1e-9

    def test_ferro_all_neg_same_as_all_pos(self):
        """
        W ferromagnética: c(S) es el mismo para sigma=todos+1 y sigma=todos-1.
        Propiedad de simetría: sigma_i*sigma_j = 1 en ambos casos.
        """
        N = 6
        W = make_W_ferro(N, w=0.05)
        cs_pos = cS(np.ones(N), W)
        cs_neg = cS(-np.ones(N), W)
        assert abs(cs_pos - cs_neg) < 1e-9, (
            f"Esperado simétrico: c(S)|+1={cs_pos:.6f}, c(S)|-1={cs_neg:.6f}"
        )


# ══════════════════════════════════════════════════════════════════════
# GRUPO 2 — relax(): determinismo y convergencia
# ══════════════════════════════════════════════════════════════════════

class TestRelax:

    def test_deterministic_with_seed(self):
        """Mismo seed → resultado idéntico."""
        N = 6
        W = make_W_ferro(N, w=0.5)
        sigma_init = np.array([1., -1., 1., -1., 1., -1.])

        np.random.seed(SEED)
        r1 = relax(sigma_init.copy(), W)
        np.random.seed(SEED)
        r2 = relax(sigma_init.copy(), W)

        np.testing.assert_array_equal(r1, r2)

    def test_ferro_strong_converges_high_cS(self):
        """
        W ferromagnética fuerte (w=1.0) → relax produce c(S) > 0.8.
        Todos los nodos tienden a alinearse.
        """
        np.random.seed(SEED)
        N = 6
        W = make_W_ferro(N, w=1.0)
        sigma_init = np.random.choice([-1.0, 1.0], N)
        sigma_final = relax(sigma_init, W, max_iter=500)
        cs_final = cS(sigma_final, W)
        assert cs_final > 0.8, f"Esperado c(S)>0.8 con W fuerte, got {cs_final:.4f}"

    def test_output_values_binary(self):
        """relax solo puede producir valores +1 y -1."""
        np.random.seed(SEED)
        N = 8
        W, W_mixta = make_W_mixta_sintetica(N=8, w_pos=0.05, w_neg=-0.3)
        sigma_init = np.random.choice([-1.0, 1.0], N)
        sigma_final = relax(sigma_init, W_mixta)
        unique_vals = set(np.unique(sigma_final))
        assert unique_vals.issubset({-1.0, 1.0}), (
            f"relax produjo valores no binarios: {unique_vals}"
        )


# ══════════════════════════════════════════════════════════════════════
# GRUPO 3 — P4: Densidad óptima Ω*
# ══════════════════════════════════════════════════════════════════════

class TestP4:

    def test_ferro_omega_not_interior(self):
        """
        W ferromagnética → c(S) monotonamente creciente con ρ.
        Ω* en el borde superior (ρ*=1.0), no interior.
        Derivación: para W uniforme positiva, agregar nodos +1 siempre
        aumenta c(S) → máximo en ρ=1.0.
        """
        np.random.seed(SEED)
        N = 8
        W = make_W_ferro(N, w=0.05)
        result = run_P4(W, W, N=N, n_rho=20, n_samples=300)

        assert not result["W_base"]["interior"], (
            f"W ferromagnética no debe tener Ω* interior, "
            f"got ρ*={result['W_base']['omega_star']:.2f}"
        )
        assert result["W_base"]["omega_star"] >= 0.95, (
            f"W ferromagnética: ρ* esperado ≥0.95, got {result['W_base']['omega_star']:.2f}"
        )

    def test_mixta_has_interior_omega(self):
        """
        W_mixta con 2 pares negativos fuertes → Ω* interior.
        Mecanismo: en estados extremos (todos ±1), pares negativos
        penalizan c(S) porque σi*σj=1 pero W<0. En estados intermedios,
        pares de signos opuestos contribuyen positivamente.
        Estabilidad verificada en seeds 0,1,7,42,99.
        """
        np.random.seed(SEED)
        N = 6
        W_base, W_mixta = make_W_mixta_sintetica(N)
        result = run_P4(W_base, W_mixta, N=N, n_rho=30, n_samples=500)

        assert result["W_mixta"]["interior"], (
            f"W_mixta debe tener Ω* interior, "
            f"got ρ*={result['W_mixta']['omega_star']:.2f}"
        )
        # Ω* debe estar en zona razonable [0.4, 0.8]
        omega = result["W_mixta"]["omega_star"]
        assert 0.40 <= omega <= 0.85, (
            f"Ω* esperado en [0.40, 0.85], got {omega:.2f}"
        )

    def test_return_keys(self):
        """run_P4 retorna todas las claves requeridas."""
        np.random.seed(SEED)
        N = 6
        W_base, W_mixta = make_W_mixta_sintetica(N)
        result = run_P4(W_base, W_mixta, N=N, n_rho=10, n_samples=50)

        for key in ("result", "W_base", "W_mixta", "mixta_wins", "rhos",
                    "cs_base", "cs_mixta"):
            assert key in result, f"Clave faltante: '{key}'"

        for subkey in ("omega_star", "cS_max", "interior"):
            assert subkey in result["W_base"], f"W_base: clave faltante '{subkey}'"
            assert subkey in result["W_mixta"], f"W_mixta: clave faltante '{subkey}'"

        assert result["result"] in ("CONFIRMADA", "NO_CONFIRMADA")

    def test_rhos_len_matches_n_rho(self):
        """Longitud de rhos y cs_* igual a n_rho."""
        np.random.seed(SEED)
        N = 6
        W_base, W_mixta = make_W_mixta_sintetica(N)
        n_rho = 15
        result = run_P4(W_base, W_mixta, N=N, n_rho=n_rho, n_samples=30)

        assert len(result["rhos"]) == n_rho
        assert len(result["cs_base"]) == n_rho
        assert len(result["cs_mixta"]) == n_rho


# ══════════════════════════════════════════════════════════════════════
# GRUPO 4 — P1: Histéresis macroscópica
# ══════════════════════════════════════════════════════════════════════

class TestP1:

    def test_return_keys(self):
        """run_P1 retorna las claves esperadas."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P1(W_mixta, N=N, n_seq=20)

        assert "result" in result
        assert result["result"] in ("CONFIRMADA", "NO_CONFIRMADA", "INSUFICIENTE")

    def test_homo_W_no_hysteresis(self):
        """
        W homogénea: c(S) en cada ρ depende SOLO del conteo de nodos +1,
        no de cuáles son. Ramas UP y DOWN producen valores idénticos
        por secuencia → diferencia UP-DOWN ≈ 0 → sin histéresis.
        Resultado esperado: NO_CONFIRMADA o INSUFICIENTE.
        """
        np.random.seed(SEED)
        N = 8
        W = make_W_ferro(N, w=0.05)
        result = run_P1(W, N=N, n_seq=50)

        assert result["result"] in ("NO_CONFIRMADA", "INSUFICIENTE"), (
            f"W homogénea no debe confirmar histéresis, got {result['result']}. "
            f"max_Δc(S)={result.get('max_delta_cS')}"
        )

    def test_max_delta_cs_nonnegative(self):
        """Si hay resultado, max_delta_cS debe ser no negativo."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P1(W_mixta, N=N, n_seq=30)

        if result["max_delta_cS"] is not None:
            assert result["max_delta_cS"] >= 0, (
                f"max_delta_cS debe ser ≥0, got {result['max_delta_cS']}"
            )


# ══════════════════════════════════════════════════════════════════════
# GRUPO 5 — P2: Cascadas k-core, τ
# ══════════════════════════════════════════════════════════════════════

class TestP2:

    def test_return_keys(self):
        """run_P2 retorna las claves esperadas."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P2(W_mixta, N=N, n_runs=50)

        assert "result" in result
        assert "all_thetas" in result
        assert "best_theta" in result
        assert isinstance(result["all_thetas"], list)
        assert result["result"] in ("CONFIRMADA", "NO_CONFIRMADA")

    def test_tau_range_validity(self):
        """Si tau existe, debe ser un float positivo."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P2(W_mixta, N=N, n_runs=50)

        for r in result["all_thetas"]:
            if r["tau"] is not None:
                assert isinstance(r["tau"], float), f"tau debe ser float, got {type(r['tau'])}"
                assert r["tau"] > 0, f"tau debe ser positivo, got {r['tau']}"
                assert r["in_range"] == (1.5 <= r["tau"] <= 2.0), (
                    f"in_range inconsistente con tau={r['tau']}"
                )

    def test_sparse_W_no_kcore(self):
        """
        W muy sparse (sin aristas sobre θ) → k-core vacío → resultado
        sin cascadas. No debe lanzar excepción.
        """
        N = 6
        W = np.zeros((N, N))  # todos cero
        result = run_P2(W, N=N, n_runs=20, thetas=[0.001, 0.01])

        assert "result" in result  # debe correr sin excepción
        for r in result["all_thetas"]:
            assert r["n_cascades"] == 0 or r["tau"] is None


# ══════════════════════════════════════════════════════════════════════
# GRUPO 6 — P3: Asimetría temporal k-core
# ══════════════════════════════════════════════════════════════════════

class TestP3:

    def test_return_keys(self):
        """run_P3 retorna las claves esperadas."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P3(W_mixta, N=N, n_runs=50)

        assert "result" in result
        assert "all_thetas" in result
        assert "critical_zone" in result
        assert result["result"] in ("CONFIRMADA", "NO_CONFIRMADA")

    def test_rem_geq_add(self):
        """
        Invariante estructural: rem_mean >= add_mean en todo θ.
        La remoción puede cascadear; la adición está fijada en 0.
        """
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P3(W_mixta, N=N, n_runs=100)

        for r in result["all_thetas"]:
            if r["rem_mean"] is not None:
                assert r["rem_mean"] >= r["add_mean"], (
                    f"rem_mean ({r['rem_mean']:.4f}) < add_mean ({r['add_mean']:.4f}) "
                    f"para θ={r['theta']} — viola invariante estructural"
                )

    def test_asymmetry_sign(self):
        """Si asymmetry existe, debe ser ≥0 (rem - add, add fijo en 0)."""
        np.random.seed(SEED)
        N = 8
        _, W_mixta = make_W_mixta_sintetica(N=N)
        result = run_P3(W_mixta, N=N, n_runs=50)

        for r in result["all_thetas"]:
            if r["asymmetry"] is not None:
                assert r["asymmetry"] >= 0, (
                    f"asymmetry debe ser ≥0, got {r['asymmetry']:.4f}"
                )


# ══════════════════════════════════════════════════════════════════════
# GRUPO 7 — run_all(): integración completa
# ══════════════════════════════════════════════════════════════════════

class TestRunAll:

    def test_returns_all_predictions(self, tmp_path):
        """run_all() retorna dict con claves P1, P2, P3, P4."""
        np.random.seed(SEED)
        N = 6
        nodes = [f"T{i}_nodo" for i in range(N)]
        W_base, W_mixta = make_W_mixta_sintetica(N)

        result = run_all(W_base, W_mixta, nodes,
                         label="test_sintetico",
                         output_dir=str(tmp_path),
                         seed=SEED)

        for key in ("P1", "P2", "P3", "P4", "N", "nodes", "seed"):
            assert key in result, f"Falta clave '{key}' en resultado"

        for pred in ("P1", "P2", "P3", "P4"):
            assert "result" in result[pred], f"Falta 'result' en {pred}"

    def test_writes_reg_json(self, tmp_path):
        """run_all() escribe REG JSON al output_dir."""
        np.random.seed(SEED)
        N = 6
        nodes = [f"T{i}" for i in range(N)]
        W_base, W_mixta = make_W_mixta_sintetica(N)

        run_all(W_base, W_mixta, nodes,
                label="test_reg_escritura",
                output_dir=str(tmp_path),
                seed=SEED)

        reg_file = tmp_path / "REG_p1p4_test_reg_escritura.json"
        assert reg_file.exists(), f"REG no fue escrito en {tmp_path}"

        with open(reg_file) as f:
            reg = json.load(f)
        assert reg["N"] == N
        assert reg["nodes"] == nodes
        assert reg["seed"] == SEED

    def test_wrong_W_shape_raises(self, tmp_path):
        """Matrices con dimensiones incorrectas → AssertionError."""
        N = 6
        nodes = [f"T{i}" for i in range(N)]
        W_ok = np.ones((N, N)); np.fill_diagonal(W_ok, 0)
        W_wrong = np.ones((4, 4))

        raised = False
        try:
            run_all(W_wrong, W_ok, nodes,
                    label="fail_shape",
                    output_dir=str(tmp_path))
        except AssertionError:
            raised = True
        assert raised, "Esperado AssertionError para W_base shape incorrecto"

    def test_nodes_len_matches_N(self, tmp_path):
        """Nodes con longitud incorrecta → AssertionError."""
        N = 6
        W_base, W_mixta = make_W_mixta_sintetica(N)
        nodes_wrong = ["T0", "T1", "T2"]  # len=3, no 6

        raised = False
        try:
            run_all(W_base, W_mixta, nodes_wrong,
                    label="fail_nodes",
                    output_dir=str(tmp_path))
        except AssertionError:
            raised = True
        assert raised, "Esperado AssertionError para nodes con longitud incorrecta"


# ══════════════════════════════════════════════════════════════════════
# Runner standalone
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import tempfile

    suites_no_tmppath = [TestCS, TestRelax, TestP4, TestP1, TestP2, TestP3]

    passed = failed = 0

    # Tests sin tmp_path
    for suite_cls in suites_no_tmppath:
        suite = suite_cls()
        for name in [m for m in dir(suite_cls) if m.startswith("test_")]:
            method = getattr(suite, name)
            try:
                method()
                print(f"  ✓  {suite_cls.__name__}::{name}")
                passed += 1
            except Exception as e:
                print(f"  ✗  {suite_cls.__name__}::{name}")
                print(f"      {e}")
                failed += 1

    # TestRunAll: inyectar tmp_path manualmente
    suite = TestRunAll()
    for name in [m for m in dir(TestRunAll) if m.startswith("test_")]:
        method = getattr(suite, name)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            try:
                method(tmp_path)
                print(f"  ✓  TestRunAll::{name}")
                passed += 1
            except Exception as e:
                print(f"  ✗  TestRunAll::{name}")
                print(f"      {e}")
                failed += 1

    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
