# ESTADO — texto 20 (el margen exacto, la simetría σ ↔ −σ, el CP-E y la torsión)

*Lo escribe Code (Opus 5) en el Codespace. Última escritura: 2026-10-29 23:08 UTC.*

Fuente: `docs/opus/TEXTO_PARA_CODE_20_REPO_CKM_margen_exacto_simetria_cpe_torsion_29oct2026.md`
(reemplaza entero al texto 18). Reportes, uno por punto, en `docs/tasks/BANDEJA_code.md`.

## Cerrado

| punto | qué | commit | script y salida |
|---|---|---|---|
| 1 | el margen exacto de las 14 W (R1) | `489b85c` | `experiments/margen_exacto_14W.py` · `..._resultado.json` |
| 2 | N_eff ≥ 2 por la simetría σ ↔ −σ (R3) | `d2a9a3e` | `experiments/simetria_neff_dos.py` · `..._resultado.json` |
| 3 | el "15.52 → 5.27" del CP-E (R2) | `9345d25` | `experiments/cpe_0e042ac_vs_head.py` · `..._resultado.json` · las dos salidas `.txt` |
| 4 | la torsión | `225aabe` | `experiments/torsion_lo_que_queda_afuera.py` · `..._resultado.json` |

Suite completa, en serie, al abrir y al cerrar: **903 passed, 7 xfailed, 0 failed** las dos veces.
`services/` y `iap_chatroom/` sin tocar. El worktree de `0e042ac` creado y borrado.

## Espera

1. **delamor:** las tres preguntas que quedaron abiertas en la BANDEJA, en orden de irreversibilidad:
   - **P19 (NO BLOQUEA, E3)** — qué es "el margen exacto" cuando el empate `h = 0` casi nunca ocurre
     en float64. Default vigente: reporto las dos dinámicas, con el paso del código como columna
     principal. Los 14 signos coinciden con las dos, por eso no bloquea.
   - **la frase de §4.3.2 del paper (E3)** — ninguno de sus cuatro números se reproduce con el
     extractor de hoy. No propongo qué hacer.
   - **lo del punto 2 que es del modelo (E3)** — la condición exacta `α ≤ 2/3` y la cota
     `N_eff ≥ 1/(α² + (1−α)²/2)`: las registra Opus, no Code.
2. **Opus:** leer los cuatro reportes y registrar las definiciones (el margen exacto, la condición de
   la simetría, qué dice §4.3.2).
3. **El texto 21** (el vivo, intento 5) es independiente de éste y **no se corrió**: un vivo no se
   corre sin orden explícita de delamor, y antes hace falta el idle timeout del Codespace ≥ 60 min.

## Hueco declarado

Ningún test de `tests/` se mueve con esto, y la regla de completitud de `readme/CONVENTIONS.md` pide
declararlo: los cuatro puntos agregan **drivers de medición** en `experiments/` y no cambian el
comportamiento de ningún servicio (el texto 20 lo prohíbe expresamente), así que no hay nada del
instrumento que un test nuevo debiera observar. Los drivers vecinos del mismo tipo
(`piso_del_colapso.py`, `simpson_en_las_curvas.py`, `driver_cpe_rango_neff.py`) tampoco tienen test en
`tests/`. Lo que sostiene cada afirmación son los controles internos de cada script, declarados en su
docstring y en el reporte: la enumeración contra `relax_orbit` (500/500 por W), la forma cerrada de
`F(N)` contra la enumeración del colapso, la distribución exacta contra la simulada con N impar, el
muestreo real del instrumento con N = 20 y 21, y el paso de float64 contra el exacto con W entera.
