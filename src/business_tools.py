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


def load_insurance_sales(filename: str) -> list[dict[str, str]]:
    """Return all rows from an insurance sales CSV as dictionaries.

    Args:
        filename: Path to ``insurance_sales.csv``.

    Returns:
        A list of dictionaries, one per CSV row.
    """
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def total_commission(records: list[dict[str, str]]) -> float:
    """Return the sum of the ``Commission`` column from insurance records.

    Args:
        records: Rows loaded via :func:`load_insurance_sales`.

    Returns:
        Total commission as a float.
    """
    total = 0.0
    for row in records:
        total += float(row["Commission"])
    return total


def filter_by_state(records: list[dict[str, str]], state: str) -> list[dict[str, str]]:
    """Return only the rows matching a given state code.

    Args:
        records: Insurance sale rows.
        state: Two-letter state abbreviation.

    Returns:
        Filtered list containing rows where ``State`` equals ``state``.
    """
    return [row for row in records if row["State"] == state]
