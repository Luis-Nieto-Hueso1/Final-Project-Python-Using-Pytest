from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class CartTotals:
    """Immutable cart monetary totals."""
    subtotal: Decimal
    discount: Decimal
    shipping: Decimal
    total: Decimal
