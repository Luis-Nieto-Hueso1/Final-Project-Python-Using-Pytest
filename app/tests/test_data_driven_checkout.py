import pytest
from app.tests.BaseTest import BaseTest
from app.tests.data.test_data_provider import TestDataProvider
from app.models.user_credentials import UserCredentials
from app.models.product_data import ProductData
from app.models.billing_details import BillingDetails
from app.steps.login_steps import LoginSteps
from app.steps.shopping_steps import ShoppingSteps
from app.steps.cart_steps import CartSteps
from app.steps.checkout_steps import CheckoutSteps
from app.steps.order_verification_steps import OrderVerificationSteps
from app.utils.report_utils import ReportUtils


class TestDataDrivenCheckout(BaseTest):
    """Data-driven checkout tests."""

    @pytest.mark.parametrize(
        "test_data",
        TestDataProvider.get_checkout_test_data(),
        ids=lambda td: f"{td.first_name}-{td.coupon}"
    )
    def test_should_complete_checkout_successfully(self, test_data):
        """
        GIVEN authenticated user with product ready for checkout
        WHEN user completes full checkout flow
        THEN order should be created and visible in order history
        """
        # GIVEN - Authenticated user with product
        user = UserCredentials(
            username=test_data.username,
            password=test_data.password
        )
        product = ProductData(name=test_data.product_name)
        billing_details = BillingDetails(
            first_name=test_data.first_name,
            last_name=test_data.last_name,
            address1=test_data.address,
            address2=test_data.address2,
            city=test_data.city,
            county=test_data.state,
            postcode=test_data.postcode,
            phone=test_data.phone
        )

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)
        checkout_steps = CheckoutSteps(self.driver, self.waiter)
        order_steps = OrderVerificationSteps(self.driver)

        ReportUtils.log_inputs(
            test_data.username,
            test_data.password,
            test_data.product_name,
            test_data.coupon
        )

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN - User completes checkout flow
        shopping_steps.add_product_to_cart(product)
        cart_steps.navigate_to_cart()
        cart_steps.apply_coupon(test_data.coupon)

        assert cart_steps.get_item_count() > 0, "Cart should have items"
        assert cart_steps.is_discount_applied(), "Discount should be applied"

        cart_steps.proceed_to_checkout()
        assert "/checkout/" in checkout_steps.get_current_url(), \
            "Should be on checkout page"

        checkout_steps.complete_checkout_with_cheque(billing_details)
        checkout_steps.place_order()

        # THEN - Order should be created and in history
        order = order_steps.capture_order_number()
        print(f"Order Number: {order.order_number}")

        order_steps.navigate_to_my_orders()
        assert "/my-account/orders/" in order_steps.get_current_url(), \
            "Should be on orders page"

        assert order_steps.is_order_in_history(order.order_number), \
            "Order should appear in order history"

        login_steps.logout()
        print("=== Checkout Test Completed Successfully ===")