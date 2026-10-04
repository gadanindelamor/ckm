# SUPERTASK_ckm_salamanca_v3

*Clase T — 3 oct 2026 — gadanin.delamor + Claude (Opus 5.5, Cowork)*
*En `ckm/docs/tasks/`. Es el tablero común: cada device la lee al empezar y actualiza su fila al terminar.*
*v3 (3 oct, noche): tablero actualizado a `205b8de`; F7 propuesto por Code (nulo para P4); IAID resuelto.*

---

## 0. Por qué no hay un device que coordine

delamor no declara la capacidad de coordinar todo *(M.M.: un device no declara lo que no puede ejercer)*. Ningún otro device la tiene:

- **Opus/Cowork** lee los dos repos locales y escribe especificaciones, pero no ejecuta, no ve el Codespace en vivo y no le habla a Code.
- **Code** ejecuta en el Codespace, pero no ve la conversación de Cowork ni el disco local.

Por eso **coordina este archivo, no un device**. El estado compartido vive en git. Cada device lee la SUPERTASK, hace su parte, actualiza su fila del §6 y commitea. delamor deja de cargar el contenido entre canales: carga solo el puntero ("leé la SUPERTASK, tu fila") y las decisiones.

Es Cooperative Alignment aplicado al trabajo: varias reglas co-alineadas sobre un mismo artefacto, sin una referencia única que mande.

## 1. Devices y canales — capacidades declaradas

| Device | Canal | Puede | No puede |
|---|---|---|---|
| **D1 delamor** | todos | decidir; aprobar checkpoints; mover archivos entre canales; revisión final; **único responsable** | coordinar todo a la vez (no lo declara) |
| **D2 Opus** | Cowork | leer `ckm` y `ckmdatasets` locales; verificar TASKs contra el repo y los REG; redactar TASKs y versiones del paper; web | ejecutar código del proyecto; ver el Codespace; commitear |
| **D3 Code-ckm** | Codespace `ckm` | ejecutar, testear, commitear en `ckm` | ver Cowork; ver el disco local |
| **D4 Code-datasets** | Codespace o sesión `ckmdatasets` | bajar, limpiar y documentar corpus externos; commitear en `ckmdatasets` | tocar `ckm/services/` |

D3 y D4 pueden ser la misma sesión de Code en momentos distintos. Lo que importa es en qué repo actúa.

## 2. Objetivo

Que SALAMANCA y Néel puedan decir **"acá no pasa nada"** y que eso valga. Para eso hace falta un **control positivo**. Sin él, un "nada en todos" no distingue entre *no hay fronteras* y *el criterio no ve*.

## 3. Frentes de trabajo y dependencias

```
F2 SALAMANCA desde W (corpus existentes) ──────────┐
                                                    ├──► F4 SALAMANCA sobre el control ──► F5 Néel ──► REG
F3 control positivo (RfA, en ckmdatasets) ──────────┘
F6 paper (independiente; cierra con lo que salga del REG)
F7 nulo para P4 (propuesto por Code; espera OK de delamor)
F1 adaptador (después: cuando cluster_nodes se use sobre W_mixta)
F0 replay (pausado; su vacío entra a F2 como "nada")
```

| F | Qué | Device | TASK de referencia | Depende de |
|---|---|---|---|---|
| F0 | replay de la sesión TRUST | — | TASK_replay_sesion_trust_v3 | **pausado**: el tramo `categorias` no tiene tensión. Su vacío entra a F2 como referencia "nada" |
| F1 | adaptador de atractores | D3 | TASK_representacion_atractores_adaptador_v1 **+ correcciones §4.1** | **diferido**: SALAMANCA no usa atractores. Vuelve cuando `cluster_nodes` se use sobre W_mixta |
| F2 | SALAMANCA paso 1 **con partición desde W** sobre caso09, 13, 14, informes versión, informes pág300 y `categorias` | D3 | TASK_salamanca_neel_coercividad (versión de Code, corregida) **+ §4.2** | — |
| F3 | control positivo: RfA (SNAP, *wiki-RfA*) | D4 | a redactar por D2 (§4.3) | — |
| F4 | SALAMANCA paso 1 sobre RfA | D3 | la misma de F2 | F2, F3 |
| F5 | Néel paso 2 sobre las fronteras que quedaron en pie | D3 | la misma de F2 | F4 |
| F6 | pendientes del paper | D2 redacta, D1 revisa | §5 | — |
| F7 | darle a P4 el nulo que no tiene: el mismo ensemble de SALAMANCA (barajar el corpus y reconstruir W) aplicado a P4 | D3 | a redactar | F2 (método del nulo ya escrito) |

