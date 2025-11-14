from selenium.webdriver.common.by import By
from app.pom.cart_pom import CartPOM
from app.pom.nav_pom import NavPOM
from app.models.cart_totals import CartTotals


class CartSteps:
    """Business workflows for cart operations."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter
        self.cart = CartPOM(driver)
        self.nav = NavPOM(driver)

    def navigate_to_cart(self):
        """Navigate to cart page."""
        self.nav.click_view_cart()
        self.waiter.url_contains("/cart/")

    def apply_coupon(self, coupon_code: str):
        """Apply coupon code to cart."""
        self.cart.enter_coupon_code(coupon_code)
        self.cart.click_apply_coupon()
        self.waiter.clickable((By.CSS_SELECTOR, "tr.cart-discount td"))

    def clear_cart(self):
        """Clear all items and coupons from cart."""
        self.navigate_to_cart()

        if self.cart.is_cart_empty():
            return

        self.cart.click_remove_all_coupons()
        self.cart.click_remove_all_items()

    def get_cart_totals(self) -> CartTotals:
        """Get current cart totals."""
        return self.cart.get_totals()

    def proceed_to_checkout(self):
        """Proceed to checkout page."""
        self.nav.click_checkout()
        self.waiter.url_contains("/checkout/")

    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.cart.is_cart_empty()

    def get_item_count(self) -> int:
        """Get number of items in cart."""
        return self.cart.get_item_count()

    def is_discount_applied(self) -> bool:
        """Check if discount is applied."""
        return self.cart.is_discount_displayed()