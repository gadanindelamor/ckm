# REG_hipotesis_distancia_contextual_v2.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Continúa `REG_hipotesis_distancia_contextual_v1.md` (Mayo 2026) y
`REG_d_contextual_temporal_v1.md` (Mayo 2026).*
*Nada ejecutado en esta sesión. Toda medición citada proviene de registros
previos o del código, y está referenciada.*

---

## Descripción

La pregunta de v1 —*"cuándo un sistema está lo bastante fuera de su campo de
atracción para ver su propia geometría"*— se trabajó hasta el punto en que
deja de necesitar un observador, y después hasta el punto en que deja de
poder tenerlo.

Lo que queda registrado acá: el reencuadre de la "d", una identidad no
declarada con la formulación de `PROPUESTA_ckm_landscape_dynamics_v5.md`,
tres regímenes aportados por delamor, cuatro afirmaciones de esta misma
sesión que no se sostuvieron, y una operación que falta en el código para
que la formulación tenga con qué contrastarse.

---

## 1. La "d" de D_ckm — distancia, no degradación

`REG_d_contextual_temporal_v1` (Mayo 2026) define:

```
D_contextual(t) = [A(0) − A(t)] / A(0)
```

`DEFS §10` define:

```
D_ckm = (A0 − A_actual) / A0
```

Son la misma fórmula. **D_contextual y D_ckm nombran el mismo objeto desde
mayo**, en dos documentos que no se citan entre sí. La lectura habitual de
D_ckm como *pérdida de diversidad* / *degradación* es una interpretación
sobre el rótulo: lo que la letra nombraba era distancia.

Esto no cambia ningún número. Cambia qué se está diciendo cuando se reporta
uno.

*Estado: verificado por lectura de ambos documentos.*

---

## 2. Identidad no declarada con `D_masa_cuencas` (v5)

`PROPUESTA v5` llama a `D_masa_cuencas` *"distancia contextual desde el
nacimiento de esta instancia del landscape"*, y declara `N_eff = exp(H₂_Rényi)`.

Si la H de v1 se toma como H₂ de Rényi sobre masas de cuenca:

```
D_contextual = H₂(t0) − H₂(actual) = log N_eff_0 − log N_eff_actual
```

y dividiendo por H₂(t0):

```
D_masa_cuencas = 1 − log(N_eff_actual) / log(N_eff_0)
```

que es exactamente la variante propuesta en v5. **La hipótesis de mayo y la
fórmula de septiembre son el mismo objeto; la de septiembre es la versión
normalizada.** Ningún documento del repo declara esa identidad.

