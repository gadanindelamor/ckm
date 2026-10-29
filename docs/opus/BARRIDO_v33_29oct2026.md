# BARRIDO — condición del v33 (29 oct 2026, Opus 5.5, Cowork)

## La intención (delamor, 29 oct, textual)

> *"Eso que citás es un ejemplo, como lo fue COCO cuando otra instancia hizo el HILO. Las líneas del machete también son ejemplos. El barrido no se arma con ellos. Es el mapa general de lo que aparece, desaparece o vuelve entre versiones contiguas, sea lo que sea, sin categorías previas y sin interpretar. Los ejemplos se usan al final, para comprobar que el mapa los encuentra."*

Y después: *"sigue. Los ejemplos quedan como prueba al final: el mapa tiene que encontrarlos."*

**Retirado (A3):**
- La primera versión (`688f68e`) armaba el barrido con las líneas del machete. Eran categorías tomadas de los ejemplos, copiadas de la forma del HILO de COCO. Queda sólo en el historial de git.
- La segunda versión (`1b0b2eb`) daba un ejemplo por encontrado sólo si "se iba". Eso era otra categoría que puse yo: el mapa registra tres eventos (aparece, desaparece, vuelve) y cualquiera de los tres cuenta.
- La segunda versión tenía además un defecto: lo que estaba en v1 y no se iba nunca no era evento de ningún tipo. Ahora hay una v0 vacía antes de cada serie.

## El machete (ejemplos, para la prueba del final)

> represent del conocimiento · W mixta · delta direccional: en W estatica al juntarlas bla bla colapso. aprendizaje hebiano etc · betta collective REGs de beta collective y coco · que se muestra a los devices en el panel y porque no se traduce. · Corpus services es CKM en parte es el contenedor? mas alla de cKM monitor de IAP? parte hace extraccion??? en mesetas?c

Además, del 29 oct: la razón del retiro de "COCO regula el campo".

## Cómo se hizo (todo declarado)

**Series.** Son dos series versionadas.

- **Paper:** v0 (vacía), v1, v2, v3, v4, v6, …, v27, v28_borrador y v29–v32_borrador_opus.
  - No hay v5.
  - Quedan fuera las variantes: v9 – copia, v10_0, v10_1, v10_2, v10_2_1, v12_1, v14_CITAS, v15_peg, v15_borrador y `_traza_paper_v27/`.
  - Por fecha, v14_CITAS y v15_peg están entre v14 y v15. v15_borrador es posterior a v27.
- **DEFS:** v0 (vacía), v2, v7, v8, v9, v10, v10_1, v12, …, v20.
  - No existen v1, v3–v6 ni v11.
  - v10_1 entra a la cadena porque es la única entre v10 y v12.

En las dos series, el orden por número coincide con el orden por fecha de los archivos.

**Sesgo declarado:** la serie DEFS la agregué porque la prueba con los ejemplos falló en el paper. El objetivo de la extensión es que el mapa encuentre los ejemplos. "Sea lo que sea, entre versiones contiguas" la alcanza igual. Las series de REGs (por ejemplo `META_REG` v2–v6, `MAPA_REG` v1–v4 y `hint_next_instance` v1–v8) **no están mapeadas**.

**Unidad.** El bloque: texto separado por una línea en blanco. Cada versión entra con el texto entero, incluido su bloque de cambios del encabezado.

**Cuándo dos bloques son el mismo.** El bloque A de v_k tiene par en v_m si algún bloque B de v_m contiene al menos θ de las palabras distintas de A.
- Se cuentan palabras de 3 o más letras, en minúsculas.
- **θ = 0,6.** La sensibilidad se midió con 0,5 y 0,7.
- Los bloques con menos de 5 palabras distintas no entran.

**Eventos.**
- **Se va:** el bloque no tiene par en v_k+1. Puede volver más adelante o no volver nunca.
- **Llega:** el bloque no tiene par en v_k. Puede ser nuevo o volver de una versión anterior.

