TAREA 4 — ckmdatasets: correr v8k (delamor, 23 oct). Un checkpoint al final.

fourforums_pipeline_v8k.py = v8j + dos cambios declarados en su docstring:
K1 autocitas fuera de A y de los conteos (diagonal en 0); K2 nulo de los triángulos con signo por mezcla de votos (1000 corridas, seed 20261023). Sin corte de n.

PASOS
1. git pull --rebase. Anotá el commit de partida (tiene que incluir el commit de v8k).
2. NO modifiques el .py. Si falla o ves un bug, reportalo con la línea y el error, y pará.
3. python fourforums_pipeline_v8k.py
4. No corras nada más.

DEVOLVER
- En el chat: el bloque final de out/run_v8k.log (desde la primera "====" hasta el final), y el tiempo de la corrida.
- En el repo: REG_sesion_ckmdatasets_<fecha>_v8k.md con commit de partida, SHA1 del dump, tiempo, los números del summary (incluido el bloque K2 entero), qué cambia respecto de v8j (E, signos, triángulos: deberían cambiar solo por las 5 autocitas), y "lo que estos números no dicen". Sin interpretar.
- Commit solo del REG. Nada de out/. Push sin --force, nunca --all ni --mirror.

A1.PAUSA al terminar: delamor decide lo siguiente.
