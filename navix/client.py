"""
Advanced HTTP Client for Navix Framework with Session Pooling & Auto-Retry
"""
import aiohttp
import asyncio
from typing import Optional, Dict, Any
from .exceptions import NavixAPIError, NetworkError, TokenError
from .log import logger

class Bot:
    """کلاینت اصلی و پیشرفته ارتباط با ربات روبیکا"""
    def __init__(self, token: str, base_url: str = "https://api.rubika.ir/v3"):
        if not token or len(token) < 10:
            raise TokenError("توکن ربات نامعتبر یا خالی است.")
        self.token = token
        self.base_url = f"{base_url}/{token}"
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def initialize(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={"User-Agent": "Navix-Framework/1.1.0"},
                timeout=aiohttp.ClientTimeout(total=30)
            )
            logger.debug("نشست ناهمگام HTTP (ClientSession) ایجاد شد.")

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
            logger.debug("نشست ناهمگام HTTP بسته شد.")

    async def request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, retries: int = 3) -> Dict[str, Any]:
        """ارسال درخواست ناهمگام به سرور روبیکا همراه با مکانیزم Retry خودکار"""
        await self.initialize()
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        last_exception = None
        for attempt in range(retries):
            try:
                async with self.session.request(method, url, json=data) as response:
                    if response.status != 200:
                        raise NavixAPIError(f"خطای سرور روبیکا با کد وضعیت: {response.status}")
                    
                    result = await response.json()
                    return result
            except aiohttp.ClientError as e:
                last_exception = NetworkError(f"خطای شبکه در ارتباط با سرور: {e}")
                logger.warning(f"تلاش {attempt + 1} برای ارسال درخواست ناموفق بود. خطا: {e}")
                await asyncio.sleep(1.0 * (attempt + 1))
            except Exception as e:
                raise NavixAPIError(f"خطای ناشناخته در ارسال درخواست: {e}")
        
        raise last_exception or NetworkError("تعداد تلاش‌های ناموفق به پایان رسید.")

    async def send_message(self, chat_id: str, text: str, reply_to_message_id: Optional[str] = None, keyboard: Optional[list] = None) -> Dict[str, Any]:
        """ارسال پیام متنی به کاربر یا گروه در روبیکا"""
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "text": text
        }
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        if keyboard:
            payload["keyboard"] = keyboard

        return await self.request("POST", "sendMessage", data=payload)
