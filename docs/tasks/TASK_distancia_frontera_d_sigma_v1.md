# TASK_distancia_frontera_d_sigma_v1.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: REG_hipotesis_distancia_contextual_v2.md §4 y §11 (`dc63dd6`). Rebuilds fuera: W congelada.*

---

## Qué hacer

Implementar la operación que §11 declara faltante:

```
d(σ) = mínimo número de flips que cambian la órbita a la que relaja σ
       — distancia de σ a la frontera de su cuenca
```

Función pura en `services/landscape_engine.py`. No se conecta al panel ni al canal.

## Definición operativa

1. `órbita_0 = relax_orbit(σ, W)`.
2. Para k = 1, 2, …, k_max: voltear k nodos de σ, relajar con `relax_orbit`, comparar la **órbita** (frozenset de estados) con `órbita_0`.
3. `d(σ)` = el menor k con al menos una perturbación que cambia la órbita. `None` si ninguna hasta k_max.

**Se comparan órbitas, no estados.** Caer en la otra fase de la misma órbita de período 2 no es cambio de cuenca. Así el abierto de §11/Abierto ("qué es cambiar de órbita cuando el estado devuelto es una fase") queda resuelto en esta definición — declarado, no descubierto.

**Búsqueda:** exhaustiva hasta `k_exhaustivo` (default 2: con N=20 son 20 + 190 perturbaciones); desde ahí, `n_muestras` subconjuntos al azar por k. La salida declara si el d encontrado es exacto o muestreado: con muestreo, d es **cota superior**.

## Verificación

- W sintética con dos cuencas conocidas: d = 1 en un estado de frontera, d > 1 en el interior.
- d(σ) ≥ 1 siempre que se devuelva.
- Determinista con la misma seed.
- Otra fase de la misma órbita no cuenta como cambio.
- Corrida: distribución de d sobre estados de atractor de caso09 natural (N=20, W de los 24 textos) y de caso09 bootstrap 12 (N=32).

## Resultado (caso09, 200 muestras, búsqueda exacta)

| W | órbitas | período 2 | d = 1 | d = 2 |
|---|---:|---:|---|---|
| natural N=20 (24 textos) | 57 | 33 | 55 órb., 81% de la masa | 2 órb., 19% |
| bootstrap 12, N=32 | 56 | 12 | 56 órb., 100% de la masa | — |

Mecanismo de los flips simples que cambian de órbita: N=20 → 424 acoplados, 74 con h=0, 0 aislados; N=32 → 313 acoplados, 33 con h=0, **168 en nodos aislados**. Sin los triviales d=1 igual domina. La W de bootstrap 12 tiene **3 nodos aislados** (fila en cero): cada atractor acoplado aparece en 2³ copias — infla A0, conteos y N_eff. Explorado en `experiments/aislados_por_bootstrap.py`.

## Qué no hace

- No mide `k` de un device real (Abierto del REG).
- No conecta d(σ) a Monitor ni al panel.
- No calcula D_masa_cuencas.

## Abierto

- Si la búsqueda muestreada para k ≥ 3 subestima la frontera en N=32.
- Qué σ corresponde en operación: `sigma_relaxed` del panel, o estados de atractor del censo.
