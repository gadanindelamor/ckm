# Criterios de diversidad en campos de conocimiento cohesivo

*Formulación conceptual y especificación técnica*

Documento autocontenido. No requiere conocer la implementación existente ni
la historia de cómo se llegó a estos criterios. Todo lo necesario para
escribir las rutinas desde cero está acá.

---

# Parte I — Formulación conceptual

## 1. El objeto

Un campo de conocimiento se representa como un grafo con pesos:

```
W ∈ ℝ^{N×N},  simétrica,  diagonal cero
σ ∈ {−1,+1}^N   estado — qué nodos están activos
```

`W_ij` codifica la interdependencia estructural entre los conceptos `i` y
`j`. Positiva: co-ocurren, se sostienen. Negativa: están en oposición
estructural. Cero: no hay relación registrada.

La dinámica es relajación de Hopfield **síncrona**:

```
h = W σ
σ' = sign(h),  con σ'_i = σ_i cuando h_i = 0
```

La regla de empate —conservar σ_i cuando el campo local es exactamente
cero— no es un detalle de implementación. Ver §4: es lo que mantiene el
mapa determinista, y de eso depende todo lo demás.

**Régimen dinámico.** W no es fija: se reconstruye a medida que el corpus
crece. Toda cantidad definida acá es de una *versión* de W, y comparar
entre versiones exige que el conjunto de nodos sea el mismo o que la
correspondencia esté declarada. No hay continuidad automática.

## 2. Qué se quiere medir, y por qué la medida obvia no sirve

La pregunta es cuánta **diversidad estructural** admite el campo: si el
conocimiento representado sostiene múltiples configuraciones estables o
colapsa a una sola.

La medida obvia —contar cuántos estados distintos alcanza la relajación
desde reinicios aleatorios— tiene dos problemas, y ninguno se arregla
mejorando el muestreo.

### 2.1 Lo que se cuenta no es lo que se cree contar

El espacio de estados es finito y el mapa determinista. Por lo tanto **toda
trayectoria entra en un ciclo en tiempo finito**. No hay caso en que no
converja: converge siempre, a un conjunto invariante.

Un punto fijo es el caso de **un** elemento. Un ciclo de dos estados es un
conjunto invariante de **dos** elementos. Los dos son órbitas; el punto fijo
no es más "convergido" que el ciclo, es una órbita degenerada.

Detener la iteración en un tope fijo y quedarse con el último estado
devuelve **una fase** de la órbita — cuál, depende de `(tope − cola) mod
período`. Dos trayectorias que llegan a la misma órbita por colas de
distinta paridad devuelven estados distintos y se cuentan como dos.

En redes con W simétrica el período está acotado por 2 (Goles), así que la
sobrecuenta por fase es a lo sumo ×2. Con W asimétrica aparecen períodos
largos y el factor llega al período: se han observado 2 órbitas contadas
como 12 con período 6.

**Entonces hay tres cantidades distintas, no una:**

| | qué es |
|---|---|
| **L** | conjunto máximo invariante — un conjunto de **estados** |
| **L/~** | sus subconjuntos invariantes mínimos — las **órbitas** |
| terminales | estados devueltos por el corte — **instancias** |

Ordenan siempre `|L/~| ≤ terminales ≤ |L|`. Contar terminales estima `|L|`
por debajo, y no estima `|L/~|` en absoluto.

### 2.2 Los conteos no convergen; las masas sí

Aun contando órbitas correctamente, el número no se estabiliza al aumentar
el presupuesto de muestreo. La razón es estructural:

> Una **masa de cuenca** es una probabilidad — P(σ₀ cae en esa órbita).
> Más muestras la estiman mejor; no la hacen crecer.
>
> Un **conteo** cuenta resultados distintos vistos. En un espacio de
> tamaño 2^N, más muestras siempre encuentran más.

Medido contra verdad exacta (enumeración completa de 2²⁰ estados): con
100.000 muestras, el conteo de órbitas puede errar **28%** mientras la masa
agregada de las diez mayores erra **0.0%**. En el mismo corpus, con 1.000
muestras el conteo erra 91% y una medida basada en masas erra 0.4%.

Hay dos regímenes:

