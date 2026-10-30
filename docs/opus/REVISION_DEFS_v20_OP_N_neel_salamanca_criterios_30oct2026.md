# Revisión — DEFS v20 (§N y §OP), Néel / SALAMANCA, full_meaning, trace_ip, CRITERIOS_diversidad, analytics.py, el criterio de calibrate y la grilla completa — 30 oct 2026 (Opus 5.5, Cowork)

*Pedido de delamor (30 oct): revisar las DEFS actuales, la grilla de OP y de N, y Néel / SALAMANCA (*"creo que hay tests que se hicieron"*), full_meaning e IP trace, y `docs/CRITERIOS_diversidad_formulacion_v1.md`. *"Luego una sola respuesta con todo en doc."* Lectura en la PC. No se tocó ningún archivo, salvo éste.*

## 0. Lo más importante, primero
1. **P19 ya estaba encontrado el 11 sep**, en `CRITERIOS_diversidad_formulacion_v1.md` §4, con su regla y tres arreglos posibles. Eso decide la forma de A: va en §6.
2. **Néel se corrió el 20 sep**, y la DEFS v20 y el paper v34 dicen que no.
3. **SALAMANCA está registrado** (Clase R) y el paper no lo menciona.
4. **Error mío en el v34 (A3):** escribí *"expelled"* en §4.2.2. La tabla N lo marca como Babel desde el 8 oct.

## 1. DEFS v20 — la última (no hay v21)

### §N, los nombres: 19 rótulos
metabolizado · `rejected` / `rechazados` · `expulsados` · torsión / `n_torsion` / `Δ_r_torsion` · "expulsión" (§11) · operador de compresión de COCO · OPERADOR_STOP_COCO / "operadorstop" · `MonitorService.stop_signal` (UNKNOWN) · H_STOP · Gatekeeper / portero / `admit()` · `count_attractors` · `d_ckm`, `A0`, `A_actual` · "degradado / expandido" · "agregar un nodo" · contagio / acoplado · UNKNOWN / NOMINAL · `services/` · E1–E4, EA1–EA3, D1–D3, L1–L4 (Orden BABEL, propuestos).

Lo que está abierto ahí y espera a delamor desde octubre:
- el renombre de `expulsados` (*"¿a dónde? ¿fuera de él?"*, 8 oct);
- OPERADOR_STOP_COCO en el código;
- Gatekeeper;
- los verbos de "agregar un nodo" (activar / desactivar, incorporar / retirar);
- los prefijos del Orden BABEL.

### §OP, los objetos del instrumento: 26
S = W estática, D = dinámica, S+D = las dos.
- **Del corpus (S):** fi, W_ij, W_ij/(fi·fj), T(W), perfect_oppositions, W_mixta.
- **Del estado:** c(S) (S+D) y r = c(S)/μ_W (D).
- **De las formulaciones (S):** Histéresis (P1) y Ω* (P4). En el paper son F1 y F4.
- **Del landscape (S+D):** Atractores A = |L|, N_eff, node_presence, d(σ), copresence_matrix, cluster_nodes, cluster_frontier_density, Boltzmann σ₀ y β_Néel (propuesto).
- **De la dinámica (D):** D_masa_cuencas, D_ckm, Δ_r, la órbita en el panel, Δ_r_torsion y UNKNOWN.

### Desactualizado en §OP
- **La nota v17:** los números del CP-E de `0e042ac` (15,52 / 5,27 / 10,10, el −66 %). Con el extractor de hoy no se reproducen (texto 20, punto 3).
- **La fila N_eff:**
  - dice "±1–5 % en casos IAP": es N_eff0 de un solo corpus (caso09), con 3 seeds (R4);
  - dice "D_ckm sigue definido sobre A", cuando desde v15 D_ckm se calcula con N_eff;
  - dice "Rango [1, A0]", y ahora hay una cota inferior: §5.

