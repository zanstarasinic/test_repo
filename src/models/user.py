from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    VENDOR = "vendor"


class AccountStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"


@dataclass
class User:
    id: int
    email: str
    name: str
    role: UserRole = UserRole.CUSTOMER
    status: AccountStatus = AccountStatus.PENDING
    discount_tier: int = 0

    def is_active(self) -> bool:
        return self.status == AccountStatus.ACTIVE

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def get_display_name(self) -> str:
        return f"{self.name} ({self.email})"

    def get_discount_percentage(self) -> float:
        tiers = {0: 0.0, 1: 0.05, 2: 0.10, 3: 0.15}
        return tiers.get(self.discount_tier, 0.0)
