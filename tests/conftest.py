from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"


@pytest.fixture()
def sales_data_csv(tmp_path: Path) -> Path:
    """Return a temporary copy of ``sales_data.csv``."""
    src = DATA_DIR / "sales_data.csv"
    dst = tmp_path / "sales_data.csv"
    dst.write_text(src.read_text())
    return dst


@pytest.fixture()
def insurance_sales_csv(tmp_path: Path) -> Path:
    """Return a temporary copy of ``insurance_sales.csv``."""
    src = DATA_DIR / "insurance_sales.csv"
    dst = tmp_path / "insurance_sales.csv"
    dst.write_text(src.read_text())
    return dst
