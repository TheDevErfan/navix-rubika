class NavixError(Exception):
    """Base exception for all Navix errors."""
    pass

class RubikaAPIError(NavixError):
    """Raised when Rubika API returns an error status."""
    def __init__(self, message: str, code: int = None):
        super().__init__(f"Rubika API Error [Code {code}]: {message}")
        self.code = code

class NetworkError(NavixError):
    """Raised when a network or connection error occurs."""
    pass

class ValidationError(NavixError):
    """Raised when input data validation fails."""
    pass
