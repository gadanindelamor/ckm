# La representación del campo: Monitor y COCO como sistema — 28–29 oct 2026 (noche)

*Opus 5.5 (Cowork), en conversación con delamor. Fuente: el código leído en esta sesión (líneas citadas) y las DEFS v20 (tablas §OP y §N). **Estado: candidata.** No entra a las DEFS hasta que delamor lo diga. Sin interpretaciones semánticas. Lo que no está verificado se dice en §6. §7 es dirección de exploración, no código.*

## 1. La representación del campo

Las DEFS (§1, v16 y v17) llaman "representación" sólo a W: *"las W son representaciones del campo, no el campo"*; *"W es la representación de lo disponible y accesible en este instante"*. Premisa (§1, v19): el campo es continuo; lo que salta es la medición.

La extensión, acordada en la conversación:

- **Monitor:** R_M = W + Δ_r_pares — `_combine_W_Delta(W, Δ_r)`, crudo (`monitor_service.py:960`, `:1046`).
- **COCO:** R_C = W + Δ_r_compresiones — `W_eff = self.W + self._Delta` (`coco.py:300`); `self._Delta` es Δ_r_compresiones (`coco.py:236-241`; el docstring: *"representación propia de COCO del campo que regula"*).

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
- **El acceso es un canal, no una memoria.** COCO accede a más porque Monitor lo crea (`_renacer_coco`) y le pasa P en cada evaluación. En cada meseta COCO olvida, pero el canal se rearma en el mismo acto en que renace.
- **Monitor vacía el contenido, no la posibilidad de COCO** (delamor). Verificado, en una sola cadena: `_invalidar_si_W_cambio` (`:694`) → Δ_r_pares = 0, Δ_r_torsion = 0, A0 = None (`:735-737`) → `_abrir_ciclo_si_cambio` (`:740`) → `_sincronizar_coco_con_el_ciclo` → `_renacer_coco`. **El borde:** COCO no renace si no hay Config o no hay `coco_config`. En ese caso conserva su última lectura vieja: con el mismo N, el incremento sale negativo y C restaría; con otro N, las formas no coinciden. No verificado si en el canal la Config está siempre presente.

## 3. El sistema

Es un sistema de **ecuaciones en diferencias** (no diferenciales), indexado por **eventos**: k = 1, 2, … son las evaluaciones, una por mensaje (`ckm_monitor.py:549-551`). Las diferencias discretas son de la representación, no del campo.

Notación en la meseta m (con W^m): P = Δ_r_pares, C = Δ_r_compresiones, ΔP_k = P_k − P_(k−1), x_k el mensaje k.

