import pytest
from src.services.pricing import PricingService
from src.models.product import Product, ProductCategory
from src.models.user import User, UserRole, AccountStatus


class TestPricingService:
    def setup_method(self):
        self.service = PricingService()
        self.product = Product(
            id=1, name="Widget", price=100.0,
            category=ProductCategory.ELECTRONICS, stock=100,
        )

    def test_basic_price_no_discounts(self):
        price = self.service.calculate_item_price(self.product, 1)
        assert price == 100.0

    def test_quantity_multiplied(self):
        price = self.service.calculate_item_price(self.product, 3)
        assert price == 300.0

    def test_user_tier_discount(self):
        user = User(id=1, email="a@b.com", name="A", discount_tier=2)
        price = self.service.calculate_item_price(self.product, 1, user)
        # 10% discount -> 90.0
        assert price == 90.0

    def test_bulk_discount(self):
        price = self.service.calculate_item_price(self.product, 5)
        # 5 items at $100 = $500, 10% bulk = $450
        assert price == 450.0

    def test_combined_discount_capped(self):
        # tier 3 (15%) + bulk (10%) = 25%, under cap of 30%
        user = User(id=1, email="a@b.com", name="A", discount_tier=3)
        price = self.service.calculate_item_price(self.product, 5, user)
        # 500 * (1 - 0.25) = 375
        assert price == 375.0

    def test_cart_total_basic(self):
        p1 = Product(id=1, name="A", price=30.0, category=ProductCategory.ELECTRONICS, stock=10)
        p2 = Product(id=2, name="B", price=20.0, category=ProductCategory.CLOTHING, stock=10)
        result = self.service.calculate_cart_total([(p1, 1), (p2, 1)])

        assert result["subtotal"] == 50.0
        assert result["shipping"] == 0.0  # exactly $50 = free shipping
        assert result["tax"] == 4.0  # 50 * 0.08
        assert result["total"] == 54.0

    def test_cart_total_with_shipping(self):
        p1 = Product(id=1, name="A", price=10.0, category=ProductCategory.BOOKS, stock=10)
        result = self.service.calculate_cart_total([(p1, 1)])

        assert result["subtotal"] == 10.0
        assert result["shipping"] == 5.99
        assert result["tax"] == 0.8
        assert result["total"] == 16.79
