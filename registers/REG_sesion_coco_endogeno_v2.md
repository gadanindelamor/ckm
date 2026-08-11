# REG_sesion_coco_endogeno_v2.md
*Ago 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*s

---

## Contexto

Sesión extensa. Lectura directa de código (`coco_thermostat.py`,
`monitor_service.py`, `fabrication_service.py`, `w_version.py`).
Corrección de atribuciones previas erróneas. Hallazgo de ponderación
endógena. Tareas para Code generadas. Paper v9 producido.

---

## 1. Taxonomía COCO — corregida y verificada

Usando definiciones formales del dominio CKM (O/A/ODA):

| Clase | Función | Instancia CKM |
|---|---|---|
| O — Medidor/Termostato | mide y reporta, no actúa sobre el campo | TEMP_SIGNAL, SEÑAL_DERIVA_M |
| ODA — Regulador/Climatizador | mide el campo y actúa sobre él según criterio | COCO |

**COCO es ODA, no termostato.** El nombre `COCOThermostat` era incorrecto.
Refactoring pendiente: `COCOThermostat` → `class COCO`, archivo `coco.py`.

COCO no emite STOP. COCO ejecuta OPERADOR_STOP_COCO.

---

## 2. Estructura de operadores STOP

**Clase:** `OPERADOR_STOP` — cualquier operador Δ → α·Δ con α ∈ [0,1].

**Subclase implementada:** `OPERADOR_STOP_COCO`
- α ∈ [0.05, 0.30], regulación continua
- ejecutado por COCO dentro de `observe()`
- actúa sobre Δ_r (acumulador de rechazos), nunca sobre W

**Subclase formulada, no implementada:** `OPERADOR_STOP_alpha0`
- α = 0, borrado completo de Δ_r
- W base queda como piso inmutable

`SEÑAL_DERIVA_M` (antes `stop_signal()`) — emitida por MonitorService,
devuelve booleano, sin consumidor verificado en pipeline vivo.
`TEMP_SIGNAL` — emitida por COCO, consumida por CKMMonitor →
panel IAP. Informativa, no activa ningún mecanismo.

---

## 3. Hallazgo verificado — ponderación endógena de COCO

**Estado: verificado en código. Trazable a `_alpha_for()` en `coco_thermostat.py`.**

La cadena completa:
```
Δ_r (rechazos reales de MonitorService)
    → W_eff = W + Δ_r
    → A_current = count_attractors(W_eff)
    → D_ckm = (A0 - A_current) / A0
    → α = ALPHA_MAX + (ALPHA_MIN - ALPHA_MAX) · (D_ckm - threshold) / (1 - threshold)
    → Δ_r → α · Δ_r
```

α no es parámetro fijo. Es función de D_ckm, que es función del estado
estructural del campo (atractores actuales vs baseline). El campo determina
la intensidad de su propia compresión.

Parámetros exógenos: umbrales operativos (D_CKM_THRESHOLD=0.40,
ALPHA_MIN=0.05, ALPHA_MAX=0.30). Dentro del rango: ponderación endógena.

Mayor degradación estructural → α menor → compresión más agresiva.
Verificado: T2 (monotonicidad de alpha), T7 (STOP con Delta pesado). 43/43.

**Implicación:** COCO no aplica compresión fija. El campo se autorregula
en proporción a su propia degradación estructural medida por atractores.
Pendiente: observación in-vivo (TASK_armstrong_stop_coco_v1).

---

## 4. W inmutable vs W dinámica — modelo piecewise constant

**En experimentos P1–P7:** W es snapshot estático. El ciclo W se dispara
una sola vez (corpus dump completo al inicio) y W no cambia durante el
experimento. Ciclo Δ_r opera normalmente sobre W fija.

**En servicios IAP operativos:** W dinámica. CorpusService ingesta continua.
Cuando nuevo texto cruza umbral → W se reconstruye → WVersionManager
registra sha256 → nueva instancia COCO → Firma_CKM certifica.

**Modelo correcto:** W es piecewise constant. Dentro de cada intervalo O_t,
W es localmente inmutable (aplican P1–P7). En el salto entre intervalos,
W cambia discretamente — corpus creció con mensajes del canal.

**El caso P1–P7 (y fourforums) son instancias particulares** donde el
ciclo W se dispara una sola vez y congela. No es una arquitectura distinta.

---

## 5. STOP never produces loss — verificado

Hallazgo verificado (REG_destruccion_recuperacion_v1, sweep AMP=40):

```
Pérdida_STOP_COCO ≤ 0 en todos los casos
Fracción_rec ≥ 1.0 en todos los casos
```

