"""
Webhook Server for Navix
"""
from aiohttp import web
from .log import logger

class WebhookServer:
    """
    سرور وب‌هوک بر پایه aiohttp برای دریافت آپدیت‌ها به صورت آنی
    """
    def __init__(self, router, dispatcher, host: str = "0.0.0.0", port: int = 8080, path: str = "/webhook"):
        self.router = router
        self.dispatcher = dispatcher
        self.host = host
        self.port = port
        self.path = path
        self.app = web.Application()
        self.app.router.add_post(self.path, self._handle_webhook)
        logger.debug("سرور وب‌هوک (WebhookServer) راه‌اندازی شد.")

    async def _handle_webhook(self, request: web.Request):
        try:
            data = await request.json()
            logger.debug(f"دریافت پکت وب‌هوک: {data}")
            await self.dispatcher._process_update(data)
            return web.json_response({"status": "ok"})
        except Exception as e:
            logger.error(f"خطا در پردازش وب‌هوک: {e}", exc_info=True)
            return web.json_response({"status": "error", "message": str(e)}, status=500)

    def run(self):
        logger.info(f"راه‌اندازی سرور وب‌هوک روی {self.host}:{self.port}{self.path}")
        web.run_app(self.app, host=self.host, port=self.port)