### Falta en §OP (medido o decidido después de la v20)
- F(N), el piso del colapso, y el margen y la separación (N_eff(W) > F(N));
- α, la masa autoconjugada, con la cota y la condición α ≤ 2/3;
- W_Monitor, W_COCO y W_calibrate, y los tres D_ckm;
- Δ_r_pares y Δ_r_compresiones: están en las SLAs, no en la tabla;
- el Threshold MEASURED / DECLARED y frac_rec;
- los criterios D.1–D.5 de CRITERIOS (§5).

### Otras dos cosas
- **"paridad" en la fila Δ_r_torsion:** ahí es la paridad de la **fase** de la órbita de período 2, no la de N. Code midió las dos en el texto 20 (2e y 4d).
- **El ítem 19 del review** ("cluster frontier coercivity" no está definida): en §OP sí está, como `cluster_frontier_density`, min(intra_a, intra_b) / inter(a, b), y también en CRITERIOS Parte III. Lo que falta es que el paper la traiga.

## 2. Néel y SALAMANCA

- **SALAMANCA S1.**
  - Fuente: `registers/REG_salamanca_s1_v1.md` (Clase R, OK de delamor el 5 oct), con 1000 barajados, k-means con 10 inicializaciones y Bonferroni sobre 7 k.
  - Lo medido: **detecta modularidad, no adversarialidad**. La saturación ordena (monótona en los cinco corpus medibles), y el criterio **devolvió vacío** en los dos corpus saturados y en el de 7 textos.
  - Control positivo: ausente. La corrección por la familia completa no se sostiene a 1000 barajados.
  - La DEFS v20 §16 lo trae completo. **El paper v34 no lo menciona.**
- **Néel.**
  - Fuente: `docs/tasks/TASK_neel_separabilidad_v1.md`, sección *"Resultado — primera corrida"*. Es una TASK, no un REG. Driver: `experiments/driver_neel_salamanca.py`, commit `abc14b3` del 20 sep.
  - El pre-registro estaba mal asignado: caso09 es el canal IAP 0.9, no el debate (lo declaró Code).
  - SALAMANCA dio ncut 0,633 contra el nulo 0,873 (20 barajados, p < 0,001). La partición separa protocolo e identidad de los devices del contenido.
  - Néel dio una frontera de profundidad cero: de los 20 pares menos correlacionados, a β = 0,244 / 0,122 / 0,068, persisten en 3 semillas 1 / 0 / 0, contra 0,03 por azar. *"Módulos sin frontera."*
  - Pendiente desde entonces: el control positivo con fourforums.
- **La contradicción:** la DEFS v20 §15 dice *"sigue no corrido"* (citando el REG de SALAMANCA, §6), y el paper v34 §8.5 trae a Néel como *"Proposed… Not verified"*.
- **Los tests:** `tests/test_coco.py:140` y `tests/test_vacio_y_orbita_en_el_panel.py:8` afirman que *"SALAMANCA: no medible" no es "nada"*. No hay un test del criterio.

## 3. full_meaning
Sólo existe en la DEFS v20, fila T(W) de §OP: con presencia sola, T = 0 por teorema (§1.1 h), así que `full_meaning` (T > τ) no se alcanza sin marcadores. No hay código (grep en `services/`, `iap_chatroom/` y `experiments/`: nada), y el v34 no lo trae.

## 4. trace_ip
- **En el paper v34**, §8.2 (MonitorService, *trajectory inflection point*) y §8.3: el momento es observable; si un device lo reconoció, no es verificable.
- **Su instancia:** `registers/REG_trace_ip_sesion_05oct_v1.md` (Clase R, 5 oct). Sus momentos son el origen de varias cosas de hoy:
  - período 2 como Möbius o cilindro (10–11);
  - *"NODE EXTRACTOR, REBUILD, Néel, SALAMANCA"* como los cuatro lugares donde una magnitud se vuelve existencia o relación (12);
  - los rebuilds que no respetaban el período 2 (13);
  - el nacimiento de la torsión, *"debe respetar la estructura"* (14);
  - los dos COCO (15).

## 5. `docs/CRITERIOS_diversidad_formulacion_v1.md` (11 sep, `550dd64`)
Es un documento autocontenido, con formulación y especificación. Lo que trae, contra lo de hoy:

