from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class OrderStatus(Enum):
    # CHANGED: values now use UPPER_SNAKE_CASE
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"  # NEW status between confirmed and shipped
    SHIPPED = "SHIPPED"
    IN_TRANSIT = "IN_TRANSIT"  # NEW status between shipped and delivered
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"  # NEW status


@dataclass
class OrderItem:
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return round(self.quantity * self.unit_price, 2)


@dataclass
class Order:
    id: int
    user_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: Optional[datetime] = None
    shipping_address: str = ""

    @property
    def subtotal(self) -> float:
        return round(sum(item.total for item in self.items), 2)

    def calculate_tax(self, tax_rate: float = 0.08) -> float:
        return round(self.subtotal * tax_rate, 2)

    def calculate_shipping(self) -> float:
        if self.subtotal >= 50:
            return 0.0
        return 5.99

    def calculate_total(self, tax_rate: float = 0.08) -> float:
        return round(
            self.subtotal + self.calculate_tax(tax_rate) + self.calculate_shipping(),
            2,
        )

    def can_cancel(self) -> bool:
        return self.status in (
            OrderStatus.PENDING,
            OrderStatus.CONFIRMED,
            OrderStatus.PROCESSING,
        )
