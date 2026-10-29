# ESTADO al cortar — 29 oct 2026, tarde (Opus 5.5, Cowork)

La traza está en `docs/opus/decisiones_en_el_acto.md`, en "29 oct (sesión de la tarde)". Esto es sólo el mapa. Lo anterior sigue en `ESTADO_al_cortar_29oct2026.md`.

## Hecho
- **El barrido, condición del v33:** `docs/opus/BARRIDO_v33_29oct2026.md`.
  - Es el mapa de lo que aparece, desaparece o vuelve entre versiones contiguas: el paper v0–v32 y las DEFS v0–v20.
  - Los eventos, bloque por bloque, están en `BARRIDO_v33_eventos_29oct2026.md` (paper) y `BARRIDO_v33_eventos_DEFS_29oct2026.md`.
  - La herramienta es `docs/opus/barrido_mapa.py`.
  - La prueba con los ejemplos del machete encuentra todos los temas. Falta la palabra "contenedor", que no está escrita en ninguna versión.
- **La verificación del PLAN_v33** contra el mapa y contra el v32: `docs/opus/VERIF_PLAN_v33_contra_mapa_29oct2026.md`.
- **Los temporales `tmp_obj_*` de git, borrados.** Vuelven con cada commit de Opus por el puente; Opus los borra después de cada commit.
- **`contexto_claude`** sigue en `antropic/___project/`. El cambio de ruta fue un dedazo de delamor y ya está corregido.
- Todo pusheado hasta `29390e4`. Este ESTADO es un commit más.

## Espera a delamor (lee lo generado y vuelve)
1. **§7.6, la representación del conocimiento: ¿vuelve al v33, y en qué forma?** Salió en v29 como "Propuesta" y no se encontró su confirmación. El 23 oct delamor dijo *"…perspectivas de lo mismo… si va"*.
2. **¿Se corrigen en el v33 las cinco líneas de "COCO … field regulator"?** Son el título de §4.2.1 y las líneas 312, 329, 702 y 706.
3. ~~La razón del corte v14 → v15~~: el giro que buscaba delamor está en v28 → v29, con razones registradas en el v29; la del v14 → v15 no se busca por ahora (delamor). §7.6 entra y las líneas de COCO se corrigen (ítems 1 y 2, decididos: ver `PLAN_v33` §6).
4. **"no se traduce":** aparece sólo en las DEFS v15, en un bloque de la extracción. ¿Es el ejemplo del panel?
5. **Qué se hace con el mapa.**

## Sigue igual
- Los textos para Code 17, 18 y 19 esperan a saber qué respaldo necesita el paper.
- B7, la razón del retiro de "COCO regula el campo", no se encontró. En el mapa hay un bloque candidato que se va en v14 → v15; no se leyó.
- Las series de REGs no están mapeadas.
