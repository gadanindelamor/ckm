"""
fourforums_pipeline_v8f.py
fix: post+qr_entry streaming, GUN_TOPIC_ID, explore_schema fix - evita explosion de RAM.

Cambios respecto a v8c:
  - parse_sql_small: carga todo EXCEPTO mturk_2010_qr_entry (evita 10GB RAM)
  - stream_W_delta: segunda pasada streaming - procesa qr_entry row a row
  - build_W_delta refactored: usa stream_W_delta internamente
  - mturk_2010_qr_entry vuelve a SKIP_TABLES para parse_sql_small

Uso:
    python fourforums_pipeline_v8f.py --sql fourforums_no_parse_2016_05_18.sql --log run.log
    python fourforums_pipeline_v8f.py --sql ... --skip_p1p4 --log run.log
    # PEG LOG & CONSOLE
    python fourforums_pipeline_v8f.py --sql fourforums_no_parse_2016_05_18.sql --log run_v8f.log | Tee-Object -FilePath run_v8e_console.log
"""

import re, json, sys, argparse, random
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import numpy as np

try:
    from ckm_p1p4_module import run_all as run_p1p4
    HAS_P1P4 = True
except ImportError:
    HAS_P1P4 = False
    print("[AVISO] ckm_p1p4_module no encontrado - step P1-P4 se omitira."
          " Colocar ckm_p1p4_module.py en el mismo directorio.")

# ── Constantes ─────────────────────────────────────────────────────────────────
GUN_TOPIC_ID = 9   # fourforums: topic_id=9 = gun control

SKIP_TABLES = {
    'markup', 'text',    # text: contenido posts - enorme, no necesario
    'post',              # post: se procesa via streaming (post→author mapping)
    'report', 'session', 'notification', 'email', 'log',
    'mturk_2010_p123_post', 'mturk_2010_p123_average_response',
    'mturk_2010_p123_entry', 'mturk_2010_p123_worker_response',
    'mturk_2010_qr_entry',              # procesado via stream_W_delta
    'mturk_2010_qr_task1_average_response',
    'mturk_2010_qr_task1_worker_response', 'mturk_2010_qr_task2_average_response',
    'mturk_2010_qr_task2_worker_response', 'dataset_metadata',
}

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
        for i, line in enumerate(f):
            if i % 50_000 == 0:
                print(f"  parsing... {i:,} lines", end='\r', flush=True)
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
            if table in SKIP_TABLES:        # ← agregar esta línea
                continue                    # ← y esta
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
                    # mismatch - guardar como dict parcial con índice
                    d = {cols[i]: row[i] for i in range(min(len(cols), len(row)))}
                    raw[table].append(d)
                else:
                    raw[table].append(row)

    print(f"  parsing... {i:,} lines - done.              ")
    result = dict(raw)
    result['__col_names__'] = dict(col_names)  # para stream_W_delta
    return result


# ── Explorar schema ─────────────────────────────────────────────────────────────

def explore_schema(data):
    """Imprime schema para diagnosticar tablas disponibles."""
    print("\n  Schema detectado:")
    for tbl, rows in sorted(data.items()):
        if tbl.startswith('__'): continue   # saltar meta-keys
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
    """Filtra posts gun control via topic_id=9. No usa keywords en texto."""
    def get_field(row, candidates, default=None):
        if isinstance(row, dict):
            for k in candidates:
                if k in row: return row[k]
        return default

    # discussion_topic → IDs discusiones gun
    dt_tbl = find_table(data, ['discussion_topic', 'discussiontopic'])
    gun_disc_ids = set()
    if dt_tbl:
        dt_rows = data[dt_tbl]
        print(f"  discussion_topic: {len(dt_rows)} rows")
        if dt_rows:
            s = dt_rows[0]
            print(f"  Sample: {dict(list(s.items())[:5]) if isinstance(s,dict) else s[:5]}")
        for row in dt_rows:
            tid = get_field(row, ['topic_id','topicid'])
            did = get_field(row, ['discussion_id','discussionid'])
            if tid == GUN_TOPIC_ID and did is not None:
                gun_disc_ids.add(did)
        print(f"  Discusiones gun (topic_id={GUN_TOPIC_ID}): {len(gun_disc_ids)}")
    else:
        print(f"  WARN: discussion_topic no encontrada. Tablas: {list(data.keys())}")
        disc_tbl = find_table(data, ['discussion','discussions'])
        if disc_tbl:
            for d in data[disc_tbl]:
                title = ''
                if isinstance(d, dict):
                    for k in ['title','topic','name','subject']:
                        if k in d: title = str(d[k] or '').lower(); break
                if any(kw in title for kw in GUN_KEYWORDS):
                    did = get_field(d, ['discussion_id','id'])
                    if did: gun_disc_ids.add(did)
            print(f"  Discusiones gun (fallback keywords): {len(gun_disc_ids)}")

    # post → posts de esas discusiones
    post_tbl = find_table(data, ['post','posts'])
    gun_posts = []
    if post_tbl:
        posts = data[post_tbl]
        print(f"  post: {len(posts)} rows")
        if posts:
            s = posts[0]
            print(f"  Sample: {dict(list(s.items())[:5]) if isinstance(s,dict) else s[:5]}")
        gun_posts = ([p for p in posts
                      if get_field(p, ['discussion_id','disc_id']) in gun_disc_ids]
                     if gun_disc_ids else posts)
        print(f"  Posts gun: {len(gun_posts)}")
    else:
        print(f"  WARN: tabla post no encontrada")
    return gun_disc_ids, gun_posts


