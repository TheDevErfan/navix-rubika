"""
Plugin & Extension Loader System for Navix
"""
import importlib
from pathlib import Path
from .log import logger

class PluginManager:
    """
    مدیریت بارگذاری خودکار پلاگین‌ها و ماژول‌های جداگانه ربات
    """
    def __init__(self, router, plugins_dir: str = "plugins"):
        self.router = router
        self.plugins_dir = plugins_dir
        logger.debug(f"سیستم پلاگین‌ها با پوشه {plugins_dir} راه‌اندازی شد.")

    def load_plugins(self):
        plugins_path = Path(self.plugins_dir)
        if not plugins_path.exists():
            logger.warning(f"پوشه پلاگین‌ها ({self.plugins_dir}) یافت نشد.")
            return

        loaded_count = 0
        for file_path in plugins_path.glob("*.py"):
            if file_path.name.startswith("_"):
                continue
            module_name = f"{self.plugins_dir}.{file_path.stem}"
            try:
                importlib.import_module(module_name)
                loaded_count += 1
                logger.info(f"پلاگین با موفقیت بارگذاری شد: {file_path.stem}")
            except Exception as e:
                logger.error(f"خطا در بارگذاری پلاگین {file_path.stem}: {e}", exc_info=True)
        logger.info(f"مجموعاً {loaded_count} پلاگین بارگذاری شد.")
