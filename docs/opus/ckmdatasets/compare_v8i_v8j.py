#!/usr/bin/env python3
"""
compare_v8i_v8j.py

Compares the outputs of fourforums_pipeline_v8i.py and fourforums_pipeline_v8j.py
and lists ONLY the differences, each marked as:
  DECLARED   - a difference v8j's docstring announces (J1 naming, J2 unsure)
  UNDECLARED - anything else; this is the divergence to look at
It interprets nothing.

What it compares (all in --out, default out/):
  summary_v8i.json  vs summary_v8j.json   key by key, after mapping J1 names
  A_v8i.npy         vs A_v8j.npy          cell by cell (NaN == NaN)
  nodes_v8i.json    vs nodes_v8j.json     same order, ids and stances
  pairs_v8i.csv     vs pairs_v8j.csv      row by row, after mapping J1 columns

Writes compare_v8i_v8j.log in --out and prints the same.

Usage:
  python compare_v8i_v8j.py
  python compare_v8i_v8j.py --out out
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

# J1: v8i name -> v8j name
J1_COLUMNS = {'quoter': 'quoted_author', 'responder': 'responding_author',
              'q_stance': 'quoted_stance', 'r_stance': 'responding_stance'}
# keys that exist only because of the version label or J2
DECLARED_ONLY_IN_J = {'J2_unsure_votes_all', 'J2_unsure_votes_resolved',
                      'declared_changes_vs_v8i', 'A_v8j_sha256'}
DECLARED_ONLY_IN_I = {'A_v8i_sha256'}
J2_COLUMNS = {'n_unsure'}

lines = []


def say(msg=''):
    print(msg)
    lines.append(msg)


def j1_stance_key(k):
    """v8i 'T0_quotes_T1' -> v8j 'T0_quoted_by_T1' (same pair, new name)."""
    return k.replace('_quotes_', '_quoted_by_')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', default='out')
    out = Path(p.parse_args().out)
    undeclared = 0

    # --- summary ---
    si = json.loads((out / 'summary_v8i.json').read_text())
    sj = json.loads((out / 'summary_v8j.json').read_text())
    say('== summary_v8i.json vs summary_v8j.json')
    for k in sorted(set(si) | set(sj)):
        if k in DECLARED_ONLY_IN_J and k not in si:
            say(f'  DECLARED   {k}: only in v8j = {sj[k]}')
            continue
        if k in DECLARED_ONLY_IN_I and k not in sj:
            continue  # its counterpart A_v8j_sha256 is compared below
        vi, vj = si.get(k), sj.get(k)
        if k == 'by_stance' and isinstance(vi, dict):
            vi = {j1_stance_key(a): b for a, b in vi.items()}
            if vi == vj:
                say('  DECLARED   by_stance: same values, J1 key names (quotes -> quoted_by)')
                continue
        if vi != vj:
            undeclared += 1
            say(f'  UNDECLARED {k}: v8i={vi} | v8j={vj}')
    if si.get('A_v8i_sha256') != sj.get('A_v8j_sha256'):
        undeclared += 1
        say(f"  UNDECLARED A sha256: v8i={si.get('A_v8i_sha256')} | v8j={sj.get('A_v8j_sha256')}")
    else:
        say('  same       A sha256')
    if si.get('votes_total') != sj.get('votes_total'):
        say('  NOTE       votes_total differs: the J2 regex change itself is the divergence')

    # --- matrix ---
    say('== A_v8i.npy vs A_v8j.npy')
    Ai, Aj = np.load(out / 'A_v8i.npy'), np.load(out / 'A_v8j.npy')
    if Ai.shape != Aj.shape:
        undeclared += 1
        say(f'  UNDECLARED shape: {Ai.shape} | {Aj.shape}')
    else:
        diff = ~((Ai == Aj) | (np.isnan(Ai) & np.isnan(Aj)))
        n = int(diff.sum())
        if n:
            undeclared += 1
            say(f'  UNDECLARED {n} cells differ (first: {list(zip(*np.nonzero(diff)))[:5]})')
        else:
            say(f'  same       {Ai.shape[0]}x{Ai.shape[1]}, NaN in the same cells')

    # --- nodes ---
    say('== nodes_v8i.json vs nodes_v8j.json')
    ni = json.loads((out / 'nodes_v8i.json').read_text())
    nj = json.loads((out / 'nodes_v8j.json').read_text())
    if ni != nj:
        undeclared += 1
        say(f'  UNDECLARED nodes differ (v8i {len(ni)}, v8j {len(nj)})')
    else:
        say(f'  same       {len(ni)} nodes, same order and stances')

    # --- pairs ---
    say('== pairs_v8i.csv vs pairs_v8j.csv')
    with open(out / 'pairs_v8i.csv', encoding='utf-8') as f:
        ri = [{J1_COLUMNS.get(c, c): v for c, v in row.items()} for row in csv.DictReader(f)]
    with open(out / 'pairs_v8j.csv', encoding='utf-8') as f:
        rj = list(csv.DictReader(f))
    say('  DECLARED   columns renamed by J1: ' + ', '.join(f'{a}->{b}' for a, b in J1_COLUMNS.items()))
    if rj and J2_COLUMNS & set(rj[0]):
        say('  DECLARED   column added by J2: n_unsure')
    rj_cmp = [{c: v for c, v in row.items() if c not in J2_COLUMNS} for row in rj]
    if ri != rj_cmp:
        undeclared += 1
        bad = sum(a != b for a, b in zip(ri, rj_cmp)) + abs(len(ri) - len(rj_cmp))
        say(f'  UNDECLARED {bad} rows differ (v8i {len(ri)} rows, v8j {len(rj_cmp)} rows)')
    else:
        say(f'  same       {len(ri)} rows, same values')

    say('')
    say(f'undeclared differences: {undeclared}')
    say('These are differences, not readings.')
    (out / 'compare_v8i_v8j.log').write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
