from decimal import Decimal
from app.tests.BaseTest import BaseTest
from app.models.user_credentials import UserCredentials
from app.models.product_data import ProductData
from app.steps.login_steps import LoginSteps
from app.steps.shopping_steps import ShoppingSteps
from app.steps.cart_steps import CartSteps
from app.utils.money_utils import MoneyUtils
from app.utils.report_utils import ReportUtils


class TestDiscountCalculation(BaseTest):
    """Test discount calculations with different coupons."""

    def test_should_apply_25_percent_discount_with_2i_discount_coupon(self):
        """
        GIVEN user is logged in with an empty cart
        WHEN user adds product and applies 2idiscount coupon
        THEN discount should be 25% of subtotal
        """
        # GIVEN - User is logged in with empty cart
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Polo")

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN - User adds product and applies discount
        shopping_steps.add_product_to_cart(product)
        assert "/product/polo" in shopping_steps.get_current_url().lower(), \
            "Should navigate to product page"

        shopping_steps.go_to_cart()
        assert "/cart/" in cart_steps.get_current_url(), \
            "Should navigate to cart page"

        totals_before = cart_steps.get_cart_totals()
        ReportUtils.log_totals("Totals BEFORE coupon", totals_before)

        cart_steps.apply_coupon("2idiscount")

        # THEN - Discount should be correctly calculated
        totals_after = cart_steps.get_cart_totals()
        ReportUtils.log_totals("Totals AFTER coupon", totals_after)

        expected_discount = MoneyUtils.pct(totals_after.subtotal, 25)
        expected_total = MoneyUtils.round2(
            totals_after.subtotal - expected_discount + totals_after.shipping
        )

        ReportUtils.log_expectation(expected_discount, expected_total)

        penny = Decimal('0.01')
        discount_diff = abs(totals_after.discount - expected_discount)

        assert discount_diff <= penny, \
            f"Discount should be 25% of subtotal (±1p), got {totals_after.discount}"
        assert cart_steps.is_discount_applied(), "Discount should be applied"

        login_steps.logout()
        print("=== Test Completed Successfully ===")

    def test_should_apply_15_percent_discount_with_edgewords_coupon(self):
        """
        GIVEN user is logged in with an empty cart
        WHEN user adds product and applies Edgewords coupon
        THEN discount should be 15% of subtotal
        """
        # GIVEN
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Sunglasses")

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN
        shopping_steps.add_product_to_cart(product)
        shopping_steps.go_to_cart()

        totals_before = cart_steps.get_cart_totals()
        cart_steps.apply_coupon("Edgewords")

        # THEN
        totals_after = cart_steps.get_cart_totals()
        expected_discount = MoneyUtils.pct(totals_after.subtotal, 15)
        discount_diff = abs(totals_after.discount - expected_discount)
        penny = Decimal('0.01')

        assert discount_diff <= penny, \
            f"Discount should be 15% of subtotal (±1p)"
        assert cart_steps.is_discount_applied(), "Discount should be applied"

        login_steps.logout()