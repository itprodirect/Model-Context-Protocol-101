"""Compatibility wrapper for the legacy ``cli`` module."""

from __future__ import annotations

from mcp101.cli import main as main

__all__ = ["main"]


if __name__ == "__main__":
    main()