- **masa concentrada** — unas pocas órbitas absorben casi todo. Las masas
  convergen rápido y el conteo es irrelevante: las órbitas que faltan no
  pesan.
- **masa plana** — muchas órbitas de peso similar. El conteo es alcanzable
  pero cada masa individual es ruidosa; hay que agregar.

### 2.3 Sin medida de referencia declarada, la cantidad no existe

Toda cantidad basada en muestreo es función de **(W, medida sobre σ₀,
presupuesto)**, no de W. Cambiando solo la distribución de la que se sortea
σ₀ —mismo campo, mismo presupuesto— el número de órbitas halladas varía por
un factor de **8×**.

Esto no es ruido a promediar: la masa de cuenca **es** P(σ₀ ∈ cuenca), y esa
probabilidad está definida respecto de una distribución. Cambiar la
distribución cambia la cantidad, por definición.

**La referencia canónica es la uniforme sobre `{−1,+1}^N`**: bajo ella la
masa de cuenca es el **volumen de cuenca**, propiedad de W sola. Cualquier
otra referencia mide otra cosa — legítima, pero otra, y hay que declararla.

Advertencia: sortear el número de nodos activos en una banda (p.ej. 30–70%
de N) y después elegir cuáles **no** es uniforme sobre el hipercubo. Es una
tercera referencia.

## 3. Los dos ejes

Los criterios se organizan en dos ejes que no coinciden con "más fino / más
grueso":

### Eje 1 — función de W sola, o dependiente de la sonda

El muestreo es un **mecanismo que se impone para probar**, no lo que el
sistema hace en operación. En operación se relaja un estado dado, uno por
entrada, no cien mil reinicios aleatorios.

Hay cantidades que no requieren muestrear nada: se calculan de W. Esas son
del instrumento. Las que requieren sortear σ₀ son de la sonda, y arrastran
la dependencia de §2.3.

### Eje 2 — topológico o métrico

Entre las de W sola, hay una separación adicional y verificada:

- **topológicas** — dependen solo del **patrón de signos**. Multiplicar los
  pesos negativos por cualquier factor no las mueve.
- **métricas** — escalan con las magnitudes.

Medido: amplificando los pesos negativos ×16, el índice de frustración no
se mueve (0.0258 en todo el rango) mientras el peso negativo relativo va de
0.031 a 0.338 y λ_min de −0.069 a −0.422.

Son dimensiones independientes. Un barrido que amplifica magnitudes mueve
lo métrico y deja lo topológico fijo — cualquier conclusión sobre
"frustración" sacada de ese barrido es sobre magnitud, no sobre estructura.

## 4. La condición de exactitud

`sign(h)` es discontinua en `h = 0`, que es exactamente donde vive la regla
de empate. Un error de un ULP en `h` se convierte en una diferencia de ±1 en
una variable de estado.

Esto **no es un defecto del software**: la suma en punto flotante no es
asociativa, y BLAS elige el orden de acumulación según cómo recorre memoria.
Dos expresiones algebraicamente idénticas —`W σ` y `σᵀ W` con W simétrica—
acumulan en distinto orden y difieren en el último bit.

Con pesos no representables exactamente en binario, eso basta para que el
**46%** de los pasos de relajación devuelva un sucesor distinto según cómo
se escriba el producto. Con pesos diádicos, **0%**.

**Regla:** los empates son exactos si y solo si los pesos lo son.

Consecuencia operativa sobre la normalización de W. Si W se construye
dividiendo conteos enteros por su máximo:

- **`max` potencia de dos** → división exacta → dinámica reproducible
- **`max` no potencia de dos** → se pierden bits → hasta 46% de los pasos
  dependen del orden de suma

Verificado: el mismo campo, normalizado por 3 en vez de por 4, produce el
**mismo número** de órbitas (33) pero **18 de las 33 son distintas**. Un
conteo idéntico sobre conjuntos que se solapan a medias. Sin comparación de
conjuntos, invisible.

Tres mitigaciones, en orden de costo:

1. **No normalizar** — trabajar con los conteos enteros. Cero divergencia.
   Cambia la escala de toda cantidad métrica (μ_W, β_c, umbrales absolutos
   sobre c(S)), no cambia las adimensionales (razones, fracciones).
