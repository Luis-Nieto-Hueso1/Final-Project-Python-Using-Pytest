from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException


class CheckoutPOM:
    """Page Object for checkout page - element interactions only."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter

        self.first_name_field = (By.ID, "billing_first_name")
        self.last_name_field = (By.ID, "billing_last_name")
        self.address1_field = (By.ID, "billing_address_1")
        self.address2_field = (By.ID, "billing_address_2")
        self.city_field = (By.ID, "billing_city")
        self.county_field = (By.ID, "billing_state")
        self.postcode_field = (By.ID, "billing_postcode")
        self.phone_field = (By.ID, "billing_phone")
        self.cheque_radio = (By.ID, "payment_method_cheque")
        self.cheque_label = (By.CSS_SELECTOR, "li.payment_method_cheque label")
        self.place_order_button = (By.ID, "place_order")

    def enter_first_name(self, first_name: str):
        """Enter first name."""
        element = self.driver.find_element(*self.first_name_field)
        element.clear()
        element.send_keys(first_name)

    def enter_last_name(self, last_name: str):
        """Enter last name."""
        element = self.driver.find_element(*self.last_name_field)
        element.clear()
        element.send_keys(last_name)

    def enter_address1(self, address: str):
        """Enter address line 1."""
        element = self.driver.find_element(*self.address1_field)
        element.clear()
        element.send_keys(address)

    def enter_address2(self, address: str):
        """Enter address line 2."""
        element = self.driver.find_element(*self.address2_field)
        element.clear()
        element.send_keys(address)

    def enter_city(self, city: str):
        """Enter city."""
        element = self.driver.find_element(*self.city_field)
        element.clear()
        element.send_keys(city)

    def enter_county(self, county: str):
        """Enter county."""
        element = self.driver.find_element(*self.county_field)
        element.clear()
        element.send_keys(county)

    def enter_postcode(self, postcode: str):
        """Enter postcode."""
        element = self.driver.find_element(*self.postcode_field)
        element.clear()
        element.send_keys(postcode)

    def enter_phone(self, phone: str):
        """Enter phone number."""
        element = self.driver.find_element(*self.phone_field)
        element.clear()
        element.send_keys(phone)

    def select_cheque_payment(self):
        """Select cheque payment method."""
        self.waiter.clickable(self.cheque_label)

        radio = self.driver.find_element(*self.cheque_radio)
        if radio.is_selected():
            return

        label = self.driver.find_element(*self.cheque_label)

        # Scroll into view
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            label
        )

        try:
            label.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", label)

    def click_place_order(self):
        """Click place order button."""
        self.driver.find_element(*self.place_order_button).click()

    def is_cheque_selected(self) -> bool:
        """Check if cheque payment is selected."""
        return self.driver.find_element(*self.cheque_radio).is_selected()