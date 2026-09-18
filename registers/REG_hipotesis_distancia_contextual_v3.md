# REG_hipotesis_distancia_contextual_v3.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Continúa `REG_hipotesis_distancia_contextual_v2.md` (`dc63dd6`). v2 dejó
§11 descrito y no ejecutado; acá se ejecuta, y lo que aparece corrige una
condición registrada.*
*Todo lo medido es de esta sesión, en Codespace ckm, con código commiteado.*

---

## Descripción

v2 declaraba faltante la operación d(σ). Se implementó y se midió sobre
caso09. El resultado principal no es d(σ): es que la W de referencia tiene
**nodos aislados**, que esos nodos aparecen en la mitad de las W del
proyecto, y que Δ_r los va acoplando durante el run — con lo cual el factor
que introducen **no es constante** y deforma D_ckm, no solo su valor.

Eso corrige la condición empírica registrada en `c32d22a` (caso09,
bootstrap 12).

---

## 1. d(σ) ejecutado (v2 §11)

`basin_distance` en `services/landscape_engine.py` (`53b4d8c`):

```
d(σ) = mínimo número de flips que cambian la ÓRBITA a la que relaja σ
```

Se comparan **órbitas**, no estados: caer en la otra fase de la misma
órbita de período 2 no es cambio de cuenca. Eso resuelve por definición el
abierto de v2 (*"qué es cambiar de órbita cuando el estado devuelto es una
fase"*) — declarado, no descubierto. Búsqueda exhaustiva hasta k=2; desde
ahí muestreada y marcada como cota superior.

Sobre caso09, 200 muestras de σ₀, búsqueda exacta:

| W | órbitas | período 2 | d = 1 | d = 2 |
|---|---:|---:|---|---|
| natural, N=20 (24 textos) | 57 | 33 | 55 órb. — 81% de la masa | 2 órb. — 19% |
| bootstrap 12, N=32 | 56 | 12 | 56 órb. — **100%** de la masa | — |

Flips simples que cambian de órbita, por tipo de nodo:

| W | total | nodo aislado | h = 0 | acoplado |
|---|---:|---:|---:|---:|
| N=20 | 498 | 0 | 74 | 424 |
| N=32 | 514 | **168** | 33 | 313 |

Sin los triviales, d = 1 igual domina: casi todo estado de atractor está a
un flip de otra cuenca en estas W (pesos chicos, campo local cerca de 0).

*Estado: verificado.*

---

## 2. Nodos aislados

Un nodo **aislado** tiene su fila de W entera en cero. Su campo local es
siempre 0 y conserva el valor que tenga. Con `a` aislados, cada atractor
acoplado aparece en **2^a copias triviales**.

La W de bootstrap 12 tiene 3: `conversation`, `about`, `low`.

`experiments/aislados_por_bootstrap.py` (`53b4d8c`): 15 corpus distintos
(casos IAP + WARMUP_TEXTS), cada bootstrap posible, 217 W.

| | |
|---|---|
| W con al menos un aislado | **113 / 217 (52%)** |
| aislados por W | media 1.12, desvío 1.65 |
| máximo | 10 / 32 (caso11_run2, k=4) |
| corpus sin ninguno | 1 / 15 |

Se concentran temprano —N ya en 32, pocos textos— y tienden a bajar con
más textos, no monótono. caso09: 3 en k=12, 1 en k=16.

**Mecanismo probable, no verificado:** `top_k=32` fija N aunque los textos
todavía no conecten ese vocabulario; un término entra por TF-IDF sin
co-ocurrir con ningún otro de los 32.

**Límite de dominio:** otro dominio de datos (fourforums, CreateDebate) no
está en el repo — sus pipelines leen un dump SQL que pertenece a
`ckmdatasets`. Los 15 corpus son conversaciones entre devices y texto de
teoría CKM.

*Estado: frecuencia verificada; mecanismo propuesto.*

---

## 3. Si el factor se transfiere *(delamor: es solo el valor, y el ratio se
mantiene — para estas métricas; el tema es si se transfiere, y si las
normalizaciones deforman otras métricas, no solo en valor)*

Por álgebra, con el factor 2^a **constante**:

| métrica | efecto |
|---|---|
| D_ckm = (A0 − A)/A0 | se cancela |
| D_masa lineal = (N_eff0 − N_eff)/N_eff0 | se cancela |
| ln N_eff0 − ln N_eff = H₂(t0) − H₂(t) (v1, v2 §2) | se cancela |
| **D_masa log = 1 − ln N_eff / ln N_eff0** | **no se cancela**: `a·ln2` se suma arriba y abajo y comprime hacia 0 |
| d(σ) | no es factor: cada aislado agrega un camino de 1 flip |
| c(S), μ_W_global | no es factor: promedian sobre pares y los del aislado son 0 — diluye, mueve β_c |

