import pytest
from src.services.inventory import InventoryService
from src.models.product import Product, ProductCategory


class TestInventoryService:
    def setup_method(self):
        self.service = InventoryService()
        self.product = Product(
            id=1, name="Widget", price=29.99,
            category=ProductCategory.ELECTRONICS, stock=50, is_active=True,
            tags=["gadget", "tech"],
        )
        self.service.add_product(self.product)

    def test_get_product(self):
        p = self.service.get_product(1)
        assert p is not None
        assert p.name == "Widget"

    def test_get_product_not_found(self):
        assert self.service.get_product(999) is None

    def test_check_availability_true(self):
        assert self.service.check_availability(1, 10) is True

    def test_check_availability_false_insufficient(self):
        assert self.service.check_availability(1, 100) is False

    def test_check_availability_false_nonexistent(self):
        assert self.service.check_availability(999, 1) is False

    def test_reserve_stock(self):
        assert self.service.reserve_stock(1, 5) is True
        assert self.product.stock == 45

    def test_reserve_stock_insufficient(self):
        assert self.service.reserve_stock(1, 100) is False
        assert self.product.stock == 50  # unchanged

    def test_restock(self):
        new_stock = self.service.restock(1, 20)
        assert new_stock == 70

    def test_restock_nonexistent(self):
        with pytest.raises(ValueError, match="not found"):
            self.service.restock(999, 10)

    def test_get_low_stock_products(self):
        low_stock_product = Product(
            id=2, name="Rare Item", price=99.0,
            category=ProductCategory.BOOKS, stock=3, is_active=True,
        )
        self.service.add_product(low_stock_product)
        low = self.service.get_low_stock_products(threshold=10)
        assert len(low) == 1
        assert low[0].name == "Rare Item"

    def test_search_by_name(self):
        results = self.service.search_products("widget")
        assert len(results) == 1

    def test_search_by_tag(self):
        results = self.service.search_products("tech")
        assert len(results) == 1

    def test_search_no_results(self):
        results = self.service.search_products("nonexistent")
        assert len(results) == 0

    def test_search_excludes_inactive(self):
        inactive = Product(
            id=3, name="Widget Pro", price=49.99,
            category=ProductCategory.ELECTRONICS, stock=10, is_active=False,
        )
        self.service.add_product(inactive)
        results = self.service.search_products("widget")
        assert len(results) == 1  # only active widget
