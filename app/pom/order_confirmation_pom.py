from selenium.webdriver.common.by import By


class OrderConfirmationPOM:
    """Page Object for order confirmation page."""

    def __init__(self, driver):
        self.driver = driver
        self.order_number_element = (By.CSS_SELECTOR, ".order > strong")

    def get_order_number(self) -> str:
        """Get order number from confirmation page."""
        return self.driver.find_element(*self.order_number_element).text.strip()

    def is_order_confirmation_displayed(self) -> bool:
        """Check if order confirmation is displayed."""
        try:
            return self.driver.find_element(*self.order_number_element).is_displayed()
        except:
            return False