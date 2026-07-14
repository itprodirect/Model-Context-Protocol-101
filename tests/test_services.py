"""Unit tests for data validation, renewal filtering, and premium arithmetic."""

from datetime import date

import pytest

from harborlight_mcp.services import (
    DataValidationError,
    PolicyRecord,
    calculate_premium_change,
    find_upcoming_renewals,
    load_fictional_policies,
    parse_policy_rows,
)


def _record(policy_id: str, renewal_date: date) -> PolicyRecord:
    return PolicyRecord(
        policy_id=policy_id,
        customer_label=f"Fictional Customer {policy_id}",
        line_of_business="Businessowners",
        renewal_date=renewal_date,
        current_premium_cents=100_000,
        proposed_premium_cents=105_000,
    )


def test_renewal_filter_is_inclusive_sorted_and_excludes_past_records() -> None:
    records = (
        _record("FIC-3", date(2026, 7, 31)),
        _record("FIC-PAST", date(2026, 6, 30)),
        _record("FIC-1", date(2026, 7, 1)),
        _record("FIC-LATER", date(2026, 8, 1)),
    )

    result = find_upcoming_renewals(records, 30, as_of_date=date(2026, 7, 1))

    assert [item["policy_id"] for item in result["renewals"]] == ["FIC-1", "FIC-3"]
    assert [item["days_until_renewal"] for item in result["renewals"]] == [0, 30]
    assert result["fictional"] is True


@pytest.mark.parametrize("days", [-1, 366, 2.5, True])
def test_renewal_filter_rejects_invalid_windows(days: object) -> None:
    with pytest.raises(ValueError, match="days must"):
        find_upcoming_renewals((), days)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("current", "renewal", "expected"),
    [
        (120_000, 126_000, (6_000, 5.0, "increase")),
        (80_000, 76_000, (-4_000, -5.0, "decrease")),
        (99_999, 99_999, (0, 0.0, "unchanged")),
        (3, 4, (1, 33.33, "increase")),
    ],
)
def test_calculate_premium_change(
    current: int, renewal: int, expected: tuple[int, float, str]
) -> None:
    result = calculate_premium_change(current, renewal)
    assert (
        result["change_cents"],
        result["change_percent"],
        result["direction"],
    ) == expected


@pytest.mark.parametrize(
    ("current", "renewal"),
    [(0, 100), (-1, 100), (100, 0), (100.5, 101), (True, 100)],
)
def test_calculate_premium_change_rejects_invalid_inputs(
    current: object, renewal: object
) -> None:
    with pytest.raises(ValueError):
        calculate_premium_change(current, renewal)  # type: ignore[arg-type]


def test_packaged_records_are_synthetic_and_loadable() -> None:
    records = load_fictional_policies()
    assert len(records) == 6
    assert all(record.policy_id.startswith("FIC-") for record in records)
    assert all(record.customer_label.startswith("Fictional ") for record in records)


def test_missing_required_field_is_rejected() -> None:
    row = {
        "policy_id": "FIC-1",
        "customer_label": "Fictional Example",
        "line_of_business": "Businessowners",
        "renewal_date": "2026-07-01",
        "current_premium_cents": "10000",
        "proposed_premium_cents": "10500",
        "fictional_record": "true",
    }
    del row["renewal_date"]

    with pytest.raises(DataValidationError, match="renewal_date"):
        parse_policy_rows([row])


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("renewal_date", "July 1", "YYYY-MM-DD"),
        ("current_premium_cents", "ten dollars", "whole cents"),
        ("fictional_record", "false", "must be true"),
        ("policy_id", "REAL-1", "must start"),
        ("customer_label", "Customer One", "must start"),
    ],
)
def test_malformed_or_unlabeled_records_are_rejected(
    field: str, value: str, message: str
) -> None:
    row = {
        "policy_id": "FIC-1",
        "customer_label": "Fictional Example",
        "line_of_business": "Businessowners",
        "renewal_date": "2026-07-01",
        "current_premium_cents": "10000",
        "proposed_premium_cents": "10500",
        "fictional_record": "true",
    }
    row[field] = value

    with pytest.raises(DataValidationError, match=message):
        parse_policy_rows([row])


def test_empty_dataset_is_rejected() -> None:
    with pytest.raises(DataValidationError, match="no records"):
        parse_policy_rows([])
