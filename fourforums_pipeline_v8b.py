"""
fourforums_pipeline_v8b.py
Fix: parser SQL robusto + schema real fourforums IAC 2010

Cambios respecto a v8:
  - _parse_values reescrito sin ast.literal_eval
  - parse_sql ahora mapea cols correctamente
  - filter_gun_posts adaptado a tabla 'discussion' real
  - build_W_delta adaptado a 'mturk_2010_p123_post' + 'mturk_2010_p123_entry'

Uso:
    python fourforums_pipeline_v8b.py --sql fourforums_no_parse_2016_05_18.sql
"""

import re, json, sys, argparse, random
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np

# ── Constantes ─────────────────────────────────────────────────────────────────
N_TOPICS   = 8
GUN_KEYWORDS = ['gun', 'weapon', 'firearm', 'shoot', 'rifle', 'pistol',
                'ammunition', 'ammo', 'nra', 'second amendment',
                'gun control', 'gun rights', 'guns']

AGREE_C7   = 0.35
C2_MIN     = 2
C5_MIN     = 1
C8_MIN     = 2
N_RUNS     = 500
MAX_ITER   = 2000
NEG_WEIGHT = -0.10
TOP_AUTHORS = [965, 555, 150, 751, 1034, 809, 3452]

CD_BASELINE = [
    {'id':'CD_GC_01','ta':1,'tb':3,'tension':0.95,'convergence':0.05,'asymmetry':0.07,'initiator':1,'c3_node':None},
    {'id':'CD_GC_02','ta':3,'tb':6,'tension':0.94,'convergence':0.06,'asymmetry':0.02,'initiator':3,'c3_node':None},
    {'id':'CD_GC_03','ta':6,'tb':7,'tension':0.91,'convergence':0.09,'asymmetry':0.10,'initiator':6,'c3_node':None},
    {'id':'CD_GC_04','ta':3,'tb':5,'tension':0.91,'convergence':0.09,'asymmetry':0.03,'initiator':3,'c3_node':None},
    {'id':'CD_GC_05','ta':5,'tb':7,'tension':0.91,'convergence':0.09,'asymmetry':0.02,'initiator':5,'c3_node':None},
    {'id':'CD_GC_06','ta':1,'tb':6,'tension':0.90,'convergence':0.10,'asymmetry':0.35,'initiator':1,'c3_node':None},
    {'id':'CD_GC_07','ta':1,'tb':5,'tension':0.88,'convergence':0.12,'asymmetry':0.36,'initiator':1,'c3_node':None},
    {'id':'CD_GC_08','ta':1,'tb':7,'tension':0.86,'convergence':0.14,'asymmetry':0.39,'initiator':1,'c3_node':None},
    {'id':'CD_GC_09','ta':4,'tb':7,'tension':0.87,'convergence':0.13,'asymmetry':0.17,'initiator':4,'c3_node':1},
]

# ── Parser SQL robusto ─────────────────────────────────────────────────────────

def _tokenize_row(s):
    """Tokeniza una fila VALUES(...) respetando strings con comas internas."""
    tokens = []
    i = 0
    while i < len(s):
        c = s[i]
        if c in (' ', '\t'):
            i += 1
            continue
        if c == ',':
            i += 1
            continue
        if c == "'":
            # string delimitado por comillas simples
            j = i + 1
            buf = []
            while j < len(s):
                if s[j] == '\\' and j+1 < len(s):
                    buf.append(s[j+1])
                    j += 2
                elif s[j] == "'":
                    j += 1
                    break
                else:
                    buf.append(s[j])
                    j += 1
            tokens.append(''.join(buf))
            i = j
        elif s[i:i+4].upper() == 'NULL':
            tokens.append(None)
            i += 4
        else:
            # número u otro literal
            j = i
            while j < len(s) and s[j] not in (',', ')'):
                j += 1
            val = s[i:j].strip()
            try:
                tokens.append(int(val))
            except ValueError:
                try:
                    tokens.append(float(val))
                except ValueError:
                    tokens.append(val)
            i = j
    return tokens


