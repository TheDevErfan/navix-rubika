"""
Configuration Manager for Navix
"""
import os
from .exceptions import ValidationError
from .log import logger

class Config:
    """
    مدیریت پیکربندی و متغیرهای محیطی ربات
    """
    def __init__(self, token: str = None, api_url: str = None):
        self.token = token or os.getenv("NAVIX_BOT_TOKEN")
        self.api_url = api_url or os.getenv("NAVIX_API_URL", "https://api.rubika.ir/v3/")
        
        if not self.token:
            logger.error("توکن ربات در تنظیمات یافت نشد!")
            raise ValidationError("توکن ربات باید از طریق پارامتر یا متغیر محیطی NAVIX_BOT_TOKEN تنظیم شود.")
        
        logger.debug("پیکربندی کلاینت با موفقیت بارگذاری شد.")
