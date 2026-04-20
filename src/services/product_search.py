from typing import Dict, List, Optional
from src.models.product import Product
from src.services.inventory import InventoryService


class ProductSearchService:
    """Handles product search and filtering — extracted from InventoryService."""

    def __init__(self, inventory: InventoryService):
        self._inventory = inventory

    def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with stock below threshold."""
        return [
            p
            for p in self._inventory.get_all_products()
            if p.is_active and p.stock < threshold
        ]

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or tags."""
        query_lower = query.lower()
        results = []
        for product in self._inventory.get_all_products():
            if not product.is_active:
                continue
            if query_lower in product.name.lower():
                results.append(product)
            elif any(query_lower in tag.lower() for tag in product.tags):
                results.append(product)
        return results

    def search_by_category(self, category) -> List[Product]:
        """Search products by category."""
        return [
            p
            for p in self._inventory.get_all_products()
            if p.is_active and p.category == category
        ]

    def get_in_stock_products(self) -> List[Product]:
        """Get all products that are currently in stock."""
        return [
            p
            for p in self._inventory.get_all_products()
            if p.is_in_stock()
        ]
