"""Tablero de clima en terminal con datos de OpenWeatherMap."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Tuple

import requests


FORECAST_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_CITIES = ["London", "New York", "Tokyo"]
SPARK_CHARS = " .:-=+*#%@"


def prompt_default(prompt: str, default: str) -> str:
    raw = input(f"{prompt} [{default}]: ").strip()
    return raw or default


def read_api_key() -> str:
    env_key = os.getenv("OPENWEATHER_API_KEY")
    default_hint = "(ENTER para usar OPENWEATHER_API_KEY)" if env_key else "(requerido)"
    raw = input(f"Ingresar API key de OpenWeatherMap {default_hint}: ").strip()
    key = raw or env_key
    if not key:
        print("ERROR: Debes proporcionar la API key.")
        sys.exit(1)
    return key



def main() -> int:
    print("=== Tablero de Clima (OpenWeatherMap) ===")
    cities_raw = prompt_default("Ciudades separadas por coma", ",".join(DEFAULT_CITIES))
    cities = [c.strip() for c in cities_raw.split(",") if c.strip()]

    units = prompt_default("Unidades (metric/imperial)", "metric").lower()
    if units not in {"metric", "imperial"}:
        print("ERROR: Unidades deben ser 'metric' o 'imperial'.")
        return 1

    hours_str = prompt_default("Horas de rango (multiplo de 3, 3-120)", "24")
    try:
        hours = int(hours_str)
    except ValueError:
        print("ERROR: Horas debe ser un numero.")
        return 1

    if hours < 3 or hours > 120 or hours % 3 != 0:
        print("ERROR: Horas debe ser multiplo de 3 entre 3 y 120.")
        return 1

    api_key = read_api_key()

    print(f"\nCiudades: {', '.join(cities)} | Unidades: {units} | Rango: {hours}h\n")

    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url=url)
        weather_data = response.json()

        if response.status_code == 200:
            weather_condition = weather_data["weather"][0]["main"]
            humidity = weather_data["main"]["humidity"]
            wind_speed = weather_data["wind"]["speed"]
            print(f"Weather Condition: {weather_condition}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s\n")
        else:
            print(f"Error: Unable to fetch weather data, Status Code: {response.status_code}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
