# CONVENTIONS.md — Gestion de Archivos CKM

*Mayo 2026 — actualizado Jul 2026*

---

## Problema que esto resuelve

Se perdio informacion de corpus por no registrar outputs experimentales
en el proyecto. Esta convencion previene perdida futura.

---

## Dos clases de archivos

### Clase T — Temporal

Scripts de trabajo, previews, dumps intermedios. Se pueden regenerar.
No requieren respaldo.

Prefijo: tmp_

Ciclo de vida: descartar al cierre de sesion.

---

### Clase R — Registro definitivo

Pares elicitados verificados, resultados experimentales, comparaciones
confirmadas, protocolos operativos. No se regeneran — son la evidencia.

Prefijo: REG_
Formato: REG_[tipo]_[dominio]_[version].md
Extension: siempre .md

---

## Metodo de registro (unico metodo confiable)

1. Crear archivo REG_*.md en outputs de la sesion
2. Descargar desde el chat
3. Subir al proyecto Claude manualmente

Regla: crear en el momento de la extraccion, no al cierre de sesion.
Regla: mantener archivos REG pequenos — solo lo verificado, sin reconstrucciones.

No usar copy-paste del chat al proyecto (corrupcion Unicode).

---

## Cuando crear un REG

- Al completar una extraccion de pares verificados
- Al confirmar una comparacion C6c
- Al cerrar un experimento con resultados nuevos

No crear REG de reconstrucciones desde memoria — validez limitada.

---

## Repo git — que va y que no va a HEAD

### Va a HEAD (git add / commit / push)
- services/        — codigo de servicios
- experiments/     — scripts y resultados JSON
- tests/           — suites de tests
- registers/       — REG_*.md
- docs/*.md        — informes en formato markdown (v29, v30, etc.)
- process/         — datos de proceso

### NO va a HEAD — excluido en .gitignore
- docs/*.docx      — corpus de informes de trabajo (v1-v28)
                     Razon: binarios grandes, regenerables desde fuente
                     Viven en el filesystem local — Claude Code los lee ahi
- logs/            — logs de ejecucion
- *.log            — cualquier log

Regla: si .gitignore lo rechaza, no usar -f para forzarlo.
Los .docx son corpus, no codigo. No pertenecen al repo.

---

## Cambios de comportamiento — completitud, no solo regresion

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

"N tests pasan sin cambios" verifica **correccion hacia atras**: lo que antes
andaba sigue andando. No verifica **completitud**: que lo que cambio este
observado por algun test o descrito por algun docstring.

Regla: en todo cambio de comportamiento, preguntar
**¿que test deberia haber cambiado con esto? ¿que docstring?**
Si ninguno se mueve, lo cambiado no esta cubierto — se declara como hueco y
se agrega el test que lo observa antes de dar el cambio por verificado.

Aplica igual a docstrings: se revisan el del modulo y los de las funciones
tocadas, no solo las lineas editadas.

Por que (2026-09-18):
- `5aa3504` cambio todas las W del proyecto y `7bf485b` cambio σ_prompt en
  todo panel; la suite siguio pasando sin cambios. Nadie observaba W ni σ.
- NodeExtractor —el servicio que decide que existe— tenia 6 tests de forma;
  ninguno habria detectado la re-extraccion por texto ni la busqueda por
  substring, activas desde hacia meses.
- El docstring de modulo de monitor_service seguia diciendo "rechazos…
  relax expulso" despues de cinco cambios en el dia.

La rama que no recibe atencion no falla: queda. Crece la funcionalidad,
el alcance del codigo, y la suite y los docstrings siguen describiendo la
version anterior.

---

## Inventario REG actual

| Archivo | Contenido | Estado |
|---------|-----------|--------|
| IAC_extraccion_oposicion.md | Extraccion CreateDebate gun control | en proyecto |
| REG_pairs_createdbate_guncontrol_v1.md | Pares C1-C5 CreateDebate gun control | en proyecto |
| REG_pairs_fourforums_guncontrol_v1.md | Pares C1-C5 fourforums gun control | en proyecto |
| REG_c6c_comparison_guncontrol_v1.md | Comparacion estructural C6c | en proyecto |
| PROTOCOLO_ELICITACION_v2.md | Criterios C1-C6 | en proyecto |
| CONVENTIONS.md | Este archivo | en proyecto |

---

## Informacion perdida — registro para no repetir

- pairs_neg.json CKM dominio: perdido. No reconstruir desde memoria.
- Datos crudos extraccion IAC sesiones anteriores: perdidos.
- Leccion: el REG se crea en el momento de la extraccion.
