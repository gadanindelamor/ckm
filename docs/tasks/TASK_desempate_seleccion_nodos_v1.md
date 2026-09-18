# TASK_desempate_seleccion_nodos_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: `tests/test_node_extractor.py` §3 (xfail); REG_hipotesis_distancia_contextual_v4.*

---

## Hallazgo

La selección de nodos es "top_k por TF-IDF medio dentro del pool". Sobre 217 W de 15 corpus: **94 de 210** con más de 32 candidatos tienen empate en el borde del top-32, y en **85** qué nodos entran depende del orden de desempate — hoy `np.argsort` no estable, invertido, sobre el orden alfabético de sklearn. Un axioma que nadie eligió decide qué existe en ~4 de cada 10 W.

El empate es indecidible con el propio criterio: para "mayor TF-IDF", dos términos con igual puntaje son indistinguibles. Cualquier desempate viene de afuera del criterio *(delamor: ¿qué diría Gödel?)*.

## Regla (delamor)

**El mismo criterio que la relajación:** si h = 0, el nodo conserva su estado — la regla que garantiza convergencia (Lyapunov/LaSalle, DEFS §4).

- **Con selección anterior:** un término empatado en el borde **conserva su pertenencia**. El empate no mueve nada.
- **Bootstrap** (sin selección anterior): el estado inicial es "ningún nodo" → los empatados en el borde quedan afuera. N ≤ top_k.

Donde el dato no decide, decide la historia del sistema — histéresis (P1). *(delamor: se abre la posibilidad de volverse hacia las decisiones de la traza, no sólo a lo resuelto.)*

## Registro — continuo, no categórico

*(delamor: registro más elástico; no cierra. Opciones para acotar sesgos de eventualidad e incertidumbre deberían ser continuas e infinitas.)*

Cada selección guarda, para cada término cerca del borde:

- `score` — TF-IDF medio, valor exacto.
- `distancia_al_corte` — score − score del corte, **con signo**.
- `pertenencia_anterior` — si era nodo en la selección previa (o `None` en bootstrap).

**No guarda categorías** ("empate", "margen", "conservado"). Toda categoría se deriva después, con la tolerancia que se elija al leer, y puede re-derivarse con otra. El registro no decide qué es un empate.

La **regla** sí decide en el momento, y para eso usa una tolerancia (`atol` sobre la distancia al corte). Es tolerancia **de la regla**, declarada; el registro conserva el valor exacto para que la tolerancia misma sea revisable.

## Qué hacer

- `NodeExtractorService.accumulate(texts, seleccion_anterior=None)`: aplica la regla y devuelve además `registro_borde` (continuo, como arriba).
- `CorpusService._rebuild` pasa la selección anterior en cada rebuild y persiste el registro junto a la versión de W.
- El xfail de `test_node_extractor.py` §3 se reemplaza por tests de la regla: bootstrap excluye empatados; con historia, empatados conservan; fuera de empates, el dato manda.

## Verificación

- Suite de NodeExtractor + nuevos tests de la regla.
- Sobre los 217 W: cuántos cambian de selección respecto de hoy, y Jaccard entre selecciones sucesivas antes/después — cuánto del cambio de nodos entre rebuilds era el desempate reordenándose.
- **Completitud** (readme/CONVENTIONS.md): qué tests y docstrings deberían moverse con esto, y si ninguno se mueve, por qué.

## Qué no hace

- No elige la tolerancia desde el dato: se declara.
- No interpreta el registro. La lectura es ejercicio de equilibrio sobre el filo del sesgo, cada vez, con el registro a la vista.
- No cambia el pool por frecuencia ni el criterio TF-IDF.
