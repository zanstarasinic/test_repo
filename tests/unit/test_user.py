import pytest
from src.models.user import User, UserRole, AccountStatus


class TestUser:
    def test_default_user_is_customer(self):
        user = User(id=1, email="test@example.com", name="Test User")
        assert user.role == UserRole.CUSTOMER

    def test_default_user_is_pending(self):
        user = User(id=1, email="test@example.com", name="Test User")
        assert user.status == AccountStatus.PENDING

    def test_is_active_returns_true_for_active_user(self):
        user = User(id=1, email="a@b.com", name="A", status=AccountStatus.ACTIVE)
        assert user.is_active() is True

    def test_is_active_returns_false_for_pending_user(self):
        user = User(id=1, email="a@b.com", name="A", status=AccountStatus.PENDING)
        assert user.is_active() is False

    def test_is_admin(self):
        user = User(id=1, email="a@b.com", name="Admin", role=UserRole.ADMIN)
        assert user.is_admin() is True

    def test_get_display_name(self):
        user = User(id=1, email="john@example.com", name="John Doe")
        assert user.get_display_name() == "John Doe (john@example.com)"

    def test_discount_tier_0(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=0)
        assert user.get_discount_percentage() == 0.0

    def test_discount_tier_1(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=1)
        assert user.get_discount_percentage() == 0.05

    def test_discount_tier_2(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=2)
        assert user.get_discount_percentage() == 0.10

    def test_discount_tier_3(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=3)
        assert user.get_discount_percentage() == 0.15

    def test_invalid_discount_tier_returns_zero(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=99)
        assert user.get_discount_percentage() == 0.0
