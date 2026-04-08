from __future__ import annotations

import os
import shutil
from pathlib import Path


CATEGORIAS = {
    "imagenes": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"},
    "videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"},
    "musica": {".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"},
    "documentos": {".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".csv", ".md"},
    "comprimidos": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "ejecutables": {".exe", ".msi", ".bat", ".sh", ".apk"},
}


def obtener_categoria(ext: str) -> str:
    ext = ext.lower()
    for nombre, extensiones in CATEGORIAS.items():
        if ext in extensiones:
            return nombre
    return "otros"


def nombre_unico(destino: Path) -> Path:
    """Evita sobrescribir archivos agregando sufijos numericos."""
    if not destino.exists():
        return destino
    stem = destino.stem
    suffix = destino.suffix
    parent = destino.parent
    contador = 1
    while True:
        candidato = parent / f"{stem}_{contador}{suffix}"
        if not candidato.exists():
            return candidato
        contador += 1


def organizar_carpeta(ruta_objetivo: Path) -> None:
    archivos_movidos = 0
    for entry in ruta_objetivo.iterdir():
        if entry.is_dir():
            continue
        categoria = obtener_categoria(entry.suffix)
        destino_dir = ruta_objetivo / categoria
        destino_dir.mkdir(exist_ok=True)
        destino_archivo = nombre_unico(destino_dir / entry.name)
        shutil.move(str(entry), str(destino_archivo))
        archivos_movidos += 1
    print(f"\nListo. Archivos movidos: {archivos_movidos}")


def solicitar_ruta() -> Path | None:
    ruta = input("\nIngresa la ruta de la carpeta a organizar: ").strip().strip('"')
    if not ruta:
        print("No se ingreso ruta.")
        return None
    ruta_objetivo = Path(ruta).expanduser().resolve()
    if not ruta_objetivo.exists() or not ruta_objetivo.is_dir():
        print("La ruta no es valida o no es una carpeta.")
        return None
    return ruta_objetivo


def mostrar_menu() -> None:
    print(
        "\n=== Organizador de Documentos (Día 52) ===\n"
        "1) Organizar carpeta\n"
        "2) Ver categorias y extensiones\n"
        "3) Salir\n"
    )


def mostrar_categorias() -> None:
    print("\nCategorias configuradas:")
    for nombre, extensiones in CATEGORIAS.items():
        lista = ", ".join(sorted(extensiones))
        print(f"- {nombre}: {lista}")
    print("- otros: cualquier extension no listada")


def main() -> None:
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            ruta = solicitar_ruta()
            if ruta:
                organizar_carpeta(ruta)
        elif opcion == "2":
            mostrar_categorias()
        elif opcion == "3":
            print("Hasta luego.")
            break
        else:
            print("Opcion no valida. Intenta de nuevo.")


if __name__ == "__main__":
    main()
