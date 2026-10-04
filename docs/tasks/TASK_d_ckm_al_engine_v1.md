# TASK_d_ckm_al_engine_v1.md

*Oct 2026 — gadanin.delamor + Claude Code (Opus 5)*
*Mismo proceso y misma forma que `TASK_landscape_engine_v1` (extracción al engine) y el pase de `analytics.py` a `services/`: todo lo del paisaje vive en `services/`, una sola vez.*

---

## Qué hacer

`D_ckm` es la única cantidad del paisaje **sin definición canónica**. Todas las demás tienen un solo lugar donde están definidas y donde están documentados sus sesgos: `relax_orbit`, `count_attractors`, `basin_masses`, `n_eff`, `d_masa_cuencas`, y desde el 3 oct `cluster_frontier_density` y `analytics`. D_ckm vive como una línea de aritmética dentro de dos servicios, con su docstring en uno de ellos.

*(delamor: el nombre va a quedar incorrecto, como `relax` o `count_attractors`, pero el código va a hacer lo que decidimos en el proyecto, no lo que el código quiera.)*

## Alcance

**Entra:** `services/monitor_service.py` y `services/coco.py`.

**No entra:**
- `services/fabrication_service.py` — **no es operativo**. Verificado: se instancia sólo en `experiments/exp_monitor_trajectory.py:44`, marcado `# [SNIPPET]`. Nada en `services/` ni en `iap_chatroom/`. Se reescribe de cero y ahí hereda el engine entero. *(El paper §8.2 lo lista como "operational and verified" — pendiente para F6.)*
- Las copias de `experiments/`: `monitor_service.py`, `monitor_service_dev.py`, `fabrication_service_dev.py`. Tratamiento especial de experiments: restos de la historia.

## Qué se extrae

`d_ckm(A_actual: int, A0: int) -> float`, en `landscape_engine`, inmediatamente antes de `d_masa_cuencas`. Las dos formas de distancia quedan una al lado de la otra: una sobre conteos que no convergen, otra sobre masas que sí.

El docstring lleva lo que hoy está disperso: que el signo es dirección y no déficit, que el nombre es incorrecto y se conserva por regresión, que **no es la cantidad canónica** y por qué (coupon-collector, el signo se invierte con seed o n_runs — REG_seleccion_nodos_desempate_v1 §8).

## Qué NO se unifica

**De dónde sale A0.** Es política de cada servicio y queda donde está:

| | A0 se cuenta sobre | ¿se resetea? |
|---|---|---|
| MonitorService | `_combine_W_Delta(W, Δ_r)` | sí, cuando W cambia (L283) |
| COCO | `self.W` sola — *"baseline sin Delta"* (L247) | no |

Extraer la fórmula **no unifica la cantidad**: la deja ser una sola cantidad con dos baselines, y pone esa diferencia a la vista en lugar de tenerla en dos líneas separadas por 350 líneas de código. Que el baseline lleve Δ_r o no, y que se re-fije o no, es decisión del modelo.

**El borde.** `A0 <= 0 → 0.0` se conserva tal cual, aunque `0.0` diga *"sin cambio"* donde no hubo medición y su hermana `d_masa_cuencas` devuelva `None`. Es la misma forma que el `NOMINAL` que se corrigió el 4 oct en `firma_ckm`. **Cambiarlo es una decisión aparte y no entra en una extracción.**

**El punto de regulación de COCO.** El umbral `D_CKM_THRESHOLD = 0.40`, el dominio de `_alpha_for` y `frac_rec` dentro de `_classify_zone` no se tocan.

## Los dos pasos *(delamor)*

**Paso 1 — duplicación exacta.** La función en el engine, con el cuerpo de hoy carácter por carácter. Nadie la llama. Checkpoint y test.

**Paso 2 — extracción.** Monitor y COCO pasan a wrapper fino, igual que sus `_count_attractors`. Checkpoint y test.

## Verificación

**Línea de base tomada ANTES de tocar los servicios** — `experiments/baseline_d_ckm.py`, guardada en `process/baseline_d_ckm/base.json`. El script de la base de `TASK_landscape_engine_v1` no quedó guardado; este sí.

- **Monitor:** replay de los 24 textos de `caso09_run2`, régimen natural, `n_runs_attractors=50` → **22 evaluaciones** con corpus establecido. Por evaluación: `D_ckm`, `c_S`, `fabrication_index`, `n_rejected_pairs`, `Delta_r_sum`, `activos_relajado`, `N_eff`, `D_masa_cuencas`, y el tipo de `D_ckm`.
- **COCO:** `W_ckm_corpus_v2` + Δ sintética con semilla fija → **6 casos** (3 modos × 2 seeds). Por `observe`: `D_ckm`, `A0`, `A_current`, `frac_rec`, `zone`, `alpha_used`, `stop_applied`, y el tipo.

**Criterio: cero diferencias exactas en las 28 filas.** No diferencias chicas. `python experiments/baseline_d_ckm.py --comparar process/baseline_d_ckm/base.json`.

Más: `tests/` completo sin regresión, `python services/coco.py` (T1–T13) y `python services/monitor_service.py` OK.

