# NO ES REPRODUCIBLE. Intento de congelar las condiciones de una experiencia en vivo.

*Freeze de la serie IAP (casos 0.4–0.15). 2026-10-08 23:05 UTC — Claude Opus 5 (Code), CP0b de
`docs/tasks/TASK_canal_iap_clock_iniciativa_v2.md`. Confirmado por delamor: **copiar, no
mover**.*

**Los originales no se tocaron.** Esto es una copia. Lo congelado sigue estando donde estaba.

---

## Qué es y qué no es

delamor: *"No hay nada que revisar en la serie de tests IAP. Lo que sí hay que hacer es congelar
las condiciones. Freeze VM. Como no tenemos los recursos materiales, hacemos el INTENTO de
moverlo a process. NO ES REPRODUCIBLE."*

- **Los casos 0.4–0.15 no se revisan ni se reinterpretan.** Son experiencia del canal vivo.
- **Se reproducen condiciones, no experimentos** (delamor). Lo que pase adentro, cada vez, es
  otra experiencia.
- **Reproducir el fenómeno es imposible:** habría que reproducir el todo, y no lo conocemos
  (delamor: *"No conocemos el todo. Las interpretaciones siempre son falsas."*).

## El límite que esto no cierra, y es el más grande

**Los modelos de lenguaje no viven acá adentro.** Se llaman por API, y el proveedor los cambia o
los retira. Aunque se congelara la VM entera, cada llamada sale de ella. **El modelo es parte de
las condiciones y queda afuera.** Lo único que queda guardado son sus identificadores
(`entorno/modelos_por_caso.txt`) y las respuestas que quedaron en los logs y en los REG.

## Qué hay acá

| carpeta | qué | de dónde |
|---|---|---|
| `tests/` | los **21** `test_caso_*.py` tal como están | `iap_chatroom/tests/` |
| `registers/` | los **14** `REG_iap_caso_*.md` | `registers/` |
| `configs/` | `groq_agent_config.json` | `iap_chatroom/` |
| `_state/` | `corpus_state.json`, `corpus_G_state.json`, `monitor_trajectory.jsonl` | `iap_chatroom/_state/` |
| raíz de esta carpeta | los módulos del canal (`channel.py`, `autonomous_device.py`, `mcp_server.py`, `server.py`, `ckm_monitor.py`, `agent_device_skin.py`, …) y `providers/` | `iap_chatroom/` |
| `entorno/` | `commit.txt`, `pip_freeze.txt`, `python.txt`, `modelos_por_caso.txt` | medido al hacer el freeze |

**67 archivos, 620 KB.**

## Lo que no se pudo congelar, y se declara

1. **El modelo.** Ver arriba. Es el límite principal.
2. **No hay `.devcontainer/`** en el repo (`entorno/devcontainer_AUSENTE.txt`). La TASK propone
   *"una imagen de contenedor (devcontainer del Codespace con dependencias fijadas) más el sha"*
   como lo más cercano al alcance. **El devcontainer no existe**, así que lo más cercano quedó
   siendo `pip_freeze.txt` + el sha. Es menos de lo que la TASK propone, y se dice.
3. **No se pudo correr ni un `test_caso_*` para verificar que la copia es fiel**: no hay claves
   de provider en este entorno (`ANTHROPIC_API_KEY`, `GROQ_API_KEY`, `OPENAI_API_KEY` ausentes,
   no hay `.env`). **La copia se verificó por `diff`, no por ejecución.**
4. **Los modelos por caso salen de un `grep` sobre los REG**, no de los logs de cada corrida:
   es lo que los REG dicen, no lo que la API respondió. Si un REG no nombra el identificador
   exacto, acá tampoco está.
5. **`process/iap_series/` no existía.** La TASK dice que el freeze va *"junto a lo que ya existe
   en `process/iap/` y `process/iap_series/`"*; la segunda no existe en el repo. Esta copia
   quedó en `process/iap_series_freeze_20261008/`, al lado de `process/iap/` (81 entradas), que
   sí existe y **no se tocó**.
6. **El estado en `_state/` es de agosto** (1 y 13 de ago). No es el estado al final de la serie:
   es el que quedó en el disco.

## Después del freeze

`trigger_mode="on_message"` deja de ser el modo del canal. **Queda sólo como parte de lo
congelado**: acá, en `autonomous_device.py`, con su loop por mensaje tal como corrió la serie.
