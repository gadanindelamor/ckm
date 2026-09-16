# TASK_delta_compresiones_coco_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, D3 — último por el orden de cascadas. DEFS_CKM_estado_actual_v11.md, sección `Δ_r_pares y Δ_r_compresiones`. Precondiciones: D6 (`6606b7c`), D1 (`f8d61ef`), D7 (`5b52992`), D2 (`341f612`), landscape_engine (`0d91e4d`).*

---

## Qué hacer

`Δ_r_compresiones` pasa a existir como objeto: la representación propia de COCO del campo que regula. Hoy no existe — `COCO._Delta` se sobrescribe con el Δ_r de Monitor en cada `observe()`.

## Estado actual (código)

```python
Monitor:  ts = thermostat.observe(self._Delta_r)      # le pasa su Δ_r
COCO:     self._Delta = Delta_new.copy()              # lo pisa
          si aplica:  self._Delta = alpha * self._Delta
Monitor:  if ts.stop_applied: self._Delta_r = thermostat.delta_state()
```

La escritura la ejecuta Monitor, pero el valor lo decidió COCO: dependencia encubierta.

## Acuerdos (delamor)

1. **Δ_r es de Monitor y Monitor es su único escritor.** Monitor es independiente de COCO: con COCO o sin COCO, se las arregla solo. **La regulación no llega a Δ_r.**
2. **COCO tiene su propia representación**, `Δ_r_compresiones`, y comprime sobre ella.

## La representación

1. **Nace en ceros**, con la W de su ciclo. COCO nace en cada rebuild, así que su ciclo coincide con el de W.
2. **Incorpora el incremento**, no el total: `Δ_r_monitor_ahora − Δ_r_monitor_leído_antes`. Dentro de un ciclo Monitor sólo suma, y en el rebuild se resetean los dos (D2). Incorporar el total volvería a pisar lo comprimido.
3. **Comprime sobre sí misma**: `Δ_coco ← α · Δ_coco`, incluyendo los pares metabolizados ya acumulados. Monitor no se entera.

Lectura del Δ_r de Monitor, nunca escritura.

## Consecuencias declaradas (no son decisiones)

- El campo de COCO **diverge** del de Monitor a partir de la primera compresión. `D_ckm_coco − D_ckm_monitor` pasa a medir esa divergencia.
- **El Δ_r de Monitor deja de estar acotado por la compresión.** En REG_wmixta_consolidado_v1 eso es la diferencia entre 62–76 con thermostat y 632 sin él. Los paneles nuevos no son comparables con los anteriores en ese campo — cascada de interpretación histórica que v4 anticipa para D3.
- La ceguera de Monitor deja de ser cancelación algebraica y pasa a ser separación de objetos: no ve las compresiones porque nunca recibe ese objeto.

## Verificación

- COCO nunca escribe en `Monitor._Delta_r`; Monitor no lo reasigna desde COCO. Verificable por inspección y por test.
- Sin compresión: `Δ_r_compresiones` == Δ_r de Monitor (sólo incrementos incorporados).
- Con compresión: divergen, y lo comprimido persiste en la observación siguiente (no se pisa con el total de Monitor).
- Δ_r de Monitor sin cota: con thermostat y sin thermostat da el mismo `Delta_r_sum`.
- Nacimiento por rebuild: COCO nuevo parte de ceros.
- Tests existentes: los que afirmen la sincronización vieja van a fallar — se revisan uno por uno, no se ajustan en bloque.

## Qué no hace

No toca `_combine_W_Delta`. No cambia el operador de compresión ni su α. No toca Δ_r de Monitor ni la metabolización. No conecta COCO al canal vivo.

## Abierto

- La forma "cruza umbral → comprime" es la heredada (v4, Parte I: *"STOP es el mismo patrón D_ckm"*). Esta TASK mueve el objeto sobre el que opera, no la forma.
- DEFS v11 §12 y v4 escriben el operador como `Δ_r ← Δ_r · (1 − alpha)`; el código hace `Δ ← alpha · Δ`. No son la misma operación. Sin resolver, no se toca acá.
- Qué significa D_ckm_coco cuando su campo ya no es el de Monitor.
