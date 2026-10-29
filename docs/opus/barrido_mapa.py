"""Mapa del barrido v33: qué aparece, desaparece o vuelve entre versiones contiguas.

Sin categorías previas, sin interpretar. Herramienta de lectura sobre docs/ (no toca el modelo).
Series: "paper" (v1–v32) y "defs" (DEFS v2–v20). Antes de la primera versión hay una v0 vacía,
así todo lo de la primera versión cuenta como "llega".
Parámetros, todos declarados al correr: THETA (contención mínima para "mismo bloque"),
MIN_TOK = 5 (bloques con menos palabras distintas no entran), TOKEN (palabras de 3+ letras).
Uso, parado en la raíz del repo:  python docs/opus/barrido_mapa.py <paper|defs> <theta>
CKM_DOCS apunta a docs/ (por defecto "docs"). Escribe mapa_<serie>_theta<θ>.json en el cwd.
Corrió el 29 oct 2026 en el contenedor de Opus (Cowork), no en la PC ni en el Codespace.
Ver docs/opus/BARRIDO_v33_29oct2026.md."""
import re, sys, json, os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

BASE = os.environ.get("CKM_DOCS", "docs")
SERIE, THETA = sys.argv[1], float(sys.argv[2])
MIN_TOK = 5
TOKEN = r"(?u)\b\w\w\w+\b"

if SERIE == "paper":
    VERS = ["1","2","3","4","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20",
            "21","22","23","24","25","26","27","28","29","30","31","32"]
    def path(v):
        n = int(v)
        if n <= 27: return f"{BASE}/paper/PAPER_Landscape_Driven_Device_v{v}.md"
        if n == 28: return f"{BASE}/paper/PAPER_Landscape_Driven_Device_v28_borrador.md"
        return f"{BASE}/opus/PAPER_Landscape_Driven_Device_v{v}_borrador_opus.md"
elif SERIE == "defs":
    VERS = ["2","7","8","9","10","10_1","12","13","14","15","16","17","18","19","20"]
    def path(v): return f"{BASE}/defs/DEFS_CKM_estado_actual_v{v}.md"
else:
    raise SystemExit("serie: paper | defs")

def blocks(text):
    out, head = [], ""
    for raw in re.split(r"\n\s*\n", text):
        b = raw.strip()
        if not b: continue
        for line in b.splitlines():
            if re.match(r"^#{1,6}\s", line): head = line.strip()
        out.append((head, b))
    return out

docs = {"0": ""}
docs.update({v: open(path(v), encoding="utf-8").read() for v in VERS})
VERS = ["0"] + VERS
B = {v: blocks(docs[v]) for v in VERS}
allb, owner = [], []
for i, v in enumerate(VERS):
    for j, (h, b) in enumerate(B[v]):
        allb.append(b); owner.append((i, j))
cv = CountVectorizer(token_pattern=TOKEN, lowercase=True, binary=True)
X = cv.fit_transform(allb).tocsr()
sizes = np.asarray(X.sum(1)).ravel()
keep = {i: [g for g, (ii, _) in enumerate(owner) if ii == i and sizes[g] >= MIN_TOK] for i in range(len(VERS))}

def has_match(i, k):
    a, b = keep[i], keep[k]
    if not a: return np.zeros(0, bool)
    if not b: return np.zeros(len(a), bool)
    I = (X[a] @ X[b].T).toarray()
    return (I / sizes[a][:, None]).max(1) >= THETA
M = {(i, k): has_match(i, k) for i in range(len(VERS)) for k in range(len(VERS)) if i != k}

rows, gone, back, new = [], [], [], []
for i in range(len(VERS) - 1):
    k = i + 1
    leaves, arrives = ~M[(i, k)], ~M[(k, i)]
    n_never = n_later = n_new = n_ret = 0
    for pos in np.where(leaves)[0]:
        later = [m for m in range(k + 1, len(VERS)) if M[(i, m)][pos]]
        h, b = B[VERS[i]][owner[keep[i][pos]][1]]
        if later: n_later += 1; back.append((VERS[i], VERS[k], VERS[later[0]], h, b))
        else: n_never += 1; gone.append((VERS[i], VERS[k], h, b))
    for pos in np.where(arrives)[0]:
        earlier = [m for m in range(1, i) if M[(k, m)][pos]]
        h, b = B[VERS[k]][owner[keep[k][pos]][1]]
        if earlier: n_ret += 1; new.append(("vuelve", VERS[k], VERS[earlier[-1]], h, b))
        else: n_new += 1; new.append(("nuevo", VERS[k], "", h, b))
    rows.append((VERS[i], VERS[k], len(keep[i]), len(keep[k]), int(leaves.sum()), n_never, n_later,
                 int(arrives.sum()), n_new, n_ret))

json.dump({"serie": SERIE, "theta": THETA, "rows": rows, "gone": gone, "back": back, "new": new},
          open(f"mapa_{SERIE}_theta{THETA}.json", "w", encoding="utf-8"), ensure_ascii=False)
print("serie", SERIE, "theta", THETA)
print("v_k v_k+1 | bloques_k bloques_k+1 | se_van no_vuelven vuelven_después | llegan nuevos vuelven")
for r in rows: print(*r)
print("total: se van y no vuelven", len(gone), "| se van y vuelven", len(back),
      "| llegan nuevos", sum(1 for x in new if x[0] == "nuevo"), "| vuelven", sum(1 for x in new if x[0] == "vuelve"))
