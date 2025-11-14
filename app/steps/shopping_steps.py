# steps/shopping_steps.py
from selenium.webdriver.common.by import By
from app.pom.shop_pom import ShopPOM
from app.pom.nav_pom import NavPOM
from app.models.product_data import ProductData


class ShoppingSteps:
    """Business workflows for shopping."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter
        self.shop = ShopPOM(driver)
        self.nav = NavPOM(driver)

    def browse_to_shop(self):
        """Navigate to shop page."""
        self.nav.click_shop()

    def select_product(self, product: ProductData):
        """Select product by name."""
        self.shop.click_product_by_name(product.name)

    def add_current_product_to_cart(self):
        """Add currently viewed product to cart."""
        self.nav.click_add_to_cart()
        self.waiter.clickable((By.LINK_TEXT, "View cart"))

    def add_product_to_cart(self, product: ProductData):
        """Complete workflow to add product to cart."""
        self.browse_to_shop()
        self.select_product(product)
        self.add_current_product_to_cart()

    def view_cart(self):
        """Navigate to view cart."""
        self.nav.click_view_cart()

    def go_to_cart(self):
        """Navigate to cart and wait for page load."""
        self.nav.click_view_cart()
        self.waiter.url_contains("/cart/")

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url

    def is_product_available(self, product_name: str) -> bool:
        """Check if product is available."""
        return self.shop.is_product_displayed(product_name)
