import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional
from aiohttp import web
from .session import AiohttpSession
from .router import Router
from .types import Message, CallbackQuery
from .fsm import MemoryStorage

logger = logging.getLogger("navix")

class Client(Router):
    def __init__(self, token: str, api_url: str = "https://bot.rubika.ir/v0"):
        super().__init__()
        self.token = token
        self.api_url = f"{api_url}/{token}"
        self.session = AiohttpSession()
        self.storage = MemoryStorage()
        self._startup_handlers: List[Callable] = []
        self._shutdown_handlers: List[Callable] = []
        self._error_handler: Optional[Callable] = None

    def on_startup(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._startup_handlers.append(func)
            return func
        return decorator

    def on_shutdown(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._shutdown_handlers.append(func)
            return func
        return decorator

    def error_handler(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._error_handler = func
            return func
        return decorator

    async def send_message(self, chat_id: str, text: str, **kwargs: Any) -> Any:
        url = f"{self.api_url}/sendMessage"
        payload = {"chat_id": chat_id, "text": text, **kwargs}
        return await self.session.request("POST", url, json=payload)

    async def _execute_with_middlewares(self, handler: Callable, event: Any, middlewares: List[Any]) -> None:
        async def make_call(ev: Any, dt: dict) -> Any:
            if inspect.iscoroutinefunction(handler):
                return await handler(ev)
            return handler(ev)

        chain = make_call
        for mw in reversed(middlewares):
            current_mw = mw
            next_handler = chain
            async def bound_mw(ev: Any, dt: dict, m=current_mw, n=next_handler) -> Any:
                return await m(n, ev, dt)
            chain = bound_mw

        try:
            await chain(event, {})
        except Exception as e:
            logger.error(f"Execution error in handler: {e}", exc_info=True)
            if self._error_handler:
                try:
                    if inspect.iscoroutinefunction(self._error_handler):
                        await self._error_handler(event, e)
                    else:
                        self._error_handler(event, e)
                except Exception as err:
                    logger.error(f"Global error handler failed: {err}", exc_info=True)

    async def _dispatch_message(self, msg: Message, router: Router, all_middlewares: List[Any]) -> bool:
        combined_middlewares = all_middlewares + router.middlewares
        for filters, handler in router.message_handlers:
            passed = True
            for f in filters:
                if callable(f):
                    try:
                        if inspect.iscoroutinefunction(f) or (hasattr(f, "__call__") and inspect.iscoroutinefunction(f.__call__)):
                            res = await f(msg)
                        else:
                            res = f(msg)
                        if not res:
                            passed = False
                            break
                    except Exception as fe:
                        logger.error(f"Filter evaluation error: {fe}")
                        passed = False
                        break
            if passed:
                asyncio.create_task(self._execute_with_middlewares(handler, msg, combined_middlewares))
                return True

        for sub in router.sub_routers:
            if await self._dispatch_message(msg, sub, combined_middlewares):
                return True
        return False

    async def start_polling(self) -> None:
        for startup_func in self._startup_handlers:
            if inspect.iscoroutinefunction(startup_func):
                await startup_func()
            else:
                startup_func()

        logger.info("Ultimate Navix Bot polling loop connected to Rubika successfully...")
        offset = 0
        try:
            while True:
                try:
                    url = f"{self.api_url}/getUpdates?offset={offset}"
                    data = await self.session.request("GET", url)
                    if isinstance(data, dict) and "result" in data:
                        for update in data["result"]:
                            if "update_id" in update:
                                offset = update["update_id"] + 1
                            if "message" in update:
                                msg = Message(update["message"], client=self)
                                await self._dispatch_message(msg, self, self.middlewares)
                    await asyncio.sleep(0.3)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.warning(f"Rubika polling warning: {e}. Reconnecting in 2s...")
                    await asyncio.sleep(2)
        finally:
            for shutdown_func in self._shutdown_handlers:
                if inspect.iscoroutinefunction(shutdown_func):
                    await shutdown_func()
                else:
                    shutdown_func()
            await self.session.close()

    def run(self) -> None:
        try:
            asyncio.run(self.start_polling())
        except KeyboardInterrupt:
            logger.info("Bot stopped.")
