import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "src" / "cli.py"


def run_cli(args: list[str]) -> str:
    """Run the CLI with the given arguments and return stdout."""
    cmd = [sys.executable, str(CLI), *args]
    result = subprocess.check_output(cmd, text=True)
    return result.strip()


def test_profit_cli():
    assert run_cli(["profit", "100", "40"]) == "60"


def test_commission_cli(tmp_path: Path):
    src = REPO_ROOT / "data" / "insurance_sales.csv"
    dst = tmp_path / "insurance_sales.csv"
    dst.write_text(src.read_text())
    out = run_cli(["commission", str(dst)])
    assert out == "2545.0"


def test_premium_cli(tmp_path: Path):
    src = REPO_ROOT / "data" / "insurance_sales.csv"
    dst = tmp_path / "insurance_sales.csv"
    dst.write_text(src.read_text())
    out = run_cli(["premium", str(dst)])
    assert out == "18480.0"
