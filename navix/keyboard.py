"""
Keyboard Builder for Navix (Inline and Reply Keyboards)
"""
from typing import List, Dict, Any

class InlineKeyboardBuilder:
    """
    سازنده پیشرفته دکمه‌های شیشه‌ای (Inline Keyboards)
    """
    def __init__(self):
        self.rows: List[List[Dict[str, Any]]] = []
        self.current_row: List[Dict[str, Any]] = []

    def add(self, text: str, callback_data: str = None, url: str = None):
        button = {"text": text}
        if callback_data:
            button["callback_data"] = callback_data
        if url:
            button["url"] = url
        self.current_row.append(button)
        return self

    def row(self):
        if self.current_row:
            self.rows.append(self.current_row)
            self.current_row = []
        return self

    def adjust(self, *sizes: int):
        # تنظیم تعداد دکمه‌ها در هر سطر
        flat_buttons = [btn for row in self.rows for btn in row] + self.current_row
        self.rows = []
        self.current_row = []

        index = 0
        for size in sizes:
            row = flat_buttons[index:index + size]
            if row:
                self.rows.append(row)
            index += size
        if index < len(flat_buttons):
            self.rows.append(flat_buttons[index:])
        return self

    def as_markup(self) -> Dict[str, Any]:
        if self.current_row:
            self.row()
        return {"inline_keyboard": self.rows}
