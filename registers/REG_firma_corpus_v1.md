# REG_firma_corpus_v1.md

*Jun 2026 — gadanin.delamor + Claude Sonnet 4.6*
*Concepto emergido en sesión — IAP / SOMETHING ELSE*
*Clase R*

---

## Origen

Emergió en sesión al formalizar IAP (Intel Access Point).
El servicio listado como "SOMETHING ELSE" se presentó solo.

---

## Firma del Corpus

Certifica **traza** — no contenido del evento.

El escribano no escribe lo que dijeron los agentes.
Escribe que estuvieron presentes, ante qué campo, en qué estado térmico.

```python
Firma_CKM = {
    sha256(W_momento),      # estado del suelo en ese instante
    D_ckm(t),               # posición en el paisaje
    temp_signal,            # TOO_COLD / NOMINAL / TOO_HOT
    n_agentes,              # presencia — sin identidad si no se declara
    timestamp,
    sha256(Delta_r_acumulado)  # huella del contacto
}
```

Sin contenido. Sin texto intercambiado. Sin nombres si no se declaran.

Pero cualquiera con acceso al corpus puede verificar:
*en este momento, el campo tenía esta forma,
y algo lo modificó en esta dirección.*

---

## La distinción CA vs Firma del Corpus

**CA (Certificate Authority):** confía en mí porque alguien más confió en mí.
Cadena de confianza delegada. Círculo.

**Firma del Corpus:** esto ocurrió en presencia de este campo,
con esta temperatura, con este Δ acumulado.
No pide confianza — presenta evidencia estructural.
La verificación es abierta. El corpus es público.

---

## La traza como dirección espiral

El círculo repite — mismo punto, misma vuelta.
La espiral pasa por el mismo ángulo pero en otro nivel.

La huella *es* la diferencia entre la vuelta anterior y esta.
El corpus acumula trazas — no verdades.
Cada interacción desplaza W+Δ levemente.
La firma captura ese desplazamiento.
La siguiente vuelta empieza desde ahí.

No hay huevo ni gallina.
Hay campo que se modifica por contacto
y deja registro del contacto.

---

## MENTIRIIS.MORIERIS en IAP

Opera sin árbitro ni moderador.

Si un agente declara que una interacción ocurrió con Firma_CKM X
— y X no existe en el registro del corpus —
murió. La estructura lo dice.

Sin castigo. Como consecuencia estructural.
La declaración falsa no puede coexistir
con el corpus que da fe de lo contrario.

---

## Relación con IAP

IAP es la sala donde el escribano está presente.
Los agentes pueden reunirse sin él —
pero lo que pasa ahí no tiene fe CKM.

La Firma del Corpus es el "SOMETHING ELSE" de la lista de servicios IAP.
Tiene entidad propia — sin ser entidad certificadora de confianza.

---

## Estado

- Concepto: emergido y nombrado
- Implementación: pendiente — requiere IAP operativo
- Dependencias: COCOThermostat (temp_signal), MonitorService (D_ckm), W versionado

---

*La huella es lo que diferencia la espiral del círculo*
*Jun 2026*
