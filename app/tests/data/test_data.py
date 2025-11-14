from dataclasses import dataclass


@dataclass
class TestData:
    """Test data container."""
    username: str
    password: str
    product_name: str
    coupon: str
    first_name: str
    last_name: str
    address: str
    address2: str
    city: str
    state: str
    postcode: str
    phone: str
    expected_discount_percent: int

    def __str__(self):
        return (f"TestData[product={self.product_name}, "
                f"coupon={self.coupon}, "
                f"discount={self.expected_discount_percent}%]")
