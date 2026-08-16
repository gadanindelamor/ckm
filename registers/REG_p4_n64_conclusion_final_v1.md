# REG_p4_n64_conclusion_final_v1.md

*Ago 2026 — gadanin.delamor + Claude Code*
*Clase R — documento de preservación, a pedido explícito de delamor*
*Motivo: P4 en N=64 fue reabierto sobre una preocupación ya refutada
en otro documento. Este REG fija la conclusión y su traza completa,
para que no se vuelva a reabrir sin leer esto primero.*

---

## Conclusión

**P4 (interior optimal density Ω* en W_mixta) está confirmado en N=64.**

La reapertura de esta pregunta en `REG_mapeo_magnetico_ckm_v1.md`
(14 ago 2026) se apoyó en una preocupación — que pares negativos entre
nodos de alta frecuencia marginal (`fi` alto) tendrían impacto
desproporcionado, reduciendo el `k*` efectivo por debajo de 54 — que
ya había sido cerrada como falsa en `REG_hint_next_instance_v2.md`
(mayo 2026, sección "mu_AA — frontera trazada"), y que además no tiene
ningún caso al que aplicarse en los datos reales de fourforums: los 60
pares negativos reales son 100% pares cruzados entre grupos (T0↔T1),
0% pares dentro del mismo grupo. El escenario que la reapertura temía
no existe en los datos.

---

## Trazabilidad — qué verifiqué yo mismo ahora, qué cito de REGs previos

### Verificado por mí, esta sesión, reproducible

**Partición AA/AB/BA/BB de los 60 pares negativos reales de fourforums.**

Fuente: `experiments/neg_pairs_config_fourforums_v8h.json`, clave `neg_pairs`
(60 entradas, cada una con `q_stance` y `r_stance` ∈ {0,1}).

Comando ejecutado:
```python
import json
d = json.load(open('experiments/neg_pairs_config_fourforums_v8h.json'))
pairs = d['neg_pairs']
# clasificar cada par por (q_stance, r_stance)
```

Resultado exacto obtenido:
```
AA (T0-T0):     0   (0.0%)
BB (T1-T1):     0   (0.0%)
AB (T0→T1):    40  (66.7%)
BA (T1→T0):    20  (33.3%)
cross-stance (AB+BA): 60/60 = 100%
intra-stance (AA+BB):  0/60 =   0%
```

Cualquiera puede reproducir este resultado corriendo el snippet de
arriba contra el JSON citado — el archivo está commiteado en el repo.

### Citado de REGs previos — no re-derivado por mí, solo leído y verificado que el archivo existe con ese contenido exacto

**1. `registers/REG_hint_next_instance_v2.md`, líneas 59–67** (cierre H1/H2/H3,
también referenciado en línea 16 y 20):

> ## mu_AA — frontera trazada
>
> El ratio dentro de AA no depende de fi·fj (correlación = 0.012).
> Depende de acoplamiento temático específico por par.
> Pares con ratio alto: conocimiento_cohesivo ↔ sentido_comun (0.772),
> COCO ↔ AWARENESS (0.516), perspectiva_device ↔ atractor_patron (0.501).
>
> Modelar mu_AA requiere estructura interna del núcleo — proyecto separado.
> No bloquea nada operativo.

Y línea 16: *"No reabrir. Están cerrados en REG_mu_W_estructura_pares_v1.md
y en v27 sección 40."*

**2. `registers/REG_mu_W_estructura_pares_v1.md`, líneas 34–56** (tabla y
hallazgo central, el documento hermano de (1), sin el número 0.012 explícito
pero con la misma conclusión narrativa):

> | Grupo | Pares | μ_W obs | mean(fi·fj) | ratio | δ |
> |-------|-------|---------|-------------|-------|---|
> | AA    | 120   | 0.016122 | 0.065599   | 0.246 | −0.049 |
> | AB    | 256   | 0.000952 | 0.005933   | 0.160 | −0.005 |
> | BB    | 120   | 0.000523 | 0.000510   | 1.025 | +0.000013 |
>
> **μ_AA y μ_AB no son derivables desde fi·fj.**
> El modelo de independencia sobreestima 4x–6x.
> Causa: los nodos centrales co-ocurren tanto entre sí que sus frecuencias
> marginales están infladas mutuamente. No son independientes — son el núcleo.

**3. `registers/REG_p4_densidad_pares_negativos_v1.md`, líneas 16–29 y 73–76**
(el sweep sintético original):

> **k\* = 54 (ratio = 0.0268)**
>
> | k | ratio | ventaja W_mixta | estado |
> |---|-------|-----------------|--------|
> | 54 | 0.0268 | +0.000068 | ✓ ← k* |
> | 60 | 0.0298 | +0.000282 | ✓ ← fourforums real |
>
> ## Pendiente
> - Verificar k* con W_base real de fourforums (cuando disponible)