Y un test de `d_ckm` puro: valor conocido, caso negativo, `A0 = 0`.

## Bloqueo explícito

Si preservar el comportamiento exige tocar algo de "qué NO se unifica", o si un test sólo pasa modificando el test — **detener y reportar**. No encadenar cambios.

## REG

Tras verificar el criterio de cero diferencias, no antes. Forma de `REG_monitor_service_unificar_rutinas_v1`. Debe registrar: que no había divergencia de implementación sino de lugar; que los dos A0 quedaron sin tocar y siguen siendo la diferencia abierta; y el borde `0.0` conservado a propósito, con su razón.

## Abierto

- Los dos A0: cuál lleva Δ_r y cuál se re-fija.
- El borde `0.0` contra `None`.
- Qué cantidad gobierna la regulación de COCO — §8.3 del paper. Con `d_ckm` y `d_masa_cuencas` una al lado de la otra, pasa de pregunta conceptual a un argumento en el call site. *(delamor: reemplazaremos D_ckm por N_eff, o como se llame en el engine; el nombre queda. La cantidad declarada en la config o en `condicion_W`, porque los 253 paneles históricos llevan la de conteo bajo la misma clave.)*
- `frac_rec` (coco L250) y `recovery` (fabrication L109): misma cantidad, dos nombres, dos bordes.

---

## Lo que apareció al preguntar de dónde sale A0 *(4 oct, delamor)*

La extracción dejó una sola pregunta abierta y es la que sostiene cada afirmación determinada sobre D_ckm: **¿de dónde sale A0?**

*(delamor: A0 es un colector de confusión — si no es también un atractor espurio.)*

### A0 son tres capas, y la primera no es ruido

**1. Copias espurias.** `monitor_service.py:190`, ya escrito en el código: *"Un aislado (fila de W en cero) duplica cada atractor acoplado; Δ_r puede acoplarlo en W_eff durante el run"*. Con **k** aislados el conteo es `2^k · A_real`. Los extra no son atractores: son el mismo estado del campo con un spin libre. **El conteo cuenta otro objeto.**

Y no es estático: Δ_r puede acoplar un aislado **dentro** del run. A0 quedó fijo con un k, A_actual se cuenta con otro.

**La aritmética:**

```
A0 = 2^k     · A_real
A  = 2^(k-1) · A_real        (se acopló UN aislado)

D_ckm = (2^k − 2^(k-1)) / 2^k = 1/2 = 0.5
```

**Exactamente 0.5, sin importar k ni A_real.** Y `D_CKM_THRESHOLD = 0.40`. Entonces **un solo nodo aislado que consigue un par cruza el umbral y dispara STOP**, sin que el campo haya perdido nada: la mitad del conteo que desapareció eran copias.

**2. El cofound_collector** *(término de delamor, `docs/El problema del testeo uniforme en el cofound_collector.md` L224 y §541)*. `sample_s0` muestrea σ₀ **uniforme** sobre un paisaje **anisotrópico**: sobremuestrea las zonas muertas y submuestrea las líneas de tensión. El sesgo **no se cancela** entre numerador y denominador, porque la forma del paisaje cambió entre el instante de A0 y ahora. La alternativa existe —`sampling_mode` acepta `weighted` y `boltzmann`— y el default de Monitor es `uniform`.

**3. El instante.** A0 es lo que el muestreador contó en la **primera** llamada con corpus establecido, con el `n_runs` y `seed` de entonces, y el conteo **no converge**: crece monótono con `n_runs`. En Monitor además se **re-fija** cuando W cambia, así que "baseline" no es el principio: es la última vez que W cambió.

### Decisión *(delamor)*

**A0 va a ser lo que `CKMlandscapeConfig` defina.** Declarado, no descubierto — entra en la lista de `theta_W`, `sampling_mode` y `scale`, que son obligatorios sin default, *"no hay default hasta que el modelo los decida"*.

Eso **cierra el abierto de los dos baselines**, y no eligiendo entre ellos: saca lo que los hacía dos. Ningún servicio lo fija más.

**Lo que no arregla:** el número sigue saliendo de un contador sesgado. Lo que cambia es que el sesgo queda **declarado** al lado de `sampling_mode` y `w_version_id` — con qué muestreador y sobre qué W se colectó.

**Pendiente de diseño:** si la config lleva A0 como **valor** (un int que el modelo declara, y alguien lo midió una vez) o como **política** (sobre qué W, en qué momento, con qué muestreador y n_runs, y el número se deriva). Code se inclina por política, porque es lo que `from_W` ya hace con `mu_W` y `beta_c`: mide y declara cómo midió.

### Chequeable y no calculado

`condicion_W` de cada panel ya registra `aislados_W` y `aislados_W_eff`. Cuántos paneles tenían aislados cuando se fijó su A0 está declarado y nunca se contó.

### Alcance en el proyecto

Esto no es una línea de código: toca **todo lo que reportó D_ckm**. El umbral `0.40` se calibró contra una cantidad que salta 0.5 de un solo acoplamiento, y cada valor publicado arrastra el `2^k` del instante en que su A0 quedó fijo.
