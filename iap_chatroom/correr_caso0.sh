#!/usr/bin/env bash
#
# correr_caso0.sh — dispara serie2_caso0 (S2-C0) con todo lo que hay que saber
#                   adentro, para no tener que recordarlo.
#
# USO
#   ./iap_chatroom/correr_caso0.sh --check     verifica TODO y no corre el vivo
#   ./iap_chatroom/correr_caso0.sh            el vivo completo (~20 min)
#   ./iap_chatroom/correr_caso0.sh --no-reset  sin preservar el estado anterior
#   ./iap_chatroom/correr_caso0.sh --modo CONTINUA   acumula, declarado en el log
#
#   Lo que no reconoce se le pasa tal cual al caso.
#
# QUÉ HACE, EN ORDEN, Y POR QUÉ CADA PASO
#
#   0. Que no haya otro server en el 7860. Uno viejo tiene el corpus del intento
#      anterior EN MEMORIA, y entonces el ZERO_SHOT aborta — o peor, si alguien
#      lo arrancó con otro state_dir, el caso escribiría en otro lado.
#   1. --reset: preserva el estado anterior en process/ con timestamp. NO BORRA.
#   2. Arranca el server con el state_dir del caso y espera a que responda.
#      El reset mueve archivos pero NO vacía el corpus en memoria: por eso el
#      server se reinicia siempre (documentado desde el Caso 0.4a).
#   3. Verifica por MCP corpus_size == 0 y canal == 0. Si no da 0, para acá.
#      Es la única verificación que atraviesa los dos procesos.
#   4. --preflight: los cuatro modelos. Si uno no responde, para acá.
#   5. El caso, ZERO_SHOT, con log propio por fecha (no pisa los anteriores).
#   6. Apaga el server, siempre, incluso si algo falla o si cortás con Ctrl-C.
#
# LO QUE HAY QUE TENER EN CUENTA
#
#   · DURA ~20 MINUTOS (DURATION = 1200 s) más el cierre. No hay forma de
#     acortarlo sin tocar el caso: DURATION es un número declarado y hay tests
#     que lo afirman. Si querés corridas cortas, hay que agregarle una bandera
#     al caso y eso se decide, no se improvisa.
#   · DURANTE EL VIVO, NINGUNA INTERVENCIÓN. Y si tenés la UI abierta, no
#     publiques: un mensaje tuyo entra al corpus como cualquier otro.
#   · GEMINI TIENE 20 REQUESTS POR DÍA, POR MODELO (medido el 22 oct:
#     quotaId GenerateRequestsPerDayPerProjectPerModel-FreeTier, quotaValue 20,
#     retryDelay 3339s). device B usa gemini-3.5-flash-lite, que aguantó 68
#     llamadas sin error. Cada prueba suelta contra un modelo le come cuota al
#     vivo: no midas con la misma key que después necesitás.
#     Si el preflight falla en B con 429, es eso: esperá ~1 h o cambiá el
#     modelo en DEVICES.
#   · Los --check también gastan: son 4 llamadas, una por modelo.
#   · experiments/_state_S2-C0/ NO SE COMMITEA. El log del driver SÍ (~750 K).
#   · El .env vive en iap_chatroom/.env, no en la raíz.
#
# Escrito por Code (Claude Opus 5) el 25 oct 2026, a pedido de delamor, para
# que pueda correr el caso sin depender de los créditos de Code.

set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

STATE_DIR="$ROOT_DIR/experiments/_state_S2-C0"
CASO="iap_chatroom/tests/test_caso_serie2_caso0.py"
MCP_URL="http://localhost:7860/mcp"
SERVER_LOG="$ROOT_DIR/experiments/_server_caso0_$(date -u +%Y%m%dT%H%M%SZ).log"
SALIDA="$ROOT_DIR/experiments/serie2_caso0_$(date -u +%Y%m%dT%H%M%SZ)_log.json"

export PYTHONPATH="$ROOT_DIR"

SOLO_CHECK=0
HACER_RESET=1
EXTRA=()
for arg in "$@"; do
  case "$arg" in
    --check)    SOLO_CHECK=1 ;;
    --no-reset) HACER_RESET=0 ;;
    *)          EXTRA+=("$arg") ;;
  esac
done

