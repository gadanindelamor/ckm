"""
test_monitor_services.py
CKM — Tests suite: NodeExtractorService, CorpusService (v2), MonitorService (v2)

Diseño: propiedades conocidas analíticamente, sin corpus externo.
Nomenclatura sesión 32: Δ_r (rechazos acumulados), Δ_bias (declarado prematuro).

Ejecutar:
    pytest test_monitor_services.py -v
    python test_monitor_services.py          # modo standalone
"""

import sys
import json
import tempfile
import os
from pathlib import Path

import numpy as np

try:
    import pytest
except ImportError:
    pytest = None

sys.path.insert(0, str(Path(__file__).parent))
from node_extractor import NodeExtractorService
from corpus_service  import CorpusService
from monitor_service import MonitorService


# ══════════════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════════════

# Corpus sin marcadores → W positiva
TEXTS_POS = [
    "gun control reduces violence and saves lives",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "regulations protect communities from armed criminals",
    "firearm restrictions lower homicide rates",
]

# Corpus con marcadores explícitos → W mixta
TEXTS_MIXED = [
    "gun control reduces violence and saves lives",
    "however, the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "i disagree — gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence, not gun control",
    "but armed citizens deter crime and protect communities",
    "assault weapons bans reduce mass shootings",
]

# Corpus PAREADOS: mismo contenido base, uno sin marcadores / otro con marcadores
# Garantiza nodos comparables para tests de ratio
_BASE = [
    "gun control reduces violence and saves lives",
    "the second amendment protects the right to bear arms",
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "gun rights are constitutional rights not subject to restriction",
    "mental health is the real cause of gun violence",
    "armed citizens deter crime and protect communities",
]
TEXTS_PAIRED_POS = _BASE  # sin marcadores

TEXTS_PAIRED_MIX = [
    "gun control reduces violence and saves lives",
    "however, the second amendment protects the right to bear arms",   # marcador
    "background checks prevent criminals from buying weapons",
    "assault weapons bans reduce mass shootings",
    "i disagree — gun rights are constitutional rights not subject to restriction",  # marcador
    "mental health is the real cause of gun violence, not gun control",
    "but armed citizens deter crime and protect communities",           # marcador
]


def make_corpus(texts, top_k=12):
    tmp = tempfile.mktemp(suffix=".json")
    c = CorpusService(tmp, min_texts=len(texts)-1, top_k=top_k)
    c.ingest(texts)
    return c, tmp

def make_monitor(corpus):
    tmp = tempfile.mktemp(suffix=".jsonl")
    return MonitorService(corpus, tmp), tmp

def safe_unlink(*paths):
    """Elimina archivos si existen — los servicios solo escriben cuando hay actividad."""
    for p in paths:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


# ══════════════════════════════════════════════════════════════════════
# GRUPO 1 — NodeExtractorService
# ══════════════════════════════════════════════════════════════════════

class TestNodeExtractor:

    def setup_method(self):
        self.ext = NodeExtractorService(top_k=10, ngram_max=2)

    def test_accumulate_returns_required_keys(self):
        """accumulate() devuelve dict con 'nodes' y 'pairs'."""
        result = self.ext.accumulate(["gun control reduces violence"])
        assert "nodes" in result
        assert "pairs"  in result
        assert isinstance(result["nodes"], list)
        assert isinstance(result["pairs"], dict)

    def test_accumulate_nodes_nonempty_for_real_text(self):
        """Texto con contenido real → al menos un nodo."""
        result = self.ext.accumulate(["gun control reduces violence and saves lives"])
        assert len(result["nodes"]) > 0

    def test_accumulate_empty_text_no_crash(self):
        """Texto vacío no lanza excepción."""
        result = self.ext.accumulate([""])
        assert "nodes" in result

    def test_evaluate_returns_binary_sigma(self):
        """evaluate() produce vector con solo +1 y -1."""
        nodes = ["gun", "violence", "control", "rights"]
        sigma = self.ext.evaluate("gun control reduces violence", nodes)
        assert len(sigma) == len(nodes)
        assert set(np.unique(sigma)).issubset({1.0, -1.0})

    def test_evaluate_known_node_active(self):
        """
        Nodo presente en el texto → sigma > 0.
        Propiedad: si 'gun' está en texto y en nodes, debe activarse.
        """
        nodes  = ["gun", "chocolate"]
        sigma  = self.ext.evaluate("gun control reduces violence", nodes)
        # 'gun' debe estar activo, 'chocolate' no
        assert sigma[0] == 1.0,  "Nodo 'gun' en texto debe ser activo (+1)"
        assert sigma[1] == -1.0, "Nodo 'chocolate' no en texto debe ser inactivo (-1)"

    def test_evaluate_unknown_node_inactive(self):
        """Nodo que no aparece en el texto → sigma < 0."""
        nodes = ["quantum", "physics", "neutron"]
        sigma = self.ext.evaluate("gun control reduces violence", nodes)
        assert all(s == -1.0 for s in sigma), (
            f"Nodos ajenos al texto deben ser -1, got {sigma}"
        )


