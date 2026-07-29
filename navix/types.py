"""
Data Types and Models for Navix Framework
"""
from typing import Dict, Any, Optional

class User:
    """مدل اطلاعات کاربر در روبیکا"""
    def __init__(self, data: Dict[str, Any]):
        self.id: str = data.get("user_id", "")
        self.first_name: Optional[str] = data.get("first_name")
        self.last_name: Optional[str] = data.get("last_name")
        self.username: Optional[str] = data.get("username")

class Message:
    """مدل ساختاریافته پیام دریافتی"""
    def __init__(self, data: Dict[str, Any]):
        self.raw: Dict[str, Any] = data
        self.message_id: str = data.get("message_id", "")
        self.chat_id: str = data.get("chat_id", "")
        self.text: str = data.get("text", "")
        self.sender_id: str = data.get("sender_id", "")
        self.author_type: str = data.get("author_type", "User")
        
    @property
    def is_text(self) -> bool:
        return bool(self.text)
