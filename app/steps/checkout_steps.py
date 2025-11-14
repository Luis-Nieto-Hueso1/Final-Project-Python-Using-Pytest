from selenium.webdriver.common.by import By
from app.pom.checkout_pom import CheckoutPOM
from app.models.billing_details import BillingDetails


class CheckoutSteps:
    """Business workflows for checkout."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter
        self.checkout = CheckoutPOM(driver, waiter)

    def fill_billing_details(self, details: BillingDetails):
        """Fill all billing details."""
        self.checkout.enter_first_name(details.first_name)
        self.checkout.enter_last_name(details.last_name)
        self.checkout.enter_address1(details.address1)
        self.checkout.enter_address2(details.address2)
        self.checkout.enter_city(details.city)
        self.checkout.enter_county(details.county)
        self.checkout.enter_postcode(details.postcode)
        self.checkout.enter_phone(details.phone)

    def select_cheque_payment(self):
        """Select cheque payment method."""
        self.waiter.clickable(
            (By.CSS_SELECTOR, "li.payment_method_cheque label")
        )
        self.checkout.select_cheque_payment()

    def place_order(self):
        """Place the order."""
        self.waiter.clickable((By.ID, "place_order"))
        self.checkout.click_place_order()
        self.waiter.clickable((By.CSS_SELECTOR, ".order > strong"))

    def complete_checkout_with_cheque(self, details: BillingDetails):
        """Complete entire checkout process with cheque payment."""
        self.fill_billing_details(details)
        self.select_cheque_payment()
    def place_order_(self):
        self.place_order()

    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url

