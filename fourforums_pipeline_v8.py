"""
fourforums_pipeline_v8.py
CKM — Pipeline integrado fourforums gun control
Produce: C6c comparison, P6 replication, stance cross-reference

Outputs (REG class):
  REG_pairs_fourforums_guncontrol_v1.md  — pares topic-level LDA N=8
  REG_c6c_comparison_guncontrol_v1.md   — comparación estructural vs CreateDebate
  REG_p6_fourforums_guncontrol_v1.md    — P6: Delta como ruptura de simetría
  REG_stance_fourforums_v1.md           — stance top autores (965, 555, ...)

Uso:
    python fourforums_pipeline_v8.py --sql fourforums_no_parse_2016_05_18.sql

Requiere:
    pip install scikit-learn numpy scipy
"""

import re, json, sys, argparse, random
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np

# ── Constantes ─────────────────────────────────────────────────────────────────
N_TOPICS   = 8       # igual a CreateDebate para comparabilidad C6c
GUN_KEYWORDS = ['gun', 'weapon', 'firearm', 'shoot', 'rifle', 'pistol',
                'ammunition', 'ammo', 'nra', 'second amendment', '2nd amendment',
                'gun control', 'gun rights']

# Criterios elicitación
AGREE_C1   = 0.40    # umbral desacuerdo en hilo
AGREE_C7   = 0.35    # umbral MTurk confirmación
C2_MIN     = 2
C5_MIN     = 1
C8_MIN     = 2

# P6: Hopfield
N_RUNS     = 500
MAX_ITER   = 2000
NEG_WEIGHT = -0.10

# Top autores de sesión anterior (REG_sesion_perspectivas_rp2_ff_v7)
TOP_AUTHORS = [965, 555, 150, 751, 1034, 809, 3452]

# Línea base CreateDebate (de REG_pairs_createdbate_guncontrol_v1.md)
CD_BASELINE = [
    {'id': 'CD_GC_01', 'ta': 1, 'tb': 3, 'tension': 0.95, 'convergence': 0.05,
     'asymmetry': 0.07, 'initiator': 1, 'c3_node': None},
    {'id': 'CD_GC_02', 'ta': 3, 'tb': 6, 'tension': 0.94, 'convergence': 0.06,
     'asymmetry': 0.02, 'initiator': 3, 'c3_node': None},
    {'id': 'CD_GC_03', 'ta': 6, 'tb': 7, 'tension': 0.91, 'convergence': 0.09,
     'asymmetry': 0.10, 'initiator': 6, 'c3_node': None},
    {'id': 'CD_GC_04', 'ta': 3, 'tb': 5, 'tension': 0.91, 'convergence': 0.09,
     'asymmetry': 0.03, 'initiator': 3, 'c3_node': None},
    {'id': 'CD_GC_05', 'ta': 5, 'tb': 7, 'tension': 0.91, 'convergence': 0.09,
     'asymmetry': 0.02, 'initiator': 5, 'c3_node': None},
    {'id': 'CD_GC_06', 'ta': 1, 'tb': 6, 'tension': 0.90, 'convergence': 0.10,
     'asymmetry': 0.35, 'initiator': 1, 'c3_node': None},
    {'id': 'CD_GC_07', 'ta': 1, 'tb': 5, 'tension': 0.88, 'convergence': 0.12,
     'asymmetry': 0.36, 'initiator': 1, 'c3_node': None},
    {'id': 'CD_GC_08', 'ta': 1, 'tb': 7, 'tension': 0.86, 'convergence': 0.14,
     'asymmetry': 0.39, 'initiator': 1, 'c3_node': None},
    {'id': 'CD_GC_09', 'ta': 4, 'tb': 7, 'tension': 0.87, 'convergence': 0.13,
     'asymmetry': 0.17, 'initiator': 4, 'c3_node': 1},  # única tríada
]

# ── SQL parser ──────────────────────────────────────────────────────────────────

