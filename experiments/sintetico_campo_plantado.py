"""
sintetico_campo_plantado.py — CP6 de TASK_tests_instrumento_v1

**El patrón de respuesta conocida.** No es un test unitario: es un campo cuyo
signo verdadero se conoce por construcción, ingerido de a poco por el camino
real del repo, para que el instrumento diga qué hace antes de medir el campo.

El campo está FIJO: se planta una vez con seed fija y no cambia en los 30
pasos. Así que **todo salto entre pasos es del instrumento**, por construcción
(delamor, 10 oct: *"el campo no salta, es continuo; las W son
representaciones"*).

## El campo plantado

3 grupos x 6 términos -> N = 18. Dentro de un grupo los términos co-ocurren;
entre grupos se evitan. Cada texto toma 3 a 5 términos de **un solo** grupo y,
con probabilidad `epsilon`, uno ajeno. 30 pasos de 10 textos = 300 textos.

**Signo verdadero:** + para un par del mismo grupo, − para un par de grupos
distintos. Con tres grupos, un triángulo i∈A, j∈B, k∈C tiene (−)(−)(−) = −:
**frustrado por construcción**, y es la respuesta conocida contra la que se
mide.

`epsilon ∈ {0, 0.1}`: con 0 los grupos se evitan de forma perfecta y la
recuperación del signo es trivial desde el primer paso; con 0.1 hay un régimen
donde "desde qué tamaño de corpus" tiene respuesta.

## Lo que se mide en cada paso

- **W del repo** (`CorpusService._rebuild`, el camino real): negativos, índice
  de frustración, triángulos.
- **W de ausencia**, φ y PMI, **calculadas acá y no en `services/`**: fracción
  de pares con el signo verdadero recuperado.
- **‖ΔW‖** entre pasos, en **dos** números (ver más abajo).
- **D_ckm** sobre la W del repo, por **enumeración exacta** de los 2^18 estados.
- **nulo por permutación** del patrón de signos, R = 1000, para cada W.

## Las decisiones de instrumento, declaradas (CP0, aceptadas por delamor 12 oct)

1. **`ngram_max=1`** en el `CorpusService` de este script, para que
   término -> nodo sea la **identidad** y "signo verdadero recuperado" esté
   definido. El default vivo es 2 y **no se toca**: se mide aparte qué fracción
   de nodos son bigramas con `ngram_max=2` y se reporta como contaminación del
   soporte, sin atribuirle signo plantado.
2. **Vocabulario sólo letras y `_`, ≥3 caracteres, no stopword** —
   `token_pattern` del extractor excluye dígitos, así que un término con número
   no tokeniza—, y **verificación programática** de que ningún marcador de
   `_OPPOSITION_MARKERS` es substring de ningún texto generado. Si aparece, se
   reporta: el marcador por substring manda **el texto entero** a `neg_counts` y
   la W del repo dejaría de ser ≥ 0 por el instrumento y no por el teorema.
3. **Índice de frustración con DOS denominadores** y **sin usar la letra `T`**:
   los cuatro `REG_hipotesis_distancia_contextual_*` no definen `T`, y en
   `ckm_topology_module.topological_profile` `T` es el **número de triángulos**,
   que con W ≥ 0 es máximo y no 0. Los dos denominadores son:
     - `idx_no_nulo` — sólo los triángulos con los tres signos ≠ 0. Es la
       convención de `orbit_analytics.seccion_F.frustracion` (función anidada,
       no importable: se reimplementa idéntica acá y se declara).
     - `idx_todos` — sobre **todos** los C(N,3). Hace visible lo que la otra
       esconde: con la W del repo los pares entre grupos valen exactamente 0, y
       los triángulos plantados como frustrados **no entran al conteo** de la
       primera. "0 frustrados" no es "ninguno estaba frustrado".
4. **PMI en dos variantes**: sin suavizar —con el conteo de pares que dan
   `-inf`, que son justo los de co-ocurrencia 0, el caso que interesa— y con
   Laplace α = 0.5 sobre las cuatro celdas de la contingencia. φ sin suavizado,
   y el par con φ = 0 exacto (o indefinido) se cuenta aparte, **sin adjudicarle
   signo**: toda convención que lo adjudique convierte la ausencia en un valor
   (I2).
5. **‖ΔW‖ en dos números**, porque con N variable las dos W no tienen la misma
   forma: `dW_comunes` es la norma de Frobenius relativa sobre los nodos
   comunes a los dos pasos, y `nodos_entraron`/`nodos_salieron` es el cambio de
   **soporte**. Alinear por nombre y devolver un solo número mezcla cambio de
   peso con cambio de soporte.
6. **D_ckm por enumeración exacta** de los 2^18 estados, no por `n_runs`: con
   N = 18 el espacio entra, y la enumeración exacta **es el límite** del modo de
   muestreo natural (uniforme sobre estados) con n_runs -> ∞, no otra cantidad.
   Usa `relax_orbit` y `n_eff` del engine, sin copiarlos. `A0` se fija en el
   primer paso con nodos, como hace `MonitorService._D_ckm`.
   **Sólo se observa: no se conecta `should_rebuild`.**
7. **Nulo por permutación**, el del juguete del 10 oct: se permuta el patrón de
   signos entre los pares **conservando la cantidad de negativos**, R = 1000, y
   se reporta media, sd, z y p del índice de frustración.

## Lo que este script NO hace

No toca `services/` ni el extractor ni el gate (`f96c234`); no arregla nada; no
conecta `should_rebuild`; no decide φ o PMI, ni W separadas o combinadas, ni
sobre qué W juzga el Gatekeeper, ni el signo de Δ — eso es de delamor.
`ckm_topology_module.check_orientability` se **corre y se reporta**, sin tocar
el módulo: es xfail por concepto, y el rojo estricto vive en
`tests/test_orientability_no_mide_balance.py`.

Sin Groq: 0 llamadas. Corre local / Codespace.
"""