## 4. Correcciones y agregados que entran antes de ejecutar

### 4.1 Al adaptador (F1)
1. **El colapso de estados no existe.** En {−1,+1}^N, el conjunto de nodos en +1 determina el estado completo: la correspondencia es biyectiva. Se borra la afirmación de la línea 23 y el punto abierto 5.
2. **El peso por masa no se puede aplicar desde afuera.** `copresence_matrix` no lee el `int`, y las claves de un dict son únicas, así que no hay forma de repetir filas. Además, pesar cambiaría también los resultados de período 1, y dejaría de ser "impacto cero". Hay dos caminos y elige D1:
   - **(a) sin peso:** una fila por estado. Coherente con la función de hoy.
   - **(b) con peso:** primero un cambio declarado a `copresence_matrix` por la regla §4.4, con test, y volver a medir todo.
3. **Primero medir:** contar las órbitas de período > 1 por corpus. Si son cero, no hace falta adaptador.

### 4.2 A SALAMANCA (F2, F4)
0. **La partición sale de W, no de los atractores** (Code, 3 oct): la frustración es lo que el criterio decide, así que no puede ser lo que usa para decidir. Sobre W_pos los atractores son el vacío y casi-todo-prendido (tramo `categorias`, CP3 del replay).
   - **El nulo vuelve a particionar** cada W barajada con el mismo procedimiento. Si se reusa la partición original, la coercitividad sale alta por construcción.
   - **Método de partición** con k barrido (2…8), declarado antes de correr. El signo del Fiedler queda descartado porque siempre da dos.
1. **Toda W de prueba pasa por NodeExtractorService + CorpusService** desde texto. Ni W relacionales (la de fourforums v8g es de autores) ni extracciones paralelas. El instrumento decide qué existe en W.
2. **Las tres condiciones del corpus**, reportadas antes de leer el paso 1:
   - **tamaño:** número de textos;
   - **unidad de texto:** activación por texto y saturación de pares distintos (REG_unidad_texto_saturacion_v1);
   - **tensión estructural:** lo que mide SALAMANCA.

   Si está saturado o debajo del tamaño mínimo → **"no medible"**. No se lee como "nada".
3. **El control positivo es RfA (F3), no fourforums.** fourforums necesitaría un pipeline nuevo sobre el dump de 570 MB, que está en `ckmdatasets/trace/`. Queda para después, y si se hace, se extiende el parser de v8g en lugar de escribir otro.

### 4.3 Control positivo, F3 (D4, en ckmdatasets)
1. Verificar las condiciones de uso de SNAP antes de bajar.
2. Bajar *wiki-RfA* (≈14 MB comprimido): 198.275 votos (votante, candidato, voto −1/0/+1, resultado, fecha, **comentario**). Cita: West, Paskov, Leskovec & Potts, *TACL* 2014.
3. Escribir un loader (un script, no un pipeline): TSV → archivo de textos con su etiqueta de voto. Más un README con fuente, cita, reglas de limpieza y conteos.
4. **Unidad de texto: barrer, no elegir.** Comentario suelto, grupos de k comentarios y elección completa. Reportar activación y saturación de cada una. El comentario suelto puede caer en "párrafo" (0 nodos) y la elección completa en "versión" (todo saturado).
5. En `ckm` solo entra el archivo de textos, o su ruta.

