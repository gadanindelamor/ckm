#!/usr/bin/env python3
"""
explore_qr_asymmetry_v2.py
Explorador QR asimétrico — versión intermedia.

Nota histórica: esta versión usa extract_cols (tokenización lazy por columna)
y multi-INSERT awareness. Aún lenta en tabla post (~414K rows).
Supersedida por fourforums_pipeline_v8h.py que usa re.findall (C-level).
Conservada como referencia del proceso de desarrollo.

Uso:
    python explore_qr_asymmetry_v2.py trace/fourforums_no_parse_2016_05_18.sql
"""

import re, sys, statistics
from pathlib import Path
from collections import Counter

SQL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('fourforums_no_parse_2016_05_18.sql')
GUN_TOPIC_ID = '9'
SAMPLE_MAX = 5000

WANT = {
    'mturk_2010_qr_entry',
    'mturk_2010_qr_task1_worker_response',
    'post',
    'mturk_author_stance',
    'discussion_topic',
}

create_re = re.compile(r'CREATE TABLE `?(\w+)`?', re.I)
col_re    = re.compile(r'^\s*`(\w+)`')
insert_re = re.compile(r'INSERT INTO `?(\w+)`?\s+VALUES\s*(.+)', re.I | re.DOTALL)


def fast_count(vals_str):
    """Cuenta grupos (a,b,...). Rápido: operación C."""
    return vals_str.count('),(') + 1


def col_index(col_names_list, col_name):
    try:    return col_names_list.index(col_name)
    except: return None


def extract_cols(vals_str, indices):
    """
    Extrae columnas específicas de cada fila VALUES.
    Tokenización lazy — para cuando el índice máximo es pequeño.
    ADVERTENCIA: lento en tablas con >100K rows o rows muy largas.
    Para producción usar re.findall (ver fourforums_pipeline_v8h.py).
    """
    max_idx = max(indices)
    results = []
    i = 0; n = len(vals_str)
    while i < n:
        while i < n and vals_str[i] != '(': i += 1
        if i >= n: break
        i += 1
        col = 0; row = {}
        while i < n and col <= max_idx:
            c = vals_str[i]
            if c in (' ', '\t'): i += 1; continue
            if c == ',':         col += 1; i += 1; continue
            if c == ')':         break
            if c == "'":
                j = i+1; buf = []
                while j < n:
                    if vals_str[j] == '\\' and j+1 < n:
                        buf.append(vals_str[j+1]); j += 2
                    elif vals_str[j] == "'":
                        j += 1; break
                    else:
                        buf.append(vals_str[j]); j += 1
                token = ''.join(buf); i = j
            elif vals_str[i:i+4].upper() == 'NULL':
                token = None; i += 4
            else:
                j = i
                while j < n and vals_str[j] not in (',', ')'): j += 1
                token = vals_str[i:j].strip(); i = j
            if col in indices: row[col] = token
        # avanzar hasta fin del grupo
        depth = 1
        while i < n and depth > 0:
            if vals_str[i] == '(':   depth += 1
            elif vals_str[i] == ')': depth -= 1
            i += 1
        if row: results.append(row)
    return results


def extract_col(vals_str, idx, sample_max=None):
    """Extrae una columna con early exit opcional."""
    results = []
    i = 0; n = len(vals_str)
    while i < n:
        while i < n and vals_str[i] != '(': i += 1
        if i >= n: break
        i += 1
        col = 0; val = None
        while i < n and col <= idx:
            c = vals_str[i]
            if c in (' ', '\t'): i += 1; continue
            if c == ',':         col += 1; i += 1; continue
            if c == ')':         break
            if c == "'":
                j = i+1; buf = []
                while j < n:
                    if vals_str[j] == '\\' and j+1 < n:
                        buf.append(vals_str[j+1]); j += 2
                    elif vals_str[j] == "'":
                        j += 1; break
                    else:
                        buf.append(vals_str[j]); j += 1
                token = ''.join(buf); i = j
            elif vals_str[i:i+4].upper() == 'NULL':
                token = None; i += 4
            else:
                j = i
                while j < n and vals_str[j] not in (',', ')'): j += 1
                token = vals_str[i:j].strip(); i = j
            if col == idx: val = token; break
        depth = 1
        while i < n and depth > 0:
            if vals_str[i] == '(':   depth += 1
            elif vals_str[i] == ')': depth -= 1
            i += 1
        if val is not None:
            results.append(val)
            if sample_max and len(results) >= sample_max: break
    return results


# ── Acumuladores ────────────────────────────────────────────────────────────────
col_names     = {}
row_counts    = {}
gun_disc_ids  = set()
author_stance = {}
post_author   = {}
qr_keys       = {}
task1_agree   = []

print(f"Leyendo: {SQL}", flush=True)
current = None; in_c = False

