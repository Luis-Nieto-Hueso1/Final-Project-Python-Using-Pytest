import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from app.utils.waiter import Waiter
from app.utils.helpers import Helpers


class BaseTest:
    """Base test class with setup and teardown."""

    @pytest.fixture(autouse=True)
    def setup(self, request):
        """Setup browser before each test."""
        # Get browser from command line or default to chrome
        browser = request.config.getoption("--browser", default="chrome")

        if browser.lower() == "firefox":
            self.driver = webdriver.Firefox()
        elif browser.lower() == "edge":
            self.driver = webdriver.Edge()
        else:  # chrome
            options = Options()
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.waiter = Waiter(self.driver, timeout=10)

        # Navigate to site and dismiss notice
        print("=== Starting Test Setup ===")
        self.driver.get(Helpers.LOGIN_URL)
        try:
            dismiss_button = self.driver.find_element(
                By.CSS_SELECTOR,
                ".woocommerce-store-notice__dismiss-link"
            )
            dismiss_button.click()
        except:
            pass  # Notice may not be present

        yield

        # Teardown
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass