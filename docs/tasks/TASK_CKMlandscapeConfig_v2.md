# TASK_CKMlandscapeConfig_v2.md

*Sep 2026 — gadanin.delamor + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v5.md (D5, Modelo Conceptual: "contrato vivo del instrumento"; CLOCK; `w_version_id`). DEFS_CKM_estado_actual_v12.md §0. Precondiciones: TASK_CKMlandscapeConfig_v1 (`450e7ba`), D6 (`6606b7c`), D7 (`5b52992`), D2 (`341f612`), D3 (TASK_delta_compresiones_coco_v1, ejecutada sin commit).*

---

## Por qué v2

v1 es una foto congelada de una W: una `dataclass(frozen=True)` que junta en un solo objeto inmutable tres cosas con causas de cambio distintas.

- **medido de W** — N, nodos, μ_W (2 formas), β_c (2 formas), `w_version_id`
- **declarado** — θ_W, scale, sampling_mode
- **identidad** — config_id, timestamp

Lo medido cambia en cada rebuild; lo declarado no tiene por qué. Congelado todo junto, cualquier rebuild deja la config desactualizada (gap D7) y cada servicio detecta el cambio por su cuenta.

**Hallazgo que lo hace visible (D3).** El COCO que Monitor recibe como `thermostat` no es `corpus.coco` y no renace en el rebuild. Monitor resetea Δ_r (D2); ese COCO no. El incremento que calcula queda negativo: medido con W de 8 nodos, una compresión α=0.1 y un reset de Monitor, `Δ_r_compresiones` terminó con 56 valores negativos (mín. −0.09). Monitor y COCO tienen cada uno su propia noción de en qué ciclo están.

La inmutabilidad de v1 es parte de la traza que trajo hasta acá, no una visión *(delamor)*.

---

## Criterio

**Principio.** Cada campo se ubica según **qué lo hace cambiar**. Dos campos con causas de cambio distintas no comparten objeto inmutable.

### Tres clases

| clase | cambia si y solo si | campos |
|---|---|---|
| **medido** | cambia `w_version_id` | `N`, `nodes`, `mu_W_nonzero`, `mu_W_global`, `beta_c_nonzero`, `beta_c_global` |
| **declarado** | alguien lo declara | `theta_W`, `scale`, `sampling_mode` |
| **identidad** | se crea una instancia | `config_id`, `timestamp` |

### Estructura

```
config = (identidad, declarado, ciclos = [c_0, c_1, …, c_k])

c_i = (
    w_version_id,        # sha256(W_i)
    medido(W_i),         # clase "medido"
    causa_i,             # "bootstrap" | "rebuild" | "estructural" | "volumen" | str
    t_señal_i,           # float | None — cuándo se señaló que W debía cambiar
    t_rebuild_i,         # float — cuándo cambió efectivamente
)

c_k = ciclo vigente
```

### Invariantes

- **I1 — Inmutabilidad en el registro.** Un ciclo cerrado (c_i, i < k) no se modifica. La config sí cambia: gana ciclos. La inmutabilidad pasa del objeto a la traza.
- **I2 — Ciclo vigente único.** Existe exactamente un c_k. Todo consumidor (Monitor, COCO) obtiene de ahí su noción de ciclo; ningún servicio detecta el cambio de ciclo por su cuenta.
- **I3 — Vigencia.** `vigente(W) ⇔ c_k.w_version_id == sha256(W)`.
- **I4 — Separación de origen.** Lo medido nunca se declara; lo declarado nunca se mide. Ninguna de las dos clases tiene defaults heredados.
- **I5 — Dependencia.** `medido(W)` es función de W sola. Dos ciclos con el mismo `w_version_id` tienen el mismo `medido`.
- **I6 — Tiempo (CLOCK).** Si hubo señal: `t_señal ≤ t_rebuild` y `deriva_i = t_rebuild_i − t_señal_i`. Sin señal, `deriva_i` es **nula, no cero**. La deriva es la medida de cuánto operó el sistema sobre una W ya señalada como obsoleta (v5).
- **I7 — Traza en el panel.** Cada panel lleva `(declarado, c_k)` en el momento de producirse. La historia no viaja en el panel.

### Transición única

```
abrir_ciclo(W, causa, t_rebuild, t_señal=None):
    si hay c_k y sha256(W) == c_k.w_version_id:
        no hace nada                                   # I5
    si no:
        cierra c_k (si existe)
        agrega c_{k+1} = (sha256(W), medido(W), causa, t_señal, t_rebuild)
```

El primer ciclo se abre en la construcción, con causa `"bootstrap"`: el primer rebuild no es degradación, es el origen (v5).

### API propuesta

```python
CKMlandscapeConfig.create(W, *, theta_W, sampling_mode, scale, causa="bootstrap", t_señal=None)
config.abrir_ciclo(W, causa, t_rebuild, t_señal=None) -> bool     # True si abrió
config.ciclo_vigente -> Ciclo
config.ciclos -> tuple[Ciclo, ...]
config.vigente(W) -> bool
config.deriva(i=-1) -> float | None
config.panel() -> dict            # (identidad, declarado, c_k) — I7
config.to_dict() / from_dict()    # config completa, con historia
```

`Ciclo` es inmutable (I1). `declarado` es inmutable dentro de esta TASK: cambiarlo no entra (ver Abierto).

---

## Verificación

Sobre `W_ckm_corpus_v2.json` y sobre un `CorpusService` con rebuilds reales:

- **I1**: tras `abrir_ciclo`, los ciclos anteriores son iguales a antes (igualdad de valores).
- **I2**: `ciclo_vigente` es siempre el último; `len(ciclos) ≥ 1` desde la construcción.
- **I3**: `vigente(W)` True con la W del ciclo; False con otra W.
- **I4**: construir sin `theta_W`, `sampling_mode` o `scale` falla; lo medido no es parámetro.
- **I5**: `abrir_ciclo` con la misma W no agrega ciclo y devuelve False.
- **I6**: con señal, `deriva ≥ 0`; sin señal, `deriva is None`; `t_señal > t_rebuild` falla.
- **I7**: `panel()` contiene identidad, declarado y el ciclo vigente, y no la historia.
- Valores medidos iguales a los de v1 sobre la misma W (μ_W 0.005977 / 0.004519, β_c global == `COCO.beta_c_corpus()`).
- Serialización completa y recarga producen la misma config, con la misma historia.
- Rebuild con nodos distintos y N igual (medido en D7, 4/4): abre ciclo nuevo.
- Tests existentes sin regresión.

## Qué no hace

- No decide qué hace cada consumidor al cambiar el ciclo. Monitor ya resetea (D2); COCO queda pendiente.
- No conecta la config a CorpusService para que abra ciclos sola.
- No reemplaza la consulta `w_change_since` (D7).
- No define la fórmula de θ_W.
- No persiste W: sólo su sha.

## A decidir antes de ejecutar

1. **v1 y v2.** ¿v2 reemplaza a v1 en `ckm_landscape_config.py`, o convive como clase nueva? Monitor hoy usa `to_dict()` y `sampling_mode` de v1, y el panel lleva la config v1 completa en `landscape_config`. Con v2, por I7, esa clave pasaría a llevar `panel()`.
2. **Quién llama a `abrir_ciclo`.** Monitor, CorpusService, o quien arma el run.

## Abierto

- Qué hace COCO al cambiar el ciclo: renace, o se ajusta (incremento negativo tras reset de Monitor, W congelada).
- Cambiar lo declarado dentro de un run: ¿abre ciclo, o es un eje aparte?
- Fórmula de θ_W.
- Las causas de rebuild como vocabulario cerrado o libre.