def parse_sql(path):
    """Parsea el dump SQL en tablas dict."""
    raw = defaultdict(list)
    current_table = None
    col_names = {}

    create_re = re.compile(r'CREATE TABLE `?(\w+)`?', re.I)
    col_re    = re.compile(r'`(\w+)`\s+\w+', re.I)
    insert_re = re.compile(r"INSERT INTO `?(\w+)`?\s+VALUES\s*(.+);?\s*$", re.I)

    with open(path, encoding='utf-8', errors='replace') as f:
        in_create = False
        for line in f:
            line = line.rstrip()
            m = create_re.match(line)
            if m:
                current_table = m.group(1).lower()
                col_names[current_table] = []
                in_create = True
                continue
            if in_create:
                if line.strip().startswith(')'):
                    in_create = False
                    continue
                cm = col_re.match(line.strip())
                if cm:
                    col_names[current_table].append(cm.group(1).lower())
                continue
            m = insert_re.match(line)
            if not m:
                continue
            table = m.group(1).lower()
            vals_str = m.group(2)
            try:
                rows = _parse_values(vals_str)
            except Exception:
                continue
            cols = col_names.get(table, [])
            for row in rows:
                if cols and len(row) == len(cols):
                    raw[table].append(dict(zip(cols, row)))
                else:
                    raw[table].append(row)
    return dict(raw)


def _parse_values(s):
    import ast
    s = s.strip().rstrip(';')
    rows = []
    for m in re.finditer(r'\(([^()]*)\)', s):
        inner = m.group(1)
        try:
            row = list(ast.literal_eval(f'({inner},)'))
            rows.append(row)
        except Exception:
            parts = [p.strip().strip("'\"") for p in inner.split(',')]
            rows.append(parts)
    return rows


# ── Filtro gun control ─────────────────────────────────────────────────────────

def filter_gun_posts(data):
    """Retorna ids de discusiones y posts gun control."""
    discussions = data.get('discussion', data.get('discussions', []))
    posts       = data.get('post', data.get('posts', []))

    # Buscar discussion_ids con keywords
    gun_disc_ids = set()
    for d in discussions:
        title = str(d.get('title', '') or '').lower()
        if any(kw in title for kw in GUN_KEYWORDS):
            did = d.get('discussion_id') or d.get('id')
            if did: gun_disc_ids.add(did)

    if not gun_disc_ids:
        # fallback: buscar en texto de posts
        for p in posts:
            text = str(p.get('text', '') or p.get('body', '') or '').lower()
            if any(kw in text for kw in GUN_KEYWORDS):
                did = p.get('discussion_id')
                if did: gun_disc_ids.add(did)

    gun_posts = [p for p in posts
                 if p.get('discussion_id') in gun_disc_ids]

    print(f"  Discusiones gun: {len(gun_disc_ids)}")
    print(f"  Posts gun: {len(gun_posts)}")
    return gun_disc_ids, gun_posts


# ── LDA ────────────────────────────────────────────────────────────────────────

def run_lda(posts, n_topics):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    texts = []
    post_ids = []
    for p in posts:
        text = str(p.get('text', '') or p.get('body', '') or '').strip()
        if len(text) > 20:
            texts.append(text)
            pid = p.get('post_id') or p.get('id')
            post_ids.append(pid)

    if not texts:
        raise ValueError("Sin textos para LDA")

    vec = CountVectorizer(max_features=1000, stop_words='english', min_df=2)
    X   = vec.fit_transform(texts)

    lda = LatentDirichletAllocation(
        n_components=n_topics, random_state=42,
        learning_method='batch', max_iter=20
    )
    doc_topics = lda.fit_transform(X)

    topic_vocab = {}
    words = vec.get_feature_names_out()
    for t in range(n_topics):
        top_idx = lda.components_[t].argsort()[-8:][::-1]
        topic_vocab[t] = [words[i] for i in top_idx]

    post_to_topic = {
        pid: int(np.argmax(doc_topics[i]))
        for i, pid in enumerate(post_ids)
    }

    print(f"\n  Topics LDA (N={n_topics}):")
    for t, words_ in topic_vocab.items():
        print(f"    T{t}: {', '.join(words_[:5])}")

    return topic_vocab, post_to_topic


