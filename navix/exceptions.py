"""
Navix Exception Hierarchy for Advanced Error Handling & Debugging
"""

class NavixError(Exception):
    """خطای پایه برای تمام خطاهای کتابخانه Navix"""
    pass

class NetworkError(NavixError):
    """خطای مربوط به شبکه، قطع اینترنت یا عدم پاسخگویی سرورهای روبیکا"""
    pass

class ValidationError(NavixError):
    """خطای نامعتبر بودن داده‌ها، پارامترها یا ساختار پیام ورودی"""
    pass

class AuthError(NavixError):
    """خطای مربوط به توکن نامعتبر، دسترسی غیرمجاز یا احراز هویت"""
    pass

class FSMError(NavixError):
    """خطاهای مربوط به ماشین حالت (مدیریت مراحل ربات و استیت‌ها)"""
    pass
