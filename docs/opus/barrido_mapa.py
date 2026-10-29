"""Mapa del barrido v33: qué aparece, desaparece o vuelve entre versiones contiguas del paper.

Sin categorías previas, sin interpretar. Herramienta de lectura sobre docs/ (no toca el modelo).
Parámetros declarados abajo: THETA (contención mínima), MIN_TOK, TOKEN, la cadena VERS.
Uso, parado en la raíz del repo:  python barrido_mapa.py 0.6   (CKM_DOCS=docs por defecto)
Corrió el 29 oct 2026 en el contenedor de Opus (Cowork), no en la PC ni en el Codespace.
Ver docs/opus/BARRIDO_v33_29oct2026.md."""
import re, sys, json, os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

BASE = os.environ.get("CKM_DOCS", "docs")
VERS = ["1","2","3","4","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",
        "21","22","23","24","25","26","27","28","29","30","31","32"]
def path(v):
    n = int(v)
    if n <= 27: return f"{BASE}/paper/PAPER_Landscape_Driven_Device_v{v}.md"
    if n == 28: return f"{BASE}/paper/PAPER_Landscape_Driven_Device_v28_borrador.md"
    return f"{BASE}/opus/PAPER_Landscape_Driven_Device_v{v}_borrador_opus.md"

THETA = float(sys.argv[1])                                # sin default: se declara al correr   # contención mínima para "es el mismo bloque"
MIN_TOK = 5                                                # bloques con < MIN_TOK tokens distintos no entran
TOKEN = r"(?u)\b\w\w\w+\b"                                 # tokens de 3+ caracteres, minúsculas

def blocks(text):
    out, head = [], ""
    for raw in re.split(r"\n\s*\n", text):
        b = raw.strip()
        if not b: continue
        for line in b.splitlines():
            if re.match(r"^#{1,6}\s", line): head = line.strip()
        out.append((head, b))
    return out

def headings(text):
    hs = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            t = re.sub(r"[*_`]", "", m.group(2)).strip()
            t = re.sub(r"^(§?\s*[\dA-Za-z]{0,3}(\.\d+)*[.)]?\s+)", "", t) if re.match(r"^§?\s*\d", t) else t
            hs.append(t.lower().strip(" :—-"))
    return hs

docs = {v: open(path(v), encoding="utf-8").read() for v in VERS}
B = {v: blocks(docs[v]) for v in VERS}
allb, owner = [], []
for i, v in enumerate(VERS):
    for j, (h, b) in enumerate(B[v]):
        allb.append(b); owner.append((i, j))
cv = CountVectorizer(token_pattern=TOKEN, lowercase=True, binary=True)
X = cv.fit_transform(allb).tocsr()
sizes = np.asarray(X.sum(1)).ravel()
idx = {i: [] for i in range(len(VERS))}
for g, (i, j) in enumerate(owner): idx[i].append(g)
keep = {i: [g for g in idx[i] if sizes[g] >= MIN_TOK] for i in idx}

# matched[i][k] = para cada bloque de la versión i, ¿tiene par en la versión k?
inter_cache = {}
def has_match(i, k):
    a, b = keep[i], keep[k]
    if not a or not b: return np.zeros(len(a), bool)
    I = (X[a] @ X[b].T).toarray()
    cont = I / sizes[a][:, None]
    return cont.max(1) >= THETA
M = {(i, k): has_match(i, k) for i in range(len(VERS)) for k in range(len(VERS)) if i != k}

rows, gone, back, new = [], [], [], []
for i in range(len(VERS) - 1):
    k = i + 1
    leaves = ~M[(i, k)]
    arrives = ~M[(k, i)]
    n_never, n_later = 0, 0
    for pos in np.where(leaves)[0]:
        later = [m for m in range(k + 1, len(VERS)) if M[(i, m)][pos]]
        g = keep[i][pos]; h, b = B[VERS[i]][owner[g][1]]
        if later:
            n_later += 1
            back.append((VERS[i], VERS[k], VERS[later[0]], h, b))
        else:
            n_never += 1
            gone.append((VERS[i], VERS[k], h, b))
    n_new, n_ret = 0, 0
    for pos in np.where(arrives)[0]:
        earlier = [m for m in range(0, i) if M[(k, m)][pos]]
        g = keep[k][pos]; h, b = B[VERS[k]][owner[g][1]]
        if earlier: n_ret += 1; new.append(("vuelve", VERS[k], VERS[earlier[-1]], h, b))
        else: n_new += 1; new.append(("nuevo", VERS[k], "", h, b))
    rows.append((VERS[i], VERS[k], len(keep[i]), len(keep[k]), int(leaves.sum()), n_never, n_later,
                 int(arrives.sum()), n_new, n_ret))

# títulos
H = {v: set(headings(docs[v])) for v in VERS}
hrows = []
for i in range(len(VERS) - 1):
    a, b = H[VERS[i]], H[VERS[i + 1]]
    out_ = sorted(a - b); in_ = sorted(b - a)
    ret = [t for t in in_ if any(t in H[VERS[m]] for m in range(i))]
    never = [t for t in out_ if not any(t in H[VERS[m]] for m in range(i + 2, len(VERS)))]
    hrows.append((VERS[i], VERS[i + 1], out_, in_, ret, never))

json.dump({"theta": THETA, "rows": rows, "gone": gone, "back": back, "new": new, "hrows": hrows},
          open(f"mapa_theta{THETA}.json", "w", encoding="utf-8"), ensure_ascii=False)
print("theta", THETA)
print("v_k v_k+1 | bloques_k bloques_k+1 | se_van (no_vuelven, vuelven_después) | llegan (nuevos, vuelven)")
for r in rows: print(*r)
print("total se van y no vuelven:", len(gone), "| se van y vuelven:", len(back))
