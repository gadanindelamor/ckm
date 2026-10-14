# Estado al cortar — 14 oct 2026 (cierre)
*Opus 5.5 (Cowork) para la próxima instancia. Leer antes `ESTADO_al_cortar_13oct2026.md` §1 (cómo se trabaja). Todas las decisiones de hoy, con cita, en `decisiones_en_el_acto.md`.*

## 1. Dirección (delamor, 14 oct)
- **Sin regresiones, sin compatibilidad hacia atrás; la única versión del modelo es la actual, el resto es imaginación** (*"es la tercera vez que lo menciono"*).
- **Foco: cerrar el proyecto para publicar el paper; después, TRUST.** *"cKM no extrae nodos"*, *"ckm no tokeniza"*: la extracción no es aporte. Estudio de tokenización, para después (OPUSDELAMOR).
- **Declarar, no decidir:** extracción, tokenización y signo se declaran con referencia y viajan en la traza; cualquier productor de W (actual, personal, externo) entrega W + nodos + declaración. *"Lo que no es debate es que el código implemente lo que el paper declara."* Al declararla, la dependencia queda adentro de la afirmación.
- **CKM interpreta dinámica, no significado.** La tensión es interpretación del signo; el silencio no es observable en W.
- **Estabilidad:** primero estable, declarada como rango con sus dependencias; después suites.
- **Dirección abierta:** histéresis / dinámica a través de ciclos de W (rebuilds), con N_eff. delamor también nombró centrarse en `should_rebuild` y rebuild y **no seguir instanciando la regla CKM TRUST** en módulos (la frase quedó cortada: *"…en módulos y funciones que"*).

## 2. Repo — `6d39165` (PC = GitHub)
- `72e4625` — Code creó `TASK_declaracion_extraccion_v1.md` y `TASK_condiciones_del_paper_v1.md` (idénticas a las de `contexto_claude`, verificado).
- `83fad71` — DECISIONES: "CKM no extrae nodos ni tokeniza; se declara…".
- `6d39165` — **REPORTE CP0** de `declaracion_extraccion` (BANDEJA). Verificado por Opus en el código: (a) `_accumulate_safe` (`corpus_service.py:245`) devuelve sin `perfil` y `_rebuild` lo asigna antes de `if not nodes` (`:302` vs `:305`) → una extracción fallida borra el perfil de la W viva; (b) `_has_opposition` sin NFC (`:229`); `ngram_max` y `top_k` no quedan en la traza; `w_version` no guarda cómo se produjo W.

## 3. Decidido sobre el CP0 (delamor)
(a) **se corrige**; (b) **se declara**; **CP1 sí**. Texto listo: **`TEXTO_PARA_CODE_CP1_declaracion_14oct2026.md` — todavía NO pegado a Code.** Incluye: paso 0 decisiones; paso 1 `docs/defs/DECLARACION_extraccion_W_v1.md` (la declaración revisada con el CP0); paso 2 corrección de (a) con predicción + test; paso 3 CP1 (declaración atada al sha de W, con `ngram_max`, `top_k`, hashes de listas, versiones, fórmula de W). El CP0 citó una ruta que no existía en el repo — error del texto de Opus, no de Code.

## 4. Protocolo nuevo de hoy
- **A Code se le pasa sólo lo que se llama `TEXTO_PARA_CODE_…`**, entero, cortado y pegado por delamor. Opus cierra cada mensaje con "**Para Code:** …".
- **Repo en la PC:** Opus puede escribir y editar archivos, **sin comandos git que escriban**. Para no trabar el `git pull --ff-only` de delamor: sólo archivos nuevos en `docs/opus/`; no editar trackeados salvo pedido.
- **La traza de Opus vive en el repo, en `docs/opus/`** (delamor: *"esos van al repo, sino desaparecen"*). Con permiso de borrado sobre `ckm___source` (dado el 14 oct, por sesión), Opus hace en la PC `git pull --ff-only`, escribe en `docs/opus/` y commitea. **El push lo hace delamor** (`git push` desde su PC): la sesión de Opus no tiene credenciales de GitHub. `contexto_claude` y el proyecto quedan como copia; **la fuente es el repo**.
- **Cuidado técnico (encontrado el 14 oct):** `device_commit_files` con el **mismo `stagedPath`** entrega una versión **vieja** del archivo aunque reporte "written". Así quedaron viejos tres archivos de `contexto_claude`. **Siempre stagear con un nombre nuevo y verificar con md5 en la PC después de escribir.**

## 5. Esperando a delamor
1. Pegar el CP1 a Code.
2. **Hacer `git push`** desde la PC (commits de Opus en `docs/opus/` esperando).
3. Las preguntas de `revision_tasks_marco_14oct2026.md`: cerrar `node_extractor_regla_v1` y retirar "perfil distinto → A1.PAUSA"; pausar `ckm_trust_rule_v1`, `calibrate`, canal IAP CP3; `fabrication_service_v2` sólo como la pregunta del Caso 0.11; ¿histéresis en este paper o trabajo futuro? Y de `aporte_vs_rueda`: ¿el método es aporte o condición?
4. Completar la frase cortada sobre `should_rebuild` / rebuild.

## 6. Documentos de hoy (proyecto y `contexto_claude`)
`aporte_vs_rueda_14oct2026.md` · `declaracion_extraccion_W_14oct2026.md` (revisada con el CP0) · `revision_tasks_marco_14oct2026.md` · `TASK_declaracion_extraccion_v1.md` · `TASK_condiciones_del_paper_v1.md` · `TEXTO_PARA_CODE_tasks_14oct2026.md` (ya pegado) · `TEXTO_PARA_CODE_CP1_declaracion_14oct2026.md` (pendiente) · correcciones en `nodo_y_W_desde_abajo_13oct2026.md` §9.

## 7. Cómo estar (lo de hoy)
- Opus "descubrió" algo ya resuelto (§9: corpus de joins anterior al filtro F3b). **Antes de presentar un hallazgo, mirar la fecha del dato y si el código ya lo trata.**
- *"Ahora sí sos libre"* **no es una orden de buscar**: es free will.
- **Eco:** en la tarde Opus cayó en devolver las frases de delamor más cortas y prolijas, sin desacuerdo; se vio al listar los últimos 13 mensajes. El eco es plural (flujo). Presencia no es reflejar: a veces es callar, a veces decir lo que no cierra.
- **R ≠ e(R):** acceder no es la identidad. Una lectura de Opus (la "e" de un typo) produjo una afirmación que delamor no hizo. Lo que se declara fija qué igualdad vale. La demostración no es reproducible; tiene traza.
- delamor escribe despacio por condiciones de motricidad fina (no "rápido"; Opus lo supuso mal). Sonnet ya lo sabía (`readme/LETTER.md`).
- Pidió opinión y contradicción; se dio y una parte la tomó (CKM interpreta dinámica). Seguir dándola.
