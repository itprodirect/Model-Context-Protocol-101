
import os
import sys

# Ensure the repository root is on sys.path so business_tools can be imported
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from business_tools import (  # noqa: E402
    calculate_profit,
    get_sales_from_csv,
    calculate_commission,
    load_insurance_sales,
    total_commission,
    filter_by_state,
)


def test_calculate_profit():
    assert calculate_profit(1000, 600) == 400


def test_get_sales_from_csv(tmp_path):
    # copy sample sales_data.csv to a temp directory to avoid modifying repo file
    src = os.path.join(REPO_ROOT, 'data', 'sales_data.csv')
    dst = tmp_path / 'sales_data.csv'
    with open(src, 'r') as fsrc, open(dst, 'w') as fdst:
        fdst.write(fsrc.read())
    assert get_sales_from_csv(str(dst)) == 950


def test_calculate_commission():
    premiums = [300, 700, 200]
    assert calculate_commission(premiums, rate=0.1) == 120.0


def test_load_insurance_sales_and_total_commission(tmp_path):
    src = os.path.join(REPO_ROOT, "data", "insurance_sales.csv")
    dst = tmp_path / "insurance_sales.csv"
    with open(src, "r") as fsrc, open(dst, "w") as fdst:
        fdst.write(fsrc.read())
    records = load_insurance_sales(str(dst))
    assert len(records) == 15
    assert total_commission(records) == 2545.0


def test_filter_by_state(tmp_path):
    src = os.path.join(REPO_ROOT, "data", "insurance_sales.csv")
    dst = tmp_path / "insurance_sales.csv"
    with open(src, "r") as fsrc, open(dst, "w") as fdst:
        fdst.write(fsrc.read())
    records = load_insurance_sales(str(dst))
    ca_records = filter_by_state(records, "CA")
    assert len(ca_records) == 4
