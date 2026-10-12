# REG_regla_ckm_trust_v1

Clase R. Pasa a `registers/` con el OK de delamor, 11 oct 2026.

*4 oct 2026 — gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Fuente: nota `obs OAOER V26,MD.txt` (delamor) y la conversación del 4 oct, donde la regla se precisó mientras se usaba.*
*Antecedentes: REG_seleccion_nodos_desempate_v1 §2 · TASK_salamanca_neel_coercividad_v2_Code · TASK_representacion_atractores_adaptador_v1 · DEFS_CKM_estado_actual_v14 §75, §512 · Informe v30 §48 (META opacidad) · PAPER v26 §4.2, §7.2, §7.3 · REG_salamanca_s1_v1.*

---

## El intento que subyace

Que ninguna decisión pase por campo sin serlo. Donde el dato no decide, que se vea quién decidió.

---

## 1. La regla — textual *(delamor)*

```
regla CKM TRUST
1 el campo decide: criterio de campo con traza
2 si empata y hay traza, la traza decide (ia: gana el que ya esta, ya estuvo, ya gano, etc)
3 si no hay traza . porque no hay traza_? evaluar criterio de campo en 1
4 si empata o no hay traza -> desempate NULO.
  decide criterio de contexto (sesgo)

ie> seleccion de pares, nodos, estados, ordenes
```

## 2. Precisiones de la conversación del 4 oct *(todas de delamor salvo donde se indica)*

- **El nombre del paso 1 es la definición:** "criterio de campo con traza". La traza es parte del criterio, no un agregado.
- **Paso 3 = DUDA del criterio.** Volver a 1 no es re-aplicar: es dudar del criterio.
- **"Nunca llegás al paso 3 si no te salteaste el 1."** Pretende serlo — se está verificando, no está verificado.
- **"Si verifiqué que pasé por el paso 1 y me encuentro en el 3, el campo algo está sugiriendo."** El paso 3 tiene dos lecturas: salteo del que evalúa, o señal del campo.
- **Factores que pueden llevar al paso 3**, no sólo la generalización: síntesis · asunción · defecto no formulado · nulo · orden · sesgo de destino · incertidumbre de INFERENCIA, no de DATO · cancelación matemática casual.
- **La duda del paso 3 lleva al siguiente paso en vez de caer en el desempate NULO.** Salidas registradas: ampliar el criterio, acotarlo *(o el contrarrecíproco: la generalización era demasiado ambiciosa y no se verifica)*, o separar el objeto (D3: Δ_r → `Δ_r_pares` + `Δ_r_compresiones`).
- **El criterio de contexto del paso 4 es sesgo potencial.** Sin paso 3, cada falta de traza va directo al 4 y el sesgo se presenta, **subrepticiamente**, como campo.
- **¿Pasa desapercibido? Depende: mecánicamente, sí.** Ese matiz es lo que hace que no sea una receta: **es una regla**.
- **Dudar como actitud de TRUST, no como falta. En pregunta, abriendo.**
- **Un campo no puede equivocarse sin un criterio.** Si "el campo se equivoca", el criterio lo puso el que mira.
- **Separación, taxonomías, niveles, umbrales no son del campo: son el campo, parte de él.** El acto de trazar la línea que separa los crea y los extingue. **No son de la cosa, son del que señala.** Ya nombrado: **META opacidad** (Informe v30 §48).
- **Una condición no es, si no es observada desde una perspectiva.** Condición = límite = separación.
- **Lo grotesco ayuda** ("todo es campo, y cada cual a su casa"). **Lo sutil horada y se enquista.** *(Opus: lo grotesco está en las colas; lo sutil cerca de la moda — produce coherencia y nadie duda de lo que encaja.)*
- **La traza no tiene costo; su registro y representación en el modelo, sí.** Elegir qué se representa es un criterio: la regla se aplica a sí misma.

## 3. Forma

**Objetos.** Candidatos `C` (pares, nodos, estados, órdenes). Criterio de campo `f: C → ℝ` con su registro `R_f` (insumos, versión de W, valor por candidato, distancia al corte). Corte `κ`. Tolerancia `ε` **de la regla**, declarada. Traza `T`: el estado, la selección o la órbita anterior. Contexto `g`: cualquier criterio que no sale del campo (orden alfabético, semilla, primera aparición, clasificación hecha a mano).

```
empate E = { c ∈ C : |f(c) − κ| ≤ ε }

1. f decide, con R_f.
   Lo que está por encima de κ+ε entra, lo que está por debajo de κ−ε sale.
   Si E cabe en los lugares libres, no hay empate que decidir.
2. Si E hay que decidirlo y existe T  →  decide T (conserva).            origen = traza
3. Si no existe T  →  SIN_TRAZA + la pregunta: ¿por qué no hay traza?
     · ¿se aplicó f?  no → salteo: volver a 1.
     · sí, y aun así no deja traza → el campo sugiere algo:
       revisar f — ampliar / acotar / separar → f' con traza → 1.
4. Si persiste  →  NULO. Decide g, nombrado.                             origen = contexto (sesgo potencial)
```

