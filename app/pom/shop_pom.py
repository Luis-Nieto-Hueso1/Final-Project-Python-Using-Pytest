from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class ShopPOM:
    """Page Object for shop page - element interactions only."""

    def __init__(self, driver):
        self.driver = driver
        self.product_titles = (By.CSS_SELECTOR, "h2.woocommerce-loop-product__title")

    def click_product_by_name(self, product_name: str):
        """Click on product by its name."""
        products = self.driver.find_elements(*self.product_titles)

        for product in products:
            if product.text.strip().lower() == product_name.lower():
                product.click()
                return

        raise NoSuchElementException(f"Product not found: {product_name}")

    def is_product_displayed(self, product_name: str) -> bool:
        """Check if product is displayed on page."""
        products = self.driver.find_elements(*self.product_titles)
        return any(
            p.text.strip().lower() == product_name.lower()
            for p in products
        )