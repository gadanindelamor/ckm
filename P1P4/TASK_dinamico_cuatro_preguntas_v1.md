# TASK_dinamico_cuatro_preguntas_v1

*Clase T — BORRADOR — 5 oct 2026 — Claude Opus 5, Codespace `ckm` @ `f8e0783`.*
*Decidido bajo la autorización de delamor ("hacé lo que te dé seguridad"). Checkpoints en cada paso.*
*Cierra sobre: `BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1.md`.*
*Marco: `docs/CKM_Modelo_Hibrido.md` §"Por qué las propiedades emergentes son inevitables" y §"predicciones falsables".*

---

## 0. Qué cambia respecto de todo lo anterior

Lo anterior medía sobre **una W snapshot no negativa**. Ahí las preguntas no son testeables: una
premisa (`force_w_pos`) decide las respuestas antes de correr, y de las cuatro, tres piden tiempo
que un snapshot no tiene.

Acá **W evoluciona**. El Modelo Híbrido prescribe la dinámica: Hamiltoniano Hopfield + Glauber
para los estados, **regla hebbiana para los pesos al ingresar información**, umbral cooperativo
tipo k-core/Watts. La frustración **no se inyecta**: aparece porque Hebb sobre patrones de ambos
signos produce pesos de ambos signos.

**Nombres nuevos, sin números.** Los cuatro nombres viejos traen la respuesta puesta —hay un REG
que dice CONFIRMADA y un informe con p≈0 sin código— así que no se usan. Las preguntas se llaman
por lo que preguntan:

| nombre | pregunta |
|---|---|
| **Q·CAMINO** | ¿el estado alcanzado depende del orden en que entró la información? |
| **Q·CASCADA** | ¿los re-pesados se propagan con distribución sin escala? |
| **Q·FLECHA** | ¿el tiempo de relajación al retirar difiere del de incorporar? |
| **Q·VENTANA** | ¿hay una densidad/modularidad intermedia que maximiza la propagación? |

**Qué se testea:** si el modelo que el CKM declara como su marco exhibe las propiedades que ese
marco predice. **No** se testea el corpus. Son dos preguntas distintas y esta TASK sólo hace la
primera. Declarado para que nadie lo lea como medición del corpus.

## 1. Las fórmulas, explícitas

**Estados.** σ ∈ {−1,+1}^N. Energía E(σ) = −½ Σ_ij W_ij σ_i σ_j.

**Relajación (determinista, GOLES).** Asíncrona, orden aleatorio por barrido:
  h_i = Σ_j W_ij σ_j ;  σ_i ← +1 si h_i > 0 ; −1 si h_i < 0 ; **σ_i si h_i = 0**.
La regla de empate es premisa del instrumento (paper §4.2 y
`REG_seleccion_nodos_desempate_v1` §2). Converge porque E es Lyapunov con W simétrica.

**Ingesta hebbiana.** Patrón ξ^(p) ∈ {−1,+1}^N. Al ingresar el p-ésimo:
  W_ij ← W_ij + (1/N) ξ_i^(p) ξ_j^(p)  para i ≠ j ;  W_ii = 0.
W queda simétrica y con pesos de ambos signos. Carga α = p/N. Referencia del marco:
α_c ≈ 0.138 (Hopfield clásica, transición de primera orden).

**Retiro.** W_ij ← W_ij − (1/N) ξ_i^(p) ξ_j^(p). Es la inversa **exacta** sobre W. Que la
inversa exista sobre W y no sobre σ es el punto de Q·FLECHA.

**Umbral cooperativo.** Grafo G(θ) con arista (i,j) si W_ij > θ. k-core con k=2 para las
cascadas de poda. θ declarado antes: cuantiles {0.3, 0.5, 0.7} de los pesos positivos.

**Parámetros declarados.** N ∈ {64, 128, 256} (el N del corpus no acota nada acá: esto es el
modelo, no el corpus). p barrido hasta α = 0.30, es decir más allá de α_c. Patrones ξ i.i.d.
Rademacher salvo donde se diga. Seed 0. 50 réplicas por celda. MAX_SWEEPS = 200; toda no
convergencia se cuenta y se reporta.

## 2. Q·CAMINO — ¿el estado depende del orden?

**Mecanismo que se ejercita.** Hebb es una suma de productos externos: **es conmutativa**, así
que la W final NO depende del orden. Si hay dependencia del camino, no puede venir de W: tiene
que venir de que σ se relaja *entre* ingestas y se arrastra.

**Protocolo.** Fijado un conjunto de p patrones y un σ inicial:
- **Rama con historia:** ingestar de a uno en el orden π, relajando σ después de cada ingesta.
  Estado final σ_π.