- **§4, la condición de exactitud: es P19.**
  - El documento dice: *"`sign(h)` es discontinua en h = 0… Regla: los empates son exactos si y sólo si los pesos lo son."* Con pesos no diádicos, el **46 %** de los pasos cambia de sucesor según cómo se escriba el producto; con pesos diádicos, el 0 %. Normalizar por 3 en vez de por 4 dio el mismo número de órbitas (33), pero 18 de ellas distintas.
  - Los tres arreglos, en orden de costo: (1) no normalizar, trabajar con los conteos enteros; (2) **normalizar por la potencia de dos siguiente**; (3) suma exacta compensada.
  - El asincrónico reduce el efecto, pero no lo elimina.
  - Code midió lo mismo el 29 oct, del otro lado: W con denominador 12, y entre el 13 y el 22 % de los estados con otro sucesor que el exacto. **Lo encontrado el 11 sep no llegó al paper, ni a las DEFS, ni al código.**
- **D.5, diagnósticos de exactitud:** `valores_distintos`, `diádico`, `frac_empates` y `frágil`. El documento dice: *"`frágil > 0`… Es diagnóstico obligatorio antes de reportar cualquier número."* No se implementó.
- **§2.3, la medida de referencia:** CRITERIOS llama **canónica** a la uniforme sobre el hipercubo (así la masa es volumen de cuenca, una propiedad de W sola), y dice que la banda 30–70 % es *"una tercera referencia"*. El 28 oct delamor eligió la banda del código. No es una contradicción, porque las dos se declaran, pero la DEFS v21 tiene que decir que la canónica de CRITERIOS fue reemplazada, y cuándo.
- **C.2:** es la fuente de la tabla de validación de §4.3.1 del paper (masa plana / intermedia / concentrada). Fue bajo la uniforme, y el paper ya lo dice. Responde en parte el ítem 36 del review.
- **D.1–D.4, criterios de W sola, sin muestrear:**
  - D.1, índice de frustración: topológico, por triángulos, invariante a la escala. Es el que usa §5.2 del paper para fourforums;
  - D.2, `frac_neg` = Σ|W<0| / Σ|W|: **es la misma fórmula que T(W) de §OP**. Dos nombres para un objeto (Babel);
  - D.3, el espectro (λ_min, λ_max);
  - D.4, el CV de las frecuencias marginales.
  En §OP sólo está T(W).
- **Eje 1 / Eje 2:** separa las cantidades de W sola de las de la sonda, y las topológicas de las métricas. Medido: con los negativos amplificados ×16, la frustración queda fija (0,0258) mientras frac_neg va de 0,031 a 0,338. El paper no usa esta distinción.
- **Parte III, lo abierto:**
  - qué tendría que contar un índice de degradación (decisión del modelo, no del teorema);
  - la medición cruzada entre los criterios de W y los de la sonda;
  - la profundidad de cuenca: la cola es plana, y el candidato son las barreras de energía, sin probar;
  - la coercividad de frontera *"de W sola"*, derivando la partición por corte espectral. **Es lo que después hizo SALAMANCA**;
  - con N > 22 no hay verdad de terreno.
- **Para el review:** el ítem 34 (Chao1, Good–Turing) tampoco tiene respuesta acá. CRITERIOS argumenta contra el conteo crudo, igual que el paper.

## 6. Lo que decide Opus (bajo el umbral; se registra en `decisiones_en_el_acto.md`)
1. **La forma de P19 A sale de CRITERIOS §4.** Primera opción: normalizar W por la potencia de dos siguiente. Escalar W por una constante positiva no cambia sign(h), así que la dinámica queda igual a la exacta; sólo cambian de escala las cantidades métricas absolutas. Code mide si eso alcanza y qué arrastra en lo métrico: c(S), μ_W, los umbrales absolutos. Si W no viene de conteos enteros, la opción es la suma exacta (3). Se implementa también D.5 (`frágil`) como diagnóstico, antes y después. Va en un texto para Code de la próxima sesión, con el recálculo de §4.3.1 y §6.4. §4.1.2 del paper (B) cita CRITERIOS §4 como el hallazgo del 11 sep.
2. **DEFS v21:** se corrigen §15 (Néel se corrió), la nota v17 de §OP, la fila N_eff y la de Δ_r_torsion. Se agrega lo que falta (§1), D.1–D.5 de CRITERIOS y el reemplazo de la medida canónica (28 oct). T(W) y frac_neg quedan declarados como el mismo objeto.
3. **Paper:** "expelled" sale de §4.2.2 hasta que delamor elija el rótulo. Mientras tanto, la frase se escribe por su definición: *"rejected in every phase of the orbit"*.