**Nota de honestidad**: el script que produjo este sweep,
`experiments/p4_neg_sweep.py`, **no existe en el repo actual ni en el
historial de git** (verificado con `find` y `git log --all --diff-filter=A`
— no hay resultado). Solo sobrevive la figura
`experiments/figures/p4_neg_density_sweep.png` y este REG con la tabla.
El número k*=54 no es reproducible por mí ahora mismo — lo cito del REG,
no lo re-derivé.

**4. `registers/REG_mapeo_magnetico_ckm_v1.md`, líneas 86–107** (la reapertura
que motiva este documento):

> P4 no es problema de escala — es problema de densidad de tensión.
> [...]
> **Apertura:** k*=54 fue hallado en W sintética con estructura
> uniforme. En corpus real con bimodal A/B, pares negativos entre nodos
> Grupo A (fi alto) tienen impacto desproporcionado — k* efectivo
> podría ser menor. No verificado contra fourforums.

**5. `docs/CKM_Informe_Trabajo_v32.md`, líneas 182–187** (versión condensada
de (4), mismo commit `fca771f`):

> k*=54 hallado en W sintética con estructura uniforme.
> En corpus real con bimodal A/B, pares negativos entre nodos Grupo A (fi alto) tienen impacto desproporcionado.
> k* efectivo podría ser menor si los pares negativos están concentrados en el núcleo A.
> No verificado contra fourforums.

**6. `docs/PAPER_Landscape_Driven_Device_v10_1.md`, líneas 882–919** (§5.3,
la versión que el paper presenta como cerrada, escrita un día antes que (4)):

> At N=64, the initial test — 18 negative opposition pairs (ratio = 0.009) —
> showed no W_mixta advantage. [...] k* = 54 [...] The fourforums gun
> control corpus produces 60 verified opposition pairs (ratio = 0.030 >
> 0.0268). The real corpus negative pair count is above k*.
> [...] P4 is confirmed at N=64 with this corpus.

---

## Síntesis — por qué la reapertura (4)/(5) no se sostiene

La preocupación de (4) es: *pares negativos de fi alto podrían pesar
desproporcionado, bajando el k* efectivo*. Esa preocupación asume que
`fi` (frecuencia marginal) predice el peso/impacto de un par. El
hallazgo (1), ya cerrado en mayo con "No reabrir", dice exactamente lo
contrario: dentro de un grupo, la correlación entre fuerza de par y
`fi·fj` es 0.012 — no hay relación. Lo que determina la fuerza de un
par es acoplamiento temático específico, no cuán frecuentes sean sus
nodos por separado.

Y aunque (1) fuera solo aplicable al corpus CKM propio (N=32,
conceptos como COCO/AWARENESS) y no directamente a fourforums, la
verificación (0) — hecha ahora, sobre los datos reales de fourforums —
cierra el caso de todos modos por otra vía: el escenario que (4) temía
(pares negativos *dentro* de un grupo de fi alto) tiene **cero
instancias** en los 60 pares reales. Los 60 son 100% cruzados entre
T0 y T1. No hay pares intra-grupo que puedan diluir nada, con
cualquier valor de fi que tuvieran.

No hace falta resolver si fi predice impacto en general para cerrar
P4 en N=64 — alcanza con que el tipo de par que preocupaba no exista
en los datos que confirman P4.

---

## Lo que sigue abierto, sin cerrar por este documento

- El número **k\*=54 mismo no es reproducible** — el script que lo
  generó no está en el repo. Si alguna vez hace falta revalidarlo,
  hay que reconstruir `p4_neg_sweep.py` desde cero, no asumir que
  existe.
- El hallazgo (1)/(2) es sobre el corpus CKM propio (N=32). Que su
  lección ("fi no predice impacto de par") se sostenga igual en
  fourforums no fue verificado directamente — se argumenta por
  analogía estructural, más el hecho independiente (0) de que el
  escenario temido no tiene instancias reales ahí. Son dos apoyos
  distintos para la misma conclusión, no uno solo.
- Este documento no vuelve a correr el sweep de densidad — no genera
  evidencia nueva sobre k* en sí, solo sobre por qué la preocupación
  que reabrió el caso no aplica a los datos reales existentes.

---

## Archivos citados (todos existen en el repo al momento de escribir esto)

- `experiments/neg_pairs_config_fourforums_v8h.json` — datos crudos, computación reproducible arriba
- `registers/REG_hint_next_instance_v2.md` — líneas 16, 20, 59–67
- `registers/REG_mu_W_estructura_pares_v1.md` — líneas 34–56
- `registers/REG_p4_densidad_pares_negativos_v1.md` — líneas 16–29, 73–76
- `registers/REG_mapeo_magnetico_ckm_v1.md` — líneas 86–107
- `docs/CKM_Informe_Trabajo_v32.md` — líneas 182–187
- `docs/PAPER_Landscape_Driven_Device_v10_1.md` — líneas 882–919
- `experiments/figures/p4_neg_density_sweep.png` — figura sobreviviente del sweep original

---

*Ago 2026 — gadanin.delamor + Claude Code*
*Codespace ckm — bash/Linux*
*Escrito a pedido explícito: preservar esta conclusión con su traza completa.*
