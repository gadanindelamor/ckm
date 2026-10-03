# TASK_salamanca_neel_coercividad_v1

*Clase T — Oct 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Antecedentes: DEFS_CKM_estado_actual_v12 §14–§16 y línea 118; REG_mapeo_magnetico_ckm_v1 §3.1–3.3; REG_unidad_texto_saturacion_v1 §3–§5; PROPUESTA_capa_analisis_services_v1 (Parte 5, pasos 1–4).*
*Reemplaza el diseño de TASK_neel_separabilidad_v1, que queda como registro de lo que se descartó y por qué.*

---

## 1. Qué entendí

**El nombre es la definición.** *(delamor: Basilio Salamanca, almacenero de Cipolletti, Río Negro. En la puerta, a la derecha, un cartel escrito a mano: "Lo que natura non da, SALAMANCA non presta". Y: "no se fía".)*

- **No presta** — la estructura que no está en el corpus no se le pide prestada a ningún procedimiento.
- **No se fía** — tampoco se le da crédito por adelantado. El ruteo por marcadores fía: asume la tensión y después la cobra en pares negativos.

**No es oposición** *(delamor)*. DEFS línea 118 ya lo dice: *"Coercitividad de frontera ≠ oposición binaria. Es gradiente por par de clusters. Alta coercitividad = la frontera resiste el cruce. **Nada es opuesto** — hay fronteras con distintos valores de resistencia."*

**Oposición supone exactamente dos** *(delamor: no hay oposición entre 33 clusters, ni entre más o menos de dos T)*. Por eso no se busca oposición: es una precondición que el dato cumple o no.

**k lo dice el dato** *(delamor: T0 y T1 tienen que existir primero)*. Un corte espectral por signo del Fiedler devuelve dos siempre. Encontrar dos no es hallazgo: es la forma de la pregunta.

**Se lee por la cola** *(delamor: no soy adepto a los promedios, ni a las distribuciones normales inexistentes; habito las colas)*. En un W denso y saturado el centro no informa: todo correlaciona por construcción. Lo que informa son los pocos pares que no.

## 2. Estado del repo — verificado leyendo, sin ejecutar

**Existe y está en `services/`:**
- `cluster_frontier_density.py` — coercitividad por par de clusters, `min(intra_a, intra_b) / inter`, con los bordes resueltos: `inf` si no hay aristas inter-cluster, `"oposicion"` si `inter < 0`, cluster de un nodo anotado como poroso. **Ya separa el régimen de oposición de la coercitividad**, desde antes de esta conversación.

**Existe, en la capa que no está en uso:**
- `cluster_nodes()` en `process/initial_static_model/analytics.py`. Agrupa nodos por **co-movimiento en el espacio de atractores** (copresencia + Ward + `fcluster`), no por los pesos de W. Toma `n_clusters` fijo, default 4. `analytics.py` hoy no importa (ImportError por import relativo; PROPUESTA Parte 2). scipy 1.17.1 disponible.

**No existe en ningún archivo del repo:**
- SALAMANCA como criterio: la partición más el ensemble nulo que decide si la frontera existe.
- Néel: el barrido de β.
- Lo medido el 20 de septiembre y el 3 de octubre sobre estos dos criterios corrió en scripts sueltos **que no se guardaron**. Está sólo en los REG y en la conversación.

**Lo que hay en `experiments/driver_neel_salamanca.py`** es el diseño **descartado**: k = 2 forzado, partición por signo del Fiedler, separabilidad leída por la media. Se reescribe, no se extiende.

## 3. Lo que ya se midió y no hay que volver a medir

