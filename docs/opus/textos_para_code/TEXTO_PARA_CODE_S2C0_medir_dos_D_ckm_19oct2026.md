DELAMOR A CODE (texto de Opus):

delamor: *"veamos qué miden, en vez de decidir qué miden"*. **Se mide, no se interpreta.** El texto va **sin nombres** de lo que significa cada serie.

**Precondición:** el paso (2) de `TEXTO_PARA_CODE_S2C0_delta_r_crudo_19oct2026` (Δ_r crudo en Monitor) cerrado en verde. Si no cerró, esto espera.

**Qué se mide**
- Una corrida **local**, sin tocar el vivo, con el canal real y Monitor y COCO conectados como en el CP1.
- Los mismos mensajes del CP1: los 8 `TEXTOS` en ciclo, dos devices.
- Que la corrida pase por **al menos dos rebuilds**.
- Donde haya rechazos, que sean los que produce el camino real, no una secuencia inventada.
- Estado en un directorio propio, aparte del de S2-C0.

**Qué se registra, mensaje por mensaje**
- El tick y el sha de W.
- Monitor: D_ckm, N_eff, N_eff₀, ‖Δ_r‖ y max Δ_r.
- COCO: D_ckm, N_eff, A0, ‖Δ_r_compresiones‖, zona y disparos.
- Rebuilds y calibraciones, con su momento.

**Restricción.** El canal **no publica** lo de COCO: es información sensible, por decisión de delamor. Lo de COCO va **sólo** al JSONL o al archivo de la corrida, nunca al panel del canal.

**Qué se entrega**
- La tabla o el JSONL alineado por mensaje, con el sha.
- Lo que se puede afirmar y lo que no.
- **Sin lectura de qué mide cada serie.**
- El driver queda en `experiments/`.

Al terminar: commits, estado de los tests y avisá para el push.
