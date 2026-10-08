# ESTADO_monitor_coco_ciclo_orbita_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 16:00 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP2b — una existencia.** Cerrado el 2026-10-08. Ver §"El CP2, partido".

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
- **CP2c — el vacío y el panel.** Zona `UNKNOWN` y `frac_rec` None sin baseline; `n_torsion` y
  `pares_torsion` en el panel. **Siguiente.**

## Qué espera, y de quién

- **Nada. P1–P9 están respondidas** y ningún default quedó vigente sin decisión. P9 la contestó
  delamor (`n_runs = 1000`) y Opus resolvió el resto por debajo del umbral. La próxima pregunta
  es **P10**.

## Próximo paso

**CP2c — el vacío y el panel.** Zona `UNKNOWN` y `frac_rec` None cuando no hay baseline, en vez
de `"stable"` y `1.0`; y las tres clases de la órbita en el panel (`n_torsion`,
`pares_torsion`), sin cambiar todavía qué entra a `Δ_r_pares`.

## Nada quedó a medias

El CP2b se cerró entero: `coco_config`, el renacimiento atado al ciclo, 13 tests nuevos y la
suite en **256/256**, en un solo commit. `pares_por_orbita` sigue **sin que nadie la llame**:
conectarla al panel es el CP2c y decidir qué entra a Δ_r es el CP3, que es de delamor. Es
deliberado, no un cabo suelto.
