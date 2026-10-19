"""
driver_medir_dos_d_ckm.py — las dos series de D_ckm, mensaje por mensaje

delamor, 19 oct: *"veamos qué miden, en vez de decidir qué miden"*. **Esto
mide. No interpreta.** El driver no nombra qué significa ninguna de las dos
series ni compara una contra la otra: registra las dos, alineadas por mensaje,
y escribe el JSONL.

**Qué corre:** el canal real (`ChatChannel`) con `CKMMonitor` registrado como
callback —Monitor y COCO conectados como en el CP1—, en un `state_dir`
**propio**, aparte del de S2-C0. Los mensajes los escribe el driver: no hay
devices de IA ni providers.

**Los rechazos son los del camino real:** salen de `MonitorService.evaluate`
(σ_prompt contra σ_relajado) en cada mensaje. No hay secuencia inventada.

**Restricción de delamor:** lo de COCO **no va al panel del canal**. Acá va
sólo al JSONL de la corrida.

**Privados que el driver lee, declarado:** `monitor._Delta_r` (la matriz, para
la norma y el máximo) y `thermostat.history()[-1]` / `delta_state()` /
`alpha_trajectory()`. Son lectura; no se escribe nada y `services/` no se toca.

Correr:
    PYTHONPATH=/workspaces/ckm python3 experiments/driver_medir_dos_d_ckm.py [salida.jsonl]
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

from iap_chatroom.channel import ChatChannel          # noqa: E402
from iap_chatroom.ckm_monitor import CKMMonitor        # noqa: E402

# Los mismos mensajes del CP1.
TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
    "gun rights are constitutional rights and should not be restricted",
    "mental health is the real cause of gun violence not access to arms",
    "urban areas report more gun violence than rural areas",
    "constitutional rights include the right to bear arms in the home",
]
# 70 mensajes: el primer W a los 30 y el volumen cada 10, así la corrida pasa
# por al menos dos rebuilds despues del primero.
N_MENSAJES = 70
ESTADO = RAIZ / "experiments" / "_state_medir_dos_dckm"


def secuencia():
    return [("d1" if i % 2 else "d2", TEXTOS[i % len(TEXTOS)])
            for i in range(N_MENSAJES)]


def norma(M):
    return None if M is None else round(float(np.linalg.norm(M)), 6)


def maximo(M):
    return None if M is None else round(float(np.max(M)), 6)


async def correr(salida: Path) -> dict:
    # Canal y Monitor nuevos, en su propio directorio.
    ChatChannel._instance = None
    CKMMonitor._instance = None
    canal = ChatChannel()
    cm = CKMMonitor(state_dir=ESTADO)
    canal.add_callback(cm.on_message)

    seq = secuencia()
    sha_seq = hashlib.sha256(
        json.dumps(seq, ensure_ascii=False).encode("utf-8")).hexdigest()

    filas = []
    n_rebuilds = 0
    with open(salida, "w") as f:
        for n, (device_id, texto) in enumerate(seq, start=1):
            canal.register = None   # no hace falta registro para publicar
            sha_antes = cm._corpus.w_sha()
            await canal.publish(device_id, "AI", texto)
            panel = cm._last_panel
            estado = cm.get_state()
            th = cm._monitor.thermostat
            ts = th.history()[-1] if (th is not None and th.history()) else None
            sha_despues = cm._corpus.w_sha()
            hubo_rebuild = (sha_antes != sha_despues)
            if hubo_rebuild:
                n_rebuilds += 1

            punto = estado.get("punto_calibrate")
            fila = {
                "n": n,
                "device_id": device_id,
                "tick": estado.get("tick"),
                "w_sha": sha_despues,
                "corpus_size": estado.get("corpus_size"),
                "n_nodes": estado.get("n_nodes"),
                # ── serie 1 ──────────────────────────────────────────────
                "monitor": {
                    "D_ckm": (panel or {}).get("D_ckm"),
                    "N_eff": (panel or {}).get("N_eff"),
                    "N_eff_0": (panel or {}).get("N_eff0"),
                    "norma_Delta_r": norma(cm._monitor._Delta_r),
                    "max_Delta_r": maximo(cm._monitor._Delta_r),
                    "n_rejected_pairs": (panel or {}).get("n_rejected_pairs"),
                } if panel else None,
                # ── serie 2 ──────────────────────────────────────────────
                # Sólo al JSONL. No va al panel del canal (restricción de
                # delamor).
                "coco": {
                    "D_ckm": ts.D_ckm if ts else None,
                    "N_eff": ts.A_current if ts else None,
                    "A0": ts.A0 if ts else None,
                    "frac_rec": ts.frac_rec if ts else None,
                    "zona": ts.zone if ts else None,
                    "stop_applied": ts.stop_applied if ts else None,
                    "alpha_used": ts.alpha_used if ts else None,
                    "norma_Delta_r_compresiones": (
                        norma(th.delta_state()) if th is not None else None),
                    "disparos_acumulados": (
                        len(th.alpha_trajectory()) if th is not None else None),
                    "generacion": (panel or {}).get("coco_generacion"),
                } if th is not None else None,
                # ── eventos del ciclo ───────────────────────────────────
                "rebuild": {
                    "ocurrio": hubo_rebuild,
                    "causa": estado.get("rebuild_causa"),
                    "w_sha_antes": sha_antes,
                } if hubo_rebuild else None,
                # La calibración va en **cada** mensaje, no sólo en los de
                # rebuild: el panel la lleva vigente, y así se ve en qué
                # momento cambió y con qué motivo.
                "calibracion": {
                    "state": punto.get("state"),
                    "reason": punto.get("reason"),
                    "values": punto.get("values"),
                    "w_sha": punto.get("w_sha"),
                    "w_sha_live_at_calibration": punto.get(
                        "w_sha_live_at_calibration"),
                    "duration_s": punto.get("duration_s"),
                    "moment": punto.get("moment"),
                } if punto else None,
            }
            f.write(json.dumps(fila, ensure_ascii=False, default=str) + "\n")
            filas.append(fila)

    return {"sha_mensajes": sha_seq, "n_mensajes": len(seq),
            "n_rebuilds": n_rebuilds, "filas": filas,
            "state_dir": str(ESTADO)}


def main() -> None:
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        RAIZ / "experiments/medir_dos_d_ckm.jsonl")
    if ESTADO.exists():
        # Estado propio y limpio: la corrida arranca de cero, declarado.
        for p in sorted(ESTADO.glob("*")):
            p.unlink()
    r = asyncio.run(correr(salida))
    print(f"[dos_dckm] {salida}")
    print(f"[dos_dckm] mensajes={r['n_mensajes']} "
          f"sha={r['sha_mensajes'][:12]} rebuilds={r['n_rebuilds']} "
          f"state_dir={r['state_dir']}")
    print(f"{'n':>3} {'tick':>4} {'w_sha':>8} "
          f"{'M.D_ckm':>9} {'M.N_eff':>8} {'M.N0':>7} {'||Dr||':>8} {'maxDr':>6} "
          f"{'C.D_ckm':>9} {'C.N_eff':>8} {'C.A0':>7} {'||Dc||':>8} "
          f"{'zona':>10} {'disp':>4} {'reb':>4}")
    for fila in r["filas"]:
        if fila["monitor"] is None:
            continue
        m, c = fila["monitor"], fila["coco"] or {}
        def fmt(x, w=9, p=4):
            return f"{x:{w}.{p}f}" if isinstance(x, (int, float)) else f"{'-':>{w}}"
        print(f"{fila['n']:>3} {str(fila['tick']):>4} {(fila['w_sha'] or '-')[:8]:>8} "
              f"{fmt(m['D_ckm'])} {fmt(m['N_eff'],8,3)} {fmt(m['N_eff_0'],7,2)} "
              f"{fmt(m['norma_Delta_r'],8,2)} {fmt(m['max_Delta_r'],6,1)} "
              f"{fmt(c.get('D_ckm'))} {fmt(c.get('N_eff'),8,3)} "
              f"{fmt(c.get('A0'),7,2)} {fmt(c.get('norma_Delta_r_compresiones'),8,2)} "
              f"{str(c.get('zona')):>10} {str(c.get('disparos_acumulados')):>4} "
              f"{'SI' if fila['rebuild'] else '':>4}")


if __name__ == "__main__":
    main()
