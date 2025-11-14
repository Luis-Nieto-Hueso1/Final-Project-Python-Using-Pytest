import pytest
from decimal import Decimal
from app.tests.BaseTest import BaseTest
from app.tests.data.test_data_provider import TestDataProvider
from app.models.user_credentials import UserCredentials
from app.models.product_data import ProductData
from app.steps.login_steps import LoginSteps
from app.steps.shopping_steps import ShoppingSteps
from app.steps.cart_steps import CartSteps
from app.utils.money_utils import MoneyUtils
from app.utils.report_utils import ReportUtils


class TestDataDrivenDiscount(BaseTest):
    """Data-driven discount calculation tests."""

    @pytest.mark.parametrize(
        "test_data",
        TestDataProvider.get_discount_test_data(),
        ids=lambda td: f"{td.product_name}-{td.coupon}"
    )
    def test_should_calculate_discount_correctly(self, test_data):
        """
        GIVEN user logs in with test credentials
        WHEN user purchases product with coupon
        THEN discount calculation should match expected percentage
        """
        # GIVEN - User logs in
        user = UserCredentials(
            username=test_data.username,
            password=test_data.password
        )
        product = ProductData(name=test_data.product_name)

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)

        ReportUtils.log_inputs(
            test_data.username,
            test_data.password,
            test_data.product_name,
            test_data.coupon
        )

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN - User purchases product with coupon
        shopping_steps.add_product_to_cart(product)
        assert f"/product/{product.name.lower()}" in shopping_steps.get_current_url(), \
            "Should be on product page"

        shopping_steps.go_to_cart()

        before = cart_steps.get_cart_totals()
        ReportUtils.log_totals("Totals BEFORE coupon", before)

        cart_steps.apply_coupon(test_data.coupon)

        # THEN - Discount should match expected percentage
        after = cart_steps.get_cart_totals()
        ReportUtils.log_totals("Totals AFTER coupon", after)

        expected_discount = MoneyUtils.pct(
            after.subtotal,
            test_data.expected_discount_percent
        )
        expected_total = MoneyUtils.round2(
            after.subtotal - expected_discount + after.shipping
        )

        ReportUtils.log_expectation(expected_discount, expected_total)

        penny = Decimal('0.01')
        discount_diff = abs(after.discount - expected_discount)

        assert discount_diff <= penny, \
            f"Discount should be {test_data.expected_discount_percent}% of subtotal (±1p)"
        assert cart_steps.is_discount_applied(), "Discount should be applied"

        login_steps.logout()
        print("=== Test Completed Successfully ===")