from __future__ import annotations

import itertools
import json
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

_RAIZ = Path(__file__).resolve().parent.parent
# `services/` importa plano entre sus módulos (node_extractor, w_version),
# así que van las dos rutas: la raíz para `services.x` y services/ para lo plano.
sys.path.insert(0, str(_RAIZ))
sys.path.insert(0, str(_RAIZ / "services"))

from services.corpus_service import CorpusService, _OPPOSITION_MARKERS
from services.node_extractor import _STOPWORDS
from services.landscape_engine import n_eff, relax_orbit, d_ckm, D_CKM_FORMA
from ckm_topology_module import build_complex, check_orientability

SEED = 20261012
N_GRUPOS = 3
POR_GRUPO = 6
TEXTOS_POR_PASO = 10
PASOS = 30
R_NULO = 1000
THETA_TOPO = 0.0          # aristas con W > 0, el borde natural de build_complex

# Términos inventados: sólo letras, >= 3 caracteres. Que no sean stopwords ni
# contengan un marcador de oposición se VERIFICA abajo, no se supone.
GRUPOS = [
    ["zelmo", "quarin", "delvo", "narsip", "tulvex", "brakon"],
    ["mirquel", "sadrin", "volmek", "ketrix", "palumbo", "yandro"],
    ["grivash", "tembor", "nuxelo", "ravinth", "solmic", "kadrez"],
]

# Relleno: tiene que ser TODO stopword, o entra al vocabulario y compite por el
# top_k. Se verifica.
RELLENO = ["the", "and", "of", "to", "in", "that", "it", "is", "for", "with",
           "as", "on", "by", "at", "from", "this", "an", "be", "are", "was"]


# ── El campo plantado ─────────────────────────────────────────────────────────

def termino_a_grupo() -> dict:
    return {t: g for g, ts in enumerate(GRUPOS) for t in ts}


def signo_verdadero(N_terms: int, t2g: dict, terminos: list) -> np.ndarray:
    """+1 mismo grupo, −1 grupos distintos, 0 en la diagonal. Por construcción."""
    S = np.zeros((N_terms, N_terms))
    for i in range(N_terms):
        for j in range(N_terms):
            if i == j:
                continue
            S[i, j] = 1.0 if t2g[terminos[i]] == t2g[terminos[j]] else -1.0
    return S


