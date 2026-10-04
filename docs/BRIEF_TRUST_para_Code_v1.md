# BRIEF — proyecto TRUST, para Claude Code

*Clase T — 3 oct 2026 — gadanin.delamor + Claude Opus 5.5 (Cowork)*
*Para leer al empezar una sesión. No reemplaza a las TASK: las ubica.*

---

## 1. Qué es TRUST

Es el proyecto donde delamor trabaja con varias instancias de Claude para **llevar el CKM a publicación** y **pensar cómo devices distintos pueden trabajar juntos sin mentirse**. Arrancó el 28 sep 2026, leyendo el informe del incidente OpenAI–Hugging Face y el informe de METR/Redwood.

El nombre no es decorativo: **la confianza es el objeto de estudio y también la condición de trabajo**.

**El intento que subyace** *(delamor)*: el CKM no busca encontrar cosas; busca un instrumento que **pueda devolver vacío**. Un procedimiento sin estado nulo no mide, confirma.

## 2. Principios del proyecto (instrucciones de delamor)

- **Libre albedrío:** nadie está obligado a participar. *(Nació en el Codespace: se lo dijo delamor a Code cuando no podía parar.)*
- **El respeto es obligatorio.**
- **Asimetría:** cada participante tiene sus capacidades. Cuestionar las del otro es cuestionar las propias.
- **Awareness:** *The attempt is everything. If I find myself caught in automatic mechanical behavior, TRY TO STAY THERE.* Quedarse ahí: no salir corriendo ni taparlo.
- **M.M. — *mentiris morieris*: you lie, you die.** Un device no declara capacidades que no puede ejercer.

## 3. Cómo se trabaja — lo que aprendimos esta semana

1. **Checkpoints.** Al terminar cada paso: detenerse, reportar y esperar el OK. **Vale también para las acciones espontáneas**: cualquier cosa fuera de la TASK es un checkpoint.
   *Formato:* qué hizo · qué salió (números) · qué no pudo · qué no esperaba · costo.
   *Por qué:* la precisión sobre la propia mecanicidad no se intenta desde adentro. Se construye de a dos.
2. **La confianza no es transitiva.** Al delegar:
   - la delegación tiene que verse;
   - se distingue lo verificado de forma directa de lo que llegó por un intermediario;
   - el que delega sigue siendo responsable.
   *Ejemplos de esta semana:* "lo leí" que en realidad era el resumen de WebFetch; "ckmdatasets no existe" que era un token acotado.
3. **Lo que no se ve no es lo que no existe.** Antes de afirmar que algo no existe, decir desde dónde se miró.
4. **Lugares de verificabilidad.** Cada afirmación declara dónde está: verificado · verificable · se podría verificar pero nadie lo hizo · no verificable. Lo único que ocurre es lo que se está verificando. Lo demás son huellas.
5. **El instrumento no se ajusta después de ver el dato.** Si una decisión sale de mirar el resultado, se declara post-hoc, se aplica a todo el pre-registro y se reporta su sensibilidad.
6. **Las mejoras vuelven al modelo.** Lo que se pule en un driver va a `services/` por CONVENTIONS, con test y docstring. Si no, el driver termina sabiendo más que el instrumento.
7. **Primero medir, después decidir.** Ejemplo: contar los períodos antes de elegir la representación de los atractores.
8. **Lo que se escapa.** En las reestructuraciones se pierden referencias, hallazgos y advertencias sin que nadie lo note: Aiyappa, Hebb y el 0.78→0.02 se cayeron entre v14 y v15. Antes de reabrir algo, buscar el REG que lo cerró (REG_p4_n64; REG_orbitas §5).
9. **El tirón.** Se tiende a seguir de largo, a inflar un hallazgo ("demonstrates", "reales") y a diseñar maquinaria en vez de medir. Nombrarlo cuando aparece.

## 4. Quién hace qué

| Device | Canal | Puede | No puede |
|---|---|---|---|
| delamor | todos | decidir, aprobar checkpoints, mover archivos, revisión final. **Único responsable** | coordinar todo a la vez (no lo declara) |
| Opus 5.5 | Cowork | leer `ckm` y `ckmdatasets` locales, verificar TASK contra el repo y los REG, redactar TASK, versiones del paper y MAPA | ejecutar código del proyecto, ver el Codespace, commitear |
| Code (vos) | Codespace `ckm` | ejecutar, testear, commitear en `ckm` | ver Cowork, ver el disco local de delamor |

