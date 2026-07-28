import asyncio
import inspect
from typing import Any, Dict, List
from .types import Message

class MockClient:
    """Enterprise Mock Client for high-performance unit testing without Rubika network."""
    def __init__(self):
        self.sent_messages: List[Dict[str, Any]] = []
        self.answered_callbacks: List[Dict[str, Any]] = []

    async def send_message(self, chat_id: str, text: str, **kwargs: Any) -> dict:
        msg = {"chat_id": chat_id, "text": text, **kwargs}
        self.sent_messages.append(msg)
        return {"result": {"message_id": 9999, **msg}}

    async def answer_callback_query(self, callback_query_id: str, text: str = "", show_alert: bool = False) -> dict:
        cb = {"callback_query_id": callback_query_id, "text": text, "show_alert": show_alert}
        self.answered_callbacks.append(cb)
        return {"result": True}

    async def feed_message(self, router: Any, text: str, chat_id: str = "123", sender_id: str = "456") -> None:
        data = {"message_id": 1, "chat_id": chat_id, "sender_id": sender_id, "text": text}
        msg = Message(data, client=self)
        for filters, handler in router.message_handlers:
            passed = True
            for f in filters:
                if callable(f):
                    try:
                        if inspect.iscoroutinefunction(f) or hasattr(f, "__call__") and inspect.iscoroutinefunction(f.__call__):
                            res = await f(msg)
                        else:
                            res = f(msg)
                        if not res:
                            passed = False
                            break
                    except Exception:
                        passed = False
                        break
            if passed:
                if inspect.iscoroutinefunction(handler):
                    await handler(msg)
                else:
                    handler(msg)
                break