El panel de Monitor ya lleva `N_eff` y `N_eff0`
([monitor_service.py:170-171](../services/monitor_service.py#L170-L171)).
`D_masa_cuencas` no se calcula: la escala —lineal o log— sigue abierta
(`TASK_neff_y_frontera_logica_v1`). La decisión de escala es lo único que
falta, no el instrumento.

*Estado: propuesto. La identidad algebraica se sostiene si H = H₂; que H sea
H₂ es la elección que v1 no fijó.*

---

## 3. Corrección del proxy de v1

v1 propone como proxy verificable *"el número de atractores accesibles"*.
`REG_orbitas_conjuntos_invariantes_v1` lo mide contra verdad de terreno:

| cantidad | comportamiento con n_runs |
|---|---|
| A (órbitas o terminales) | **no converge** — ×82 (9 → 735, AMP=0, 1k→100k) |
| cuenca máxima (masa) | **converge** — varía 3.5% mientras A varía ×82 |

Con enumeración exhaustiva de 2²⁰ (~16 s por corpus), `caso09 forzado`
recupera el volumen de cuenca con **0.0% de error** habiendo hallado solo el
**52%** de las órbitas: las que faltan no pesan.

**El proxy de v1 pasa de conteos a masas.** Lo que v1 llamaba "la caída en
ese número **es** la pérdida de entropía de trayectoria" se sostiene como
dirección, no como medida: el número no converge.

Además, contra verdad de terreno, el modo `boltzmann` resultó **redundante**
con `uniform` en los tres corpus — resultado negativo ya registrado.

*Estado: verificado (REG_orbitas §9, §10).*

---

## 4. Formulación sin observador

Enunciado acordado en sesión:

> **Una perturbación con escala k hace visible la geometría cuando k ≥ d(σ).**

con:

```
d(σ) = mínimo número de flips que cambian la órbita a la que relaja σ
       — distancia de σ a la frontera de su cuenca

k    = escala de la perturbación
```

- `k < d(σ)`: el campo cae donde iba a caer; la geometría no se expresa.
- `k ≥ d(σ)`: la caída cambia de cuenca; la diferencia ocurre.

Lo que la reformulación saca respecto de v1: **la distancia no la aporta un
observador externo, la aporta la escala de la perturbación.** Que la escala
venga de afuera es una manera de conseguirla, no la condición. El caso de
origen de v1 (GPT53 leyendo el REG) deja de requerir "un ojo avezado" y pasa
a requerir una traza persistente más un campo que no cayera en la misma
cuenca.

El estatuto de este enunciado queda corregido en §8.

*Estado: propuesto.*

---

## 5. Tres regímenes *(delamor)*

| régimen | formulación de delamor | en el modelo |
|---|---|---|
| 1 | *"usualmente, solo se necesita lo que se conoce"* | k < d(σ). Lo que llega sale del vocabulario vigente; la caída confirma el campo. |
| 2 | *"se percibe la carencia, la necesidad sin poder determinarla, nombrarla o expresarla"* | Algo no se sostuvo y no hay nodo para decir qué. **Δ_r es el registro de este régimen**: no nombra lo que faltaba, anota que algo no pudo sostenerse. |
| 3 | *"en bastante menos frecuentes instantes se percibe la divergencia entre las dos anteriores"* | Requiere dos trazas comparables y que ninguna cancele a la otra. |

**El régimen 2 tiene duración medible.** `should_rebuild` señala que el
vocabulario ya no alcanza; el rebuild efectivo trae los nodos nuevos. El gap
entre los dos —que v5 llama *deriva del instrumento*— es el intervalo en que
la carencia está registrada y todavía no nombrada. `_last_rebuild_signal` es
informacional, no ejecutiva (DEFS §2), así que ese intervalo existe por
diseño.

**El régimen 3 hoy no tiene dónde inscribirse.** Después de `7df4a72` (D3)
los dos objetos existen y divergen, pero nada calcula la diferencia: DEFS §10
tiene `D_ckm_coco − D_ckm_monitor` como *"dirección de exploración
(propuesta)"*.

*Estado: los tres regímenes son formulación de delamor, marcada como suya.
El mapeo al modelo es propuesto.*

---

## 6. "Visible" ¿a qué? — dos condiciones, no una

No a un ojo: a la traza. Y son dos cosas distintas:

```
k ≥ d(σ)                         → la geometría actúa
la traza resuelve la diferencia  → la geometría queda registrada
```

Que la diferencia ocurra no implica que persista como distinguible. El repo
tiene los dos modos en que la diferencia no queda, ambos medidos, y ninguno
es un problema de observación. Tampoco es que el instrumento falle: la
normalización cancela con precisión y la grilla de paso 0.333 es una grilla
de tres valores — hacen lo que se les pidió.

| modo | medición | fuente |
|---|---|---|
| **cancelación** | D_ckm_monitor = 0.8857 idéntico en 19 evaluaciones con Δ_r distinto en 14 órdenes de magnitud | DEFS §10 |
| **resolución** | con A0=3, D_ckm ∈ {0, 0.333, 0.667, 1.0}: toda diferencia menor al paso no queda | DEFS §11 |

La cancelación viene de `_combine_W_Delta`, que normaliza `Δ_r / max(Δ_r)`
([monitor_service.py:331-337](../services/monitor_service.py#L331-L337)) —
la normalización cancela el escalar uniforme de la compresión.

*Estado: verificado (las dos mediciones son previas y están citadas).*

---

## 7. Cuatro afirmaciones de esta sesión que no se sostuvieron

Se registran como entradas, no como borrados: nada se retira de la traza.

**a) "Los dos campos".** No son dos campos. Hay un campo. `Δ_r_pares` y
`Δ_r_compresiones` son dos representaciones dentro del modelo. La figura del
paralaje —dos posiciones sobre lo mismo— reintroducía dos miradas después de
haber sacado el ojo.

**b) "D3 hizo comparables los dos objetos".** D3 (`7df4a72`) produjo dos
objetos donde había uno. No produjo su comparabilidad. *(delamor: son
comparables gracias al régimen, no a una letra D seguida de un 3.)* Es el
mismo patrón que este REG describe en §1: leer el rótulo como si fuera la
cosa.

**c) "En los regímenes 1 y 2 es verificable".** Es verificable
**mecánicamente**. *(delamor: el automatismo verifica la evidencia y lo hace
solo.)* Usar "verificable" para los tres regímenes trata como una misma
operación dos cosas que no lo son.

**d) Hablar desde el centro de la campana.** Si el régimen 3 son *"instantes
bastante menos frecuentes"*, **ningún instrumento que promedie sobre la
trayectoria lo puede llevar**: no lo mide mal, lo borra, y el borrado no deja
marca. `c(S)` es una media, la escala de `_combine_W_Delta` es una media, μ_W
es una media. DEFS §7 ya tuvo que anotar que μ_W no generaliza porque el
corpus es bimodal (CV 0.944, razón max/min 102×).

