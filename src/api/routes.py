"""
Simulated API route handlers — v2 response format.
"""
from typing import Dict, Any, Optional, List
from src.models.user import User, UserRole, AccountStatus
from src.models.product import Product, ProductCategory
from src.services.pricing import PricingService
from src.services.inventory import InventoryService


def _success(data: Any, meta: Optional[Dict] = None) -> Dict[str, Any]:
    """Standard success envelope."""
    resp = {"success": True, "data": data}
    if meta:
        resp["meta"] = meta
    return resp


def _error(code: int, message: str, details: Optional[Dict] = None) -> Dict[str, Any]:
    """Standard error envelope."""
    resp = {"success": False, "error": {"code": code, "message": message}}
    if details:
        resp["error"]["details"] = details
    return resp


def get_product_detail(product_id: int, inventory: InventoryService) -> Dict[str, Any]:
    """GET /api/v2/products/{id}"""
    product = inventory.get_product(product_id)
    if not product:
        return _error(404, "Product not found", {"product_id": product_id})

    return _success({
        "id": product.id,
        "name": product.name,
        "pricing": {
            "amount": product.price,
            "currency": "USD",
        },
        "category": product.category.value,
        "availability": {
            "in_stock": product.is_in_stock(),
            "quantity": product.stock,
        },
    })


def search_products(query: str, inventory: InventoryService) -> Dict[str, Any]:
    """GET /api/v2/products/search?q={query}"""
    if not query or len(query) < 2:
        return _error(400, "Query must be at least 2 characters")

    results = inventory.search_products(query)
    return _success(
        [{"id": p.id, "name": p.name, "price": p.price} for p in results],
        meta={"total_count": len(results), "query": query},
    )


def calculate_cart(
    items: list, inventory: InventoryService, user: Optional[User] = None
) -> Dict[str, Any]:
    """POST /api/v2/cart/calculate"""
    pricing = PricingService()
    cart_items = []

    for item in items:
        product = inventory.get_product(item["product_id"])
        if not product:
            return _error(400, f"Product {item['product_id']} not found")
        if not inventory.check_availability(product.id, item["quantity"]):
            return _error(400, f"Insufficient stock for {product.name}")
        cart_items.append((product, item["quantity"]))

    result = pricing.calculate_cart_total(cart_items, user)
    return _success(result)
