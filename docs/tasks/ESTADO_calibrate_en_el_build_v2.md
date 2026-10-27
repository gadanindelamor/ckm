# ESTADO — TASK_calibrate_en_el_build_v2

*Última escritura: 2026-10-27 07:20 UTC, por Claude Opus 5 (Code, Codespace).*

## La TASK está CERRADA en CPa–CP2

**Cerrada el 27 oct 2026.** CPa, CP0, CP1 y CP2, cada uno con su commit y su reporte en la BANDEJA.
Suite al cerrar: **872 passed, 7 xfailed, 0 failed**.

**CP3 —el vivo— queda FUERA de la TASK**, y sólo se corre **con orden explícita de delamor**.

## CP2 — cerrado el 27 oct

D3 + D4 + D6'. La calibración tiene **su lugar en la Config** —un escritor, el punto único del
canal— con el `w_sha` de la W calibrada, `duration_s` y `blocking`, que hasta hoy se medían y se
descartaban. **COCO deriva su vara de ahí**, como `Threshold` de `ckm_trust_rule`: `MEASURED` si el
registro es de esta W, `DECLARED` con el default de `coco.py` y su causa si no. **Nunca los números
de otra W** — el caso 1, cerrado y con test. Los parámetros de `calibrate` se declaran en el estado,
con `n_runs = 1000`. Y el 17% (reusar `A0` en λ=0), en commit aparte, con la premisa verificada bit
a bit.

Reporte completo en la BANDEJA, 07:10 UTC. Commits: `0d4598c` (CP2), `ec008f7` (el 17%) y `e940c81`
(el cierre).

## Lo que la TASK deja abierto — una línea cada cosa

1. **La tensión del margen de `calibrate`, sostenida.** No se cambia para que separe (delamor, 27
   oct). Con extremos esa W no separa en 10/10 semillas; con máximo interno la cantidad es positiva
   en 10/10. **E3**, y la decisión es no decidir ahora.
2. **E5 — el docstring de la "primera calibración que separa"** (`ckm_monitor.py:84-90`) y el ÍTEM 6
   del 22 oct: son ciertos como hecho, y les falta decir que ese veredicto fue con `n_runs=200,
   seed=0`. Espera a delamor.
3. **La divergencia de `w_version` en el origen:** lo marca `"rebuild"`, igual que un rebuild por
   ingesta. Declarada, con un test que la afirma; se revisa con el renombre general.
4. **El mecanismo general de defaults** (centinela, inventario): caer en `N_RUNS_DEFAULT` /
   `SEED_DEFAULT` de la Config **no queda visible** — verificado en CP2. Es otra TASK.
5. **El `state_dir` por default de `CKMMonitor`** es el directorio declarado traza (F3a). **E1**, de
   delamor.
6. **P14** — tres cosas que los drivers declaran y IAP no (la lista de archivos de estado, el
   puerto, el registro de providers). Sin implementar; espera quién la toma.
7. **El `n_runs` de `calibrate` quedó en campo aparte del de COCO y puede derivar** (lo abrió CP2).
   Mi lectura: un solo campo. **E3**, de delamor. Default vigente: los dos campos.
8. **El test de β puede fallar ~1% de las corridas** por buscar el valor como subcadena sobre el
   estado serializado (coincide con un timestamp). No lo toqué: es otra afirmación.

- **CPa** (`74d97fc`): P12, P15 y P16 registradas en `DECISIONES_opus.md`; los contadores de la
  línea de `rebuild_decisions.jsonl` se capturan al decidir, no después del reset; un test nuevo y
  el caller del test actualizado. **Extensión declarada:** el CPa nombra `n_puntos_d_ckm` y el mismo
  mecanismo afectaba a `ciclos_sin_rebuild` en la misma línea; los dos corregidos.
  `textos_desde_rebuild` sigue sin estar en la línea (es el ÍTEM 5 del 22 oct, otra decisión).
- **CP0**: la evaluación de D1–D6' contra el repo, sin código. Reporte en la BANDEJA, 02:58 UTC.

