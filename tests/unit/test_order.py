import pytest
from src.models.order import Order, OrderItem, OrderStatus


class TestOrderItem:
    def test_total_calculation(self):
        item = OrderItem(product_id=1, product_name="Widget", quantity=3, unit_price=10.0)
        assert item.total == 30.0

    def test_total_single_item(self):
        item = OrderItem(product_id=1, product_name="Gadget", quantity=1, unit_price=49.99)
        assert item.total == 49.99


class TestOrder:
    def make_order(self, items=None, status=OrderStatus.PENDING):
        if items is None:
            items = [
                OrderItem(product_id=1, product_name="Widget", quantity=2, unit_price=25.0),
                OrderItem(product_id=2, product_name="Gadget", quantity=1, unit_price=15.0),
            ]
        return Order(id=1, user_id=1, items=items, status=status)

    def test_subtotal(self):
        order = self.make_order()
        # 2*25 + 1*15 = 65
        assert order.subtotal == 65.0

    def test_calculate_tax_default(self):
        order = self.make_order()
        # 65 * 0.08 = 5.2
        assert order.calculate_tax() == 5.2

    def test_calculate_tax_custom_rate(self):
        order = self.make_order()
        # 65 * 0.10 = 6.5
        assert order.calculate_tax(0.10) == 6.5

    def test_free_shipping_over_50(self):
        order = self.make_order()  # subtotal=65
        assert order.calculate_shipping() == 0.0

    def test_shipping_under_50(self):
        items = [OrderItem(product_id=1, product_name="X", quantity=1, unit_price=20.0)]
        order = self.make_order(items=items)
        assert order.calculate_shipping() == 5.99

    def test_calculate_total(self):
        order = self.make_order()
        # 65 + 5.2 + 0 = 70.2
        assert order.calculate_total() == 70.2

    def test_calculate_total_with_shipping(self):
        items = [OrderItem(product_id=1, product_name="X", quantity=1, unit_price=20.0)]
        order = self.make_order(items=items)
        # 20 + 1.6 + 5.99 = 27.59
        assert order.calculate_total() == 27.59

    def test_can_cancel_pending(self):
        order = self.make_order(status=OrderStatus.PENDING)
        assert order.can_cancel() is True

    def test_can_cancel_confirmed(self):
        order = self.make_order(status=OrderStatus.CONFIRMED)
        assert order.can_cancel() is True

    def test_cannot_cancel_shipped(self):
        order = self.make_order(status=OrderStatus.SHIPPED)
        assert order.can_cancel() is False

    def test_cannot_cancel_delivered(self):
        order = self.make_order(status=OrderStatus.DELIVERED)
        assert order.can_cancel() is False
