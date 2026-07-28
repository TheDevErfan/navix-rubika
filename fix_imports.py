import os

init_path = "navix/__init__.py"

# کارهایی که باید انجام دهیم: بازنویسی تمیز و کامل __init__.py برای اکسپورت تمام ابزارهای تست و اصلی
init_content = '''# Navix - Rubika Bot Framework
from navix.client import Client
from navix.router import Router
from navix.filters import Filters
from navix.fsm import MemoryStorage
from navix.test import MockClient

# ابزارهای کمکی در صورت وجود
try:
    from navix.utils import TextFormatter, Validators, TTLCache
except ImportError:
    pass

__version__ = "1.0.0"
__all__ = [
    "Client",
    "Router",
    "Filters",
    "MemoryStorage",
    "MockClient",
]
'''

with open(init_path, "w", encoding="utf-8") as f:
    f.write(init_content)

print("✅ فایل navix/__init__.py با موفقیت بروزرسانی شد و تمام ایمپورت‌های تست اضافه شدند.")
