from selenium.webdriver.common.by import By
from pom.login_page_pom import *
from pom.nav_pom import *
from app.models.user_credentials import *
from app.utils.helpers import *


class LoginSteps:
    """Business workflows for authentication."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter
        self.login_page = LoginPagePOM(driver)
        self.nav = NavPOM(driver)

    def navigate_to_login_page(self):
        """Navigate to login page."""
        self.driver.get(Helpers.LOGIN_URL)

    def login_with(self, credentials: UserCredentials):
        """Perform login with credentials."""
        self.login_page.enter_username(credentials.username)
        self.login_page.enter_password(credentials.password)
        self.login_page.click_submit()
        self.waiter.visible((By.LINK_TEXT, "Log out"))

    def login_as(self, credentials: UserCredentials):
        """Complete login workflow."""
        self.navigate_to_login_page()
        self.login_with(credentials)

    def logout(self):
        """Perform logout."""
        self.nav.click_my_account()
        self.waiter.clickable((By.LINK_TEXT, "Log out"))
        self.nav.click_logout()

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
