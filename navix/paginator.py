"""
Inline Keyboard Paginator for Navix
"""
from typing import List, Dict, Any

class Paginator:
    """
    ابزار خودکار ساخت دکمه‌های صفحه‌بندی برای لیست‌های طولانی
    """
    def __init__(self, items: List[Any], per_page: int = 5):
        self.items = items
        self.per_page = per_page
        self.total_pages = max(1, (len(items) + per_page - 1) // per_page)

    def get_page(self, page: int) -> List[Any]:
        """
        دریافت آیتم‌های یک صفحه مشخص
        """
        page = max(1, min(page, self.total_pages))
        start = (page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]

    def generate_keyboard(self, page: int, callback_prefix: str) -> List[Dict[str, Any]]:
        """
        تولید سطر دکمه‌های ناوبری (صفحه قبل، شماره صفحه، صفحه بعد)
        """
        page = max(1, min(page, self.total_pages))
        nav_row = []

        if page > 1:
            nav_row.append({"text": "⬅️ قبلی", "callback_data": f"{callback_prefix}:{page - 1}"})
        
        nav_row.append({"text": f"📄 {page} / {self.total_pages}", "callback_data": "ignore"})

        if page < self.total_pages:
            nav_row.append({"text": "بعدی ➡️", "callback_data": f"{callback_prefix}:{page + 1}"})

        return nav_row
