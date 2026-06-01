# CONVENTIONS.md — Gestion de Archivos CKM

*Mayo 2026*

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

## Inventario REG actual

| Archivo | Contenido | Estado |
|---------|-----------|--------|
| IAC_extraccion_oposicion.md | Extraccion CreateDebate gun control | en proyecto |
| REG_pairs_createdbate_guncontrol_v1.md | Pares C1-C5 CreateDebate gun control | en proyecto |
| REG_pairs_fourforums_guncontrol_v1.md | Pares C1-C5 fourforums gun control | pendiente C6c |
| REG_c6c_comparison_guncontrol_v1.md | Comparacion estructural C6c | pendiente C6c |
| PROTOCOLO_ELICITACION_v2.md | Criterios C1-C6 | en proyecto |
| CONVENTIONS.md | Este archivo | en proyecto |

---

## Principio de nombres unicos — sin duplicados entre carpetas

**Dos archivos de codigo del proyecto no deben llevar el mismo nombre.**

Un archivo con el mismo nombre en dos carpetas distintas es una fuente
documentada de confusion: agentes, instancias de Claude y el propio autor
pueden leer la version incorrecta sin saberlo. Verificado empiricamente
en sesion Mayo 2026.

Convencion de sufijo para versiones de desarrollo:

| Carpeta | Sufijo | Ejemplo |
|---------|--------|---------|
| `services/` | sin sufijo — version estable | `fabrication_service.py` |
| `experiments/` | `_dev` — version de trabajo | `fabrication_service_dev.py` |

Renombramientos aplicados (1 jun. 2026):

| Nombre anterior | Ubicacion | Nombre actual |
|-----------------|-----------|---------------|
| `ckm_monitor.py` | `services/` | `fabrication_service.py` |
| `ckm_monitor.py` | `experiments/` | `fabrication_service_dev.py` |
| `monitor_service.py` | `experiments/` | `monitor_service_dev.py` |
| `corpus_service.py` | `experiments/` | `corpus_service_dev.py` |
| `node_extractor.py` | `experiments/` | `node_extractor_dev.py` |

Regla: al crear un archivo nuevo en `experiments/` que tenga un
homologo en `services/`, agregar sufijo `_dev` desde el inicio.

---

## Informacion perdida — registro para no repetir

- pairs_neg.json CKM dominio: perdido. No reconstruir desde memoria.
- Datos crudos extraccion IAC sesiones anteriores: perdidos.
- Leccion: el REG se crea en el momento de la extraccion.