La variante log es la que v2 §2 identifica con la hipótesis de mayo. La
diferencia sin normalizar cancela; **la normalización es la que deforma.**

*Estado: álgebra verificada; efecto sobre c(S)/μ_W/r no medido.*

---

## 4. El factor no es constante

Un aislado declarado por un prompt nunca es expulsado (campo 0). Pero si
otro nodo del mismo prompt lo es, el par se metaboliza: Δ_r[aislado, otro]
crece, y `_combine_W_Delta` lo lleva a W_eff. **El nodo deja de estar
aislado en el paisaje que Monitor mide.**

caso09, bootstrap 12, W congelada:

| msj | aislados en W_eff | A | D_ckm | A sin aislados | D sin aislados |
|---:|---:|---:|---:|---:|---:|
| 12 | 2 | 25 | 0.00 | 11 | 0.00 |
| 13 | 2 | 16 | 0.36 | 4 | 0.64 |
| 14 | 2 | 19 | 0.24 | 5 | 0.55 |
| **15** | **1** | 12 | **0.52** | 6 | 0.45 |
| 17 | 1 | 10 | 0.60 | 6 | 0.45 |
| 22 | 1 | 7 | 0.72 | 5 | 0.55 |
| 24 | 1 | 7 | 0.72 | 5 | 0.55 |

`low` ya estaba acoplado al fijar A0 (msj 12); `conversation` se acopla en
el msj 15. Desde ahí A pierde un factor 2 que A0 conserva: **el cociente no
se sostiene.**

Límites de esta separación: sacar los aislados cambia también el espacio
donde se muestrea σ₀ (no es "la misma medición menos el factor"); sin
aislados A cae a 4–11 y la grilla de D es gruesa (0.09–0.25); un caso, un
seed.

Es el mismo patrón que v2 §9: **el campo sobre el que Monitor mide está
constituido por haber medido** — acá, hasta la dimensión efectiva del
espacio de estados.

*Estado: verificado (una corrida).*

---

## 5. Corrección de lo registrado

`c32d22a` registró como condición empírica para caso09:

> bootstrap = 12 … D_ckm sube de 0 a 0.72 y cruza 0.40 en el mensaje 15.

**El cruce del msj 15 coincide con el acople de `conversation`.** La subida
0 → 0.72 está mezclada con el cambio de factor. Sin aislados, D queda plano
entre 0.45 y 0.64 desde el msj 13.

bootstrap 12 sigue siendo la W de referencia; lo que se corrige es la
lectura de su curva. Corregido también en el docstring de
`experiments/replay_caso09_camino_vivo.py`.

N_eff del panel (`696b19f`, 14.7 → 4.6) arrastra el mismo factor.

---

## Lo que este REG no establece

- No decide si los aislados se excluyen del conteo o se registran como
  condición de la W.
- No verifica el mecanismo de §2 (qué términos quedan aislados y por qué).
- No mide el efecto sobre c(S), μ_W, β_c ni r.
- No mide en otro dominio.
- No cierra la pregunta de v1 ni la de v2.

---

## Abierto — a repetir y profundizar *(delamor)*

- Repetir §4 con varios seeds y n_runs mayores.
- Repetir sobre otros corpus y otros bootstraps: cuántas veces el acople de
  un aislado coincide con saltos de D_ckm.
- Verificar el mecanismo de §2 mirando los términos aislados.
- Medir c(S), μ_W_global, β_c y r con y sin aislados.
- Otro dominio de datos (`ckmdatasets`).
- d(σ) excluyendo aislados: cuánto de d = 1 queda.

---

## Archivos

- `services/landscape_engine.py` — `basin_distance`, `basin_masses`, `n_eff`
- `experiments/aislados_por_bootstrap.py` — §2
- `experiments/replay_caso09_camino_vivo.py` — condición bootstrap 12, corrección §5
- `docs/tasks/TASK_distancia_frontera_d_sigma_v1.md` — §1
- `docs/tasks/TASK_neff_y_frontera_logica_v1.md` — N_eff
- `registers/REG_hipotesis_distancia_contextual_v2.md` — §2, §9, §11

---

## Estado

- Hipótesis: **abierta**
- §1 (d(σ)): **verificado**
- §2 (frecuencia de aislados): **verificado**; mecanismo **propuesto**
- §3 (transferencia): álgebra **verificada**; c(S)/μ_W **no medido**
- §4 (factor no constante): **verificado**, una corrida
- §5: **corrección** de `c32d22a`

No cierra. Abre.

---

*Sep 2026 — Codespace ckm*
