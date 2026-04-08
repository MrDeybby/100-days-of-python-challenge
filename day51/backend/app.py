from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "expenses.csv"
WEB_DIR = BASE_DIR.parent / "web"

app = Flask(__name__, static_folder=None)
CORS(app)


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CSV_PATH.exists():
        CSV_PATH.write_text("date,category,description,amount\n", encoding="utf-8")


def _read_expenses() -> List[Dict[str, str]]:
    _ensure_storage()
    rows: List[Dict[str, str]] = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def _append_expense(expense: Dict[str, str]) -> None:
    _ensure_storage()
    fieldnames = ["date", "category", "description", "amount"]
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(expense)


def _parse_amount(value: str) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError("El monto debe ser numérico.")
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a 0.")
    return amount


def _parse_date(value: str | None) -> str:
    if not value:
        return date.today().isoformat()
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("La fecha debe tener formato AAAA-MM-DD.")
    return parsed.isoformat()


def _build_summary(expenses: List[Dict[str, str]]) -> Dict:
    totals = defaultdict(float)
    monthly = defaultdict(float)
    daily = defaultdict(float)

    for exp in expenses:
        amount = float(exp["amount"])
        category = exp["category"] or "Sin categoría"
        totals[category] += amount

        dt = datetime.strptime(exp["date"], "%Y-%m-%d").date()
        monthly_key = dt.strftime("%Y-%m")
        monthly[monthly_key] += amount
        daily[dt.isoformat()] += amount

    def to_list(data: Dict[str, float]):
        return sorted(
            [{"label": k, "total": round(v, 2)} for k, v in data.items()],
            key=lambda x: x["label"],
        )

    total_spent = round(sum(totals.values()), 2)

    return {
        "total_spent": total_spent,
        "by_category": to_list(totals),
        "by_month": to_list(monthly),
        "by_day": to_list(daily),
        "count": len(expenses),
    }


@app.route("/api/expenses", methods=["GET", "POST"])
def expenses():
    if request.method == "POST":
        payload = request.get_json(force=True, silent=True) or {}
        try:
            amount = _parse_amount(str(payload.get("amount")))
            expense_date = _parse_date(payload.get("date"))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        expense = {
            "date": expense_date,
            "category": (payload.get("category") or "").strip() or "General",
            "description": (payload.get("description") or "").strip(),
            "amount": f"{amount:.2f}",
        }
        _append_expense(expense)
        return jsonify({"message": "Gasto guardado", "expense": expense}), 201

    # GET
    expenses = _read_expenses()
    limit = request.args.get("limit")
    if limit:
        try:
            n = int(limit)
            expenses = expenses[-n:]
        except ValueError:
            pass
    return jsonify({"expenses": expenses})


@app.route("/api/summary", methods=["GET"])
def summary():
    expenses = _read_expenses()
    data = _build_summary(expenses)
    return jsonify(data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path: str):
    target = WEB_DIR / path
    if path and target.exists():
        return send_from_directory(WEB_DIR, path)
    return send_from_directory(WEB_DIR, "index.html")


if __name__ == "__main__":
    _ensure_storage()
    app.run(debug=True, port=5000)