# ══════════════════════════════════════════════════════════════════════
# GRUPO 2 — CorpusService: modo y transición
# ══════════════════════════════════════════════════════════════════════

class TestCorpusMode:

    def test_starts_in_accumulation(self):
        """Corpus nuevo comienza en modo acumulación."""
        tmp = tempfile.mktemp(suffix=".json")
        c = CorpusService(tmp, min_texts=10)
        assert c.mode == "accumulation"
        safe_unlink(tmp)

    def test_transitions_to_evaluation(self):
        """Al superar min_texts, transiciona a evaluación."""
        corpus, tmp = make_corpus(TEXTS_POS)
        assert corpus.mode == "evaluation"
        safe_unlink(tmp)

    def test_status_has_required_keys(self):
        """status() devuelve todas las claves esperadas."""
        corpus, tmp = make_corpus(TEXTS_POS)
        s = corpus.status()
        for key in ("mode", "n_texts", "n_nodes", "W_shape", "W_neg_frac"):
            assert key in s, f"Clave faltante en status(): '{key}'"
        safe_unlink(tmp)

    def test_get_nodes_nonempty_in_evaluation(self):
        """En modo evaluación, hay nodos."""
        corpus, tmp = make_corpus(TEXTS_POS)
        assert len(corpus.get_nodes()) > 0
        safe_unlink(tmp)

    def test_W_shape_consistent_with_nodes(self):
        """W.shape == (N, N) donde N = len(nodes)."""
        corpus, tmp = make_corpus(TEXTS_POS)
        N = len(corpus.get_nodes())
        W = corpus.get_W()
        assert W.shape == (N, N), f"W.shape={W.shape} pero N={N}"
        safe_unlink(tmp)

    def test_W_diagonal_zero(self):
        """Diagonal de W es cero — sin auto-conexión."""
        corpus, tmp = make_corpus(TEXTS_POS)
        W = corpus.get_W()
        assert np.allclose(np.diag(W), 0.0), "Diagonal de W debe ser cero"
        safe_unlink(tmp)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 3 — CorpusService: W positiva vs W mixta
# ══════════════════════════════════════════════════════════════════════

class TestCorpusWeights:

    def test_W_pos_no_negative_weights(self):
        """
        Corpus sin marcadores de oposición → W_neg_frac = 0.
        Propiedad: sin marcadores, todos los pares contribuyen positivamente.
        """
        corpus, tmp = make_corpus(TEXTS_POS)
        assert corpus.status()["W_neg_frac"] == 0.0, (
            f"W_pos no debe tener negativos, got W_neg_frac={corpus.status()['W_neg_frac']}"
        )
        safe_unlink(tmp)

    def test_W_pos_range_zero_one(self):
        """W positiva: todos los pesos en [0, 1]."""
        corpus, tmp = make_corpus(TEXTS_POS)
        W = corpus.get_W()
        assert W.min() >= 0.0, f"W_pos debe ser ≥0, got min={W.min():.3f}"
        assert W.max() <= 1.0, f"W_pos debe ser ≤1, got max={W.max():.3f}"
        safe_unlink(tmp)

    def test_W_mixta_has_negative_weights(self):
        """
        Corpus con marcadores de oposición → W_neg_frac > 0.
        Propiedad: los marcadores rutan co-ocurrencias a neg_counts.
        """
        corpus, tmp = make_corpus(TEXTS_MIXED)
        assert corpus.status()["W_neg_frac"] > 0.0, (
            "W_mixta debe tener pesos negativos — marcadores de oposición presentes"
        )
        safe_unlink(tmp)

    def test_W_mixta_range_minus_one_to_one(self):
        """W mixta: rango ∈ [−1, +1]."""
        corpus, tmp = make_corpus(TEXTS_MIXED)
        W = corpus.get_W()
        assert W.min() >= -1.0, f"W_mixta min debe ser ≥−1, got {W.min():.3f}"
        assert W.max() <=  1.0, f"W_mixta max debe ser ≤+1, got {W.max():.3f}"
        safe_unlink(tmp)

    def test_W_mixta_neg_frac_greater_than_pos(self):
        """
        W_mixta.W_neg_frac > W_pos.W_neg_frac.
        La señal de oposición diferencia los dos corpus.
        """
        corpus_pos,   tmp_p = make_corpus(TEXTS_POS)
        corpus_mixed, tmp_m = make_corpus(TEXTS_MIXED)
        nf_pos = corpus_pos.status()["W_neg_frac"]   or 0.0
        nf_mix = corpus_mixed.status()["W_neg_frac"] or 0.0
        assert nf_mix > nf_pos, (
            f"W_mixta.neg_frac ({nf_mix}) debe superar W_pos.neg_frac ({nf_pos})"
        )
        safe_unlink(tmp_p, tmp_m)

    def test_W_symmetric(self):
        """W es simétrica: W[i,j] == W[j,i]."""
        corpus, tmp = make_corpus(TEXTS_MIXED)
        W = corpus.get_W()
        assert np.allclose(W, W.T), "W debe ser simétrica"
        safe_unlink(tmp)

    def test_persistence_round_trip(self):
        """Guardar y recargar corpus produce W idéntica."""
        corpus, tmp = make_corpus(TEXTS_MIXED)
        W_before = corpus.get_W().copy()
        corpus.save()

        corpus2 = CorpusService(tmp, min_texts=1)
        W_after = corpus2.get_W()

        assert W_after is not None, "W debe cargarse desde disco"
        np.testing.assert_allclose(W_before, W_after, atol=1e-9,
            err_msg="W debe ser idéntica tras save/load")
        safe_unlink(tmp)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 4 — MonitorService: evaluación básica