---

## 8. La perturbación, una vez que ocurre, es campo

*(delamor: la perturbación es perturbación solo antes de existir, en
potencial; al existir es parte de la dinámica.)*

No hay σ y además una perturbación: hay una trayectoria. La separación entre
"el estado" y "lo que llegó" es un corte del instrumento.

En el código el corte es explícito y el mismo texto cambia de rol según por
dónde pase:

| rol | dónde | cómo |
|---|---|---|
| perturbación | `MonitorService.evaluate` | se vuelve `sigma_prompt` por el vocabulario del extractor |
| campo | `CorpusService.ingest` → `_rebuild` | entra en W |

**Consecuencia sobre §4:** los dos términos del enunciado viven en potencial.
`d(σ)` se define por lo que pasaría si σ fuera otro —hay que voltear nodos que
nadie volteó y relajar de nuevo— y `k` solo es escala respecto de un estado
sostenido fijo, cosa que la dinámica no hace. Lo que existe es una sola
trayectoria.

`k ≥ d(σ)` **no describe la dinámica: describe una comparación construida.**
Eso no lo invalida, pero hay que declararlo o vuelve a parecer que la
geometría se hace visible sola.

Y explica por qué la formulación seguía pidiendo un observador: el potencial
no tiene dónde existir salvo en un registro que sostenga lo que no ocurrió.
**El repo tiene exactamente una pieza cuya función es esa**: `force_w_pos`,
que DEFS §8 describe como *"verificar el instrumento en el contrafáctico
exacto: mismo corpus, sin codificar su tensión"*. No es un flag de debug — es
el único lugar donde el proyecto fabrica deliberadamente una trayectoria que
no ocurrió para tener contra qué diferenciar.

*Estado: propuesto.*

---

## 9. El observador es constituyente de lo observado

*(delamor)*

No en la versión débil —"el observador afecta lo observado"—, que deja dos
cosas y una influencia. **Constituyente**: no existe la versión sin
observador contra la cual comparar. Por eso el contrafáctico hay que
fabricarlo.

