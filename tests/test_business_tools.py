
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so business_tools can be imported
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from business_tools import (  # noqa: E402
    calculate_profit,
    get_sales_from_csv,
    calculate_commission,
    load_insurance_sales,
    total_commission,
    filter_by_state,
    calculate_total_premium,
    filter_policies_by_state,
)


def test_calculate_profit() -> None:
    assert calculate_profit(1000, 600) == 400


def test_get_sales_from_csv(sales_data_csv: Path) -> None:
    """Verify reading the sales CSV sums correctly."""
    assert get_sales_from_csv(str(sales_data_csv)) == 950


def test_calculate_commission() -> None:
    premiums = [300.0, 700.0, 200.0]
    assert calculate_commission(premiums, rate=0.1) == 120.0


def test_load_insurance_sales_and_total_commission(
    insurance_sales_csv: Path,
) -> None:
    records = load_insurance_sales(str(insurance_sales_csv))
    assert len(records) == 15
    assert total_commission(records) == 2545.0


def test_filter_by_state(insurance_sales_csv: Path) -> None:
    records = load_insurance_sales(str(insurance_sales_csv))
    ca_records = filter_by_state(records, "CA")
    assert len(ca_records) == 4

def test_calculate_total_premium(insurance_sales_csv: Path) -> None:
    records = load_insurance_sales(str(insurance_sales_csv))
    assert calculate_total_premium(records) == 18480.0


def test_filter_policies_by_state(insurance_sales_csv: Path) -> None:
    records = load_insurance_sales(str(insurance_sales_csv))
    ca_records = filter_policies_by_state(records, "CA")
    assert len(ca_records) == 4