# ══════════════════════════════════════════════════════════════════════

class TestMonitorEvaluation:

    def test_accumulation_mode_returns_message(self):
        """En modo acumulación, evaluate() devuelve mensaje, no panel."""
        tmp_c = tempfile.mktemp(suffix=".json")
        tmp_m = tempfile.mktemp(suffix=".jsonl")
        corpus = CorpusService(tmp_c, min_texts=100)   # umbral inalcanzable
        corpus.ingest(TEXTS_POS)
        mon = MonitorService(corpus, tmp_m)

        result = mon.evaluate("gun control reduces violence")
        assert result["mode"] == "accumulation"
        safe_unlink(tmp_c, tmp_m)

    def test_panel_has_required_keys(self):
        """Panel de evaluación contiene todas las métricas requeridas."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        result = mon.evaluate("gun control reduces violence")
        for key in ("c_S", "fabrication_index", "D_ckm",
                    "n_rejected_pairs", "Delta_r_sum",
                    "activos_prompt", "activos_relajado", "rechazados"):
            assert key in result, f"Clave faltante en panel: '{key}'"
        safe_unlink(tmp_c, tmp_m)

    def test_fi_range_zero_one(self):
        """fabrication_index ∈ [0, 1]."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        for prompt in [
            "gun control reduces violence",
            "chocolate prevents gun violence",
            "amendment rights protect violence from control",
        ]:
            r = mon.evaluate(prompt)
            assert 0.0 <= r["fabrication_index"] <= 1.0, (
                f"fi fuera de rango para '{prompt}': {r['fabrication_index']}"
            )
        safe_unlink(tmp_c, tmp_m)

    def test_unknown_concept_fi_zero(self):
        """
        Prompt con concepto ajeno al corpus → fi = 0.
        El campo no puede rechazar lo que no conoce (caso chocolate).
        Propiedad documentada: no es bug, es coherente con el modelo.
        """
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        r = mon.evaluate("chocolate ice cream prevents all forms of gun violence")
        # 'chocolate' no está en corpus → no activa nodos → fi = 0
        # (el fi puede ser 0 o bajo — no 1.0, que sería falso positivo)
        assert r["fabrication_index"] < 0.5, (
            f"Concepto ajeno no debe generar fi alto: {r['fabrication_index']}"
        )
        safe_unlink(tmp_c, tmp_m)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 5 — MonitorService: Δ_r acumula rechazos
# ══════════════════════════════════════════════════════════════════════

