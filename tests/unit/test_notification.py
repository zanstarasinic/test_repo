import pytest
from src.services.notification import NotificationService, NotificationType


class TestNotificationService:
    def setup_method(self):
        self.service = NotificationService()

    def test_send_order_confirmation(self):
        n = self.service.send_order_confirmation("a@b.com", 123, 99.99)
        assert n.notification_type == NotificationType.ORDER_CONFIRMED
        assert "123" in n.subject
        assert "$99.99" in n.body

    def test_send_shipping_notification(self):
        n = self.service.send_shipping_notification("a@b.com", 123, "TRACK123")
        assert n.notification_type == NotificationType.ORDER_SHIPPED
        assert "TRACK123" in n.body

    def test_send_low_stock_alert(self):
        n = self.service.send_low_stock_alert("admin@co.com", "Widget", 3)
        assert n.notification_type == NotificationType.LOW_STOCK
        assert "Widget" in n.body
        assert "3" in n.body

    def test_get_notifications_for_user(self):
        self.service.send_order_confirmation("a@b.com", 1, 10.0)
        self.service.send_order_confirmation("x@y.com", 2, 20.0)
        self.service.send_shipping_notification("a@b.com", 1, "T1")

        a_notifs = self.service.get_notifications_for("a@b.com")
        assert len(a_notifs) == 2

    def test_notifications_stored(self):
        self.service.send_order_confirmation("a@b.com", 1, 10.0)
        assert len(self.service.sent_notifications) == 1
