# Texto para Code — 20 — repo ckm — el margen exacto, la simetría σ ↔ −σ, el CP-E y la torsión — 29 oct 2026 (Opus 5.5)

*Reemplaza entero al texto 18 (el punto 2 de aquel, λ*, sigue cerrado). Respalda los Pendientes R1, R2 y R3 del paper v33 y suma la medición de la torsión que decidió Opus. delamor, 29 oct: "tenes mi aprobación para lo que decidas OPus que sostenga o de robustez"; "textos y tareas para Code… autónomas". Va antes del texto 21, que es independiente de éste.*

```
Code: cuatro mediciones, sin tocar services/ ni iap_chatroom/. Por favor.
Es instrumento: primera prioridad (delamor: CKM, IAP, devices, servicios).

Cómo, por favor:
- En el Codespace, el git pull --rebase y el push los hacés vos.
- Este texto es UNA unidad: los cuatro puntos de corrido, en este orden,
  sin esperar a delamor ni a Opus. Si un punto encuentra una tensión, anotala
  en la BANDEJA, dejá ese punto (o la parte afectada) y seguí con los demás.
  A1.PAUSA sólo al final.
- Leé primero docs/opus/decisiones_en_el_acto.md: 28 oct, desde "La medida
  de referencia es la del código", y 29 oct (noche) entero.
- Scripts en experiments/, cada uno con su docstring: qué mide, con qué
  condiciones y qué declara. Regla de .py: A1.PAUSA al acceder; después de
  modificar, el docstring propio y grep de los nombres tocados en el resto
  del repo.
- Defaults (delamor, 29 oct): donde se muestree con el instrumento, n_runs
  = 200, seed = 0 y la distribución uniforme (sampling_mode "uniform": la
  banda de sample_s0 con elección uniforme de nodos), leídos de
  ckm_landscape_config (N_RUNS_DEFAULT, SEED_DEFAULT), no escritos a mano.
  Cualquier otro valor (la enumeración exacta, el 1000 y las seeds 0–9 del
  CP-E reproducido) lo declara el driver en su docstring y en su salida
  como declaración propia, con su razón.
- Enumeración exacta: cada estado pesado por su probabilidad bajo sample_s0,
  como en experiments/piso_del_colapso.py. Usá eso, no lo reescribas.
- En toda tabla: N y su paridad (par/impar) como columnas (delamor, 29 oct:
  "N paridad"). Sólo se mide: sin nombrar qué significa.
- Sin interpretación, y sin elegir ningún número para que algo separe.

1. El margen exacto de las 14 W de las curvas (intentos 2, 3 y 4; R1).
   Contexto (definición candidata, no registrada): con los extremos, el
   margen es m = 1 − ln F / ln N_eff0, con F = N_eff del colapso de N nodos
   bajo la medida; "separa" ⇔ N_eff(W) > F(N, μ). F cerrada: N impar → 2;
   N par → 1/((1−2,5/N)²/2 + 2(2,5/N)²/C(N,N/2)); F(20) = 2,612244.
   Para cada W, reconstruida y verificada por su sha (como en el 14.1):
   - N_eff0 exacto por enumeración;
   - F(N) por la forma cerrada y, una vez por N, por enumeración del
     colapso, como control;
   - m exacto y su signo;
   - al lado: lo que registró calibrate (N_eff0 y margen muestreados, su
     estado, su n_runs) y el IC del 14.1;
   - además, N_eff0 muestreado a 200 / 0 / uniforme, el default de hoy
     (el intento 4 calibró a 1000).
   La W bdb98f5b del intento 3, la única que separó, en la primera fila.

2. N_eff ≥ 2 por la simetría σ ↔ −σ (R3). El v33 la deja como Pendiente:
   "salvo órbitas autosimétricas dominantes". Por favor, que la pruebes o
   la refutes, sin forzar ninguna de las dos.
   a) La prueba corta, contra el código (líneas de relax_orbit y sample_s0):
      - ¿el mapa síncrono con la regla de empate (h = 0 → se queda) cumple
        f(−σ) = −f(σ)?
      - ¿la medida es invariante bajo σ → −σ? Revisá P(n_act = k) =
        P(n_act = N − k) para cada N de 2 a 21 con el redondeo real de
        numpy y el max(1, ·), y la elección uniforme de nodos.
      - Entonces las órbitas vienen en pares O ↔ −O de igual masa. Pero
        una órbita puede ser su propia imagen (O = −O, por ejemplo
        {σ, −σ} de período 2: en el colapso con N par ocurre en los
        estados balanceados). Escribí la condición exacta bajo la que vale
        N_eff ≥ 2, y la cota que queda cuando hay masa en órbitas
        autoconjugadas.
   b) Búsqueda de contraejemplos, exhaustiva: todas las W simétricas, de
      diagonal cero y entradas en {−1, 0, +1}, para N = 2..5, con N_eff
      exacto. Para N = 6..8, una muestra de 10.000 W por N (seed 0,
      declarada; no es la seed del instrumento, es la de la muestra de W).
      Por N y paridad: el N_eff mínimo, la W que lo da, cuántas W dan
      N_eff < 2 y cuánta masa autoconjugada tienen.
   c) Sobre las 14 W del punto 1: cuántas órbitas autoconjugadas hay,
      cuánta masa tienen (exacta), y si el estimador a 200 / 0 / uniforme
      da menos de 2 aunque el exacto no.
   d) Verificá también la línea del REG de fourforums v8n que el paper
      cita: "relax(−σ) = −relax(σ): las órbitas vienen en pares ±". Decí
      si vale tal como está escrita, o con qué condición.
   e) La paridad de n_runs contra la de N, sobre el colapso (delamor, 29
      oct: "n de n_runs par pasa tal cosa, n_runs para colapso tal > 2,
      impar tal cosa… vs torsión"). Lectura de Opus, para que la verifiques:
      con N impar el colapso tiene dos cuencas ± de masa 1/2, y el plug-in
      1/(p² + (1−p)²) es ≤ 2, con igualdad sólo si cada lado recibe
      exactamente n_runs/2, lo que exige n_runs par. Con N par, F(N) > 2 por
      las órbitas balanceadas. Por favor, la distribución del plug-in de F
      (media, percentiles 5/50/95 y P(≥ F)) para N = 4..21, con n_runs =
      199, 200 y 201. El 200 es el default; 199 y 201 los declara el driver,
      con esta razón. Exacta por la binomial donde se pueda (N impar); si no,
      con 1000 seeds declaradas (0..999).
   Si (b) encuentra W con N_eff < 2, reportalas: no ajustes el enunciado
   para que valga.

3. El "15.52 → 5.27" del CP-E (R2; commit 0e042ac). El v32 dice que un
   texto más mueve N_eff un 66 % en A24 (15.52 → 5.27); 5.27 es también
   el N_eff base de D12, y por eso el v33 sacó la frase hasta saberlo. Ya
   verificado por Opus en el repo local: la columna "+1 texto" del driver
   es |extra − base| / base y da 0,660 en A24; los tres corpus no
   cambiaron desde 0e042ac; el extractor sí (min_df = 2, signo por palabra
   completa con NFC, pool ≤ top_k: 9414157, 595d0b7 y otros).
   a) Reproducí el CP-E en 0e042ac: git worktree en un directorio fuera
      del repo (por ejemplo /tmp/ckm_0e042ac), y corré
      experiments/driver_cpe_rango_neff.py sin cambios. El driver declara
      n_runs = 1000 y las seeds 0–9: es una reproducción, y así se declara.
      Guardá la salida completa. Decí qué N_eff da A24 "+1 texto"
      (media ± sd) y la base de D12.
   b) Lo mismo en HEAD. Si el driver no corre igual por cambios de API,
      hacé una copia experiments/driver_cpe_rango_neff_head.py con las
      adaptaciones mínimas, cada una declarada; services/ no se toca.
   c) La tabla 0e042ac contra HEAD, celda por celda. Los números del
      paper (§4.3.2: 15.52 ± 0.32, 5.27 ± 0.16, 10.10 ± 0.20 y la tabla de
      perillas) son de 0e042ac: decí cuáles cambian con el extractor de hoy.
   Borrá el worktree al terminar (git worktree remove).

4. La torsión: lo que deja afuera el rechazo completo de período 2
   (decisión de delamor del 8 oct, CP3 1a; Opus decide medir, 29 oct).
   A Δ_r_pares entran sólo los pares rechazados en las dos fases de la
   órbita; la torsión va a Δ_r_torsion y no entra a W_eff
   (services/monitor_service.py:328-350). Los logs del driver de los
   intentos 2–4 no guardan periodo_orbita ni n_torsion.
   a) Buscá los estados preservados de los intentos 2, 3 y 4 en process/
      (los mueve el --reset, con timestamp). Para cada uno, de
      monitor_trajectory.jsonl, por evaluación de Monitor: periodo_orbita,
      cola_orbita, n_aceptados, n_expulsados, n_torsion, Delta_r_sum,
      Delta_r_torsion_sum, N y su paridad. Una tabla por intento y un
      resumen: cuántas evaluaciones de período 2, cuántas con torsión > 0.
      Si un estado no está, o el archivo no tiene esas claves, decilo.
   b) Sólo si hay torsión > 0 en algún intento: la contrafáctica offline.
      Reconstruí por ciclo Δ_r_pares y Δ_r_torsion (con lo que el estado
      guarde; verificá la reconstrucción contra el Delta_r_sum registrado,
      como control) y calculá, con la función del código que arma W_eff,
      el N_eff de W_eff tal como es y el de W_eff con Δ_r_pares +
      Δ_r_torsion: a 200 / 0 / uniforme, y exacto si N ≤ 21 en la última
      evaluación de cada ciclo. También el D_ckm^Monitor de los dos.
      Sesgo declarado (Opus): la contrafáctica supone que la torsión
      entraría con la misma regla que los expulsados. Es una elección del
      experimento, no del instrumento: escribilo en el docstring.
      Si no se puede reconstruir, decí qué falta, sin inventarlo.
   c) Si no hay torsión en ningún intento: reportalo con la tabla de (a), y
      no armes la contrafáctica.
   d) Las órbitas autoconjugadas y la torsión ("vs torsión", delamor, 29
      oct). Lectura de Opus de pares_por_orbita (landscape_engine.py:93-146),
      para que la verifiques: un par está expulsado en una fase si alguno de
      sus nodos está en −1. En una órbita {σ, −σ} los caídos de una fase son
      los activos de la otra. Entonces un par con un nodo caído y el otro
      no queda expulsado en las dos fases; un par con los dos nodos del
      mismo lado queda en torsión. Si es así, el rechazo completo deja
      afuera justo esos pares en las órbitas autoconjugadas. Por favor:
      - verificalo con el código, sobre el colapso con N par (4..20), con
        un sigma_prompt de la banda: cuántos pares aceptados, expulsados y
        en torsión, por N;
      - lo mismo sobre las W del punto 2b que tengan masa autoconjugada, y
        sobre las órbitas autoconjugadas de las 14 W (punto 2c), si las hay;
      - también para las órbitas de período 2 que no son autoconjugadas
        ({a, b}, b ≠ −a), separadas de las otras.
      Sólo se cuenta: no se decide nada sobre qué entra a Δ_r.

NO: tocar services/ ni iap_chatroom/; cambiar calibrate, el margen, la
grilla, el estimador, los defaults o qué entra a Δ_r; registrar ninguna
definición (lo hace Opus con tu reporte); λ*; el vivo (es el texto 21);
lo de los textos 17 y 19.

Al cerrar: la suite completa, en serie. Reporte en
docs/tasks/BANDEJA_code.md, uno por punto, sin veredicto global. Scripts y
resúmenes (JSON) en experiments/. Commits nombrando archivos, uno por punto.
Pull --rebase y push. A1.PAUSA.
```
