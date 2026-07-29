"""Navix Rubika Framework - Exceptions."""

class NavixError(Exception):
    """Base exception for all Navix errors."""
    pass

class ValidationError(NavixError):
    """Raised when data validation fails."""
    pass

class NetworkError(NavixError):
    """Raised when network or API requests fail."""
    pass

class APIError(NavixError):
    """Raised when Rubika API returns an error status."""
    def __init__(self, message: str, status_code: int = 400, data: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.data = data or {}