**Límites.**
- θ y el mínimo de 5 palabras los elegí yo.
- Un bloque reescrito o traducido cuenta como "se va" y "llega".
- El mapa sólo ve el texto de las dos series. No ve el código ni los REGs.

**Dónde corrió.** `docs/opus/barrido_mapa.py`, en el contenedor de Opus. Se re-corre con `python docs/opus/barrido_mapa.py <paper|defs> 0.6`.

## El mapa — paper (θ = 0,6)

| paso | bloques | se van (no vuelven / vuelven) | llegan (nuevos / vuelven) |
|---|---|---|---|
| v0 → v1 | 0 → 111 | 0 | 111 |
| v1 → v2 | 111 → 161 | 0 | 37 |
| v2 → v3 | 161 → 270 | 2 (2 / 0) | 103 |
| v3 → v4 | 270 → 297 | 1 (1 / 0) | 26 |
| v4 → v6 | 297 → 304 | 0 | 6 |
| v6 → v7 | 304 → 304 | 1 (1 / 0) | 0 |
| v7 → v9 | 304 → 307 | 0 | 4 |
| v9 → v10 | 307 → 305 | 3 (3 / 0) | 3 |
| v10 → v13 | 305 → 334 | 0 | 33 |
| v13 → v14 | 334 → 361 | 2 (2 / 0) | 35 |
| **v14 → v15** | **361 → 240** | **157 (151 / 6)** | **59** |
| **v15 → v16** | **240 → 186** | **39 (38 / 1)** | 1 (0 / 1) |
| v16 → v17 | 186 → 182 | 5 (5 / 0) | 3 |
| v17 → v22 | 182 → 192 | 0 | 13 |
| v22 → v23 | 192 → 192 | 1 (1 / 0) | 2 |
| v23 → v25 | 192 → 193 | 0 | 1 |
| v25 → v26 | 193 → 196 | 1 (1 / 0) | 6 (1 / **5**) |
| v26 → v27 | 196 → 211 | 0 | 20 (19 / 1) |
| v27 → v28 | 211 → 222 | 0 | 14 |
| **v28 → v29** | **222 → 233** | **39 (39 / 0)** | **58** |
| v29 → v30 | 233 → 233 | 0 | 0 |
| v30 → v31 | 233 → 242 | 9 (9 / 0) | 23 |
| v31 → v32 | 242 → 245 | 0 | 3 |

**Totales:** 253 bloques se van y no vuelven, 7 se van y vuelven, llegan 554 nuevos y vuelven 7.

**Los cortes:** v14 → v15, v15 → v16 y v28 → v29. Son los mismos con θ = 0,5 (208 se van y no vuelven) y con θ = 0,7 (298).

**Dónde está lo que se fue y no volvió.** Se buscó con el mismo criterio en v14_CITAS, v15_peg, v15_borrador y DEFS v20.
- **v14 → v15 (151 bloques):** 145 están en v14_CITAS y v15_borrador; 6 sólo en v15_borrador.
- **v15 → v16 (38):** 35 están en v14_CITAS y v15_borrador; 3 no están en ninguno.
- **v28 → v29 (39):** 12 no están en ninguno; el resto está en las variantes; 2 están en DEFS v20.
- **Los demás pasos (25):** 12 no están en ninguno; 13 tienen copia en las variantes, 8 de ellos en v30 → v31.
- **En total, 3 de los 253 están en DEFS v20.**

**Lo que vuelve.**
- Seis bloques del corte v14 → v15 vuelven en v26 (3), v29, v31 y v32. Son de §3.6 *Terminological Precision*, §3.y *The IAP Chatroom as Methodological Instance*, §4.2 *Cohesion Measure* y la nota de P5.
- En v26 llegan además 5 bloques que estaban en v14.

## El mapa — DEFS (θ = 0,6)