## 7. Lo que decide delamor
1. **¿SALAMANCA y Néel entran al paper?** Lo que aportan: un criterio que puede devolver vacío, y lo devolvió (en el canal y en los corpus saturados). Lo que no tienen: un solo corpus para Néel (mal asignado en el pre-registro), sin control positivo, con 20 nulos y 3 semillas.
2. **El rótulo de `expulsados`.** Está abierto desde el 8 oct. Hoy el código dice `expulsados` y el paper *"expelled"*.
3. **¿Entran al paper los criterios de W sola (D.1–D.4) y la distinción topológico / métrico?** §5.2 ya usa D.1 sin nombrarlo como criterio.

## 8. `services/analytics.py`, cruzado con lo de arriba (delamor: *"revisá analytics.py y cruzalo con lo generado antes"*)
Archivo de 183 líneas, último cambio `0ca5494` (3 oct). Tiene `copresence_matrix`, `cluster_nodes`, `perfect_oppositions`, `attractor_stats` y `optimal_density` (P4 / Ω*).
1. **Cuenta en vez de pesar.** Las cuatro primeras reciben `attractors: dict[frozenset, int]`, los conjuntos de nodos activos de un estado terminal, y la correlación se hace sobre los atractores **únicos, sin peso**. CRITERIOS C.4 y C.5 (11 sep) dicen que ponderar por masa *"es necesario"*: promediar sobre órbitas únicas sin peso *"hereda el sesgo de conteo"* (deriva 0,19 contra 0,03 al multiplicar el presupuesto por 100). Además, la clave es un estado y no una órbita (CRITERIOS §2.1). La versión con peso existe, pero en un experimento: `experiments/driver_neel_salamanca.py`, `copresencia_pesada`, con un control de que, con pesos uniformes, da lo mismo que `analytics.copresence_matrix`. **En `services/` no está.**
2. **`node_presence`:** la fila de §OP dice *"implementado, landscape_engine.py"*, y en `landscape_engine.py` no existe. El único `node_presence` es la clave de `attractor_stats` (`analytics.py:129`): la fracción de atractores **únicos**, sin peso. La DEFS y el código no coinciden.
3. **Defaults en la firma** (contra la regla del 26 oct): `n_clusters = 4`, `threshold = −0.90`, `rho_steps = 30`, `n_samples = 300` y **`seed = 42`**, que no es el seed 0 del instrumento. `optimal_density` usa el RNG global (`np.random.seed`) y `int(rho·N)` (el piso).
4. **Un veredicto en el código:** `optimal_density` devuelve `"confirmed": omega_interior`, y su docstring dice *"P4 prediction"*. Es interpretación dentro de una función; en el paper es F4 (el review, ítem 22, también la toca). Depende de `CKMGraph`, de `process/initial_static_model/`, que está archivado.
5. **Quién lo usa:** sólo `experiments/driver_neel_salamanca.py`, para el control de `copresence_matrix`. Monitor y COCO no lo usan, así que las filas copresence_matrix, cluster_nodes y perfect_oppositions de §OP, marcadas S+D, hoy sólo tienen la forma S, offline.
6. **`cluster_frontier_density`** no está en `analytics.py`: es su propio módulo, `services/cluster_frontier_density.py`, con el docstring *"Función propuesta para analytics.py"*. Lo usa `driver_neel_salamanca.py`. Está implementado y es la respuesta al ítem 19 del review.
7. **Criterios de W sola** (CRITERIOS D.1–D.5): en `services/` no hay índice de frustración, espectro, CV ni diagnósticos de exactitud. El grep de `frustr` y `eigvalsh` no da nada. Los triángulos frustrados de fourforums están en el pipeline de `ckmdatasets` (copia en `docs/opus/ckmdatasets/build_W_v8n.py`).