def _split_value_groups(vals_str):
    """Divide la parte VALUES (...),(...) en grupos individuales."""
    groups = []
    depth = 0
    start = None
    for i, c in enumerate(vals_str):
        if c == '(':
            if depth == 0:
                start = i + 1
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0 and start is not None:
                groups.append(vals_str[start:i])
                start = None
    return groups


def parse_sql(path):
    """Parser SQL robusto para dumps MySQL."""
    raw = defaultdict(list)
    col_names = {}
    current_table = None

    create_re = re.compile(r'CREATE TABLE `?(\w+)`?', re.I)
    col_re    = re.compile(r'^\s*`(\w+)`', re.I)
    insert_re = re.compile(r'INSERT INTO `?(\w+)`?\s+(?:VALUES|values)\s*(.+)', re.DOTALL)

    with open(path, encoding='utf-8', errors='replace') as f:
        in_create = False
        for line in f:
            line_s = line.rstrip()

            # CREATE TABLE
            m = create_re.match(line_s)
            if m:
                current_table = m.group(1).lower()
                col_names[current_table] = []
                in_create = True
                continue

            if in_create:
                if re.match(r'\s*\)', line_s):
                    in_create = False
                    continue
                cm = col_re.match(line_s)
                if cm:
                    col_names[current_table].append(cm.group(1).lower())
                continue

            # INSERT INTO
            m = insert_re.match(line_s)
            if not m:
                continue
            table = m.group(1).lower()
            vals_str = m.group(2).rstrip(';')

            cols = col_names.get(table, [])
            for group in _split_value_groups(vals_str):
                try:
                    row = _tokenize_row(group)
                except Exception:
                    continue
                if cols and len(row) == len(cols):
                    raw[table].append(dict(zip(cols, row)))
                elif cols:
                    # mismatch — guardar como dict parcial con índice
                    d = {cols[i]: row[i] for i in range(min(len(cols), len(row)))}
                    raw[table].append(d)
                else:
                    raw[table].append(row)

    return dict(raw)


# ── Explorar schema ─────────────────────────────────────────────────────────────

def explore_schema(data):
    """Imprime schema para diagnosticar tablas disponibles."""
    print("\n  Schema detectado:")
    for tbl, rows in sorted(data.items()):
        if not rows: continue
        first = rows[0]
        if isinstance(first, dict):
            keys = list(first.keys())[:8]
        else:
            keys = [f'col{i}' for i in range(min(len(first), 8))]
        print(f"    {tbl}: {len(rows)} rows | cols: {keys}")


def find_table(data, candidates):
    """Retorna el primer nombre de tabla que existe en data."""
    for c in candidates:
        if c in data and data[c]:
            return c
    return None


# ── Filtrar gun control ─────────────────────────────────────────────────────────

