# REG_borrador_serie2_caso0_intento5 — serie2_caso0, intento 5

**BORRADOR.** Lo escribe Code (Claude Opus 5) en el Codespace el 29 oct 2026, por el texto para Code
21 (`docs/opus/TEXTO_PARA_CODE_21_REPO_CKM_caso0_intento5_vivo_200_seed0_29oct2026.md`), punto 3.
Está **fuera de `registers/`**: pasa a Clase R sólo con el OK de delamor.

Estructura tomada de `registers/REG_iap_serie2_caso0_intento4_v1.md`. **No interpreta**: lo que no se
midió no está.

| | |
|---|---|
| corrida | `experiments/serie2_caso0_20261029T231324Z_log.json`, copiado a `experiments/serie2_caso0_intento5_log.json` |
| `repo_commit` del log | `180844e789ce7bde762e5b542b67e78074a5d30b` |
| modo | `ZERO_SHOT`, corpus de partida 0, sin seed, sin agentes, sin coordinador |
| duración real | **1204,67 s** (`DURATION = 1200`) |
| estado | `experiments/_state_S2-C0/` (no se commitea) |
| datos de este REG | `experiments/registro_intento5_resultado.json`, de `experiments/registro_intento5.py` |
| orden | delamor, 29 oct, en el chat: *"lee y ejecuta ... Es el vivo"* |

## 1. Para qué corrió, y qué cambió respecto del intento 4

Para qué, declarado por el texto 21 (el `objetivo_declarado_como_sesgo` lo escribe el caso y no se
tocó): **que exista evidencia medible del vivo con el muestreo por default de hoy — `n_runs = 200`,
`seed = 0`, distribución uniforme —, el mismo para Monitor, COCO y la W de `calibrate`.** El intento 4
calibró a 1000. Sin predecir el resultado.

| | intento 4 | intento 5 |
|---|---|---|
| `n_runs` de los tres (Monitor, COCO, `calibrate`) | **1000**, declarado en el estado | **200**, el default único de la Config (texto 13 p1, delamor) |
| ¿algún caso declara valor propio? | no | **no** — `declared_by = None` y `propios = []` en los tres |
| el registro de la calibración trae la W viva | no existía | **sí** (`w_sha_live_at_calibration`, texto 13 p2) |
| el caso construye los providers | mapa `_PROVIDERS` local (2 de 4) | **`build_provider` del registro de IAP** (texto 16 p1; verificado equivalente: misma clase y mismo modelo) |
| lo demás | — | **igual**: `DURATION` 1200, `POLL_INTERVAL` 5,0, la consigna, las ventanas, los cuatro modelos y sus techos (bloque `DEVICES` byte a byte idéntico) |

## 2. Los números

| | intento 3 | intento 4 | **intento 5** |
|---|---|---|---|
| duración real | 1204,61 s | 1204,04 s | **1204,67 s** |
| mensajes en el canal | 60 | 98 | **44** (4 son joins SYSTEM, que no entran al corpus) |
| corpus (textos) | — | 94 | **40** |
| evaluaciones de Monitor | 27 | 65 | **11** |
| generaciones de COCO | 4 | 7 | **1** |
| decisiones de rebuild registradas | 27 | 31 | **26** |
| de ésas, que movieron W | 3 | 7 | **2** (`bootstrap` en 30 textos, `volumen` en 40) |
| llamadas a LLM | 250 | 288 | **221** |
| errores `429` | 0 | 0 | **0** |
| errores fatales | 0 | 1 (device B) | **0** |
| calibraciones registradas | 3 | 7 | **1** |
| evaluaciones sin registro de calibración | 4 | 0 | **0** |
| `triggers` de COCO | 0 | 0 | **0** |
| `D_ckm` al cerrar | — | — | **0,0** |
| `Σ Δ_r` de toda la corrida | — | 3880,0 | **0,0** |

Preflight: **los cuatro responden** (latencias 0,334 · 0,488 · 0,285 · 0,072 s). Ticks del canal: 610;
`t` del último tick: `1793316852,49` (el reloj del canal es del canal, no por device).

### Por device

| device | modelo | vueltas | llamadas | errores | 429 | ilegibles | decisiones | mensajes publicados | última decisión (UTC) |
|---|---|---|---|---|---|---|---|---|---|
| device_a | groq `openai/gpt-oss-120b` | 225 | 70 | 0 | 0 | 0 | INTERACT 16 · OP_SILENCE 38 · SKIP 171 | 16 | 23:34:07 |
| device_b | gemini `gemini-3.5-flash-lite` | 229 | 64 | 0 | 0 | 0 | INTERACT 4 · OP_SILENCE 56 · SKIP 169 | 4 | 23:34:04 |
| device_c | groq `openai/gpt-oss-20b` | 229 | 72 | 0 | 0 | 0 | INTERACT 15 · OP_SILENCE 42 · SKIP 172 | 15 | 23:34:04 |
| device_d | groq `qwen/qwen3.8-27b` | **10** | 15 | 0 | 0 | 0 | INTERACT 5 · OP_SILENCE 4 · **LEAVE 1** | 5 | **23:15:17** |

