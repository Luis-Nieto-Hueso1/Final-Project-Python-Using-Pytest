# utils/waiter.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Waiter:
    """Utility class for explicit waits."""

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def clickable(self, locator):
        """Wait until element is clickable."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def visible(self, locator):
        """Wait until element is visible."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def invisible(self, locator):
        """Wait until element is invisible."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def url_contains(self, fragment: str):
        """Wait until URL contains fragment."""
        return self.wait.until(EC.url_contains(fragment))