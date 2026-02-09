import pytest
from src.models.product import Product, ProductCategory


class TestProduct:
    def make_product(self, **kwargs):
        defaults = {
            "id": 1,
            "name": "Widget",
            "price": 29.99,
            "category": ProductCategory.ELECTRONICS,
            "stock": 100,
            "is_active": True,
        }
        defaults.update(kwargs)
        return Product(**defaults)

    def test_is_in_stock_true(self):
        p = self.make_product(stock=10, is_active=True)
        assert p.is_in_stock() is True

    def test_is_in_stock_false_when_zero(self):
        p = self.make_product(stock=0)
        assert p.is_in_stock() is False

    def test_is_in_stock_false_when_inactive(self):
        p = self.make_product(stock=10, is_active=False)
        assert p.is_in_stock() is False

    def test_apply_discount_10_percent(self):
        p = self.make_product(price=100.0)
        assert p.apply_discount(0.10) == 90.0

    def test_apply_discount_zero(self):
        p = self.make_product(price=100.0)
        assert p.apply_discount(0.0) == 100.0

    def test_apply_discount_invalid_negative(self):
        p = self.make_product(price=100.0)
        with pytest.raises(ValueError):
            p.apply_discount(-0.1)

    def test_apply_discount_invalid_over_one(self):
        p = self.make_product(price=100.0)
        with pytest.raises(ValueError):
            p.apply_discount(1.5)

    def test_reduce_stock(self):
        p = self.make_product(stock=50)
        remaining = p.reduce_stock(10)
        assert remaining == 40
        assert p.stock == 40

    def test_reduce_stock_insufficient(self):
        p = self.make_product(stock=5)
        with pytest.raises(ValueError, match="Not enough stock"):
            p.reduce_stock(10)
