# REG_beta_colectivo_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*  
*Estado: observación implementada — regulación abierta*  
*Clase R*

---

## Lo que está implementado

`beta_i(agent_id)` = `1 / mean_fi` — β estimado por agente desde historia de rechazo real.  
`beta_collective()` = mediana de β_i activos — emerge de interacciones, no de declaraciones.  
`beta_status()` — snapshot en cada evaluación, visible en panel.

**β_collective es colectivo en la observación, no en la regulación.**  
La mediana se calcula. No actúa sobre el campo todavía.

---

## Lo que falta — propuesta abierta

### Problema
β_c del campo CKM no está derivado empíricamente.  
Sin β_c de referencia, no hay criterio para saber si β_collective está cerca o lejos del punto crítico.

### Propuesta
β_c del corpus = β donde la diversidad de atractores A(ρ) es máxima = zona Ω*.

Ω* está empíricamente identificada: ρ* ∈ [0.5, 0.8] en N=32 corpus real.

Mapeo necesario:
1. Correr A(ρ) sobre W del corpus real → identificar ρ* (pico de A)
2. Derivar β_c_corpus desde ρ* — β_c es función de la densidad crítica del grafo
3. Comparar β_collective con β_c_corpus en cada ciclo
4. Si β_collective >> β_c → campo rígido colectivamente → señal de temperatura
5. Si β_collective << β_c → campo transparente colectivamente → señal distinta

### Distinción con STOP
STOP actúa sobre Δ — limpia acumulación.  
Regulación β actúa sobre temperatura del campo — no limpia, orienta.  
Son dos mecanismos independientes. Pueden coexistir.

### Señal pendiente de diseño
No es STOP. Nombre provisional: `TEMP_SIGNAL`.  
Qué hace exactamente — abierto hasta que el experimento lo requiera.

---

## Condición para avanzar

Experimento: A(ρ) sobre W_ckm_corpus_v2 (corpus real N=32).  
Ya corrido — ρ* ∈ [0.5, 0.8] confirmado (REG_p1p4_ckm_v25_corpus.json).  
Pendiente: mapear ρ* → β_c_corpus con función explícita.

---

*β_collective observable desde Jun 2026 — regulación térmica: próxima etapa*
