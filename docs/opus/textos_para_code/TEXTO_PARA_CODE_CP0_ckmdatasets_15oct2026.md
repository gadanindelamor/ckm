DELAMOR A CODE (texto de Opus):

Soy delamor. **Va después del freeze del CP-E/CP-M**, no antes. `git pull` antes de nada.

**Decisión mía (15 oct), para DECISIONES en commit propio:** se empieza a vincular `ckmdatasets` con `ckm`, desde el Codespace. Los dumps son zips de SQL bajados del IAC; el pipeline **lee el `.sql` directo** (sin MySQL) — por eso v8b…v8g: *"no son tan exactas los schemas, hubo que rengar con claves"*. *"Está todo en el repo; lo que falte, en GitHub, y backups."* El parser del dump es **un operador más de ese productor** y se declara. El dump **no se redistribuye** (licencias: preprint); se baja de la fuente o lo sube delamor, y se declara con URL, fecha y sha256.

**CP0 — sólo lectura. Nada vivo cambia; no se corre el pipeline todavía.**

1. **Predicción antes**, commiteada: qué esperás encontrar en los puntos 2–5.
2. **Acceso:** clonar `https://github.com/gadanindelamor/ckmdatasets` **al lado** de `ckm` en el Codespace (no adentro, no submódulo). Si el token del Codespace no alcanza, **A1.PAUSA** y reportá qué hace falta (por ejemplo permiso en `.devcontainer/devcontainer.json`); no lo crees sin orden.
3. **Qué hay:** qué está en GitHub y qué no. Los dumps (`fourforums_no_parse_2016_05_18.sql`, 544 MB; `.gz`, 164 MB) superan el límite de GitHub: verificá si están (LFS, release) o no. Si no están, decilo; no los bajes todavía.
4. **El productor, leyendo `fourforums_pipeline_v8g.py`** (y `find_965_v3.py`, `ckm_p1p4_module.py` si los usa), en el formato de `docs/defs/DECLARACION_extraccion_W_v1.md`:
   - cómo parsea el dump: tablas, claves (incluida la compuesta de `post_id`, `ac6211f`), qué hace con lo que no calza;
   - qué es un nodo (¿autor?), qué es una unidad, cómo se arma W;
   - **de dónde sale el signo**: ¿marcadores, anotaciones del IAC (stance, quote/disagreement), otra cosa? Es lo que más importa para M4;
   - qué tópicos hay en el dump (no sólo gun control) — contar, sin analizar;
   - dependencias y versiones; qué ejecuta.
5. **Otros datasets del IAC** nombrados en `trace/FORUMS_IACv2_README.txt` (createdebate, createdebate_released, convinceme): sólo nombrarlos y decir si el parser serviría o haría falta otro. No bajarlos.
6. REPORTE en la BANDEJA de `ckm` y **A1.PAUSA**.

Reglas de siempre: no se ejecuta código ajeno; en `ckmdatasets` no se escribe nada en este CP; archivos nombrados uno por uno al commitear, sin `git add -A`; sin regresiones; no se toca el gate (`f96c234`); donde se duda, A1.PAUSA.
