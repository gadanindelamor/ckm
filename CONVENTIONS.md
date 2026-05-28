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

## Principio de reporte — ratio, no diferencia absoluta

**El ratio es lo que importa. La diferencia absoluta opaca lo que se deriva de ella.**

La diferencia absoluta depende de la escala — cambia con la normalización.
El ratio es invariante a la escala. Es lo que el campo hizo con lo que tenía.

Este principio no es preferencia de presentación. Es derivación directa de la divergencia como operador CKM:
la divergencia mide tasa de separación, no distancia. El ratio preserva esa tasa.
La diferencia absoluta la destruye.

Regla operativa:
- En comparaciones experimentales: reportar ratio primero, diferencia absoluta solo si aporta contexto adicional.
- Nunca reportar diferencia absoluta como hallazgo principal en resultados CKM.
- Ejemplos correctos: "fi ×2.25", "c_S ×2.7", "W_mixta produce c(S) 13× mayor que W_pos"
- Ejemplos incorrectos: "fi subió 0.417", "c_S aumentó 0.129"

La diferencia absoluta opaca la divergencia. El ratio la expone.

---

## Principio de distinción — invariante de código vs resultado experimental

**Los tests testean invariantes de código. Los REG registran resultados experimentales.**

Un invariante de código es una propiedad que el sistema garantiza en cualquier corpus válido:
- fi ∈ [0, 1]
- Δ_r no decrece
- W simétrica
- W_mixta.neg_frac > W_pos.neg_frac cuando hay marcadores

Un resultado experimental es una medición sobre un corpus específico:
- fi(W_mixta) = 0.750 vs fi(W_pos) = 0.333 → ratio ×2.25 (sesión 32, gun control)
- c_S(W_mixta) ×2.7 para prompt de tensión

Codificar un resultado experimental como invariante de código produce tests frágiles
que fallan cuando el corpus cambia — incluso si el sistema funciona correctamente.
La fragilidad no indica bug: indica que se confundieron las dos categorías.

Regla operativa:
- Tests: propiedades que el código garantiza estructuralmente.
- REG: ratios, magnitudes, comparaciones sobre corpus específicos.
- Si un test falla porque el corpus cambió → mover la aserción al REG, no parchar el corpus.

---

## Informacion perdida — registro para no repetir

- pairs_neg.json CKM dominio: perdido. No reconstruir desde memoria.
- Datos crudos extraccion IAC sesiones anteriores: perdidos.
- Leccion: el REG se crea en el momento de la extraccion.
