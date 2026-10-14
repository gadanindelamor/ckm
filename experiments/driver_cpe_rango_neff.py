"""
driver_cpe_rango_neff.py — CP-E de TASK_condiciones_del_paper_v1

**Cuánto se mueve N_eff** al variar, **de a una por vez**: `top_k`, el tamaño
del pool, la lista de stopwords, y un texto más con vocabulario ya visto. Con
varias seeds de muestreo, reportando dispersión.

Salida: la tabla *"N_eff estable dentro de este rango, con estas
dependencias"*, para el paper. **No se fija umbral** (lo dice el CP-E).

No arregla nada: mide. No toca `services/` ni el gate (`f96c234`).

## Las tres decisiones de alcance, declaradas

1. **Los corpus** son los **tres independientes** del repo que fijó A.3
   (`tests/test_corpus_del_repo_A3.py`): A24, D12, E7. Los otros tres del
   inventario son prefijos o subconjuntos. Nada de `ckmdatasets`.
2. **El pool no es hoy una perilla independiente:** está cableado en
   `max_features = self.top_k * 3` (`node_extractor.py`). Se varía **desde
   acá**, con una subclase local que sólo cambia ese multiplicador. **El
   servicio no se toca**, y por eso la subclase vive en este archivo.
3. **`nltk` no está instalado** y la lista de 703 está embebida, así que
   "sólo NLTK" no se puede construir ni descomponer. El tercer nivel de
   stopwords es **0**, que es el extremo y acota el rango por abajo.

Que las stopwords se puedan variar sin tocar nada es de **S0b**: se declara
**otro `PerfilDeIdioma`** y el extractor lo recibe.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS      # noqa: E402

from services.node_extractor import (NodeExtractorService,          # noqa: E402
                                     PerfilDeIdioma, PERFIL_ES_EN)
from services.corpus_service import CorpusService                   # noqa: E402
from services.landscape_engine import count_attractors              # noqa: E402

N_RUNS = 1000
SEEDS  = list(range(10))

CORPUS = {
    "A24": RAIZ / "process/experiments/wmixta_paso2_natural/corpus_natural_uniform.json",
    "D12": RAIZ / "iap_chatroom/_state/corpus_state.json",
    "E7" : RAIZ / "process/iap/corpus_state.json",
}


# --------------------------------------------------------------------------
# Las perillas
# --------------------------------------------------------------------------

def perfil_con(stopwords, nombre, origen) -> PerfilDeIdioma:
    """Otro perfil, que es la forma declarada de cambiar los criterios (S0b)."""
    return PerfilDeIdioma(
        nombre=nombre,
        alcance=f"variante del CP-E para medir la dependencia: {origen}",
        token_pattern=PERFIL_ES_EN.token_pattern,
        largo_minimo=PERFIL_ES_EN.largo_minimo,
        lowercase=PERFIL_ES_EN.lowercase,
        normalizacion=PERFIL_ES_EN.normalizacion,
        stopwords=frozenset(stopwords),
        stopwords_origen=origen,
        separador_de_palabras=PERFIL_ES_EN.separador_de_palabras,
    )


PERFILES = {
    703: PERFIL_ES_EN,
    318: perfil_con(ENGLISH_STOP_WORDS, "solo_sklearn_cpe",
                    "318: solo sklearn ENGLISH_STOP_WORDS"),
    0  : perfil_con([], "sin_stopwords_cpe", "0: sin filtrado, el extremo"),
}


class ExtractorConPool(NodeExtractorService):
    """Sólo para el CP-E: hace del multiplicador del pool una perilla.
    `services/` no se toca; el default sigue siendo ×3."""

    def __init__(self, *a, pool_mult: int = 3, **kw):
        super().__init__(*a, **kw)
        self.pool_mult = pool_mult

    def _vectorizer(self, **extra):
        """
        El pool entra por `max_features`, y `accumulate` lo pasa como
        `top_k*3`. Acá se reemplaza **sólo ese valor**: `top_k` sigue siendo el
        real para `_seleccionar`, que es lo que hace que la perilla sea una
        sola. `evaluate` llama sin `max_features` y no se toca.
        """
        if "max_features" in extra:
            extra["max_features"] = self.top_k * self.pool_mult
        return super()._vectorizer(**extra)


def textos_de(ruta: Path) -> list[str]:
    return [t for t in json.loads(ruta.read_text())["texts"] if t and t.strip()]


def un_texto_mas(textos: list[str], perfil=PERFIL_ES_EN) -> str:
    """Un texto armado con vocabulario YA VISTO: los 8 términos más frecuentes."""
    svc = NodeExtractorService(perfil=perfil, ngram_max=1)
    freq: dict[str, int] = {}
    for t in textos:
        for w in set(svc.analizar(t)):
            freq[w] = freq.get(w, 0) + 1
    top = [w for w, _ in sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:8]]
    return " ".join(top)


# --------------------------------------------------------------------------
# La medición
# --------------------------------------------------------------------------

def medir(textos, top_k=20, pool_mult=3, perfil=PERFIL_ES_EN, extra=None) -> dict:
    """W por el camino del repo, y N_eff con 10 seeds. `None` si no hay W."""
    ts = list(textos) + ([extra] if extra else [])
    ex = ExtractorConPool(top_k=top_k, ngram_max=2, perfil=perfil,
                          pool_mult=pool_mult)
    c = CorpusService(storage_path="/dev/null", min_texts=10**9)  # no persiste
    c._extractor = ex
    c._texts = ts
    c._rebuild()
    W = c.get_W()
    if W is None:
        return {"N": 0, "neff": None, "sd": None, "min": None, "max": None}
    vals = [count_attractors(W, n_runs=N_RUNS, seed=s) for s in SEEDS]
    return {
        "N"   : W.shape[0],
        "neff": statistics.mean(vals),
        "sd"  : statistics.stdev(vals),
        "min" : min(vals),
        "max" : max(vals),
    }


def fmt(r: dict) -> str:
    if r["neff"] is None:
        return f"{'sin W':>22}  (N=0)"
    return (f"N={r['N']:>3}  N_eff={r['neff']:6.3f}  sd={r['sd']:5.3f}  "
            f"[{r['min']:.3f}, {r['max']:.3f}]")


def main() -> None:
    print(f"CP-E — rango de estabilidad de N_eff   (n_runs={N_RUNS}, "
          f"{len(SEEDS)} seeds)\n")
    resumen: dict[str, dict] = {}

    for nombre, ruta in CORPUS.items():
        if not ruta.exists():
            print(f"## {nombre}: NO ESTÁ ({ruta}) — se declara y se sigue\n")
            continue
        ts = textos_de(ruta)
        print(f"## {nombre} — {len(ts)} textos")
        base = medir(ts)
        print(f"   base (top_k=20, pool x3, 703 sw)        {fmt(base)}")

        print("   top_k:")
        por_topk = {}
        for k in (10, 15, 20, 25, 32):
            r = medir(ts, top_k=k); por_topk[k] = r
            print(f"     top_k={k:>3}                            {fmt(r)}")

        print("   pool (multiplicador de top_k):")
        por_pool = {}
        for m in (2, 3, 4, 6):
            r = medir(ts, pool_mult=m); por_pool[m] = r
            print(f"     pool x{m}                              {fmt(r)}")

        print("   stopwords:")
        por_sw = {}
        for n, p in PERFILES.items():
            r = medir(ts, perfil=p); por_sw[n] = r
            print(f"     |S|={n:>4}                             {fmt(r)}")

        extra = un_texto_mas(ts)
        r_extra = medir(ts, extra=extra)
        print(f"   un texto más (vocabulario ya visto)     {fmt(r_extra)}")
        print(f"     el texto: {extra!r}\n")

        resumen[nombre] = {"base": base, "top_k": por_topk, "pool": por_pool,
                           "sw": por_sw, "extra": r_extra}

    # ── la tabla para el paper ───────────────────────────────────────────
    print("\n## Cuánto mueve cada perilla  (rango de N_eff / N_eff de la base)")
    print(f"{'corpus':<7}{'seed':>10}{'top_k':>10}{'pool':>10}"
          f"{'stopwords':>12}{'+1 texto':>11}")
    for nombre, d in resumen.items():
        b = d["base"]
        if b["neff"] is None:
            print(f"{nombre:<7}{'sin W en la base':>53}")
            continue
        def rango(rs):
            v = [r["neff"] for r in rs if r["neff"] is not None]
            return (max(v) - min(v)) / b["neff"] if len(v) > 1 else float("nan")
        seed_rel  = (b["max"] - b["min"]) / b["neff"]
        extra_rel = (abs(d["extra"]["neff"] - b["neff"]) / b["neff"]
                     if d["extra"]["neff"] is not None else float("nan"))
        print(f"{nombre:<7}{seed_rel:>10.3f}{rango(d['top_k'].values()):>10.3f}"
              f"{rango(d['pool'].values()):>10.3f}"
              f"{rango(d['sw'].values()):>12.3f}{extra_rel:>11.3f}")

    print("\nNo se fija umbral (CP-E). 'sin W' = el caso límite del paso 5: "
          "empate total en el corte y sin selección anterior -> N=0.")


if __name__ == "__main__":
    main()
