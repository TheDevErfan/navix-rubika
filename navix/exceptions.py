"""
Comprehensive Exception Hierarchy for Navix Framework
"""

class NavixError(Exception):
    """پایه تمام خطاهای فریمورک Navix"""
    pass

class TokenError(NavixError):
    """خطای مربوط به توکن نامعتبر یا خالی"""
    pass

class NavixAPIError(NavixError):
    """خطاهای برگشتی از سمت سرور یا API روبیکا"""
    pass

class NetworkError(NavixError):
    """خطاهای مربوط به قطع شبکه، تایم‌اوت یا ارتباط با سرور"""
    pass

class FSMError(NavixError):
    """خطاهای مربوط به مدیریت حالت‌ها (Finite State Machine)"""
    pass