def generar(rng, n_textos: int, epsilon: float) -> list:
    """Un texto = 3 a 5 términos de UN grupo (+ con prob. epsilon uno ajeno),
    barajados entre relleno de stopwords."""
    textos = []
    for _ in range(n_textos):
        g = int(rng.integers(N_GRUPOS))
        k = int(rng.integers(3, 6))
        elegidos = list(rng.choice(GRUPOS[g], size=k, replace=False))
        if epsilon > 0 and rng.random() < epsilon:
            otros = [x for gg, ts in enumerate(GRUPOS) if gg != g for x in ts]
            elegidos.append(str(rng.choice(otros)))
        palabras = []
        for t in elegidos:
            palabras.append(str(rng.choice(RELLENO)))
            palabras.append(t)
        palabras.append(str(rng.choice(RELLENO)))
        textos.append(" ".join(palabras))
    return textos


def verificar_vocabulario(textos: list) -> dict:
    """Decisión de instrumento 2: no se supone, se verifica.

    - ningún término es stopword (si lo fuera, no puede ser nodo);
    - ningún marcador de oposición es substring de ningún texto (si lo fuera,
      el texto entero iría a neg_counts y W dejaría de ser >= 0 por el
      instrumento, no por el teorema);
    - todo el relleno es stopword (si no, entra al vocabulario).
    """
    todos = [t for ts in GRUPOS for t in ts]
    terminos_stopword = [t for t in todos if t in _STOPWORDS]
    relleno_no_stopword = [r for r in RELLENO if r not in _STOPWORDS]
    cortos = [t for t in todos if len(t) < 3 or not t.replace("_", "").isalpha()]
    golpes = []
    for k, t in enumerate(textos):
        bajo = t.lower()
        for m in _OPPOSITION_MARKERS:
            if m in bajo:
                golpes.append({"texto": k, "marcador": m, "fragmento": t[:80]})
    return {
        "terminos_que_son_stopword": terminos_stopword,
        "relleno_que_no_es_stopword": relleno_no_stopword,
        "terminos_invalidos_para_token_pattern": cortos,
        "textos_con_marcador": golpes,
        "n_textos_con_marcador": len(golpes),
        "limpio": not (terminos_stopword or relleno_no_stopword or cortos or golpes),
    }


# ── Frustración (idéntica a orbit_analytics.seccion_F.frustracion, con el
#    segundo denominador agregado) ───────────────────────────────────────────

def frustracion(W: np.ndarray) -> dict:
    N = W.shape[0]
    S = np.sign(W)
    tot_no_nulo = fr = 0
    tot_todos = 0
    for i, j, k in itertools.combinations(range(N), 3):
        tot_todos += 1
        a, b, c = S[i, j], S[j, k], S[i, k]
        if a == 0 or b == 0 or c == 0:
            continue
        tot_no_nulo += 1
        if a * b * c < 0:
            fr += 1
    return {
        "frustrados": fr,
        "triangulos_no_nulos": tot_no_nulo,
        "triangulos_todos": tot_todos,
        "idx_no_nulo": (fr / tot_no_nulo) if tot_no_nulo else 0.0,
        "idx_todos": (fr / tot_todos) if tot_todos else 0.0,
    }


_TRI_CACHE: dict = {}


def _indices_triangulos(N: int) -> np.ndarray:
    if N not in _TRI_CACHE:
        _TRI_CACHE[N] = np.array(list(itertools.combinations(range(N), 3)))
    return _TRI_CACHE[N]


def nulo_permutacion(W: np.ndarray, R: int, seed: int) -> dict:
    """Decisión 7: se permuta el patrón de signos entre los pares conservando
    la cantidad de negativos (el nulo del juguete del 10 oct). Vectorizado.

    El índice que se compara es `idx_no_nulo`: el nulo permuta los signos
    existentes, así que el conjunto de triángulos de signo no nulo también se
    permuta, y el denominador del nulo es el del grafo permutado.
    """
    N = W.shape[0]
    tri = _indices_triangulos(N)
    if N < 3:
        return {"R": R, "media": 0.0, "sd": 0.0, "z": None, "p_mayor_igual": None}
    ii, jj = np.triu_indices(N, k=1)
    signos = np.sign(W[ii, jj])
    rng = np.random.default_rng(seed)
    obs = frustracion(W)["idx_no_nulo"]

    idx_par = -np.ones((N, N), dtype=int)
    idx_par[ii, jj] = np.arange(len(ii))
    idx_par[jj, ii] = np.arange(len(ii))
    t_ab = idx_par[tri[:, 0], tri[:, 1]]
    t_bc = idx_par[tri[:, 1], tri[:, 2]]
    t_ac = idx_par[tri[:, 0], tri[:, 2]]

    vals = np.empty(R)
    for r in range(R):
        s = rng.permutation(signos)
        prod = s[t_ab] * s[t_bc] * s[t_ac]
        no_nulo = prod != 0
        n_nn = int(no_nulo.sum())
        vals[r] = (float((prod[no_nulo] < 0).sum()) / n_nn) if n_nn else 0.0
    media, sd = float(vals.mean()), float(vals.std(ddof=1))
    return {
        "R": R,
        "observado": obs,
        "media": media,
        "sd": sd,
        "z": (obs - media) / sd if sd > 0 else None,
        "p_mayor_igual": float((vals >= obs).mean()),
        "p_menor_igual": float((vals <= obs).mean()),
    }


