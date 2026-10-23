TAREA 5 — ckmdatasets: correr v8l (delamor, 23 oct). Un checkpoint al final.

fourforums_pipeline_v8l.py = v8k + L1 (docstring), L2 (conteos de resueltos sin autocitas) y L3 (segundo nulo: mezcla los signos de las aristas no dirigidas, conserva cuántas son -, 0 y +). K2 queda igual, para comparar los dos nulos.

PASOS
1. git pull --rebase. Anotá el commit de partida (tiene que incluir el commit de v8l).
2. NO modifiques el .py. Si falla o ves un bug, reportalo con la línea y el error, y pará.
3. python fourforums_pipeline_v8l.py
4. No corras nada más.

DEVOLVER
- En el chat: del bloque final de out/run_v8l.log, solo estas líneas: votes_resolved, disagree_agree_values_resolved, J2_unsure_votes_resolved, self_pair_votes, self_pair_unsure, K2_null_vote_shuffle y L3_null_edge_sign_shuffle. Y el tiempo.
- En el repo: REG_sesion_ckmdatasets_<fecha>_v8l.md con esas líneas, qué cambia respecto de v8k y "lo que estos números no dicen". Sin interpretar.
- Commit solo del REG. Nada de out/. Push sin --force, nunca --all ni --mirror.

A1.PAUSA al terminar.
