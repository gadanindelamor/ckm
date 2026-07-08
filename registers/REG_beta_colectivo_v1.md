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

---

## Traza de W — puntos de invalidación de β_c_corpus

*Agregado Jun 30 2026*

### Problema

β_c_corpus es estimado, no derivable. Su cálculo requiere correr A(ρ) sobre un W específico e identificar ρ*. Si W cambia — por crecimiento del corpus, por adición de nodos, por recalibración de pesos en el proceso verificador continuo — el β_c_corpus calculado previamente queda stale sin que nada lo señale.

El corpus es dinámico y compartido. W no es estático entre instancias del thermostat.

### Decisión

No se versiona W como objeto entero. Se registran **puntos en la traza de W** — marcas livianas que señalan cuándo W cambió lo suficiente como para invalidar β_c_corpus vigente.

Cada punto de traza contiene mínimo:
- Referencia al evento causal (REG o circunstancia que produjo el cambio)
- `corpus_size` en ese momento
- Estado de β_c_corpus: vigente → invalidado

### Qué hace la marca

No reconstruye β_c_corpus. No lo recalcula automáticamente.

Señala: *el valor que tenés ya no corresponde al W actual.*

El recálculo es un evento posterior, separado, ejecutado cuando alguien lo requiere. La marca solo declara la necesidad.

### Por qué no es derivable

Corpus dinámico + compartido → W cambia entre instancias → ρ* puede estar en otro lugar → no hay función que infiera el nuevo β_c_corpus desde el anterior más un delta. Requiere estimación completa cada vez.

### Relación con STOP

STOP opera sobre Δ. Las marcas en la traza de W operan sobre W. Son planos que no se cruzan. Un STOP no agrega ni elimina marcas en la traza de W. Un cambio real de W no dispara STOP.

La distinción es operacional. W y Δ son ontológicamente la misma cosa.

---

*β_collective observable desde Jun 2026 — regulación térmica: próxima etapa*
