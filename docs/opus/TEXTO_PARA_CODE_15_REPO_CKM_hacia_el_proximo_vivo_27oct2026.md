# Texto para Code — 15 — repo ckm — hacia el próximo vivo: cinco puntos bajo el umbral — 27 oct 2026 (Opus 5.5)

*Va después del texto 14. Decisiones de Opus, con el OK de delamor (27 oct: "sip porfa Opus").*

```
Code: cinco puntos, después del texto 14, en este orden. Por favor.

- En el Codespace, el git pull --rebase y el push los hacés vos.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring propio
  y grep de los nombres tocados en docstrings y comentarios del resto del repo.
- Unidad: cada punto, de corrido. Sin pausa entre puntos salvo que uno
  encuentre una tensión: A1.PAUSA sólo para ése y seguí con lo demás.
- Para qué: dejar preparado el próximo vivo, que todavía no está definido.
  Ningún punto corre un vivo.

1. Probar iap_chatroom/correr_caso0.sh --check. Nunca corrió como script
   (lo dijo delamor en el CP3). --check hace todo menos el caso y gasta 4
   llamadas (una de Gemini: cuota de 20 por día y por modelo). Antes de
   correrlo, que no haya server en el 7860. Reportá paso por paso qué hizo,
   y si algo falla, por qué, sin arreglarlo en caliente: si el arreglo es
   del script (no del caso ni del instrumento), hacelo en un commit aparte y
   volvé a correr --check una sola vez. Atención: --check también hace el
   --reset, que mueve experiments/_state_S2-C0/ del intento 4 a process/
   con timestamp (no borra). Verificá que quedó preservado.

2. La caída de device B en el intento 4, sólo lectura. El REG
   (registers/REG_iap_serie2_caso0_intento4_v1.md, §2) dice: McpError
   "Timed out while waiting for response" en el cierre del cliente
   (autonomous_device.run, Client.__aexit__), y B hizo 90 vueltas contra
   223 y 228 de A y C (~40% del tiempo). Por favor: cuándo dejó de dar
   vueltas (t del último tick de B), qué estaba haciendo en ese momento,
   si el timeout ocurrió al cerrar o antes (y el cierre sólo lo levantó),
   y qué dice el log del server en ese tramo. Con línea de código y de log.
   Sin arreglar nada: el arreglo, si hace falta, se decide con el reporte.

3. El test prometido el 26 oct: AgentDeviceSkin, por default, no aplica el
   criterio local. Hoy ningún test de tests/ lo construye con o sin
   criterio (sólo test_caso_serie2_caso0_diseno.py verifica que el caso 0
   no lo usa). El test: un AgentDeviceSkin sin local_criterion no filtra
   ninguna vuelta (ningún SKIP por criterio) y su panel lo dice como
   ausencia (None, no un panel en cero), como ya hacen los de
   AutonomousDevice en tests/test_local_criterion.py. Además, grep: ¿algún
   driver le pasa un local_criterion a un AgentDeviceSkin? Reportalo. Si el
   skin debe rechazar un criterio local es otra decisión, de delamor, y no
   está tomada: no lo implementes.

4. Inventario de defaults, sólo lectura (insumo de la TASK de defaults; no
   se implementa nada). Una tabla, un parámetro por fila, para los
   parámetros con default de función o de módulo en services/ e
   iap_chatroom/ (sin tests/ ni experiments/), con tres columnas que pidió
   delamor el 26 oct:
   (a) dónde se declara antes de que empiece un flujo, o "no se declara";
   (b) si aparece en la traza o el panel como default (con su valor y de
       dónde sale);
   (c) si no se declara: por qué, y qué impacto tiene.
   Incluí el state_dir por default de CKMMonitor (E1) y los de server.py.
   Marcá los que ya resolvió el texto 13 (n_runs y seed vía sampling_for).
   Medido en el CP2: en la Config un default y una declaración explícita
   del mismo valor no se distinguen; decí si pasa lo mismo en otros lugares.
   Va a docs/tasks/INVENTARIO_defaults_v1.md y un resumen a la BANDEJA.

5. El docstring de coco.py:173-175. Mediste en el texto 13 que, tal como
   está escrito, ya no es cierto (habla de "contar atractores" y del sesgo
   del conteo, y _count_attractors devuelve n_eff; el sweep 60→70 no lo
   corre la suite). Corregilo para que diga lo que el código hace hoy, con
   la referencia a lo que el sesgo medido era y a dónde vive
   (deprecated_count_attractors), sin cambiar código ni el 80 de la firma.
   Si el texto 14 midió algo sobre el sesgo del estimador de N_eff con
   n_runs (el plug-in de Simpson), citalo; si no, no lo afirmes.

NO: el margen, la grilla, el patrón de calibrate, el muestreo, el
state_dir (E1, espera el inventario y el --check), P14, la medida de
referencia, w_sha_match, el vivo.

Reporte en docs/tasks/BANDEJA_code.md (sin veredicto global), commits
nombrando archivos (uno por punto), suite completa en serie al cerrar,
pull --rebase y push. A1.PAUSA.
```