**Ningún device se cayó.** `errores_llm = 0`, `errores = []`, `write_failures = 0` en los cuatro, y en
el stdout del vivo **0 ocurrencias** de `McpError` y de `Traceback` — a diferencia del intento 4, donde
device B murió al cerrar el cliente. **device_d salió por su propia decisión**: `LEAVE` en la vuelta
10, tick 90, `criterio_motivo: "auditoria"`, `action_result: "left"`, `run_end` a los 69 s. No es una
caída: es la decisión que el caso le deja tomar.

## 3. La calibración: estado, condiciones y costo

**Una sola**, la del **origen**, disparada por el ciclo `bootstrap`:

| | valor |
|---|---|
| estado | **`no_calibrado`** |
| causa | **`sin_separacion`** |
| `n_runs` / `seed` | **200 / 0** |
| `declared_by` / `propios` | **`None` / `[]`** — ningún valor propio |
| `sampling_mode` registrado en las condiciones | `None` (la Config lo tiene en `uniform`; en este registro la clave no viaja) |
| grilla λ | `[0,0 · 0,25 · 0,5 · 0,75 · 1,0]` |
| `w_sha` de la candidata | `66ea8d05a4c6…` |
| `w_sha_live_at_calibration` | **`None`** — es el origen, donde no había ninguna W viva (`ckm_monitor.py:785`) |
| `duration_s` | **0,0675** (el intento 4, a 1000: 0,26–0,31) |
| `blocking` | **True** |
| `N` y paridad | **20, par** |
| `N_eff0` muestreado (λ=0) | **1,983930** |
| `N_eff` del colapso muestreado (λ=1) | **2,436944** |
| **margen muestreado** | **−0,300206** |
| `valores` | `{}` |

La curva, como la registró `calibrate`:

| λ | `n_eff` | `d_ckm` | `frac_rec` |
|---|---|---|---|
| 0,00 | 1,983930 | 0,0 | 1,000000 |
| 0,25 | 2,018775 | −0,025414 | 1,017563 |
| 0,50 | 2,213859 | −0,160065 | 1,115896 |
| 0,75 | 2,436944 | −0,300206 | 1,228342 |
| 1,00 | 2,436944 | −0,300206 | 1,228342 |

`d_max = 0,0` en λ=0, `curva_monotona = False`, `colapso_es_el_maximo = False`.

### El margen exacto, por enumeración (N ≤ 21)

Con el script del texto 20 punto 1 (`experiments/margen_exacto_14W.py`), que es el que el texto 21
manda reusar. **Las dos W del vivo se reconstruyen desde los prefijos del corpus y se verifican contra
su sha** (`simpson_en_las_curvas.w_por_sha`): 0 no recomputables. La enumeración del paso del código
está verificada contra `relax_orbit` real, 500/500 en las dos.

| W | textos | ¿calibrada? | `N_eff0` muestreado 200/0 | **`N_eff0` exacto** | `F(20)` | **m exacto** | ¿separa exacto? | α | órbitas | autoconj. |
|---|---|---|---|---|---|---|---|---|---|---|
| `66ea8d05` | 30 | **sí** (el origen) | 1,983930 | **2,056066** | 2,612244 | **−0,332154** | **no** | 0,004864 | 178 | 94 |
| `6c16bb08` | 40 | **no** | 6,067961 | **6,608718** | 2,612244 | **+0,491519** | **sí** | 0,198664 | 21 | 1 |

Con aritmética exacta en lugar del paso de float64 (la divergencia que midió el texto 20 punto 1):
`66ea8d05` da 2,045826 (m = −0,341446) y `6c16bb08` da 6,954992 (m = +0,504909). **Ningún signo
cambia.**

**Lo medido, sin interpretar:**

1. **El veredicto de la única calibración coincide entre lo muestreado y lo exacto:** `sin_separacion`
   con margen muestreado −0,300206 y margen exacto −0,332154. A 200 corridas, acá, el muestreo no
   invirtió el signo. (En las 14 W del texto 20 punto 1 sí lo había invertido en una: `bdb98f5b`,
   +0,011 muestreado contra −0,065 exacto.)
2. **`N_eff0` muestreado da 1,983930, por debajo de 2; el exacto da 2,056066, por encima.** Es el mismo
   patrón que el punto 2c del texto 20 midió en 3 de las 14 W: donde el exacto roza 2 por arriba, el
   estimador a 200 cruza para abajo. α = 0,004864 ≤ 2/3, así que el teorema del punto 2 da
   `N_eff ≥ 2` para esta W, y el exacto lo cumple.
3. **La W con la que cierra el vivo (`6c16bb08`) nunca se calibró ni se evaluó.** El segundo rebuild
   (`volumen`, 40 textos) ocurrió a las **23:31:13**, que es el instante de la **última** evaluación de
   Monitor (la 11.ª, `last_evaluation_utc 23:31:13,45`), y no hubo ninguna evaluación después: la
   corrida siguió hasta las 23:34 con los devices y cerró. Esa W **sí separa** con el margen exacto
   (+0,491519). No se calibró porque no hubo evaluación que la juzgara.

