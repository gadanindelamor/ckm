#!/usr/bin/env bash
# keepalive — actividad periodica liviana mientras el codespace esta ocioso.
#
# No hay garantia de que prevenga el idle timeout: depende de que criterio use
# GitHub (conexion de usuario vs actividad de proceso), y eso no se puede
# determinar desde adentro. Se corre y se observa: el log es la traza.
#
# El control confiable del timeout NO esta en el repo, esta en la cuenta:
#   github.com/settings/codespaces  ->  Default idle timeout  (max 240 min)
#
# Uso:
#   tools/keepalive.sh start    arranca en background si no hay otro corriendo
#   tools/keepalive.sh stop     detiene el que este corriendo
#   tools/keepalive.sh status   dice si corre, desde cuando, y las ultimas lineas
#   tools/keepalive.sh run      corre en primer plano (lo que start invoca)
#
# Persistencia: 'start' es idempotente (PID file). Se lo engancha al arranque
# de cualquier shell desde ~/.bashrc; ver tools/keepalive.sh install-hook.
#
# El log queda en logs/keepalive.log, ignorado por git (*.log). No es evidencia
# del proyecto: es traza operativa. Si el codespace se corta, el ultimo timestamp
# dice donde.

set -uo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG="${KEEPALIVE_LOG:-$RAIZ/logs/keepalive.log}"
PIDF="${KEEPALIVE_PID:-$RAIZ/logs/keepalive.pid}"
INTERVALO="${KEEPALIVE_INTERVAL:-60}"
HOOK_MARCA="# ckm-keepalive"

mkdir -p "$(dirname "$LOG")"

_corriendo() {
    [[ -f "$PIDF" ]] || return 1
    local pid; pid="$(cat "$PIDF" 2>/dev/null)"
    [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

cmd_run() {
    printf '%s INICIO pid=%s intervalo=%ss\n' \
        "$(date -u +%FT%TZ)" "$$" "$INTERVALO" >> "$LOG"
    while true; do
        printf '%s up=%s load=%s\n' \
            "$(date -u +%FT%TZ)" \
            "$(cut -d' ' -f1 /proc/uptime)" \
            "$(cut -d' ' -f1 /proc/loadavg)" >> "$LOG"
        touch "$LOG"
        : $(( $(date +%s) % 7 ))
        sleep "$INTERVALO"
    done
}

cmd_start() {
    if _corriendo; then
        echo "keepalive ya corre (pid $(cat "$PIDF"))"
        return 0
    fi
    setsid nohup "${BASH_SOURCE[0]}" run >/dev/null 2>&1 &
    echo $! > "$PIDF"
    sleep 0.3
    if _corriendo; then
        echo "keepalive arrancado (pid $(cat "$PIDF"))  log=$LOG"
    else
        echo "keepalive no arranco"; rm -f "$PIDF"; return 1
    fi
}

cmd_stop() {
    if _corriendo; then
        local pid; pid="$(cat "$PIDF")"
        kill "$pid" 2>/dev/null
        printf '%s STOP pid=%s\n' "$(date -u +%FT%TZ)" "$pid" >> "$LOG"
        rm -f "$PIDF"
        echo "keepalive detenido (pid $pid)"
    else
        rm -f "$PIDF"
        echo "keepalive no estaba corriendo"
    fi
}

cmd_status() {
    if _corriendo; then
        echo "keepalive CORRE  pid=$(cat "$PIDF")"
    else
        echo "keepalive DETENIDO"
    fi
    echo "log=$LOG"
    [[ -f "$LOG" ]] && { echo "--- ultimas lineas ---"; tail -5 "$LOG"; }
}

cmd_install_hook() {
    local rc="$HOME/.bashrc"
    if grep -qF "$HOOK_MARCA" "$rc" 2>/dev/null; then
        echo "hook ya presente en $rc"
        return 0
    fi
    {
        echo ""
        echo "$HOOK_MARCA — arranca el keepalive si no corre (idempotente)"
        echo "[ -x \"$RAIZ/tools/keepalive.sh\" ] && \"$RAIZ/tools/keepalive.sh\" start >/dev/null 2>&1"
    } >> "$rc"
    echo "hook agregado a $rc"
}

case "${1:-status}" in
    run)          cmd_run ;;
    start)        cmd_start ;;
    stop)         cmd_stop ;;
    status)       cmd_status ;;
    install-hook) cmd_install_hook ;;
    *) echo "uso: $0 {start|stop|status|run|install-hook}"; exit 2 ;;
esac
