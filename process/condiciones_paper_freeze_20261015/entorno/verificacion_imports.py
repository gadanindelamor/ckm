"""Replica las DOS lineas de sys.path de los drivers y reporta de donde sale cada modulo.
No edita nada: el freeze se pasa por argumento."""
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))

import services.node_extractor, services.corpus_service, services.landscape_engine
import node_extractor, w_version
import numpy, sklearn

print("cwd                        :", Path.cwd())
print("RAIZ                       :", RAIZ)
for m in (services.node_extractor, services.corpus_service, services.landscape_engine,
          node_extractor, w_version):
    f = Path(m.__file__).resolve()
    dentro = "DENTRO del freeze" if str(f).startswith(str(RAIZ)) else "*** FUERA ***"
    print(f"{m.__name__:<28}: {f}   -> {dentro}")
print("numpy                      :", numpy.__version__, Path(numpy.__file__).parent)
print("sklearn                    :", sklearn.__version__)
print("services.node_extractor is node_extractor ?", services.node_extractor is node_extractor)
