from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from decimal import Decimal
from typing import List

from app.models.cart_totals import CartTotals
from app.utils.money_utils import MoneyUtils


class CartPOM:
    """
    Page Object for cart page - element interactions only.

    Responsibilities:
    - Locate elements on cart page
    - Perform single actions (click, type, read)
    - Return data as models

    Does NOT:
    - Contain assertions
    - Include waits (those go in Steps)
    - Implement business workflows
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize Cart POM with WebDriver.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver

        # Define locators as tuples (strategy, value)
        self.subtotal_amount = (By.CSS_SELECTOR, ".cart-subtotal .woocommerce-Price-amount")
        self.discount_amount = (By.CSS_SELECTOR, "tr.cart-discount td")
        self.shipping_amount = (By.CSS_SELECTOR, "tr.shipping .woocommerce-Price-amount")
        self.order_total_amount = (By.CSS_SELECTOR, ".order-total .woocommerce-Price-amount")

        self.coupon_field = (By.ID, "coupon_code")
        self.apply_coupon_button = (By.NAME, "apply_coupon")

        self.remove_buttons = (By.CSS_SELECTOR, "a.remove")
        self.remove_coupon_buttons = (By.CSS_SELECTOR, "a.woocommerce-remove-coupon")
        self.update_cart_button = (By.NAME, "update_cart")


    def enter_coupon_code(self, code: str) -> None:
        """
        Enter coupon code into the coupon field.

        Args:
            code: Coupon code to enter
        """
        element = self.driver.find_element(*self.coupon_field)
        element.clear()
        element.send_keys(code)

    def click_apply_coupon(self) -> None:
        """Click the apply coupon button."""
        self.driver.find_element(*self.apply_coupon_button).click()

    def click_remove_all_coupons(self) -> None:
        """Remove all applied coupons from cart."""
        coupons = self.driver.find_elements(*self.remove_coupon_buttons)
        for coupon in coupons:
            coupon.click()


    def click_remove_all_items(self) -> None:
        """Remove all items from cart."""
        items = self.driver.find_elements(*self.remove_buttons)
        for item in items:
            item.click()

    def click_remove_item(self, index: int = 0) -> None:
        """
        Remove a specific item from cart.

        Args:
            index: Index of item to remove (0-based)
        """
        items = self.driver.find_elements(*self.remove_buttons)
        if 0 <= index < len(items):
            items[index].click()

    def click_update_cart(self) -> None:
        """Click the update cart button."""
        self.driver.find_element(*self.update_cart_button).click()

    def get_totals(self) -> CartTotals:
        """
        Get cart totals as CartTotals model object.

        Returns:
            CartTotals: Model containing subtotal, discount, shipping, and total
        """
        subtotal = MoneyUtils.parse(
            self.driver.find_element(*self.subtotal_amount).text
        )

        # Discount may not be present if no coupon applied
        discount = Decimal('0.00')
        if self.is_discount_displayed():
            discount_text = self.driver.find_element(*self.discount_amount).text
            discount = abs(MoneyUtils.parse(discount_text))  # Make positive

        shipping = MoneyUtils.parse(
            self.driver.find_element(*self.shipping_amount).text
        )

        total = MoneyUtils.parse(
            self.driver.find_element(*self.order_total_amount).text
        )

        return CartTotals(
            subtotal=subtotal,
            discount=discount,
            shipping=shipping,
            total=total
        )

    def get_subtotal_text(self) -> str:
        """Get raw subtotal text from page."""
        return self.driver.find_element(*self.subtotal_amount).text

    def get_discount_text(self) -> str:
        """Get raw discount text from page."""
        return self.driver.find_element(*self.discount_amount).text

    def get_shipping_text(self) -> str:
        """Get raw shipping text from page."""
        return self.driver.find_element(*self.shipping_amount).text

    def get_total_text(self) -> str:
        """Get raw total text from page."""
        return self.driver.find_element(*self.order_total_amount).text



    def is_discount_displayed(self) -> bool:
        """
        Check if discount row is displayed on page.

        Returns:
            bool: True if discount is visible, False otherwise
        """
        try:
            element = self.driver.find_element(*self.discount_amount)
            return element.is_displayed()
        except Exception:
            return False

    def is_cart_empty(self) -> bool:
        """
        Check if cart contains any items.

        Returns:
            bool: True if no items in cart, False otherwise
        """
        items = self.driver.find_elements(*self.remove_buttons)
        return len(items) == 0

    def get_item_count(self) -> int:
        """
        Get number of items currently in cart.

        Returns:
            int: Number of items (based on remove buttons)
        """
        items = self.driver.find_elements(*self.remove_buttons)
        return len(items)

    def has_coupons_applied(self) -> bool:
        """
        Check if any coupons are currently applied.

        Returns:
            bool: True if coupons are applied, False otherwise
        """
        coupons = self.driver.find_elements(*self.remove_coupon_buttons)
        return len(coupons) > 0


    def update_product_quantity(self, product_name: str, quantity: int) -> None:
        """
        Update quantity for a specific product.

        Args:
            product_name: Name of product to update
            quantity: New quantity value

        Note: Implementation depends on your page structure.
        """
        # Example implementation - adjust based on your HTML
        try:
            # Find the row containing the product
            product_row = self.driver.find_element(
                By.XPATH,
                f"//td[@data-title='Product']//a[contains(text(), '{product_name}')]"
                "/ancestor::tr"
            )

            # Find quantity input in that row
            qty_input = product_row.find_element(
                By.CSS_SELECTOR,
                "input.qty"
            )
            qty_input.clear()
            qty_input.send_keys(str(quantity))
        except Exception as e:
            print(f"Could not update quantity for {product_name}: {e}")
