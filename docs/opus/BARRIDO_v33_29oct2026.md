# BARRIDO — condición del v33 (29 oct 2026, Opus 5.5, Cowork)

**Qué es:** ver qué fue quedando afuera del paper con las versiones (delamor, 28 oct: *"ver qué fue quedando afuera con las versiones… algo que quedó en el camino del paper siento es la representación del conocimiento"*; *"es condición para la versión 33"*).
**Qué no es:** un estudio nuevo, ni material nuevo para el v33. Lo que el barrido encuentre se clasifica: (a) entra al v33 porque es aporte y ya está verificado; (b) entra sólo si da sentido a lo que aporta; (c) queda para otro paper; (d) no se sostiene y se dice dónde.
**Antecedentes:** `docs/opus/INVENTARIO_versiones_paper_22oct2026.md` y `docs/opus/HILO_frase_COCO_versiones_paper_22oct2026.md` (COCO era el ejemplo, 22 oct).

## El machete de delamor (29 oct, textual)

> represent del conocimiento
> W mixta
> delta direccional: en W estatica al juntarlas bla bla colapso. aprendizaje hebiano etc
> betta collective REGs de beta collective y coco
> que se muestra a los devices en el panel y porque no se traduce.
> Corpus services es CKM en parte es el contenedor? mas alla de cKM monitor de IAP? parte hace extraccion??? en mesetas?c

Más lo que dejó pendiente el 29 oct: **dónde quedó registrada la razón del retiro de "COCO regula el campo"** (decisiones, 29 oct), para corregirla donde esté.

| # | ítem | fuentes de partida (sin leer todavía) |
|---|---|---|
| B1 | la representación del conocimiento | `docs/CKM_encuadre_representacion_conocimiento_v1.md`; doc X (§1, §8–§9); paper v11–v14 |
| B2 | W mixta | `REG_wmixta_natural_paso2_v1`, `REG_wmixta_forzado_paso3_v1`, `REG_wmixta_consolidado_v1`; `iap_chatroom/tests/wmixta_*` |
| B3 | el delta direccional: al juntar W estáticas, el colapso; aprendizaje hebbiano | paper v1–v14 ("direccional"); `docs/Spike-timing-dependent_plasticity.pdf` |
| B4 | β colectivo, y los REGs de β colectivo y de COCO | `REG_beta_colectivo_v1`; `REG_coco_*`, `REG_iap_coco_convergence_v1`, `REG_sesion_coco_endogeno_v2`; la divergencia de docstring de `beta_i` (doc X, "Raro") |
| B5 | qué se les muestra a los devices en el panel, y por qué no se traduce | `monitor_service.py` (panel); REGs de la serie 2 |
| B6 | services y el corpus: ¿es CKM en parte?, ¿es el contenedor?, ¿va más allá del Monitor de IAP?, ¿una parte hace extracción?, ¿en mesetas? | `services/`; `docs/PROPUESTA_capa_analisis_services_v1.md`; `REG_monitor_service_*` |
| B7 | la razón del retiro de "COCO regula el campo" | decisiones 29 oct; `HILO_frase_COCO_versiones_paper_22oct2026.md` |

## Primera pasada, mecánica (grep, líneas que coinciden; sin leer)

Sólo dice dónde aparece cada palabra y cuándo deja de aparecer. Una línea que coincide no es un tema tratado. Patrones (`grep -ciE`): repr `knowledge representation|representaci[oó]n del conocimiento`; wmix `W mixta|wmixta|W_mix|mixed W|W_mixta`; direc `direccional|directional`; hebb `hebb`; beta `beta_colectivo|beta colectivo|collective beta|beta_collective|β_col|beta_i`; panel `panel`; serv `services/|corpus service|CorpusService`; meseta `meseta|plateau`; extrac `extracci[oó]n|extraction`.

| ver | repr | wmix | direc | hebb | beta | panel | serv | meseta | extrac |
|---|---|---|---|---|---|---|---|---|---|
| v1 | 0 | 5 | 8 | 0 | 1 | 0 | 4 | 0 | 2 |
| v3 | 2 | 9 | 14 | 1 | 1 | 0 | 10 | 0 | 3 |
| v10 | 2 | 10 | 17 | 2 | 1 | 0 | 10 | 0 | 3 |
| v11 | 6 | 13 | 17 | 4 | 1 | 0 | 10 | 0 | 3 |
| v14 | 6 | 14 | 17 | 10 | 1 | 2 | 14 | 0 | 8 |
| v15 | 5 | 7 | 7 | 5 | 4 | 3 | 9 | 0 | 4 |
| v16–v21 | 4 | 5 | 6 | 3 | 3 | 3 | 5 | 0 | 2 |
| v27 | 4 | 7 | 7 | 5 | 3 | 3 | 8 | 1 | 2 |
| v28 | 4 | 7 | 7 | 5 | 3 | 3 | 10 | 1 | 3 |
| v30 | 2 | 6 | 7 | 5 | 4 | 3 | 8 | 1 | 9 |
| v32 | 2 | 6 | 6 | 5 | 4 | 4 | 13 | 1 | 9 |
| DEFS v20 | 0 | 47 | 3 | 3 | 0 (β: 16) | 27 | 30 | 1 | 19 |

(Tabla completa por versión, v1–v32: el comando está en la entrada del 29 oct de `decisiones_en_el_acto.md`; se re-corre igual.)
Lo que se ve, sin leer: el corte grande está entre v14 y v15 (direc 17 → 7, wmix 14 → 7, hebb 10 → 5). "Representación del conocimiento" pasa de 6 (v11–v14) a 4 (v15–v28) y a 2 (v30–v32); en las DEFS v20 no aparece la frase.

## Método, por ítem
1. Dónde aparece por primera vez y dónde se va (versión y línea).
2. Qué decía, citado; si había un REG o una medición detrás.
3. Si se fue: si quedó registrada la razón (decisiones, REVIEW, traza de modificaciones).
4. Clasificación (a)–(d), con la cadena expuesta. Lo que no tenga cadena se dice.
Sin interpretar lo que los resultados significan.

## Avance
- [ ] B1 · [ ] B2 · [ ] B3 · [ ] B4 · [ ] B5 · [ ] B6 · [ ] B7