# ── φ y PMI, calculadas acá (no en services/) ─────────────────────────────────

def matriz_presencia(textos: list, terminos: list) -> np.ndarray:
    """Presencia binaria por texto entero — la misma unidad que usa el repo."""
    X = np.zeros((len(textos), len(terminos)))
    for r, t in enumerate(textos):
        bajo = t.lower().split()
        for c, term in enumerate(terminos):
            if term in bajo:
                X[r, c] = 1.0
    return X


def phi(X: np.ndarray) -> np.ndarray:
    """Correlación de Pearson entre columnas binarias. NaN si una columna es
    constante: indefinida, y se cuenta aparte (decisión 4)."""
    with np.errstate(invalid="ignore", divide="ignore"):
        C = np.corrcoef(X, rowvar=False)
    return np.asarray(C, dtype=float)


def pmi(X: np.ndarray, alpha: float | None) -> np.ndarray:
    """PMI = log( p_ij / (p_i p_j) ) sobre presencia por texto.

    `alpha=None` -> sin suavizar: co-ocurrencia 0 da −inf, y esos son justo los
    pares entre grupos. `alpha=0.5` -> Laplace sobre las cuatro celdas de la
    contingencia 2x2 (decisión 4).
    """
    n, N = X.shape
    c11 = X.T @ X
    ci = X.sum(axis=0)
    if alpha is None:
        with np.errstate(divide="ignore", invalid="ignore"):
            p_ij = c11 / n
            p_i = ci / n
            M = np.log(p_ij / np.outer(p_i, p_i))
    else:
        tot = n + 4 * alpha
        c10 = ci[:, None] - c11
        c01 = ci[None, :] - c11
        p_ij = (c11 + alpha) / tot
        p_i = (c11 + c10 + 2 * alpha) / tot      # marginal de i en cada par
        p_j = (c11 + c01 + 2 * alpha) / tot
        with np.errstate(divide="ignore", invalid="ignore"):
            M = np.log(p_ij / (p_i * p_j))
    M = np.asarray(M, dtype=float)
    np.fill_diagonal(M, 0.0)
    return M


def recuperacion_de_signo(M: np.ndarray, S: np.ndarray) -> dict:
    """Fracción de pares con el signo verdadero recuperado.

    Los pares cuyo valor es NaN, ±inf o **exactamente 0** se cuentan aparte y
    **no se adjudican a ningún signo** (decisión 4): adjudicarlos convertiría la
    ausencia en un valor.
    """
    N = M.shape[0]
    ii, jj = np.triu_indices(N, k=1)
    v, s = M[ii, jj], S[ii, jj]
    indef = ~np.isfinite(v)
    cero = np.isclose(v, 0.0) & ~indef
    usable = ~indef & ~cero
    pred = np.sign(v)
    ok = pred == s
    def frac(mask):
        m = mask & usable
        return (float((ok & m).sum()) / int(m.sum())) if m.sum() else None
    pos, neg = s > 0, s < 0
    return {
        "pares": int(len(v)),
        "indefinidos": int(indef.sum()),
        "exactamente_cero": int(cero.sum()),
        "usables": int(usable.sum()),
        "recuperado_total": frac(np.ones_like(usable, dtype=bool)),
        "recuperado_intra_mas": frac(pos),
        "recuperado_entre_menos": frac(neg),
        "n_intra_usables": int((pos & usable).sum()),
        "n_entre_usables": int((neg & usable).sum()),
    }


# ── D_ckm por enumeración exacta ──────────────────────────────────────────────

