#!/usr/bin/env python3
"""
build_W_v8m.py

Extraction step for fourforums: from the author pairs of
fourforums_pipeline_v8l.py (out/pairs_v8l.csv) it produces SEVERAL W, each
one with its extraction declared as data, in the format the ckm repo reads
({"nodes": [...], "W": [[...]], ...}). It does not run CKM; CKM measures
these W in the ckm repo. It reads no dump: only v8l's outputs.

Why more than one W: the sign comes from the annotators, but symmetrizing,
choosing nodes and scaling are extraction (ours). Each W below changes ONE
thing against W_obs, so what the instrument sees can be traced to that one
thing. Each is a question, not a preference.

Operators common to all (declared):
  O1 pairs: pairs_v8l.csv rows with self_pair = 0 (K1).
  O2 symmetrization: W_ij = (sum_ij + sum_ji) / (n_ij + n_ji), the
     n-weighted mean of the votes of both directions; one direction only ->
     that direction. (Same rule as the provisional triangle sign of v8i-v8l.)
  O3 nodes: the largest connected component of the undirected graph; the
     other components are named in the declaration, not used.
  O4 scale: divide by max |W| (as corpus_service in ckm) -> W in [-1, 1].
  O5 diagonal: 0 (K1).
  O6 absence: W_ij = 0 means NO PAIR in the corpus (in A it was NaN).
     In W, 0 cannot tell "no pair" from "pair with mean 0" (12 such edges in
     v8l); both are 0 here, and the count is declared.
  O7 node names: anonymized as a000, a001, ... in W files; the map to IAC
     author ids goes to a separate file (nodes_map_v8m.json), never with W.

The W produced:
  W_obs         O1-O7. The observed one.
  W_sign        sign(W_obs) in {-1, 0, +1}: same edges and signs, no
                magnitudes. Asks how much the instrument depends on weights.
  W_presence    (n_ij + n_ji) / max: same edges, all positive (vote counts,
                sign removed). The presence-only analog of ckm's W: no
                frustration by construction.
  W_null_s{k}   W_obs with its edge SIGNS permuted among its edges (as L3),
                magnitudes kept per edge; k = 1..5 seeds. Known answer: no
                structure in who-agrees-with-whom beyond the sign counts.

Outputs (in --out/W, default out/W/; keep out/ out of git):
  W_<name>_v8m.json   one per W: nodes, W, source, declaration
  nodes_map_v8m.json  a### -> IAC author_id and stance
  manifest_v8m.json   every W with its sha256, and the parents' hashes
  run_v8m.log

Usage:
  python build_W_v8m.py
  python build_W_v8m.py --out out --null_seeds 5
"""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

SEED_BASE = 20261023
_LOG = None


def log(msg=''):
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if _LOG:
        _LOG.write(line + '\n')
        _LOG.flush()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


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
    groups = defaultdict(list)
    for n in nodes:
        groups[find(n)].append(n)
    return sorted(groups.values(), key=lambda g: (-len(g), min(int(x) for x in g)))