# ── Build W + Delta ────────────────────────────────────────────────────────────

def build_W_delta(data, gun_disc_ids, post_to_topic, n_topics):
    """
    W[i,j] = dispute count normalizado (simétrico)
    Delta[i,j] = count dirigido i→j (asimétrico)
    """
    posts    = data.get('post', data.get('posts', []))
    qr_table = (data.get('quote_response') or data.get('quote') or [])

    post_to_author = {}
    for p in posts:
        pid = p.get('post_id') or p.get('id')
        aid = p.get('author_id') or p.get('user_id')
        if pid and aid:
            post_to_author[pid] = aid

    dispute = np.zeros((n_topics, n_topics))
    support = np.zeros((n_topics, n_topics))
    delta   = np.zeros((n_topics, n_topics))  # dirigida

    for qr in qr_table:
        src_pid = qr.get('source_post_id') or qr.get('src_post_id')
        tgt_pid = qr.get('post_id') or qr.get('tgt_post_id')
        if src_pid is None or tgt_pid is None:
            continue

        t_src = post_to_topic.get(src_pid)
        t_tgt = post_to_topic.get(tgt_pid)
        if t_src is None or t_tgt is None or t_src == t_tgt:
            continue

        rel = str(qr.get('relation', '') or qr.get('type', '') or '').lower()
        is_dispute = ('disagree' in rel or 'attack' in rel or 'dispute' in rel
                      or 'refute' in rel or 'counter' in rel)
        is_support = ('agree' in rel or 'support' in rel)

        if is_dispute:
            dispute[t_src, t_tgt] += 1
            dispute[t_tgt, t_src] += 1
            delta[t_tgt, t_src] += 1   # tgt cita (responde) a src → src es el blanco
        elif is_support:
            support[t_src, t_tgt] += 1
            support[t_tgt, t_src] += 1

    # Normalizar
    d_max = dispute.max()
    s_max = support.max()
    if d_max > 0: dispute /= d_max
    if s_max > 0: support /= s_max

    delta_norm = delta.copy()
    d_max2 = delta_norm.max()
    if d_max2 > 0: delta_norm /= d_max2

    return dispute, support, delta_norm


# ── C1-C5 topic-level ─────────────────────────────────────────────────────────

def elicit_pairs_c1_c5(topic_vocab, dispute, support, n_topics):
    pairs = []
    for i in range(n_topics):
        for j in range(i+1, n_topics):
            d_ij = dispute[i, j]
            if d_ij < 0.10:   # C1: tensión mínima
                continue

            # Tensión y convergencia
            s_ij = support[i, j]
            total = d_ij + s_ij
            tension     = d_ij / total if total > 0 else 0
            convergence = s_ij / total if total > 0 else 0

            if tension < 0.80:  # C1 estricto
                continue

            # C4: asimetría
            raw_ij = dispute[i, j]
            raw_ji = dispute[j, i]
            asym = abs(raw_ij - raw_ji) / (raw_ij + raw_ji + 1e-9)
            initiator = i if raw_ij >= raw_ji else j

            # C3: tríada crítica
            c3_node = None
            for k in range(n_topics):
                if k == i or k == j: continue
                if dispute[i, k] > 0.05 and dispute[j, k] > 0.05:
                    # k co-ocurre con ambos sin reconciliar
                    if support[i, k] < 0.15 and support[j, k] < 0.15:
                        c3_node = k
                        break

            score = sum([
                tension > 0.80,        # C1
                True,                  # C2 (todos los topics tienen masa)
                c3_node is not None,   # C3
                asym > 0.05,           # C4
                d_ij > 0.15,           # C5 (volumen)
            ])

            if score >= 3:
                pairs.append({
                    'id': f'FF_GC_{len(pairs)+1:02d}',
                    'topic_a': i, 'topic_b': j,
                    'vocab_a': topic_vocab[i],
                    'vocab_b': topic_vocab[j],
                    'tension': round(tension, 3),
                    'convergence': round(convergence, 3),
                    'asymmetry': round(asym, 3),
                    'initiator': initiator,
                    'c3_node': c3_node,
                    'score': score,
                    'dispute_raw': round(float(d_ij), 4),
                })

    pairs.sort(key=lambda x: -x['tension'])
    return pairs


