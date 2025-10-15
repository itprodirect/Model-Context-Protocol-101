import os
import subprocess
import sys
from pathlib import Path

MODULE = "mcp101.cli"


def run_cli(args: list[str]) -> str:
    """Run the CLI with the given arguments and return stdout."""
    cmd = [sys.executable, "-m", MODULE, *args]
    env = os.environ.copy()
    src_dir = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(src_dir), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)
    result = subprocess.check_output(cmd, text=True, env=env)
    return result.strip()


def test_profit_cli() -> None:
    assert run_cli(["profit", "100", "40"]) == "60"


def test_commission_cli(insurance_sales_csv: Path) -> None:
    out = run_cli(["commission", str(insurance_sales_csv)])
    assert out == "2545.0"


def test_premium_cli(insurance_sales_csv: Path) -> None:
    out = run_cli(["premium", str(insurance_sales_csv)])
    assert out == "18480.0"
