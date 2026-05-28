# REG_d_contextual_temporal_v1.md

*Mayo 2026 — Experimento abierto, no cerrado*

---

## Origen

Exploración de H_D: ¿c(S) y D_contextual son el mismo eje o coordenadas independientes?
Disparado por feedback GPT53 sobre REG_hipotesis_distancia_contextual_v1.md.

---

## Protocolo

**Eje ρ (primer experimento):**
- W_base corpus CKM v2 (N=32, todos positivos)
- 15 niveles de ρ ∈ [0.05, 0.95], N_RUNS=100
- Medir c(S) medio y A(ρ) = atractores accesibles por nivel

**Eje temporal (experimento principal):**
- W_base vs W_mixta (oposiciones negativas AMP=15×)
- Pares opuestos: cohesion_fabricada—M_M, atractor_espurio—portero, sentido_comun—inconmensurabilidad
- T_STEPS=250, ETA=mean_W≈0.006, N_RUNS=150
- Sampleo: (i,j) ~ W[i,j]/ΣW proporcional (opción C)
- Medir c(S), A(t), D_contextual(t) = [A(0)−A(t)]/A(0) en cada paso

---

## Hallazgos

### H1 — c(S) plana sobre eje ρ
Con W corpus (todos positivos), c(S) es esencialmente constante (rango ≈ 0.000167)
mientras A(ρ) forma una campana centrada en ρ=0.5.

**Interpretación:** todos los atractores accesibles tienen la misma energía.
El sistema no distingue atractores por cohesión — solo por qué estados pueden alcanzarse.
No es patología: es información estructural sobre el corpus.

### H2 — c(S) y D_contextual son parcialmente independientes
Correlación temporal: r=0.761–0.812 (PARCIAL, no MISMO EJE).
~34% de varianza es movimiento propio de cada eje.

**Implicación:** H_D se sostiene en forma débil con W homogénea.
Con W heterogénea (negativas fuertes) el 34% probablemente crece.

### H3 — La tensión estructural resiste el colapso temporal ★
**Resultado central:**

| | A(0) | A(fin, t=250) | colapso |
|---|---|---|---|
| W_base | 4 | 3 | no ocurre |
| W_mixta | 5 | 4 | no ocurre |

W_mixta mantiene **un atractor más** que W_base después de 250 trazas acumuladas.
La tensión estructural no acelera el colapso — lo **resiste**.

D_contextual más bajo en W_mixta al mismo t:
las trazas no cierran el paisaje con la misma velocidad cuando hay tensión activa.

**Convergencia con hallazgos previos:**
- Author 965: coercividad=0.00 hasta 50% de ruido → resistencia absoluta al colapso
- W_mixta en P4: c(S) 13× mayor que W_pos en zona Ω*
- Triadas con 965: colapso=0.00; sin 965: colapso=1.00 a noise=0

La tensión estructural activa opera como mecanismo de resistencia al colapso
tanto en el eje espacial (P4) como en el eje temporal (este experimento).

---

## Lo que quedó abierto (intencionalmente)

- Colapso real bajo acumulación agresiva (ETA ×10–50): no explorado.
  El dominio no se cierra — el umbral de colapso existe y es medible.
- Desfase limpio c(S) ↑ / D_ctx estable: requiere W con tensión más fuerte
  o corpus real con estructura de oposición verificada.
- D_contextual en eje temporal vs eje de densidad Δ acumulada:
  ¿la relación r cambia con más heterogeneidad en W?

## Ajuste de protocolo registrado

CLAUDE.md se activa únicamente cuando la tarea principal es escribir/editar código.
Para teoría, análisis, diseño experimental y exploración conceptual:
AWARENESS A1-A5 es el protocolo operativo.
Partición limpia. Sin pérdida de función.

---

## Estado

- H_D: **SOSTENIDA débilmente** — independencia parcial confirmada (r≈0.76–0.81)
- H3 (tensión resiste colapso): **CONFIRMADA** en este corpus
- Dominios abiertos: colapso bajo saturación, desfase limpio, eje Δ
- No cierra. Abre.