def filter_gun_posts(data):
    # Tabla de discusiones
    disc_tbl = find_table(data, ['discussion', 'discussions'])
    post_tbl = find_table(data, [
        'mturk_2010_p123_post', 'post', 'posts',
        'mturk_post', 'four_forums_post'
    ])

    if disc_tbl is None:
        print("  ERROR: tabla discussion no encontrada")
        print(f"  Tablas disponibles: {list(data.keys())}")
        sys.exit(1)

    discussions = data[disc_tbl]
    print(f"  Tabla discusiones: {disc_tbl} ({len(discussions)} rows)")

    # Mostrar sample para verificar estructura
    if discussions:
        first = discussions[0]
        print(f"  Sample disc: {dict(list(first.items())[:5]) if isinstance(first, dict) else first[:5]}")

    # Buscar campo título
    def get_title(d):
        if isinstance(d, dict):
            for k in ['title', 'topic', 'name', 'subject', 'discussion_title']:
                if k in d: return str(d[k] or '')
            return str(list(d.values())[0] if d else '')
        return str(d[0] if d else '')

    def get_id(d, candidates):
        if isinstance(d, dict):
            for k in candidates:
                if k in d: return d[k]
        return None

    # IDs de discusiones gun
    gun_disc_ids = set()
    for d in discussions:
        title = get_title(d).lower()
        if any(kw in title for kw in GUN_KEYWORDS):
            did = get_id(d, ['discussion_id', 'id', 'disc_id'])
            if did is not None:
                gun_disc_ids.add(did)

    print(f"  Discusiones gun: {len(gun_disc_ids)}")
    if not gun_disc_ids:
        print("  Títulos disponibles (sample 10):")
        for d in discussions[:10]:
            print(f"    {get_title(d)}")

    # Posts
    if post_tbl:
        posts = data[post_tbl]
        print(f"  Tabla posts: {post_tbl} ({len(posts)} rows)")

        def get_disc_id(p):
            if isinstance(p, dict):
                for k in ['discussion_id', 'disc_id', 'thread_id']:
                    if k in p: return p[k]
            return None

        gun_posts = [p for p in posts if get_disc_id(p) in gun_disc_ids]

        if not gun_posts and gun_disc_ids:
            # fallback: buscar por keywords en texto
            def get_text(p):
                if isinstance(p, dict):
                    for k in ['text', 'body', 'content', 'post_text']:
                        if k in p: return str(p[k] or '')
                return ''
            gun_posts = [p for p in posts
                         if any(kw in get_text(p).lower() for kw in GUN_KEYWORDS)]
            print(f"  Posts gun (fallback keyword): {len(gun_posts)}")
        else:
            print(f"  Posts gun: {len(gun_posts)}")
    else:
        print("  WARN: tabla posts no encontrada — usando posts de todas las tablas mturk")
        gun_posts = []
        for tbl_name, rows in data.items():
            if 'post' in tbl_name.lower() and rows:
                gun_posts.extend(rows)
        print(f"  Posts combinados: {len(gun_posts)}")

    return gun_disc_ids, gun_posts


# ── LDA ────────────────────────────────────────────────────────────────────────

def run_lda(posts, n_topics):
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    def get_text(p):
        if isinstance(p, dict):
            for k in ['text', 'body', 'content', 'post_text']:
                if k in p: return str(p[k] or '')
        elif isinstance(p, (list, tuple)) and len(p) > 1:
            return str(p[1] or '')
        return ''

    def get_pid(p):
        if isinstance(p, dict):
            for k in ['post_id', 'id']:
                if k in p: return p[k]
        elif isinstance(p, (list, tuple)):
            return p[0]
        return None

    texts, post_ids = [], []
    for p in posts:
        t = get_text(p)
        if len(t) > 20:
            texts.append(t)
            post_ids.append(get_pid(p))

    if not texts:
        print("  ERROR: sin textos para LDA")
        sys.exit(1)

    print(f"  Textos para LDA: {len(texts)}")

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
        if pid is not None
    }

    print(f"\n  Topics LDA:")
    for t, wds in topic_vocab.items():
        print(f"    T{t}: {', '.join(wds[:5])}")

    return topic_vocab, post_to_topic


# ── Build W + Delta ────────────────────────────────────────────────────────────