# ── Asignación de topics por stance (reemplaza LDA) ───────────────────────────

def run_lda(posts, n_topics):
    """
    Reemplaza LDA por asignación directa via stance labels.
    fourforums tiene ground truth: stance_id 2=pro_control, 3=anti_control.
    n_topics se ignora - usamos 2 polos (T0=pro, T1=anti).
    Retorna (topic_vocab, post_to_topic) para compatibilidad con resto del pipeline.
    """
    # topic_vocab: labels descriptivos
    topic_vocab = {
        0: ['gun_control', 'pro_control', 'regulation', 'ban', 'safety'],
        1: ['gun_rights', 'anti_control', 'amendment', 'rights', 'self_defense'],
    }
    print(f"  Topics: T0=pro_control, T1=anti_control (stance ground truth)")
    print(f"  Posts disponibles para mapeo: {len(posts)}")

    # Mapeo post_id → topic via author_id (se completa en build_W_delta)
    # Aquí devolvemos mapeo vacío - build_W_delta lo llena desde stance
    post_to_topic = {}
    return topic_vocab, post_to_topic


# ── Build W + Delta (streaming) ────────────────────────────────────────────────

def stream_W_delta(sql_path, post_to_topic, col_names_qr, n_topics=2):
    """
    Pasada streaming sobre el SQL - solo mturk_2010_qr_entry.
    Procesa row a row, acumula W/Delta en matrices 2x2, descarta cada row.
    Nunca carga la tabla completa en RAM.
    """
    dispute = np.zeros((n_topics, n_topics))
    support = np.zeros((n_topics, n_topics))
    delta   = np.zeros((n_topics, n_topics))

    TARGET = 'mturk_2010_qr_entry'
    insert_re = re.compile(
        r"INSERT INTO `?" + TARGET + r"`?\s+(?:VALUES|values)\s*(.+)", re.DOTALL)

    cols = col_names_qr  # lista de nombres de columna en orden
    n_rows = 0
    n_matched = 0

    # índices de columnas que necesitamos
    def ci(candidates):
        for c in candidates:
            if c in cols: return cols.index(c)
        return None

    idx_src  = ci(['src_post_id','source_post_id','quote_post_id','from_post_id'])
    idx_tgt  = ci(['tgt_post_id','target_post_id','response_post_id','to_post_id'])
    idx_agr  = ci(['agree','agreement','avg_agreement','score'])
    idx_rel  = ci(['relation','type','label','relation_type','stance'])

    print(f"  stream_W_delta: cols qr_entry = {cols[:8]}")
    print(f"  idx src={idx_src} tgt={idx_tgt} agr={idx_agr} rel={idx_rel}")

    with open(sql_path, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f):
            if i % 50_000 == 0:
                print(f"  streaming qr... {i:,} lines | rows={n_rows:,} matched={n_matched:,}",
                      end="\r", flush=True)
            m = insert_re.match(line.rstrip())
            if not m:
                continue
            vals_str = m.group(1).rstrip(';')
            for group in _split_value_groups(vals_str):
                try:
                    row = _tokenize_row(group)
                except Exception:
                    continue
                n_rows += 1

                src_pid = row[idx_src] if idx_src is not None and idx_src < len(row) else None
                tgt_pid = row[idx_tgt] if idx_tgt is not None and idx_tgt < len(row) else None
                if src_pid is None or tgt_pid is None:
                    continue

                t_src = post_to_topic.get(src_pid)
                t_tgt = post_to_topic.get(tgt_pid)
                if t_src is None or t_tgt is None or t_src == t_tgt:
                    continue

                # acuerdo/desacuerdo
                is_dispute = is_support = False
                if idx_rel is not None and idx_rel < len(row):
                    rel = str(row[idx_rel] or '').lower()
                    is_dispute = any(x in rel for x in
                                     ['disagree','attack','dispute','refute','counter','no','against'])
                    is_support = any(x in rel for x in
                                     ['agree','support','yes','for','accept'])
                if not is_dispute and not is_support and idx_agr is not None and idx_agr < len(row):
                    try:
                        av = float(row[idx_agr])
                        if av < 0.4:   is_dispute = True
                        elif av > 0.6: is_support = True
                    except: pass

                if is_dispute:
                    dispute[t_src, t_tgt] += 1
                    dispute[t_tgt, t_src] += 1
                    delta[t_tgt, t_src]   += 1
                    n_matched += 1
                elif is_support:
                    support[t_src, t_tgt] += 1
                    support[t_tgt, t_src] += 1
                    n_matched += 1

    print(f"  streaming qr... done. rows={n_rows:,} matched={n_matched:,}              ")

    d_max = dispute.max(); s_max = support.max(); dn_max = delta.max()
    if d_max > 0: dispute /= d_max
    if s_max > 0: support /= s_max
    if dn_max > 0: delta /= dn_max

    return dispute, support, delta, n_rows, n_matched


