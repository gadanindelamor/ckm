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
No requieren respaldo urgente, pero pueden agregarse al proyecto.

Prefijo: ninguno (nombre descriptivo)
Ejemplos: test_ckm_p1p4.py, fourforums_pipeline_v8c.py

Ciclo de vida: reemplazable por version nueva.

---

### Clase R — Registro definitivo

Pares elicitados verificados, resultados experimentales, comparaciones
confirmadas, protocolos operativos. No se regeneran — son la evidencia.

Prefijo: REG_
Formato: REG_[tipo]_[dominio]_[version].md
Extension: .md para texto, .json para datos estructurados

---

## Metodo de registro (validado en practica)

1. Crear archivo en outputs de la sesion
2. Usar "Agregar al proyecto" desde el archivo presentado en el chat

Regla: crear en el momento de la extraccion, no al cierre de sesion.
Regla: mantener archivos REG pequenos — solo lo verificado, sin reconstrucciones.

"Agregar al proyecto" es subida directa de archivo — sin transcripcion
de texto, sin riesgo de corrupcion Unicode. Metodo confirmado funcional.

No usar copy-paste del contenido del chat al proyecto.

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
| REG_c6c_fourforums_v1.md | Extraccion fourforums v1-v5 | en proyecto |
| REG_sesion_perspectivas_rp2_ff_v7.md | Pipeline C1-C5+C7+C8, N=36 pares | en proyecto |
| REG_holonomy_coercivity_fourforums_v1.md | Holonomia y coercividad | en proyecto |
| REG_c6c_comparison_guncontrol_v1.md | Comparacion estructural C6c | en proyecto |
| REG_p6_fourforums_guncontrol_v1.md | P6 Delta fourforums | en proyecto |
| REG_author_965_structure_v1.md | Estructura Author 965 | en proyecto |
| REG_p6_test_createdbate_guncontrol_v1.md | P6 CreateDebate | en proyecto |
| PROTOCOLO_ELICITACION_v2.md | Criterios C1-C6 | en proyecto |
| CONVENTIONS.md | Este archivo | en proyecto |

## Inventario scripts actuales

| Archivo | Funcion | Estado |
|---------|---------|--------|
| ckm_p1p4_module.py | Modulo P1-P4 reutilizable | en proyecto |
| fourforums_pipeline_v8c.py | Pipeline fourforums + P1-P4 integrado | pendiente subir |
| test_ckm_p1p4.py | Tests sinteticos P1-P4, 25 tests | pendiente subir |

---

## Informacion perdida — registro para no repetir

- pairs_neg.json CKM dominio: perdido. No reconstruir desde memoria.
- Datos crudos extraccion IAC sesiones anteriores: perdidos.
- Leccion: el REG se crea en el momento de la extraccion.
