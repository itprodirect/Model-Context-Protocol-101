"""Utility functions for business operations."""

import csv
from pathlib import Path
from typing import Iterable

PathLike = str | Path
Record = dict[str, str]


def calculate_profit(revenue: float, cost: float) -> float:
    """Return the profit calculated as revenue minus cost."""
    return revenue - cost


def get_sales_from_csv(filename: PathLike) -> float:
    """Read a CSV of sales data and return total sales as float."""
    total = 0.0
    with Path(filename).expanduser().open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            total += float(row["sales"])
    return total


def calculate_commission(premiums: Iterable[float], rate: float = 0.1) -> float:
    """Return total commission in USD rounded to two decimals."""
    return round(sum(premiums) * rate, 2)


def load_insurance_sales(filename: PathLike) -> list[Record]:
    """Return all rows from an insurance sales CSV as dictionaries."""
    with Path(filename).expanduser().open(newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def total_commission(records: Iterable[Record]) -> float:
    """Return the sum of the ``Commission`` column from insurance records."""
    total = 0.0
    for row in records:
        total += float(row["Commission"])
    return total


def filter_by_state(records: Iterable[Record], state: str) -> list[Record]:
    """Return only the rows matching a given state code."""
    state_upper = state.upper()
    return [row for row in records if row["State"].upper() == state_upper]


def calculate_total_premium(records: Iterable[Record]) -> float:
    """Return the sum of the ``Premium`` column from insurance records."""
    total = 0.0
    for row in records:
        total += float(row["Premium"])
    return total


def filter_policies_by_state(records: Iterable[Record], state: str) -> list[Record]:
    """Wrapper around :func:`filter_by_state` with a clearer name."""
    return filter_by_state(records, state)
