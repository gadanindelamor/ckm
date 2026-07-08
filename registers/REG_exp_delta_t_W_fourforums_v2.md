# REG_exp_delta_t_W_fourforums_v1.md
*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Pregunta

¿El intervalo temporal Δt entre réplicas co-ocurrentes correlaciona
con el peso W[i,j] observado en el corpus fourforums?

Motivación: convergencia estructural entre STDP (ventana temporal
determina fortalecimiento/debilitamiento de conexión) y W/Δ en CKM
(co-ocurrencia + direccionalidad). W actual es Hebbiano clásico —
captura co-ocurrencia simétrica sin ventana temporal. Si Δt correlaciona
con W[i,j], la ventana temporal es variable informativa en este corpus.

---

## Datos

- `quote` table (fourforums SQL): timestamp via `post.creation_date`
- `W_asim_v8h.json`: pesos W[i,j] = mean_da por par (desacuerdo/acuerdo MTurk)
- Filtro: gun_disc_ids (gun control discussions)
- Script: `delta_t_wobs_v1.py`

---

## Resultado

**n pares: 100**
**rho = -0.0575**
**p-value = 0.570**
**Significancia: n.s.**

---

## Interpretación

Correlación ≈ 0. El criterio de falsación del diseño: dirección se cierra.

Δt mediana no predice W_obs en este corpus. Los pares más activos
responden rápido (0.5–2h) — propiedad del foro activo, no de la
estructura de tensión entre autores. La velocidad de respuesta no
es la variable que captura la estructura de tensión.

La hipótesis más profunda — que orden temporal y ventana importan
para W — no fue falsada en sentido estricto. Fue testada en una
dimensión particular: Δt mediana por par vs W_obs agregado.
Lo que el experimento cierra: esa operacionalización específica
de la ventana temporal no es la relevante en este corpus.

---

## Nota técnica

Par 372→148: Δt = -107.37h (negativo). Timestamp inconsistente
en el SQL — post citante anterior al post citado. No afecta
determinantemente la correlación (n=100) pero queda registrado.

---

## Estado

**EJECUTADO — Jul 1 2026**
Resultado: n.s. Rama cerrada.
Script: `delta_t_wobs_v1.py` / Output: `delta_t_wobs_v1.csv`

---

*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*
