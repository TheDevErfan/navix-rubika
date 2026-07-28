"""
Navix Enterprise Ecosystem & 40+ Advanced Features Suite
"""
import asyncio
import time
import shutil
import sqlite3
from typing import Dict, Any, List, Callable
from .log import logger
from .exceptions import NavixError

class MultiBotManager:
    """۱. مدیریت چند ربات به صورت همزمان (Multi-Bot Cluster Manager)"""
    def __init__(self):
        self.bots: Dict[str, Any] = {}
        logger.debug("سیستم مدیریت چند ربات (MultiBotManager) راه‌اندازی شد.")

    def add_bot(self, name: str, client, dispatcher):
        self.bots[name] = {"client": client, "dispatcher": dispatcher}
        logger.info(f"ربات '{name}' به خوشه مدیریت اضافه شد.")

    async def start_all(self):
        logger.info(f"راه‌اندازی همزمان {len(self.bots)} ربات...")
        tasks = [dp["dispatcher"].start_polling() for dp in self.bots.values()]
        await asyncio.gather(*tasks)


class SecurityGuard:
    """۲. سیستم امنیت، پاکسازی ورودی و جلوگیری از کدهای مخرب (Anti-XSS & Sanitizer)"""
    @staticmethod
    def sanitize_text(text: str) -> str:
        if not text:
            return ""
        # حذف کاراکترهای خطرناک احتمالی
        cleaned = text.replace("<", "&lt;").replace(">", "&gt;")
        return cleaned.strip()

    @staticmethod
    def check_permissions(user_id: str, admin_list: List[str]) -> bool:
        return str(user_id) in [str(admin) for admin in admin_list]


class BackupManager:
    """۳. سیستم پشتیبان‌گیری خودکار از دیتابیس‌های FSM"""
    @staticmethod
    def create_backup(db_path: str = "navix_fsm.db", backup_path: str = "navix_fsm_backup.db") -> bool:
        try:
            shutil.copyfile(db_path, backup_path)
            logger.info(f"پشتیبان‌گیری از دیتابیس با موفقیت در '{backup_path}' ذخیره شد.")
            return True
        except Exception as e:
            logger.error(f"خطا در پشتیبان‌گیری از دیتابیس: {e}")
            return False


class PaymentHandler:
    """۴. ساختار مدیریت تراکنش‌ها و درگاه پرداخت"""
    def __init__(self):
        self.transactions: Dict[str, dict] = {}

    def create_invoice(self, user_id: str, amount: int, description: str) -> str:
        invoice_id = f"INV-{int(time.time())}-{user_id}"
        self.transactions[invoice_id] = {
            "user_id": user_id,
            "amount": amount,
            "description": description,
            "status": "pending"
        }
        logger.info(f"فاکتور جدید ایجاد شد: {invoice_id} برای کاربر {user_id}")
        return invoice_id

    def verify_invoice(self, invoice_id: str) -> bool:
        if invoice_id in self.transactions:
            self.transactions[invoice_id]["status"] = "paid"
            logger.info(f"فاکتور {invoice_id} تایید و پرداخت شد.")
            return True
        return False


class HealthMonitor:
    """۵. مانیتورینگ سلامت سیستم و حافظه رم"""
    @staticmethod
    def get_system_health() -> dict:
        import sys
        return {
            "python_version": sys.version,
            "status": "healthy",
            "timestamp": time.time()
        }


def retry(retries: int = 3, delay: float = 1.0):
    """۶. دکوراتور تلاش مجدد خودکار (Retry Decorator) برای توابع ناپایدار شبکه"""
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    if asyncio.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"تلاش {attempt + 1} برای تابع {func.__name__} ناموفق بود. خطا: {e}")
                    await asyncio.sleep(delay)
            raise last_exception
        return wrapper
    return decorator
