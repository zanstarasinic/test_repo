from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class NotificationType(Enum):
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    LOW_STOCK = "low_stock"
    PRICE_DROP = "price_drop"


@dataclass
class Notification:
    recipient_email: str
    subject: str
    body: str
    notification_type: NotificationType


class NotificationService:
    """Handles sending notifications."""

    def __init__(self):
        self.sent_notifications: List[Notification] = []

    def send_order_confirmation(self, email: str, order_id: int, total: float) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Order #{order_id} Confirmed",
            body=f"Your order #{order_id} has been confirmed. Total: ${total:.2f}",
            notification_type=NotificationType.ORDER_CONFIRMED,
        )
        self.sent_notifications.append(notification)
        return notification

    def send_shipping_notification(
        self, email: str, order_id: int, tracking_number: str
    ) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Order #{order_id} Shipped",
            body=f"Your order #{order_id} has been shipped. Tracking: {tracking_number}",
            notification_type=NotificationType.ORDER_SHIPPED,
        )
        self.sent_notifications.append(notification)
        return notification

    def send_low_stock_alert(
        self, email: str, product_name: str, current_stock: int
    ) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Low Stock Alert: {product_name}",
            body=f"{product_name} is running low. Current stock: {current_stock}",
            notification_type=NotificationType.LOW_STOCK,
        )
        self.sent_notifications.append(notification)
        return notification

    def get_notifications_for(self, email: str) -> List[Notification]:
        return [n for n in self.sent_notifications if n.recipient_email == email]