def main():
    global _LOG
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='out')
    p.add_argument('--null_seeds', type=int, default=5)
    args = p.parse_args()
    out = Path(args.out)
    wdir = out / 'W'
    wdir.mkdir(parents=True, exist_ok=True)
    _LOG = open(wdir / 'run_v8m.log', 'w', encoding='utf-8')
    log('build_W_v8m')

    pairs_path = out / 'pairs_v8l.csv'
    summary_path = out / 'summary_v8l.json'
    if not pairs_path.exists() or not summary_path.exists():
        log('STOP: run fourforums_pipeline_v8l.py first (needs out/pairs_v8l.csv, out/summary_v8l.json)')
        raise SystemExit(1)
    parent = {
        'pairs_v8l_sha256': sha256_bytes(pairs_path.read_bytes()),
        'summary_v8l': {k: json.loads(summary_path.read_text()).get(k)
                        for k in ('git_head', 'sql_sha1', 'A_v8l_sha256')},
    }
    log(f"parents: {parent}")

    rows = []
    with open(pairs_path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if int(r['self_pair']):
                continue                                          # O1
            rows.append(r)
    stance = {}
    und = defaultdict(lambda: [0.0, 0])                           # O2: [sum, n]
    for r in rows:
        q, s = r['quoted_author'], r['responding_author']
        stance[q] = int(r['quoted_stance']); stance[s] = int(r['responding_stance'])
        k = tuple(sorted((q, s), key=int))
        und[k][0] += float(r['sum']); und[k][1] += int(r['n'])
    log(f'non-self directed pairs: {len(rows)}  undirected edges: {len(und)}')

    comps = components(sorted(stance, key=int), list(und))        # O3
    giant = sorted(comps[0], key=int)
    others = [sorted(c, key=int) for c in comps[1:]]
    log(f'components: {[len(c) for c in comps]}  -> nodes = largest ({len(giant)})')
    idx = {a: i for i, a in enumerate(giant)}
    N = len(giant)
    anon = [f'a{i:03d}' for i in range(N)]                        # O7

    raw = np.zeros((N, N))
    cnt = np.zeros((N, N))
    mean_zero_edges = 0
    for (a, b), (s, n) in und.items():
        if a in idx and b in idx:
            m = s / n
            raw[idx[a], idx[b]] = raw[idx[b], idx[a]] = m
            cnt[idx[a], idx[b]] = cnt[idx[b], idx[a]] = n
            mean_zero_edges += (m == 0)
    np.fill_diagonal(raw, 0.0); np.fill_diagonal(cnt, 0.0)       # O5
    E = int((cnt > 0).sum() // 2)
    log(f'edges in largest component: {E}  edges with mean exactly 0: {mean_zero_edges}')

    def scaled(M):                                                # O4
        mx = float(np.abs(M).max())
        return (M / mx if mx > 0 else M), mx

    common = {
        'O1': 'pairs_v8l.csv rows with self_pair = 0',
        'O2': 'W_ij = (sum_ij + sum_ji) / (n_ij + n_ji); one direction -> that direction',
        'O3': f'largest connected component ({N} nodes); not used: {[len(c) for c in others]}',
        'O4': 'divide by max |W|',
        'O5': 'diagonal 0',
        'O6': f'0 = no pair; also 0 for {mean_zero_edges} edges whose mean is exactly 0',
        'O7': 'nodes anonymized a###; map in nodes_map_v8m.json',
        'parents': parent,
        'producer': 'build_W_v8m.py (ckmdatasets)',
    }

    Ws = {}
    W_obs, mx_obs = scaled(raw)
    Ws['W_obs'] = (W_obs, {'variant': 'observed', 'scale_max_abs_before': mx_obs})
    Ws['W_sign'] = (np.sign(W_obs), {'variant': 'sign(W_obs): magnitudes removed'})
    W_pres, mx_pres = scaled(cnt)
    Ws['W_presence'] = (W_pres, {'variant': 'vote counts per edge, all positive (sign removed)',
                                 'scale_max_abs_before': mx_pres})
    iu = np.triu_indices(N, 1)
    edge = cnt[iu] > 0
    signs = np.sign(W_obs[iu][edge])
    mags = np.abs(W_obs[iu][edge])
    for k in range(1, args.null_seeds + 1):
        rng = np.random.default_rng([SEED_BASE, 8, k])
        perm = rng.permutation(signs)
        M = np.zeros((N, N))
        vals = np.zeros(len(iu[0])); vals[edge] = perm * mags
        M[iu] = vals; M = M + M.T
        Ws[f'W_null_s{k}'] = (M, {'variant': 'W_obs edge signs permuted among edges, magnitudes kept per edge',
                                  'seed': [SEED_BASE, 8, k]})

    manifest = {'common_declaration': common, 'W': {}}
    for name, (M, extra) in Ws.items():
        assert np.allclose(M, M.T) and np.all(np.diag(M) == 0)
        obj = {'nodes': anon, 'W': np.round(M, 8).tolist(),
               'source': f'fourforums gun control, IAC dump sha1 {parent["summary_v8l"]["sql_sha1"]}',
               'declaration': {**common, **extra}}
        b = json.dumps(obj).encode('utf-8')
        (wdir / f'{name}_v8m.json').write_bytes(b)
        neg = int((M[iu] < 0).sum()); pos = int((M[iu] > 0).sum())
        manifest['W'][name] = {'file': f'{name}_v8m.json', 'sha256': sha256_bytes(b),
                               'N': N, 'edges_neg': neg, 'edges_pos': pos,
                               'edges_zero_with_pair': int(edge.sum()) - neg - pos}
        log(f"{name}: N={N} neg={neg} pos={pos} sha256={manifest['W'][name]['sha256'][:16]}…")
    (wdir / 'nodes_map_v8m.json').write_text(json.dumps(
        [{'node': anon[i], 'author_id': a, 'stance': stance[a]} for i, a in enumerate(giant)], indent=1))
    (wdir / 'manifest_v8m.json').write_text(json.dumps(manifest, indent=1))
    log(f'written in {wdir}/: {len(Ws)} W, nodes_map_v8m.json, manifest_v8m.json, run_v8m.log')
    log('done. These W are extraction products; what CKM sees in them is measured in the ckm repo.')
    _LOG.close()


if __name__ == '__main__':
    main()
