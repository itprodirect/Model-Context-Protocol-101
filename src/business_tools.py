"""Utility functions for business operations."""

import csv


def calculate_profit(revenue: float, cost: float) -> float:
    """Return the profit calculated as revenue minus cost."""
    return revenue - cost


def get_sales_from_csv(filename: str) -> float:
    """Read a CSV of sales data and return total sales as float."""
    total = 0.0
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total += float(row["sales"])
    return total


def calculate_commission(premiums: list[float], rate: float = 0.1) -> float:
    """Return total commission in USD rounded to two decimals."""
    return round(sum(premiums) * rate, 2)
