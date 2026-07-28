from typing import Any, Dict, Optional

class User:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("user_id") or data.get("id")
        self.first_name = data.get("first_name")
        self.last_name = data.get("last_name")
        self.username = data.get("username")

class Chat:
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("chat_id") or data.get("id")
        self.type = data.get("type")
        self.title = data.get("title")

class Message:
    def __init__(self, data: Dict[str, Any], client: Optional[Any] = None):
        self._data = data
        self.client = client
        self.message_id = data.get("message_id") or data.get("id")
        self.chat_id = data.get("chat_id") or (data.get("chat", {}) if isinstance(data.get("chat"), dict) else {}).get("chat_id")
        self.sender_id = data.get("sender_id") or data.get("from_id")
        self.text = data.get("text") or data.get("caption")
        self.chat = Chat(data.get("chat", {})) if isinstance(data.get("chat"), dict) else None
        self.from_user = User(data.get("from", {})) if isinstance(data.get("from"), dict) else None

    async def reply(self, text: str, **kwargs: Any) -> Any:
        if not self.client:
            raise RuntimeError("Client is not bound to this Message object.")
        target_chat_id = self.chat_id or (self.chat.id if self.chat else None)
        if not target_chat_id:
            raise ValueError("Cannot reply: chat_id is missing.")
        return await self.client.send_message(chat_id=target_chat_id, text=text, **kwargs)

    async def edit(self, text: str, **kwargs: Any) -> Any:
        if not self.client:
            raise RuntimeError("Client is not bound to this Message object.")
        target_chat_id = self.chat_id or (self.chat.id if self.chat else None)
        if not target_chat_id or not self.message_id:
            raise ValueError("Cannot edit: chat_id or message_id is missing.")
        return await self.client.edit_message_text(chat_id=target_chat_id, message_id=str(self.message_id), text=text, **kwargs)

    async def delete(self) -> Any:
        if not self.client:
            raise RuntimeError("Client is not bound to this Message object.")
        target_chat_id = self.chat_id or (self.chat.id if self.chat else None)
        if not target_chat_id or not self.message_id:
            raise ValueError("Cannot delete: chat_id or message_id is missing.")
        return await self.client.delete_message(chat_id=target_chat_id, message_id=str(self.message_id))

class CallbackQuery:
    def __init__(self, data: Dict[str, Any], client: Optional[Any] = None):
        self._data = data
        self.client = client
        self.id = data.get("callback_query_id") or data.get("id")
        self.sender_id = data.get("sender_id") or data.get("from_id")
        self.data = data.get("data")
        self.message = Message(data.get("message", {}), client=client) if isinstance(data.get("message"), dict) else None

    async def answer(self, text: str = "", show_alert: bool = False) -> Any:
        if not self.client:
            raise RuntimeError("Client is not bound to this CallbackQuery object.")
        return await self.client.answer_callback_query(callback_query_id=str(self.id), text=text, show_alert=show_alert)
