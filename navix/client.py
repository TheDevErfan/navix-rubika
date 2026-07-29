"""Navix Rubika Framework - Main Client."""

import logging
from typing import Optional, Dict, Any
from .api import API
from .dispatcher import Dispatcher
from .router import Router

logger = logging.getLogger("navix")

class NavixBot:
    """Main bot client for interacting with Rubika."""
    
    def __init__(self, token: str, session: Any = None, **kwargs: Any):
        if not token:
            raise ValueError("A valid bot token must be provided.")
            
        self.token: str = token
        self.options: Dict[Any, Any] = kwargs
        self.session = session

        # راه‌اندازی بخش ارتباط با API و سیستم رویدادها
        self.api = API(session=self.session, token=self.token, **self.options)
        self.router = Router()
        self.dispatcher = Dispatcher(client=self, router=self.router)
        self.is_running: bool = False

    async def request(self, method_name: str, data: Optional[Dict[str, Any]] = None) -> Any:
        """ارسال درخواست به API روبیکا"""
        return await self.api.call(method_name, data)

    async def start(self) -> None:
        """Start the bot polling loop."""
        logger.info("Starting Navix bot...")
        self.is_running = True
        try:
            await self.dispatcher.start_polling()
        except Exception as e:
            logger.error(f"Error in bot execution: {e}")
            raise
        finally:
            await self.stop()

    async def stop(self) -> None:
        """Stop the bot gracefully."""
        self.is_running = False
        self.dispatcher.stop_polling()
        logger.info("Navix bot stopped.")