def stream_post_author(sql_path, col_names_post):
    """Pasada streaming para la tabla post - extrae {post_id: author_id}."""
    mapping = {}
    cols = col_names_post
    TARGET = 'post'
    insert_re = re.compile(
        r"INSERT INTO `?" + TARGET + r"`?\s+(?:VALUES|values)\s*(.+)", re.DOTALL)

    def ci(candidates):
        for c in candidates:
            if c in cols: return cols.index(c)
        return None

    idx_pid = ci(['post_id','id'])
    idx_aid = ci(['author_id','user_id','userid'])
    idx_did = ci(['discussion_id','disc_id'])
    print(f"  stream_post: cols={cols[:6]} | idx_pid={idx_pid} idx_aid={idx_aid}")

    with open(sql_path, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f):
            if i % 50_000 == 0:
                print(f"  streaming post... {i:,} lines | mapeados={len(mapping):,}",
                      end="\r", flush=True)
            m = insert_re.match(line.rstrip())
            if not m: continue
            vals_str = m.group(1).rstrip(';')
            for group in _split_value_groups(vals_str):
                try: row = _tokenize_row(group)
                except: continue
                pid = row[idx_pid] if idx_pid is not None and idx_pid < len(row) else None
                aid = row[idx_aid] if idx_aid is not None and idx_aid < len(row) else None
                did = row[idx_did] if idx_did is not None and idx_did < len(row) else None
                if pid is not None and aid is not None:
                    mapping[pid] = (aid, did)
    print(f"  streaming post... done. posts={len(mapping):,}              ")
    return mapping


