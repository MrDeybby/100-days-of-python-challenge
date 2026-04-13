"""
Conversor sencillo de Markdown a HTML (Day 59).
- Pide ruta de archivo .md
- Convierte a HTML usando la libreria markdown si esta disponible
- Inserta CSS basico dentro de una plantilla HTML
- Pregunta donde guardar el resultado
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import markdown  # type: ignore
except ImportError:
    markdown = None


CSS = """
body {
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px 60px;
  background: #f7f7fb;
  color: #222;
}
h1, h2, h3, h4 {
  color: #222;
  margin-top: 1.6em;
}
a { color: #0d6efd; }
code {
  background: #eef0f4;
  padding: 2px 5px;
  border-radius: 4px;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 0.95em;
}
pre code {
  display: block;
  padding: 14px;
  overflow-x: auto;
}
blockquote {
  border-left: 4px solid #d0d4dd;
  padding-left: 12px;
  color: #555;
}
table {
  border-collapse: collapse;
  width: 100%;
}
th, td {
  border: 1px solid #d0d4dd;
  padding: 8px 10px;
}
"""


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
<main>
{content}
</main>
</body>
</html>
"""


def pedir_ruta_markdown() -> Path:
    while True:
        ruta = input("Ruta del archivo Markdown (.md): ").strip().strip('"')
        if not ruta:
            print("Ingresa una ruta valida.")
            continue
        md_path = Path(ruta).expanduser()
        if md_path.is_file():
            return md_path
        print("No se encontro el archivo, intenta de nuevo.")


def pedir_salida(md_path: Path) -> Path:
    por_defecto = md_path.with_suffix(".html")
    while True:
        ruta = input(
            f"Ruta de salida del HTML (Enter para {por_defecto}): "
        ).strip().strip('"')
        if not ruta:
            return por_defecto
        out_path = Path(ruta).expanduser()
        # Si el usuario paso solo una carpeta, usar mismo nombre
        if out_path.is_dir():
            out_path = out_path / por_defecto.name
        # Crear carpetas si no existen
        out_path.parent.mkdir(parents=True, exist_ok=True)
        return out_path


def convertir_markdown(texto: str) -> str:
    if markdown:
        return markdown.markdown(
            texto, extensions=["fenced_code", "tables", "toc", "codehilite"]
        )
    # Fallback ultra simple si markdown no esta instalado
    print(
        "Advertencia: la libreria 'markdown' no esta instalada. "
        "Se generara HTML basico sin formato.",
        file=sys.stderr,
    )
    escaped = (
        texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    return f"<pre><code>{escaped}</code></pre>"


def main() -> None:
    print("=== Conversor Markdown a HTML (Day 59) ===")
    md_path = pedir_ruta_markdown()
    salida = pedir_salida(md_path)

    contenido_md = md_path.read_text(encoding="utf-8")
    html_body = convertir_markdown(contenido_md)
    titulo = md_path.stem

    final_html = HTML_TEMPLATE.format(title=titulo, css=CSS, content=html_body)
    salida.write_text(final_html, encoding="utf-8")

    print(f"Listo! HTML guardado en: {salida}")
    if not markdown:
        print("Tip: instala la libreria completa con `pip install markdown`.")


if __name__ == "__main__":
    main()