**Suite: 851 passed, 7 xfailed, 0 failed.** Las 13 de `test_should_rebuild_conectado.py`, en verde.

## CP1 — cerrado el 27 oct

D1 + D2 + D5 implementados: el origen nace por su condición propia
(`CorpusService.build_first_W()`), pasa por el punto único de calibración del canal
(`_calibrar_antes_de_instalar`, que llaman los dos caminos) y deja su línea en
`rebuild_decisions.jsonl` con causa `bootstrap`, escrita aparte.

- **El caso 2 del REG queda cerrado:** el primer ciclo ya no trae `calibration: None` sino un
  registro con su estado y su `w_sha`. Con el corpus de test da `no_calibrado: sin_separacion`, así
  que los umbrales siguen en 0,40 / 0,60 — **pero ahora se ve por qué**.
- **Divergencia declarada, no corregida:** `w_version` marca el origen como `"rebuild"`. Hay un test
  que afirma la divergencia para que una corrección futura no pase sola.
- **Se movieron 5 tests, no 3**, y los dos que mi CP0 no vio afirmaban sobre **claves del panel**
  (`ultimo_rebuild_por_decision`, `punto_calibrate`), no sobre el archivo de decisiones. Los cinco
  reescritos para afirmar lo mismo de otra forma; el del CP5 cambió el contenido de lo que afirma,
  con su docstring.
- Tests nuevos: `tests/test_bootstrap_calibra_y_registra.py`, 6.
- Suite al cerrar: **857 passed, 7 xfailed, 0 failed**. Las 13 de la PoC, en verde.

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

## Respuestas de delamor del 27 oct, en el chat, después del CP0

*Registradas acá porque CP1 las necesita. La anotación formal en `DECISIONES_opus.md` es de Opus
(§8 del protocolo); esto es el ESTADO, que es de Code.*

- **D3 — contestada.** delamor: *"EL LUGAR DONDE NACE ES PERPETUO. es el estado.. en Landscape
  Config"*. Lectura de Code: **el lugar es de la Config, no del `Ciclo`.** El registro se escribe
  cuando se produce y **no espera** al ciclo; el ciclo que nace después lo referencia. Eso resuelve
  la tensión del CP0: la lectura que no funcionaba era la otra —meterlo dentro de `Ciclo`, que es
  `frozen` y nace cuando Monitor abre el ciclo, o sea después—. Para CP2: la Config gana un lugar
  (slot + `to_dict`/`from_dict`), **un escritor** (el servicio de calibración) y muchos lectores; y
  `from_dict` sobre un estado viejo lo lee **UNKNOWN**, no `nulo_calibrado` (ése es *"no miré"*, y
  acá el caso es *"no se sabe si miró"*).
- **D5 — confirmada.** delamor: *"cambia el contenido de lo que afirma, no un número… CONFIRMO"*.
  El test `test_cp5_el_camino_de_la_decision_queda_INERTE_con_suspendido_False` **no se afloja**: se
  reescribe lo que afirma. Forma propuesta por Code, para CP1: afirmar **exactamente una línea, con
  `causa == "bootstrap"`, y que sea la única** — así sigue diciendo "ninguna decisión del régimen" y
  además dice que el origen dejó la suya.
- **D6' — Code recomendó 1000; la decisión es de delamor.** Medición en la BANDEJA, 03:20 UTC
  (**E5**): a `n_runs=200` el veredicto **depende de la semilla** (2 `calibrado` y 8
  `no_calibrado` en 10 seeds, sobre la W exacta que calibró en el vivo); a 1000, `no_calibrado` en
  10 de 10. delamor precisó la unidad del costo: *"el delay por mensaje es el costo de n runs"*; a
  1000 son 0,302 s en el 5% de los mensajes, o sea **30% de un tick** de canal — entra sin tocar el
  ritmo. **1000 no vuelve medible el margen** (el recorrido entre seeds, 0,0847, sigue ~7× por
  encima del margen de 0,0114): es el piso de congruencia, no la precisión.

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
