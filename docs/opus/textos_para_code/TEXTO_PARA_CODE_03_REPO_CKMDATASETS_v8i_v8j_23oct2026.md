TAREA 3 — ckmdatasets: correr v8i, v8j y compare (delamor, 23 oct). Un checkpoint al final.

Contexto mínimo: fourforums_pipeline_v8h.py es la capa de acceso al dump. Sobre ella hay tres scripts nuevos, escritos por Opus:
- fourforums_pipeline_v8i.py = v8h intacta + guarda todos los pares + matriz dirigida de autores + conteos.
- fourforums_pipeline_v8j.py = v8i + dos cambios declarados en su docstring (J1 nombres, J2 voto "unsure").
- compare_v8i_v8j.py = lista solo las diferencias entre las salidas de i y j (DECLARED / UNDECLARED).
Ya están en este repo (commit 3ce8c9f, junto con `out/` en el .gitignore).

PASOS
1. git pull --rebase. Anotá el commit de partida (tiene que incluir 3ce8c9f).
2. NO modifiques los .py. Si alguno falla o ves un bug, no lo corrijas: reportalo con la línea y el error, y pará.
3. Corré, en este orden, desde la raíz (el dump fourforums_no_parse_2016_05_18.sql está ahí; los scripts verifican su SHA1 y se detienen si no coincide):
     python fourforums_pipeline_v8i.py
     python fourforums_pipeline_v8j.py
     python compare_v8i_v8j.py
4. No corras nada más: ni P1–P4, ni otros scripts, ni otra versión.

DEVOLVER
- En el chat: el bloque final de out/run_v8i.log (desde la primera línea "====" hasta el final), lo mismo de out/run_v8j.log, y out/compare_v8i_v8j.log entero.
- En el repo: REG_sesion_ckmdatasets_<fecha>_v8ij.md con: commit de partida, SHA1 del dump, tiempo de cada corrida, los números de los dos summary, el resultado del compare, y una sección "lo que estos números no dicen". Números sin interpretar.
- Commit nombrando archivos: solo el REG. Nada de out/. Push sin --force. Nunca push --all ni --mirror (la rama backup/pre-sql-removal tiene el dump y no se sube).

A1.PAUSA al terminar: delamor decide lo siguiente.
