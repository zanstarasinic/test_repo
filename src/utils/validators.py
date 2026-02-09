import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format. Returns (is_valid, error_message)."""
    if not email:
        return False, "Email is required"
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength. Returns (is_valid, error_message)."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain a digit"
    return True, ""


def validate_shipping_address(address: str) -> Tuple[bool, str]:
    """Validate shipping address."""
    if not address:
        return False, "Shipping address is required"
    if len(address) < 10:
        return False, "Address seems too short"
    if len(address) > 500:
        return False, "Address is too long"
    return True, ""


def sanitize_input(text: str) -> str:
    """Basic input sanitization."""
    return text.strip().replace("<", "&lt;").replace(">", "&gt;")
