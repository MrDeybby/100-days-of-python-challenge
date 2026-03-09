import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def clean_and_preprocess(input_csv: Path, output_csv: Path) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(input_csv)
    initial_rows = len(df)

    df.columns = [c.strip().lower() for c in df.columns]

    text_cols = ["product", "category", "region", "sales_channel"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    df["region"] = df["region"].str.title()
    df["sales_channel"] = df["sales_channel"].str.title()

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    before_drop_invalid_dates = len(df)
    df = df.dropna(subset=["order_date"])
    invalid_date_rows = before_drop_invalid_dates - len(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    before_drop_duplicates = len(df)
    df = df.drop_duplicates()
    duplicate_rows = before_drop_duplicates - len(df)

    qty_median = max(1, int(df["quantity"].median(skipna=True)))
    df["quantity"] = df["quantity"].fillna(qty_median)
    bad_qty_mask = df["quantity"] <= 0
    bad_qty_rows = int(bad_qty_mask.sum())
    df.loc[bad_qty_mask, "quantity"] = qty_median
    df["quantity"] = df["quantity"].round().astype(int)

    product_price_median = df.groupby("product")["unit_price"].transform("median")
    category_price_median = df.groupby("category")["unit_price"].transform("median")
    global_price_median = float(df["unit_price"].median(skipna=True))
    df["unit_price"] = (
        df["unit_price"]
        .where(df["unit_price"] > 0)
        .fillna(product_price_median)
        .fillna(category_price_median)
        .fillna(global_price_median)
    )

    df["revenue"] = (df["quantity"] * df["unit_price"]).round(2)
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    df = df.sort_values("order_date").reset_index(drop=True)
    
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    stats = {
        "initial_rows": initial_rows,
        "final_rows": len(df),
        "duplicates_removed": duplicate_rows,
        "invalid_date_rows_removed": invalid_date_rows,
        "invalid_or_missing_quantity_fixed": bad_qty_rows,
    }
    return df, stats


def print_report(df: pd.DataFrame, top_n: int = 5) -> None:
    total_revenue = df["revenue"].sum()
    total_units = df["quantity"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders else 0

    print("\n===== SALES ANALYTICS REPORT =====")
    print(f"Records analyzed: {len(df):,}")
    print(f"Total orders: {total_orders:,}")
    print(f"Total units sold: {total_units:,}")
    print(f"Total revenue: ${total_revenue:,.2f}")
    print(f"Average order value: ${avg_order_value:,.2f}")

    print("\n--- Top Products by Units Sold ---")
    top_units = (
        df.groupby("product", as_index=False)["quantity"]
        .sum()
        .sort_values("quantity", ascending=False)
        .head(top_n)
    )
    for _, row in top_units.iterrows():
        print(f"{row['product']}: {int(row['quantity'])} units")

    print("\n--- Top Products by Revenue ---")
    top_revenue = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(top_n)
    )
    for _, row in top_revenue.iterrows():
        print(f"{row['product']}: ${row['revenue']:,.2f}")

    print("\n--- Monthly Revenue Trend ---")
    monthly = df.groupby("month", as_index=False)["revenue"].sum().sort_values("month")
    for _, row in monthly.iterrows():
        print(f"{row['month']}: ${row['revenue']:,.2f}")

    best_month = monthly.loc[monthly["revenue"].idxmax()]
    worst_month = monthly.loc[monthly["revenue"].idxmin()]
    print(f"Best month: {best_month['month']} (${best_month['revenue']:,.2f})")
    print(f"Lowest month: {worst_month['month']} (${worst_month['revenue']:,.2f})")

    print("\n--- Revenue Breakdown by Category ---")
    by_category = (
        df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    )
    category_total = by_category["revenue"].sum()
    for _, row in by_category.iterrows():
        pct = (row["revenue"] / category_total * 100) if category_total else 0
        print(f"{row['category']}: ${row['revenue']:,.2f} ({pct:.1f}%)")

    print("\n--- Revenue Breakdown by Sales Channel ---")
    by_channel = (
        df.groupby("sales_channel", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    )
    channel_total = by_channel["revenue"].sum()
    for _, row in by_channel.iterrows():
        pct = (row["revenue"] / channel_total * 100) if channel_total else 0
        print(f"{row['sales_channel']}: ${row['revenue']:,.2f} ({pct:.1f}%)")


def save_visualizations(df: pd.DataFrame, output_dir: Path, top_n: int = 8) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    top_products = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(top_n)
        .iloc[::-1]
    )

    plt.figure(figsize=(10, 6))
    plt.barh(top_products["product"], top_products["revenue"], color="#2a9d8f")
    plt.title("Top Products by Revenue")
    plt.xlabel("Revenue (USD)")
    plt.tight_layout()
    plt.savefig(output_dir / "top_products_revenue.png", dpi=150)
    plt.close()

    monthly = df.groupby("month", as_index=False)["revenue"].sum().sort_values("month")
    plt.figure(figsize=(10, 6))
    plt.plot(monthly["month"], monthly["revenue"], marker="o", color="#264653")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_revenue_trend.png", dpi=150)
    plt.close()

    by_category = (
        df.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    )
    plt.figure(figsize=(8, 8))
    plt.pie(by_category["revenue"], labels=by_category["category"], autopct="%1.1f%%", startangle=140)
    plt.title("Revenue Share by Category")
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_by_category.png", dpi=150)
    plt.close()

    kpi = {
        "Total Revenue": df["revenue"].sum(),
        "Total Units": df["quantity"].sum(),
        "Orders": df["order_id"].nunique(),
        "Avg Order Value": df["revenue"].sum() / max(df["order_id"].nunique(), 1),
    }
    plt.figure(figsize=(10, 6))
    plt.bar(kpi.keys(), kpi.values(), color=["#e76f51", "#2a9d8f", "#f4a261", "#457b9d"])
    plt.title("Key Sales Metrics")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(output_dir / "key_metrics.png", dpi=150)
    plt.close()

def main() -> None:

    input_csv = input("Enter the path to the sales data CSV file (or press Enter to use default 'sales_data.csv'): ").strip()
    output_dir = input("Enter the directory to save the report and charts (or press Enter to use default 'output'): ").strip()
    output_dir = Path(output_dir)

    clean_df, stats = clean_and_preprocess(input_csv, input_csv[:-4] + "_cleaned.csv")
    print(f"Cleaned data saved: {output_dir}")
    print("Cleaning summary:")
    for key, value in stats.items():
        print(f"- {key}: {value}")

    print_report(clean_df, top_n=5)
    save_visualizations(clean_df, output_dir, top_n=5)
    print(f"\nCharts saved in: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
