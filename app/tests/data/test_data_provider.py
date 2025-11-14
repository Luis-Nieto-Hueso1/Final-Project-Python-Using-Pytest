from app.tests.data.test_data import TestData
from typing import List


class TestDataProvider:
    """Provider for test data sets."""

    @staticmethod
    def get_discount_test_data() -> List[TestData]:
        """Get test data for discount tests."""
        return [
            TestData(
                username="luis.hueso@2.com",
                password="luis.hueso",
                product_name="Polo",
                coupon="2idiscount",
                first_name="Luis",
                last_name="Hueso",
                address="Edgewords",
                address2="2itesting",
                city="London",
                state="Camden",
                postcode="SE10 9LS",
                phone="07956987456",
                expected_discount_percent=25
            ),
            TestData(
                username="luis.hueso@2.com",
                password="luis.hueso",
                product_name="Sunglasses",
                coupon="Edgewords",
                first_name="John",
                last_name="Doe",
                address="Test Street",
                address2="Suite 100",
                city="Manchester",
                state="Greater Manchester",
                postcode="M1 1AA",
                phone="07123456789",
                expected_discount_percent=15
            )
        ]

    @staticmethod
    def get_checkout_test_data() -> List[TestData]:
        """Get test data for checkout tests."""
        return [
            TestData(
                username="luis.hueso@2.com",
                password="luis.hueso",
                product_name="Polo",
                coupon="2idiscount",
                first_name="Alice",
                last_name="Smith",
                address="123 Main St",
                address2="Apt 4B",
                city="Birmingham",
                state="West Midlands",
                postcode="B1 1HQ",
                phone="07111222333",
                expected_discount_percent=25
            ),
            TestData(
                username="luis.hueso@2.com",
                password="luis.hueso",
                product_name="Sunglasses",
                coupon="Edgewords",
                first_name="Bob",
                last_name="Johnson",
                address="456 Oak Ave",
                address2="",
                city="Leeds",
                state="West Yorkshire",
                postcode="LS1 1UR",
                phone="07444555666",
                expected_discount_percent=15
            )
        ]
