import time
import logging
from typing import Dict, Any, Callable, Optional

logger = logging.getLogger("navix")

class BaseMiddleware:
    async def __call__(self, handler: Callable, event: Any, data: Dict[str, Any]) -> Any:
        return await handler(event, data)

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.users_last_time: Dict[int, float] = {}

    async def __call__(self, handler: Callable, event: Any, data: Dict[str, Any]) -> Any:
        user_id = getattr(event, "sender_id", None)
        if user_id:
            now = time.time()
            last_time = self.users_last_time.get(user_id, 0)
            if now - last_time < self.rate_limit:
                if hasattr(event, "reply"):
                    await event.reply("لطفاً آرام‌تر پیام دهید! درخواست شما بیش از حد سریع است.")
                return None
            self.users_last_time[user_id] = now
        return await handler(event, data)

class RedisThrottlingMiddleware(BaseMiddleware):
    """Enterprise distributed rate-limiter using Redis backend for multi-server clusters."""
    def __init__(self, redis_client: Any, rate_limit_seconds: float = 1.0):
        self.redis = redis_client
        self.rate_limit = rate_limit_seconds

    async def __call__(self, handler: Callable, event: Any, data: Dict[str, Any]) -> Any:
        user_id = getattr(event, "sender_id", None)
        if user_id:
            key = f"navix:throttle:{user_id}"
            exists = await self.redis.get(key)
            if exists:
                if hasattr(event, "reply"):
                    await event.reply("درخواست‌های شما بیش از حد سریع است. لطفاً کمی صبر کنید.")
                return None
            await self.redis.setex(key, int(self.rate_limit) or 1, "1")
        return await handler(event, data)

class ORMSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory: Callable):
        self.session_factory = session_factory

    async def __call__(self, handler: Callable, event: Any, data: Dict[str, Any]) -> Any:
        session = self.session_factory()
        data["db_session"] = session
        try:
            result = await handler(event, data)
            if hasattr(session, "commit"):
                session.commit()
            return result
        except Exception as e:
            if hasattr(session, "rollback"):
                session.rollback()
            raise e
        finally:
            if hasattr(session, "close"):
                session.close()
