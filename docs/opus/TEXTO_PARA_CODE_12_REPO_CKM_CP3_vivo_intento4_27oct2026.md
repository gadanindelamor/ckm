# Texto para Code — 12 — repo ckm — CP3 de TASK_calibrate_en_el_build_v2: el vivo (serie2_caso0, intento 4) — 27 oct 2026 (Opus 5.5)

*Si delamor te pega este texto, eso es su orden explícita para el CP3 (TASK v2, §4: "CP3 — el vivo: solo con orden explícita de delamor"). delamor, 27 oct: "Puedes dejar todo listo para el vivo? dura 20 minutos y debo estar en el codspace para que no se stopee".*

```
Code: orden de delamor para el CP3 de docs/tasks/TASK_calibrate_en_el_build_v2.md:
el vivo, serie2_caso0, intento 4. delamor está en el Codespace durante la
corrida para que no se detenga. Por favor, en este orden.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en el resto del repo. En este CP no se espera
  modificar código.
- Unidades: (1) chequeo previo; (2) el vivo; (3) el registro. De corrido
  dentro de cada una. Entre (1) y (2) sólo hay A1.PAUSA si algo del chequeo
  falla; si todo da bien, seguí al vivo sin esperar.

Para qué corre, declarado: medir el flujo nuevo (CP1 + CP2: el origen calibra
antes de instalarse, n_runs de calibrate = 1000, la vara de COCO como
Threshold MEASURED/DECLARED, firmada con su W) con todo lo demás igual que el
intento 3. Sin predecir el resultado: separe o no separe, se registra. Lo de
siempre (delamor): no se ajusta ningún número para que algo pase; la tensión
se sostiene.

(1) Chequeo previo — si algo falla, A1.PAUSA y reportá, sin correr:
- CP2 y el cierre de la TASK (texto 11) están commiteados, pusheados y con la
  suite completa en verde (en serie). Si no, el vivo no corre.
- El código del caso es el del intento 3 salvo lo que traen CP1 y CP2:
  iap_chatroom/tests/test_caso_serie2_caso0.py sin cambios desde el intento 3
  (DURATION 1200, consigna, ventanas, los cuatro modelos y sus techos por
  modelo). Si hay otra diferencia, declarala.
- En el panel o el estado del canal, que calibrate quede con n_runs = 1000,
  declarado en su lugar del estado (no como default de función).
- --preflight: los cuatro modelos responden.
- ZERO_SHOT: --reset (mueve experiments/_state_S2-C0/ del intento 3 a
  process/ con timestamp; no borra), reiniciá el server con
  --state-dir /workspaces/ckm/experiments/_state_S2-C0, y verificá por MCP
  corpus_size = 0 y canal en 0. Verificá que lo del intento 3 quedó en
  process/.

(2) El vivo:
- Disparalo con salida experiments/serie2_caso0_intento4_log.json.
- Durante el vivo no hay tareas ni intervenciones (regla vigente).

(3) El registro, al terminar:
- REG borrador en docs/REG_borrador_serie2_caso0_intento4.md, con la misma
  estructura que registers/REG_iap_serie2_caso0_intento3_v1.md y una tabla
  intento 3 contra intento 4. Pasa a registers/ sólo con el OK de delamor.
- Por favor, que el REG muestre sin interpretar: para cada calibración
  (el origen y cada rebuild), estado, causa, n_runs, seed, w_sha de la
  candidata, w_sha_live_at_calibration, duration_s y blocking; para cada
  evaluación de COCO, el Threshold que usó (MEASURED o DECLARED, source,
  w_sha) y si ese w_sha es el de la W que juzgó; la línea bootstrap del
  origen en rebuild_decisions.jsonl; y cuántas veces se cayó en un default
  y dónde.
- Commiteá el log; experiments/_state_S2-C0/ no se commitea (como en el
  intento 3).

NO: cambiar el margen, la grilla, el patrón ni ningún número de default;
los docstrings E5 (ckm_monitor.py:84-90); P14; el state_dir por default (E1).

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos, pull --rebase y push. A1.PAUSA.
```
