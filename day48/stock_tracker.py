"""
Rastreador simple de precios de acciones desde Yahoo Finance usando BeautifulSoup.

Uso:
    python day48/stock_tracker.py

El script solicita:
- Ticker (por defecto AAPL)
- Intervalo de actualización en segundos (por defecto 10)
- Número de lecturas (por defecto 5; 0 para infinito)

Scrapea la página https://finance.yahoo.com/quote/<ticker> y extrae
precio, cambio y variación porcentual con BeautifulSoup.
Maneja fallos de red/parseo sin detener el bucle.
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://finance.yahoo.com/quote/{ticker}"


@dataclass
class Quote:
    price: float
    change: float
    change_percent: float
    time_utc: datetime


def fetch_quote_bs(ticker: str) -> Optional[Quote]:
    """Scrapea la página de Yahoo Finance y devuelve la última cotización."""
    url = BASE_URL.format(ticker=ticker)
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; StockTracker/1.0)",
        "Accept-Language": "en-US,en;q=0.9",
    }
    # try:
    #     resp = requests.get(url, headers=headers, timeout=8)
    #     resp.raise_for_status()
    # except Exception:
    #     return None

    resp = requests.get(url, headers=headers, timeout=8)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Yahoo suele usar <fin-streamer data-symbol="AAPL" data-field="regularMarketPrice">...</fin-streamer>
    price_tag = soup.find("fin-streamer", {"data-symbol": ticker, "data-field": "regularMarketPrice"})
    change_tag = soup.find("fin-streamer", {"data-symbol": ticker, "data-field": "regularMarketChange"})
    pct_tag = soup.find("fin-streamer", {"data-symbol": ticker, "data-field": "regularMarketChangePercent"})

    try:
        price = float(price_tag.text.replace(",", ""))
        change = float(change_tag.text.replace(",", ""))
        change_percent = float(pct_tag.text.replace("%", "").replace(",", ""))
    except Exception:
        return None

    ts = datetime.now(tz=timezone.utc)
    return Quote(price=price, change=change, change_percent=change_percent, time_utc=ts)


def prompt_default(prompt: str, default: str) -> str:
    raw = input(f"{prompt} [{default}]: ").strip()
    return raw or default


def main() -> int:
    print("=== Rastreador de precios Yahoo Finance (BeautifulSoup) ===")
    ticker = prompt_default("Ticker", "AAPL").upper()

    interval = 3

    print(f"\nComenzando seguimiento de {ticker}. Ctrl+C para salir.\n")
    header = f"{'Hora UTC':<20} {'Ticker':<6} {'Precio':>10} {'Cambio':>10} {'%':>8}"
    print(header)
    print("-" * len(header))

    while True:
        quote = fetch_quote_bs(ticker)
        if quote:
            ts = quote.time_utc.strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"{ts:<20} {ticker:<6} {quote.price:>10.2f} {quote.change:>+10.2f} {quote.change_percent:>+8.2f}%"
            )
        else:
            print(f"{datetime.utcnow():%Y-%m-%d %H:%M:%S}   {ticker:<6}  ERROR al obtener datos")

        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nInterrumpido por el usuario.")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
