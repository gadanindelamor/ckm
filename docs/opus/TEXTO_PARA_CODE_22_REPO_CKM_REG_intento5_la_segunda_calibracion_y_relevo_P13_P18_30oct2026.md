# Texto para Code — 22 — repo ckm — el REG del intento 5: la segunda calibración; y el relevo de P13, P14, P17 y P18 — 30 oct 2026 (Opus 5.5)

*Sale de la revisión de Opus de los reportes de los textos 20 y 21. Decisiones de Opus, bajo el umbral. Lectura y texto: no corre ningún vivo.*

```
Code: dos puntos, sin tocar services/ ni iap_chatroom/. Por favor.

Cómo, por favor:
- En el Codespace, el git pull --rebase y el push los hacés vos.
- Este texto es UNA unidad: los dos puntos de corrido, sin esperar a
  delamor ni a Opus. Si uno encuentra una tensión, anotala en la BANDEJA y
  seguí con el otro. A1.PAUSA sólo al final.
- Regla de .py: A1.PAUSA al acceder; después de modificar, el docstring
  propio y grep de los nombres tocados en el resto del repo.
- Defaults como siempre: n_runs = 200, seed = 0, uniforme, leídos de la
  Config. Sin interpretación.

1. El REG borrador del intento 5 dice que la W 6c16bb08 "nunca se
   calibró". Opus leyó el log del driver
   (experiments/serie2_caso0_intento5_log.json): el panel final trae un
   segundo punto_calibrate, el del rebuild "volumen" (t = 25, 40 textos),
   con:
   - w_sha 6c16bb08…, w_sha_live_at_calibration 66ea8d05…;
   - state "calibrado", D_CKM_THRESHOLD 0,252986, FRAC_REC_MIN 0,700804;
   - margen_separacion 0,505971 (curva: 6,068 / 2,375 / 1,999 / 2,359 /
     2,437);
   - n_runs 200, seed 0, duration_s 0,0805, applied_to "el COCO del
     proximo ciclo".
   La causa medida: experiments/registro_intento5.py lee las calibraciones
   de panel.coco.calibration en monitor_trajectory.jsonl, o sea sólo las
   que un COCO usó. Ésta corrió y quedó registrada
   (ckm_monitor.py:790, registrar_calibracion), pero ningún COCO nació
   después de ella. Por favor:
   a) Verificá lo de arriba en el log y en el estado preservado. Decí
      dónde queda persistido el registro de la Config (en qué archivo del
      state_dir, si está en alguno) y si la segunda calibración está ahí.
      Si sólo está en el panel final del log, decilo así.
   b) Corregí registro_intento5.py para que lea las calibraciones de su
      lugar (el registro de la Config, D3) y, al lado, cuáles usó un COCO.
      Volvé a correrlo.
   c) Corregí el REG borrador: §2 (la tabla: calibraciones 2, no 1), §3
      (las dos calibraciones, con los mismos campos), el punto 3 de §3, y
      la tabla de margen exacto: 6c16bb08 sí se calibró, con margen
      muestreado +0,506 y exacto +0,4915, y los dos dicen que separa.
      Como siempre: la entrada anterior de la BANDEJA no se reescribe, se
      corrige con una nueva.

2. El relevo de P13, P14, P17 y P18 a docs/tasks/DECISIONES_opus.md. En
   tu arranque del 29 oct figuran "sin decisión", porque no tienen entrada
   ahí. Están decididas en docs/opus/decisiones_en_el_acto.md; por favor,
   una entrada por pregunta, con la cita y la línea:
   - P13: resuelta el 27 oct (l.387; BANDEJA, 03:30 UTC, 092368f);
   - P14: punto 3 (l.401, texto 16) y puntos 1 y 2 (l.448: "ídem 4. sigue
     esa lógica"); la implementación de 1 y 2 es del texto 19;
   - P17: opción B (l.446): --check no hace --reset y usa su propio
     directorio, experiments/_check_<UTC>/; se implementa con el texto 19;
   - P18: el caso vivo se ancla a la copia preservada en process/ (l.424);
     se implementa con el texto 17.
   Si al leerlas encontrás que alguna no dice lo que acá resumo, anotalo y
   relevá lo que dice la fuente.

NO: tocar services/ ni iap_chatroom/; implementar P17, P18 o los textos 17
y 19; P19 (espera a delamor); el vivo.

Al cerrar: la suite completa, en serie. Reporte en
docs/tasks/BANDEJA_code.md, sin veredicto global. Commits nombrando
archivos, uno por punto. Pull --rebase y push. A1.PAUSA.
```