2. **Normalizar por la potencia de dos siguiente** — mantiene W en [0,1] y
   conserva la exactitud. Cero divergencia, verificado.
3. **Suma exacta** (compensada, tipo Kahan/Shewchuk) para el campo local.
   Da el signo correcto siempre; costo despreciable a N ≤ 100.

Ninguna es garantía de reproducibilidad entre entornos: elimina una fuente
identificada. La reproducibilidad completa exige congelar el entorno, no
enumerar sus variables.

Nota sobre actualización asíncrona: reduce el efecto en un orden de
magnitud —de ~46% de pasos a ~5% de trayectorias— porque la función de
energía disipa el error en vez de propagarlo lateralmente. No lo elimina:
la degeneración en `h = 0` es exactamente el punto donde la garantía de
Lyapunov no distingue entre las dos movidas.

---

# Parte II — Especificación técnica

Cada criterio: definición, algoritmo, complejidad, y qué requiere.

## A. Primitiva común — detección de órbita

Todo lo del grupo dependiente-de-sonda se construye sobre esta rutina.

```
ENTRADA:  σ₀ ∈ {−1,+1}^N,  W,  tope
SALIDA:   (órbita, período, cola, estado_en_tope)

visto ← mapa vacío        # estado → paso en que se vio
seq   ← lista vacía
s ← σ₀
para t = 0 .. tope−1:
    k ← clave(s)                      # serialización exacta del estado
    si k ∈ visto:
        cola    ← visto[k]
        período ← t − cola
        idx     ← cola + ((tope − cola) mod período)
        devolver (conjunto(seq[cola:]), período, cola, seq[idx])
    visto[k] ← t
    seq.append(s)
    h ← W s
    s ← sign(h), con s_i = s_i previo donde h_i = 0
devolver (conjunto({s}), 0, −1, s)    # tope agotado — defensivo
```

**Por qué la detección es exacta y no heurística.** El espacio es finito y
el mapa determinista: la trayectoria debe repetir un estado. El tramo entre
las dos apariciones es la órbita.

**La órbita se representa sin orden** (conjunto de estados). Eso no pierde
información: el mapa es determinista, cada estado tiene **un** sucesor, así
que el orden cíclico queda determinado por el conjunto. Dos órbitas
distintas no pueden compartir un estado. Verificado sobre grafos asimétricos
con períodos de 1 a 30: el número de conjuntos coincide con el de ciclos
ordenados, y ningún estado aparece en dos órbitas.

**`estado_en_tope` reconstruye qué habría devuelto iterar hasta el tope**,
sin recorrer el ciclo. Sirve para compatibilidad con un contador de
terminales previo. La reconstrucción es exacta.

**Complejidad:** O(cola + período) pasos por trayectoria, cada uno un
producto matriz-vector O(N²). Reemplazar la comparación de convergencia por
un lookup en tabla hash de la serialización exacta —los estados son ±1, no
hay tolerancia que ganar— y salir al cerrar la órbita da aceleraciones de
40–87× frente a iterar siempre hasta el tope, en campos donde las órbitas de
período 2 son mayoritarias.

**Serialización del estado:** representación binaria exacta y canónica.
Cualquier codificación determinista sirve mientras sea consistente.

## B. Enumeración exhaustiva — verdad de terreno

Para `N ≤ 22`, no hay que estimar: se enumera.

```
ENTRADA: W  (N ≤ 22)
SALIDA:  órbitas, volumen exacto por órbita, |L|

M ← 2^N
# tabla de sucesores
para x = 0 .. M−1:
    sig[x] ← índice_de(paso_relajación(estado_de(x)))
# etiquetado por órbita, con memoización de trayectorias
memo ← array de −1, tamaño M
para x₀ = 0 .. M−1:
    si memo[x₀] ≥ 0: continuar
    recorrer desde x₀ siguiendo sig, registrando el camino;
    detenerse al llegar a un estado ya etiquetado (adoptar su etiqueta)
    o al repetir uno del propio camino (nueva órbita)
    etiquetar todo el camino
volumen[o] ← |{x : memo[x] = o}| / M
|L|        ← Σ_o |órbita_o|
```

**Costo:** ~1M relajaciones para N=20, del orden de 15 segundos con
memoización. La memoización es esencial: sin ella el costo se multiplica por
la longitud media de las colas.

