# Residuo del `_state` del repo — 22 oct 2026

*Movido acá el 27 oct 2026 por Claude Opus 5 (Code), por **P13**, con la instrucción de delamor:
*"la línea suelta resolvelo ya Code. Coherente con los criterios del proyecto. no puedo evaluar el
impacto de ello."**

## Qué es

`channel_ticks.jsonl`, **dos líneas**, las dos del 22 oct 2026:

| tick | t | written_at_utc |
|---|---|---|
| 1 | 1792647558.650591 | 2026-10-22T05:39:18 |
| 0 | 1792648647.896816 | 2026-10-22T05:57:27 |

Los `tick` son 1 y 0 y los relojes están a 18 minutos: **son dos invocaciones distintas**, cada una
con su propio `ChatChannel`, no dos workers de una misma corrida.

## Por qué no se queda donde estaba

Estaba en `iap_chatroom/_state/`, que **es traza declarada**: el corpus de agosto, 8 de cuyos 12
textos son joins, que es la condición en la que corrió la serie congelada. Esas dos líneas **no son
de ningún vivo**: son residuo de una corrida de la suite. Un directorio declarado traza no puede
tener líneas que ningún vivo produjo.

## Por qué no se borra

Es el **testigo** de que el aislamiento se rompió una vez. Borrarlo dejaría el mecanismo intacto y
sin rastro, que es exactamente lo que el propio guardia del `conftest.py` dice de sí mismo:
*"**No se borra nada**: fallar es el punto. Borrar en silencio dejaría el mecanismo intacto y la
próxima vez aparecerían nombres distintos."*

## Qué se verificó antes de moverlo (27 oct)

1. **Los tres archivos trackeados de agosto están intactos.** `corpus_state.json` tiene 12 textos,
   los tres primeros son joins, y sus 6 versiones de W llevan timestamps de agosto
   (1785557005 → 1786584450). Su `mtime` es del 20 oct y **el contenido no cambió**: `git status`
   está limpio. Algo lo tocó sin cambiarlo; desde acá no se puede decir si fue un `save()` de
   contenido idéntico o una operación de git, y no se afirma.
2. **El archivo entero era residuo**: no existía en agosto y no estaba trackeado.
3. **La causa está cerrada, y se verificó así:**
   - el guardia del `conftest.py` existe desde el 20 oct (`cb4752f`), compara **nombre y tamaño** y
     falla nombrando el test;
   - `pytest --collect-only` (858 tests, sin correr ninguno) **no escribe**: el archivo quedó en
     300 bytes. Era la hipótesis de una escritura en tiempo de colección, **y quedó falsificada**;
   - las dos corridas completas del 27 oct (851 passed) dejaron el archivo **sin tocar**; con el
     guardia comparando tamaño, un append habría fallado.
4. **Lo que NO se pudo verificar:** la causa exacta del 22 oct. Ese día la BANDEJA registra la suite
   en paralelo (`-n 4`) con *"3 errores que en serie no salen"*. Reproducirlo pediría volver al
   código de ese día y escribir otra vez en la traza. **No se hizo, y la causa queda como no
   reproducida, no como explicada.**

## Lo que queda dicho, y es de delamor

La raíz estructural es que **el `state_dir` por default de `CKMMonitor` es el directorio declarado
traza** (`iap_chatroom/_state/`, F3a: *"Default: el de siempre, así que nada cambia para quien no lo
pase"*). Todo lo que se construyó después —las dos fixtures autouse del `conftest.py`, la
eliminación del `CKMMonitor()` a nivel de módulo— existe para proteger de ese único default. No se
tocó: cambiar un default que decidió delamor es **E1**.
