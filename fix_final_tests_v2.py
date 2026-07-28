import os

# ۱. کامل کردن TTLCache با متدهای set و get در navix/utils.py
utils_path = "navix/utils.py"
utils_code = '''import re
import time

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
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.store = {}

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)

    def get(self, key, default=None):
        if key in self.store:
            val, expiry = self.store[key]
            if time.time() < expiry:
                return val
            else:
                del self.store[key]
        return default
'''
with open(utils_path, "w", encoding="utf-8") as f:
    f.write(utils_code)

# ۲. ایجاد MockMessage در navix/test.py تا رشته‌ها به شیء دارای ویژگی .text تبدیل شوند
test_path = "navix/test.py"
test_code = '''import asyncio

class MockMessage:
    def __init__(self, text):
        self.text = text

class MockClient:
    async def feed_message(self, router, text, *args, **kwargs):
        # اگر متن رشته باشد آن را به شیء دارای .text تبدیل می‌کنیم
        msg_obj = text if hasattr(text, "text") else MockMessage(text)

        if hasattr(router, "dispatch"):
            if asyncio.iscoroutinefunction(router.dispatch):
                await router.dispatch(msg_obj)
            else:
                router.dispatch(msg_obj)
        elif hasattr(router, "handlers"):
            for handler in router.handlers:
                if asyncio.iscoroutinefunction(handler):
                    await handler(msg_obj)
                else:
                    handler(msg_obj)
        return True
'''
with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_code)

print("✅ اصلاحات نهایی با موفقیت اعمال شدند.")
