TAREA 6 — ckmdatasets: producir las W declaradas (delamor, 23 oct). Un checkpoint al final.

build_W_v8m.py lee out/pairs_v8l.csv y out/summary_v8l.json (no lee el dump) y escribe en out/W/ varias W, cada una con su extracción declarada adentro: W_obs, W_sign, W_presence y W_null_s1..s5. Los nodos van anonimizados (a000…); el mapa a ids de autor queda aparte, en nodes_map_v8m.json.

PASOS
1. git pull --rebase. Anotá el commit de partida (tiene que incluir build_W_v8m.py).
2. Si out/pairs_v8l.csv no existe, corré antes python fourforums_pipeline_v8l.py.
3. NO modifiques el .py. Si falla o ves un bug, reportalo con la línea y el error, y pará.
4. python build_W_v8m.py
5. No corras nada más.

DEVOLVER
- En el chat: out/W/run_v8m.log entero y out/W/manifest_v8m.json entero.
- En el repo: REG_sesion_ckmdatasets_<fecha>_W_v8m.md con el log, el manifest y "lo que estas W no dicen". Sin interpretar.
- Commit solo del REG. out/ no se versiona (ni las W). Push sin --force, nunca --all ni --mirror.

A1.PAUSA al terminar. Las W después se miden en el repo ckm; cómo llegan allá lo decide delamor.