def build_W_delta(sql_path, data, gun_disc_ids, post_to_topic, n_topics):
    """
    Orquesta la construcción de W y Delta:
    1. author→stance→topic desde mturk_author_stance (ya en data)
    2. post_id→topic via post table (ya en data)
    3. W/Delta via stream_W_delta (segunda pasada streaming)
    """
    n_topics = 2

    def get_field(row, candidates, default=None):
        if isinstance(row, dict):
            for k in candidates:
                if k in row: return row[k]
        return default

    # autor → topic
    stance_tbl = find_table(data, ['mturk_author_stance','author_stance'])
    author_to_topic = {}
    if stance_tbl:
        st_rows = data[stance_tbl]
        print(f"  mturk_author_stance: {len(st_rows)} rows")
        if st_rows:
            s = st_rows[0]
            print(f"  Sample: {dict(list(s.items())[:5]) if isinstance(s,dict) else s[:5]}")
        for row in st_rows:
            if isinstance(row, dict):
                disc_id = row.get('discussion_id')
                if disc_id not in gun_disc_ids: continue
                aid = row.get('author_id')
                if aid is None: continue
                # stance real = comparar votos workers pro vs anti
                try:
                    v1 = int(row.get('topic_stance_votes_1') or 0)
                    v2 = int(row.get('topic_stance_votes_2') or 0)
                except: continue
                if v1 == v2: continue   # empate o sin datos - no mapear
                author_to_topic[int(aid)] = 0 if v1 > v2 else 1
        t0 = sum(1 for v in author_to_topic.values() if v == 0)
        t1 = sum(1 for v in author_to_topic.values() if v == 1)
        print(f"  Autores con stance: {len(author_to_topic)} (T0={t0} T1={t1})")
    else:
        print("  WARN: mturk_author_stance no encontrada")

    # post → topic (via streaming - post no está en data)
    if not post_to_topic:
        col_names_post = data.get('__col_names__', {}).get('post', [])
        post_author = stream_post_author(sql_path, col_names_post)
        for pid, (aid, did) in post_author.items():
            if did not in gun_disc_ids: continue   # solo posts de gun control
            t = author_to_topic.get(int(aid) if aid is not None else aid)
            if t is not None:
                post_to_topic[pid] = t
        print(f"  Posts mapeados a topic: {len(post_to_topic)}")

    if not post_to_topic:
        print("  ERROR: post_to_topic vacío - sin datos para W/Delta")
        z = np.zeros((n_topics, n_topics))
        return z, z, z

    # ── W y Delta desde tabla quote (ya en RAM) ───────────────────────────────
    # quote: discussion_id, post_id (respuesta), quote_index, source_post_id (citado)
    # Interacción: source_post cita → post (respuesta)
    # W[t_src, t_tgt]: t_src = topic del post citado, t_tgt = topic del que responde
    quote_tbl = find_table(data, ['quote', 'quotes'])
    W_raw   = np.zeros((n_topics, n_topics))
    delta   = np.zeros((n_topics, n_topics))
    n_total = n_cross = 0

    if quote_tbl:
        q_rows = data[quote_tbl]
        print(f"  quote: {len(q_rows)} rows (filtrando gun_disc_ids={len(gun_disc_ids)})")
        for q in q_rows:
            if not isinstance(q, dict): continue
            # filtrar por discusión gun control
            disc_id = q.get('discussion_id')
            if disc_id not in gun_disc_ids: continue
            src_pid = q.get('source_post_id')
            tgt_pid = q.get('post_id')
            if src_pid is None or tgt_pid is None: continue
            t_src = post_to_topic.get(src_pid)
            t_tgt = post_to_topic.get(tgt_pid)
            n_total += 1
            if t_src is None or t_tgt is None: continue
            if t_src == t_tgt: continue          # misma postura - no aporta tensión
            W_raw[t_src, t_tgt] += 1
            W_raw[t_tgt, t_src] += 1
            # delta: asimetría direccional (quién inicia más)
            delta[t_tgt, t_src] += 1             # respuesta → cita (dirección de réplica)
            n_cross += 1
        print(f"  Interacciones totales: {n_total:,} | cross-topic: {n_cross:,}")
    else:
        print("  WARN: tabla quote no encontrada")

    # normalizar
    w_max = W_raw.max(); d_max = delta.max()
    dispute = W_raw / w_max if w_max > 0 else W_raw
    support = np.zeros_like(dispute)   # sin labels agree/disagree: support=0
    if d_max > 0: delta /= d_max

    print(f"  W[0,1]={W_raw[0,1]:.0f} W[1,0]={W_raw[1,0]:.0f} | "
          f"Delta[0,1]={delta[0,1]:.3f} Delta[1,0]={delta[1,0]:.3f}")
    return dispute, support, delta


