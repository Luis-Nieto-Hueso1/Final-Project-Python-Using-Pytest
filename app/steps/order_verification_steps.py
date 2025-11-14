from app.pom.order_confirmation_pom import OrderConfirmationPOM
from app.pom.my_account_orders_pom import MyAccountOrdersPOM
from app.pom.nav_pom import NavPOM
from app.models.order_confirmation import OrderConfirmation


class OrderVerificationSteps:
    """Business workflows for order verification."""

    def __init__(self, driver):
        self.driver = driver
        self.order_confirmation = OrderConfirmationPOM(driver)
        self.my_account_orders = MyAccountOrdersPOM(driver)
        self.nav = NavPOM(driver)

    def capture_order_number(self) -> OrderConfirmation:
        """Capture order number from confirmation page."""
        order_number = self.order_confirmation.get_order_number()
        return OrderConfirmation(order_number=order_number)

    def navigate_to_my_orders(self):
        """Navigate to My Orders page."""
        self.nav.click_my_account()
        self.my_account_orders.click_orders_tab()

    def is_order_in_history(self, order_number: str) -> bool:
        """Check if order appears in order history."""
        return self.my_account_orders.is_order_number_displayed(order_number)

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url