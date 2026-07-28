"""
Rate Limiting and Throttling System for Navix
"""
import time
from typing import Dict
from .log import logger

class Throttler:
    """
    سیستم کنترل سرعت و جلوگیری از اسپم کاربران (Rate Limiting)
    """
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.users_last_time: Dict[str, float] = {}
        logger.debug(f"سیستم ضد اسپم (Throttler) با محدودیت {rate_limit} ثانیه راه‌اندازی شد.")

    def is_throttled(self, user_id: str) -> bool:
        current_time = time.time()
        last_time = self.users_last_time.get(user_id, 0.0)
        
        if current_time - last_time < self.rate_limit:
            logger.debug(f"کاربر {user_id} تحت محدودیت اسپم قرار گرفت.")
            return True
        
        self.users_last_time[user_id] = current_time
        return False
