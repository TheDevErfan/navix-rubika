"""
Diagnostic and Doctor Tool for Navix Framework
"""
import sys
import platform
import aiohttp
from .log import logger

async def run_doctor(token: str = None):
    """
    بررسی سلامت محیط، نسخه‌ها، پکیج‌ها و اتصال به سرور
    """
    print("=" * 50)
    print("🔍 در حال اجرای ابزار عیب‌یاب Navix Doctor...")
    print("=" * 50)
    
    # ۱. بررسی نسخه پایتون
    py_version = platform.python_version()
    print(f"• نسخه پایتون: {py_version}")
    if sys.version_info < (3, 8):
        print("  ⚠️ هشدار: نسخه پایتون پایین‌تر از 3.8 است و ممکن است با برخی قابلیت‌ها مشکل داشته باشد.")
    else:
        print("  ✅ نسخه پایتون استاندارد و تایید شده است.")

    # ۲. بررسی کتابخانه‌های حیاتی
    try:
        import aiohttp
        print(f"• پکیج aiohttp: نصب شده (نسخه {aiohttp.__version__})")
    except ImportError:
        print("  ❌ خطا: پکیج aiohttp نصب نشده است! دستور `pip install aiohttp` را بزنید.")

    # ۳. بررسی توکن در صورت وجود
    if token:
        if len(token) < 10:
            print("  ⚠️ هشدار: طول توکن به نظر کوتاه می‌آید یا نامعتبر است.")
        else:
            print(f"• بررسی توکن: توکن دریافت شد (طول: {len(token)} کاراکتر).")
            
            # تست اتصال واقعی به سرور روبیکا
            print("• در حال تست اتصال به سرورهای روبیکا...")
            try:
                async with aiohttp.ClientSession() as session:
                    url = f"https://api.rubika.ir/v3/{token}/getMe"
                    async with session.get(url, timeout=10) as resp:
                        if resp.status == 200:
                            print("  ✅ اتصال به سرور موفقیت‌آمیز بود و پاسخ دریافت شد!")
                        else:
                            print(f"  ⚠️ سرور پاسخ داد اما با کد وضعیت: {resp.status} (ممکن است توکن نامعتبر باشد)")
            except Exception as e:
                print(f"  ❌ خطا در اتصال به سرور روبیکا: {e}")
    else:
        print("• بررسی توکن: توکنی برای تست ارسال نشده است.")

    print("=" * 50)
    print("✨ عیب‌یابی به پایان رسید.")
    print("=" * 50)
