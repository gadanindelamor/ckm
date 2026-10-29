# BARRIDO — condición del v33 (29 oct 2026, Opus 5.5, Cowork)

## La intención (delamor, 29 oct, textual)

> *"Eso que citás es un ejemplo, como lo fue COCO cuando otra instancia hizo el HILO. Las líneas del machete también son ejemplos. El barrido no se arma con ellos. Es el mapa general de lo que aparece, desaparece o vuelve entre versiones contiguas, sea lo que sea, sin categorías previas y sin interpretar. Los ejemplos se usan al final, para comprobar que el mapa los encuentra."*

**Retirado (A3):** la primera versión de este doc (`688f68e`) armaba el barrido con las líneas del machete y contaba palabras por versión. Eso eran categorías previas tomadas de los ejemplos: copiaba la forma del HILO de COCO (22 oct). Fue peso de contexto, no comprensión. La tabla de conteos queda sólo en el historial de git.

## El machete (ejemplos, para la prueba del final)

> represent del conocimiento · W mixta · delta direccional: en W estatica al juntarlas bla bla colapso. aprendizaje hebiano etc · betta collective REGs de beta collective y coco · que se muestra a los devices en el panel y porque no se traduce. · Corpus services es CKM en parte es el contenedor? mas alla de cKM monitor de IAP? parte hace extraccion??? en mesetas?c

Además, del 29 oct: la razón del retiro de "COCO regula el campo".

## Cómo se hizo (todo declarado)

- **Cadena de versiones:** v1, v2, v3, v4, v6, …, v27, v28_borrador, v29–v32_borrador_opus. **No hay v5.** El orden por número coincide con el orden por fecha de modificación de los archivos.
- **Quedan fuera de la cadena** (son variantes): v9 – copia, v10_0, v10_1, v10_2, v10_2_1, v12_1, v14_CITAS, v15_peg, v15_borrador y `_traza_paper_v27/`. Por fecha, entre v14 y v15 están v14_CITAS y v15_peg. **v15_borrador es posterior a v27** (4 oct, aprox.), no está entre v14 y v15.
- **Unidad:** el bloque, o sea el texto separado por una línea en blanco. Se toma el texto entero de cada versión, con el bloque de cambios del encabezado incluido.
- **Mismo bloque:** el bloque A de v_k tiene par en v_m si algún bloque B de v_m contiene al menos θ de las palabras distintas de A. Se cuentan palabras de 3 o más letras, en minúsculas. **θ = 0,6.** Bloques con menos de 5 palabras distintas no entran.
- **Eventos:**
  - **Se va:** en v_k no tiene par en v_k+1. Después **vuelve** (tiene par en alguna versión posterior) o **no vuelve** hasta v32.
  - **Llega:** en v_k+1 no tiene par en v_k. Es **nuevo** (sin par en ninguna versión anterior) o **vuelve** (tenía par en una anterior).
- **Títulos:** los títulos `#`, sin numeración, comparados como texto exacto.
- **Dónde está lo que se fue:** cada bloque que se va y no vuelve se buscó, con el mismo criterio, en v14_CITAS, v15_peg, v15_borrador y DEFS v20.
- **Sesgos y límites:**
  - θ y el mínimo de 5 palabras son elecciones de Opus.
  - Un bloque reescrito en otras palabras cuenta como "se va" más "llega".
  - El paper cambió de idioma por partes (v1 tiene el índice en castellano). Una traducción aparece como "se va" más "llega".
  - El mapa cubre sólo los textos del paper. Lo que vive en el código o en los REGs y nunca entró al paper no puede aparecer.
- **Dónde corrió:** `docs/opus/barrido_mapa.py`, en el contenedor de Opus, no en la PC ni en el Codespace. Se re-corre con `python docs/opus/barrido_mapa.py 0.6`.

## El mapa

Bloques por versión, y los eventos de cada paso (θ = 0,6):

| paso | bloques | se van (no vuelven / vuelven) | llegan (nuevos / vuelven) |
|---|---|---|---|
| v1 → v2 | 111 → 161 | 0 | 37 (37 / 0) |
| v2 → v3 | 161 → 270 | 2 (2 / 0) | 103 (103 / 0) |
| v3 → v4 | 270 → 297 | 1 (1 / 0) | 26 (26 / 0) |
| v4 → v6 | 297 → 304 | 0 | 6 |
| v6 → v7 | 304 → 304 | 1 (1 / 0) | 0 |
| v7 → v8 | 304 → 306 | 0 | 3 |
| v8 → v9 | 306 → 307 | 0 | 1 |
| v9 → v10 | 307 → 305 | 3 (3 / 0) | 3 |
| v10 → v11 | 305 → 317 | 0 | 15 |
| v11 → v12 | 317 → 328 | 0 | 11 |
| v12 → v13 | 328 → 334 | 0 | 7 |
| v13 → v14 | 334 → 361 | 2 (2 / 0) | 35 |
| **v14 → v15** | **361 → 240** | **157 (151 / 6)** | **59 (59 / 0)** |
| **v15 → v16** | **240 → 186** | **39 (38 / 1)** | 1 (0 / 1) |
| v16 → v17 | 186 → 182 | 5 (5 / 0) | 3 |
| v17 → v22 | 182 → 192 | 0 | 13 en total |
| v22 → v23 | 192 → 192 | 1 (1 / 0) | 2 |
| v23 → v25 | 192 → 193 | 0 | 1 |
| v25 → v26 | 193 → 196 | 1 (1 / 0) | 6 (1 / **5**) |
| v26 → v27 | 196 → 211 | 0 | 20 (19 / 1) |
| v27 → v28 | 211 → 222 | 0 | 14 |
| **v28 → v29** | **222 → 233** | **39 (39 / 0)** | **58 (58 / 0)** |
| v29 → v30 | 233 → 233 | 0 | 0 |
| v30 → v31 | 233 → 242 | 9 (9 / 0) | 23 |
| v31 → v32 | 242 → 245 | 0 | 3 |

