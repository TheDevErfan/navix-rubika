"""
Internationalization (i18n) and Localization System for Navix
"""
from typing import Dict, Any
from .log import logger

class I18n:
    """
    مدیریت چندزبانگی و ترجمه متن‌های ربات
    """
    def __init__(self, default_locale: str = "fa"):
        self.default_locale = default_locale
        self.translations: Dict[str, Dict[str, str]] = {}
        logger.debug(f"سیستم چندزبانگی با زبان پیش‌فرض {default_locale} راه‌اندازی شد.")

    def load_translations(self, locale: str, data: Dict[str, str]):
        """
        بارگذاری دیکشنری ترجمه‌ها برای یک زبان خاص
        """
        self.translations[locale] = data
        logger.debug(f"ترجمه‌های زبان {locale} بارگذاری شد ({len(data)} کلید).")

    def get(self, key: str, locale: str = None, **kwargs) -> str:
        """
        دریافت متن ترجمه شده بر اساس کلید و زبان
        """
        loc = locale or self.default_locale
        text = self.translations.get(loc, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception as e:
                logger.error(f"خطا در قالب‌بندی ترجمه کلید {key}: {e}")
        return text