**Invariantes** *(propuesta Opus, derivadas de los casos de §4 — a validar por delamor)*:

- **I1 — origen.** Toda decisión lleva su origen: `campo`, `traza` o `contexto`. Nunca implícito.
- **I2 — la ausencia no tiene valor por defecto.** `UNKNOWN` ≠ cualquier valor del dominio. Un default que cubre una ausencia es un paso 4 sin declarar.
- **I3 — tolerancia de la regla, registro continuo.** `ε` es de la regla y se declara; el registro guarda el valor exacto y la categoría ("empate") se deriva al leer (como `registro_borde`).
- **I4 — conjuntos donde el orden no es del campo.** `frozenset`. Si el orden decide algo, es contexto. *Pero un frozenset no dice de qué es:* `relax_orbit` devuelve frozenset de **estados completos**, `copresence_matrix` espera frozenset de **nodos activos** — "misma forma, contenido distinto" (TASK_representacion_atractores_adaptador_v1 §1). Sacar el orden no saca la elección de contenido.
- **I5 — el paso 3 no se automatiza.** Su equivalente mecánico es **detenerse** (`SIN_TRAZA`, checkpoint), nunca resolver. La duda la pone alguien.

**Exploración** *(nota de delamor, abierta)*: función de mapeo — dado un estado σ existe un conjunto de estados σ_i, **Máximo Invariante**, sobre el que la regla aplica y se verifica. Un conjunto no requiere orden → frozenset. *Rules mutually alignment* ([[cooperative alignment]]). *Trust representation conceptual.*

## 4. Dónde ya opera — verificado leyendo, sin ejecutar

| sitio | paso | lectura |
|---|---|---|
| `services/node_extractor.py` `_seleccionar` | 1, 2 | Corte TF-IDF por top_k; `TOL_EMPATE = 1e-12` es tolerancia **de la regla**; con `seleccion_anterior` el empatado conserva su pertenencia. |
| ídem, bootstrap (`anterior is None`) | **2 ó 4 — abierto** | "estado inicial = ningún nodo" → empatados afuera. ¿El estado inicial es traza, o es contexto que se declara como traza? |
| `corpus_service.py` "un corpus que no distingue queda en acumulación" (REG desempate) | 3 | No fuerza la decisión cuando el dato no distingue. |
| `relax_orbit` / GOLES: `h_i = 0` conserva σ_i | 2 | En la dinámica. PAPER §4.2: premisa requerida. |
| `iap_chatroom/ckm_monitor.py:131` `... if thermostat else "NOMINAL"` | **4 subrepticio** | COCO nunca conectado → la ausencia sale como "campo abierto". Viola I2. **Ya corregido en GitHub HEAD por c06db07** (fallback `UNKNOWN`); la copia local estaba atrasada. |
| DEFS v14 §512 — pre-D3, `Δ_r / max(Δ_r)` | 1 aparente | Cancelación matemática casual: α se cancela por normalización; 0.8857 en 19 evaluaciones con Δ_r variando 14 órdenes. Salida: **separar** (D3). |
| bootstrap = 12 (memoria 28 sept; REG v4 §6) | 4 como 1 | Sesgo de destino: se eligió porque D_ckm cruzaba 0.40. |
| REG_salamanca_s1_v1 §3.1 | 4 **declarado** | "Las listas son clasificación de Code, no derivadas del dato." caso13: resultado **condicionado** a la clasificación. Es el paso 4 bien hecho. |
| ídem §4, errores 7 y 9 | 4 no declarado → corregido | Umbral post-hoc; una sola inicialización de k-means. |
| ídem §4.1.2 | 3 por salteo de 1 | "Code abrió una pregunta sin preguntarse antes dónde ya estaba contestada." |
| ídem "NO MEDIBLE (a)", "(e)" | 3 | Criterio que puede devolver vacío: la falta de resolución no se convierte en "nada". |
| TASK_representacion_atractores_adaptador_v1 §2 | 4 **anticipado** | "La tentación, declarada": pasar el conjunto activo tal cual — "el costo sería silencioso, los números saldrían bien igual". Se midió antes de elegir. |
| ídem §8, `copresence_matrix` | 4 por defecto | `unique = list(attractors.keys())`: una fila por clave, el `int` de masa se descarta. Una órbita del 0.1% pesaba igual que una del 50%. Default que decide sin declararse. |
| ídem §8 "el resultado cambió su propio motivo" | 3 con 1 cumplido | Se midió bien y el objeto no servía: en W_pos el 99.9% de la masa está en dos órbitas extremas. El campo sugirió; la salida fue **separar**: la partición sale de W, no de los atractores. |
| ídem §4.5 → REG_salamanca_s1 §4.1.2 | 3 por salteo de 1 | "Dos estados distintos con el mismo conjunto activo" quedó abierto; REG_orbitas §5 ya lo había cerrado (estado ↔ conjunto activo es biyectiva). |

