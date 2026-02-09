"""
Simulated API route handlers (no framework dependency).
Each handler takes a dict request and returns a dict response.
"""
from typing import Dict, Any, Optional
from src.models.user import User, UserRole, AccountStatus
from src.models.product import Product, ProductCategory
from src.services.pricing import PricingService
from src.services.inventory import InventoryService


def get_product_detail(product_id: int, inventory: InventoryService) -> Dict[str, Any]:
    """GET /api/products/{id}"""
    product = inventory.get_product(product_id)
    if not product:
        return {"status": 404, "error": "Product not found"}

    return {
        "status": 200,
        "data": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "category": product.category.value,
            "in_stock": product.is_in_stock(),
            "stock_count": product.stock,
        },
    }


def search_products(query: str, inventory: InventoryService) -> Dict[str, Any]:
    """GET /api/products/search?q={query}"""
    if not query or len(query) < 2:
        return {"status": 400, "error": "Query must be at least 2 characters"}

    results = inventory.search_products(query)
    return {
        "status": 200,
        "data": [
            {"id": p.id, "name": p.name, "price": p.price}
            for p in results
        ],
        "count": len(results),
    }


def calculate_cart(
    items: list, inventory: InventoryService, user: Optional[User] = None
) -> Dict[str, Any]:
    """POST /api/cart/calculate"""
    pricing = PricingService()
    cart_items = []

    for item in items:
        product = inventory.get_product(item["product_id"])
        if not product:
            return {"status": 400, "error": f"Product {item['product_id']} not found"}
        if not inventory.check_availability(product.id, item["quantity"]):
            return {"status": 400, "error": f"Insufficient stock for {product.name}"}
        cart_items.append((product, item["quantity"]))

    result = pricing.calculate_cart_total(cart_items, user)
    return {"status": 200, "data": result}