## 4. La vara de COCO, en cada evaluación

Las **11** evaluaciones, idénticas entre sí:

| | valor |
|---|---|
| `D_CKM_THRESHOLD` / `FRAC_REC_MIN` | **0,4 / 0,6** |
| `source` | **`default`** (las 11) |
| `calibrated` | **False** (las 11) |
| `provenance` de los dos | **`DECLARED`** (las 11) |
| `source` del origen | `"default de coco.py — no_calibrado:sin_separacion"` |
| `causa` | `no_calibrado:sin_separacion` |
| `w_sha_del_registro` | `66ea8d05a4c6…` |
| ¿es el sha de la W que COCO juzgó? | **sí** — `w_version_id` de COCO es el mismo en las 11, y `w_matches` (COCO contra Monitor) es **True** en las 11 |
| `w_sha_match` del registro | **`false`** en las 11 |
| `triggers` | **0** |

**La colisión de `w_sha_match`, que ya está decidida.** El campo dice `false` mientras el
`w_sha_del_registro` **es** el de la W juzgada. No es un hallazgo nuevo: está escrito en
`iap_chatroom/ckm_monitor.py:787` — *"No se toca `w_sha_match` (`monitor_service.py:610`): delamor
marcó como sesgo de control el arreglo que se proponía, y la colisión —dos situaciones distintas con
el mismo valor— queda registrada como está"*. Se registra como está, y acá queda la medición: en este
vivo el valor `false` corresponde a la situación en que **sí** coincide.

## 5. La torsión

De `monitor_trajectory.jsonl`, por evaluación de Monitor. **Las siete claves están las siete en las 11
evaluaciones** (`claves_ausentes: ninguna`).

| | valor |
|---|---|
| evaluaciones | **11** |
| de período 2 | **0** (`periodo_orbita = 1` en las 11) |
| con `n_torsion > 0` | **0** |
| con `Delta_r_torsion_sum > 0` | **0** |
| Σ `n_aceptados` | **745** |
| Σ `n_expulsados` | **0** |
| Σ `n_torsion` | **0** |
| Σ `Delta_r_sum` | **0,0** |
| Σ `Delta_r_torsion_sum` | **0,0** |

**La contrafáctica no va**, por el punto 4b del texto 20: no hay torsión > 0 en ninguna evaluación.
Y una medición que es de este intento y no de los anteriores: **`Σ Δ_r = 0`** — los 745 pares
declarados quedaron **aceptados** y ninguno expulsado, así que `W_eff = W` en toda la corrida (los
intentos 2, 3 y 4 acumularon Δ_r 3136, 768 y 3880). `D_ckm` quedó en 0,0 en las 11 evaluaciones.

## 6. El bootstrap del origen

La línea de `rebuild_decisions.jsonl` (26 líneas; `causa` sólo `bootstrap` y `volumen`; las que no
ocurrieron tienen `motivo_no_rebuild: "corpus_en_acumulacion"`):

```json
{"series": "S2", "case": "S2-C0", "t": 24, "ts": 1793315914.651885, "tick": 294,
 "reloj": "channel", "causa": "bootstrap", "ocurrio": true, "motivo_no_rebuild": null,
 "w_sha_antes": null, "w_sha_despues": "66ea8d05a4c6…", "w_cambio": true,
 "corpus_size": 30, "message_count": 33, "ciclos_sin_rebuild": 33, "n_puntos_d_ckm": 0}
```

La segunda que ocurrió: `causa "volumen"`, `t = 25`, `ts 1793316673,42`, tick 1053, 40 textos,
`w_sha_despues 6c16bb08…`, `w_cambio true`. `rebuild_state.json` cierra con `w_sha 6c16bb08…`.

## 7. Cuántas veces se cayó en un default, y dónde

| dónde | cuántas | qué valor |
|---|---|---|
| la vara de COCO (`coco.py`) | **11 de 11** evaluaciones | `0,4 / 0,6`, `provenance DECLARED`, `source "default de coco.py — no_calibrado:sin_separacion"` |
| la calibración | **1 de 1** quedó `no_calibrado` | `valores = {}`: no entregó ningún número |

Se cuenta el **lugar** que usó un valor no medido, no la coincidencia de un número con otro. **Los
defaults de muestreo no se cuentan acá**: `n_runs = 200` y `seed = 0` son el default único de la
Config y eso es lo que este intento viene a registrar, con `declared_by = None` y `propios = []` —
nadie declaró un valor propio, y así se ve en la traza.

## 8. Lo que este REG no dice

- No dice por qué este intento produjo 44 mensajes contra 98 del intento 4, ni por qué `Σ Δ_r = 0`.
  Se midió; no se interpreta.
- No dice si el margen exacto o el muestreado es "el" margen: eso es la pregunta **P19** de la
  BANDEJA (29 oct), abierta y marcada **E3**.
- No compara contra el CP0 (`4d219ae`), que midió que con 200 el veredicto de la única calibración que
  separó depende de la seed (2 de 10 `calibrado`; a 1000, 0 de 10): acá la única calibración corrió con
  **una** seed, la 0, que es el default. La dependencia de la seed en esta W no se midió.
