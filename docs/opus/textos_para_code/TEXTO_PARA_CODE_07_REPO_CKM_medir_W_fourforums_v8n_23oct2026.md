TAREA 7 — ckm: medir las W de fourforums (delamor, 23 oct). Predicción antes, un checkpoint al final.

Qué son: ocho W producidas en el repo ckmdatasets por build_W_v8n.py, a partir de votos humanos de acuerdo/desacuerdo del IAC (fourforums, gun control). El signo lo pusieron los anotadores, no nosotros. Cada W trae su extracción declarada adentro (clave "declaration", operadores O1–O7). Nodos anonimizados (a000…a145), N = 146.
- W_obs: la observada.
- W_sign: sign(W_obs), sin magnitudes.
- W_presence: conteos de votos, todo positivo (sin signo).
- W_null_s1..s5: W_obs con los signos de sus aristas no nulas permutados (mismos 297 −, 75 +, 11 en 0). Respuesta conocida: sin estructura de quién con quién.
Formato: {"nodes": [...], "W": [[...]], "source": ..., "declaration": {...}}, más manifest_v8n.json con el sha256 de cada archivo.

Dónde están: delamor las sube a mano a process/datasets_private/fourforums_W_v8n/ (8 W + manifest; el mapa de ids NO viene). Agregá esa carpeta al .gitignore ANTES de que lleguen: son un derivado del IAC y no van a git.

PASOS
1. git pull --rebase. .gitignore con process/datasets_private/. Verificá el sha256 de cada W contra el manifest; si alguno no coincide, pará.
2. Escribí la PREDICCIÓN en la BANDEJA antes de correr nada (qué esperás de cada W y por qué).
3. Script nuevo en experiments/ (con docstring), que use SOLO el instrumento existente (services/landscape_engine.py: basin_masses, n_eff, relax_orbit, beta_c_landscape). No toques services/ ni iap_chatroom/.
4. Por cada W: N_eff con n_runs ∈ {1000, 5000, 20000} (convergencia, no se supone), cantidad de órbitas distintas, fracción de período 2, masa de la órbita mayor, beta_c_landscape. Misma seed por n_runs para las ocho W.
5. Nada de vivos. Nada más que esto.

DEVOLVER
- En el chat: una tabla W × medidas y el contraste con tu predicción.
- registers/REG_ckm_W_fourforums_v8n_<fecha>.md: commit de partida, sha256 verificados, la predicción (copiada tal cual), la tabla, la convergencia y "lo que estos números no dicen". Sin interpretar.
- Resultados numéricos en JSON fuera de git (en la misma carpeta privada), con el sha256 de cada W.
- Commit: el script, el .gitignore, el REG y la BANDEJA. Push.

A1.PAUSA al terminar: delamor decide.