**Importante:** el producto matriz-vector debe escribirse **igual** que en
la rutina que se quiere verificar. Dos orientaciones algebraicamente
equivalentes dan dinámicas distintas cuando los pesos no son diádicos (§4).

## C. Criterios dependientes de la sonda

Todos requieren declarar la medida de referencia sobre σ₀ y el presupuesto.

### C.1 Distribución de masas de cuenca — la base

```
ENTRADA: W, presupuesto n, medida de referencia μ
SALIDA:  masas m₁ ≥ m₂ ≥ ... (una por órbita hallada)

cuenta ← contador vacío
repetir n veces:
    σ₀ ← muestrear según μ
    (órbita, ...) ← detectar_órbita(σ₀, W)
    cuenta[órbita] += 1
m ← ordenar_desc(cuenta[o] / n  para cada o)
```

Con μ = uniforme sobre `{−1,+1}^N`, `m_o` estima el **volumen de cuenca**:
la fracción del espacio de estados que fluye a esa órbita. Propiedad de W.

Todo lo que sigue se deriva de `m`.

### C.2 Número efectivo de órbitas — `N_eff`

```
N_eff = 1 / Σ_o m_o²
```

Inverso del índice de Simpson. Se comporta como un conteo —"cuántas órbitas
efectivamente"— pero converge como una masa, porque lo es.

**Propiedad verificada.** Contra verdad exacta, con presupuesto 100.000:

| campo | error del conteo de órbitas | error de N_eff |
|---|---:|---:|
| masa plana | 0% | **0.3%** |
| masa intermedia | 15% | **0.6%** |
| masa concentrada | 28% | **0.0%** |

Con presupuesto 1.000 en el campo de masa concentrada: el conteo erra 91%,
N_eff erra 0.4%.

**Es el reemplazo directo del conteo** en cualquier índice construido como
razón de conteos. Preserva la orientación: más órbitas efectivas = más
diversidad.

### C.3 Masa agregada top-k

```
T_k = Σ_{i=1..k} m_i        ∈ [0,1]
```

Medida de **concentración**: alta = la masa está en pocas órbitas.

**Usar el agregado, no el máximo individual.** El máximo estimado por
muestreo tiene sesgo **hacia arriba** cuando las cuencas son parecidas: es
el máximo de estimaciones ruidosas, y el máximo del ruido supera al máximo
real. Agregando, el sesgo se cancela — verificado: 26.5% de error en el
máximo contra 16.0% en el top-10, mismo muestreo.

Nota de orientación: `T_k` **crece** cuando la diversidad **baja**. Si se lo
usa dentro de un índice construido para que "más alto = más degradado", el
signo se invierte respecto de un conteo. Usar `N_eff` evita el problema.

### C.4 Presencia de nodo, ponderada por masa

Para cada nodo `i`:

```
p_i = Σ_o  m_o · fracción_de_estados_de_o_con_σ_i_activo
```

Es P(nodo `i` activo en el estado final). Responde **qué nodos habitan los
atractores**, no cuántos hay. Ninguna cantidad de C.1–C.3 lo captura.

**Ponderar por masa es necesario.** Promediar sobre órbitas *únicas* sin
ponderar hereda el sesgo de conteo: verificado, deriva **0.19** contra
**0.03** de la versión ponderada, al aumentar el presupuesto ×100.

### C.5 Estructura de co-presencia

Sobre la matriz `A` de órbitas × nodos (entrada = fracción de estados de la
órbita con el nodo activo), **ponderando las filas por masa**:

- **correlación de co-presencia** entre nodos → matriz N×N
- **clusters** por co-movimiento (aglomerativo sobre `1 − corr`)
- **oposiciones perfectas**: pares con correlación por debajo de un umbral
  (p.ej. −0.90)

Mide la **organización interna** del conjunto de atractores, no su
cardinalidad ni su masa.

**Cuidado con nodos de presencia constante:** varianza cero produce
correlación indefinida. Reemplazar por 0 —sin información de co-presencia
diferencial, no correlación artificial— y registrar cuáles fueron.

## D. Criterios de W sola

Ninguno requiere muestrear. Son propiedades del campo.

