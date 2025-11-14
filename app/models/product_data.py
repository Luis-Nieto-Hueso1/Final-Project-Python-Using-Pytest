from dataclasses import dataclass

@dataclass(frozen=True)
class ProductData:
    """Immutable product information."""
    name: str

