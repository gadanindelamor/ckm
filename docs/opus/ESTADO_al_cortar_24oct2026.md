# ESTADO al cortar — 24 oct 2026 (Opus 5.5, Cowork)

Traza completa en `docs/opus/decisiones_en_el_acto.md`, entradas del 24 oct. Esto es solo el mapa.

## Hecho hoy
- Code (madrugada, sin Opus, por los límites de uso): el build de W no calibra.
  - REG: ahora `registers/REG_calibrate_no_corre_en_el_build_v1.md`, con el OK de delamor.
  - TASK: `docs/tasks/TASK_calibrate_en_el_build_v1.md`.
  - El CP1 (`bootstrap`) se commiteó y se revirtió solo en el código (`7040a02`). El vivo no se corrió.
- Review del v32 hecho por Kimi, sin acceso al repo: `docs/paper/REVIEW_REPORT_PAPER_v32.md` (sin commitear) y `contexto_claude/`.
- Opus: `docs/opus/CONSIDERACIONES_v33_24oct2026.md`, que es el plan del v33 con el review de Kimi verificado contra el repo.
- Push al día: `ffdc77b`.

## Lo que sigue
- **Opus:** armar el v33 en dos archivos, `_borrador` y `_print`, siguiendo las CONSIDERACIONES. Antes de escribir:
  - leer el CP-E (el 15.52 → 5.27 del §4.3.2);
  - leer la cita de P2 en Goltsev 2006;
  - leer el criterio estructural de rebuild;
  - buscar en `DECISIONES` el origen del baseline de Monitor.
  - Después, ajustar `cold-referee` y el pedido de review para que apunten al `_print`.
- **delamor:**
  - qué hacer con las 13 de `test_should_rebuild_conectado.py`: acotarlas o archivarlas. Code retoma en dos días;
  - P13 y P14;
  - la definición del margen de `calibrate`: extremos o máximo interno (E3);
  - J1, J2, los subgrafos chicos y si se versiona `W_asim`, que vienen del 23;
  - la figura Monitor contra COCO, si la querés.
- **Sin dueño:** en `docs/paper/` hay copias sin commitear del v31, el v32 y el review del v31, idénticas a las de `docs/opus/`, más el review del v32.

## Raro
- En `.git/objects` hay cientos de `tmp_obj_*` sobrantes de sesiones anteriores. No son locks y no se tocaron.
- Uso al 95% del límite semanal; se repone en un día.
