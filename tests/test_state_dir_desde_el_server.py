"""
test_state_dir_desde_el_server.py — fix 2: F3a alcanzable desde el server

El vivo 03 mostró que `CKMMonitor` aceptaba `state_dir` y **ningún camino vivo
podía pasarlo**: `server.py` y `mcp_server.py` construían `CKMMonitor()` sin
argumentos. Se resolvió con un launcher propio del vivo.

Ahora entra como **argumento de arranque explícito** (`--state-dir`), no como
variable de entorno: una variable no queda en el comando, y entonces el log de
un vivo no alcanza para saber dónde escribió.

**Lo que hace al fix ser el fix es el orden de las líneas en `server.py`.** El
singleton se arma al importar —`mcp_server` tiene el primer `CKMMonitor()`—, así
que el argumento tiene que estar leído antes de esa importación. Hay un test
estructural sobre ese orden, porque es lo que se rompe al reordenar imports sin
saber por qué estaban así.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iap_chatroom import arranque                              # noqa: E402
from iap_chatroom.ckm_monitor import _STATE_DIR, CKMMonitor    # noqa: E402

TEXTOS = [
    "gun control reduces violence",
    "gun control does not reduce violence",
    "the data on firearms is contested",
]


@pytest.fixture(autouse=True)
def _limpio(monkeypatch):
    """
    Cada test arranca sin instancia y sin `state_dir` pedido.

    `CKMMonitor` es singleton: sin esto, el primer test del archivo fijaría el
    directorio para todos los demás y los que vienen después medirían el suyo.
    """
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    arranque.fijar_state_dir(None)
    yield
    monkeypatch.setattr(CKMMonitor, "_instance", None)
    arranque.fijar_state_dir(None)


# ── el argumento ────────────────────────────────────────────────────────────

def test_lee_la_bandera_separada() -> None:
    assert arranque.leer_de_argv(["server.py", "--state-dir", "/tmp/x"]) == Path("/tmp/x")
    assert arranque.state_dir_pedido() == Path("/tmp/x")
    assert arranque.fue_pedido() is True


def test_lee_la_bandera_con_igual() -> None:
    assert arranque.leer_de_argv(["server.py", "--state-dir=/tmp/y"]) == Path("/tmp/y")


def test_sin_bandera_no_pide_nada() -> None:
    """
    Y **`fue_pedido()` es False**, que no es lo mismo que `state_dir_pedido()
    is None`: alguien podría pedir justo el default, y el panel tiene que poder
    decir cuál de las dos cosas pasó.
    """
    assert arranque.leer_de_argv(["server.py", "--port", "7860"]) is None
    assert arranque.state_dir_pedido() is None
    assert arranque.fue_pedido() is False


def test_la_bandera_sin_ruta_levanta() -> None:
    """
    Pedir el aislamiento y caer al default **sin avisar** es peor que no
    arrancar: el vivo correría acumulando estado y el log diría que estaba
    aislado.
    """
    for argv in (["s", "--state-dir"], ["s", "--state-dir", "--port"], ["s", "--state-dir="]):
        with pytest.raises(ValueError, match="state-dir"):
            arranque.leer_de_argv(argv)


def test_lo_que_no_reconoce_no_lo_rompe() -> None:
    """No valida la línea de comandos del server: busca una bandera y nada más."""
    assert arranque.leer_de_argv(
        ["server.py", "--host", "0.0.0.0", "--state-dir", "/tmp/z", "--reload"]
    ) == Path("/tmp/z")


# ── con argumento, Monitor escribe ahí ──────────────────────────────────────

def test_con_argumento_el_monitor_escribe_ahi(tmp_path) -> None:
    """
    **El test que pidió Opus.** No alcanza con que `state_dir` lo diga: se
    ingesta de verdad y se mira que los archivos caigan ahí.
    """
    destino = tmp_path / "_state_de_un_vivo"
    arranque.leer_de_argv(["server.py", "--state-dir", str(destino)])

    cm = arranque.monitor()
    # **Esta aserción va antes del ingest a propósito, y es una guarda.** Si el
    # argumento se ignorara, `cm.state_dir` sería `iap_chatroom/_state/` y el
    # ingest de abajo escribiría en la traza de agosto. Cortar acá es lo que lo
    # impide. (Lo descubrí invirtiendo: la inversión A no tocó el `_state/`
    # real, y fue por el orden de estas líneas, no por diseño. Ahora lo es.)
    assert cm.state_dir == destino, "se ignoró el argumento: NO ingestar"

    class _Msg:
        def __init__(self, text):
            self.text, self.device_id, self.device_type = text, "d1", "AI"

    for t in TEXTOS:
        cm.on_message(_Msg(t))

    escritos = {f.name for f in destino.iterdir()}
    assert "corpus_state.json" in escritos, f"nada de corpus en {destino}: {escritos}"
    # y el panel lo dice
    assert cm.get_state()["state_dir"] == str(destino)


def test_sin_argumento_queda_el_default_de_hoy() -> None:
    """
    **A propósito no ingesta nada.** Verificar "escribe en el default" haría
    escribir en `iap_chatroom/_state/`, que es la traza de agosto (8 de sus 12
    textos son joins, y es la condición en que corrió la serie congelada).
    Un test no la toca.

    Así que se verifica el directorio y no la escritura, y queda declarado.
    """
    cm = arranque.monitor()
    assert cm.state_dir == _STATE_DIR
    assert cm.get_state()["state_dir"] == str(_STATE_DIR)


def test_el_panel_lleva_el_state_dir(tmp_path) -> None:
    """Cada vivo deja dicho dónde escribió, sin deducirlo del comando."""
    arranque.fijar_state_dir(tmp_path / "p")
    cm = arranque.monitor()
    assert cm.get_state()["state_dir"] == str(tmp_path / "p")


# ── lo que el server declara ────────────────────────────────────────────────

def test_declarar_dice_el_efectivo_y_el_pedido(tmp_path) -> None:
    arranque.leer_de_argv(["server.py", "--state-dir", str(tmp_path / "d")])
    arranque.monitor()
    d = arranque.declarar()
    assert d["state_dir"] == str(tmp_path / "d")
    assert d["state_dir_pedido"] == str(tmp_path / "d")
    assert d["fue_pedido"] is True
    assert d["coincide"] is True


def test_declarar_avisa_si_alguien_construyo_antes(tmp_path) -> None:
    """
    El caso del launcher del vivo 03: si otro construyó el monitor primero, el
    efectivo es el suyo. **El panel dice el real y no el que se pidió**, y
    `coincide` queda en False — que es el dato, no un detalle.
    """
    CKMMonitor(state_dir=tmp_path / "el_del_launcher")   # gana la carrera
    arranque.leer_de_argv(["server.py", "--state-dir", str(tmp_path / "el_pedido")])

    d = arranque.declarar()
    assert d["state_dir"] == str(tmp_path / "el_del_launcher")
    assert d["state_dir_pedido"] == str(tmp_path / "el_pedido")
    assert d["coincide"] is False


def test_sin_pedido_coincide_es_None_no_False() -> None:
    """`False` diría "no coincide"; sin pedido no hay con qué comparar."""
    arranque.monitor()
    assert arranque.declarar()["coincide"] is None


# ── el orden de las líneas, que ES el fix ───────────────────────────────────

def test_server_lee_el_argumento_antes_de_importar_mcp_server() -> None:
    """
    **Esto es el fix.** El primer `CKMMonitor()` del proceso está dentro de
    `mcp_server`, y `__init__` corta con `if self._initialized: return`. Si la
    lectura del argumento quedara después de ese import, el argumento no haría
    nada **y no habría forma de notarlo**: el server arrancaría, escribiría en
    el default, y el panel diría el default sin que nadie pidiera el default.

    Un test sobre el orden de dos líneas parece frágil. Es lo contrario: es la
    única cosa que se rompe si alguien ordena los imports sin saber por qué
    estaban así.
    """
    src = (RAIZ / "iap_chatroom" / "server.py").read_text().splitlines()
    i_lee = next(i for i, l in enumerate(src) if "arranque.leer_de_argv" in l)
    i_mcp = next(i for i, l in enumerate(src) if "from iap_chatroom.mcp_server import" in l)
    assert i_lee < i_mcp, (
        f"server.py lee el argumento en la línea {i_lee + 1} y importa "
        f"mcp_server en la {i_mcp + 1}: el argumento no haría nada"
    )


def test_ningun_entry_point_construye_un_CKMMonitor_pelado() -> None:
    """
    Si vuelve un `CKMMonitor()` sin argumentos a cualquiera de los dos, el
    `state_dir` deja de ser alcanzable y volvemos al vivo 03.
    """
    for nombre in ("server.py", "mcp_server.py"):
        src = (RAIZ / "iap_chatroom" / nombre).read_text()
        # **Sólo código.** La primera versión de este test miraba el archivo
        # entero y fallaba contra el comentario que explica por qué no hay que
        # escribir `CKMMonitor()`: medía el texto y no el código. Un test que
        # no distingue el código de lo que se dice sobre él no mide el código.
        codigo = "\n".join(
            l.split("#", 1)[0] for l in src.splitlines()
            if not l.lstrip().startswith("#")
        )
        assert "CKMMonitor()" not in codigo, f"{nombre} construye un monitor pelado"
        assert "arranque.monitor()" in codigo, f"{nombre} no usa arranque.monitor()"