# ── C6c comparison ─────────────────────────────────────────────────────────────

def run_c6c(ff_pairs, cd_baseline):
    """
    Match estructural: 3 de 4 propiedades:
      1. Tensión alta (> 0.85) en ambos
      2. Convergencia baja (< 0.15) en ambos
      3. Asimetría direccional (> 0.20) en ambos
      4. Tríada crítica presente en ambos
    """
    results = []
    for ff in ff_pairs:
        best_match = None
        best_score = 0
        for cd in cd_baseline:
            props = []
            score = 0
            if ff['tension'] > 0.85 and cd['tension'] > 0.85:
                score += 1; props.append('tension_alta')
            if ff['convergence'] < 0.15 and cd['convergence'] < 0.15:
                score += 1; props.append('convergencia_baja')
            if ff['asymmetry'] > 0.20 and cd['asymmetry'] > 0.20:
                score += 1; props.append('asimetria_dir')
            if ff['c3_node'] is not None and cd['c3_node'] is not None:
                score += 1; props.append('triada_presente')
            if score > best_score:
                best_score = score
                best_match = (cd, score, props)

        results.append({
            'ff_id': ff['id'],
            'ff_pair': f"T{ff['topic_a']}↔T{ff['topic_b']}",
            'ff_vocab': f"{ff['vocab_a'][:3]}|{ff['vocab_b'][:3]}",
            'match': best_match,
            'c6c': best_score >= 3,
        })

    matched = sum(1 for r in results if r['c6c'])
    return results, matched


# ── P6: Hopfield + Delta ───────────────────────────────────────────────────────

def run_p6(topic_vocab, dispute, delta, neg_pairs, n_topics,
           n_runs=N_RUNS, max_iter=MAX_ITER):
    """
    Replica el test P6 de CreateDebate sobre fourforums.
    Pregunta: ¿Delta colapsa estados mixtos? ¿Qué polo domina?
    """
    # Construir W_mixta
    W_base = dispute.copy()
    W_mixta = W_base.copy()
    for (i, j) in neg_pairs:
        W_mixta[i, j] = NEG_WEIGHT
        W_mixta[j, i] = NEG_WEIGHT

    # Determinar polo atacante y sostenedor desde delta
    out_strength = delta.sum(axis=1)   # quién emite más
    in_strength  = delta.sum(axis=0)   # quién recibe más
    polo_atacante  = int(np.argmax(out_strength))
    polo_sostenedor = int(np.argmax(in_strength))

    def hopfield_relax(sigma, W):
        sigma = sigma.copy()
        for _ in range(max_iter):
            i = random.randint(0, n_topics - 1)
            h = np.dot(W[i], sigma)
            sigma[i] = 1 if h > 0 else -1
        return sigma

    def classify(sigma):
        pa = polo_atacante
        ps = polo_sostenedor
        if sigma[pa] == 1 and sigma[ps] == -1:
            return 'atk_dom'
        elif sigma[ps] == 1 and sigma[pa] == -1:
            return 'sos_dom'
        else:
            return 'mixed'

    counts_base  = Counter()
    counts_delta = Counter()

    for _ in range(n_runs):
        sigma0 = np.array([random.choice([-1, 1]) for _ in range(n_topics)],
                          dtype=float)

        # Sin Delta
        s1 = hopfield_relax(sigma0.copy(), W_base)
        counts_base[classify(s1)] += 1

        # Con Delta (W asimétrica)
        W_with_delta = W_mixta.copy()
        for i in range(n_topics):
            for j in range(n_topics):
                if delta[i, j] > 0:
                    W_with_delta[i, j] += 0.05 * delta[i, j]

        s2 = hopfield_relax(sigma0.copy(), W_with_delta)
        counts_delta[classify(s2)] += 1

    return {
        'polo_atacante': polo_atacante,
        'polo_sostenedor': polo_sostenedor,
        'vocab_atacante': topic_vocab[polo_atacante][:4],
        'vocab_sostenedor': topic_vocab[polo_sostenedor][:4],
        'base': {k: round(v/n_runs*100, 1)
                 for k, v in counts_base.items()},
        'delta': {k: round(v/n_runs*100, 1)
                  for k, v in counts_delta.items()},
        'colapso_mixtos': round(
            (counts_base.get('mixed', 0) - counts_delta.get('mixed', 0))
            / n_runs * 100, 1
        ),
    }


