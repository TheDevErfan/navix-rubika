"""
Advanced Profiling and Packet Inspection Debugger for Navix
"""
import time
import functools
import json
from .log import logger

def profile_handler(func):
    """
    دکوراتور برای اندازه‌گیری دقیق زمان اجرای هندلرها و شناسایی توابع کند یا مشکل‌دار
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func_name = func.__name__
        logger.debug(f"[PROFILER] شروع اجرای هندلر: {func_name}")
        
        try:
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start_time) * 1000  # میلی‌ثانیه
            logger.debug(f"[PROFILER] هندلر {func_name} با موفقیت در مدت {elapsed:.2f}ms اجرا شد.")
            return result
        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(f"[PROFILER] هندلر {func_name} پس از {elapsed:.2f}ms با خطا مواجه شد: {e}")
            raise
            
    return wrapper

def inspect_packet(direction: str, payload: dict):
    """
    ابزار بازرس بسته‌ها برای نمایش ساختاریافته و زیبای درخواست‌ها و پاسخ‌ها
    """
    try:
        formatted = json.dumps(payload, indent=2, ensure_ascii=False)
        logger.debug(f"\n--- [PACKET INSPECTOR: {direction.upper()}گون] ---\n{formatted}\n--------------------------------------")
    except Exception as e:
        logger.debug(f"[PACKET INSPECTOR] خطا در فرمت‌بندی پکت: {e} | داده خام: {payload}")