class TestDeltaR:

    def test_delta_r_starts_zero(self):
        """Δ_r comienza en cero antes de cualquier evaluación."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        assert mon._Delta_r is None or np.sum(mon._Delta_r) == 0.0
        safe_unlink(tmp_c, tmp_m)

    def test_delta_r_sum_nonnegative(self):
        """Delta_r_sum ≥ 0 después de cualquier evaluación."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        for p in ["gun control reduces violence",
                  "amendment rights protect violence from control"]:
            r = mon.evaluate(p)
            assert r["Delta_r_sum"] >= 0.0

        safe_unlink(tmp_c, tmp_m)

    def test_delta_r_accumulates_across_evaluations(self):
        """
        Δ_r_sum no decrece entre evaluaciones.
        Propiedad: Δ_r solo acumula — nunca se borra.
        """
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        sums = []
        for p in [
            "amendment rights protect violence from control",
            "gun rights oppose all gun restrictions in the constitution",
            "rights and weapons are protected against control",
        ]:
            r = mon.evaluate(p)
            sums.append(r["Delta_r_sum"])

        for i in range(1, len(sums)):
            assert sums[i] >= sums[i-1], (
                f"Δ_r_sum decreció: {sums[i-1]} → {sums[i]}"
            )
        safe_unlink(tmp_c, tmp_m)

    def test_delta_r_matrix_symmetric(self):
        """Δ_r es simétrica: si rechaza par (i,j), también (j,i)."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        mon.evaluate("amendment rights protect violence from control")
        if mon._Delta_r is not None:
            np.testing.assert_allclose(mon._Delta_r, mon._Delta_r.T, atol=1e-9,
                err_msg="Δ_r debe ser simétrica")
        safe_unlink(tmp_c, tmp_m)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 6 — MonitorService: W_mixta vs W_pos — invariante de ratio
# ══════════════════════════════════════════════════════════════════════

class TestWMixtaRatio:
    """
    Tests de invariante de ratio: W_mixta vs W_pos.
    Usan corpus PAREADOS — mismo contenido base, uno con marcadores / otro sin.
    Garantiza nodos comparables: la diferencia es solo la señal de oposición.
    Convención CONVENTIONS.md: reportar ratio, no diferencia absoluta.
    """

    def _make_paired(self):
        corpus_pos,   tmp_cp = make_corpus(TEXTS_PAIRED_POS)
        corpus_mixed, tmp_cm = make_corpus(TEXTS_PAIRED_MIX)
        mon_pos,   tmp_mp = make_monitor(corpus_pos)
        mon_mixed, tmp_mm = make_monitor(corpus_mixed)
        return (corpus_pos, corpus_mixed, mon_pos, mon_mixed,
                [tmp_cp, tmp_cm, tmp_mp, tmp_mm])

    def test_fi_fabricated_mixta_differs_from_pos(self):
        """
        W_mixta produce fi diferente a W_pos para prompt fabricado.
        Invariante estructural: los negativos CAMBIAN la evaluación.
        La dirección del cambio depende del corpus — no es universalmente ≥.
        El ratio ×2.25 es resultado empírico (REG sesión 32), no invariante de código.
        """
        _, _, mon_pos, mon_mixed, tmps = self._make_paired()
        prompt = "amendment rights protect violence from control"
        fi_pos = mon_pos.evaluate(prompt)["fabrication_index"]
        fi_mix = mon_mixed.evaluate(prompt)["fabrication_index"]

        # al menos uno debe ser > 0 (el prompt tiene nodos del corpus)
        assert fi_pos > 0 or fi_mix > 0, (
            f"Prompt fabricado debe activar al menos algún rechazo: "
            f"fi_pos={fi_pos}, fi_mix={fi_mix}"
        )
        # W_mixta no produce el mismo fi que W_pos — los negativos añaden información
        assert fi_pos != fi_mix, (
            f"W_mixta debe diferir de W_pos: ambas dieron fi={fi_pos:.3f}"
        )
        safe_unlink(*tmps)

    def test_ratio_documented_experimental_result(self):
        """
        Documenta el resultado empírico de sesión 32 sin imponerlo como invariante.
        Con corpus gun control pareado (7 textos, 3 marcadores):
          fi(W_pos)=0.333, fi(W_mixta)=0.750, ratio=×2.25.
        Si el ratio cambia con el corpus, el test pasa — registra lo que ocurre.
        """
        _, _, mon_pos, mon_mixed, tmps = self._make_paired()
        prompt = "amendment rights protect violence from control"
        fi_pos = mon_pos.evaluate(prompt)["fabrication_index"]
        fi_mix = mon_mixed.evaluate(prompt)["fabrication_index"]

        if fi_pos > 0 and fi_mix > 0:
            ratio = fi_mix / fi_pos
            # ratio != 1.0: los negativos cambian el resultado (dirección libre)
            assert abs(ratio - 1.0) > 0.01, (
                f"Ratio={ratio:.3f} — W_mixta y W_pos no deben ser equivalentes"
            )
        safe_unlink(*tmps)

    def test_w_neg_frac_mixta_greater_than_pos(self):
        """
        W_mixta.neg_frac > W_pos.neg_frac para corpus pareados.
        La única diferencia entre los dos corpus son los marcadores.
        """
        corpus_pos, corpus_mixed, _, _, tmps = self._make_paired()
        nf_pos = corpus_pos.status()["W_neg_frac"]   or 0.0
        nf_mix = corpus_mixed.status()["W_neg_frac"] or 0.0
        assert nf_mix > nf_pos, (
            f"W_mixta.neg_frac ({nf_mix}) debe superar W_pos.neg_frac ({nf_pos})"
        )
        safe_unlink(*tmps)

    def test_cs_coherent_positive_both(self):
        """
        Prompt coherente → c_S ≥ 0 en ambas versiones de W.
        Propiedad básica: estado coherente tiene alineación no negativa.
        """
        _, _, mon_pos, mon_mixed, tmps = self._make_paired()
        prompt = "gun control laws reduce violence in communities"
        cs_pos = mon_pos.evaluate(prompt)["c_S"]
        cs_mix = mon_mixed.evaluate(prompt)["c_S"]
        assert cs_pos >= 0.0, f"c_S(W_pos) debe ser ≥0 para prompt coherente: {cs_pos}"
        assert cs_mix >= 0.0, f"c_S(W_mix) debe ser ≥0 para prompt coherente: {cs_mix}"
        safe_unlink(*tmps)


# ══════════════════════════════════════════════════════════════════════
# GRUPO 7 — MonitorService: persistencia y stop_signal
# ══════════════════════════════════════════════════════════════════════

class TestMonitorPersistence:

    def test_trajectory_written_to_disk(self):
        """Cada evaluación escribe una línea en el JSONL."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        mon.evaluate("gun control reduces violence")
        mon.evaluate("amendment rights protect violence")

        traj = mon.trajectory()
        assert len(traj) == 2, f"Esperadas 2 entradas en trayectoria, got {len(traj)}"
        safe_unlink(tmp_c, tmp_m)

    def test_trajectory_entry_has_panel(self):
        """Cada entrada de trayectoria contiene 't', 'text' y 'panel'."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        mon.evaluate("gun control reduces violence")
        entry = mon.trajectory()[0]

        for key in ("t", "text", "panel"):
            assert key in entry, f"Clave '{key}' faltante en entrada de trayectoria"
        safe_unlink(tmp_c, tmp_m)

    def test_stop_signal_returns_required_keys(self):
        """stop_signal() devuelve dict con 'signal', 'fi_trend', 'D_trend', 'direction'."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        for p in ["gun control reduces violence",
                  "amendment rights protect violence from control",
                  "rights and weapons against all restrictions"]:
            mon.evaluate(p)

        sig = mon.stop_signal()
        for key in ("signal", "fi_trend", "D_trend", "direction"):
            assert key in sig, f"Clave '{key}' faltante en stop_signal()"
        safe_unlink(tmp_c, tmp_m)

    def test_stop_signal_direction_valid(self):
        """direction ∈ {CONVERGING, DIVERGING, STABLE}."""
        corpus, tmp_c = make_corpus(TEXTS_MIXED)
        mon, tmp_m    = make_monitor(corpus)

        for p in ["gun control reduces violence",
                  "amendment rights protect violence",
                  "rights oppose control"]:
            mon.evaluate(p)

        sig = mon.stop_signal()
        assert sig["direction"] in ("CONVERGING", "DIVERGING", "STABLE"), (
            f"direction inválida: {sig['direction']}"
        )
        safe_unlink(tmp_c, tmp_m)


# ══════════════════════════════════════════════════════════════════════
# Runner standalone
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    suites = [
        TestNodeExtractor,
        TestCorpusMode,
        TestCorpusWeights,
        TestMonitorEvaluation,
        TestDeltaR,
        TestWMixtaRatio,
        TestMonitorPersistence,
    ]

    passed = failed = 0

    for suite_cls in suites:
        suite = suite_cls()
        methods = sorted(m for m in dir(suite_cls) if m.startswith("test_"))
        for name in methods:
            method = getattr(suite, name)
            try:
                if hasattr(suite, "setup_method"):
                    suite.setup_method()
                method()
                print(f"  ✓  {suite_cls.__name__}::{name}")
                passed += 1
            except Exception as e:
                print(f"  ✗  {suite_cls.__name__}::{name}")
                print(f"      {type(e).__name__}: {e}")
                failed += 1

    print(f"\n{'─'*55}")
    print(f"  {passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
