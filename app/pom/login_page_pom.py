from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPagePOM:
    """Page Object for login page - element interactions only."""

    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.submit_button = (By.CSS_SELECTOR, "button[name='login']")

    def enter_username(self, username: str):
        """Enter username into field."""
        element = self.driver.find_element(*self.username_field)
        element.clear()
        element.send_keys(username)

    def enter_password(self, password: str):
        """Enter password into field."""
        element = self.driver.find_element(*self.password_field)
        element.clear()
        element.send_keys(password)

    def click_submit(self):
        """Click login submit button."""
        self.driver.find_element(*self.submit_button).click()

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url

