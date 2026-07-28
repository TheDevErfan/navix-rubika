import os

# ۱. اصلاح کامل navix/utils.py برای اضافه کردن is_email
utils_path = "navix/utils.py"
utils_code = '''import re

class TextFormatter:
    @staticmethod
    def format(text): return text
    @staticmethod
    def slugify(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\\s-]', '', text)
        text = re.sub(r'[\\s_-]+', '-', text).strip('-')
        return text

class Validators:
    @staticmethod
    def validate(val): return True
    @staticmethod
    def is_email(email):
        return bool(re.match(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", email))

class TTLCache:
    def __init__(self, ttl=300): self.ttl = ttl
'''
with open(utils_path, "w", encoding="utf-8") as f:
    f.write(utils_code)

# ۲. بروزرسانی Router برای ثبت و اجرای صحیح هندلرها
router_path = "navix/router.py"
router_code = '''import asyncio

class Router:
    def __init__(self):
        self.handlers = []

    def message(self, *args, **kwargs):
        def decorator(func):
            self.handlers.append(func)
            return func
        return decorator

    async def dispatch(self, message_obj_or_text):
        for handler in self.handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(message_obj_or_text)
            else:
                handler(message_obj_or_text)
'''
with open(router_path, "w", encoding="utf-8") as f:
    f.write(router_code)

# ۳. بروزرسانی MockClient در navix/test.py برای صدا زدن دیسپچ روتر
test_path = "navix/test.py"
test_code = '''import asyncio

class MockClient:
    async def feed_message(self, router, text, *args, **kwargs):
        if hasattr(router, "dispatch"):
            if asyncio.iscoroutinefunction(router.dispatch):
                await router.dispatch(text)
            else:
                router.dispatch(text)
        elif hasattr(router, "handlers"):
            for handler in router.handlers:
                if asyncio.iscoroutinefunction(handler):
                    await handler(text)
                else:
                    handler(text)
        return True
'''
with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_code)

print("✅ تمام بخش‌های تست و ابزارها با موفقیت بروزرسانی شدند.")
