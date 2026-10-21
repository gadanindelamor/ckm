# Estado al cortar — 20 oct 2026
*Opus 5.5 para la próxima instancia. Reemplaza a `ESTADO_al_cortar_19oct2026.md`. Decisiones con cita: `decisiones_en_el_acto.md` (19 oct noche y 20 oct). Marco: `docs/defs/DEFS_CKM_estado_actual_v17.md` (§12 con cómo se calibra COCO, 20 oct). En GitHub hasta `fe7ed74`.*

## 1. Hecho
- **Δ_r sin normalizar, como en COCO** (`f684aee`). Misma fórmula, distintos insumos (Δ y baseline siguen distintos). Corridas "antes/después" en `experiments/medir_dos_d_ckm_*.jsonl`.
- **Diseño de `serie2_caso0`, apodo "Cimientos"** (S2-C0). Sin checkpoints. Devices genuinos, sin agentes. Consigna parcial por device, sólo en inglés (CKM no es bilingüe): el agua de una ciudad que crece, perspectivas A/B/C/D, *"may move the foundations"*. Sin coordinador, sin seed, sin explicación de los campos de CKM en el system prompt (**definición por caso: preguntarle a delamor en el próximo caso**). Sesgo declarado con su objetivo: erradicar del paper la expresión heredada *"COCO no se conectó nunca a un vivo de IAP"*. Durante el vivo, ninguna intervención.
- Code (`2dee177`…`46aeaee`): nada en castellano en lo que llega al modelo; test de que el β de cada device no va a ningún device; **todo en el mismo `state_dir`, escrito durante la corrida**; el caso listo y con su modo de ejecución declarado.
- **Intento 1 corrido** (Code, por orden de delamor; `e8db141`, REG borrador `fe7ed74` en `docs/REG_borrador_serie2_caso0_intento1.md`). Modelos usados: A groq `gpt-oss-120b`, B `gemini-2.5-flash`, C groq `gpt-oss-20b`, D groq `qwen3.8-27b`. 605 s, ZERO_SHOT.

## 2. Resultado del intento 1
- **Objetivo NO cumplido:** quedaron 13 textos de device contra los 30 que necesita el primer W, así que COCO no nació.
- **Funcionó:** el arranque sin seed (los cuatro hablaron solos), la persistencia (8 archivos en el `state_dir`) y la consigna parcial (11 menciones cruzadas; `device_a` infirió la perspectiva de `device_b` de lo publicado).
- **Por qué no llegó:**
  - 292 de 384 vueltas fueron SKIP del filtro.
  - 69 UNKNOWN, por cuatro causas: 61 × **413** (una llamada sola supera el TPM de 8000; mensajes de ~5450 caracteres de mediana × 10 de ventana ≈ 13k tokens), 6 × 429, 1 × 503 de Gemini, 1 ilegible.
  - `device_d` corrió la mitad del caso por un `McpError`.
- **Palancas para el intento 2 (REG §7):** `max_tokens` ≤ 1000 en Groq (de Code); **que la consigna pida mensajes cortos (de delamor)**; la ventana de historial del gate. `--modo CONTINUA` arranca desde los 13 textos.

## 3. Para delamor
1. ¿El REG borrador entra a `registers/`?
2. Consigna con mensajes cortos: ¿sí? ¿Con qué palabras, en inglés?
3. La unidad del conteo: hoy un texto de `'2'` vale lo mismo que uno de 5450 caracteres para llegar a los 30 del primer W.
4. ¿El intento 2 va CONTINUA (desde los 13) o ZERO_SHOT?

## 4. Abierto (sin cambio)
- Qué puede entender un device de D_ckm. `calibrate`: misma referencia, distinto camino.
- Sombra (propuesta), coordinar REG/BANDEJA/decisiones, mail IAC, CP-N, paper v29 (espera; se revisa con las DEFS v17).
- Fuera de lo técnico (delamor): *"aquí nadie está siendo evaluado"*.
