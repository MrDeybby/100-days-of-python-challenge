"""
Diario personal cifrado (Day 60) usando cryptography.fernet.
- Protección por contraseña.
- Cifra contenido de cada entrada.
- Lista y lee entradas guardadas en ./entries.
"""

from __future__ import annotations

import base64
import getpass
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    print("Necesitas instalar cryptography: pip install cryptography")
    sys.exit(1)


BASE_DIR = Path(__file__).parent
ENTRIES_DIR = BASE_DIR / "entries"
KEY_FILE = BASE_DIR / ".secret_key.json"
ITERATIONS = 200_000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def load_or_create_fernet(password: str) -> Fernet:
    if KEY_FILE.exists():
        data = json.loads(KEY_FILE.read_text(encoding="utf-8"))
        salt = base64.b64decode(data["salt"])
        enc_master = base64.b64decode(data["enc_master"])
    else:
        salt = Fernet.generate_key()[:16]
        master = Fernet.generate_key()
        key_for_master = derive_key(password, salt)
        enc_master = Fernet(key_for_master).encrypt(master)
        KEY_FILE.write_text(
            json.dumps(
                {
                    "salt": base64.b64encode(salt).decode("utf-8"),
                    "enc_master": base64.b64encode(enc_master).decode("utf-8"),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
    key_for_master = derive_key(password, salt)
    try:
        master = Fernet(key_for_master).decrypt(enc_master)
    except InvalidToken:
        print("Contraseña incorrecta o archivo de clave corrupto.")
        sys.exit(1)
    return Fernet(master)


def prompt_password() -> str:
    while True:
        pwd = getpass.getpass("Contraseña: ").strip()
        if pwd:
            return pwd
        print("La contraseña no puede estar vacía.")


def sanitize_title(title: str) -> str:
    title = title.strip()
    title = re.sub(r"[\\/:*?\"<>|]", "_", title)
    title = re.sub(r"\s+", "_", title)
    return title or "entrada"


def list_entries() -> List[Path]:
    ENTRIES_DIR.mkdir(exist_ok=True)
    return sorted(ENTRIES_DIR.glob("*.enc"))


def create_entry(fernet: Fernet) -> None:
    title = input("Título de la entrada: ").strip()
    content_lines: List[str] = []
    print("Escribe el contenido. Línea vacía para terminar:")
    while True:
        line = input()
        if line == "":
            break
        content_lines.append(line)
    content = "\n".join(content_lines).strip()
    if not content:
        print("Contenido vacío, cancelado.")
        return

    safe_title = sanitize_title(title)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{safe_title}.enc"
    filepath = ENTRIES_DIR / filename
    ENTRIES_DIR.mkdir(exist_ok=True)
    token = fernet.encrypt(content.encode("utf-8"))
    filepath.write_bytes(token)
    print(f"Entrada guardada en {filepath}")


def view_all_entries() -> None:
    files = list_entries()
    if not files:
        print("No hay entradas todavía.")
        return
    print("\nEntradas:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file.name}")
    print("")


def read_entry(fernet: Fernet) -> None:
    files = list_entries()
    if not files:
        print("No hay entradas para leer.")
        return
    print("\nEntradas disponibles:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file.name}")
    choice = input("Número de entrada: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(files)):
        print("Selección inválida.")
        return
    selected = files[int(choice) - 1]
    try:
        decrypted = fernet.decrypt(selected.read_bytes()).decode("utf-8")
    except InvalidToken:
        print("No se pudo descifrar el contenido (clave/contraseña incorrecta).")
        return
    print(f"\n--- {selected.name} ---")
    print(decrypted)
    print("--- fin de la entrada ---\n")


def menu(fernet: Fernet) -> None:
    options = {
        "1": ("Crear nueva entrada", lambda: create_entry(fernet)),
        "2": ("Ver todas las entradas", view_all_entries),
        "3": ("Leer una entrada", lambda: read_entry(fernet)),
        "4": ("Salir", None),
    }
    while True:
        print("===== Diario Personal (Day 60) =====")
        for k, (txt, _) in options.items():
            print(f"{k}. {txt}")
        choice = input("Elige una opción: ").strip()
        if choice == "4":
            print("Hasta luego.")
            break
        action = options.get(choice)
        if action and action[1]:
            action[1]()
        else:
            print("Opción no válida.\n")


def main() -> None:
    print("=== Inicio de sesión del diario ===")
    password = prompt_password()
    fernet = load_or_create_fernet(password)
    menu(fernet)


if __name__ == "__main__":
    main()