- Repetir con n_ord = 30 órdenes π distintos.
- **Estadístico:** d = media de la distancia de Hamming normalizada entre pares de σ_π.
  d = 0 significa que el orden no importó.

**Nulo que puede decir no — N·SIN_HISTORIA.** Las mismas p ingestas, misma W final, **sin
relajar en el medio**: se relaja una sola vez al final, desde el mismo σ inicial. Por
conmutatividad de Hebb, la W es idéntica; lo único que cambia es que no hay historia. Si el
orden importa por la historia, d_real > 0 y d_nulo = 0 por construcción. **Si d_real también da
0, Q·CAMINO sale negativa, y es un resultado.**

**Segundo nulo — N·PERM.** W final permutada en su triángulo superior (conserva la distribución
de pesos, destruye la estructura hebbiana), mismo protocolo con historia. Contesta si la
dependencia del camino es de la estructura o de cualquier W con esos pesos.

**Qué sería "sí":** d_real fuera del p95 de N·PERM, con N·SIN_HISTORIA en 0.
**Qué sería "no":** d_real ≈ 0, o d_real dentro del nulo de permutación.
**Expectativa declarada (Opus, antes de correr):** d_real > 0 para α cerca de α_c y ≈ 0 para α
chico. Lo segundo haría que la propiedad exista sólo en un régimen, y el régimen es el resultado.

## 3. Q·CASCADA — ¿distribución sin escala?

**Protocolo.** Para cada ingesta individual sobre un sistema ya cargado: relajar y contar
s = número de nodos que cambiaron de signo. Barrer α. Reunir la distribución de s.

**Ajuste.** Ley de potencia discreta truncada [s_min=2, N] por máxima verosimilitud → τ.
Comparación por razón de verosimilitud normalizada (Vuong) **contra exponencial y contra
lognormal**. Se reporta τ, el estadístico z, su p, y las **décadas disponibles** log10(s_max/2).
**Criterio declarado:** la pregunta sólo se contesta si hay ≥ 100 cascadas con s ≥ 2 y ≥ 1.5
décadas. Con menos, el veredicto es NO MEDIBLE y se dice con los números.
El marco predice τ ∈ [1.5, 2] cerca de criticidad; eso es la predicción, no el criterio de éxito.

**Nulo — N·PERM** sobre la W del momento, mismo conteo.

**Por qué acá sí y antes no:** antes N=32 daba < 10 cascadas y < 1.2 décadas. Con N=256 y barrido
de α el rango existe. El bloqueo era del tamaño, no de la pregunta.

## 4. Q·FLECHA — ¿asimetría temporal?

**Lo que NO es un test** (y por qué): remover un nodo del k-core y volverlo a poner cuenta rondas
de poda y de bootstrap sobre un **grafo fijo**. El k-core de un grafo fijo es único, así que la
re-adición recupera lo mismo en orden inverso: recuperación 1.000 garantizada. Eso ya se midió y
se retiró el 4 oct. **No se repite.**

**Lo que sí se mide: tiempo, no conjunto.** El marco predice que el tiempo de relajación
post-retiro diverge cerca de criticidad mientras el de incorporación queda acotado.

**Protocolo.** Sistema cargado a α. Sobre el estado relajado:
- **Retiro:** W ← W − (1/N)ξξ^T del patrón más reciente; relajar; contar **barridos hasta
  converger**: t_rem.
- **Incorporación:** desde el mismo estado y la misma W, ingestar un patrón nuevo; relajar;
  contar barridos: t_add.
- **Estadístico:** Δt = t_rem − t_add, y su dependencia con α. Se reporta la curva completa.

**Nulo — N·PERM** sobre W antes de la operación.
**Qué sería "no":** Δt ≈ 0 en todo α, o dentro del nulo. Posible y declarado.
**Nota de honestidad:** la inversa sobre **W** es exacta (§1). Si aparece asimetría, es de σ y de
su tiempo, no de W. Eso es lo que la hace una pregunta sobre dinámica.

## 5. Q·VENTANA — ¿densidad intermedia óptima?

**Protocolo.** Patrones con estructura de bloques: C comunidades, probabilidad μ de que un bit
siga el bloque ajeno. μ barre de 0.01 a 0.5. Ingesta hebbiana → W con estructura modular que
**salió de los patrones**, no puesta a mano. Medir profundidad de propagación: fracción de nodos
que cambian de signo tras una ingesta coherente con un bloque.