## 9. calibrate: el criterio del máximo en vez del de los extremos (delamor: *"calibrate NO separa, pero con el criterio de Code del promedio del máximo, en vez del actual"*)

**Lo que hace hoy el código** (`services/calibrate.py:328-358`):
- *separa* ⇔ margen = d(λ = 1) − d(λ = 0) > 0;
- el umbral es d(0) + margen/2, *"el punto medio del salto"*;
- `d_max` y `lambda_de_d_max` se registran, pero no deciden. Code lo dejó escrito el 10 oct (`bdbe053`): *"el colapso es λ=1 por construcción, así que no cambio la definición por mi cuenta: el margen sigue siendo entre los extremos. Lo que sí hago es declarar el máximo"*.

**Lo que daría el criterio del máximo:** separa ⇔ d_max > 0, con el umbral en d_max/2. Con lo que se puede leer desde la PC (el paper y la última calibración de cada log):

| intento | W | n_runs | d en λ = 0 / 0,25 / 0,5 / 0,75 / 1 | margen (hoy) | d_max @ λ | hoy | con el máximo |
|---|---|---|---|---|---|---|---|
| 2 | las 4 de los rebuilds | 200 | d_max = 0 en λ = 0, las cuatro (paper §6.4) | < 0 | 0 @ 0 | no | no |
| 3 | rebuilds 1 y 2 | 200 | (sólo el máximo, en el paper) | < 0 | 0,0280 y 0,1760 @ 0,25 | no | **sí** (umbrales 0,014 y 0,088) |
| 3 | bdb98f5b | 200 | 0 / 0,2312 / 0,1536 / 0,0114 / 0,0114 | +0,0114 | 0,2312 @ 0,25 | sí (0,0057) | sí (0,1156) |
| 4 | 6ca344c3 (las otras 6, no leídas desde la PC) | 1000 | 0 / −0,032 / −0,200 / −0,316 / −0,316 | −0,316 | 0 @ 0 | no | no |
| 5 | 66ea8d05 (origen) | 200 | 0 / −0,025 / −0,160 / −0,300 / −0,300 | −0,300 | 0 @ 0 | no | no |
| 5 | 6c16bb08 | 200 | 0 / 0,520 / 0,616 / 0,524 / 0,506 | +0,506 | 0,616 @ 0,5 | sí (0,253) | sí (0,308) |

**Lo que eso muestra, sin interpretar:**
1. **Con el máximo, la separación depende del interior del camino**, de W_λ en un λ intermedio, y no sólo de N_eff(W) contra F(N). Hoy, por R1, separar es N_eff(W) > F(N), y F(N) no depende de W: es el ítem 7 del review. Con el máximo, la comparación pasa a ser N_eff(W) contra el mínimo de N_eff(W_λ) sobre la grilla, y eso sí depende de W.
2. **Sesgo declarado del criterio:** d_max es el máximo de cuatro estimaciones con ruido (λ = 0 da 0 por construcción). Un máximo sobre puntos muestreados se infla: es el mismo efecto que la TASK de Néel midió para *"S sobre la mejor partición"* (0,030 / 0,014 / 0,005 con 200 / 1000 / 5000 muestras). A n_runs = 200, d_max > 0 puede salir sólo del ruido. La regla *separa ⇔ d_max > 0* dice que sí en cuanto un punto interior da menos N_eff que λ = 0.
3. **Lo que falta para decidir:** el d exacto de cada punto de la grilla, por enumeración, para las 14 + 2 W. Son 5 puntos × 16 W de 2^20 estados: con lo que tardó el texto 20, debería entrar en una corrida autónoma. Con eso se ve qué diría el criterio del máximo sin ruido. Va como texto para Code en la próxima sesión, con el de P19 A: los dos tocan la dinámica y conviene medirlos después de A.
4. **La decisión es de delamor:** el patrón es suyo (*"el colapso es λ=1 por construcción"*).

