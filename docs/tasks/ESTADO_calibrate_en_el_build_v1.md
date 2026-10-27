# ESTADO — TASK_calibrate_en_el_build_v1

> **SUPERADA el 27 oct 2026.** `docs/tasks/TASK_calibrate_en_el_build_v2.md` reemplaza a la v1 (sus
> opciones A y B quedaron atrás: delamor decidió *"otra opción"*, que es el diseño D1–D6' de la v2).
> El estado vivo está en `docs/tasks/ESTADO_calibrate_en_el_build_v2.md`. Lo de abajo queda como
> estaba: describe hasta dónde llegó la v1.

*Última escritura: 2026-10-26 23:10 UTC, por Claude Opus 5 (Code, Codespace).*
*Lo pide el §3 del `PROTOCOLO_code_continuidad_v1`: la TASK estaba en curso sin ESTADO.*

## Último CP cerrado

**CP0 y CP0b**, commiteados el 24 oct (ver BANDEJA, entrada del 24 oct 01:10 UTC).

## Qué se hizo después

- **CP1 implementado, probado y REVERTIDO en el código el mismo día.**
  - La versión que quedó registrada es `a7d065f` (*"la causa del nacimiento de W es bootstrap"*),
    commiteada **en rojo** por pedido de delamor: 843 passed, **13 failed**, todas en
    `tests/test_should_rebuild_conectado.py`, **sin tocar** esos tests.
  - El revert es `7040a02`, y es lo que tiene `main`. **La traza quedó intacta**: `a7d065f` sigue
    en la historia y el REG y la BANDEJA dicen qué midió.
  - Hoy (26 oct) la suite está en **850 passed, 7 xfailed, 0 failed**, con las 13 en verde.
- **26 oct: verificación V1–V6 del texto 08, hecha y reportada** (BANDEJA, entrada
  *"REPORTE TEXTO 08"*, 23:05 UTC). Lo que esta TASK necesitaba saber antes de seguir —**cómo nace
  la primera W y por qué no pasa por `calibrate`**— está medido ahí, con `file:line` y con las dos
  corridas vivas. El punto nuevo: no es sólo que `ingest` vaya antes del bloque de la decisión;
  **el cambio de sha resetea los tres contadores en la misma vuelta**, así que ningún criterio
  puede votar en el mensaje en que W nace. Es un candado doble.
- Del texto 08 salieron también dos correcciones de docstring (`f37648d`) y dos hallazgos no
  pedidos, los dos sin tocar: la decisión `estructural` registra `n_puntos_d_ckm: 0`, y el
  nacimiento de la primera W es el único cambio de W sin línea en `rebuild_decisions.jsonl`.

## Qué espera, y de quién

**Espera a delamor.** Su decisión del 26 oct fija el orden y descarta las dos opciones que había
(*"NO ES la opcion B Dejarlo como esta. NO ES. es otra opcion."*):

1. **primero** dejar claro cómo nace la primera W por el camino del rebuild, con qué condiciones,
   y si es un flujo limpio → **esta parte está hecha y reportada** (V1 del texto 08);
2. **después**, ver si las 13 de `test_should_rebuild_conectado.py` son completas, correctas o
   requieren ajustes.

O sea: lo que falta es la lectura de delamor (y de Opus) del V1, y con eso la decisión sobre el
paso 2. **`a7d065f` sigue sin reaplicar y no se reaplica sin esa decisión** (toca la semántica del
modelo y lo que delamor decidió: **E1/E3**).

Dos cosas más, de delamor, que esta TASK arrastra:

- **el margen de `calibrate`**: extremos o máximo interno (**E3**). Del V5 del texto 08: en las 7
  curvas medidas `colapso_es_el_maximo = False`, y el máximo cae en λ=0.25 en 3 de 7;
- **los defaults de `LandscapeConfig`**: el docstring dice que `n_runs` y `seed` son obligatorios y
  el código les da default. El V3 del texto 08 agrega que el docstring afirma además que son
  *"UNO SOLO para Monitor y COCO"* y que *"COCO ya no tiene un default propio"*, y que el código no
  sostiene ninguna de las dos. **No se corrigió nada de eso**: es la misma decisión.

## Si esta línea sigue acá en la próxima sesión

Nada quedó a medias: no hay cambios sin commitear de esta TASK, `main` está verde, y lo último que
se hizo fue verificación. `git status` y la BANDEJA dicen el resto.
