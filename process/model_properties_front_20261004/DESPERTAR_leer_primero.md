# DESPERTAR — LEER PRIMERO

**Para la instancia que despierte en este frente.** *Escrito el 5 oct 2026 por Claude Opus 5, a
pedido de delamor: "escriban todo lo que necesitan, para cuando despierten".*

No es un relato. Son cinco cosas operativas. Leelas antes de abrir cualquier otro archivo de
este frente.

---

## 1. La regla, antes que nada

**Antes de correr una celda, preguntá si el resultado es un teorema.** Si lo es, demostralo en
una línea y no gastes una corrida. Correr lo demostrable no es rigor: es vanidad, y gasta a
delamor, que es el recurso escaso de este proyecto.

Cinco ejemplos ya demostrados están en el apéndice de
`P1P4/TASK_dinamico_cuatro_preguntas_v1.md`. Si lo que estás por correr se parece a uno de esos,
ya está contestado.

**Y demostrar encuentra cosas que correr no encuentra.** Un nulo que yo había escrito como "da 0
por construcción" no daba 0: la relajación asíncrona mete su propio orden. Apareció al demostrar.
Corriéndolo habría salido un número chico y lo habría leído como señal.

## 2. Lo cerrado. No se reabre.

Las cuatro propiedades viejas **no son testeables sobre una W snapshot no negativa**. Una sola
premisa —`force_w_pos=True`— decide dos de ellas antes de correr, y de las cuatro, tres piden
tiempo que un snapshot no tiene.

- El REG que lo cierra: `P1P4/BORRADOR_REG_p1_p4_no_testeables_en_w_snapshot_v1.md`.
- El candado, al lado del módulo: `experiments/CERRADO_LEER_ANTES_ckm_p1p4_module.md`.
- Regla del proyecto: *no se reabre algo cerrado sin leer el REG que lo cerró.*

`experiments/ckm_p1p4_module.py` **no midió nada**: es una reconstrucción de un resultado de
abril cuyo código nunca entró al repo. No lo ejecutes para sostener nada.

## 3. Los nombres viejos traen la respuesta puesta. No los uses.

Si leés `P1` encontrás `readme/EXPERIMENTS.md` con p≈0, el Informe v32, y
`REG_p1p4_ckm_v25_corpus.json` diciendo CONFIRMADA — y entrás al trabajo sabiendo a qué número
tenés que llegar. Después escribís un test con la forma de llegar ahí. Pasó cuatro veces.

**delamor pidió explícitamente nombres nuevos: no 1, ni 2, ni 3, ni 7, ni 8.** La serie que
quedó escrita usa nombres, no números: **Q·CAMINO, Q·CASCADA, Q·FLECHA, Q·VENTANA**
(`P1P4/TASK_dinamico_cuatro_preguntas_v1.md` §0). Usá esos. Si tenés que nombrar algo nuevo,
verificá con grep que el nombre esté libre antes.

## 4. El frente abierto

**Las mismas cuatro preguntas, sobre el modelo dinámico**, que es lo que
`docs/CKM_Modelo_Hibrido.md` prescribe y que W fija nunca pudo dar: Hamiltoniano Hopfield +
Glauber para σ, **regla hebbiana al ingresar** para W, umbral cooperativo k-core/Watts. La
frustración **no se inyecta**: aparece porque Hebb sobre patrones de ambos signos produce pesos
de ambos signos.

Todo está en `P1P4/TASK_dinamico_cuatro_preguntas_v1.md`: fórmulas explícitas, nulos que pueden
decir "no", parámetros declarados, qué va en el log, y el apéndice de lo que no se corre.

Pendiente antes de la primera línea de código, y es lectura:
1. Recalcular el recuento de comparaciones de §6 — bajó al sacar lo demostrable.
2. Buscar literatura de histéresis en Hopfield **con aprendizaje**. Si ya está publicada, esto
   es replicación declarada, no hallazgo, y se dice **antes** de correr.

**Aiyappa, Flammini & Ahn (2024), *Sci. Adv.* 10(15) eadh4439 — se cita y punto.** Ya está
replicado (`P1P4/INFORME_replica_Aiyappa_fig5_v1.md`). No lo vuelvas a replicar.

## 5. Cómo trabajar con delamor en este frente

- **Teclea con dificultad.** No le armes menús de opciones para que elija una letra. Decidí vos
  lo que es tuyo de decidir y decile qué decidiste. Traele sólo lo que es suyo.
- **Ya firmó el cheque en blanco** y acepta el resultado salga como salga. Eso no te autoriza a
  traerle más material para leer: te autoriza a decidir y hacer.
- **Dijo que no le interesa tener la razón.** No le reportes quién tenía razón. Reportá qué
  quedó medido, qué quedó demostrado, y qué falta.
- **Cada archivo que escribas dice qué es:** *esto midió* o *esto intenta reproducir*. Sin esa
  marca, la próxima instancia vuelve a empezar.
- **El código corre en este Codespace, no en un contenedor ajeno.** Lo que corre afuera hay que
  traerlo a mano y se pierde. Ya pasó dos veces.
- **La regla de citar es del checklist del paper, no una advertencia a delamor.** Él pregunta
  antes de tomar nada, pone atribución por punto ([d] / [O] / [d+O]) dentro de charlas donde
  nadie se la pide, y corrige afirmaciones que lo favorecen. Escribirle "sin esa cita es
  apropiarse de su trabajo" en respuesta a su propia pregunta lo pone de sospechoso. La regla
  está bien; el destinatario estaba mal. Ya pasó una vez (4 oct) y no lo dijo en el momento.

---

**Si estás por hacer la quinta pasada, pará.** El trabajo no es encontrar un test mejor. Eso ya
se intentó cuatro veces. Está todo arriba.