SERVER_PID=""
limpiar() {
  if [[ -n "$SERVER_PID" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    echo
    echo "[correr_caso0] apagando el server (pid $SERVER_PID)"
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
}
trap limpiar EXIT INT TERM

echo "=============================================================="
echo " serie2_caso0 (S2-C0)"
echo " state_dir : $STATE_DIR"
echo " log        : $SALIDA"
echo " server log : $SERVER_LOG"
[[ $SOLO_CHECK -eq 1 ]] && echo " MODO --check: verifica y NO corre el vivo"
echo "=============================================================="

# ── 0. que no haya otro server escuchando ─────────────────────────────────
if python3 - <<'PY'
import socket, sys
s = socket.socket()
s.settimeout(1)
sys.exit(0 if s.connect_ex(("127.0.0.1", 7860)) == 0 else 1)
PY
then
  echo
  echo "ALTO: algo ya está escuchando en el 7860."
  echo
  echo "  Un server viejo tiene el corpus del intento anterior EN MEMORIA, así"
  echo "  que el ZERO_SHOT va a abortar. Y si lo arrancaron con otro"
  echo "  --state-dir, el caso escribiría en otro lado sin decirlo."
  echo
  echo "  Bajalo y volvé a correr esto:   pkill -f iap_chatroom/server.py"
  exit 1
fi

# ── 1. preservar el estado anterior ───────────────────────────────────────
if [[ $HACER_RESET -eq 1 ]]; then
  echo
  echo "[1/5] --reset: preservando el estado anterior en process/ (no borra)"
  python3 "$CASO" --reset
else
  echo
  echo "[1/5] --no-reset: el estado anterior QUEDA. Si el corpus no está en 0,"
  echo "      el paso 3 va a parar la corrida (salvo --modo CONTINUA)."
fi

# ── 2. el server ──────────────────────────────────────────────────────────
echo
echo "[2/5] arrancando el server con el state_dir del caso"
python3 iap_chatroom/server.py --state-dir "$STATE_DIR" > "$SERVER_LOG" 2>&1 &
SERVER_PID=$!
echo "      pid $SERVER_PID — log en $SERVER_LOG"

echo "      esperando que responda…"
for i in $(seq 1 40); do
  if python3 - <<'PY' 2>/dev/null
import asyncio, sys
from fastmcp import Client
async def m():
    async with Client("http://localhost:7860/mcp") as c:
        await c.call_tool("get_clock", {})
asyncio.run(m())
PY
  then
    echo "      responde (intento $i)"
    break
  fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo
    echo "ALTO: el server murió al arrancar. Últimas líneas de su log:"
    tail -20 "$SERVER_LOG"
    exit 1
  fi
  sleep 2
  if [[ $i -eq 40 ]]; then
    echo
    echo "ALTO: el server no respondió en 80 s. Su log:"
    tail -20 "$SERVER_LOG"
    exit 1
  fi
done

# ── 3. corpus en 0, por MCP ───────────────────────────────────────────────
echo
echo "[3/5] verificando por MCP que el corpus y el canal estén en 0"
python3 - <<'PY'
import asyncio, sys
from fastmcp import Client

async def m():
    async with Client("http://localhost:7860/mcp") as c:
        ms = (await c.call_tool("get_monitor_state", {})).data
        msgs = (await c.call_tool("get_messages", {"since": None})).data
    corpus, canal = ms["corpus_size"], len(msgs)
    coco = ms.get("coco")
    print(f"      corpus_size = {corpus} | mensajes en el canal = {canal}")
    print(f"      coco = {coco}")
    if corpus != 0 or canal != 0:
        print()
        print("ALTO: el corpus o el canal no están en 0.")
        print()
        print("  Un ZERO_SHOT no corre sobre un estado sucio sin decirlo. Las")
        print("  dos cosas que lo causan:")
        print("   · no se hizo el --reset, o")
        print("   · se hizo el --reset pero NO se reinició el server (el reset")
        print("     mueve archivos; el corpus sigue en memoria).")
        print()
        print("  Este script hace las dos. Si llegaste acá con --no-reset, es")
        print("  lo esperado: o corrés sin esa bandera, o usás --modo CONTINUA,")
        print("  que acumula a propósito y lo declara en el log.")
        sys.exit(1)

asyncio.run(m())
PY

# ── 4. preflight ──────────────────────────────────────────────────────────
echo
echo "[4/5] preflight: los cuatro modelos (4 llamadas, gastan cuota)"
if ! python3 "$CASO" --preflight; then
  echo
  echo "ALTO: el preflight falló. No se toca el canal."
  echo
  echo "  Si el que falla es device B con 429: es la cuota diaria de Gemini,"
  echo "  20 requests por día y por modelo. Esperá ~1 h (retryDelay medido:"
  echo "  3339 s) o cambiá el modelo de B en DEVICES del caso."
  exit 1
fi

# ── 5. el caso ────────────────────────────────────────────────────────────
if [[ $SOLO_CHECK -eq 1 ]]; then
  echo
  echo "[5/5] --check: todo verificado y el vivo NO se corrió."
  echo "      Para correrlo: ./iap_chatroom/correr_caso0.sh"
  exit 0
fi

echo
echo "[5/5] disparando el caso. DURA ~20 MINUTOS (DURATION = 1200 s)."
echo "      Durante el vivo, ninguna intervención. Si tenés la UI abierta,"
echo "      no publiques: tu mensaje entra al corpus como cualquier otro."
echo
python3 "$CASO" "${EXTRA[@]}" "$SALIDA"

echo
echo "=============================================================="
echo " log del driver : $SALIDA"
echo " state_dir      : $STATE_DIR  (NO se commitea)"
echo " el log del driver SÍ se commitea (~750 K)"
echo "=============================================================="
