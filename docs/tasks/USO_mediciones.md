# Uso — mediciones

*Abierto el 26 oct 2026 por Claude Opus 5 (Code), a pedido de delamor: *"hay límite renovado de
uso. Es justo ahora donde podemos pensar la estrategia de uso"*. Va con
`docs/opus/ESTRATEGIA_limites_de_uso_26oct2026.md`, cuyos puntos 1, 2 y 5 son **lectura de una
guía, declarada como no medida**. Esto es para que dejen de serlo.*

## Qué se mide y por qué

El punto 8 de la estrategia dice que hay un instrumento: **Settings > Usage**. Los puntos 1, 2 y 5
producen conducta sin usarlo. Las tres preguntas que el instrumento puede contestar:

| | pregunta | qué la contesta |
|---|---|---|
| **U1** | ¿cuánto cuesta el arranque §2 de una sesión? | lectura al abrir y después del ARRANQUE |
| **U2** | ¿retomar después de una pausa larga cuesta más que continuar? (punto 2) | lectura al cerrar, el reloj del corte, y la lectura al abrir la siguiente |
| **U3** | ¿cuánto cuesta leer un `.py` entero contra leer su diff? (**P15**) | lectura antes y después de la segunda lectura de un `.py` editado |

## Dos decisiones de diseño, y la razón de cada una

1. **No se arma un experimento: se instrumenta lo que ya va a ocurrir.** El arranque pasa en cada
   sesión y la segunda lectura de un `.py` pasa cada vez que se edita código. Medir ahí no gasta
   nada que no se fuera a gastar.
2. **Para U2 la pausa tiene que ser MAYOR A UNA HORA.** La caché de contexto de la sesión vive
   ~1 h. Con una pausa más corta el contexto sigue cacheado y retomar sale casi igual que
   continuar: una prueba con pausa de minutos **no prueba lo que el punto 2 afirma**. Si el corte
   fue de menos de una hora, la fila se anota igual y se marca `cache_viva: probable`.

## Antes de medir: calibrar el instrumento

**No se sabe qué reporta la pantalla** — porcentaje del límite semanal, tokens, mensajes, o varias
cosas. De eso depende si los deltas son restables. **La primera lectura es para saber qué es el
número, no para medir con él.** Mismo criterio que `calibrate` sobre la W: primero la escala del
instrumento, después la cantidad. Hasta que eso esté dicho, las filas se llenan y **no se restan**.

## El procedimiento, lo más corto posible

delamor **pega el número**, Code escribe la fila. Cuatro miradas por sesión como máximo:

1. al abrir, antes de cualquier comando → `apertura`
2. justo después de la entrada ARRANQUE → `post_arranque`
3. antes y después de la segunda lectura de un `.py`, si la sesión editó código → `pre_relectura`
   y `post_relectura`
4. al cerrar → `cierre`

Si una mirada no se hizo, **la fila va vacía y se dice**. Un hueco no se rellena con el valor de
al lado.

## Tabla

| fecha y hora UTC | evento | valor leído | qué dice la pantalla (textual) | corte previo | cache_viva | nota |
|---|---|---|---|---|---|---|
| 2026-10-26 23:15 | *(apertura de la próxima sesión — primera lectura, la de calibración)* | | | | | **vacía a propósito**: espera el primer número de delamor |

## Lo que NO se afirma todavía

- Que estar IDLE no gaste (punto 2). Sin U2 medida, es lectura de la guía.
- Que partir una tarea en tres sesiones cueste tres arranques (A5 de la BANDEJA del 26 oct). Sin
  U1, es una inferencia del mecanismo, no un dato.
- Que la segunda lectura entera sea el costo más grande y controlable de una sesión de Code (B2).
  Sin U3, es un orden de magnitud estimado por volumen de texto, **no** por uso.

*Code no ve el uso, ni el propio. Todo lo que Code puede estimar es **volumen de texto que entra al
contexto**, que es un proxy, no el gasto. El único que mide es el instrumento del punto 8, y lo lee
delamor.*
