# PROPUESTA_estructura_modelo_formal_paper_v27

*5 oct 2026 — pedido de delamor; redacta Claude Opus 5.5 (Cowork). Es un BORRADOR: el paper sigue en DRAFT hasta la revisión final de delamor.*
*Parte de `PAPER_Landscape_Driven_Device_v26.md`. El estado de cada predicción sale de `verificacion_p1_p4_04oct/INFORME_verificacion_P1_P4_v2.md` (con su addendum).*

---

## El pedido (delamor, textual)

> Que en el PAPER, en el modelo formal, se separe:
> **Modelo estático híbrido** → P1–P4. **Extensión adversarial** → P5, P6, P7.
> **Modelo dinámico** → empieza en P11.
> **Modelo Landscape** → empieza en P111.

## Orden BABEL — v2 (5 oct)

*El nombre y el pedido son de delamor: trazar líneas que separen contextos de referencia. La v1 (P1 / P11 / P111) queda descartada: delamor ya no la quiere, y además la regla "P1k es la versión dinámica de Pk" pegaba el significado de una premisa a otra.*

**Reglas.**
1. **El identificador dice el modelo y el orden, y nada más.** Tiene la forma `<modelo><n>`. El número es el orden de formulación dentro de ese modelo: no codifica contenido ni linaje.
2. **Hay una línea por contexto de referencia:**

| prefijo | contexto |
|---|---|
| **E** | modelo estático híbrido |
| **EA** | extensión adversarial del estático |
| **D** | modelo dinámico |
| **L** | modelo Landscape |

3. **Una premisa no cruza modelos.** Si la misma idea (por ejemplo, la histéresis) se formula en dos modelos, son dos premisas con dos identificadores, y ninguno remite al otro. E1 y D1 no "son lo mismo en otro modelo": son entradas distintas de órdenes distintos.
4. **En el texto se cita el identificador, no la palabra.** "E1", no "la histéresis". El enunciado vive una sola vez, en la tabla del modelo.
5. **Una premisa falsada conserva su identificador** y se marca. El identificador no se reutiliza.
6. **El orden se fija por la primera vez que la premisa aparece registrada en la traza.** Cuando no se encuentra esa fecha, se declara.

**Correspondencia con la v26.** La numeración vieja se conserva solo para trazabilidad, porque README, THEORY y los REG usan P1–P7:

| v26 | Orden BABEL |
|---|---|
| P1–P4 | E1–E4 |
| P5, P6, P7 | EA1, EA2, EA3 |
| H_STOP (falsada) | D1 |
| "STOP no produce pérdida" | D2 |
| β_collective emergente | D3 |
| P1–P7 bajo W dinámica (§8.5 de la v26) | sin identificador hasta que se formulen como premisas propias de D |

### El Orden BABEL del Modelo Landscape — PROPUESTO (5 oct)

*delamor: "el ORDEN BABEL del Modelo Landscape es la conjunción, las perspectivas de los 2 modelos anteriores". Estado: **propuesto**.*

El Landscape no es un tercer modelo con su propia lista: es donde se miran juntos el estático (E) y el dinámico (D). Pasa lo mismo que en R13 (THEORY): G[A∪B] ≠ G[A] ∪ G[B]. La conjunción no es la suma; aparece algo que no estaba en ninguna de las dos.

**Notación propuesta:**
- `L(E)<n>` — el paisaje visto desde el estático, con una W fija.
- `L(D)<n>` — el paisaje visto desde el dinámico, mientras W se construye y crece.
- `L(E∧D)<n>` — lo que existe solo en la conjunción. Es el Landscape en sentido estricto.

**Cómo queda la tabla L1–L4 de abajo, reubicada (propuesto):**
- L2 (período 2) y L3 (N_eff) → `L(E)`: geometría de una sola W.
- L4 (saturación por unidad de texto) → `L(D)`: depende de cómo se construye W.
- L1 (Néel) → sin ubicar. Barre β sobre una W fija, pero su uso es elegir pares para construir W_mixta. Lo decide delamor.
- Candidatos a `L(E∧D)`: la D_ckm canónica (compara N_eff entre versiones de W), d(σ) bajo Δ_r, y el lazo de histéresis cuando W se reconstruye. Ninguno está testeado como premisa.

La tabla siguiente queda como versión anterior, para la traza.

#### (versión anterior) Orden BABEL del Modelo Landscape como lista propia

Ordenado por la primera aparición en la traza que pude ver. Fuente: el repo de GitHub y NOTAS_proxima_sesion_paper_v12.

