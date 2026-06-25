#!/usr/bin/env python3
"""
fourforums_pipeline_v8h.py
W asimétrico desde mturk_2010_qr_task1_worker_response.disagree_agree.
Cadena: task1_vote → qr_entry → post(responder) → quote → post(quoter) → stance
"""
import re, json, sys, argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime

GUN_TOPIC_ID = 9

WANT = {
    'discussion_topic', 'mturk_author_stance', 'post',
    'quote', 'mturk_2010_qr_entry', 'mturk_2010_qr_task1_worker_response',
}

RE_INSERT = re.compile(r'INSERT INTO `?(\w+)`?', re.I)
RE_DISC_T = re.compile(r'\((\d+),(\d+)')
RE_STANCE = re.compile(r'\(\d+,(\d+),(\d+),\d+,(\d+),\d+,(\d+),')
RE_POST   = re.compile(r'\((\d+),(\d+),(\d+),')
RE_QUOTE  = re.compile(r'\((\d+),(\d+),(\d+),(?:\d+|NULL),\d+,\d+,(\d+),(\d+),')
RE_QR     = re.compile(r'\((\d+),(\d+),(\d+),(\d+),(\d+),')
RE_TASK1  = re.compile(r"\((\d+),(\d+),'[^']*',\d+,(-?\d+),")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sql', default='trace/fourforums_no_parse_2016_05_18.sql')
    p.add_argument('--log', default='run_v8h.log')
    args = p.parse_args()

    gun_dids  = set()
    ast       = {}         # author_id -> stance (0|1), topic=9
    post_auth = {}         # (did,pid) -> aid
    quote_src = {}         # (did,pid,qi) -> (src_did,src_pid)
    qr_map    = {}         # (pg,tab) -> (did,pid,qi)
    votes     = []         # (pg,tab,da)

    log(f"Leyendo: {args.sql}")
    with open(args.sql, encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f):
            if i % 50 == 0:
                print(f"  L{i} | post={len(post_auth):,} quote={len(quote_src):,} "
                      f"qr={len(qr_map):,} votes={len(votes):,}", end='\r', flush=True)
            if not line.startswith('INSERT'): continue
            m = RE_INSERT.match(line)
            if not m: continue
            tbl = m.group(1).lower()
            if tbl not in WANT: continue

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
    log(f"Lectura completa.")
    log(f"  gun_dids={len(gun_dids):,}  stanced={len(ast):,}")
    log(f"  post_auth(gun)={len(post_auth):,}  quote_src(gun)={len(quote_src):,}")
    log(f"  qr_map={len(qr_map):,}  votes={len(votes):,}")

    log("Construyendo W_asim...")
    pair_da = defaultdict(lambda: defaultdict(list))
    no_qr = no_post = no_quote = no_stance = resolved = 0

    for pg, tab, da in votes:
        entry = qr_map.get((pg, tab))
        if not entry: no_qr += 1; continue
        did, pid, qi = entry

        rsp_aid = post_auth.get((did, pid))
        if not rsp_aid: no_post += 1; continue

        src = quote_src.get((did, pid, qi))
        if not src: no_quote += 1; continue
        qtr_aid = post_auth.get(src)
        if not qtr_aid: no_post += 1; continue

        if ast.get(rsp_aid) is None or ast.get(qtr_aid) is None:
            no_stance += 1; continue

        pair_da[qtr_aid][rsp_aid].append(da)
        resolved += 1

    log(f"  resueltos={resolved:,}  no_qr={no_qr:,}  no_post={no_post:,}  "
        f"no_quote={no_quote:,}  no_stance={no_stance:,}")

    stance_stats = defaultdict(lambda: {'n':0,'sum':0.0,'neg':0,'pos':0})
    pairs = []

    for qtr, responders in pair_da.items():
        qs = ast[qtr]
        for rsp, das in responders.items():
            rs = ast[rsp]
            n = len(das); s = sum(das)
            k = f"T{qs}_quotes_T{rs}"
            stance_stats[k]['n'] += n
            stance_stats[k]['sum'] += s
            stance_stats[k]['neg'] += sum(1 for d in das if d < 0)
            stance_stats[k]['pos'] += sum(1 for d in das if d > 0)
            if n >= 2:
                pairs.append({'quoter':qtr,'responder':rsp,
                              'q_stance':qs,'r_stance':rs,
                              'n':n,'mean_da':round(s/n,3)})

    stance_summary = {k: {'n':v['n'],
                           'mean_da':round(v['sum']/v['n'],3) if v['n'] else 0,
                           'pct_disagree':round(100*v['neg']/v['n'],1) if v['n'] else 0,
                           'pct_agree':round(100*v['pos']/v['n'],1) if v['n'] else 0}
                      for k,v in stance_stats.items()}

    pairs.sort(key=lambda x: -x['n'])

    result = {
        'meta': {
            'gun_dids': len(gun_dids),
            'stanced_authors': len(ast),
            'T0': sum(1 for v in ast.values() if v==0),
            'T1': sum(1 for v in ast.values() if v==1),
            'qr_pairs': len(qr_map),
            'total_votes': len(votes),
            'resolved_votes': resolved,
            'author_pairs_n2plus': len(pairs),
        },
        'stance_asymmetry': stance_summary,
        'top_pairs': pairs[:100],
    }

    Path('W_asim_v8h.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    log("Guardado: W_asim_v8h.json")

    print("\n" + "="*60)
    print("STANCE ASYMMETRY")
    print("="*60)
    for k, v in sorted(stance_summary.items()):
        print(f"  {k}: n={v['n']:,}  mean_da={v['mean_da']:+.3f}  "
              f"disagree={v['pct_disagree']}%  agree={v['pct_agree']}%")
    print(f"\n  Pares autor N≥2: {len(pairs):,}")
    print("\nListo.")

if __name__ == '__main__':
    main()
