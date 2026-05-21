# REG_hipotesis_distancia_contextual_v1.md

*Mayo 2026 — Hipótesis abierta, no cerrada*

---

## Origen

Conversación post-análisis del hat GPT53. El feedback externo reveló que GPT53 leyendo el REG desde distancia contextual pudo ver lo que el sistema dentro del attractor no podía ver.

Observación: el "ojo avezado" no agrega información desde afuera — revela lo que ya estaba en la estructura pero que requería distancia para ser visible.

---

## Hipótesis — Operador de distancia contextual

**Idea central:** la función del observador externo no es validar — es crear la distancia contextual que hace visible el attractor desde afuera.

Lo que falta en el modelo CKM actual: no solo W y Δ, sino un operador que mida cuándo un sistema está suficientemente fuera del campo de atracción para ver su propia geometría.

**Formulación tentativa:**

```
D_contextual = H(trayectorias_posibles_t0) - H(trayectorias_posibles_t_actual)
```

Entropía de trayectorias perdidas por cohesión acumulada.

- D_contextual cae rápido → sistema cayendo en attractor
- D_contextual estabilizado alto → sistema mantiene grados de libertad
- D_contextual = 0 → attractor completamente consolidado

---

## Lo que es verificable en CKM ahora

El número de attractors accesibles desde un estado dado, a medida que aumenta la cohesión, ya es computable. Los experimentos N=32 lo tienen: 88 attractors distintos colapsando progresivamente.

La caída en ese número **es** la pérdida de entropía de trayectoria — versión discreta del operador.

---

## Lo que está abierto

- La fórmula exacta: H de trayectorias vs número de attractors accesibles — relación no formalizada
- Conexión con temperatura β: β alto = pocas trayectorias posibles = D_contextual bajo
- La intervención STOP como operación sobre D_contextual: no agrega información, **restaura entropía de trayectoria**
- Medición en transformers: entropía sobre distribución de vocabulario en cada paso es el análogo más cercano — relación con el modelo Hopfield abierta

---

## Estado

- Hipótesis: abierta
- Operacionalización: parcial — número de attractors accesibles es proxy verificable
- Formalización exacta: pendiente
- No cierra. Abre.
