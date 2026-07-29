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