def build_W_delta(data, gun_disc_ids, post_to_topic, n_topics):
    # Encontrar tabla de relaciones quote/response
    qr_tbl = find_table(data, [
        'mturk_2010_p123_entry',
        'quote_response', 'quote', 'response',
        'markup', 'mturk_markup'
    ])

    if qr_tbl is None:
        print("  WARN: tabla quote/response no encontrada")
        print(f"  Tablas disponibles: {list(data.keys())}")
        return (np.zeros((n_topics, n_topics)),
                np.zeros((n_topics, n_topics)),
                np.zeros((n_topics, n_topics)))

    qr_rows = data[qr_tbl]
    print(f"  Tabla relaciones: {qr_tbl} ({len(qr_rows)} rows)")
    if qr_rows:
        first = qr_rows[0]
        print(f"  Sample: {dict(list(first.items())[:6]) if isinstance(first, dict) else first[:6]}")

    def get_field(row, candidates, default=None):
        if isinstance(row, dict):
            for k in candidates:
                if k in row: return row[k]
        return default

    dispute = np.zeros((n_topics, n_topics))
    support = np.zeros((n_topics, n_topics))
    delta   = np.zeros((n_topics, n_topics))

    n_matched = 0
    for qr in qr_rows:
        src_pid = get_field(qr, ['src_post_id', 'source_post_id', 'quote_post_id',
                                  'from_post_id', 'post_id_src'])
        tgt_pid = get_field(qr, ['tgt_post_id', 'target_post_id', 'response_post_id',
                                  'to_post_id', 'post_id_tgt', 'post_id'])

        t_src = post_to_topic.get(src_pid)
        t_tgt = post_to_topic.get(tgt_pid)
        if t_src is None or t_tgt is None or t_src == t_tgt:
            continue

        rel = str(get_field(qr, ['relation', 'type', 'label', 'agreement',
                                   'relation_type', 'stance'], '') or '').lower()

        is_dispute = any(x in rel for x in
                        ['disagree', 'attack', 'dispute', 'refute',
                         'counter', 'no', 'against', 'reject'])
        is_support = any(x in rel for x in
                        ['agree', 'support', 'yes', 'for', 'accept'])

        if not is_dispute and not is_support:
            # Intentar por campo numérico de agreement
            agree_val = get_field(qr, ['agree', 'agreement', 'score', 'avg_agreement'])
            if agree_val is not None:
                try:
                    av = float(agree_val)
                    if av < 0.4:   is_dispute = True
                    elif av > 0.6: is_support = True
                except: pass

        if is_dispute:
            dispute[t_src, t_tgt] += 1
            dispute[t_tgt, t_src] += 1
            delta[t_tgt, t_src] += 1
            n_matched += 1
        elif is_support:
            support[t_src, t_tgt] += 1
            support[t_tgt, t_src] += 1
            n_matched += 1

    print(f"  Relaciones mapeadas a topics: {n_matched}")

    if n_matched == 0:
        print("  WARN: 0 relaciones mapeadas. Verificar:")
        print("    1. post_ids en post_to_topic coinciden con src/tgt_post_id")
        print("    2. Campo 'relation' tiene valores reconocibles")
        if qr_rows:
            print(f"    Sample relation field: "
                  f"{[get_field(r, ['relation','type','label','agreement']) for r in qr_rows[:5]]}")

    d_max = dispute.max()
    s_max = support.max()
    dn_max = delta.max()
    if d_max > 0: dispute /= d_max
    if s_max > 0: support /= s_max
    if dn_max > 0: delta /= dn_max

    return dispute, support, delta


# ── C1-C5, C6c, P6, stance — igual que v8 ─────────────────────────────────────

def elicit_pairs_c1_c5(topic_vocab, dispute, support, n_topics):
    pairs = []
    for i in range(n_topics):
        for j in range(i+1, n_topics):
            d_ij = dispute[i, j]
            if d_ij < 0.10: continue
            s_ij = support[i, j]
            total = d_ij + s_ij
            tension     = d_ij / total if total > 0 else 0
            convergence = s_ij / total if total > 0 else 0
            if tension < 0.70: continue
            asym = abs(d_ij - d_ij) / (d_ij + d_ij + 1e-9)
            # asimetría real desde raw counts
            raw_ij = float(dispute[i, j])
            raw_ji = float(dispute[j, i])
            asym = abs(raw_ij - raw_ji) / (raw_ij + raw_ji + 1e-9)
            initiator = i if raw_ij >= raw_ji else j
            c3_node = None
            for k in range(n_topics):
                if k in (i, j): continue
                if dispute[i,k] > 0.05 and dispute[j,k] > 0.05:
                    if support[i,k] < 0.20 and support[j,k] < 0.20:
                        c3_node = k; break
            score = sum([
                tension > 0.70,
                True,
                c3_node is not None,
                asym > 0.05,
                d_ij > 0.10,
            ])
            if score >= 3:
                pairs.append({
                    'id': f'FF_GC_{len(pairs)+1:02d}',
                    'topic_a': i, 'topic_b': j,
                    'vocab_a': topic_vocab.get(i, []),
                    'vocab_b': topic_vocab.get(j, []),
                    'tension': round(tension, 3),
                    'convergence': round(convergence, 3),
                    'asymmetry': round(asym, 3),
                    'initiator': initiator,
                    'c3_node': c3_node,
                    'score': score,
                })
    pairs.sort(key=lambda x: -x['tension'])
    return pairs


