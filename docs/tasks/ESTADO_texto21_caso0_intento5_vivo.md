# ESTADO — texto 21 (el vivo: serie2_caso0, intento 5, con los defaults 200 / 0 / uniforme)

*Lo escribe Code (Opus 5) en el Codespace. Última escritura: 2026-10-29 23:45 UTC.*

Fuente: `docs/opus/TEXTO_PARA_CODE_21_REPO_CKM_caso0_intento5_vivo_200_seed0_29oct2026.md`.
Orden de delamor en el chat, 29 oct. Reportes en `docs/tasks/BANDEJA_code.md`.

## Cerrado — los tres puntos

| punto | qué | commit |
|---|---|---|
| 1 — chequeo previo | suite 910 recolectados / 903 passed; muestreo 200/0/uniform en los tres casos; el cambio del caso declarado y verificado equivalente | `180844e` |
| 2 — el vivo | `correr_caso0.sh` completo, exit 0, 1204,67 s, 0 errores en los cuatro devices | `dc48298` |
| 3 — el registro | `docs/REG_borrador_serie2_caso0_intento5.md` + `experiments/registro_intento5.py` | `dc48298` |

Log del driver commiteado con los dos nombres (`..._20261029T231324Z_log.json` y
`..._intento5_log.json`). `experiments/_state_S2-C0/` no se commitea.

## Espera

1. **delamor:** el OK para que el REG borrador pase a `registers/` (Clase R). Y las preguntas
   abiertas: **P19** (del texto 20), **P13**, **P14**, **P17**, **P18**.
2. **Opus:** leer el REG borrador y los reportes de los textos 20 y 21, y registrar lo que es del
   modelo.

## Lo que quedó medido y nadie decidió

- **La W con la que cierra el vivo (`6c16bb08`, 40 textos) nunca se calibró ni se evaluó**, y su
  margen exacto es **+0,491519**: separa. El rebuild `volumen` que la creó ocurrió en el instante de
  la última evaluación de Monitor y no hubo ninguna después.
- **`Σ Δ_r = 0,0`** en toda la corrida: los 745 pares declarados quedaron aceptados, ninguno
  expulsado, `W_eff = W`, `D_ckm = 0,0` en las 11 evaluaciones. Los intentos 2, 3 y 4 habían
  acumulado 3136, 768 y 3880.
- **`N_eff0` muestreado 1,983930 contra exacto 2,056066** en la W calibrada: el estimador a 200 cruza
  por debajo de 2 donde el exacto está por encima.
- **P17 y P18 quedaron medidos** (el `--reset` sí se lleva el residuo del `--check`; la recolección
  pasó de 910 a 913 con la W nueva), pero **las dos siguen sin decisión**.

## Corregido en la BANDEJA

El reporte del chequeo previo (23:12 UTC) nombró modelos que no son los del repo: los puse yo en mi
script de verificación en vez de leerlos del archivo, y de ahí salió también una "deriva de
comentario" en `correr_caso0.sh` que **no existe**. Corregido en la entrada de las 23:42, sin
reescribir la anterior. Los modelos reales son `openai/gpt-oss-120b`, `gemini-3.5-flash-lite`,
`openai/gpt-oss-20b` y `qwen/qwen3.8-27b`.
