"""
Trazador de temperatura con prompts secuenciales en la terminal.

Uso:
    python day47/trazador.py

Pide la ruta de un CSV con columnas 'fecha' y temperatura (segunda columna),
calcula medias moviles y anomalias contra la media movil mas larga, y guarda
un PNG en la misma carpeta llamado <nombre_csv>_temperatura.png.
"""

from pathlib import Path
from typing import List


def parse_windows(raw: str) -> List[int]:
    if not raw.strip():
        return [7, 30]
    parsed: List[int] = []
    for v in raw.split(","):
        v = v.strip()
        if not v:
            continue
        try:
            parsed.append(int(v))
        except ValueError:
            print(f"Ventana invalida ignorada: {v}")
    return parsed or [7, 30]


def main() -> int:
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
    except ImportError as exc:
        print("Faltan dependencias: pip install pandas matplotlib")
        print(f"Detalle: {exc}")
        return 1

    csv_input = input("Ruta del CSV (columna fecha y temperatura): ").strip().strip('"')
    if not csv_input:
        print("No se indico ruta. Saliendo.")
        return 1

    csv_path = Path(csv_input)
    if not csv_path.exists():
        print(f"No se encontro el archivo: {csv_path}")
        return 1

    windows_raw = input("Ventanas de promedio movil separadas por coma (default 7,30): ")
    windows = parse_windows(windows_raw)

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:  # pragma: no cover - simple CLI
        print(f"No se pudo leer el CSV: {exc}")
        return 1

    if "fecha" not in df.columns or len(df.columns) < 2:
        print("Se espera al menos columnas 'fecha' y 'temperatura_c'.")
        return 1

    df["fecha"] = pd.to_datetime(df["fecha"])
    temp_col = df.columns[1]
    df = df.sort_values("fecha").reset_index(drop=True)

    for w in windows:
        df[f"ma_{w}"] = df[temp_col].rolling(window=w, min_periods=1, center=False).mean()

    base_window = max(windows)
    df["anomalia"] = df[temp_col] - df[f"ma_{base_window}"]

    plt.style.use("seaborn-v0_8")
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    axes[0].plot(df["fecha"], df[temp_col], label=temp_col, color="#1f77b4", linewidth=1)
    for w in windows:
        axes[0].plot(df["fecha"], df[f"ma_{w}"], label=f"MA {w}d", linewidth=1.4)
    axes[0].set_ylabel("C")
    axes[0].set_title("Serie diaria y promedios moviles")
    axes[0].legend()

    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].bar(df["fecha"], df["anomalia"], color="#d62728", width=1, alpha=0.7, label="Anomalia vs MA larga")
    axes[1].set_ylabel("Delta C")
    axes[1].set_title(f"Anomalias respecto a MA {base_window}d")

    fig.autofmt_xdate()
    fig.tight_layout()

    output_name = csv_path.stem + "_temperatura.png"
    output_path = csv_path.with_name(output_name)
    fig.savefig(output_path, dpi=150)
    print(f"Grafico guardado en: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
