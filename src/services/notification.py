from typing import List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class NotificationType(Enum):
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_SHIPPED = "order_shipped"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    LOW_STOCK = "low_stock"
    PRICE_DROP = "price_drop"


class NotificationPriority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Notification:
    recipient_email: str
    subject: str
    body: str
    notification_type: NotificationType
    priority: NotificationPriority = NotificationPriority.NORMAL
    timestamp: Optional[datetime] = None


class NotificationService:
    """Handles sending notifications."""

    def __init__(self):
        self.sent_notifications: List[Notification] = []

    # CHANGED: added required `user_name` param, added `priority` param
    def send_order_confirmation(
        self, email: str, order_id: int, total: float,
        user_name: str, priority: NotificationPriority = NotificationPriority.NORMAL,
    ) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Order #{order_id} Confirmed - Thank you, {user_name}!",
            body=f"Hi {user_name}, your order #{order_id} has been confirmed. Total: ${total:.2f}",
            notification_type=NotificationType.ORDER_CONFIRMED,
            priority=priority,
        )
        self.sent_notifications.append(notification)
        return notification

    # CHANGED: `tracking_number` renamed to `tracking_id`, added `carrier` param
    def send_shipping_notification(
        self, email: str, order_id: int, tracking_id: str,
        carrier: str = "USPS",
    ) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Order #{order_id} Shipped via {carrier}",
            body=f"Your order #{order_id} has shipped via {carrier}. Tracking ID: {tracking_id}",
            notification_type=NotificationType.ORDER_SHIPPED,
        )
        self.sent_notifications.append(notification)
        return notification

    # CHANGED: added `threshold` param, renamed `current_stock` -> `remaining`
    def send_low_stock_alert(
        self, email: str, product_name: str, remaining: int, threshold: int = 10,
    ) -> Notification:
        notification = Notification(
            recipient_email=email,
            subject=f"Low Stock Alert: {product_name}",
            body=f"{product_name} stock ({remaining}) is below threshold ({threshold})",
            notification_type=NotificationType.LOW_STOCK,
            priority=NotificationPriority.HIGH,
        )
        self.sent_notifications.append(notification)
        return notification

    def get_notifications_for(self, email: str) -> List[Notification]:
        return [n for n in self.sent_notifications if n.recipient_email == email]
