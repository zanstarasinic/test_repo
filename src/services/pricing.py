from typing import List, Optional, Tuple
from src.models.product import Product
from src.models.user import User


class PricingService:
    """Handles all pricing calculations."""

    BULK_DISCOUNT_THRESHOLD = 10
    BULK_DISCOUNT_RATE = 0.05
    MAX_DISCOUNT = 0.30

    def calculate_item_price(
        self, product: Product, quantity: int, user: Optional[User] = None
    ) -> float:
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
    ) -> dict:
        line_totals = []
        for product, qty in items:
            price = self.calculate_item_price(product, qty, user)
            line_totals.append(
                {"product_id": product.id, "quantity": qty, "line_total": price}
            )
        subtotal = sum(lt["line_total"] for lt in line_totals)
        shipping = 0.0 if subtotal >= 75 else 5.99
        tax = round(subtotal * 0.10, 2)
        return {
            "lines": line_totals,
            "subtotal": round(subtotal, 2),
            "shipping": shipping,
            "tax": tax,
            "total": round(subtotal + shipping + tax, 2),
        }
