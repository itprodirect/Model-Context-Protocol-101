"""Compatibility wrapper for legacy ``business_tools`` imports.

This module re-exports the public helpers from :mod:`mcp101.business_tools`
so existing guides, notebooks, or downstream scripts that still import the
original ``business_tools`` module keep working without modification.
"""

from __future__ import annotations

from mcp101 import business_tools as _impl

calculate_profit = _impl.calculate_profit
get_sales_from_csv = _impl.get_sales_from_csv
calculate_commission = _impl.calculate_commission
load_insurance_sales = _impl.load_insurance_sales
total_commission = _impl.total_commission
filter_by_state = _impl.filter_by_state
calculate_total_premium = _impl.calculate_total_premium
filter_policies_by_state = _impl.filter_policies_by_state

__all__ = [
    "calculate_profit",
    "get_sales_from_csv",
    "calculate_commission",
    "load_insurance_sales",
    "total_commission",
    "filter_by_state",
    "calculate_total_premium",
    "filter_policies_by_state",
]
