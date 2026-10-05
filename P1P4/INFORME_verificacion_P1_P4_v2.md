# INFORME_verificacion_P1_P4_v2

*4 oct 2026 — Claude Opus 5.5 (Cowork). Reemplaza a la v1.*
*Autorización (delamor, por escrito en el chat): pruebas que se ajusten a la ciencia, sin su participación; "Doy como válido lo que sus informes determinen".*
*Dónde corrió: contenedor de Cowork. No es el Codespace ni la PC de delamor. Repo leído: GitHub `gadanindelamor/ckm` @ `2097ca4`. No se modificó nada del repo.*

---

## 0. Qué código se usó

**El código de los drivers lo escribí desde cero.** No usa `experiments/ckm_p1p4_module.py` ni `process/initial_static_model/hopfield.py`, los dos que tienen los defectos encontrados hoy.

Del repo se importa una sola cosa: `services/corpus_service.py` (`CorpusService`), y solo para construir `W_nuevo` a partir del texto de los informes.

| archivo | qué hace |
|---|---|
| `verificacion_p1_p3.py` | Driver principal. Arma las W, aplica los nulos N_perm y N_grado, y corre P1, P2 y P3. |
| `nulo_fuerza.py` | Nulo N_fuerza: conserva la fuerza de cada nodo. Es la corrección de la §2. |
| `p1_nulo_fuerza.py` | P1 contra N_fuerza. |
| `p1_relajado.py` | Primera corrida de P1, con un solo nulo. Queda como traza. |
| `*_log.json` | Salidas, con commit, versiones, plataforma y seed. |

Para reproducir: `python3 verificacion_p1_p3.py <repo> out.json` y `python3 p1_nulo_fuerza.py <repo> out.json`. Hace falta el repo en `2097ca4`, numpy y networkx. Seed 0. Tarda unos 3 + 6 minutos.

## 1. Veredicto

| | Veredicto |
|---|---|
| **P1, histéresis** | **Verificada como propiedad del modelo.** Con relajación, el lazo aparece en las dos W. **Más allá de la fuerza de los nodos:** en W_viejo, sí (p < 0.005). En W_nuevo, apenas (p = 0.045), y eso no sobrevive a la corrección por comparaciones. |
| **P2, cascadas** | **No medible con N = 32.** Hay menos de 10 cascadas de tamaño ≥ 2 por grafo. |
| **P3, asimetría** | **No testeada.** La forma k-core que corrí es reversible por matemática (§4), así que no es un test. La P3 dinámica, con tiempos de relajación, no se corrió. |
| **P4, densidad óptima** | **No medible.** No hay ninguna W_mixta de un corpus con tensión estructural. |

## 2. Corrección declarada: el nulo N_grado no era válido

En la v1 escribí que "el exceso del lazo lo explica el grado (p = 0.22 y 0.28)". **Eso no se sostiene.** En grafos tan densos (densidad 0.76 y 0.78), los intercambios de aristas que conservan el grado casi no encuentran lugar. En W_viejo movieron el **6.5%** de los pesos, y el nulo quedó con correlación **0.98** con la W real. Un nulo casi idéntico a lo que se testea no puede diferenciarse de ello. Era un nulo que no podía dar "no".

**Lo reemplazo por N_fuerza.** Cada paso suma δ a W_ij y a W_kl y lo resta de W_il y de W_kj, con δ elegido para que ningún peso quede negativo. La fuerza (suma de pesos) de cada nodo se conserva **exactamente** (|Δ| ≤ 2e-15). Mezcla de verdad: la correlación media con W es 0.70 en W_viejo y 0.41 en W_nuevo. Queda algo de correlación, que es inherente a fijar las fuerzas, y la declaro.

## 3. P1: histéresis con relajación

**Protocolo.** Se fijan k nodos en +1 según un orden; el resto queda libre y relaja con Hopfield asíncrono, regla GOLES (h = 0 conserva σ). El estado se arrastra de un paso al siguiente. La rama UP va de k = 0 a N y la DOWN de k = N a 0. Para cada k, el conjunto fijado es el mismo en las dos ramas, así que cualquier diferencia entre ellas es dependencia del camino. Estadístico: área A = media de |m_up − m_down|, con m la fracción de nodos en +1. 60 órdenes. Ninguna relajación dejó de converger.

