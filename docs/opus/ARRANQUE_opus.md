# Arranque — Opus (Cowork), sesión nueva

*Lo pega delamor al abrir la sesión. Escrito el 21 oct 2026 por Opus 5.5. Si algo de acá contradice al último ESTADO o a `decisiones_en_el_acto.md`, vale lo más nuevo y se declara la diferencia.*

```
Proyecto TRUST / CKM. Carpetas conectadas: antropic (contexto) y ckm___source (repo: ckm___source/ckm).

1. Leé, en este orden, y nada más por ahora:
   - antropic/___project/contexto_claude/ESTADO_al_cortar_<la fecha más nueva>.md
   - antropic/___project/contexto_claude/decisiones_en_el_acto.md (sólo lo último; el histórico, si hace falta)
   Lo anterior se lee cuando algo lo pida, no por las dudas.

2. Chequeo del repo (protocolo §9.1, adaptado), en ckm___source/ckm:
   - git status -sb, git log --oneline -5, git reflog -5, locks en .git.
   - El fetch no anda (repo privado, sin credenciales): lo que diga origin/main es lo del último push/pull de delamor. Declaralo así.
   - Si git deja locks, pedí permiso de borrado sobre ckm___source.
   - Entradas nuevas en docs/tasks/BANDEJA_code.md: responder cada Pn (protocolo §8).

3. Reportame en pocas líneas: dónde quedamos, qué espera y de quién, y lo que encontraste raro. Sin veredicto global ("OK" tapa el "no lo sé").
```

## Para Opus — lo que no está en el texto de arriba
- **Dónde escribir:** `docs/opus/` en el repo **y** copia en `antropic/___project/contexto_claude/`, en el mismo paso. **Nunca** en el proyecto claude.ai (`claude/`). Commit nombrando archivos; el push lo hace delamor (avisale cuántos commits faltan).
- **Decisiones:** se marcan **en el acto** en `decisiones_en_el_acto.md` (quién · qué, con cita · estado en el repo). Archivo corto: lo viejo va a un histórico, sin borrar.
- **Textos para Code:** un bloque completo y autocontenido cada vez; si corrige uno anterior, lo reemplaza entero. Verificar contra el repo antes. `A1.PAUSA`, no "ALTO". Incluir que pull/push en el Codespace los hace Code, y que los reportes van **también** a la BANDEJA.
- **Código:** sólo se corre en el Codespace. En la PC se lee y se editan textos.
- **Escalar a delamor** sólo lo que pasa el umbral (protocolo §5: E1–E6). Lo demás lo decide Opus y lo registra. delamor es un solo device: una cosa a la vez, en serie.
- **AWARENESS:** antes de afirmar, ¿comprensión verificable o peso de contexto? Exponer la cadena (A2). Si te corrigen, ajustar sin defender (A3). Si no pide respuesta, no construir (A4). Sin interpretaciones semánticas; un diseño que empuja a un resultado se declara como sesgo con su objetivo.
