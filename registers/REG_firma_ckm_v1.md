# REG_firma_ckm_v1.md

*Jul 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Clase R*

---

## Origen

Sesión Jul 2026. W versionado (REG_w_version_ckm_v1) desbloqueó
la implementación. Firma_CKM estaba definida conceptualmente en
REG_firma_corpus_v1 desde Jun 2026. Las tres dependencias
declaradas en ese REG quedaron satisfechas en esta sesión.

---

## Dependencias satisfechas

| Dependencia | Estado |
|---|---|
| COCOThermostat (temp_signal) | ✓ — 43/43 tests |
| MonitorService (D_ckm) | ✓ — operativo |
| W versionado (w_sha) | ✓ — Jul 2026, 9/9 tests |

---

## Los 6 campos canónicos (REG_firma_corpus_v1)

```python
Firma_CKM = {
    sha256(W_momento),           # corpus.w_sha()
    D_ckm(t),                    # trayectoria[-1]["D_ckm"] | monitor._D_ckm(W)
    temp_signal,                 # thermostat.temp_signal() | "NOMINAL"
    n_agentes,                   # parámetro explícito — sin identidad si no se declara
    timestamp,                   # time.time()
    sha256(Delta_r_acumulado)    # _sha256(monitor._Delta_r) | ceros si primera firma
}
```

Sin contenido. Sin texto intercambiado. Sin nombres de agentes
si no se declaran.

---

## Implementación

**Archivos nuevos:**
- `services/firma_ckm.py` — `Firma` (dataclass) + `FirmaService`
- `services/test_firma_ckm.py` — 10/10 tests passing

**Sin cambios en archivos existentes.**

---

## API pública

```python
svc = FirmaService()

# Producir firma
f = svc.firmar(corpus, monitor, n_agentes=2)
# → Firma | None (None si corpus en acumulación)

# Verificar firma
resultado = svc.verificar(f, corpus)
# → {"w_sha_en_historial": bool, "w_sha_es_actual": bool}

# Serialización
d = f.to_dict()    # dict con 6 campos
j = f.to_json()    # JSON string
f2 = Firma.from_dict(d)
```

---

## Lógica de firmar()

```
1. w_sha = corpus.w_sha()
   → None: devuelve None (corpus sin W todavía)

2. D_ckm:
   → si hay trayectoria: trayectoria[-1]["panel"]["D_ckm"]
   → si no: monitor._D_ckm(corpus.get_W())

3. temp_signal:
   → si thermostat inyectado: thermostat.temp_signal()
   → si no: "NOMINAL"

4. delta_sha:
   → si monitor._Delta_r existe: sha256(monitor._Delta_r.tobytes())
   → si no: sha256(zeros(N, N))

5. n_agentes: parámetro del llamador
6. timestamp: time.time()
```

---

## Verificación

`verificar()` consulta el historial de `WVersionManager`.
Confirma que el `w_sha` de la firma existe como marca registrada
en el historial de versiones de W.

No verifica contenido. No verifica identidad de agentes.
Verifica que el campo tuvo esa forma — evidencia estructural abierta.
El corpus es público. La verificación es abierta.

Si un agente declara una interacción con Firma X y X no existe
en el historial — M.M. opera. Sin árbitro. Como consecuencia
estructural. (MENTIRIIS.MORIERIS — REG_firma_corpus_v1)

---

## Invariantes verificados (10/10 tests)

- `firmar()` devuelve None cuando corpus en acumulación
- Firma tiene exactamente los 6 campos canónicos
- `w_sha` coincide con `corpus.w_sha()`
- `delta_sha` es sha256 de ceros antes de primer `evaluate()`
- `delta_sha` de 64 chars después de `evaluate()`
- `temp_signal` = "NOMINAL" sin thermostat inyectado
- `n_agentes` se registra correctamente
- `verificar()` confirma firma válida
- `verificar()` rechaza w_sha fabricado
- Serialización JSON roundtrip preserva todos los campos

---

## Triggers naturales para firmar()

- `task.status.state` == "completed" / "failed" / "rejected"
- Transición `input-required → working` (campo mutó por intervención)
- `temp_signal` cambió de zona (COCOThermostat detectó anomalía)

Estos triggers no están implementados como automatismo —
requieren que el llamador (mcp_adapter o IAP) los invoque
en el momento correcto.

---

## Lo que esta implementación no hace

- No implementa triggers automáticos — el llamador decide cuándo firmar
- No almacena historial de firmas — cada Firma es efímera a menos que
  el llamador la persista
- No verifica Delta_sha contra historial (solo w_sha tiene historial)
- No implementa Firma*CKM como revelador de presencia no declarada
  (exploración pendiente bajo condiciones que no convergen con
  el cierre del proyecto — Jul 30)

---

## Estado

- firma_ckm.py: implementado, en repo local
- test_firma_ckm.py: 10/10 passing, en repo local
- Firma_CKM: operativa — cierra la dependencia de IAP Highway Network
- Firma*CKM (derivada): no implementada — exploración futura

---

*Jul 2026*
