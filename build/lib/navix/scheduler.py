"""
Background Task Scheduler for Navix
"""
import asyncio
from typing import Callable
from .log import logger

class BackgroundScheduler:
    """
    سیستم زمان‌بندی برای اجرای دوره‌ای تسک‌ها در پس‌زمینه
    """
    def __init__(self):
        self._tasks = []
        logger.debug("سیستم زمان‌بندی (BackgroundScheduler) راه‌اندازی شد.")

    def interval(self, seconds: float):
        """
        دکوراتور برای اجرای دوره‌ای یک تابع در بازه‌های زمانی مشخص
        """
        def decorator(func: Callable):
            async def wrapper():
                while True:
                    await asyncio.sleep(seconds)
                    try:
                        if asyncio.iscoroutinefunction(func):
                            await func()
                        else:
                            func()
                    except Exception as e:
                        logger.error(f"خطا در اجرای تسک زمان‌بندی شده {func.__name__}: {e}", exc_info=True)
            
            self._tasks.append(wrapper())
            return func
        return decorator

    async def start(self):
        """
        شروع تمام تسک‌های پس‌زمینه
        """
        if self._tasks:
            logger.info("تسک‌های زمان‌بندی شده پس‌زمینه روشن شدند.")
            await asyncio.gather(*self._tasks)
