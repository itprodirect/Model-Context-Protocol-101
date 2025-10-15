"""Compatibility wrapper for the legacy ``cli`` module.

Historically the project exposed a top-level :mod:`cli` module. The command line
implementation now lives in :mod:`mcp101.cli`, but this shim keeps ``python -m
cli`` and ``from cli import main`` working for existing automation.
"""

from __future__ import annotations

from mcp101.cli import main as main  # re-export for backward compatibility

__all__ = ["main"]

if __name__ == "__main__":
    main()
