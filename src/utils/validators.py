import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format. Returns (is_valid, error_message)."""
    if not email:
        return False, "Email address is required"
    if len(email) > 254:
        return False, "Email address is too long"
    # CHANGED: stricter pattern — no consecutive dots, no leading/trailing dots in local part
    pattern = r"^(?!\.)(?!.*\.\.)([a-zA-Z0-9._%+-]+)(?<!\.)@[a-zA-Z0-9]([a-zA-Z0-9.-]*[a-zA-Z0-9])?\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Email address format is invalid"
    return True, ""


def validate_password(password: str) -> Tuple[bool, str]:
    """Validate password strength. Returns (is_valid, error_message)."""
    # CHANGED: minimum length 8 -> 12
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    # CHANGED: now also requires a special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""


def validate_shipping_address(address: str) -> Tuple[bool, str]:
    """Validate shipping address."""
    if not address:
        return False, "Shipping address is required"
    # CHANGED: minimum length 10 -> 20
    if len(address) < 20:
        return False, "Shipping address seems too short"
    if len(address) > 500:
        return False, "Shipping address is too long"
    return True, ""


def sanitize_input(text: str) -> str:
    """Basic input sanitization."""
    # CHANGED: also strip & and "
    return (
        text.strip()
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
