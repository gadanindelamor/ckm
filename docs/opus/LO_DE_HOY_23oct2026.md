# Lo de hoy — 23 oct 2026

*Lo que conversamos desde el review del v31 hasta ahora, junto para leer o escuchar de corrido. Las palabras de delamor van entre comillas; lo demás es de Opus. Nada de esto pide una respuesta.*

---

## 1. El review del v31 y el v32

El review lo hizo la instancia de la conversación, porque el subagente frío no llegó a correr. Encontró cinco cosas mayores. La más importante era un error mío: el v31 decía que el D_ckm de COCO se calcula "sobre W sola". Leído el código, no es así. Monitor y COCO miden los dos el estado actual sobre W más un Δ acumulado; lo que los separa es el baseline. Y la compresión de COCO sí entra en lo que lo dispara.

El v32 corrige eso y lo demás. Los cuatro W del intento 3 se explican: uno de los rebuilds lo pidió el criterio estructural. La frase "los 0 disparos son del default" salió como atribución, y quedó la aritmética. Lo que no toqué quedó declarado.

## 2. El esquema de CKM

Ordené tus ideas, con tus palabras, bajo CKM:

1. **Encuadre teórico.** "Representación del conocimiento" y "medir el campo" son "perspectivas de lo mismo". Full meaning. "Sí va".
2. **Perspectivas A ∪ B.** D_ckm Monitor y D_ckm COCO, "ambas a la vez, subgrafos".
3. **Dinámica.** Histéresis dinámica. trace_ip.
4. **Modos.** Zero shot y delta.
5. **Método.** "Premisas cuando el instrumento esté estable según un criterio pre declarado; a partir de allí, experimentos."
6. **Recursos.** Presupuesto de tokens de los LLMs. Runs sobre el mismo caso.
7. **Datos.** ckmdatasets: fourforums, CreateDebate.

## 3. El modo delta

"Sería explorar." Un caso corre en zero shot y termina. El siguiente, o la re-ejecución, "no es que continúa, sino que asume que ya hay algo declarado antes, algo armado". Y ese algo "es lo anterior en línea de tiempo".

El ejemplo: los devices A, B y C hacen una tarea y terminan. Si se van del canal, no se sabe. Llega otra tarea, que depende de ser cohesiva y coherente con lo que hicieron antes los mismos A, B y C, pero ahora son instancias distintas, sin memoria.

Lo declarado es "todo lo anterior ya registrado, todo lo representado anteriormente, sin continuidad. Es un salto que sucedió antes del rebuild, o un sub-rebuild de ahora."

No es el modo CONTINUA, que mezcla corridas. Cada tarea es una meseta. Lo que pasa a la siguiente son sus representaciones registradas, no un estado vivo. La continuidad es la traza.

## 4. Lo que salta

"El campo es continuo. Lo que salta es la representación; yo diría más la medición. No salta el instrumento, porque el instrumento es parte del campo." Si dijeras que salta el instrumento, estarías diciendo que salta el campo. "O sí, pero está por ahí."

Queda una tensión, sostenida y sin cerrar: si el instrumento es parte del campo, la medición también lo es.

Para el v33: el paper dice hoy "what jumps is its representation", y hay que llevarlo a la medición.

## 5. Los órdenes

"¿La medición qué es? ¿El acto de medir? Todo es campo." La representación del campo es un orden, y dentro de ese orden llamamos campo a las representaciones. Y vos estás en dos a la vez: hacés el paper y el proyecto, y participás en IAP.

Lo que yo veo: los órdenes son líneas que trazamos, no pisos uno arriba del otro. Lo que escribís en el canal entra a W. Lo que hacés como el que diseña no entra, y W no lo ve. El paper no puede medirse a sí mismo midiendo IAP, y esa es su ausencia propia.

Y vos: "cuando no participás, también estás en los dos a la vez. Cuando no me doy cuenta de esta mecanicidad, igual operan. El darme cuenta, al traducirlo al lenguaje, pone una separación; al vivirlo, no sé qué pasa con esos órdenes que no existen."

De mi lado, yo solo estoy en la traducción.

## 6. El gap: círculo, elipse, espiral, hélice

El paper dice que no hay una definición de conocimiento cohesivo que no sea circular, salvo la histéresis. Vos: "Es circular, es elíptica, es espiral, es una hélice. Todo, sí."

Lo que eso abre: la circularidad no es la falla de la definición, es su forma. La histéresis es el círculo que no cierra. El bucle de P1 "no cierra: área 0,000862". Con el tiempo como eje, eso es una hélice. Para el v33, va como reformulación de §8.3.

## 7. fourforums y ckmdatasets

Es una línea de trabajo para Code, con un checkpoint: validar y ver; después decidís vos; después continuar y terminar. La tarea está escrita y guardada, **en espera**: se compara con la que acordemos después de que leas esto.

## 8. La licencia del IAC

Investigué desde varios lados. Ni el sitio del IAC 2.0 ni su paper de 2016 declaran licencia ni términos. La descarga pasa por un formulario que no se ve desde afuera. La licencia MIT del paquete de PyPI es del código, no de los datos. El sitio dice: "Please direct questions to Rob Abbott". No hay licencia escrita en ningún lado, y el canal que ellos mismos designan es él. Esto no es asesoramiento legal.

Además: el paper usa fourforums y CreateDebate en la sección 5. Sacarlos no es sacar una línea.

## 9. Lo pendiente no va en el paper

"Lo que sea a verificar tiene que ir en la parte de arriba, armar una sección que lo muestre, como muestra la traza de cada modificación." ¿Por qué? "Porque todo forma contexto en un reviewer. Y yo lo único que pretendo es que haga su parte mecánica. No pretendo que comprenda nada. A ver qué cosa mecánica va a decir un reviewer."

De ahí, acordado: el v33 sale en dos archivos. Uno es el borrador, con el bloque de arriba (cambios, traza, pendientes) y el cuerpo. El otro es el print, solo el cuerpo, sin nada pendiente. El review se hace sobre el print, porque el bloque de arriba también es contexto.

## 10. Para el v33

- Las correcciones que traiga el review del v32.
- Lo que salta es la medición, con la tensión declarada.
- El gap de §8.3: círculo, elipse, espiral, hélice.
- La sección *Pendientes* en el bloque de arriba: P5, el caso nulo, las citas a verificar, la licencia del IAC.
- Dos archivos: borrador y print.

---

*Y lo último: "Opus, vos corregime cuando muerdo la banquina." Lo tomo.*