with open(SQL, encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        if i % 200 == 0:
            print(f"  línea {i} | tablas: {list(row_counts.keys())}",
                  end='\r', flush=True)

        m = create_re.match(line)
        if m:
            current = m.group(1).lower(); col_names[current] = []; in_c = True; continue
        if in_c:
            if re.match(r'\s*\)', line): in_c = False; continue
            cm = col_re.match(line)
            if cm: col_names[current].append(cm.group(1).lower())
            continue

        if not line.startswith('INSERT'): continue
        m = insert_re.match(line.rstrip())
        if not m: continue
        tbl = m.group(1).lower()
        if tbl not in WANT: continue

        vals = m.group(2).rstrip(';')
        cols = col_names.get(tbl, [])
        row_counts[tbl] = row_counts.get(tbl, 0) + fast_count(vals)
        print(f"\n  {tbl}: +{fast_count(vals):,} rows (total={row_counts[tbl]:,})", flush=True)

        if tbl == 'discussion_topic':
            idx_tid = col_index(cols, 'topic_id')
            idx_did = col_index(cols, 'discussion_id')
            if None not in (idx_tid, idx_did):
                for r in extract_cols(vals, {idx_tid, idx_did}):
                    if str(r.get(idx_tid)) == GUN_TOPIC_ID:
                        gun_disc_ids.add(r.get(idx_did))

        elif tbl == 'mturk_author_stance':
            idx_aid = col_index(cols, 'author_id')
            idx_v1  = col_index(cols, 'topic_stance_votes_1')
            idx_v2  = col_index(cols, 'topic_stance_votes_2')
            if None not in (idx_aid, idx_v1, idx_v2):
                for r in extract_cols(vals, {idx_aid, idx_v1, idx_v2}):
                    aid = r.get(idx_aid)
                    try:
                        v1 = int(r.get(idx_v1, 0) or 0)
                        v2 = int(r.get(idx_v2, 0) or 0)
                        if v1 != v2 and aid:
                            author_stance[aid] = 0 if v1 > v2 else 1
                    except: pass

        elif tbl == 'post':
            # ADVERTENCIA: lento — ~414K rows. Ver v8h para alternativa rápida.
            idx_did = col_index(cols, 'discussion_id')
            idx_pid = col_index(cols, 'post_id')
            idx_aid = col_index(cols, 'author_id')
            if None not in (idx_did, idx_pid, idx_aid):
                for r in extract_cols(vals, {idx_did, idx_pid, idx_aid}):
                    did, pid, aid = r.get(idx_did), r.get(idx_pid), r.get(idx_aid)
                    if did and pid and aid: post_author[(did, pid)] = aid

        elif tbl == 'mturk_2010_qr_entry':
            idx_pg  = col_index(cols, 'page_id')
            idx_tab = col_index(cols, 'tab_number')
            idx_did = col_index(cols, 'discussion_id')
            idx_pid = col_index(cols, 'post_id')
            if None not in (idx_pg, idx_tab, idx_did, idx_pid):
                for r in extract_cols(vals, {idx_pg, idx_tab, idx_did, idx_pid}):
                    pg  = r.get(idx_pg)
                    tab = r.get(idx_tab)
                    did = r.get(idx_did)
                    pid = r.get(idx_pid)
                    if pg and tab and did and pid:
                        qr_keys[(pg, tab)] = (did, pid)

        elif tbl == 'mturk_2010_qr_task1_worker_response':
            idx_da = col_index(cols, 'disagree_agree')
            if idx_da is not None:
                for v in extract_col(vals, idx_da, SAMPLE_MAX):
                    try: task1_agree.append(float(v))
                    except: pass

print(f"\n\nLectura completa.\n", flush=True)

# ── Output ───────────────────────────────────────────────────────────────────
print("=" * 60)
print("ROW COUNTS")
print("=" * 60)
for t, c in sorted(row_counts.items()):
    print(f"  {t}: {c:,}")

print()
print("=" * 60)
print("GUN CONTROL (topic_id=9)")
print("=" * 60)
print(f"  gun_disc_ids: {len(gun_disc_ids):,}")
print(f"  post_author entries: {len(post_author):,}")
print(f"  author_stance: {len(author_stance):,}  "
      f"(T0={sum(v==0 for v in author_stance.values())} "
      f"T1={sum(v==1 for v in author_stance.values())})")

print()
print("=" * 60)
print(f"DISTRIBUCIÓN disagree_agree (n={len(task1_agree)})")
print("=" * 60)
if task1_agree:
    neg  = sum(1 for x in task1_agree if x < 0)
    zero = sum(1 for x in task1_agree if x == 0)
    pos  = sum(1 for x in task1_agree if x > 0)
    print(f"  rango:   [{min(task1_agree):.0f}, {max(task1_agree):.0f}]")
    print(f"  media:   {statistics.mean(task1_agree):.2f}")
    print(f"  mediana: {statistics.median(task1_agree):.2f}")
    print(f"  negativo: {neg:,} ({100*neg/len(task1_agree):.1f}%)")
    print(f"  cero:     {zero:,} ({100*zero/len(task1_agree):.1f}%)")
    print(f"  positivo: {pos:,} ({100*pos/len(task1_agree):.1f}%)")
else:
    print("  NINGÚN valor encontrado.")

print()
print("=" * 60)
print("CARDINALIDAD DEL JOIN")
print("=" * 60)
print(f"  qr_entry keys: {len(qr_keys):,}")
resolvable_all = resolvable_gun = 0
for (pg, tab), (did, pid) in qr_keys.items():
    aid = post_author.get((did, pid))
    if not aid: continue
    if author_stance.get(aid) is None: continue
    resolvable_all += 1
    if did in gun_disc_ids: resolvable_gun += 1

print(f"  con author+stance (todos topics): {resolvable_all:,}")
print(f"  con author+stance (gun control):  {resolvable_gun:,}")
if qr_keys:
    jr = resolvable_all / len(qr_keys)
    t1n = row_counts.get('mturk_2010_qr_task1_worker_response', 0)
    print(f"  join_rate: {jr:.3f}")
    print(f"  votos estimados con stance: ~{int(t1n * jr):,}")

print("\nNota: para ejecución rápida usar fourforums_pipeline_v8h.py")
