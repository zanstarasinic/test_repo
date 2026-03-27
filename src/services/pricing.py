from typing import List, Optional, Tuple
from dataclasses import dataclass
from src.models.product import Product
from src.models.user import User


@dataclass
class LineItem:
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    line_total: float


@dataclass
class CartSummary:
    """Structured cart result instead of plain dict."""
    items: List[LineItem]
    subtotal: float
    shipping_cost: float
    tax_amount: float
    total: float
    discount_applied: float = 0.0
    currency: str = "USD"


class PricingService:
    """Handles all pricing calculations."""

    BULK_DISCOUNT_THRESHOLD = 5
    BULK_DISCOUNT_RATE = 0.10
    MAX_DISCOUNT = 0.30

    def calculate_item_price(
        self, product: Product, quantity: int, user: Optional[User] = None
    ) -> float:
        """Calculate price for a line item."""
        base_price = product.price * quantity
        discount = 0.0

        if user:
            discount += user.get_discount_percentage()

        if quantity >= self.BULK_DISCOUNT_THRESHOLD:
            discount += self.BULK_DISCOUNT_RATE

        discount = min(discount, self.MAX_DISCOUNT)

        return round(base_price * (1 - discount), 2)

    def calculate_cart_total(
        self,
        items: List[Tuple[Product, int]],
        user: Optional[User] = None,
    ) -> CartSummary:
        """Calculate full cart breakdown - now returns CartSummary dataclass."""
        line_items = []
        total_discount = 0.0

        for product, qty in items:
            full_price = product.price * qty
            discounted = self.calculate_item_price(product, qty, user)
            total_discount += full_price - discounted
            line_items.append(LineItem(
                product_id=product.id,
                product_name=product.name,
                quantity=qty,
                unit_price=product.price,
                line_total=discounted,
            ))

        subtotal = sum(li.line_total for li in line_items)
        shipping = 0.0 if subtotal >= 50 else 5.99
        tax = round(subtotal * 0.08, 2)

        return CartSummary(
            items=line_items,
            subtotal=round(subtotal, 2),
            shipping_cost=shipping,
            tax_amount=tax,
            total=round(subtotal + shipping + tax, 2),
            discount_applied=round(total_discount, 2),
        )
