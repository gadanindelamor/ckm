#!/usr/bin/env python3
"""
util_count_sql_rows.py
Cuenta rows por tabla en un dump MySQL sin parsear valores.

Método: str.count('),(') por línea INSERT — operación C, muy rápida.
Funciona con dumps de batch INSERT (múltiples INSERT por tabla = múltiples líneas).

Uso:
    python util_count_sql_rows.py <path_sql> [tabla1 tabla2 ...]

Ejemplos:
    python util_count_sql_rows.py trace/fourforums_no_parse_2016_05_18.sql
    python util_count_sql_rows.py dump.sql post quote mturk_author_stance

Tiempo esperado: ~5 segundos para 544MB / 1270 líneas.
"""

import re, sys
from pathlib import Path
from collections import defaultdict

SQL = Path(sys.argv[1]) if len(sys.argv) > 1 else None
FILTER = set(a.lower() for a in sys.argv[2:]) if len(sys.argv) > 2 else None

if SQL is None:
    print(__doc__)
    sys.exit(1)

RE_INSERT = re.compile(r'INSERT INTO `?(\w+)`?', re.I)
counts = defaultdict(int)

print(f"Leyendo: {SQL}", flush=True)
with open(SQL, encoding='utf-8', errors='replace') as f:
    for i, line in enumerate(f):
        if not line.startswith('INSERT'): continue
        m = RE_INSERT.match(line)
        if not m: continue
        tbl = m.group(1).lower()
        if FILTER and tbl not in FILTER: continue
        counts[tbl] += line.count('),(') + 1

print(f"\n{'Tabla':<50} {'Rows':>12}")
print("-" * 64)
total = 0
for tbl, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"{tbl:<50} {n:>12,}")
    total += n
print("-" * 64)
print(f"{'TOTAL':<50} {total:>12,}")