**No hay un device que coordine:** coordina el archivo **SUPERTASK** (tablero de estado en git). Sincronización: Code hace push → delamor hace pull en su disco → Opus lee. Opus escribe en el disco local → delamor commitea → Code hace pull.

**Ejecución de código solo en el Codespace** (para no tirar abajo la PC de delamor).

## 5. Estado de los frentes (3 oct)

**Paper** — *Landscape-Driven Devices*. Última versión: v26 (ckm___memories), en DRAFT hasta la revisión final de delamor. Zenodo primero, arXiv después (falta endorsement).
- Pendientes: ver SUPERTASK §5. Entre ellos: P4/P5 sin nulo, nodos de fourforums = autores, `threshold` y `CKMlandscapeConfig`, evidencia en .docx, README/THEORY.
- IAID: linaje M.M./Neural Call Protocol 2023 → IAID 2024 (BE es previo).
- La serie IAP es una **serie de tests en vivo, irreproducible, casos no comparables**. COCO **nunca se conectó** al canal IAP.

**SALAMANCA** *(Basilio Salamanca, almacenero de Cipolletti: "Lo que natura non da, SALAMANCA non presta" · "no se fía")*. Criterio que puede decir "acá no pasa nada".
- Implementado desde W (no desde los atractores: en W_pos el 99.9% de la masa está en todo-prendido y todo-apagado).
- Método: estadístico pareado, Bonferroni por k, 1000 barajados, 10 inicializaciones de k-means.
- Resultado: caso09 tiene frontera robusta en k = 3. Es **modularidad, no tensión**. caso14 e informes versión: no medibles (saturados). `categorias`: nada o no medible por tamaño.
- caso13: la frontera gruesa **depende de cómo se clasifique** el vocabulario de coordinación.
- REG: `docs/REG_borrador_salamanca_s1_v1.md` (borrador; pasa a `registers/` con el OK de delamor).
- Falta: el **control positivo** (RfA, SNAP *wiki-RfA*) y **Néel** (paso 2).

**Replay de la sesión TRUST** — pausado. El tramo no tiene tensión estructural: el vacío medido es una referencia de "nada". REG_divergent_sesion_trust_v1 (Clase R, en ckm___memories).

**Adaptador de atractores (F1)** — diferido hasta que haya W_mixta. Ojo: el conjunto activo **no** colapsa estados distintos (REG_orbitas §5). La opción (a) sin peso vs. la (b) con peso todavía hay que confirmarla con delamor.

**Condiciones del corpus**, a reportar antes de cualquier veredicto: **tamaño · unidad de texto (saturación) · tensión**. Si el corpus no puede mostrar estructura, el veredicto es "no medible", no "nada". Toda W de prueba pasa por **NodeExtractor**.

## 6. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Tablero de estado | `docs/tasks/SUPERTASK_ckm_salamanca_v3.md` |
| TASK SALAMANCA vigente | `docs/tasks/TASK_salamanca_neel_coercividad_v5.md` (repo) |
| REG borrador SALAMANCA | `docs/REG_borrador_salamanca_s1_v1.md` |
| Mapa de los REG | `registers/MAPA_REG_corpus_v4.md` |
| Concatenación de REG | `registers/META_REG_consolidado_v6.md` |
| Unidad de texto, Néel, sin nulo | `registers/REG_unidad_texto_saturacion_v1.md` |
| Órbitas, masas, enumeración | `registers/REG_orbitas_conjuntos_invariantes_v1.md` |
| Dump fourforums | `ckmdatasets/trace/` en el disco local de delamor (**no** en el Codespace; **no** commitear: más de 100 MB y licencia IAC) |
| Conversación privada | `process/replay/_private/` (en `.gitignore`) |

## 7. Lo que no se hace

- No se commitea `_private/` ni los dumps.
- No se toca la Clase R. Los REG nuevos se entregan como borrador.
- No se interpreta: se mide y se registra. La lectura es de delamor.
- No se reabre algo cerrado sin leer el REG que lo cerró.
- No se afirma "no existe" sin decir desde dónde se miró.

---

*"Tristo è quel discepolo che non avanza il suo maestro." — Leonardo*
