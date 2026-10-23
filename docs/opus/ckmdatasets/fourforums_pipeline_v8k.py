#!/usr/bin/env python3
"""
fourforums_pipeline_v8k.py

Same as fourforums_pipeline_v8k.py (v8h access layer, J1 naming, J2 unsure
reported) with two DECLARED changes (delamor, 23 oct 2026):

K1 — diagonal zero by construction.
  A pair where an author answers his own post (quoted_author ==
  responding_author) is kept in pairs_v8k.csv with self_pair = 1, but it is
  EXCLUDED from A (A[i, i] = 0.0, as W's diagonal in the ckm repo,
  corpus_service.py fill_diagonal) and from every count below (E, signs,
  stance blocks, triangles, null). The node list is the same as v8j's, so A
  keeps v8j's shape; an author present only in a self pair stays as an
  isolated node.

K2 — null model for the signed triangles: shuffle the votes.
  The graph is kept (which pairs exist and how many votes each has); the
  pooled resolved votes of the non-self pairs are permuted at random and
  dealt back with the same n per pair. Each run recomputes the pair sums,
  the provisional undirected sign (sign of the n-weighted mean of both
  directions, as in v8i/v8j) and the number of frustrated triangles.
  It keeps the vote distribution and breaks who agrees with whom.
  Reported: observed vs null (mean, sd, z, empirical one-sided p, both
  sides). Default 1000 runs, seed 20261023. No reading of the result.

No cut on n (delamor: "sin corte"). n = annotator votes; the unit is the
annotated quote-response pair (not an "interaction": static corpus, not a
live run). Still open for delamor: symmetrization A -> W, which N.

Outputs (in --out, default out/; keep out/ out of git: it has author ids):
  pairs_v8k.csv, A_v8k.npy, nodes_v8k.json, summary_v8k.json, run_v8k.log

Usage:
  python fourforums_pipeline_v8k.py
  python fourforums_pipeline_v8k.py --null_runs 1000 --seed 20261023
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
RE_TASK1  = re.compile(r"\((\d+),(\d+),'[^']*',\d+,(-?\d+),(\d+),")  # J2: + disagree_agree_unsure

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
                for pg, tab, da, uns in RE_TASK1.findall(line):
                    votes.append((pg, tab, int(da), int(uns)))
    print(flush=True)
    return gun_dids, ast, post_auth, quote_src, qr_map, votes


def resolve(ast, post_auth, quote_src, qr_map, votes):
    """Vote -> (quoted_author, responding_author). Same chain and drops as v8h."""
    pair_votes = defaultdict(list)
    pair_unsure = Counter()
    drops = Counter()
    for pg, tab, da, uns in votes:
        entry = qr_map.get((pg, tab))
        if not entry:
            drops['no_qr'] += 1; continue
        did, pid, qi = entry
        responding = post_auth.get((did, pid))
        if not responding:
            drops['no_post'] += 1; continue
        src = quote_src.get((did, pid, qi))
        if not src:
            drops['no_quote'] += 1; continue
        quoted = post_auth.get(src)
        if not quoted:
            drops['no_post'] += 1; continue
        if ast.get(responding) is None or ast.get(quoted) is None:
            drops['no_stance'] += 1; continue
        pair_votes[(quoted, responding)].append(da)
        pair_unsure[(quoted, responding)] += uns
    return pair_votes, drops, pair_unsure


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
    p.add_argument('--null_runs', type=int, default=1000)
    p.add_argument('--seed', type=int, default=20261023)
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    _LOG = open(out / 'run_v8k.log', 'w', encoding='utf-8')

    log('fourforums_pipeline_v8k')
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

    da_all = Counter(v[2] for v in votes)
    unsure_all = sum(v[3] for v in votes)
    log(f'J2 unsure-marked votes, all: {unsure_all:,} of {len(votes):,}')
    log('disagree_agree values, all votes (value: count):')
    log('  ' + '  '.join(f'{k}:{da_all[k]}' for k in sorted(da_all)))

    pair_votes, drops, pair_unsure = resolve(ast, post_auth, quote_src, qr_map, votes)
    resolved = sum(len(v) for v in pair_votes.values())
    log(f'resolved votes={resolved:,}  dropped: ' + '  '.join(f'{k}={v:,}' for k, v in sorted(drops.items())))
    da_res = Counter(d for v in pair_votes.values() for d in v)
    log('disagree_agree values, resolved votes (value: count):')
    log('  ' + '  '.join(f'{k}:{da_res[k]}' for k in sorted(da_res)))

    # pairs table
    rows = []
    for (q, r), das in pair_votes.items():
        n, s = len(das), sum(das)
        rows.append({'quoted_author': q, 'responding_author': r,
                     'quoted_stance': ast[q], 'responding_stance': ast[r],
                     'n': n, 'sum': s, 'mean': round(s / n, 6),
                     'n_negative': sum(d < 0 for d in das),
                     'n_zero': sum(d == 0 for d in das),
                     'n_positive': sum(d > 0 for d in das),
                     'n_unsure': pair_unsure[(q, r)],
                     'self_pair': int(q == r)})
    rows.sort(key=lambda x: (-x['n'], x['quoted_author'], x['responding_author']))
    with open(out / 'pairs_v8k.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['quoted_author'])
        w.writeheader()
        w.writerows(rows)

    # directed matrix, NaN = no data
    nodes = sorted({x['quoted_author'] for x in rows} | {x['responding_author'] for x in rows}, key=int)
    idx = {a: i for i, a in enumerate(nodes)}
    N = len(nodes)
    A = np.full((N, N), np.nan)
    all_rows = rows
    rows = [x for x in all_rows if not x['self_pair']]   # K1
    for x in rows:
        A[idx[x['quoted_author']], idx[x['responding_author']]] = x['mean']
    np.fill_diagonal(A, 0.0)                              # K1
    np.save(out / 'A_v8k.npy', A)
    a_sha256 = hashlib.sha256((out / 'A_v8k.npy').read_bytes()).hexdigest()
    (out / 'nodes_v8k.json').write_text(json.dumps(
        [{'index': i, 'author_id': a, 'stance': ast[a]} for i, a in enumerate(nodes)], indent=1))

    # counts, no interpretation
    E = len(rows)
    self_pairs = len(all_rows) - len(rows)   # K1: excluded
    means = [x['mean'] for x in rows]
    neg, zero, pos = sum(m < 0 for m in means), sum(m == 0 for m in means), sum(m > 0 for m in means)
    dpairs = {(x['quoted_author'], x['responding_author']): x for x in rows}
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
        k = f"T{x['quoted_stance']}_quoted_by_T{x['responding_stance']}"
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

    # K2: null by shuffling votes (graph and n per pair fixed)
    keys = list(dpairs.keys())
    kpos = {k: i for i, k in enumerate(keys)}
    pooled = np.array([d for k in keys for d in pair_votes[k]], dtype=float)
    ns = np.array([len(pair_votes[k]) for k in keys])
    starts = np.concatenate([[0], np.cumsum(ns)[:-1]])
    ukeys = list(und.keys())
    upos = {k: i for i, k in enumerate(ukeys)}
    U = np.zeros((len(ukeys), len(keys)))
    for k, v in und.items():
        for d in v:
            U[upos[k], kpos[d]] = 1.0
    tris = []
    for a in nodes:
        for b, c in combinations(sorted(x for x in adj[a] if int(x) > int(a)), 2):
            if c in adj[b]:
                tris.append([upos[tuple(sorted(e, key=int))] for e in ((a, b), (a, c), (b, c))])
    tris = np.array(tris, dtype=int).reshape(-1, 3)

    def frustration(vote_array):
        sums = np.add.reduceat(vote_array, starts) if len(vote_array) else np.zeros(0)
        us = np.sign(U @ sums)
        if not len(tris):
            return 0, 0, float(np.mean(us < 0)) if len(us) else 0.0
        t = us[tris]
        has_zero = (t == 0).any(axis=1)
        frus = (~has_zero) & (t.prod(axis=1) < 0)
        return int(frus.sum()), int(has_zero.sum()), float(np.mean(us < 0))

    obs_f, obs_z, obs_neg = frustration(pooled)
    assert obs_f == tri_frustrated and obs_z == tri_with_zero, 'K2 observed differs from direct count'
    rng = np.random.default_rng(args.seed)
    null_f, null_neg = [], []
    for _ in range(args.null_runs):
        f_, z_, n_ = frustration(rng.permutation(pooled))
        null_f.append(f_); null_neg.append(n_)
    null_f = np.array(null_f, dtype=float); null_neg = np.array(null_neg)
    sd = float(null_f.std(ddof=1)) if args.null_runs > 1 else float('nan')
    null_block = {
        'runs': args.null_runs, 'seed': args.seed,
        'what_is_shuffled': 'pooled resolved votes of non-self pairs; graph and n per pair fixed',
        'observed_frustrated': obs_f,
        'null_mean': round(float(null_f.mean()), 3), 'null_sd': round(sd, 3),
        'z': round((obs_f - float(null_f.mean())) / sd, 3) if sd and sd == sd else None,
        'p_null_le_observed': round((1 + int((null_f <= obs_f).sum())) / (1 + args.null_runs), 4),
        'p_null_ge_observed': round((1 + int((null_f >= obs_f).sum())) / (1 + args.null_runs), 4),
        'observed_frac_negative_undirected': round(obs_neg, 4),
        'null_frac_negative_undirected_mean': round(float(null_neg.mean()), 4),
    }

    summary = {
        'git_head': git_head(), 'sql_sha1': sha1, 'A_v8k_sha256': a_sha256,
        'inherited_from_v8h': ['topic 9 only', 'stance ties dropped', 'full chain required'],
        'disagree_agree_values_all': dict(sorted(da_all.items())),
        'disagree_agree_values_resolved': dict(sorted(da_res.items())),
        'J2_unsure_votes_all': unsure_all, 'J2_unsure_votes_resolved': sum(pair_unsure.values()),
        'declared_changes_vs_v8i': ['J1 naming quoted_author/responding_author', 'J2 unsure flag read and reported, not used'],
        'declared_changes_vs_v8j': ['K1 self pairs excluded, diagonal 0', 'K2 null by vote shuffle'],
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
        'K2_null_vote_shuffle': null_block,
        'n_cut': 'none (delamor)',
        'left_open_for_delamor': ['symmetrization A -> W', 'which N'],
    }
    (out / 'summary_v8k.json').write_text(json.dumps(summary, indent=1))

    log('=' * 60)
    for k, v in summary.items():
        log(f'{k}: {v}')
    log('=' * 60)
    log(f'written in {out}/: pairs_v8k.csv, A_v8k.npy, nodes_v8k.json, summary_v8k.json, run_v8k.log')
    log('done. These are counts; they say nothing yet about what the structure means.')
    _LOG.close()


if __name__ == '__main__':
    main()