def run_c6c(ff_pairs, cd_baseline):
    results = []
    for ff in ff_pairs:
        best_match, best_score = None, 0
        for cd in cd_baseline:
            props, score = [], 0
            if ff['tension'] > 0.80 and cd['tension'] > 0.80:
                score += 1; props.append('tension_alta')
            if ff['convergence'] < 0.20 and cd['convergence'] < 0.20:
                score += 1; props.append('conv_baja')
            if ff['asymmetry'] > 0.15 and cd['asymmetry'] > 0.15:
                score += 1; props.append('asim_dir')
            if ff['c3_node'] is not None and cd['c3_node'] is not None:
                score += 1; props.append('triada')
            if score > best_score:
                best_score = score; best_match = (cd, score, props)
        results.append({
            'ff_id': ff['id'], 'ff_pair': f"T{ff['topic_a']}↔T{ff['topic_b']}",
            'ff_vocab': f"{ff['vocab_a'][:3]}|{ff['vocab_b'][:3]}",
            'match': best_match, 'c6c': best_score >= 3,
        })
    matched = sum(1 for r in results if r['c6c'])
    return results, matched


def run_p6(topic_vocab, dispute, delta, neg_pairs, n_topics):
    W_base = dispute.copy()
    W_mixta = W_base.copy()
    for (i, j) in neg_pairs:
        W_mixta[i, j] = NEG_WEIGHT
        W_mixta[j, i] = NEG_WEIGHT

    out_s = delta.sum(axis=1)
    in_s  = delta.sum(axis=0)
    pa = int(np.argmax(out_s)) if out_s.max() > 0 else 0
    ps = int(np.argmax(in_s))  if in_s.max()  > 0 else 1

    def relax(sigma, W):
        sigma = sigma.copy()
        for _ in range(MAX_ITER):
            i = random.randint(0, n_topics-1)
            h = float(np.dot(W[i], sigma))
            sigma[i] = 1.0 if h > 0 else -1.0
        return sigma

    def classify(sigma):
        if sigma[pa] == 1 and sigma[ps] == -1: return 'atk_dom'
        if sigma[ps] == 1 and sigma[pa] == -1: return 'sos_dom'
        return 'mixed'

    cb, cd_ = Counter(), Counter()
    for _ in range(N_RUNS):
        s0 = np.array([random.choice([-1.0, 1.0]) for _ in range(n_topics)])
        cb[classify(relax(s0.copy(), W_base))] += 1
        Wd = W_mixta.copy()
        for i in range(n_topics):
            for j in range(n_topics):
                if delta[i,j] > 0:
                    Wd[i,j] += 0.05 * delta[i,j]
        cd_[classify(relax(s0.copy(), Wd))] += 1

    return {
        'polo_atacante': pa, 'polo_sostenedor': ps,
        'vocab_atacante':  topic_vocab.get(pa, [])[:4],
        'vocab_sostenedor': topic_vocab.get(ps, [])[:4],
        'base':  {k: round(v/N_RUNS*100,1) for k,v in cb.items()},
        'delta': {k: round(v/N_RUNS*100,1) for k,v in cd_.items()},
        'colapso_mixtos': round((cb.get('mixed',0)-cd_.get('mixed',0))/N_RUNS*100,1),
    }


