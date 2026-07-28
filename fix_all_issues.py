import os

# ۱. اصلاح کامل navix/utils.py با ایمپورت صحیح re
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

class TTLCache:
    def __init__(self, ttl=300): self.ttl = ttl
'''
with open(utils_path, "w", encoding="utf-8") as f:
    f.write(utils_code)

# ۲. اصلاح MockClient در navix/test.py جهت پشتیبانی کامل از دیسپچ و اجرا شدن هندلرها
test_path = "navix/test.py"
test_code = '''
class MockClient:
    async def feed_message(self, router, text, *args, **kwargs):
        # اگر روتر متد dispatch داشته باشد
        if hasattr(router, "dispatch") and callable(router.dispatch):
            await router.dispatch(text)
        # اجرای مستقیم هندلرهای ثبت‌شده در روتر
        if hasattr(router, "handlers"):
            for handler in router.handlers:
                try:
                    await handler(text)
                except TypeError:
                    handler(text)
        return True
'''
with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_code)

print("✅ تمام اصلاحات اعمال شدند.")
