from selenium.webdriver.common.by import By
from typing import List


class MyAccountOrdersPOM:
    """Page Object for My Account Orders page."""

    def __init__(self, driver):
        self.driver = driver
        self.orders_link = (By.LINK_TEXT, "Orders")
        self.order_links = (
            By.CSS_SELECTOR,
            "table.woocommerce-orders-table tbody tr "
            "td.woocommerce-orders-table__cell-order-number a"
        )

    def click_orders_tab(self):
        """Click Orders tab."""
        self.driver.find_element(*self.orders_link).click()

    def get_all_order_numbers(self) -> List[str]:
        """Get all order numbers from orders table."""
        order_elements = self.driver.find_elements(*self.order_links)
        return [
            elem.text.replace("#", "").strip()
            for elem in order_elements
        ]

    def is_order_number_displayed(self, order_number: str) -> bool:
        """Check if specific order number is displayed."""
        return order_number in self.get_all_order_numbers()
