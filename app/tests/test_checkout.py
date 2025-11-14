import pytest
from app.tests.BaseTest import BaseTest
from app.models.user_credentials import UserCredentials
from app.models.product_data import ProductData
from app.models.billing_details import BillingDetails
from app.steps.login_steps import LoginSteps
from app.steps.shopping_steps import ShoppingSteps
from app.steps.cart_steps import CartSteps
from app.steps.checkout_steps import CheckoutSteps
from app.steps.order_verification_steps import OrderVerificationSteps


class TestCheckout(BaseTest):
    """Test complete checkout process."""

    def test_should_complete_checkout_and_verify_order_in_history(self):
        """
        GIVEN user is logged in with product in cart
        WHEN user completes checkout process
        THEN order should be confirmed and appear in order history
        """
        # GIVEN - User with product ready for checkout
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Polo")
        billing_details = BillingDetails(
            first_name="Alice",
            last_name="Smith",
            address1="123 Main St",
            address2="Apt 4B",
            city="Birmingham",
            county="West Midlands",
            postcode="B1 1HQ",
            phone="07111222333"
        )

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)
        checkout_steps = CheckoutSteps(self.driver, self.waiter)
        order_steps = OrderVerificationSteps(self.driver)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN - User completes checkout
        shopping_steps.add_product_to_cart(product)
        cart_steps.navigate_to_cart()
        cart_steps.apply_coupon("2idiscount")
        cart_steps.proceed_to_checkout()

        assert "/checkout/" in checkout_steps.get_current_url(), \
            "Should navigate to checkout page"

        checkout_steps.complete_checkout_with_cheque(billing_details)

        # THEN - Order should be confirmed and in history
        order = order_steps.capture_order_number()
        print(f"Order Number: {order.order_number}")

        order_steps.navigate_to_my_orders()
        assert "/my-account/orders/" in order_steps.get_current_url(), \
            "Should navigate to orders page"

        assert order_steps.is_order_in_history(order.order_number), \
            "Order should appear in order history"

        login_steps.logout()
        print("=== Test Completed Successfully ===")

    def test_should_checkout_with_different_product_and_coupon(self):
        """
        GIVEN user is logged in
        WHEN user purchases different product with different coupon
        THEN order should be created successfully
        """
        # GIVEN
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Sunglasses")
        billing_details = BillingDetails(
            first_name="Bob",
            last_name="Johnson",
            address1="456 Oak Ave",
            address2="",
            city="Leeds",
            county="West Yorkshire",
            postcode="LS1 1UR",
            phone="07444555666"
        )

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)
        checkout_steps = CheckoutSteps(self.driver, self.waiter)
        order_steps = OrderVerificationSteps(self.driver)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN
        shopping_steps.add_product_to_cart(product)
        cart_steps.navigate_to_cart()
        cart_steps.apply_coupon("Edgewords")
        cart_steps.proceed_to_checkout()
        checkout_steps.complete_checkout_with_cheque(billing_details)
        checkout_steps.place_order()

        # THEN
        order = order_steps.capture_order_number()
        order_steps.navigate_to_my_orders()

        assert order_steps.is_order_in_history(order.order_number), \
            "Order should appear in order history"

        login_steps.logout()