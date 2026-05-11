# REG_p6_fourforums_guncontrol_v1

*CKM — P6: Delta como ruptura de simetría — fourforums gun control*
*2026-05-08*

## Setup

- Red: 19 autores, 36 pares C1-C5+C7+C8 verificados
- Polo atacante:   Author 555 (top iniciador: 5 pares, out/in ratio 1.1x)
- Polo sostenedor: Author 965 (C3 en 32/36 pares, in/out ratio 455x)
- Comunidad atacante:  [555, 53, 751, 115]
- Comunidad sostenedora: [965, 3452]
- Pares negativos (|asim| > 0.50): 14 pares
- N_runs: 1000 | MAX_ITER: 9500

## Resultados P6

| Condición    | atk_dom | sos_dom | mixed  |
|-------------|---------|---------|--------|
| W_base       |   0.0%  |   0.0%  | 100.0% |
| W + Delta    |  38.5%  |  41.5%  |  20.0% |
| Efecto Delta | +38.5pp | +41.5pp | -80.0pp|

Colapso de mixtos: **80.0 pp**

## Comparación con CreateDebate

| Métrica              | CreateDebate | fourforums |
|---------------------|-------------|------------|
| Mixtos sin Delta     | 54.0%       | 100.0%     |
| Mixtos con Delta     | 0.0%        | 20.0%      |
| Colapso              | 54.0 pp     | **80.0 pp**|
| Polo dominante       | sos_dom 55.8%| sos_dom 41.5%|
| Balance atk/sos      | 44.2/55.8   | 38.5/41.5  |

→ **Escenario A+**: colapso más pronunciado con Delta densa.
Delta es propiedad del dominio gun control, no del corpus chico.
El sostenedor (frame defensivo/constitucional) domina en ambos corpora.

## Estructura de atractores (W_delta, 300 runs)

Atractores únicos: 8
Fracción activa media: 50% N — convergencia con CKM N=32 (54%N)

Top 5 atractores:

| Runs | %N activo | 555 | 965 | Comunidad activa |
|------|-----------|-----|-----|-----------------|
| 73   | 41%       | -   | +   | [37,53,679,682,965,1443,3452] — defensiva |
| 64   | 59%       | +   | -   | [115,150,381,501,555,680,751,809,1034,3351] — atacante |
| 56   | 12%       | -   | +   | [965,3452] — núcleo mínimo defensivo |
| 56   | 88%       | +   | -   | [todos excepto 965+3452] — saturación atacante |
| 14   | 29%       | -   | -   | [751,809,1034,3351,3452] — estado mixto residual |

Los 2 atractores principales son **complementos perfectos**:
- Cuando 555 activo → 965 inactivo (comunidad atacante domina)
- Cuando 965 activo → 555 inactivo (comunidad defensiva domina)
Sin superposición. Separación estructural verificada.

## Nota metodológica

W_base produce 100% mixed — sin Delta no hay ruptura de simetría.
Delta actúa como campo externo que fuerza la resolución.
Mismo mecanismo verificado en CreateDebate: Delta colapsa ambigüedad.
