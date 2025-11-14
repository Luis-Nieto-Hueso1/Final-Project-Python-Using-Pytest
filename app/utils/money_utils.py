# utils/money_utils.py
from decimal import Decimal, ROUND_HALF_UP
import re


class MoneyUtils:
    """Utility class for monetary calculations."""

    @staticmethod
    def parse(text: str) -> Decimal:
        """Parse strings like '£33.95', '-£4.50', 'Total: £12.00'"""
        if not text:
            return Decimal('0.00')

        # Remove non-numeric characters except decimal point, minus, and comma
        cleaned = re.sub(r'[^0-9.,-]', '', text)
        cleaned = cleaned.replace(',', '.')

        if not cleaned:
            return Decimal('0.00')

        # Get last numeric token
        parts = cleaned.strip().split()
        candidate = parts[-1] if parts else cleaned

        return Decimal(candidate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def pct(base: Decimal, percent: int) -> Decimal:
        """Calculate percentage of base value."""
        return (base * Decimal(percent) / Decimal(100)).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )

    @staticmethod
    def round2(value: Decimal) -> Decimal:
        """Round to 2 decimal places."""
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    @staticmethod
    def fmt(value: Decimal) -> str:
        """Format as '£x.xx' for logging."""
        return f"£{value}"
