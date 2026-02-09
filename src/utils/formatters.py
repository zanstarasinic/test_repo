from datetime import datetime
from typing import Optional


def format_currency(amount: float) -> str:
    """Format amount as USD currency string."""
    return f"${amount:,.2f}"


def format_date(dt: datetime) -> str:
    """Format datetime as readable string."""
    return dt.strftime("%B %d, %Y")


def format_datetime(dt: datetime) -> str:
    """Format datetime with time."""
    return dt.strftime("%B %d, %Y at %I:%M %p")


def format_order_summary(
    order_id: int,
    items_count: int,
    total: float,
    status: str,
) -> str:
    """Format order as a summary string."""
    return (
        f"Order #{order_id}: {items_count} item(s) | "
        f"Total: {format_currency(total)} | Status: {status.upper()}"
    )


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
