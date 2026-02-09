from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"


@dataclass
class Product:
    id: int
    name: str
    price: float
    category: ProductCategory
    stock: int = 0
    is_active: bool = True
    tags: List[str] = field(default_factory=list)

    def is_in_stock(self) -> bool:
        return self.stock > 0 and self.is_active

    def apply_discount(self, percentage: float) -> float:
        """Returns discounted price."""
        if percentage < 0 or percentage > 1:
            raise ValueError("Discount must be between 0 and 1")
        return round(self.price * (1 - percentage), 2)

    def reduce_stock(self, quantity: int) -> int:
        """Reduces stock by quantity, returns remaining stock."""
        if quantity > self.stock:
            raise ValueError(f"Not enough stock. Available: {self.stock}")
        self.stock -= quantity
        return self.stock
