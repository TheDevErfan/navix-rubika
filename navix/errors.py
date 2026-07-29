from __future__ import annotations
from typing import Optional, Any

class NavixError(Exception):
    """Base exception for all Navix errors."""
    pass

class APIError(NavixError):
    """Raised when the Rubika API returns an error response."""
    def __init__(self, message: str, status_code: Optional[int] = None, data: Optional[Any] = None):
        super().__init__(f"Rubika API Error: {message} (Code: {status_code})")
        self.message = message
        self.status_code = status_code
        self.data = data

class NetworkError(NavixError):
    """Raised when network or HTTP requests fail."""
    pass

class ValidationError(NavixError):
    """Raised when data validation fails."""
    pass
