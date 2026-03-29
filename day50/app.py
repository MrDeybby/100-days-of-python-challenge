import os
from typing import Dict, List, Optional

import requests
from flask import Flask, flash, render_template, request

# Config
DEFAULT_CITIES: List[str] = ["London", "New York", "Tokyo", "Santo Domingo"]
DEFAULT_UNITS = "metric"
API_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")


class WeatherError(Exception):
    pass


def fetch_weather(city: str, units: str, api_key: str) -> Dict:
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
        "lang": "es",
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise WeatherError(f"No se pudo obtener clima para {city}: {exc}")

    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    sys_info = data.get("sys", {})

    return {
        "city": data.get("name", city.title()),
        "country": sys_info.get("country", ""),
        "temp": main.get("temp"),
        "feels_like": main.get("feels_like"),
        "humidity": main.get("humidity"),
        "pressure": main.get("pressure"),
        "wind": wind.get("speed"),
        "description": weather.get("description", "N/D"),
        "icon": weather.get("icon", "01d"),
        "units": units,
    }


def ensure_api_key() -> str:
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise WeatherError(
            "Configura la variable de entorno OPENWEATHER_API_KEY antes de iniciar la app."
        )
    return api_key


@app.route("/", methods=["GET", "POST"])
def index():
    try:
        api_key: str = ensure_api_key()
    except WeatherError as err:
        flash(str(err), "error")
        api_key = None

    cities_input = request.form.get("cities") if request.method == "POST" else None
    units = request.form.get("units") or DEFAULT_UNITS

    city_names = (
        [c.strip() for c in cities_input.split(",") if c.strip()]
        if cities_input
        else DEFAULT_CITIES
    )

    results = []

    if api_key:
        for city in city_names:
            try:
                results.append(fetch_weather(city, units, api_key))
            except WeatherError as err:
                flash(str(err), "error")

    units_label = "\u00B0C" if units == "metric" else "\u00B0F"

    return render_template(
        "index.html",
        results=results,
        units=units,
        units_label=units_label,
        default_cities=",".join(city_names),
    )


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)