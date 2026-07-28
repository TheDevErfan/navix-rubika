"""
Dispatcher and Long Polling System for Navix with Middleware Support
"""
import asyncio
from .log import logger
from .router import Router
from .types import Message
from .middleware import MiddlewareManager

class Dispatcher:
    """
    مدیریت‌کننده آپدیت‌ها، سیستم Long Polling و میدلورها
    """
    def __init__(self, client, router: Router):
        self.client = client
        self.router = router
        self.middleware = MiddlewareManager()
        self.is_running = False
        logger.debug("دیسپچر مجهز به میدلور مقداردهی اولیه شد.")

    async def start_polling(self, interval: float = 1.0):
        """
        شروع حلقه مداوم دریافت پیام‌ها از سرور روبیکا
        """
        self.is_running = True
        logger.info("سیستم Long Polling با موفقیت روشن شد...")
        
        offset = None
        while self.is_running:
            try:
                payload = {"offset": offset} if offset else {}
                response = await self.client.request("getUpdates", payload)
                
                if response and isinstance(response, dict):
                    updates = response.get("result", [])
                    for update in updates:
                        update_id = update.get("update_id")
                        if update_id:
                            offset = int(update_id) + 1
                            
                        # پردازش آپدیت از طریق میدلورها و روتر
                        await self._process_update(update)
                        
            except asyncio.CancelledError:
                logger.info("سیستم پولینگ متوقف شد.")
                break
            except Exception as e:
                logger.error(f"خطا در حلقه Long Polling: {e}", exc_info=True)
            
            await asyncio.sleep(interval)

    async def _process_update(self, update: dict):
        """
        عبور دادن آپدیت از میدلورها و سپس ارسال به هندلرهای روتر
        """
        msg = Message(update, client=self.client)
        
        # اجرای هندلرهای روتر به همراه رد شدن از فیلتر میدلورها
        for handler, filters in self.router.message_handlers:
            async def target_wrapper(m):
                if asyncio.iscoroutinefunction(handler):
                    await handler(m)
                else:
                    handler(m)
            
            # اجرای زنجیره میدلور برای هر هندلر
            await self.middleware.dispatch(msg, target_wrapper)

    def stop_polling(self):
        self.is_running = False
        logger.info("درخواست توقف پولینگ صادر شد.")
