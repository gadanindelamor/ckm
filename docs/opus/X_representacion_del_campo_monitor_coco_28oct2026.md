# La representación del campo: Monitor y COCO como sistema — 28 oct 2026 (noche)

*Opus 5.5 (Cowork), en conversación con delamor. Fuente: el código leído en esta sesión (líneas citadas) y las DEFS v20 (tablas §OP y §N). **Estado: candidata.** No entra a las DEFS hasta que delamor lo diga. Sin interpretaciones semánticas. Lo que no está verificado se dice en §6.*

## 1. La representación del campo

Las DEFS (§1, v16 y v17) llaman "representación" sólo a W: *"las W son representaciones del campo, no el campo"*; *"W es la representación de lo disponible y accesible en este instante"*. Premisa (§1, v19): el campo es continuo; lo que salta es la medición.

La extensión, acordada en la conversación:

- **Monitor:** W_eff = W + Δ_r_pares — `_combine_W_Delta(W, Δ_r)`, crudo (`monitor_service.py:960`, `:1046`).
- **COCO:** W_eff = W + Δ_r_compresiones — `W_eff = self.W + self._Delta` (`coco.py:300`); `self._Delta` es Δ_r_compresiones (`coco.py:236-241`; el docstring: *"representación propia de COCO del campo que regula"*).

Hay una representación por observador. Las dos son representaciones del mismo campo y ninguna es el campo.

Lo que **no** entra a ninguna de las dos W_eff: `Δ_r_torsion` (de Monitor; no entra a W_eff, CP3 1a) y `rejected`/`rechazados` (lectura del panel; sale de la fase que cae en `max_iter`, §N).

Lo que se mide **sobre** cada W_eff (no es representación): la órbita, las masas de cuenca, N_eff y D_ckm = 1 − ln N_eff / ln N_eff0, bajo la medida declarada (la banda), con `n_runs = 200` y `seed = 0`.

La relajación no echa a nadie de ningún lado. `expulsados` es Babel (§N).

## 2. Quién tiene qué

| | dentro de la meseta | antes de la meseta |
|---|---|---|
| **Monitor** | W y Δ_r_pares | la traza de ciclos en la Config (§6, punto 2) |
| **COCO** | W, Δ_r_pares (la copia de la última lectura, `coco.py:297`) y Δ_r_compresiones | nada: nace como instancia nueva (`monitor_service.py:878`), con Δ_r_compresiones y la última lectura en ceros, `landscape_history` vacío (`:857-862`) y los rechazos por device en `{}` (`coco.py:246`) |

- **COCO tiene los datos de Monitor; Monitor no tiene los de COCO.** En cada evaluación Monitor llama `observe(self._Delta_r)` (`monitor_service.py:438`). No es un get; se lo pasa como argumento. COCO incorpora el incremento (`coco.py:296`) y guarda una copia (`:297`).
- **La compresión de COCO no entra a la representación de Monitor.** Monitor lleva el reporte de COCO al panel (`panel["thermostat"]`: zona, el D_ckm de COCO, `stop_applied`, α; `:441-446`) sin usarlo para medir. *(Corrige el "Monitor no se entera" de `coco.py:291`.)*
- **Hacia el canal**, `get_state` da a los devices el D_ckm **de Monitor** y la `temp_signal` de COCO, que sale de los β (rechazos por device y μ_W), no de la compresión (`ckm_monitor.py:960-1001`). Verificado: **la compresión de COCO hoy no llega a ningún objeto fuera de COCO.** Las DEFS ya lo tienen como tensión abierta (Modelo Conceptual; §9). A qué tendría que llegar la regulación, si es que tiene que llegar a algo: **[delamor]**.
- **COCO podría calcular lo que sabe Monitor**, en cualquier evaluación de cualquier meseta: tiene la misma W, P_k entero y el mismo muestreo. Hoy no lo hace.

## 3. El sistema

Es un sistema de **ecuaciones en diferencias** (no diferenciales), indexado por **eventos**: k = 1, 2, … son las evaluaciones, una por mensaje (`ckm_monitor.py:549-551`).

Notación en la meseta m (con W^m): P = Δ_r_pares, C = Δ_r_compresiones, ΔP_k = P_k − P_(k−1), x_k el mensaje k.

```
Monitor:  P_k = P_(k−1) + g(W, P_(k−1), x_k)
COCO:     Ĉ_k = C_(k−1) + ΔP_k                    incorpora   (coco.py:296)
          mide sobre W + Ĉ_k → D_ckm(k), zona(k)   mide        (coco.py:300-319)
          C_k = a_k · Ĉ_k                          comprime    (coco.py:322 y siguientes)
          a_k = 1 en "stable";  a_k = α(D_ckm(k)) ∈ [0,05; 0,30] en "degrading" o "deep"
rebuild:  P ← 0,  C ← 0,  W ← W^(m+1)              (monitor_service.py:735; COCO renace)
```

