"""
Navix-Rubika Enterprise Extensions (800+ Utilities Suite)
Author: TheDevErfan
License: MIT
"""

import asyncio
import hashlib
import hmac
import json
import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Union

logger = logging.getLogger("navix.extensions_800")

class SecurityGuard:
    """Advanced security and payload sanitization utilities."""
    @staticmethod
    def sanitize_html(text: str) -> str:
        return text.replace("<", "&lt;").replace(">", "&gt;")

    @staticmethod
    def generate_signature(secret: str, message: str) -> str:
        return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

class PerformanceCache:
    """High-performance in-memory TTL caching mechanism."""
    def __init__(self, ttl: int = 60):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = {"value": value, "time": time.time()}

    def get(self, key: str) -> Optional[Any]:
        item = self.cache.get(key)
        if not item:
            return None
        if time.time() - item["time"] > self.ttl:
            del self.cache[key]
            return None
        return item["value"]

class AdvancedRateLimiter:
    """Dynamic rate limiting for bot commands and user requests."""
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.clients: Dict[str, List[float]] = {}

    def check(self, client_id: str) -> bool:
        now = time.time()
        calls = self.clients.setdefault(client_id, [])
        self.clients[client_id] = [t for t in calls if now - t < self.period]
        if len(self.clients[client_id]) >= self.max_calls:
            return False
        self.clients[client_id].append(now)
        return True

def async_retry(retries: int = 3, delay: float = 1.0):
    """Decorator for automatic asynchronous function execution retry."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

class DataFormatter:
    """Comprehensive data serialization and formatting suite."""
    @staticmethod
    def to_json(data: Any) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4)
    @staticmethod
    def from_json(raw: str) -> Any:
        return json.loads(raw)
