"""Deterministic business logic for Harborlight's fictional renewal workflow."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
from importlib.resources import files
from typing import Literal

from typing_extensions import TypedDict

DATA_AS_OF_DATE = date(2026, 7, 1)
DATA_NOTICE = "Synthetic records for the fictional Harborlight Insurance Agency."
MAX_RENEWAL_WINDOW_DAYS = 365


class DataValidationError(ValueError):
    """Raised when the packaged fictional policy data is incomplete or malformed."""


@dataclass(frozen=True)
class PolicyRecord:
    """Validated internal representation of one fictional policy record."""

    policy_id: str
    customer_label: str
    line_of_business: str
    renewal_date: date
    current_premium_cents: int
    proposed_premium_cents: int


class Renewal(TypedDict):
    """JSON-serializable renewal returned to an MCP client."""

    policy_id: str
    customer_label: str
    line_of_business: str
    renewal_date: str
    days_until_renewal: int
    current_premium_cents: int
    proposed_premium_cents: int


class UpcomingRenewals(TypedDict):
    """Structured response for an upcoming-renewals query."""

    fictional: bool
    data_notice: str
    as_of_date: str
    window_days: int
    renewals: list[Renewal]


class PremiumChange(TypedDict):
    """Structured response for a premium comparison."""

    current_cents: int
    renewal_cents: int
    change_cents: int
    change_percent: float
    direction: Literal["increase", "decrease", "unchanged"]


def _required_text(row: Mapping[str, str | None], field: str, row_number: int) -> str:
    value = row.get(field)
    if value is None or not value.strip():
        raise DataValidationError(f"Row {row_number}: missing required field '{field}'.")
    return value.strip()


def _positive_cents(row: Mapping[str, str | None], field: str, row_number: int) -> int:
    raw_value = _required_text(row, field, row_number)
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise DataValidationError(f"Row {row_number}: '{field}' must be whole cents.") from exc
    if value <= 0:
        raise DataValidationError(f"Row {row_number}: '{field}' must be greater than zero.")
    return value


def parse_policy_rows(rows: Iterable[Mapping[str, str | None]]) -> tuple[PolicyRecord, ...]:
    """Validate CSV-like rows and return immutable policy records.

    Every row must explicitly identify itself as fictional. This prevents a copied or
    substituted data file from being mistaken for the tutorial dataset.
    """

    records: list[PolicyRecord] = []
    seen_policy_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=2):
        policy_id = _required_text(row, "policy_id", row_number)
        customer_label = _required_text(row, "customer_label", row_number)
        fictional_record = _required_text(row, "fictional_record", row_number).lower()

        if fictional_record != "true":
            raise DataValidationError(
                f"Row {row_number}: 'fictional_record' must be true for tutorial data."
            )
        if not policy_id.startswith("FIC-"):
            raise DataValidationError(f"Row {row_number}: policy_id must start with 'FIC-'.")
        if not customer_label.startswith("Fictional "):
            raise DataValidationError(
                f"Row {row_number}: customer_label must start with 'Fictional '."
            )
        if policy_id in seen_policy_ids:
            raise DataValidationError(f"Row {row_number}: duplicate policy_id '{policy_id}'.")

        raw_renewal_date = _required_text(row, "renewal_date", row_number)
        try:
            renewal_date = date.fromisoformat(raw_renewal_date)
        except ValueError as exc:
            raise DataValidationError(
                f"Row {row_number}: 'renewal_date' must use YYYY-MM-DD."
            ) from exc

        records.append(
            PolicyRecord(
                policy_id=policy_id,
                customer_label=customer_label,
                line_of_business=_required_text(row, "line_of_business", row_number),
                renewal_date=renewal_date,
                current_premium_cents=_positive_cents(
                    row, "current_premium_cents", row_number
                ),
                proposed_premium_cents=_positive_cents(
                    row, "proposed_premium_cents", row_number
                ),
            )
        )
        seen_policy_ids.add(policy_id)

    if not records:
        raise DataValidationError("The fictional policy dataset contains no records.")
    return tuple(records)


def load_fictional_policies() -> tuple[PolicyRecord, ...]:
    """Load the one packaged dataset; callers cannot supply filesystem paths."""

    data_file = files("harborlight_mcp").joinpath("data", "fictional_policies.csv")
    with data_file.open("r", encoding="utf-8", newline="") as handle:
        return parse_policy_rows(csv.DictReader(handle))


def find_upcoming_renewals(
    records: Iterable[PolicyRecord],
    days: int,
    *,
    as_of_date: date = DATA_AS_OF_DATE,
) -> UpcomingRenewals:
    """Return renewals from ``as_of_date`` through ``days`` later, inclusive."""

    if isinstance(days, bool) or not isinstance(days, int):
        raise ValueError("days must be an integer.")
    if not 0 <= days <= MAX_RENEWAL_WINDOW_DAYS:
        raise ValueError(f"days must be between 0 and {MAX_RENEWAL_WINDOW_DAYS}.")

    end_date = as_of_date + timedelta(days=days)
    matches: list[Renewal] = []
    for record in sorted(records, key=lambda item: (item.renewal_date, item.policy_id)):
        if as_of_date <= record.renewal_date <= end_date:
            matches.append(
                Renewal(
                    policy_id=record.policy_id,
                    customer_label=record.customer_label,
                    line_of_business=record.line_of_business,
                    renewal_date=record.renewal_date.isoformat(),
                    days_until_renewal=(record.renewal_date - as_of_date).days,
                    current_premium_cents=record.current_premium_cents,
                    proposed_premium_cents=record.proposed_premium_cents,
                )
            )

    return UpcomingRenewals(
        fictional=True,
        data_notice=DATA_NOTICE,
        as_of_date=as_of_date.isoformat(),
        window_days=days,
        renewals=matches,
    )


def list_upcoming_renewals(days: int) -> UpcomingRenewals:
    """List renewals from the fixed fictional data snapshot within ``days``."""

    return find_upcoming_renewals(load_fictional_policies(), days)


def calculate_premium_change(current_cents: int, renewal_cents: int) -> PremiumChange:
    """Compare positive whole-cent premiums and return a rounded percentage change."""

    for name, value in (("current_cents", current_cents), ("renewal_cents", renewal_cents)):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{name} must be an integer number of cents.")
        if value <= 0:
            raise ValueError(f"{name} must be greater than zero.")

    change_cents = renewal_cents - current_cents
    change_percent = Decimal(change_cents) * Decimal(100) / Decimal(current_cents)
    change_percent = change_percent.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    direction: Literal["increase", "decrease", "unchanged"]
    if change_cents > 0:
        direction = "increase"
    elif change_cents < 0:
        direction = "decrease"
    else:
        direction = "unchanged"

    return PremiumChange(
        current_cents=current_cents,
        renewal_cents=renewal_cents,
        change_cents=change_cents,
        change_percent=float(change_percent),
        direction=direction,
    )