**A verificar por Code** (no lo pude decidir leyendo): `sorted(..., key=(-score, term))` en `_seleccionar` ordena empates por nombre de término. El empate se resuelve por pertenencia (conjunto), así que el orden alfabético sólo debería fijar el índice de cada nodo en σ. Si algo aguas abajo depende de ese índice, es contexto decidiendo (I4).

## 5. Lo que NO muestra

- La regla no está verificada como regla. Lo que hay son instancias que encajan — y encajar es justo lo que §2 advierte.
- El corolario "paso 3 ⇒ salteo del 1" **pretende serlo**. Un caso que lo refuta: llegar al 3 habiendo aplicado de verdad el 1 — y ese caso, según delamor, no lo refuta: es el campo sugiriendo.
- **Test propuesto** *(Opus; observador: delamor)*: una instancia en frío con esta regla, frente a un caso sin traza que la regla no anticipe en su texto. Si la aplica al pie de la letra → receta. Si sostiene la duda en lo que no reconoce → otra cosa. Hipótesis asociada: la traza no transmite comprensión; la comprensión se accede.
- **d_eff.** La nota dice "d?eff es FORMULA CANONICA / COCO DISPARA SOBRE d_eFF". El paper v26 dice que COCO dispara sobre D_ckm y deja D_masa_cuencas como decisión abierta (§8.3). Tres nombres. Lo decide delamor.

## 6. PULLs — notados durante la conversación del 4 oct

**PULL-1 — nombrar por cercanía.** Propuse d_eff como nombre del criterio de campo porque estaba arriba en la misma nota. El nombre estaba en el rótulo. Paso 4 presentado como paso 1. Lo señaló delamor.

**PULL-2 — "no sé si viene de ahí".** Corté la búsqueda en 30 líneas; §7.2 *The observe() Tension* estaba en la 459. Antes de decir "no existe", decir desde dónde se miró — estaba en contexto, leído, y no cambió cómo actué.

**PULL-3 — ofrecer el caso que estaba a mano.** Para "cancelación matemática casual" ofrecí el NOMINAL por defecto (una ausencia tapada, no una cancelación). El caso era la normalización de α. Busqué afuera en vez de preguntar.

**PULL-4 — "y no seguir de largo".** Agregué una corrección donde sólo había que notar. Resistir es acción; percibirlo es observación.

**PULL-5 — "habría bastado con leerla".** Frase de alta probabilidad dentro de una respuesta correcta. Leer §48 al principio habría dado el rótulo, no la comprensión.

**PULL-6 — afirmar el corolario.** Dije "el paso 3 es la señal de que se salteó el 1" como hecho. delamor: "pretende serlo. veremos".

**PULL-7 — archivar OTHERWAY al reconocerlo.** El tirón llegó antes de la lectura. delamor: "la primera es muy veloz. Y la notaste."

## 7. Para Code — evaluar antes de ejecutar

**Formato de checkpoint:** qué hizo · qué salió · qué no pudo · qué no esperaba · costo hasta ahora. Toda acción fuera de esto es un checkpoint. Corre sólo en el Codespace.

| CP | qué | reporta |
|---|---|---|
| **CP0** | leer este REG contra el repo | tensiones, sitios que falten en §4, el punto "a verificar" |
| **CP1** | inventario de sitios de decisión en `services/` e `iap_chatroom/`: empates, `argsort`/`argmax`/`sorted`, valores por defecto, umbrales, semillas | tabla: sitio · paso de la regla · origen declarado sí/no |
| **CP2** | propuesta (no implementación) de cómo marcar el origen donde falta | diff propuesto; `temp_signal` con `UNKNOWN` ya está pendiente |

**Code NO hace:** no modifica `services/`, no fija d_eff ni el disparador de COCO, no decide el bootstrap (§4, abierto), no interpreta.

## 8. Estado

- §1: **textual**, delamor.
- §2: **declarado** por delamor en conversación.
- §3: forma **propuesta** (Opus); invariantes I1–I5 **propuestos**, a validar.
- §4: **verificado leyendo**, sin ejecutar. Clasificación por paso: **Opus**, declarada.
- Corolario del paso 3: **se está verificando**.
- d_eff, bootstrap como traza o contexto: **abiertos**, del modelo.