En total, a θ = 0,6: **253 bloques se van y no vuelven**, 7 se van y vuelven, y 7 llegan desde una versión anterior.

**Los cortes:** v14 → v15, v15 → v16 y v28 → v29. Los demás pasos agregan; casi no quitan.

**Con otro θ:** la forma no cambia. Los mismos cortes aparecen con θ = 0,5 y con θ = 0,7.
- θ = 0,5: no vuelven 208, vuelven 14; v14 → v15 se van 132.
- θ = 0,6: no vuelven 253, vuelven 7; v14 → v15 se van 157.
- θ = 0,7: no vuelven 298, vuelven 4; v14 → v15 se van 175.

**Títulos:**
- v14 → v15: salen 26 y no vuelve ninguno; entran 21.
- v15 → v16: salen 7.
- v28 → v29: salen 5 y entran 8.
- v30 → v31: salen 4 y entran 5.
- Ningún título que sale vuelve.

**Dónde está lo que se fue y no volvió (253 bloques):**
- **v14 → v15 (151):** 145 están en v14_CITAS y en v15_borrador; 6 sólo en v15_borrador.
- **v15 → v16 (38):** 35 están en v14_CITAS y v15_borrador; 3 en ningún lado.
- **v28 → v29 (39):**
  - 12 en ningún lado;
  - 7 sólo en v15_peg;
  - 11 en v14_CITAS, v15_peg y v15_borrador;
  - 7 en v14_CITAS y v15_borrador;
  - 1 en DEFS v20;
  - 1 en v14_CITAS, v15_borrador y DEFS v20.
- **Los demás pasos (25):** 12 bloques en ningún lado y 13 con copia en las variantes (8 de ellos en v30 → v31).
- **En DEFS v20 están 3 de los 253.**

**Lo que vuelve después de irse:** son 7. Seis son del corte v14 → v15 y vuelven en v26 (3), v29, v31 y v32. El séptimo es de v15 → v16 (una nota de cambios) y vuelve en v23. Los seis son bloques de §3.6 *Terminological Precision*, §3.y *The IAP Chatroom as Methodological Instance*, §4.2 *Cohesion Measure* (las órbitas de período 2; las masas convergen y los conteos no; N_eff) y la nota de P5. En v26 llegan además 5 bloques que estaban en v14: §2.3 Aiyappa, §4.2 período 2, §5.1 Fourforums, la condición de pares negativos, y P5.

Cada bloque, con su título y su texto: `docs/opus/BARRIDO_v33_eventos_29oct2026.md`.

## La prueba con los ejemplos

¿El mapa encuentra los ejemplos entre sus eventos? Se buscó cada ejemplo, como texto, en los bloques que se van y en los que llegan.

| ejemplo | ¿se va? (paso) | ¿llega? (versión) |
|---|---|---|
| representación del conocimiento | sí, 4 bloques (v14→v15, v15→v16, v28→v29) | v3, v11 (3), v29 |
| W mixta | sí, 18 (v2→v3, v14→v15, v15→v16, v28→v29); 1 vuelve en v26 | desde v2 |
| delta direccional / juntar W / colapso | sí, 13 ("direccional"; v14→v15, v15→v16, v28→v29) | desde v2 |
| aprendizaje hebbiano | sí, 5 (v14→v15, v15→v16) | desde v3 (10 bloques) |
| β colectivo | sí, 2 (v14→v15, v15→v16) | v15 (4), v29 (2) |
| COCO regula | sí, 1 (v14→v15) | desde v10 (6 bloques) |
| qué ven los devices en el panel; por qué no se traduce | **no** se va. "panel" llega en v14 y v31; "traduce/translate", en ningún evento | — |
| services / corpus / contenedor | **no** se va. "services" llega en v23 y v31; "contenedor/container", en ningún evento | — |
| extracción | sí, 6 (v14→v15, v15→v16, v28→v29) | desde v2 (13 bloques) |
| mesetas | **no** se va; llega en v27 y v28 | — |
| razón del retiro de "COCO regula el campo" | el bloque que se va en v14→v15 es un candidato. No se leyó | — |

**Sin leer:**
- El mapa encuentra como "se va" seis de los ejemplos: representación del conocimiento, W mixta, direccional, hebbiano, β colectivo y extracción.
- No encuentra como "se va" tres: panel / traducción, services / contenedor y mesetas. Llegan tarde o nunca aparecen, y no se van.
- Por el límite del mapa no se puede saber si esos tres viven fuera del paper (en el código o en los REGs), y el mapa no lo dice.

## Avance
- [x] El mapa (v1–v32, θ = 0,6, con sensibilidad a 0,5 y 0,7)
- [x] La prueba con los ejemplos
- [ ] Lo que sigue lo decide delamor: el mapa no clasifica ni lee