| | premisa | primera traza | estado |
|---|---|---|---|
| **L1** | La temperatura de Néel efectiva separa las subredes T0/T1 sin sesgo editorial | ago 2026, DEFS v3 §12 (vía NOTAS v12) | propuesta, no verificada |
| **L2** | La prevalencia de órbitas de período 2 depende del corpus, no de la dinámica síncrona | 8 sep 2026, REG_orbitas_conjuntos_invariantes_v1 §2 | verificada como medición (141/200 y 136/200 contra 3/200) |
| **L3** | N_eff sobre masas de cuenca converge; el conteo de órbitas no | 8 sep 2026, REG_orbitas §10 | verificada contra enumeración exacta de 2²⁰ estados |
| **L4** | La saturación de pares distintos, que depende de la unidad de texto, ordena el colapso del paisaje | 20 sep 2026, REG_unidad_texto_saturacion_v1 | verificada como medición; el criterio es propuesto |

Las condiciones del modelo Landscape no son premisas y van aparte, sin identificador L: la medida de referencia (§2.3), la exactitud de los empates (§4) y la definición canónica de D_ckm.

---

## Estructura propuesta del §4 (Formal Model) y del §5 (Validation)

### 4.A Modelo estático híbrido (E)

**El objeto.** Una W fija (un snapshot del corpus) junto con c(S), la relajación Hopfield, el k-core y la pre-activación BP. Es el modelo de abril: *El CKM como bootstrap bayesiano sobre un paisaje Hopfield* (`docs/CKM_Modelo_Hibrido.md`), que tiene que citarse acá como fuente formal.

**Lo que va en esta sección** (de la v26):
- §4.1 Knowledge Graph: la W simétrica; Δ queda para 4.A′.
- §4.2 Relaxation and Convergence (GOLES, LaSalle): la parte de la relajación sobre W fija.
- §4.4 Cohesion c(S).
- §4.5 Gatekeeper: modelo estático sobre capacidades MCP, como capa aplicada.
- La condición N (`CKM_experiments_correct_N.md`): N ≥ 30 para histéresis y cascadas, N ≥ 100 para rigor cuantitativo, y la transición híbrida de k-core solo con k ≥ 3.

| | Predicción | Estado (informe v2, 4–5 oct) |
|---|---|---|
| **E1** | Histéresis: incorporar ≠ remover | **Verificada como propiedad del modelo**, con relajación. Supera al nulo de fuerza en W_viejo (20 de 20 seeds); en W_nuevo es moderada. El test de abril (`run_P1`, sin relajación) se retira. |
| **E2** | Cascadas P(s) ∝ s^-τ | **No medible** con N = 32 y k = 2. Por la condición N hacen falta k ≥ 3 y N de 50 a 100 o más. |
| **E3** | Asimetría temporal | **No testeada.** La forma k-core estática es reversible por matemática. Falta una versión con dinámica. |
| **E4** | Densidad óptima interior Ω* | **No medible** con el protocolo de abril: con subconjuntos al azar, Ω* interior equivale a media(W) < 0. Hace falta un protocolo con relajación y un nulo de ubicación de los pares negativos. |

### 4.A′ Extensión adversarial (EA)

**El objeto.** W_mixta (W_pos más los pares negativos del ruteo por marcadores), Δ direccional y los corpus diseñados con tensión (fourforums, CreateDebate).

**Lo que va en esta sección:** la parte de Δ en §4.1, la condición del ruteo de §5.1 ("no null outcome") y **SALAMANCA como precondición de admisión** (un criterio que puede devolver vacío; modularidad no es adversarialidad).

| | Predicción | Estado |
|---|---|---|
| **EA1** | Colapso de diversidad en corpus adversarial | Sin revisar en esta verificación. Pendiente ya registrado: ninguna W_mixta se verificó contra nulo. |
| **EA2** | Δ rompe la simetría de los estados ambiguos | Sin revisar. Ojo: en fourforums los nodos son **autores** (W relacional), no términos. |
| **EA3** | Nodo tipo 965 | Sin revisar. Confirmada en dos corpus según la v26; la universalidad queda abierta. |

### 4.B Modelo dinámico (D)

**El objeto.** W se reconstruye mientras el corpus crece.

