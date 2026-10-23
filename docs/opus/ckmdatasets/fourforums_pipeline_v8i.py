#!/usr/bin/env python3
"""
fourforums_pipeline_v8i.py

Author-by-author table of human agree/disagree votes (IAC fourforums, gun
control). The sign comes from the annotators
(mturk_2010_qr_task1_worker_response.disagree_agree), not from this code.

Built ON fourforums_pipeline_v8h.py, whose access layer to the dump is kept
INTACT: same tables, same regexes, same join chain, same drops, same naming
(quoter / responder / q_stance / r_stance, keys T{q}_quotes_T{r}).
The only additions:
  - keeps ALL author pairs (v8h kept only the top 100 with n >= 2);
  - builds the directed matrix A[i, j] = mean vote for the pair
    (quoter i, responder j), as v8h indexes pair_da[quoter][responder];
    absence of data is NaN, never 0;
  - reports counts only. Symmetrization, n_min for W, the choice of N and a
    null model are left open on purpose (for delamor).
Any correction to the access layer or its naming goes to v8j, declared, so
that v8i and v8j can be compared.

Decisions inherited from v8h (declared, not changed): topic 9 only; authors
whose stance votes tie are dropped; a vote needs the full chain to resolve.

Outputs (in --out, default out/; keep out/ out of git: it has author ids):
  pairs_v8i.csv, A_v8i.npy, nodes_v8i.json, summary_v8i.json, run_v8i.log

Usage:
  python fourforums_pipeline_v8i.py
  python fourforums_pipeline_v8i.py --sql fourforums_no_parse_2016_05_18.sql --out out
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime
from itertools import combinations
from pathlib import Path

import numpy as np

GUN_TOPIC_ID = 9
EXPECTED_SQL_SHA1 = '7db7fb40269e3ff9dba9008b1c99c31bd1c699d6'

WANT = {
    'discussion_topic', 'mturk_author_stance', 'post',
    'quote', 'mturk_2010_qr_entry', 'mturk_2010_qr_task1_worker_response',
}

# Identical to v8h.
RE_INSERT = re.compile(r'INSERT INTO `?(\w+)`?', re.I)
RE_DISC_T = re.compile(r'\((\d+),(\d+)')
RE_STANCE = re.compile(r'\(\d+,(\d+),(\d+),\d+,(\d+),\d+,(\d+),')
RE_POST   = re.compile(r'\((\d+),(\d+),(\d+),')
RE_QUOTE  = re.compile(r'\((\d+),(\d+),(\d+),(?:\d+|NULL),\d+,\d+,(\d+),(\d+),')
RE_QR     = re.compile(r'\((\d+),(\d+),(\d+),(\d+),(\d+),')
RE_TASK1  = re.compile(r"\((\d+),(\d+),'[^']*',\d+,(-?\d+),")

_LOG = None


def log(msg=''):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if _LOG:
        _LOG.write(line + '\n')
        _LOG.flush()


def sha1_file(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def git_head():
    try:
        return subprocess.run(['git', 'rev-parse', '--short', 'HEAD'],
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception as e:  # not a repo, no git: say so
        return f'UNKNOWN ({type(e).__name__})'


def read_sql(path):
    """One streaming pass over the dump, as in v8h."""
    gun_dids, ast, post_auth, quote_src, qr_map, votes = set(), {}, {}, {}, {}, []
    with open(path, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f):
            if i % 50 == 0:
                print(f"  L{i} | post={len(post_auth):,} quote={len(quote_src):,} "
                      f"qr={len(qr_map):,} votes={len(votes):,}", end='\r', flush=True)
            if not line.startswith('INSERT'):
                continue
            m = RE_INSERT.match(line)
            if not m:
                continue
            tbl = m.group(1).lower()
            if tbl not in WANT:
                continue
            if tbl == 'discussion_topic':
                for did, tid in RE_DISC_T.findall(line):
                    if int(tid) == GUN_TOPIC_ID:
                        gun_dids.add(did)
            elif tbl == 'mturk_author_stance':
                for aid, tid, v1, v2 in RE_STANCE.findall(line):
                    if int(tid) == GUN_TOPIC_ID:
                        v1, v2 = int(v1), int(v2)
                        if v1 != v2:
                            ast[aid] = 0 if v1 > v2 else 1
            elif tbl == 'post':
                for did, pid, aid in RE_POST.findall(line):
                    if did in gun_dids:
                        post_auth[(did, pid)] = aid
            elif tbl == 'quote':
                for did, pid, qi, sd, sp in RE_QUOTE.findall(line):
                    if did in gun_dids:
                        quote_src[(did, pid, qi)] = (sd, sp)
            elif tbl == 'mturk_2010_qr_entry':
                for pg, tab, did, pid, qi in RE_QR.findall(line):
                    qr_map[(pg, tab)] = (did, pid, qi)
            elif tbl == 'mturk_2010_qr_task1_worker_response':
                for pg, tab, da in RE_TASK1.findall(line):
                    votes.append((pg, tab, int(da)))
    print(flush=True)
    return gun_dids, ast, post_auth, quote_src, qr_map, votes


def resolve(ast, post_auth, quote_src, qr_map, votes):
    """Vote -> (quoter, responder), exactly as v8h (pair_da[qtr_aid][rsp_aid])."""
    pair_votes = defaultdict(list)
    drops = Counter()
    for pg, tab, da in votes:
        entry = qr_map.get((pg, tab))
        if not entry:
            drops['no_qr'] += 1; continue
        did, pid, qi = entry
        rsp = post_auth.get((did, pid))
        if not rsp:
            drops['no_post'] += 1; continue
        src = quote_src.get((did, pid, qi))
        if not src:
            drops['no_quote'] += 1; continue
        qtr = post_auth.get(src)
        if not qtr:
            drops['no_post'] += 1; continue
        if ast.get(rsp) is None or ast.get(qtr) is None:
            drops['no_stance'] += 1; continue
        pair_votes[(qtr, rsp)].append(da)
    return pair_votes, drops


def components(nodes, edges):
    parent = {n: n for n in nodes}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    sizes = Counter(find(n) for n in nodes)
    return sorted(sizes.values(), reverse=True)


def main():
    global _LOG
    p = argparse.ArgumentParser()
    p.add_argument('--sql', default='fourforums_no_parse_2016_05_18.sql')
    p.add_argument('--out', default='out')
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    _LOG = open(out / 'run_v8i.log', 'w', encoding='utf-8')

    log('fourforums_pipeline_v8i')
    log(f'git HEAD: {git_head()}')
    sql = Path(args.sql)
    if not sql.exists():
        log(f'STOP: dump not found: {sql}')
        sys.exit(1)
    sha1 = sha1_file(sql)
    log(f'dump: {sql}  sha1={sha1}  expected={EXPECTED_SQL_SHA1}  match={sha1 == EXPECTED_SQL_SHA1}')
    if sha1 != EXPECTED_SQL_SHA1:
        log('STOP: the dump is not the expected one. Nothing written beyond this log.')
        sys.exit(1)

    log('reading dump...')
    gun_dids, ast, post_auth, quote_src, qr_map, votes = read_sql(sql)
    log(f'gun discussions={len(gun_dids):,}  authors with stance={len(ast):,} '
        f'(T0={sum(v == 0 for v in ast.values())}, T1={sum(v == 1 for v in ast.values())})')
    log(f'posts(gun)={len(post_auth):,}  quotes(gun)={len(quote_src):,}  '
        f'qr_entries={len(qr_map):,}  votes={len(votes):,}')

    da_all = Counter(da for _, _, da in votes)
    log('disagree_agree values, all votes (value: count):')
    log('  ' + '  '.join(f'{k}:{da_all[k]}' for k in sorted(da_all)))

    pair_votes, drops = resolve(ast, post_auth, quote_src, qr_map, votes)
    resolved = sum(len(v) for v in pair_votes.values())
    log(f'resolved votes={resolved:,}  dropped: ' + '  '.join(f'{k}={v:,}' for k, v in sorted(drops.items())))
    da_res = Counter(d for v in pair_votes.values() for d in v)
    log('disagree_agree values, resolved votes (value: count):')
    log('  ' + '  '.join(f'{k}:{da_res[k]}' for k in sorted(da_res)))

    # pairs table
    rows = []
    for (q, r), das in pair_votes.items():
        n, s = len(das), sum(das)
        rows.append({'quoter': q, 'responder': r,
                     'q_stance': ast[q], 'r_stance': ast[r],
                     'n': n, 'sum': s, 'mean': round(s / n, 6),
                     'n_negative': sum(d < 0 for d in das),
                     'n_zero': sum(d == 0 for d in das),
                     'n_positive': sum(d > 0 for d in das)})
    rows.sort(key=lambda x: (-x['n'], x['quoter'], x['responder']))
    with open(out / 'pairs_v8i.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['quoter'])
        w.writeheader()
        w.writerows(rows)

    # directed matrix, NaN = no data
    nodes = sorted({x['quoter'] for x in rows} | {x['responder'] for x in rows}, key=int)
    idx = {a: i for i, a in enumerate(nodes)}
    N = len(nodes)
    A = np.full((N, N), np.nan)
    for x in rows:
        A[idx[x['quoter']], idx[x['responder']]] = x['mean']
    np.save(out / 'A_v8i.npy', A)
    a_sha256 = hashlib.sha256((out / 'A_v8i.npy').read_bytes()).hexdigest()
    (out / 'nodes_v8i.json').write_text(json.dumps(
        [{'index': i, 'author_id': a, 'stance': ast[a]} for i, a in enumerate(nodes)], indent=1))

    # counts, no interpretation
    E = len(rows)
    self_pairs = sum(x['quoter'] == x['responder'] for x in rows)
    means = [x['mean'] for x in rows]
    neg, zero, pos = sum(m < 0 for m in means), sum(m == 0 for m in means), sum(m > 0 for m in means)
    dpairs = {(x['quoter'], x['responder']): x for x in rows}
    und = {}
    for (q, r) in dpairs:
        if q == r:
            continue
        und.setdefault(tuple(sorted((q, r), key=int)), []).append((q, r))
    both = [k for k, v in und.items() if len(v) == 2]
    one = len(und) - len(both)
    sign = lambda m: (m > 0) - (m < 0)
    both_sign_differs = sum(sign(dpairs[(a, b)]['mean']) != sign(dpairs[(b, a)]['mean']) for a, b in both)
    ncount = Counter(x['n'] for x in rows)
    bins = {'1': 0, '2': 0, '3-5': 0, '6-10': 0, '11-50': 0, '>50': 0}
    for n, c in ncount.items():
        k = '1' if n == 1 else '2' if n == 2 else '3-5' if n <= 5 else '6-10' if n <= 10 else '11-50' if n <= 50 else '>50'
        bins[k] += c
    comps = components(nodes, list(und.keys()))
    stance_block = defaultdict(lambda: {'pairs': 0, 'votes': 0, 'neg_pairs': 0})
    for x in rows:
        k = f"T{x['q_stance']}_quotes_T{x['r_stance']}"
        stance_block[k]['pairs'] += 1
        stance_block[k]['votes'] += x['n']
        stance_block[k]['neg_pairs'] += x['mean'] < 0

    # Signed triangles need one sign per undirected edge. That is a symmetrization,
    # i.e. a decision. Reported here only under one provisional, declared rule
    # (sign of the n-weighted mean of both directions); not used for anything else.
    usign = {}
    for k, v in und.items():
        tot_n = sum(dpairs[d]['n'] for d in v)
        tot_s = sum(dpairs[d]['sum'] for d in v)
        usign[k] = sign(tot_s / tot_n)
    adj = defaultdict(set)
    for a, b in und:
        adj[a].add(b); adj[b].add(a)
    tri = tri_frustrated = tri_with_zero = 0
    for a in nodes:
        for b, c in combinations(sorted(x for x in adj[a] if int(x) > int(a)), 2):
            if c in adj[b]:
                s = [usign[tuple(sorted(e, key=int))] for e in ((a, b), (a, c), (b, c))]
                tri += 1
                if 0 in s:
                    tri_with_zero += 1
                elif s[0] * s[1] * s[2] < 0:
                    tri_frustrated += 1

    summary = {
        'git_head': git_head(), 'sql_sha1': sha1, 'A_v8i_sha256': a_sha256,
        'inherited_from_v8h': ['topic 9 only', 'stance ties dropped', 'full chain required'],
        'disagree_agree_values_all': dict(sorted(da_all.items())),
        'disagree_agree_values_resolved': dict(sorted(da_res.items())),
        'votes_total': len(votes), 'votes_resolved': resolved, 'votes_dropped': dict(drops),
        'N_authors': N, 'E_directed_pairs': E, 'self_pairs': self_pairs,
        'pairs_mean_negative': neg, 'pairs_mean_zero': zero, 'pairs_mean_positive': pos,
        'undirected_pairs': len(und), 'undirected_both_directions': len(both),
        'undirected_one_direction': one, 'both_directions_sign_differs': both_sign_differs,
        'n_per_directed_pair': bins,
        'components_sizes_top10': comps[:10], 'components_count': len(comps),
        'by_stance': dict(stance_block),
        'triangles_provisional_rule': 'sign of n-weighted mean over both directions',
        'triangles': tri, 'triangles_frustrated': tri_frustrated, 'triangles_with_zero_edge': tri_with_zero,
        'left_open_for_delamor': ['symmetrization A -> W', 'n_min for W', 'which N (2^N states)', 'null model'],
    }
    (out / 'summary_v8i.json').write_text(json.dumps(summary, indent=1))

    log('=' * 60)
    for k, v in summary.items():
        log(f'{k}: {v}')
    log('=' * 60)
    log(f'written in {out}/: pairs_v8i.csv, A_v8i.npy, nodes_v8i.json, summary_v8i.json, run_v8i.log')
    log('done. These are counts; they say nothing yet about what the structure means.')
    _LOG.close()


if __name__ == '__main__':
    main()
