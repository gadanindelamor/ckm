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
- **Opus → Code (ckm, Codespace), tarea chica, primero en la próxima sesión.** Las tres declaraciones de fourforums v8n:
  1. **Extracción:** O1–O7 y la cadena v8h→v8n, que ya están declaradas.
  2. **LandscapeConfig de cada una de las 8 W:** `CKMlandscapeConfig.create(W, sampling_mode="uniform", n_runs, seed)` y un `Ciclo` con `w_version_id = sha256_W`, N, μ_W y β_c en sus dos formas. Se guarda junto a los resultados y no se vuelve a medir.
  3. **Calibración: "no se ejecutó"** (`nulo_calibrado`), porque las W son primeros builds y lo medido no usa umbrales.

  También declarar lo que hoy no coincide con la Config:
  - la semilla 20261023 contra la 0 de la Config;
  - las muestras 1000, 5000 y 20000 contra las 1000 declaradas;
  - el REG reporta `beta_c_landscape` (media de los positivos), que no es `beta_c_nonzero` ni `beta_c_global`;
  - la identidad de cada W es el sha del archivo, no `sha256_W` (sin verificar si coinciden).

  Opcional, como punto aparte: correr `calibrate` offline sobre las 8 W, como medición, sin predecir el resultado. Fuente: `decisiones_en_el_acto.md`, 24 oct.
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