**Criterio declarado:** óptimo **interior** que supere a los dos extremos de la grilla por más de
2 errores estándar, en al menos un valor de los parámetros de semilla.

**Nulo — N·UBICACION.** Mismos números de pesos, misma media, bloques barajados. Contesta la
pregunta que el snapshot no podía: **¿importa la ubicación estructural, o sólo la suma?**

**Aiyappa, Flammini & Ahn (2024), *Sci. Adv.* 10(15) eadh4439 — se cita, no se replica.** Su
modularidad óptima Ω* es el antecedente de esta pregunta. Su resultado ya está replicado
(`INFORME_replica_Aiyappa_fig5_v1`) y **no se vuelve a tocar**. Acá la pregunta es otra: si el
fenómeno aparece bajo dinámica hebbiana + Glauber, que no es su modelo.

## 6. Comparaciones, declaradas antes

| pregunta | celdas | comparaciones |
|---|---|---|
| Q·CAMINO | 3 N × 6 α × 2 nulos | 36 |
| Q·CASCADA | 3 N × 2 alternativas (exp, lognormal) | 6 |
| Q·FLECHA | 3 N × 6 α × 1 nulo | 18 |
| Q·VENTANA | 1 N × 1 nulo | 1 |
| | | **61** |

Bonferroni α = 0.05/61 = 8.2e-4. **Con 200 nulos el p mínimo resoluble es 1/201 ≈ 5e-3, que NO
alcanza.** Por lo tanto: **1200 nulos** donde se quiera poder cruzar el umbral (p mínimo
8.3e-4), o se declara que la celda no puede alcanzarlo y se reporta el p crudo. Se decide por
celda **antes** de correr y queda en el log.

## 7. Qué va en el log, sin excepción

`repo_commit`, seed, N, α, n_nulos, n_ord, MAX_SWEEPS, no_convergencias, versiones de Python y
numpy, plataforma, `donde` (este Codespace, no un contenedor ajeno), y
`variables_no_consideradas: "todas las que no están en este log"`.

Export **después de cada celda**, no al final. Si se corta, lo corrido queda.

## 8. Reglas de ejecución

1. **Driver nuevo en `experiments/`, escrito de cero.** No se copia y pega de
   `verificacion_p1_p3.py` ni de `ckm_p1p4_module.py` (pedido explícito de delamor).
2. **No se toca** `experiments/ckm_p1p4_module.py` ni `process/initial_static_model/hopfield.py`:
   son traza. Ver `experiments/CERRADO_LEER_ANTES_ckm_p1p4_module.md`.
3. Se importa de `services/landscape_engine.py` lo que ya existe y está testeado
   (`relax`, `n_eff`, `basin_masses`) en vez de reescribirlo. Si algo se pule, vuelve a
   `services/` con test y docstring, por CONVENTIONS.
4. **Cada archivo que se escriba dice qué es:** *esto midió* o *esto intenta reproducir*.
5. Checkpoint al terminar cada pregunta: se reporta y se espera el OK.
6. **No se interpreta.** Los cuatro veredictos pueden ser "no" o "no medible". Sale como salga.

## 9. Lo que esta TASK NO hace

- No mide el corpus. No dice nada sobre W_ckm_corpus_v2 ni sobre los informes.
- No reabre lo cerrado en el REG borrador. Si un resultado de acá lo tocara, se escribe un REG
  nuevo, no se edita el viejo.
- No replica a Aiyappa. Lo cita.
- No toca N_eff contra enumeración exacta, SALAMANCA, D3, ni la D_ckm canónica.
- No decide si el CKM "sirve". Registra si su marco declarado exhibe lo que predice.

## 10. Antes de la primera línea de código

Dos revisiones, que son lectura:

1. **Comparabilidad.** Con W móvil hay que declarar qué se fija y qué corre en cada protocolo.
   En Q·CAMINO ya está resuelto por conmutatividad de Hebb (la W final es la misma en todas las
   ramas; sólo cambia la historia). En Q·FLECHA hay que fijar que la comparación t_rem vs t_add
   parta del **mismo** estado y la **misma** W. Escrito en §2 y §4; se verifica en el código.
2. **Literatura.** Histéresis y asimetría en Hopfield **con aprendizaje** puede estar publicada
   (el Modelo Híbrido ya cita arxiv:2508.10765 para histéresis como cruce inverso de la
   bifurcación, y Lipiecki–Sznajd-Weron arXiv:2511.17837 para q+≠q−). Si lo que acá se pregunta
   ya está contestado en la literatura, **esto es replicación declarada, no hallazgo**, y se dice
   antes de correr. Buscar y reportar.

---

