"""
Planificador de presupuesto personal para terminal.
Permite registrar ingresos y gastos, categorizarlos, calcular balance,
mostrar avance de objetivo de ahorro y generar un gráfico de pastel de gastos.
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, TypedDict

DATA_FILE = Path(__file__).with_name("budget_data.json")
PIE_FILE = Path(__file__).with_name("gastos_pastel.png")


class Movimiento(TypedDict):
    descripcion: str
    monto: float
    categoria: str
    fecha: str


class Datos(TypedDict):
    ingresos: List[Movimiento]
    gastos: List[Movimiento]
    objetivo_ahorro: float


def cargar_datos() -> Datos:
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            contenido = json.load(f)
        # Validación mínima para robustez
        return Datos(
            ingresos=contenido.get("ingresos", []),
            gastos=contenido.get("gastos", []),
            objetivo_ahorro=float(contenido.get("objetivo_ahorro", 0.0)),
        )
    return Datos(ingresos=[], gastos=[], objetivo_ahorro=0.0)


def guardar_datos(datos: Datos) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def pedir_float(mensaje: str) -> float:
    while True:
        valor = input(mensaje).replace(",", ".").strip()
        try:
            return float(valor)
        except ValueError:
            print("Ingrese un número válido (ej. 1250.50).")


def pedir_fecha(opcional: bool = True) -> str:
    hoy = datetime.now().strftime("%Y-%m-%d")
    texto = " (YYYY-MM-DD, vacío para hoy)" if opcional else " (YYYY-MM-DD)"
    while True:
        fecha = input(f"Fecha{texto}: ").strip()
        if not fecha and opcional:
            return hoy
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print("Fecha inválida. Use el formato YYYY-MM-DD.")


def registrar_ingreso(datos: Datos) -> None:
    print("\n--- Registrar ingreso ---")
    descripcion = input("Descripción: ").strip() or "Ingreso"
    monto = pedir_float("Monto: ")
    fecha = pedir_fecha()
    datos["ingresos"].append(
        {"descripcion": descripcion, "monto": monto, "categoria": "Ingreso", "fecha": fecha}
    )
    guardar_datos(datos)
    print("Ingreso registrado.\n")


def registrar_gasto(datos: Datos) -> None:
    print("\n--- Registrar gasto ---")
    descripcion = input("Descripción: ").strip() or "Gasto"
    monto = pedir_float("Monto: ")
    categorias = sorted({g["categoria"] for g in datos["gastos"]})
    if categorias:
        print("Categorías existentes:", ", ".join(categorias))
    categoria = input("Categoría (nuevo o existente): ").strip() or "General"
    fecha = pedir_fecha()
    datos["gastos"].append(
        {"descripcion": descripcion, "monto": monto, "categoria": categoria, "fecha": fecha}
    )
    guardar_datos(datos)
    print("Gasto registrado.\n")


def configurar_objetivo(datos: Datos) -> None:
    print("\n--- Objetivo de ahorro ---")
    objetivo = pedir_float("Nuevo objetivo de ahorro: ")
    datos["objetivo_ahorro"] = max(0.0, objetivo)
    guardar_datos(datos)
    print("Objetivo actualizado.\n")


def resumen(datos: Datos) -> None:
    total_ingresos = sum(m["monto"] for m in datos["ingresos"])
    total_gastos = sum(m["monto"] for m in datos["gastos"])
    balance = total_ingresos - total_gastos
    objetivo = datos["objetivo_ahorro"]
    avance = min(balance, objetivo) if objetivo > 0 else 0
    progreso = (avance / objetivo * 100) if objetivo > 0 else 0

    print("\n=== Resumen ===")
    print(f"Ingresos:      ${total_ingresos:,.2f}")
    print(f"Gastos:        ${total_gastos:,.2f}")
    print(f"Presupuesto restante: ${balance:,.2f}")
    if objetivo > 0:
        print(f"Objetivo de ahorro: ${objetivo:,.2f}")
        print(f"Ahorrado estimado (balance): ${balance:,.2f}")
        print(f"Progreso objetivo: {progreso:.1f}%")
    else:
        print("Objetivo de ahorro: no configurado.")

    # Top de categorías de gasto
    categorias: Dict[str, float] = defaultdict(float)
    for g in datos["gastos"]:
        categorias[g["categoria"]] += g["monto"]
    if categorias:
        print("\nGasto por categoría:")
        for cat, monto in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
            print(f"- {cat}: ${monto:,.2f}")
    print("")


def grafico_pastel(datos: Datos) -> None:
    categorias: Dict[str, float] = defaultdict(float)
    for g in datos["gastos"]:
        categorias[g["categoria"]] += g["monto"]

    if not categorias:
        print("Aún no hay gastos para graficar.\n")
        return

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        etiquetas = list(categorias.keys())
        valores = list(categorias.values())
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(valores, labels=etiquetas, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("Distribución de gastos por categoría")
        plt.tight_layout()
        plt.savefig(PIE_FILE, dpi=150)
        print(f"Gráfico guardado en: {PIE_FILE}")
        print("Ábrelo con tu visor de imágenes preferido.\n")
    except ImportError:
        print("matplotlib no está instalado. Instale con `pip install matplotlib` para generar el gráfico.\n")


def menu() -> None:
    datos = cargar_datos()
    opciones = {
        "1": ("Registrar ingreso", registrar_ingreso),
        "2": ("Registrar gasto", registrar_gasto),
        "3": ("Ver resumen y presupuesto restante", resumen),
        "4": ("Configurar objetivo de ahorro", configurar_objetivo),
        "5": ("Generar gráfico de pastel de gastos", grafico_pastel),
        "6": ("Salir", None),
    }

    while True:
        print("===== Planificador de Presupuesto (Day 56) =====")
        for clave, (texto, _) in opciones.items():
            print(f"{clave}. {texto}")
        eleccion = input("Elige una opción: ").strip()

        if eleccion == "6":
            print("Guardado. ¡Hasta luego!")
            break

        accion = opciones.get(eleccion)
        if not accion:
            print("Opción no válida. Intente de nuevo.\n")
            continue

        funcion = accion[1]
        if funcion:
            funcion(datos)


if __name__ == "__main__":
    menu()
