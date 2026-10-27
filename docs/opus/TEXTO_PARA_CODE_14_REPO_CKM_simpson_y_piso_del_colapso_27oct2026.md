# Texto para Code — 14 — repo ckm — dos mediciones: el intervalo de Simpson y el piso del colapso — 27 oct 2026 (Opus 5.5)

```
Code: dos mediciones y una lectura, sin tocar el instrumento. Por favor.
delamor, 27 oct: "si. CONFIRMO" a las dos mediciones; y sobre el piso: "N
es variable, y sería una referencia de piso variable también? y sería en
qué condiciones? en qué se sostiene?".

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados. Acá no se modifica services/: los scripts van
  a experiments/ con su docstring (qué miden, con qué condiciones).
- Unidad: cada punto, de corrido. A1.PAUSA al final.
- Sin interpretación: se mide y se registra. Ningún resultado se usa para
  elegir un margen, un umbral ni un percentil (la tensión del margen se
  sostiene).

1. El intervalo de Simpson sobre las curvas que ya existen (intentos 2, 3 y
   4: las curvas de calibrate). Para cada punto de cada curva:
   - N_eff como lo calcula el código hoy (plug-in, 1/Σ(c/n)²);
   - N_eff con el estimador insesgado de Simpson (1949) para Σm²:
     Σ c_k(c_k − 1) / (n(n − 1));
   - un intervalo aproximado para Σm² con Var ≈ (4/n)·(Σm³ − (Σm²)²)
     (método delta), llevado a N_eff y a d_ckm.
   Si los conteos por cuenca no están guardados, recomputalos con la misma
   W, n_runs y seed de cada registro (es determinista) y decí que se
   recomputaron. Reportá también, para cada curva, si el intervalo de
   λ=0 se superpone con el de cada λ. Las fórmulas y la cita están "a
   verificar": si encontrás que alguna está mal, decilo antes de usarla.

2. El piso del colapso, por enumeración, con N = 20 y otros N.
   Lo que Opus calculó a mano, a verificar (no lo des por cierto):
   con extremo_colapso (todos los acoplamientos = escala, diagonal 0),
   dinámica sincrónica de relax_orbit y la regla de empate "conserva σ",
   un σ con S = Σσ ≠ 0 va en un paso a todos +1 o todos −1, y un σ con
   S = 0 (N par) cae en una órbita de período 2 {σ, −σ}. Entonces:
   - bajo la medida uniforme sobre {−1,+1}^N: N impar → N_eff = 2 exacto;
     N par → N_eff = 1 / ((1 − p0)²/2 + p0·2^(1−N)), p0 = C(N, N/2)/2^N
     (N=20: 2,9470; N=40: 2,6145; tiende a 2 cuando N crece);
   - bajo la medida que usa el código (sample_s0: fracción activa uniforme
     en [0,3; 0,7], después un subconjunto al azar), con N=20:
     P(todos −1) = P(todos +1) = 0,4375 y P(S=0) = 0,125, y
     N_eff exacto ≈ 2,6122.
   - Lo medido en las 7 curvas es 2,4369 (n_runs = 200, seed = 0).
   Por favor: (a) verificá la dinámica y la regla de empate en el código;
   (b) enumerá los 2^20 estados del colapso y calculá N_eff exacto bajo las
   dos medidas (la del código, pesando cada estado por su probabilidad bajo
   sample_s0); (c) hacé lo mismo para algunos N (por ejemplo 10, 11, 19, 21,
   y los que tengan las W del repo); (d) decí si 2,4369 cae dentro de lo
   que el muestreo con n_runs = 200 y seed = 0 puede dar alrededor del
   valor exacto, o si hay algo que mi cálculo no ve.

3. Lectura, sin cambiar nada: la medida de referencia.
   - El paper v32 declara "uniform sampling of σ₀ ∈ {−1,+1}^N" (l.264) y
     valida contra enumeración "under the uniform reference measure on
     {−1,+1}^N" con 100.000 estados muestreados (l.346).
   - sample_s0 (landscape_engine.py:234) no muestrea uniforme sobre el
     hipercubo: sortea la fracción activa uniforme en [0,3; 0,7] y después
     qué nodos. "uniforme" en el código es "uniforme sobre nodos".
   Decí: qué muestreo usó la validación de l.346 (el script o el REG que
   la sostiene), y si la comparación fue con la misma medida en los dos
   lados. Sin corregir el paper ni el código: es para que delamor decida
   cuál es la medida de referencia declarada.

NO: cambiar el estimador del instrumento, el margen, la grilla, el patrón de
calibrate, el n_runs, el muestreo; el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), los scripts en
experiments/ con su salida, commits nombrando archivos, suite en serie si
tocaste algo fuera de experiments/, pull --rebase y push. A1.PAUSA.
```