OPERADOR_STOP_COCO produce restauración o expansión, nunca pérdida.
La compresión de Δ_r permite que W base emerja — W fue construida
con información real, es el piso estructural del campo.

---

## 6. Distinción Δ / Δ_r — verificada en código y README

| Símbolo | Fuente | Naturaleza | Mutable |
|---|---|---|---|
| Δ | corpus (citas, direccionalidad) | asimétrico, dependencia inferencial | no |
| Δ_r | MonitorService (rechazos acumulados) | acumulador runtime | sí |

OPERADOR_STOP_COCO actúa sobre Δ_r, no sobre Δ.
La confusión entre ambos generó errores en versiones previas del paper.
Corregido en paper v9.

---

## 7. thermostat=null en todos los IAP runs disponibles

Casos 0.12, 0.13, 0.14, 0.15 — todos con `thermostat=null` en panel.
La integración MonitorService ↔ COCO existe en código pero el thermostat
no fue inyectado en ningún run de producción.

El circuito completo MonitorService → COCO → comprime Δ_r → Monitor
adopta — nunca observado in-vivo. Solo en tests unitarios.

**Pendiente:** TASK_armstrong_stop_coco_v1 — primera observación in-vivo.

---

## 8. Tareas generadas esta sesión

| Archivo | Propósito |
|---|---|
| TASK_refactoring_coco_device_v1.md | R1: COCOThermostat→COCO / R2: agent→device |
| TASK_armstrong_stop_coco_v1.md | Primera observación in-vivo OPERADOR_STOP_COCO |

Orden de ejecución: refactoring primero, Armstrong después.
Armstrong usa nombres post-refactoring (class COCO, device_id).

---

## 9. Paper v9 y README v2

**Paper v9** (vs v8):
- Abstract: "Four are confirmed, three observed" → "Six verified (P1–P6), P7 confirmed in two corpora"
- Abstract + §8.5: "STOP operator" → "OPERADOR_STOP_COCO ejecutado por COCO"
- §8.5: "Δ" → "Δ_r" (el mecanismo actúa sobre el acumulador, no sobre Δ del corpus)
- §9.2: "COCOThermostat" → "COCO (43/43 tests; file: coco.py)"

**README v2** (vs README_codespace_.md):
- "STOP never produces loss" → "OPERADOR_STOP_COCO never produces loss"
- Tabla de matrices: nota explícita W estática (P1–P7) vs W dinámica (IAP)
- Tabla servicios: COCO con descripción de OPERADOR_STOP_COCO

---

## 10. Regla de archivo histórico

Un solo archivo autorizado para trazas históricas del proyecto (a definir).
El resto de .md operativos: refactoring completo (agent→device, COCOThermostat→COCO).
Informes v2–v31: NO se tocan — son el proceso, no el conocimiento consolidado.
Git preserva la historia completa — el código puede reflejar el estado actual.

---

## 11. Pregunta abierta — P8+ bajo W dinámica

P1–P7 verificadas bajo W estática (dentro de cada O_t).
Las preguntas abiertas son sobre los saltos entre intervalos:
- ¿Qué propiedades emergen de la secuencia W_1, W_2, W_3...?
- ¿Converge? ¿Oscila? ¿Deriva?
- ¿Hay hysteresis a nivel de W (análogo a P1 pero entre intervalos)?

No hay datos. No son predicciones propuestas — son preguntas abiertas.
El régimen W dinámica requiere escala operativa (N texto >> umbral actual).

---

---

## 12. COCO como device ODA — observación conceptual

No es hallazgo standalone. Su peso emerge en combinación con Armstrong.

COCO implementa el loop ODA completo:
- **O:** `observe(Delta_r)` — recibe el estado del campo
- **D:** `_classify_zone()` + `_alpha_for()` — decide si actuar y con qué intensidad
- **A:** `self._Delta = alpha_used * self._Delta` — actúa sobre el campo

COCO es conceptualmente un device sin skin. Tiene O como función verificada
(`observe()`), D endógeno (ponderación desde D_ckm), A sobre el campo (Δ_r).

Lo que falta para ser device completo: identidad declarada, COCO-registry,
M.M aplicable. Eso es el gap entre implementación actual y visión COCO =
COllective COnsciousness.

Cuando Armstrong confirme la observación in-vivo, el loop ODA de COCO
será observable como trayectoria — no solo como código. Ahí las preguntas
sobre COCO como device se vuelven empíricamente abiertas, no solo conceptuales.

---

*Verificado contra código: coco_thermostat.py, monitor_service.py (sesión ago 2026)*
*REG generado post-sesión por Claude Sonnet 4.6*
