# Texto para Code — 21 — repo ckm — el vivo: serie2_caso0, intento 5, con los defaults (200, seed 0, uniforme) — 29 oct 2026 (Opus 5.5)

*Si delamor te pega este texto, eso es su orden explícita para el vivo. delamor, 29 oct: "un texto separado adicional para Code que ejecute un intento más para el caso 0, de manera que exista evidencia medible en vivo, para n_runs 200 seed=0 y traza de ello"; "autónomas… sin intervención de delamor ni de Opus". Es independiente del texto 20.*

```
Code: orden de delamor. El vivo de serie2_caso0, intento 5. Por favor.

Cómo, por favor:
- En el Codespace, el git pull --rebase y el push los hacés vos.
- Este texto es UNA unidad: (1) chequeo previo, (2) el vivo, (3) el
  registro, de corrido, sin esperar a delamor ni a Opus. Sólo hay A1.PAUSA
  antes del vivo si algo del chequeo falla, y al final.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring
  propio y grep de los nombres tocados en el resto del repo. En este texto
  no se espera modificar código.
- Leé primero docs/opus/decisiones_en_el_acto.md, 29 oct (noche).

Para qué corre, declarado (va al REG; el campo objetivo_declarado_como_sesgo
del log lo escribe el caso, test_caso_serie2_caso0.py:630, y no se toca):
que exista evidencia medible del vivo con
el muestreo por default de hoy: n_runs = 200, seed = 0, distribución
uniforme, el mismo para Monitor, COCO y la W_calibrate (texto 13; el
intento 4 calibró a 1000). Ningún driver declara un valor propio en este
intento: es el default, y así debe verse en la traza. Sin predecir el
resultado: separe o no separe, se registra. Para saber, no para
interpretar: con 200, el CP0 (4d219ae) midió que el veredicto de la
única calibración que separó depende de la seed (2 de 10 "calibrado"; a
1000, 0 de 10). No se ajusta ningún número para que algo pase.

(1) Chequeo previo. Si algo falla: A1.PAUSA, reportalo y no corras el vivo.
- La suite completa en serie, en verde, en HEAD. Anotá cuántos tests se
  recolectan. Atención (P18, todavía sin aplicar: es del texto 17): 3 tests
  parametrizados usan la W del último vivo si el archivo está, y el
  --reset se la lleva. Anotá cuál W usan antes, y repetí la recolección
  después del --reset y después del vivo. Sólo se registra.
- Las diferencias con el intento 4: git log y git diff entre 481d744 (el
  repo_commit del intento 4) y HEAD, sobre iap_chatroom/, services/ y
  iap_chatroom/tests/test_caso_serie2_caso0.py. Listalas. La que se espera:
  el n_runs de calibrate pasa de 1000 a 200 (texto 13). DURATION 1200, la
  consigna, las ventanas, los cuatro modelos y sus techos tienen que ser
  los del intento 4; si otra cosa cambió, declarala. Si cambió algo del
  caso que no sea muestreo, A1.PAUSA.
- El muestreo declarado, leído del estado, no de un default de función:
  sampling_for(c) para los tres casos ("monitor", "coco", "calibrate")
  debe dar n_runs = 200, seed = 0, declared_by = None y propios = []. El
  sampling_mode de la Config debe ser "uniform". Si algo de esto no da,
  A1.PAUSA.
- Qué hay hoy en experiments/_state_S2-C0/ (el residuo del --check, P17):
  listalo antes de correr. El --reset lo moverá a process/.
- Que no haya server en el 7860.

(2) El vivo:
- Corré ./iap_chatroom/correr_caso0.sh, sin --check: el script ya hace
  el --reset, el arranque del server, el corpus en 0 por MCP y el
  --preflight. Correr el --check antes gastaría 4 llamadas más (Gemini:
  20 por día y por modelo).
- Dura unos 20 minutos más el cierre. Lanzalo en background, con la salida
  a un archivo, y esperá el final sin intervenir. Durante el vivo no hay
  tareas ni intervenciones.
- Si el preflight falla con 429 en device B: si el retryDelay que informa
  es de 3600 s o menos, esperá ese tiempo una sola vez y volvé a correr el
  script una sola vez. Si vuelve a fallar, o el error es otro: A1.PAUSA. No
  cambies el modelo de B: eso cambia el caso.
- Al terminar, copiá el log del driver a
  experiments/serie2_caso0_intento5_log.json, con el mismo nombre que los
  anteriores. El original con timestamp queda.

(3) El registro:
- REG borrador en docs/REG_borrador_serie2_caso0_intento5.md, con la
  estructura de registers/REG_iap_serie2_caso0_intento4_v1.md y una tabla
  intento 3 / intento 4 / intento 5. Pasa a registers/ sólo con el OK de
  delamor.
- Por favor, que el REG muestre, sin interpretar:
  - para cada calibración (el origen y cada rebuild): estado, causa,
    n_runs, seed, sampling_mode, declared_by, w_sha de la candidata,
    w_sha_live_at_calibration, duration_s, blocking, N y su paridad,
    N_eff0 y margen muestreados;
  - para cada W calibrada, N ≤ 21: N_eff0 exacto por enumeración bajo la
    medida del código, F(N) exacto y el margen exacto. Si el script del
    texto 20, punto 1, ya está en experiments/, usalo; si no, escribí uno
    con la misma enumeración que experiments/piso_del_colapso.py;
  - para cada evaluación de COCO: el Threshold que usó (MEASURED o
    DECLARED, source, w_sha) y si ese w_sha es el de la W que juzgó;
  - la torsión, decidida por Opus el 29 oct: por evaluación de Monitor,
    de monitor_trajectory.jsonl, periodo_orbita, cola_orbita,
    n_aceptados, n_expulsados, n_torsion, Delta_r_sum,
    Delta_r_torsion_sum, N y su paridad. Un resumen: cuántas de período 2,
    cuántas con torsión > 0. Si el archivo no trae esas claves, decilo.
    La contrafáctica (W_eff con Δ_r_torsion) va sólo si hay torsión > 0,
    con el sesgo declarado del texto 20, punto 4b;
  - la línea bootstrap del origen en rebuild_decisions.jsonl;
  - cuántas veces se cayó en un default, y dónde;
  - por device: vueltas, errores y el t del último tick. Si un device se
    cae como B en el intento 4 (McpError al cerrar el cliente), con línea
    de código y de log, como en el texto 15, punto 2. Sin arreglar nada.
- Commiteá el log del driver (los dos nombres). experiments/_state_S2-C0/
  no se commitea, como siempre.

NO: cambiar el margen, la grilla, el patrón, el estimador, ningún default
ni qué entra a Δ_r; declarar un valor de muestreo propio; los docstrings
E5 (ckm_monitor.py:84-90); P14; el state_dir (E1, texto 19); lo de los
textos 17 y 20.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos, pull --rebase y push. A1.PAUSA.
```
