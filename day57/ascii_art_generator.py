"""
Generador simple de arte ASCII para terminal.
Pide una ruta de imagen, la redimensiona si es grande y guarda el
resultado en un archivo .txt en la misma carpeta.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable, List

try:
    from PIL import Image
except ImportError:  # pragma: no cover - se alerta al usuario en tiempo de ejecucion
    print("Necesitas instalar Pillow primero: pip install pillow")
    sys.exit(1)

# Cuanto mas corta sea la cadena, mas contrastado el resultado.
PALETTE = "@%#*+=-:. "
MAX_WIDTH = 120
MAX_HEIGHT = 120
# Ajuste porque los caracteres son mas altos que anchos en la terminal.
HEIGHT_ADJUST = 0.55


def prompt_image_path() -> Path:
    """Solicita al usuario la ruta de la imagen y valida su existencia."""
    while True:
        ruta = input("Ruta de la imagen: ").strip().strip('"')
        if not ruta:
            print("Ingresa una ruta valida.")
            continue
        imagen_path = Path(ruta).expanduser()
        if imagen_path.is_file():
            return imagen_path
        print("No se encontro el archivo, intenta de nuevo.")


def prompt_output_name(carpeta: Path, base: str) -> Path:
    """Pide un nombre de archivo sin extension y devuelve la ruta final .txt."""
    while True:
        nombre = input("Nombre para el archivo ASCII (sin extension): ").strip()
        if not nombre:
            print("El nombre no puede estar vacio.")
            continue
        destino = carpeta / f"{nombre}.txt"
        if destino.exists():
            sobreescribir = input(
                "El archivo ya existe. Sobrescribir? (s/n): "
            ).strip().lower()
            if sobreescribir != "s":
                continue
        return destino


def resize_for_terminal(img: Image.Image) -> Image.Image:
    """Redimensiona manteniendo proporcion y limitando el tamano."""
    ancho, alto = img.size
    escala_w = MAX_WIDTH / ancho
    escala_h = MAX_HEIGHT / alto
    escala = min(1.0, escala_w, escala_h)

    nuevo_ancho = max(1, int(ancho * escala))
    # Ajuste de altura para que el ASCII no quede aplastado.
    nuevo_alto = max(1, int(alto * escala * HEIGHT_ADJUST))
    return img.resize((nuevo_ancho, nuevo_alto))


def pixel_to_char(pixel: int) -> str:
    """Mapea un valor de 0-255 al caracter correspondiente en la paleta."""
    escala = (len(PALETTE) - 1) / 255
    return PALETTE[int(pixel * escala)]


def image_to_ascii_lines(img: Image.Image) -> List[str]:
    """Convierte una imagen PIL a una lista de lineas de ASCII."""
    gray = img.convert("L")  # escala de grises
    pix = gray.load()
    ancho, alto = gray.size
    lineas: List[str] = []
    for y in range(alto):
        fila = "".join(pixel_to_char(pix[x, y]) for x in range(ancho))
        lineas.append(fila)
    return lineas


def save_ascii(lines: Iterable[str], destino: Path) -> None:
    destino.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print("=== Generador de Arte ASCII (Day 57) ===")
    img_path = prompt_image_path()
    try:
        original = Image.open(img_path)
    except OSError as exc:  # archivo no es imagen
        print(f"No se pudo abrir la imagen: {exc}")
        return

    ajustada = resize_for_terminal(original)
    lineas = image_to_ascii_lines(ajustada)

    destino = prompt_output_name(img_path.parent, img_path.stem)
    save_ascii(lineas, destino)

    print(f"Listo! Archivo guardado en: {destino}")
    print("Puedes abrirlo con cualquier editor de texto.")


if __name__ == "__main__":
    main()