**Lo que va en esta sección:**
- CorpusService y NodeExtractor, con la regla de desempate (REG_seleccion_nodos_desempate_v1).
- WVersionManager.
- Δ_r como metabolización (§4.7).
- MonitorService.
- COCO y OPERADOR_STOP_COCO (§4.6).
- Firma_CKM.
- El ciclo de vida de CKMlandscapeConfig.
- La serie IAP (§6), que es una serie viva, irreproducible, con casos no comparables.
- trace_ip.

**Premisas del modelo dinámico.** Salen de la traza; delamor decide cuáles entran:
- P1–P7 bajo W dinámica (§8.5 de la v26): sin identificador hasta que se formulen como premisas de D.
- **D1, H_STOP: falsada.** La monotonía de D_ckm bajo STOP no se cumple; se reformula como f(A_pre).
- **D2, OPERADOR_STOP_COCO no produce pérdida.** El README da pérdida ≤ 0 y fracción recuperada ≥ 1. Está verificada en drivers y tests, nunca en el canal vivo.
- **D3, β_collective emerge como mediana de los β individuales.** Está implementada como observación; no regula.

### 4.C Modelo Landscape (L)

**El objeto.** La geometría del paisaje de atractores de una versión de W. Cantidades que **convergen**, con medida de referencia declarada.

**Lo que va en esta sección:**
- §4.3 Basin Masses and N_eff.
- Las tres cantidades: L, L/~ y terminales.
- La medida de referencia: uniforme = volumen de cuenca. La banda de 30 a 70% de nodos activos es una tercera referencia.
- La condición de exactitud: los empates son exactos si y solo si los pesos son diádicos.
- D_ckm, con el nombre conservado y la cantidad canónica 1 − ln N_eff / ln N_eff0, decidida el 4 oct.
- d(σ), la distancia a la frontera de cuenca.
- Los criterios de W sola: frustración, peso negativo relativo, espectro.
- La coercitividad de frontera (SALAMANCA).
- Néel.
- La unidad de texto y la saturación.

Todo esto ya está especificado en `CRITERIOS_diversidad_formulacion_v1.md`.

**Premisas del modelo Landscape:** L1–L4, en la tabla del Orden BABEL de más arriba.
---

## Lo que cambia en el resto del paper (lista, sin redactar)

- **Abstract y §1:** dejar de decir "P1–P6 verified"; describir los tres modelos.
- **§5.2, §8.1 (tabla) y README/THEORY:** pasar al estado de la tabla de arriba.
- **§2.3:** citar el Modelo Híbrido como fuente formal del modelo estático. Aiyappa queda como antecedente del modelo estático; su modelo no afirma histéresis (replicación de su Fig. 5, 4 oct: se sostiene).
- **§7.2–7.3:** quedan como discusión transversal a los tres modelos.
- **Encuadre (`CKM_encuadre_representacion_conocimiento_v1.md`), §3.1, §3.4 y §4.1:** se apoyan en los tests de abril de P1, P3 y P4. Hay que reformularlos o marcarlos como pendientes.

## Lo que decide delamor

*Respuesta de delamor (6 oct), aplicada en `PAPER_Landscape_Driven_Device_v27.md` §4 (copia previa: `..._v27_antes_definiciones.md`):*

0. **Cada modelo debe definirse, identificando sus diferencias.** → Se aplicó: hay una tabla de diferencias al comienzo del §4 y una definición en la cabecera de 4.1 y de 4.3. Las de 4.2 y 4.4 quedan pendientes.
1. **Modelo estático híbrido:** su dominio son las declaraciones de capacidades de los devices. El corpus no varía; solo se evalúan declaraciones.
2. **Modelo dinámico:** W cambia y se reconstruye; hay ciclos y componentes.

Sobre las preguntas:

1. **Gatekeeper → modelo estático (4.1)**, porque su dominio es la validación de declaraciones de capacidades. **Decidido**; la nota de pendiente se reemplazó.
2. Qué premisas entran en D y en L. Los identificadores los fija el Orden BABEL. **Criterio de delamor (6 oct) para D:** *"no todo lo que sucede es premisa"*: se eligen entre los selected findings (§6.4), o ninguna si es el caso. Queda anotado en §4.3.4. La elección sigue abierta. **L:** abierto.
3. **Serie IAP: es del modelo dinámico y queda como §6 aparte.** delamor: *"es una experiencia, no un experimento; lo que se evaluaba era el CANAL, el vivo"*. Aplicado en la cabecera del §6 y en 4.3.
4. Aplicar sobre la v26 para generar la v27. **Ya existe la v27** (5 oct): §4 en cuatro modelos, P1–P4 con su validación y las definiciones de 4.1 y 4.3.
