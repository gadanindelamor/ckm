# REG_monitor_ckm_v1.md

*Mayo 2026 — Estado real del servicio de monitoreo*

---

## Concepto

Monitor stateful que evalúa coherencia fabricada en un estado CKM.
Corpus crece desde prompts del dominio que lo usa.
No busca verdad — detecta inconsistencia entre lo declarado (Δ) y lo activo (σ).

---

## Lo que funciona

**Storage JSONL:** append-only por state_id, verificado.
Cada snapshot guarda: sigma, Delta_sum, panel completo, runs individuales,
parámetros. 8000 runs guardados en experimento de 80 pasos — sin degradación.

**Trayectoria cohesiva:** sigma evoluciona desde paso anterior (no reinicializa).
W_mixta muestra fi variando 1.0 → 0.69 con nodos críticos cambiando en el tiempo.
Eso es información estructural real.

**Métodos operativos:**
- `snapshot(sigma, Delta, t)` — mide, computa panel, persiste
- `trajectory()` — lee JSONL completo
- `stop_signal(window)` — deriva señal desde trayectoria reciente

---

## Lo que NO funciona / está incompleto

**fi=1.0 saturado en W_base:**
Con W homogénea (todos positivos), fabrication_index = 1.000 en todos los pasos.
No es señal — es saturación. Causa: `_direction_score` cuenta cualquier nodo
inactivo con Delta>0 como "fabricado". Con sigma parcial siempre hay alguno.

**Δ incorrecto para este propósito:**
El experimento usa Δ_acumulado (trazas temporales proporcionales a W).
El servicio necesita Δ_declarado (dependencias explícitas del dominio).
En CKM: `ckm_graph.delta`. No son lo mismo. No están separados en el código.

**Umbrales de cuadrante no calibrados:**
`COHESION_FABRICADA` y `LOCKED` aparecen constantemente.
Los valores (c_S > 0.003, T > 0.05, A0 >= 5) son supuestos, no calibrados
desde datos reales del corpus.

---

## Lo que queda abierto por diseño

- Parseo de prompts → nodos + Δ: exploración pendiente, no implementado
- Calibración de umbrales desde corpus real con ground truth parcial
- Política de verificación de trazas: cuándo una observación entra al corpus
  como "verificada" vs "observada sin validar"
- Separación formal Δ_declarado / Δ_acumulado en la interfaz del servicio

---

## Archivos generados

- `ckm_monitor.py` — clase FabricationService, operativa con los límites arriba
- `exp_monitor_trajectory.py` — experimento con trayectoria cohesiva
- JSONL en `storage/W_base/` y `storage/W_mixta/`

---

## Estado

- Concepto: sólido
- Implementación base: funcional con limitaciones documentadas
- Δ_declarado: no conectado aún
- Umbrales: no calibrados
- No cierra. Abre.
