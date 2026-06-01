# REG_hint_next_instance_v2.md

*Mayo 2026 — Hint para próxima instancia. Actualización desde sesión v27.*

---

## LEER PRIMERO — antes que cualquier otra cosa

**REG_hint_next_instance_v1.md** sigue vigente para todo lo de código (relax, sigma, D_ckm, STOP).
Este archivo agrega lo nuevo de esta sesión.

---

## HOLDINGs H1/H2/H3 — CERRADOS

No reabrir. Están cerrados en REG_mu_W_estructura_pares_v1.md y en v27 sección 40.

Resumen ejecutivo del cierre:
- mu_BB ≈ mean(fi·fj) — verificado (ratio 1.025)
- mu_AA no derivable desde fi·fj — ratio varía por par según acoplamiento semántico, no frecuencia
- mu_W no generaliza entre N porque composición A/B cambia, no N per se
- Medir mu_W empíricamente al inicio de sesión es el procedimiento correcto, no workaround

---

## Señal STOP — grados de pérdida

Hipótesis nueva (sección 41 v27), no verificada:

```
Pérdida_STOP(t) = A(t_pre) - max_alpha [ A(t_post)(alpha) ]
Hipótesis: monótona creciente en D_ckm(t_stop)
```

Experimento mínimo pendiente: sweep D_ckm(t_stop) × alpha → medir Pérdida_STOP.

**PERO:** ver punto siguiente antes de hacer ese experimento.

---

## Prioridad para próxima sesión

**"Ver funcionar el conjunto"** antes del sweep STOP.

Esto significa: antes de abrir nuevos experimentos, verificar que el sistema
completo (monitor + COCO-thermostat + garantías G1/G2/G3 + señal r) funciona
de punta a punta con los parámetros calibrados de esta sesión.

Secuencia sugerida:
1. Correr ckm_monitor.py con W_ckm_corpus_v2.json y mu_W=0.004519 calibrado
2. Verificar que r = c(S)/mu_W cae en zona G1 esperada
3. Verificar señal STOP con D_ckm diagnóstico previo
4. Solo entonces: sweep D_ckm(t_stop) × alpha

No abrir sweep STOP sin haber visto funcionar el conjunto primero.

---

## mu_AA — frontera trazada

El ratio dentro de AA no depende de fi·fj (correlación = 0.012).
Depende de acoplamiento temático específico por par.
Pares con ratio alto: conocimiento_cohesivo ↔ sentido_comun (0.772),
COCO ↔ AWARENESS (0.516), perspectiva_device ↔ atractor_patron (0.501).

Modelar mu_AA requiere estructura interna del núcleo — proyecto separado.
No bloquea nada operativo.

---

## Observación metodológica — STOP conversacional

La señal STOP tiene el mismo D_ckm subyacente en conversación que en el modelo.
Una afirmación no verificada que se corrige temprano = STOP con D_ckm bajo → restaura sin pérdida.
Esto fue verificado empíricamente en esta sesión (caso log-normal).

---

## Archivos nuevos en proyecto (subir si no están)

- REG_mu_W_estructura_pares_v1.md
- REG_stop_grados_perdida_v1.md
- CKM_Informe_Trabajo_v27.docx

---

*Clase R · subir al proyecto · formato .md*
