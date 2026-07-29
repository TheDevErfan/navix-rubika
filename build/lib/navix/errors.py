from __future__ import annotations
from typing import Optional

class NavixError(Exception):
    pass

class APIError(NavixError):
    def __init__(self, message: str, status_code: Optional[int] = None, data: Optional[dict] = None):
        super().__init__(f"Rubika API Error: {message} (Code: {status_code})")
        self.status_code = status_code
        self.data = data

class NetworkError(NavixError):
    pass
