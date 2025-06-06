"""Command line interface for business tools.

Provides a small set of utilities to perform
common calculations from the terminal.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from business_tools import (
    calculate_profit,
    calculate_total_premium,
    load_insurance_sales,
    total_commission,
)


def main(argv: list[str] | None = None) -> None:
    """Run the command line interface.

    Args:
        argv: Optional list of arguments for easier testing.
    """
    parser = argparse.ArgumentParser(
        description="Business tools command line interface",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    profit_parser = subparsers.add_parser(
        "profit", help="Calculate profit from revenue and cost"
    )
    profit_parser.add_argument("revenue", type=float, help="Revenue in USD")
    profit_parser.add_argument("cost", type=float, help="Cost in USD")

    commission_parser = subparsers.add_parser(
        "commission",
        help="Calculate total commission from an insurance sales CSV",
    )
    commission_parser.add_argument(
        "file", type=Path, help="Path to insurance_sales.csv"
    )

    premium_parser = subparsers.add_parser(
        "premium", help="Calculate total premium from an insurance sales CSV"
    )
    premium_parser.add_argument("file", type=Path, help="Path to insurance_sales.csv")

    args = parser.parse_args(argv)

    if args.command == "profit":
        result = calculate_profit(args.revenue, args.cost)
        print(int(result) if result.is_integer() else result)
    elif args.command == "commission":
        records = load_insurance_sales(str(args.file))
        print(total_commission(records))
    elif args.command == "premium":
        records = load_insurance_sales(str(args.file))
        print(calculate_total_premium(records))


if __name__ == "__main__":
    main()
