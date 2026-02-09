from typing import Dict, List, Optional, Tuple
from src.models.product import Product


class InventoryService:
    """Manages product inventory."""

    def __init__(self):
        self._products: Dict[int, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.id] = product

    def get_product(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def check_availability(self, product_id: int, quantity: int) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        return product.is_in_stock() and product.stock >= quantity

    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        """Reserve stock for an order. Returns True if successful."""
        product = self.get_product(product_id)
        if not product or not self.check_availability(product_id, quantity):
            return False
        product.reduce_stock(quantity)
        return True

    def restock(self, product_id: int, quantity: int) -> int:
        """Add stock. Returns new stock level."""
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        product.stock += quantity
        return product.stock

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with stock below threshold."""
        return [
            p
            for p in self._products.values()
            if p.is_active and p.stock < threshold
        ]

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or tags."""
        query_lower = query.lower()
        results = []
        for product in self._products.values():
            if not product.is_active:
                continue
            if query_lower in product.name.lower():
                results.append(product)
            elif any(query_lower in tag.lower() for tag in product.tags):
                results.append(product)
        return results
