# Lectura del pipeline fourforums v8g — 15 oct 2026
*Opus 5.5, a pedido de delamor ("abrí el pipeline"). Sólo lectura en la PC: `ckmdatasets` en `ac6211f` (con `REG_stance_fourforums_v1.md` modificado sin commitear). Leído: `fourforums_pipeline_v8g.py` (líneas 1–75, 231–668, 840–890), cabecera de `ckm_p1p4_module.py`, cabecera de `find_965_v3.py`, `REG_p6_fourforums_guncontrol_v1.md`. **No leído:** el resto de esos archivos, `trace/DOC_ckm_scripts_v1.md`, los otros REG, el dump. No se ejecutó nada.*

## De dónde sale el signo (delamor: "sale de las anotaciones del IAC, eso")
1. **La postura sí es anotación humana.** `build_W_delta` lee `mturk_author_stance` (votos de Mechanical Turk): `topic_stance_votes_1` vs `_2` → autor en T0 (pro control) o T1 (anti); empate → no se mapea. Post → autor → polo, con clave compuesta `(discussion_id, post_id)`.
2. **La interacción sale de la tabla `quote`**: un post cita a otro. Sólo cuenta si los dos polos son distintos (`if t_src == t_tgt: continue` — *"misma postura, no aporta tensión"*). `W_raw` cuenta citas cruzadas (positivas); `delta` la dirección de la réplica.
3. **El peso negativo lo pone la construcción, no se observa.** `support = np.zeros_like(dispute)` (*"sin labels agree/disagree"*), entonces `tension = d/(d+s) = 1` siempre que haya alguna cita cruzada; con `tension > 0.80` el par entra en `neg_pairs` y en `W_mixta` recibe `NEG_WEIGHT = −0.10`. En esta versión **el par T0–T1 queda negativo por definición**.
4. Resumen: la **oposición entre polos** viene de humanos (stance MTurk); **que ese par sea negativo** lo decide el código. No hay marcadores de texto en este productor.

## El parser, por registro (delamor: *"levanta por registro, por la explosión de memoria RAM en mi PC; también está todo eso relatado"*)
- Lee el `.sql` línea a línea; `mturk_2010_qr_entry` y `post` se procesan en streaming, fila por fila (el docstring de v8g: evita ~10 GB de RAM).
- `SKIP_TABLES` deja afuera, entre otras, **`text`** (el contenido de los posts) y la mayoría de las tablas `mturk_2010_*`. **En este productor el texto de los posts no se lee**: W sale de quién cita a quién y de la postura del autor. Por eso aquí no puede haber marcadores.
- Lo que se salta es parte de la declaración: define qué información puede llegar a W.

## Lo que hay que mirar (para el CP0 de Code)
- **N = 2.** Los nodos de W en v8g son los dos polos (T0, T1); `run_lda` ya no hace LDA (devuelve 2 polos fijos). P6 y P1–P4 corren sobre una W de 2×2 (4 estados). `REG_p6`: sin Δ 100 % mixed, con Δ 0 % mixed. **No verificado** si los P6 del paper vienen de esta corrida.
- **El docstring dice que `build_W_delta` usa `stream_W_delta`; el código no la llama.** `stream_W_delta` (etiquetas agree/disagree de `mturk_2010_qr_entry`) existe sin uso. Si se usara, tiene el mismo problema de subcadena que los marcadores (`'no'`, `'for'` dentro de otras palabras).
- **`CD_BASELINE` está escrito a mano en el código** (9 pares de CreateDebate con `tension`, `convergence`, …). La comparación C6c "vs CreateDebate" compara contra esas constantes, no contra una corrida. Hay que declarar de dónde salieron.
- `elicit_pairs_c1_c5`: uno de los cinco criterios es `True` fijo; la primera línea de `asym` se sobreescribe.
- En `run_p6`, `Wd[i,j] += 0.05·delta[i,j]` hace W **no simétrica** durante la relajación.
- **Type-965** (P7) es un **autor** (`TOP_AUTHORS = [965, …]`); su W sale de otro script (`find_965_v3.py`, autores activos de gun control) — **otro productor**, no leído.
- `ckm_p1p4_module.run_all(W_base, W_mixta, …)`: P1–P4 con su propia `cS` y `relax` (asíncrona, `h > 0`), distinta de `landscape_engine` del repo `ckm`. **No verificado** el desempate en h = 0.

## Para M4
El signo de este productor **no tiene el problema de M4** (no hay marcadores), pero tiene otro: es **impuesto** sobre el par de polos. El nulo que corresponde no es barajar marcadores, sino preguntar qué pasa con la estructura si la postura de los autores se asigna al azar (mismas cantidades por polo), y con una W de autores, no de 2 polos.