## 10. La grilla completa de objetos, borrador para DEFS v21 §OP
*S = W estática, D = dinámica. "services" = implementado en el instrumento; "exp" = sólo en `experiments/`; "—" = no hay código. **Las ubicaciones son las verificadas hoy con grep; donde no se verificó, se dice.** Las filas que vienen de la v20 conservan su objeto; lo nuevo va marcado ★.*

| # | Objeto | Forma | Dónde (código) | Qué es | Estado / nota |
|---|---|---|---|---|---|
| 1 | fi | S | no verificado | fracción de textos donde aparece el nodo i | v20 |
| 2 | W_ij | S | `services/corpus_service.py`, `node_extractor.py` | co-ocurrencia normalizada; signo por procedimiento declarado | v20. ★ Normalización: CRITERIOS §4 y P19 (diádica o no) |
| 3 | W_ij/(fi·fj) | S | no verificado | observado/esperado | v20 |
| 4 | T(W) ≡ ★frac_neg (CRITERIOS D.2) | S | — (en `services/` no hay) | Σ\|W<0\| / Σ\|W\| | ★ **dos nombres, un objeto** (Babel); métrico |
| 5 | ★ índice de frustración (D.1) | S | `ckmdatasets` (fourforums), no en `services/` | triángulos con producto de signos < 0 / triángulos completos | ★ topológico; lo usa §5.2 del paper |
| 6 | ★ espectro λ_min, λ_max (D.3) | S | — | autovalores de W | ★ métrico; no implementado |
| 7 | ★ CV de las marginales (D.4) | S | — | desvío(f)/media(f), f_i = Σ_j\|W_ij\| | ★ no implementado |
| 8 | ★ diagnósticos de exactitud (D.5) | S | — | `valores_distintos`, `diádico`, `frac_empates`, `frágil` | ★ *"obligatorio antes de reportar"* (CRITERIOS); no implementado; entra con P19 A |
| 9 | perfect_oppositions | S | `services/analytics.py:76` | pares con corr. de co-presencia ≤ −0,90 | ★ sin peso, default −0,90 en la firma (§8) |
| 10 | W_mixta | S | no verificado | W_pos + negativos en fronteras coercitivas | v20; su admisión requiere SALAMANCA + Néel |
| 11 | c(S) | S+D | `landscape_engine.mean_cS` | mean(W_ij σ_i σ_j) | v20 |
| 12 | r = c(S)/μ_W | D | no verificado | cohesión relativa | v20 |
| 13 | Histéresis (P1 → F1) | S | no verificado | rama UP vs DOWN de c(S) | v20; review ítem 20 |
| 14 | Ω* (P4 → F4) | S | `services/analytics.optimal_density` | argmax de c(S) sobre ρ | ★ `"confirmed"` en el código; seed 42; depende de un módulo archivado (§8) |
| 15 | ★ σ₀, la medida de referencia | S+D | `landscape_engine.sample_s0` | banda 30–70 % de activos, elección uniforme | ★ decidida el 28 oct; CRITERIOS §2.3 la llamaba *"tercera referencia"* y canónica a la uniforme |
| 16 | Boltzmann σ₀ | S+D | `landscape_engine.boltzmann_warmup` | calentamiento con β_c | v20 |
| 17 | ★ órbita (relax_orbit) | S+D | `landscape_engine.relax_orbit` | el conjunto invariante alcanzado; período ≤ 2 (Goles) | ★ regla de empate h = 0 en float64: P19 |
| 18 | Atractores A = \|L\| | S+D | `landscape_engine.deprecated_count_attractors` | conteo de terminales | v20; no converge |
| 19 | ★ masas de cuenca | S+D | `landscape_engine.basin_masses` | fracción de σ₀ por órbita | ★ |
| 20 | N_eff | S+D | `landscape_engine.n_eff`, `count_attractors` | 1/Σm² | v20, corregida: ±1–5 % es caso09 (R4); ★ cota inferior (fila 21) |
| 21 | ★ α, masa autoconjugada, y la cota | S+D | `experiments/simetria_neff_dos.py` | N_eff ≥ 1/(α² + (1−α)²/2); ≥ 2 si α ≤ 2/3 | ★ probado (texto 20, 2) |
| 22 | ★ F(N), el piso del colapso | S | `experiments/piso_del_colapso.py` | N_eff exacto del colapso: 2 con N impar, forma cerrada con N par | ★ verificado hasta N = 21 |
| 23 | ★ enumeración exacta | S | `experiments/margen_exacto_14W.py`, `piso_del_colapso.py` | N_eff exacto bajo la medida del código | ★ hasta N ≈ 21; con el paso del código (P19) |
| 24 | node_presence | S+D | `analytics.attractor_stats` (clave) — **no en landscape_engine** | presencia en atractores únicos | ★ la v20 dice landscape_engine: no está; sin peso, contra CRITERIOS C.4 |
| 25 | d(σ) | S+D | `landscape_engine.basin_distance` | flips hasta cambiar de órbita | v20; no está en el panel |
| 26 | copresence_matrix | S (★ hoy sólo S) | `services/analytics.py:22` | Pearson sobre atractores únicos | ★ sin peso; la versión con peso está sólo en exp |
| 27 | cluster_nodes | S (★ hoy sólo S) | `services/analytics.py:48` | Ward sobre 1 − corr | ★ default `n_clusters = 4` en la firma |
| 28 | cluster_frontier_density | S | `services/cluster_frontier_density.py` | min(intra_a, intra_b)/inter(a, b); "oposicion" si inter < 0 | v20; ★ módulo propio; lo usa el driver de Néel |
| 29 | ★ SALAMANCA (ncut contra el nulo) | S | `experiments/driver_neel_salamanca.py` | ¿hay T0/T1 en W_pos? corte espectral contra barajados | ★ S1 registrado (`REG_salamanca_s1_v1`); detecta modularidad |
| 30 | β_Néel | S | `experiments/driver_neel_salamanca.py` (`neel`) | barrido de β con la partición fija; persistencia de la cola | ★ **corrido** (20 sep): frontera de profundidad cero; la v20 decía "no corrido" |
| 31 | D_masa_cuencas | D | `landscape_engine.d_masa_cuencas` | 1 − ln N_eff/ln N_eff0 | v20; ≡ D_ckm desde `dabd1ed` |
| 32 | D_ckm (★ tres instancias) | D | `landscape_engine.d_ckm` | ídem | ★ D_ckm^calibrate, D_ckm^Monitor, D_ckm^COCO, con baselines distintos |
| 33 | ★ W_Monitor, W_COCO, W_calibrate (W_λ) | D | `monitor_service`, `coco`, `calibrate` | W + Δ_r_pares; W + Δ_r_compresiones; (1−λ)W + λW_colapso | ★ notación confirmada el 29 oct; review ítem 11: W_eff ≡ W_Monitor |
| 34 | Δ_r → ★ Δ_r_pares | D | `services/monitor_service.py` | pares rechazados **en todas** las fases | v20 (rótulo `expulsados`: Babel, [delamor]) |
| 35 | ★ Δ_r_compresiones | D | `services/coco.py` | Δ_r_compresiones ← α_c · Δ_r_compresiones | ★ estaba en las SLAs; **α_c ≠ α de la fila 21** (review, ítem 3) |
| 36 | Δ_r_torsion | D | `services/monitor_service.py:240-350` | pares rechazados en una fase y sostenidos en la otra | v20; ★ 0 en 154 evaluaciones; en una órbita autoconjugada = pares del mismo lado (texto 20, 4d) |
| 37 | órbita en el panel | D | `monitor_service` (panel) | `periodo_orbita`, `n_aceptados`, `n_expulsados`, `n_torsion`, `pares_torsion` | v20 |
| 38 | ★ margen y separación | S | `services/calibrate.py:337-348` | d(1) − d(0); separa ⇔ > 0 ⇔ N_eff(W) > F(N) | ★ R1: 0 de 14 W separan exacto; intento 5: 1 de 2 |
| 39 | ★ d_max, λ de d_max | S | `services/calibrate.py:328-330` | máximo de la curva, registrado, no decide | ★ §9: criterio alternativo, a decidir por delamor |
| 40 | ★ frac_rec | S+D | `calibrate`, `coco`, `monitor_service` | N_eff/N_eff0 | ★ |
| 41 | ★ Threshold (MEASURED / DECLARED) | D | `services/ckm_trust_rule.py:255`; uso en `monitor_service.py:646` | el umbral con su procedencia y su W | ★ |
| 42 | UNKNOWN | S+D | código y panel | ausencia de medición | v20 |
| 43 | ★ full_meaning | S | — | T > τ | ★ sólo en la DEFS; inalcanzable con presencia sola (§1.1 h) |
| 44 | ★ trace_ip | D | — (MonitorService lo hace observable) | el momento en que cambia el patrón distribucional | ★ en el paper §8.2–8.3; instancia en `REG_trace_ip_sesion_05oct_v1` |

