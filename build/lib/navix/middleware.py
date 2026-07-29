"""
Advanced Middleware System for Navix Framework
"""
import asyncio
from typing import Callable, List, Any
from .log import logger

class MiddlewareManager:
    """
    مدیریت صف میدلورها برای پیش‌پردازش پیام‌ها و کنترل دسترسی پیش از رسیدن به هندلر
    """
    def __init__(self):
        self._middlewares: List[Callable] = []
        logger.debug("سیستم MiddlewareManager راه‌اندازی شد.")

    def use(self, middleware: Callable):
        """
        ثبت یک میدلور جدید در زنجیره پردازش
        """
        self._middlewares.append(middleware)
        logger.debug(f"میدلور ثبت شد: {getattr(middleware, '__name__', 'anonymous')}")

    async def dispatch(self, event: Any, handler: Callable):
        """
        اجرای زنجیروار میدلورها پیش از رسیدن به هندلر اصلی
        """
        async def execute_chain(index: int, ev: Any):
            if index < len(self._middlewares):
                middleware = self._middlewares[index]
                # عبور دادن رویداد و تابع next به میدلور
                return await middleware(ev, lambda next_ev=ev: execute_chain(index + 1, next_ev))
            else:
                if asyncio.iscoroutinefunction(handler):
                    return await handler(ev)
                return handler(ev)

        try:
            return await execute_chain(0, event)
        except Exception as e:
            logger.error(f"خطا در اجرای زنجیره میدلورها: {e}", exc_info=True)
            raise
