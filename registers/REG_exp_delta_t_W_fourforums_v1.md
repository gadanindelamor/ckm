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

## Datos requeridos

- `quote` table (fourforums SQL): timestamp de cada cita
- `W_asim_v8h.json`: pesos W[i,j] por par de autores
- Filtro: gun_disc_ids (gun control discussions)

---

## Tarea atómica para Claude Code

```
Extraer de fourforums SQL:
  tabla quote — verificar nombre exacto del campo timestamp
  para cada par (author_i, author_j) en gun_disc_ids
  calcular Δt = timestamp_post_citante - timestamp_post_citado (segundos)
  agregar por par:
    delta_t_mediana
    delta_t_media
    count (n interacciones)
    W_obs desde W_asim_v8h.json

output: CSV con columnas
  [autor_i, autor_j, delta_t_mediana, delta_t_media, w_obs, n_interacciones]

calcular:
  Spearman(delta_t_mediana, w_obs)
  p-value
  scatter plot delta_t_mediana vs w_obs (log scale en ambos ejes)
```

---

## Criterio de falsación

| Resultado | Interpretación |
|---|---|
| correlación ≈ 0, p > 0.05 | Timing no agrega información sobre W. Ventana temporal no es variable relevante en este corpus. Dirección se cierra. |
| correlación < 0, p < 0.05 | Δt corto → W alto. Consistente con STDP. Réplicas rápidas fortalecen conexión. Dirección se abre. |
| correlación > 0, p < 0.05 | Réplicas lentas → mayor peso. Inesperado. Requiere interpretación antes de continuar. |

---

## Criterio de éxito

CSV generado + coeficiente Spearman + p-value + scatter plot.

---

## Conexiones abiertas (no decisiones)

- Si confirmado: base empírica para incorporar Δt como variable
  en weighted event graph sobre corpus CKM.
- Si confirmado: posible mecanismo para intervalos de confianza
  sobre "secuencia de tiempo" como parámetro (punto 4 — gadanin.delamor).
- No implica cambio a W ni a NodeExtractor — solo observación.
- Weighted event graphs (literatura): arista (i, j, t, w) con
  Δt-connectivity como restricción. Formalismo disponible,
  no requiere construcción nueva.

---

## Estado

Pendiente ejecución — requiere Codespace ckmdatasets disponible.
Diseño completo. Tarea atómica lista para Claude Code.

---

*Jul 1 2026 — gadanin.delamor + Claude Sonnet 4.6*
