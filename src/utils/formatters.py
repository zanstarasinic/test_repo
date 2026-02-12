from datetime import datetime
from typing import Optional


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency string. CHANGED: added currency param, new format."""
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, currency + " ")
    # CHANGED: negative amounts shown with parentheses
    if amount < 0:
        return f"({symbol}{abs(amount):,.2f})"
    return f"{symbol}{amount:,.2f}"


def format_date(dt: datetime) -> str:
    """Format datetime as readable string. CHANGED: ISO-like format."""
    return dt.strftime("%Y-%m-%d")


def format_datetime(dt: datetime) -> str:
    """Format datetime with time. CHANGED: 24-hour format."""
    return dt.strftime("%Y-%m-%d %H:%M")


def format_order_summary(
    order_id: int,
    items_count: int,
    total: float,
    status: str,
    currency: str = "USD",
) -> str:
    """Format order as a summary string."""
    return (
        f"Order #{order_id} — {items_count} item(s) — "
        f"Total: {format_currency(total, currency)} — Status: {status.capitalize()}"
    )


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis. CHANGED: default max_length 100 -> 50."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