def run_stance(data, top_authors):
    tbl = find_table(data, [
        'mturk_author_stance', 'author_stance',
        'mturk_2010_p123_worker_response', 'stance'
    ])
    if tbl is None:
        return {a: 'table_not_found' for a in top_authors}

    rows = data[tbl]
    print(f"  Stance table: {tbl} ({len(rows)} rows)")
    if rows:
        first = rows[0]
        print(f"  Sample: {dict(list(first.items())[:5]) if isinstance(first,dict) else first[:5]}")

    stance_map = {}
    for row in rows:
        if isinstance(row, dict):
            aid    = row.get('author_id') or row.get('user_id')
            stance = row.get('stance') or row.get('label') or row.get('answer')
        elif isinstance(row, (list, tuple)):
            aid, stance = (row[0], row[1]) if len(row) >= 2 else (None, None)
        else:
            continue
        if aid is not None:
            try: stance_map[int(aid)] = stance
            except: pass

    return {a: stance_map.get(a, 'not_found') for a in top_authors}


# ── REG writers ────────────────────────────────────────────────────────────────

def write_regs(pairs, topic_vocab, c6c_results, matched,
               p6, stance_result, out_dir):
    now = datetime.now().strftime('%Y-%m-%d')

    # REG pairs
    lines = [
        "# REG_pairs_fourforums_guncontrol_v1", "",
        f"*fourforums gun control — {now}*", "",
        "## Topics LDA", "",
        "| ID | Palabras |", "|----|---------|",
    ]
    for t, wds in topic_vocab.items():
        lines.append(f"| T{t} | {', '.join(wds[:5])} |")
    lines += ["", "## Pares C1-C5", ""]
    for p in pairs:
        lines += [
            f"### {p['id']} — T{p['topic_a']}↔T{p['topic_b']}",
            f"- Tensión: {p['tension']} | Conv: {p['convergence']} | Asim: {p['asymmetry']}",
            f"- Iniciador: T{p['initiator']} | C3: {p['c3_node']} | Score: {p['score']}/5", "",
        ]
    (out_dir / 'REG_pairs_fourforums_guncontrol_v1.md').write_text(
        '\n'.join(lines), encoding='utf-8')

    # REG C6c
    lines = [
        "# REG_c6c_comparison_guncontrol_v1", "",
        f"*fourforums vs CreateDebate — {now}*", "",
        f"## Resultado: {matched}/{len(pairs)} pares coinciden (C6c)", "",
    ]
    if matched > 0:
        lines.append("→ Oposiciones son propiedad del dominio gun control.")
    else:
        lines.append("→ Sin coincidencias — estructuras difieren entre corpora.")
    lines += ["", "## Detalle", ""]
    for r in c6c_results:
        status = "✓" if r['c6c'] else "✗"
        mi = ""
        if r['match']:
            cd, sc, pr = r['match']
            mi = f" best={cd['id']} ({sc}/4: {pr})"
        lines.append(f"- {status} {r['ff_id']} {r['ff_pair']}{mi}")
    (out_dir / 'REG_c6c_comparison_guncontrol_v1.md').write_text(
        '\n'.join(lines), encoding='utf-8')

    # REG P6
    b, d = p6['base'], p6['delta']
    colapso = p6['colapso_mixtos']
    lines = [
        "# REG_p6_fourforums_guncontrol_v1", "",
        f"*P6: Delta como ruptura de simetría — fourforums — {now}*", "",
        f"Polo atacante:   T{p6['polo_atacante']} {p6['vocab_atacante']}",
        f"Polo sostenedor: T{p6['polo_sostenedor']} {p6['vocab_sostenedor']}", "",
        "| Condición | atk_dom | sos_dom | mixed |",
        "|-----------|---------|---------|-------|",
        f"| sin Delta | {b.get('atk_dom',0)}% | {b.get('sos_dom',0)}% | {b.get('mixed',0)}% |",
        f"| con Delta | {d.get('atk_dom',0)}% | {d.get('sos_dom',0)}% | {d.get('mixed',0)}% |",
        "",
        f"Colapso mixtos: {colapso} pp",
        "",
        "## vs CreateDebate",
        "| | CreateDebate | fourforums |",
        "|-|-------------|------------|",
        f"| Colapso mixtos | 54.0 pp | {colapso} pp |",
        f"| Polo dominante | sos_dom 55.8% | sos_dom {d.get('sos_dom',0)}% |",
        "",
    ]
    if abs(colapso - 54.0) < 15:
        lines.append("→ Escenario A: colapso similar. Delta es propiedad del dominio.")
    elif colapso > 54.0:
        lines.append("→ Escenario A+: colapso más pronunciado. P6 reforzada.")
    else:
        lines.append("→ Escenario B: colapso menor. Investigar dilución Delta.")
    (out_dir / 'REG_p6_fourforums_guncontrol_v1.md').write_text(
        '\n'.join(lines), encoding='utf-8')

    # REG stance
    lines = [
        "# REG_stance_fourforums_v1", "",
        f"*Stance top autores — {now}*", "",
        "| Author | Stance |", "|--------|--------|",
    ]
    for aid, s in stance_result.items():
        lines.append(f"| {aid} | {s} |")
    s555 = stance_result.get(555, 'not_found')
    s965 = stance_result.get(965, 'not_found')
    lines += ["", "## Interpretación"]
    if s555 not in ('not_found','table_not_found') and \
       s965 not in ('not_found','table_not_found'):
        if s555 != s965:
            lines.append(f"Atacante (555): {s555} | Sostenedor (965): {s965}")
            lines.append("→ Asimetría tiene contenido ideológico verificado.")
        else:
            lines.append(f"Mismo stance ({s555}). Asimetría es de rol, no de posición.")
    else:
        lines.append("Stance no disponible — verificar tabla en SQL.")
    (out_dir / 'REG_stance_fourforums_v1.md').write_text(
        '\n'.join(lines), encoding='utf-8')

    print(f"\n  REGs escritos en {out_dir}")
    for f in sorted(out_dir.glob('REG_*.md')):
        print(f"    {f.name}")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sql', required=True)
    ap.add_argument('--out', default='.')
    ap.add_argument('--n_topics', type=int, default=N_TOPICS)
    ap.add_argument('--explore', action='store_true',
                    help='Solo explorar schema y salir')
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("CKM Pipeline v8b — fourforums gun control")
    print("=" * 60)

    print("\n[1] Parseando SQL...")
    data = parse_sql(args.sql)
    explore_schema(data)

    if args.explore:
        print("\n--explore: deteniendo aquí.")
        return

    print("\n[2] Filtrando gun control...")
    gun_disc_ids, gun_posts = filter_gun_posts(data)

    print(f"\n[3] LDA N={args.n_topics}...")
    topic_vocab, post_to_topic = run_lda(gun_posts, args.n_topics)

    print("\n[4] Construyendo W y Delta...")
    dispute, support, delta = build_W_delta(
        data, gun_disc_ids, post_to_topic, args.n_topics)

    print("\n[5] Elicitando pares C1-C5...")
    pairs = elicit_pairs_c1_c5(topic_vocab, dispute, support, args.n_topics)
    print(f"  Pares: {len(pairs)}")
    for p in pairs:
        print(f"    {p['id']}: T{p['topic_a']}↔T{p['topic_b']} "
              f"tensión={p['tension']} asim={p['asymmetry']} "
              f"C3={'✓' if p['c3_node'] is not None else '✗'}")

    print("\n[6] C6c vs CreateDebate...")
    c6c_results, matched = run_c6c(pairs, CD_BASELINE)
    print(f"  Matches: {matched}/{len(pairs)}")

    neg_pairs = [(p['topic_a'], p['topic_b']) for p in pairs
                 if p['tension'] > 0.80]
    print(f"\n[7] P6 (neg_pairs={len(neg_pairs)})...")
    p6 = run_p6(topic_vocab, dispute, delta, neg_pairs, args.n_topics)
    print(f"  Colapso mixtos: {p6['colapso_mixtos']} pp")

    print("\n[8] Stance cross-reference...")
    stance = run_stance(data, TOP_AUTHORS)
    for a, s in stance.items():
        print(f"  {a}: {s}")

    write_regs(pairs, topic_vocab, c6c_results, matched,
               p6, stance, out_dir)

    print("\n" + "=" * 60)
    print("Subir al proyecto: los 4 REG_*.md generados")
    print("=" * 60)


if __name__ == '__main__':
    main()