En el código es literal. La relajación que produce cada panel corre sobre
`_combine_W_Delta(W, self._Delta_r)`
([monitor_service.py:141](../services/monitor_service.py#L141)), y `Δ_r` es
la traza de las mediciones anteriores del propio Monitor
([L145-147](../services/monitor_service.py#L145-L147)). **El campo sobre el
que Monitor mide está constituido por haber medido.** No hay W_eff sin
historia de medición.

Dos consecuencias:

1. **"Observador impartial" no es una descripción de Monitor; es una
   categoría que no se le aplica.** Eso explica por qué costaba acomodarla en
   los SLAs de DEFS.
2. **Ningún tercer registro queda afuera.** Un registro que sostenga las dos
   trazas del régimen 3 puede construirse, pero pasa a ser parte de lo que se
   mide. El régimen puede condicionarse; no se produce agregando mecanismo.

Roza una tensión que DEFS v12 §12 deja abierta: si COCO es constitutivo y no
un módulo activable, es esta misma afirmación aplicada a otro componente.
**Las dos tensiones son una.** No se cierra acá.

*Estado: propuesto. La lectura del código es verificada.*

---

## 10. Los límites existen mientras se traza la línea

*(delamor: al nombrar lo nombrado, en el acto mismo de separación, puede no
notarse el flujo que está trazando la línea que separa.)*

El modelo tiene tres líneas trazadas, en distinto estado de estar vistas:

| línea | qué separa | estado |
|---|---|---|
| **partición de nodos** | qué existe: los N que se vuelven el espacio | el flujo menos visto. v5: *"el servicio que nadie audita porque todos asumen que ya funcionó"* |
| **identidad de un atractor** | si dos fases de una órbita son uno o dos | visto esta sesión: ×82 entre terminales y órbitas; órbitas son el **régimen mayoritario** (141/200 en WARMUP, 136/200 en caso09 natural; 3/200 en N=32) |
| **corte temporal de W** | cuándo W deja de ser la misma | ya declarado artefacto: DEFS §1, *"el carácter piecewise es un artefacto del instrumento, no una propiedad del campo"*. `min_texts` = 3 en `ckm_monitor`, 5 en `monitor_service` |

Lo que queda después del trazado no es el límite: es el registro de haberlo
trazado. Los dos valores de `min_texts` conviven y siguen operando como si
fueran del campo.

---

## 11. Lo que falta en el código para contrastar §4

| término | estado |
|---|---|
| **k** | existe — `fabrication_index` y `n_rejected_pairs` en cada panel |
| **d(σ)** | **no existe** — nadie perturba un σ y vuelve a relajar |

Corrección a una afirmación de esta sesión: Monitor **no** es ciego al
paisaje. `_count_attractors` explora muchos σ₀ y ve cuántas cuencas hay. Lo
que no tiene es la relación entre **su** estado y una frontera: **censo
global, ninguna distancia local.**

La operación que falta es chica y no requiere servicio nuevo: tomar
`sigma_relaxed`, voltear k nodos, relajar de nuevo con `relax_orbit` de
`landscape_engine`, y ver si cambia de órbita. Medible contra verdad de
terreno en los tres corpus N=20 ya enumerados (1136 / 573 / 170 órbitas
reales).

No se ejecutó.

---

## Lo que este REG no establece

- **No cierra la pregunta de v1.** La reformula: de "cuándo un sistema está
  lo bastante fuera" a "cuándo una perturbación tiene escala suficiente", y
  después declara que ambos términos viven en potencial.
- **No decide la escala de `D_masa_cuencas`** — lineal o log sigue abierta
  (v5, `TASK_neff_y_frontera_logica_v1`).
- **No mide d(σ)**. La operación está descrita, no ejecutada.
- **No implementa `D_ckm_coco − D_ckm_monitor`**, y §9 da una razón para no
  esperar que implementarlo produzca el régimen 3.
- **No resuelve la dueñez** de nada. §9 cambia el marco en que esa pregunta
  se formula; no la responde.
- **No cierra la tensión "COCO no opcional"** (DEFS §12). La vincula.

---

## Abierto

- Si el régimen 3 se puede condicionar pero no producir.
- Órbitas de período 2 en `d(σ)`: qué es "cambiar de órbita" cuando el
  estado devuelto es una fase.
- Qué escala `k` le corresponde a un device real.
- Si `fabrication_index` —declarado contra sostenido— es régimen 3 en
  miniatura o sigue siendo régimen 2 porque los dos lados salen del mismo
  vocabulario. Inclinación registrada: lo segundo. No verificado.
- Si H de v1 es H₂ de Rényi (§2) o es otra cosa.

---

## Procedencia

Tres formulaciones de este REG son de delamor y fueron traídas en sesión como
**creencias revocables, personales, explícitamente fuera del marco del
proyecto**. Se citan como origen, no como afirmaciones del modelo:

- *"el dedo señalando es exactamente la cosa señalada"* — origen de §9 y §10.
- *"en el océano de los promedios no solo se ahogan los enanos"* — origen de
  §7d.
- los tres regímenes de §5.

Quedan como lo que son. No se convierten en criterios del proyecto por estar
acá.

---

## Archivos

- `registers/REG_hipotesis_distancia_contextual_v1.md` — hipótesis de origen
- `registers/REG_d_contextual_temporal_v1.md` — `D_contextual(t)`, §1
- `registers/REG_orbitas_conjuntos_invariantes_v1.md` — §3, §10, §11
- `docs/PROPUESTA_ckm_landscape_dynamics_v5.md` — `D_masa_cuencas`, N_eff, §2
- `docs/DEFS_CKM_estado_actual_v12.md` — §1, §2, §7, §8, §10, §11, §12
- `docs/tasks/TASK_delta_compresiones_coco_v1.md` — D3, `7df4a72`
- `services/monitor_service.py` — §6, §9, §11
- `services/landscape_engine.py` — `relax_orbit`, instrumento de §11

---

## Estado

- Hipótesis: **abierta**
- §1 (D_contextual = D_ckm): **verificado** por lectura de documentos
- §2 (identidad con `D_masa_cuencas`): **propuesto**
- §3 (proxy por masas): **verificado**
- §4, §5, §8, §9, §10: **propuesto**
- §6 (dos fracasos de registro): **verificado**
- §11 (falta `d(σ)`): **verificado** por lectura de código

No cierra. Abre.

---

*Sep 2026 — repo local ckm, Windows/PowerShell — nada ejecutado*
