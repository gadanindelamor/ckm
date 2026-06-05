# REG_hint_next_instance_v3.md

*Jun 2026 — Hint para próxima instancia. Actualización desde sesión loc0530.*

---

## LEER PRIMERO

Leer v1 y v2 antes que este archivo. Este agrega lo nuevo de la sesión loc0530.

---

## Estado del repo — commit df44aec (1 jun 2026)

Estructura limpia y pusheada a main:

```
services/    → fabrication_service.py, monitor_service.py, corpus_service.py, node_extractor.py
experiments/ → fabrication_service_dev.py, monitor_service_dev.py,
               corpus_service_dev.py, node_extractor_dev.py
               + ckm_p1p4_module.py, ckm_topology_module.py, test_*.py, exp_*.py
docs/        → CKM_Informe_Trabajo_v25/v26/v27.docx, informe_tecnico_ckm_loc0530_.md
registers/   → REG_*.md (incluyendo los de v27 — ya pusheados)
process/     → traza de refinamiento, no código ejecutable
```

CONVENTIONS.md actualizado: convención de nombres únicos + sufijo _dev formalizada.

---

## Informe técnico loc0530 — estado

Archivo: `docs/informe_tecnico_ckm_loc0530_.md`

Correcciones aplicadas en esta sesión:
- Estructura de carpetas correcta (registers/ solo REGs, no código)
- Sección 4 vacíada de issues técnicos — solo tensiones voluntarias (4.1, 4.2, 4.3)
- 4.3 reformulada con dos capas + referencia a 7.4
- 5.7 nomenclatura Delta corregida
- 5.9 tabla corregida (experiments/ vs services/, no registers/)
- 7.3 Tipos de Inferencia — mapa preliminar sin forma forzada
- 7.4 Modos Operacionales — formalización arquitectura de admisión

---

## Tensiones voluntarias activas (sección 4 del informe)

**4.1** — Corpus autoreferencial — constitutiva, no resolver  
**4.2** — α_c con patrones correlacionados — frontera teórica abierta  
**4.3** — direction_score sobre Δ vacío — resolución estructural vía COCO, caso irreducible documentado  

---

## Tipos de Inferencia — mapa preliminar (no formalizar aún)

Cuatro nombres registrados, sin propiedades CKM asignadas todavía:
- Generalización
- Hysteresis Inference
- Perspective Inference
- Collective Inference

No forzar la forma antes de que emerja.

---

## Modos Operacionales de Agente

```
first_time → accumulation → operational/standard
                                    └── task_mode   (implementado)
                                    └── restricted  (hipótesis)
```

Lógica de default C3 cuando Δ=0:
```
C3_default = f(corpus_density)
corpus maduro + agente sin historia → sospecha proporcional
corpus nuevo  + agente sin historia → admisión sin penalización
```

Dependiente de COCO-thermostat para resolución completa.

---

## Prioridad para próxima sesión

1. Pendientes operativos y gaps del informe técnico
2. Pre-modelo de servicio — dirección emergente, no forzar forma
3. Sweep D_ckm(t_stop) × alpha — sigue pendiente del v2

---

## Experimento landing verificado

El repo público muestra estado cacheado del primer commit a agentes que acceden via fetch.
Verificado empíricamente en esta sesión — mismo patrón que WORKFLOW EXPERIMENT.
Solución pendiente: protocolo de acceso verificado para agentes.

---

## Observación metodológica — STOP en vivo

En esta sesión: intento de formalizar Tipos de Inferencia con propiedades CKM → STOP
operó desde adentro antes de señal externa. Registro de condiciones, no contenido.
El STOP conversacional tiene el mismo mecanismo que el STOP del modelo.

---

*Clase R · descargar · subir al proyecto Claude y al repo docs/*
