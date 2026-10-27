# ESTADO — TASK_calibrate_en_el_build_v2

*Última escritura: 2026-10-27 03:00 UTC, por Claude Opus 5 (Code, Codespace).*

## Último CP cerrado

**CPa y CP0**, los dos del 27 oct, en un commit cada uno. Ninguno necesitaba OK (lo dice la TASK).

- **CPa** (`74d97fc`): P12, P15 y P16 registradas en `DECISIONES_opus.md`; los contadores de la
  línea de `rebuild_decisions.jsonl` se capturan al decidir, no después del reset; un test nuevo y
  el caller del test actualizado. **Extensión declarada:** el CPa nombra `n_puntos_d_ckm` y el mismo
  mecanismo afectaba a `ciclos_sin_rebuild` en la misma línea; los dos corregidos.
  `textos_desde_rebuild` sigue sin estar en la línea (es el ÍTEM 5 del 22 oct, otra decisión).
- **CP0**: la evaluación de D1–D6' contra el repo, sin código. Reporte en la BANDEJA, 02:58 UTC.

**Suite: 851 passed, 7 xfailed, 0 failed.** Las 13 de `test_should_rebuild_conectado.py`, en verde.

## Qué espera, y de quién

**CP1 espera el OK de Opus** (la TASK: *"CP1 en adelante, no sin OK"*). Antes de ese OK, el CP0
dejó **tres cosas que el diseño no dice** y que CP1 necesita resueltas:

1. **D2 — quién corre los pasos 2 y 3** (calibrar y registrar). El canal duplica el hook en dos
   lugares; `CorpusService._rebuild` lo unifica pero correría `calibrate` en **cada ingesta** del
   régimen default (`rebuild_suspendido=False`, que un test exige mantener), a 0,16 s medidos por
   corrida.
2. **D5 — si el origen cambia de `causal_event`.** Hoy deja `"rebuild"`. Si pasa por
   `rebuild_por_decision("bootstrap")` pasa a `rebuild_por_decision:bootstrap` y mueve 4
   aserciones más, todas de `CorpusService` directo.
3. **D5 mueve tres tests** que cuentan decisiones, y en uno de ellos
   (`test_cp5_el_camino_de_la_decision_queda_INERTE_con_suspendido_False`) **cambia el contenido de
   lo que afirma**, no un número. Eso no lo aflojo yo.

**De delamor** (los que el CP0 marca como suyos o que la TASK sube):
- **D6', el valor de `n_runs` de `calibrate`**: 200 cuesta 0,16 s a N=20 (medido); 1000 cuesta 5×
  (demostrado, no corrido). La dependencia con N no está medida.
- **D3**: si el registro de la calibración va dentro del `Ciclo` —y entonces `abrir_ciclo` lo
  recibe— o al lado, en la Config. El registro nace **antes** que su ciclo.
- Lo de siempre que esta TASK arrastra: el margen de `calibrate` (extremos o máximo interno, E3) y
  los defaults de `LandscapeConfig`.

## Lo que el CP0 contestó, para no volver a abrirlo

- **D1 no rompe nada** y quita la causa de las 30 de `a7d065f`: el bootstrap **no** es un criterio
  de la jerarquía, así que no depende de ningún contador.
- **D4 [abierto]: no choca.** Un test ya exige exactamente lo que D4 pide
  (`test_serie2_caso0_cp1.py:620-644`, escrito condicional), y el vocabulario de "umbral declarado
  con su origen" **ya existe** en `services/ckm_trust_rule.py:255-368` (`Threshold` con `source`,
  `provenance` y `calibrated` derivado), módulo puro y ya en producción en `local_criterion.py`.
- **El costo de `calibrate` se mide y no se persiste**: `duration_s` vive sólo en `get_state()`,
  que no se registra. El dato se produjo en los dos vivos y se descartó.

## Si esta línea sigue acá en la próxima sesión

Nada quedó a medias: `main` verde, sin cambios sin commitear de esta TASK, y lo último fue el
reporte del CP0. `git status` y la BANDEJA dicen el resto.