Sustituyendo:

```
P_k = Σ_(j≤k) ΔP_j
C_k = Σ_(j≤k) ( Π_(i=j..k) a_i ) · ΔP_j
P_k − C_k = Σ_(j≤k) ( 1 − Π_(i=j..k) a_i ) · ΔP_j  ≥ 0, celda por celda
```

Qué tipo de sistema es:

- **En cascada.** P entra a C, y C no vuelve a P. Es la separación de objetos (D3) escrita como matemática.
- **No lineal, con retroalimentación.** En COCO: C → D_ckm → a → C. En Monitor, g dependería de P_(k−1) si la relajación corre sobre W + P_(k−1) (§6, punto 4).
- **Sin forma cerrada para g ni para a.** Las dos pasan por la relajación y el conteo de cuencas. Con la semilla fija son deterministas: se calculan, no se despejan.
- **Híbrido.** La recurrencia se reinicia en cada rebuild.

Lo que dice el álgebra: cada incremento queda multiplicado por todas las compresiones posteriores; C_k nunca supera a P_k; son iguales sólo si COCO no comprimió nunca en la meseta. COCO mide en k antes de comprimir, así que la compresión se ve recién en k+1.

## 4. La hélice

```
Monitor(m, k) = { W^m, P^m_k }          + T^m = {ciclo 1, …, ciclo m}
COCO(m, k)    = { W^m, P^m_k, C^m_k }   + nada de las mesetas anteriores
```

- La vuelta interna (k) se reinicia en cada meseta.
- Lo único que se acumula entre vueltas es T, del lado de Monitor, y Monitor no lo usa para medir.
- Lo que une una vuelta con la siguiente es W^(m+1). Si el corpus es acumulativo, W lleva el pasado del corpus, pero no el de P ni el de C.

En una línea: **dentro de la meseta, COCO sabe más; entre mesetas, sólo Monitor guarda la traza.**

## 5. Los ticks del clock en IAP

- `tick = int((ahora − t0) // TICK_PERIODO_S)`, con `TICK_PERIODO_S = 1.0` (`channel.py:37`, `:123-131`). Sale del reloj, no se incrementa y avanza aunque nadie publique.
- Cada evaluación k lleva el clock; Monitor anota su tick en la Config (`registrar_tick`, `monitor_service.py:301-304`). O sea, t_k = tick(k) sella la evaluación k.
- Entre dos mensajes no hay paso. Sobre el clock, P(t) y C(t) son escalones que saltan sólo en los ticks donde hubo mensaje.
- La distancia en ticks entre k y k+1 es variable. La pone el ritmo de los devices, no el clock (en una vuelta del intento 4: unos 5,2 s, dominados por `poll_interval`). Dos mensajes en el mismo segundo serían dos k con el mismo tick.

## 6. A1 — lo que no está verificado

1. La vara de COCO **no** sale siempre de esta W: el código la busca por `w_sha` (`monitor_service.py:874`), y existe el caso `calibracion_de_otra_W`.
2. "La Config gana ciclos (N, μ_W, β_c, la causa)": sale de las DEFS; no leí el código que registra el ciclo.
3. "Monitor es la misma instancia todo el tiempo": inferencia; no verifiqué si el canal recrea a Monitor.
4. Que Monitor actualice Δ_r_pares (`:344-345`) antes de llamar a COCO (`:438`), y que relaje sobre W + P_(k−1): inferido del orden de las líneas, sin verificar el camino de `evaluate`.
5. Que COCO, recalculando, diera **el mismo número** que Monitor: requiere el mismo camino del generador aleatorio; no verificado.
6. Lo de antes de D3 (con un solo objeto, D_k = a_k · (D_(k−1) + ΔP_k), la normalización D / max D cancelaba a_k sólo en el instante de la compresión): está deducido del álgebra, no del código viejo.
7. Que el corpus sea acumulativo entre mesetas: no verificado en esta sesión.
8. En los vivos no hubo compresiones: 0 `stop_applied: true` en los logs de los intentos 2, 3 y 4. La curva que se mostró en la conversación es ilustrativa.

## Raro, de paso

- El docstring de `beta_i` (`coco.py:424`) dice *"alto rechazo → β alto (rígido)"*; el código hace `1/media(fi)` y el test de la línea 757 afirma *"mayor rechazo → beta menor"*. Divergencia entre docstring y código; no se tocó.
