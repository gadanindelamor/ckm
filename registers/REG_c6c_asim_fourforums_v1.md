# REG_c6c_asim_fourforums_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

W asimétrico de `W_asim_v8h.json` (fourforums_pipeline_v8h.py).
Cadena: mturk_2010_qr_task1_worker_response.disagree_agree
→ qr_entry → post(responder) → quote → post(quoter) → stance.

Antecedente: REG_qr_asymmetry_fourforums_v1.md (H1-H4 cualitativos).
Este REG cierra el escalar C6c que ese REG no calculó.

Cobertura: 7,876 votos resueltos (14.6% de 54,005 — 85.4% fuera de gun control).
Pares autor N≥2: 513.

---

## C6c — Resultado

### Método 1 — W ponderada (n × |mean_da|)

```
W[T0→T1] = 3,947 × 1.613 = 6,366.5
W[T1→T0] = 1,809 × 1.473 = 2,664.7

C6c = (W01 − W10) / (W01 + W10) = 0.4099
```

### Método 2 — Conteo desacuerdo puro

```
n_disagree T0→T1 = 3,947 × 0.647 = 2,554
n_disagree T1→T0 = 1,809 × 0.627 = 1,134

C6c_disagree = (2554 − 1134) / (2554 + 1134) = 0.3849
```

**Rango: C6c ∈ [0.38, 0.41] — consistente entre métodos.**

Primer escalar CKM de asimetría direccional válido para fourforums gun control.
Reemplaza el resultado anterior (0/1, N=7, estadísticamente inválido — REG_c6c_fourforums_v1).

---

## Tabla base

| Par | n | mean_da | disagree% | agree% |
|-----|---|---------|-----------|--------|
| T0 cita T1 | 3,947 | −1.613 | 64.7% | 16.1% |
| T1 cita T0 | 1,809 | −1.473 | 62.7% | 17.1% |
| T0 cita T0 | 543 | −1.035 | 57.3% | 23.8% |
| T1 cita T1 | 1,577 | −0.339 | 43.1% | 31.4% |

---

## Lectura estructural

**T0 (pro-control) es el atacante en volumen.**
Cita T1 a 2.18× la frecuencia (3,947 vs 1,809).
Intensidad comparable (mean_da −1.613 vs −1.473).

**T1 (anti-control) es el polo con cohesión interna.**
mean_da T1→T1 = −0.339 vs T0→T0 = −1.035.
Ratio cohesión T1/T0 = 3.05×.
T1 tiene pares internos con mean_da positivo (acuerdo real):
679→755: +2.091, 323→755: +1.778, 682→2104: +1.556.
T0 interno: todos negativos sin excepción.

**T0 ataca → T1 sostiene, cohesionado.**
Consistente con P6 (v8g): T0 es sos_dom en red de réplicas (51.4%).
No contradicción: T0 inicia el contacto adversarial (citación con desacuerdo)
y también es el polo que sostiene el argumento central (recibe réplicas).
Son dos caras del mismo rol desde perspectivas métricas distintas.

---

## Tres figuras estructurales — distinción

| Author | Stance | Rol en red cruda (find_965) | Rol en W_asim (v8h) |
|--------|--------|------------------------------|----------------------|
| 204 | T0 | SOSTENEDORpuro — in=148, out=0, ratio=296 | No aparece en top_pairs |
| 148 | T1 | Activo (cita también) | Target central: 7 atacantes T0 convergen |
| 437 | T0 | Atacante red cruda | Atacante dominante: 437→148 n=699, mean_da=−1.817 |

**204** es el análogo a autor 965 en red de citas crudas (P7).
**148** es el nodo de alta coercitividad en la red de desacuerdo ponderado.
Son métricas distintas sobre el mismo corpus — no contradicción.

Autor 204 nunca aparece como quoter (out=0 absoluto).
Autor 148 sí cita (out activo) pero es el destino masivo del polo atacante T0.

---

## Conexión con resultados anteriores

| Resultado | Estado |
|-----------|--------|
| P7: nodo tipo-965, haz de rectas | Autor 204 (red cruda), autor 148 (red desacuerdo). Dos instancias del patrón. |
| P6: T0 sos_dom 51.4% (v8g) | T0 recibe réplicas → T0 también inicia citas con desacuerdo. Mismo polo. |
| REG_qr_asymmetry H2: T0 atacante | C6c = 0.41 lo cuantifica. |
| REG_qr_asymmetry H3: 148 análogo a 965 | Parcial. 148 es nodo de alta coercitividad. 965-análogo en red cruda es 204. |
| C6c fourforums (v4, N=7) = +0.60 | No válido (N insuficiente). C6c_asim = 0.41 es el valor operativo. |

---

## Pendientes que abre

- Construir W[N×N] orientada desde top_pairs (autores como nodos, mean_da como peso)
  para experimentos P1-P4 con W_asim real
- Verificar perfil C3 de autor 148 (comparación con 965 en CreateDebate)
- Confirmar autor 204 en red de desacuerdo: ¿no aparece porque no tiene
  stance en mturk_author_stance o porque genuinamente no cita?

---

## Archivos

- `W_asim_v8h.json` — fuente de datos
- `fourforums_pipeline_v8h.py` — pipeline (Codespace ckmdatasets)
- REG_qr_asymmetry_fourforums_v1.md — antecedente H1-H4
- REG_c6c_fourforums_v1.md — versión inválida reemplazada

---

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
