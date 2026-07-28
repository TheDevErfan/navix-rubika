"""
Broadcast System for Navix Bots
"""
import asyncio
from typing import List
from .log import logger

class Broadcaster:
    """
    سیستم مدیریت و ارسال پیام همگانی (Broadcast) به صورت ناهمزمان
    """
    def __init__(self, client):
        self.client = client
        logger.debug("سیستم ارسال پیام همگانی (Broadcaster) راه‌اندازی شد.")

    async def broadcast(self, user_ids: List[str], text: str, delay: float = 0.1, **kwargs) -> dict:
        success_count = 0
        fail_count = 0
        blocked_count = 0

        for user_id in user_ids:
            try:
                await self.client.request("sendMessage", {
                    "chat_id": user_id,
                    "text": text,
                    **kwargs
                })
                success_count += 1
            except Exception as e:
                err_str = str(e).lower()
                if "blocked" in err_str or "forbidden" in err_str or "403" in err_str:
                    blocked_count += 1
                else:
                    fail_count += 1
                logger.debug(f"ارسال پیام به کاربر {user_id} ناموفق بود: {e}")
            
            if delay > 0:
                await asyncio.sleep(delay)

        logger.info(f"عملیات ارسال همگانی به پایان رسید. موفق: {success_count} | مسدودشده: {blocked_count} | ناموفق: {fail_count}")
        return {
            "success": success_count,
            "blocked": blocked_count,
            "failed": fail_count,
            "total": len(user_ids)
        }