| | |
|---|---|
| Máximo sobre particiones | Con spins **independientes**, S de la mejor partición da 0.030 (200 muestras), 0.014 (1000), 0.005 (5000). Nunca cero: es un máximo, positivo aunque no haya nada. |
| λ₁ del laplaciano normalizado contra 20 barajados | caso09 0.425 / nulo 0.741 · caso13 0.759 / 0.870 · caso14 0.850 / 0.970 · informes pág300 0.898 / 0.980 · informes versión 0.947 / 0.990. **p = 0.00 en los cinco: todos tienen estructura. Ninguno sostiene k = 2.** |
| Coercitividad por par, k = 3, contra 10 barajados | caso09 máx **4.59** contra nulo p90 1.63, y las 3 fronteras sobre el nulo. caso13 máx 1.11 contra 1.23: **debajo** del nulo. informes versión máx 1.09 contra 1.04: pegado. |
| Cola de Néel en caso09 (k=2, partición vieja) | De los 20 pares menos correlacionados, persisten en 3 semillas: 1, 0 y 0 según β, contra 0.03 por azar. **La cola era ruido.** |
| Artefacto a evitar | Con k = 5 y k = 6 la coercitividad llega a 16–18 por clusters chicos donde `inter → 0`, y el nulo también. **La lectura vale donde el nulo es estable.** |

## 4. Lo que hace Code

**Orden: 0 → 1 → 2 → 3.** Cada paso es un checkpoint.

### Paso 0 — traer la partición
Seguir los pasos 1–2 de PROPUESTA_capa_analisis_services_v1: `analytics.py` → `services/` con imports planos, y `core.py` si `analytics` lo necesita. Criterio del proyecto: **impacto cero por default, replicación exacta** de lo que ya corría.

No reescribir `cluster_nodes`. Se usa como está, con una sola cosa agregada afuera: cómo se elige `n_clusters` (paso 1).

### Paso 1 — SALAMANCA: ¿existe la frontera?
1. W_pos del corpus (`force_w_pos=True`, `rebuild_suspendido=True`, estado aislado).
2. Atractores → `cluster_nodes(attractors, nodes, n_clusters=k)` para un **rango** de k (2…8). No se fija k de antemano.
3. Para cada k, `cluster_frontier_density` → coercitividad de **cada par** de clusters.
4. **Ensemble nulo prestado**: el mismo corpus barajado palabra por palabra (conserva frecuencias y largos de texto, destruye la co-ocurrencia), W reconstruida con los servicios reales, mismo pipeline. N barajados.
5. Una frontera **existe** si su coercitividad cae fuera de la distribución nula de su mismo k. Si ninguna, en ningún k: **no pasa nada**, y W_pos es la respuesta.

**Salida: la matriz completa de coercitividad por par y por k, con su nulo.** Continua. La categoría se deriva al leer, como el `registro_borde`.

### Paso 2 — Néel: ¿qué profundidad tiene?
Solo sobre las fronteras que el paso 1 dejó en pie, y con la partición **fija** (reajustarla por β es reajustarla al ruido, §3).

Para cada β de frío a caliente: muestrear estados con `boltzmann_warmup`, `C_ij = ⟨σ_i σ_j⟩`, y registrar **C_ij por par cruzante** *(delamor: qué sucede entre ellos)*. No la media.

- β_Néel **por par**: los pares no sueltan todos juntos. La frontera es un perfil, no una línea.
- Lectura por **cola con persistencia**: los K pares que más resisten, y cuántos siguen ahí con otras semillas. Cola que se rebaraja = ruido.

### Paso 3 — correr sobre los corpus con respuesta conocida
caso09, caso13, caso14, informes versión, informes página 300. Y **fourforums**, que es el único corpus del proyecto elicitado con posiciones opuestas por diseño — el control positivo que faltaba. Está en `process/experiments/`.

## 5. Pre-registro — declarado antes de correr

| corpus | posiciones | paso 1 debe dar |
|---|---|---|
| **fourforums** gun control | dos, por diseño, con etiquetas de stance | **fronteras que resisten** |
| caso09 IAP | coordinación | ya dio 4.59 sobre nulo 1.63 con k=3 — hay que ver si sobrevive con la partición por co-movimiento |
| caso13, caso14 IAP | coordinación | nada, o debajo del nulo |
| informes CKM | **autor único** | nada |

