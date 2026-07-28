import os

filters_path = "navix/filters.py"

# اگر فایل filters.py وجود داشته باشد یا نداشته باشد، محتوای آن را بررسی و ایمن می کنیم
if os.path.exists(filters_path):
    with open(filters_path, "r", encoding="utf-8") as f:
        content = f.read()
else:
    content = ""

# اگر کلاس Filters در آن تعریف نشده باشد، آن را اضافه می‌کنیم
if "class Filters" not in content:
    print("➕ اضافه کردن کلاس Filters به navix/filters.py")
    patch = '''

class Filters:
    """Filter collection container"""
    @staticmethod
    def text(msg):
        return True
    @staticmethod
    def command(cmd):
        return True
'''
    with open(filters_path, "a", encoding="utf-8") as f:
        f.write(patch)
else:
    print("✅ کلاس Filters از قبل در فایل موجود است.")

