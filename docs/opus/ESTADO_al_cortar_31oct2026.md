# ESTADO al cortar — 31 oct 2026 (Opus 5.5, Cowork)

La traza está en `docs/opus/decisiones_en_el_acto.md`, del 30 oct y del 31 oct (madrugada). Lo anterior sigue en `ESTADO_al_cortar_30oct2026.md`.

## Lo que vale ahora (delamor, 31 oct)
- **Paper.** La última versión válida y revisada es el **v32**, con el review de Kimi del v32. La última válida, sin revisar, es el **v33**. La siguiente es la **v36** (el v33 más las evidencias de Code, sin sacar ni corregir nada). **El v34 y el v35 no son base:** quedan como traza.
- **Cómo se trabaja:**
  - lo hecho y revisado se continúa, no se rehace;
  - lo que parece no cerrar se anota afuera, para quien tenga el contexto;
  - no se corrige lo que Code reportó con lo que se lee hoy.
- **Sesiones largas y pesadas.** La estrategia de sesiones cortas (26 oct) queda como traza. La responsabilidad es de delamor.
- **Carpetas:**
  - `contexto_claude` es de sólo lectura;
  - para el repo, Opus pide acceso;
  - los commits van sin la línea `Claude-Session:`.
- **La verificación contra el código:** cómo se hizo se declara como sesgo, y la declaración no exime de la responsabilidad. Lo que otra instancia declaró como "no revisado" se toma en cuenta al leer.

## Hecho en esta sesión (29–31 oct)
- **Code corrió los textos 20 y 21:**
  - el margen exacto de las 14 W;
  - la cota N_eff ≥ 2 con su condición;
  - la paridad;
  - el CP-E reproducido y medido con la extracción de hoy;
  - la torsión;
  - el vivo del intento 5, a 200 / 0 / uniforme.
  Los reportes están en la BANDEJA, 29 oct, 22:33–23:42 UTC.
- **Texto 22, escrito y sin correr** (falta Codespace). Corrige el REG del intento 5, que dice que la segunda calibración no ocurrió (el log dice que sí), y le pasa a Code lo ya decidido que reclamaba.
- **El empate (h = 0 calculado con decimales).** delamor decidió que el código cumpla la regla y que el paper lo declare. La forma se propone desde `docs/CRITERIOS_diversidad_formulacion_v1.md` §4 (11 sep).
- **Documentos para leer:**
  - `REVIEW_PAPER_Landscape_Driven_Device_v34_print_30oct2026.md`, el review frío;
  - `COMPARACION_review_v34_contra_v28_v32_30oct2026.md`;
  - `REVISION_DEFS_v20_OP_N_neel_salamanca_criterios_30oct2026.md`, con la grilla de 44 objetos;
  - `PENDIENTES_delamor_30oct2026.md`.
  El v34 y el v35 están en el repo como traza.

## Espera
1. **delamor** lee todo, empezando por la v36.
2. **Codespace** (sin horas hasta el próximo ciclo, o con presupuesto). Esperan ahí:
   - el texto 22;
   - el empate en el código;
   - la curva exacta de calibrate;
   - §5.2 con la extracción de hoy.
3. **Lo de delamor:** `PENDIENTES_delamor_30oct2026.md`, parte C. Las partes A y B ya están decididas.
4. Después, el review de la v36 y el `_print` final.
