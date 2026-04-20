from typing import Dict, List, Optional
from src.models.product import Product


class InventoryService:
    """Manages product stock — search moved to ProductSearchService."""

    def __init__(self):
        self._products: Dict[int, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.id] = product

    def get_product(self, product_id: int) -> Optional[Product]:
        return self._products.get(product_id)

    def get_all_products(self) -> List[Product]:
        return list(self._products.values())

    def check_availability(self, product_id: int, quantity: int) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        return product.is_in_stock() and product.stock >= quantity

    def reserve_stock(self, product_id: int, quantity: int) -> bool:
        product = self.get_product(product_id)
        if not product or not self.check_availability(product_id, quantity):
            return False
        product.reduce_stock(quantity)
        return True

    def restock(self, product_id: int, quantity: int) -> int:
        product = self.get_product(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")
        product.stock += quantity
        return product.stock

    # REMOVED: get_low_stock_products (moved to ProductSearchService)
    # REMOVED: search_products (moved to ProductSearchService)
