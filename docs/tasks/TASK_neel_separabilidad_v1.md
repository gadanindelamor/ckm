# TASK_neel_separabilidad_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: DEFS §15 (Néel) y §16 (SALAMANCA), ambos "propuesto — no
verificado" desde que se escribieron. REG_mapeo_magnetico_ckm_v1 §3.1–3.3.
REG_unidad_texto_saturacion_v1 §5.1–5.3 (autor único; no hay estado nulo;
el drift de contar "pero").*

---

## Qué entendí

**El nombre es la definición.** *(delamor: Basilio Salamanca, almacenero de
Cipolletti, Río Negro. En la puerta, a la derecha, un cartel escrito a mano:
"Lo que natura non da, SALAMANCA non presta". Y: "no se fía".)*

- **No presta**: la estructura que no está en el corpus no se la puede pedir
  prestada a ningún procedimiento.
- **No se fía**: tampoco se le da crédito por adelantado. El ruteo por
  marcadores fía — asume la tensión y después la cobra en pares negativos.

**Néel es más preciso, pero va segundo** *(delamor: Néel es más preciso
que Don Basilio. Y: T0 y T1 tienen que existir primero, creo)*.

SALAMANCA responde **si existe** la partición; Néel responde **cuán
profunda** es, en una cantidad continua —una temperatura— igual que el
registro de borde de REG_seleccion_nodos. No compiten: van uno después del
otro, que es el orden original de DEFS §15/§16.

**Corrección de un diseño anterior de esta misma TASK** (Code, Opus 5):
propuse derivar T0/T1 en cada β desde las correlaciones muestreadas, y
afirmé que así el nulo quedaba interno —S ≈ 0 en los dos extremos, un pico
sólo si hay módulos—. Es falso. `S` calculada sobre la partición elegida en
ese mismo β es un **máximo sobre particiones**, y un máximo es positivo
aunque no haya nada. Medido con spins independientes (cero estructura):

| muestras | S de la mejor partición |
|---:|---:|
| 200 | 0.030 |
| 1000 | 0.014 |
| 5000 | 0.005 |

Nunca cero, y decae como 1/√muestras: la altura del pico dependería de
cuántas muestras se tomen. Para saber si un pico es real haría falta una
referencia externa — exactamente lo que el diseño decía evitar. Era el drift
de §5.3 otra vez, con más álgebra.

## Qué hacer

Dos pasos, en este orden.

**Paso 1 — SALAMANCA**: establecer si T0/T1 existen en W_pos, y cuáles son.
Estructural, sobre W_pos, una sola vez. Normalized cut espectral (sin
semilla: el problema huevo/gallina del min-cut está en
REG_mapeo_magnetico §3.2). Necesita **ensemble nulo prestado** para decir
"no pasa nada" — es un nivel, y un nivel necesita contra qué compararse.

**Paso 2 — Néel**: barrido de β *(delamor)* sobre W_pos con la partición
T0/T1 **fija**, la que dio el paso 1. Sin reajuste por β, sin sesgo de
maximización.

### El punto que hubo que resolver

W_pos es ferromagnética: el fundamental es todo encendido y **los signos no
separan**. No hay T0/T1 legible de un atractor. La separabilidad sale de las
correlaciones sobre el ensemble térmico.

### Procedimiento

**Paso 1 — SALAMANCA (existencia de T0/T1)**

1. Corte espectral de W_pos: segundo autovector del laplaciano → partición
   T0/T1. `ncut(T0,T1)` observado.
2. Ensemble nulo: mismo corpus con la co-ocurrencia destruida, W
   reconstruida con los servicios reales (el barajado de
   REG_unidad_texto §4.1 ya está probado). `ncut` de cada barajado.
3. T0/T1 **existen** si el ncut observado cae fuera de la distribución
   nula. Si no: no hay partición, y Néel no tiene sobre qué barrer.

**Paso 2 — Néel (profundidad de la frontera)**

Con T0/T1 fijos del paso 1, para cada β de frío a caliente:

1. Muestrear `n_muestras` estados con `boltzmann_warmup` desde σ₀ aleatorios.
2. `C_ij = ⟨σ_i σ_j⟩` sobre las muestras.
3. `S(β) = media(C dentro de T0 o de T1) − media(C que cruza)`, con la
   partición **fija**.

- β frío → la frontera se sostiene → **S alto**
- β caliente → ruido → **S → 0**
- β_Néel = donde S colapsa.

**Salida: la curva S(β) completa**, no un veredicto. Continua, y la
categoría se deriva al leer.

## Pre-registro — declarado ANTES de correr

Para que el criterio pueda fallar:

| corpus | posiciones | paso 1 (SALAMANCA) | paso 2 (Néel) |
|---|---|---|---|
| caso09 — debate gun control | dos, por diseño | **T0/T1 existen** | curva con colapso |
| informes CKM (versión y página) | una, autor único | **no existen** | no corre |
| canal IAP caso13 / caso14 — coordinación | varias voces, ninguna opuesta | **no existen** | no corre |

Si sale al revés, el que está mal es el criterio, no el corpus.