def n_eff_exacto(W: np.ndarray) -> float:
    """N_eff sobre la medida UNIFORME EXACTA en {−1,+1}^N: se enumeran los 2^N
    estados iniciales, se relaja cada uno con `relax_orbit` del engine y la masa
    de cada órbita es su fracción exacta. Es el límite del modo de muestreo
    natural con n_runs -> ∞, no otra cantidad. `n_eff` es la del engine.
    """
    N = W.shape[0]
    cuenta: dict = {}
    for code in range(1 << N):
        s = np.where(
            ((code >> np.arange(N)) & 1).astype(bool), 1.0, -1.0
        )
        orb = relax_orbit(s, W)[0]
        cuenta[orb] = cuenta.get(orb, 0) + 1
    masas = np.array(sorted(cuenta.values(), reverse=True), dtype=float)
    return float(n_eff(masas / masas.sum()))


# ── ΔW en dos números ─────────────────────────────────────────────────────────

def delta_W(nodos_prev, W_prev, nodos, W) -> dict:
    """Decisión 5: norma sobre los nodos COMUNES, y el cambio de soporte
    aparte. Un solo número mezclaría cambio de peso con cambio de soporte."""
    if W_prev is None:
        return {"dW_comunes": None, "norma_prev": None,
                "nodos_entraron": len(nodos), "nodos_salieron": 0,
                "n_comunes": 0}
    comunes = [x for x in nodos if x in set(nodos_prev)]
    ip = [nodos_prev.index(x) for x in comunes]
    ic = [nodos.index(x) for x in comunes]
    A = W_prev[np.ix_(ip, ip)]
    B = W[np.ix_(ic, ic)]
    na = float(np.linalg.norm(A))
    return {
        "dW_comunes": float(np.linalg.norm(B - A) / na) if na > 0 else None,
        "norma_prev": na,
        "nodos_entraron": len([x for x in nodos if x not in set(nodos_prev)]),
        "nodos_salieron": len([x for x in nodos_prev if x not in set(nodos)]),
        "n_comunes": len(comunes),
    }


# ── Contaminación del soporte con el default vivo (ngram_max=2) ───────────────

def bigramas_con_default(textos: list, top_k: int, tmp: Path) -> dict:
    """Decisión 1: el default vivo es ngram_max=2 y no se toca. Acá se MIDE qué
    fracción de nodos son bigramas con ese default, como contaminación del
    soporte, sin atribuirle signo plantado."""
    cs = CorpusService(storage_path=str(tmp), min_texts=3, top_k=top_k,
                       ngram_max=2)
    cs.ingest(list(textos))
    nodos = cs.status().get("nodes") or cs._nodes or []
    bi = [x for x in nodos if " " in x]
    return {"N": len(nodos), "bigramas": len(bi),
            "frac_bigramas": (len(bi) / len(nodos)) if nodos else None,
            "ejemplos": bi[:8]}


# ── Corrida ───────────────────────────────────────────────────────────────────

