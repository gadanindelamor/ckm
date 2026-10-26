# INFORME_verificacion_P1_P4_v1

**BORRADOR — informe de verificación.** *4 oct 2026 — Claude Opus 5.5 (Cowork).*
*Autorización (delamor, escrita en el chat): "Dejo por la presente constancia de mi autorización … que Opus 5.5 y quien él determine realice las pruebas que consideren necesarias y se ajusten a la ciencia. Es requerido que no participe. Doy como válido lo que sus informes determinen. Luego decidiré en base a la verdad, la evidencia que presenten." — Pablo Gadano.*
*Dónde corrió: contenedor de Cowork (no el Codespace, no la PC de delamor). Repo leído: GitHub `gadanindelamor/ckm` @ `2097ca4`. No se modificó nada del repo.*
*Archivos: `verificacion_p1_p3.py` + `verificacion_p1_p3_log.json` (principal) · `p1_relajado.py` + `p1_relajado_log.json` (primera corrida, un solo nulo).*

---

## Veredicto

| | Veredicto | En una línea |
|---|---|---|
| **P1** histéresis | **VERIFICADA como propiedad del modelo** | Con relajación el lazo aparece. Es más grande que el de pesos permutados, pero **no** más grande que el de un nulo que conserva el grado de cada nodo. |
| **P2** cascadas τ | **NO MEDIBLE** con N=32 | Menos de 10 cascadas de tamaño ≥ 2 por grafo. No hay datos para ajustar ni para descartar una ley de potencia. |
| **P3** asimetría | **NO SE OBSERVA** con la definición k-core | Remover y re-adicionar el mismo nodo: mismas rondas, recuperación completa (100%). Matemáticamente esperado: el k-core de un grafo fijo es único. |
| **P4** densidad óptima | **NO MEDIBLE** | Requiere W_mixta de un corpus con tensión estructural; no hay ninguna en este entorno. El test de abril con subconjuntos aleatorios depende sólo de la suma de W (ver OBS del 4 oct). |

Estado de los tests de abril (`experiments/ckm_p1p4_module.py`), por lectura de código: P1 sin relajación; P3 con la rama de adición fija en 0; P4 dependiente sólo de media(W); P2 "CONFIRMADA si algún θ cae en rango" sin test de ajuste. Ninguno ejercita la dinámica del Modelo Híbrido. Eso fue antes de que existieran los REG y la metodología (delamor).

---

## Pre-registro (escrito en el driver antes de correr)

- **Dos W.** `W_viejo` = `process/experiments/W_ckm_corpus_v2.json` (marco previo a las correcciones de septiembre; la W del paper para N=32). `W_nuevo` = informes, unidad párrafo (870 textos), `CorpusService` actual, `top_k=32`, `force_w_pos=True`.
- **Dos nulos, 200 cada uno.** `N_perm`: pesos del triángulo superior permutados (conserva la distribución de pesos). `N_grado`: intercambios dobles de aristas, el peso viaja con la arista (conserva el grado de cada nodo y la distribución de pesos).
- **16 comparaciones**, Bonferroni α = 0.003125. Con 200 nulos la resolución de p es ≈ 0.005: **ningún p de esta corrida puede alcanzar Bonferroni**. Se declara.
- Expectativa declarada (Opus): P1 aparece también en el nulo.

## P1 — histéresis con relajación

Protocolo: k nodos fijados en +1 según un orden; el resto libre, Hopfield asíncrono, regla GOLES (h=0 conserva σ); estado arrastrado. UP k=0→N, DOWN k=N→0. A igual k, mismo conjunto fijado: toda diferencia es dependencia del camino. Área A = media de |m_up − m_down|. 60 órdenes por W, 0 no-convergencias.

| W | A real | N_perm (p5–p95) | p | N_grado (p5–p95) | p |
|---|---:|---|---:|---|---:|
| W_viejo | **0.316** | 0.252–0.266 | < 0.005 | 0.301–0.320 | 0.22 |
| W_nuevo | **0.307** | 0.284–0.294 | < 0.005 | 0.297–0.311 | 0.28 |

**Lectura.**
1. **El lazo existe** — la rama DOWN queda en m=1 (remanencia total): el campo recuerda. Es física de Ising/Hopfield con campo; cualquier W positiva lo produce (los nulos dan 0.25–0.32).
2. El lazo real es mayor que el de pesos permutados, **pero ese exceso lo explica el grado de los nodos**: con el nulo que conserva grado, el real queda dentro (p = 0.22 y 0.28).
3. **No hay evidencia de estructura del corpus más allá del grado.** La primera corrida de hoy (un solo nulo, `p1_relajado_log.json`) decía "la estructura del corpus agranda el lazo"; con el nulo más exigente, **eso no se sostiene**. Corregido acá.

**P1 queda: verificada como propiedad del modelo** (histéresis de un ferromagneto con campo, modulada por la distribución de grados). Coincide con lo que delamor dijo hoy: "características del modelo, matemáticas".

## P2 — cascadas

k-core (k=2) sobre grafos umbral; θ en los cuantiles 0.3/0.5/0.7 de los pesos positivos. Remover cada nodo del core, medir tamaño de la cascada. Cascadas de tamaño ≥ 2 por grafo: W_viejo 6, 4, 0; W_nuevo 2, 5, 7. El ajuste exige ≥ 10. Además, con N=32 el rango posible es < 1.2 décadas.
**NO MEDIBLE.** Lo que el README reporta como τ∈[1.53, 1.98] salió de un protocolo que no testea ley de potencia.

## P3 — asimetría remoción / re-adición

Remover nodo → rondas de poda del k-core. Re-adicionar el mismo nodo con sus aristas → rondas de bootstrap y fracción del core original recuperada.
Resultado, 6 grafos: rondas iguales en remoción y re-adición, **recuperación 1.000** en todos; nulos idénticos.
**Por qué (matemática):** el k-core de un grafo fijo es único; lo que la remoción poda, la re-adición lo recupera en orden inverso. La irreversibilidad de Goltsev–Dorogovtsev–Mendes aparece en percolación (remociones al azar, límite termodinámico), no al sacar y devolver un nodo.
**NO SE OBSERVA** con esta definición. Una P3 dinámica (tiempos de relajación Hopfield) no se corrió.

## P4 — densidad óptima

**NO MEDIBLE** en este entorno: no hay W_mixta de un corpus con tensión estructural. La de fourforums es relacional y su dump no está acá; el corpus de informes es de autor único (SALAMANCA / REG_unidad_texto §5). Verificado aparte (OBS 4 oct): con subconjuntos aleatorios, Ω* interior ⇔ media(W_mixta) < 0, sin importar dónde estén los pares negativos.

---

## Lo que este informe NO dice

- No dice que el CKM no sirva. N_eff contra enumeración exacta, SALAMANCA (criterio que puede devolver vacío) y D3 no se tocaron y siguen en pie.
- No dice que P2–P4 sean falsas. Dice que con N=32 y sin un corpus con tensión **no se pueden medir**, y que P3 en su forma k-core estática es reversible por construcción.
- No sustituye al Codespace: es una verificación independiente, reproducible con los scripts y logs adjuntos (seed 0).
- Variables no consideradas: todas las que no están en los logs.

## Para que otro lo verifique

`python3 verificacion_p1_p3.py <ruta_al_repo> salida.json` — numpy, networkx, el repo en `2097ca4`. ~3 minutos.
