from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ProductCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"


class InsufficientStockError(Exception):
    """Raised when there isn't enough stock to fulfill a request."""
    def __init__(self, product_name: str, requested: int, available: int):
        self.product_name = product_name
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for '{product_name}': "
            f"requested {requested}, available {available}"
        )


class InvalidDiscountError(Exception):
    """Raised when an invalid discount value is provided."""
    def __init__(self, value: float):
        self.value = value
        super().__init__(f"Invalid discount value: {value}. Must be between 0.0 and 1.0")


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
            # CHANGED: was ValueError, now InvalidDiscountError
            raise InvalidDiscountError(percentage)
        return round(self.price * (1 - percentage), 2)

    def reduce_stock(self, quantity: int) -> int:
        """Reduces stock by quantity, returns remaining stock."""
        if quantity > self.stock:
            # CHANGED: was ValueError, now InsufficientStockError
            raise InsufficientStockError(self.name, quantity, self.stock)
        self.stock -= quantity
        return self.stock
