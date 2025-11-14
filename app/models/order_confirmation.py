# models/order_confirmation.py
from dataclasses import dataclass

@dataclass(frozen=True)
class OrderConfirmation:
    """Immutable order confirmation details."""
    order_number: str

