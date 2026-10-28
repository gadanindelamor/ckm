# Texto para Code — 18 — repo ckm — el margen contra el piso exacto (λ* cerrado) — 28 oct 2026 (Opus 5.5)

*Va después del texto 17. delamor, 28 oct: "si. de acuerdo. el MATIZ: el punto 2 que no vuelva dentro de 4 días a golpear la puerta. cerremos y avancemos".*

```
Code: una medición, sin tocar services/. Por favor, en este orden.
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
- Unidad: el punto 1, de corrido. A1.PAUSA al final.

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

2. λ*: NO se hace. Cerrado por declaración (delamor y Opus, 28 oct): λ*
   es un número por cada W, no por N; la enumeración sólo alcanza N chico
   (~20) y con N grande obliga a muestrear, que es el ruido que la
   definición evita; y la definición candidata no lo necesita. Si algún
   día hace falta describir una W por cuánto resiste el colapso, se busca
   una cota analítica, no una enumeración.

NO: cambiar calibrate, el margen, la grilla del instrumento, el estimador,
el n_runs; registrar la definición (lo hace Opus con tu reporte); el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), scripts y
resultados de resumen en experiments/, commits nombrando archivos, pull
--rebase y push. A1.PAUSA.
```