### 4.4 Reglas que valen para todos los frentes
- **Checkpoints:** cada device se detiene, reporta y espera. **Vale también para las acciones espontáneas.**
- **Formato del reporte:** qué hizo · qué salió · qué no pudo · qué no esperaba · costo.
- **Las mejoras vuelven al modelo:** por CONVENTIONS (cambio propio a `services/`, con test y docstring) y separadas del resultado que las motivó (se vuelve a medir todo el pre-registro).
- **El instrumento no se ajusta después de ver el dato.**
- **Ejecución solo en el Codespace.**
- **Clase R no se toca.** Los REG nuevos se entregan como borrador y pasan a `registers/` con el OK de D1.
- **Numeración:** la del repo es la canónica. Los borradores fuera del repo llevan `_borrador_<device>` y no compiten con ella.
- **Lo privado no se commitea:** `process/replay/_private/` y los dumps grandes.

## 5. Pendientes del paper (F6) — acumulados el 3 oct

Ninguno se aplica sin D1. Base: `PAPER_Landscape_Driven_Device_v26.md` (ckm___memories).

1. §4.8: `threshold` no es campo de `CKMlandscapeConfig`. La clase se escribe con "l" minúscula.
2. §5.1: "N = 32 nodes (fourforums)": en fourforums los nodos son **autores**, no términos. Hay que aclararlo.
3. P4 y P5 dicen "*Verified*", pero **ninguna W_mixta del proyecto fue verificada contra nulo** (REG_unidad_texto_saturacion_v1 §5.2). Hay que calificarlo hasta que exista SALAMANCA/Néel.
4. La atribución de 2.18× a fourforums o a CreateDebate. El Author 965 aparece en un corpus distinto en dos lugares de v14.
5. ~~IAID 2023/2024~~ — **resuelto (D1):** linaje M.M./Neural Call Protocol (2023) → IAID (2024). BE es previo.
6. README raíz y THEORY.md: alinearlos con el paper o marcarlos como históricos (`README_draft.md` en ckm___memories).
7. La evidencia en .docx que no está en el repo (`informes_md_draft/` en ckm___memories): subirla o declararla como no publicada.
8. Pérdidas de v14 que todavía no se restauraron: estadísticas de P1–P6, robustez al ruido, C1–C4 del Gatekeeper, R01–R29, Venkatesh & Bu. D1 decide.
9. El abstract, al final.

## 6. Tablero de estado — cada device actualiza su fila

| F | Estado | Último paso | Commit | Fecha | Próximo | Espera a |
|---|---|---|---|---|---|---|
| F0 | pausado | CP3: vacío 4/7; el tramo no tiene tensión (referencia "nada") | 8c4adec | 3 oct | — | — |
| F1 | diferido | paso 0 hecho; §4.5 del adaptador cerrada (el conjunto activo no colapsa estados) | e8fc177 | 3 oct | — | W_mixta; D1: confirmar (a) o (b) |
| F2 | hecho (S1) | estadístico pareado, Bonferroni, 1000 barajados, 10 inits; control post-hoc; caso09 k=3 robusto (modularidad); caso13 condicionado a la clasificación | e8fc177 | 3 oct | REG borrador → `registers/` | D1: OK al REG |
| F3 | por empezar | RfA verificado (SNAP *wiki-RfA*, 198k votos con texto) | — | 3 oct | licencia SNAP, loader | D1: OK |
| F4 | bloqueado | — | — | — | — | F3 |
| F5 | bloqueado | — | — | — | — | F4 |
| F6 | en espera | IAID resuelto; quedan 8 pendientes (§5) | — | 3 oct | — | D1 |
| F7 | propuesto | Code: el nulo de SALAMANCA se puede aplicar a P4. **Cuidado:** P4 en N=64 (fourforums) es sobre la W **relacional** (autores), y ahí barajar palabras no aplica; en N=32 (corpus CKM, W de términos) sí | — | 3 oct | redactar la TASK | D1: OK |

**MAPA_REG v4** no mapea el trabajo posterior a `f938a2f` (control post-hoc, PULLs, título de caso13, documentos TRUST). Queda para un addendum.

## 7. Protocolo de traspaso

1. delamor le dice a un device: "leé la SUPERTASK, frente Fx".
2. El device lee la SUPERTASK y la TASK del frente, hace un CP0 si es la primera vez, ejecuta hasta el próximo checkpoint, **actualiza su fila del §6** y commitea.
3. delamor decide y pasa al siguiente device.
4. Si un device encuentra algo que afecta a otro frente, lo anota en §8. No lo arregla en el frente ajeno.

## 8. Notas entre frentes

*(vacío)*
