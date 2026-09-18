# TASK_traza_gatekeeper_c1_v1.md

*Sep 2026 — gadanin.delamor + Claude Sonnet + Claude Code (Opus 5)*

*Contexto: PROPUESTA_ckm_landscape_dynamics_v4.md, D4. Precondiciones: TASK_gatekeeper_C1_theta_W_v1 (`f8d61ef`), TASK_invalidacion_delta_r_v1 (`341f612`).*

---

## Qué hacer

El panel registra si C1 se evaluó y con qué θ_W. Hace trazable la distinción entre **rechazo** (admisión, node-level) y **metabolización** (pair-level, Δ_r) sin cambiar ninguna mecánica.

## Acuerdos (delamor)

1. **Solo registrar (opción a).** Hoy ningún servicio evalúa C1: `gatekeeper_c1` existe en `services/` y nadie lo llama. La clave del panel queda en `None` y eso es el dato: Δ_r es metabolización sin admisión previa.
2. **La configuración del gatekeeper va a la config.** θ_W ya viaja en `CKMlandscapeConfig`; el σ contra el que se evalúa C1 falta. **Quién escribe la evaluación se decide después.** Queda abierto y declarado, no implementado a medias.

## Comportamiento

- `panel["gatekeeper_c1"] = None` — C1 no evaluado en esta evaluación.
- Cuando alguien lo conecte, esa clave llevará al menos el θ_W usado.

## Verificación

- La clave `gatekeeper_c1` está presente en todos los paneles, con y sin `landscape_config`.
- Vale `None` en todos los paneles actuales.
- Tests existentes sin regresión.

## Qué no hace

No evalúa C1. No filtra ni admite nada. No toca `gatekeeper_c1.py`, Δ_r ni la metabolización.

## Abierto

- Quién evalúa C1 y en qué momento del flujo.
- σ contra el que se evalúa C1 (`sigma_prompt` — lo declarado — o `sigma_relaxed` — lo que el campo sostuvo). Son preguntas distintas.
- Que el σ del gatekeeper viaje en `CKMlandscapeConfig`, junto a θ_W.
