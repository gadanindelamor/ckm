"""
explore_tables.py
Lista TODAS las tablas del dump con sus columnas y primeros valores.
Busca cualquier tabla que tenga post_id + author_id.
"""
import re

SQL = 'fourforums_no_parse_2016_05_18.sql'
create_re = re.compile(r'CREATE TABLE `?(\w+)`?', re.I)
col_re    = re.compile(r'^\s*`(\w+)`', re.I)
insert_re = re.compile(r'INSERT INTO `?(\w+)`?\s+(?:VALUES|values)\s*(.+)', re.DOTALL)

col_names = {}
current = None; in_c = False
first_row = {}

def tokenize_first(s, n=8):
    """Extrae los primeros n tokens del primer grupo VALUES."""
    depth=0; start=None
    for i,c in enumerate(s):
        if c=='(':
            if depth==0: start=i+1
            depth+=1
        elif c==')':
            depth-=1
            if depth==0 and start is not None:
                group = s[start:i]
                break
    else: return []
    tokens=[]; i=0
    while i<len(group) and len(tokens)<n:
        c=group[i]
        if c in (' ','\t'): i+=1; continue
        if c==',': i+=1; continue
        if c=="'":
            j=i+1; buf=[]
            while j<len(group):
                if group[j]=='\\' and j+1<len(group): buf.append(group[j+1]); j+=2
                elif group[j]=="'": j+=1; break
                else: buf.append(group[j]); j+=1
            tokens.append("'"+(''.join(buf[:20]))+"'"); i=j
        elif group[i:i+4].upper()=='NULL': tokens.append('NULL'); i+=4
        else:
            j=i
            while j<len(group) and group[j] not in (',',')'): j+=1
            tokens.append(group[i:j].strip()); i=j
    return tokens

with open(SQL, encoding='utf-8', errors='replace') as f:
    for line in f:
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
        tbl=m.group(1).lower()
        if tbl not in first_row:
            first_row[tbl] = tokenize_first(m.group(2))

print("=== TODAS LAS TABLAS ===\n")
all_tables = sorted(set(col_names) | set(first_row))
for tbl in all_tables:
    cols = col_names.get(tbl,[])
    vals = first_row.get(tbl,[])
    sample = dict(zip(cols, vals)) if cols and vals else {}
    has_post = any('post' in c for c in cols)
    has_author = any('author' in c for c in cols)
    flag = ' <-- POST+AUTHOR' if has_post and has_author else (
           ' <-- POST' if has_post else (
           ' <-- AUTHOR' if has_author else ''))
    print(f"{tbl}{flag}")
    print(f"  cols: {cols}")
    if sample: print(f"  sample: {sample}")
    print()

print("\n=== TABLAS CON POST_ID + AUTHOR_ID ===")
for tbl in all_tables:
    cols = col_names.get(tbl,[])
    if any('post' in c for c in cols) and any('author' in c for c in cols):
        print(f"  {tbl}: {cols}")
