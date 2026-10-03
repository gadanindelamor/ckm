# REG_borrador_salamanca_s1_v1

**BORRADOR.** Fuera de `registers/` a propósito (TASK_salamanca_neel_coercividad_v5 §9, CP5). Pasa a `registers/` y a Clase R sólo con el OK de delamor.

*Oct 2026 — gadanin.delamor + Claude Code (Opus 5) + Claude Opus 5.5 (revisión de método)*
*Instrumento: `experiments/driver_neel_salamanca.py --salamanca --nulos 1000`*

---

## El intento que subyace

*(delamor: no olvidemos el intento que subyace.)*

No es encontrar fronteras. Es tener un criterio que **pueda devolver vacío**.

Lo que hay hoy en el canal —el ruteo por marcadores de oposición— no puede: siempre encuentra un "pero" en algún texto suficientemente largo. Un procedimiento sin estado nulo no mide, confirma (REG_unidad_texto §5.2).

> *"Lo que natura non da, SALAMANCA non presta."* Y: *"no se fía."*
> — el cartel escrito a mano en la puerta del almacén de Basilio Salamanca, Cipolletti, Río Negro *(delamor)*.

**No presta:** la estructura que no está no se le pide prestada a ningún procedimiento. **No se fía:** tampoco se le da crédito por adelantado.

---

## 1. Qué se midió

W_pos de cada corpus (`force_w_pos`, `rebuild_suspendido`, top_k 32; 27 en `categorias`). Partición espectral del laplaciano normalizado, k barrido 2…8, declarada antes de correr (v5 §13). Coercitividad por par de clusters con `services/cluster_frontier_density.py`.

**Nulo:** el mismo corpus barajado palabra por palabra —conserva frecuencias y largos, destruye la co-ocurrencia—, W reconstruida con los servicios reales, y **cada W barajada se vuelve a particionar** con el mismo método y el mismo k. 1000 barajados.

**Estadístico:** el nulo es la distribución del **mínimo de porosidad por barajado**; se compara contra el mínimo observado. Umbral **Bonferroni α = 0.05/7 = 0.0071** por los 7 k. `p` se reporta con su resolución: cero coincidencias es `p < 0.001`, no `p = 0`.

---

## 2. Resultado — guarda ≥ 8 pares, 1000 barajados

| corpus | saturación | veredicto | k que pasan | mejor celda |
|---|---:|---|---|---|
| **caso09** | 0.619 | **FRONTERA** | 3, 6 | k=3: coerc 4.59, poros 0.218 vs nulo 0.646, `p < 0.001`, cluster mín **6** nodos, efecto **2.97×** |
| **caso13** | 0.875 | **FRONTERA** | 6, 7 | k=6: coerc 16.00, `p < 0.001`, cluster mín **2** nodos, efecto 10.37× |
| caso14 | 0.992 | **NO MEDIBLE (a)** | — | saturada: sin ceros no hay corte barato |
| informes versión | 1.000 | **NO MEDIBLE (a)** | — | ídem |
| informes página 300 | 0.964 | **FRONTERA** | 6, 7, 8 | k=6: coerc 1.45, efecto 1.29×, cluster mín 3 |
| tramo `categorias` | 0.467 | **NADA** / no medible (e) | — | 7 textos: el nulo es más coercitivo que el observado en 3 de 4 k |

### 2.1 La diferencia no es de p — es de dónde aparece la frontera

**caso09 la tiene con clusters grandes.** k=3, cluster más chico de 6 nodos, efecto 2.97×. El campo se parte en partes que resisten.

**caso13 e informes sólo la tienen con clusters de 1 a 3 nodos.** En particiones gruesas no hay nada: caso13 en k=2 y k=3 da `p = 0.95` y `p = 0.90` — y además entra en el criterio (e), el barajado es *más* coercitivo que el corpus real. Aparecen grupitos chicos que resisten dentro de un campo que no se parte.

Eso no es "más o menos significativo". Son dos cosas distintas.

### 2.2 La saturación ordena

```
caso09      0.619  →  frontera con clusters de 6 nodos
caso13      0.875  →  sólo con clusters de 2
informes    0.964  →  sólo con clusters de 3, efecto 1.29x
caso14      0.992  →  no medible
informes v  1.000  →  no medible
```