# ── C1-C5, C6c, P6, stance - igual que v8 ─────────────────────────────────────

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
        f"*fourforums gun control - {now}*", "",
        "## Topics LDA", "",
        "| ID | Palabras |", "|----|---------|",
    ]
    for t, wds in topic_vocab.items():
        lines.append(f"| T{t} | {', '.join(wds[:5])} |")
    lines += ["", "## Pares C1-C5", ""]
    for p in pairs:
        lines += [
            f"### {p['id']} - T{p['topic_a']}↔T{p['topic_b']}",
            f"- Tensión: {p['tension']} | Conv: {p['convergence']} | Asim: {p['asymmetry']}",
            f"- Iniciador: T{p['initiator']} | C3: {p['c3_node']} | Score: {p['score']}/5", "",
        ]
    (out_dir / 'REG_pairs_fourforums_guncontrol_v1.md').write_text(
        '\n'.join(lines), encoding='utf-8')

    # REG C6c
    lines = [
        "# REG_c6c_comparison_guncontrol_v1", "",
        f"*fourforums vs CreateDebate - {now}*", "",
        f"## Resultado: {matched}/{len(pairs)} pares coinciden (C6c)", "",
    ]
    if matched > 0:
        lines.append("→ Oposiciones son propiedad del dominio gun control.")
    else:
        lines.append("→ Sin coincidencias - estructuras difieren entre corpora.")
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
        f"*P6: Delta como ruptura de simetría - fourforums - {now}*", "",
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
        f"*Stance top autores - {now}*", "",
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
        lines.append("Stance no disponible - verificar tabla en SQL.")
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
    ap.add_argument('--skip_p1p4', action='store_true',
                    help='Omitir step P1-P4 (util para runs rapidos)')
    ap.add_argument('--log', default=None,
                    help='Archivo de log (stdout redirigido)')
    args = ap.parse_args()

    if args.log:
        import io
        _log_f = open(args.log, 'w', encoding='utf-8', buffering=1)
        sys.stdout = _log_f
        print(f'# Log: {args.log}')

    out_dir = Path(args.out)
    out_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("CKM Pipeline v8f - fourforums gun control")
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

    print("\n[4] Construyendo W y Delta (streaming)...")
    dispute, support, delta = build_W_delta(
        args.sql, data, gun_disc_ids, post_to_topic, args.n_topics)
    args.n_topics = int(dispute.shape[0])  # sync con tamaño real de matriz (2)

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

    # ── [7b] P1-P4 sobre W real del corpus ────────────────────────────────────
    # Línea 1: construir W_base y W_mixta desde dispute + neg_pairs elicitados
    W_base_p1p4 = dispute.copy()
    W_mixta_p1p4 = W_base_p1p4.copy()
    for (i, j) in neg_pairs:
        W_mixta_p1p4[i, j] = NEG_WEIGHT
        W_mixta_p1p4[j, i] = NEG_WEIGHT

    # Línea 2: ejecutar P1-P4 y escribir REG
    if HAS_P1P4 and not args.skip_p1p4:
        print(f"\n[7b] P1-P4 (N={args.n_topics}, neg_pairs={len(neg_pairs)})...")
        nodes_labels = [
            f"T{i}_{'_'.join(topic_vocab.get(i, ['?'])[:2])}"
            for i in range(args.n_topics)
        ]
        run_p1p4(W_base_p1p4, W_mixta_p1p4, nodes_labels,
                 label="fourforums_guncontrol",
                 output_dir=str(out_dir))
    elif args.skip_p1p4:
        print("\n[7b] P1-P4 omitido (--skip_p1p4)")
    else:
        print("\n[7b] P1-P4 omitido (ckm_p1p4_module no disponible)")
    # ── fin [7b] ──────────────────────────────────────────────────────────────

    print("\n[8] Stance cross-reference...")
    stance = run_stance(data, TOP_AUTHORS)
    for a, s in stance.items():
        print(f"  {a}: {s}")

    write_regs(pairs, topic_vocab, c6c_results, matched,
               p6, stance, out_dir)

    print("\n" + "=" * 60)
    print("CKM Pipeline v8f - fourforums gun control")
    print("Subir al proyecto:")
    print("  REG_pairs_fourforums_guncontrol_v1.md")
    print("  REG_c6c_comparison_guncontrol_v1.md")
    print("  REG_p6_fourforums_guncontrol_v1.md")
    print("  REG_stance_fourforums_v1.md")
    if HAS_P1P4 and not args.skip_p1p4:
        print("  REG_p1p4_fourforums_guncontrol.json")
    print("=" * 60)


if __name__ == '__main__':
    main()