| paso | bloques | se van (no vuelven / vuelven) | llegan |
|---|---|---|---|
| v0 → v2 | 0 → 71 | 0 | 71 |
| **v2 → v7** | **71 → 109** | **41 (34 / 7)** | 79 |
| v7 → v8 | 109 → 130 | 2 (2 / 0) | 24 |
| v8 → v9 | 130 → 164 | 5 (4 / 1) | 38 |
| v9 → v12 | 164 → 187 | 0 | 23 |
| **v12 → v13** | **187 → 190** | **12 (10 / 2)** | 18 |
| v13 → v14 | 190 → 242 | 1 (1 / 0) | 60 |
| v14 → v15 | 242 → 305 | 0 | 75 |
| v15 → v20 | 305 → 351 | 0 | 44 |

**Totales:** 51 bloques se van y no vuelven, 10 se van y vuelven, llegan 432 nuevos y no vuelve ninguno.

**Los cortes:** v2 → v7 y v12 → v13. Son los mismos con θ = 0,5 y con θ = 0,7. Desde v13 casi no se va nada: sólo 1 bloque en v13 → v14.

**Lo que vuelve.** De v2 → v7 vuelven 7 bloques:
- la cabecera del doc;
- Δ, la matriz asimétrica de orientación;
- c(S);
- la coercividad de W_mixta;
- el umbral de D_ckm;
- los estados epistémicos (dos bloques).

Vuelven en v9, v14, v15, v19 y v20. Del conteo de atractores con β_c (Boltzmann), vuelven 3 bloques en v13 y v15.

Cada bloque, con su título y su texto:
- `docs/opus/BARRIDO_v33_eventos_29oct2026.md` (paper)
- `docs/opus/BARRIDO_v33_eventos_DEFS_29oct2026.md` (DEFS)

## La prueba con los ejemplos

Cuenta cualquier evento: llega, se va o vuelve. Se buscó cada ejemplo, como texto, en los bloques de los eventos de las dos series.

| ejemplo | paper | DEFS |
|---|---|---|
| representación del conocimiento | llega v3, v11, v29; se va v15, v16, v29 | — |
| W mixta | llega v1…v29; se va v3, v15, v16, v29; vuelve v26 | llega v2…v19; se va v7, v8, v9, v13 |
| delta direccional | llega v1…v29; se va v15, v16, v29 | llega v2, v7; se va v7 |
| aprendizaje hebbiano | llega v3…v25; se va v15, v16 | llega v2, v7, v15; se va v7 |
| β colectivo | llega v1, v15, v29; se va v15, v16 | — |
| COCO regula (el retiro) | llega v1…v31; se va v15 (1 bloque, sin leer) | llega v2…v15; se va v7 |
| el panel (qué se muestra a los devices) | llega v14, v31 | llega v8…v20; se va v13 |
| "no se traduce" | — | llega v15: un bloque de la extracción (*"extrae formas, no significados… traducciones: UNKNOWN / desconocido"*). Si es el ejemplo: **[delamor]** |
| services / CorpusService | llega v1…v31; se va v15, v16, v23, v29, v31 | llega v10…v19 |
| "contenedor" | — | — |
| extracción | llega v1…v29; se va v15, v16, v29 | llega v13…v19 |
| mesetas | llega v27, v28 | llega v17 |

**Resultado, sin leer:**
- Las dos series juntas encuentran como evento todos los temas del machete.
- **No** encuentran la palabra "contenedor/container", que no está en ninguna versión del paper ni de las DEFS. Es una palabra de la pregunta de delamor. El tema de esa línea, services y CorpusService, sí está.
- "no se traduce" aparece una sola vez, en las DEFS v15, en un bloque de la extracción. Si es lo mismo que el ejemplo no lo sé.
- "β colectivo" no aparece en las DEFS. `REG_beta_colectivo_v1` distingue `beta_collective` de β_c, así que el β_c de las DEFS (conteo de Boltzmann) no se contó como β colectivo.

## Avance
- [x] El mapa del paper (v0–v32) y el de las DEFS (v0–v20), θ = 0,6, con sensibilidad a 0,5 y 0,7
- [x] La prueba con los ejemplos: encontrados todos los temas; falta "contenedor" (nunca escrito); "no se traduce" queda para delamor
- [ ] Sin mapear: las series de REGs
- [ ] Qué se hace con el mapa: **[delamor]**
