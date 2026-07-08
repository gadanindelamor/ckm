"""
test_w_version.py — Tests: WVersionManager + CorpusService integration

Ejecutar:
    pytest test_w_version.py -v
    python test_w_version.py   # modo standalone
"""

from __future__ import annotations
import sys
import json
import tempfile
import os
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from w_version import WVersionManager, WTracePoint, sha256_W

try:
    import pytest
    HAS_PYTEST = True
except ImportError:
    HAS_PYTEST = False


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_W(N=4, seed=0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    W = rng.uniform(-0.5, 0.5, (N, N))
    W = (W + W.T) / 2
    np.fill_diagonal(W, 0.0)
    return W


# ---------------------------------------------------------------------------
# Tests WVersionManager
# ---------------------------------------------------------------------------

def test_register_creates_trace():
    """register() crea una marca con sha correcto."""
    vm = WVersionManager()
    W = make_W()
    sha = vm.register(W, corpus_size=10)

    assert len(vm) == 1
    assert sha == sha256_W(W)
    assert vm.current_sha() == sha
    assert vm.history()[0].corpus_size == 10
    assert vm.history()[0].causal_event == "rebuild"


def test_register_no_duplicate_on_same_W():
    """register() con W idéntica no crea marca duplicada."""
    vm = WVersionManager()
    W = make_W()
    vm.register(W, corpus_size=10)
    vm.register(W, corpus_size=10)

    assert len(vm) == 1


def test_register_new_mark_on_changed_W():
    """register() crea segunda marca cuando W cambia."""
    vm = WVersionManager()
    W1 = make_W(seed=0)
    W2 = make_W(seed=1)

    vm.register(W1, corpus_size=10)
    vm.register(W2, corpus_size=20)

    assert len(vm) == 2
    assert vm.history()[0].sha256 != vm.history()[1].sha256
    assert vm.current_corpus_size() == 20


def test_changed_since():
    """changed_since() detecta cambio de W."""
    vm = WVersionManager()
    W1 = make_W(seed=0)
    W2 = make_W(seed=1)

    sha1 = vm.register(W1, corpus_size=10)
    assert not vm.changed_since(sha1)

    vm.register(W2, corpus_size=20)
    assert vm.changed_since(sha1)
    assert not vm.changed_since(vm.current_sha())


def test_initial_state():
    """Estado inicial: sin registros."""
    vm = WVersionManager()
    assert vm.current_sha() is None
    assert vm.current_corpus_size() is None
    assert len(vm) == 0
    assert vm.changed_since("cualquier-sha") is True


def test_serialization_roundtrip():
    """to_list() / from_list() preservan el historial."""
    vm = WVersionManager()
    vm.register(make_W(seed=0), corpus_size=10)
    vm.register(make_W(seed=1), corpus_size=20)

    data = vm.to_list()
    vm2 = WVersionManager()
    vm2.from_list(data)

    assert vm2.current_sha() == vm.current_sha()
    assert len(vm2) == len(vm)
    assert vm2.history()[0].corpus_size == 10
    assert vm2.history()[1].corpus_size == 20


# ---------------------------------------------------------------------------
# Tests integración con CorpusService
# ---------------------------------------------------------------------------

def test_corpus_service_w_sha_after_ingest():
    """CorpusService expone w_sha en status() y vía w_sha() tras ingest()."""
    from corpus_service import CorpusService

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name
    try:
        corpus = CorpusService(storage_path=tmp, min_texts=3, top_k=5)
        assert corpus.w_sha() is None

        texts = [
            "gun control reduces violence",
            "the second amendment protects rights",
            "background checks prevent crime",
        ]
        status = corpus.ingest(texts)

        assert status["w_sha"] is not None
        assert corpus.w_sha() == status["w_sha"]
        assert len(status["w_sha"]) == 64   # sha256 hex
    finally:
        os.unlink(tmp)


def test_corpus_service_sha_changes_when_W_changes():
    """sha cambia cuando W se reconstruye con nuevos textos."""
    from corpus_service import CorpusService

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name
    try:
        corpus = CorpusService(storage_path=tmp, min_texts=3, top_k=5)
        corpus.ingest([
            "gun control reduces violence",
            "the second amendment protects rights",
            "background checks prevent crime",
        ])
        sha1 = corpus.w_sha()

        corpus.ingest([
            "i disagree — armed citizens deter crime",
            "mental health is the real issue not guns",
            "assault weapons bans save lives however",
        ])
        sha2 = corpus.w_sha()

        assert sha1 != sha2
        assert corpus.w_changed_since(sha1)
        assert not corpus.w_changed_since(sha2)
    finally:
        os.unlink(tmp)


def test_corpus_service_sha_persists_across_sessions():
    """w_sha persiste en JSON y se restaura en nueva instancia."""
    from corpus_service import CorpusService

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp = f.name
    try:
        c1 = CorpusService(storage_path=tmp, min_texts=3, top_k=5)
        c1.ingest([
            "gun control reduces violence",
            "the second amendment protects rights",
            "background checks prevent crime",
        ])
        sha_original = c1.w_sha()

        # nueva instancia — carga desde JSON
        c2 = CorpusService(storage_path=tmp, min_texts=3, top_k=5)
        assert c2.w_sha() == sha_original
    finally:
        os.unlink(tmp)


# ---------------------------------------------------------------------------
# Runner standalone
# ---------------------------------------------------------------------------

def run_all():
    tests = [
        test_register_creates_trace,
        test_register_no_duplicate_on_same_W,
        test_register_new_mark_on_changed_W,
        test_changed_since,
        test_initial_state,
        test_serialization_roundtrip,
        test_corpus_service_w_sha_after_ingest,
        test_corpus_service_sha_changes_when_W_changes,
        test_corpus_service_sha_persists_across_sessions,
    ]
    passed = 0
    failed = 0
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