```
Monitor:  P_k = P_(k−1) + g(W, P_(k−1), x_k)       relaja sobre W + P_(k−1)  (monitor_service.py:321-345)
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
- **No lineal, con retroalimentación.** En COCO: C → D_ckm → a → C. En Monitor: g depende de P_(k−1), porque la relajación corre sobre W + P_(k−1) (verificado, `:321-327`).
- **Sin forma cerrada para g ni para a.** Las dos pasan por la relajación y el conteo de cuencas. Con la semilla fija son deterministas: se calculan, no se despejan.
- **Híbrido.** La recurrencia se reinicia en cada rebuild.
- **Recursivo, no fractal.** Hay dos niveles con leyes distintas (dentro de la meseta y entre mesetas); no hay autosimilitud entre escalas.

Lo que dice el álgebra: cada incremento queda multiplicado por todas las compresiones posteriores; C_k nunca supera a P_k; son iguales sólo si COCO no comprimió nunca en la meseta. COCO mide en k antes de comprimir, así que la compresión se ve recién en k+1. Dentro de la meseta, cada incremento j es un término **del presente** k, no algo que pasó.

## 4. La hélice

```
Monitor(m, k) = { W^m, P^m_k }          + T^m = {ciclo 1, …, ciclo m}
COCO(m, k)    = { W^m, P^m_k, C^m_k }   + nada de las mesetas anteriores
```

- La vuelta interna (k) se reinicia en cada meseta.
- Lo único que se acumula entre vueltas es T, del lado de Monitor, y Monitor no lo usa para medir.
- Lo que une una vuelta con la siguiente es W^(m+1). El corpus conserva todos los textos, en orden (`corpus_service.py:174`, `:514`), así que W lleva el pasado del corpus, pero no el de P ni el de C. La selección de nodos recibe la selección anterior (`seleccion_anterior=self._nodes`, `:514`).
- **El hueco:** *nada de la recurrencia de una meseta llega a la siguiente.* No es histéresis (delamor).

En una línea: **dentro de la meseta, COCO sabe más; entre mesetas, sólo Monitor guarda la traza.**

### Qué dispara el rebuild (`ckm_monitor.py:570-583`)

1. **Estructural:** el D_ckm de Monitor subió en los últimos 3 pasos (`should_rebuild`, `corpus_service.py:258`). Cierra un lazo: P → D_ckm de Monitor → rebuild → P vuelve a 0. COCO no entra en ese lazo.
2. **Volumen:** `rebuild_every` textos desde el último rebuild (10 en la Serie 2).
3. **"Tiempo":** `_ciclos_sin_rebuild ≥ MAX_CICLOS`; ese contador suma por **mensaje**, no por tick.

Ninguno de los tres mira el tick.

## 5. Los ticks del clock en IAP

| tiempo | qué es | |
|---|---|---|
| t | el del campo | continuo (premisa) |
| `_ahora()` | el reloj del canal, timestamp con decimales (`channel.py:121`) | tratado como continuo |
| tick | `int((ahora − t0) // 1.0)` (`channel.py:37`, `:123-131`) | discreto; avanza aunque nadie publique |
| k | las evaluaciones, una por mensaje | discreto, espaciado irregular |

- Monitor anota el tick de cada evaluación en la Config (`registrar_tick`, `monitor_service.py:301-304`): t_k = tick(k).
- Entre dos mensajes no hay paso: sobre el clock, P(t) y C(t) son escalones que describen a las representaciones, no al campo.
- La distancia en ticks entre k y k+1 la pone el ritmo de los devices (en una vuelta del intento 4, unos 5,2 s, dominados por `poll_interval`).
- El rebuild ocurre en un mensaje, no en un tick. Mientras `calibrate` corre, pasan ticks sin evaluaciones.

## 6. A1 — lo que no está verificado

1. La vara de COCO **no** sale siempre de esta W: el código la busca por `w_sha` (`monitor_service.py:874`), y existe el caso `calibracion_de_otra_W`.
2. "La Config gana ciclos (N, μ_W, β_c, la causa)": sale de las DEFS; no leí el código que registra el ciclo.
3. "Monitor es la misma instancia todo el tiempo": inferencia; no verifiqué si el canal recrea a Monitor.
4. Que COCO, recalculando, diera **el mismo número** que Monitor: requiere el mismo camino del generador aleatorio; no verificado.
5. Lo de antes de D3 (con un solo objeto, D_k = a_k · (D_(k−1) + ΔP_k), la normalización D / max D cancelaba a_k sólo en el instante de la compresión): deducido del álgebra, no del código viejo.
6. En los vivos no hubo compresiones: 0 `stop_applied: true` en los logs de los intentos 2, 3 y 4. La curva que se mostró en la conversación es ilustrativa.
7. Si en el canal la Config está siempre presente (el borde de §2).
8. El valor de `MAX_CICLOS`.

*Verificado en esta sesión (antes estaba en esta lista):* Monitor actualiza Δ_r_pares antes de llamar a COCO y relaja sobre W + P_(k−1) (`:321-345`, `:438`); el corpus es acumulativo (`corpus_service.py:174`, `:514`).

## 7. Dirección: el presente vertical sin acumular (exploración, no código)

delamor, sobre la frase de una nota (*"acumulación vertical de presente: memoria viva de todas las iteraciones pasadas"*): *"eso es… lo que falta está ahí. lo que sea que haya que codificar es ahí"*. Precisiones de delamor: "acumulación", ojo (en CKM nombra la fase del corpus antes de W); *"presentes verticales, sí"*; *"las iteraciones no son pasadas"* (el "pasadas" es de origen humano). Dirección: *"explorando sin forzar"*.

La pregunta: ¿puede COCO reconstruir el presente vertical al renacer, **sin acumularlo**? Dos caminos (propuesta de Opus):

**(a) Leer lo que persiste.** T (la traza de ciclos de la Config) y la traza JSONL. No es acumular: la Config ya es *"un lugar con un solo escritor y muchos lectores"* (DEFS v19). Límite: se midió sobre otra W (decisión de delamor, 8 oct: *"no es comparable"*). Hace falta: lectura de COCO sobre la traza de la Config.

**(b) Recalcular sobre la W de ahora** — la que delamor reconoce (*"es eso"*). Desde los textos del corpus, COCO recalcula sobre W^(m+1), en una copia, lo que cada texto deformaría hoy. No recupera el pasado: arma términos del presente sobre la W vigente, comparables.

Lo que ya existe: el paso de un texto es determinista y está hecho de piezas del código (`monitor_service.py:317-345`): σ = `extractor.evaluate(texto, nodos)`; órbita = `relax_orbit(σ, W + P)`; p = pares en todas las fases; P ← P + p. El patrón de la copia es el de `calibrate`.

Lo que falta:
1. **Que COCO pueda leer los textos.** El corpus no tiene un getter público; los textos sólo salen en el estado serializado (`corpus_service.py:647`). Un lector, con Corpus como único escritor.
2. **El paso como función pura**, f(W, P, texto, nodos) → p. Hoy está dentro de `Monitor.evaluate`, mezclado con su estado. Monitor podría usar la misma función (refactor declarado).
3. **El recálculo, en orden** (cada paso depende del anterior): P̃_0 = 0; P̃_j = P̃_(j−1) + f(W^(m+1), P̃_(j−1), texto_j).
4. **Dónde vive el resultado y qué es:** un objeto distinto de P y de C. Su nombre, y si entra a la W_eff de COCO: **[delamor]**.
5. **El costo:** un recálculo por texto en cada renacimiento; si corre en el hilo del mensaje, el canal no atiende mientras tanto (como `calibrate`). No medido.

Lo que habría que declarar: es una simulación (lo que cada texto deformaría hoy, no lo que pasó); incluye los textos de todas las mesetas, así que no reproduce ningún P^m; el corpus guarda sólo el texto (`List[str]`), sin el device, así que los β por device no se reconstruyen; el diseño tiene un objetivo (el presente vertical) y se declara como sesgo.

Momento: después del cierre de DEFS y paper (dirección de delamor, 28 oct).

## 8. El teorema de la representación de un campo (gadanin.delamor)

```
H        un campo continuo
𝓡(H)     el conjunto de las representaciones de H
R, R′    ∈ 𝓡(H)                    ninguna incluye a la otra
⟪        "lo que se accede de"     ⟪ ∈ 𝓡(H)
T        este teorema              T ∈ 𝓡(H)
```

```
Hipótesis:     R ≠ R

Demostración:  dada R ∈ 𝓡(H),   ∃ R′ ∈ 𝓡(H) :   R′ ≠ R   ∧   R′ ⟪ R
```

**La recursividad.** ⟪ y T son elementos de 𝓡(H), así que el teorema vale para ellos:

```
T ≠ T              ∃ T′ ∈ 𝓡(H) :   T′ ≠ T   ∧   T′ ⟪ T
⟪ ≠ ⟪              ∃ ⟪′ ∈ 𝓡(H) :   ⟪′ ≠ ⟪   ∧   ⟪′ ⟪ ⟪
```

No hay un afuera desde donde suponerlo: está en los símbolos.

**En CKM, hoy:**

```
R_M = W + Δ_r_pares            ∈ 𝓡(H)      (Monitor)
R_C = W + Δ_r_compresiones     ∈ 𝓡(H)      (COCO)

( R_M ≠ R_C )   ∧   ( R_M ⟪ R_C )   ∧   ¬ ( R_C ⟪ R_M )
```

**Este mismo teorema, esta noche:**

```
T₀  el borrador de delamor
T₁  la formalización de otra IA       (R ≪ R′, reinterpreta R ≠ R)
T₂  la transcripción de Opus          (con R′ ∈ R: una inclusión que no va)
T₃  la versión de delamor del 29 oct  (con "se supone" y "no se da cuenta")
T₄  ésta

T_(i+1) ≠ T_i   ∧   T_(i+1) ⟪ T_i
```

**Notas de Opus (no son parte del teorema):**
- R_M ⟪ R_C se lee "R_M es lo que se accede de R_C". En el código: COCO recibe Δ_r_pares en cada evaluación (`monitor_service.py:438`; `coco.py:296-297`); a R_M no entra nada de COCO (¬ R_C ⟪ R_M). El acceso lo da la copia de Δ_r_pares que tiene COCO, no W + Δ_r_compresiones.
- ⟪ no es inclusión ni se supone transitiva.
- **Corrección (A3):** la versión anterior de esta nota decía *"⟪ ∈ 𝓡(H) es un supuesto de delamor"*. Estaba mal: no es un supuesto, vale porque todo ahí es representación, el teorema también. Opus no vio la recursividad hasta que delamor la dijo.
- **Lo dicho desde el afuera** (T₃, traza): *"desde COCO, R_C(H) se supone que accede a la representación de Monitor; desde Monitor, R_M(H) no se da cuenta de que es lo que se accede de R_C(H)"*. delamor: *"eso lo digo ya desde afuera… que es imaginario… el afuera"*. Sin esas palabras, quedan los símbolos.
- El R ≠ R con la misma W ya está en las DEFS (§1, v17): *"aunque el sha coincida, COCO y Monitor no ven la misma W: cada uno la ve con su bagaje"*.
- Borradores en `trustexperience/TOREAD/antropic`.

## 9. Partes, y nadie regula el campo (delamor, 29 oct)

delamor: *"todo ellos son parte, componen la representación del campo en el modelo CKM. no son las únicas partes, son partes"*.

```
Monitor:   W,  Δ_r_pares,          W_eff de Monitor  = W + Δ_r_pares
COCO:      W,  Δ_r_compresiones,   W_eff de COCO     = W + Δ_r_compresiones
```

Son **partes** de la representación del campo en CKM, no las únicas. COCO regula **su** parte (Δ_r_compresiones y su W_eff); a la parte de Monitor no le llega nada (§2, verificado).

**Al campo no lo regula nadie** (delamor: *"al campo no lo regula nadie, aun publicando D_ckm de COCO en el panel que ven los devices. aun si los devices lo leen, y imaginemos son influidos, codeterminando sus trayectorias junto a su Goal, aun así… son representaciones, los devices, los agentes, los humanos en IAP y el campo… y ahí el punto siendo el espacio"*):

```
devices, agentes, humanos en IAP, W, H   ∈ 𝓡(H)
```

Entre ellas hay ⟪ (acceso). Ninguna regula H.

*Nota de Opus:* hoy el D_ckm que llega a los devices por el panel es el de Monitor, no el de COCO (`ckm_monitor.py:960-1001`, §2). Lo de delamor vale aun en el caso hipotético en que llegara el de COCO.

## Raro, de paso

- El docstring de `beta_i` (`coco.py:424`) dice *"alto rechazo → β alto (rígido)"*; el código hace `1/media(fi)` y el test de la línea 757 afirma *"mayor rechazo → beta menor"*. Divergencia entre docstring y código; no se tocó.