## 11. Pendientes de delamor — la lista completa (orden: instrumento, IAP, devices, servicios)
**Instrumento**
1. **Leer el v34** (`_borrador` y `_print`).
2. **El criterio de calibrate:** ¿los extremos (hoy) o el máximo (§9)? Primero se mide exacto (texto para Code); después decidís.
3. **¿Se pondera por masa en `services/analytics.py`** (CRITERIOS C.4–C.5)? Cambia lo que miden copresence_matrix, cluster_nodes, perfect_oppositions y node_presence. Recomendación de Opus: sí, porque es lo que ya decía el 11 sep y ya existe en el driver de Néel.
4. **El rótulo de `expulsados`.** Abierto desde el 8 oct.
5. **Los otros rótulos abiertos de §N:** OPERADOR_STOP_COCO en el código, Gatekeeper, los verbos de "agregar un nodo" y los prefijos del Orden BABEL.

**Paper (el review del v34)**
6. **¿Entran SALAMANCA y Néel?** (§7.1)
7. **¿Entran los criterios de W sola (D.1–D.4) y la distinción topológico / métrico?** (§7.3)
8. **Review, ítem 1:** "field" con tres sentidos. ¿Cuál es *el campo*, y cómo se llaman los otros dos?
9. **Review, ítem 7:** calibrar compara N_eff0 con F(N), que no depende de W. Se cruza con el punto 2.
10. **Review, ítems 18 y 28:** §3.3 (la verificación por convergencia independiente) y §7.6 (*"representar conocimiento y medir el campo son dos perspectivas de lo mismo"*): ¿se sostienen como están, se fundamentan o salen?
11. **Review, ítem 34:** ¿contra qué se ubica el aporte de N_eff (Chao1, Good–Turing, la literatura de riqueza de especies)?
12. **R8 / review, ítem 27:** quién revisa la literatura de KR 2023–2026 y cómo; mientras tanto, la afirmación de §7.6 sobre KR.
13. **Acknowledgments:** *"verified all references"* con R9 pendiente, y nombrar a Claude Opus 5, el modelo de Code. Es tu voz.

**IAP**
14. **El OK para pasar el REG del intento 5 a `registers/`**, después del texto 22.

**Infraestructura**
15. **Codespace:** esperar el ciclo de facturación o subir el presupuesto (la hora de 2 núcleos cuesta USD 0,18). Lo que espera al Codespace: el texto 22, P19 A, el d exacto de la grilla (§9) y §5.2 a HEAD (review, ítem 38).

## 12. Lo que no hizo esta revisión
- No leyó las DEFS v20 enteras: §N, §OP, §15, §16 y §17, y las filas que se nombran.
- No leyó CRITERIOS §C.1, C.3–C.5 en detalle, ni las TASK de SALAMANCA y Néel v1–v5, ni la SUPERTASK.
- No leyó `services/cluster_frontier_density.py` ni el driver de Néel enteros.
- Las calibraciones de los intentos 3 y 4 que no son la última de cada log no se leyeron desde la PC: el §9 usa el paper para los máximos de los intentos 2 y 3, y deja seis del intento 4 sin leer.
- No corrió nada.
