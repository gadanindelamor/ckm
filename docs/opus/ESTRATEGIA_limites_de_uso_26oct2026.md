# Estrategia para trabajar con los límites de uso — 26 oct 2026

Acordada con delamor (*"sí, de acuerdo"*). Fuente: `contexto_claude/Estrategias para  optimizar el uso de Opus.md` (guía de soporte de Anthropic), aplicada a TRUST / CKM.

1. **Sesiones cortas, una tarea cada una.** Cada paso vuelve a cargar toda la conversación, así que una conversación larga cuesta cada vez más. Una sesión arranca en el ESTADO, hace una cosa y cierra con el ESTADO.
2. **Retomar cuesta más que estar IDLE.** Según la guía, la caché vence con la inactividad, y el primer mensaje después de una pausa larga vuelve a cargar todo el contexto. Estar IDLE no gasta. Además, todas las superficies (claude.ai, Code, Desktop) descuentan del mismo límite. Esto es lectura de la guía, no está medido.
3. **Lo grande se lee una sola vez.** El paper, una vez por sesión. De la BANDEJA (más de 13.000 líneas) se lee solo lo nuevo desde el último commit, nunca entera. No se vuelcan salidas largas.
4. **Las preguntas se juntan.** Las de delamor, en un mensaje o archivo (como el OBS del 26 oct). Las de Opus, en una sola tanda.
5. **El esfuerzo según la tarea.** Registros, ESTADO y git, con menos esfuerzo o con un modelo más liviano. El paper y las verificaciones, con Opus y esfuerzo alto. Coincide con la regla de buscar primero alternativas baratas.
6. **Se apaga lo que no se usa.** Conectores y herramientas que no sirven en TRUST: Google Drive, Docs, navegador.
7. **Code trabaja de corrido.** Tareas autónomas, checkpoints en puntos fijos, la BANDEJA como único canal.
8. **Antes de algo pesado se mira el uso** en Settings > Usage. Si queda poco, se cierra con el ESTADO en vez de empezar.
