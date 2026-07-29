"""
Advanced Logging and Debugging System for Navix
"""
import logging
import sys

def setup_logger(name: str = "navix", level: int = logging.INFO) -> logging.Logger:
    """
    تنظیم یک لاگر حرفه‌ای برای ردیابی خطاها و جریان اجرای ربات
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # جلوگیری از اضافه شدن چند هندلر تکراری در صورت فراخوانی مجدد
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # فرمت استاندارد و خوانا برای لاگ‌ها (شامل تاریخ، ساعت، سطح و پیام)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# ایجاد نمونه پیش‌فرض لاگر برای استفاده در سراسر کتابخانه
logger = setup_logger()
