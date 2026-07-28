"""
Object-oriented types and models for Navix
"""
from typing import Optional, Dict, Any
from .log import logger

class Message:
    """
    مدل شیءگرا برای مدیریت پیام‌های دریافتی
    """
    def __init__(self, data: Dict[str, Any], client=None):
        self.raw: Dict[str, Any] = data
        self.client = client
        
        # استخراج فیلدهای اصلی پیام (با توجه به ساختار روبیکا)
        self.text: Optional[str] = data.get("text")
        self.sender_id: Optional[str] = data.get("sender_id") or data.get("author_id")
        self.chat_id: Optional[str] = data.get("chat_id") or data.get("object_guid")
        self.message_id: Optional[str] = data.get("message_id")

    async def reply(self, text: str, **kwargs):
        """
        ارسال پاسخ مستقیم به همین پیام
        """
        if not self.client:
            logger.error("کلاینت به پیام متصل نیست، امکان ارسال پاسخ وجود ندارد.")
            return None
        
        # ارسال پیام از طریق کلاینت
        return await self.client.request("sendMessage", {
            "chat_id": self.chat_id,
            "text": text,
            "reply_to_message_id": self.message_id,
            **kwargs
        })

    def __repr__(self) -> str:
        return f"<Message id={self.message_id} text='{self.text}'>"
