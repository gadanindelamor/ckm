"""
test_extraccion_fallida_no_borra.py — divergencia (a) del CP0

Una extracción que falla **no puede borrar la declaración de la W que sigue
viva**. Es la divergencia (a) del CP0 de `TASK_declaracion_extraccion_v1`
(BANDEJA, 14 oct), que delamor decidió corregir el mismo día
(`DECISIONES_opus.md`).

Lo que pasaba: `_accumulate_safe` absorbe el `ValueError` de
`TfidfVectorizer` devolviendo un dict **sin** la clave `"perfil"`, y
`_rebuild` asignaba `_perfil_extraccion` y `_registro_borde` **antes** del
`return` por `nodes` vacío. Resultado: la W anterior quedaba viva y su perfil
en `None`.

Y `None` ahí no es inocuo: el `None` que escribe `_load` quiere decir *"no se
sabe bajo qué condición se extrajo"* —un estado anterior a S0b— y es cierto.
**Éste decía lo mismo y era falso.** Es I2 al revés: no se completa de más, se
borra de menos.

La regla que el test fija: **el perfil y el `registro_borde` describen la W que
está viva.** Se actualizan cuando se actualiza W, y no antes.

El test fuerza la falla con `monkeypatch` sobre `accumulate`, no con un corpus
degenerado: con textos buenos ya acumulados `TfidfVectorizer` no levanta, así
que por ahí no se llega. Lo que se afirma es el **contrato** de
`_accumulate_safe` —si la extracción falla, lo vivo no se toca—, no una causa
particular de falla.

**El parche va sobre la instancia, no sobre la clase, y no es un detalle de
estilo.** `services/` se importa plano entre sus módulos
(`corpus_service.py:47`: `from node_extractor import ...`), así que
`node_extractor.NodeExtractorService` y `services.node_extractor.NodeExtractorService`
son **dos clases distintas**: parchear la que ve el test deja intacta la que usa
el servicio, y el test pasa sin haber medido nada. Verificado al escribirlo
(BANDEJA, 14 oct).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "services"))
from services.corpus_service import CorpusService          # noqa: E402
# NO se importa NodeExtractorService: el parche va sobre la instancia (ver arriba)


TEXTOS = [
    "gun control reduces violence and saves lives in urban areas",
    "the second amendment protects the right to bear arms",
    "background checks do not stop criminals from getting weapons",
    "assault weapons bans reduce mass shootings and gun violence",
    "gun rights are constitutional rights that should not be restricted",
]


@pytest.fixture
def corpus_vivo(tmp_path):
    """Un CorpusService con W, nodos, perfil y registro_borde ya construidos."""
    c = CorpusService(storage_path=str(tmp_path / "c.json"), min_texts=3, top_k=8)
    c.ingest(TEXTOS)
    assert c.get_W() is not None, "el fixture no construyó W: el test no mide nada"
    assert c._perfil_extraccion is not None
    assert c._registro_borde
    return c


def _romper_extraccion(monkeypatch, corpus):
    def explota(texts, seleccion_anterior=None):
        raise ValueError("Empty vocabulary; perhaps the documents only contain stop words")
    # sobre la INSTANCIA: ver el docstring del módulo
    monkeypatch.setattr(corpus._extractor, "accumulate", explota)


def test_extraccion_fallida_no_borra_lo_vivo(corpus_vivo, monkeypatch):
    """Los cuatro —W, nodos, perfil y registro_borde— quedan como estaban."""
    W_antes        = corpus_vivo.get_W().copy()
    nodes_antes    = list(corpus_vivo.get_nodes())
    perfil_antes   = dict(corpus_vivo._perfil_extraccion)
    registro_antes = list(corpus_vivo._registro_borde)
    sha_antes      = corpus_vivo.w_sha()

    _romper_extraccion(monkeypatch, corpus_vivo)
    corpus_vivo.ingest(["ok"])

    np.testing.assert_array_equal(corpus_vivo.get_W(), W_antes)
    assert corpus_vivo.get_nodes()        == nodes_antes
    assert corpus_vivo._perfil_extraccion == perfil_antes
    assert corpus_vivo._registro_borde    == registro_antes
    # la W no cambió, así que tampoco hay marca nueva
    assert corpus_vivo.w_sha() == sha_antes


def test_el_estado_guardado_no_queda_sin_declaracion(corpus_vivo, monkeypatch):
    """
    La huella en disco, que es la que sobrevive al proceso: un estado con una W
    no nula **no** puede declarar `perfil_extraccion: null`.
    """
    _romper_extraccion(monkeypatch, corpus_vivo)
    corpus_vivo.ingest(["ok"])

    estado = json.loads(Path(corpus_vivo.storage_path).read_text())
    assert estado["W"] is not None
    assert estado["perfil_extraccion"] is not None, (
        "W viva con `perfil_extraccion: null`: el estado declara que no se sabe "
        "bajo qué condición se extrajo, y sí se sabe"
    )
    assert estado["registro_borde"]


def test_el_texto_igual_se_acumula(corpus_vivo, monkeypatch):
    """
    Lo que la corrección **no** cambia: el texto entra al corpus aunque la
    extracción falle. Sólo se preserva la declaración de la W vieja.
    """
    n_antes = len(corpus_vivo._texts)
    _romper_extraccion(monkeypatch, corpus_vivo)
    corpus_vivo.ingest(["ok"])
    assert len(corpus_vivo._texts) == n_antes + 1