Si fourforums no da fronteras, el que no ve es el instrumento.

**Precondición de REG_unidad_texto §3:** un W saturado no tiene ceros, y sin ceros no hay frontera que separar. caso09 está al 62% de pares distintos; informes versión al 100%. Si los saturados dan nada, hay que distinguir *no hay estructura* de *no hay resolución*. Se declara, no se resuelve acá.

## 6. Decisiones

**Tomadas:**
1. k sale del dato, barriendo un rango. No se fija.
2. Coercitividad por par de clusters, cualquier k. No oposición binaria.
3. Néel se lee por par y por cola con persistencia, no por la media.
4. SALAMANCA necesita nulo prestado y eso queda declarado: es un nivel, y un nivel necesita contra qué compararse.
5. `cluster_nodes` se usa como está.

**Abiertas, son del modelo:**
6. **Cómo se elige `n_clusters`.** Barrer 2…8 y leer la matriz es lo que propongo, pero si hay que elegir uno solo, falta el criterio.
7. **El nulo**: barajar el corpus (más fiel, probado) o barajar los pesos de W conservando el grado (más barato). Esta TASK usa el primero; el segundo queda abierto.
8. **Qué hacer con los pares que el paso 2 identifique.** Esta TASK los **lista**. No los incorpora a W. Construir W_mixta desde ahí es otra decisión.
9. **Babel a resolver antes de que entren juntas a un criterio** (PROPUESTA paso 4): hay **dos coercividades** — la de P1 (el ρ donde c(S) cruza cero, campo coercitivo, DEFS §14) y la de frontera de cluster. Comparten nombre y no son lo mismo.

## 7. Corrección a los DEFS, a aplicar si el paso 1 lo confirma

**§16 dice** *"detecta si W_pos tiene estructura adversarial"*. Lo que detecta es **modularidad**. Una palabra, dos objetos. Es la razón de que el criterio admita de más: SALAMANCA sola habría admitido W_mixta en un canal de coordinación. La admisión requiere los dos pasos.

*(delamor: modularidad no es adversarialidad.)*

## 8. Lo que Code NO hace

- No construye W_mixta ni cambia el ruteo por marcadores.
- No reescribe `cluster_nodes` ni `cluster_frontier_density`.
- No conecta nada al canal vivo.
- No interpreta: mide y registra.
- Toda acción fuera de esta TASK es un checkpoint: se detiene, reporta y espera.

## 9. Checkpoints

**Por qué:** la precisión sobre la propia mecanicidad no se intenta desde adentro. Se construye como par.

**Formato:** qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo hasta ahora.

| CP | Después de | Reporta |
|---|---|---|
| **CP0** | leer | Tensiones con el repo. *(Hecho: §2 y §3 de esta TASK.)* |
| **CP1** | paso 0 | Que `analytics` importe desde `services/`; qué replicó exacto y qué no; qué test debería haber cambiado |
| **CP2** | paso 1 sobre **un** corpus | Matriz de coercitividad por par y por k, con el nulo. Dónde el nulo deja de ser estable |
| **CP3** | paso 1 sobre todos | La tabla contra el pre-registro, salga como salga |
| **CP4** | paso 2 sobre la primera frontera que quedó en pie | Curva por par, β_Néel por par, persistencia de la cola |
| **CP5** | todo | REG borrador fuera de `registers/` |

## 10. Criterio de cierre

- Tests: que `analytics` importe y replique; el nulo; la coercitividad contra un caso a mano; el barrido de k.
- REG borrador entregado.
- Según CONVENTIONS: ¿qué test debería haber cambiado con esto? Declarar los huecos.
- Si el paso 1 da vacío en todos los corpus menos fourforums, **eso es el resultado**, y el REG lo dice así.
