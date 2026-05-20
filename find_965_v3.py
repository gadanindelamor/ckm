"""
find_965_v3.py
Candidatos a polo sostenedor puro en fourforums - clave compuesta (disc_id, post_id).
Usa todos los autores activos en gun_disc_ids.
"""
import re
from collections import defaultdict, Counter

SQL = 'fourforums_no_parse_2016_05_18.sql'
create_re = re.compile(r'CREATE TABLE `?(\w+)`?', re.I)
col_re    = re.compile(r'^\s*`(\w+)`', re.I)
insert_re = re.compile(r'INSERT INTO `?(\w+)`?\s+(?:VALUES|values)\s*(.+)', re.DOTALL)

def tokenize(s):
    tokens, i = [], 0
    while i < len(s):
        c = s[i]
        if c in (' ','\t'): i+=1; continue
        if c == ',': i+=1; continue
        if c == "'":
            j=i+1; buf=[]
            while j<len(s):
                if s[j]=='\\' and j+1<len(s): buf.append(s[j+1]); j+=2
                elif s[j]=="'": j+=1; break
                else: buf.append(s[j]); j+=1
            tokens.append(''.join(buf)); i=j
        elif s[i:i+4].upper()=='NULL': tokens.append(None); i+=4
        else:
            j=i
            while j<len(s) and s[j] not in (',',')'): j+=1
            val=s[i:j].strip()
            try: tokens.append(int(val))
            except:
                try: tokens.append(float(val))
                except: tokens.append(val)
            i=j
    return tokens

def split_groups(vs):
    groups,depth,start=[],0,None
    for i,c in enumerate(vs):
        if c=='(':
            if depth==0: start=i+1
            depth+=1
        elif c==')':
            depth-=1
            if depth==0 and start is not None:
                groups.append(vs[start:i]); start=None
    return groups

WANT = {'discussion_topic','mturk_author_stance','post','quote'}
SKIP = {'text','markup','report','session','notification','email','log',
        'mturk_2010_p123_post','mturk_2010_p123_entry','mturk_2010_p123_worker_response',
        'mturk_2010_qr_entry','mturk_2010_qr_task1_average_response',
        'mturk_2010_qr_task1_worker_response','mturk_2010_qr_task2_average_response',
        'mturk_2010_qr_task2_worker_response'}

raw = defaultdict(list)
col_names = {}
current = None; in_c = False

print("Parseando...", flush=True)
with open(SQL, encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        if i % 100_000 == 0: print(f"  {i:,}", end='\r', flush=True)
        m = create_re.match(line)
        if m:
            current=m.group(1).lower(); col_names[current]=[]; in_c=True; continue
        if in_c:
            if re.match(r'\s*\)', line): in_c=False; continue
            cm=col_re.match(line)
            if cm: col_names[current].append(cm.group(1).lower())
            continue
        m = insert_re.match(line.rstrip())
        if not m: continue
        tbl = m.group(1).lower()
        if tbl in SKIP or tbl not in WANT: continue
        cols = col_names.get(tbl,[])
        for g in split_groups(m.group(2).rstrip(';')):
            try: row=tokenize(g)
            except: continue
            if cols and len(row)==len(cols):
                raw[tbl].append(dict(zip(cols,row)))
            elif cols:
                raw[tbl].append({cols[k]:row[k] for k in range(min(len(cols),len(row)))})

print(f"\nPost: {len(raw['post']):,} | Quote: {len(raw['quote']):,}")

# gun_disc_ids
gun = {r['discussion_id'] for r in raw['discussion_topic'] if r.get('topic_id')==9}
print(f"Discusiones gun: {len(gun)}")

# stance por autor (votos)
author_stance = {}
for r in raw['mturk_author_stance']:
    if r.get('discussion_id') not in gun: continue
    aid = r.get('author_id')
    if aid is None: continue
    try:
        v1=int(r.get('topic_stance_votes_1') or 0)
        v2=int(r.get('topic_stance_votes_2') or 0)
    except: continue
    if v1==v2: continue
    author_stance[int(aid)] = 0 if v1>v2 else 1

# post_id -> author_id (TODOS los posts gun, sin filtro stance)
post_author = {}
for r in raw['post']:
    did=r.get('discussion_id')
    if did not in gun: continue
    pid=r.get('post_id'); aid=r.get('author_id')
    if pid and aid and did: post_author[(did,pid)]=aid  # clave compuesta

print(f"Posts gun: {len(post_author):,}")

# in/out por autor (citas entre autores distintos)
in_deg  = Counter()
out_deg = Counter()
for q in raw['quote']:
    if q.get('discussion_id') not in gun: continue
    src_auth = post_author.get((q.get('source_discussion_id'), q.get('source_post_id')))
    tgt_auth = post_author.get((q.get('discussion_id'), q.get('post_id')))
    if src_auth and tgt_auth and src_auth != tgt_auth:
        in_deg[src_auth]  += 1
        out_deg[tgt_auth] += 1

print(f"Autores con actividad: {len(set(in_deg)|set(out_deg)):,}")

# ranking
candidates = []
for aid in set(in_deg)|set(out_deg):
    inp = in_deg.get(aid,0)
    out = out_deg.get(aid,0)
    if inp < 10: continue
    ratio = inp / (out + 0.5)
    stance = author_stance.get(aid, '?')
    s = {0:'T0',1:'T1'}.get(stance,'--')
    candidates.append((ratio, inp, out, aid, s))

candidates.sort(reverse=True)

print(f"\n{'Author':>8} {'Stance':>6} {'in':>7} {'out':>7} {'ratio':>8}  {'type'}")
print("-" * 55)
for ratio, inp, out, aid, s in candidates[:30]:
    tipo = 'SOSTENEDORpuro' if ratio > 10 else ('SOSTENEDOR' if ratio > 3 else '')
    print(f"{aid:>8} {s:>6} {inp:>7,} {out:>7,} {ratio:>8.1f}  {tipo}")

# estadísticas del network
all_in  = list(in_deg.values())
all_out = list(out_deg.values())
print(f"\nNetwork stats:")
print(f"  in_deg  max={max(all_in):,} mean={sum(all_in)/len(all_in):.1f}")
print(f"  out_deg max={max(all_out):,} mean={sum(all_out)/len(all_out):.1f}")
