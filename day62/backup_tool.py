import json
import shutil
from datetime import datetime
from pathlib import Path


class BackupTool:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.config_file = base_dir / "backup_config.json"
        self.log_file = base_dir / "backup_activity.log"
        self.source_dir = None
        self.backup_root = None
        self.load_config()

    def load_config(self):
        if self.config_file.exists():
            try:
                with self.config_file.open("r", encoding="utf-8") as file:
                    data = json.load(file)
                self.source_dir = Path(data.get("source_dir", "")).expanduser() if data.get("source_dir") else None
                self.backup_root = Path(data.get("backup_root", "")).expanduser() if data.get("backup_root") else None
            except Exception as exc:
                self.log_activity(f"ERROR al cargar configuración: {exc}")

    def save_config(self):
        data = {
            "source_dir": str(self.source_dir) if self.source_dir else "",
            "backup_root": str(self.backup_root) if self.backup_root else "",
        }
        with self.config_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    def log_activity(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {message}\n")

    def prompt_path(self, label: str):
        return input(f"{label}: ").strip()

    def configure_directories(self):
        print("\nConfiguración de directorios")
        source = self.prompt_path("Ingrese la ruta del directorio fuente")
        backup_root = self.prompt_path("Ingrese la ruta del repositorio de respaldo")

        if not source or not backup_root:
            print("Error: ambos campos son obligatorios.")
            self.log_activity("ERROR: configuración incompleta")
            return

        self.source_dir = Path(source).expanduser()
        self.backup_root = Path(backup_root).expanduser()

        if not self.source_dir.exists():
            print("Error: el directorio fuente no existe.")
            self.log_activity(f"ERROR: directorio fuente no encontrado: {self.source_dir}")
            return

        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.save_config()
        print("Configuración guardada correctamente.")
        self.log_activity(f"Configuración guardada: fuente={self.source_dir} respaldo={self.backup_root}")

    def create_backup(self):
        if not self.source_dir or not self.backup_root:
            print("Primero configure los directorios.")
            return

        if not self.source_dir.exists():
            print("Error: el directorio fuente no existe.")
            self.log_activity(f"ERROR: directorio fuente no encontrado: {self.source_dir}")
            return

        if not self.backup_root.exists():
            self.backup_root.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = self.backup_root / f"backup_{timestamp}"
        backup_folder.mkdir(parents=True, exist_ok=True)

        try:
            for item in self.source_dir.iterdir():
                destination = backup_folder / item.name
                if item.is_dir():
                    shutil.copytree(item, destination, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, destination)

            print(f"Respaldo creado correctamente en: {backup_folder}")
            self.log_activity(f"OK: respaldo creado en {backup_folder}")
        except Exception as exc:
            print(f"Error durante el respaldo: {exc}")
            self.log_activity(f"ERROR: respaldo fallido - {exc}")

    def show_log(self):
        if not self.log_file.exists():
            print("No hay actividades registradas todavía.")
            return

        print("\nRegistro de actividades:")
        with self.log_file.open("r", encoding="utf-8") as file:
            for line in file.readlines():
                print(line.rstrip())

    def show_menu(self):
        while True:
            print("\n=== Herramienta de Backups ===")
            print("1. Configurar directorios")
            print("2. Crear respaldo")
            print("3. Mostrar registro")
            print("4. Salir")

            option = input("Seleccione una opción: ").strip()

            if option == "1":
                self.configure_directories()
            elif option == "2":
                self.create_backup()
            elif option == "3":
                self.show_log()
            elif option == "4":
                print("Saliendo de la herramienta de backups...")
                self.log_activity("Información: salida del menú")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
                self.log_activity(f"ERROR: opción inválida seleccionada: {option}")


def main():
    base_dir = Path(__file__).resolve().parent
    tool = BackupTool(base_dir)
    tool.show_menu()


if __name__ == "__main__":
    main()
