TAREA — línea fourforums / ckmdatasets (delamor, 23 oct). Con un checkpoint: validar y ver → A1.PAUSA, decide delamor → continuar y finalizar. Registrado en docs/opus/decisiones_en_el_acto.md.

Leé primero: docs/opus/datasets_que_es_publicable_15oct2026.md y docs/opus/lectura_pipeline_fourforums_v8g_15oct2026.md. Decisiones vigentes: opción B (un repo ckm, dos entornos/devcontainers); los datos crudos del IAC NUNCA en un repo nuestro (ni privado): se declaran con URL de origen, archivo y sha256; licencia de redistribución no clara, revisión legal en el preprint.

Git: pull --rebase antes y antes de cada push; commits nombrando archivos.

CP0 — VALIDAR Y VER (sólo lectura; NO bajes ningún dato del IAC):
1. El repo gadanindelamor/ckmdatasets: estado (último commit ac6211f, v8g), qué hay, qué se ejecuta, con qué dependencias. Si no podés clonarlo desde el Codespace, decilo y seguí con lo que haya en ckm.
2. El pipeline fourforums (v8g en el repo; v8h existe fuera del repo, en la PC de delamor, no lo busques): qué produce W, de dónde sale el signo, N de nodos, y lo que la lectura del 15 oct dejó marcado (N = 2, stream_W_delta sin uso, CD_BASELINE a mano, W no simétrica en run_p6).
3. Qué haría falta para el CP-N (TASK_condiciones_del_paper_v1) con fourforums: qué corpus, qué N, qué producto de W, y si el productor declarado (DECLARACION_extraccion_W_v2) aplica o es otro productor.
4. El plan de la opción B, propuesto, no aplicado: carpeta datasets/, .gitignore, devcontainer, MANIFIESTO con sha256 y fuente.
5. Qué es publicable y qué no, con la clasificación del 15 oct (crudo / derivado por fila / agregado / código).

Reporte en la BANDEJA y en el chat. A1.PAUSA: delamor decide antes de seguir (incluido si se bajan datos al Codespace y desde dónde, o si se espera permiso).

CP1 — CONTINUAR Y FINALIZAR, según lo que decida delamor en el CP0. Resultados los que sean, con números, sin interpretar, y lo que no dicen. Commit, push, ESTADO, BANDEJA, reporte, A1.PAUSA.

Reglas de siempre: docstrings con cada .py tocado; sin nomenclatura nueva sin declararla; docs/opus/ es de Opus; nada de vivos.
