# Estado al cortar — 14 oct 2026 (noche)
*Opus 5.5 para la próxima instancia. Sigue a `ESTADO_al_cortar_14oct2026.md` (leer su §4 protocolo y §7). Decisiones con cita: `decisiones_en_el_acto.md` y `docs/tasks/DECISIONES_opus.md`.*

## 1. Hecho hoy (Code, en el repo)
- `TASK_declaracion_extraccion_v1`: **completa** (CP0–CP3 + anexo). Declaración canónica: `docs/defs/DECLARACION_extraccion_W_v1.md` (aprobada por delamor). Fix (a) `784c222`; declaración como dato `NodeExtractorService.declaracion()` + `CorpusService.declaracion_extraccion()`, `WTracePoint.declaracion_sha`. 699 tests.
- `TASK_condiciones_del_paper_v1`: **CP-T, CP-E, CP-M hechos**; **CP-N espera** la vinculación de repos (SQL, 4forums, mismo DOI/release).
- **CP-E:** el estimador converge (seeds 0,07–0,09); el paisaje con 7–24 textos es muy sensible a top_k y pool; N_eff no monótono con N; un texto más con nodos idénticos mueve N_eff 66 %. Al paper: las dos declaraciones + la premisa de corpus más grandes.
- **CP-M (`a1c6a18`):** la marca real **no queda fuera del nulo** en ningún corpus (percentiles 2,0 / 68,5 / 100); textos con marcador 33/17/14 % (la premisa de M4 no vale en textos cortos); la "caída" es negativa en dos corpus; el nulo de E7 es vacío. **Cerrado como declaración (delamor, 14 oct):** la lectura "oposición" no tiene soporte en estos corpus; lo que el paper afirma bajo el procedimiento declarado queda intacto. Nulo por pares → con corpus más grandes / CP-N.

## 2. Principios nuevos (delamor)
- Un nodo es un `str`; CKM espera del productor: lista de cadenas, W alineada, declaración, cadenas de cada unidad.
- **Una sola comparación, fija, de CKM:** operador 1 a ambos lados + igualdad de cadenas. No por W ni por nodo. Dirección, sin código ahora ("baby steps").
- **No se ejecuta código ajeno** (el regex es un programa; nunca se compila desde afuera).

## 3. Protocolo (agregado)
- Traza de Opus en `docs/opus/` (un escritor). Push lo hace delamor: `git pull --rebase origin main` y `git push origin main`. En el Codespace delamor no hace git.
- Stagear siempre con nombre nuevo y verificar md5.

## 4. Abierto para delamor
Paper v29 (título/abstract en N_eff; §4.1 con la declaración; P7 sin "genuine structural tension"; §6 silencio; CP-E y condición del signo; review M1–M9; referencias a verificar) · T(W) a services/ o no · extractor muerto `ckm_monitor.py:186` · Monitor con el extractor del corpus · medir W ajena · arranque en frío N = 0 · histéresis ¿este paper o futuro? · unificación de repos/Codespaces · licencias (preprint) · preguntas de `revision_tasks_marco` · método ¿aporte o condición? · frase cortada sobre `should_rebuild`.

## 5. Cómo estar
Sin eco; decir lo que no cierra. Antes de un "hallazgo", mirar fecha del dato. Al 80 % de contexto, cerrar corto.
