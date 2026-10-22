# Estado al cortar — 22 oct 2026
*Opus 5.5 para la próxima instancia. Reemplaza a `ESTADO_al_cortar_21oct2026.md`. Decisiones con cita: `decisiones_en_el_acto.md` (22 oct).*

## 1. Hecho hoy
- **Tarea PAPER (Opus):** `docs/defs/DEFS_CKM_estado_actual_v18.md`; `PAPER_Landscape_Driven_Device_v30_borrador_opus.md` (frase de COCO retirada de **cuatro** lugares, sin reemplazo; tres rastros listados sin tocar); `HILO_frase_COCO_versiones_paper_22oct2026.md`; `METODOLOGIA_TRUST_v1.md`; `INVENTARIO_versiones_paper_22oct2026.md`.
- **Tarea REPO (Code), cerrada:** techo de Groq por modelo; el log registra el canal entero; Gemini → `gemini-3.5-flash-lite` (decidido por Code con autorización de delamor); **intento 3**: 0 errores de provider, 0 truncamientos, **`calibrate` separó por primera vez en un vivo**. REG borrador: `docs/REG_borrador_serie2_caso0_intento3.md`.

## 2. Espera a delamor (de a una)
1. **P13** (BANDEJA, ítem 0): la línea escrita en `iap_chatroom/_state/` por un aislamiento roto con `pytest -n 4`. Recomendación de Opus: preservarla en `process/`; suite en serie por defecto (`-n 4` no acelera: 169 s vs 95 s) y en paralelo sólo para buscar fugas; que Code arregle el aislamiento (`import iap_chatroom.mcp_server` re-apunta el `state_dir`).
2. ¿El REG del intento 3 pasa a `registers/`?
3. **Review externo del paper v30:** pegar a Kimi (u otro) el v30 completo + `PEDIDO_REVIEW_paper_v30_22oct2026.md`. Con el review, Opus arma la versión final para delamor (sin preguntas).

## 3. Abierto, sin apuro
- La carpeta de las raíces de CKM: delamor la vinculó en la app, pero no aparece en esta sesión (en `ckmexperience\` hay `ckm___model`, `___paper`, `___project`, `___research`). Pedir acceso sólo lectura a la que diga. **No escribir ahí.**
- Memoria: lo de los 17 años de práctica fue rechazado (sensibles desactivado); delamor dice haberlo habilitado; pedirlo de nuevo en una sesión nueva.
- METODOLOGIA v2: anotar lo que la lente no anticipó.
