"""
Diagnostic and Doctor Tool for Navix Framework
"""
import sys
import platform
import aiohttp
from .log import logger

async def run_doctor(token: str = None):
    """
    بررسی سلامت محیط، نسخه‌ها، پکیج‌ها و اتصال به سرور با ظاهر مدرن
    """
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;32m 🩺 Navix Framework Professional Doctor & Diagnostics \033[0m")
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    
    # ۱. بررسی نسخه پایتون
    py_version = platform.python_version()
    print(f"\033[1;33m• نسخه پایتون:\033[0m {py_version}")
    if sys.version_info < (3, 8):
        print("  \033[1;31m⚠️ هشدار: نسخه پایتون پایین‌تر از 3.8 است.\033[0m")
    else:
        print("  \033[1;32m✅ نسخه پایتون استاندارد و تایید شده است.\033[0m")

    # ۲. بررسی کتابخانه‌های حیاتی
    try:
        import aiohttp
        print(f"\033[1;33m• پکیج aiohttp:\033[0m \033[1;32mنصب شده (نسخه {aiohttp.__version__})\033[0m")
    except ImportError:
        print("  \033[1;31m❌ خطا: پکیج aiohttp نصب نشده است! دستور `pip install aiohttp` را بزنید.\033[0m")

    # ۳. بررسی توکن در صورت وجود
    if token:
        if len(token) < 10:
            print("  \033[1;31m⚠️ هشدار: طول توکن به نظر کوتاه می‌آید یا نامعتبر است.\033[0m")
        else:
            print(f"\033[1;33m• بررسی توکن:\033[0m دریافت شد (طول: {len(token)} کاراکتر).")

            print("\033[1;33m• در حال تست اتصال به سرورهای روبیکا...\033[0m")
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"https://api.rubika.ir/v3/{token}/getMe"
                    async with session.get(url, timeout=10) as resp:
                        if resp.status == 200:
                            print("  \033[1;32m✅ اتصال به سرور موفقیت‌آمیز بود و پاسخ دریافت شد!\033[0m")
                        else:
                            print(f"  \033[1;33m⚠️ سرور پاسخ داد با کد وضعیت: {resp.status}\033[0m")
            except Exception as e:
                print(f"  \033[1;31m❌ خطا در اتصال به سرور روبیکا: {e}\033[0m")
    else:
        print("\033[1;33m• بررسی توکن:\033[0m توکنی برای تست ارسال نشده است.")

    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;32m ✨ عیب‌یابی با موفقیت به پایان رسید! \033[0m")
    print("\033[1;36m" + "=" * 60 + "\033[0m")