**Las dos W.**
- **W_viejo:** `W_ckm_corpus_v2.json`. Es la W del paper para N = 32, en el marco anterior a las correcciones de septiembre.
- **W_nuevo:** el corpus de informes por párrafo (870 textos), armado con el `CorpusService` actual, top_k = 32, W_pos.

| W | A real | N_perm (p5–p95) · p | N_fuerza (p5–p95) · p |
|---|---:|---|---|
| W_viejo | 0.316 | 0.252–0.266 · **< 0.005** | 0.267–0.293 · **< 0.005** |
| W_nuevo | 0.302–0.307 | 0.284–0.294 · **< 0.005** | 0.281–0.301 · **0.045** |

En W_nuevo, A cambia entre corridas (0.302–0.307) porque el orden de los barridos es aleatorio. Ese rango está declarado.

**Lectura.**
1. **El lazo existe.** La rama DOWN se queda en m = 1, que es remanencia total. Es física de Ising y Hopfield con campo: cualquier W positiva lo produce, porque los nulos dan entre 0.25 y 0.31.
2. **En la W del paper (W_viejo), la estructura del corpus agranda el lazo** por encima de lo que explica la fuerza de cada nodo. Ninguno de los 200 nulos alcanza el valor real.
3. **En la W corregida (W_nuevo), ese efecto es débil.** Da p = 0.045 en una sola comparación, y no sobrevive a Bonferroni.

## 4. P3: por qué la forma k-core no es un test

Se remueve un nodo del k-core y se cuentan las rondas de poda. Después se lo vuelve a agregar con sus aristas y se cuentan las rondas de bootstrap. En los 6 grafos dio rondas iguales y una recuperación de 1.000. **Eso no es un hallazgo.** El k-core de un grafo fijo es único, así que lo que la remoción poda, la re-adición lo recupera en orden inverso. Este test no puede fallar en la otra dirección, y lo retiro como evidencia: P3 queda **no testeada**. La irreversibilidad de Goltsev, Dorogovtsev y Mendes aparece en percolación con remociones al azar, en el límite termodinámico. No aparece al sacar un nodo y devolverlo.

## 5. P2 y P4

- **P2:** θ en los cuantiles 0.3, 0.5 y 0.7 de los pesos positivos. Cascadas de tamaño ≥ 2: 6, 4 y 0 en W_viejo; 2, 5 y 7 en W_nuevo. El ajuste pide al menos 10, y con N = 32 el rango no llega a 1.2 décadas. **No medible.**
- **P4:** no hay ninguna W_mixta de un corpus con tensión estructural en este entorno. Lo que sí quedó verificado (OBS del 4 de octubre): el test de abril, con subconjuntos aleatorios, da Ω* interior si y solo si media(W_mixta) < 0, sin importar dónde estén los pares negativos.

## 6. Comparaciones y límites

- **Comparaciones de P1:** son 4, dos W por dos nulos (N_perm y N_fuerza). Con Bonferroni α = 0.0125. Con 200 nulos el p mínimo es ≈ 0.005, así que W_viejo/N_fuerza **pasa** y W_nuevo/N_fuerza **no**. La familia de la v1 tenía 16 comparaciones e incluía tests que no eran tests, como P3 k-core. Para P1 se declara esta familia de 4.
- **Errores míos corregidos en el camino:** dos.
  - La conclusión de "un solo nulo" de `p1_relajado`.
  - El nulo N_grado, que no mezclaba.
- **No dice:**
  - Que el CKM no sirva: N_eff contra la enumeración exacta, SALAMANCA y D3 siguen en pie.
  - Que P2, P3 o P4 sean falsas.
  - Nada sobre fourforums ni CreateDebate, que no estaban disponibles.
- **Variables no consideradas:** todas las que no están en los logs.