Monótono en los cinco. Y la saturación se mide sobre W **antes** de particionar nada, así que no es un supuesto introducido por el método. Le da base a la precondición que REG_unidad_texto §3 había dejado como lectura: un W sin ceros no tiene frontera que mostrar, y entre medio hay gradiente, no corte.

---

## 3. Lo que NO muestra

### Modularidad no es adversarialidad *(delamor)*

**caso09 no prueba tensión.** Lo medido es que su W_pos tiene una partición con fronteras que resisten el cruce más de lo que resistiría por azar. Eso es **modularidad**. Que haya módulos no dice que haya posiciones que se opongan.

Y la evidencia de eso está en el mismo trabajo: la partición de caso09 encontrada esta sesión separa **protocolo e identidad de device** (`claudesonnet_`, `groqllama_`, `joined`, `channel`, `task`) de **contenido** (`ava`, `cartographer`, `bell`, `story`, `memory`). Es un canal de coordinación. No hay dos posiciones.

**Corrección a DEFS §16:** dice *"detecta si W_pos tiene estructura adversarial"*. Lo que detecta es modularidad. Una palabra, dos objetos, y es la razón de que el criterio admita de más: SALAMANCA sola habría admitido W_mixta en un canal de coordinación.

La admisión necesita los dos pasos. Néel —qué profundidad tiene esa frontera— es el segundo, y no está corrido.

### Lo que falta para que haya control positivo

Ninguno de los seis corpus fue elicitado con posiciones opuestas por diseño. El único del proyecto que sí es **fourforums**, y su W del paper es **relacional**: `SKIP_TABLES` incluye `'text'`, los nodos son **autores**. Hace falta una W de términos desde los posts del topic 9, y el dump no está en el filesystem (v5 §11).

**Sin control positivo, "frontera" en estos corpus no se puede contrastar con un corpus donde la respuesta correcta sea conocida.**

---

## 4. Errores de método encontrados y corregidos en el camino

Todos de Code, todos señalados por delamor o por Opus 5.5, ninguno encontrado por Code antes de que lo señalaran:

1. **Partición desde los atractores.** En W_pos el 99.9% de la masa está en dos órbitas —todo en +1 y todo en −1— y ahí todos los nodos se mueven juntos: no hay co-movimiento diferencial. *(delamor: la frustración es lo que el criterio decide, así que no puede ser lo que el criterio usa para decidir.)* La partición sale de W (v3 §12).
2. **k forzado a 2.** Un corte por signo del Fiedler devuelve dos siempre: encontrar dos no era hallazgo, era la forma de la pregunta. *(delamor: oposición supone exactamente dos, y T0/T1 tienen que existir primero.)*
3. **Nulo interno falso.** `S` sobre la mejor partición es un máximo sobre particiones: con spins independientes da 0.030 / 0.014 / 0.005 según muestras. Nunca cero.
4. **Guarda de un solo lado.** Se verificaba `inf` en el nulo y no en el observado.
5. **Estadístico sesgado.** El mínimo observado contra el pool de todas las fronteras del nulo. Al corregirlo, tres corpus perdieron celdas y `categorias` perdió su única frontera.
6. **`p = 0`.** Con n barajados lo afirmable es `p < 1/n`.
7. **Umbral post-hoc.** La guarda de 8 pares se fijó mirando el dato. Declarada, barrida en 4/8/16, y **a este nivel de corrección decide** (v5 §15.5).
8. **"Fronteras reales"** antes de pasar por el nulo. Son candidatas.

---

## 5. Estado

- §1, §2: **verificado**, 1000 barajados, una corrida por celda, seed 0.
- §2.2 (la saturación ordena): **verificado** como medición; su lectura causal es **propuesta**.
- §3: **declarado**. Modularidad no es adversarialidad, y caso09 no prueba tensión.
- Control positivo: **ausente**.
- Néel: **no corrido**.

No cierra. Y lo que más importa de esta corrida es que el criterio **devolvió vacío** donde no había con qué: dos corpus no medibles por saturación, uno no medible por tamaño. Eso es lo que el ruteo por marcadores nunca pudo hacer.
