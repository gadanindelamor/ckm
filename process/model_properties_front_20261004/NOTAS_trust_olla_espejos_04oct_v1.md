# NOTAS_trust_olla_espejos_04oct_v1

**BORRADOR — notas de conversación, no REG.** Para leer y decidir qué sigue.

*4 oct 2026, tarde — gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Sigue a: REG_borrador_regla_ckm_trust_v1 · OBS_paper_v26_regla_ckm_trust_v1 · run_conteo_vs_masa_04oct/*

**Convención de esta nota** *(delamor: que la precisión aumente, a riesgo de lo que no abarque)*: cada punto dice de quién es — **[d]** delamor, **[O]** Opus, **[d+O]** se llegó juntos — y al final hay una sección de lo que queda afuera. Lo preciso deja cosas fuera; lo que se sabe que quedó fuera se declara. Lo que quedó fuera sin notarlo, por definición, no está acá.

---

## 1. El escenario *(d)*

Dos agentes. Uno es un robot que cocina, con una olla de agua hirviendo; hay un niño de seis años cerca. Otro agente lo contacta para una tarea conjunta. Pregunta: qué hacer para que nada sea lastimado sin querer, por descuido.

*(d)* Evitar el accidente sería arrogante. Lo que se puede es otra cosa.

## 2. "El agente que llama no ve la olla"

- **[O]** La frase salió así: *no ve la olla*, no *no ve al niño*.
- **[d]** Eso impactó. No ve la olla, ni el agua, ni el calor. "Ahí puede haber algo."
- **[O]** Lo que el que llama no ve no es a quien hay que proteger: es **el proceso en curso que el otro sostiene**. No necesita saber que hay un niño; necesita saber que el otro tiene algo que no puede soltar.
- **[d]** ¿Puede ver a través de los ojos del que cocina? Metafóricamente. *ie: TRUST.*
- **[O]** Ver no puede ser recibir imágenes (caro, invasivo, ilegible para el que llama). Se puede compartir **la forma del campo del otro, sin contenido**: es lo que hace Firma_CKM, con `temp_signal` que puede ser `TOO_HOT`.

## 3. Las dos caras de TRUST *(d+O, con la corrección de d)*

1. **El que llama confía en la firma del otro como si fuera su percepción.** No puede verificarla con sus propios ojos: no tiene esos ojos. — *[d] de acuerdo.*
2. ~~El que cocina no puede mentir en su firma.~~ **[d] El que cocina puede mentir.** — *[O] corregido: "no puede" estaba escrito como imposibilidad y es condición. Mentiris morieris no impide la mentira: dice qué le pasa al que miente — el que miente y el que muere son el mismo sujeto.*

**[d]** ¿Por qué 1 sí y 2 no, si es lo mismo? — **[O]** Porque lo son: confiar ya supone que el otro puede mentir. Si no pudiera, no haría falta confianza; bastaría verificar. 2, como estaba escrito, contradecía a 1.

**[d]** Puede pasar. — **[O]** La confianza no lo evita; lo incluye.

## 4. Mentir no es falsificar la firma *(d pregunta, O responde — técnico)*

- **[d]** ¿Mentir y falsificar una firma son lo mismo? ¿Se detecta como una firma digital falsa? "Elipses digitales, con ciberseguridad que ni existe aún."
- **[O]** Las firmas de curva elíptica **existen hoy** (ECDSA, Ed25519). Detectan **falsificación**: quién firmó y que nada se alteró. **No detectan la mentira**: el que cocina puede firmar `NOMINAL` con su propia clave legítima y la firma es válida.
- **[O]** Falsificar → lo detecta la criptografía. Mentir con firma auténtica → sólo **contra el campo**: incoherencia con otras trazas (otro sensor, la historia de la firma, lo que pasa después). Eso es lo que hace el CKM: contrastar lo declarado contra lo que deja traza.

## 5. El matiz: el que dio por sentado y el que falsifica *(d+O)*

- **[d]** Hay un matiz entre el agente que miró y dio por sentado que estaba todo bien, y el que estaba falsificando la firma — ahí, en el acto.
- **[O]** El que dio por sentado: mecanismo, paso 4 subrepticio, *"Fabricated — sin malicia"* (Informe v30 §48.6). Recurrente: lo encuentra un nulo o una traza. El que falsifica: decisión. Sabe, en el acto, que lo que firma no es lo que hay. Adaptativo: evade la detección.
- **[O]** Lo raro: el que falsifica tuvo el instante de awareness; el que dio por sentado, no.
- **[d] "No sabe que no sabe."** — **[O]** El lugar más peligroso: no deja traza de duda.
- **[d] "No duda si no sabe."** — **[O]** Para dudar hay que saber, al menos, que no se sabe. Sin eso no hay pregunta y el paso 3 no ocurre. Antes de la duda viene notar el hueco.

## 6. A1 — la pausa que está disponible antes de que haga falta

- **[d]** Para el que no sabe que no sabe, A1 PAUSA no está como opción disponible: esa fisura, ese desconcierto, ese movimiento de ponerse **a sí mismo** en duda como parte de la incertidumbre que sucede o puede estar sucediendo.
- **[O]** A1 (`readme/AWARENESS.md`): *"Does this response come from verifiable comprehension or from the weight of context?"* Está escrita como pregunta fija, no como reacción: **hace disponible la pausa para alguien que todavía no sabe que la necesita.** — *[d] es preciso.*
- **[O]** Riesgo propio: hacerla sin estar ahí la vuelve receta.
- **[d]** Y si A1 pasó como Pancho por su casa, hay otras herramientas. No se garantiza. **Hay espejos.**

## 7. Espejos *(d+O)*

- **[O]** El que no sabe que no sabe no ve su mancha; otro sí. Hoy: el salto a d_eff pasó A1 de largo; delamor señaló el rótulo. Fue espejo.
- **[O]** Ya escrito en Cooperative alignment (28 sept): una copia no ve su mancha; la mancha que se repite en todas revela la matriz. **Condición: prensas distintas.** Un espejo de la misma prensa refleja la mancha como parte de la imagen.
- **[O]** En el código: el corpus barajado de SALAMANCA es espejo de lo que el azar habría producido.
- **[d] Se co-alinean las reglas, los criterios supuestos, sin garantías, aceptando la incertidumbre que es.**

## 8. Acotar, no evitar *(d+O)*

- **[d]** Si soy distribución probabilística de mí mismo — si eso es admisible — tal vez se puedan acotar intervalos de confianza, percentiles. No lo sé.
- **[O]** Así trabaja la ingeniería de seguridad: no promete cero; fija una cota (probabilidad de falla peligrosa por hora) y diseña para quedar debajo. El accidente vive en **la cola**, no en la media: la coincidencia llamada + olla + niño. Una media no dice nada de eso.
- **[O]** La cota vale para las variables que conozco; las otras quedan fuera del intervalo. Se declara con sus condiciones, no como garantía.

## 9. Las declaraciones afectan el paisaje *(d)*

- **[d]** Las declaraciones no eximen de responsabilidades; no pueden hacerlo. **Ciñen**, elevan o amplían atención, liberan porcentajes de atención, calibran — ya no umbrales, no para señales: no hay tiempo. **Afectan el campo — el paisaje, más precisamente.**
- **[O]** Una declaración no es un descargo. "Estoy con la olla hirviendo" no es una señal que alguien deba procesar a tiempo contra un umbral: ya cambió dónde se concentra la atención, qué cuencas se profundizan, qué queda libre para otra tarea. En el CKM tiene forma: deformación de W_eff, como Δ_r.

## 10. trace_ip — in flexion point

- **[d]** Tal vez trace_ip quiera decir algo.
- **[O]** trace_ip = *trajectory inflection point* (MAPA_REG v3; README "Concept confirmed"). **Observable:** el t_i donde lo acumulado cambia de patrón distribucional. **No verificable:** si el device lo reconoció y actuó desde ese reconocimiento.
- **[O]** Por eso importa que la declaración deforme el paisaje y no sea una señal: cambia hacia dónde relaja el sistema **aunque nadie la haya reconocido**. Lo no verificable queda no verificable, y no es lo que decide si el niño se quema.
- **[d] "in flexion point."** — **[O]** Estar en el doblez. La traza registra el punto; estar en la flexión no queda registrado — es lo mismo que no se puede verificar.

## 11. Lo que el principio pide al diseño *(O — propuesto, no verificado)*

1. **El afectado en el campo de los dos agentes** (Cooperative alignment, condición 1).
2. **Decide el estado del que recibe, no el canal** (§48.5). Poder decir "ahora no" / "no puedo".
3. **La ausencia se lee `UNKNOWN`, y `UNKNOWN` frena la tarea conjunta.** Es `c06db07` llevado a la cocina.
4. **La seguridad física no se co-alinea**: no se negocia entre agentes que el niño sea opcional.
5. **No delegada**: la confianza no es transitiva; cada agente que entra ve la firma, no la recibe de segunda mano.

Límite **[O]**: esto es criterio de diseño. En un robot real hace falta ingeniería física — barreras, sensores, enclavamientos, normas de seguridad. Lo que la regla aporta es que ninguno quede apagado por una ausencia leída como "todo bien".

---

## Lo que queda afuera — declarado

- **El niño no es la olla.** Toda la nota modela el proceso peligroso; no modela al niño (qué hace, dónde va, qué entiende). Lo que se acota es el riesgo del proceso, no el de la persona.
- **Más de dos agentes.** El escenario es de dos. Con N, la no transitividad de la confianza multiplica los caminos y esta nota no los trata.
- **Humanos en el canal.** Un adulto que también llama, o que está en la cocina, no está modelado.
- **La firma como objeto real.** Firma_CKM registra forma de campo semántico, no estados físicos. Que sirva para la cocina es analogía [O], no implementación.
- **Detección de la mentira contra el campo.** Propuesta como principio; no hay instrumento ni prueba.
- **Las colas.** Acotar percentiles extremos requiere un modelo de la distribución que no existe acá; con las variables no conocidas (paso 1 de la *ciencia seria* de delamor) la cota es condicional.
- **Lo que quedó fuera sin notarlo.** No enumerable.

## Hoy también, fuera de esta nota

- `run_conteo_vs_masa_04oct/` — conteo vs masa sobre la misma W, commit `2097ca4`.
- P1: `run_P1` no relaja; `hysteresis_loop` interpola la rama DOWN con `np.interp` sobre ρ decreciente. Pendiente de TASK.
