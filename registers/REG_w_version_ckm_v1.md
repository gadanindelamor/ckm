# REG_w_version_ckm_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Jul 2026. W versionado era la dependencia bloqueante
de Firma_CKM (REG_firma_corpus_v1) y de IAP Highway Network.
Implementado en esta sesión como paso previo a Firma_CKM.

---

## Qué es W versionado

No es una copia de W en cada momento.
Es un historial de **marcas livianas** (WTracePoint) que registran
que W cambió, cuándo, a qué tamaño de corpus, y por qué evento.

**Lo que no almacena:** el contenido de W.
**Lo que almacena:** la huella de que W cambió.

---

## Plano separado

W versionado opera en un plano distinto de STOP/Δ.
STOP limpia Δ_r — nunca alcanza las marcas de versión de W.
W es invariante intra-ciclo. Las marcas registran los límites
entre ciclos (cambios de corpus).

---

## Implementación

**Archivos nuevos:**
- `services/w_version.py` — WVersionManager + WTracePoint + sha256_W()
- `services/test_w_version.py` — 9/9 tests passing

**Archivo modificado (cirugía):**
- `services/corpus_service.py` — 7 cambios sobre repo. API pública preservada.

**Archivo corregido:**
- `services/monitor_service.py` — 1 cambio. Bug T5: `_Delta` → `_Delta_r`.

---

## API pública — WVersionManager

```python
vm = WVersionManager()

# Registrar cuando W cambia (llamado desde _rebuild() en CorpusService)
sha = vm.register(W, corpus_size=len(texts), causal_event="rebuild")

# Consultar estado actual
vm.current_sha()          # → str | None — para Firma_CKM
vm.current_corpus_size()  # → int | None

# Señal de invalidación para beta_c_corpus
vm.changed_since(sha_anterior)  # → bool
# True = W cambió = beta_c_corpus debe re-estimarse

# Historial
vm.history()   # → List[WTracePoint]
len(vm)        # → int

# Serialización (se persiste en corpus_state.json)
vm.to_list()         # → list
vm.from_list(data)   # → None
```

---

## Integración en CorpusService

```python
# En __init__:
self._w_versions = WVersionManager()

# En _rebuild() — al final, después de self._W = W:
self._w_versions.register(W, len(self._texts), causal_event="rebuild")

# En status():
"w_sha": self._w_versions.current_sha()   # campo nuevo

# Métodos públicos nuevos:
corpus.w_sha()                   # sha256(W_momento) para Firma_CKM
corpus.w_changed_since(sha)      # señal de invalidación

# En save() / _load():
"w_version_history": self._w_versions.to_list()  # persiste en JSON
self._w_versions.from_list(state.get("w_version_history", []))
```

---

## WTracePoint — campos

```python
@dataclass
class WTracePoint:
    timestamp   : float   # time.time() en el momento del cambio
    sha256      : str     # sha256(W.tobytes()) — 64 hex chars
    corpus_size : int     # len(texts) cuando W fue construida
    causal_event: str     # "rebuild" | str libre
```

---

## Invariantes verificados (9/9 tests)

- `register()` crea marca con sha correcto
- W idéntica no crea marca duplicada
- W distinta crea segunda marca
- `changed_since()` detecta cambio de W
- Estado inicial: `current_sha() == None`
- Serialización roundtrip preserva historial completo
- `corpus.w_sha()` presente en `status()` tras `ingest()`
- sha cambia cuando W se reconstruye con textos nuevos
- sha persiste entre sesiones (JSON roundtrip)

---

## Qué desbloquea

**Firma_CKM** — `sha256(W_momento)` ahora disponible como `corpus.w_sha()`.
El campo `Firma_CKM.sha256(W_momento)` de REG_firma_corpus_v1 puede ser
poblado en el momento del evento a certificar.

**beta_c_corpus invalidación** — `corpus.w_changed_since(sha)` señaliza
que beta_c_corpus debe re-estimarse. No dispara recalculación automática
(diseño conservador — delamor decide cuándo recalcular).

**IAP Highway Network** — tiene suelo de referencia verificable.

---

## Lo que no hace

No implementa Firma_CKM completa — ese es el próximo paso.
No recalcula beta_c_corpus automáticamente cuando W cambia.
No almacena copias históricas de W — solo las huellas.

---

## Estado

- w_version.py: implementado, en repo local
- test_w_version.py: 9/9 passing, en repo local
- corpus_service.py: actualizado, en repo local
- monitor_service.py: bug T5 corregido, en repo local
- Firma_CKM: desbloqueada — pendiente implementación

---

*Jul 2026*
