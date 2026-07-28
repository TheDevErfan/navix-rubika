"""
Navix Core Client with Advanced Error Handling and Logging
"""
import aiohttp
from .log import logger
from .exceptions import NetworkError, AuthError, ValidationError, NavixError

class Client:
    """
    کلاینت اصلی برای ارتباط با API روبیکا همراه با سیستم دیباگ و مدیریت خطای پیشرفته
    """
    def __init__(self, token: str, api_url: str = "https://api.rubika.ir/v3/"):
        self.token = token
        self.api_url = api_url
        if not token:
            logger.error("توکن ربات مقدار خالی دارد!")
            raise AuthError("توکن معتبر برای اتصال به روبیکا ارائه نشده است.")
        logger.info("کلاینت Navix با موفقیت مقداردهی اولیه شد.")

    async def request(self, method_name: str, payload: dict = None):
        """
        ارسال درخواست به سرور با مکانیزم کامل دیباگ، لاگ و مدیریت خطا
        """
        url = f"{self.api_url}{self.token}/{method_name}"
        logger.debug(f"در حال ارسال درخواست به متد: {method_name} | آدرس: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload or {}, timeout=30) as response:
                    logger.debug(f"وضعیت پاسخ سرور برای {method_name}: کد {response.status}")
                    
                    if response.status == 401 or response.status == 403:
                        logger.error(f"خطای احراز هویت (تتوکن نامعتبر): {response.status}")
                        raise AuthError("توکن ربات نامعتبر است یا دسترسی غیرمجاز صورت گرفته است.")
                    
                    if response.status >= 500:
                        logger.error(f"خطای سرور روبیکا: کد {response.status}")
                        raise NetworkError(f"سرورهای روبیکا با خطا مواجه شدند. کد وضعیت: {response.status}")
                        
                    data = await response.json()
                    return data
                    
        except aiohttp.ClientError as e:
            logger.error(f"خطای شبکه در ارتباط با روبیکا: {e}")
            raise NetworkError(f"خطا در برقراری ارتباط با اینترنت یا سرور: {e}") from e
        except Exception as e:
            if isinstance(e, NavixError):
                raise e
            logger.critical(f"خطای ناشناخته و بحرانی در متد {method_name}: {e}", exc_info=True)
            raise NavixError(f"یک خطای پیش‌بینی نشده رخ داد: {e}") from e
