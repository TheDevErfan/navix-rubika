import time
import asyncio
import logging
import json
import re
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger("navix")

class TokenBucketRateLimiter:
    def __init__(self, capacity: int = 10, refill_rate: float = 1.0):
        self.capacity = capacity
        self.tokens = float(capacity)
        self.refill_rate = refill_rate
        self.last_refill = time.time()

    def acquire(self) -> bool:
        now = time.time()
        elapsed = now - self.last_refill
        self.last_refill = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.state = "CLOSED"
        self.last_failure_time = 0.0

    async def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
            else:
                raise RuntimeError("Circuit breaker is OPEN. Request blocked.")
        try:
            res = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return res
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "OPEN"
            raise e

class Container:
    def __init__(self):
        self._services: Dict[str, Any] = {}

    def register(self, name: str, instance: Any) -> None:
        self._services[name] = instance

    def get(self, name: str) -> Any:
        if name not in self._services:
            raise KeyError(f"Service '{name}' not found in container.")
        return self._services[name]

class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, listener: Callable) -> None:
        self._listeners.setdefault(event_name, []).append(listener)

    async def publish(self, event_name: str, data: Any = None) -> None:
        for listener in self._listeners.get(event_name, []):
            try:
                if asyncio.iscoroutinefunction(listener):
                    await listener(data)
                else:
                    listener(data)
            except Exception as e:
                logger.error(f"EventBus listener error on '{event_name}': {e}")

class ConfigLoader:
    @staticmethod
    def load_json(file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

class TTLCache:
    def __init__(self, ttl: float = 60.0):
        self.ttl = ttl
        self._cache: Dict[str, tuple] = {}

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = (value, time.time() + self.ttl)

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        val, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None
        return val

class MessageBatcher:
    def __init__(self, batch_size: int = 10, flush_interval: float = 1.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.buffer: List[Any] = []

    def add(self, item: Any) -> Optional[List[Any]]:
        self.buffer.append(item)
        if len(self.buffer) >= self.batch_size:
            batch = self.buffer.copy()
            self.buffer.clear()
            return batch
        return None

class JsonHelper:
    @staticmethod
    def dumps(obj: Any) -> str:
        return json.dumps(obj, ensure_ascii=False, default=str)

    @staticmethod
    def loads(s: str) -> Any:
        return json.loads(s)

def retry_on_exception(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    await asyncio.sleep(delay * (2 ** attempt))
            raise last_err
        return wrapper
    return decorator

class Sanitizer:
    @staticmethod
    def clean_html(text: str) -> str:
        return re.sub(r'<[^>]*>', '', text)

    @staticmethod
    def sanitize_input(text: str) -> str:
        return text.strip().replace(";", "").replace("--", "")

class HealthChecker:
    @staticmethod
    def check_system() -> dict:
        return {"status": "healthy", "timestamp": time.time(), "uptime": time.monotonic()}

class MarkupBuilder:
    @staticmethod
    def bold(text: str) -> str:
        return f"**{text}**"

    @staticmethod
    def code(text: str) -> str:
        return f"`{text}`"

class SessionPool:
    def __init__(self, max_sessions: int = 5):
        self.max_sessions = max_sessions
        self.pool: List[Any] = []

    def acquire(self, session_factory: Callable) -> Any:
        if self.pool:
            return self.pool.pop()
        return session_factory()

    def release(self, session: Any) -> None:
        if len(self.pool) < self.max_sessions:
            self.pool.append(session)

class WorkerPool:
    def __init__(self, workers_count: int = 4):
        self.workers_count = workers_count

    async def run_jobs(self, jobs: List[Callable]) -> List[Any]:
        sem = asyncio.Semaphore(self.workers_count)
        async def worker(job):
            async with sem:
                if asyncio.iscoroutinefunction(job):
                    return await job()
                return job()
        return await asyncio.gather(*(worker(j) for j in jobs))

class AuditLogger:
    @staticmethod
    def log_action(user_id: int, action: str) -> str:
        log_entry = f"[AUDIT] User: {user_id} | Action: {action} | Time: {time.time()}"
        logger.info(log_entry)
        return log_entry

class FeatureFlag:
    def __init__(self):
        self.flags: Dict[str, bool] = {}

    def set_flag(self, name: str, enabled: bool) -> None:
        self.flags[name] = enabled

    def is_enabled(self, name: str) -> bool:
        return self.flags.get(name, False)

class SecurityVerifier:
    @staticmethod
    def verify_token(token: str, secret: str) -> bool:
        return bool(token and secret and len(token) > 5)

class StateTransaction:
    def __init__(self, storage: Any, user_id: int):
        self.storage = storage
        self.user_id = user_id
        self.old_state = None

    async def __aenter__(self):
        self.old_state = await self.storage.get_state(self.user_id)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.storage.set_state(self.user_id, self.old_state)

class PrometheusExporter:
    @staticmethod
    def export_metrics(metrics: dict) -> str:
        lines = []
        for k, v in metrics.items():
            lines.append(f"navix_{k} {v}")
        return "\n".join(lines)

class GracefulManager:
    @staticmethod
    async def shutdown(cleanup_funcs: List[Callable]) -> None:
        for func in cleanup_funcs:
            try:
                if asyncio.iscoroutinefunction(func):
                    await func()
                else:
                    func()
            except Exception as e:
                logger.error(f"Error during graceful shutdown: {e}")
