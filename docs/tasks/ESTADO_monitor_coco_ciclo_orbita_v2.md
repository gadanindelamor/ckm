# ESTADO_monitor_coco_ciclo_orbita_v2

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*
*Rama única: `main` (§6, 8 oct).*

---

## Última escritura

**2026-10-08 01:59 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP1 — medir lo que hoy se rompe, sin tocar `services/`.** Cerrado el 2026-10-08.
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

## Qué espera, y de quién

- **P9 — BLOQUEA — [delamor]:** con qué configuración nace COCO y dónde se declara.
  Sigue pendiente, y **ahora bloquea más que antes**: el CP2 no sólo alinea baselines, también
  es donde deja de romperse.

## Próximo paso

**CP2 — una existencia, medida sobre la órbita.** Necesita P9.

## Nada quedó a medias

El driver escribe con `.tmp` + rename, y su log está completo. La suite sigue en 220/220:
el CP1 no tocó `services/`.
