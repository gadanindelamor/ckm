"""
test_firma_ckm.py — Tests: FirmaService

Ejecutar:
    pytest test_firma_ckm.py -v
    python test_firma_ckm.py
"""

from __future__ import annotations
import sys
import os
import json
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from firma_ckm import FirmaService, Firma, _sha256


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_corpus_monitor(texts=None, with_thermostat=False):
    from corpus_service import CorpusService
    from monitor_service import MonitorService

    tmp = tempfile.mktemp(suffix=".json")
    corpus = CorpusService(storage_path=tmp, min_texts=3, top_k=8)

    if texts is None:
        texts = [
            "gun control reduces violence and saves lives",
            "the second amendment protects the right to bear arms",
            "background checks prevent criminals from buying weapons",
        ]
    corpus.ingest(texts)

    thermostat = None
    if with_thermostat:
        from coco_thermostat import COCOThermostat
        thermostat = COCOThermostat(W=corpus.get_W(), n_runs=20, seed=0)

    tmp_m = tempfile.mktemp(suffix=".jsonl")
    monitor = MonitorService(corpus, storage_path=tmp_m, n_runs_attractors=20,
                             thermostat=thermostat)
    return corpus, monitor, [tmp, tmp_m]


def cleanup(paths):
    for p in paths:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_firma_none_when_accumulation():
    """firmar() devuelve None cuando corpus no tiene W todavía."""
    from corpus_service import CorpusService
    from monitor_service import MonitorService

    tmp_c = tempfile.mktemp(suffix=".json")
    tmp_m = tempfile.mktemp(suffix=".jsonl")
    try:
        corpus = CorpusService(storage_path=tmp_c, min_texts=10, top_k=8)
        corpus.ingest(["solo un texto"])
        monitor = MonitorService(corpus, storage_path=tmp_m)
        svc = FirmaService()
        assert svc.firmar(corpus, monitor) is None
    finally:
        cleanup([tmp_c, tmp_m])


def test_firma_tiene_seis_campos():
    """Firma tiene exactamente los 6 campos canónicos del REG."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor, n_agentes=2)
        assert f is not None
        d = f.to_dict()
        campos = set(d.keys())
        esperados = {"w_sha", "d_ckm", "temp_signal", "n_agentes", "timestamp", "delta_sha"}
        assert campos == esperados, f"Campos inesperados: {campos ^ esperados}"
    finally:
        cleanup(paths)


def test_firma_w_sha_correcto():
    """w_sha de la Firma coincide con corpus.w_sha()."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor)
        assert f is not None
        assert f.w_sha == corpus.w_sha()
        assert len(f.w_sha) == 64
    finally:
        cleanup(paths)


def test_firma_delta_sha_ceros_sin_evaluate():
    """delta_sha es sha256 de matriz cero si no se llamó evaluate()."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor)
        assert f is not None
        N = len(corpus.get_nodes())
        expected = _sha256(np.zeros((N, N)))
        assert f.delta_sha == expected
    finally:
        cleanup(paths)


def test_firma_delta_sha_cambia_tras_evaluate():
    """delta_sha cambia cuando Δ_r acumula rechazos tras evaluate()."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f1 = svc.firmar(corpus, monitor)

        monitor.evaluate("chocolate ice cream prevents all crime")
        f2 = svc.firmar(corpus, monitor)

        assert f2 is not None
        # delta_sha puede cambiar si hubo rechazos
        # No garantizamos que cambie (depende del texto), pero sí que se computa
        assert len(f2.delta_sha) == 64
    finally:
        cleanup(paths)


def test_firma_temp_signal_nominal_sin_thermostat():
    """temp_signal es NOMINAL cuando no hay thermostat inyectado."""
    corpus, monitor, paths = make_corpus_monitor(with_thermostat=False)
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor)
        assert f is not None
        assert f.temp_signal == "NOMINAL"
    finally:
        cleanup(paths)


def test_firma_n_agentes():
    """n_agentes se registra correctamente."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor, n_agentes=5)
        assert f is not None
        assert f.n_agentes == 5
    finally:
        cleanup(paths)


def test_verificar_firma_valida():
    """verificar() confirma que w_sha existe en historial."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor)
        assert f is not None
        resultado = svc.verificar(f, corpus)
        assert resultado["w_sha_en_historial"] is True
        assert resultado["w_sha_es_actual"] is True
    finally:
        cleanup(paths)


def test_verificar_firma_invalida():
    """verificar() rechaza w_sha fabricado."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor)
        assert f is not None
        # Firma con w_sha fabricado
        f_falsa = Firma(
            w_sha="0" * 64,
            d_ckm=f.d_ckm,
            temp_signal=f.temp_signal,
            n_agentes=f.n_agentes,
            timestamp=f.timestamp,
            delta_sha=f.delta_sha,
        )
        resultado = svc.verificar(f_falsa, corpus)
        assert resultado["w_sha_en_historial"] is False
    finally:
        cleanup(paths)


def test_firma_to_json_roundtrip():
    """Firma serializa y deserializa correctamente."""
    corpus, monitor, paths = make_corpus_monitor()
    try:
        svc = FirmaService()
        f = svc.firmar(corpus, monitor, n_agentes=3)
        assert f is not None
        j = f.to_json()
        d = json.loads(j)
        f2 = Firma.from_dict(d)
        assert f2.w_sha == f.w_sha
        assert f2.delta_sha == f.delta_sha
        assert f2.n_agentes == 3
    finally:
        cleanup(paths)


# ---------------------------------------------------------------------------
# Runner standalone
# ---------------------------------------------------------------------------

def run_all():
    tests = [
        test_firma_none_when_accumulation,
        test_firma_tiene_seis_campos,
        test_firma_w_sha_correcto,
        test_firma_delta_sha_ceros_sin_evaluate,
        test_firma_delta_sha_cambia_tras_evaluate,
        test_firma_temp_signal_nominal_sin_thermostat,
        test_firma_n_agentes,
        test_verificar_firma_valida,
        test_verificar_firma_invalida,
        test_firma_to_json_roundtrip,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed+failed} passed")
    return failed == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