Precondición de §3 del REG: **un W saturado no tiene ceros**, y sin ceros no
hay módulos que separar. caso09 es el único corpus no saturado (307/496).
Si los saturados no dan partición, hay que distinguir "no hay estructura" de
"no hay resolución para verla" — queda como lectura, no se resuelve acá.

## Decisiones

1. **Sobre W_pos, siempre.** El criterio es previo a W_mixta: decide si
   W_mixta tiene objeto. Se construye con `force_w_pos=True`.
2. **Partición fija, establecida antes del barrido** *(delamor)*. §3.3
   dice que los clusters emergen del barrido; medido, eso no se sostiene
   —reajustar por β es reajustar al ruido— así que emergen del paso 1, que
   es estructural y no muestreado.
3. **k = 2** para esta TASK. Adversarial es bipolar por definición. k > 2
   queda abierto como diagnóstico, nunca como admisión.
4. **No decide nada en el canal.** Es análisis sobre W acumulada, no por
   ingesta (REG_mapeo_magnetico §3.1: la partición no es estable hasta que W
   converge).

## Qué no hace

- No construye W_mixta ni cambia el ruteo por marcadores.
- No incorpora nada a W ni cambia services/. Vive en `experiments/` hasta
  que haya qué decidir.

## Verificación

- El extremo caliente del barrido da S ≈ 0 en todo corpus (control de que
  la curva es la que se cree). El extremo frío NO tiene que dar 0: si la
  partición existe, en frío se sostiene.
- Control negativo del paso 1: un corpus barajado no debe dar T0/T1.
- El pre-registro se cumple o no, y se reporta como haya salido.
- Determinismo: misma seed, misma curva.

## Abierto

- k > 2.
- El ensemble nulo se arma **barajando el corpus** y reconstruyendo W con
  los servicios reales — más fiel al campo y ya probado en
  REG_unidad_texto §4.1. Queda abierto si conviene además el barajado de
  pesos conservando el grado, que es más barato y no necesita los textos.
- Qué hacer con los candidatos a pares negativos que el pico identifique —
  esta TASK los deja listados, no los incorpora a W.


---

## Resultado — primera corrida (caso09, sep 2026)

Instrumento: `experiments/driver_neel_salamanca.py`.

### R0. Error en el pre-registro (Code, Opus 5)

`caso09` **no es el debate de gun control**: es el canal IAP (caso 0.9,
heterogeneidad de proveedor). Los nodos lo dicen — `claudesonnet_`,
`groqllama_`, `ava`, `cartographer`, `bell`, `story`. El corpus adversarial
real es **fourforums** (`process/experiments/`, once REGs). La condición de
referencia declarada en esta TASK **no tenía ningún corpus adversarial**, y
el ✓ que imprimió el driver comparó contra una expectativa mal asignada.

### R1. SALAMANCA encuentra partición, y es real

| | valor |
|---|---:|
| ncut observado | **0.633** |
| nulo: media / p10 (20 barajados) | 0.873 / 0.840 |
| p | **< 0.001** |

- **T0** — `claudesonnet_` `groqllama_` `joined` `channel` `task` `topic` `conversation`
- **T1** — `ava` `cartographer` `bell` `eyes` `paper` `story` `memory`

Es el corte **protocolo/identidad contra contenido**, el mismo de
REG_unidad_texto §4.3. Estructura hay.

### R2. Néel: la frontera tiene profundidad cero

Leído por la **cola**, no por la media *(delamor: no soy adepto a los
promedios, ni a las distribuciones normales inexistentes; habito las
colas)*. Discriminante entre cola real y cola de ruido: **persistencia** —
una cola de ruido se rebaraja con la semilla.

| β | de los 20 pares menos correlacionados, cuántos persisten en 3 semillas | por azar |
|---:|---:|---:|
| 0.244 | **1** (interno, `joined channel — language`) | 0.03 |
| 0.122 | **0** | 0.03 |
| 0.068 | **0** | 0.03 |

La cola es ruido. En frío, interno y cruzado son ambos +0.999: W_pos no
tiene frustración, así que todo se alinea, también a través de la frontera.

### R3. Modularidad no es adversarialidad

*(delamor)*

Ninguno de los dos criterios dice esto solo:

- SALAMANCA: **hay dos módulos**.
- Néel: **esa frontera no tiene profundidad**.

Módulos sin frontera. **SALAMANCA sola habría admitido W_mixta en un canal
de coordinación** — que es el error que esta TASK venía a evitar.

**Corrección a DEFS §16**: dice *"detecta si W_pos tiene estructura
adversarial"*. Lo que detecta es **modularidad**. Una palabra, dos objetos —
Babel, y es la razón de que el criterio admita de más. La admisión requiere
los dos pasos, no el primero.

Y salva a §15 de lo que Code le había achacado en el camino ("Néel no puede
funcionar sobre W_pos"): **Néel funcionó** — devolvió el vacío, que es
aquello para lo que delamor lo eligió. No hace falta frustración para que
haya señal; alcanza con que dos módulos se alineen internamente antes que
entre sí.

### Pendiente

Control positivo con **fourforums**. Si ahí tampoco hay cola persistente, el
que no ve es el instrumento.