### D.1 Índice de frustración — topológico

```
S ← sign(W)
para cada triángulo (i,j,k) con S_ij, S_jk, S_ik todos ≠ 0:
    frustrado si  S_ij · S_jk · S_ik < 0
índice = frustrados / triángulos_completos
```

Un grafo con signos es **balanceado** si y solo si el índice es 0: existe
una partición de los nodos en dos grupos con todas las aristas internas
positivas y todas las cruzadas negativas. Índice > 0 significa que ninguna
partición lo logra — hay tensión que no se puede resolver reordenando.

**Invariante a escalar los pesos.** Depende solo de signos. Verificado:
amplificar los negativos ×16 no lo mueve.

**Complejidad** O(N³) por enumeración de triples; trivial hasta N ~ 200. Para
N grande, muestrear triples da un estimador insesgado.

**Uso:** distingue un campo con tensión estructural de uno sin ella, sin
ambigüedad y sin muestrear. Un campo cuya construcción descarta los signos
negativos pasa de índice alto a exactamente 0 — no "pierde pesos negativos":
pierde **toda** la frustración.

### D.2 Peso negativo relativo — métrico

```
frac_neg = Σ_{i<j, W_ij<0} |W_ij|  /  Σ_{i<j} |W_ij|
```

Cuánto del peso total está en oposición. Escala con la amplitud de los
negativos; complementa a D.1, que no la ve.

### D.3 Espectro — métrico

```
λ = autovalores(W)   # W simétrica → reales
```

`λ_min` se hace más negativo con la amplitud de la frustración. `λ_max`
domina el modo cohesivo. La brecha entre ambos caracteriza cuánto compite la
tensión con la cohesión.

**Complejidad** O(N³), una sola vez por versión de W.

### D.4 Heterogeneidad de frecuencias marginales

```
f_i = Σ_j |W_ij|
CV  = desvío(f) / media(f)
```

CV alto indica estructura bimodal: un núcleo de nodos fuertemente acoplados
y una periferia de nodos poco conectados. Predice que las cantidades
promediadas sobre todos los nodos van a estar dominadas por el núcleo.

### D.5 Diagnósticos de exactitud

Baratos, y condicionan la confiabilidad de todo lo demás (§4):

```
valores_distintos = |{W_ij ≠ 0}|
diádico           = todo peso no nulo exactamente representable en binario
frac_empates      = fracción de h_i que dan exactamente 0 sobre muestras
frágil            = fracción de pasos cuyo sucesor cambia al reescribir
                    el producto en la otra orientación
```

`frágil > 0` significa que los resultados dependen de cómo se escribió el
producto matricial. Es diagnóstico obligatorio antes de reportar cualquier
número.

---

# Parte III — Lo que queda abierto

**Qué debería contar un índice de degradación del campo.** El principio de
invariancia define el conjunto máximo invariante; no dice si el modelo debe
medir `|L|`, `|L/~|`, masas o `N_eff`. Es decisión del modelo, no del
teorema.

**Si los criterios de W sola y los de sonda miden lo mismo.** Está medido
que la frustración es invariante a amplificar magnitudes mientras el conteo
de órbitas y la forma de las cuencas se mueven — eso descarta que uno resuma
al otro. Falta medición cruzada sistemática.

**Profundidad de cuenca.** La longitud de cola —cuántos pasos hasta entrar
en la órbita— resultó plana en todo un barrido de amplitud, así que no
sirve como proxy de profundidad. Queda abierto qué la mide: barreras de
energía entre órbitas es el candidato natural y no está probado.

**Frontera entre clusters.** Una coercividad definida como
`min(cohesión_interna_a, cohesión_interna_b) / cohesión_cruzada` mide
cuánto resiste una frontera. Requiere clusters, que vienen de C.5, que
depende de la sonda. Si se la quiere de W sola, hay que derivar la partición
de W directamente —corte espectral— y no de los atractores.

**N > 22.** La verdad de terreno por enumeración no escala. Para campos
mayores todo criterio de sonda queda sin referencia exacta contra la cual
validarse.

---

*Todas las propiedades marcadas como verificadas lo fueron por medición
directa, incluyendo comparación contra enumeración exhaustiva del espacio de
estados completo en campos de N = 20.*
