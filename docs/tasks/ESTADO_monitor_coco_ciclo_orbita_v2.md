# ESTADO_monitor_coco_ciclo_orbita_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 16:49 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP3i — implementación de las cuatro decisiones del CP3.** Cerrado el 2026-10-08.
Reporte: `BANDEJA_code.md`, `REPORTE CP3i`. Suite **276/276**.

Antes: **CP2c**, y con él el CP2 completo. Ver §"El CP2, partido".

Antes: **CP1 — medir lo que hoy se rompe, sin tocar `services/`.** Cerrado el 2026-10-08.
Driver: `experiments/cp1_paridad_y_dos_existencias.py` (pre-registro commiteado antes de
correr, `d3230c1`). Log: `experiments/cp1_paridad_log.json`.
Reporte: `BANDEJA_code.md`, `REPORTE CP1`.
(CP0 cerrado en `27c6559`.)

## Los dos resultados

**A. La paridad pesa, en los dos corpus.** caso09_run2: **16 de 24 textos** relajan a período
2, `‖Δ_r^A − Δ_r^B‖₁ = 24.0`, `max|Δc(S)| = 2.35e−02`. WARMUP: 3 de 20, L1 = 12.0.
Las tres condiciones U1, U2 y U3 se cumplen. **Mi expectativa declarada antes de correr era que
habría pocos o ningún texto con período 2: estaba equivocada.**

**B. Las dos existencias divergen hasta romper.** No hay incrementos negativos que contar: en la
primera evaluación posterior al rebuild salta
`ValueError: operands could not be broadcast together with shapes (31,31) (28,28)`
en `coco.py:254`. COCO quedó con N=28 y Monitor creció a 31. Capturado como dato, no esquivado.

## Lo que corrige de la TASK

**La invariante de compatibilidad de §1 no vale a lo largo de un recorrido.** Dice que en un
punto fijo R_A = R_B. Medido: el texto `i=22` tiene **período 1** y aun así
`|R_A △ R_B| = 1`. La divergencia se compone porque Δ_r entra a W_eff. **Vale a igual W_eff**,
no a lo largo de una serie — así que en el CP2 se testea sobre una evaluación, no sobre un
recorrido.

**Y el corte de las dos existencias tiene dos caras, no una.** Con N fija da los 56 incrementos
negativos registrados; **con N variable levanta una excepción**. La segunda no estaba medida.

## El CP2, partido

Por §4, después del corte por límite de uso de hoy:

- **CP2a — la órbita. CERRADO.** `pares_por_orbita` y `fases_de_orbita` en el engine, `n_runs`
  y `seed` al `declarado` de la Config. 19 tests nuevos, suite 243/243. No toca Monitor ni COCO.
- **CP2b — una existencia. CERRADO.** Monitor recibe `coco_config` en vez de instancia; COCO
  renace cuando cambia el ciclo. **El `ValueError` del CP1 dejó de romper**, verificado al
  revés: sin renacimiento fallan 4 de 13. 13 tests nuevos, suite 256/256.
- **CP2c — el vacío y el panel. CERRADO.** Zona `UNKNOWN` y `frac_rec` None sin baseline, en
  vez de `"stable"` y `1.0`; los defaults de `ThermostatState` ya no afirman un campo estable;
  las tres clases de la órbita en el panel. 10 tests nuevos, suite 267/267, y verificado al
  revés: devolviendo "stable" al vacío fallan 4.

**El CP2 completo: 47 tests nuevos, un test existente cambiado y declarado, 267/267.**

## Qué espera, y de quién

- **Nada. P1–P9 están respondidas** y ningún default quedó vigente sin decisión. P9 la contestó
  delamor (`n_runs = 1000`) y Opus resolvió el resto por debajo del umbral. La próxima pregunta
  es **P10**.

## El CP3

**Las cuatro decisiones son de delamor y están tomadas** (1a, 2b, 3, 4; `DECISIONES_opus.md`).
**Implementadas en el CP3i**, con las cinco inversiones corridas: cada una rompe el test que le
corresponde, y la salida literal de las diez corridas está en el reporte.

Dos tests míos **no podían fallar** y aparecieron invirtiendo, no leyendo: el de la torsión en
W_eff (dos veces: la segunda miraba sólo la última llamada a `_combine_W_Delta`, y `evaluate` la
llama varias veces) y el de Δ_r desde la órbita (pasaba porque en el corpus chico la órbita es de
período 1 y `expulsados == rejected`).

**Trazado, no tapado:** en el corpus de los tests la decisión 1(a) no se ejerce. En el corpus
real sí — el CP1 midió **16 de 24 textos con período 2** en caso09_run2.

## Próximo paso

**CP4 — CorpusService suelta a COCO.** Sacar `self._coco` de `_rebuild`, deprecar la property
`coco` y declararlo en el CHANGELOG; `ckm_monitor.py` pasa a leer desde Monitor; correr los tests
que no son Armstrong.

Es también donde **lo del CP3i empieza a ejercerse en el canal**: hoy `ckm_monitor.py` no pasa
`coco_config`, así que en el canal COCO sigue siendo el de Corpus y nada de esto corre ahí.

## Nada quedó a medias

El CP3i se cerró entero: las cuatro decisiones, 6 tests nuevos, un existente cambiado y
declarado, las cinco inversiones corridas y restauradas, y la suite en **276/276**.
`grep -c INVERSION services/monitor_service.py` → 0: no quedó ningún experimento adentro.