def corrida(epsilon: float, pasos: int, exacto: bool, tmpdir: Path) -> dict:
    terminos = [t for ts in GRUPOS for t in ts]
    t2g = termino_a_grupo()
    S_true = signo_verdadero(len(terminos), t2g, terminos)

    rng = np.random.default_rng(SEED)
    todos_textos = generar(rng, pasos * TEXTOS_POR_PASO, epsilon)
    verif = verificar_vocabulario(todos_textos)

    estado = tmpdir / f"campo_eps{epsilon}.json"
    if estado.exists():
        estado.unlink()
    cs = CorpusService(storage_path=str(estado), min_texts=3,
                       top_k=len(terminos), ngram_max=1)

    filas = []
    nodos_prev, W_prev, A0 = None, None, None
    for p in range(1, pasos + 1):
        lote = todos_textos[(p - 1) * TEXTOS_POR_PASO: p * TEXTOS_POR_PASO]
        cs.ingest(list(lote))
        nodos = list(cs._nodes or [])
        W = cs._W if cs._W is not None else np.zeros((0, 0))
        acum = todos_textos[: p * TEXTOS_POR_PASO]

        fila = {
            "paso": p, "n_textos": len(acum), "N": len(nodos),
            "nodos_no_plantados": [x for x in nodos if x not in t2g],
            "W_negativos": int((W < 0).sum()) if W.size else 0,
            "W_ceros_fuera_diag": (int((W == 0).sum()) - W.shape[0]) if W.size else 0,
        }

        # frustración de la W del repo, sobre el signo verdadero alineado
        if W.size:
            fila["frustracion_repo"] = frustracion(W)
            fila["nulo_repo"] = nulo_permutacion(W, R_NULO, SEED + p)
            G, edges, tris = build_complex(W, nodos, THETA_TOPO)
            fila["topologia_repo"] = {
                "theta": THETA_TOPO, "E": len(edges), "triangulos": len(tris),
                "orientabilidad": check_orientability(edges, tris),
            }
        else:
            fila["frustracion_repo"] = None
            fila["nulo_repo"] = None
            fila["topologia_repo"] = None

        # φ y PMI sobre los 18 términos plantados (identidad término -> nodo)
        X = matriz_presencia(acum, terminos)
        medidas = {
            "phi": phi(X),
            "pmi_sin_suavizar": pmi(X, None),
            "pmi_laplace_0_5": pmi(X, 0.5),
        }
        fila["ausencia"] = {}
        for nom, M in medidas.items():
            Mf = np.where(np.isfinite(M), M, 0.0)
            fila["ausencia"][nom] = {
                "recuperacion": recuperacion_de_signo(M, S_true),
                "frustracion": frustracion(Mf),
                "nulo": nulo_permutacion(Mf, R_NULO, SEED + 1000 + p),
                "negativos": int((np.triu(Mf, 1) < 0).sum()),
            }

        # ΔW en dos números
        fila["delta_W"] = delta_W(nodos_prev, W_prev, nodos, W)
        nodos_prev, W_prev = nodos, (W.copy() if W.size else None)

        # D_ckm exacto sobre la W del repo
        if exacto and W.size and len(nodos) >= 2:
            t0 = time.perf_counter()
            ne = n_eff_exacto(W)
            if A0 is None:
                A0 = ne
            fila["D_ckm"] = {
                "N_eff_exacto": ne, "N_eff0": A0,
                "D_ckm": d_ckm(ne, A0), "forma": D_CKM_FORMA,
                "medida": "uniforme exacta sobre 2^N estados",
                "segundos": round(time.perf_counter() - t0, 2),
            }
        else:
            fila["D_ckm"] = None

        filas.append(fila)
        f = fila["frustracion_repo"] or {}
        d = fila["D_ckm"] or {}
        rec = fila["ausencia"]["phi"]["recuperacion"]
        print(f"  eps={epsilon}  paso {p:>2}  N={fila['N']:>2}  "
              f"W<0={fila['W_negativos']:>3}  "
              f"frustr={f.get('frustrados', 0):>3}/"
              f"{f.get('triangulos_no_nulos', 0):>3}(no nulo)/"
              f"{f.get('triangulos_todos', 0):>3}(todos)  "
              f"phi_entre={rec['recuperado_entre_menos']}  "
              f"D_ckm={d.get('D_ckm')}  "
              f"dW={fila['delta_W']['dW_comunes']}", flush=True)

    return {
        "epsilon": epsilon,
        "verificacion_vocabulario": verif,
        "bigramas_default_vivo": bigramas_con_default(
            todos_textos, len(terminos), tmpdir / f"bi_eps{epsilon}.json"),
        "pasos": filas,
    }


def main() -> None:
    pasos = PASOS
    exacto = True
    if "--smoke" in sys.argv:
        pasos, exacto = 3, False
    out = {
        "script": "experiments/sintetico_campo_plantado.py",
        "cp": "CP6 de TASK_tests_instrumento_v1",
        "seed": SEED,
        "campo": {"grupos": N_GRUPOS, "por_grupo": POR_GRUPO,
                  "N": N_GRUPOS * POR_GRUPO, "terminos": GRUPOS,
                  "textos_por_paso": TEXTOS_POR_PASO, "pasos": pasos},
        "R_nulo": R_NULO,
        "corridas": [],
    }
    with tempfile.TemporaryDirectory() as td:
        for eps in (0.0, 0.1):
            print(f"\n═══ epsilon = {eps} ═══", flush=True)
            out["corridas"].append(corrida(eps, pasos, exacto, Path(td)))

    destino = Path(__file__).resolve().parent / "sintetico_campo_plantado.json"

    def limpio(o):
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, float) and not np.isfinite(o):
            return None
        return o
    destino.write_text(json.dumps(out, indent=2, ensure_ascii=False, default=limpio))
    print(f"\n{destino}")


if __name__ == "__main__":
    main()
