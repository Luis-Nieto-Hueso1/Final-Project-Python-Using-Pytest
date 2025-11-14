from dataclasses import dataclass

@dataclass(frozen=True)
class UserCredentials:
    """Immutable user credentials."""
    username: str
    password: str

