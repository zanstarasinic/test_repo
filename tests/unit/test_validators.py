import pytest
from src.utils.validators import (
    validate_email,
    validate_password,
    validate_shipping_address,
    sanitize_input,
)


class TestValidateEmail:
    def test_valid_email(self):
        valid, msg = validate_email("user@example.com")
        assert valid is True
        assert msg == ""

    def test_empty_email(self):
        valid, msg = validate_email("")
        assert valid is False
        assert "required" in msg.lower()

    def test_invalid_format(self):
        valid, msg = validate_email("not-an-email")
        assert valid is False
        assert "invalid" in msg.lower()


class TestValidatePassword:
    def test_valid_password(self):
        valid, msg = validate_password("MyPass123")
        assert valid is True

    def test_too_short(self):
        valid, msg = validate_password("Ab1")
        assert valid is False
        assert "8 characters" in msg

    def test_no_uppercase(self):
        valid, msg = validate_password("password123")
        assert valid is False
        assert "uppercase" in msg.lower()

    def test_no_lowercase(self):
        valid, msg = validate_password("PASSWORD123")
        assert valid is False
        assert "lowercase" in msg.lower()

    def test_no_digit(self):
        valid, msg = validate_password("PasswordOnly")
        assert valid is False
        assert "digit" in msg.lower()


class TestValidateShippingAddress:
    def test_valid_address(self):
        valid, msg = validate_shipping_address("123 Main St, City, ST 12345")
        assert valid is True

    def test_empty_address(self):
        valid, msg = validate_shipping_address("")
        assert valid is False

    def test_too_short(self):
        valid, msg = validate_shipping_address("123 Main")
        assert valid is False
        assert "short" in msg.lower()


class TestSanitizeInput:
    def test_strips_whitespace(self):
        assert sanitize_input("  hello  ") == "hello"

    def test_escapes_html(self):
        assert sanitize_input("<script>alert('xss')</script>") == "&lt;script&gt;alert('xss')&lt;/script&gt;"
