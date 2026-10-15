# ckmdatasets: qué es publicable — 15 oct 2026
*Opus 5.5. Decidido por delamor: opción B (un repo `ckm`, dos entornos), en el orden que Opus considere; **prioridad: versiones del paper, no de infraestructura; "y mucho menos una infracción por novato en GitHub"**. Sólo lectura salvo el paso 1.*

## Paso 1 — hecho (PC, `ckmdatasets`, sin commit, sin borrar nada del disco)
Sacados del índice: los dos dumps, `trace/schema_preview.txt`, `trace/4foreums INSERTS.txt`, `bash.exe.stackdump`. Agregados a `.gitignore` (`*.sql`, `*.sql.gz`, `schema_preview.txt`, `4foreums INSERTS*.txt`, `*.stackdump`). `.gitignore` queda modificado sin commitear; el resto de `trace/` sigue en el índice como estaba. sha256: `.sql` `70fcdc64140737bb6e1cc541a720dfddf45dab1da4963e21a732c486a0853e14`; `.sql.gz` `e26e6d27a5fc88ee5837b3838f099f8268d42fe50fbbd9cd88b66dfe7744dd9c`.

## Licencia del IAC (buscado hoy)
Las páginas del IAC ([iac2](https://nlds.soe.ucsc.edu/iac2), [iac](https://nlds.soe.ucsc.edu/iac)) **no declaran licencia ni términos de redistribución**; sólo piden citar (Walker et al., LREC 2012; Abbott et al. 2016 para IAC 2.0). La descarga pasa por un **formulario** — los términos, si los hay, estarían ahí (no visto). Contacto: Rob Abbott. **Sin licencia explícita, lo prudente es no redistribuir nada a nivel de fila**, hasta leer el formulario o preguntar.

### Lo que dejó delamor: `antropic/iac.pdf` (15 oct)
Es la página general **"Website Privacy and Terms and Conditions" de UCSC** (its.ucsc.edu, actualizada 11/01/2021), no una licencia del IAC. Dice: *"No material from any Official UCSC website may be copied, reproduced, republished, uploaded, posted, transmitted, or distributed in any way, without explicit permission, except that you may download one copy of the materials on any single computer for your personal, non-commercial home use only… the use of any such material on any other website or networked computer environment is prohibited."*
- **Duda de alcance:** vale para los sitios **oficiales** de UCSC (los que llevan el sello); el mismo texto dice que los demás sitios alojados en UCSC no son oficiales. No está claro si `nlds.soe.ucsc.edu` (sitio de un laboratorio) es oficial, ni si el dataset tiene términos propios en el formulario.
- **Lectura prudente (Opus, no es asesoramiento legal):** si aplica, ni siquiera subir el dump a GitHub privado o a un Codespace ("networked computer environment") estaría cubierto sin permiso explícito. **Pedir permiso por escrito a Rob Abbott** resuelve las tres cosas: uso en un entorno de nube privado, publicación de agregados y de datos derivados (IDs de autor, posturas), y la cita.

## Clasificación
| clase | qué | va a `ckm` público |
|---|---|---|
| **Dato crudo del IAC** | dumps; `schema_preview.txt` (27 MB, 32 INSERT); `4foreums INSERTS*.txt` (563 INSERT) | **nunca** — se bajan del IAC al Codespace, `_iac/` ignorado, sha256 en el MANIFIESTO |
| **Derivado a nivel de fila** (IDs de autor, posturas, pares autor–autor con n) | `REG_stance` (IDs + postura), `W_asim_v8h.json` (`top_pairs`: quoter, responder, posturas, n), probablemente `fourforums_delta.json` | **no por ahora** — esperan el formulario/consulta |
| **Agregado** (conteos por polo, porcentajes, N_eff, tablas 2×2) | `REG_p6`, `REG_c6c`, la tabla de v8h en `lectura_pipeline_…` | sí, con cita al IAC |
| **Nuestro código y docs** | pipelines v8…v8h, `ckm_p1p4_module`, `find_965_v3`, `DOC_ckm_scripts_v1`, CONVENTIONS, logs sin filas | sí (revisar los logs: que no impriman filas) |

## Visto de paso
`REG_stance`: el autor **965** (el Type-965 de P7) figura con postura **`None`** (sin anotación de stance). Para P7 importa: el "sostenedor" no tiene postura humana.

## Orden
1. ✔ índice limpio. 2. ✔ este documento. 3. Ver los términos del formulario del IAC o preguntar a Rob Abbott (delamor decide). 4. Recién entonces el TEXTO_PARA_CODE de la migración (`datasets/`, `.gitignore`, devcontainers, MANIFIESTO). **El paper v29 no espera a nada de esto**: M4 va declarado como límite, con v8h como validación en curso.
