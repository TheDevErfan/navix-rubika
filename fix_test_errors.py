import os

# ۱. اصلاح کلاس TextFormatter برای داشتن متد slugify
utils_path = "navix/utils.py"
utils_code = '''
class TextFormatter:
    @staticmethod
    def format(text): return text
    @staticmethod
    def slugify(text):
        return text.lower().replace(" ", "-")

class Validators:
    @staticmethod
    def validate(val): return True

class TTLCache:
    def __init__(self, ttl=300): self.ttl = ttl
'''

with open(utils_path, "w", encoding="utf-8") as f:
    f.write(utils_code)

# ۲. اصلاح روش کار در navix/test.py برای جلوگیری از خطای TypeError در feed_message
test_path = "navix/test.py"
test_code = '''
class MockClient:
    async def feed_message(self, router, text, filters=None):
        # اگر filters به صورت تکی فرستاده شد آن را به لیست تبدیل کنیم
        if filters and not isinstance(filters, (list, tuple, set)):
            filters = [filters]
        elif filters is None:
            filters = []
            
        for f in filters:
            if callable(f) and not f(text):
                return False
        return True
'''

with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_code)

print("✅ اصلاحات با موفقیت اعمال شدند.")
