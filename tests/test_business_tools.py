
import os
import sys
import pytest

# Ensure the repository root is on sys.path so business_tools can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

from business_tools import calculate_profit, get_sales_from_csv


def test_calculate_profit():
    assert calculate_profit(1000, 600) == 400


def test_get_sales_from_csv(tmp_path):
    # copy sample sales_data.csv to a temp directory to avoid modifying repo file
    src = os.path.join(os.path.dirname(__file__), os.pardir, 'sales_data.csv')
    dst = tmp_path / 'sales_data.csv'
    with open(src, 'r') as fsrc, open(dst, 'w') as fdst:
        fdst.write(fsrc.read())
    assert get_sales_from_csv(str(dst)) == 950
