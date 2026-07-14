"""MCP tool registration and stdio server entry point."""

from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from . import services

mcp = FastMCP(
    name="Harborlight Insurance Agency",
    instructions=(
        "Read-only tutorial tools over synthetic records for the fictional "
        "Harborlight Insurance Agency."
    ),
    log_level="ERROR",
)


@mcp.tool()
def list_upcoming_renewals(
    days: Annotated[
        int,
        Field(strict=True, ge=0, le=services.MAX_RENEWAL_WINDOW_DAYS),
    ],
) -> services.UpcomingRenewals:
    """List fictional policy renewals in the next 0-365 days.

    The window begins at the dataset's documented snapshot date (2026-07-01),
    not the computer's current date, so tutorial output remains deterministic.
    """

    return services.list_upcoming_renewals(days)


@mcp.tool()
def calculate_premium_change(
    current_cents: Annotated[
        int,
        Field(strict=True, gt=0),
    ],
    renewal_cents: Annotated[
        int,
        Field(strict=True, gt=0),
    ],
) -> services.PremiumChange:
    """Calculate the amount, percentage, and direction of a proposed premium change.

    Both inputs are positive whole cents. This arithmetic helper does not provide
    insurance advice or make underwriting, eligibility, or claim decisions.
    """

    return services.calculate_premium_change(current_cents, renewal_cents)


def main() -> None:
    """Run the MCP server over stdio without ordinary stdout output."""

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
