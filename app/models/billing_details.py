from dataclasses import dataclass

@dataclass(frozen=True)
class BillingDetails:
    """Immutable billing details for checkout."""
    first_name: str
    last_name: str
    address1: str
    address2: str
    city: str
    county: str
    postcode: str
    phone: str