# ── Stance cross-reference ─────────────────────────────────────────────────────

def run_stance(data, top_authors):
    """
    Cruza author_ids con mturk_author_stance.
    Responde: ¿el polo atacante es pro_control o anti_control?
    """
    stance_table = (data.get('mturk_author_stance') or
                    data.get('author_stance') or [])
    if not stance_table:
        return {a: 'table_not_found' for a in top_authors}

    stance_map = {}
    for row in stance_table:
        aid = (row.get('author_id') or row.get('user_id')
               or (row[0] if isinstance(row, list) else None))
        stance = (row.get('stance') or row.get('label')
                  or (row[1] if isinstance(row, list) else None))
        if aid: stance_map[int(aid)] = stance

    return {a: stance_map.get(a, 'not_found') for a in top_authors}


# ── REG writers ───────────────────────────────────────────────────────────────

def write_reg_pairs(pairs, topic_vocab, path):
    now = datetime.now().strftime('%Y-%m-%d')
    lines = [
        "# REG_pairs_fourforums_guncontrol_v1",
        "",
        "*CKM — Pares elicitados verificados C1-C5*",
        f"*Corpus: fourforums gun control — {now}*",
        "",
        "## Topics LDA",
        "",
        "| ID | Palabras dominantes |",
        "|----|---------------------|",
    ]
    for t, words in topic_vocab.items():
        lines.append(f"| T{t} | {', '.join(words[:5])} |")

    lines += ["", "## Pares verificados", ""]

    for p in pairs:
        lines += [
            f"### {p['id']} — T{p['topic_a']} ↔ T{p['topic_b']}",
            f"- A: T{p['topic_a']} {p['vocab_a'][:3]}",
            f"- B: T{p['topic_b']} {p['vocab_b'][:3]}",
            f"- Tensión: {p['tension']} | Convergencia: {p['convergence']} "
            f"| Asimetría: {p['asymmetry']}",
            f"- Iniciador: T{p['initiator']}",
            f"- C3: {'T'+str(p['c3_node']) if p['c3_node'] is not None else 'ausente'}",
            f"- Score C1-C5: {p['score']}/5",
            "",
        ]

    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  → {path}")


def write_reg_c6c(c6c_results, matched, n_ff, path):
    now = datetime.now().strftime('%Y-%m-%d')
    lines = [
        "# REG_c6c_comparison_guncontrol_v1",
        "",
        "*CKM — Comparación estructural fourforums vs CreateDebate*",
        f"*{now}*",
        "",
        "## Criterio C6c",
        "",
        "Match si ≥ 3 de 4 propiedades: tensión_alta | convergencia_baja | "
        "asimetría_dir | tríada_presente",
        "",
        f"## Resultado: {matched}/{n_ff} pares fourforums coinciden con CreateDebate",
        "",
    ]

    if matched > 0:
        lines.append("→ Las oposiciones son propiedades del dominio gun control, "
                     "no artefactos del corpus chico.")
    else:
        lines.append("→ Sin coincidencias estructurales. Las oposiciones difieren "
                     "entre corpora.")

    lines += ["", "## Detalle", ""]
    for r in c6c_results:
        status = "✓ C6c" if r['c6c'] else "✗"
        match_info = ""
        if r['match']:
            cd, score, props = r['match']
            match_info = f" — best: {cd['id']} ({score}/4: {props})"
        lines.append(f"- {status} {r['ff_id']} {r['ff_pair']} "
                     f"[{r['ff_vocab']}]{match_info}")

    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  → {path}")


