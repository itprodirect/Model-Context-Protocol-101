import os
import subprocess
import sys
from pathlib import Path

import pytest

MODULES = ("mcp101.cli", "cli")


def run_cli(module: str, args: list[str]) -> str:
    """Run the CLI module with the given arguments and return stdout."""
    cmd = [sys.executable, "-m", module, *args]
    env = os.environ.copy()
    src_dir = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = os.pathsep.join(
        [str(src_dir), env.get("PYTHONPATH", "")]
    ).rstrip(os.pathsep)
    result = subprocess.check_output(cmd, text=True, env=env)
    return result.strip()


@pytest.mark.parametrize("module", MODULES)
def test_profit_cli(module: str) -> None:
    assert run_cli(module, ["profit", "100", "40"]) == "60"


@pytest.mark.parametrize("module", MODULES)
def test_commission_cli(module: str, insurance_sales_csv: Path) -> None:
    out = run_cli(module, ["commission", str(insurance_sales_csv)])
    assert out == "2545.0"


@pytest.mark.parametrize("module", MODULES)
def test_premium_cli(module: str, insurance_sales_csv: Path) -> None:
    out = run_cli(module, ["premium", str(insurance_sales_csv)])
    assert out == "18480.0"
