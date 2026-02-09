import pytest
from datetime import datetime
from src.utils.formatters import (
    format_currency,
    format_date,
    format_datetime,
    format_order_summary,
    truncate_text,
)


class TestFormatCurrency:
    def test_basic(self):
        assert format_currency(99.99) == "$99.99"

    def test_large_number(self):
        assert format_currency(1234567.89) == "$1,234,567.89"

    def test_zero(self):
        assert format_currency(0) == "$0.00"


class TestFormatDate:
    def test_format_date(self):
        dt = datetime(2024, 3, 15)
        assert format_date(dt) == "March 15, 2024"


class TestFormatDatetime:
    def test_format_datetime(self):
        dt = datetime(2024, 3, 15, 14, 30)
        assert format_datetime(dt) == "March 15, 2024 at 02:30 PM"


class TestFormatOrderSummary:
    def test_basic_summary(self):
        result = format_order_summary(123, 3, 99.99, "pending")
        assert "Order #123" in result
        assert "3 item(s)" in result
        assert "$99.99" in result
        assert "PENDING" in result


class TestTruncateText:
    def test_short_text_unchanged(self):
        assert truncate_text("hello", 100) == "hello"

    def test_long_text_truncated(self):
        result = truncate_text("a" * 200, 100)
        assert len(result) == 100
        assert result.endswith("...")
