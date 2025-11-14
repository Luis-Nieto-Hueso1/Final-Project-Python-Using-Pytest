from selenium.webdriver.common.by import By


class NavPOM:
    """Page Object for navigation elements."""

    def __init__(self, driver):
        self.driver = driver

        self.shop_link = (By.LINK_TEXT, "Shop")
        self.my_account_link = (By.LINK_TEXT, "My account")
        self.view_cart_link = (By.LINK_TEXT, "Cart")
        self.add_to_cart_button = (By.NAME, "add-to-cart")
        self.logout_link = (By.LINK_TEXT, "Log out")
        self.checkout_button = (By.CSS_SELECTOR, "a.checkout-button")

    def click_shop(self):
        """Navigate to shop page."""
        self.driver.find_element(*self.shop_link).click()

    def click_my_account(self):
        """Navigate to my account page."""
        self.driver.find_element(*self.my_account_link).click()

    def click_view_cart(self):
        """Navigate to cart page."""
        self.driver.find_element(*self.view_cart_link).click()

    def click_add_to_cart(self):
        """Click add to cart button."""
        self.driver.find_element(*self.add_to_cart_button).click()

    def click_logout(self):
        """Click logout link."""
        self.driver.find_element(*self.logout_link).click()

    def click_checkout(self):
        """Click checkout button."""
        self.driver.find_element(*self.checkout_button).click()

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url

