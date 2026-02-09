import pytest
from src.api.routes import get_product_detail, search_products, calculate_cart
from src.services.inventory import InventoryService
from src.models.product import Product, ProductCategory
from src.models.user import User, UserRole, AccountStatus


@pytest.fixture
def inventory():
    svc = InventoryService()
    svc.add_product(Product(
        id=1, name="Laptop", price=999.99,
        category=ProductCategory.ELECTRONICS, stock=10,
        is_active=True, tags=["computer", "tech"],
    ))
    svc.add_product(Product(
        id=2, name="Python Book", price=39.99,
        category=ProductCategory.BOOKS, stock=50,
        is_active=True, tags=["programming", "education"],
    ))
    svc.add_product(Product(
        id=3, name="Vintage Shirt", price=25.0,
        category=ProductCategory.CLOTHING, stock=0,
        is_active=True, tags=["retro"],
    ))
    return svc


class TestGetProductDetail:
    def test_existing_product(self, inventory):
        resp = get_product_detail(1, inventory)
        assert resp["status"] == 200
        assert resp["data"]["name"] == "Laptop"
        assert resp["data"]["price"] == 999.99
        assert resp["data"]["in_stock"] is True

    def test_out_of_stock_product(self, inventory):
        resp = get_product_detail(3, inventory)
        assert resp["status"] == 200
        assert resp["data"]["in_stock"] is False

    def test_nonexistent_product(self, inventory):
        resp = get_product_detail(999, inventory)
        assert resp["status"] == 404


class TestSearchProducts:
    def test_search_by_name(self, inventory):
        resp = search_products("laptop", inventory)
        assert resp["status"] == 200
        assert resp["count"] == 1

    def test_search_by_tag(self, inventory):
        resp = search_products("programming", inventory)
        assert resp["status"] == 200
        assert resp["count"] == 1

    def test_search_short_query(self, inventory):
        resp = search_products("a", inventory)
        assert resp["status"] == 400

    def test_search_no_results(self, inventory):
        resp = search_products("xyz", inventory)
        assert resp["status"] == 200
        assert resp["count"] == 0


class TestCalculateCart:
    def test_basic_cart(self, inventory):
        items = [{"product_id": 2, "quantity": 2}]
        resp = calculate_cart(items, inventory)
        assert resp["status"] == 200
        data = resp["data"]
        assert data["subtotal"] == 79.98
        assert data["shipping"] == 0.0  # over $50

    def test_cart_with_user_discount(self, inventory):
        user = User(id=1, email="a@b.com", name="A", discount_tier=1,
                    status=AccountStatus.ACTIVE)
        items = [{"product_id": 1, "quantity": 1}]
        resp = calculate_cart(items, inventory, user)
        assert resp["status"] == 200
        # 999.99 * 0.95 = 949.99
        assert resp["data"]["subtotal"] == 949.99

    def test_cart_nonexistent_product(self, inventory):
        items = [{"product_id": 999, "quantity": 1}]
        resp = calculate_cart(items, inventory)
        assert resp["status"] == 400

    def test_cart_insufficient_stock(self, inventory):
        items = [{"product_id": 3, "quantity": 1}]  # out of stock
        resp = calculate_cart(items, inventory)
        assert resp["status"] == 400
