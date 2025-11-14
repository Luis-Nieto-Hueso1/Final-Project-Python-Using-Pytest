# Final-Project-Python-Using-Pytest

This is a **Selenium-based test automation framework** for testing a WooCommerce e-commerce application [1](#0-0) . The framework uses **pytest** as the test runner and follows a **three-layer architecture** with clear separation of concerns<cite />.

## Architecture

The framework is organized into three distinct layers<cite />:

### 1. Test Infrastructure Layer
- **BaseTest** (`app/tests/BaseTest.py`): Provides WebDriver initialization with multi-browser support (Chrome, Firefox, Edge) [2](#0-1) 
- **Waiter** utility: Handles explicit waits [3](#0-2) 
- **Helpers**: Stores configuration constants like URLs and credentials [4](#0-3) 

### 2. Business Logic Layer (Steps)
Step classes orchestrate test workflows by composing Page Objects [5](#0-4) :
- `CartSteps`: Cart operations (apply coupons, get totals, clear cart)
- `CheckoutSteps`: Checkout workflows
- `LoginSteps`: Authentication
- `ShoppingSteps`: Product browsing and selection
- `OrderVerificationSteps`: Order confirmation verification

### 3. Page Object Layer (POMs)
POMs encapsulate Selenium interactions and element locators<cite />:
- `CartPOM`: Cart page interactions [6](#0-5) 
- `CheckoutPOM`: Checkout form interactions
- `LoginPagePOM`: Login form
- `NavPOM`: Shared navigation across pages [7](#0-6) 
- `ShopPOM`: Product catalog
- `OrderConfirmationPOM`: Order confirmation page [8](#0-7) 

## Key Features

**Immutable Data Models**: All data is represented using frozen dataclasses (e.g., `CartTotals`, `BillingDetails`, `UserCredentials`) to ensure type safety<cite />.

**Multi-Browser Support**: Run tests on Chrome, Firefox, or Edge using the `--browser` command-line option [9](#0-8) .

**Explicit Wait Strategy**: Waits are handled in the Step layer, not in POMs, for better maintainability [10](#0-9) .

## Test Examples

The framework includes tests for:
- **Discount calculations**: Verifying 25% discount with "2idiscount" coupon and 15% with "Edgewords" coupon [11](#0-10) 
- **Checkout workflows**: Complete purchase flows with different products and billing details [12](#0-11) 

## Running Tests

```bash
pytest --browser=chrome  # Run with Chrome (default)
pytest --browser=firefox # Run with Firefox
pytest --browser=edge    # Run with Edge
```

## Notes

The framework tests against a demo WooCommerce site at `https://www.edgewordstraining.co.uk/demo-site` [1](#0-0) . Test credentials are stored in the `Helpers` class [13](#0-12) . The architecture follows best practices with clear separation between test logic, business workflows, and UI interactions<cite />.

Wiki pages you might want to explore:
- [Architecture (Luis-Nieto-Hueso1/Final-Project-Python-Using-Pytest)](/wiki/Luis-Nieto-Hueso1/Final-Project-Python-Using-Pytest#2)

### Citations

**File:** app/utils/helpers.py (L5-13)
```python
    BASE_URL = "https://www.edgewordstraining.co.uk/demo-site"
    LOGIN_URL = f"{BASE_URL}/my-account/"
    SHOP_URL = f"{BASE_URL}/shop/"
    CART_URL = f"{BASE_URL}/cart/"
    CHECKOUT_URL = f"{BASE_URL}/checkout/"
    ACCOUNT_URL = f"{BASE_URL}/my-account/"

    USERNAME = "luis.hueso@2.com"
    PASSWORD = "luis.hueso"
```

**File:** app/tests/BaseTest.py (L16-16)
```python
        browser = request.config.getoption("--browser", default="chrome")
```

**File:** app/tests/BaseTest.py (L18-24)
```python
        if browser.lower() == "firefox":
            self.driver = webdriver.Firefox()
        elif browser.lower() == "edge":
            self.driver = webdriver.Edge()
        else:  # chrome
            options = Options()
            self.driver = webdriver.Chrome(options=options)
```

**File:** app/tests/BaseTest.py (L28-28)
```python
        self.waiter = Waiter(self.driver, timeout=10)
```

**File:** app/steps/cart_steps.py (L7-14)
```python
class CartSteps:
    """Business workflows for cart operations."""

    def __init__(self, driver, waiter):
        self.driver = driver
        self.waiter = waiter
        self.cart = CartPOM(driver)
        self.nav = NavPOM(driver)
```

**File:** app/steps/cart_steps.py (L25-25)
```python
        self.waiter.clickable((By.CSS_SELECTOR, "tr.cart-discount td"))
```

**File:** app/pom/order_confirmation_pom.py (L4-13)
```python
class OrderConfirmationPOM:
    """Page Object for order confirmation page."""

    def __init__(self, driver):
        self.driver = driver
        self.order_number_element = (By.CSS_SELECTOR, ".order > strong")

    def get_order_number(self) -> str:
        """Get order number from confirmation page."""
        return self.driver.find_element(*self.order_number_element).text.strip()
```

**File:** app/tests/test_discount_calculation.py (L15-47)
```python
    def test_should_apply_25_percent_discount_with_2i_discount_coupon(self):
        """
        GIVEN user is logged in with an empty cart
        WHEN user adds product and applies 2idiscount coupon
        THEN discount should be 25% of subtotal
        """
        # GIVEN - User is logged in with empty cart
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Polo")

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN - User adds product and applies discount
        shopping_steps.add_product_to_cart(product)
        assert "/product/polo" in shopping_steps.get_current_url().lower(), \
            "Should navigate to product page"

        shopping_steps.go_to_cart()
        assert "/cart/" in cart_steps.get_current_url(), \
            "Should navigate to cart page"

        totals_before = cart_steps.get_cart_totals()
        ReportUtils.log_totals("Totals BEFORE coupon", totals_before)

        cart_steps.apply_coupon("2idiscount")
```

**File:** app/tests/test_checkout.py (L73-111)
```python
    def test_should_checkout_with_different_product_and_coupon(self):
        """
        GIVEN user is logged in
        WHEN user purchases different product with different coupon
        THEN order should be created successfully
        """
        # GIVEN
        user = UserCredentials(
            username="luis.hueso@2.com",
            password="luis.hueso"
        )
        product = ProductData(name="Sunglasses")
        billing_details = BillingDetails(
            first_name="Bob",
            last_name="Johnson",
            address1="456 Oak Ave",
            address2="",
            city="Leeds",
            county="West Yorkshire",
            postcode="LS1 1UR",
            phone="07444555666"
        )

        login_steps = LoginSteps(self.driver, self.waiter)
        shopping_steps = ShoppingSteps(self.driver, self.waiter)
        cart_steps = CartSteps(self.driver, self.waiter)
        checkout_steps = CheckoutSteps(self.driver, self.waiter)
        order_steps = OrderVerificationSteps(self.driver)

        login_steps.login_as(user)
        cart_steps.clear_cart()

        # WHEN
        shopping_steps.add_product_to_cart(product)
        cart_steps.navigate_to_cart()
        cart_steps.apply_coupon("Edgewords")
        cart_steps.proceed_to_checkout()
        checkout_steps.complete_checkout_with_cheque(billing_details)
        checkout_steps.place_order()
```