# APÉNDICE — Lo que NO se corre, porque se demuestra

*Agregado el 5 oct 2026 a señalamiento de delamor: "es obvio matemáticamente".*
*Regla que queda: antes de correr una celda, preguntar si el resultado es un teorema. Si lo es,
se demuestra en una línea y no se gasta una corrida. Correr lo demostrable es vanidad.*

## D1 — La re-adición en k-core recupera siempre. No hace falta medirlo.

Sea G fijo, k fijo. El k-core de G es **único**: es la unión de todos los subconjuntos con grado
interno ≥ k, y la unión de dos tales subconjuntos vuelve a serlo. Llamemos C = core(G).

Quitar el nodo i y podar da core(G−i) ⊆ C. Volver a poner i y hacer bootstrap sobre **el mismo G**:
el operador de bootstrap es monótono y C es un punto fijo que contiene a la semilla
core(G−i) ∪ {i}; además ningún nodo agregado puede caer fuera de C, porque entra con ≥ k vecinos
en un conjunto contenido en C. Entonces el bootstrap termina exactamente en C.

**Recuperación = 1 idénticamente, para todo G, todo k y todo i.** No es un hallazgo de 6 grafos:
es el enunciado de unicidad del k-core. Las 200 corridas de nulo que se hicieron el 4 oct no
podían dar otra cosa. **No se repite** (ya está en §4 de la TASK, ahora con la demostración).

## D2 — Con W ≥ 0, la rama DOWN del protocolo viejo es constante. Tampoco hacía falta medirlo.

σ = todo +1 con W ≥ 0: h_i = Σ_j W_ij > 0 para todo i con algún peso, y la regla GOLES conserva
σ_i cuando h_i = 0. Entonces todo +1 es **absorbente**. Liberar clamps no puede bajar ningún
nodo. `md ≡ 1` para toda W no negativa, y el estadístico se reduce a `1 − mean(m_up)`.
Lo medí hoy con 3 corridas; era un teorema. Queda como ejemplo de lo que esta regla evita.

## D3 — El óptimo sobre subconjuntos aleatorios depende sólo de la media. Es linealidad.

c(S) es lineal en los pesos y los subconjuntos son aleatorios, así que
E[c(S)] = media(W)·g(ρ) con g igual para todo par. El óptimo interior existe ⇔ media(W) < 0, sin
importar **dónde** estén los pares negativos. Ya verificado por el operador el 4 oct; es álgebra.
Por eso Q·VENTANA §5 **no** usa subconjuntos aleatorios: usa estructura de bloques que salió de
los patrones, y su nulo es de ubicación con media fija. Esa sí es una pregunta.

## D4 — El retiro es la inversa exacta sobre W. Por construcción.

W ← W + (1/N)ξξ^T y W ← W − (1/N)ξξ^T se cancelan exactamente. No hay nada que medir sobre W.
Por eso Q·FLECHA mide **barridos de relajación**, no conjuntos: la asimetría, si existe, es de σ
y de su tiempo. Si alguien mide la W y encuentra simetría, midió la identidad.

## D5 — N·SIN_HISTORIA da 0, pero sólo con el orden de barrido fijo.

Hebb es suma de productos externos, luego conmuta: la W final no depende del orden de ingesta.
Si además se relaja **una sola vez** desde el mismo σ inicial, el estado final es el mismo para
todos los órdenes de ingesta → d = 0. **Pero** la relajación asíncrona usa un orden de barrido
aleatorio, que es otra fuente de variación. Para que el nulo valga 0 exacto hay que **fijar el
orden de barrido** en esa rama. Si no se fija, d_nulo > 0 por el barrido y el nulo deja de ser
0 por construcción: pasa a ser un nulo que hay que medir.

**Corrección a §2 de esta TASK:** N·SIN_HISTORIA se corre con orden de barrido fijo y declarado.
Queda escrito acá porque lo encontré al demostrarlo, no al correrlo.

---

## Qué queda para código, después de esto

| | ¿se demuestra? | ¿se corre? |
|---|---|---|
| Q·CAMINO | el nulo sí (D5); el resultado real no | **sí** |
| Q·CASCADA | no — el exponente τ no sale de un teorema | **sí** |
| Q·FLECHA | la inversa sobre W sí (D4); los tiempos no | **sí** |
| Q·VENTANA | el caso de subconjuntos aleatorios sí (D3); el modular no | **sí** |

Cuatro corridas, no sesenta y una. Lo que se saca son los nulos y las celdas cuyo resultado era
un teorema. **El recuento de comparaciones de §6 baja y hay que recalcularlo antes de correr.**