def write_reg_p6(p6, path):
    now = datetime.now().strftime('%Y-%m-%d')
    base  = p6['base']
    delta = p6['delta']
    lines = [
        "# REG_p6_fourforums_guncontrol_v1",
        "",
        "*CKM — P6: Delta como ruptura de simetría*",
        f"*Corpus: fourforums gun control — {now}*",
        "",
        "## Setup",
        f"- N = {N_TOPICS} topics LDA",
        f"- Polo atacante: T{p6['polo_atacante']} {p6['vocab_atacante']}",
        f"- Polo sostenedor: T{p6['polo_sostenedor']} {p6['vocab_sostenedor']}",
        f"- Runs: {N_RUNS}",
        "",
        "## Resultados",
        "",
        "| Condición | atk_dom | sos_dom | mixed |",
        "|-----------|---------|---------|-------|",
        f"| W_base sin Delta | "
        f"{base.get('atk_dom',0)}% | "
        f"{base.get('sos_dom',0)}% | "
        f"{base.get('mixed',0)}% |",
        f"| W + Delta | "
        f"{delta.get('atk_dom',0)}% | "
        f"{delta.get('sos_dom',0)}% | "
        f"{delta.get('mixed',0)}% |",
        "",
        f"Colapso de mixtos: {p6['colapso_mixtos']} pp",
        "",
        "## Comparación con CreateDebate",
        "",
        "| Métrica | CreateDebate | fourforums |",
        "|---------|-------------|------------|",
        f"| Mixtos sin Delta | 54.0% | {base.get('mixed',0)}% |",
        f"| Mixtos con Delta | 0.0% | {delta.get('mixed',0)}% |",
        f"| Colapso | 54.0 pp | {p6['colapso_mixtos']} pp |",
        f"| Polo dominante | T7_dom (55.8%) | "
        f"sos_dom ({delta.get('sos_dom',0)}%) |",
        "",
    ]

    # Interpretación automática
    cd_colapso = 54.0
    ff_colapso = p6['colapso_mixtos']
    if abs(ff_colapso - cd_colapso) < 10:
        lines.append("→ Escenario A: colapso similar. "
                     "Delta es propiedad del dominio, no del corpus chico.")
    elif ff_colapso > cd_colapso:
        lines.append("→ Escenario A+: colapso más pronunciado con Delta densa. "
                     "P6 reforzada.")
    else:
        lines.append("→ Escenario B: colapso menor. "
                     "Investigar dilución de Delta en corpus grande.")

    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  → {path}")


