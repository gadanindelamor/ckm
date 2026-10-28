# Texto para Code — 18 — repo ckm — el margen contra el piso exacto, y λ* — 28 oct 2026 (Opus 5.5)

*Va después del texto 17. delamor, 28 oct: "si. de acuerdo. el MATIZ: el punto 2 que no vuelva dentro de 4 días a golpear la puerta. cerremos y avancemos".*

```
Code: dos mediciones, sin tocar services/. Por favor, en este orden.
Es instrumento: primera prioridad (delamor: CKM, IAP, devices, servicios).

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Leé primero docs/opus/decisiones_en_el_acto.md, 28 oct, desde "La medida
  de referencia es la del código" hasta el final.
- Scripts en experiments/, con su docstring (qué miden, con qué
  condiciones). Regla de .py como siempre.
- Medida de referencia: la del código (sample_s0, la banda), decidida por
  delamor. Enumeración exacta: cada estado pesado por su probabilidad bajo
  sample_s0, como en experiments/piso_del_colapso.py.
- Sin interpretación, y sin elegir ningún número para que algo separe.
- Unidad: los dos puntos, de corrido. A1.PAUSA al final, o antes si el
  costo del punto 2 pasa lo declarado abajo.

Contexto (definición candidata, todavía no registrada): con los extremos,
el margen de calibrate es d(1) = 1 − ln F / ln N_eff0, con F = N_eff del
ferromagneto de N nodos bajo la medida. O sea "separa" ⇔ N_eff(W) > F(N, μ).
F tiene forma cerrada (N impar: 2; N par: 1/((1−2,5/N)²/2 +
2(2,5/N)²/C(N,N/2)); N=20: 2,612244), verificada en tu texto 14.2.

1. El margen exacto de las 14 W de las curvas (intentos 2, 3 y 4).
   Para cada W (reconstruida y verificada por su sha, como en el 14.1):
   - N_eff0 exacto por enumeración bajo la medida del código;
   - F(N, μ) por la forma cerrada (y por enumeración del colapso, una vez
     por N, como control);
   - el margen exacto m = 1 − ln F / ln N_eff0, y su signo;
   - al lado, lo que registró calibrate (N_eff0 y margen muestreados, su
     estado) y lo que da el IC del 14.1.
   Con la W bdb98f5b del intento 3 (la única que separó) en primera fila.

2. λ* — dónde termina de colapsar cada W, para que no quede pendiente.
   Definición operativa, sin tolerancia elegida: λ* es el menor λ de la
   grilla en que la partición en órbitas de W_λ = (1−λ)·W + λ·colapso es
   IGUAL a la del colapso (cada estado en la misma órbita que bajo el
   ferromagneto), por enumeración exacta. Si no se alcanza antes de λ = 1,
   se reporta "no antes de 1", con la fracción de estados (pesada por la
   medida) cuya órbita todavía difiere en cada λ.
   - Grilla: λ de 0 a 1 en pasos de 0,05.
   - Para cada λ de la grilla: N_eff exacto de W_λ y la fracción que
     difiere. Es la curva exacta de calibrate, sin semilla.
   - Costo: estimalo antes de correr (≈16 s por enumeración con N=20). Si
     las 14 W pasan de ~1 h de Codespace, corré primero las 3 del intento 3
     y 1 del intento 4, reportá, y A1.PAUSA con la estimación del resto.
   - Reportá también si λ* varía entre W y cuánto, y si coincide con el
     salto entre 0,5 y 0,75 que se ve en las curvas muestreadas. Sin decir
     qué significa.
   - Si encontrás una cota analítica de λ* (por ejemplo en función de las
     sumas por fila de |W|), escribila como "a verificar" y comparala con
     lo medido; si no, no la busques más allá de lo razonable.

NO: cambiar calibrate, el margen, la grilla del instrumento, el estimador,
el n_runs; registrar la definición (lo hace Opus con tu reporte); el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), scripts y
resultados de resumen en experiments/, commits nombrando archivos, pull
--rebase y push. A1.PAUSA.
```
