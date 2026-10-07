# ESTADO_CKMlandscapeConfig_v3

*Estado vivo de la TASK. Lo escribe Code. Protocolo: `PROTOCOLO_code_continuidad_v1.md` §3.*

---

## Última escritura

**2026-10-07 03:54 UTC** — Claude Opus 5 (Code, Codespace `ckm`).

## Último CP cerrado

**CP0 — lectura, sin código.** Cerrado el 2026-10-07. Commit: `<este commit>`.
Base leída: `5aac176`.

## Qué se hizo

Los cuatro puntos del CP0, medidos (no supuestos). Detalle completo en
`BANDEJA_code.md`, entrada `REPORTE CP0` del 2026-10-07.

1. **Consumidores.** La lista de la TASK §3.CP0.1 se confirma y no hay ninguno más.
   Una divergencia: `services/gatekeeper_c1.py` **no importa** la config — la menciona
   sólo en un docstring (L12). No hay nada que migrar ahí en el CP3.
2. **Concurrencia.** Hay concurrencia real **de hilos, en un mismo proceso**
   (Gradio `gr.Timer(3s)` → handler sync → `anyio.to_thread.run_sync` → lee estado;
   el escritor corre en el event loop). **No** hay consumidores en procesos distintos.
   → el get y el reemplazo van bajo un mismo lock (TASK §2, primera rama).
   **No se escala.**
3. **Serializaciones históricas.** Una sola con contenido real:
   `P1P4/run_conteo_vs_masa_04oct/log_conteo_vs_masa.jsonl` (dict plano de v1).
   Los 76 paneles de `monitor_trajectory.jsonl` llevan `panel.landscape_config = None`.
4. **Medido v1 == v2.** `mu_W_nonzero = 0.005977` y `mu_W_global = 0.004519` sobre
   `services/W_ckm_corpus_v2.json`, idénticos a los declarados en la TASK.

## Qué espera, y de quién

- **Una respuesta [delamor] marcada BLOQUEA** antes del **CP2**, no antes del CP1:
  quién construye la config en el canal IAP vivo. `CKMMonitor` no le pasa
  `landscape_config` a `MonitorService`, así que hoy en vivo la config es `None` y D4
  ("Monitor abre el ciclo") no tiene sobre qué abrirlo. Ver la pregunta P3 de la bandeja.
- **Tres preguntas NO BLOQUEA** (P1, P2, P4 en la bandeja) siguen con default declarado
  y reversible si nadie contesta.

## Próximo paso

**CP1 — la clase nueva, sin tocar a los consumidores.** No está empezado. No necesita
la respuesta BLOQUEA: el CP1 no toca el canal.

## Nada quedó a medias

No hubo corte. El CP0 era lectura y se cerró entero. No se escribió código ni se tocó
`services/`.