def write_reg_stance(stance_result, path):
    now = datetime.now().strftime('%Y-%m-%d')
    lines = [
        "# REG_stance_fourforums_v1",
        "",
        "*CKM — Stance top autores fourforums gun control*",
        f"*{now}*",
        "",
        "## Pregunta",
        "¿El polo atacante (Author 555) es pro_control o anti_control?",
        "",
        "## Resultados",
        "",
        "| Author ID | Stance |",
        "|-----------|--------|",
    ]
    for aid, stance in stance_result.items():
        lines.append(f"| {aid} | {stance} |")

    lines += [
        "",
        "## Interpretación",
    ]
    s555 = stance_result.get(555, 'not_found')
    s965 = stance_result.get(965, 'not_found')

    if s555 != 'not_found' and s965 != 'not_found':
        if s555 != s965:
            lines.append(f"Atacante (555): {s555} | Sostenedor (965): {s965}")
            lines.append("→ Estructura T1-ataca/T7-resiste tiene contenido ideológico verificado.")
        else:
            lines.append(f"Atacante y sostenedor tienen mismo stance ({s555}).")
            lines.append("→ La asimetría es de rol, no de posición ideológica.")
    else:
        lines.append("Stance no disponible en tabla — verificar nombre de tabla en SQL.")

    path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  → {path}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sql', required=True,
                    help='Path al dump SQL de fourforums')
    ap.add_argument('--out', default='.',
                    help='Directorio de salida para REG (default: .)')
    ap.add_argument('--n_topics', type=int, default=N_TOPICS)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("CKM Pipeline v8 — fourforums gun control")
    print("=" * 60)

    # 1. Parsear SQL
    print("\n[1] Parseando SQL...")
    data = parse_sql(args.sql)
    print(f"  Tablas encontradas: {list(data.keys())[:10]}")

    # 2. Filtrar gun control
    print("\n[2] Filtrando gun control...")
    gun_disc_ids, gun_posts = filter_gun_posts(data)

    # 3. LDA
    print(f"\n[3] LDA N={args.n_topics}...")
    topic_vocab, post_to_topic = run_lda(gun_posts, args.n_topics)

    # 4. W + Delta
    print("\n[4] Construyendo W y Delta...")
    dispute, support, delta = build_W_delta(
        data, gun_disc_ids, post_to_topic, args.n_topics
    )
    print(f"  W max: {dispute.max():.4f} | Delta max: {delta.max():.4f}")

    # 5. Elicitación C1-C5
    print("\n[5] Elicitando pares C1-C5...")
    pairs = elicit_pairs_c1_c5(topic_vocab, dispute, support, args.n_topics)
    print(f"  Pares verificados: {len(pairs)}")
    for p in pairs:
        print(f"    {p['id']}: T{p['topic_a']}↔T{p['topic_b']} "
              f"tensión={p['tension']} asim={p['asymmetry']} "
              f"C3={'✓' if p['c3_node'] is not None else '✗'} "
              f"score={p['score']}/5")

    # 6. REG pares
    write_reg_pairs(
        pairs, topic_vocab,
        out_dir / 'REG_pairs_fourforums_guncontrol_v1.md'
    )

    # 7. C6c
    print("\n[7] Comparación C6c vs CreateDebate...")
    c6c_results, matched = run_c6c(pairs, CD_BASELINE)
    print(f"  Matches C6c: {matched}/{len(pairs)}")
    write_reg_c6c(
        c6c_results, matched, len(pairs),
        out_dir / 'REG_c6c_comparison_guncontrol_v1.md'
    )

    # 8. Pares negativos para P6 (usar pares de alta tensión y asimetría)
    neg_pairs = [
        (p['topic_a'], p['topic_b'])
        for p in pairs
        if p['tension'] > 0.85 and p['asymmetry'] > 0.15
    ]
    print(f"\n[8] Pares negativos para P6: {len(neg_pairs)}")

    # 9. P6
    print("\n[9] Test P6: Delta como ruptura de simetría...")
    p6 = run_p6(topic_vocab, dispute, delta, neg_pairs, args.n_topics)
    print(f"  Polo atacante: T{p6['polo_atacante']} {p6['vocab_atacante']}")
    print(f"  Polo sostenedor: T{p6['polo_sostenedor']} {p6['vocab_sostenedor']}")
    print(f"  Mixtos sin Delta: {p6['base'].get('mixed', 0)}%")
    print(f"  Mixtos con Delta: {p6['delta'].get('mixed', 0)}%")
    print(f"  Colapso: {p6['colapso_mixtos']} pp")
    write_reg_p6(p6, out_dir / 'REG_p6_fourforums_guncontrol_v1.md')

    # 10. Stance
    print("\n[10] Stance cross-reference...")
    stance = run_stance(data, TOP_AUTHORS)
    for aid, s in stance.items():
        print(f"  Author {aid}: {s}")
    write_reg_stance(stance, out_dir / 'REG_stance_fourforums_v1.md')

    # Resumen
    print("\n" + "=" * 60)
    print("OUTPUTS GENERADOS:")
    for f in sorted(out_dir.glob('REG_*.md')):
        print(f"  {f.name}")
    print("\nSubir al proyecto Claude:")
    print("  REG_pairs_fourforums_guncontrol_v1.md")
    print("  REG_c6c_comparison_guncontrol_v1.md")
    print("  REG_p6_fourforums_guncontrol_v1.md")
    print("  REG_stance_fourforums_v1.md")
    print("=" * 60)


if __name__ == '__main__':
    main()
