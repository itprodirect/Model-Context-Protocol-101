
import os
import sys
import pytest

# Ensure the repository root is on sys.path so business_tools can be imported
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from business_tools import calculate_profit, get_sales_from_csv, calculate_commission


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
