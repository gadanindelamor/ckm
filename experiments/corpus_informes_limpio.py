"""
corpus_informes_limpio.py — corpus limpio desde los informes de trabajo

Clase T. Extrae el texto de `docs/CKM_Informe_Trabajo*.docx` y produce un
corpus de párrafos, uno por línea, sin repetidos ni restos de formato.

Los informes v1–v24 son acumulativos: cada uno contiene al anterior. Sin
deduplicar, un párrafo pesa hasta 24 veces — la misma saturación por fuente
repetida que frenó la Clase R. Se conserva la PRIMERA aparición.

Reglas de limpieza (declaradas, no inferidas al leer):
  - v27 y v28 son texto plano con extensión .docx; el resto son zip/docx.
  - Se descartan líneas de menos de MIN_CHARS caracteres: en la extracción,
    cada celda de tabla queda como línea suelta ("Estado", "0", "−1").
  - Se descartan filas de tabla (contienen "|"), encabezados numerados
    cortos ("12.2 Protocolo A1-A5 …") y viñetas sueltas.
  - Se quitan marcas markdown (**, *, `, #) y se colapsan los espacios.
  - Se decodifican las entidades XML con html.unescape (&apos; incluido: sin
    eso, cada apostrofe queda como la palabra "apos" y puede volverse nodo).
  - Deduplicación por texto normalizado en minúsculas.

Unidad de texto (CKM define la co-ocurrencia "en el mismo texto", así que la
unidad decide qué significa co-ocurrir):
  - parrafo: un párrafo = un texto.
  - pagina: se agrupan párrafos COMPLETOS hasta llegar a PALABRAS_PAGINA
    palabras (300 por defecto: una carilla a espacio simple). Ningún párrafo
    se corta; uno más largo que la medida queda solo como página.

Uso:
    python experiments/corpus_informes_limpio.py [--salida DIR]
                        [--unidad parrafo|pagina] [--palabras-pagina 300]
"""

import argparse
import glob
import html
import hashlib
import re
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MIN_CHARS = 40
PALABRAS_PAGINA = 300
SALIDA = REPO / "process/corpus_informes"


def _texto(path: Path) -> str:
    """docx (zip) o texto plano con extensión .docx."""
    try:
        x = zipfile.ZipFile(path).read("word/document.xml").decode("utf8")
    except zipfile.BadZipFile:
        return path.read_text(encoding="utf8")
    x = re.sub(r"</w:p>", "\n", x)
    x = re.sub(r"<[^>]+>", "", x)
    return _entidades(x)


def _entidades(x: str) -> str:
    """Decodifica entidades XML. &apos; se pasaba por alto y cada apostrofe
    quedaba como la palabra "apos", que llego a ser nodo del campo."""
    return html.unescape(x)


def _es_prosa(linea: str) -> bool:
    if len(linea) < MIN_CHARS:
        return False
    if "|" in linea:                                   # fila de tabla
        return False
    if re.match(r"^\d+(\.\d+)*[\.\)]?\s+\S", linea) and len(linea) < 80:
        return False                                   # encabezado numerado
    if re.match(r"^[-•*]\s", linea) and len(linea) < 60:
        return False                                   # viñeta suelta
    letras = sum(c.isalpha() for c in linea)
    return letras >= 0.5 * len(linea)                  # no es tabla de números


def limpiar(linea: str) -> str:
    linea = re.sub(r"[*`#]+", "", linea)
    return re.sub(r"\s+", " ", linea).strip()


def construir(informes):
    vistos, parrafos, por_informe = set(), [], {}
    for f in informes:
        n = 0
        for cruda in _texto(f).splitlines():
            linea = limpiar(cruda)
            if not _es_prosa(linea):
                continue
            h = hashlib.sha256(linea.lower().encode()).hexdigest()
            if h in vistos:
                continue
            vistos.add(h)
            parrafos.append(linea)
            n += 1
        por_informe[f.stem] = n
    return parrafos, por_informe


def paginar(parrafos, palabras_pagina=PALABRAS_PAGINA):
    """Agrupa párrafos completos en páginas de ~palabras_pagina palabras."""
    paginas, actual, n = [], [], 0
    for p in parrafos:
        actual.append(p)
        n += len(p.split())
        if n >= palabras_pagina:
            paginas.append(" ".join(actual))
            actual, n = [], 0
    if actual:
        paginas.append(" ".join(actual))
    return paginas


def _orden(p: Path) -> int:
    m = re.search(r"_v(\d+)", p.stem)
    return int(m.group(1)) if m else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=str(SALIDA))
    ap.add_argument("--unidad", choices=("parrafo", "pagina"), default="parrafo")
    ap.add_argument("--palabras-pagina", type=int, default=PALABRAS_PAGINA)
    args = ap.parse_args()

    informes = sorted((Path(p) for p in glob.glob(str(REPO / "docs/CKM_Informe_Trabajo*.docx"))),
                      key=_orden)
    parrafos, por_informe = construir(informes)

    textos = (parrafos if args.unidad == "parrafo"
              else paginar(parrafos, args.palabras_pagina))
    nombre = ("corpus_informes.txt" if args.unidad == "parrafo"
              else f"corpus_informes_paginas{args.palabras_pagina}.txt")

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    (salida / nombre).write_text("\n".join(textos) + "\n", encoding="utf8")

    palabras = sum(len(p.split()) for p in parrafos)
    lineas = [f"# corpus_informes — párrafos únicos de los informes de trabajo", "",
              f"- informes: {len(informes)} ({informes[0].stem} … {informes[-1].stem})",
              f"- párrafos: {len(parrafos)} · palabras: {palabras}",
              f"- unidad de este archivo: {args.unidad}"
              + (f" ({args.palabras_pagina} palabras, párrafos sin cortar) → {len(textos)} páginas"
                 if args.unidad == "pagina" else f" → {len(textos)} textos"),
              f"- min. caracteres por párrafo: {MIN_CHARS}",
              "- deduplicado: primera aparición (v1–v24 son acumulativos)",
              "- descartados: filas de tabla, encabezados numerados cortos, viñetas,",
              "  líneas con menos de la mitad de letras",
              "- generado por `experiments/corpus_informes_limpio.py`", "",
              "## Párrafos nuevos por informe", ""]
    lineas += [f"- {k}: {v}" for k, v in por_informe.items()]
    (salida / "README.md").write_text("\n".join(lineas) + "\n", encoding="utf8")

    print(f"{len(textos)} textos ({args.unidad}) · {len(parrafos)} párrafos · "
          f"{palabras} palabras → {salida}/{nombre}")
    print("nuevos por informe:", {k.split('_')[-1]: v for k, v in por_informe.items()})


if __name__ == "__main__":
    main()
