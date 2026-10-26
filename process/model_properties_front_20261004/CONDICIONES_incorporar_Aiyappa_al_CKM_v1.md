# CONDICIONES_incorporar_Aiyappa_al_CKM_v1

*4 oct 2026 — Claude Opus 5.5 (Cowork), a pedido de delamor. Borrador para estudiar; no es una TASK todavía.*

## La idea (delamor)

Si Aiyappa no se refuta, copiar su modelo al CKM: tocar pocas líneas del código, agregar texto al paper, y que la parte estática siga funcionando.

## Corrección previa

**Aiyappa no es hebbiano.** Su regla es:

> Δb ~ N(α·b_emisor + β·b_y·b_z, σ²)

Mueve cada creencia hacia lo que dice el otro (α) y hacia la coherencia de la tríada (β), con ruido. Si se copia "exactamente", se copia eso. Si se agrega aprendizaje hebbiano (W_ij += ξ_i·ξ_j), es **otro modelo**, y hay que declararlo como tal.

## Condición 1 — Citar

Incorporar su dinámica es legítimo **solo** si el paper lo dice de frente, por ejemplo: *"implementamos la dinámica de Aiyappa, Flammini & Ahn (2024) sobre…"*, con link a su repo `rachithaiyappa/beliefnet` @ `2289c39`.
Sin esa cita, es apropiarse de su trabajo.

## Condición 2 — El aporte es la diferencia

Si queda idéntico a Aiyappa, **no aporta nada**. El aporte posible está en lo que el CKM tiene y ellos no:

| Aiyappa | CKM | Lo nuevo posible |
|---|---|---|
| cambian los pesos (creencias) | cambian los estados σ; W fija | **las dos capas juntas:** W evoluciona por su regla, y σ relaja sobre W |
| energía triádica (Heider): −b_x·b_y·b_z | energía por pares (Hopfield): −½ΣW_ij·σ_i·σ_j | **qué pasa al combinar** las dos energías |
| no mide histéresis | histéresis verificada con relajación (4 oct) | **¿la histéresis sobrevive** con W dinámica? |

## Condición 3 — Lo estático no se toca; lo nuevo se testea aparte

- P1–P7 sobre W estática no cambian (tenés razón).
- La capa dinámica es **nueva**: necesita sus propios tests, que **puedan fallar**, con nulos y pre-registro, como los del 4 oct.
- En el paper va en una sección propia, marcada como extensión, no mezclada con las predicciones sobre W estática.

## Si se hace

Escribir una TASK para Code (Codespace) con checkpoints. Primero, replicar su Fig. 5 dentro del CKM, como control de que la copia es fiel. Después, agregar la capa σ y medir.

## Antecedentes del mismo día

- `replica_aiyappa_04oct/INFORME_replica_Aiyappa_fig5_v1.md` — su resultado se sostiene.
- `verificacion_p1_p4_04oct/INFORME_verificacion_P1_P4_v2.md` — estado de P1–P4 del CKM.
