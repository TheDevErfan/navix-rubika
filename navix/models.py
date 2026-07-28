from __future__ import annotations
from typing import Optional, Dict, Any, List

class Button:
    def __init__(self, text: str, button_id: Optional[str] = None, type: str = "Simple"):
        self.text = text
        self.button_id = button_id
        self.type = type

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "button_id": self.button_id, "type": self.type}

class Keypad:
    def __init__(self):
        self.rows: List[List[Button]] = []

    def add_row(self, *buttons: Button) -> Keypad:
        self.rows.append(list(buttons))
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {"rows": [[btn.to_dict() for btn in row] for row in self.rows]}

class Message:
    def __init__(self, text: Optional[str] = None, sender_id: Optional[str] = None, chat_id: Optional[str | int] = None, client: Optional[Any] = None):
        self.text = text
        self.sender_id = sender_id
        self.chat_id = chat_id
        self._client = client

    async def reply(self, text: str, **kwargs: Any) -> Any:
        if not self._client or not self.chat_id:
            raise RuntimeError("Client or chat_id is not bound.")
        return await self._client.send_message(chat_id=self.chat_id, text=text, **kwargs)

class CallbackQuery:
    def __init__(self, button_id: str, chat_id: str | int, sender_id: Optional[str] = None, client: Optional[Any] = None):
        self.button_id = button_id
        self.chat_id = chat_id
        self.sender_id = sender_id
        self._client = client

    async def answer(self, text: Optional[str] = None, **kwargs: Any) -> Any:
        if not self._client:
            raise RuntimeError("Client is not bound.")
        return await self._client.answer_callback_query(chat_id=self.chat_id, button_id=self.button_id, text=text, **kwargs)

class Update:
    def __init__(self, new_message: Optional[Message] = None, callback_query: Optional[CallbackQuery] = None):
        self.new_message = new_message
        self.callback_query = callback_query
