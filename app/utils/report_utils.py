# utils/report_utils.py
from decimal import Decimal
from app.utils.money_utils  import MoneyUtils


class ReportUtils:
    """Utility for logging test information."""

    @staticmethod
    def log_inputs(username: str, password: str, product_name: str, coupon: str):
        """Log test input parameters."""
        print("=== Test Inputs ===")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Product:  {product_name}")
        print(f"Coupon:   {coupon}")
        print("===================")

    @staticmethod
    def log_totals(title: str, totals):
        """Log cart totals snapshot."""
        print(f"=== {title} ===")
        print(f"Subtotal: {MoneyUtils.fmt(totals.subtotal)}")
        print(f"Discount: {MoneyUtils.fmt(totals.discount)}")
        print(f"Shipping: {MoneyUtils.fmt(totals.shipping)}")
        print(f"Total:    {MoneyUtils.fmt(totals.total)}")
        print("======================")

    @staticmethod
    def log_expectation(expected_discount: Decimal, expected_total: Decimal):
        """Log expected values."""
        print(f"Expected Discount: {MoneyUtils.fmt(expected_discount)}")
        print(f"Expected Total:    {MoneyUtils.fmt(expected_total)}")

